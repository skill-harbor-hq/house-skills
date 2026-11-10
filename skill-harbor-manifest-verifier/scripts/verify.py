#!/usr/bin/env python3
"""Verify a Skill Harbor signed manifest (v1).

Usage:
    python3 verify.py <manifest-file-or-url> [--pubkey <file-or-url>] [--check-file <path>] [--installed-manifest <file>] [--json]

Checks, in order:
  1. status is "signed"
  2. bundle hash recomputed from per-file hashes matches bundle_hash_sha256
  3. Ed25519 signature verifies against the public key for the manifest kid
  4. (optional) one file hash verified at the pinned commit

Exit codes: 0 = PASS, 1 = FAIL, 2 = INCOMPLETE (a check was skipped, or the
manifest is unsigned). A skipped check is never a pass.

Canonical bundle hash (see references/manifest-schema.md):
  sort files by path; for each, line = path + "\\n" + sha256 + "\\n";
  SHA-256 of the concatenated lines, lowercase hex.
Signature: Ed25519 over the UTF-8 bytes of the lowercase hex bundle hash.
Public key: /.well-known/skill-harbor-signing-key.json, field "x" is the
32-byte raw public key, base64.
"""
import argparse
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
import os
import urllib.request

PUBLIC_KEY_URL = "https://theskillharbor.com/.well-known/skill-harbor-signing-key.json"
USER_AGENT = "SkillHarborManifestVerifier/1.0 (read-only manifest check)"


def load_json_source(source):
    if source.startswith("http://") or source.startswith("https://"):
        req = urllib.request.Request(source, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    with open(source, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def canonical_bundle_hash(files):
    parts = []
    for entry in sorted(files, key=lambda e: e["path"]):
        parts.append(entry["path"] + "\n" + entry["sha256"] + "\n")
    return hashlib.sha256("".join(parts).encode("utf-8")).hexdigest()


def verify_signature_cryptography(raw_key, signature, message):
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.exceptions import InvalidSignature
    except ImportError:
        return None, "cryptography library not installed"
    try:
        key = Ed25519PublicKey.from_public_bytes(raw_key)
        key.verify(signature, message)
        return True, "cryptography"
    except InvalidSignature:
        return False, "cryptography"
    except Exception as exc:
        return None, "cryptography error: %s" % exc


def verify_signature_nacl(raw_key, signature, message):
    try:
        from nacl.signing import VerifyKey
        from nacl.exceptions import BadSignatureError
    except ImportError:
        return None, "nacl library not installed"
    try:
        vk = VerifyKey(raw_key)
        vk.verify(message, signature)
        return True, "nacl"
    except BadSignatureError:
        return False, "nacl"
    except Exception as exc:
        return None, "nacl error: %s" % exc


def verify_signature_openssl(raw_key, signature, message):
    # Build DER SubjectPublicKeyInfo for Ed25519: 302a300506032b6570032100 + key
    der = bytes.fromhex("302a300506032b6570032100") + raw_key
    pem = "-----BEGIN PUBLIC KEY-----\n"
    pem += base64.encodebytes(der).decode("ascii")
    pem += "-----END PUBLIC KEY-----\n"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            pub_path = os.path.join(tmp, "pub.pem")
            msg_path = os.path.join(tmp, "msg.bin")
            sig_path = os.path.join(tmp, "sig.bin")
            with open(pub_path, "w", encoding="ascii") as f:
                f.write(pem)
            with open(msg_path, "wb") as f:
                f.write(message)
            with open(sig_path, "wb") as f:
                f.write(signature)
            proc = subprocess.run(
                ["openssl", "pkeyutl", "-verify", "-pubin", "-inkey", pub_path,
                 "-rawin", "-in", msg_path, "-sigfile", sig_path],
                capture_output=True, text=True, timeout=30)
            if proc.returncode == 0:
                return True, "openssl"
            return False, "openssl: %s" % (proc.stderr.strip() or proc.stdout.strip())
    except FileNotFoundError:
        return None, "openssl not found"
    except Exception as exc:
        return None, "openssl error: %s" % exc


def verify_signature(raw_key, signature, message):
    for fn in (verify_signature_cryptography, verify_signature_nacl, verify_signature_openssl):
        ok, how = fn(raw_key, signature, message)
        if ok is not None:
            return ok, how
    return None, "no Ed25519 verifier available (install cryptography: pip install cryptography)"


def main():
    parser = argparse.ArgumentParser(description="Verify a Skill Harbor signed manifest (v1).")
    parser.add_argument("manifest", help="manifest JSON file path or https:// URL")
    parser.add_argument("--pubkey", default=None,
                        help="public key JSON file path or URL (default: fetch the well-known key)")
    parser.add_argument("--check-file", default=None,
                        help="verify this one file hash at the pinned commit (needs network)")
    parser.add_argument("--installed-manifest", default=None,
                        help="previously installed manifest JSON, for a diff report")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON result")
    args = parser.parse_args()

    checks = []
    try:
        manifest = load_json_source(args.manifest)
    except Exception as exc:
        print("FAIL: cannot load manifest: %s" % exc)
        return 1

    slug = manifest.get("slug", "?")
    status = manifest.get("status")
    if status == "signed":
        checks.append(("status", "pass", "signed"))
    else:
        checks.append(("status", "fail", "status is %r, not signed" % status))

    bundle_hash = manifest.get("bundle_hash_sha256", "")
    files = manifest.get("files", [])
    try:
        recomputed = canonical_bundle_hash(files)
        if recomputed == bundle_hash:
            checks.append(("bundle_hash", "pass", recomputed[:8]))
        else:
            checks.append(("bundle_hash", "fail",
                           "recomputed %s != manifest %s" % (recomputed, bundle_hash)))
    except Exception as exc:
        checks.append(("bundle_hash", "fail", "cannot recompute: %s" % exc))
        recomputed = None

    # Signature
    sig = manifest.get("signature") or {}
    sig_value = sig.get("value")
    kid = sig.get("kid")
    if not sig_value or sig.get("alg") != "Ed25519":
        checks.append(("signature", "fail", "no Ed25519 signature in manifest"))
    else:
        raw_key = None
        key_note = ""
        try:
            if args.pubkey:
                key_doc = load_json_source(args.pubkey)
            else:
                key_doc = load_json_source(PUBLIC_KEY_URL)
            # key_doc may be a single key, or {"keys": [...]}
            candidates = key_doc.get("keys", [key_doc]) if isinstance(key_doc, dict) else []
            for cand in candidates:
                if cand.get("kid") == kid or (kid is None and cand.get("crv") == "Ed25519"):
                    raw_key = base64.b64decode(cand["x"])
                    break
            if raw_key is None and candidates:
                # Single-key doc without matching kid: use it but note the mismatch.
                cand = candidates[0]
                raw_key = base64.b64decode(cand["x"])
                key_note = " (kid mismatch: manifest %s, key %s)" % (kid, cand.get("kid"))
        except Exception as exc:
            checks.append(("signature", "skipped", "public key unavailable: %s" % exc))
            raw_key = None
        if raw_key is not None:
            try:
                signature = base64.b64decode(sig_value)
                message = bundle_hash.encode("utf-8")
                ok, how = verify_signature(raw_key, signature, message)
                if ok is True:
                    checks.append(("signature", "pass", "verified with %s%s" % (how, key_note)))
                elif ok is False:
                    checks.append(("signature", "fail", "signature invalid (%s)%s" % (how, key_note)))
                else:
                    checks.append(("signature", "skipped", "%s%s" % (how, key_note)))
            except Exception as exc:
                checks.append(("signature", "fail", "cannot verify: %s" % exc))

    # Optional file check at the pin
    if args.check_file:
        entry = next((e for e in files if e["path"] == args.check_file), None)
        repo = manifest.get("repo")
        pin = manifest.get("pinned_commit")
        if entry is None:
            checks.append(("file_at_pin", "fail", "%s not in manifest" % args.check_file))
        elif not repo or not pin:
            checks.append(("file_at_pin", "skipped", "no repo or pinned commit in manifest"))
        else:
            url = "https://raw.githubusercontent.com/%s/%s/%s" % (repo, pin, args.check_file)
            try:
                data = fetch_bytes(url)
                digest = hashlib.sha256(data).hexdigest()
                if digest == entry["sha256"]:
                    checks.append(("file_at_pin", "pass", "%s matches" % args.check_file))
                else:
                    checks.append(("file_at_pin", "fail",
                                   "%s: live %s != manifest %s" % (args.check_file, digest, entry["sha256"])))
            except Exception as exc:
                checks.append(("file_at_pin", "skipped", "cannot fetch raw file: %s" % exc))

    # Diff against an installed manifest, if given
    diff = None
    if args.installed_manifest:
        try:
            old = load_json_source(args.installed_manifest)
            old_files = {e["path"]: e["sha256"] for e in old.get("files", [])}
            new_files = {e["path"]: e["sha256"] for e in files}
            diff = {
                "from_version": old.get("version"),
                "to_version": manifest.get("version"),
                "files_added": sorted(set(new_files) - set(old_files)),
                "files_removed": sorted(set(old_files) - set(new_files)),
                "files_changed": sorted(p for p in set(old_files) & set(new_files)
                                        if old_files[p] != new_files[p]),
                "requires_reconsent": old.get("bundle_hash_sha256") != bundle_hash,
            }
        except Exception as exc:
            diff = {"error": str(exc)}

    failed = [c for c in checks if c[1] == "fail"]
    skipped = [c for c in checks if c[1] == "skipped"]
    verdict = "FAIL" if failed else ("INCOMPLETE" if skipped else "PASS")
    exit_code = 1 if failed else (2 if skipped else 0)

    result = {
        "slug": slug,
        "verdict": verdict,
        "version": manifest.get("version"),
        "bundle_hash_sha256": bundle_hash,
        "status": status,
        "checks": [{"name": n, "result": r, "detail": d} for n, r, d in checks],
        "permissions": manifest.get("permissions"),
        "cost": manifest.get("cost"),
        "diff": diff,
        "listing_url": (manifest.get("links") or {}).get("listing"),
    }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("%s: %s (version %s, status %s)" % (verdict, slug, manifest.get("version"), status))
        for name, res, detail in checks:
            print("  [%s] %s: %s" % (res.upper(), name, detail))
        perms = manifest.get("permissions") or {}
        print("  permissions: runs_code=%s writes=%s domains=%s needs_key=%s needs_account=%s (source %s)" % (
            perms.get("runs_code"), perms.get("writes"), perms.get("network_domains"),
            perms.get("needs_api_key"), perms.get("needs_account"), perms.get("source")))
        cost = manifest.get("cost") or {}
        print("  cost: %s" % cost.get("price"))
        if diff:
            print("  diff: requires_reconsent=%s added=%s removed=%s changed=%s" % (
                diff.get("requires_reconsent"), diff.get("files_added"),
                diff.get("files_removed"), diff.get("files_changed")))
        if verdict == "PASS":
            print("  This exact code, at this hash, matches the signed manifest, for the checks that ran.")
        elif verdict == "INCOMPLETE":
            print("  Some checks were skipped. This is not a pass.")
        else:
            print("  Do not install this version as verified.")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
