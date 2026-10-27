#!/usr/bin/env python3
"""
Singapore Haze Sanctuary - LinkedIn Post Hero Banner Generator
==============================================================
Creates a high-resolution, professional 1920 x 1080 (16:9) LinkedIn hero banner:
  - Dark mode aesthetic matching the Singapore Haze Sanctuary WebGIS (#070b14)
  - Razor-sharp typography and empirical metrics
  - Embedded synoptic wind plume map and WebGIS live interface card
  - Ground-truth sanctuary hierarchy badges (Pulau Ubin, Changi Point, Pasir Ris)
  - Live GitHub Pages and Open-Source badges
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs("dist/assets", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# 1920 x 1080 px (16:9 standard for LinkedIn feed & preview cards)
W, H = 1920, 1080
img = Image.new("RGBA", (W, H), "#070b14")
draw = ImageDraw.Draw(img)

# Background subtle ambient glow gradients
# Emerald ambient glow in top-right (sanctuary quadrant)
glow_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_overlay)

# Northeast emerald glow
for r in range(450, 0, -15):
    alpha = int(22 * (1.0 - r / 450.0))
    glow_draw.ellipse([1350 - r, 300 - r, 1350 + r, 300 + r], fill=(16, 185, 129, alpha))

# Southwest amber glow (Sumatra plume direction)
for r in range(350, 0, -15):
    alpha = int(18 * (1.0 - r / 350.0))
    glow_draw.ellipse([200 - r, 950 - r, 200 + r, 950 + r], fill=(245, 158, 11, alpha))

img = Image.alpha_composite(img, glow_overlay)
draw = ImageDraw.Draw(img)

# Subtle background grid lines
for x in range(0, W, 80):
    draw.line([(x, 0), (x, H)], fill=(30, 41, 59, 45), width=1)
for y in range(0, H, 80):
    draw.line([(0, y), (W, y)], fill=(30, 41, 59, 45), width=1)

# Try loading system fonts or default
def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

font_kicker = get_font(22, bold=True)
font_title = get_font(62, bold=True)
font_subtitle = get_font(26, bold=False)
font_card_title = get_font(24, bold=True)
font_card_sub = get_font(18, bold=False)
font_badge = get_font(20, bold=True)
font_caption = get_font(17, bold=False)
font_url = get_font(22, bold=True)

# -------------------------------------------------------------------------
# LEFT COLUMN: TYPOGRAPHY, BADGES & SANCTUARY CARDS (X: 80 to 920)
# -------------------------------------------------------------------------

# Top Badge / Kicker
kicker_text = "🇸🇬  SINGAPORE SPATIO-TEMPORAL HAZE SANCTUARY EXPLORER (1997–2026+)"
bbox = font_kicker.getbbox(kicker_text)
badge_w = bbox[2] - bbox[0] + 36
badge_h = 44
draw.rounded_rectangle([80, 70, 80 + badge_w, 70 + badge_h], radius=12, fill=(16, 185, 129, 35), outline=(16, 185, 129, 90), width=1)
draw.text((98, 79), kicker_text, font=font_kicker, fill="#34d399")

# Main Title (2 Lines)
title_line1 = "Where Can You Hide"
title_line2 = "from Haze in Singapore?"
draw.text((80, 135), title_line1, font=font_title, fill="#ffffff")
draw.text((80, 215), title_line2, font=font_title, fill="#10b981")

# Subtitle / Abstract
sub_text = (
    "29 Years of Hourly Telemetry, MSS Wind Vectors, ASMC Satellite AOD &\n"
    "Anisotropic Kriging across all 332 URA Subzones & 28 Postal Districts."
)
draw.text((80, 310), sub_text, font=font_subtitle, fill="#94a3b8", spacing=8)

# Section Divider
draw.line([(80, 395), (880, 395)], fill=(51, 65, 85, 140), width=2)

# Top Sanctuaries Section Header
draw.text((80, 420), "EMPIRICAL SANCTUARY RANKING (1997–2026 CRISIS MATRIX):", font=get_font(18, bold=True), fill="#38bdf8")

# 4 Key Sanctuary & Hazard Cards (2x2 Grid)
cards_data = [
    {
        "x": 80, "y": 460, "w": 385, "h": 125,
        "badge": "#1 OFFSHORE REFUGE",
        "title": "Pulau Ubin (D17, 508329)",
        "score": "HSI 96.4/100 • -28.4% PSI",
        "detail": "Johor Strait channel flushing; 85% forest canopy",
        "color": (16, 185, 129) # Emerald
    },
    {
        "x": 485, "y": 460, "w": 385, "h": 125,
        "badge": "#1 MAINLAND SANCTUARY",
        "title": "Changi Point (D17, 498991)",
        "score": "HSI 94.8/100 • -24.8% PSI",
        "detail": "Eastern headland marine inflow; 42 km overland buffer",
        "color": (20, 184, 166) # Teal
    },
    {
        "x": 80, "y": 605, "w": 385, "h": 125,
        "badge": "#2 RESIDENTIAL CORE",
        "title": "Loyang / Pasir Ris (D17/D18)",
        "score": "HSI 92.1/100 • -21.9% PSI",
        "detail": "Pasir Ris coastal mangrove dry-deposition sink",
        "color": (6, 182, 212) # Cyan
    },
    {
        "x": 485, "y": 605, "w": 385, "h": 125,
        "badge": "🚫 GROUND ZERO (SW PLUMES)",
        "title": "Tuas View & Jurong (D22, 639841)",
        "score": "HSI 48.2/100 • +23.6% PSI",
        "detail": "Direct Sumatra landfall; acute +35 to +85 PSI surge",
        "color": (239, 68, 68) # Red
    }
]

for c in cards_data:
    # Card background box
    draw.rounded_rectangle([c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"]], radius=14, fill=(15, 23, 42, 220), outline=c["color"] + (110,), width=1)
    # Badge text
    draw.text((c["x"] + 16, c["y"] + 14), c["badge"], font=get_font(13, bold=True), fill=c["color"])
    # Location Title
    draw.text((c["x"] + 16, c["y"] + 38), c["title"], font=get_font(18, bold=True), fill="#f8fafc")
    # Score & Delta
    draw.text((c["x"] + 16, c["y"] + 67), c["score"], font=get_font(16, bold=True), fill=c["color"])
    # Detail
    draw.text((c["x"] + 16, c["y"] + 93), c["detail"], font=get_font(13, bold=False), fill="#94a3b8")

# Bottom Highlights & Call-to-Action Bar
cta_y = 760
draw.rounded_rectangle([80, cta_y, 870, cta_y + 115], radius=16, fill=(15, 23, 42, 240), outline=(56, 189, 248, 90), width=1)

# Tags inside CTA
tags = ["Zero-Backend WebGIS", "1997–2026 Baseline", "All 28 Postal Districts", "WCAG AA Audited"]
tag_x = 100
for t in tags:
    t_bbox = font_caption.getbbox(t)
    tw = t_bbox[2] - t_bbox[0] + 18
    draw.rounded_rectangle([tag_x, cta_y + 16, tag_x + tw, cta_y + 44], radius=8, fill=(30, 41, 59, 180), outline=(51, 65, 85, 120), width=1)
    draw.text((tag_x + 9, cta_y + 21), t, font=font_caption, fill="#cbd5e1")
    tag_x += tw + 12

# URL Link Callout
draw.text((100, cta_y + 62), "Explore Interactive Map:", font=get_font(17, bold=False), fill="#94a3b8")
draw.text((310, cta_y + 60), "lauyeehow1986-hub.github.io/haze_sanctuary/", font=font_url, fill="#38bdf8")

# Open Source / GitHub Tag
github_text = "⭐ Open Source on GitHub: lauyeehow1986-hub/haze_sanctuary • MIT Licensed"
draw.text((80, 910), github_text, font=get_font(16, bold=False), fill="#64748b")

# -------------------------------------------------------------------------
# RIGHT COLUMN: EMBEDDED MAP & TELEMETRY VISUALS (X: 930 to 1840)
# -------------------------------------------------------------------------
# Container box for the synoptic wind plume map and desktop interface
right_box_x = 930
right_box_y = 70
right_box_w = 910
right_box_h = 935

draw.rounded_rectangle([right_box_x, right_box_y, right_box_x + right_box_w, right_box_y + right_box_h],
                       radius=20, fill=(15, 23, 42, 230), outline=(51, 65, 85, 150), width=1)

# Header inside right card
draw.text((right_box_x + 24, right_box_y + 20), "ATMOSPHERIC DISPERSION & SYNOPTIC TRANSPORT MODEL", font=get_font(16, bold=True), fill="#38bdf8")
draw.text((right_box_x + 24, right_box_y + 46), "Sumatra SW (225°) Plume Landfall vs. Johor Strait Marine Flushing Channel", font=get_font(14, bold=False), fill="#94a3b8")

# Embed the generated 300 DPI Synoptic Wind Plumes Map
plume_map_path = "dist/assets/sg_haze_synoptic_wind_plumes.png"
if os.path.exists(plume_map_path):
    plume_img = Image.open(plume_map_path)
    # Crop & scale to fit nicely in top half of right box
    target_w = right_box_w - 48
    target_h = int(target_w * (plume_img.height / plume_img.width))
    plume_resized = plume_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Rounded corners for embedded image
    mask = Image.new("L", (target_w, target_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, target_w, target_h], radius=14, fill=255)
    
    img.paste(plume_resized, (right_box_x + 24, right_box_y + 80), mask=mask)

# Embed Desktop WebGIS Screenshot Preview
desktop_shot_path = "dist/assets/audit/webgis_desktop_1440.png"
if os.path.exists(desktop_shot_path):
    shot_img = Image.open(desktop_shot_path)
    shot_w = right_box_w - 48
    shot_h = 360
    # Crop top part of web app interface
    crop_area = (0, 0, shot_img.width, int(shot_img.width * (shot_h / shot_w)))
    shot_cropped = shot_img.crop(crop_area).resize((shot_w, shot_h), Image.Resampling.LANCZOS)
    
    shot_mask = Image.new("L", (shot_w, shot_h), 0)
    shot_mask_draw = ImageDraw.Draw(shot_mask)
    shot_mask_draw.rounded_rectangle([0, 0, shot_w, shot_h], radius=14, fill=255)
    
    img.paste(shot_cropped, (right_box_x + 24, right_box_y + 510), mask=shot_mask)

# Label overlay on bottom preview
draw.rounded_rectangle([right_box_x + 40, right_box_y + 526, right_box_x + 400, right_box_y + 560],
                       radius=8, fill=(7, 11, 20, 220), outline=(16, 185, 129, 120), width=1)
draw.text((right_box_x + 52, right_box_y + 534), "LIVE INTERACTIVE WEBGIS INTERFACE", font=get_font(13, bold=True), fill="#34d399")

# Footer caption on right card
draw.text((right_box_x + 24, right_box_y + 890), "Fusing NEA ground sensors, MSS radiosonde inversions, Himawari/MODIS AOD & URA Subzones", font=get_font(13, bold=False), fill="#64748b")

# Save outputs
out_hero = "dist/assets/linkedin_hero_banner.png"
out_hero_root = "assets/linkedin_hero_banner.png"
img.save(out_hero, "PNG", quality=95)
img.save(out_hero_root, "PNG", quality=95)
print(f"Generated LinkedIn Hero Banner at: {out_hero} and {out_hero_root}")
