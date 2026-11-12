# Tools reference

All tools are read-only and idempotent, and each takes one input per call: one address, one
identifier, one area, one facility, or one capped list of public reference data. Every property tool also takes a point (`lat` and `lon`): a point inside a parcel reads that parcel, and a point with no parcel reads the location itself. Each result has two parts: a short Markdown card as the text content block, ready to
show as is, and the full answer as JSON in `structuredContent`. No tool calls a model.

| Tool | Title | Annotations |
|---|---|---|
| [`lookup_property`](#lookup_property) | Look up a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`census_for_area`](#census_for_area) | Census figures for an area | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`zoning_for_property`](#zoning_for_property) | Zoning for a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`hazards_for_property`](#hazards_for_property) | Hazards for a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`nearby_for_property`](#nearby_for_property) | Infrastructure, utilities and energy around a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`districts_for_property`](#districts_for_property) | Political and school districts for a US property or point | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`energy_service_for_property`](#energy_service_for_property) | Grid, electric utility, supplier and gas for a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`site_screen_for_property`](#site_screen_for_property) | Site screen for a US property (flood, wetlands, protected areas, contamination, terrain, sewer) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`data_center_projects`](#data_center_projects) | Data center projects from official records (permits, zoning, dockets, air permits) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`energy_plant_history`](#energy_plant_history) | Power plant generation history (EIA-923) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`electricity_state_profile`](#electricity_state_profile) | State electricity prices, sales and emissions (EIA) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`grid_demand_mix`](#grid_demand_mix) | Hourly electricity demand and fuel mix by balancing authority (EIA-930) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`grid_interchange`](#grid_interchange) | Electricity interchange between balancing authorities (EIA-930) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`coal_shipments`](#coal_shipments) | Coal shipments from mines to power plants (EIA) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`lookup_facility`](#lookup_facility) | Look up a US facility (plant, data center, airport, port, water system and more) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`coverage_for_county`](#coverage_for_county) | What L3R holds for a US county | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`list_reference_data`](#list_reference_data) | Ranked lists from public reference data (ports, FEMA risk tracts, power plants) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |

Every example below is real output from the live server at `https://mcp.l3r.io/mcp`, captured on 8 November 2026. The examples for `districts_for_property`, `energy_service_for_property` and `site_screen_for_property` were captured on 11 November 2026, as were those for `data_center_projects`, `energy_plant_history`, `electricity_state_profile`, `grid_demand_mix`, `grid_interchange` and `coal_shipments`. The examples for `coverage_for_county` and `list_reference_data` were captured on 12 November 2026. Each
passed the server's own answer gates: a key allowlist at every depth, a guard against owner, holder and contact fields,
and a size cap. Nothing was edited by hand.

**Contents**

- [`lookup_property`](#lookup_property)
- [`census_for_area`](#census_for_area)
- [`zoning_for_property`](#zoning_for_property)
- [`hazards_for_property`](#hazards_for_property)
- [`nearby_for_property`](#nearby_for_property)
- [`districts_for_property`](#districts_for_property)
- [`energy_service_for_property`](#energy_service_for_property)
- [`site_screen_for_property`](#site_screen_for_property)
- [`data_center_projects`](#data_center_projects)
- [`energy_plant_history`](#energy_plant_history)
- [`electricity_state_profile`](#electricity_state_profile)
- [`grid_demand_mix`](#grid_demand_mix)
- [`grid_interchange`](#grid_interchange)
- [`coal_shipments`](#coal_shipments)
- [`lookup_facility`](#lookup_facility)
- [`coverage_for_county`](#coverage_for_county)
- [`list_reference_data`](#list_reference_data)
- [Errors and refusals](#errors-and-refusals)

---

## `lookup_property`

Find a US property by a street address or any parcel identifier. The answer is one stable L3R property key (`PROP-…`),
a one-line summary, the property type, building facts where the source's terms allow them, the property's parcels and
buildings, related groups (a condominium, a New York City zoning lot, an assemblage), its location and its Census
geography with headline ACS figures. It points to the other tools when they hold something for the property.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a county parcel number. |
| `lat` | number, -90 to 90 | no | Latitude of one point, WGS84 decimal degrees. Use with `lon`, instead of `query`. |
| `lon` | number, -180 to 180 | no | Longitude of the same point, WGS84 decimal degrees. |
| `query` | string, at most 200 characters | no | One street address or one parcel identifier. See accepted forms below. Give `query`, or `lat` with `lon`. |
| `state` | string, at most 200 characters | no | Two-letter state, for example `TX`. Needed for a county parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Accepted forms of `query`, exactly one per call:

- A street address, with city and state or a ZIP code.
- A county parcel number (APN or PIN) as the county prints it. Give `state` and `county`.
- A San Francisco block and lot (`3725018`, `3725/018`).
- A New York City BBL (`1008350041`, `1-00835-0041`, `Manhattan block 835 lot 41`) or BIN.
- An L3R `PROP-`, `PARCEL-` or `BLDG-` key.
- Or, instead of `query`, one point (`lat` and `lon`) in the 50 states, DC or Puerto Rico. The answer is the property whose parcel holds the point. Otherwise it is the nearest held lot within 100 m (status `NEAREST`, with its distance, never an exact match). Otherwise it is the place and its Census geography.

### Statuses

| Status | Meaning |
|---|---|
| `MATCHED` | One property found. |
| `AMBIGUOUS` | Up to 3 candidates. Add the county or unit. |
| `NEAREST` | A point only. No parcel holds it. The nearest held lot within 100 m is returned, with its distance. |
| `LOCATION_ONLY` | The place and its Census geography, but no parcel is held. |
| `OUTSIDE_COVERAGE` | A point outside the US and Puerto Rico. |
| `UNMATCHED` | Nothing found. `reason` and `what_would_resolve` say why and what to try. |
| `NO_PLACE` | The query did not resolve to a US place. |

### Response fields

| Field | Contents |
|---|---|
| `property_key` | The stable `PROP-…` key. Use it with the other tools. |
| `summary` | One plain line, for example "Single-family home, ~3,289 sq ft living area, built 2001". |
| `property_type` | Class (for example `single_family`, `multifamily`, `commercial`, `vacant_land`) with the source's own code and description. |
| `building_facts` | Building count, roof footprint, height, occupancy, year built, floors, units, living area, bedrooms, bathrooms and rooms, each with its source and licence. Only where the fact is held and its terms allow it. |
| `building_name` | A landmark record's name for the building, where one names it. |
| `parcels`, `buildings`, `related` | Parcel numbers and `PARCEL-` keys, `BLDG-` keys and NYC BINs, and related groups. Capped at 50, 50 and 10 members per group, with true `counts` and `truncated: true`. |
| `location`, `geography`, `census` | The point where the source allows it, the state, county, place and tract, and ACS 2020–2024 figures for the tract, place and county. A top-coded figure carries `top_coded` and a display string such as `250,000+`. |
| `more` | Which of zoning, hazards and nearby hold something for this property. |
| `missing` | What is not held, for example `PROPERTY_TYPE_NOT_HELD`. A missing fact is left out, never estimated. |
| `attribution` | Credits to show with the result. |

Roof footprint is ground area from aerial mapping. It is not living area or square footage. An NYC condominium unit is
described by its building's billing lot. No owners, values, sale prices, outlines or bulk lists are returned.

### Examples


**An office building, by address**

Building facts and Census figures for a downtown Austin address.

Call:

```json
{"name": "lookup_property", "arguments": {"query": "401 Congress Ave, Austin, TX"}}
```

Card:

```markdown
### 401 Congress Ave, Austin, TX
**Office building, 1 building, ~546,000 sq ft, built 2002**

- Parcel: Appraisal district property ID 192833
- Type: Office building (F1: Commercial real property)
- Buildings: 1 building, ~159 ft tall
- Building area: ~546,000 sq ft
- Roof footprint: ~92,100 sq ft (ground area from aerial mapping, not living area)
- Year built: 2002

| 2020–2024 ACS | Tract 11.03 | Austin | Travis County |
|---|---:|---:|---:|
| Median household income | $166,513 | $93,658 | $99,611 |
| Median home value | $600,000 | $555,300 | $523,000 |
| Median gross rent | $2,827 | $1,729 | $1,744 |
| Owner-occupied homes | 45% | 43% | 52% |

_Also held: zoning maps for this county (zoning_for_property); hazard ratings (hazards_for_property); infrastructure, utilities and energy nearby (nearby_for_property)._

From Athena by L3R (PROP-BB7EE15E11E023427CB). Sources: Texas GIO, USA Structures (CC BY 4.0), Travis CAD, Census ACS 2020–24.

_This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau._

Zoning, rights or permits for this property? Ask Athena, L3R's assistant → https://3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "status": "MATCHED",
  "query_kind": "ADDRESS",
  "property_key": "PROP-BB7EE15E11E023427CB",
  "parcels": [
    {
      "parcel_id": "192833",
      "parcel_key": "PARCEL-BB7EE15E11E023427CB",
      "namespace": "tx_cad_prop_id:48453",
      "county_fips": "48453",
      "role": "PRIMARY",
      "source": "Texas Geographic Information Office",
      "licence": "CC0 1.0 (public domain dedication)",
      "as_of": "2026-10-13"
    }
  ],
  "buildings": [],
  "related": [],
  "location": {
    "lat": 30.266445,
    "lon": -97.742926,
    "precision": "PARCEL_POINT",
    "source": "Texas Geographic Information Office",
    "licence": "CC0 1.0 (public domain dedication)"
  },
  "geography": {
    "state": "TX",
    "county_fips": "48453",
    "county": "Travis County, Texas",
    "place_geoid": "4805000",
    "place": "Austin city, Texas",
    "tract_geoid": "48453001103",
    "tract_method": "POINT_IN_TRACT"
  },
  "census": {
    "areas": [
      {
        "level": "tract",
        "geoid": "48453001103",
        "name": "Census Tract 11.03; Travis County; Texas",
        "acs": "2020-2024 ACS 5-year",
        "population": {
          "est": 4129.0,
          "moe": 850.0
        },
        "housing_units": {
          "est": 3071.0,
          "moe": 436.0
        },
        "occupied_units": {
          "est": 2826.0,
          "moe": 500.0
        },
        "owner_occupied": {
          "est": 1282.0,
          "moe": 533.0
        },
        "renter_occupied": {
          "est": 1544.0,
          "moe": 336.0
        },
        "owner_share": 0.453645,
        "median_household_income": {
          "est": 166513.0,
          "moe": 42188.0
        },
        "median_home_value": {
          "est": 600000.0,
          "moe": 138677.0
        },
        "median_gross_rent": {
          "est": 2827.0,
          "moe": 216.0
        }
      },
      {
        "level": "place",
        "geoid": "4805000",
        "name": "Austin city, Texas",
        "acs": "2020-2024 ACS 5-year",
        "population": {
          "est": 979539.0,
          "moe": 484.0
        },
        "housing_units": {
          "est": 483071.0,
          "moe": 2022.0
        },
        "occupied_units": {
          "est": 456113.0,
          "moe": 2401.0
        },
        "owner_occupied": {
          "est": 198180.0,
          "moe": 3375.0
        },
        "renter_occupied": {
          "est": 257933.0,
          "moe": 3227.0
        },
        "owner_share": 0.434498,
        "median_household_income": {
          "est": 93658.0,
          "moe": 1670.0
        },
        "median_home_value": {
          "est": 555300.0,
          "moe": 8017.0
        },
        "median_gross_rent": {
          "est": 1729.0,
          "moe": 14.0
        }
      },
      {
        "level": "county",
        "geoid": "48453",
        "name": "Travis County, Texas",
        "acs": "2020-2024 ACS 5-year",
        "population": {
          "est": 1330015.0,
          "moe": null
        },
        "housing_units": {
          "est": 618236.0,
          "moe": 232.0
        },
        "occupied_units": {
          "est": 583747.0,
          "moe": 1810.0
        },
        "owner_occupied": {
          "est": 304165.0,
          "moe": 3566.0
        },
        "renter_occupied": {
          "est": 279582.0,
          "moe": 3455.0
        },
        "owner_share": 0.521056,
        "median_household_income": {
          "est": 99611.0,
          "moe": 1578.0
        },
        "median_home_value": {
          "est": 523000.0,
          "moe": 6613.0
        },
        "median_gross_rent": {
          "est": 1744.0,
          "moe": 13.0
        }
      }
    ],
    "census_notice": "This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau."
  },
  "match": {
    "confidence": 0.95,
    "method": "ADDRESS_POINT/KEY"
  },
  "counts": {
    "parcels": 1,
    "buildings": 0,
    "units": 0
  },
  "truncated": false,
  "property_kind": "fee",
  "summary": "Office building, 1 building, ~546,000 sq ft, built 2002",
  "property_type": {
    "class": "office",
    "name": "Office building",
    "source_code": "F1",
    "source_description": "Commercial real property",
    "source": "Texas Geographic Information Office",
    "licence": "CC0 1.0 (public domain dedication)"
  },
  "building_facts": {
    "count": 1,
    "footprint_sqft": 92100,
    "height_ft": 159,
    "occupancy": "Professional/Technical Services",
    "year_built": 2002,
    "building_area_sqft": 546000,
    "sources": [
      {
        "fields": [
          "property_type"
        ],
        "source": "Texas Geographic Information Office",
        "licence": "CC0 1.0 (public domain dedication)"
      },
      {
        "fields": [
          "count",
          "footprint_sqft",
          "height_ft",
          "occupancy"
        ],
        "source": "FEMA and Oak Ridge National Laboratory, USA Structures",
        "licence": "CC BY 4.0"
      },
      {
        "fields": [
          "year_built",
          "building_area_sqft"
        ],
        "source": "Travis Central Appraisal District",
        "licence": null
      }
    ]
  },
  "attribution": [
    "From Athena by L3R (l3r.io); property key PROP-BB7EE15E11E023427CB",
    "Parcel number: Texas Geographic Information Office",
    "Location: Texas Geographic Information Office (CC0 1.0 (public domain dedication))",
    "U.S. Census Bureau, 2020-2024 ACS 5-year estimates. This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.",
    "Property facts: Texas Geographic Information Office (CC0 1.0 (public domain dedication))",
    "Property facts: FEMA and Oak Ridge National Laboratory, USA Structures (CC BY 4.0)",
    "Property facts: Travis Central Appraisal District"
  ],
  "census_notice": "This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.",
  "athena_url": "https://3drights.com",
  "terms_url": "https://l3r.io/mcp/terms",
  "read_ms": 232,
  "more": {
    "zoning": "SHOWN_IN_COUNTY",
    "hazards": "HELD",
    "nearby": "HELD"
  },
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

**A San Francisco home**

Facts from the Assessor's roll, including bedrooms and bathrooms.

Call:

```json
{"name": "lookup_property", "arguments": {"query": "710 Steiner St, San Francisco, CA"}}
```

Card:

```markdown
### 710 Steiner St, San Francisco, CA
**Single-family home, ~3,683 sq ft, 4 bedrooms, 4 bathrooms (11 rooms), built 1898**

- Parcel: SF block/lot 0803017
- Type: Single-family home (D: Dwelling)
- Buildings: 3 floors
- Units: 1
- Building area: ~3,683 sq ft
- Rooms: 4 bedrooms, 4 bathrooms (11 rooms)
- Year built: 1898

| 2020–2024 ACS | Tract 163 | San Francisco | San Francisco County |
|---|---:|---:|---:|
| Median household income | $135,658 | $140,970 | $140,970 |
| Median home value | $1,161,800 | $1,394,500 | $1,394,500 |
| Median gross rent | $2,267 | $2,476 | $2,476 |
| Owner-occupied homes | 17% | 38% | 38% |

_Also held: hazard ratings (hazards_for_property); infrastructure, utilities and energy nearby (nearby_for_property)._

From Athena by L3R (PROP-41C64FDB3980343D). Sources: San Francisco Assessor-Recorder and DataSF, SF Assessor-Recorder (DataSF), Census ACS 2020–24.

_This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau._

Zoning, rights or permits for this property? Ask Athena, L3R's assistant → https://3drights.com
```

**A New York City lot, by BBL**

The building is named by a landmark record.

Call:

```json
{"name": "lookup_property", "arguments": {"query": "1-00835-0041"}}
```

Card:

```markdown
### Empire State Building
338 5 Avenue, New York, NY 10001
**Office building, 1 building, 102 floors, ~2,812,739 sq ft, built 1931**

- Parcel: NYC BBL 1008350041
- Type: Office building (land use 05, building class O4: Commercial and office buildings)
- Buildings: 1 building, 102 floors
- Units: 513
- Building area: ~2,812,739 sq ft
- Year built: 1931

| 2020–2024 ACS | Tract 76 | New York | New York County |
|---|---:|---:|---:|
| Median household income | $193,644 | $80,483 | $103,931 |
| Median home value | – | $777,600 | $1,090,500 |
| Median gross rent | $3,304 | $1,821 | $2,197 |
| Owner-occupied homes | 30% | 33% | 25% |

_Also held: this city's zoning rules by district (zoning_for_property); hazard ratings (hazards_for_property); infrastructure, utilities and energy nearby (nearby_for_property)._

From Athena by L3R (PROP-D168D2CBF662B6AB). Sources: NYC DOF/DCP (NYC Open Data), NYC PLUTO, NYC LPC, Census ACS 2020–24.

_This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau._

Zoning, rights or permits for this property? Ask Athena, L3R's assistant → https://3drights.com
```

## `census_for_area`

Census basics for the area of an address, a property key or a Census GEOID: population, housing units, occupied, owner-
and renter-occupied units, owner share, median household income, median home value and median gross rent. Each figure
has its 90% margin of error. The source is the 2020–2024 ACS 5-year estimates, shown for the tract, place and county.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `address` | string, at most 200 characters | no | A US street address with city and state, or ZIP. |
| `geoid` | string, at most 200 characters | no | A Census GEOID: 5-digit county, 7-digit place or 11-digit tract. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |

Give exactly one of `address`, `property_key` or `geoid`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Figures returned in `areas`. |
| `NOT_HELD` | No figures held for this area. |
| `NO_PLACE` | The address or key did not resolve to a place. |

### Response fields

- `areas[]`: one entry per level (`tract`, `place`, `county`) with `geoid`, `name` and each figure as `{est, moe}`.
- A missing figure is `null`, never estimated. A Census top or bottom code (for example 250001) carries `top_coded` or
  `bottom_coded` and a display string such as `250,000+`.
- `geography`, `attribution` and `census_notice`. Show the Census notice with the figures.

### Examples


**Figures for an address's area**

Tract, place and county.

Call:

```json
{"name": "census_for_area", "arguments": {"address": "675 Ponce De Leon Ave NE, Atlanta, GA 30308"}}
```

Card:

```markdown
### Census figures: Tract 13.02 / Atlanta / Fulton County

| 2020–2024 ACS | Tract 13.02 | Atlanta | Fulton County |
|---|---:|---:|---:|
| Median household income | $106,661 | $85,652 | $95,292 |
| Median home value | $396,400 | $439,600 | $458,800 |
| Median gross rent | $1,858 | $1,711 | $1,732 |
| Owner-occupied homes | 57% | 46% | 54% |

Population: Tract 13.02 1,916, Atlanta 505,268, Fulton County 1,076,561.

From Athena by L3R (PROP-742CC7940929A11EE71). Sources: Census ACS 2020–24.

_This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau._

Zoning, rights or permits for this property? Ask Athena, L3R's assistant → https://3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "status": "READ",
  "query_kind": "ADDRESS",
  "areas": [
    {
      "level": "tract",
      "geoid": "13121001302",
      "name": "Census Tract 13.02; Fulton County; Georgia",
      "acs": "2020-2024 ACS 5-year",
      "population": {
        "est": 1916.0,
        "moe": 261.0
      },
      "housing_units": {
        "est": 1155.0,
        "moe": 116.0
      },
      "occupied_units": {
        "est": 1093.0,
        "moe": 146.0
      },
      "owner_occupied": {
        "est": 623.0,
        "moe": 197.0
      },
      "renter_occupied": {
        "est": 470.0,
        "moe": 191.0
      },
      "owner_share": 0.569991,
      "median_household_income": {
        "est": 106661.0,
        "moe": 31946.0
      },
      "median_home_value": {
        "est": 396400.0,
        "moe": 117044.0
      },
      "median_gross_rent": {
        "est": 1858.0,
        "moe": 528.0
      }
    },
    {
      "level": "place",
      "geoid": "1304000",
      "name": "Atlanta city, Georgia",
      "acs": "2020-2024 ACS 5-year",
      "population": {
        "est": 505268.0,
        "moe": 79.0
      },
      "housing_units": {
        "est": 265899.0,
        "moe": 2133.0
      },
      "occupied_units": {
        "est": 236468.0,
        "moe": 2330.0
      },
      "owner_occupied": {
        "est": 109792.0,
        "moe": 2262.0
      },
      "renter_occupied": {
        "est": 126676.0,
        "moe": 2540.0
      },
      "owner_share": 0.4643,
      "median_household_income": {
        "est": 85652.0,
        "moe": 1846.0
      },
      "median_home_value": {
        "est": 439600.0,
        "moe": 10668.0
      },
      "median_gross_rent": {
        "est": 1711.0,
        "moe": 22.0
      }
    },
    {
      "level": "county",
      "geoid": "13121",
      "name": "Fulton County, Georgia",
      "acs": "2020-2024 ACS 5-year",
      "population": {
        "est": 1076561.0,
        "moe": null
      },
      "housing_units": {
        "est": 507119.0,
        "moe": 197.0
      },
      "occupied_units": {
        "est": 462481.0,
        "moe": 1915.0
      },
      "owner_occupied": {
        "est": 251193.0,
        "moe": 3472.0
      },
      "renter_occupied": {
        "est": 211288.0,
        "moe": 3701.0
      },
      "owner_share": 0.543142,
      "median_household_income": {
        "est": 95292.0,
        "moe": 1748.0
      },
      "median_home_value": {
        "est": 458800.0,
        "moe": 6100.0
      },
      "median_gross_rent": {
        "est": 1732.0,
        "moe": 16.0
      }
    }
  ],
  "geography": {
    "county_fips": "13121",
    "tract_geoid": "13121001302",
    "place_geoid": "1304000",
    "state": "GA",
    "county": "Fulton County, Georgia",
    "place": "Atlanta city, Georgia"
  },
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Census Bureau, 2020-2024 ACS 5-year estimates. This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau."
  ],
  "athena_url": "https://3drights.com",
  "property_key": "PROP-742CC7940929A11EE71",
  "terms_url": "https://l3r.io/mcp/terms",
  "docs_url": "https://l3r.io/mcp",
  "census_notice": "This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau."
}
```

</details>

## `zoning_for_property`

Base zoning for one property: its district code and description from the city's or county's official zoning map, where
the map's terms allow public display, credited to the publisher with an as-of date. Where the city's zoning code is
compiled (New York City, San Francisco, Pittsburgh, Detroit, Tulsa, Columbus, St. Louis and Boise), the answer adds the
district's rules: floor area ratio, height, setbacks, lot size and density, each with its code section, a short quote and
a link to the code. Where a county has no zoning, such as unincorporated Texas, the answer says so with its legal basis.
That is an answer.

With no property, give `district` and `city` to read one district's rules from the code alone.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | With `district`: the city whose code to read, for example `Tulsa, OK`. With `query`: the address's city. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `district` | string, at most 200 characters | no | A zoning district code, with `city`, when no property is given, for example `RS-3`. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier, as `lookup_property` takes it. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `property_key` or `query`, or `district` with `city`. Not both a property and a district.

### Statuses

| Status | Meaning |
|---|---|
| `SHOWN` | District or districts returned, with rules where the city's code is compiled. |
| `NO_ZONING` | The county has no zoning. `no_zoning` carries the answer and its legal basis. |
| `NOT_SHOWN` | A map for the property is held, but its publisher's terms do not allow showing it here. |
| `NOT_HELD` | No zoning held for this place or district. |
| `DISTRICT_RULES` | Rules for the `district` and `city` asked for, from the code alone. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `zoning.districts[]`: `code`, `name`, `share` of the lot, `primary`, and a `source_ref`.
- `zoning.district_rules`: the code's name and link, and `rules[]`, each with `field`, `value`, `unit`, `condition`,
  `section`, a short `quote` and `as_of`.
- `zoning.no_zoning`: `answer`, `basis` and `exceptions`.
- `zoning.not_applied`: what the answer leaves out.
- `sources[]` with each publisher and as-of date, `disclaimer` and `attribution`.

### Limits

Not a zoning determination. This is base zoning only. Overlays, special districts, variances, pending changes and
recorded restrictions are not applied, and ADU and duplex permission are not answered. Confirm with the city or county
before relying on it.

### Examples


**A district from the official map**

The map's publisher is credited, with an as-of date.

Call:

```json
{"name": "zoning_for_property", "arguments": {"query": "401 Congress Ave, Austin, TX"}}
```

Card:

```markdown
### 401 Congress Ave, Austin, TX
**Zoning (base district)**, map as of 2026-10-31
- CBD-CURE-DDB400 (98% of the lot) — Austin

_Not a zoning determination. Base zoning only: overlays, special districts, variances, pending changes and recorded restrictions are not applied. Confirm with the city or county before relying on it._

From Athena by L3R (PROP-BB7EE15E11E023427CB). Sources: Austin zoning map.

Overlays, permits or what you could build here? Ask Athena, L3R's assistant → https://3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "query_kind": "ADDRESS",
  "property_key": "PROP-BB7EE15E11E023427CB",
  "geography": {
    "state": "TX",
    "county_fips": "48453",
    "county": "Travis County, Texas",
    "place_geoid": "4805000",
    "place": "Austin city, Texas"
  },
  "location": {
    "lat": 30.266445,
    "lon": -97.742926,
    "precision": "PARCEL_POINT",
    "source": "Texas Geographic Information Office",
    "licence": "CC0 1.0 (public domain dedication)"
  },
  "parcels": [
    {
      "parcel_id": "192833",
      "parcel_key": "PARCEL-BB7EE15E11E023427CB",
      "namespace": "tx_cad_prop_id:48453",
      "county_fips": "48453",
      "role": "PRIMARY",
      "source": "Texas Geographic Information Office",
      "licence": "CC0 1.0 (public domain dedication)",
      "as_of": "2026-10-13"
    }
  ],
  "counts": {
    "parcels": 1,
    "buildings": 0,
    "units": 0
  },
  "status": "SHOWN",
  "zoning": {
    "not_applied": [
      "overlays and special districts",
      "variances and conditional approvals",
      "recorded restrictions (deeds, covenants, HOA rules)",
      "pending rezonings",
      "ADU and duplex permission (not answered here yet)"
    ],
    "districts": [
      {
        "code": "CBD-CURE-DDB400",
        "name": null,
        "share": 0.98,
        "primary": true,
        "source_ref": "zoning:tx_austin_zoning"
      }
    ]
  },
  "sources": [
    {
      "ref": "zoning:tx_austin_zoning",
      "name": "Austin zoning map",
      "url": "https://services.arcgis.com/0L95CJ0VTaxqcmED/arcgis/rest/services/PLANNINGCADASTRE_zoning_small_map_scale/FeatureServer/0",
      "licence": null,
      "as_of": "2026-10-31"
    }
  ],
  "disclaimer": "Not a zoning determination. Base zoning only: overlays, special districts, variances, pending changes and recorded restrictions are not applied. Confirm with the city or county before relying on it.",
  "attribution": [
    "From Athena by L3R (l3r.io); property key PROP-BB7EE15E11E023427CB"
  ],
  "athena_url": "https://3drights.com",
  "terms_url": "https://l3r.io/mcp/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

**One district's rules, from the code alone**

Call:

```json
{"name": "zoning_for_property", "arguments": {"district": "RS-3", "city": "Tulsa, OK"}}
```

Card:

```markdown
### Zoning district RS-3, Tulsa, OK

**District rules (RS-3, Tulsa Zoning Code (Title 42))**
- Max height: 35 ft (§ 5.030-A)
- Front setback (Arterial or fwy service rd.): 35 ft (§ 5.030-A)
- Front setback (Other streets): 25 ft (§ 5.030-A)
- Side setback: 5 ft (§ 5.030-A)
- Rear setback: 20 ft (§ 5.030-A)
- Lot area per unit (Detached house): 6,900 sq ft per unit (§ 5.030-A)
- Lot area per unit (Patio house): 6,900 sq ft per unit (§ 5.030-A)
- Lot area per unit (Townhouse): 4,500 sq ft per unit (§ 5.030-A)
- Min lot area (Detached house): 6,900 sq ft (§ 5.030-A)
- Min lot area (Patio house): 6,900 sq ft (§ 5.030-A)
- Min lot area (Townhouse): 4,500 sq ft (§ 5.030-A)
- Min lot width (Detached house): 60 ft (§ 5.030-A)
- Min lot width (Patio house): 60 ft (§ 5.030-A)
- Min lot width (Townhouse): 30 ft (§ 5.030-A)
Code: https://www.municode.com/library/ok/tulsa/codes/code_of_ordinances

_Not a zoning determination. Base zoning only: overlays, special districts, variances, pending changes and recorded restrictions are not applied. Confirm with the city or county before relying on it._

From Athena by L3R. Sources: Tulsa Zoning Code (Title 42).

Overlays, permits or what you could build here? Ask Athena, L3R's assistant → https://3drights.com
```

**A county with no zoning**

Unincorporated Texas. The answer gives its legal basis.

Call:

```json
{"name": "zoning_for_property", "arguments": {"query": "24300 Hamilton Pool Rd, Spicewood, TX 78669"}}
```

Card:

```markdown
### 24300 Hamilton Pool Rd, Spicewood, TX 78669
**Zoning (base district)**
- No county zoning; city rules may apply nearby.
- Basis: Texas counties have no general zoning power: county zoning exists only under narrow statutory exceptions (e.g. lake, airport and military-base areas, Tex. Loc. Gov't Code ch. 231). City zoning applies inside city limits, and a city's extraterritorial jurisdiction regulates subdivision only (LGC 212.003).
- Exceptions: Narrow statutory special-purpose county zoning areas (LGC ch. 231); the answer does not apply inside them. Houston has no zoning ordinance but is a city (its own letter: https://houstontx.gov/planning/DevelopRegs/docs_pdfs/2026/No-Zoning-Letter-and-Boundary-Map-061726.pdf) and is not covered by this source.

_Not a zoning determination. Base zoning only: overlays, special districts, variances, pending changes and recorded restrictions are not applied. Confirm with the city or county before relying on it._

From Athena by L3R (PROP-7E0251FF4880BBBD7D0). Sources: L3R no-zoning answer.

Overlays, permits or what you could build here? Ask Athena, L3R's assistant → https://3drights.com
```

## `hazards_for_property`

Hazard screening for one property. It gives FEMA National Risk Index ratings for the property's Census tract (wildfire,
earthquake, inland and coastal flooding, hurricane, tornado, heat wave, hail and more, plus the overall rating) with
FEMA's required statement. It also counts EPA Superfund (NPL) and brownfield sites within 1 mile of the property's public
point, with links to EPA's records.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give exactly one of `property_key` or `query`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Ratings and EPA sites returned. |
| `PARTIAL` | Part of the screening is held, for example ratings without a point for the EPA search. |
| `NOT_HELD` | Neither is held for this property. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `hazards.risk_index`: `tract_geoid`, `overall`, `expected_annual_loss`, `ratings` by hazard, `basis` and FEMA's `statement`.
- `hazards.cleanups`: `within_miles`, counts of `superfund_npl` and `brownfields`, and `sites[]` with `program`, `status`, `distance_mi` and an EPA `url`.
- `hazards.flood`: why no flood zone is given.
- `not_held[]`, `disclaimer`, `sources[]` and `attribution`.

### Limits

A rating describes the Census tract, not the parcel. The FEMA flood zone is not given yet, and not being shown in a
mapped flood zone never means no flood risk. An EPA site nearby is not a finding about the property, and absence from
EPA's lists is not a clean bill. Screening information only, not a hazard, flood or environmental determination.

### Examples


**Tract ratings and nearby EPA sites**

Ratings for the tract. No Superfund or brownfield sites are within a mile.

Call:

```json
{"name": "hazards_for_property", "arguments": {"query": "1200 Getty Center Dr, Los Angeles, CA 90049"}}
```

Card:

```markdown
### 1200 Getty Center Dr, Los Angeles, CA 90049
**Hazards (screening)**
- Overall risk (FEMA National Risk Index, tract 06037262302): Relatively High
- Wildfire: Relatively Moderate · Earthquake: Relatively High · Inland flooding: Relatively High · Tornado: Very Low · Heat wave: Very Low
- _FEMA tract rating, planning only: a rating for the Census tract, not an assessment of this parcel_
- Flood zone: not given. FEMA's flood map (NFHL) is not loaded yet, so no flood zone is given here. Not being shown in a mapped flood zone never means no flood risk.
- EPA sites within 1 mile: 0 Superfund (NPL); 0 brownfields
- _EPA sites within 1 mile of the property's public point (straight-line distance); a nearby site is not a finding about this property, and absence from EPA's lists is not a clean bill_

_Screening information only, not a hazard, flood or environmental determination. Tract ratings describe the Census tract, not this parcel._

_This product uses the Federal Emergency Management Agency's National Risk Index dataset API or downloadable datasets but is not endorsed by FEMA. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency's website(s)._

From Athena by L3R (PROP-E667A394F6BE301459D). Sources: FEMA National Risk Index, EPA FRS.

Zoning, rights or permits for this property? Ask Athena, L3R's assistant → https://3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "query_kind": "ADDRESS",
  "property_key": "PROP-E667A394F6BE301459D",
  "geography": {
    "state": "CA",
    "county_fips": "06037",
    "county": "Los Angeles County, California",
    "place_geoid": "0644000",
    "place": "Los Angeles city, California"
  },
  "location": {
    "lat": 34.082794,
    "lon": -118.475323,
    "precision": "PARCEL_POINT",
    "source": "County of Los Angeles",
    "licence": "Open data, shown with attribution"
  },
  "parcels": [
    {
      "parcel_id": "4429037025",
      "parcel_key": "PARCEL-E667A394F6BE301459D",
      "namespace": "apn:06037",
      "county_fips": "06037",
      "role": "PRIMARY",
      "source": "County of Los Angeles",
      "licence": "Open data, shown with attribution",
      "as_of": "2026-10-13"
    }
  ],
  "counts": {
    "parcels": 1,
    "buildings": 0,
    "units": 0
  },
  "status": "READ",
  "hazards": {
    "risk_index": {
      "tract_geoid": "06037262302",
      "overall": "Relatively High",
      "expected_annual_loss": "Relatively High",
      "ratings": {
        "avalanche": "Not Applicable",
        "coastal_flooding": "No Rating",
        "cold_wave": "No Rating",
        "drought": "Very Low",
        "earthquake": "Relatively High",
        "hail": "Very Low",
        "heat_wave": "Very Low",
        "hurricane": "No Rating",
        "ice_storm": "Not Applicable",
        "inland_flooding": "Relatively High",
        "landslide": "Relatively Low",
        "lightning": "Very Low",
        "strong_wind": "Very Low",
        "tornado": "Very Low",
        "tsunami": "Not Applicable",
        "volcanic_activity": "Not Applicable",
        "wildfire": "Relatively Moderate",
        "winter_weather": "Very Low"
      },
      "basis": "FEMA tract rating, planning only: a rating for the Census tract, not an assessment of this parcel",
      "nri_version": "December 2025",
      "source_ref": "fema_nri",
      "statement": "This product uses the Federal Emergency Management Agency's National Risk Index dataset API or downloadable datasets but is not endorsed by FEMA. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency's website(s)."
    },
    "flood": {
      "basis": "FEMA's flood map (NFHL) is not loaded yet, so no flood zone is given here. Not being shown in a mapped flood zone never means no flood risk."
    },
    "cleanups": {
      "within_miles": 1.0,
      "superfund_npl": 0,
      "superfund_npl_current": 0,
      "brownfields": 0,
      "sites": [],
      "basis": "EPA sites within 1 mile of the property's public point (straight-line distance); a nearby site is not a finding about this property, and absence from EPA's lists is not a clean bill",
      "source_ref": "epa_cleanups",
      "point_precision": "PARCEL_POINT"
    }
  },
  "sources": [
    {
      "ref": "fema_nri",
      "name": "FEMA National Risk Index, census tracts (version 1.20.0, December 2025)",
      "url": "https://hazards.fema.gov/nri/",
      "licence": "FEMA National Risk Index terms (planning use, cited)",
      "as_of": "2026-10-18"
    },
    {
      "ref": "epa_cleanups",
      "name": "U.S. EPA Facility Registry Service: Superfund NPL (SEMS) and brownfields (ACRES) sites",
      "url": "https://www.epa.gov/frs",
      "licence": "Public domain (17 U.S.C. 105); credit EPA",
      "as_of": null
    }
  ],
  "not_held": [
    {
      "what": "FEMA flood zone",
      "why": "FEMA's NFHL flood map is not loaded yet"
    }
  ],
  "disclaimer": "Screening information only, not a hazard, flood or environmental determination. Tract ratings describe the Census tract, not this parcel.",
  "attribution": [
    "From Athena by L3R (l3r.io); property key PROP-E667A394F6BE301459D",
    "FEMA National Risk Index, census tracts (version 1.20.0, December 2025). This product uses the Federal Emergency Management Agency's National Risk Index dataset API or downloadable datasets but is not endorsed by FEMA. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency's website(s).",
    "U.S. EPA Facility Registry Service: Superfund NPL (SEMS) and brownfields (ACRES) sites (Public domain (17 U.S.C. 105); credit EPA)"
  ],
  "athena_url": "https://3drights.com",
  "terms_url": "https://l3r.io/mcp/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `nearby_for_property`

What is around a property, kept short: the nearest item in each category, with its straight-line distance (miles, or feet
under 0.1 mile) and its source. Pass `topics` to answer only what was asked.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `limit` | integer, 1 to 3 | no | Items per category, 1 to 3. Default 1. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `topics` | array of strings | no | Only these categories. See the table below. Default: all but `towers` and `mines`. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give exactly one of `property_key` or `query`.

### Topics

| Topic | What it returns |
|---|---|
| `utilities` | EPA water service area at the point, nearest community water system and wastewater plant. |
| `transport` | Nearest interstate, US or state highway, rail line, public-use airport and port. |
| `energy` | Nearest EIA-860 power plant: fuel and MW. |
| `renewables` | Nearest solar, wind or storage project, operating or proposed, within 10 miles. |
| `data_centers` | Registry rows that a government record places: name, status and MW. |
| `community` | Nearest public school (NCES) and hospital (CMS). |
| `broadband` | Top fixed providers at the point with max advertised speeds, from the FCC National Broadband Map. Satellite is not listed. |
| `ev` | Nearest open public EV charging station (AFDC): network, DC fast and Level 2 ports. |
| `towers` | FCC-registered antenna structures: type and height. Only when asked. |
| `mines` | Active MSHA mines and quarries: commodity. Only when asked. |

### Response fields

- `status` is `READ` when the property has a point. Otherwise the lookup's own status (`AMBIGUOUS`, `UNMATCHED` and so on) comes back with its `reason`.
- `nearby`: one object per topic group, each item with `name`, `distance_mi`, the kind-specific fields, `source` and `licence`.
- `not_held[]`: categories with nothing held. A category left off the card never means the thing does not exist.
- `topics`, `limit`, `attribution` and `location`.

### Limits

`limit` is 1 to 3 items per category, and a value outside that range is refused. Substations, transmission lines and
interconnection queues are not shown yet. Data comes from federal open data (EIA, EPA, FAA, BTS NTAD, Census TIGER,
NCES, CMS, FCC, MSHA) and official public records. Company names such as a plant's operating utility do show. Owners,
values and sales do not.

### Examples


**The default card**

Call:

```json
{"name": "nearby_for_property", "arguments": {"query": "401 Congress Ave, Austin, TX"}}
```

Card:

```markdown
### Around 401 Congress Ave, Austin, TX
- **Utilities:** inside a community water system's water service area [EPA]; wastewater plant Goforth Wwtp 4.3 mi [EPA ECHO]
- **Transport:** I-35 0.48 mi [TIGER]; E 1st St 0.23 mi [TIGER]; rail Central Subdivision (AWRR) 0.23 mi [NTAD]; airport Austin-Bergstrom International (AUS) 6.6 mi [FAA]; port Victoria, TX 112.6 mi [NTAD]
- **Energy:** Hal C Weaver Power Plant (natural gas, 152 MW, operated by University of Texas at Austin) 1.5 mi [EIA-860]; renewable Austin (hydroelectric, 18 MW, operated by Lower Colorado River Authority) 3.1 mi [EIA-860]
- **Schools and hospitals:** school Sanchez El (Elementary, grades PK-06) 0.74 mi [NCES]; hospital Dell Seton Med Center At The University Of Tx (Acute Care Hospitals) about 0.8 mi [CMS]
- **EV charging within 10 mi:** ChargePoint Network, 2 Level 2 430 ft [AFDC]

From Athena by L3R (PROP-BB7EE15E11E023427CB). Sources: EPA water service areas, EPA ECHO, Census TIGER/Line, BTS NTAD rail, FAA/BTS NTAD airports, USACE/BTS NTAD ports, U.S. Energy Information Administration, Form EIA-860 2025, NCES schools, CMS hospitals, U.S. DOE Alternative Fuels Data Center, NLR data; no endorsement implied. Straight-line distances.

Power, water, access or rights here? Ask Athena, L3R's assistant → https://3drights.com
```

**Three topics, two items each**

`topics` narrows the answer and `limit` raises the count.

Call:

```json
{"name": "nearby_for_property", "arguments": {"query": "30 W Pershing Rd, Kansas City, MO 64108", "topics": ["energy", "transport", "ev"], "limit": 2}}
```

Card:

```markdown
### Around 30 W Pershing Rd, Kansas City, MO 64108
- **Transport:** I-35 0.42 mi [TIGER]; US Hwy 71 0.76 mi [TIGER]; rail Main Tracks Subdivision (KCTL) 0.18 mi [NTAD]; airport Kansas City Downtown/Wheeler Field (MKC) 2.7 mi [FAA]; airport Kansas City/Lee'S Summit Regional (LXT) 14.3 mi [FAA]; port Heartland Port Authority, MO 142.3 mi [NTAD]; port Mid-America Port, IA, IL and MO 187.2 mi [NTAD]
- **Energy:** Grand Ave Plant (natural gas, 5.0 MW, operated by Vicinity Energy Kansas City) 1.9 mi [EIA-860]; Northeast (MO) (petroleum, 540 MW, operated by Evergy Metro) 3.0 mi [EIA-860]
- **EV charging within 10 mi:** ChargePoint Network, 2 Level 2 0.11 mi [AFDC]; ChargePoint Network, 2 Level 2 0.11 mi [AFDC]

From Athena by L3R. Sources: Census TIGER/Line, BTS NTAD rail, FAA/BTS NTAD airports, USACE/BTS NTAD ports, U.S. Energy Information Administration, Form EIA-860 2025, U.S. DOE Alternative Fuels Data Center, NLR data; no endorsement implied. Straight-line distances.

Power, water, access or rights here? Ask Athena, L3R's assistant → https://3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "status": "READ",
  "query_kind": "ADDRESS",
  "what_would_resolve": [
    "the parcel number with its county"
  ],
  "reason": "NOT_IN_OPEN_INDEX",
  "geography": {
    "state": "MO",
    "county": "Jackson County, Missouri",
    "place": "Kansas City city, Missouri",
    "county_fips": "29095"
  },
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Census Bureau TIGER/Line 2026 primary and secondary roads (U.S. Government work, not copyrighted)",
    "North American Rail Network via BTS NTAD (U.S. Government work)",
    "FAA airports via BTS NTAD (U.S. Government work)",
    "USACE principal ports via BTS NTAD (U.S. Government work)",
    "U.S. Energy Information Administration, Form EIA-860 2025 (public domain)",
    "U.S. DOE Alternative Fuels Data Center, NLR data; no endorsement implied (AFDC data terms)"
  ],
  "location": {
    "lat": 39.083959,
    "lon": -94.584678,
    "precision": "ADDRESS_RANGE"
  },
  "status_detail": "LOCATION_ONLY",
  "nearby": {
    "transport": {
      "interstate": [
        {
          "name": "I-35",
          "distance_mi": 0.42,
          "kind": "interstate",
          "route": "I-35",
          "source": "U.S. Census Bureau TIGER/Line 2026 primary and secondary roads",
          "licence": "U.S. Government work, not copyrighted"
        }
      ],
      "major_road": [
        {
          "name": "US Hwy 71",
          "distance_mi": 0.76,
          "kind": "primary",
          "route": "US Hwy 71",
          "source": "U.S. Census Bureau TIGER/Line 2026 primary and secondary roads",
          "licence": "U.S. Government work, not copyrighted"
        }
      ],
      "rail_line": [
        {
          "name": "Main Tracks Subdivision",
          "distance_mi": 0.18,
          "kind": "rail",
          "railroad": "KCTL",
          "source": "North American Rail Network via BTS NTAD",
          "licence": "U.S. Government work"
        }
      ],
      "airport": [
        {
          "name": "Kansas City Downtown/Wheeler Field",
          "distance_mi": 2.7,
          "kind": "commercial service",
          "ident": "MKC",
          "source": "FAA airports via BTS NTAD",
          "licence": "U.S. Government work"
        },
        {
          "name": "Kansas City/Lee'S Summit Regional",
          "distance_mi": 14.3,
          "kind": "public use",
          "ident": "LXT",
          "source": "FAA airports via BTS NTAD",
          "licence": "U.S. Government work"
        }
      ],
      "port": [
        {
          "name": "Heartland Port Authority, MO",
          "distance_mi": 142.3,
          "kind": "principal port",
          "source": "USACE principal ports via BTS NTAD",
          "licence": "U.S. Government work"
        },
        {
          "name": "Mid-America Port, IA, IL and MO",
          "distance_mi": 187.2,
          "kind": "principal port",
          "source": "USACE principal ports via BTS NTAD",
          "licence": "U.S. Government work"
        }
      ]
    },
    "energy": {
      "power_plants": [
        {
          "name": "Grand Ave Plant",
          "distance_mi": 1.9,
          "fuel": "natural gas",
          "mw": 5.0,
          "status": "operating",
          "ident": "EIA 58205",
          "operator": "Vicinity Energy Kansas City",
          "source": "U.S. Energy Information Administration, Form EIA-860 2025",
          "licence": "public domain"
        },
        {
          "name": "Northeast (MO)",
          "distance_mi": 3.0,
          "fuel": "petroleum",
          "mw": 540.0,
          "status": "operating",
          "ident": "EIA 2081",
          "operator": "Evergy Metro",
          "source": "U.S. Energy Information Administration, Form EIA-860 2025",
          "licence": "public domain"
        }
      ]
    },
    "ev": {
      "stations": [
        {
          "distance_mi": 0.11,
          "kind": "Level 2",
          "ident": "AFDC 80525",
          "source": "U.S. DOE Alternative Fuels Data Center, NLR data; no endorsement implied",
          "licence": "AFDC data terms",
          "network": "ChargePoint Network",
          "ports": "2 Level 2"
        },
        {
          "distance_mi": 0.11,
          "kind": "Level 2",
          "ident": "AFDC 172022",
          "source": "U.S. DOE Alternative Fuels Data Center, NLR data; no endorsement implied",
          "licence": "AFDC data terms",
          "network": "ChargePoint Network",
          "ports": "2 Level 2"
        }
      ]
    }
  },
  "not_held": [
    {
      "category": "substation",
      "note": "Not shown: no open national substation layer."
    },
    {
      "category": "transmission_line",
      "note": "Not shown: no national transmission-line layer is available for public display."
    },
    {
      "category": "interconnection_queue",
      "note": "Not shown: the RTO queue lists name a county, not a point, and no national compilation is available for public display."
    }
  ],
  "topics": [
    "transport",
    "energy",
    "ev"
  ],
  "limit": 2,
  "build": "p1-20261106",
  "version": "v3",
  "terms_url": "https://l3r.io/mcp/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `districts_for_property`

The districts a property or point sits in: its U.S. House district, its state senate and state house districts, its school districts, and its county, place and Census tract. The boundaries are Census TIGER/Line maps. The U.S. House district is the one for the 119th Congress, which sits until January 3, 2027. Where the map changed for the 120th Congress, the answer gives that district too and says when it starts. At-large states and the non-voting seats of DC and Puerto Rico say so. DC has no state legislature. Nebraska has one chamber.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `lat` | number, -90 to 90 | no | Latitude of one point, WGS84 decimal degrees, for example `30.2747`. Use with `lon`, instead of `query`. |
| `lon` | number, -180 to 180 | no | Longitude of the same point, WGS84 decimal degrees, for example `-97.7404`. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `property_key`, `query`, or `lat` with `lon`. Not a property and a point together.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Districts returned. |
| `NO_POINT` | The property has no public point and no Census tract to read. |
| `NOT_HELD` | The district maps are not available right now. |
| `OUTSIDE_COVERAGE` | A point outside the 50 states, DC and Puerto Rico. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `districts.us_house`: `congress`, `district`, `name`, `at_large`, `voting`, `until`, and `same_next`. `same_next` says whether the district stays the same from January 3, 2027. When it changes, `us_house_next` gives the new one, with its start date in `from`.
- `districts.state_senate` and `districts.state_house`: `district`, `geoid` and `name`, as the Census prints them.
- `districts.school[]`: `kind` (`unified`, `elementary` or `secondary`), `geoid`, `name` and `grades`.
- `basis` says how the districts were found: the property's point, the parcel's point, or the Census tract. A tract split between districts lists every district it spans, with shares.
- A point close to a district line is flagged.
- `geography`, `not_held[]`, `confirm_url`, `disclaimer` and `attribution`.

### Limits

District names and numbers only. No representatives' names, precincts or polling places. Census boundaries are drawn for statistics. They are not a legal determination: the state or local election office places each address. The answer links to vote.gov for election offices.

### Examples

**A property, by address**

U.S. House, state legislature and school district for a San Francisco address. The lookup matched the address to 1019 Stockton St.

Call:

```json
{"name": "districts_for_property", "arguments": {"query": "1021 Stockton St, San Francisco, CA"}}
```

Card:

```markdown
### Districts at 1019 Stockton St, San Francisco, CA
- **U.S. House (119th Congress):** California's 11th district; the same district from January 3, 2027
- **State senate:** State Senate District 11
- **State house:** Assembly District 17
- **School district (unified):** San Francisco Unified School District, grades K-12
- **County and place:** San Francisco County, in San Francisco, CA

_Read at the property's point. Census boundaries drawn for statistics, not a legal determination: the state or local election office places each address. Election offices by state: https://vote.gov/_

From Athena by L3R (PROP-440992A6740C3CD4). Sources: Census TIGER/Line.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "status": "READ",
  "query_kind": "ADDRESS",
  "property_key": "PROP-440992A6740C3CD4",
  "match": {
    "confidence": 0.95,
    "method": "ADDRESS"
  },
  "athena_url": "https://3drights.com",
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Census Bureau, TIGER/Line Shapefiles (2025: 119th Congress districts) (public domain; credit the U.S. Census Bureau)",
    "U.S. Census Bureau, TIGER/Line Shapefiles (2026: state legislative districts, upper) (public domain; credit the U.S. Census Bureau)",
    "U.S. Census Bureau, TIGER/Line Shapefiles (2026: state legislative districts, lower) (public domain; credit the U.S. Census Bureau)",
    "U.S. Census Bureau, TIGER/Line Shapefiles (2026: unified school districts) (public domain; credit the U.S. Census Bureau)"
  ],
  "disclaimer": "Census boundaries drawn for statistics, not a legal determination: the state or local election office places each address.",
  "geography": {
    "state": "CA",
    "county": "San Francisco County, California",
    "place": "San Francisco city, California",
    "county_fips": "06075",
    "place_geoid": "0667000",
    "tract_geoid": "06075011300"
  },
  "location": {
    "address": "1019 STOCKTON ST",
    "lat": 37.795262,
    "lon": -122.408496
  },
  "status_detail": "MATCHED",
  "districts": {
    "us_house": {
      "congress": 119,
      "district": "11",
      "geoid": "0611",
      "name": "Congressional District 11",
      "at_large": false,
      "voting": true,
      "basis": "PROPERTY_POINT",
      "until": "2027-01-03",
      "same_next": true
    },
    "state_senate": {
      "district": "11",
      "geoid": "06011",
      "name": "State Senate District 11",
      "basis": "PROPERTY_POINT"
    },
    "state_house": {
      "district": "17",
      "geoid": "06017",
      "name": "Assembly District 17",
      "basis": "PROPERTY_POINT"
    },
    "school": [
      {
        "kind": "unified",
        "geoid": "0634410",
        "name": "San Francisco Unified School District",
        "grades": "K-12",
        "basis": "PROPERTY_POINT"
      }
    ]
  },
  "not_held": [],
  "basis": "PROPERTY_POINT",
  "confirm_url": "https://vote.gov/",
  "build": "p1-20261106",
  "version": "v1",
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

**A point in DC**

A point instead of an address. DC has a non-voting delegate and no state legislature.

Call:

```json
{"name": "districts_for_property", "arguments": {"lat": 38.8899, "lon": -77.0091}}
```

Card:

```markdown
### Districts at 38.88990, -77.00910 (Washington, DC)
- **U.S. House (119th Congress):** the District of Columbia's Delegate (at large, non-voting); the same district from January 3, 2027
- **State legislature:** The District of Columbia has no state legislature (its Council is elected by ward and at large).
- **School district (unified):** District of Columbia Public Schools, grades PK-12
- **County and place:** District of Columbia, in Washington, DC

_Read at the point. Census boundaries drawn for statistics, not a legal determination: the state or local election office places each address. Election offices by state: https://vote.gov/_

From Athena by L3R. Sources: Census TIGER/Line.

More: 3drights.com
```

## `energy_service_for_property`

What energy a property connects to, one layer at a time. Each layer has its source and how certain it is. The layers are the grid (the balancing authority and the ISO or RTO, such as ERCOT, CAISO, PJM, MISO, SPP, NYISO or ISO-NE), the electric delivery utility (the wires company), the retail supplier, and the natural gas utility. The nearest power plant is listed for context. The supplier is a community choice or municipal aggregation programme as the default, customer choice where the state has it, or the utility itself.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give exactly one of `property_key` or `query`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Layers returned. A layer that is not held is listed in `not_held`. |
| `NO_POINT` | The property has no point or county to read. |
| `NOT_HELD` | The energy data is not available right now. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `energy_service.grid`: `code`, `name`, `rto`, `interconnect`, `certainty`, `basis`, `source` and `licence`.
- `energy_service.delivery`: the wires utility `name`, `utility_type`, `certainty`, `basis`, and `others[]` with the other utilities in the county.
- `energy_service.supplier`: `choice` (`utility` or `customer choice`), or, for a community choice or municipal aggregation programme, `programme`, `kind`, `operator`, `opt_out` and `url`, `certainty`, `state_status`, `basis` and `note`.
- `energy_service.plants[]`: the nearest plant, with `distance_mi`, `fuel`, `mw` and `status`.
- `certainty` is `INSIDE_MAP` where an open state map holds the point, `PLACE` or `COUNTY` where a city's or county's utility is read from EIA-861 (worded "likely"), and `STATE` for a state-wide fact such as retail choice.
- `not_held[]`, `geography`, `location` and `attribution`.

### Limits

This is the general setup for the location. It is not a record for one house: the owner's bill shows the actual supplier and plan. A single wires utility is named only where a state map holds the point. Otherwise it is the utility EIA-861 lists for the county, worded "likely", with the others named. Natural gas is given only where an open state map holds it. Electricity data is EIA-861 (2025) and EIA-860. Utility names are company names.

### Examples

**A county with two utilities**

Menlo Park, California. No open territory map places the point, so the wires utility is "likely". The city's community choice programme, if any, is not held.

Call:

```json
{"name": "energy_service_for_property", "arguments": {"query": "870 Santa Cruz Ave, Menlo Park, CA"}}
```

Card:

```markdown
### Energy at 870 Santa Cruz Ave, Menlo Park, CA
- **Grid:** CAISO (California ISO) (CISO balancing authority) [EIA-861]
- **Wires (delivery):** likely Pacific Gas & Electric Co.; 2 utilities serve this county (also City & County of San Francisco) (investor-owned utility) [EIA-861]
- **Supplier:** the utility itself (bundled service) [EIA-861]. Community choice aggregators serve many California cities in this utility's territory; the city's programme, if any, is not held here.
- **Natural gas:** not held. No open natural gas service-territory map is held for this location; CA gas retail choice: partial.
- **Nearest plant:** SRI International Cogen Project 0.79 mi [EIA-860]. A house draws from the grid as a whole, not from any one plant; the plants below are only what is nearby.

That's the general setup for this location, not a record for this house; the owner's bill shows the actual supplier and plan.

From Athena by L3R (PROP-2B077424A725D5AEC0C). Sources: U.S. EIA Form EIA-861 service territories, via Catalyst Cooperative PUDL (CC BY 4.0), U.S. EIA Form EIA-861 sales, reliability and balancing authorities, via Catalyst Cooperative PUDL (CC BY 4.0), U.S. Energy Information Administration, Form EIA-860 2025.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "status": "READ",
  "query_kind": "ADDRESS",
  "property_key": "PROP-2B077424A725D5AEC0C",
  "match": {
    "confidence": 0.9,
    "method": "ADDRESS"
  },
  "athena_url": "https://3drights.com",
  "geography": {
    "state": "CA",
    "county": "San Mateo County, California",
    "place": "Menlo Park city, California",
    "county_fips": "06081",
    "place_geoid": "0646870"
  },
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. EIA Form EIA-861 service territories, via Catalyst Cooperative PUDL (CC BY 4.0)",
    "U.S. EIA Form EIA-861 sales, reliability and balancing authorities, via Catalyst Cooperative PUDL (CC BY 4.0)",
    "U.S. Energy Information Administration, Form EIA-860 2025 (public domain)"
  ],
  "location": {
    "lat": 37.450466,
    "lon": -122.185926
  },
  "status_detail": "MATCHED",
  "energy_service": {
    "grid": {
      "code": "CISO",
      "name": "California Independent System Operator",
      "rto": "CAISO (California ISO)",
      "interconnect": "western",
      "certainty": "COUNTY",
      "basis": "every wires utility EIA-861 lists for this county reports to this balancing authority",
      "source": "U.S. EIA Form EIA-861 sales, reliability and balancing authorities, via Catalyst Cooperative PUDL",
      "licence": "CC BY 4.0"
    },
    "delivery": {
      "name": "Pacific Gas & Electric Co.",
      "certainty": "LIKELY",
      "utility_type": "investor-owned utility",
      "n_utilities": 2,
      "basis": "the largest of the 2 utilities EIA-861 lists for this county, by distribution customers; no open territory map places the point",
      "source": "U.S. EIA Form EIA-861 service territories, via Catalyst Cooperative PUDL",
      "licence": "CC BY 4.0",
      "others": [
        {
          "name": "City & County of San Francisco"
        }
      ]
    },
    "supplier": {
      "choice": "utility",
      "certainty": "STATE",
      "state_status": "partial",
      "basis": "homes here buy supply from the utility (bundled service; no residential retail marketer sales in the state, EIA-861)",
      "source": "U.S. EIA Form EIA-861 sales, reliability and balancing authorities, via Catalyst Cooperative PUDL",
      "licence": "CC BY 4.0",
      "note": "Community choice aggregators serve many California cities in this utility's territory; the city's programme, if any, is not held here."
    },
    "plants": [
      {
        "name": "SRI International Cogen Project",
        "distance_mi": 0.79,
        "fuel": "natural gas",
        "mw": 6.0,
        "status": "operating",
        "ident": "EIA 50537",
        "operator": "IPT SRI Cogeneration Inc",
        "role": "nearest",
        "source": "U.S. Energy Information Administration, Form EIA-860 2025",
        "licence": "public domain"
      }
    ],
    "wording": "That's the general setup for this location, not a record for this house; the owner's bill shows the actual supplier and plan."
  },
  "not_held": [
    {
      "category": "gas",
      "note": "No open natural gas service-territory map is held for this location; CA gas retail choice: partial."
    }
  ],
  "build": "p1-20261106",
  "version": "2026-11-10",
  "year": 2025,
  "census": false,
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `site_screen_for_property`

A development site screen for one property, from federal open data. It covers flood zone, wetlands, protected areas, contamination, terrain and sewer service.

- **Flood:** FEMA flood zones with the share of the lot in each, whether the lot is in a Special Flood Hazard Area, and the FIRM panel and its effective date.
- **Wetlands:** USFWS National Wetlands Inventory wetlands, with the share of the lot and the type.
- **Protected areas:** USGS PAD-US areas on or within half a mile of the lot, with GAP status and manager type. Names are given only for public agencies.
- **Contamination:** EPA sites within 1 mile, with distances and EPA links. These are Superfund (NPL) and other SEMS sites, ACRES brownfields, RCRA corrective action areas, federal facilities, and leaking underground storage tank releases from EPA's UST Finder, open or closed.
- **Terrain:** USGS 3DEP minimum, maximum and mean elevation, and the share of the lot by slope band: 0 to 5, 5 to 15, 15 to 30 and over 30 percent.
- **Sewer:** an open sewer service-area layer where one exists. Otherwise it says so and names the nearest wastewater plant.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give exactly one of `property_key` or `query`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Every layer returned. |
| `PARTIAL` | Some layers returned. The others are in `not_held`. |
| `NOT_HELD` | No layer held for this place. |
| `NO_POINT` | The property has no public point to screen. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `site.basis` says what the layers were read against: the parcel outline where L3R has screened it, else the property's point. The card says which.
- `site.flood` (`zones[]`, `sfha`, `panel`), `site.wetlands`, `site.protected_areas[]`, `site.contamination`, `site.terrain` (`elevation_ft`, `slope_bands_pct[]`) and `site.sewer`. A layer that is not held is left out.
- `not_held[]`: each layer not held, with `what` and `why`. A layer not held never means the hazard is absent.
- `sources[]` with each publisher, licence and as-of date, `disclaimer` and `attribution`.

### Limits

Screening only. It is not a flood determination, a wetland delineation, a Phase I environmental site assessment or a survey. Not being in a mapped flood zone or wetland never means no flood or wetland. Confirm with the agencies before relying on it. Layers are loaded state by state and area by area. At the time of these examples the FEMA flood map and the terrain tiles were not held for the addresses below, and the answer said so.

### Examples

**Wetlands, parks, contamination and sewer**

Menlo Park, California. The flood and terrain layers are not held here yet, so the status is `PARTIAL` and both are listed in `not_held`.

Call:

```json
{"name": "site_screen_for_property", "arguments": {"query": "870 Santa Cruz Ave, Menlo Park, CA"}}
```

Card:

```markdown
### Site screen: 870 Santa Cruz Ave, Menlo Park, CA
_Read at the property's point (no screened parcel outline is held for it)._
- **Wetlands:** none mapped at the point [USFWS NWI]
- **Protected areas:** Fremont Park (local government-managed, GAP 4) 440 ft; Nealon Park (local government-managed, GAP 4) 0.28 mi; Jack W. Lyle Park (local government-managed, GAP 4) 0.38 mi [PAD-US]
- **Contamination within 1 mi:** 26 leaking underground tank release; nearest: Leaking underground storage tank (state list) 0.17 mi [EPA FRS, EPA RCRA, EPA UST Finder]
- **Sewer:** No open sewer service-area layer for this place; nearest wastewater plant Palo Alto Regional Water Quality Control Plant 4.2 mi [EPA ECHO]
- Not held: FEMA flood zone (FEMA's flood map (NFHL) is not held for this state yet, so no flood zone is given here).
- Not held: terrain (3DEP elevation and slope) (the 3DEP elevation tile for this point is not held or could not be read in time).

_Screening only: not a flood zone determination, wetland delineation, Phase I environmental site assessment or survey. Not being in a mapped flood zone or wetland never means no flood or wetland. Confirm with the agencies before relying on it._

From Athena by L3R (PROP-2B077424A725D5AEC0C). Sources: U.S. Fish and Wildlife Service, National Wetlands Inventory, USGS Protected Areas Database of the United States (PAD-US) 4.1, U.S. EPA Facility Registry Service: remediation sites (SEMS, ACRES, FFDOCKET, BRAC, LUST-ARRA), U.S. EPA RCRA corrective action areas, U.S. EPA UST Finder: leaking underground storage tank releases (national composite of state data, 2018-2021), U.S. EPA ECHO facility records.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "status": "PARTIAL",
  "query_kind": "ADDRESS",
  "property_key": "PROP-2B077424A725D5AEC0C",
  "match": {
    "confidence": 0.9,
    "method": "ADDRESS"
  },
  "athena_url": "https://3drights.com",
  "geography": {
    "state": "CA",
    "county": "San Mateo County, California",
    "place": "Menlo Park city, California",
    "county_fips": "06081"
  },
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. EPA ECHO facility records (U.S. Government work)",
    "U.S. Fish and Wildlife Service, National Wetlands Inventory (U.S. Government work)",
    "USGS Protected Areas Database of the United States (PAD-US) 4.1 (public domain)",
    "U.S. EPA Facility Registry Service: remediation sites (SEMS, ACRES, FFDOCKET, BRAC, LUST-ARRA) (U.S. Government work)",
    "U.S. EPA RCRA corrective action areas (U.S. Government work)",
    "U.S. EPA UST Finder: leaking underground storage tank releases (national composite of state data, 2018-2021) (U.S. Government work)"
  ],
  "disclaimer": "Screening only: not a flood zone determination, wetland delineation, Phase I environmental site assessment or survey. Not being in a mapped flood zone or wetland never means no flood or wetland. Confirm with the agencies before relying on it.",
  "location": {
    "lat": 37.450466,
    "lon": -122.185926,
    "precision": "PARCEL_POINT"
  },
  "status_detail": "MATCHED",
  "site": {
    "basis": "POINT",
    "wetlands": {
      "inside": false,
      "types": []
    },
    "protected_areas": [
      {
        "name": "Fremont Park",
        "manager_type": "local government",
        "manager": "CITY",
        "gap_status": "GAP 4 (no known mandate for protection)",
        "designation": "Local Park",
        "category": "Fee",
        "distance_mi": 0.08,
        "distance_ft": 440
      },
      {
        "name": "Nealon Park",
        "manager_type": "local government",
        "manager": "CITY",
        "gap_status": "GAP 4 (no known mandate for protection)",
        "designation": "Local Park",
        "category": "Fee",
        "distance_mi": 0.28
      },
      {
        "name": "Jack W. Lyle Park",
        "manager_type": "local government",
        "manager": "CITY",
        "gap_status": "GAP 4 (no known mandate for protection)",
        "designation": "Local Park",
        "category": "Fee",
        "distance_mi": 0.38
      }
    ],
    "contamination": {
      "within_miles": 1.0,
      "counts": {
        "superfund_npl": 0,
        "superfund_other": 0,
        "brownfields": 0,
        "federal_facility": 0,
        "base_closure": 0,
        "lust": 26,
        "lust_open": 0,
        "rcra_corrective_action": 0
      },
      "sites": [
        {
          "program": "Leaking underground storage tank (state list)",
          "status": "No Further Action",
          "distance_mi": 0.17
        },
        {
          "program": "Leaking underground storage tank (state list)",
          "status": "No Further Action",
          "distance_mi": 0.28
        },
        {
          "program": "Leaking underground storage tank (state list)",
          "status": "No Further Action",
          "distance_mi": 0.29
        },
        {
          "program": "Leaking underground storage tank (state list)",
          "status": "No Further Action",
          "distance_mi": 0.32
        },
        {
          "program": "Leaking underground storage tank (state list)",
          "status": "No Further Action",
          "distance_mi": 0.33
        }
      ]
    },
    "sewer": {
      "note": "No open sewer service-area layer for this place.",
      "nearest_wastewater_plant": {
        "name": "Palo Alto Regional Water Quality Control Plant",
        "distance_mi": 4.2,
        "ident": "CA0037834",
        "source": "U.S. EPA ECHO facility records",
        "licence": "U.S. Government work"
      }
    }
  },
  "not_held": [
    {
      "what": "FEMA flood zone",
      "why": "FEMA's flood map (NFHL) is not held for this state yet, so no flood zone is given here"
    },
    {
      "what": "terrain (3DEP elevation and slope)",
      "why": "the 3DEP elevation tile for this point is not held or could not be read in time"
    }
  ],
  "build": "p1-20261106",
  "version": "v1",
  "sources": [
    {
      "ref": "us_fws_nwi_wetlands",
      "name": "U.S. Fish and Wildlife Service, National Wetlands Inventory",
      "licence": "U.S. Government work",
      "as_of": "2026-10-25"
    },
    {
      "ref": "us_padus_fee",
      "name": "USGS Protected Areas Database of the United States (PAD-US) 4.1",
      "licence": "public domain",
      "as_of": "2026-10-28"
    },
    {
      "ref": "us_epa_frs_remediation_sites",
      "name": "U.S. EPA Facility Registry Service: remediation sites (SEMS, ACRES, FFDOCKET, BRAC, LUST-ARRA)",
      "licence": "U.S. Government work",
      "as_of": "2026-10-18"
    },
    {
      "ref": "us_epa_rcra_corrective_action_areas",
      "name": "U.S. EPA RCRA corrective action areas",
      "licence": "U.S. Government work",
      "as_of": "2026-11-06"
    },
    {
      "ref": "us_epa_ust_finder_releases",
      "name": "U.S. EPA UST Finder: leaking underground storage tank releases (national composite of state data, 2018-2021)",
      "licence": "U.S. Government work",
      "as_of": "2018-2021 (tribal data to 2025-10)"
    }
  ],
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `data_center_projects`

US data center projects backed by official records only: building or grading permits, zoning cases, site plans and special use permits, utility large-load filings and dockets, state incentive or tax abatement approvals, environmental, air and generator permits, EIS notices, and interconnection or large-load study lists that name the site. News articles, press releases and company blogs never count and never set a status.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `project_id` | string | no | A `FACILITY-` project ID. |
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | Or an L3R `PROP-` key: the projects near it. |
| `query` | string, at most 200 characters | no | Or one street address or parcel identifier: the projects near it. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `project_id`, or `property_key` or `query` for the projects within 15 miles (up to 3).

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Projects returned. With a property and none within 15 miles, `projects` is empty and the card says so. |
| `NOT_HELD` | The project data is not available right now. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `project`: `project_id`, `name`, `state`, `county`, `location_precision` (a point, or the county), `status`, `status_date`, `history[]` (each step with its date and the record that shows it), `evidence[]` and `n_evidence`. MW and square feet appear only where an official record states them. The developer or applicant company appears as the record prints it (a business, never a person), with its parent only where an SEC or state filing shows it.
- Each `evidence` item has `record_type`, `stage`, `date`, `agency`, `url` and `record_id`.
- `status` is the latest official record: proposed, zoning approved, building permit issued, permitted, under construction, energised, denied or withdrawn, or approval voided by court.
- With a property: `projects[]` with `distance_mi`, and `radius_mi`.
- `basis`, `not_held[]` and `attribution`.

### Limits

A project not listed here may still exist. Only official records count, so a project known only from news is not shown. Each evidence item links to its record. No owners, values or person names. Interconnection and large-load study lists count as evidence of a proposal only.

### Examples

**A project, by ID**

A rezoning in Prince William County, Virginia. The status comes from the latest official record, here a court ruling.

Call:

```json
{"name": "data_center_projects", "arguments": {"project_id": "FACILITY-45b796647b37"}}
```

Card:

```markdown
### Data center projects
**Prince William Digital Gateway** (FACILITY-45b796647b37) — Prince William County, VA
- Status: approval voided by court (2026-07-29, from the record below)
- Official records (3):
  - 2022-11-01: zoning or land-use case (rezoning, site plan, special use permit) REZ2022-00032/33/36, Prince William County, VA — https://www.pwcva.gov/department/planning-office/pw-digital-gateway
  - 2023-12: zoning or land-use case (rezoning, site plan, special use permit) REZ2022-00032/33/36, Prince William County, VA — https://www.pwcva.gov/department/planning-office/pw-digital-gateway
  - 2026-07-29: zoning or land-use case (rezoning, site plan, special use permit) REZ2022-00032/33/36, Prince William County, VA — https://www.pwcva.gov/department/planning-office/pw-digital-gateway

_Shown only from official records (permits, zoning and land-use cases, utility dockets, incentive approvals, environmental and air permits, EIS notices, interconnection or large-load lists), each dated and linked. News, press releases and company announcements never count. A project not listed here may still exist._

From Athena by L3R. Sources: Official public records, linked.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "query_kind": "PROJECT_ID",
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "Official public records (permits, zoning cases, utility dockets, incentive approvals, environmental permits, interconnection lists), each linked (official public records)"
  ],
  "basis": "Shown only from official records (permits, zoning and land-use cases, utility dockets, incentive approvals, environmental and air permits, EIS notices, interconnection or large-load lists), each dated and linked. News, press releases and company announcements never count. A project not listed here may still exist.",
  "status": "READ",
  "project": {
    "project_id": "FACILITY-45b796647b37",
    "name": "Prince William Digital Gateway",
    "state": "VA",
    "county": "Prince William",
    "location_precision": "county",
    "status": "approval voided by court",
    "status_date": "2026-07-29",
    "status_record": 2,
    "history": [
      {
        "status": "proposed",
        "date": "2022-11-01",
        "record": 0
      },
      {
        "status": "zoning approved",
        "date": "2023-12",
        "record": 1
      },
      {
        "status": "approval voided by court",
        "date": "2026-07-29",
        "record": 2
      }
    ],
    "evidence": [
      {
        "record_type": "zoning or land-use case (rezoning, site plan, special use permit)",
        "stage": "proposed",
        "date": "2022-11-01",
        "agency": "Prince William County, VA",
        "url": "https://www.pwcva.gov/department/planning-office/pw-digital-gateway",
        "record_id": "REZ2022-00032/33/36"
      },
      {
        "record_type": "zoning or land-use case (rezoning, site plan, special use permit)",
        "stage": "zoning approved",
        "date": "2023-12",
        "agency": "Prince William County, VA",
        "url": "https://www.pwcva.gov/department/planning-office/pw-digital-gateway",
        "record_id": "REZ2022-00032/33/36"
      },
      {
        "record_type": "zoning or land-use case (rezoning, site plan, special use permit)",
        "stage": "approval voided by court",
        "date": "2026-07-29",
        "agency": "Prince William County, VA",
        "url": "https://www.pwcva.gov/department/planning-office/pw-digital-gateway",
        "record_id": "REZ2022-00032/33/36"
      }
    ],
    "n_evidence": 3
  },
  "build": "p1-20261106",
  "version": "v2",
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

**An address with no project nearby**

The card says none is held within 15 miles. That does not mean none exists.

Call:

```json
{"name": "data_center_projects", "arguments": {"query": "21711 Filigree Ct, Ashburn, VA 20147"}}
```

Card:

```markdown
### Data center projects: 21711 Filigree Ct, Ashburn, VA 20147
No data center project with an official record is held within 15 mi.

_Shown only from official records (permits, zoning and land-use cases, utility dockets, incentive approvals, environmental and air permits, EIS notices, interconnection or large-load lists), each dated and linked. News, press releases and company announcements never count. A project not listed here may still exist._

From Athena by L3R (PROP-0141F3838A29AA9C3D4). Sources: Official public records, linked.

More: 3drights.com
```

## `energy_plant_history`

Monthly and annual net generation (MWh) and fuel consumed (MMBtu) for one US power plant, from EIA-923. It also gives the plant's fuel mix, operating MW, balancing authority and operating company.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `limit` | integer, 1 to 3 | no | With a property: the nearest 1 to 3 operating plants. Default 1. |
| `plant_id` | string | no | One EIA plant ID, for example `EIA 3470`, as `lookup_facility` and `nearby_for_property` show it. |
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `plant_id`, or `property_key` or `query` for the nearest operating plants.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Plants returned. |
| `NOT_HELD` | No data held. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `plants[]`: the plant's `plant_id`, `name`, `state`, `fuel`, `mw`, `balancing_authority` and `operator`, with `monthly[]` and `annual[]` generation, `fuel_mix` and `fuel_mix_basis`.
- `as_of[]`: each EIA dataset with its newest period.
- `attribution`.

### Limits

The last 24 months are held monthly where EIA surveys the plant monthly, and the last 6 years annually. A month not held is left out, never estimated. Public-domain EIA data, read from a daily index. The service does not call EIA per request.

### Examples

**A coal plant, by EIA ID**

W A Parish in Texas.

Call:

```json
{"name": "energy_plant_history", "arguments": {"plant_id": "EIA 3470"}}
```

Card:

```markdown
### Power plant generation
**W A Parish** (EIA 3470, TX)
- subbituminous coal; 4,008 MW; balancing authority ERCO; operated by NRG Texas Power LLC
- Net generation, 2025-09 to 2026-08: 13,652 GWh (prior 12 months 15,069 GWh)
- Newest month 2026-08: 1,307 GWh
- By year: 2025 15,579 GWh, 2024 12,166 GWh, 2023 10,743 GWh, 2022 13,122 GWh, 2021 14,817 GWh
- Fuel mix (2025-09 to 2026-08): Subbituminous Coal 82%, Natural Gas 18%

From Athena by L3R. Sources: U.S. Energy Information Administration (EIA): EIA-860M to 2026-08; EIA-923 monthly to 2026-08; EIA-923 annual to 2025.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Energy Information Administration (EIA), EIA-860M generator inventory, data to 2026-08 (public domain)",
    "U.S. Energy Information Administration (EIA), EIA-923 power plant operations (monthly), data to 2026-08 (public domain)",
    "U.S. Energy Information Administration (EIA), EIA-923 power plant operations (annual), data to 2025 (public domain)"
  ],
  "query_kind": "PLANT_ID",
  "status": "READ",
  "plants": [
    {
      "plant_id": "EIA 3470",
      "name": "W A Parish",
      "state": "TX",
      "balancing_authority": "ERCO",
      "operator": "NRG Texas Power LLC",
      "mw": 4008.4,
      "fuel": "Subbituminous Coal",
      "monthly": [
        {
          "period": "2026-08",
          "net_mwh": 1307188,
          "fuel_mmbtu": 14984865
        },
        {
          "period": "2026-07",
          "net_mwh": 1437669,
          "fuel_mmbtu": 16198900
        },
        {
          "period": "2026-06",
          "net_mwh": 1263580,
          "fuel_mmbtu": 14381139
        },
        {
          "period": "2026-05",
          "net_mwh": 768026,
          "fuel_mmbtu": 8842428
        },
        {
          "period": "2026-04",
          "net_mwh": 865262,
          "fuel_mmbtu": 9576968
        },
        {
          "period": "2026-03",
          "net_mwh": 785657,
          "fuel_mmbtu": 8863998
        },
        {
          "period": "2026-02",
          "net_mwh": 636410,
          "fuel_mmbtu": 7143632
        },
        {
          "period": "2026-01",
          "net_mwh": 1206495,
          "fuel_mmbtu": 13517572
        },
        {
          "period": "2025-12",
          "net_mwh": 1082392,
          "fuel_mmbtu": 12411772
        },
        {
          "period": "2025-11",
          "net_mwh": 1317843,
          "fuel_mmbtu": 14917938
        },
        {
          "period": "2025-10",
          "net_mwh": 1414804,
          "fuel_mmbtu": 15954341
        },
        {
          "period": "2025-09",
          "net_mwh": 1567057,
          "fuel_mmbtu": 17572321
        },
        {
          "period": "2025-08",
          "net_mwh": 1705697,
          "fuel_mmbtu": 19285562
        },
        {
          "period": "2025-07",
          "net_mwh": 1552663,
          "fuel_mmbtu": 17941491
        },
        {
          "period": "2025-06",
          "net_mwh": 1392040,
          "fuel_mmbtu": 15790163
        },
        {
          "period": "2025-05",
          "net_mwh": 1298658,
          "fuel_mmbtu": 14616297
        },
        {
          "period": "2025-04",
          "net_mwh": 921624,
          "fuel_mmbtu": 10391959
        },
        {
          "period": "2025-03",
          "net_mwh": 1096546,
          "fuel_mmbtu": 12168688
        },
        {
          "period": "2025-02",
          "net_mwh": 878771,
          "fuel_mmbtu": 10082563
        },
        {
          "period": "2025-01",
          "net_mwh": 1350590,
          "fuel_mmbtu": 15033983
        },
        {
          "period": "2024-12",
          "net_mwh": 1158192,
          "fuel_mmbtu": 13125122
        },
        {
          "period": "2024-11",
          "net_mwh": 1032907,
          "fuel_mmbtu": 11867495
        },
        {
          "period": "2024-10",
          "net_mwh": 1399201,
          "fuel_mmbtu": 16013555
        },
        {
          "period": "2024-09",
          "net_mwh": 1282333,
          "fuel_mmbtu": 15030091
        }
      ],
      "annual": [
        {
          "period": "2025",
          "net_mwh": 15578685,
          "fuel_mmbtu": 176167078
        },
        {
          "period": "2024",
          "net_mwh": 12165789,
          "fuel_mmbtu": 140788773
        },
        {
          "period": "2023",
          "net_mwh": 10743262,
          "fuel_mmbtu": 125498704
        },
        {
          "period": "2022",
          "net_mwh": 13122023,
          "fuel_mmbtu": 147336723
        },
        {
          "period": "2021",
          "net_mwh": 14816763,
          "fuel_mmbtu": 162698296
        },
        {
          "period": "2020",
          "net_mwh": 10810190,
          "fuel_mmbtu": 121651510
        }
      ],
      "fuel_mix": [
        {
          "fuel": "Subbituminous Coal",
          "net_mwh": 11212345,
          "share": 0.821
        },
        {
          "fuel": "Natural Gas",
          "net_mwh": 2440038,
          "share": 0.179
        }
      ],
      "fuel_mix_basis": "2025-09 to 2026-08"
    }
  ],
  "as_of": [
    {
      "category": "EIA-860M",
      "period": "2026-08"
    },
    {
      "category": "EIA-923 monthly",
      "period": "2026-08"
    },
    {
      "category": "EIA-923 annual",
      "period": "2025"
    }
  ],
  "build": "p1-20261106",
  "version": "2026-11-10",
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `electricity_state_profile`

Electricity in one US state, or the US: average retail price by sector with the year-earlier price, sales and customers for the newest month EIA has published, 24 months and 6 years of the all-sector price and sales, and CO2 from electricity generation by fuel.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`: its state. |
| `query` | string, at most 200 characters | no | Or one street address or parcel identifier: its state. |
| `state` | string | no | One state: two letters (`TX`), its name, or `US`. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `state`, or `property_key` or `query`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Profile returned. |
| `NOT_HELD` | No data held. |

### Response fields

- `retail`: `latest_month`, `sectors[]` (`price_cents_kwh`, `price_year_ago`, `sales_gwh` and `customers`), `monthly[]`, `annual[]` and `nation` for the US average.
- `emissions`: `latest_year`, `co2_kt`, `co2_lb_mwh`, `by_fuel[]` and `annual[]`.
- `as_of[]` and `attribution`.

### Limits

Public-domain EIA data, read from a daily index. The service does not call EIA per request. Sector codes are all, residential, commercial, industrial and transportation.

### Examples

**A state**

Texas.

Call:

```json
{"name": "electricity_state_profile", "arguments": {"state": "TX"}}
```

Card:

```markdown
### Electricity in TX
**Average retail price, 2026-08** (cents/kWh; a year earlier in brackets):
- all sectors 11.23 (10.42); residential 15.91 (15.40); commercial 8.96 (8.76); industrial 7.21 (6.42); transportation 6.56 (3.76)
- Sales 54,796 GWh to 14,919,749 customers
- U.S. average, all sectors: 14.87
- By year, all sectors: 2025 9.97, 2024 9.79, 2023 10.04, 2022 10.16, 2021 9.14
**CO2 from electricity, 2025:** 213.8 million metric tons (783 lb/MWh)
- By fuel: natural gas 138.5, coal 74.9, petroleum 0.3 million t

From Athena by L3R. Sources: U.S. Energy Information Administration (EIA): EIA-861M to 2026-08; EIA-861 to 2025; State Electricity Profiles to 2025.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Energy Information Administration (EIA), EIA electricity retail sales (EIA-861M), data to 2026-08 (public domain)",
    "U.S. Energy Information Administration (EIA), EIA electricity retail sales (EIA-861), data to 2025 (public domain)",
    "U.S. Energy Information Administration (EIA), EIA State Electricity Profiles, emissions by state and fuel, data to 2025 (public domain)"
  ],
  "query_kind": "STATE",
  "state": "TX",
  "retail": {
    "latest_month": "2026-08",
    "sectors": [
      {
        "sector": "all sectors",
        "price_cents_kwh": 11.23,
        "price_year_ago": 10.42,
        "sales_gwh": 54795.8,
        "customers": 14919749
      },
      {
        "sector": "residential",
        "price_cents_kwh": 15.91,
        "price_year_ago": 15.4,
        "sales_gwh": 21667.8,
        "customers": 12977001
      },
      {
        "sector": "commercial",
        "price_cents_kwh": 8.96,
        "price_year_ago": 8.76,
        "sales_gwh": 18258.3,
        "customers": 1529193
      },
      {
        "sector": "industrial",
        "price_cents_kwh": 7.21,
        "price_year_ago": 6.42,
        "sales_gwh": 14869.6,
        "customers": 413553
      },
      {
        "sector": "transportation",
        "price_cents_kwh": 6.56,
        "price_year_ago": 3.76,
        "sales_gwh": 0.0,
        "customers": 2
      },
      {
        "sector": "other",
        "price_cents_kwh": 0.0,
        "price_year_ago": 0.0,
        "sales_gwh": 0.0,
        "customers": 0
      }
    ],
    "monthly": [
      {
        "period": "2026-08",
        "price_cents_kwh": 11.23,
        "sales_gwh": 54795.8
      },
      {
        "period": "2026-07",
        "price_cents_kwh": 10.91,
        "sales_gwh": 53555.7
      },
      {
        "period": "2026-06",
        "price_cents_kwh": 10.55,
        "sales_gwh": 47880.8
      },
      {
        "period": "2026-05",
        "price_cents_kwh": 10.05,
        "sales_gwh": 43180.1
      },
      {
        "period": "2026-04",
        "price_cents_kwh": 9.99,
        "sales_gwh": 40084.1
      },
      {
        "period": "2026-03",
        "price_cents_kwh": 9.9,
        "sales_gwh": 38862.5
      },
      {
        "period": "2026-02",
        "price_cents_kwh": 10.35,
        "sales_gwh": 37731.6
      },
      {
        "period": "2026-01",
        "price_cents_kwh": 10.46,
        "sales_gwh": 42658.7
      },
      {
        "period": "2025-12",
        "price_cents_kwh": 9.94,
        "sales_gwh": 40782.3
      },
      {
        "period": "2025-11",
        "price_cents_kwh": 9.47,
        "sales_gwh": 39842.3
      },
      {
        "period": "2025-10",
        "price_cents_kwh": 10.09,
        "sales_gwh": 45744.8
      },
      {
        "period": "2025-09",
        "price_cents_kwh": 10.38,
        "sales_gwh": 49032.2
      },
      {
        "period": "2025-08",
        "price_cents_kwh": 10.42,
        "sales_gwh": 53361.9
      },
      {
        "period": "2025-07",
        "price_cents_kwh": 10.36,
        "sales_gwh": 52605.7
      },
      {
        "period": "2025-06",
        "price_cents_kwh": 9.95,
        "sales_gwh": 47955.6
      },
      {
        "period": "2025-05",
        "price_cents_kwh": 9.87,
        "sales_gwh": 42648.1
      },
      {
        "period": "2025-04",
        "price_cents_kwh": 9.58,
        "sales_gwh": 38954.2
      },
      {
        "period": "2025-03",
        "price_cents_kwh": 9.62,
        "sales_gwh": 38583.0
      },
      {
        "period": "2025-02",
        "price_cents_kwh": 9.68,
        "sales_gwh": 40116.1
      },
      {
        "period": "2025-01",
        "price_cents_kwh": 9.88,
        "sales_gwh": 43634.4
      },
      {
        "period": "2024-12",
        "price_cents_kwh": 9.62,
        "sales_gwh": 38123.0
      },
      {
        "period": "2024-11",
        "price_cents_kwh": 9.5,
        "sales_gwh": 38226.6
      },
      {
        "period": "2024-10",
        "price_cents_kwh": 9.72,
        "sales_gwh": 44332.7
      },
      {
        "period": "2024-09",
        "price_cents_kwh": 10.1,
        "sales_gwh": 46250.9
      }
    ],
    "nation": {
      "period": "2026-08",
      "price_cents_kwh": 14.87
    },
    "annual": [
      {
        "period": "2025",
        "price_cents_kwh": 9.97,
        "sales_gwh": 533260.5,
        "customers": 14723690
      },
      {
        "period": "2024",
        "price_cents_kwh": 9.79,
        "sales_gwh": 505431.3,
        "customers": 14481051
      },
      {
        "period": "2023",
        "price_cents_kwh": 10.04,
        "sales_gwh": 492820.4,
        "customers": 14191104
      },
      {
        "period": "2022",
        "price_cents_kwh": 10.16,
        "sales_gwh": 475401.2,
        "customers": 13960246
      },
      {
        "period": "2021",
        "price_cents_kwh": 9.14,
        "sales_gwh": 435627.9,
        "customers": 13660929
      },
      {
        "period": "2020",
        "price_cents_kwh": 8.36,
        "sales_gwh": 426863.3,
        "customers": 13319015
      }
    ]
  },
  "emissions": {
    "latest_year": "2025",
    "co2_kt": 213766,
    "co2_lb_mwh": 783,
    "by_fuel": [
      {
        "fuel": "Natural Gas",
        "co2_kt": 138542
      },
      {
        "fuel": "Coal",
        "co2_kt": 74923
      },
      {
        "fuel": "Petroleum",
        "co2_kt": 301
      }
    ],
    "annual": [
      {
        "period": "2025",
        "co2_kt": 213766
      },
      {
        "period": "2024",
        "co2_kt": 211902
      },
      {
        "period": "2023",
        "co2_kt": 212769
      },
      {
        "period": "2022",
        "co2_kt": 213621
      },
      {
        "period": "2021",
        "co2_kt": 206175
      },
      {
        "period": "2020",
        "co2_kt": 202444
      }
    ]
  },
  "status": "READ",
  "as_of": [
    {
      "category": "EIA-861M",
      "period": "2026-08"
    },
    {
      "category": "EIA-861",
      "period": "2025"
    },
    {
      "category": "State Electricity Profiles",
      "period": "2025"
    }
  ],
  "build": "p1-20261106",
  "version": "2026-11-10",
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `grid_demand_mix`

Hourly demand, day-ahead demand forecast, net generation and interchange for one balancing authority or region. The data is the EIA-930 Hourly Electric Grid Monitor. The answer has the last 48 hours in local time, a daily summary for the last 7 days (total and peak demand), and generation by fuel over the newest 24 hours.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `ba` | string | no | One balancing authority or region code as EIA-930 prints it: `ERCO`, `PJM`, `MISO`, `CISO`, `SWPP`, `NYIS`, `ISNE`, a utility such as `FPL`, `TVA` or `DUK`, or a region such as `TEX`, `CAL` or `US48`. |
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `ba`, or `property_key` or `query`. With a property, the balancing authority is taken from the nearest EIA-860 plant that names one. This is an approximation, and the card says so.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Demand and mix returned. |
| `NOT_HELD` | No data held. |

### Response fields

- `balancing_authority`: `code` and `name`.
- `latest`: the newest hour's `demand_mwh`, `forecast_mwh`, `net_generation_mwh` and `interchange_mwh`.
- `hourly[]`, `daily[]` and `fuel_mix` (`window`, `hours` and `fuels[]`).
- `as_of[]` and `attribution`.

### Limits

The data is as of the index's daily refresh, not live. EIA-930 is public-domain data from the U.S. Energy Information Administration. Fuel shares are of net generation for the window.

### Examples

**A balancing authority**

ERCOT. The full JSON is long (48 hourly rows), so only the card is shown.

Call:

```json
{"name": "grid_demand_mix", "arguments": {"ba": "ERCO"}}
```

Card:

```markdown
### Grid demand and fuel mix: Electric Reliability Council of Texas, Inc. (ERCO)
**Newest hour 2026-11-08 23:00 (UTC-6):** demand 47,818 MWh, forecast 48,225 MWh, net generation 46,933 MWh, interchange -881 MWh
- Last 48 hours: peak 53,531 MWh at 2026-11-09 19:00 (UTC-6), low 42,681 MWh at 2026-11-09 04:00 (UTC-6)
- Daily demand: 2026-11-09 1,171 GWh (peak 53,531 MWh 19:00); 2026-11-08 1,152 GWh (peak 51,677 MWh 19:00); 2026-11-07 1,181 GWh (peak 53,525 MWh 19:00); 2026-11-06 1,232 GWh (peak 57,133 MWh 16:00)
- Generation by fuel, 24 hours to 2026-11-08 23:00 (UTC-6): natural gas 58%, coal 18%, wind 10%, nuclear 8%, solar 7%, hydro 0%

From Athena by L3R. Sources: U.S. Energy Information Administration (EIA): EIA-930 demand to 2026-11-11 05:00 UTC; EIA-930 by fuel to 2026-11-09 07:00 UTC.

More: 3drights.com
```

## `grid_interchange`

Hourly net interchange between one balancing authority and each neighbour, from the EIA-930 Hourly Electric Grid Monitor: the newest hour and the last 24 hours per neighbour, and 48 hours of the total, or of one neighbour with `neighbor`. A positive figure is net flow out to the neighbour. A negative figure is flow into the balancing authority.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `ba` | string | no | One balancing authority code, for example `ERCO`. |
| `neighbor` | string | no | Only this neighbouring balancing authority, for example `SWPP`. |
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | An L3R `PROP-` key from `lookup_property`. |
| `query` | string, at most 200 characters | no | Or one street address or one parcel identifier. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `ba`, or `property_key` or `query`, and optionally `neighbor`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Interchange returned. |
| `NOT_HELD` | No data held. |

### Response fields

- `balancing_authority`: `code` and `name`.
- `neighbors[]`: each neighbour with `latest_mwh` and `last_24h_mwh`.
- `latest` and `hourly[]` for the total, or for the one neighbour asked for.
- `sign` says which way is positive.
- `as_of[]` and `attribution`.

### Limits

The data is as of the index's daily refresh, not live. EIA-930 is public-domain data from the U.S. Energy Information Administration.

### Examples

**A balancing authority**

ERCOT and its neighbours.

Call:

```json
{"name": "grid_interchange", "arguments": {"ba": "ERCO"}}
```

Card:

```markdown
### Grid interchange: Electric Reliability Council of Texas, Inc. (ERCO)
**Newest hour 2026-11-08 00:00 (UTC-6):** net interchange -833 MWh (positive: out to neighbours)
- Last 24 hours by neighbour: SWPP -7,709 MWh; CEN 56 MWh

From Athena by L3R. Sources: U.S. Energy Information Administration (EIA): EIA-930 interchange to 2026-11-09 04:00 UTC.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Energy Information Administration (EIA), EIA-930 Hourly Electric Grid Monitor, data to 2026-11-09T04 UTC (public domain)"
  ],
  "query_kind": "BA",
  "balancing_authority": {
    "code": "ERCO",
    "name": "Electric Reliability Council of Texas, Inc."
  },
  "neighbors": [
    {
      "neighbor": "SWPP",
      "name": "Southwest Power Pool",
      "latest_mwh": -814,
      "last_24h_mwh": -7709
    },
    {
      "neighbor": "CEN",
      "name": "Centro Nacional de Control de Energia",
      "latest_mwh": -19,
      "last_24h_mwh": 56
    }
  ],
  "latest": {
    "period": "2026-11-08T00-06",
    "interchange_mwh": -833
  },
  "hourly": [
    {
      "period": "2026-11-08T00-06",
      "interchange_mwh": -833
    },
    {
      "period": "2026-11-07T23-06",
      "interchange_mwh": -809
    },
    {
      "period": "2026-11-07T22-06",
      "interchange_mwh": -805
    },
    {
      "period": "2026-11-07T21-06",
      "interchange_mwh": -816
    },
    {
      "period": "2026-11-07T20-06",
      "interchange_mwh": -780
    },
    {
      "period": "2026-11-07T19-06",
      "interchange_mwh": -760
    },
    {
      "period": "2026-11-07T18-06",
      "interchange_mwh": -677
    },
    {
      "period": "2026-11-07T17-06",
      "interchange_mwh": -363
    },
    {
      "period": "2026-11-07T16-06",
      "interchange_mwh": -117
    },
    {
      "period": "2026-11-07T15-06",
      "interchange_mwh": 8
    },
    {
      "period": "2026-11-07T14-06",
      "interchange_mwh": 8
    },
    {
      "period": "2026-11-07T13-06",
      "interchange_mwh": 7
    },
    {
      "period": "2026-11-07T12-06",
      "interchange_mwh": 5
    },
    {
      "period": "2026-11-07T11-06",
      "interchange_mwh": 5
    },
    {
      "period": "2026-11-07T10-06",
      "interchange_mwh": 5
    },
    {
      "period": "2026-11-07T09-06",
      "interchange_mwh": -45
    },
    {
      "period": "2026-11-07T08-06",
      "interchange_mwh": -149
    },
    {
      "period": "2026-11-07T07-06",
      "interchange_mwh": -201
    },
    {
      "period": "2026-11-07T06-06",
      "interchange_mwh": -241
    },
    {
      "period": "2026-11-07T05-06",
      "interchange_mwh": -218
    },
    {
      "period": "2026-11-07T04-06",
      "interchange_mwh": -218
    },
    {
      "period": "2026-11-07T03-06",
      "interchange_mwh": -218
    },
    {
      "period": "2026-11-07T02-06",
      "interchange_mwh": -217
    },
    {
      "period": "2026-11-07T01-06",
      "interchange_mwh": -224
    },
    {
      "period": "2026-11-07T00-06",
      "interchange_mwh": -473
    },
    {
      "period": "2026-11-06T23-06",
      "interchange_mwh": -529
    },
    {
      "period": "2026-11-06T22-06",
      "interchange_mwh": -237
    },
    {
      "period": "2026-11-06T21-06",
      "interchange_mwh": -159
    },
    {
      "period": "2026-11-06T20-06",
      "interchange_mwh": -135
    },
    {
      "period": "2026-11-06T19-06",
      "interchange_mwh": -67
    },
    {
      "period": "2026-11-06T18-06",
      "interchange_mwh": -76
    },
    {
      "period": "2026-11-06T17-06",
      "interchange_mwh": 181
    },
    {
      "period": "2026-11-06T16-06",
      "interchange_mwh": 335
    },
    {
      "period": "2026-11-06T15-06",
      "interchange_mwh": 605
    },
    {
      "period": "2026-11-06T14-06",
      "interchange_mwh": 609
    },
    {
      "period": "2026-11-06T13-06",
      "interchange_mwh": 587
    },
    {
      "period": "2026-11-06T12-06",
      "interchange_mwh": 0
    },
    {
      "period": "2026-11-06T11-06",
      "interchange_mwh": -1
    },
    {
      "period": "2026-11-06T10-06",
      "interchange_mwh": -17
    },
    {
      "period": "2026-11-06T09-06",
      "interchange_mwh": -68
    },
    {
      "period": "2026-11-06T08-06",
      "interchange_mwh": -94
    },
    {
      "period": "2026-11-06T07-06",
      "interchange_mwh": -95
    },
    {
      "period": "2026-11-06T06-06",
      "interchange_mwh": -76
    },
    {
      "period": "2026-11-06T05-06",
      "interchange_mwh": -75
    },
    {
      "period": "2026-11-06T04-06",
      "interchange_mwh": -76
    },
    {
      "period": "2026-11-06T03-06",
      "interchange_mwh": -82
    },
    {
      "period": "2026-11-06T02-06",
      "interchange_mwh": -314
    },
    {
      "period": "2026-11-06T01-06",
      "interchange_mwh": -464
    }
  ],
  "sign": "positive: net flow out of the balancing authority to the neighbour; negative: into it (EIA-930)",
  "status": "READ",
  "as_of": [
    {
      "category": "EIA-930 interchange",
      "period": "2026-11-09T04"
    }
  ],
  "build": "p1-20261106",
  "version": "2026-11-10",
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `coal_shipments`

Coal received at one US power plant by mine, or shipped from one mine to plants, from EIA's coal receipts. The answer gives tons, coal rank, transport mode (rail, barge or truck), contract or spot, supplier company, heat content and sulfur.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `mine_id` | string | no | Or one MSHA mine ID, for example `MSHA 4800732`. |
| `plant_id` | string | no | One EIA plant ID, for example `EIA 3470`. |

Give exactly one of `plant_id` or `mine_id`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Shipments returned. |
| `NOT_HELD` | No data held. |

### Response fields

- `plant` or `mine`: the plant's `plant_id`, `name` and `state`, or the mine's MSHA ID, state, county and basin.
- `years[]`: for each of the last 3 years, `period`, `tons`, `n_shipments` and the largest `shipments`.
- `as_of[]` and `attribution`.

### Limits

Mines are shown by MSHA ID, state, county and basin. A mine's name is shown only where it is a company's. Supplier names are companies. Public-domain EIA data, read from a daily index. The service does not call EIA per request.

### Examples

**Coal received at a plant**

W A Parish in Texas.

Call:

```json
{"name": "coal_shipments", "arguments": {"plant_id": "EIA 3470"}}
```

Card:

```markdown
### Coal shipments
**W A Parish** (EIA 3470, TX)
- Tons by year: 2025 7,749,861, 2024 7,699,688, 2023 6,620,137
- Largest flows, 2025:
  - MSHA 4800993 (WY, Powder River Basin): 3,629,646 tons, Subbituminous, rail, supplier COALSALES LLC
  - MSHA 4801200 (WY, Powder River Basin): 2,056,327 tons, Subbituminous, rail, supplier BUCKSKIN
  - MSHA 4801078 (WY, Powder River Basin): 1,449,254 tons, Subbituminous, rail, supplier BLUEGRASS COMMODITIES LP
  - MSHA 4800992 (WY, Powder River Basin): 507,188 tons, Subbituminous, rail, supplier NAVAJO TRANSITIONAL ENERGY CO., LLC
  - MSHA 4800732 (WY, Powder River Basin): 75,581 tons, Subbituminous, rail, supplier BLUEGRASS COMMODITIES LP

From Athena by L3R. Sources: U.S. Energy Information Administration (EIA): EIA-923 coal receipts to 2025.

More: 3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Energy Information Administration (EIA), EIA-923 coal receipts by mine (coal shipments), data to 2025 (public domain)"
  ],
  "query_kind": "PLANT_ID",
  "plant": {
    "plant_id": "EIA 3470",
    "name": "W A Parish",
    "state": "TX"
  },
  "status": "READ",
  "years": [
    {
      "period": "2025",
      "tons": 7749861,
      "n_shipments": 6,
      "shipments": [
        {
          "tons": 3629646,
          "rank": "Subbituminous",
          "transport": "Rail",
          "contract": "Contract Purchase",
          "supplier": "COALSALES LLC",
          "heat_btu_lb": 8325,
          "sulfur_pct": 0.34,
          "mine": {
            "msha_id": "MSHA 4800993",
            "state": "WY",
            "county": "Campbell",
            "basin": "Powder River Basin"
          }
        },
        {
          "tons": 2056327,
          "rank": "Subbituminous",
          "transport": "Rail",
          "contract": "Contract Purchase",
          "supplier": "BUCKSKIN",
          "heat_btu_lb": 8248,
          "sulfur_pct": 0.32,
          "mine": {
            "msha_id": "MSHA 4801200",
            "state": "WY",
            "county": "Campbell",
            "basin": "Powder River Basin"
          }
        },
        {
          "tons": 1449254,
          "rank": "Subbituminous",
          "transport": "Rail",
          "contract": "Contract Purchase",
          "supplier": "BLUEGRASS COMMODITIES LP",
          "heat_btu_lb": 8372,
          "sulfur_pct": 0.35,
          "mine": {
            "msha_id": "MSHA 4801078",
            "state": "WY",
            "county": "Campbell",
            "basin": "Powder River Basin"
          }
        },
        {
          "tons": 507188,
          "rank": "Subbituminous",
          "transport": "Rail",
          "contract": "Contract Purchase",
          "supplier": "NAVAJO TRANSITIONAL ENERGY CO., LLC",
          "heat_btu_lb": 8536,
          "sulfur_pct": 0.43,
          "mine": {
            "msha_id": "MSHA 4800992",
            "state": "WY",
            "county": "Campbell",
            "basin": "Powder River Basin"
          }
        },
        {
          "tons": 75581,
          "rank": "Subbituminous",
          "transport": "Rail",
          "contract": "Contract Purchase",
          "supplier": "BLUEGRASS COMMODITIES LP",
          "heat_btu_lb": 8572,
          "sulfur_pct": 0.34,
          "mine": {
            "msha_id": "MSHA 4800732",
            "state": "WY",
            "county": "Campbell",
            "basin": "Powder River Basin"
          }
        },
        {
          "tons": 31865,
          "rank": "Subbituminous",
          "transport": "Rail",
          "contract": "Contract Purchase",
          "supplier": "COALSALES LLC",
          "heat_btu_lb": 9070,
          "sulfur_pct": 0.18,
          "mine": {
            "msha_id": "MSHA 4801353",
            "state": "WY",
            "county": "Campbell",
            "basin": "Powder River Basin"
          }
        }
      ]
    },
    {
      "period": "2024",
      "tons": 7699688,
      "n_shipments": 5
    },
    {
      "period": "2023",
      "tons": 6620137,
      "n_shipments": 4
    }
  ],
  "as_of": [
    {
      "category": "EIA-923 coal receipts",
      "period": "2025"
    }
  ],
  "build": "p1-20261106",
  "version": "2026-11-10",
  "terms_url": "https://mcp.l3r.io/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

## `lookup_facility`

One facility card for a US site that L3R's open data holds: a power plant (fuel, MW, status), data center (name,
operator company where a government record names it, status and MW), airport, port, community water system, wastewater
plant, public school, hospital, antenna structure or mine. There is no search or list.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `city` | string, at most 200 characters | no | City or county, with `name`. Optional. |
| `facility_id` | string, at most 200 characters | no | One facility ID: `EIA 3470`, an FAA code such as `HOU`, `FACILITY-…`, an EPA PWSID or NPDES ID, `MSHA …`, `ASR …` or an NCES ID. |
| `name` | string, at most 200 characters | no | Or the facility's name as the publisher prints it. Give `state` with it. |
| `state` | string, at most 200 characters | no | Two-letter state, with `name`. |

Give `facility_id`, or `name` with `state`.

### Statuses

| Status | Meaning |
|---|---|
| `MATCHED` | One facility found. |
| `AMBIGUOUS` | The name fits several. Up to 3 `candidates` with their places and IDs. Ask again with one `facility_id`. |
| `UNMATCHED` | Nothing found. |

### Response fields

`facility` has `name`, `category`, `facility_id`, `place`, `state`, and the fields that apply to its kind, such as `fuel`,
`mw`, `status`, `as_of`, `source` and `licence`. `candidates[]` and `n_candidates` come with `AMBIGUOUS`.

### Limits

One facility per call. Federal open data and official public records only. No owners, values or person names.

### Examples


**A power plant, by name and state**

Call:

```json
{"name": "lookup_facility", "arguments": {"name": "Hoover Dam", "state": "NV"}}
```

Card:

```markdown
### Hoover Dam (NV)
Power plant (EIA 154), Clark County, NV
- fuel: hydroelectric; 1,039 MW; operating; operated by U S Bureau of Reclamation
- Location: 36.01551, -114.73801

From Athena by L3R. Sources: U.S. Energy Information Administration, Form EIA-860 2025.

Rights, permits or ownership questions? Ask Athena, L3R's assistant → https://3drights.com
```

<details><summary>Full JSON</summary>

```json
{
  "query_kind": "NAME",
  "attribution": [
    "From Athena by L3R (l3r.io)",
    "U.S. Energy Information Administration, Form EIA-860 2025 (public domain)"
  ],
  "status": "MATCHED",
  "facility": {
    "name": "Hoover Dam (NV)",
    "category": "Power plant",
    "facility_id": "EIA 154",
    "place": "Clark County",
    "state": "NV",
    "source": "U.S. Energy Information Administration, Form EIA-860 2025",
    "licence": "public domain",
    "fuel": "hydroelectric",
    "mw": 1039.4,
    "status": "operating",
    "operator": "U S Bureau of Reclamation",
    "lat": 36.01551,
    "lon": -114.73801
  },
  "terms_url": "https://l3r.io/mcp/terms",
  "docs_url": "https://l3r.io/mcp"
}
```

</details>

**An airport, by code**

Call:

```json
{"name": "lookup_facility", "arguments": {"facility_id": "HOU"}}
```

Card:

```markdown
### William P Hobby
Airport (HOU), Harris County, TX
- commercial service
- Location: 29.6458, -95.27723

From Athena by L3R. Sources: FAA/BTS NTAD airports.

Rights, permits or ownership questions? Ask Athena, L3R's assistant → https://3drights.com
```

**A power plant, by EIA ID**

Call:

```json
{"name": "lookup_facility", "arguments": {"facility_id": "EIA 3470"}}
```

Card:

```markdown
### W A Parish
Power plant (EIA 3470), Fort Bend County, TX
- fuel: coal; 4,008 MW; operating; operated by NRG Texas Power LLC
- Location: 29.4828, -95.6311

From Athena by L3R. Sources: U.S. Energy Information Administration, Form EIA-860 2025.

Rights, permits or ownership questions? Ask Athena, L3R's assistant → https://3drights.com
```
## `coverage_for_county`

What L3R holds for one US county, in one call: parcels (the count of keyed properties with a location), base zoning (the official layers shown and how many properties have a district shown), the cities whose zoning rules are quoted, zoning overlays held, data center projects from official records, FEMA's flood map (NFHL), recorded water wells and lots screened for the site screen. Counts and layer names only: no property is listed.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with `state`. |
| `state` | string, at most 200 characters | no | Two-letter state, for example `TX`. Use it with `county`. |
| `fips` | string, at most 200 characters | no | Or the 5-digit county FIPS code, for example `48453`. |

Give `county` with `state`, or `fips`.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | Coverage returned. |
| `NOT_FOUND` | No US county matches. |

### Response fields

- `county_fips`, `county` and `state`.
- `coverage`: `parcels`, `zoning` (with `layers[]` and `properties_shown`), `rules`, `overlays`, `data_centers`, `flood`, `wells` and `site_lots`, each with `held` and a count where one applies.
- `attribution`.

### Limits

"Not held" means L3R does not hold it yet, never that it does not exist. Every county also has FEMA National Risk Index tract ratings, Census figures and nearby infrastructure.

### Examples

**A county by name**

Call:

```json
{"name": "coverage_for_county", "arguments": {"county": "Loudoun", "state": "VA"}}
```

Card:

```markdown
### Coverage: Loudoun County, Virginia
_County FIPS 51107._

- **Parcels:** 132,520 properties keyed, with a location point
- **Base zoning:** shown for 132,521 properties (County Of Loudoun zoning map; Loudoun County Unincorporated Area zoning map)
- **District rules:** none quoted for a city here yet
- **Zoning overlays:** none held
- **Data center projects (official records):** 20
- **FEMA flood map (NFHL):** not held yet
- **Recorded water wells:** not held for this state
- **Site screen lots:** screened (shares of each lot)

_Not held means L3R does not hold it yet, never that it does not exist. Every county also has FEMA National Risk Index tract ratings, Census figures and nearby infrastructure._

From Athena by L3R.

More: 3drights.com
```

Structured content:

```json
{
 "query_kind": "COUNTY",
 "attribution": [
  "From Athena by L3R (l3r.io)"
 ],
 "athena_url": null,
 "status": "READ",
 "county_fips": "51107",
 "county": "Loudoun County, Virginia",
 "state": "VA",
 "coverage": {
  "parcels": {
   "held": true,
   "count": 132520
  },
  "zoning": {
   "held": true,
   "properties_shown": 132521,
   "layers": [
    {
     "name": "County Of Loudoun zoning map"
    },
    {
     "name": "Loudoun County Unincorporated Area zoning map"
    }
   ],
   "count": 2
  },
  "rules": {
   "held": false
  },
  "overlays": {
   "held": false
  },
  "data_centers": {
   "held": true,
   "count": 20
  },
  "flood": {
   "held": false
  },
  "wells": {
   "held": false
  },
  "site_lots": {
   "held": true
  }
 },
 "terms_url": "https://mcp.l3r.io/terms",
 "docs_url": "https://l3r.io/mcp"
}
```

**A county by FIPS code**

Call:

```json
{"name": "coverage_for_county", "arguments": {"fips": "48245"}}
```

Card:

```markdown
### Coverage: Jefferson County, Texas
_County FIPS 48245._

- **Parcels:** 122,071 properties keyed, with a location point
- **Base zoning:** shown for 81,994 properties (City of Beaumont, TX own ArcGIS Server gis.beaumonttexas.gov zoning map; City of Port Arthur zoning map)
- **District rules:** none quoted for a city here yet
- **Zoning overlays:** none held
- **Data center projects (official records):** 0
- **FEMA flood map (NFHL):** not held yet
- **Recorded water wells:** not held for this state
- **Site screen lots:** screened (shares of each lot)

_Not held means L3R does not hold it yet, never that it does not exist. Every county also has FEMA National Risk Index tract ratings, Census figures and nearby infrastructure._

From Athena by L3R.

More: 3drights.com
```

## `list_reference_data`

A short ranked list from public reference data. No property, parcel or owner is ever listed. Three lists:

- `strategic_seaports`: the commercial strategic seaports in the U.S. DOT BTS National Transportation Atlas, by state or nationally.
- `nri_tracts`: Census tracts ranked by a FEMA National Risk Index rating, the overall risk or one hazard, by state or nationally. The index gives ratings, not scores, so ties are broken by the expected annual loss rating and then by how many hazards rate high.
- `power_plants`: operating plants from EIA's generator inventory by state, optionally one fuel, largest first.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `list` | string, at most 200 characters | yes | `strategic_seaports`, `nri_tracts` or `power_plants`. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for `power_plants`. |
| `hazard` | string, at most 200 characters | no | `nri_tracts`: `overall` (the default) or a hazard, for example `wildfire`, `coastal_flooding`, `inland_flooding`, `earthquake`, `hurricane`, `tornado` or `heat_wave`. |
| `fuel` | string, at most 200 characters | no | `power_plants`: `solar`, `wind`, `hydro`, `nuclear`, `gas`, `coal`, `oil`, `biomass`, `geothermal` or `storage`. |
| `limit` | integer, 1 to 50 | no | Rows to return (default 10). |

### Statuses

| Status | Meaning |
|---|---|
| `READ` | List returned, with the true count beside the capped list. |
| `NOT_HELD` | No data held for this list. |

### Response fields

- `list`, `state`, and `hazard` or `fuel` as given.
- `items[]`, each with `rank` and the list's own fields (for power plants: `plant_id`, `name`, `county`, `fuel`, `mw` and `operator`).
- `total`, `limit`, `as_of`, `source` and `attribution`.

### Limits

Lists come only from public reference layers credited to their federal publisher. Parcels, properties and owners are never listed: property data stays one address per call.

### Examples

**Strategic seaports in a state**

Call:

```json
{"name": "list_reference_data", "arguments": {"list": "strategic_seaports", "state": "CA"}}
```

Card:

```markdown
### Commercial strategic seaports: CA
_3 listed (BTS National Transportation Atlas)._

1. Long Beach, CA
2. Oakland, CA
3. San Diego, CA

From Athena by L3R. Sources: BTS National Transportation Atlas (U.S. Government work).

More: 3drights.com
```

**Power plants by fuel**

Call:

```json
{"name": "list_reference_data", "arguments": {"list": "power_plants", "state": "TX", "fuel": "nuclear"}}
```

Card:

```markdown
### Operating power plants (nuclear): TX
_2, largest first; EIA generator inventory 2026-08._

1. South Texas Project (EIA 6251): nuclear, 2,709 MW, Matagorda County, operated by STP Nuclear Operating Co
2. Comanche Peak (EIA 6145): nuclear, 2,430 MW, Somervell County, operated by Luminant Generation Company LLC

From Athena by L3R. Sources: U.S. Energy Information Administration (public domain).

More: 3drights.com
```

Structured content:

```json
{
 "status": "READ",
 "list": "power_plants",
 "state": "TX",
 "fuel": "nuclear",
 "items": [
  {
   "rank": 1,
   "plant_id": "EIA 6251",
   "name": "South Texas Project",
   "county": "Matagorda",
   "fuel": "Nuclear",
   "mw": 2708.6,
   "operator": "STP Nuclear Operating Co"
  },
  {
   "rank": 2,
   "plant_id": "EIA 6145",
   "name": "Comanche Peak",
   "county": "Somervell",
   "fuel": "Nuclear",
   "mw": 2430.0,
   "operator": "Luminant Generation Company LLC"
  }
 ],
 "total": 2,
 "limit": 10,
 "as_of": "2026-08",
 "source": "U.S. Energy Information Administration (EIA), EIA-860M generator inventory (public domain)",
 "attribution": [
  "From Athena by L3R (l3r.io)",
  "U.S. Energy Information Administration (EIA), EIA-860M generator inventory (public domain)"
 ],
 "query_kind": "LIST",
 "athena_url": null,
 "terms_url": "https://mcp.l3r.io/terms",
 "docs_url": "https://l3r.io/mcp"
}
```

## Errors and refusals

| Case | What the client sees |
|---|---|
| More than one address or identifier, a list, or a semicolon, vertical bar, tab or newline in the input | A tool result with `isError: true` and a message, for example `one address or identifier per call; lists are not accepted`. |
| An input over 200 characters | `isError: true`: `at most 200 characters: one address or identifier per call`. |
| `census_for_area` with none or several of its inputs | `isError: true`: `give exactly one of address, property_key or geoid`. |
| `zoning_for_property`, `hazards_for_property`, `nearby_for_property`, `site_screen_for_property`, `energy_service_for_property` or `districts_for_property`, with none or both of `property_key` and `query` (and no `lat` and `lon`) | `isError: true`: `give exactly one of property_key (a PROP- key from lookup_property) or query (one address or parcel identifier)`. |
| `zoning_for_property` with `district` but no `city` | `isError: true`: `with district, give city (e.g. 'Tulsa, OK')`. |
| `districts_for_property` with `lat` and `lon` and also a property | `isError: true`: `give either a property (property_key or query) or lat and lon, not both`. |
| `lookup_facility` with `name` but no `state` | `isError: true`: `with name, give state (and city if known)`. |
| `nearby_for_property` with `limit` over 3 | `isError: true`, an input validation message that `limit` must be at most 3. |
| A malformed GEOID | `isError: true`: `a GEOID is 5 (county), 7 (place) or 11 (tract) digits`. |
| A JSON-RPC batch (an array body) | HTTP 400, JSON-RPC error `-32600`, `batches are not accepted`. |
| A request body over 16 KB | HTTP 413. |
| Over a rate limit | HTTP 429 with a `Retry-After` header and JSON-RPC error `-32029`. |
| A lookup that runs past 8 seconds | `status: UNMATCHED`, `reason: TIMEOUT`. Try again in a moment. |
| An internal failure | `isError: true`: `the lookup could not be completed; try again later`. |

Refused calls, for example:

```json
{"name": "lookup_property", "arguments": {"query": "1 Main St; 2 Main St"}}
```

```text
one address or identifier per call; lists are not accepted
```

```json
{"name": "zoning_for_property", "arguments": {"district": "RS-3"}}
```

```text
with district, give city (e.g. 'Tulsa, OK')
```

```json
{"name": "lookup_facility", "arguments": {"name": "Hoover Dam"}}
```

```text
with name, give state (and city if known)
```
