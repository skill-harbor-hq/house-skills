"""Faux serveur Amazon local et fixtures HTML, pour les tests.

Ce fichier ne touche jamais au vrai Amazon, ni au PC, ni a D1.
Les pages factices suivent la structure publique connue des pages
Amazon (resultats de recherche, page produit, panier, page de
blocage). Le faux serveur garde un panier en memoire et accepte le
POST d'ajout, comme le ferait Amazon.
"""

import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

SEARCH_HTML = """<html><body>
<div data-component-type="s-search-result" data-asin="B012345678">
  <h2><a href="/dp/B012345678"><span>USB-C Cable 2m braided</span></a></h2>
  <span class="a-price"><span class="a-offscreen">$12.99</span></span>
  <span class="a-icon-star-small"><span class="a-icon-alt">4.5 out of 5 stars</span></span>
  <a href="/dp/B012345678#customerReviews"><span>1,234</span></a>
  <img class="s-image" src="https://example.com/img.jpg">
</div>
<div data-component-type="s-search-result" data-asin="B087654321">
  <h2><a href="/dp/B087654321"><span>USB-C Charger 30W</span></a></h2>
  <span class="a-price"><span class="a-offscreen">$24.99</span></span>
</div>
</body></html>"""

PRODUCT_HTML = """<html><body>
<span id="productTitle">USB-C Cable 2m braided</span>
<div id="corePriceDisplay"><span class="a-price"><span class="a-offscreen">$12.99</span></span></div>
<a id="bylineInfo">BrandX</a>
<span id="acrCustomerReviewText">1,234 ratings</span>
<div id="availability"><span>In Stock</span></div>
<div id="feature-bullets"><ul>
<li><span class="a-list-item">Braided nylon</span></li>
<li><span class="a-list-item">2 meters</span></li>
</ul></div>
<img id="landingImage" src="https://example.com/main.jpg">
<form id="addToCart" action="/gp/aws/cart/add.html" method="post">
  <input type="hidden" name="session-id" value="FAKESESSION">
  <input type="hidden" name="ASIN" value="{asin}">
  <input type="hidden" name="offeringID" value="OFFER1">
  <input type="submit" name="submit.add-to-cart" value="Add to Cart">
</form>
</body></html>"""

PRODUCT_NO_FORM_HTML = """<html><body>
<span id="productTitle">USB-C Cable 2m braided</span>
</body></html>"""

BLOCK_HTML = """<html><head><title>Sorry</title></head><body>
<h1>Sorry, we just need to make sure you're not a robot</h1>
</body></html>"""

CART_EMPTY_HTML = """<html><body><p>Your Amazon Cart is empty</p></body></html>"""

SIGNIN_HTML = """<html><body><form name="signIn" id="ap_signin_form"></form></body></html>"""

VARIATIONS_HTML = """<html><body>
<span id="productTitle">USB-C Cable 2m braided</span>
<div id="variation_color">
<label>Color</label>
<ul>
<li title="Black" data-defaultasin="B012345678"></li>
<li title="White" data-defaultasin="B012345679"></li>
</ul>
</div>
</body></html>"""


def cart_html(items):
    rows = ""
    for asin, title, qty, price in items:
        rows += f"""<div class="sc-list-item" data-asin="{asin}">
<span class="sc-product-title">{title}</span>
<select name="quantity"><option selected>{qty}</option></select>
<span class="sc-price"><span class="a-offscreen">{price}</span></span>
</div>"""
    return f"""<html><body>{rows}
<span id="sc-subtotal-amount-buybox"><span class="a-offscreen">$12.99</span></span>
</body></html>"""


class FakeAmazon(BaseHTTPRequestHandler):
    cart_items = []
    mode = "normal"  # normal | block | signin | noform | variations | cart-marker

    def log_message(self, *args):
        pass

    def _send(self, body, code=200):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/s":
            if FakeAmazon.mode == "block":
                return self._send(BLOCK_HTML)
            return self._send(SEARCH_HTML)
        if parsed.path.startswith("/dp/"):
            if FakeAmazon.mode == "block":
                return self._send(BLOCK_HTML)
            if FakeAmazon.mode == "noform":
                return self._send(PRODUCT_NO_FORM_HTML)
            if FakeAmazon.mode == "variations":
                return self._send(VARIATIONS_HTML)
            asin = parsed.path.split("/dp/")[1].split("/")[0]
            return self._send(PRODUCT_HTML.format(asin=asin))
        if parsed.path == "/gp/cart/view.html":
            if FakeAmazon.mode == "signin":
                return self._send(SIGNIN_HTML)
            if FakeAmazon.mode == "block":
                return self._send(BLOCK_HTML)
            if not FakeAmazon.cart_items:
                body = CART_EMPTY_HTML
            else:
                body = cart_html(FakeAmazon.cart_items)
            if FakeAmazon.mode == "cart-marker":
                # Marqueur transitoire d'Amazon sur une vraie page
                # panier (regression phase 2, 2026-11-05) : le
                # contenu est la, la lecture doit passer.
                body = body.replace(
                    "</body>",
                    "<div>Something went wrong on our end</div></body>",
                )
            return self._send(body)
        self._send("not found", code=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/gp/aws/cart/add.html":
            length = int(self.headers.get("Content-Length", 0))
            fields = parse_qs(self.rfile.read(length).decode())
            asin = fields.get("ASIN", [""])[0] or fields.get("asin", [""])[0]
            qty = int(fields.get("quantity", ["1"])[0])
            FakeAmazon.cart_items = [
                (asin, "USB-C Cable 2m braided", qty, "$12.99")
            ]
            return self._send("<html><body>Added to Cart</body></html>")
        self._send("not found", code=404)


def start_fake_server():
    """Demarre le faux serveur sur un port libre. Renvoie
    (serveur, port). Le serveur tourne en tache de fond."""
    server = HTTPServer(("127.0.0.1", 0), FakeAmazon)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port
