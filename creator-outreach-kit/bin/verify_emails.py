#!/usr/bin/env python3
"""Verify collected emails: syntax check + MX/A record lookup via dig. Free, DIY.

Usage: verify_emails.py profiles.json --out emails-verified.json
profiles.json: {"seller_id": {"github_login": "...", "seller_name": "...", "email": "..."}}
Writes: [{"seller_id": ..., "github_login": ..., "email": ..., "syntax_ok": bool,
          "mx_ok": bool, "valid": bool}]
"""
from __future__ import annotations
import argparse, json, re, subprocess

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def has_mx(domain: str) -> bool:
    for rtype in ("MX", "A"):
        try:
            out = subprocess.run(["dig", "+short", rtype, domain],
                                 capture_output=True, text=True, timeout=15).stdout.strip()
            if out:
                return True
        except Exception:
            pass
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profiles")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    profiles = json.load(open(args.profiles))
    mx_cache: dict[str, bool] = {}
    results = []
    for sid, p in profiles.items():
        email = (p.get("email") or "").strip()
        if not email:
            continue
        ok_syntax = bool(EMAIL_RE.match(email))
        domain = email.split("@")[-1].lower() if "@" in email else ""
        if domain not in mx_cache:
            mx_cache[domain] = has_mx(domain) if domain else False
        results.append({
            "seller_id": sid,
            "seller_name": p.get("seller_name"),
            "github_login": p.get("github_login"),
            "email": email,
            "syntax_ok": ok_syntax,
            "mx_ok": mx_cache[domain],
            "valid": ok_syntax and mx_cache[domain],
        })
    json.dump(results, open(args.out, "w"), indent=1)
    n_valid = sum(1 for r in results if r["valid"])
    print(f"checked: {len(results)}, valid: {n_valid}")

if __name__ == "__main__":
    main()
