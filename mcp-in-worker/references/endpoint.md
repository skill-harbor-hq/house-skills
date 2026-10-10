# MCP in Worker — endpoint skeleton

## Routes (worker entry, before other handlers)
```js
if (url.pathname === '/mcp' && request.method === 'POST')
  return await handleMCP(request, env);
if (url.pathname === '/mcp' && request.method === 'GET')
  return handleMCPInfo();
if (url.pathname === '/mcp' && request.method === 'OPTIONS')
  return new Response(null, { status: 204, headers: MCP_CORS });
```

## Constants
```js
const MCP_VERSION = '1.0.0';
const MCP_PROTOCOL_VERSION = '2025-11-25'; // current streamable-HTTP version
const MCP_CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Accept, Mcp-Session-Id',
  'Access-Control-Max-Age': '86400',
};
```

## Tool definitions (example: catalog)
```js
const MCP_TOOLS = [
  { name: 'search_items',
    description: 'Search the catalog. Pass the user\'s words through exactly as written, never translate.',
    inputSchema: { type: 'object',
      properties: {
        q: { type: 'string', description: 'Search keywords' },
        limit: { type: 'number', description: 'Max results, 1-10 (default 5)' } },
      required: ['q'] } },
  { name: 'get_item',
    description: 'Full details of one item: description, price, seller, links.',
    inputSchema: { type: 'object',
      properties: { id: { type: 'string', description: 'Item id/slug from search_items' } },
      required: ['id'] } },
  { name: 'get_action_payload',
    description: 'Get the copy-paste payload for using this item (install prompt, config snippet).',
    inputSchema: { type: 'object',
      properties: { id: { type: 'string', description: 'Item id/slug from search_items' } },
      required: ['id'] } },
];
```

## Dispatcher (JSON-RPC 2.0)
Handle `initialize` (reply with protocol version + server info),
`tools/list` (return `MCP_TOOLS`), `tools/call` (switch on
`params.name`, validate args, return `{ content: [{ type: 'text',
text }] }`), and `ping`. Unknown methods → JSON-RPC error
`{ code: -32601, message: 'Method not found' }`.

## Reusing an existing search handler
```js
// Synthesize an internal request to your own tested endpoint so ranking,
// synonyms, and rate limits behave identically. Forward caller headers.
const inner = new Request(
  'https://your-site.com/api/search?q=' + encodeURIComponent(q) + '&limit=' + limit,
  { headers: request.headers });
const resp = await handleSearch(inner, env);
```

## Live verification
```bash
curl -s https://your-site.com/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
curl -s https://your-site.com/mcp   # GET → human-readable info page
```
