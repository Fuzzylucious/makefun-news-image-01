#!/usr/bin/env python3
"""Render the news-image-01 entry: a newspaper front page summing up the
world news of Friday 13 November 2026.

Build-time tool only (Pillow is NOT available in the make.fun sandbox).
The graded entrypoint is main.py, which copies the rendered entry.png.
Run: python3 gen.py  ->  writes entry.png (1024x1024, deterministic).

Stories verified 14 Nov 2026 against AP / BBC / Al Jazeera / Reuters / NPR
reporting of 13 November 2026. Claims are attributed where the source
itself attributed them ("Iran claims...").
"""

from PIL import Image, ImageDraw, ImageFont

SS = 2                      # render at 2048, downsample to 1024
W, H = 1024 * SS, 1024 * SS
M = 36 * SS                 # outer margin

PAPER = (246, 241, 231)
INK = (20, 33, 61)
RED = (172, 32, 22)
TEAL = (0, 102, 102)
GOLD = (146, 104, 0)
GRAY = (96, 92, 82)
RULE = (186, 176, 152)
NAVY_BAND = (20, 33, 61)
WHITE = (255, 255, 255)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size * SS))


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r, color, width):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=width)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=width)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
          0, 360, fill=color, width=width)
    d.arc([cx - r * 0.8, cy - r * 0.85, cx + r * 0.8, cy + r * 0.85],
          0, 360, fill=color, width=width)


def draw_drone(d, cx, cy, s, color, width):
    # simple quadcopter glyph: body + 4 rotors + legs
    d.ellipse([cx - s * 0.28, cy - s * 0.16, cx + s * 0.28, cy + s * 0.16],
              fill=color)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        rx, ry = cx + dx * s * 0.42, cy + dy * s * 0.30
        d.ellipse([rx - s * 0.20, ry - s * 0.06, rx + s * 0.20, ry + s * 0.06],
                  outline=color, width=width)
        d.line([cx + dx * s * 0.22, cy + dy * s * 0.12,
                rx - dx * s * 0.08, ry - dy * s * 0.04],
               fill=color, width=width)
    d.line([cx - s * 0.16, cy + s * 0.16, cx - s * 0.22, cy + s * 0.34],
           fill=color, width=width)
    d.line([cx + s * 0.16, cy + s * 0.16, cx + s * 0.22, cy + s * 0.34],
           fill=color, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- outer border ------------------------------------------------------------
d.rectangle([M // 2, M // 2, W - M // 2, H - M // 2], outline=INK,
            width=3 * SS)

# --- masthead --------------------------------------------------------------
f_title = font(F_SERIF_B, 50)
f_date = font(F_SANS, 23)
title = "THE WORLD IN ONE DAY"
tw = d.textlength(title, font=f_title)
tx = (W - tw) / 2
ty = 40 * SS
draw_globe(d, int(M + 34 * SS), int(ty + 26 * SS), 28 * SS, INK, 3 * SS)
d.text((tx, ty), title, font=f_title, fill=INK)
date = "FRIDAY, 13 NOVEMBER 2026  ·  THE DAY IN WORLD NEWS"
dw = d.textlength(date, font=f_date)
d.text(((W - dw) / 2, ty + 66 * SS), date, font=f_date, fill=GRAY)
y = ty + 104 * SS
d.line([M, y, W - M, y], fill=INK, width=3 * SS)
d.line([M, y + 7 * SS, W - M, y + 7 * SS], fill=INK, width=1 * SS)
y += 15 * SS

# --- lead story: Ukraine ----------------------------------------------------
f_kick = font(F_SANS_B, 21)
f_lead = font(F_SERIF_B, 40)
f_deck = font(F_SANS, 22)
LEAD_W = 700 * SS
d.text((M, y), "UKRAINE  ·  WAR & TALKS", font=f_kick, fill=RED)
y += 30 * SS
lead_head = "Ukraine fires ~1,200 drones in one of its biggest attacks"
for line in wrap(d, lead_head, f_lead, LEAD_W):
    d.text((M, y), line, font=f_lead, fill=INK)
    y += 47 * SS
y += 4 * SS
lead_deck = ("US envoys say Europe will join the next round of peace talks; "
             "work begins on the war's largest prisoner exchange.")
for line in wrap(d, lead_deck, f_deck, LEAD_W):
    d.text((M, y), line, font=f_deck, fill=INK)
    y += 28 * SS
# drone swarm art, right of the lead
draw_drone(d, W - M - 150 * SS, 250 * SS, 92 * SS, INK, 3 * SS)
draw_drone(d, W - M - 60 * SS, 305 * SS, 62 * SS, RED, 3 * SS)
draw_drone(d, W - M - 215 * SS, 320 * SS, 52 * SS, TEAL, 3 * SS)

lead_bottom = y + 12 * SS
d.line([M, lead_bottom, W - M, lead_bottom], fill=INK, width=2 * SS)
y = lead_bottom + 20 * SS

# --- grid: 6 stories, 2 cols x 3 rows --------------------------------------
stories = [
    ("GULF  ·  IRAN", RED,
     "US downs two Iranian drones bound for Bahrain",
     "Iran claims it destroyed a US radar in Bahrain; four tankers were "
     "hit in Hormuz."),
    ("TECH  ·  CHIPS", NAVY_BAND,
     "Nvidia chief Jensen Huang resigns",
     "CFO Colette Kress takes over as interim chief; the board names "
     "its first chair."),
    ("TECH  ·  OUTAGE", TEAL,
     "Microsoft 365 outage enters a second day",
     "Outlook, Teams and Copilot disrupted worldwide; police and court "
     "systems hit."),
    ("CRIME  ·  CRYPTO", GOLD,
     "US moves to seize $1.2bn from Binance hack",
     "Court backs seizure of crypto stolen on 29 October; FBI blames "
     "North Korean hackers."),
    ("ASIA  ·  TAIWAN", NAVY_BAND,
     "Taiwan says China ran large unannounced Pacific drills",
     "Taipei calls the earlier-November naval deployment intimidation; "
     "Beijing silent."),
    ("SPORT  ·  FOOTBALL", RED,
     "Kane breaks England's caps record",
     "Striker wins his 126th cap against Croatia in the Nations League "
     "quarter-final."),
]
f_head = font(F_SERIF_B, 29)
f_body = font(F_SANS, 20)
COL_W = (W - 2 * M - 28 * SS) // 2
ROW_H = 160 * SS
for i, (kick, kc, head, body) in enumerate(stories):
    cx = M + (i % 2) * (COL_W + 28 * SS)
    cy = y + (i // 2) * ROW_H
    d.text((cx, cy), kick, font=f_kick, fill=kc)
    hy = cy + 30 * SS
    for line in wrap(d, head, f_head, COL_W):
        d.text((cx, hy), line, font=f_head, fill=INK)
        hy += 33 * SS
    by = hy + 2 * SS
    for line in wrap(d, body, f_body, COL_W):
        d.text((cx, by), line, font=f_body, fill=(52, 50, 44))
        by += 26 * SS
    if i % 2 == 0:
        d.line([cx + COL_W + 14 * SS, cy + 4 * SS,
                cx + COL_W + 14 * SS, cy + ROW_H - 26 * SS],
               fill=RULE, width=1 * SS)
    if i // 2 < 2:
        d.line([M, cy + ROW_H - 8 * SS, W - M, cy + ROW_H - 8 * SS],
               fill=RULE, width=1 * SS)
y = y + 3 * ROW_H + 8 * SS

# --- ticker band ------------------------------------------------------------
band_y = y + 6 * SS
band_h = 64 * SS
d.rectangle([M, band_y, W - M, band_y + band_h], fill=NAVY_BAND)
f_tick = font(F_SANS_B, 20)
ticker = ("ALSO TODAY  ·  US reports a record 483,200 deportations in 2026  ·  "
          "IEA sees a Q4 oil surplus of 1.7m barrels a day")
tlines = wrap(d, ticker, f_tick, W - 2 * M - 24 * SS)
ty = band_y + (band_h - len(tlines) * 26 * SS) // 2
for line in tlines:
    lw = d.textlength(line, font=f_tick)
    d.text(((W - lw) / 2, ty), line, font=f_tick, fill=WHITE)
    ty += 26 * SS

# --- footer -----------------------------------------------------------------
f_foot = font(F_SANS, 15)
foot = "Stories as reported on 13 November 2026  ·  AP  ·  BBC  ·  Al Jazeera  ·  Reuters  ·  NPR"
fw = d.textlength(foot, font=f_foot)
d.text(((W - fw) / 2, band_y + band_h + 14 * SS), foot, font=f_foot, fill=GRAY)

img = img.resize((1024, 1024), Image.LANCZOS)
img.save("entry.png", "PNG")
print("wrote entry.png")
