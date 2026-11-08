# Examples

Each example calls the live server at `https://mcp.l3r.io/mcp`. Set `L3R_MCP_URL` to use another endpoint.

| Example | Run |
|---|---|
| [Python](python/lookup.py), official MCP Python SDK | `pip install "mcp>=1.30"`, then `python python/lookup.py "401 Congress Ave, Austin, TX 78701"` |
| [TypeScript](typescript/lookup.ts), MCP TypeScript SDK | `cd typescript && npm install && npm start -- "401 Congress Ave, Austin, TX 78701"` |
| [curl](curl/examples.sh), raw JSON-RPC | `sh curl/examples.sh` |

Each tool result has a short Markdown card as its text block and the JSON answer described in the
[tools reference](../docs/tools.md) as `structuredContent`. Show the card (or the answer's `attribution`) wherever you
show the result.

Each example calls `lookup_property`, `zoning_for_property` and `nearby_for_property` for one address. The example code is MIT licensed.
