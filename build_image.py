#!/usr/bin/env python3
"""Build entry.png v2 — 'The World in One Day', 17 November 2026.

Dense front page in the winning pattern: masthead + dotted world map with
eight numbered pins + 'By the numbers' strip + six lead story cards + 27
one-line briefs in three columns = 33 real, verified stories from the day.
All facts checked against 17 Nov 2026 editions (Reuters, AP, BBC, CNN,
Al Jazeera, NYT, Algenom daily briefing). Deterministic: same input ->
same bytes.
"""
import json
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
NAVY = (22, 35, 63)
INK = (46, 42, 36)
MUTED = (107, 101, 88)
RED = (192, 57, 43)
AMBER = (232, 163, 61)
CARD = (255, 255, 255)
BORDER = (220, 213, 194)
MAP_FILL = (158, 172, 182)
MAP_LINE = (247, 242, 231)
GRAT = (216, 210, 194)
LIGHT_BLUE = (159, 176, 200)

FDIR = "/usr/share/fonts/truetype/liberation/"


def F(name, size):
    return ImageFont.truetype(FDIR + name, size)


GEO = "/tmp/countries.geo.json"

C_EUROPE = (31, 78, 121)
C_MIDEAST = (140, 47, 57)
C_DIPLOMACY = (156, 107, 0)
C_MIGRATION = (91, 74, 138)
C_ASIAPAC = (46, 107, 79)
C_BUSINESS = (51, 51, 51)
C_AMERICAS = (122, 72, 20)
C_HEALTH = (150, 40, 90)
C_CLIMATE = (20, 110, 110)
C_CULTURE = (150, 90, 20)
C_SPORT = (60, 90, 160)
C_AFRICA = (110, 80, 30)

# (number, tag, tag_color, headline, summary, lon, lat, label, label_dx, label_dy)
# lon/lat/label only used for the 8 map pins (stories 1-8).
LEADS = [
    (1, "EUROPE", C_EUROPE,
     "Kerch Bridge partly collapses in second strike",
     "Second strike in two days drops the road arch; Russia hits Kyiv's bridges in reply.",
     36.5, 45.3, "KERCH", -58, -16),
    (2, "MIDDLE EAST", C_MIDEAST,
     "Tankers mined near Hormuz; Gulf strikes spread",
     "Two tankers hit mines and burn; Iran's drones at a US base in Bahrain are intercepted.",
     56.5, 26.5, "HORMUZ", 14, 10),
    (3, "DIPLOMACY", C_DIPLOMACY,
     "Xi, Trump and Putin to meet in Shenzhen",
     "China confirms the first three-way summit, Thu 19 Nov on the APEC sidelines.",
     114.1, 22.5, "SHENZHEN", -78, -16),
    (4, "ASIA-PACIFIC", C_ASIAPAC,
     "Trump lands in Manila for ASEAN and Quad",
     "Trump lands for ASEAN and the Quad; critical-minerals deals signed amid protests.",
     121.0, 14.6, "MANILA", 14, 12),
    (5, "ASIA-PACIFIC", C_ASIAPAC,
     "Japan scrambles jets over Russian planes",
     "Tokyo launches fighters and protests after two suspected Russian jets enter its airspace.",
     140.5, 36.0, "TOKYO", 12, -16),
    (6, "BUSINESS", C_BUSINESS,
     "Nvidia tops earnings amid Huang exit drama",
     "Bumper quarterly results land as ex-CEO Huang exits; the firm says it won't reinstate him.",
     -122.0, 37.3, "SANTA CLARA", -96, 12),
    (7, "MIGRATION", C_MIGRATION,
     "Five nations plan Rwanda return hub for rejected asylum seekers", "",
     30.5, -1.9, "KIGALI", -62, 12),
    (8, "MIDDLE EAST", C_MIDEAST,
     "Houthis close in on Aden as Yemeni forces fall back", "",
     45.0, 12.8, "ADEN", 14, 10),
]

# (number, tag, tag_color, headline) — one-line briefs, reading order row-major
BRIEFS = [
    (7, "MIGRATION", C_MIGRATION,
     "Five nations plan Rwanda return hub for rejected asylum seekers"),
    (8, "MIDDLE EAST", C_MIDEAST,
     "Houthis close in on Aden as Yemeni forces fall back"),
    (9, "BUSINESS", C_BUSINESS,
     "Banking glitch hits JPMorgan and Zelle; thousands locked out"),
    (10, "EUROPE", C_EUROPE,
     "Iran-linked assassination plot foiled; five arrested"),
    (11, "HEALTH", C_HEALTH,
     "US loses measles-free status after 26 years"),
    (12, "ASIA-PACIFIC", C_ASIAPAC,
     "Russian military plane crashes in Siberia; all 19 killed"),
    (13, "MIDDLE EAST", C_MIDEAST,
     "UK sanctions eight Israeli firms over West Bank building"),
    (14, "CLIMATE", C_CLIMATE,
     "COP31 draft climate deal stalls over IPCC report"),
    (15, "AMERICAS", C_AMERICAS,
     "Fed's Lisa Cook refuses White House hearing"),
    (16, "EUROPE", C_EUROPE,
     "France to represent EU in Ukraine talks"),
    (17, "BUSINESS", C_BUSINESS,
     "AI chip curbs rattle markets as US squeezes Beijing"),
    (18, "AMERICAS", C_AMERICAS,
     "US indicts Irishman over $60m damage to C-130H jet"),
    (19, "ASIA-PACIFIC", C_ASIAPAC,
     "China and Canada widen tariff relief after Carney-Xi talks"),
    (20, "EUROPE", C_EUROPE,
     "NATO cancels 2027 summit in Albania; Tirana offers 2028"),
    (21, "EUROPE", C_EUROPE,
     "100,000+ march in France over pay"),
    (22, "MIDDLE EAST", C_MIDEAST,
     "Settler attack kills Palestinian woman, 72, in West Bank"),
    (23, "CULTURE", C_CULTURE,
     "Raye leads Grammy nominations with 11"),
    (24, "CULTURE", C_CULTURE,
     "Robert Pattinson named the next James Bond"),
    (25, "AFRICA", C_AFRICA,
     "At least 17 killed in two shootings in South Africa"),
    (26, "AMERICAS", C_AMERICAS,
     "FAA: new AI system did not cause Friday's ground stop"),
    (27, "AFRICA", C_AFRICA,
     "Congo Ebola outbreak spreads at record pace"),
    (28, "ASIA-PACIFIC", C_ASIAPAC,
     "Phuket fire kills 11, injures 16"),
    (29, "BUSINESS", C_BUSINESS,
     "Deutsche Bank shares sink after whistleblower leaks"),
    (30, "AMERICAS", C_AMERICAS,
     "Zelensky urges SpaceX to lift Starshield limits"),
    (31, "MIDDLE EAST", C_MIDEAST,
     "Israel's parliament elects Matan Kahana as speaker"),
    (32, "SPORT", C_SPORT,
     "India's footballers beat Pakistan to win SAFF final"),
    (33, "ASIA-PACIFIC", C_ASIAPAC,
     "Imran Khan says he fears dying in jail"),
]

STATS = [("1,441", "drones Russia says it downed"),
         ("19", "killed in Siberian plane crash"),
         ("100,000+", "march in France over pay"),
         ("5,400", "US measles cases, 10 deaths")]

SOURCES = ("Sources: Reuters  ·  AP  ·  BBC  ·  CNN  ·  Al Jazeera  ·  NYT  —  "
           "All events of 17 November 2026")

# Map panel geometry (equirectangular, lat 83..-58)
MAP_X0, MAP_X1 = 24, 1000
MAP_Y0, MAP_Y1 = 134, 284
LAT_TOP, LAT_BOT = 83.0, -58.0

# Lead grid geometry
COL_X = [24, 360, 696]
COL_W = 304
LEAD_Y = [356, 480]
LEAD_H = 116
BRIEF_Y0 = 632
BRIEF_PITCH = 40


def lonlat_to_xy(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (MAP_Y1 - MAP_Y0)
    return x, y


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def wrap_balanced(draw, text, font, max_w):
    """Wrap to at most 2 lines, splitting so the two lines are as equal
    in width as possible (no orphaned last word)."""
    if draw.textlength(text, font=font) <= max_w:
        return [text]
    words = text.split()
    best = None
    for i in range(1, len(words)):
        l1 = " ".join(words[:i])
        l2 = " ".join(words[i:])
        if (draw.textlength(l1, font=font) <= max_w
                and draw.textlength(l2, font=font) <= max_w):
            diff = abs(draw.textlength(l1, font=font)
                       - draw.textlength(l2, font=font))
            if best is None or diff < best[0]:
                best = (diff, [l1, l2])
    if best:
        return best[1]
    return wrap(draw, text, font, max_w)


def label_with_halo(d, x, y, text, font, fill):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        d.text((x + dx, y + dy), text, font=font, fill=(255, 255, 255))
    d.text((x, y), text, font=font, fill=fill)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    warnings = []

    # ---- Masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((24, 14), "THE WORLD IN ONE DAY",
           font=F("LiberationSans-Bold.ttf", 46), fill=(255, 255, 255))
    d.text((24, 68), "33 STORIES FROM SIX CONTINENTS",
           font=F("LiberationSans-Bold.ttf", 15), fill=LIGHT_BLUE)
    d.text((1000, 16), "TUESDAY", font=F("LiberationSans-Bold.ttf", 16),
           fill=AMBER, anchor="ra")
    d.text((1000, 38), "17 NOVEMBER 2026", font=F("LiberationSans-Bold.ttf", 22),
           fill=AMBER, anchor="ra")
    d.rectangle([0, 96, W, 101], fill=RED)

    # ---- Map panel ----
    d.text((24, 110), "WHERE IT HAPPENED  —  EIGHT FLASHPOINTS",
           font=F("LiberationSans-Bold.ttf", 14), fill=NAVY)
    geo = json.load(open(GEO))
    for lon in range(-150, 181, 30):
        x, _ = lonlat_to_xy(lon, 0)
        d.line([(x, MAP_Y0), (x, MAP_Y1)], fill=GRAT, width=1)
    for lat in range(-60, 84, 30):
        _, y = lonlat_to_xy(0, lat)
        d.line([(MAP_X0, y), (MAP_X1, y)], fill=GRAT, width=1)
    for feat in geo["features"]:
        geom = feat["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"]]
        elif geom["type"] == "MultiPolygon":
            polys = geom["coordinates"]
        for poly in polys:
            for ring in poly:
                pts = [lonlat_to_xy(lon, lat) for lon, lat in ring
                       if lat >= -60]
                if len(pts) >= 3:
                    d.polygon(pts, fill=MAP_FILL, outline=MAP_LINE)
    pin_font = F("LiberationSans-Bold.ttf", 13)
    lab_font = F("LiberationSans-Bold.ttf", 11)
    for num, tag, color, head, summ, lon, lat, label, ldx, ldy in LEADS[:8]:
        x, y = lonlat_to_xy(lon, lat)
        d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((x, y - 1), str(num), font=pin_font, fill=(255, 255, 255),
               anchor="mm")
        label_with_halo(d, x + ldx, y + ldy, label, lab_font, NAVY)

    # ---- By the numbers strip ----
    d.rectangle([0, 292, W, 324], fill=NAVY)
    num_f = F("LiberationSans-Bold.ttf", 20)
    lab_f = F("LiberationSans-Regular.ttf", 13)
    seg = W // 4
    for i, (num, lab) in enumerate(STATS):
        nw = d.textlength(num, font=num_f)
        lw = d.textlength(lab, font=lab_f)
        total = nw + 8 + lw
        sx = seg * i + (seg - total) / 2
        d.text((sx, 308), num, font=num_f, fill=AMBER, anchor="lm")
        d.text((sx + nw + 8, 308), lab, font=lab_f, fill=(255, 255, 255),
               anchor="lm")

    # ---- Lead story cards: 3 cols x 2 rows ----
    d.text((24, 334), "TOP STORIES",
           font=F("LiberationSans-Bold.ttf", 15), fill=NAVY)
    for i, (num, tag, color, head, summ, *_) in enumerate(LEADS[:6]):
        cx = COL_X[i % 3]
        cy = LEAD_Y[i // 3]
        d.rectangle([cx, cy, cx + COL_W, cy + LEAD_H], fill=CARD,
                    outline=BORDER, width=1)
        d.rectangle([cx, cy, cx + 5, cy + LEAD_H], fill=color)
        chip_cx, chip_cy = cx + 28, cy + 22
        d.ellipse([chip_cx - 12, chip_cy - 12, chip_cx + 12, chip_cy + 12],
                  fill=RED)
        d.text((chip_cx, chip_cy - 1), str(num),
               font=F("LiberationSans-Bold.ttf", 14), fill=(255, 255, 255),
               anchor="mm")
        d.text((cx + 46, chip_cy), tag, font=F("LiberationSans-Bold.ttf", 13),
               fill=color, anchor="lm")
        hl_font = F("LiberationSans-Bold.ttf", 17)
        lines = wrap_balanced(d, head, hl_font, COL_W - 28)
        if len(lines) > 2:
            warnings.append(f"lead {num}: headline wraps to {len(lines)} lines")
        hy = cy + 40
        for ln in lines[:2]:
            d.text((cx + 14, hy), ln, font=hl_font, fill=NAVY)
            hy += 19
        sm_font = F("LiberationSans-Regular.ttf", 12)
        slines = wrap(d, summ, sm_font, COL_W - 28)
        if len(slines) > 2:
            warnings.append(f"lead {num}: summary wraps to {len(slines)} lines")
        sy = hy + 3
        for ln in slines[:2]:
            d.text((cx + 14, sy), ln, font=sm_font, fill=INK)
            sy += 15
        if sy > cy + LEAD_H - 4:
            warnings.append(f"lead {num}: text overflows card (bottom {sy})")

    # ---- Briefs: 3 cols x 9 rows ----
    d.text((24, 606), "MORE FROM THE DAY",
           font=F("LiberationSans-Bold.ttf", 15), fill=NAVY)
    d.text((1000, 606), "27 MORE STORIES",
           font=F("LiberationSans-Bold.ttf", 13), fill=RED, anchor="ra")
    tag_f = F("LiberationSans-Bold.ttf", 10)
    bf_font = F("LiberationSans-Bold.ttf", 13)
    for i, (num, tag, color, head) in enumerate(BRIEFS):
        col, row = i % 3, i // 3
        bx = COL_X[col]
        by = BRIEF_Y0 + row * BRIEF_PITCH
        # tag on first line, headline wraps around it then full width
        tag_w = d.textlength(tag, font=tag_f)
        d.text((bx, by + 1), tag, font=tag_f, fill=color)
        first_w = COL_W - tag_w - 8
        lines = wrap(d, head, bf_font, first_w)
        if len(lines) > 1:
            rest = " ".join(lines[1:])
            rest_lines = wrap(d, rest, bf_font, COL_W)
            lines = [lines[0]] + rest_lines
        if len(lines) > 2:
            warnings.append(f"brief {num}: headline wraps to {len(lines)} lines")
        ly = by
        for j, ln in enumerate(lines[:2]):
            lx = bx + tag_w + 8 if j == 0 else bx
            d.text((lx, ly), ln, font=bf_font, fill=NAVY)
            ly += 16
        if ly > by + BRIEF_PITCH - 4:
            warnings.append(f"brief {num}: text overflows row (bottom {ly})")
        # hairline divider under each brief except last row
        if row < 8:
            d.line([(bx, by + 34), (bx + COL_W, by + 34)], fill=BORDER, width=1)

    # ---- Footer ----
    d.line([(24, 992), (1000, 992)], fill=BORDER, width=1)
    d.text((24, 1000), SOURCES, font=F("LiberationSans-Regular.ttf", 12),
           fill=MUTED)

    out = "/home/hatch/workspace/makefun-news-image-20261117/entry.png"
    img.save(out, "PNG", optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")
    print("stories:", len(LEADS[:6]) + len(BRIEFS))
    print("warnings:", warnings if warnings else "none")


if __name__ == "__main__":
    main()
