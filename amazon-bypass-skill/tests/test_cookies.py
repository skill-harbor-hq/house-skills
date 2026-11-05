"""Tests du jar de cookies seul, sans navigateur et sans reseau.

Verifie surtout has_session() : le suffixe des cookies de session
varie selon la place de marche (main sur .com, acbca sur .ca), et un
jar .ca reel doit passer comme un jar .com. Aucune valeur de cookie
n'est jamais affichee ici : les fixtures n'utilisent que des noms.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from harbor_amazon.cookies import Cookie, Jar, load_jar


def _cookie(name):
    return Cookie(
        domain=".amazon.ca",
        flag="TRUE",
        path="/",
        secure="TRUE",
        expires="0",
        name=name,
        value="FAKE",
    )


def run_tests():
    passed = []

    def check(name, condition, detail=""):
        status = "OK  " if condition else "FAIL"
        passed.append(condition)
        print(f"[{status}] {name} {detail}")

    check("session .com sess-at-main", Jar(path="x", cookies=[_cookie("sess-at-main")]).has_session())
    check("session .com at-main", Jar(path="x", cookies=[_cookie("at-main")]).has_session())
    check("session .com x-main", Jar(path="x", cookies=[_cookie("x-main")]).has_session())
    check("session .ca sess-at-acbca", Jar(path="x", cookies=[_cookie("sess-at-acbca")]).has_session())
    check("session .ca at-acbca", Jar(path="x", cookies=[_cookie("at-acbca")]).has_session())
    check("session .ca x-acbca", Jar(path="x", cookies=[_cookie("x-acbca")]).has_session())
    check(
        "pas de session avec session-id seul",
        not Jar(path="x", cookies=[_cookie("session-id"), _cookie("session-token")]).has_session(),
    )
    check("pas de session jar vide", not Jar(path="x", cookies=[]).has_session())
    check(
        "business detecte",
        Jar(path="x", cookies=[_cookie("sess-at-main"), _cookie("b2b")]).is_business(),
    )
    check(
        "pas business sans b2b",
        not Jar(path="x", cookies=[_cookie("sess-at-main")]).is_business(),
    )

    # Chargement d'un vrai fichier Netscape avec des noms .ca.
    jar_text = (
        "# Netscape HTTP Cookie File\n"
        ".amazon.ca\tTRUE\t/\tTRUE\t0\tsess-at-acbca\tFAKE\n"
        ".amazon.ca\tTRUE\t/\tTRUE\t0\tsession-id\tFAKE\n"
    )
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
        handle.write(jar_text)
        tmp = handle.name
    try:
        jar = load_jar(tmp)
        check("load_jar .ca a une session", jar.has_session())
        check("load_jar .ca 2 cookies", len(jar.cookies) == 2)
    finally:
        os.unlink(tmp)

    ok = sum(passed)
    print(f"\n{ok} checks passes, {len(passed) - ok} echec.")
    return all(passed)


if __name__ == "__main__":
    sys.exit(0 if run_tests() else 1)
