---
name: github-pages-publisher
description: Package the Singapore Haze Sanctuary WebGIS application, GeoJSON datasets, static charts, and educational documentation into a GitHub repository with automated GitHub Actions Pages deployment.
---
# GitHub Pages WebGIS Publisher

Structure, validate, and publish the Singapore Haze Sanctuary interactive application and educational dataset to GitHub and GitHub Pages.

## When to Use

- Packaging the single-file or modular WebGIS HTML app, GeoJSON subzone layers, and methodology README for public sharing on GitHub Pages

## Steps

1. **Verify Repository Layout**:
   - Ensure `index.html`, `README.md`, `data/sg_subzone_haze_1997_2026.geojson`, and `.github/workflows/deploy-pages.yml` are present at root.
2. **Validate Zero-Backend Portability**:
   - Confirm that the HTML application runs 100% client-side with embedded fallback datasets so any visitor or student opening the GitHub Pages URL gets instant interactive rendering without API key barriers.
