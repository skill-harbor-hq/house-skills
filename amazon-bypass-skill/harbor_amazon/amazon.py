"""Client Amazon pour Harbor Amazon : navigation par vrai navigateur,
detection des blocages, parsing.

Code original, ecrit de zero. La connaissance utilisee ici vient de
l'etude du skill aasper03 et des pages Amazon publiques, pas de son code :
- la recherche ne demande pas de login, l'ajout au panier oui ;
- une page de blocage, un captcha ou un interstitial se detecte et se
  signale par une erreur 503, on ne pretend jamais que ca a marche ;
- les cookies de session viennent d'un jar Netscape exporte du
  navigateur normal, jamais d'un login automatise.

La v2 remplace la couche HTTP (curl_cffi) par un vrai Chromium pilote
par Playwright : la phase 1 v1 a prouve qu'Amazon sert un HTTP 503
direct aux requetes HTTP, meme avec un fingerprint TLS Chrome. Les
pages sont donc chargees par le navigateur (voir browser.py), puis
leur HTML est parse ici avec BeautifulSoup, avec les memes parseurs
que la v1.

Ce module ne fait ni checkout, ni paiement, ni login automatise, et ne
contient aucun mot de passe.
"""

from __future__ import annotations

import asyncio
import os
import re
from collections.abc import Callable
from urllib.parse import quote_plus, urljoin

from bs4 import BeautifulSoup

from .browser import (
    BrowserFetchError,
    BrowserStartError,
    FormNotFound,
    get_engine,
)
from .cookies import Jar

# Region -> hote Amazon. La region par defaut est ca.
REGIONS = {
    "ca": "www.amazon.ca",
    "us": "www.amazon.com",
    "uk": "www.amazon.co.uk",
    "de": "www.amazon.de",
    "fr": "www.amazon.fr",
    "es": "www.amazon.es",
    "it": "www.amazon.it",
    "nl": "www.amazon.nl",
    "jp": "www.amazon.co.jp",
    "au": "www.amazon.com.au",
    "mx": "www.amazon.com.mx",
    "in": "www.amazon.in",
    "ae": "www.amazon.ae",
    "sa": "www.amazon.sa",
    "ie": "www.amazon.ie",
    "be": "www.amazon.com.be",
}
DEFAULT_REGION = "ca"

# Textes qui signalent une page de blocage, un captcha ou un interstitial.
BLOCK_MARKERS = (
    "Enter the characters you see below",
    "Sorry, we just need to make sure you're not a robot",
    "automated access to Amazon data",
    "To discuss automated access",
    "dogs of amazon",
    "api-services-support@amazon",
    "bm-verify",
    "Please verify you are a human",
    "are you a robot",
    "Robot Check",
    "Something went wrong on our end",
)

# Surcharge de l'hote pour les tests seulement. Ne jamais definir en
# production : les requetes iraient vers un autre serveur.
TEST_BASE_URL_ENV = "HARBOR_AMAZON_BASE_URL"


def _has_selector(html: str, selector: str) -> bool:
    """Vrai si le selecteur CSS trouve un element dans le HTML."""
    try:
        return BeautifulSoup(html, "html.parser").select_one(selector) is not None
    except Exception:
        return False


def _is_cart_page(html: str) -> bool:
    """Vrai si le HTML ressemble a une vraie page panier (avec ou
    sans articles), par opposition a une page d'erreur. Corrige le
    faux 503 de la phase 2 (2026-11-05) : apres un ajout reussi, la
    page panier portait le marqueur transitoire "Something went wrong
    on our end" tout en contenant les articles — la confirmation
    declarait un blocage alors que l'ajout avait passe."""
    try:
        soup = BeautifulSoup(html, "html.parser")
    except Exception:
        return False
    if soup.select_one("div.sc-list-item[data-asin]"):
        return True
    return "Your Amazon Cart is empty" in soup.get_text(" ", strip=True)


def _content_present(
    html: str,
    wait_selector: str | None,
    content_ok: Callable[[str], bool] | None,
) -> bool:
    """Vrai si le contenu attendu est present dans le HTML : soit le
    selecteur attendu, soit le test de contenu fourni par l'appelant.
    C'est ce critere, et non l'absence de marqueur, qui decide si une
    page est utilisable."""
    if wait_selector is not None and _has_selector(html, wait_selector):
        return True
    if content_ok is not None and content_ok(html):
        return True
    return False


class AmazonBlocked(Exception):
    """Amazon a servi une page de blocage, un captcha ou un interstitial."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class AmazonFetchError(Exception):
    """La requete vers Amazon a echoue au niveau reseau."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class NotSignedIn(Exception):
    """Aucune session Amazon valide pour ce compte."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class WrongAccount(Exception):
    """Le jar appartient a l'autre type de compte (personal / business)."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class BrowserUnavailable(Exception):
    """Le navigateur n'a pas pu demarrer : erreur de configuration du
    serveur, pas un blocage Amazon. L'API la traduit en 500, jamais
    en 503, avec la raison exacte."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _is_blocked(status: int | None, html: str) -> str | None:
    """Renvoie la raison du blocage, ou None si la page semble normale."""
    if status in (429, 503):
        return f"Amazon returned HTTP {status}"
    lowered = html.lower()
    for marker in BLOCK_MARKERS:
        if marker.lower() in lowered:
            return f"block page marker found: {marker}"
    title = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title and "sorry" in title.group(1).lower():
        return "block page title: Sorry"
    return None


def _text(element) -> str | None:
    if element is None:
        return None
    value = element.get_text(" ", strip=True)
    return value or None


def _price_text(element) -> str | None:
    """Prix sous forme de texte, ex. $12.99 ou 12,99 $."""
    if element is None:
        return None
    offscreen = element.select_one(".a-offscreen")
    if offscreen is not None:
        return _text(offscreen)
    whole = element.select_one(".a-price-whole")
    fraction = element.select_one(".a-price-fraction")
    if whole is not None:
        price = _text(whole) or ""
        if fraction is not None:
            price += "." + (_text(fraction) or "00")
        return price or None
    return _text(element)


def _parse_rating(element) -> float | None:
    if element is None:
        return None
    text = _text(element) or ""
    match = re.search(r"([0-9]+(?:[.,][0-9]+)?)\s+out of 5", text)
    if match:
        return float(match.group(1).replace(",", "."))
    return None


def _parse_int(text: str | None) -> int | None:
    if not text:
        return None
    digits = re.sub(r"[^0-9]", "", text)
    return int(digits) if digits else None


# -- Parsing pur : HTML en entree, donnees en sortie. Ces fonctions
# ne touchent ni au reseau ni au navigateur : elles sont testables
# sur des fichiers HTML locaux. -------------------------------------


def parse_search(html: str, base_url: str, max_results: int = 16) -> list:
    """Resultats de recherche depuis le HTML d'une page /s."""
    soup = BeautifulSoup(html, "html.parser")
    results = []
    blocks = soup.select('div[data-component-type="s-search-result"]')
    for block in blocks:
        asin = block.get("data-asin")
        if not asin:
            continue
        # Titre : la structure reelle varie. Sur amazon.ca en 2026-11,
        # le titre est dans un <span> nu sous <h2> (cas sponsorise,
        # verifie sur page reelle), ou dans le lien <h2><a>, ou dans
        # le lien a.s-line-clamp-2/3. On essaie dans cet ordre.
        title = None
        h2 = block.select_one("h2")
        if h2 is not None:
            title = _text(h2.select_one("span")) or _text(h2)
        if not title:
            link = block.select_one("h2 a")
            if link is not None:
                title = _text(link.select_one("span")) or _text(link)
        if not title:
            clamp = block.select_one("a.s-line-clamp-2, a.s-line-clamp-3")
            if clamp is not None:
                title = _text(clamp)
        url = None
        link = block.select_one("h2 a")
        if link is not None:
            href = link.get("href") or ""
            if href.startswith("/dp/"):
                url = urljoin(base_url + "/", href)
        price_block = block.select_one("span.a-price")
        price = _price_text(price_block)
        rating_el = block.select_one(".a-icon-star-small .a-icon-alt")
        if rating_el is None:
            rating_el = block.select_one(".a-icon-star .a-icon-alt")
        rating = _parse_rating(rating_el)
        reviews = None
        reviews_link = block.select_one('a[href*="customerReviews"] span')
        if reviews_link is not None:
            reviews = _parse_int(_text(reviews_link))
        image = block.select_one("img.s-image")
        image_url = None
        if image is not None:
            image_url = image.get("src") or image.get("data-src")
        sponsored = "Sponsored" in block.get_text()
        results.append(
            {
                "asin": asin,
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "url": url or f"{base_url}/dp/{asin}",
                "image": image_url,
                "sponsored": sponsored,
            }
        )
        if len(results) >= max_results:
            break
    return results


def parse_product(html: str, asin: str, base_url: str) -> dict:
    """Detail d'un produit depuis le HTML d'une page /dp/{asin}."""
    soup = BeautifulSoup(html, "html.parser")
    title = _text(soup.select_one("#productTitle"))
    price = None
    price_block = soup.select_one("#corePriceDisplay span.a-price")
    if price_block is None:
        price_block = soup.select_one("span.a-price")
    price = _price_text(price_block)
    brand = _text(soup.select_one("#bylineInfo"))
    rating = _parse_rating(soup.select_one('[data-hook="rating-out-of-text"]'))
    if rating is None:
        rating = _parse_rating(soup.select_one("#acrPopover .a-icon-alt"))
    reviews = None
    reviews_el = soup.select_one("#acrCustomerReviewText")
    if reviews_el is not None:
        reviews = _parse_int(_text(reviews_el))
    availability = _text(soup.select_one("#availability span"))
    features = []
    for item in soup.select("#feature-bullets li span.a-list-item"):
        text = _text(item)
        if text:
            features.append(text)
    images = []
    main_image = soup.select_one("#landingImage")
    if main_image is not None and main_image.get("src"):
        images.append(main_image["src"])
    for thumb in soup.select("#altImages img"):
        src = thumb.get("src")
        if src and src not in images:
            images.append(src)
    return {
        "asin": asin,
        "title": title,
        "price": price,
        "brand": brand,
        "rating": rating,
        "reviews": reviews,
        "availability": availability,
        "features": features,
        "images": images,
        "url": f"{base_url}/dp/{asin}",
    }


def parse_variations(html: str) -> list:
    """Variantes d'un produit (couleur, taille, style). Best effort."""
    soup = BeautifulSoup(html, "html.parser")
    groups = []
    for container in soup.select('div[id^="variation_"]'):
        group_id = container.get("id") or ""
        label = None
        label_el = container.select_one("label, .a-form-label, span.a-text-bold")
        if label_el is not None:
            label = _text(label_el)
        options = []
        for option in container.select("li[title], li[data-defaultasin]"):
            option_asin = option.get("data-defaultasin") or option.get("data-asin")
            option_title = option.get("title") or _text(option)
            if option_title:
                options.append(
                    {"asin": option_asin, "label": option_title.strip()}
                )
        if options:
            groups.append(
                {
                    "group": group_id.replace("variation_", ""),
                    "label": label,
                    "options": options,
                }
            )
    return groups


def parse_cart(html: str) -> dict:
    """Contenu du panier depuis le HTML de /gp/cart/view.html.
    Leve NotSignedIn si la page demande de se connecter."""
    soup = BeautifulSoup(html, "html.parser")
    if soup.select_one("form[name='signIn'], #ap_signin_form"):
        raise NotSignedIn("Amazon asks for sign in, no valid session")
    page_text = soup.get_text(" ", strip=True)
    if "Your Amazon Cart is empty" in page_text:
        return {"items": [], "count": 0, "subtotal": None}
    items = []
    for block in soup.select("div.sc-list-item[data-asin]"):
        asin = block.get("data-asin")
        if not asin:
            continue
        title_el = block.select_one(".sc-product-title")
        title = _text(title_el)
        quantity = 1
        qty_select = block.select_one('select[name="quantity"]')
        if qty_select is not None:
            selected = qty_select.select_one("option[selected]")
            if selected is not None:
                quantity = _parse_int(_text(selected)) or 1
        price_block = block.select_one(".sc-price")
        price = _price_text(price_block)
        items.append(
            {
                "asin": asin,
                "title": title,
                "quantity": quantity,
                "price": price,
            }
        )
    subtotal = None
    subtotal_el = soup.select_one("#sc-subtotal-amount-buybox .a-offscreen")
    if subtotal_el is not None:
        subtotal = _text(subtotal_el)
    return {
        "items": items,
        "count": sum(item["quantity"] for item in items),
        "subtotal": subtotal,
    }


class AmazonClient:
    """Un client Amazon pour une region, avec ou sans cookies.

    Toutes les methodes sont async : elles tournent sur la boucle
    d'evenements de FastAPI, avec un seul navigateur partage. Le
    verrou du moteur serialise les navigations, une seule a la
    fois."""

    def __init__(
        self,
        region: str = DEFAULT_REGION,
        cookies: dict | None = None,
        jar: Jar | None = None,
    ):
        if region not in REGIONS:
            raise ValueError(f"unknown region: {region}")
        self.region = region
        self.host = REGIONS[region]
        self.cookies = dict(cookies or {})
        self._jar = jar
        if jar is not None:
            self.cookies = jar.as_dict()
        self._engine = get_engine()

    # -- URL de base ----------------------------------------------------

    def base_url(self) -> str:
        override = os.environ.get(TEST_BASE_URL_ENV)
        if override:
            return override.rstrip("/")
        return f"https://{self.host}"

    # -- Cookies ------------------------------------------------------

    def _playwright_cookies(self) -> list | None:
        """Les cookies de session au format Playwright, seulement
        quand un jar est connu (appel authentifie). Sans jar, on
        renvoie None : le navigateur garde ses propres cookies,
        comme un vrai navigateur. Ne pas re-injecter les cookies
        synchronises depuis le navigateur : les reconstruire en
        cree un sous-ensemble incoherent qu'Amazon rejette (page
        produit en 503, verifie 2026-11-05)."""
        if self._jar is not None:
            cookies = []
            for cookie in self._jar.cookies:
                try:
                    expires = int(cookie.expires)
                except (TypeError, ValueError):
                    expires = -1
                cookies.append(
                    {
                        "name": cookie.name,
                        "value": cookie.value,
                        "domain": cookie.domain,
                        "path": cookie.path or "/",
                        "expires": expires if expires > 0 else -1,
                        "secure": str(cookie.secure).upper() == "TRUE",
                    }
                )
            return cookies or None
        return None

    def _cookie_belongs_here(self, domain: str) -> bool:
        """Vrai si un domaine de cookie couvre l'hote courant."""
        domain = (domain or "").lstrip(".").lower()
        host = self.host.lower()
        return domain == host or host.endswith("." + domain)

    async def _sync_cookies_from_browser(self) -> None:
        """Recopie les cookies que le navigateur a recus ou
        rafraichis pendant la navigation (session qui se prolonge).
        Le jar est mis a jour par l'API apres l'appel, comme en v1."""
        if self._jar is None and not self.cookies:
            return
        try:
            browser_cookies = await self._engine.current_cookies()
        except Exception:
            return
        for cookie in browser_cookies:
            domain = cookie.get("domain") or ""
            if not self._cookie_belongs_here(domain):
                continue
            name = cookie.get("name")
            value = cookie.get("value")
            if not name or value is None:
                continue
            self.cookies[name] = value
            if self._jar is not None:
                self._jar.update(name, value, domain)

    # -- Chargement d'une page ----------------------------------------

    async def get(
        self,
        path: str,
        wait_selector: str | None = None,
        referer: str | None = None,
        content_ok: Callable[[str], bool] | None = None,
    ) -> str:
        """Charge une page Amazon dans le navigateur. Leve
        AmazonBlocked, AmazonFetchError ou BrowserUnavailable.

        content_ok, quand il est fourni, dit si le HTML contient le
        contenu attendu (par ex. une vraie page panier) : c'est ce
        critere qui decide si la page est utilisable, marqueur ou
        pas — comme wait_selector pour le detail produit."""
        url = self.base_url() + path
        async with self._engine.lock:
            try:
                result = await self._engine.navigate(
                    url,
                    cookies=self._playwright_cookies(),
                    wait_selector=wait_selector,
                    referer=referer,
                )
            except BrowserStartError as exc:
                raise BrowserUnavailable(exc.reason) from exc
            except BrowserFetchError as exc:
                raise AmazonFetchError(exc.reason) from exc
            await self._sync_cookies_from_browser()
        html = result.html
        blocked = _is_blocked(result.status, html)
        if blocked:
            # Un marqueur peut coexister avec le contenu attendu : sur
            # la page produit, Amazon affiche parfois "Something went
            # wrong on our end" pour une section en cours de chargement
            # pendant que le detail (#productTitle, prix, ajout) est
            # deja la (verifie 2026-11-05 : 503 declare alors que le
            # detail etait present, marqueur absent a la relecture
            # suivante). Meme chose pour le panier : apres un ajout
            # reussi, la page panier portait le marqueur tout en
            # contenant l'article — la confirmation declarait un
            # blocage alors que l'ajout avait passe (phase 2,
            # 2026-11-05). Le critere decisif est donc le contenu
            # attendu : s'il est present, la page est utilisable,
            # marqueur ou pas. Sinon, le marqueur est peut-etre
            # transitoire : on relit la page jusqu'a 3 fois, 10 s
            # d'intervalle, et on avance des que le marqueur a disparu
            # ou que le contenu attendu est arrive. S'il persiste sans
            # contenu attendu, c'est un vrai blocage : 503.
            for _ in range(3):
                if _content_present(html, wait_selector, content_ok):
                    break
                await asyncio.sleep(10)
                async with self._engine.lock:
                    fresh = await self._engine.current_html()
                html = fresh.html
                if _is_blocked(result.status, html) is None:
                    break
            if _is_blocked(result.status, html) is not None and not (
                _content_present(html, wait_selector, content_ok)
            ):
                raise AmazonBlocked(blocked)
        if result.status is not None and result.status != 200:
            raise AmazonFetchError(f"Amazon returned HTTP {result.status}")
        return html

    # -- Recherche ------------------------------------------------------

    async def search(self, query: str, max_results: int = 16) -> list:
        """Recherche des produits. Aucun login requis."""
        html = await self.get(
            f"/s?k={quote_plus(query)}",
            wait_selector='div[data-component-type="s-search-result"]',
        )
        return parse_search(html, self.base_url(), max_results=max_results)

    # -- Produit --------------------------------------------------------

    async def product(self, asin: str) -> dict:
        """Detail d'un produit par son ASIN."""
        html = await self.get(f"/dp/{asin}", wait_selector="#productTitle")
        return parse_product(html, asin, self.base_url())

    async def variations(self, asin: str) -> list:
        """Variantes d'un produit (couleur, taille, style). Best effort."""
        html = await self.get(f"/dp/{asin}", wait_selector="#productTitle")
        return parse_variations(html)

    # -- Panier ---------------------------------------------------------

    async def read_cart(self) -> dict:
        """Contenu du panier pour la session courante."""
        html = await self.get("/gp/cart/view.html", content_ok=_is_cart_page)
        return parse_cart(html)

    async def add_to_cart(self, asin: str, quantity: int = 1) -> dict:
        """Ajoute un article au panier. Ne paie jamais, ne passe pas en caisse.

        Etapes : charger la page produit avec les cookies, cliquer sur
        le vrai bouton d'ajout (le navigateur envoie le formulaire
        comme un humain), puis relire le panier pour confirmer que
        l'article y est. Si le formulaire est absent, la session n'est
        pas valide : 409, pas de tentative aveugle. Tout le flux tient
        le verrou du navigateur, pour qu'aucune autre requete ne
        detourne la page entre le chargement et le clic.
        """
        product_url = f"/dp/{asin}"
        async with self._engine.lock:
            html = await self.get(
                product_url, wait_selector="form#addToCart"
            )
            soup = BeautifulSoup(html, "html.parser")
            if soup.select_one("form#addToCart") is None:
                raise NotSignedIn(
                    "no add to cart form on the product page, session is not valid"
                )
            try:
                await self._engine.submit_add_to_cart(quantity=quantity)
            except FormNotFound as exc:
                raise NotSignedIn(
                    "no add to cart form on the product page, session is not valid"
                ) from exc
            except BrowserStartError as exc:
                raise BrowserUnavailable(exc.reason) from exc
            except BrowserFetchError as exc:
                raise AmazonFetchError(exc.reason) from exc
            cart = await self.read_cart()
        found = next(
            (item for item in cart["items"] if item["asin"] == asin), None
        )
        if found is None:
            raise AmazonFetchError(
                "add to cart posted but the item is not in the cart"
            )
        return {
            "added": True,
            "asin": asin,
            "quantity": found["quantity"],
            "cart_count": cart["count"],
        }
