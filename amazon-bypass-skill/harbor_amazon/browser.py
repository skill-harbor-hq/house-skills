"""Moteur navigateur pour Harbor Amazon : un vrai Chromium pilote par
Playwright.

La v1 parlait a Amazon en HTTP direct (curl_cffi, fingerprint TLS
Chrome) et se faisait servir un HTTP 503. La v2 charge les pages dans
un vrai navigateur, rendu JavaScript compris : c'est beaucoup plus dur
a detecter comme robot, au prix de requetes plus lentes (quelques
secondes par page).

Regles de ce module :
- Un seul navigateur, un seul contexte, une seule page, reutilises.
  La navigation est stateful, donc une seule navigation a la fois :
  tout passe par un verrou reentrant (``engine.lock``).
- Aucun checkout, aucun paiement, aucun login automatise, aucune
  resolution de captcha. Si Amazon bloque, on le detecte et on le dit,
  on ne le contourne pas.
- Les mesures anti-detection ci-dessous reduisent le risque d'etre
  signale comme robot. Aucune ne garantit quoi que ce soit, et le
  code ne pretend jamais le contraire.
"""

from __future__ import annotations

import asyncio
import platform
from dataclasses import dataclass


# Arguments de lancement Chromium. Chacun est documente, aucun n'est
# magique :
# - --disable-blink-features=AutomationControlled : retire le drapeau
#   Blink qui expose l'automatisation (navigator.webdriver devient
#   False au lieu de True). Mesure standard, pas une garantie.
# - --disable-dev-shm-usage : evite de remplir /dev/shm, petit sur
#   certaines machines. Sans effet sur la detection.
# - --no-first-run : saute l'ecran de premier lancement.
# - --disable-extensions : pas d'extension, un navigateur propre.
LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--no-first-run",
    "--disable-extensions",
]

# Script injecte dans chaque page avant tout autre script. Il masque
# la propriete navigator.webdriver, au cas ou le drapeau Blink
# ci-dessus ne suffirait pas. C'est une mesure de discretion, pas
# une garantie d'invisibilite.
INIT_SCRIPT = "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"

# Delais en millisecondes. Une page Amazon met quelques secondes a
# charger dans un vrai navigateur ; 30 s laisse de la marge sans
# attendre indefiniment. L'attente du selecteur est de 30 s parce
# que la page produit met parfois plus de 10 s a rendre son detail
# (verifie 2026-11-05 : #productTitle absent a 10 s, present apres
# une attente longue, avec le formulaire d'ajout et le prix).
GOTO_TIMEOUT_MS = 30000
SELECTOR_TIMEOUT_MS = 30000
CLICK_TIMEOUT_MS = 10000

# Selecteurs de la feuille "Added to Cart" d'Amazon, attendus apres
# un clic sur le bouton d'ajout. Si aucun n'apparait, on continue
# quand meme : la relecture du panier reste la verite de reference.
ADD_CONFIRM_SELECTORS = (
    "#attachDisplayAddToCart",
    "#huc-v2-order-row-confirm-text",
    "#sw-atc-details-single-container",
)


class BrowserStartError(Exception):
    """Le navigateur n'a pas pu demarrer (playwright absent, Chromium
    absent, lancement refuse). Erreur de configuration, pas un
    blocage Amazon : l'API la traduit en 500, jamais en 503."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class BrowserFetchError(Exception):
    """La navigation a echoue au niveau reseau (timeout, connexion
    coupee). Erreur reseau, traduite en 502 par l'API."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class FormNotFound(Exception):
    """Le formulaire attendu est absent de la page chargee."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass
class FetchResult:
    """Ce qu'une navigation a rapporte."""

    status: int | None  # Code HTTP de la reponse, None si inconnu
    html: str           # Contenu HTML complet de la page
    title: str          # Titre de la page


class _ReentrantLock:
    """Verrou asyncio reentrant : la meme tache peut le reprendre
    plusieurs fois (ex. ajout au panier qui relit le panier), sans
    interblocage. Une autre tache attend son tour."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._owner = None
        self._count = 0

    async def __aenter__(self):
        task = asyncio.current_task()
        if self._owner is task:
            self._count += 1
            return self
        await self._lock.acquire()
        self._owner = task
        self._count = 1
        return self

    async def __aexit__(self, *exc):
        self._count -= 1
        if self._count == 0:
            self._owner = None
            self._lock.release()
        return False


def _user_agent(chromium_version: str) -> str:
    """Un user-agent de vrai Chrome, construit avec la version du
    Chromium qui tourne vraiment, pour que l'agent corresponde au
    binaire. Sans ca, Playwright laisse "HeadlessChrome" dans
    l'agent, ce qui signale un navigateur sans tete au premier
    regard. La plateforme (Windows, Linux, Mac) suit la machine
    qui fait tourner le navigateur, pour rester coherente avec
    navigator.platform."""
    system = platform.system()
    if system == "Windows":
        os_part = "Windows NT 10.0; Win64; x64"
    elif system == "Darwin":
        os_part = "Macintosh; Intel Mac OS X 10_15_7"
    else:
        os_part = "X11; Linux x86_64"
    return (
        f"Mozilla/5.0 ({os_part}) AppleWebKit/537.36 "
        f"(KHTML, like Gecko) Chrome/{chromium_version} Safari/537.36"
    )


class BrowserEngine:
    """Un navigateur Chromium partage, pilote par Playwright en mode
    async. Toutes les methodes supposent que l'appelant detient
    ``engine.lock`` : elles ne le prennent jamais elles-memes, pour
    qu'un flux en plusieurs etapes (aller sur la page produit, puis
    cliquer sur ajouter) reste atomique."""

    def __init__(self) -> None:
        self.lock = _ReentrantLock()
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        self._started = False
        # Vrai quand le contexte porte les cookies d'un jar (appel
        # authentifie) : un appel anonyme suivant doit les effacer.
        self._session_cookies_active = False

    @property
    def started(self) -> bool:
        return self._started

    async def start(self) -> None:
        """Demarre Chromium si ce n'est pas deja fait. Leve
        BrowserStartError avec une raison claire si playwright ou
        Chromium manque."""
        if self._started:
            return
        try:
            from playwright.async_api import async_playwright
        except ImportError as exc:
            raise BrowserStartError(
                "playwright is not installed, run install.ps1"
            ) from exc
        try:
            self._playwright = await async_playwright().start()
            # channel="chromium" : Playwright utilise sinon le
            # "headless shell" en mode sans tete, un Chromium allege
            # plus facile a reconnaitre. Le canal "chromium" force
            # le build complet, moins detectable en mode headless
            # moderne (verifie : le processus lance est bien
            # chromium-1248/chrome, pas chrome-headless-shell).
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                channel="chromium",
                args=LAUNCH_ARGS,
            )
            # L'agent utilisateur est construit avec la version du
            # Chromium qui tourne vraiment (voir _user_agent).
            version = self._browser.version
            self._context = await self._browser.new_context(
                viewport={"width": 1280, "height": 800},
                locale="en-CA",
                timezone_id="America/Toronto",
                user_agent=_user_agent(version),
            )
            await self._context.add_init_script(INIT_SCRIPT)
            self._page = await self._context.new_page()
        except Exception as exc:
            await self._close_quietly()
            raise BrowserStartError(
                f"Chromium did not start: {exc}. "
                "Check PLAYWRIGHT_BROWSERS_PATH and run install.ps1."
            ) from exc
        self._started = True

    async def stop(self) -> None:
        """Arrete le navigateur. Sans effet s'il n'a jamais demarre."""
        await self._close_quietly()
        self._started = False

    async def _close_quietly(self) -> None:
        for closable in (self._page, self._context, self._browser):
            if closable is not None:
                try:
                    await closable.close()
                except Exception:
                    pass
        if self._playwright is not None:
            try:
                await self._playwright.stop()
            except Exception:
                pass
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None

    # -- Cookies ------------------------------------------------------

    async def set_cookies(self, cookies: list | None) -> None:
        """Fixe les cookies du contexte. Avec une liste (appel
        authentifie, jar) : remplacement complet par exactement
        ceux donnes. Avec None (appel anonyme) : on ne touche a
        rien, sauf si le contexte porte encore les cookies d'un
        appel authentifie precedent, qu'on efface alors pour
        retrouver un etat anonyme propre.

        Ne JAMAIS re-injecter des cookies synchronises depuis le
        navigateur : le navigateur les a deja, et les reconstruire
        (domaine, expiration, secure) en cree un sous-ensemble
        incoherent qu'Amazon rejette (verifie 2026-11-05 : page
        produit en 503 avec cookies re-injectes, 200 sans). Le
        navigateur garde ses propres cookies comme un vrai
        navigateur ; on ne lui impose un jeu exact que pour un jar.
        """
        if self._context is None:
            raise BrowserStartError("browser is not started")
        if cookies is None:
            if self._session_cookies_active:
                await self._context.clear_cookies()
                self._session_cookies_active = False
            return
        await self._context.clear_cookies()
        self._session_cookies_active = True
        clean = []
        for cookie in cookies:
            name = str(cookie.get("name") or "").strip()
            value = str(cookie.get("value") or "")
            domain = str(cookie.get("domain") or "").strip().lstrip(".")
            if not name or not domain:
                continue
            try:
                expires = int(cookie.get("expires", -1))
            except (TypeError, ValueError):
                expires = -1
            clean.append(
                {
                    "name": name,
                    "value": value,
                    "domain": domain,
                    "path": str(cookie.get("path") or "/"),
                    "expires": expires if expires > 0 else -1,
                    "secure": bool(cookie.get("secure")),
                }
            )
        if clean:
            await self._context.add_cookies(clean)

    async def current_cookies(self) -> list:
        """Cookies actuels du contexte, au format Playwright."""
        if self._context is None:
            return []
        return await self._context.cookies()

    # -- Navigation ---------------------------------------------------

    async def navigate(
        self,
        url: str,
        cookies: list | None = None,
        wait_selector: str | None = None,
        referer: str | None = None,
    ) -> FetchResult:
        """Va sur une URL et renvoie son contenu. Suppose que
        l'appelant detient le verrou. Un selecteur d'attente qui
        n'apparait pas n'est pas une erreur : on renvoie le contenu
        tel quel, c'est au code appelant de le juger (page de
        blocage, page vide, mise en page changee)."""
        await self.start()
        await self.set_cookies(cookies)
        page = self._page
        try:
            response = await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=GOTO_TIMEOUT_MS,
                referer=referer,
            )
        except Exception as exc:
            raise BrowserFetchError(f"navigation to {url} failed: {exc}") from exc
        if wait_selector:
            try:
                await page.wait_for_selector(
                    wait_selector, state="attached", timeout=SELECTOR_TIMEOUT_MS
                )
            except Exception:
                pass  # Contenu tel quel, voir docstring.
        status = response.status if response is not None else None
        html = await page.content()
        title = await page.title()
        return FetchResult(status=status, html=html, title=title)

    async def current_html(self) -> FetchResult:
        """Relit le contenu actuel de la page, sans naviguer. Sert
        a reverifier une page dont le marqueur de blocage etait
        transitoire (erreur de chargement d'une section, resolue
        apres quelques secondes) : on relit au lieu de declarer
        un blocage sur un instantane trop tot. Suppose que
        l'appelant detient le verrou."""
        page = self._page
        html = await page.content()
        title = await page.title()
        return FetchResult(status=None, html=html, title=title)

    async def submit_add_to_cart(self, quantity: int = 1) -> FetchResult:
        """Clique sur le bouton d'ajout au panier du formulaire
        #addToCart de la page courante, puis attend la confirmation
        ou le chargement. Suppose que l'appelant detient le verrou
        et que la page courante est une page produit.

        Le clic sur le vrai bouton est prefere : il envoie aussi le
        nom du bouton, comme un humain. Si le bouton est introuvable
        (page pas encore rendue, bouton absent), on soumet le
        formulaire directement en JavaScript. Si le formulaire est
        absent, FormNotFound : la session n'est pas valide.
        """
        page = self._page
        form = await page.query_selector("form#addToCart")
        if form is None:
            raise FormNotFound("no add to cart form on the product page")
        if quantity > 1:
            # La quantite se choisit avant le clic, si le menu existe.
            for selector in ("select#quantity", "form#addToCart select[name='quantity']"):
                select = await page.query_selector(selector)
                if select is not None:
                    try:
                        await select.select_option(str(quantity), timeout=3000)
                    except Exception:
                        pass
                    break
        submit = page.locator(
            "form#addToCart input[type='submit'], "
            "form#addToCart button[type='submit']"
        ).first
        clicked = False
        try:
            await submit.click(timeout=CLICK_TIMEOUT_MS)
            clicked = True
        except Exception:
            pass
        if not clicked:
            await page.evaluate(
                "() => { const f = document.querySelector('form#addToCart'); "
                "if (f) f.submit(); }"
            )
        # Attendre la confirmation, ou le chargement, sans exiger.
        # La relecture du panier qui suit reste la verite de reference.
        try:
            await page.wait_for_selector(
                ", ".join(ADD_CONFIRM_SELECTORS),
                state="attached",
                timeout=SELECTOR_TIMEOUT_MS,
            )
        except Exception:
            try:
                await page.wait_for_load_state("load", timeout=SELECTOR_TIMEOUT_MS)
            except Exception:
                pass
        html = await page.content()
        title = await page.title()
        return FetchResult(status=None, html=html, title=title)


_ENGINE: BrowserEngine | None = None


def get_engine() -> BrowserEngine:
    """Le moteur partage de l'application (singleton par processus)."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = BrowserEngine()
    return _ENGINE


async def close_engine() -> None:
    """Arrete le moteur partage, si demarre. Appele a l'arret du
    serveur."""
    global _ENGINE
    if _ENGINE is not None:
        await _ENGINE.stop()
