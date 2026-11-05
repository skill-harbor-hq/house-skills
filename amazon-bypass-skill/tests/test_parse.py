"""Tests des parseurs seuls, sans navigateur et sans reseau.

Les fonctions parse_* de harbor_amazon.amazon prennent du HTML et
renvoient des donnees : on les verifie ici sur les fixtures locales
de fake_amazon.py. Si Chromium n'est pas disponible, ces tests
restent la seule verification possible sur la machine, et les tests
navigateur sont alors a faire sur le PC seulement.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fake_amazon import (
    BLOCK_HTML,
    CART_EMPTY_HTML,
    PRODUCT_HTML,
    SEARCH_HTML,
    SIGNIN_HTML,
    VARIATIONS_HTML,
    cart_html,
)
from harbor_amazon.amazon import (
    NotSignedIn,
    _is_blocked,
    parse_cart,
    parse_product,
    parse_search,
    parse_variations,
)

BASE = "https://www.amazon.ca"


def run_tests():
    passed = []

    def check(name, condition, detail=""):
        status = "OK  " if condition else "FAIL"
        print(f"[{status}] {name} {detail}")
        if condition:
            passed.append(name)
        else:
            raise AssertionError(f"FAILED: {name} {detail}")

    # 1. Recherche parsee
    results = parse_search(SEARCH_HTML, BASE, max_results=5)
    check("search 2 resultats", len(results) == 2, str(len(results)))
    first = results[0]
    check("search asin", first["asin"] == "B012345678", str(first))
    check("search titre", first["title"] == "USB-C Cable 2m braided", str(first["title"]))
    check("search prix", first["price"] == "$12.99", str(first["price"]))
    check("search note", first["rating"] == 4.5, str(first["rating"]))
    check("search avis", first["reviews"] == 1234, str(first["reviews"]))
    check("search url", first["url"] == f"{BASE}/dp/B012345678", str(first["url"]))
    check("search image", first["image"] == "https://example.com/img.jpg", str(first["image"]))
    check("search limite max_results", len(parse_search(SEARCH_HTML, BASE, max_results=1)) == 1)

    # 1b. Bloc reel amazon.ca (phase 1 v2, 2026-11-05) : le titre est
    # dans un <span> nu sous <h2>, pas dans un lien <h2><a>. Le
    # premier resultat de la phase 1 v2 sortait avec un titre vide.
    real_path = os.path.join(os.path.dirname(__file__), "real_search_block.html")
    with open(real_path, encoding="utf-8") as fh:
        real_block = fh.read()
    real_results = parse_search(real_block, BASE, max_results=5)
    check("reel 1 resultat", len(real_results) == 1, str(len(real_results)))
    check("reel asin", real_results[0]["asin"] == "B0HMHG3SSH", str(real_results[0].get("asin")))
    check("reel titre non vide", bool(real_results[0]["title"]), str(real_results[0]["title"]))
    check("reel titre cable", "USB C Fast Charging Cable" in (real_results[0]["title"] or ""), str(real_results[0]["title"]))
    check("reel prix", real_results[0]["price"] == "$11.99", str(real_results[0]["price"]))
    check("reel url dp", real_results[0]["url"] == f"{BASE}/dp/B0HMHG3SSH", str(real_results[0]["url"]))

    # 2. Produit parse
    product = parse_product(PRODUCT_HTML.format(asin="B012345678"), "B012345678", BASE)
    check("product titre", product["title"] == "USB-C Cable 2m braided", str(product["title"]))
    check("product prix", product["price"] == "$12.99", str(product["price"]))
    check("product marque", product["brand"] == "BrandX", str(product["brand"]))
    check("product avis", product["reviews"] == 1234, str(product["reviews"]))
    check("product dispo", product["availability"] == "In Stock", str(product["availability"]))
    check("product features", product["features"] == ["Braided nylon", "2 meters"], str(product["features"]))
    check("product images", product["images"] == ["https://example.com/main.jpg"], str(product["images"]))

    # 3. Variantes parsees
    groups = parse_variations(VARIATIONS_HTML)
    check("variations 1 groupe", len(groups) == 1, str(groups))
    check("variations 2 options", len(groups[0]["options"]) == 2, str(groups[0]["options"]))
    check("variations asin option", groups[0]["options"][1]["asin"] == "B012345679", str(groups[0]["options"]))

    # 4. Panier vide, puis avec article
    cart = parse_cart(CART_EMPTY_HTML)
    check("cart vide count 0", cart["count"] == 0, str(cart))
    cart = parse_cart(cart_html([("B012345678", "USB-C Cable 2m braided", 1, "$12.99")]))
    check("cart 1 article", cart["count"] == 1, str(cart))
    check("cart titre", cart["items"][0]["title"] == "USB-C Cable 2m braided", str(cart["items"]))
    check("cart sous-total", cart["subtotal"] == "$12.99", str(cart["subtotal"]))

    # 5. Page de connexion -> NotSignedIn
    try:
        parse_cart(SIGNIN_HTML)
        check("cart signin -> NotSignedIn", False)
    except NotSignedIn:
        check("cart signin -> NotSignedIn", True)

    # 6. Detection des blocages
    check("blocage marqueur robot", _is_blocked(200, BLOCK_HTML) is not None, str(_is_blocked(200, BLOCK_HTML)))
    check("blocage HTTP 503", _is_blocked(503, "<html></html>") is not None)
    check("blocage HTTP 429", _is_blocked(429, "<html></html>") is not None)
    check("page normale non bloquee", _is_blocked(200, SEARCH_HTML) is None)
    check("blocage titre Sorry", _is_blocked(200, "<html><head><title>Sorry, Amazon</title></head></html>") is not None)

    print(f"\n{len(passed)} checks passes, 0 echec.")
    return 0


if __name__ == "__main__":
    sys.exit(run_tests())
