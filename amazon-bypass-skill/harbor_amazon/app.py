"""API locale Harbor Amazon : recherche et panier Amazon pour Muse.

Code original, ecrit de zero. Un seul service, lie a 127.0.0.1
seulement, protege par une cle API locale en Bearer. La recherche ne
demande pas de login ; le panier demande les cookies de session de
l'utilisateur, exportes de son navigateur normal. Ce service ne fait
ni checkout, ni paiement, ni login automatise, et ne contient aucun
mot de passe.

V2 : les pages Amazon sont chargees par un vrai Chromium pilote par
Playwright (voir browser.py), parce que la v1 se faisait servir un
HTTP 503 direct en requete HTTP. Les endpoints sont donc async et
tournent sur la boucle d'evenements de FastAPI, avec un seul
navigateur partage.
"""

from __future__ import annotations

import hmac
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel

from .amazon import (
    AmazonBlocked,
    AmazonClient,
    AmazonFetchError,
    BrowserUnavailable,
    NotSignedIn,
    WrongAccount,
    DEFAULT_REGION,
    REGIONS,
)
from .browser import close_engine
from .cookies import Jar, jar_path_for_account, load_jar, save_jar

SERVICE_NAME = "harbor-amazon"


class CartAddBody(BaseModel):
    """Corps JSON accepte par POST /cart."""

    asin: str
    quantity: int = 1
    region: Optional[str] = None
    account: str = "personal"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Le navigateur demarre paresseusement, a la premiere requete
    # Amazon : /health reste rapide. A l'arret du serveur, on le
    # ferme proprement s'il a demarre.
    yield
    await close_engine()


def configured_key() -> Optional[str]:
    """Cle API du serveur, lue dans l'environnement. Jamais en dur."""
    for name in ("AMAZON_API_KEY", "MUSE_API_KEY", "API_KEY"):
        value = os.environ.get(name)
        if value:
            return value
    return None


def cookie_dir() -> str:
    """Dossier des jars de cookies."""
    value = os.environ.get("AMAZON_COOKIE_DIR")
    if value:
        return value
    return os.path.join(os.path.expanduser("~"), ".harbor-amazon")


def default_region() -> str:
    return os.environ.get("AMAZON_DEFAULT_REGION", DEFAULT_REGION)


def check_auth(
    authorization: Optional[str] = Header(default=None),
    x_api_key: Optional[str] = Header(default=None),
) -> None:
    """Verifie la cle Bearer. 401 si absente ou fausse, 500 si le
    serveur n'a pas de cle configuree."""
    key = configured_key()
    if not key:
        raise HTTPException(status_code=500, detail="server API key is not configured")
    supplied = None
    if authorization and authorization.lower().startswith("bearer "):
        supplied = authorization[7:].strip()
    elif x_api_key:
        supplied = x_api_key.strip()
    if not supplied or not hmac.compare_digest(supplied, key):
        raise HTTPException(status_code=401, detail="missing or wrong API key")


def load_account_jar(account: str) -> Jar:
    """Charge le jar d'un compte et verifie la session et le type."""
    if account not in ("personal", "business"):
        raise HTTPException(status_code=400, detail="account must be personal or business")
    path = jar_path_for_account(cookie_dir(), account)
    try:
        jar = load_jar(path)
    except FileNotFoundError:
        raise HTTPException(
            status_code=409,
            detail=f"no cookie jar for account {account}, export cookies first",
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if not jar.has_session():
        raise HTTPException(
            status_code=409,
            detail=f"no Amazon session in the {account} cookie jar",
        )
    if account == "personal" and jar.is_business():
        raise HTTPException(
            status_code=409,
            detail="business cookie found in the personal jar, wrong account",
        )
    if account == "business" and not jar.is_business():
        raise HTTPException(
            status_code=409,
            detail="no business cookie in the business jar, wrong account",
        )
    return jar


def make_client(region: Optional[str], jar: Optional[Jar] = None) -> AmazonClient:
    region = region or default_region()
    if region not in REGIONS:
        raise HTTPException(status_code=400, detail=f"unknown region: {region}")
    return AmazonClient(region=region, jar=jar)


def create_app() -> FastAPI:
    app = FastAPI(title="Harbor Amazon", version="0.2.0", lifespan=lifespan)

    @app.get("/health")
    def health():
        # Sans auth : simple signe de vie.
        return {"ok": True, "service": SERVICE_NAME}

    @app.get("/regions")
    def regions():
        return {"default": default_region(), "regions": sorted(REGIONS.keys())}

    @app.get("/search", dependencies=[Depends(check_auth)])
    @app.get("/products", dependencies=[Depends(check_auth)])
    async def search(
        query: str = Query(..., min_length=1),
        region: Optional[str] = Query(default=None),
        max_results: int = Query(default=16, ge=1, le=50),
    ):
        client = make_client(region)
        try:
            results = await client.search(query, max_results=max_results)
        except AmazonBlocked as exc:
            raise HTTPException(status_code=503, detail=f"Amazon blocked the fetch: {exc.reason}")
        except BrowserUnavailable as exc:
            raise HTTPException(status_code=500, detail=f"browser unavailable: {exc.reason}")
        except AmazonFetchError as exc:
            raise HTTPException(status_code=502, detail=exc.reason)
        return {"query": query, "region": client.region, "results": results}

    @app.get("/product/{asin}", dependencies=[Depends(check_auth)])
    async def product(asin: str, region: Optional[str] = Query(default=None)):
        client = make_client(region)
        try:
            details = await client.product(asin)
        except AmazonBlocked as exc:
            raise HTTPException(status_code=503, detail=f"Amazon blocked the fetch: {exc.reason}")
        except BrowserUnavailable as exc:
            raise HTTPException(status_code=500, detail=f"browser unavailable: {exc.reason}")
        except AmazonFetchError as exc:
            raise HTTPException(status_code=502, detail=exc.reason)
        return details

    @app.get("/product/{asin}/variations", dependencies=[Depends(check_auth)])
    async def product_variations(asin: str, region: Optional[str] = Query(default=None)):
        client = make_client(region)
        try:
            groups = await client.variations(asin)
        except AmazonBlocked as exc:
            raise HTTPException(status_code=503, detail=f"Amazon blocked the fetch: {exc.reason}")
        except BrowserUnavailable as exc:
            raise HTTPException(status_code=500, detail=f"browser unavailable: {exc.reason}")
        except AmazonFetchError as exc:
            raise HTTPException(status_code=502, detail=exc.reason)
        return {"asin": asin, "variations": groups}

    @app.get("/cart", dependencies=[Depends(check_auth)])
    async def read_cart(
        account: str = Query(default="personal"),
        region: Optional[str] = Query(default=None),
    ):
        jar = load_account_jar(account)
        client = make_client(region, jar=jar)
        try:
            cart = await client.read_cart()
        except NotSignedIn as exc:
            raise HTTPException(status_code=409, detail=exc.reason)
        except AmazonBlocked as exc:
            raise HTTPException(status_code=503, detail=f"Amazon blocked the fetch: {exc.reason}")
        except BrowserUnavailable as exc:
            raise HTTPException(status_code=500, detail=f"browser unavailable: {exc.reason}")
        except AmazonFetchError as exc:
            raise HTTPException(status_code=502, detail=exc.reason)
        save_jar(_sync_jar(jar, client))
        return {"account": account, **cart}

    @app.get("/cart/add", dependencies=[Depends(check_auth)])
    async def add_to_cart_get(
        asin: str = Query(...),
        quantity: int = Query(default=1, ge=1, le=99),
        account: str = Query(default="personal"),
        region: Optional[str] = Query(default=None),
    ):
        jar = load_account_jar(account)
        client = make_client(region, jar=jar)
        try:
            result = await client.add_to_cart(asin, quantity=quantity)
        except NotSignedIn as exc:
            raise HTTPException(status_code=409, detail=exc.reason)
        except WrongAccount as exc:
            raise HTTPException(status_code=409, detail=exc.reason)
        except AmazonBlocked as exc:
            raise HTTPException(status_code=503, detail=f"Amazon blocked the fetch: {exc.reason}")
        except BrowserUnavailable as exc:
            raise HTTPException(status_code=500, detail=f"browser unavailable: {exc.reason}")
        except AmazonFetchError as exc:
            raise HTTPException(status_code=502, detail=exc.reason)
        save_jar(_sync_jar(jar, client))
        return {"account": account, **result}

    @app.post("/cart", dependencies=[Depends(check_auth)])
    async def add_to_cart_post(body: CartAddBody):
        jar = load_account_jar(body.account)
        client = make_client(body.region, jar=jar)
        try:
            result = await client.add_to_cart(body.asin, quantity=body.quantity)
        except NotSignedIn as exc:
            raise HTTPException(status_code=409, detail=exc.reason)
        except WrongAccount as exc:
            raise HTTPException(status_code=409, detail=exc.reason)
        except AmazonBlocked as exc:
            raise HTTPException(status_code=503, detail=f"Amazon blocked the fetch: {exc.reason}")
        except BrowserUnavailable as exc:
            raise HTTPException(status_code=500, detail=f"browser unavailable: {exc.reason}")
        except AmazonFetchError as exc:
            raise HTTPException(status_code=502, detail=exc.reason)
        save_jar(_sync_jar(jar, client))
        return {"account": body.account, **result}

    return app


def _sync_jar(jar: Jar, client: AmazonClient) -> Jar:
    """Recopie les cookies mis a jour par les requetes dans le jar."""
    host = client.host
    for name, value in client.cookies.items():
        jar.update(name, value, host)
    return jar


app = create_app()
