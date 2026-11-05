"""Harbor Amazon : recherche et panier Amazon.ca pour Muse.

API locale seulement, liee a 127.0.0.1, protegee par une cle Bearer.
Recherche sans login, panier avec les cookies de session de
l'utilisateur. Aucun checkout, aucun paiement, aucun login automatise.
V2 : les pages sont chargees par un vrai Chromium pilote par Playwright.
"""

__version__ = "0.2.0"

from .amazon import AmazonClient, DEFAULT_REGION, REGIONS  # noqa: F401
from .app import create_app  # noqa: F401
