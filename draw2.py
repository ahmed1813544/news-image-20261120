#!/usr/bin/env python3
"""Entry image v2 for make.fun news-image-20261120, modelled on the
current #1 entry's front page (35 stories, 7 regions, every story
dated Friday 20 November 2026) and drawn to beat it on polish:
crisper scenes, sourced captions, a date-check box, zero overflow.

All stories are Friday 20 November 2026's, cross-checked against
the day's reporting. Two famous items are deliberately left out as
19 November news (the World Court's Myanmar ruling and the
Shenzhen declaration) and the date-check box says so.
"""

import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 236)
INK = (20, 22, 27)
RED = (176, 30, 40)
BLUE = (26, 74, 132)
TEAL = (14, 116, 128)
GREEN = (38, 110, 62)
ORANGE = (196, 108, 20)
PURPLE = (96, 62, 150)
GREY = (96, 96, 100)
WHITE = (255, 255, 255)
DARKRED = (122, 20, 28)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def tw(text, font):
    return d.textlength(text, font=font)


def fit(text, path, size, maxw, min_size=9):
    """Shrink the font until the text fits maxw; return (font, text)."""
    s = size
    while s > min_size and tw(text, F(path, s)) > maxw:
        s -= 1
    return F(path, s)


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


# ---------- kicker + date ----------
d.text((30, 10), "THE WORLD IN ONE DAY", font=F(SANS_B, 17), fill=RED)
kt = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
d.text((W - 30, 12), kt, font=F(SANS_B, 13), fill=GREY, anchor="ra")
d.line([(30, 34), (W - 30, 34)], fill=INK, width=2)
d.text((W // 2, 44), "Friday 20 November 2026",
       font=fit("Friday 20 November 2026", SERIF_B, 82, W - 56),
       fill=INK, anchor="ma")
deck = ("Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India · "
        "An AI sell-off sinks Asia's markets · UK and EU seal a deal")
d.text((W // 2, 140), deck, font=fit(deck, SERIF_I, 19, W - 60), fill=INK, anchor="ma")

# ---------- stat strip ----------
STATS = [
    ("3", "bridges over the Dnipro\ndamaged in Kyiv"),
    ("300,000+", "people moved to shelters\nbefore Akvan"),
    ("−6.2%", "Taiwan's share index,\nFriday's close"),
    ("100,000", "youth visas a year in\nthe UK–EU deal"),
    ("2.3%", "Japan's consumer inflation\nin October"),
    ("118", "runs by Glenn Phillips\nagainst India"),
]
sy = 168
d.line([(30, sy), (W - 30, sy)], fill=INK, width=1)
cell = (W - 60) // 6
for i, (num, cap) in enumerate(STATS):
    x = 30 + i * cell
    if i:
        d.line([(x, sy + 4), (x, sy + 52)], fill=GREY, width=1)
    d.text((x + 8, sy + 2), num, font=F(SERIF_B, 29), fill=RED if i in (0, 2) else INK)
    for j, ln in enumerate(cap.split("\n")):
        d.text((x + 8, sy + 38 + j * 14), ln, font=F(SANS, 11), fill=INK)
d.line([(30, sy + 68), (W - 30, sy + 68)], fill=INK, width=1)

# ---------- region tally ----------
REGIONS = [("Europe", 8, RED), ("Asia", 8, BLUE), ("Middle East", 3, ORANGE),
           ("Africa", 5, GREEN), ("Americas", 4, PURPLE), ("Oceania", 3, TEAL),
           ("Global", 4, GREY)]
ry = sy + 76
x = 30
total = sum(n for _, n, _ in REGIONS)
for name, n, col in REGIONS:
    wseg = (W - 60) * n // total
    d.rectangle([x, ry, x + wseg - 2, ry + 20], fill=col)
    label = f"{name} {n}"
    d.text((x + wseg // 2, ry + 4), label,
           font=fit(label, SANS_B, 12, wseg - 8), fill=WHITE, anchor="ma")
    x += wseg

# ---------- lead panels ----------
LY = 272
PW = (W - 60 - 24) // 3
PH = 118


def tag(x, y, text):
    w_ = int(tw(text, F(SANS, 10))) + 12
    d.rectangle([x, y, x + w_, y + 16], fill=(12, 12, 14))
    d.text((x + 6, y + 3), text, font=F(SANS, 10), fill=WHITE)


def lead_caption(x, num, kicker, headline, body):
    cy = LY + PH + 10
    d.ellipse([x, cy, x + 20, cy + 20], fill=RED)
    d.text((x + 10, cy + 3), str(num), font=F(SANS_B, 12), fill=WHITE, anchor="ma")
    d.text((x + 27, cy + 3), kicker, font=F(SANS_B, 12), fill=INK)
    hy = cy + 26
    for ln in wrap(headline, F(SERIF_B, 18), PW - 4):
        d.text((x, hy), ln, font=F(SERIF_B, 18), fill=INK)
        hy += 22
    by = hy + 2
    for ln in wrap(body, F(SANS, 12), PW - 4):
        d.text((x, by), ln, font=F(SANS, 12), fill=GREY if False else INK)
        by += 15


# 1 — Kyiv
x1 = 30
d.rectangle([x1, LY, x1 + PW, LY + PH], fill=(13, 19, 38))
rnd = random.Random(7)
for _ in range(34):
    d.point((rnd.randint(x1 + 3, x1 + PW - 3), rnd.randint(LY + 3, LY + 52)),
            fill=(205, 212, 228))
# dashed missile trails
for (ax, ay, bx, by) in [(36, 8, 120, 74), (120, 2, 196, 78), (216, 10, 268, 72)]:
    steps = 9
    for s in range(0, steps, 2):
        t0, t1 = s / steps, (s + 1) / steps
        d.line([(x1 + ax + (bx - ax) * t0, LY + ay + (by - ay) * t0),
                (x1 + ax + (bx - ax) * t1, LY + ay + (by - ay) * t1)],
               fill=(255, 178, 92), width=2)
# skyline + river + bridges
d.rectangle([x1, LY + 76, x1 + PW, LY + 92], fill=(7, 9, 16))
d.rectangle([x1, LY + 92, x1 + PW, LY + PH], fill=(22, 48, 92))
for cx in (52, 156, 260):
    d.line([(x1 + cx - 40, LY + 88), (x1 + cx + 40, LY + 88)], fill=(214, 219, 226), width=5)
    d.line([(x1 + cx - 34, LY + 88), (x1 + cx - 34, LY + 106)], fill=(214, 219, 226), width=3)
    d.line([(x1 + cx + 34, LY + 88), (x1 + cx + 34, LY + 106)], fill=(214, 219, 226), width=3)
for _ in range(26):
    d.point((rnd.randint(x1 + 4, x1 + PW - 4), rnd.randint(LY + 78, LY + 90)),
            fill=(255, 214, 120))
for fx in (108, 226):
    d.ellipse([x1 + fx, LY + 62, x1 + fx + 22, LY + 80], fill=(255, 138, 54))
    d.ellipse([x1 + fx + 6, LY + 67, x1 + fx + 16, LY + 77], fill=(255, 205, 110))
tag(x1 + 6, LY + PH - 22, "Officials' count")
lead_caption(x1, 1, "KYIV, UKRAINE · WAR",
             "Russian missiles hit three Kyiv bridges",
             "An overnight barrage of about 110 missiles and 400 drones "
             "killed at least eight people across Ukraine and cut power "
             "and water in the capital. (Kyiv Independent, BBC)")

# 2 — Cyclone Akvan
x2 = 30 + PW + 12
d.rectangle([x2, LY, x2 + PW, LY + PH], fill=(24, 84, 138))
for r in range(46, 6, -10):
    d.arc([x2 + 108 - r, LY + 56 - r, x2 + 108 + r, LY + 56 + r],
          start=15, end=305, fill=WHITE, width=4)
d.polygon([(x2 + 218, LY), (x2 + PW, LY), (x2 + PW, LY + PH), (x2 + 196, LY + PH)],
          fill=(216, 188, 122))
d.rectangle([x2 + 176, LY + 12, x2 + 296, LY + 34], fill=(12, 12, 14))
d.text((x2 + 186, LY + 17), "Landfall · 8 am", font=F(SANS_B, 13), fill=WHITE)
tag(x2 + 6, LY + PH - 22, "Weather office")
lead_caption(x2, 2, "ODISHA, INDIA · CYCLONE",
             "Cyclone Akvan comes ashore in eastern India",
             "The storm crossed the coast near Gopalpur from about 8 am "
             "after more than 300,000 people were moved to shelters. "
             "No deaths were reported. (IMD, Deccan Herald)")

# 3 — AI sell-off
x3 = 30 + 2 * (PW + 12)
d.rectangle([x3, LY, x3 + PW, LY + PH], fill=DARKRED)
d.text((x3 + 12, LY + 8), "AI SELL-OFF", font=F(SANS_B, 21), fill=WHITE)
d.text((x3 + 12, LY + 36), "Asia, Friday's close", font=F(SANS, 12), fill=(240, 200, 200))
pts = [(12, 66), (52, 72), (88, 70), (118, 88), (146, 106)]
d.line([(x3 + px, LY + py) for px, py in pts], fill=(255, 120, 120), width=3)
d.polygon([(x3 + 146, LY + 106), (x3 + 134, LY + 102), (x3 + 142, LY + 92)],
          fill=(255, 120, 120))
rows = [("Taipei", "−6.2%"), ("Seoul", "−5.2%"), ("Tokyo", "−5.1%"), ("Hong Kong", "−1.9%")]
for j, (city, pct) in enumerate(rows):
    yy = LY + 12 + j * 26
    d.text((x3 + 186, yy), city, font=F(SANS, 13), fill=WHITE)
    d.text((x3 + PW - 10, yy), pct, font=F(SANS_B, 14), fill=(255, 150, 150), anchor="ra")
tag(x3 + 6, LY + PH - 22, "Closing prices")
lead_caption(x3, 3, "TAIPEI · SEOUL · TOKYO · MARKETS",
             "AI sell-off sinks Asia's stock markets",
             "Taiwan's index fell 6.2% to end its worst week since 1991. "
             "Seoul lost 5.2% and Tokyo 5.1% as chipmakers led the slide. "
             "(Al Jazeera, Anadolu)")

# ---------- story cards 4-13 ----------
def art(kind, x, y, w, h):
    if kind == "jack":
        d.rectangle([x, y, x + w, y + h], fill=(24, 52, 116))
        d.line([(x, y), (x + w, y + h)], fill=WHITE, width=7)
        d.line([(x + w, y), (x, y + h)], fill=WHITE, width=7)
        d.line([(x, y), (x + w, y + h)], fill=RED, width=3)
        d.line([(x + w, y), (x, y + h)], fill=RED, width=3)
        d.rectangle([x + w // 2 - 13, y, x + w // 2 + 13, y + h], fill=WHITE)
        d.rectangle([x, y + h // 2 - 9, x + w, y + h // 2 + 9], fill=WHITE)
        d.rectangle([x + w // 2 - 8, y, x + w // 2 + 8, y + h], fill=RED)
        d.rectangle([x, y + h // 2 - 5, x + w, y + h // 2 + 5], fill=RED)
    elif kind == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(168, 205, 228))
        d.ellipse([x + 16, y + 4, x + 58, y + h - 4], fill=BLUE)
        d.polygon([(x + 26, y + 10), (x + 40, y + 8), (x + 36, y + 20), (x + 26, y + 18)], fill=GREEN)
        d.polygon([(x + 38, y + 24), (x + 50, y + 26), (x + 44, y + 34), (x + 36, y + 30)], fill=GREEN)
        d.ellipse([x + w - 58, y + 4, x + w - 16, y + h - 4], outline=INK, width=3)
        d.line([(x + w - 37, y + h // 2), (x + w - 37, y + 10)], fill=INK, width=3)
        d.line([(x + w - 37, y + h // 2), (x + w - 24, y + h // 2 + 6)], fill=INK, width=3)
    elif kind == "poland":
        d.rectangle([x, y, x + w, y + h], fill=(104, 148, 74))
        d.rectangle([x, y, x + w, y + 12], fill=(168, 205, 228))
        d.polygon([(x + 60, y + 26), (x + 118, y + 12), (x + 122, y + 20), (x + 68, y + 36)],
                  fill=(120, 124, 130))
        d.polygon([(x + 118, y + 12), (x + 132, y + 8), (x + 122, y + 20)], fill=RED)
        d.ellipse([x + 128, y + 4, x + 148, y + 22], fill=(255, 150, 60))
    elif kind == "iraq":
        d.rectangle([x, y, x + w, y + h], fill=(226, 198, 140))
        d.rectangle([x + 30, y + 16, x + 108, y + 34], fill=(92, 98, 62))
        d.polygon([(x + 108, y + 22), (x + 128, y + 26), (x + 128, y + 34), (x + 108, y + 34)],
                  fill=(92, 98, 62))
        d.rectangle([x + 44, y + 6, x + 46, y + 16], fill=INK)
        d.polygon([(x + 46, y + 6), (x + 60, y + 8), (x + 46, y + 11)], fill=RED)
        for wx in (48, 96):
            d.ellipse([x + wx, y + 30, x + wx + 14, y + 44], fill=(30, 30, 30))
    elif kind == "italy":
        d.rectangle([x, y, x + w, y + 22], fill=RED)
        d.text(((x + x + w) // 2, y + 4), "SCIOPERO", font=F(SANS_B, 13), fill=WHITE, anchor="ma")
        for i in range(9):
            hx = x + 14 + i * 18
            d.ellipse([hx, y + 28, hx + 9, y + 37], fill=INK)
            d.rectangle([hx + 1, y + 37, hx + 8, y + h], fill=BLUE if i % 2 else GREY)
    elif kind == "japan":
        d.rectangle([x, y, x + w, y + h], fill=WHITE)
        d.ellipse([x + 18, y + 6, x + 52, y + h - 6], fill=RED)
        for i, bh in enumerate((10, 16, 24)):
            d.rectangle([x + 84 + i * 26, y + h - 6 - bh, x + 102 + i * 26, y + h - 6],
                        fill=(150, 150, 154))
        d.line([(x + 80, y + 22), (x + 158, y + 8)], fill=RED, width=3)
    elif kind == "seoul":
        d.rectangle([x, y, x + w, y + h], fill=(214, 208, 192))
        d.polygon([(x + 30, y + 14), (x + w - 30, y + 14), (x + w // 2, y + 2)], fill=INK)
        for i in range(4):
            cx_ = x + 44 + i * 26
            d.rectangle([cx_, y + 16, cx_ + 9, y + h - 10], fill=WHITE, outline=INK)
        d.rectangle([x + 30, y + h - 10, x + w - 30, y + h - 4], fill=INK)
    elif kind == "kenya":
        d.rectangle([x, y, x + w, y + h], fill=(240, 214, 150))
        d.polygon([(x + 70, y + 4), (x + 96, y + h - 6), (x + 44, y + h - 6)], outline=INK, width=3)
        d.line([(x + 58, y + 24), (x + 84, y + 24)], fill=INK, width=2)
        d.line([(x + 52, y + 34), (x + 90, y + 34)], fill=INK, width=2)
        d.ellipse([x + 130, y + 6, x + 152, y + 28], fill=ORANGE)
    elif kind == "bukele":
        d.rectangle([x, y, x + w, y + h], fill=(206, 216, 232))
        d.rectangle([x + 52, y + 20, x + 132, y + h - 4], fill=(90, 96, 104))
        d.rectangle([x + 62, y + 24, x + 122, y + 28], fill=(20, 20, 22))
        d.rectangle([x + 66, y + 2, x + 118, y + 22], fill=WHITE, outline=INK)
        d.line([(x + 76, y + 12), (x + 88, y + 18), (x + 108, y + 6)], fill=GREEN, width=3)
    elif kind == "cricket":
        d.rectangle([x, y, x + w, y + h], fill=(56, 128, 66))
        for i in range(3):
            d.rectangle([x + 40 + i * 8, y + 10, x + 44 + i * 8, y + h - 8], fill=(232, 214, 160))
        d.polygon([(x + 108, y + 8), (x + 118, y + 6), (x + 128, y + h - 10), (x + 118, y + h - 8)],
                  fill=(196, 160, 92))
        d.ellipse([x + 146, y + 16, x + 160, y + 30], fill=RED)


CARDS = [
    ("UK–EU DEAL", RED, "jack", "Agreed · Reuters", "BRUSSELS · DIPLOMACY",
     "UK and EU seal a “reset” deal", "Food trade, youth visas, carbon link."),
    ("COP31: NO DEAL", BLUE, "cop31", "Ongoing · UN News", "ANTALYA · CLIMATE",
     "COP31 reaches its last day with no deal", "The draft text leaves out fossil fuels."),
    ("POLAND: MISSILE", INK, "poland", "Minister says · Reuters", "EASTERN POLAND · SECURITY",
     "Russian cruise missile lands in Poland", "It fell in a field; two airports paused."),
    ("IRAQ: ARMY IN", GREEN, "iraq", "Witnessed · Reuters", "CENTRAL IRAQ · SECURITY",
     "Iraqi army enters a militia stronghold", "Troops deploy to Jurf al-Sakhar."),
    ("ITALY: STRIKE", RED, "italy", "Reported · Reuters", "ITALY · LABOUR",
     "General strike over Italy's budget", "Workers and students march."),
    ("JAPAN: +2.3%", INK, "japan", "Official data · Reuters", "TOKYO · ECONOMY",
     "Japan's inflation picks up to 2.3%", "A December rate rise stays in view."),
    ("SEOUL: IMPEACH", BLUE, "seoul", "Party decision · Korea Herald", "SEOUL · POLITICS",
     "Korea's ruling party to impeach top judge", "It follows an overturned conviction."),
    ("KENYA: OIL", ORANGE, "kenya", "Ceremony held · allAfrica", "TURKANA, KENYA · ENERGY",
     "Kenya starts drilling its first oil well", "First crude is due on 1 December."),
    ("BUKELE: 3RD BID", PURPLE, "bukele", "Filed · AP", "SAN SALVADOR · POLITICS",
     "Bukele files to run for a third term", "The vote is on 28 February 2027."),
    ("PHILLIPS: 118", GREEN, "cricket", "Scorecard · ICC", "WELLINGTON · CRICKET",
     "Phillips hits 118 against India", "Hundreds v India in all three formats."),
]

CW = 184
CY1 = 548
for idx, (banner, col, kind, srctag, meta, head, summ) in enumerate(CARDS):
    row, cidx = divmod(idx, 5)
    x = 30 + cidx * (CW + 10)
    y = CY1 + row * 156
    d.rectangle([x, y, x + CW, y + 24], fill=col)
    d.text((x + 8, y + 5), banner, font=fit(banner, SANS_B, 14, CW - 16), fill=WHITE)
    art(kind, x, y + 24, CW, 40)
    tw_ = int(tw(srctag, F(SANS, 9))) + 10
    d.rectangle([x, y + 52, x + tw_, y + 66], fill=(12, 12, 14))
    d.text((x + 5, y + 55), srctag, font=F(SANS, 9), fill=WHITE)
    my = y + 72
    d.ellipse([x, my, x + 15, my + 15], fill=RED)
    d.text((x + 7, my + 2), str(idx + 4), font=F(SANS_B, 9), fill=WHITE, anchor="ma")
    d.text((x + 20, my + 2), meta, font=fit(meta, SANS_B, 10, CW - 22), fill=INK)
    hy = my + 19
    for ln in wrap(head, F(SERIF_B, 14), CW - 2)[:2]:
        d.text((x, hy), ln, font=F(SERIF_B, 14), fill=INK)
        hy += 17
    for ln in wrap(summ, F(SANS, 11), CW - 2)[:2]:
        d.text((x, hy + 1), ln, font=F(SANS, 11), fill=INK)
        hy += 14

# ---------- date check strip ----------
DY = 866
d.rectangle([30, DY, W - 30, DY + 22], outline=RED, width=1)
dcheck = ("DATE CHECK — Left out as 19 November news: the World Court's Myanmar ruling · "
          "the Shenzhen declaration · Tonga's drought emergency · Not yet happened: a final COP31 text")
d.text((42, DY + 5), dcheck, font=fit(dcheck, SANS, 11, W - 84), fill=RED)

# ---------- also on Friday: 22 more stories ----------
HY = DY + 34
d.text((30, HY), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES", font=F(SANS_B, 14), fill=INK)
d.text((W - 30, HY + 2), "Sources named beside each story · Original drawings",
       font=F(SANS, 10), fill=GREY, anchor="ra")
MORE = [
    "Lviv: railway-station strike kills two (BBC)",
    "Moscow decries Estonia border closure (Reuters)",
    "Berlin pupils strike over military service (Al Jazeera)",
    "London general: UK runs cyber attacks (Sky News)",
    "Beijing holds loan rates, 18th month (Xinhua)",
    "Tokyo: SoftBank falls 14% in a day (Al Jazeera)",
    "Seoul: Kospi ends week 7.9% lower (Anadolu)",
    "Ganjam: 209 mm rain as Akvan crosses (PTI)",
    "Lebanon: Israeli strikes hit south (Anadolu)",
    "Yemen: gunmen fire on a cargo ship (UKMTO)",
    "Abuja court bars Tinubu evidence (Channels TV)",
    "Kampala: Ebola rally ban enforced (allAfrica)",
    "Malawi fuel crisis: night queues (Al Jazeera)",
    "AfDB: 22 states in debt distress (allAfrica)",
    "Las Vegas: Russell tops wet practice (Autosport)",
    "New York: Nasdaq futures −1.6% (24/7 Wall St)",
    "Washington: Democrats query law firm (Al Jazeera)",
    "Wellington: Nicholls 175 in stand of 216 (ICC)",
    "Sydney shares fall 1.6% in sell-off (Reuters)",
    "Antalya: Panama bids to cap oil output (Anadolu)",
    "Antalya: EU calls draft unacceptable (RTÉ)",
    "Turin: ATP backs $350m player-pay plan (Anadolu)",
]
cols = [MORE[:8], MORE[8:15], MORE[15:]]
for ci, colitems in enumerate(cols):
    x = 30 + ci * 327
    for j, item in enumerate(colitems):
        yy = HY + 22 + j * 12
        num = 14 + sum(len(c) for c in cols[:ci]) + j
        d.text((x, yy), str(num), font=F(SANS_B, 10), fill=RED)
        d.text((x + 22, yy), item, font=fit(item, SANS, 10, 300), fill=INK)

img.save("/home/hatch/workspace/bounties/news-image/repo/entry.png")
print("saved entry.png", img.size)
