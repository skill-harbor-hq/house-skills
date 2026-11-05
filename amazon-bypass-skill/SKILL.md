# Amazon Bypass Skill

## Nom

Amazon Bypass Skill

## Description

Recherche sur Amazon.ca et ajout au panier pour Muse, avec une API
locale qui tourne sur la machine de l'utilisateur. La recherche ne
demande pas de login. L'ajout au panier utilise les cookies de session
exportes du navigateur normal. Le skill ne paie jamais et ne passe
jamais en caisse.

V2 : les pages Amazon sont chargees par un vrai navigateur Chromium
pilote par Playwright, rendu JavaScript compris. Chaque page prend
quelques secondes a charger. Le skill ne resout jamais un captcha :
si Amazon bloque, le serveur renvoie 503 et le dit clairement.

## Installation

1. Installer les dependances en wheels dans le Python portable, puis
   copier le paquet dans `Lib\site-packages` (voir `install.ps1`) et
   verifier que Chromium se lance. Aucun venv, aucune construction
   depuis les sources, aucun PYTHONPATH.
2. Lancer `start.ps1` : il genere la cle API locale si elle est absente,
   fixe `PLAYWRIGHT_BROWSERS_PATH`, puis demarre le serveur sur
   `127.0.0.1:8792` et attend `/health`. Le navigateur demarre
   paresseusement, a la premiere requete Amazon.
3. Exporter les cookies Amazon du navigateur normal (format
   Netscape) dans le dossier des cookies du skill :
   `<dossier du skill>\cookies\cookies-personal.txt` pour le compte
   personnel (ou pointez `AMAZON_COOKIE_DIR` vers le dossier qui
   contient le jar avant de lancer `start.ps1`). Sans jar dans ce
   dossier, la recherche passe mais le panier repond 409.
   Voir `README.md` pour l'avertissement de securite.

## Utilisation dans Muse

Coller le prompt de `MUSE.md` dans Muse, sur la machine ou tourne le
serveur. Base URL : `http://127.0.0.1:8792`, auth Bearer avec
`AMAZON_API_KEY` lue dans l'environnement de cette machine.

## Endpoints

- `GET /health` (sans auth) : signe de vie.
- `GET /regions` (sans auth) : codes de regions.
- `GET /search?query=...&region=ca&max_results=10` : recherche.
- `GET /products?query=...` : alias de la recherche.
- `GET /product/{asin}` : detail d'un produit.
- `GET /product/{asin}/variations` : variantes.
- `GET /cart?account=personal` : panier.
- `GET /cart/add?asin=...&quantity=1&account=personal` : ajouter.
- `POST /cart` : corps JSON `{"asin","quantity","region","account"}`.

## Codes d'erreur

- `401` : cle API absente ou fausse.
- `409` : compte non connecte, ou mauvais jar de cookies.
- `503` : Amazon a bloque la requete (page de blocage, captcha ou
  interstitial). Le dire clairement, ne pas inventer de resultats.
- `502` : la requete vers Amazon a echoue au niveau reseau.
- `500` : le navigateur n'a pas pu demarrer (raison exacte dans le
  detail). Ce n'est pas un blocage Amazon.

## Limites connues (v2)

- Selecteurs HTML verifies en direct sur PC : phase 1 v2 (recherche +
  detail, 2026-11-05) et phase 2 (ajout au panier, 2026-11-05) passent
  sur amazon.ca. Un marqueur d'erreur Amazon peut coexister avec le
  contenu attendu : le serveur avance quand le contenu est la, et ne
  declare un blocage que si le marqueur persiste sans contenu.
- Une page d'interstitial Akamai ou un captcha est detecte et signale
  en 503. La v2 ne tente pas de les resoudre, jamais.
- Chaque requete prend quelques secondes (chargement d'une vraie page
  dans Chromium). Une seule navigation a la fois : les requetes sont
  traitees en file.
- Le skill ne gere pas le checkout, le paiement, ni le login
  automatise. C'est volontaire et permanent.
