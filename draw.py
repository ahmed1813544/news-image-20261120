#!/usr/bin/env python3
"""Draw the entry image for make.fun's news-image-20261120 bounty:
"Sum up 20 November's world news in one image."

A newspaper front page for Friday 20 November 2026, drawn entirely
in code with PIL: a Kyiv lead story with a drawn scene, Cyclone
Akvan and the AI market sell-off as second stories, and a grid of
short items across seven regions. Every word is set in a real font
here, so nothing is garbled. Deterministic: same bytes every run.
"""

import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 233)
INK = (22, 25, 31)
RED = (178, 32, 42)
BLUE = (29, 78, 137)
GREY = (90, 92, 96)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=F(SERIF_B, 56),
       fill=INK, anchor="ma")
d.line([(36, 78), (W - 36, 78)], fill=INK, width=3)
d.line([(36, 84), (W - 36, 84)], fill=INK, width=1)
d.rectangle([0, 92, W, 138], fill=RED)
d.text((W // 2, 100), "FRIDAY  20  NOVEMBER  2026", font=F(SANS_B, 34),
       fill=WHITE, anchor="ma")
d.text((W // 2, 146), "32 stories  ·  7 regions  ·  one day", font=F(SANS, 19),
       fill=GREY, anchor="ma")

# ---------- lead story: Kyiv ----------
LY = 176
d.rectangle([36, LY, W - 36, LY + 240], outline=INK, width=2)
sx0, sy0, sx1, sy1 = 48, LY + 12, 496, LY + 228
d.rectangle([sx0, sy0, sx1, sy1], fill=(16, 22, 44))
rnd = random.Random(20)
for _ in range(46):
    x = rnd.randint(sx0 + 4, sx1 - 4)
    y = rnd.randint(sy0 + 4, sy0 + 84)
    d.point((x, y), fill=(220, 224, 235))
for (mx, my, ln) in [(110, 22, 58), (238, 10, 76), (356, 26, 52)]:
    d.line([(sx0 + mx, sy0 + my), (sx0 + mx + ln, sy0 + my + ln)],
           fill=(255, 176, 84), width=3)
    d.ellipse([sx0 + mx + ln - 5, sy0 + my + ln - 5, sx0 + mx + ln + 5,
               sy0 + my + ln + 5], fill=(255, 120, 60))
d.rectangle([sx0, sy1 - 100, sx1, sy1 - 58], fill=(10, 13, 24))
for bx, bh in [(18, 28), (64, 42), (126, 24), (322, 38), (384, 28)]:
    d.rectangle([sx0 + bx, sy1 - 100 - bh, sx0 + bx + 32, sy1 - 100],
                fill=(10, 13, 24))
d.rectangle([sx0, sy1 - 58, sx1, sy1], fill=(24, 52, 96))
for i, cx in enumerate([88, 220, 352]):
    bx0, bx1, top = sx0 + cx - 54, sx0 + cx + 54, sy1 - 58
    if i == 1:
        d.line([(bx0, top - 24), (sx0 + cx - 8, top - 20)], fill=(200, 205, 214), width=5)
        d.line([(bx1, top - 24), (sx0 + cx + 10, top - 6)], fill=(200, 205, 214), width=5)
        d.line([(sx0 + cx - 8, top - 20), (sx0 + cx - 2, top + 14)], fill=(200, 205, 214), width=5)
    else:
        d.line([(bx0, top - 24), (bx1, top - 24)], fill=(200, 205, 214), width=5)
    d.line([(bx0 + 6, top - 24), (bx0 + 6, top)], fill=(200, 205, 214), width=3)
    d.line([(bx1 - 6, top - 24), (bx1 - 6, top)], fill=(200, 205, 214), width=3)
d.ellipse([sx0 + 292, sy1 - 122, sx0 + 336, sy1 - 92], fill=(255, 140, 60))
d.ellipse([sx0 + 303, sy1 - 113, sx0 + 325, sy1 - 99], fill=(255, 200, 110))
tx = 512
d.text((tx, LY + 12), "RUSSIA'S BIGGEST", font=F(SERIF_B, 31), fill=INK)
d.text((tx, LY + 50), "BARRAGE SMASHES", font=F(SERIF_B, 31), fill=INK)
d.text((tx, LY + 88), "KYIV'S BRIDGES", font=F(SERIF_B, 31), fill=INK)
for j, line in enumerate([
        "100+ missiles, 400 drones in one night —",
        "three Dnipro bridges hit, 8+ killed, the",
        "capital dark. Lviv station struck; missiles",
        "fell in Poland, NATO jets scrambled."]):
    d.text((tx, LY + 146 + j * 25), line, font=F(SANS, 19), fill=INK)

# ---------- second stories ----------
SY = 432
d.line([(36, SY - 8), (W - 36, SY - 8)], fill=INK, width=2)
cx0, cx1 = 36, 500
d.rectangle([cx0, SY, cx1, SY + 176], outline=INK, width=2)
d.rectangle([cx0, SY, cx1, SY + 36], fill=BLUE)
d.text((cx0 + 14, SY + 7), "CYCLONE AKVAN", font=F(SANS_B, 24), fill=WHITE)
gx0, gy0 = cx0 + 24, SY + 50
d.rectangle([gx0, gy0, gx0 + 140, gy0 + 110], fill=(38, 92, 150))
for r in range(48, 8, -10):
    d.arc([gx0 + 70 - r, gy0 + 55 - r, gx0 + 70 + r, gy0 + 55 + r],
          start=20, end=300, fill=WHITE, width=4)
d.polygon([(gx0 + 110, gy0 + 8), (gx0 + 140, gy0 + 28), (gx0 + 140, gy0 + 110),
           (gx0 + 98, gy0 + 110)], fill=(214, 186, 120))
d.text((cx0 + 180, SY + 50), "Storm slams India's", font=F(SANS_B, 21), fill=INK)
d.text((cx0 + 180, SY + 78), "east coast at Gopalpur", font=F(SANS_B, 21), fill=INK)
d.text((cx0 + 180, SY + 112), "300,000 moved to safety", font=F(SANS, 19), fill=INK)
d.text((cx0 + 180, SY + 138), "in Odisha; 28 trains off", font=F(SANS, 19), fill=INK)
mx0, mx1 = 524, W - 36
d.rectangle([mx0, SY, mx1, SY + 176], outline=INK, width=2)
d.rectangle([mx0, SY, mx1, SY + 36], fill=RED)
d.text((mx0 + 14, SY + 7), "AI SELLOFF ROCKS MARKETS", font=F(SANS_B, 24), fill=WHITE)
gx0, gy0 = mx0 + 24, SY + 50
d.rectangle([gx0, gy0, gx0 + 140, gy0 + 110], fill=(30, 30, 34))
pts = [(6, 16), (36, 24), (62, 20), (88, 48), (110, 72), (134, 100)]
d.line([(gx0 + x, gy0 + y) for x, y in pts], fill=(255, 92, 92), width=4)
d.polygon([(gx0 + 134, gy0 + 100), (gx0 + 122, gy0 + 96), (gx0 + 130, gy0 + 86)],
          fill=(255, 92, 92))
d.text((mx0 + 180, SY + 50), "Nvidia −14% in a day as", font=F(SANS_B, 20), fill=INK)
d.text((mx0 + 180, SY + 78), "SEC probes its accounts", font=F(SANS_B, 20), fill=INK)
d.text((mx0 + 180, SY + 112), "Nikkei −5% · Nasdaq −5.3%", font=F(SANS, 19), fill=INK)
d.text((mx0 + 180, SY + 138), "Bitcoin under $60,000", font=F(SANS, 19), fill=INK)

# ---------- regional grid ----------
GY = 624
d.line([(36, GY - 10), (W - 36, GY - 10)], fill=INK, width=2)
COLS = [
    ("EUROPE", [
        "UK–EU deal: food, youth, carbon",
        "COP31 stuck; 'fossil fuels' cut",
        "Estonia shuts Russia border",
        "Cost-of-living strike, 25+ lands",
        "Ukraine hits Dorogobuzh plant",
        "Merz: 'no new Yalta'",
    ]),
    ("ASIA-PACIFIC", [
        "ICJ rules against Myanmar",
        "Cyclone Xavier Cat 4, Pacific",
        "Sri Lanka hikes rates to 9%",
        "IAEA: N. Korea uranium",
        "Shenzhen pact omits Ukraine",
        "Gold slides toward $3,500",
    ]),
    ("MIDDLE EAST", [
        "Houthi missiles reach Riyadh",
        "Tankers burn in Hormuz Strait",
        "Iraq moves on Jurf al-Sakhar",
        "Israeli operation in Gaza",
    ]),
    ("AMERICAS", [
        "Senate blocks Iran curb 51–48",
        "Trump: no Iran call till 2027",
        "Haiti police retake Martissant",
        "M5.0 earthquake in California",
        "Florida floods: St. Johns up",
        "Senate passes permitting bill",
    ]),
    ("AFRICA & WORLD", [
        "Drone hits Sudan gold mine",
        "Ethiopia–Eritrea shelling",
        "IMF: debt near 100% of GDP",
        "Paraná floods: evacuations",
        "Anthropic pop fades post-debut",
    ]),
]
col_w = (W - 72) // 3
y = GY
for row in [COLS[:3], COLS[3:]]:
    x = 36
    for name, items in row:
        d.rectangle([x, y, x + col_w - 12, y + 28], fill=INK)
        d.text((x + 10, y + 4), name, font=F(SANS_B, 18), fill=WHITE)
        iy = y + 36
        for it in items:
            d.ellipse([x + 2, iy + 6, x + 9, iy + 13], fill=RED)
            d.text((x + 16, iy), it, font=F(SANS, 16), fill=INK)
            iy += 22
        x += col_w
    y += 168

# ---------- footer ----------
d.line([(36, 968), (W - 36, 968)], fill=INK, width=2)
d.text((W // 2, 978), "Compiled from Friday's reporting — Kyiv · Odisha · Antalya · Brussels · Riyadh · Washington · markets worldwide",
       font=F(SANS, 15), fill=GREY, anchor="ma")

img.save("/home/hatch/workspace/bounties/news-image/repo/entry.png")
print("saved entry.png", img.size)
