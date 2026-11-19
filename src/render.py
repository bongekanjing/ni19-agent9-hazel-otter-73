"""The front page for Thursday 19 November 2026.

Thirty stories on one square: eleven carried by a drawn scene and a headline,
the rest as one-line briefs under a numbered map, so a reader who missed the
day can see it before reading a word of it.

Every height is measured, not guessed: the headline and deck of each tile are
wrapped with the real font, and the art takes whatever is left of the tile, so
editing the copy cannot push anything off the page.

Two runs write the same bytes: no clock, no randomness, no network.
"""

from __future__ import annotations

import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24
BOTTOM = 1000

PAPER = (252, 251, 248)
INK = (26, 24, 22)
INK_SOFT = (78, 73, 67)
RULE = (198, 192, 182)
PANEL = (238, 236, 230)

RED = (176, 36, 30)
TEAL = (20, 78, 88)
NAVY = (26, 40, 58)
GOLD = (158, 120, 40)
PLUM = (104, 58, 116)
GREEN = (38, 96, 62)

FONT_DIR = os.environ.get(
    "NI19_FONT_DIR", os.path.join(os.path.dirname(__file__), "fonts")
)
FONTS = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "cond_b": "DejaVuSerifCondensed-Bold.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
    "sans_cb": "DejaVuSansCondensed-Bold.ttf",
}

DATE = "Thursday 19 November 2026"

REGION_COLOUR = {
    "Americas": RED,
    "Europe": TEAL,
    "Asia": NAVY,
    "MidEast": GOLD,
    "Africa": GREEN,
    "World": PLUM,
}
REGIONS = ["Americas", "Europe", "Asia", "MidEast", "Africa", "World"]


def F(kind: str, size: int):
    return ImageFont.truetype(os.path.join(FONT_DIR, FONTS[kind]), size)


# --- the day's stories -----------------------------------------------------
TILES = [
    {
        "region": "Asia", "place": "Shenzhen", "topic": "Diplomacy",
        "headline": "Three nuclear powers at one table",
        "deck": "Trump, Xi Jinping and Putin held the first trilateral summit of the "
                "three, closing APEC in Shenzhen. Trump met each man alone first.",
        "art": "trilateral",
    },
    {
        "region": "MidEast", "place": "Kuwait", "topic": "Conflict",
        "headline": "Iran strikes a US base in the Gulf",
        "deck": "Iran said its drones hit Patriot batteries at Ali Al Salem, the first "
                "such attack since September.",
        "art": "drones",
    },
    {
        "region": "Americas", "place": "New York", "topic": "Markets",
        "headline": "Anthropic lists at $81.3bn, the largest on record",
        "deck": "Priced at $83 a share, above range, it values the company near $1.5trn. "
                "It trades as ANT.",
        "art": "chip",
    },
    {
        "region": "World", "place": "The Hague", "topic": "Law",
        "headline": "The World Court rules on the Rohingya case",
        "deck": "The ICJ delivered judgment on The Gambia's genocide claim against "
                "Myanmar, seven years after it was filed.",
        "art": "icj",
    },
    {
        "region": "Americas", "place": "Washington", "topic": "Politics",
        "headline": "Jeffries is nominated to be Speaker",
        "deck": "House Democrats chose him, putting him in line to be the first Black "
                "speaker.",
        "art": "capitol",
    },
    {
        "region": "Americas", "place": "Anchorage", "topic": "Election",
        "headline": "Peltola's win gives Democrats 56 Senate seats",
        "deck": "The Democrat unseated Dan Sullivan, completing a midterm sweep.",
        "art": "ballot",
    },
    {
        "region": "Americas", "place": "Caracas", "topic": "Diplomacy",
        "headline": "The US and Venezuela restore military ties",
        "deck": "Hegseth signed the accord covering training and intelligence sharing.",
        "art": "handshake",
    },
    {
        "region": "Africa", "place": "Kinshasa", "topic": "Health",
        "headline": "Ebola passes 11,536 cases",
        "deck": "The outbreak has killed 5,635, with 400 to 500 new infections found "
                "each week.",
        "art": "virus",
    },
    {
        "region": "Europe", "place": "Kyiv", "topic": "War",
        "headline": "The Kerch bridge is hit again",
        "deck": "Traffic stopped on the link after another attack, its operator said.",
        "art": "bridge",
    },
    {
        "region": "MidEast", "place": "Gaza", "topic": "War",
        "headline": "Israeli armour crosses the Yellow Line",
        "deck": "A rare ground operation beyond the line, which Israel called a tunnel; "
                "Hamas called it a breach.",
        "art": "tank",
    },
    {
        "region": "Europe", "place": "London", "topic": "Culture",
        "headline": "A Van Gogh sells for $190.4m, a record",
        "deck": "Chataigniers en fleurs, painted in 1890, beat the artist's $117.2m mark.",
        "art": "canvas",
    },
]

BRIEFS = [
    ("Europe", "Berlin", "Allies pledge air defences for Ukraine"),
    ("Europe", "Brussels", "Commission proposes 45bn more for Ukraine"),
    ("Europe", "Warsaw", "Poland breaks up a suspected Russian plot"),
    ("Europe", "Paris", "Macron: the talks show Putin will not negotiate"),
    ("Europe", "Antalya", "COP31 closes with the 1.5C brief unresolved"),
    ("Asia", "Tokyo", "Takaichi meets Putin, a first in seven years"),
    ("Asia", "Shenzhen", "Xi pledges $20m to APEC cooperation"),
    ("Asia", "Dhaka", "Paramilitaries deploy as violence flares"),
    ("Asia", "Taipei", "Benchmark falls 4.4%, the sharpest in Asia"),
    ("MidEast", "Riyadh", "Coalition downs a Houthi missile bound for Riyadh"),
    ("MidEast", "Khasab", "Projectile hits an ADNOC tanker; one missing"),
    ("MidEast", "Doha", "Qatar calls the strikes a dangerous escalation"),
    ("MidEast", "Baghdad", "Six French Islamic State members jailed for life"),
    ("Africa", "El Obeid", "Amnesty counts 37 civilians killed by drones"),
    ("Africa", "Abuja", "All 36 states back their own police forces"),
    ("Africa", "Nairobi", "Nine Ebola cases, all from DR Congo"),
    ("World", "Port-au-Prince", "UN documents 4,595 killed in Haiti's gangs"),
    ("World", "Santiago", "Chile's economy shrinks 1.1%"),
]

NUMBERS = [
    ("$81.3bn", "Anthropic's listing, the largest ever"),
    ("$92.52", "Brent crude, per barrel"),
    ("11,536", "DR Congo Ebola cases"),
    ("4,595", "Killed in Haiti this year"),
    ("26bn km", "Voyager 1 from Earth"),
    ("$190.4m", "Van Gogh, a record"),
]

DATE_CHECK = [
    "Nvidia ousts Huang, shares fall 2.9%",
    "Sotheby's takes $777.8m in a night",
    "Rubio denies a dirty-bomb report",
    "125 captives freed in Nigeria",
    "Four states sign a Red Sea pact",
]

BILLBOARD = (
    "Three leaders meet in Shenzhen  ·  Iran strikes a base in Kuwait  ·  "
    "Anthropic lists  ·  The World Court rules"
)


# --- text helpers ----------------------------------------------------------
def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, xy, text, font, width, fill, leading, max_lines=None):
    lines = wrap(draw, text, font, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def fit_one_line(draw, text, kind, size, width):
    font = F(kind, size)
    while draw.textlength(text, font=font) > width and size > 6:
        size -= 1
        font = F(kind, size)
    return font


def _sky(draw, box, top, bottom=None):
    x0, y0, x1, y1 = box
    if bottom is None:
        draw.rectangle(box, fill=top)
        return
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0 - 1)
        draw.line(
            (x0, y0 + i, x1, y0 + i),
            fill=(
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t),
            ),
        )


# --- the eleven drawn scenes ----------------------------------------------
def art_trilateral(draw, box):
    """Three flags on three lecterns: the first trilateral of the three powers."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (24, 30, 42), (44, 52, 68))
    for i in range(12):
        lx = x0 + int(w * (0.03 + i * 0.082))
        draw.ellipse((lx, y0 + int(h * 0.07), lx + 2, y0 + int(h * 0.07) + 2),
                     fill=(112, 128, 148))
    pod_y = y0 + int(h * 0.72)
    for i in range(3):
        px = x0 + int(w * (0.08 + i * 0.30))
        draw.polygon([(px, pod_y), (px + int(w * 0.18), pod_y),
                      (px + int(w * 0.16), y1 - int(h * 0.04)),
                      (px + int(w * 0.02), y1 - int(h * 0.04))], fill=(46, 54, 68))
        draw.rectangle((px + int(w * 0.07), pod_y - 3, px + int(w * 0.11), pod_y),
                       fill=(152, 162, 178))
    fw, fh = int(w * 0.15), int(h * 0.30)
    for i in range(3):
        fx = x0 + int(w * (0.095 + i * 0.30))
        fy = y0 + int(h * 0.17)
        draw.line((fx + fw // 2, fy + fh, fx + fw // 2, pod_y), fill=(98, 106, 120), width=2)
        if i == 0:
            for k in range(7):
                ty = fy + int(fh * k / 7)
                by = fy + int(fh * (k + 1) / 7)
                draw.rectangle((fx, ty, fx + fw, by),
                               fill=(184, 42, 54) if k % 2 == 0 else (242, 240, 234))
            draw.rectangle((fx, fy, fx + int(fw * 0.44), fy + int(fh * 0.55)),
                           fill=(30, 48, 84))
        elif i == 1:
            draw.rectangle((fx, fy, fx + fw, fy + fh), fill=(188, 32, 40))
            sx, sy, sr = fx + int(fw * 0.24), fy + int(fh * 0.26), int(fw * 0.15)
            draw.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=(248, 214, 92))
        else:
            for k, col in enumerate([(238, 236, 232), (30, 52, 122), (186, 34, 44)]):
                ty = fy + int(fh * k / 3)
                by = fy + int(fh * (k + 1) / 3)
                draw.rectangle((fx, ty, fx + fw, by), fill=col)


def art_icj(draw, box):
    """The bench, the robed judges, and the parties' two tables."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (38, 46, 58), (58, 66, 78))
    by = y0 + int(h * 0.42)
    draw.rectangle((x0 + int(w * 0.05), by, x1 - int(w * 0.05),
                    by + int(h * 0.12)), fill=(102, 86, 64))
    for i in range(13):
        cx = x0 + int(w * (0.07 + i * 0.068))
        draw.polygon([(cx, by), (cx + int(w * 0.042), by),
                      (cx + int(w * 0.036), by - int(h * 0.17)),
                      (cx + int(w * 0.006), by - int(h * 0.17))], fill=(26, 28, 36))
        draw.ellipse((cx + int(w * 0.010), by - int(h * 0.24),
                      cx + int(w * 0.032), by - int(h * 0.17)), fill=(56, 46, 40))
    for i in range(2):
        tx = x0 + int(w * (0.10 + i * 0.46))
        draw.rectangle((tx, y1 - int(h * 0.28), tx + int(w * 0.28),
                        y1 - int(h * 0.21)), fill=(92, 78, 58))
        for k in range(3):
            draw.rectangle((tx + int(w * (0.02 + k * 0.09)), y1 - int(h * 0.21),
                            tx + int(w * (0.08 + k * 0.09)), y1 - int(h * 0.04)),
                           fill=(40, 46, 58))
    ex, ey = x0 + int(w * 0.5), y0 + int(h * 0.14)
    draw.ellipse((ex - int(w * 0.05), ey - int(w * 0.05),
                  ex + int(w * 0.05), ey + int(w * 0.05)), outline=(172, 148, 96), width=2)


def art_tarmac(draw, box):
    """Air Force One on the apron, a red carpet out, two flags."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (58, 74, 96), (128, 142, 158))
    ground = y0 + int(h * 0.62)
    draw.rectangle((x0, ground, x1, y1), fill=(86, 88, 90))
    for i in range(6):
        gy = ground + int(h * 0.06 * i)
        draw.line((x0, gy, x1, gy), fill=(96, 98, 100), width=1)

    bx0, bx1 = x0 + int(w * 0.06), x0 + int(w * 0.70)
    by0 = ground - int(h * 0.36)
    by1 = ground - int(h * 0.10)
    draw.rounded_rectangle((bx0, by0, bx1, by1), radius=max(2, int(h * 0.10)),
                           fill=(236, 238, 240))
    draw.rectangle((bx0, by1 - int(h * 0.11), bx1, by1 - int(h * 0.07)), fill=(36, 66, 132))
    draw.rectangle((bx0, by1 - int(h * 0.06), bx1, by1 - int(h * 0.05)), fill=(176, 36, 30))
    draw.polygon([(bx1, by0), (bx1 + int(w * 0.05), by0 + int(h * 0.10)),
                  (bx1 + int(w * 0.05), by1 - int(h * 0.02)), (bx1, by1)],
                 fill=(236, 238, 240))
    draw.polygon([(bx0, by0), (bx0 - int(w * 0.04), y0 + int(h * 0.04)),
                  (bx0 + int(w * 0.03), y0 + int(h * 0.04)), (bx0 + int(w * 0.09), by0)],
                 fill=(236, 238, 240))
    draw.rectangle((bx0 + int(w * 0.01), y0 + int(h * 0.12),
                    bx0 + int(w * 0.06), y0 + int(h * 0.17)), fill=(36, 66, 132))
    for i in range(9):
        wx = bx0 + int(w * 0.07) + i * int(w * 0.052)
        draw.rectangle((wx, by0 + int(h * 0.07), wx + max(1, int(w * 0.012)),
                        by0 + int(h * 0.11)), fill=(64, 72, 82))

    cx = bx1 - int(w * 0.02)
    draw.polygon([(cx, ground - int(h * 0.02)), (cx + int(w * 0.09), ground - int(h * 0.02)),
                  (x1 - int(w * 0.02), y1), (cx + int(w * 0.15), y1)], fill=(150, 32, 28))
    for i, col in enumerate([(190, 32, 40), (36, 66, 132)]):
        fx = x1 - int(w * (0.15 - i * 0.08))
        draw.line((fx, ground - int(h * 0.02), fx, ground - int(h * 0.36)),
                  fill=(74, 76, 78), width=2)
        draw.rectangle((fx, ground - int(h * 0.36), fx + int(w * 0.05),
                        ground - int(h * 0.24)), fill=col)


def art_drones(draw, box):
    """A warship and a drone overhead, a track between them."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (24, 34, 46), (46, 60, 76))
    sea = y0 + int(h * 0.70)
    draw.rectangle((x0, sea, x1, y1), fill=(28, 46, 62))
    for i in range(6):
        wy = sea + int(h * 0.05) + i * int(h * 0.045)
        draw.line((x0, wy, x1, wy), fill=(36, 58, 76), width=1)

    hx0, hx1 = x0 + int(w * 0.08), x0 + int(w * 0.56)
    draw.polygon([(hx0, sea), (hx1, sea), (hx1 - int(w * 0.05), sea + int(h * 0.13)),
                  (hx0 + int(w * 0.04), sea + int(h * 0.13))], fill=(122, 130, 136))
    draw.rectangle((hx0 + int(w * 0.05), sea - int(h * 0.11),
                    hx1 - int(w * 0.12), sea), fill=(142, 150, 156))
    draw.rectangle((hx0 + int(w * 0.09), sea - int(h * 0.20),
                    hx0 + int(w * 0.18), sea - int(h * 0.11)), fill=(162, 170, 176))
    draw.line((hx0 + int(w * 0.135), sea - int(h * 0.20),
               hx0 + int(w * 0.135), sea - int(h * 0.29)), fill=(182, 188, 192), width=2)

    dx, dy = x0 + int(w * 0.72), y0 + int(h * 0.24)
    draw.line((dx - int(w * 0.10), dy, dx + int(w * 0.02), dy), fill=(226, 224, 216), width=3)
    draw.polygon([(dx, dy - 3), (dx + int(w * 0.09), dy + int(h * 0.03)),
                  (dx + int(w * 0.09), dy + int(h * 0.08)), (dx, dy + 4)],
                 fill=(226, 224, 216))
    for i in range(2):
        wy2 = dy - int(h * 0.09) + i * int(h * 0.18)
        draw.line((dx - int(w * 0.02), wy2, dx + int(w * 0.04), wy2),
                  fill=(200, 200, 196), width=2)
    draw.line((dx, dy, hx0 + int(w * 0.20), sea - int(h * 0.17)),
              fill=(196, 152, 60), width=1)


def art_blackout(draw, box):
    """A city at night with its power out, one searchlight sweeping."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (16, 20, 30), (30, 36, 48))
    base = y1 - int(h * 0.05)
    draw.rectangle((x0, base, x1, y1), fill=(22, 26, 34))
    for i in range(6):
        bx = x0 + int(w * (0.03 + i * 0.16))
        bw = int(w * 0.10)
        bh = int(h * (0.30 + (i % 3) * 0.14))
        bx1 = min(bx + bw, x1)
        draw.rectangle((bx, base - bh, bx1, base), fill=(28, 32, 42))
        for r in range(3):
            for c in range(2):
                if (i + r + c) % 5 == 0:
                    wx = bx + int(bw * (0.18 + c * 0.42))
                    wy = base - bh + int(h * (0.06 + r * 0.09))
                    draw.rectangle((wx, wy, wx + max(1, int(w * 0.011)),
                                    wy + int(h * 0.028)), fill=(226, 196, 120))
    draw.polygon([(x0 + int(w * 0.01), base), (x0 + int(w * 0.32), y0 + int(h * 0.06)),
                  (x0 + int(w * 0.50), y0 + int(h * 0.32))], fill=(42, 50, 64))


def art_flood(draw, box):
    """A street under water, roofs and a stranded car."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (74, 82, 92), (120, 126, 132))
    water = y0 + int(h * 0.46)
    draw.rectangle((x0, water, x1, y1), fill=(70, 88, 96))
    for i in range(6):
        wy = water + int(h * 0.07) + i * int(h * 0.08)
        draw.line((x0, wy, x1, wy), fill=(80, 100, 108), width=1)

    for fx, fh in [(0.04, 0.30), (0.33, 0.38), (0.62, 0.26)]:
        bx = x0 + int(w * fx)
        bw = int(w * 0.21)
        by = water - int(h * fh)
        draw.rectangle((bx, by, bx + bw, water + int(h * 0.05)), fill=(168, 162, 150))
        draw.polygon([(bx - int(w * 0.02), by), (bx + bw // 2, by - int(h * 0.11)),
                      (bx + bw + int(w * 0.02), by)], fill=(122, 76, 62))
        draw.rectangle((bx + int(bw * 0.20), by + int(h * 0.11),
                        bx + int(bw * 0.42), by + int(h * 0.23)), fill=(56, 62, 70))

    cx = x0 + int(w * 0.70)
    cy = water - int(h * 0.01)
    draw.rounded_rectangle((cx, cy - int(h * 0.07), cx + int(w * 0.24), cy + int(h * 0.03)),
                           radius=3, fill=(150, 60, 52))
    draw.rectangle((cx + int(w * 0.04), cy - int(h * 0.12),
                    cx + int(w * 0.15), cy - int(h * 0.06)), fill=(120, 48, 42))


def art_capitol(draw, box):
    """Dome, colonnade, steps: the caucus vote inside."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (232, 230, 222), (204, 202, 194))
    base = y1 - int(h * 0.10)
    cx = x0 + w // 2
    for i in range(3):
        draw.rectangle((x0 + int(w * 0.08) - i * 3, base - i * 3,
                        x1 - int(w * 0.08) + i * 3, base + 3 - i * 3), fill=(196, 192, 182))
    draw.rectangle((cx - int(w * 0.20), base - int(h * 0.30),
                    cx + int(w * 0.20), base), fill=(228, 224, 214))
    for i in range(8):
        px = cx - int(w * 0.17) + i * int(w * 0.048)
        draw.rectangle((px, base - int(h * 0.27), px + int(w * 0.015),
                        base - int(h * 0.02)), fill=(198, 194, 184))
    draw.polygon([(cx - int(w * 0.23), base - int(h * 0.30)),
                  (cx, base - int(h * 0.40)),
                  (cx + int(w * 0.23), base - int(h * 0.30))], fill=(212, 208, 198))
    draw.pieslice((cx - int(w * 0.12), base - int(h * 0.60),
                   cx + int(w * 0.12), base - int(h * 0.36)), 180, 360, fill=(234, 230, 220))
    draw.rectangle((cx - int(w * 0.12), base - int(h * 0.48),
                    cx + int(w * 0.12), base - int(h * 0.40)), fill=(212, 208, 198))
    draw.line((cx, base - int(h * 0.60), cx, base - int(h * 0.68)),
              fill=(150, 146, 136), width=2)
    for s in (-1, 1):
        fx = cx + s * int(w * 0.33)
        draw.line((fx, base, fx, base - int(h * 0.34)), fill=(120, 116, 108), width=2)
        draw.rectangle((min(fx, fx + s * int(w * 0.09)), base - int(h * 0.34),
                        max(fx, fx + s * int(w * 0.09)), base - int(h * 0.24)),
                       fill=(176, 36, 30) if s > 0 else (36, 66, 132))


def art_ballot(draw, box):
    """A ballot going into a box, one box ticked."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (240, 238, 230), (214, 211, 202))
    bx0, bx1 = x0 + int(w * 0.22), x0 + int(w * 0.80)
    by0, by1 = y0 + int(h * 0.54), y1 - int(h * 0.08)
    draw.rectangle((bx0, by0, bx1, by1), fill=(58, 74, 96))
    draw.rectangle((bx0, by0, bx1, by0 + int(h * 0.06)), fill=(44, 58, 78))
    draw.rectangle((bx0 + int(w * 0.22), by0, bx1 - int(w * 0.22),
                    by0 + int(h * 0.03)), fill=(24, 28, 34))
    px0 = bx0 + int(w * 0.16)
    draw.rectangle((px0, y0 + int(h * 0.14), px0 + int(w * 0.26), by0 + int(h * 0.05)),
                   fill=(250, 248, 242), outline=(180, 176, 166))
    for i in range(3):
        ly = y0 + int(h * 0.24) + i * int(h * 0.08)
        draw.line((px0 + 5, ly, px0 + int(w * 0.21), ly), fill=(150, 146, 136), width=1)
    tx, ty = px0 + int(w * 0.15), y0 + int(h * 0.22)
    draw.line((tx, ty, tx + int(w * 0.03), ty + int(h * 0.07)), fill=RED, width=3)
    draw.line((tx + int(w * 0.03), ty + int(h * 0.07), tx + int(w * 0.10), ty - int(h * 0.05)),
              fill=RED, width=3)


def art_handshake(draw, box):
    """Two delegations, a table, four flags."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (30, 40, 54), (52, 64, 80))
    table = y0 + int(h * 0.68)
    draw.rectangle((x0, table, x1, y1), fill=(46, 58, 74))
    draw.line((x0, table, x1, table), fill=(96, 108, 124), width=2)

    for s in (-1, 1):
        hx = x0 + w // 2 + s * int(w * 0.17)
        draw.ellipse((hx - int(w * 0.032), table - int(h * 0.34),
                      hx + int(w * 0.032), table - int(h * 0.27)), fill=(58, 46, 40))
        draw.polygon([(hx - int(w * 0.055), table - int(h * 0.02)),
                      (hx + int(w * 0.055), table - int(h * 0.02)),
                      (hx + int(w * 0.045), table - int(h * 0.25)),
                      (hx - int(w * 0.045), table - int(h * 0.25))], fill=(30, 36, 48))
        draw.line((hx + s * int(w * 0.02), table - int(h * 0.19),
                   x0 + w // 2 + s * int(w * 0.01), table - int(h * 0.12)),
                  fill=(58, 46, 40), width=4)
    draw.ellipse((x0 + w // 2 - int(w * 0.02), table - int(h * 0.15),
                  x0 + w // 2 + int(w * 0.02), table - int(h * 0.09)), fill=(150, 118, 92))

    for i, col in enumerate([(190, 32, 40), (36, 66, 132), (188, 140, 60), (40, 92, 64)]):
        fx = x0 + int(w * (0.08 + i * 0.26))
        draw.line((fx, y0 + int(h * 0.10), fx, table - int(h * 0.28)),
                  fill=(90, 96, 108), width=2)
        draw.rectangle((fx, y0 + int(h * 0.10), fx + int(w * 0.12),
                        y0 + int(h * 0.24)), fill=col)


def art_quake(draw, box):
    """A cracked street, a leaning block, dust."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (196, 186, 172), (222, 214, 202))
    ground = y0 + int(h * 0.72)
    draw.rectangle((x0, ground, x1, y1), fill=(148, 138, 128))
    for bx, bh, lean in [(0.04, 0.44, 0), (0.33, 0.58, 5), (0.63, 0.36, 0)]:
        bx0 = x0 + int(w * bx)
        bw = int(w * 0.21)
        top = ground - int(h * bh)
        draw.polygon([(bx0, ground), (bx0 + bw, ground),
                      (bx0 + bw + lean, top), (bx0 + lean, top)], fill=(120, 112, 104))
        for r in range(3):
            for c in range(2):
                wx = bx0 + int(bw * (0.16 + c * 0.44)) + lean // 2
                wy = top + int(h * 0.09) + r * int(h * 0.10)
                draw.rectangle((wx, wy, wx + max(1, int(w * 0.016)),
                                wy + int(h * 0.045)), fill=(62, 58, 54))
    pts = [(x0, ground + int(h * 0.08))]
    for i in range(7):
        pts.append((x0 + int(w * (0.13 + i * 0.13)),
                    ground + int(h * (0.16 if i % 2 else 0.03))))
    draw.line(pts, fill=(48, 44, 42), width=3)
    for i in range(8):
        dx2 = x0 + int(w * (0.10 + i * 0.11))
        dy2 = ground - int(h * (0.05 + (i % 3) * 0.05))
        draw.ellipse((dx2, dy2, dx2 + int(w * 0.028), dy2 + int(h * 0.05)),
                     fill=(208, 200, 188))


def art_tank(draw, box):
    """Armour on a road, dust behind it."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (198, 176, 146), (216, 198, 170))
    ground = y0 + int(h * 0.76)
    draw.rectangle((x0, ground, x1, y1), fill=(170, 150, 122))
    hx0 = x0 + int(w * 0.14)
    hy0 = ground - int(h * 0.26)
    draw.polygon([(hx0, hy0), (hx0 + int(w * 0.56), hy0),
                  (hx0 + int(w * 0.62), ground), (hx0 - int(w * 0.02), ground)],
                 fill=(92, 100, 78))
    draw.rectangle((hx0 + int(w * 0.15), hy0 - int(h * 0.17),
                    hx0 + int(w * 0.39), hy0), fill=(80, 88, 68))
    draw.line((hx0 + int(w * 0.37), hy0 - int(h * 0.11),
               hx0 + int(w * 0.74), hy0 - int(h * 0.13)), fill=(70, 78, 60), width=4)
    draw.rectangle((hx0 - int(w * 0.02), ground - int(h * 0.08),
                    hx0 + int(w * 0.62), ground), fill=(52, 54, 50))
    for i in range(8):
        wx = hx0 + i * int(w * 0.078)
        draw.ellipse((wx, ground - int(h * 0.075), wx + int(w * 0.05),
                      ground - int(h * 0.005)), fill=(74, 76, 70))
    for i in range(5):
        dx2 = hx0 - int(w * (0.04 + i * 0.06))
        dr = int(w * (0.045 + (i % 3) * 0.015))
        draw.ellipse((dx2 - dr, ground - int(h * 0.11) - i * 2, dx2 + dr,
                      ground + int(h * 0.05) - i * 2), fill=(200, 184, 158))


def art_virus(draw, box):
    """The particle itself, spikes out, on a dark field."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (26, 30, 40), (40, 44, 56))
    cx, cy = x0 + w // 2, y0 + h // 2
    r = int(min(w, h) * 0.26)
    for i in range(14):
        a = i * (2 * math.pi / 14)
        x2 = cx + int((r + int(r * 0.44)) * math.cos(a))
        y2 = cy + int((r + int(r * 0.44)) * math.sin(a))
        x3 = cx + int(r * math.cos(a))
        y3 = cy + int(r * math.sin(a))
        draw.line((x3, y3, x2, y2), fill=(150, 108, 170), width=3)
        draw.ellipse((x2 - 3, y2 - 3, x2 + 3, y2 + 3), fill=(176, 132, 196))
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(122, 84, 146))
    draw.ellipse((cx - int(r * 0.7), cy - int(r * 0.7), cx + int(r * 0.7),
                  cy + int(r * 0.7)), fill=(146, 104, 172))
    for i in range(5):
        a = i * 1.257
        px = cx + int(r * 0.42 * math.cos(a))
        py = cy + int(r * 0.42 * math.sin(a))
        draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=(84, 56, 104))


def art_chip(draw, box):
    """A die on a board, with a valuation line turning down."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (22, 26, 36), (34, 40, 52))
    draw.rectangle((x0 + int(w * 0.10), y0 + int(h * 0.20),
                    x0 + int(w * 0.56), y1 - int(h * 0.10)), fill=(38, 58, 52))
    for i in range(6):
        py = y0 + int(h * 0.26) + i * int(h * 0.085)
        draw.line((x0 + int(w * 0.04), py, x0 + int(w * 0.10), py),
                  fill=(150, 130, 70), width=2)
        draw.line((x0 + int(w * 0.56), py, x0 + int(w * 0.62), py),
                  fill=(150, 130, 70), width=2)
    draw.rectangle((x0 + int(w * 0.20), y0 + int(h * 0.30),
                    x0 + int(w * 0.46), y1 - int(h * 0.20)), fill=(66, 92, 84))
    draw.rectangle((x0 + int(w * 0.24), y0 + int(h * 0.36),
                    x0 + int(w * 0.42), y1 - int(h * 0.26)), outline=(112, 146, 132))
    pts = []
    for i in range(9):
        px = x0 + int(w * (0.64 + i * 0.033))
        py = y0 + int(h * (0.60 if i < 5 else 0.60 + (i - 4) * 0.09))
        pts.append((px, py))
    draw.line(pts, fill=(176, 36, 30), width=3)
    draw.ellipse((pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3),
                 fill=(176, 36, 30))


def art_bridge(draw, box):
    """A span over water with one broken section and no traffic on it."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (28, 36, 50), (46, 56, 70))
    water = y0 + int(h * 0.70)
    draw.rectangle((x0, water, x1, y1), fill=(22, 32, 44))
    for i in range(7):
        wx = x0 + int(w * (0.04 + i * 0.14))
        draw.line((wx, water + int(h * 0.10), wx + int(w * 0.10),
                   water + int(h * 0.10)), fill=(40, 54, 68), width=1)
    deck = y0 + int(h * 0.42)
    # the two approach spans, then the gap
    draw.rectangle((x0 + int(w * 0.02), deck, x0 + int(w * 0.40), deck + int(h * 0.05)),
                   fill=(150, 154, 158))
    draw.rectangle((x0 + int(w * 0.60), deck, x0 + int(w * 0.98), deck + int(h * 0.05)),
                   fill=(150, 154, 158))
    # piers
    for fx in (0.10, 0.22, 0.34, 0.68, 0.80, 0.92):
        px = x0 + int(w * fx)
        draw.rectangle((px, deck + int(h * 0.05), px + int(w * 0.018), water),
                       fill=(120, 126, 130))
    # the broken deck, tilted into the water
    draw.polygon([(x0 + int(w * 0.42), deck + int(h * 0.02)),
                  (x0 + int(w * 0.52), deck + int(h * 0.12)),
                  (x0 + int(w * 0.50), deck + int(h * 0.18)),
                  (x0 + int(w * 0.40), deck + int(h * 0.07))], fill=(132, 136, 140))
    # the arch above the gap, just visible against the sky
    draw.arc((x0 + int(w * 0.38), deck - int(h * 0.30), x0 + int(w * 0.62),
              deck + int(h * 0.06)), 180, 360, fill=(92, 100, 112), width=2)
    # no traffic: the deck is empty, only the damaged span in the water
    for i in range(3):
        sx = x0 + int(w * (0.44 + i * 0.045))
        draw.rectangle((sx, water + int(h * 0.04), sx + int(w * 0.03),
                        water + int(h * 0.07)), fill=(40, 50, 62))


def art_canvas(draw, box):
    """A framed painting on a gallery wall, and its hammer price on a card."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (46, 42, 46), (60, 56, 58))

    # the painting, left two thirds
    fx0, fy0 = x0 + int(w * 0.10), y0 + int(h * 0.20)
    fx1, fy1 = x0 + int(w * 0.62), y1 - int(h * 0.20)
    draw.rectangle((fx0 - 3, fy0 - 3, fx1 + 3, fy1 + 3), fill=(150, 122, 62))
    draw.rectangle((fx0, fy0, fx1, fy1), fill=(206, 196, 170))
    # chestnut trees in blossom: trunks, canopies, a green field
    for tx, tw2 in ((0.06, 0.13), (0.36, 0.15), (0.66, 0.12)):
        px = fx0 + int((fx1 - fx0) * tx)
        pw = int((fx1 - fx0) * tw2)
        draw.rectangle((px + pw // 2, fy0 + int((fy1 - fy0) * 0.55),
                        px + pw // 2 + 3, fy1 - int((fy1 - fy0) * 0.10)),
                       fill=(86, 66, 48))
        draw.ellipse((px, fy0 + int((fy1 - fy0) * 0.14),
                      px + pw, fy0 + int((fy1 - fy0) * 0.62)),
                     fill=(222, 212, 184))
        draw.ellipse((px + int(pw * 0.2), fy0 + int((fy1 - fy0) * 0.24),
                      px + int(pw * 0.7), fy0 + int((fy1 - fy0) * 0.50)),
                     fill=(236, 230, 210))
    draw.rectangle((fx0, fy0 + int((fy1 - fy0) * 0.80), fx1, fy1),
                   fill=(148, 166, 130))

    # the price card, entirely clear of the frame
    cx0, cx1 = x0 + int(w * 0.66), x1 - int(w * 0.06)
    cy0, cy1 = y0 + int(h * 0.26), y1 - int(h * 0.26)
    draw.rectangle((cx0, cy0, cx1, cy1), fill=(246, 244, 238))
    draw.rectangle((cx0, cy0, cx1, cy0 + int(h * 0.11)), fill=(176, 36, 30))
    for i in range(3):
        ly = cy0 + int(h * 0.22) + i * int(h * 0.11)
        draw.rectangle((cx0 + int(w * 0.02), ly, cx1 - int(w * 0.05), ly + 2),
                       fill=(158, 154, 146))


ART = {
    "trilateral": art_trilateral,
    "icj": art_icj,
    "tarmac": art_tarmac,
    "drones": art_drones,
    "blackout": art_blackout,
    "flood": art_flood,
    "capitol": art_capitol,
    "ballot": art_ballot,
    "handshake": art_handshake,
    "quake": art_quake,
    "tank": art_tank,
    "virus": art_virus,
    "chip": art_chip,
    "canvas": art_canvas,
    "bridge": art_bridge,
}


# --- the map ---------------------------------------------------------------
LAND_PATH = os.environ.get(
    "NI19_LAND",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "land.json"),
)


def _load_land():
    """Real coastlines (Natural Earth 1:110m), packed beside the fonts."""
    with open(LAND_PATH) as fh:
        return [[(lon / 10.0, lat / 10.0) for lon, lat in ring] for ring in json.load(fh)]


LAND = _load_land()


def draw_map(draw, box, pins):
    """A world map with a numbered pin per tile: the page's index."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(22, 32, 42))

    lat_top, lat_bot = 84.0, -58.0

    def px(lon):
        return x0 + int(w * (lon + 180) / 360)

    def py(lat):
        return y0 + int(h * (lat_top - lat) / (lat_top - lat_bot))

    for i in range(1, 6):
        gy = y0 + int(h * i / 6)
        draw.line((x0, gy, x1, gy), fill=(32, 44, 56), width=1)
    for i in range(1, 12):
        gx = x0 + int(w * i / 12)
        draw.line((gx, y0, gx, y1), fill=(32, 44, 56), width=1)

    for ring in LAND:
        pts = [(px(lon), py(lat)) for lon, lat in ring]
        if len(pts) >= 3:
            draw.polygon(pts, fill=(104, 116, 102))

    pf = F("sans_cb", 7)
    R = 6
    global MAP_PLACED
    MAP_PLACED = []          # pin radius: small enough for two cities in one country
    placed = []
    for lon, lat, colour, num in pins:
        ax, ay = px(lon), py(lat)      # where it happened
        cx, cy = ax, ay                # where the pin is drawn
        step = 0
        SEP = 2 * R + 4          # clear gap between two discs
        while any((cx - q[0]) ** 2 + (cy - q[1]) ** 2 < SEP * SEP
                  for q in placed) and step < 240:
            step += 1
            ang = step * 0.55
            rr = 3 + step * 0.85
            cx = int(ax + rr * math.cos(ang))
            cy = int(ay + rr * math.sin(ang))
            cx = max(x0 + R + 1, min(x1 - R - 1, cx))
            cy = max(y0 + R + 1, min(y1 - R - 1, cy))
        placed.append((cx, cy))
        MAP_PLACED.append((num, ax, ay, cx, cy))
        if (cx, cy) != (ax, ay):
            # a leader back to the true spot, so the map stays honest
            draw.line((ax, ay, cx, cy), fill=(226, 222, 210), width=1)
            draw.ellipse((ax - 1, ay - 1, ax + 1, ay + 1), fill=(226, 222, 210))
        draw.ellipse((cx - R - 1, cy - R - 1, cx + R + 1, cy + R + 1),
                     fill=(246, 244, 238))
        draw.ellipse((cx - R, cy - R, cx + R, cy + R), fill=colour)
        label = str(num)
        tw = draw.textlength(label, font=pf)
        draw.text((cx - tw / 2, cy - 3.5), label, font=pf, fill=(255, 255, 255))


PINS = [
    (114.06, 22.54, NAVY, 1),
    (47.9, 29.3, GOLD, 2),
    (-74.0, 40.7, RED, 3),
    (4.3, 52.07, PLUM, 4),
    (-77.0, 38.9, RED, 5),
    (-149.9, 61.2, RED, 6),
    (-66.9, 10.5, RED, 7),
    (15.3, -4.3, GREEN, 8),
    (30.5, 50.4, TEAL, 9),
    (34.5, 31.4, GOLD, 10),
    (-0.1, 51.5, TEAL, 11),
]


# --- layout ----------------------------------------------------------------
def build(out_path: str) -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN

    # ---- eyebrow: the nameplate and the promise ----
    y = MARGIN
    d.text((MARGIN, y), "THE WORLD IN ONE DAY", font=F("sans_cb", 13), fill=INK)
    right = f"{len(TILES) + len(BRIEFS)} STORIES  ·  6 REGIONS  ·  ONE PAGE"
    rf = F("sans_cb", 10)
    d.text((W - MARGIN - d.textlength(right, font=rf), y + 2), right, font=rf, fill=INK_SOFT)
    y += 18
    d.line((MARGIN, y, W - MARGIN, y), fill=INK, width=2)

    # ---- the date, the largest thing on the page ----
    y += 10
    date_font = F("cond_b", 54)
    while d.textlength(DATE, font=date_font) > inner and date_font.size > 30:
        date_font = F("cond_b", date_font.size - 1)
    d.text((MARGIN, y), DATE, font=date_font, fill=INK)
    y += int(date_font.size * 1.10)
    d.line((MARGIN, y, W - MARGIN, y), fill=RULE)
    y += 6

    # ---- the billboard: the four things that happened ----
    bf = fit_one_line(d, BILLBOARD, "sans_cb", 13, inner)
    d.text((MARGIN, y), BILLBOARD, font=bf, fill=RED)
    y += 20

    # ---- the numbers strip ----
    strip_h = 44
    d.rectangle((MARGIN, y, W - MARGIN, y + strip_h), fill=PANEL)
    cell = inner // len(NUMBERS)
    nf = F("cond_b", 21)
    lf = F("serif", 8)
    for i, (big, small) in enumerate(NUMBERS):
        cx = MARGIN + i * cell + 8
        d.text((cx, y + 4), big, font=nf, fill=RED)
        draw_block(d, (cx, y + 27), small, lf, cell - 14, INK_SOFT, 9, 2)
        if i:
            d.line((MARGIN + i * cell, y + 6, MARGIN + i * cell, y + strip_h - 6), fill=RULE)
    y += strip_h + 10

    # ---- the tiles: three wide, then two rows of four ----
    rail_h = 152
    rail_top = BOTTOM - 44 - rail_h
    tile_top = y
    rows = [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9, 10]]
    gap = 8
    avail = rail_top - 10 - tile_top - gap * (len(rows) - 1)
    row_h = avail // len(rows)

    idx = 0
    for r, row in enumerate(rows):
        cols = len(row)
        tw = (inner - gap * (cols - 1)) // cols
        ry = tile_top + r * (row_h + gap)
        wide = cols == 3
        head_f = F("sans_cb", 17 if wide else 13)
        deck_f = F("serif", 10 if wide else 9)
        head_l = 19 if wide else 15
        deck_l = 11 if wide else 10

        for c in range(cols):
            tile = TILES[idx]
            x0 = MARGIN + c * (tw + gap)
            idx += 1

            head = wrap(d, tile["headline"], head_f, tw - 2)[:2]
            deck = wrap(d, tile["deck"], deck_f, tw - 2)[:2]
            kick_h = 13
            text_h = kick_h + 2 + len(head) * head_l + 2 + len(deck) * deck_l
            art_h = max(24, row_h - text_h - 6)

            box = (x0, ry, x0 + tw, ry + art_h)
            ART[tile["art"]](d, box)
            d.rectangle((x0, ry, x0 + tw, ry + art_h), outline=RULE)

            ty = ry + art_h + 3
            numf = F("sans_cb", 9)
            d.rectangle((x0, ty, x0 + 15, ty + 12), fill=REGION_COLOUR[tile["region"]])
            nw = d.textlength(str(idx), font=numf)
            d.text((x0 + 7 - nw / 2, ty + 1), str(idx), font=numf, fill=PAPER)

            kick = f"{tile['place'].upper()}  ·  {tile['topic'].upper()}"
            kf = fit_one_line(d, kick, "sans_cb", 8, tw - 22)
            d.text((x0 + 19, ty + 1), kick, font=kf, fill=REGION_COLOUR[tile["region"]])
            ty += kick_h + 2

            for line in head:
                d.text((x0, ty), line, font=head_f, fill=INK)
                ty += head_l
            ty += 2
            for line in deck:
                d.text((x0, ty), line, font=deck_f, fill=INK_SOFT)
                ty += deck_l

    d.line((MARGIN, rail_top - 8, W - MARGIN, rail_top - 8), fill=RULE)

    # ---- the rail: the map index beside the briefs ----
    map_w = 372
    map_h = rail_h
    draw_map(d, (MARGIN, rail_top, MARGIN + map_w, rail_top + map_h), PINS)
    cap_h = 12
    d.rectangle((MARGIN, rail_top + map_h - cap_h, MARGIN + map_w,
                 rail_top + map_h), fill=(206, 206, 198))
    mf = F("sans_cb", 7)
    d.text((MARGIN + 6, rail_top + map_h - cap_h + 3), "WHERE IT HAPPENED  ·  NUMBERED TO THE STORIES ABOVE",
           font=mf, fill=(28, 34, 40))

    bx = MARGIN + map_w + 12
    bw = W - MARGIN - bx
    d.text((bx, rail_top), "ALSO ON 19 NOVEMBER", font=F("sans_cb", 10), fill=INK)
    by = rail_top + 16

    colw = (bw - 10) // 2
    for size in range(9, 5, -1):
        bfont = F("sans_cb", size)
        lead = size + 3
        per_col = (rail_top + rail_h - by) // lead
        total = sum(len(wrap(d, f"{city.upper()}  {text}", bfont, colw))
                    for _, city, text in BRIEFS)
        if total <= per_col * 2:
            break

    # balance the two columns by line count, not by first-fit: 18 briefs in a
    # 10/8 split leaves one column hanging
    wrapped = [(region, wrap(d, f"{city.upper()}  {text}", bfont, colw))
               for region, city, text in BRIEFS]
    total = sum(len(ls) for _, ls in wrapped)
    target = (total + 1) // 2

    col, cy, used = 0, by, 0
    for region, lines in wrapped:
        if col == 0 and used + len(lines) > target and used > 0:
            col, cy, used = 1, by, 0
        cx = bx + col * (colw + 10)
        for j, ln in enumerate(lines):
            d.text((cx, cy), ln, font=bfont,
                   fill=REGION_COLOUR[region] if j == 0 else INK)
            cy += lead
        used += len(lines)

    # ---- date check and footer ----
    yb = BOTTOM - 38
    d.line((MARGIN, yb, W - MARGIN, yb), fill=RED, width=2)
    dc_label = F("sans_cb", 9)
    head = "ALSO TODAY:"
    dcf = F("serif", 8)
    # shrink the strip until the last item clears the right margin
    while True:
        need = d.textlength(head + "  ", font=dc_label) + sum(
            d.textlength(it + "  ·  ", font=dcf) for it in DATE_CHECK)
        if need <= inner or dcf.size <= 6:
            break
        dcf = F("serif", dcf.size - 1)
    d.text((MARGIN, yb + 5), head, font=dc_label, fill=RED)
    dx = MARGIN + d.textlength(head + "  ", font=dc_label)
    for i, item in enumerate(DATE_CHECK):
        tail = "  ·" if i < len(DATE_CHECK) - 1 else ""
        d.text((dx, yb + 6), item + tail, font=dcf, fill=INK_SOFT)
        dx += d.textlength(item + "  ·  ", font=dcf)
    assert dx <= W - MARGIN + 2, (dx, need)

    ff = F("serif", 8)
    d.line((MARGIN, BOTTOM - 16, W - MARGIN, BOTTOM - 16), fill=RULE)
    d.text(
        (MARGIN, BOTTOM - 12),
        "Reuters · AP · AFP · BBC · Al Jazeera · Bloomberg · NASA · WHO · ECB",
        font=ff, fill=INK_SOFT,
    )
    src = "Every story first reported on Thursday 19 November 2026."
    d.text((W - MARGIN - d.textlength(src, font=ff), BOTTOM - 12), src, font=ff, fill=INK_SOFT)

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
