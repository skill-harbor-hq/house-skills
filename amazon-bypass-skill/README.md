# Amazon Bypass Skill

API locale pour chercher sur Amazon.ca et ajouter au panier, avec
Muse. Code maison de Skill Harbor, ecrit de zero. La recherche ne
demande pas de login. L'ajout au panier utilise les cookies de session
exportes du navigateur normal. Ce service ne paie jamais, ne passe
jamais en caisse, ne fait aucun login automatise et ne contient aucun
mot de passe.

V2 : les pages Amazon sont chargees par un vrai navigateur Chromium
pilote par Playwright, rendu JavaScript compris. La v1 parlait a
Amazon en requetes HTTP directes et se faisait servir un HTTP 503 :
un vrai navigateur est beaucoup plus dur a detecter comme robot. En
contrepartie, chaque page prend quelques secondes a charger, et le
serveur ne repond jamais instantanement sur la recherche.

## Avertissement de securite (a lire avant tout)

Les cookies de session Amazon sont aussi puissants qu'un mot de passe
temporaire : quiconque possede le fichier peut se faire passer pour
vous sur Amazon. Regles :

- Exportez les cookies depuis votre navigateur normal, ou vous etes
  deja connecte a Amazon. Ne collez jamais leur contenu dans un chat,
  un courriel ou un fichier partage.
- Gardez le fichier dans le dossier local du skill seulement, avec
  les droits restreints. Supprimez-le apres un test.
- Si le fichier fuit, changez votre mot de passe Amazon et
  deconnectez toutes les sessions depuis les reglages du compte.

Amazon dit que l'acces par un agent non autorise viole ses conditions
d'utilisation. Si Amazon bloque la requete, le serveur renvoie 503 et
le dit clairement. Un blocage repete peut mener a une suspension du
compte, c'est un risque connu et assume par l'utilisateur.

## Installation (PC Windows, Python portable)

Le Python portable est celui de `C:\Users\muse-build\work\tools\python-embed`.
L'installation est volontairement simple, pour eviter les pieges
rencontres avec l'ancien skill (venv absent, setuptools absent,
PYTHONPATH ignore par le Python portable en mode isole) :

```powershell
cd C:\Users\muse-build\work\amazon-bypass-maison\src
.\install.ps1
```

`install.ps1` fait trois choses seulement :

1. `pip install fastapi uvicorn pydantic beautifulsoup4 playwright`,
   en wheels, directement dans `Lib\site-packages` du Python portable.
   Aucun venv, aucune construction depuis les sources, aucun PYTHONPATH.
2. Copie du paquet `harbor_amazon` dans `Lib\site-packages`, puis
   verification de l'import.
3. Verification que Chromium se lance (`check_browser.py`, ouvre
   `about:blank` et ferme). Si les navigateurs sont absents, un seul
   `playwright install chromium`, puis on reteste une fois.

## Demarrage

```powershell
.\start.ps1
```

`start.ps1` genere la cle API locale si elle est absente (fichier
`api-key` dans le dossier du skill, longueur seulement dans les logs,
jamais la valeur), fixe `PLAYWRIGHT_BROWSERS_PATH` vers le dossier
des navigateurs du PC (la variable n'est pas persistante), puis
demarre le serveur lie a `127.0.0.1:8792` seulement et attend
`/health` 200 pendant 20 secondes maximum. Sinon, il arrete le serveur
et affiche l'erreur exacte.

Le navigateur Chromium demarre paresseusement, a la premiere requete
Amazon : `/health` reste rapide. Si Chromium ne demarre pas, l'API
renvoie 500 avec la raison exacte, jamais un faux 503. Le skill ne
resout jamais un captcha : si Amazon en presente un, le serveur
renvoie 503 et le dit clairement.

Variables d'environnement (toutes optionnelles) :

- `AMAZON_API_KEY` : cle API. Sinon, `MUSE_API_KEY` ou `API_KEY`.
  `start.ps1` la genere et la lit depuis le fichier `api-key`.
- `AMAZON_DEFAULT_REGION` : region par defaut, `ca` (amazon.ca).
- `AMAZON_COOKIE_DIR` : dossier des jars, defaut `~\.harbor-amazon`.
- `PLAYWRIGHT_BROWSERS_PATH` : dossier des navigateurs Chromium.
  `start.ps1` le fixe sur le PC ; sans lui, Playwright ne trouve
  pas Chromium.
- `HOST` : defaut `127.0.0.1`. Ne jamais l'exposer en public.
- `PORT` : defaut `8792`.

## Cookies de session

Connectez-vous a Amazon dans votre navigateur normal (Amazon bloque
les fenetres de login automatisees), puis exportez les cookies au
format Netscape :

| Compte | Fichier |
| --- | --- |
| `personal` | `cookies-personal.txt` |
| `business` | `cookies-business.txt` |

Une session business contient un cookie `b2b`. Un ajout personnel
est refuse si ce cookie est present, un ajout business est refuse
s'il est absent. Apres un test, retirez l'article du panier a la main
et supprimez le fichier de cookies.

## API

| Methode | Chemin | Usage |
| --- | --- | --- |
| GET | `/health` | Signe de vie, sans auth |
| GET | `/regions` | Codes de regions, sans auth |
| GET | `/search?query=...&region=ca&max_results=10` | Recherche |
| GET | `/products?query=...` | Alias de la recherche |
| GET | `/product/{asin}` | Detail d'un produit |
| GET | `/product/{asin}/variations` | Variantes |
| GET | `/cart?account=personal` | Panier |
| GET | `/cart/add?asin=...&quantity=1&account=personal` | Ajouter |
| POST | `/cart` | Corps JSON `{"asin","quantity","region","account"}` |

Auth : `Authorization: Bearer <cle>` ou `X-Api-Key: <cle>`.

Codes : `401` cle absente ou fausse, `409` compte non connecte ou
mauvais jar, `503` Amazon a bloque, `502` requete reseau echouee,
`500` le navigateur n'a pas pu demarrer (raison exacte dans le detail).

## Tests (VM, avec un faux serveur Amazon)

```bash
cd tests
python3 test_parse.py          # parsing seul, sans navigateur
python3 test_browser_mock.py   # API complete avec un vrai Chromium
```

`test_parse.py` verifie les parseurs sur du HTML factice local, sans
navigateur ni reseau. `test_browser_mock.py` demarre un faux serveur
Amazon local et appelle la vraie application avec un vrai Chromium :
`/health`, la recherche parsee, le 401 sans cle, le 409 sur
`/cart/add` sans cookies, le 503 sur page de blocage et le panier
avec un faux jar. Si Chromium n'est pas disponible sur la machine de
test, ce fichier l'indique et s'arrete proprement : les tests
navigateur sont alors a faire sur le PC seulement. Les selecteurs
Amazon reels, la page interstitielle Akamai et l'ajout reel au panier
restent a verifier en direct sur le PC (phases 1 et 2).

## Licence

MIT, Skill Harbor. Code ecrit de zero ; la connaissance du mecanisme
vient de l'etude du skill aasper03 et des pages Amazon publiques.
