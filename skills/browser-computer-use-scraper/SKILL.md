---
name: browser-computer-use-scraper
description: Automate headless Playwright browser scraping and multimodal vision computer-use for dynamic Singapore air quality portals (haze.gov.sg, asmc.asean.org, weather.gov.sg, onemap.gov.sg) and visual verification of the generated WebGIS dashboard.
---
# Browser & Computer-Use Automation Skill

Orchestrate Playwright browser automation and multimodal computer-use vision inspection to extract dynamic canvas maps from `haze.gov.sg` and `asmc.asean.org`, and visually audit rendered WebGIS deliverables.

## When to Use

- Extracting interactive hotspot maps, wind-barb overlays, or dynamic charts from `haze.gov.sg`, `asmc.asean.org`, or `weather.gov.sg`
- Performing automated headless browser testing and visual regression checks on the generated GitHub Pages WebGIS application

## Steps

1. **Launch Headless Chromium with Geolocation Set to Singapore**:
   - Set timezone `Asia/Singapore` and viewport `1440x900`.
2. **Intercept XHR/Fetch JSON Payloads**:
   - Attach `page.on("response", ...)` listeners when loading `haze.gov.sg` and `onemap.gov.sg` to capture raw JSON tile and station payloads directly before DOM parsing.
3. **Computer-Use Visual QA**:
   - Capture full-page screenshots across desktop and mobile viewports, asserting zero overlapping tooltips, clear legend contrast, and interactive subzone click responsiveness.
