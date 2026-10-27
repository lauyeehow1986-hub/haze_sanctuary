#!/usr/bin/env bash
set -euo pipefail

echo "=================================================================="
echo " Setting up Singapore Haze Sanctuary Antigravity Kit (1997-2026+) "
echo "=================================================================="

# 1. Python virtual environment & geospatial dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 2. Node.js MCP & WebGIS packages
npm install

# 3. Install Playwright Chromium for Computer-Use & Portal Scraping
npx playwright install --with-deps chromium

echo ""
echo "[OK] Setup complete!"
echo "1. Import the 'skills/' directory into Antigravity Skill Manager."
echo "2. Load 'mcp_config.json' into Antigravity MCP Settings."
echo "3. Open 'ANTIGRAVITY_MASTER_PROMPT.md' and paste into Gemini 3.8 Flash (High Effort)."
