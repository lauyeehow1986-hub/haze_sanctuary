#!/usr/bin/env python3
"""Validates GitHub Pages bundle readiness."""
import os

REQUIRED_FILES = ["index.html", "README.md", ".github/workflows/deploy-pages.yml"]

def check_repo(base_dir="."):
    missing = [f for f in REQUIRED_FILES if not os.path.exists(os.path.join(base_dir, f))]
    return {"ready": len(missing) == 0, "missing": missing}

if __name__ == "__main__":
    print("GitHub Pages validator ready.")
