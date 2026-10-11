---
name: "beta-gate"
description: "Ship unfinished features to staging but never to production: a build-time flag that strips beta UI from prod builds, plus a runtime worker guard that 404s beta routes on production hostnames even if the wrong build is deployed. Use when a static site needs a safe staging-only area."
---

# Beta Gate

## Purpose
Keep work-in-progress features visible on staging and **impossible** to
serve in production — with two independent layers, so one mistake can't
leak beta UI to real users. Proven in production on an Astro +
Cloudflare Pages site.

## Workflow
1. **Build flag** — gate every beta surface (nav link, teaser, pages) behind
   a single boolean read from the shell environment at build time:
   - Staging: `SHOW_BETA=1 npm run build`
   - Prod: `npm run build` (no flag) → zero beta HTML in the output.
2. **Runtime guard** — in the worker/server entry, 404 `/beta*` and
   `/api/beta*` when the request hostname is a production domain. This
   catches the "wrong build deployed to prod" accident.
3. **Deploy discipline** — staging and prod are separate projects/targets.
   Never rebuild the output dir while an upload is in flight, and never run
   two builds concurrently (one build's output can clobber the other's).

## Output Contract
- A prod build contains **no** beta routes, links, or API handlers in its
  static output (verify: grep the output dir for beta path strings — zero
  hits tolerated).
- A request to a beta path on a production hostname returns **404**, even
  from a beta-enabled build.
- Staging serves the full beta surface.

## Operating Rules
1. Read the flag via `process.env` (Node), **not** `import.meta.env` — Vite
   does not inject arbitrary shell vars into `import.meta.env`.
2. Keep the flag module build-time only: import it from frontmatter/server
   code, never from client-side `<script>` (it would ship the check, and
   relative imports there break — see references).
3. Default is OFF. Prod must be safe with zero configuration.
4. The runtime guard is a safety net, not the primary gate — keep both.
5. Verify live after every deploy: curl a beta path on the prod hostname,
   expect 404.

See `references/astro-cloudflare.md` for the concrete Astro + Pages
implementation (flag module, worker guard snippet, deploy commands, and
the build-collision lesson).
