"""Lecture et ecriture des jars de cookies au format Netscape.

Un jar Netscape est un fichier texte, une ligne par cookie :
domaine, flag, chemin, secure, expiration, nom, valeur, separes par
des tabulations. La premiere ligne est :
    # Netscape HTTP Cookie File

Ces cookies viennent d'une session ouverte dans le navigateur normal de
l'utilisateur. Le fichier ne doit jamais quitter la machine locale, ne
jamais etre colle dans un chat, et doit etre supprime apres un test.
Ce module ne fait que lire et ecrire le fichier, il ne se connecte
jamais a Amazon et ne contient aucun secret.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

HEADER = "# Netscape HTTP Cookie File"

# Cookies qui prouvent qu'une session Amazon est ouverte. Le suffixe
# varie selon la place de marche : "main" sur amazon.com, "acbca" sur
# amazon.ca (verifie 2026-11-05 sur un vrai jar .ca : at-acbca,
# sess-at-acbca, x-acbca), et d'autres suffixes ailleurs. Le critere
# est donc la famille at-/sess-at-/x- suivie d'un suffixe, pas le nom
# exact .com.
_SESSION_COOKIE_RE = re.compile(r"^(at|sess-at|x)-[a-z]+$")

# Cookie present seulement dans une session Amazon Business.
BUSINESS_COOKIE = "b2b"


@dataclass
class Cookie:
    """Un seul cookie d'un jar Netscape."""

    domain: str
    flag: str
    path: str
    secure: str
    expires: str
    name: str
    value: str


@dataclass
class Jar:
    """Un jar de cookies charge en memoire."""

    path: str
    cookies: list = field(default_factory=list)

    def as_dict(self) -> dict:
        """Les cookies sous forme de dictionnaire nom -> valeur."""
        return {c.name: c.value for c in self.cookies}

    def has_session(self) -> bool:
        """Vrai si un marqueur de session Amazon est present."""
        return any(_SESSION_COOKIE_RE.match(c.name) for c in self.cookies)

    def is_business(self) -> bool:
        """Vrai si le cookie business est present."""
        return BUSINESS_COOKIE in self.as_dict()

    def update(self, name: str, value: str, domain: str) -> None:
        """Ajoute ou remplace un cookie, en gardant ses metadonnees."""
        for cookie in self.cookies:
            if cookie.name == name and cookie.domain == domain:
                cookie.value = value
                return
        self.cookies.append(
            Cookie(
                domain=domain,
                flag="TRUE",
                path="/",
                secure="TRUE",
                expires="0",
                name=name,
                value=value,
            )
        )


def load_jar(path: str) -> Jar:
    """Charge un jar Netscape depuis le disque.

    Leve FileNotFoundError si le fichier est absent, et ValueError si
    le contenu n'est pas au format Netscape.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"cookie jar not found: {path}")
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        lines = handle.read().splitlines()
    if not lines or not lines[0].startswith("# Netscape HTTP Cookie File"):
        raise ValueError(f"not a Netscape cookie file: {path}")
    jar = Jar(path=path)
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 7:
            parts = line.split()
        if len(parts) < 7:
            continue
        jar.cookies.append(
            Cookie(
                domain=parts[0],
                flag=parts[1],
                path=parts[2],
                secure=parts[3],
                expires=parts[4],
                name=parts[5],
                value=parts[6],
            )
        )
    return jar


def save_jar(jar: Jar) -> None:
    """Reecrit le jar sur le disque, au format Netscape."""
    lines = [HEADER, ""]
    for cookie in jar.cookies:
        fields = [
            cookie.domain,
            cookie.flag,
            cookie.path,
            cookie.secure,
            cookie.expires,
            cookie.name,
            cookie.value,
        ]
        lines.append("\t".join(fields))
    with open(jar.path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def jar_path_for_account(cookie_dir: str, account: str) -> str:
    """Chemin du jar pour un compte (personal ou business)."""
    return os.path.join(cookie_dir, f"cookies-{account}.txt")
