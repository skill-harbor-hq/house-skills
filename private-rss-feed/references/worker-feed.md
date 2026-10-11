# Private RSS Feed — worker handler skeleton

## Route (worker entry)
```js
if (url.pathname === '/feed.xml' || url.pathname === '/fr/feed.xml')
  return await handleFeed(request, env, url.pathname.startsWith('/fr') ? 'fr' : 'en');
```

## Handler
```js
async function handleFeed(request, env, lang) {
  const token = new URL(request.url).searchParams.get('token') || '';
  let secret = '';
  try {
    const row = await env.DB.prepare(
      "SELECT value FROM app_secrets WHERE key = 'feed'").first();
    secret = row ? row.value : '';
  } catch (e) { secret = ''; }
  // Quiet 404 on missing/wrong token — never hint the feed exists.
  if (!secret || !timingSafeEqual(token, secret)) {
    return new Response('Not found',
      { status: 404, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }
  const items = await env.DB.prepare(
    `SELECT slug, title, summary, created_at FROM posts
     WHERE published = 1 ORDER BY created_at DESC LIMIT 50`).all();
  const xml = buildRss(items.results || [], lang, request);
  return new Response(xml, { headers: {
    'Content-Type': 'application/rss+xml; charset=utf-8',
    'Cache-Control': 'private, max-age=300',
  }});
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++)
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}
```

## RSS builder notes
- Escape: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`.
- Dates: RFC-2822 via `new Date(dt.replace(' ', 'T') + 'Z').toUTCString()`.
- Private line example (optional, in channel `<description>`):
  `" Traffic: 128 visits yesterday (+12% vs the day before)."`
- `Cache-Control: private` — shared caches must not store a tokened feed.

## Token lifecycle
```bash
openssl rand -hex 32   # new token
# store: UPDATE app_secrets SET value='<token>' WHERE key='feed';
# then redeploy (Pages binds secrets at deploy time)
```
If it leaks: regenerate → update store → redeploy → give the subscriber
the new URL. Never reuse a leaked token.
