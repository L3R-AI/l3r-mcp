// Look up a US property with the L3R MCP server, using the MCP TypeScript SDK over streamable HTTP.
// No key or account is needed.
//
//   npm install
//   npm start -- "401 Congress Ave, Austin, TX 78701"
//
// Set L3R_MCP_URL to point at another endpoint (for example a local test server).
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const url = new URL(process.env.L3R_MCP_URL ?? "https://mcp.l3r.io/mcp");
const query = process.argv.slice(2).join(" ") || "401 Congress Ave, Austin, TX 78701";

const client = new Client({ name: "l3r-example", version: "1.0.0" });
await client.connect(new StreamableHTTPClientTransport(url));

const { tools } = await client.listTools();
console.log("tools:", tools.map((t) => t.name).join(", "));

const result = await client.callTool({ name: "lookup_property", arguments: { query } });
const text = (result.content as Array<{ type: string; text: string }>)[0].text;
if (result.isError) {
  console.error("refused:", text);
  process.exit(1);
}

// structuredContent is the JSON answer; the text block is a Markdown card to show as is
const answer = (result.structuredContent as any) ?? JSON.parse(text);
console.log(text);
console.log("status:", answer.status);
console.log("property key:", answer.property_key);
for (const p of answer.parcels ?? []) console.log("parcel:", p.parcel_id, `(${p.namespace})`);
for (const b of answer.buildings ?? []) if (b.bin) console.log("NYC BIN:", b.bin);

// zoning_for_property and nearby_for_property take a property_key or a query
const zoning = await client.callTool({ name: "zoning_for_property", arguments: { query } });
const z = zoning.structuredContent as any;
console.log("zoning status:", z.status);
for (const d of z.zoning?.districts ?? []) console.log("zoning district:", d.code);
console.log(z.disclaimer); // not a zoning determination: show it with the district

const nearby = await client.callTool({
  name: "nearby_for_property",
  arguments: { query, topics: ["energy", "transport"], limit: 2 },
});
const n = nearby.structuredContent as any;
console.log("nearby status:", n.status);
for (const [group, kinds] of Object.entries(n.nearby ?? {}))
  for (const [kind, rows] of Object.entries(kinds as Record<string, any[]>))
    for (const r of rows) console.log(`${group}/${kind}: ${r.name} (${r.distance_mi} mi)`);

// show the attribution wherever you show the result
console.log("\n" + answer.attribution.join("\n"));

await client.close();
