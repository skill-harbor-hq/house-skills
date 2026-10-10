---
name: "mcp-in-worker"
description: "Expose a read-only MCP server (streamable HTTP) directly inside a Cloudflare Worker: POST /mcp with a small toolset wrapping your existing search/data API. Deploys with the site, no separate server. Use when users ask to 'connect their Muse/AI assistant' to your catalog or dataset."
---

# MCP in Worker

## Purpose
Give AI assistants direct tools into your data — search, record detail,
and action payloads — without running separate MCP infrastructure. A
single `POST /mcp` endpoint inside your existing Cloudflare Worker speaks
MCP (streamable HTTP, JSON-RPC 2.0) and reuses your tested API handlers.
Proven live: 3 tools, bilingual, zero auth.

## Workflow
1. **Define 3–5 read-only tools** with tight JSON schemas. Keep the set
   minimal: search → detail → action-payload covers most catalogs.
   Pass user wording through untranslated; cap free-text inputs (~120 chars).
2. **Reuse existing handlers.** Don't reimplement search: synthesize an
   internal `Request` to your own tested endpoint and forward the caller's
   headers, so IP-based rate limits and logging stay accurate.
3. **Wire the routes** in the worker entry, before other handlers:
   - `POST /mcp` → JSON-RPC dispatcher (initialize, tools/list,
     tools/call, ping).
   - `GET /mcp` → human-readable info page (what it is, endpoint, tools).
   - `OPTIONS /mcp` → CORS preflight (MCP clients are cross-origin).
4. **Rate-limit the tools** like the underlying API (e.g. 60/hour). MCP
   clients retry aggressively; fail-open logging, never fail-closed data.
5. **Verify live**: call `tools/list` and one `tools/call` against the
   deployed hostname with curl before announcing it.

## Output Contract
- `GET /mcp` returns a readable description (name, endpoint, tool list).
- `POST /mcp` answers `initialize`, `tools/list`, `tools/call`, `ping`
  as JSON-RPC 2.0 with the declared protocol version.
- Every tool result is plain text or structured content the model can
  quote — no HTML.

## Operating Rules
1. **Read-only.** No tool writes, deletes, or spends. If a tool must act,
   it returns a payload/link the user confirms elsewhere.
2. Keep tool descriptions self-contained: the calling model never sees
   your site, only these strings.
3. CORS: `Access-Control-Allow-Origin: *`, allow `Content-Type, Accept,
   Mcp-Session-Id`. Preflight returns 204.
4. Version the protocol string and bump it on breaking changes.
5. Never log or echo secrets; the endpoint is public by design.
6. If your deploy pipeline strips or neutralizes routes (like a beta-gate
   would), exempt `/mcp` explicitly and re-verify after every deploy.

See `references/endpoint.md` for the dispatcher skeleton and tool
definitions.
