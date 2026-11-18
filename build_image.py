#!/usr/bin/env python3
"""Build entry.png — 'The World in One Day', 17 November 2026.

Atlas-style board: masthead + dotted world map with numbered pins + six
story cards + 'also in brief' ticker. All facts verified against 17 Nov 2026
news editions (Al Jazeera, Reuters, AP, BBC, CNN, NYT via Algenom /
Just Security Early Edition / FeedCast / TFI roundups).
Deterministic: same input -> same bytes.
"""
import json
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

# (number, tag, tag_color, headline, summary, lon, lat, label, label_dx, label_dy)
STORIES = [
    (1, "EUROPE", (31, 78, 121),
     "Ukraine hits Crimea bridge again",
     "Kyiv strikes the Kerch Bridge a second straight day as Russia hits river crossings in Kyiv; traffic on the bridge was suspended.",
     36.5, 45.3, "KERCH", -62, -20),
    (2, "MIDDLE EAST", (140, 47, 57),
     "Tankers hit by mines near Hormuz",
     "Two tankers hit mines and burned south of the strait on Monday; Iran fired drones at a U.S. radar base in Bahrain on Tuesday \u2014 all intercepted, no casualties.",
     56.5, 26.5, "HORMUZ", 18, 8),
    (3, "DIPLOMACY", (156, 107, 0),
     "Xi, Trump and Putin to meet in Shenzhen",
     "China confirms the first three-way summit, Thu 19 Nov on the APEC sidelines, on peace and nuclear risks.",
     114.1, 22.5, "SHENZHEN", -30, 18),
    (4, "MIGRATION", (91, 74, 138),
     "Five nations plan Rwanda return hub",
     "Germany, Denmark, Austria, Greece and the Netherlands announce a joint return facility in Rwanda for rejected asylum seekers, amid human-rights challenges.",
     30.5, -1.9, "KIGALI", -64, 10),
    (5, "ASIA-PACIFIC", (46, 107, 79),
     "Japan scrambles jets after incursion",
     "Tokyo launches fighters and lodges a strong protest after two suspected Russian aircraft enter its airspace early in the morning.",
     140.5, 36.0, "TOKYO", 16, -14),
    (6, "BUSINESS", (51, 51, 51),
     "Banking glitch hits JPMorgan, Zelle",
     "A technical fault at JPMorgan Chase disrupts online banking at several U.S. banks and Zelle; thousands of customers reported problems.",
     -74.0, 40.7, "NEW YORK", -88, -14),
]

BRIEFS = ("Singapore seeks trusted access to AI chips  ·  "
          "At least 17 killed in two shootings in South Africa  ·  "
          "U.S. flights still delayed after Friday's grounding")
SOURCES = "Sources: Al Jazeera  ·  Reuters  ·  AP  ·  BBC  ·  CNN  ·  NYT  —  17 November 2026"

# Map panel geometry (equirectangular, lat 83..-58)
MAP_X0, MAP_X1 = 24, 1000
MAP_Y0, MAP_Y1 = 146, 408
LAT_TOP, LAT_BOT = 83.0, -58.0


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


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((40, 22), "THE WORLD IN ONE DAY",
           font=F("LiberationSans-Bold.ttf", 52), fill=(255, 255, 255))
    d.text((40, 82), "SIX STORIES THAT DEFINED THE DAY",
           font=F("LiberationSans-Bold.ttf", 16), fill=LIGHT_BLUE)
    d.text((984, 26), "TUESDAY", font=F("LiberationSans-Bold.ttf", 20),
           fill=AMBER, anchor="ra")
    d.text((984, 52), "17 NOVEMBER 2026", font=F("LiberationSans-Bold.ttf", 26),
           fill=AMBER, anchor="ra")
    d.rectangle([0, 108, W, 114], fill=RED)

    # ---- Map panel ----
    d.text((24, 122), "WHERE IT HAPPENED",
           font=F("LiberationSans-Bold.ttf", 16), fill=NAVY)
    geo = json.load(open(GEO))
    # graticule
    for lon in range(-150, 181, 30):
        x, _ = lonlat_to_xy(lon, 0)
        d.line([(x, MAP_Y0), (x, MAP_Y1)], fill=GRAT, width=1)
    for lat in range(-60, 84, 30):
        _, y = lonlat_to_xy(0, lat)
        d.line([(MAP_X0, y), (MAP_X1, y)], fill=GRAT, width=1)
    # countries
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
    # pins + labels
    pin_font = F("LiberationSans-Bold.ttf", 18)
    lab_font = F("LiberationSans-Bold.ttf", 13)
    for num, tag, color, head, summ, lon, lat, label, ldx, ldy in STORIES:
        x, y = lonlat_to_xy(lon, lat)
        d.ellipse([x - 15, y - 15, x + 15, y + 15], fill=RED, outline=(255, 255, 255), width=2)
        d.text((x, y - 1), str(num), font=pin_font, fill=(255, 255, 255), anchor="mm")
        d.text((x + ldx, y + ldy), label, font=lab_font, fill=NAVY)

    # ---- By the numbers strip (bottom of map panel) ----
    d.rectangle([0, 372, W, 408], fill=NAVY)
    stats = [("2", "tankers hit by mines"),
             ("5", "nations back the Rwanda plan"),
             ("17", "killed in South Africa"),
             ("2", "Russian jets over Japan")]
    num_f = F("LiberationSans-Bold.ttf", 20)
    lab_f = F("LiberationSans-Regular.ttf", 14)
    seg = W // 4
    for i, (num, lab) in enumerate(stats):
        nw = d.textlength(num, font=num_f)
        lw = d.textlength(lab, font=lab_f)
        total = nw + 8 + lw
        sx = seg * i + (seg - total) / 2
        cy2 = 390
        d.text((sx, cy2), num, font=num_f, fill=AMBER, anchor="lm")
        d.text((sx + nw + 8, cy2), lab, font=lab_f, fill=(255, 255, 255), anchor="lm")

    # ---- Story cards: 2 cols x 3 rows ----
    cw, ch, gap = 480, 160, 16
    x0, y0 = 24, 420
    warnings = []
    for i, (num, tag, color, head, summ, lon, lat, label, ldx, ldy) in enumerate(STORIES):
        cx = x0 + (i % 2) * (cw + gap)
        cy = y0 + (i // 2) * (ch + 12)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=BORDER, width=1)
        d.rectangle([cx, cy, cx + 5, cy + ch], fill=color)
        # number chip + region tag
        chip_cx, chip_cy = cx + 32, cy + 28
        d.ellipse([chip_cx - 14, chip_cy - 14, chip_cx + 14, chip_cy + 14], fill=RED)
        d.text((chip_cx, chip_cy - 1), str(num),
               font=F("LiberationSans-Bold.ttf", 17), fill=(255, 255, 255), anchor="mm")
        d.text((cx + 54, chip_cy), tag, font=F("LiberationSans-Bold.ttf", 15),
               fill=color, anchor="lm")
        # headline (max 2 lines, 24px bold, balanced split)
        hl_font = F("LiberationSans-Bold.ttf", 24)
        lines = wrap_balanced(d, head, hl_font, cw - 32)
        if len(lines) > 2:
            warnings.append(f"story {num}: headline wraps to {len(lines)} lines")
        hy = cy + 50
        for ln in lines[:2]:
            d.text((cx + 16, hy), ln, font=hl_font, fill=NAVY)
            hy += 28
        # summary (max 3 lines, 17px)
        sm_font = F("LiberationSans-Regular.ttf", 17)
        slines = wrap(d, summ, sm_font, cw - 32)
        if len(slines) > 3:
            warnings.append(f"story {num}: summary wraps to {len(slines)} lines")
        sy = hy + 5
        for ln in slines[:3]:
            d.text((cx + 16, sy), ln, font=sm_font, fill=INK)
            sy += 20
        if sy > cy + ch - 8:
            warnings.append(f"story {num}: text overflows card (bottom {sy} > {cy + ch - 8})")

    # ---- Ticker ----
    d.rectangle([0, 936, W, H], fill=NAVY)
    tk_font = F("LiberationSans-Regular.ttf", 17)
    tk_bold = F("LiberationSans-Bold.ttf", 15)
    prefix = "ALSO IN BRIEF   "
    # wrap briefs with the prefix on the first line
    lines = wrap(d, BRIEFS, tk_font, W - 48 - d.textlength(prefix, font=tk_bold))
    ty = 946
    d.text((24, ty), "ALSO IN BRIEF", font=tk_bold, fill=AMBER)
    px = 24 + d.textlength(prefix, font=tk_bold)
    for j, ln in enumerate(lines[:2]):
        d.text((px if j == 0 else 24, ty), ln, font=tk_font, fill=(255, 255, 255))
        ty += 21
    d.text((24, 997), SOURCES, font=F("LiberationSans-Regular.ttf", 13), fill=LIGHT_BLUE)
    if len(lines) > 2:
        warnings.append(f"ticker wraps to {len(lines)} lines")

    out = "/home/hatch/workspace/makefun-news-image-20261117/entry.png"
    img.save(out, "PNG", optimize=True)
    import os
    print("saved", out, os.path.getsize(out), "bytes")
    print("warnings:", warnings if warnings else "none")


if __name__ == "__main__":
    main()
