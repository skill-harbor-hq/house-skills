"""Test rapide : Chromium se lance-t-il et ouvre-t-il une page ?

Utilise par install.ps1. Sortie 0 et "Chromium OK" si le navigateur
demarre et ouvre about:blank, sinon sortie 1 avec l'erreur exacte.
Le chemin des navigateurs vient de PLAYWRIGHT_BROWSERS_PATH, sinon
du dossier standard du PC. Aucun appel reseau vers Amazon ici.
"""

import os
import sys

DEFAULT_BROWSERS_PATH = r"C:\Users\muse-build\work\tools\ms-playwright"

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", DEFAULT_BROWSERS_PATH)


async def main():
    import asyncio

    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        # channel="chromium" : force le build complet, pas le
        # headless shell (voir browser.py).
        browser = await p.chromium.launch(
            headless=True,
            channel="chromium",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = await browser.new_page()
        await page.goto("about:blank")
        await browser.close()
    print("Chromium OK")


if __name__ == "__main__":
    try:
        import asyncio

        asyncio.run(main())
    except Exception as exc:  # noqa: BLE001 - on veut l'erreur exacte
        print(f"Chromium KO : {exc}")
        sys.exit(1)
