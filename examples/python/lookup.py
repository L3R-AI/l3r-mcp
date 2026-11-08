"""Look up a US property, its Census figures, zoning and nearby infrastructure with the L3R MCP server.

Uses the official MCP Python SDK over streamable HTTP. No key or account is needed.

    pip install "mcp>=1.30"
    python lookup.py "401 Congress Ave, Austin, TX 78701"

Set L3R_MCP_URL to point at another endpoint (for example a local test server).
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ.get("L3R_MCP_URL", "https://mcp.l3r.io/mcp")


def payload(result) -> dict:
    """The tool's JSON answer: structuredContent (the text block is a Markdown card to show)."""
    if result.isError:
        raise SystemExit(f"refused: {result.content[0].text}")
    return result.structuredContent or json.loads(result.content[0].text)


async def main(query: str) -> None:
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("tools:", ", ".join(t.name for t in tools.tools))

            prop = payload(await session.call_tool("lookup_property", {"query": query}))
            print("status:", prop["status"])
            print("property key:", prop.get("property_key"))
            for p in prop.get("parcels", []):
                print("parcel:", p["parcel_id"], f"({p['namespace']})")

            # census_for_area takes exactly one of address, property_key or geoid
            if prop.get("property_key"):
                census = payload(await session.call_tool("census_for_area",
                                                         {"property_key": prop["property_key"]}))
                for area in census["areas"]:
                    income = area["median_household_income"]["est"]
                    print(f"{area['level']:>6}  {area['name']}: median household income {income:,.0f}")

            # zoning_for_property and nearby_for_property take a property_key or a query
            zoning = payload(await session.call_tool("zoning_for_property", {"query": query}))
            print("zoning status:", zoning["status"])
            for d in (zoning.get("zoning") or {}).get("districts", []):
                print("zoning district:", d["code"])
            print(zoning["disclaimer"])  # not a zoning determination: show it with the district

            near = payload(await session.call_tool("nearby_for_property",
                                                   {"query": query, "topics": ["energy", "transport"], "limit": 2}))
            print("nearby status:", near["status"])
            for group, items in (near.get("nearby") or {}).items():
                for kind, rows in items.items():
                    for r in rows:
                        print(f"{group}/{kind}: {r['name']} ({r['distance_mi']} mi)")

            # show the attribution wherever you show the result
            print()
            print("\n".join(prop["attribution"]))


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "401 Congress Ave, Austin, TX 78701"))
