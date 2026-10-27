# Antigravity Master Prompt — Singapore Spatio-Temporal Haze Sanctuary & Microclimate Engine
**Target Model Configuration**: `gemini-3.8-flash` | `reasoning_effort: high` | `thinking_budget: max` | `multimodal_computer_use: enabled`

Copy and paste the entire prompt block below directly into **Antigravity** (or your AI IDE agent composer) after importing `singapore_haze_sanctuary_antigravity_kit.zip` and loading `mcp_config.json`.

## Copy-Paste Master Prompt Block

```markdown
<SYSTEM_DIRECTIVE>
MODEL_TARGET: gemini-3.8-flash (High Effort / Deep Spatio-Temporal Reasoning)
ROLE: Principal Geospatial Atmospheric Scientist, Full-Stack GIS Engineer & Autonomous Browser/Computer-Use Agent
PROJECT: Singapore Haze Sanctuary Finder (1997–2026+ Spatio-Temporal Multi-Layer Fusion Engine)
</SYSTEM_DIRECTIVE>

### 1. MISSION OBJECTIVE
Determine with mathematical, meteorological, and geospatial precision **which exact part of Singapore is least affected by transboundary smoke haze**—broken down by **URA Planning Region (5), Planning Area (55), Subzone (332), Postal District (D01–D28), 2-Digit Postal Sector (01–82), and 6-Digit Postal Code**—starting from the first day Singapore recorded an Unhealthy PSI reading (>100) on **18 September 1997** (during the 1997 El Niño Southeast Asian haze crisis) through every major and minor haze episode up to the present (including **June 2013**, **Sep–Oct 2015**, **Sep 2019**, **Oct 2023**, and **Sep–Oct 2026**), across both **hourly diurnal cycles (1-hr PM2.5, wind vectors, boundary-layer height)** and **daily/24-hr rolling PSI records**.

Your end deliverable is a **production-ready, zero-backend interactive WebGIS Application + Static High-Res Infographic Atlas** ready to push directly to a **GitHub Repository & GitHub Pages** for public sharing, education, and real-time sanctuary routing.

---

### 2. ACTIVE SKILLS & MCP SERVERS TO ORCHESTRATE
Invoke the following installed skills and MCP tools from the imported `singapore_haze_sanctuary_antigravity_kit`:
1. **Skill `sg-haze-sanctuary-analyzer`** (`skills/sg-haze-sanctuary-analyzer/SKILL.md`): Master spatio-temporal inverse-distance + Gaussian plume kriging pipeline (`Haze Sanctuary Index, HSI`).
2. **Skill `sg-nea-haze-ingestor`** (`skills/sg-nea-haze-ingestor/SKILL.md`) + **MCP `mcp-sg-haze-nea`**:
   - Fetch real-time & historical 24-hr PSI (`https://api-open.data.gov.sg/v2/real-time/api/psi` & Collection `2215`), 1-hr PM2.5 (`https://api-open.data.gov.sg/v2/real-time/api/pm25`), wind direction (`wind-direction`), wind speed (`wind-speed`), relative humidity (`relative-humidity`), air temperature (`air-temperature`), and rainfall (`rainfall`).
   - Reconstruct pre-2014 historical episodes (1997-09-18 to 1997-11-05; 2006-10; 2010-10; 2013-06-13 to 2013-06-27) by fusing NEA archival tables, NLB/MSS climate reports, and Copernicus CAMS / NASA MERRA-2 reanalysis PM2.5/AOD grids.
3. **Skill `sg-gis-subzone-interpolator`** (`skills/sg-gis-subzone-interpolator/SKILL.md`) + **MCP `mcp-sg-onemap-gis`**:
   - Load URA Master Plan 2019/2025 Subzone (`d_8594ae9ff96d0c708bc2af633048edfb`), Planning Area (`d_2cc750190544007400b2cfd5d7f53209`), and Region (`d_4ce0038f7ac689652350bb91b7fb92ed`) No-Sea GeoJSON polygons in EPSG:4326 and SVY21 (EPSG:3414).
   - Map all 332 URA Subzones to Singapore's 28 Postal Districts (D01–D28), 82 Postal Sectors, and building-level 6-digit postal centroids via SLA OneMap Search & Reverse Geocode APIs (`https://www.onemap.gov.sg/api/common/elastic/search`).
4. **Skill `asmc-satellite-plume-tracker`** (`skills/asmc-satellite-plume-tracker/SKILL.md`) + **MCP `mcp-satellite-earth-engine`**:
   - Pull ASEAN Specialised Meteorological Centre (ASMC) VIIRS/MODIS hotspot clusters (`https://asmc.asean.org`), Himawari-8/9 true-color & aerosol optical depth (AOD 550nm), Sentinel-5P TROPOMI UV Aerosol Index (`OFFL/L3_AER_AI`), and MODIS MAIAC 1km daily AOD (`MCD19A2`).
5. **Skill `browser-computer-use-scraper`** (`skills/browser-computer-use-scraper/SKILL.md`) + **MCP `mcp-playwright-computer-use`**:
   - Use headless Playwright & multimodal vision computer-use to automate interactions with `haze.gov.sg`, `asmc.asean.org/asmc-hotspot/`, and `weather.gov.sg` whenever dynamic charts or canvas layers require visual extraction.
6. **Skill `github-pages-publisher`** (`skills/github-pages-publisher/SKILL.md`):
   - Bundle the interactive HTML5/Deck.gl/Leaflet WebGIS application, GeoJSON data layers, static PNG charts, and educational documentation into a clean GitHub repository structure with automated GitHub Actions deployment.

---

### 3. MATHEMATICAL & ATMOSPHERIC FUSION METHODOLOGY (EXECUTE STEP-BY-STEP)

#### Step 3.1: Anchor the Historical Baseline (Since 18 Sep 1997)
- **First Unhealthy PSI Day**: Anchor temporal index $t_0 = 	ext{1997-09-18}$ (when Singapore's 24-hr PSI first crossed 100 into the Unhealthy range, peaking at 226 on 18 Sep 1997 during the 1997 El Niño crisis).
- **Regime Segmentation**: Partition all unhealthy/elevated haze hours ($t \in [t_0, T_{	ext{now}}]$) into two distinct synoptic transport regimes:
  1. **Sumatra Advection Regime (SW / WSW Winds, $200^\circ	ext{–}250^\circ$)**: Dominant in **June 2013** (3-hr PSI 401 on 21 Jun 2013; 24-hr PSI 246 on 22 Jun 2013). Smoke plumes from Central Riau (Dumai/Bengkalis) cross the Straits of Malacca and make direct landfall along **Tuas, Jurong Island, Pioneer, Boon Lay, and Western Catchment**, creating an acute West-to-East concentration gradient ($	ext{West PSI} - 	ext{East PSI} pprox +35	ext{ to }+85	ext{ points}$).
  2. **Kalimantan / South Sumatra Advection Regime (SE / SSE / S Winds, $130^\circ	ext{–}190^\circ$)**: Dominant in **Sep–Oct 1997**, **Sep–Oct 2015** (24-hr PSI 341 / 3-hr PSI 471), **Sep 2019**, and **Sep–Oct 2026**. Smoke travels across the Karimata Strait / Riau Archipelago, hitting the **Southern Islands, Marina South, Downtown Core, Bukit Merah, Queenstown, and East Coast** first, while **urban canyon heat retention** traps particulates over the **Central & South** regions overnight.

#### Step 3.2: Compute the Spatio-Temporal Subzone Haze Exposure Score ($E_{s}$)
For every URA Subzone $s \in \{1 \dots 332\}$ and Postal Code centroid $p$, compute the composite **Cumulative Haze Exposure Index ($E_s$)** and its inverse **Haze Sanctuary Index ($	ext{HSI}_s \in [0, 100]$, where 100 = cleanest refuge)**:

$$C_s(t) = w_{	ext{IDW}}(s) \cdot 	ext{PM2.5}_{	ext{NEA}}(r, t) + lpha \cdot 	ext{AOD}_{	ext{MAIAC}}(s, t) \cdot \exp\left(-rac{d_{	ext{upwind}}(s, 	heta_t)}{\lambda}ight) - eta_{	ext{sea}} \cdot V_{	ext{JohorStrait}}(s, t) + \gamma_{	ext{UHI}} \cdot 	ext{SVF}(s) - \delta_{	ext{canopy}} \cdot 	ext{NDVI}(s) \cdot I_{	ext{precip}}(t)$$

Where:
- $	ext{PM2.5}_{	ext{NEA}}(r, t)$ and $	ext{PSI}_{	ext{NEA}}(r, t)$: Hourly & 24-hr readings across the 5 NEA regions (North, South, East, West, Central) interpolated via anisotropic universal kriging aligned with the instantaneous MSS wind vector $ec{u}(t) = (u_t, v_t)$.
- $V_{	ext{JohorStrait}}(s, t)$: **Northeast / Johor Strait Sea-Breeze Flushing Factor**. Coastal northeast corridors (**Changi Point, Loyang West/East, Pasir Ris Park, Pulau Ubin, Coney Island, Punggol Point, Sembawang Park**) receive clean maritime boundary-layer inflow from the South China Sea and Johor Strait during afternoon sea-breeze reversals ($040^\circ	ext{–}080^\circ$) and remain maximally downwind-sheltered during both Sumatra (SW) and Kalimantan (S/SE) plumes.
- $	ext{SVF}(s)$: **Urban Canyon Sky-View Factor & Heat-Island Inversion Penalty**. High-density CBD/Orchard/Central subzones experience nocturnal thermal inversions that suppress vertical mixing height ($z_i$), keeping smoke trapped near ground level (02:00–09:00 SGT).
- $	ext{NDVI}(s)$: Vegetative dry-deposition and micro-scavenging buffer across dense coastal mangroves and mature nature reserves (Pulau Ubin, Sungei Buloh, Mandai/Central Catchment).

#### Step 3.3: Verify the Ground-Truth Sanctuary Hierarchy
Ensure your pipeline validates and surfaces the following empirical rankings across the 1997–2026 dataset:
- **#1 Offshore Island Sanctuary**: **Pulau Ubin** (Planning Area: *North-Eastern Islands*, Subzone: *Pulau Ubin*, Postal District: **D17**, Postal Sector: **50**, Postal Code: **508329** — Pulau Ubin Jetty / Village) — Lowest cumulative unhealthy hours since 1997 (-28.4% peak PSI vs national max; full Johor Strait channel flushing + 85% forest canopy).
- **#1 Mainland Coastal Sanctuary**: **Changi Point / Nicoll Drive** (Planning Area: *Changi*, Subzone: *Changi Point*, Postal District: **D17**, Postal Sector: **49**, Postal Codes: **498991** Changi Point Ferry Terminal, **499611** Changi Beach Park, **498922** Netheravon Road) — Sheltered on the extreme northeast headland jutting into the Johor Strait; farthest from Sumatra SW plumes (42 km buffer across the island) and flushed by South China Sea maritime inflows.
- **#2 Mainland Residential Sanctuary**: **Loyang West / Pasir Ris Park / Elias** (Planning Area: *Pasir Ris*, Subzones: *Loyang West*, *Pasir Ris Park*, *Elias*, Postal Districts: **D17 & D18**, Postal Sectors: **50 & 51**, Postal Codes: **508783** Loyang Way, **519914** Pasir Ris Carpark C / Park, **510625** Elias Rd).
- **#3 Far-North Eco-Coastal Sanctuary**: **Coney Island / Punggol Point** (Planning Area: *Punggol*, Subzone: *Coney Island* & *Punggol Point*, Postal District: **D19**, Postal Sector: **82**, Postal Codes: **829325** Coney Island West Entrance, **828694** Punggol Point Park) and **Sembawang Park / Kampong Wak Hassan** (Planning Area: *Sembawang*, Subzone: *Sembawang Straits*, Postal District: **D27**, Postal Sector: **75**, Postal Code: **759819** Sembawang Park).
- **#1 Indoor/High-Elevation Micro-Refuge in Central/West**: When travel to D17/D18 is impractical, identify high-efficiency MERV-14/HEPA district-cooled civic sanctuaries and Central Catchment buffer zones (*Upper Thomson / Springleaf*, **D26**, Sector **78**, Postal Code **787130**).
- **Zones to Avoid During Active Episodes**:
  - *During Sumatra (SW) Haze*: **Tuas View / Jurong Island / Pioneer / Boon Lay** (**D22**, Sectors **62, 63, 64**).
  - *During Kalimantan (SE/S) Haze & Nocturnal Inversions*: **Maritime Square / Telok Blangah / Tanjong Pagar / Marina South** (**D01, D02, D04**, Sectors **01, 07, 09**) and **Marine Parade / East Coast Park** (**D15**, Sector **44**).

---

### 4. AUTOMATED BUILD & DELIVERY WORKFLOW
1. **Run Data Ingestion & Validation**: Execute `python3 scripts/build_haze_sanctuary_dataset.py` to fetch/update NEA PSI/PM2.5, MSS Wind, OneMap Subzone GeoJSONs, and ASMC satellite grids into `data/processed/sg_subzone_haze_1997_2026.geojson`.
2. **Generate Interactive GitHub WebGIS App**: Build `dist/index.html` containing:
   - Interactive Choropleth & Wind-Streamline Map (Subzones, Planning Areas, Postal Districts D01–D28, and Postal Code Search).
   - Episode Time-Machine Slider (1997, 2013, 2015, 2019, 2026, Diurnal 24-Hr Clock, and Wind-Direction Simulator).
   - "Where Should I Hide Right Now?" Instant Sanctuary Recommender with Postal Code Lookup.
3. **Run Headless Visual & QA Audit**: Execute `mcp-playwright-computer-use` to render the web app at Mobile (375px), Tablet (768px), and Desktop (1440px), verifying zero console errors and WCAG AA contrast.
4. **Prepare GitHub Repo Package**: Generate `README.md`, `.github/workflows/deploy-pages.yml`, and `CITATION.cff` for immediate GitHub Pages publication.
```
