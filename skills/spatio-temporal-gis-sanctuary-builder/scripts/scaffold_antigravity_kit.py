#!/usr/bin/env python3
"""
Scaffolds a complete Antigravity IDE Kit directory and ZIP archive for any
Spatio-Temporal GIS Sanctuary project (Skills + FastMCP Servers + Master Prompt + GitHub Actions).
"""
import os
import json
import zipfile

def create_kit_skeleton(target_dir: str, project_slug: str):
    os.makedirs(os.path.join(target_dir, "skills"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "mcp-servers"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "dist"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, ".github/workflows"), exist_ok=True)

    mcp_cfg = {
        "mcpServers": {
            f"{project_slug}-telemetry": {
                "command": "python3",
                "args": [f"./mcp-servers/mcp-{project_slug}-telemetry/server.py"]
            },
            f"{project_slug}-gis": {
                "command": "python3",
                "args": [f"./mcp-servers/mcp-{project_slug}-gis/server.py"]
            },
            "satellite-earth-engine": {
                "command": "python3",
                "args": ["./mcp-servers/mcp-satellite-earth-engine/server.py"]
            },
            "playwright-computer-use": {
                "command": "python3",
                "args": ["./mcp-servers/mcp-playwright-computer-use/server.py"]
            },
            "github-mcp": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"]
            }
        }
    }
    with open(os.path.join(target_dir, "mcp_config.json"), "w") as f:
        json.dump(mcp_cfg, f, indent=2)
    return os.path.join(target_dir, "mcp_config.json")

if __name__ == "__main__":
    print("Antigravity Kit Scaffolder ready.")
