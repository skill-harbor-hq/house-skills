# Amazon Bypass Skill : prompt pour Muse

Colle ce prompt dans Muse quand le serveur tourne sur la machine
accessible en SSH. Le serveur est une API locale ecrite par
Skill Harbor, de zero, pour chercher sur Amazon.ca et ajouter au
panier. Il ne paie jamais et ne passe jamais en caisse. V2 : les
pages sont chargees par un vrai navigateur Chromium, donc chaque
requete prend quelques secondes. Ne jamais demander un captcha a
l'utilisateur : si Amazon bloque, le serveur renvoie 503.

## Prompt a coller

```
Amazon search and cart is already running on the machine you SSH into.
Base URL: http://127.0.0.1:8792
Auth: Authorization: Bearer, using AMAZON_API_KEY from that host.
Do not ask me to paste the key in chat.

Use GET /search?query=...&region=ca to search (region ca by default,
amazon.ca first). Use GET /product/{asin} for details and
GET /product/{asin}/variations for variants. Use
GET /cart?account=personal to read the personal cart and
GET /cart/add?asin=...&quantity=1&account=personal to add to it.
Use account=business only for the business cart.

Adding does not purchase. HTTP 401 means the API key is missing or
wrong. HTTP 409 means that account is not signed in, or the wrong
cookie jar was used. HTTP 503 means Amazon blocked the fetch.
HTTP 500 means the browser did not start on the server. If you get
503, say so plainly and do not pretend the search worked. Pages load
in a real browser, so each request takes a few seconds: wait for the
answer instead of retrying. Never ask the user to solve a captcha.
```

## Details de l'API

| Methode | Chemin | Usage |
| --- | --- | --- |
| GET | `/health` | Signe de vie, sans auth |
| GET | `/regions` | Codes de regions, sans auth |
| GET | `/search?query=...&region=ca&max_results=10` | Recherche de produits |
| GET | `/products?query=...` | Alias de la recherche |
| GET | `/product/{asin}` | Detail d'un produit |
| GET | `/product/{asin}/variations` | Variantes (couleur, taille, style) |
| GET | `/cart?account=personal` | Panier personnel |
| GET | `/cart?account=business` | Panier business |
| GET | `/cart/add?asin=...&quantity=1&account=personal` | Ajouter au panier |
| POST | `/cart` | Corps JSON `{"asin","quantity","region","account"}` |

## Regles

- La recherche ne demande pas de login. L'ajout au panier demande les
  cookies de session, exportes du navigateur normal de l'utilisateur.
  Les cookies vont dans `<dossier du skill>\cookies\cookies-personal.txt`
  (compte personnel), ou dans le dossier pointe par `AMAZON_COOKIE_DIR`.
  Sans jar dans ce dossier, le panier repond 409 « no cookie jar » :
  c'est qu'il manque le fichier, pas un blocage Amazon.
- Ne jamais demander le mot de passe Amazon, ne jamais tenter un login
  automatise, ne jamais passer en caisse, ne jamais demander de
  resoudre un captcha.
- La region par defaut est `ca` (amazon.ca). Les autres regions sont
  `us`, `uk`, `de`, `fr`, `es`, `it`, `nl`, `jp`, `au`, `mx`, `in`,
  `ae`, `sa`, `ie`, `be`.
- Si Amazon bloque (503), le dire clairement. Ne pas inventer de
  resultats.
