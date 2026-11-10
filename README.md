# <img src="assets/icon-512.png" alt="" width="40" height="40" align="absmiddle"> L3R MCP Server

Real property intelligence for Claude, ChatGPT and other AI agents.

<p align="center">
  <img src="assets/demo-2090-vallejo.gif" alt="Asking Claude what's at 2090 Vallejo St in San Francisco with L3R" width="460">
</p>

Property, zoning, hazard and Census facts for any US address or parcel number:

1. **What's there:** property type, buildings, floors, size, year built and official building name.
2. **Which parcel:** the county parcel number and a stable L3R property key.
3. **Where it is:** location, plus Census tract, place and county with 2020–2024 figures.
4. **Zoning:** the district from the official map, with its rules where held.
5. **Hazards:** FEMA natural hazard ratings and nearby EPA cleanup sites.
6. **Nearby:** water, roads, rail, airports, ports, power plants, renewables, EV charging and data centers.
7. **Site screen:** flood zone, wetlands, protected areas, contamination, terrain and sewer for a lot.
8. **Data center projects:** permits, zoning cases, dockets and air permits, each dated and linked.
9. **Energy:** plant generation, state electricity prices and emissions, grid demand, fuel mix, interchange and coal shipments from EIA.

Each answer comes as a short Markdown card plus the full JSON. Free, read-only, no account.

```text
https://mcp.l3r.io/mcp
```

## Connect

**Claude:** add it from the [connector directory](https://claude.ai/directory/l3r), or add a custom connector with the URL.

**Claude Code:**

```sh
claude mcp add --transport http l3r https://mcp.l3r.io/mcp
```

**ChatGPT:** turn on Developer mode, then add a connector with the URL and no authentication.

**Other clients:** add the URL as a streamable HTTP server.

```json
{ "mcpServers": { "l3r": { "url": "https://mcp.l3r.io/mcp" } } }
```

Code examples: [Python](examples/python/lookup.py), [TypeScript](examples/typescript/lookup.ts), [curl](examples/curl/examples.sh).

## Example questions

- **Single-family home:** "Is 710 Steiner St in San Francisco a single-family home, and what year was it built?"
- **Condo:** "How many units are in 432 Park Ave in New York?"
- **Apartments:** "What kind of property is 300 N State St in Chicago?"
- **Retail:** "What's at 2623 NE University Village St in Seattle?"
- **Parcel number:** "What's the parcel number for 401 Congress Ave in Austin?"
- **Office tower:** "How tall is 1 S Broad St in Philadelphia, and when was it built?"
- **Census:** "What's the median rent around Ponce City Market in Atlanta?"
- **Zoning:** "What does RS-3 zoning allow in Tulsa?"
- **Hazards:** "What are the wildfire and earthquake risks at the Getty Center in Los Angeles?"
- **Nearby:** "What rail lines, airports and EV chargers are near Union Station in Kansas City?"
- **Facility:** "Tell me about the Hoover Dam power plant."
- **Site screen:** "Is 543 Union St in Brooklyn near a Superfund site, and how steep is 1000 Lombard St in San Francisco?"
- **Data center projects:** "What data center projects have official records near Woodbridge, VA?"
- **Energy:** "How much did Peach Bottom generate last year, and what's ERCOT's fuel mix right now?"

## Tools

| Tool | What it does |
|---|---|
| [`lookup_property`](docs/tools.md#lookup_property) | Property type, building facts, parcel and location for an address. |
| [`census_for_area`](docs/tools.md#census_for_area) | Population, income, home value and rent for an area. |
| [`zoning_for_property`](docs/tools.md#zoning_for_property) | Zoning district from the official map, with its rules where held. |
| [`hazards_for_property`](docs/tools.md#hazards_for_property) | FEMA hazard ratings and EPA cleanup sites within a mile. |
| [`nearby_for_property`](docs/tools.md#nearby_for_property) | Utilities, transport, energy, schools and EV charging nearby. |
| [`lookup_facility`](docs/tools.md#lookup_facility) | A power plant, airport, port or hospital by name or ID. |
| [`site_screen_for_property`](docs/tools.md#site_screen_for_property) | Flood, wetlands, protected areas, contamination, terrain and sewer for a lot. |
| [`data_center_projects`](docs/tools.md#data_center_projects) | Data center projects from official records, each dated and linked. |
| [`energy_plant_history`](docs/tools.md#energy-tools) | Generation and fuel history of a power plant. |
| [`electricity_state_profile`](docs/tools.md#energy-tools) | Electricity prices, sales and emissions by state. |
| [`grid_demand_mix`](docs/tools.md#energy-tools) | Hourly demand and fuel mix of a grid operator. |
| [`grid_interchange`](docs/tools.md#energy-tools) | Power flows between grid operators. |
| [`coal_shipments`](docs/tools.md#energy-tools) | Coal shipments from mines to plants. |

All tools are read-only. Schemas and example responses are in the [tools reference](docs/tools.md).

## Coverage and limits

- **Parcels:** about 124 million properties in 2,216 of 3,222 US counties.
- **Census:** all 50 states, DC and Puerto Rico.
- **Building facts:** county assessor data, NYC PLUTO, the SF Assessor and USA Structures.
- **Building names:** official names from NYC Landmarks, the National Register and the GSA.
- **Zoning:** official city and county maps, with district rules for some cities.
- **Hazards:** FEMA ratings by Census tract, not parcel.
- **Site screen:** wetlands, protected areas, EPA sites and terrain nationwide; flood zones as FEMA's state files load.
- **Data center projects:** official records only.
- **Not returned:** owners, values, sales or parcel outlines.
- **Rate limit:** one address per call, 60 calls an hour.

Coverage grows as L3R adds sources. L3R shows a fact only where the publisher's terms allow it, so a missing value often means it isn't licensed for display here yet, not that it doesn't exist.

Municipal code, permits and rights are handled by [Athena](https://3drights.com), L3R's property expert; still in private development.

## Attribution

Each answer ends with a short source line. Please show it with the result, for example:

> From Athena by L3R (PROP-…). Sources: Texas GIO, USA Structures (CC BY 4.0), Travis CAD, Census ACS 2020–24.

Where Census figures appear, also show:

> This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.

Full credits are in each answer's `attribution` field.

<details>
<summary><b>Sources</b></summary>

- **Parcels and buildings:** county parcel and assessor records, Texas GIO (CC0), NYC PLUTO, the San Francisco Assessor (PDDL), and USA Structures from FEMA and Oak Ridge National Laboratory (CC BY 4.0).
- **Building names:** NYC Landmarks, the National Register of Historic Places and the GSA.
- **Census:** U.S. Census Bureau, 2020–2024 ACS 5-year estimates and the Census Geocoder.
- **Zoning:** official city and county zoning maps and codes, credited to each publisher.
- **Hazards:** FEMA National Risk Index and EPA cleanup sites.
- **Nearby and facilities:** EIA, EPA, FAA, NCES and CMS records, and the DOE Alternative Fuels Data Center (NLR data; no endorsement implied).
- **Site screen:** FEMA National Flood Hazard Layer, USFWS National Wetlands Inventory, USGS PAD-US, EPA FRS and RCRA, USGS 3DEP.
- **Data center projects:** county, state, utility commission and RTO records, each linked.
- **Energy:** U.S. Energy Information Administration (EIA-923, EIA-930, retail sales, emissions, coal receipts).

</details>

<details>
<summary><b>Contact</b></summary>

- Feedback: [feedback@l3r.io](mailto:feedback@l3r.io) or [open an issue](../../issues)
- Questions: [mcp@l3r.io](mailto:mcp@l3r.io)

</details>

<details>
<summary><b>Legal</b></summary>

- [Terms of use](TERMS.md)
- [Privacy](PRIVACY.md)
- [Security](SECURITY.md)

</details>

---

Built by L3R.
