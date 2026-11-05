"""Tests de Harbor Amazon v2 contre un faux serveur Amazon local,
avec un VRAI Chromium pilote par Playwright.

Ce fichier ne touche jamais au vrai Amazon, ni au PC, ni a D1.
Il demarre un faux serveur Amazon (pages HTML factices avec la
structure publique connue des pages Amazon), puis il appelle la
vraie application FastAPI avec httpx, comme le ferait Muse.

Ce qui est verifie ici :
  - /health 200 sans auth
  - /search renvoie des resultats parses depuis du HTML factice
  - 401 sans cle, 401 avec une mauvaise cle
  - 409 sur /cart/add sans cookies, 409 avec un jar sans session
  - 503 quand le faux Amazon sert une page de blocage
  - /cart avec un faux jar de session, /cart/add qui ajoute
    (clic sur le vrai bouton, dans le navigateur)
  - /product/{asin}/variations
  - 409 quand la page produit n'a pas de formulaire d'ajout
  - 409 quand le panier demande de se connecter
  - /regions

Si Chromium n'est pas disponible sur la machine de test, le fichier
l'indique clairement et s'arrete proprement (sortie 0) : les tests
navigateur sont alors a faire sur le PC seulement. Les parseurs,
eux, sont testes sans navigateur dans test_parse.py.

Ce qui reste NON verifie (a faire sur le PC, phases 1 et 2) :
  - les selecteurs HTML contre les vraies pages Amazon
  - la page interstitielle Akamai reelle
  - l'ajout reel au panier sur amazon.ca
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

from fake_amazon import FakeAmazon, start_fake_server

# Le faux serveur est sur 127.0.0.1 : les jars de test utilisent ce
# domaine, pour que le navigateur envoie bien les cookies au faux
# serveur (un cookie pour .amazon.ca ne serait pas envoye a
# 127.0.0.1).
FAKE_DOMAIN = "127.0.0.1"


def write_jar(path, lines):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# Netscape HTTP Cookie File\n")
        for name, value in lines:
            handle.write(
                f"{FAKE_DOMAIN}\tTRUE\t/\tTRUE\t1893456000\t{name}\t{value}\n"
            )


async def run_tests():
    server, port = start_fake_server()

    tmpdir = "/tmp/hb-test-cookies-v2"
    os.makedirs(tmpdir, exist_ok=True)
    # Menage : un run precedent laisse des jars valides, ce qui fausserait
    # le test "sans jar -> 409".
    for name in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, name))
    os.environ["HARBOR_AMAZON_BASE_URL"] = f"http://127.0.0.1:{port}"
    os.environ["AMAZON_API_KEY"] = "testkey1234567890"
    os.environ["AMAZON_COOKIE_DIR"] = tmpdir
    os.environ["AMAZON_DEFAULT_REGION"] = "ca"

    # 0. Le navigateur est-il disponible ? Sinon, on s'arrete ici,
    # proprement : les tests navigateur sont pour le PC seulement.
    from harbor_amazon.browser import BrowserStartError, get_engine

    engine = get_engine()
    try:
        await engine.start()
    except BrowserStartError as exc:
        print("NAVIGATEUR INDISPONIBLE : " + exc.reason)
        print("Tests navigateur ignores (PC seulement). Voir test_parse.py")
        print("pour les parseurs, testables sans navigateur.")
        server.shutdown()
        return 0
    print("Navigateur demarre (vrai Chromium).")

    import httpx

    from harbor_amazon.app import create_app

    passed = []

    def check(name, condition, detail=""):
        status = "OK  " if condition else "FAIL"
        print(f"[{status}] {name} {detail}")
        if condition:
            passed.append(name)
        else:
            raise AssertionError(f"FAILED: {name} {detail}")

    key = {"Authorization": "Bearer testkey1234567890"}
    transport = httpx.ASGITransport(app=create_app())
    # Delai large : une page dans un vrai navigateur prend quelques
    # secondes, et une page de blocage attend le selecteur 10 s.
    # base_url : ASGITransport exige une URL de base pour les chemins
    # relatifs, meme si rien ne sort sur le reseau.
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver", timeout=120.0
    ) as client:
        # 1. /health sans auth
        r = await client.get("/health")
        check("health 200 sans auth", r.status_code == 200, str(r.json()))
        check("health service harbor-amazon", r.json().get("service") == "harbor-amazon")

        # 2. /search sans cle -> 401
        r = await client.get("/search?query=usb+cable")
        check("search sans cle -> 401", r.status_code == 401, str(r.status_code))

        # 3. /search avec mauvaise cle -> 401
        r = await client.get(
            "/search?query=usb+cable", headers={"Authorization": "Bearer wrong"}
        )
        check("search mauvaise cle -> 401", r.status_code == 401, str(r.status_code))

        # 4. /search avec cle -> resultats parses (vrai navigateur)
        r = await client.get("/search?query=usb+cable&max_results=5", headers=key)
        data = r.json()
        check("search 200", r.status_code == 200, str(r.status_code))
        check("search 2 resultats", len(data["results"]) == 2, str(len(data["results"])))
        first = data["results"][0]
        check("search asin", first["asin"] == "B012345678", str(first))
        check("search titre", first["title"] == "USB-C Cable 2m braided", str(first["title"]))
        check("search prix", first["price"] == "$12.99", str(first["price"]))
        check("search note", first["rating"] == 4.5, str(first["rating"]))
        check("search avis", first["reviews"] == 1234, str(first["reviews"]))
        check("search region ca", data["region"] == "ca", str(data["region"]))

        # 5. /product
        r = await client.get("/product/B012345678", headers=key)
        data = r.json()
        check("product 200", r.status_code == 200, str(r.status_code))
        check("product titre", data["title"] == "USB-C Cable 2m braided", str(data["title"]))
        check("product marque", data["brand"] == "BrandX", str(data["brand"]))
        check("product features", data["features"] == ["Braided nylon", "2 meters"], str(data["features"]))

        # 6. /product/{asin}/variations
        FakeAmazon.mode = "variations"
        r = await client.get("/product/B012345678/variations", headers=key)
        data = r.json()
        check("variations 200", r.status_code == 200, str(r.status_code))
        check("variations 1 groupe", len(data["variations"]) == 1, str(data))
        check(
            "variations 2 options",
            len(data["variations"][0]["options"]) == 2,
            str(data["variations"]),
        )
        FakeAmazon.mode = "normal"

        # 7. /cart/add sans cookies -> 409
        r = await client.get(
            "/cart/add?asin=B012345678&quantity=1&account=personal", headers=key
        )
        check("cart/add sans jar -> 409", r.status_code == 409, str(r.status_code))

        # 8. /cart avec jar sans session -> 409
        jar_path = os.path.join(tmpdir, "cookies-personal.txt")
        write_jar(jar_path, [("some-cookie", "VALUE")])
        r = await client.get("/cart?account=personal", headers=key)
        check("cart jar sans session -> 409", r.status_code == 409, str(r.status_code))

        # 9. /cart avec jar de session, panier vide
        write_jar(jar_path, [("sess-at-main", "FAKESESSION")])
        FakeAmazon.cart_items = []
        r = await client.get("/cart?account=personal", headers=key)
        check("cart vide 200", r.status_code == 200, str(r.status_code))
        check("cart vide count 0", r.json()["count"] == 0, str(r.json()))

        # 10. /cart/add avec session -> ajoute (clic dans le navigateur)
        r = await client.get(
            "/cart/add?asin=B012345678&quantity=1&account=personal", headers=key
        )
        data = r.json()
        check("cart/add 200", r.status_code == 200, str(r.status_code))
        check("cart/add added", data.get("added") is True, str(data))
        check("cart/add count 1", data.get("cart_count") == 1, str(data))

        # 11. jar business dans le fichier personal -> 409
        write_jar(jar_path, [("sess-at-main", "FAKESESSION"), ("b2b", "1")])
        r = await client.get(
            "/cart/add?asin=B012345678&quantity=1&account=personal", headers=key
        )
        check("cart/add jar business en personal -> 409", r.status_code == 409, str(r.status_code))

        # 12. page de blocage -> 503
        write_jar(jar_path, [("sess-at-main", "FAKESESSION")])
        FakeAmazon.mode = "block"
        r = await client.get("/search?query=usb+cable", headers=key)
        check("search page bloquee -> 503", r.status_code == 503, str(r.status_code))
        FakeAmazon.mode = "normal"

        # 13. produit sans formulaire -> 409 (pas de session valide)
        FakeAmazon.mode = "noform"
        r = await client.get(
            "/cart/add?asin=B012345678&quantity=1&account=personal", headers=key
        )
        check("cart/add sans formulaire -> 409", r.status_code == 409, str(r.status_code))
        FakeAmazon.mode = "normal"

        # 14. panier qui demande de se connecter -> 409
        FakeAmazon.mode = "signin"
        r = await client.get("/cart?account=personal", headers=key)
        check("cart signin -> 409", r.status_code == 409, str(r.status_code))
        FakeAmazon.mode = "normal"

        # 15. panier avec marqueur transitoire -> 200 (regression
        # phase 2, 2026-11-05 : l'ajout avait passe mais la
        # confirmation repondait 503 parce que la page panier
        # portait le marqueur tout en contenant l'article)
        FakeAmazon.mode = "cart-marker"
        FakeAmazon.cart_items = [("B012345678", "USB-C Cable 2m braided", 1, "$12.99")]
        r = await client.get("/cart?account=personal", headers=key)
        check("cart marqueur 200", r.status_code == 200, str(r.status_code))
        check("cart marqueur count 1", r.json()["count"] == 1, str(r.json()))

        # 16. panier vide avec marqueur transitoire -> 200
        FakeAmazon.cart_items = []
        r = await client.get("/cart?account=personal", headers=key)
        check("cart vide marqueur 200", r.status_code == 200, str(r.status_code))
        check("cart vide marqueur count 0", r.json()["count"] == 0, str(r.json()))
        FakeAmazon.mode = "normal"

        # 17. panier vraiment bloque -> 503 (le marqueur seul, sans
        # contenu panier, reste un blocage)
        FakeAmazon.mode = "block"
        r = await client.get("/cart?account=personal", headers=key)
        check("cart bloque -> 503", r.status_code == 503, str(r.status_code))
        FakeAmazon.mode = "normal"

        # 18. /regions
        r = await client.get("/regions")
        check("regions defaut ca", r.json().get("default") == "ca", str(r.json()))
        check("regions contient us", "us" in r.json()["regions"], str(r.json()))

    server.shutdown()
    print(f"\n{len(passed)} checks passes, 0 echec.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(run_tests()))
