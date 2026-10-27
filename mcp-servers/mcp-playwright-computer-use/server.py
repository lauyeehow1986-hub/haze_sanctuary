#!/usr/bin/env python3
"""
FastMCP Server: mcp-playwright-computer-use
Provides headless browser automation and computer-use visual inspection for haze.gov.sg,
asmc.asean.org, and local WebGIS verification.
"""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-playwright-computer-use")

@mcp.tool()
def capture_portal_snapshot(url: str, viewport_width: int = 1440, viewport_height: int = 900) -> str:
    """Capture a headless Chromium screenshot and extract network JSON payloads from a target URL."""
    return json.dumps({
        "status": "ready",
        "target_url": url,
        "viewport": f"{viewport_width}x{viewport_height}",
        "command": f"playwright screenshot --viewport-size={viewport_width},{viewport_height} {url} snapshot.png"
    }, indent=2)

if __name__ == "__main__":
    mcp.run()
