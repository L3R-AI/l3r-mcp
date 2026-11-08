#!/bin/sh
# JSON-RPC over streamable HTTP with curl. The server is stateless: no session header is needed,
# and each call is a single POST. Requires curl; jq is optional (for pretty output).
#
#   sh examples.sh
#
# Set L3R_MCP_URL to point at another endpoint (for example a local test server).
set -eu
URL="${L3R_MCP_URL:-https://mcp.l3r.io/mcp}"

rpc() {
  curl -sS "$URL" \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json, text/event-stream' \
    -H 'MCP-Protocol-Version: 2025-11-25' \
    -d "$1"
  echo
}

echo "# initialize"
rpc '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}}}'

echo "# tools/list"
rpc '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

echo "# lookup_property: a street address"
rpc '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"lookup_property","arguments":{"query":"401 Congress Ave, Austin, TX 78701"}}}'

echo "# lookup_property: a New York City BBL"
rpc '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"lookup_property","arguments":{"query":"1-00835-0041"}}}'

echo "# census_for_area: a Census tract GEOID"
rpc '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"census_for_area","arguments":{"geoid":"48113002100"}}}'

echo "# zoning_for_property: the zoning district at an address"
rpc '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"zoning_for_property","arguments":{"query":"401 Congress Ave, Austin, TX 78701"}}}'

echo "# nearby_for_property: power and transport near an address, up to 2 items each"
rpc '{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"nearby_for_property","arguments":{"query":"401 Congress Ave, Austin, TX 78701","topics":["energy","transport"],"limit":2}}}'
