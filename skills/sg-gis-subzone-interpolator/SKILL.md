---
name: sg-gis-subzone-interpolator
description: Perform GIS spatial joins between URA Master Plan 2019/2025 Subzone/Planning Area GeoJSON boundaries, SLA OneMap 6-digit Postal Codes, and Singapore's 28 Postal Districts (D01-D28). Use for Singapore geospatial mapping and postal district lookup.
---
# Singapore GIS Subzone & Postal District Interpolator

Execute high-precision spatial joins across Singapore's URA Planning Regions (5), Planning Areas (55), Subzones (332), Postal Districts (D01-D28), and 6-digit Postal Codes.

## When to Use

- Mapping any 6-digit Singapore postal code (e.g., `498991`) to its 2-digit Postal Sector (`49`), Postal District (`D17`), URA Subzone (`CHANGI POINT`), Planning Area (`CHANGI`), and Region (`EAST REGION`)
- Converting between WGS84 (`EPSG:4326`) and Singapore SVY21 (`EPSG:3414`) metric coordinates for distance-to-coast and upwind buffer calculations

## Steps

1. **Load Official Boundary Datasets**:
   - URA Master Plan Subzone Boundary (No Sea): Dataset `d_8594ae9ff96d0c708bc2af633048edfb`
   - URA Master Plan 2025 Planning Area Boundary: Dataset `d_2cc750190544007400b2cfd5d7f53209`
2. **Postal Sector (01-82) to District (D01-D28) Crosswalk**:
   - Use the canonical SLA/SingPost 2-digit prefix crosswalk (`references/postal_district_crosswalk.json`) to tag every building and subzone centroid.
3. **Compute Microclimate Modifiers**:
   - Project polygons to `EPSG:3414` (meters) to calculate exact distance to the Johor Strait (NE coast) and Singapore Strait (S/SW coast).

## Gotchas

- Postal Districts (`D01-D28`) do not share 1:1 boundaries with URA Planning Areas; always perform point-in-polygon spatial joins using building coordinates from SLA OneMap Search API.
