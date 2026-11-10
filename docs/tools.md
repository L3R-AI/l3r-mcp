# Tools reference

The server exposes thirteen tools. All are read-only and idempotent, and each takes one input per call: one address, one
identifier, one area, one facility. Each result has two parts: a short Markdown card as the text content block, ready to
show as is, and the full answer as JSON in `structuredContent`. No tool calls a model.

| Tool | Title | Annotations |
|---|---|---|
| [`lookup_property`](#lookup_property) | Look up a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`census_for_area`](#census_for_area) | Census figures for an area | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`zoning_for_property`](#zoning_for_property) | Zoning for a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`hazards_for_property`](#hazards_for_property) | Hazards for a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`nearby_for_property`](#nearby_for_property) | Infrastructure, utilities and energy around a US property | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`lookup_facility`](#lookup_facility) | Look up a US facility (plant, data center, airport, port, water system and more) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`site_screen_for_property`](#site_screen_for_property) | Site screen for a US property (flood, wetlands, protected areas, contamination, terrain, sewer) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`data_center_projects`](#data_center_projects) | Data center projects from official records (permits, zoning, dockets, air permits) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`energy_plant_history`](#energy_plant_history) | Generation and fuel history of a US power plant (EIA-923) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`electricity_state_profile`](#electricity_state_profile) | Electricity prices, sales and emissions by state | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`grid_demand_mix`](#grid_demand_mix) | Hourly demand and fuel mix of a balancing authority (EIA-930) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`grid_interchange`](#grid_interchange) | Power flows between balancing authorities (EIA-930) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |
| [`coal_shipments`](#coal_shipments) | Coal shipments from mines to plants (EIA) | `readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false` |

Every example below is real output from the live server at `https://mcp.l3r.io/mcp`, captured on 8 November 2026. Each
passed the server's own answer gates: a key allowlist at every depth, a guard against owner, holder and contact fields,
and a size cap. Nothing was edited by hand.

**Contents**

- [`lookup_property`](#lookup_property)
- [`census_for_area`](#census_for_area)
- [`zoning_for_property`](#zoning_for_property)
- [`hazards_for_property`](#hazards_for_property)
- [`nearby_for_property`](#nearby_for_property)
- [`lookup_facility`](#lookup_facility)
- [`site_screen_for_property`](#site_screen_for_property)
- [`data_center_projects`](#data_center_projects)
- [Energy tools](#energy-tools)
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
| `query` | string, at most 200 characters | yes | One street address or one parcel identifier. See accepted forms below. |
| `state` | string, at most 200 characters | no | Two-letter state, for example `TX`. Needed for a county parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Accepted forms of `query`, exactly one per call:

- A street address, with city and state or a ZIP code.
- A county parcel number (APN or PIN) as the county prints it. Give `state` and `county`.
- A San Francisco block and lot (`3725018`, `3725/018`).
- A New York City BBL (`1008350041`, `1-00835-0041`, `Manhattan block 835 lot 41`) or BIN.
- An L3R `PROP-`, `PARCEL-` or `BLDG-` key.

### Statuses

| Status | Meaning |
|---|---|
| `MATCHED` | One property found. |
| `AMBIGUOUS` | Up to 3 candidates. Add the county or unit. |
| `LOCATION_ONLY` | The place and its Census geography, but no parcel is held. |
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

## `site_screen_for_property`

A development site screen for one property, from federal open data. Shares are of the whole parcel where L3R has
screened its outline. Otherwise each layer is read at the property's point, and the card says which.

- **Flood:** FEMA flood zones with the share of the lot in each, whether it is a Special Flood Hazard Area, and the FIRM
  panel with its effective date.
- **Wetlands:** National Wetlands Inventory wetlands, the share of the lot and the type.
- **Protected areas:** PAD-US areas on the lot or within 0.5 mile, with GAP status and manager type. Names only for
  public agencies.
- **Contamination:** EPA Superfund (NPL and other SEMS sites), ACRES brownfields, RCRA corrective action areas, federal
  facilities and Recovery Act leaking tanks within 1 mile, with distances and EPA links.
- **Terrain:** USGS 3DEP elevation (min, max, mean) and the share of the lot by slope band: 0–5, 5–15, 15–30, over 30%.
- **Sewer:** an open sewer service-area layer where one exists. Otherwise it says so and names the nearest wastewater
  plant.

### Input

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
| `READ` | The screen is returned. |
| `PARTIAL` | Some layers are not held for this place yet, for example the flood map. |
| `NOT_HELD` | The layers are not loaded right now. |
| `NO_POINT` | The property was found but no public point is held for it. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | Nothing found. |

### Response fields

- `site.basis`: `LOT` (shares of the parcel, with `lot_acres`) or `POINT`.
- `site.flood`: `zones[]` (`zone`, `subtype`, `sfha`, `share_pct`), `sfha_share_pct` and `panel` (`firm_panel`, `effective_date`).
- `site.wetlands`: `share_pct` (or `inside` at a point) and `types[]` with the NWI `code`, `wetland_type` and `share_pct`.
- `site.protected_areas[]`: `name` (public managers only), `manager_type`, `gap_status`, `designation`, `share_pct` or a distance.
- `site.contamination`: `within_miles`, `counts` by program and `sites[]` with `program`, distance and EPA `url`.
- `site.terrain`: `elevation_ft` (`min`, `max`, `mean`) and `slope_bands_pct[]` (`band`, `share_pct`).
- `site.sewer`: a `service_area`, or a `note` and the `nearest_wastewater_plant`.
- `not_held[]`, `disclaimer`, `sources[]` and `attribution`.

### Limits

Screening only: not a flood zone determination, wetland delineation, Phase I environmental site assessment or survey.
Not being in a mapped flood zone or wetland never means no flood or wetland. Flood zones are added state by state as
FEMA's flood map files are loaded. No parcel outlines, owners, values or person names.

---

## `data_center_projects`

US data center projects, shown only with evidence from official records, each dated and linked: building or grading
permits, zoning or rezoning cases, site plans and special use permits, utility large-load filings and dockets, state
incentive or tax abatement approvals, environmental, air and generator permits, EIS notices, and interconnection or
large-load study lists naming the site. News articles, press releases and company blogs never count and never set a
status.

### Input

| Field | Type | Required | Description |
|---|---|---|---|
| `project_id` | string, at most 200 characters | no | A `FACILITY-` project ID. |
| `city` | string, at most 200 characters | no | The city, for an address that does not name one. |
| `county` | string, at most 200 characters | no | County name, for example `Travis`. Use it with a parcel number. |
| `property_key` | string, at most 200 characters | no | Or an L3R `PROP-` key: the projects near it. |
| `query` | string, at most 200 characters | no | Or one street address or parcel identifier: the projects near it. |
| `state` | string, at most 200 characters | no | Two-letter state. Needed for a parcel number. |
| `zip` | string, at most 200 characters | no | Five-digit ZIP code. |

Give `project_id`, or one of `property_key` or `query` for the projects within 15 miles (up to 3), and those placed only
by the property's county.

### Statuses

| Status | Meaning |
|---|---|
| `READ` | The project, or the projects near the property, returned. |
| `NOT_HELD` | The project list is not loaded right now. |
| `AMBIGUOUS` | More than one property fits. Add detail. |
| `UNMATCHED` | No project with that ID, or the address was not found. |

### Response fields

- `project` (or `projects[]`): `project_id`, `name`, `state`, `county`, `location_precision` (a point, or `county`), and
  a distance near a property.
- `status`, `status_date` and `status_record`: the rung of the latest official record (`proposed`, `zoning approved`,
  `permitted`, `under construction`, `energised`, or `denied or withdrawn`), and `history[]` of each rung with its
  record.
- `evidence[]`: `record_type`, `date`, `agency`, `url`, `record_id` and whether L3R holds a copy.
- `mw` and `sq_ft`: only where an official record states them, with the record.
- `companies[]`: the developer or applicant as the record names it (`name_in_record`, `role`), a business and never a
  person, with its `parent` only where an SEC or state filing shows it (`parent_basis`, `parent_url`).

### Limits

Official records only, so many announced projects are not listed. A project not listed here may still exist. No
owners, values or person names.

---

## Energy tools

Five tools served from a daily index of the U.S. Energy Information Administration's public data (EIA API v2, public
domain; credit EIA). Each card names the period of the data it shows.

| Tool | Input | What it returns |
|---|---|---|
| `energy_plant_history` | `plant_id` (`EIA 3470`), or `property_key` / `query` with `limit` 1–3 nearest plants | EIA-923 net generation and fuel use: 24 months and 6 years, fuel mix, MW, balancing authority. |
| `electricity_state_profile` | `state` (`TX`, `US`), or a property | Retail price by sector, sales and customers, and CO2 from electricity by fuel. |
| `grid_demand_mix` | `ba` code (`ERCO`, `PJM`), or a property | EIA-930 demand, forecast, generation and interchange, 48 hours hourly, a 7-day summary and generation by fuel. |
| `grid_interchange` | `ba`, optional `neighbor` | Flows to each neighbouring balancing authority: the newest hour and the last 24 hours. |
| `coal_shipments` | `plant_id`, or `mine_id` (MSHA) | Three years of coal receipts, the newest year's flows by rank, transport and contract. |

For a property, the balancing authority comes from the nearest EIA-860 plant that names one; the property's own utility
is not mapped. Mines are shown by MSHA ID and place. No owners or person names.

---

## Errors and refusals

| Case | What the client sees |
|---|---|
| More than one address or identifier, a list, or a semicolon, vertical bar, tab or newline in the input | A tool result with `isError: true` and a message, for example `one address or identifier per call; lists are not accepted`. |
| An input over 200 characters | `isError: true`: `at most 200 characters: one address or identifier per call`. |
| `census_for_area` with none or several of its inputs | `isError: true`: `give exactly one of address, property_key or geoid`. |
| `zoning_for_property`, `hazards_for_property` or `nearby_for_property` with none or both of `property_key` and `query` | `isError: true`: `give exactly one of property_key (a PROP- key from lookup_property) or query (one address or parcel identifier)`. |
| `zoning_for_property` with `district` but no `city` | `isError: true`: `with district, give city (e.g. 'Tulsa, OK')`. |
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
