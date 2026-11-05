"""Point d'entree : python -m harbor_amazon

Demarre le serveur sur HOST (defaut 127.0.0.1) et PORT (defaut 8792).
Le serveur ne s'expose jamais en public : il repond seulement sur
l'interface locale de la machine.
"""

from __future__ import annotations

import os

import uvicorn

from .app import create_app


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8792"))
    print(f"Harbor Amazon listening on http://{host}:{port} (localhost only)")
    uvicorn.run(create_app(), host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
