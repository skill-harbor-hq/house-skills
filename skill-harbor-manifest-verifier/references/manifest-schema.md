# Manifest v1 schema (Skill Harbor consent manifests, Phase 1)

Source: `~/workspace/your_files/skill-harbor-consent-manifests/spec-phase-1.md` and `spec-phase-2.md`. This file pins down the exact details a verifier needs. If the live server disagrees with this file, the server is the authority and this file must be updated, never worked around silently.

## Endpoints

- Manifest: `GET https://theskillharbor.com/api/manifest/<slug>`
- Diff (Phase 2): `GET https://theskillharbor.com/api/manifest/<slug>/diff?from=<bundle_hash>`
- Connection manifest: `GET https://theskillharbor.com/connect/manifest.json`
- Public key: `GET https://theskillharbor.com/.well-known/skill-harbor-signing-key.json`
- MCP: `POST https://theskillharbor.com/mcp`, tools `search_builds`, `get_build`, `get_install` (v1), `get_install_package` (v2).

## Manifest v1 fields

| Field | Meaning |
|---|---|
| `manifest_version` | Integer, 1 for v1. |
| `slug` | Listing slug, exactly as in the URL. |
| `status` | `signed`, `unsigned-unpinned`, `revoked`, `suspended`. Only `signed` gives the signed-build badge. |
| `version` | First 8 characters of `bundle_hash_sha256`. Display only. Verification always uses the full hash. |
| `bundle_hash_sha256` | Lowercase hex SHA-256 of the file list, computed by the canonical algorithm below. |
| `pinned_commit` | Full commit SHA the files were read at. Empty when unpinned. |
| `repo` | `owner/repo`. Empty when unpinned. |
| `publisher` | `Skill Harbor`. The signer is Skill Harbor, not the seller. |
| `signature` | `{ alg: "Ed25519", kid: "sh-sign-...", value: "base64..." }`. |
| `files` | Array of `{ path, sha256, bytes }`. `path` is relative to the repository root (not to the skill folder, not to any subfolder), forward slashes. `sha256` is lowercase hex. |
| `permissions` | `{ source: "declared+scanned", runs_code: bool, writes: ["skill_dir" \| "none" \| "unknown"], network_domains: [string], needs_api_key: bool, needs_account: bool }`. |
| `cost` | `{ price: "Free" \| "...", paid_note: string \| null }`. |
| `changelog` | Array of `{ version, date, summary }`, one entry per manifest version. |
| `links` | `{ listing, repo }`. |

## Canonical bundle-hash algorithm

This is the exact algorithm. The server and the verifier must use the same one, byte for byte.

1. Sort `files` by `path`, ascending, byte order.
2. For each file, in that order, build one line: `path + "\n" + sha256 + "\n"`, UTF-8.
3. Concatenate all lines, in sorted order, with no extra header, footer, or separator.
4. SHA-256 of those bytes, lowercase hex. That is `bundle_hash_sha256`.

Use `path` and `sha256` exactly as written in the manifest, lowercase, with no normalisation (no `./` removed, no backslash converted). Sort by the UTF-8 bytes of `path`. `path` is relative to the repository root: for a skill in a subfolder, the path includes that subfolder (e.g. `my-skill/SKILL.md`, not `SKILL.md`). A verifier that resolves a path against the skill folder instead of the repo root will fetch the wrong file (or 404) at the pin. Empty `files` list: SHA-256 of the empty string. Duplicate paths: undefined, the generator must never produce them. (Clarified 2026-11-10 after an independent re-implementation: the Phase 1 spec alone was ambiguous on separators and case; this file and the spec now use the same exact wording.)

Example, two files:
- `SKILL.md`, sha256 `11aa...`
- `scripts/run.py`, sha256 `22bb...`

Input bytes:
```
SKILL.md\n11aa...\nscripts/run.py\n22bb...\n
```
SHA-256 of that input is the bundle hash. `scripts/verify.py` implements exactly this.

## Signature rules

- Algorithm: Ed25519. `signature.alg` is always `"Ed25519"`.
- What is signed: the UTF-8 bytes of the lowercase hex `bundle_hash_sha256` string. Not the raw 32 hash bytes, not the JSON. Sign the hex string.
- `signature.value`: base64 of the 64-byte Ed25519 signature.
- Public key: published at `/.well-known/skill-harbor-signing-key.json` as `{ kty: "OKP", crv: "Ed25519", kid: "...", x: "base64..." }`, where `x` is the 32-byte raw public key, base64.
- Verification: decode `x` (32 bytes) and `value` (64 bytes), verify the signature over the UTF-8 bytes of the hex bundle hash. Key rotation uses a new `kid`. An old `kid` stays published for 30 days so old manifests stay verifiable.
- If no verifier is available, the signature check is SKIPPED, never passed.

## Status meanings

- `signed`: all checks are possible, manifest is signed. The signed-build badge may be shown.
- `unsigned-unpinned`: no verified pin, no signature, no badge. The manifest is still served, with this status stated plainly.
- `revoked` / `suspended`: do not install. Warn even if the hashes still match. Check `/api/manifest/<slug>/status` for the reason.

## Permissions v1, read honestly

- `source` is always `declared+scanned`.
- `network_domains` lists domains detected by scan plus seller declaration. Empty means none detected, not a guarantee of no network call.
- `writes` is one of `skill_dir`, `none`, `unknown`. No free text.
- Permissions are information in v1 and v2. They become enforced only in Phase 3, on the platform, when the scan is precise enough. Never present them as enforced before then.

## Diff (Phase 2)

`GET /api/manifest/<slug>/diff?from=<bundle_hash>` returns `from_version`, `to_version`, `requires_reconsent`, `files_added`, `files_removed`, `files_changed`, `permissions_changed`, `tools_changed`, `changelog_new`. `requires_reconsent` is true when any file, permission or tool changed. No diff, no change. A yes for one version never covers another version.
