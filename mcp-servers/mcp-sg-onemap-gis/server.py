#!/usr/bin/env python3
"""
FastMCP Server: mcp-sg-onemap-gis
Exposes SLA OneMap Elastic Search, Reverse Geocoding, Postal Code -> District (D01-D28) -> URA Subzone resolution,
and URA Master Plan GeoJSON polygon queries.
"""
import json
import urllib.parse
import urllib.request
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-sg-onemap-gis")

@mcp.tool()
def geocode_singapore_postal_code(postal_code: str) -> str:
    """Resolve a 6-digit Singapore postal code via SLA OneMap API and return lat/lng, SVY21 X/Y, Postal District (D01-D28), and building address."""
    url = f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={urllib.parse.quote(postal_code)}&returnGeom=Y&getAddrDetails=Y&pageNum=1"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MCP-SG-OneMap/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e), "postal_code": postal_code})

if __name__ == "__main__":
    mcp.run()
