---
name: "private-rss-feed"
description: "Serve a private RSS/Atom feed from a Cloudflare Worker: token-gated (?token=), 404-disguised on bad tokens, never a static file, with a private stats line for the subscriber. Use when a feed must stay private (internal dashboards, paid subscribers, personal briefings)."
---

# Private RSS Feed

## Purpose
Some feeds must not be public: internal changelogs, subscriber-only
updates, personal briefings. Serve the feed **live from your worker**,
gated by a per-feed secret token — never as a static file, never linked
with `<link rel="alternate">`. A wrong or missing token gets a quiet 404,
indistinguishable from "no feed here".

## Workflow
1. **Secret** — generate with `openssl rand -hex 32`, store in the
   worker's secrets table (e.g. D1 `app_secrets` key `'feed'`). The token
   is also needed by any health-check job — keep a copy somewhere safe
   but private.
2. **Route** — `GET /feed.xml` (and localized variants) handled live by
   the worker: read `?token=`, compare against the secret in constant
   time, return `404 'Not found'` on mismatch. Valid token → build the
   feed from the live database (latest N items).
3. **Private extras** — the feed can carry subscriber-only lines a public
   feed never would (e.g. "yesterday vs day-before traffic", unpublished
   counts). Keep them clearly useful, never sensitive.
4. **Hygiene** — no static feed file in the build, no autodiscovery link
   tag, no token in URLs you share publicly. If the token leaks:
   regenerate, update the secret store, update the subscriber's URL.

## Output Contract
- `GET /feed.xml` without token → `404`, plain text, no hint a feed exists.
- `GET /feed.xml?token=WRONG` → same `404`.
- `GET /feed.xml?token=RIGHT` → valid RSS 2.0, correct
  `Content-Type: application/rss+xml`, items newest-first with RFC-2822
  dates.

## Operating Rules
1. **Never a static file.** A static `feed.xml` in the build output is
   one deploy away from being public.
2. Compare tokens in constant time; don't leak "token exists but wrong"
   vs "no token" — both are the same 404.
3. Escape all item content for XML (`&`, `<`, `>`, quotes).
4. Fail-open on the private stats line: if the stats query errors, the
   feed still returns valid without it.
5. Binding changes (like worker secrets) require a redeploy on Pages —
   secrets bind at deploy time.

See `references/worker-feed.md` for the handler skeleton.
