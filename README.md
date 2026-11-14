<h1 align="center"><img src="assets/icon-512.png" alt="" width="40" height="40" align="absmiddle"> L3R MCP Server</h1>

<p align="center">
  <img src="assets/demo-2090-vallejo.gif" alt="Asking Claude what's at 2090 Vallejo St in San Francisco with L3R" width="460">
</p>

<p align="center">Ask about US property, power plants and the grid. No account required.</p>

<p align="center">
  <a href="https://claude.ai/directory/l3r"><img src="https://img.shields.io/badge/Add_to_Claude-000000?style=for-the-badge&logo=claude&logoColor=white" alt="Add to Claude"></a>
  <a href="https://cursor.com/en/install-mcp?name=l3r&config=eyJ1cmwiOiJodHRwczovL21jcC5sM3IuaW8vbWNwIn0="><img src="https://img.shields.io/badge/Install_in_Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" alt="Install in Cursor"></a>
  <a href="https://vscode.dev/redirect/mcp/install?name=l3r&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fmcp.l3r.io%2Fmcp%22%7D"><img src="https://custom-icon-badges.demolab.com/badge/Install_in_VS_Code-000000?style=for-the-badge&logo=vsc&logoColor=white" alt="Install in VS Code"></a>
  <a href="#codex"><img src="https://img.shields.io/badge/Add_to_Codex-000000?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0yMi4yODE5IDkuODIxMWE1Ljk4NDcgNS45ODQ3IDAgMCAwLS41MTU3LTQuOTEwOCA2LjA0NjIgNi4wNDYyIDAgMCAwLTYuNTA5OC0yLjlBNi4wNjUxIDYuMDY1MSAwIDAgMCA0Ljk4MDcgNC4xODE4YTUuOTg0NyA1Ljk4NDcgMCAwIDAtMy45OTc3IDIuOSA2LjA0NjIgNi4wNDYyIDAgMCAwIC43NDI3IDcuMDk2NiA1Ljk4IDUuOTggMCAwIDAgLjUxMSA0LjkxMDcgNi4wNTEgNi4wNTEgMCAwIDAgNi41MTQ2IDIuOTAwMUE1Ljk4NDcgNS45ODQ3IDAgMCAwIDEzLjI1OTkgMjRhNi4wNTU3IDYuMDU1NyAwIDAgMCA1Ljc3MTgtNC4yMDU4IDUuOTg5NCA1Ljk4OTQgMCAwIDAgMy45OTc3LTIuOTAwMSA2LjA1NTcgNi4wNTU3IDAgMCAwLS43NDc1LTcuMDcyOXptLTkuMDIyIDEyLjYwODFhNC40NzU1IDQuNDc1NSAwIDAgMS0yLjg3NjQtMS4wNDA4bC4xNDE5LS4wODA0IDQuNzc4My0yLjc1ODJhLjc5NDguNzk0OCAwIDAgMCAuMzkyNy0uNjgxM3YtNi43MzY5bDIuMDIgMS4xNjg2YS4wNzEuMDcxIDAgMCAxIC4wMzguMDUydjUuNTgyNmE0LjUwNCA0LjUwNCAwIDAgMS00LjQ5NDUgNC40OTQ0em0tOS42NjA3LTQuMTI1NGE0LjQ3MDggNC40NzA4IDAgMCAxLS41MzQ2LTMuMDEzN2wuMTQyLjA4NTIgNC43ODMgMi43NTgyYS43NzEyLjc3MTIgMCAwIDAgLjc4MDYgMGw1Ljg0MjgtMy4zNjg1djIuMzMyNGEuMDgwNC4wODA0IDAgMCAxLS4wMzMyLjA2MTVMOS43NCAxOS45NTAyYTQuNDk5MiA0LjQ5OTIgMCAwIDEtNi4xNDA4LTEuNjQ2NHpNMi4zNDA4IDcuODk1NmE0LjQ4NSA0LjQ4NSAwIDAgMSAyLjM2NTUtMS45NzI4VjExLjZhLjc2NjQuNzY2NCAwIDAgMCAuMzg3OS42NzY1bDUuODE0NCAzLjM1NDMtMi4wMjAxIDEuMTY4NWEuMDc1Ny4wNzU3IDAgMCAxLS4wNzEgMGwtNC44MzAzLTIuNzg2NUE0LjUwNCA0LjUwNCAwIDAgMSAyLjM0MDggNy44NzJ6bTE2LjU5NjMgMy44NTU4TDEzLjEwMzggOC4zNjQgMTUuMTE5MiA3LjJhLjA3NTcuMDc1NyAwIDAgMSAuMDcxIDBsNC44MzAzIDIuNzkxM2E0LjQ5NDQgNC40OTQ0IDAgMCAxLS42NzY1IDguMTA0MnYtNS42NzcyYS43OS43OSAwIDAgMC0uNDA3LS42Njd6bTIuMDEwNy0zLjAyMzFsLS4xNDItLjA4NTItNC43NzM1LTIuNzgxOGEuNzc1OS43NzU5IDAgMCAwLS43ODU0IDBMOS40MDkgOS4yMjk3VjYuODk3NGEuMDY2Mi4wNjYyIDAgMCAxIC4wMjg0LS4wNjE1bDQuODMwMy0yLjc4NjZhNC40OTkyIDQuNDk5MiAwIDAgMSA2LjY4MDIgNC42NnpNOC4zMDY1IDEyLjg2M2wtMi4wMi0xLjE2MzhhLjA4MDQuMDgwNCAwIDAgMS0uMDM4LS4wNTY3VjYuMDc0MmE0LjQ5OTIgNC40OTkyIDAgMCAxIDcuMzc1Ny0zLjQ1MzdsLS4xNDIuMDgwNUw4LjcwNCA1LjQ1OWEuNzk0OC43OTQ4IDAgMCAwLS4zOTI3LjY4MTN6bTEuMDk3Ni0yLjM2NTRsMi42MDItMS40OTk4IDIuNjA2OSAxLjQ5OTh2Mi45OTk0bC0yLjU5NzQgMS40OTk3LTIuNjA2Ny0xLjQ5OTdaIi8+PC9zdmc+" alt="Add to Codex"></a>
</p>

| | Includes |
|---|---|
| **Property** | Type, buildings, floors, size, year built, official name, county parcel number, a stable L3R key |
| **Place** | Location, Census tract and 2020–24 figures, congressional, legislative and school districts |
| **Zoning** | District from the official map, with its rules where held |
| **Map** | The lot among nearby lots, buildings, streets and zoning |
| **Risk and site** | FEMA hazard ratings, EPA cleanup sites, wetlands, protected areas, sewer |
| **Nearby** | Water, roads, rail, airports, ports, power plants, EV charging, data centers |
| **Energy** | Grid and utilities, plant output, coal deliveries, state prices, hourly demand and flows |
| **Data centers** | Projects backed by official records |
| **City records** | Permits, code cases, council votes, landmark history, hearings |

Each answer is a short Markdown card plus the full JSON.

## Connect

```text
https://mcp.l3r.io/mcp
```

### Claude

Add from [connector directory](https://claude.ai/directory/l3r) (listing description pending update), or add a custom connector with URL.

#### Claude Code

```sh
claude mcp add --transport http l3r https://mcp.l3r.io/mcp
```

### ChatGPT

Turn on Developer mode, then add a connector with URL and no authentication.

#### Codex

```sh
codex mcp add l3r --url https://mcp.l3r.io/mcp
```

### Other clients

Add URL as a streamable HTTP server:

```json
{ "mcpServers": { "l3r": { "url": "https://mcp.l3r.io/mcp" } } }
```

<details>
<summary>Where each client keeps it</summary>

| Client | Config |
|---|---|
| Cursor | `~/.cursor/mcp.json`, or the button above |
| VS Code | The button above, or `.vscode/mcp.json` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |
| Gemini CLI | `~/.gemini/settings.json` |
| Zed | `settings.json`, under `context_servers` |

</details>

Code examples: [Python](examples/python/lookup.py), [TypeScript](examples/typescript/lookup.ts), [curl](examples/curl/examples.sh).

## Try it

<details>
<summary>Example questions</summary>

- **Condo:** "How many units are in 432 Park Ave in New York?"
- **Parcel number:** "What's the parcel number for 401 Congress Ave in Austin?"
- **Office tower:** "How tall is 1 S Broad St in Philadelphia, and when was it built?"
- **Census:** "What's the median rent around Ponce City Market in Atlanta?"
- **Zoning:** "What does RS-3 zoning allow in Tulsa?"
- **Hazards:** "What are the wildfire and earthquake risks at the Getty Center in Los Angeles?"
- **Nearby:** "What rail lines, airports and EV chargers are near Union Station in Kansas City?"
- **Site screen:** "Are there wetlands or contaminated sites near 1 Canal St in New Orleans?"
- **Energy service:** "Which companies supply electricity and gas at 870 Santa Cruz Ave in Menlo Park?"
- **Districts:** "Which congressional and school districts is 200 E Colfax Ave in Denver in?"
- **Data center projects:** "What is the status of the Prince William Digital Gateway in Virginia?"
- **Power plant:** "How much power did the W A Parish plant generate last year, and from what fuels?"
- **Coal:** "Which mines supply coal to the Labadie plant in Missouri?"
- **State electricity:** "What do homes in Maine pay for electricity?"
- **Grid demand:** "What is ERCOT's demand right now, and what is the fuel mix?"
- **Grid flows:** "How much power does the California ISO import from its neighbours?"
- **Facility:** "Tell me about the Hoover Dam power plant."
- **City records:** "What zoning hearings are coming up in Dallas, and who decides them?"
- **Projects:** "What's in review at 3908 Menchaca Rd in Austin?"

</details>

## Tools

| Tool | Returns |
|---|---|
| [`lookup_property`](docs/tools.md#lookup_property) | Property type, building facts, parcel and location for an address. |
| [`show_property_map`](docs/tools.md#show_property_map) | Map picture of the lot with nearby buildings, streets and zoning. |
| [`census_for_area`](docs/tools.md#census_for_area) | Population, income, home value and rent for an area. |
| [`zoning_for_property`](docs/tools.md#zoning_for_property) | Zoning district from the official map, with its rules where held. |
| [`hazards_for_property`](docs/tools.md#hazards_for_property) | FEMA hazard ratings and EPA cleanup sites within a mile. |
| [`nearby_for_property`](docs/tools.md#nearby_for_property) | Utilities, transport, energy, schools and EV charging nearby. |
| [`site_screen_for_property`](docs/tools.md#site_screen_for_property) | Wetlands, protected areas, contamination and sewer service. |
| [`energy_service_for_property`](docs/tools.md#energy_service_for_property) | Grid, electric utility, retail supplier and gas utility. |
| [`districts_for_property`](docs/tools.md#districts_for_property) | U.S. House, state legislature and school districts for a property or point. |
| [`data_center_projects`](docs/tools.md#data_center_projects) | Data center projects backed by official records, each dated and linked. |
| [`energy_plant_history`](docs/tools.md#energy_plant_history) | Monthly and annual generation and fuel mix for a power plant. |
| [`electricity_state_profile`](docs/tools.md#electricity_state_profile) | State electricity prices, sales, customers and CO2. |
| [`grid_demand_mix`](docs/tools.md#grid_demand_mix) | Hourly demand, forecast, generation and fuel mix for a balancing authority. |
| [`grid_interchange`](docs/tools.md#grid_interchange) | Hourly electricity flows between balancing authorities. |
| [`coal_shipments`](docs/tools.md#coal_shipments) | Coal received at a plant by mine, or shipped from a mine. |
| [`lookup_facility`](docs/tools.md#lookup_facility) | A power plant, airport, port or hospital by name or ID. |
| [`coverage_for_county`](docs/tools.md#coverage_for_county) | What L3R holds for a county. |
| [`list_reference_data`](docs/tools.md#list_reference_data) | Ranked lists of seaports, risk tracts or power plants. |
| [`city_hall_for_place`](docs/tools.md#city_hall_for_place) | Hearings, decisions and boards for a city. |
| [`projects_for_property`](docs/tools.md#projects_for_property) | Planning cases and permits in review at an address, with their stage. |

All tools are read-only. Schemas and example responses are in the [tools reference](docs/tools.md).

## Coverage & limits

- **Parcels:** 119M+ properties in 2,100+ US counties. Census figures for all 50 states, DC and Puerto Rico.
- **Zoning:** district rules for some cities only.
- **Ranches and farms:** shown one tax parcel at a time; a holding's other parcels aren't linked.
- **Hazards:** FEMA ratings by Census tract, not parcel. Flood zones only where held (SF for now).
- **Site screen:** a first look only. Layers we don't hold are named, never shown as clear.
- **Energy service:** confirmed where a state map covers the address; otherwise likely, by county.
- **Districts:** names and numbers only. Election offices decide.
- **Data centers:** official records only, such as permits and zoning cases. News never counts.
- **Grid:** hourly figures, refreshed daily, not live.
- **City records:** where cities publish them. Hearings in Austin, Chicago, Dallas, NYC and SF; projects in review in SF, NYC, Austin and Chicago.
- **Not returned:** owners, values or sales. Parcel outlines appear only inside map images.
- **Rate limit:** one address per call; 60 calls an hour and 300 a day from each network address.

<details>
<summary>Property types</summary>

| Type | Includes |
|---|---|
| Single-family home | Detached and attached houses |
| Multifamily building | Two units or more, from duplexes to large apartment buildings |
| Condominium | Condo buildings and their units |
| Mixed-use building | Homes and businesses in one building |
| Manufactured or mobile home | Manufactured and mobile homes |
| Office building | Offices |
| Retail property | Shops, restaurants, shopping centers |
| Commercial property | Hotels, parking and other commercial uses |
| Industrial property | Factories, warehouses, utilities |
| Government or institutional property | Public buildings, schools, hospitals, churches |
| Agricultural land | Farms, ranches, timber |
| Vacant land | Undeveloped lots and tracts |

Types come from the county's own land-use code, mapped to these groups. Where a county gives no code, the type is left out.

</details>

This is the public slice of L3R. Facts appear only where publishers allow, so a missing value often isn't licensed for display yet. [Athena](https://3drights.com) covers much more, including municipal code, permits, records and rights.

## Attribution

<details>
<summary>Credit</summary>

Each answer ends with a short source line. Please show it with the result, for example:

> From Athena by L3R (PROP-…). Sources: Texas GIO, USA Structures (CC BY 4.0), Travis CAD, Census ACS 2020–24.

Where Census figures appear, also show:

> This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.

Full credits are in each answer's `attribution` field.

</details>

<details>
<summary>Sources</summary>

- **Parcels and buildings:** county assessors, Texas GIO, NYC PLUTO, SF Assessor, USA Structures (CC BY 4.0)
- **Building names:** NYC Landmarks, National Register of Historic Places, GSA
- **Zoning:** city and county maps and codes
- **Permits:** DataSF, NYC Department of Buildings
- **Census:** ACS 2020–24 5-year estimates, Census Geocoder
- **Districts:** Census TIGER/Line
- **Hazards:** FEMA National Risk Index, EPA cleanup sites
- **Site screen:** USFWS wetlands, USGS PAD-US and 3DEP, FEMA flood maps, EPA
- **Nearby:** EIA, EPA, FAA, NCES, CMS, DOE AFDC (NLR data, no endorsement implied)
- **Energy service:** EIA-861 and EIA-860 via Catalyst Cooperative PUDL (CC BY 4.0)
- **Power plants and grid:** EIA (public domain)
- **Data center projects:** official public records, each linked
- **City records:** city open data, clerks and councils, landmark reports

</details>

## Contact

Questions: [mcp@l3r.io](mailto:mcp@l3r.io) or [open an issue](../../issues).

[Terms](TERMS.md) | [Privacy](PRIVACY.md) | [Security](SECURITY.md)

---

Built by L3R, Real Property Intelligence
