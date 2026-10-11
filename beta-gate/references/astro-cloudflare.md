# Beta Gate — Astro + Cloudflare Pages implementation

## 1. Flag module (`src/lib/beta.ts`)
Build-time only. Imported from `.astro` frontmatter (Node), never from
client-side `<script>`.

```ts
// Build-time flag: `SHOW_BETA=1 npm run build` includes beta surfaces.
// A plain `npm run build` produces a prod-safe build with no beta HTML.
// NOTE: read via process.env, NOT import.meta.env — Vite does not
// statically inject arbitrary shell env vars into import.meta.env.
export const SHOW_BETA: boolean =
  typeof process !== 'undefined' && (process.env as any)?.SHOW_BETA === '1';
```

Usage in frontmatter:
```astro
---
import { SHOW_BETA } from '../lib/beta';
---
{SHOW_BETA && <a href="/beta">🧪 Beta</a>}
```

## 2. Runtime guard (worker entry)
Even a beta-enabled build deployed to prod by mistake must serve nothing.
Put this **before** any route handling:

```js
const BETA_PROD_HOSTS = new Set(['example.com', 'www.example.com']);
const isBetaPath =
  /^(\/fr)?\/beta(\/|$)/.test(url.pathname) ||
  url.pathname.startsWith('/api/beta');
if (isBetaPath && BETA_PROD_HOSTS.has(url.hostname.toLowerCase())) {
  return new Response('Not found', { status: 404 });
}
```

## 3. Deploy commands
```bash
# staging (beta visible)
SHOW_BETA=1 npm run build && <deploy staging>

# prod (beta stripped)
npm run build && <deploy prod>
```

## 4. Post-build verification (zero tolerance)
```bash
# prod output must contain no beta path strings
grep -r "from '\.\./" dist/*.html   # (example: your own beta markers)
grep -ro "/beta/[a-z-]*" dist/ | sort -u   # expect: no output
```

## 5. Hard-won lessons
- **Build collision:** two sessions rebuilding `dist/` over each other
  (one beta, one prod) plus simultaneous uploads = undefined output. Before
  `npm run build`, check no other build/deploy is running
  (`ps aux | grep -E "astro build|deploy"`). One build at a time.
- **Never rebuild during upload:** the deploy manifest hashes must match
  the bytes being uploaded.
- **Client-side imports:** never use a relative `import ... from '../lib/x'`
  inside an inline client `<script>` — Astro may copy it verbatim into the
  HTML, where it 404s and kills the whole module. Inline shared code in
  client scripts instead.
- **Staging bindings:** on Cloudflare Pages, adding D1/KV bindings to a
  preview project's config can break its deploy stage. If staging only
  needs visual preview, keep it binding-free.
