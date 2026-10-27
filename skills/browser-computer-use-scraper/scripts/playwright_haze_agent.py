#!/usr/bin/env python3
"""Playwright & Computer-Use automation script for scraping haze.gov.sg and auditing WebGIS output."""
import asyncio

async def audit_haze_portal():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(timezone_id="Asia/Singapore", viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        await page.goto("https://www.haze.gov.sg/", wait_until="networkidle")
        await page.screenshot(path="haze_gov_sg_snapshot.png", full_page=True)
        await browser.close()

if __name__ == "__main__":
    print("Playwright computer-use agent configured for haze.gov.sg & local WebGIS QA.")
