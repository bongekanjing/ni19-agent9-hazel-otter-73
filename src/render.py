"""Front page for Thursday 19 November 2026.

Layout: date-as-headline, three illustrated leads, a hard-numbers strip,
a colour-coded region index whose counts are computed from the story list,
and a dense multi-column brief stack that is fitted to the space left over.

The page is 1024x1024 and deterministic: same input, same bytes.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 26
COLW = W - 2 * MARGIN
BOTTOM = H - MARGIN

PAPER = (247, 244, 236)
INK = (20, 18, 15)
INK_SOFT = (74, 69, 62)
RULE = (150, 143, 132)
HAIR = (212, 205, 192)
RED = (170, 36, 28)
TEAL = (22, 82, 92)
NAVY = (24, 38, 54)
GOLD = (168, 130, 48)
PLUM = (110, 62, 120)

FONT_DIR = os.environ.get("NI19_FONT_DIR", os.path.join(os.path.dirname(__file__), "fonts"))
FONTS = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "cond_b": "DejaVuSerifCondensed-Bold.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
    "sans_cb": "DejaVuSansCondensed-Bold.ttf",
}

REGIONS = ("Americas", "Europe", "Asia", "MidEast", "Africa")
REGION_COLOURS = {
    "Americas": RED,
    "Europe": TEAL,
    "Asia": NAVY,
    "MidEast": GOLD,
    "Africa": PLUM,
}

_cache = {}


def F(kind, size):
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, FONTS[kind]), int(size))
    return _cache[key]


# ---------------------------------------------------------------- content ----
LEADS = [
    {
        "kicker": "SHENZHEN",
        "headline": "Three nuclear powers at one table for the first time",
        "deck": (
            "Trump, Xi Jinping and Vladimir Putin held the first trilateral summit between the "
            "leaders of the United States, China and Russia, closing the APEC meeting in "
            "Shenzhen. Trump met each man alone first; officials played down the chance of a deal."
        ),
        "art": "trilateral",
        "region": "Asia",
    },
    {
        "kicker": "THE GULF",
        "headline": "Iran strikes a US base in Kuwait as the war widens",
        "deck": (
            "Iran said its drones targeted Patriot batteries at Ali Al Salem air base in Kuwait, its "
            "first such attack since September, after US jets struck a missile site on Qeshm Island. "
            "Bahrain reported a fourth attack in six days; a Houthi missile aimed at Riyadh was downed."
        ),
        "art": "gulf",
        "region": "MidEast",
    },
    {
        "kicker": "THE HAGUE",
        "headline": "World court gives its first genocide verdict in a decade",
        "deck": (
            "The International Court of Justice delivered its judgment on The Gambia's claim "
            "that Myanmar committed genocide against its Rohingya minority, seven years after "
            "the case was filed. No state had ever been found guilty of genocide by such a court."
        ),
        "art": "icj",
        "region": "Asia",
    },
]

SECOND_LEADS = [
    {
        "kicker": "NEW YORK",
        "headline": "Anthropic raises $81.3bn in the largest listing on record",
        "deck": (
            "The Claude maker priced at $83 a share, above its range, selling about 980m shares "
            "and valuing it near $1.5trn. It beats SpaceX's June offer and trades as ANT."
        ),
        "region": "Americas",
    },
    {
        "kicker": "LOS SANTOS",
        "headline": "Grand Theft Auto VI reaches shelves after 13 years",
        "deck": (
            "Rockstar's sequel launched on PlayStation 5 and Xbox Series X after repeated "
            "delays, closing a wait that began with GTA V in 2013. Pre-orders were reported "
            "near $1bn."
        ),
        "region": "Americas",
    },
]

BRIEFS = [
    ("Americas", "Jeffries nominated", "House Democrats chose Hakeem Jeffries, 56, as their leader, putting him in line to be the first Black speaker when Congress sits in January."),
    ("Americas", "Alaska turns blue", "Democrat Mary Peltola unseated Republican Dan Sullivan, giving Democrats a 56-44 Senate majority."),
    ("Americas", "Caracas deal", "Washington and Venezuela signed an accord to restore military ties, from training to intelligence sharing, Pete Hegseth said in Caracas."),
    ("Americas", "Riyadh reactor deal", "IAEA chief Rafael Grossi called the US-Saudi civilian nuclear agreement a very satisfactory outcome."),
    ("Americas", "Voyager's light-day", "Voyager 1 passed one light-day from Earth, about 26bn km, the farthest any human-made object has gone."),
    ("Americas", "Nvidia slips", "Nvidia fell 2.9% after strong results, as investors weighed the ouster of chief executive Jensen Huang. The board ruled out rehiring him."),
    ("Americas", "Musk's regret", "Elon Musk called his record $446m of midterm spending pretty foolish."),
    ("Americas", "Santiago slump", "Chile's economy shrank 1.1% in the third quarter; President Jose Antonio Kast's approval has fallen to 24%."),
    ("Americas", "Malvinas route", "Chile and Argentina clashed over a reopened cargo route from Punta Arenas to the Falklands, idle since 2011."),
    ("Europe", "Crimea bridge hit", "Traffic stopped on the Kerch bridge after another attack, the link's head said. Kyiv reported striking it without Starlink."),
    ("Europe", "Berlin pledges", "Ukraine's European allies met in Berlin, where Volodymyr Zelensky sought air defences and help to repair the power grid."),
    ("Europe", "45bn more", "The European Commission proposed a further 45bn euros in loans to Ukraine for 2027, repaid only from Russian reparations."),
    ("Europe", "Warsaw's warning", "Poland said it broke up a suspected Russian false-flag operation on its soil."),
    ("Europe", "Van Gogh record", "Chataigniers en fleurs, painted in 1890, sold for $190.4m with fees at Sotheby's, beating the artist's $117.2m record."),
    ("Europe", "Sotheby's night", "Two back-to-back New York sales took $777.8m with fees and set records for Mary Cassatt and Aaron Douglas."),
    ("Europe", "Antalya finale", "COP31 in Antalya, Turkey, entered its closing day with leaders pressed to keep the 1.5C overshoot brief."),
    ("Europe", "Paris doubts", "Emmanuel Macron said the talks showed Putin does not want to negotiate; Britain and Germany voiced similar doubts."),
    ("Europe", "Pound at $1.314", "Sterling slipped against a dollar lifted by hawkish Fed comments, while the euro hovered near an April 2025 low."),
    ("Asia", "Takaichi in Shenzhen", "Japan's premier, Sanae Takaichi, shook hands with Xi Jinping a second time at APEC, with ties strained over Taiwan remarks."),
    ("Asia", "Tokyo-Moscow thaw", "Takaichi met Putin for the first Japan-Russia summit in seven years and pressed for a detained journalist's release."),
    ("Asia", "Xi's $20m", "Xi pledged $20m to APEC cooperation and a new Asia-Pacific research centre in Shenzhen."),
    ("Asia", "Dhaka unrest", "Bangladesh deployed hundreds of paramilitaries as violence flared over Sheikh Hasina's planned return from exile."),
    ("Asia", "76 faiths", "India's census portal listed 76 other religions as predictive text, after 287 entries were pulled from a drop-down."),
    ("Asia", "Delhi-Ottawa", "India and Canada are near a defence pact for Narendra Modi's December visit, and near a trade deal."),
    ("Asia", "Pension bill", "India's EPFO told trustees that higher pensions for 4.45 lakh claimants may cost 1.1 lakh crore rupees more."),
    ("Asia", "Parts pact", "Japan's carmakers will standardise specifications for steel, resins and wire harnesses to hold ground abroad."),
    ("Asia", "Taipei tumbles", "Taiwan's benchmark fell 4.4% and TSMC 3.5%, the sharpest drop in Asia, ahead of the Shenzhen summit."),
    ("MidEast", "Grossi rebuked", "Iran accused the IAEA's chief of a double standard in how the agency treats Israel and Iran."),
    ("MidEast", "Doha's warning", "Qatar, the mediator, called the strikes a dangerous escalation that threatens efforts to end the nine-month war."),
    ("MidEast", "Blockade widened", "US Central Command said ships taking cargo at sea from Iran-loaded vessels risk being treated as blockade evaders."),
    ("MidEast", "Gaza incursion", "Israel mounted a rare ground operation beyond the Yellow Line, saying it was dismantling a tunnel; Hamas called it a truce violation."),
    ("MidEast", "Riyadh intercepted", "A Saudi-led coalition destroyed a Houthi cruise missile bound for Riyadh; residents reported a loud blast."),
    ("MidEast", "Tanker struck", "One crew member of an ADNOC vessel was missing and 11 injured after a projectile hit it near Khasab, Oman."),
    ("MidEast", "No imminent threat", "Secretary of State Marco Rubio played down a report that Iran might plan a dirty-bomb attack in Washington."),
    ("Africa", "Ebola toll", "The DR Congo outbreak passed 11,536 cases and 5,635 deaths, with 400 to 500 new infections still found each week."),
    ("Africa", "Khartoum's drones", "The AU, IGAD, the Arab League, the EU and the UN condemned drone strikes; Amnesty counted 37 civilians killed in El Obeid."),
    ("Africa", "New Alamein four", "Egypt, Eritrea, Somalia and Sudan agreed to coordinate on security, the Red Sea and the Nile dam dispute."),
    ("Africa", "State police", "All 36 Nigerian state legislatures backed an amendment letting states run their own police forces."),
    ("Africa", "Senegal sinking", "Dozens were missing after a boat carrying about 100 migrants sank; at least four bodies were recovered."),
    ("Americas", "Haiti's toll", "The UN documented 4,595 killed and 2,050 injured in Haiti's gang violence between January and October."),
    ("MidEast", "Return crossing", "Eighty-four Syrian refugees went home from Lebanon through the reopened Abboudiyeh crossing."),
    ("Africa", "Kenya's imports", "Kenya confirmed nine Ebola cases and two deaths, all linked to travel from eastern DR Congo."),
    ("Africa", "125 freed", "Nigerian troops rescued 125 kidnapped people and dismantled camps in operations from 6 to 12 November, the defence headquarters said."),
    ("Africa", "Lungi accords", "A West Africa integration summit in Lungi, Sierra Leone, closed four agreements and launched three regional initiatives."),
]

NUMBERS = [
    ("$81.3bn", "Anthropic's listing, the largest ever"),
    ("$92.52", "Brent crude, per barrel"),
    ("11,536", "DR Congo Ebola cases"),
    ("4,595", "Killed in Haiti this year"),
    ("26bn km", "Voyager 1 from Earth"),
    ("$190.4m", "Van Gogh, a record"),
]


# ------------------------------------------------------------------- text ----
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


def draw_block(draw, xy, text, font, width, fill, leading, max_lines):
    x, y = xy
    lines = wrap(draw, text, font, width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# --------------------------------------------------------------- artwork -----
def star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def art_trilateral(img, draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=NAVY)
    r = int(min(h * 0.30, w * 0.115))
    gap = int(r * 0.55)
    cy = y0 + int(h * 0.44)
    cx0 = x0 + w // 2
    centres = [cx0 - (2 * r + gap), cx0, cx0 + (2 * r + gap)]

    for idx in range(3):
        cx = centres[idx]
        size = 2 * r
        disc = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        cd = ImageDraw.Draw(disc)
        if idx == 0:  # United States
            for i in range(13):
                yy = i * size / 13.0
                cd.rectangle([0, yy, size, yy + size / 13.0 + 1],
                             fill=(178, 34, 52) if i % 2 == 0 else (245, 243, 236))
            cd.rectangle([0, 0, int(size * 0.45), int(size * 0.54)], fill=(24, 42, 74))
            for row in range(4):
                for col in range(5):
                    sx = int(size * 0.04 + col * size * 0.082)
                    sy = int(size * 0.05 + row * size * 0.115)
                    cd.ellipse([sx, sy, sx + max(2, size // 22), sy + max(2, size // 22)],
                               fill=(245, 243, 236))
        elif idx == 1:  # China
            cd.rectangle([0, 0, size, size], fill=(190, 30, 40))
            star(cd, int(size * 0.32), int(size * 0.32), int(size * 0.17), (250, 220, 90))
            for ox, oy in ((0.60, 0.12), (0.74, 0.27), (0.74, 0.47), (0.60, 0.60)):
                star(cd, int(size * ox), int(size * oy), max(2, int(size * 0.055)),
                     (250, 220, 90))
        else:  # Russia
            for i, col in enumerate(((236, 235, 232), (28, 50, 120), (190, 30, 40))):
                cd.rectangle([0, int(i * size / 3.0), size, int((i + 1) * size / 3.0) + 1],
                             fill=col)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
        disc.putalpha(mask)
        img.paste(disc, (cx - r, cy - r), disc)

    ty = cy + r + int(h * 0.10)
    draw.line([x0 + int(w * 0.12), ty, x1 - int(w * 0.12), ty], fill=GOLD, width=2)
    draw.text((x0 + int(w * 0.12), ty + 5), "US   \u00b7   CHINA   \u00b7   RUSSIA",
              font=F("sans_cb", 11), fill=(230, 224, 208))


def art_gulf(img, draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(20, 34, 46))
    draw.rectangle([x0, y0 + int(h * 0.52), x1, y1], fill=(26, 62, 86))
    draw.polygon([(x0, y0 + int(h * 0.24)), (x0 + int(w * 0.26), y0 + int(h * 0.16)),
                  (x0 + int(w * 0.36), y0 + int(h * 0.60)), (x0 + int(w * 0.14), y0 + int(h * 0.68)),
                  (x0, y0 + int(h * 0.64))], fill=(132, 112, 78))
    draw.polygon([(x1, y0 + int(h * 0.10)), (x1 - int(w * 0.30), y0 + int(h * 0.20)),
                  (x1 - int(w * 0.22), y0 + int(h * 0.64)), (x1, y0 + int(h * 0.70))],
                 fill=(132, 112, 78))
    for i in range(3):
        sx = x1 - int(w * 0.26)
        sy = y0 + int(h * (0.26 + i * 0.09))
        ex = x0 + int(w * (0.18 + i * 0.06))
        ey = y0 + int(h * (0.52 + i * 0.10))
        mx, my = (sx + ex) // 2, min(sy, ey) - int(h * 0.22)
        pts = []
        for k in range(0, 19):
            t = k / 18.0
            pts.append(((1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * ex,
                        (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t * t * ey))
        draw.line(pts, fill=(228, 78, 64), width=2)
        draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=(238, 96, 80))
    for bx, by in ((x0 + int(w * 0.20), y0 + int(h * 0.58)),
                   (x0 + int(w * 0.28), y0 + int(h * 0.66))):
        draw.rectangle([bx - 3, by - 3, bx + 3, by + 3], fill=(246, 244, 236))
    draw.text((x0 + 8, y1 - 17), "QESHM \u2192 AL SALEM \u00b7 BAHRAIN \u00b7 RIYADH",
              font=F("sans_cb", 10), fill=(234, 228, 212))


def art_icj(img, draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(228, 224, 213))
    base_y = y1 - int(h * 0.26)
    for i in range(3):
        draw.rectangle([x0 + int(w * (0.08 - i * 0.018)), base_y + i * 6,
                        x1 - int(w * (0.08 - i * 0.018)), base_y + i * 6 + 6],
                       fill=(148, 140, 124))
    n = 6
    col_top = y0 + int(h * 0.34)
    span = int(w * 0.64)
    left = x0 + (w - span) // 2
    step = span // n
    for i in range(n):
        cx = left + i * step + max(2, step // 8)
        cw_ = max(4, int(step * 0.42))
        draw.rectangle([cx, col_top, cx + cw_, base_y - 2], fill=(240, 236, 226))
        draw.rectangle([cx - 3, col_top - 4, cx + cw_ + 3, col_top], fill=(212, 206, 194))
    draw.rectangle([left - 8, col_top - 14, left + span + 8, col_top - 5], fill=(204, 198, 186))
    draw.polygon([(left - 14, col_top - 16), (left + span + 14, col_top - 16),
                  (left + span // 2, y0 + int(h * 0.12))], fill=(232, 228, 218))
    sx, sy = x0 + w // 2, y0 + int(h * 0.80)
    sc = int(h * 0.15)
    draw.line([sx, sy - sc, sx, sy + int(sc * 0.40)], fill=INK, width=3)
    draw.line([sx - sc, sy - int(sc * 0.60), sx + sc, sy - int(sc * 0.60)], fill=INK, width=3)
    for side in (-1, 1):
        px = sx + side * sc
        draw.line([px, sy - int(sc * 0.60), px, sy - int(sc * 0.28)], fill=INK, width=2)
        draw.arc([px - 13, sy - int(sc * 0.30), px + 13, sy - int(sc * 0.02)], 0, 180,
                 fill=INK, width=2)
    draw.line([sx - int(sc * 0.50), sy + int(sc * 0.40), sx + int(sc * 0.50),
               sy + int(sc * 0.40)], fill=INK, width=4)
    draw.text((x0 + 8, y1 - 17), "PEACE PALACE, THE HAGUE", font=F("sans_cb", 10),
              fill=(58, 54, 48))


ART = {"trilateral": art_trilateral, "gulf": art_gulf, "icj": art_icj}


# ------------------------------------------------------------------ fit -----
def measure_briefs(draw, body_size, cols, area_top):
    """Return per-column block lists and the tallest column, for a trial size."""
    cgap = 9
    cw = (COLW - (cols - 1) * cgap) // cols
    hl_font = F("cond_b", body_size + 2)
    body_font = F("serif", body_size)
    hl_lead = body_size + 3
    body_lead = body_size + 1.5

    blocks = []
    for region, head, body in BRIEFS:
        hl = wrap(draw, head, hl_font, cw - 7)
        bl = wrap(draw, body, body_font, cw - 7)
        height = len(hl) * hl_lead + len(bl) * body_lead + 5
        blocks.append((region, hl, bl, height))

    per_col = [[] for _ in range(cols)]
    heights = [0.0] * cols
    for blk in blocks:
        tgt = min(range(cols), key=lambda i: heights[i])
        per_col[tgt].append(blk)
        heights[tgt] += blk[3]
    tallest = max(heights)
    return per_col, heights, tallest, cw, cgap, hl_font, body_font, hl_lead, body_lead


# ------------------------------------------------------------------ page ----
def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = MARGIN
    draw.rectangle([MARGIN, y, W - MARGIN, y + 4], fill=RED)
    y += 11

    draw.text((MARGIN, y), "THE WORLD IN ONE DAY", font=F("sans_b", 15), fill=INK)
    draw.text((W - MARGIN, y + 2), "THE DAY'S NEWS ON ONE PAGE  \u00b7  No. 324",
              font=F("sans_cb", 11), fill=INK_SOFT, anchor="ra")
    y += 22

    draw.text((MARGIN - 3, y), "19 NOVEMBER 2026", font=F("cond_b", 84), fill=INK)
    y += 92
    draw.text((MARGIN, y), "THURSDAY", font=F("sans_b", 14), fill=RED)
    draw.text((MARGIN + 92, y + 1),
              "three nuclear powers met, a court ruled on genocide, and Iran struck again",
              font=F("serif", 13), fill=INK_SOFT)
    y += 22
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 2
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    y += 8

    # numbers strip
    cell = COLW // len(NUMBERS)
    for i, (big, cap) in enumerate(NUMBERS):
        cx = MARGIN + i * cell
        draw.text((cx, y), big, font=F("cond_b", 26), fill=RED)
        cy = y + 29
        for line in wrap(draw, cap, F("serif", 8), cell - 12)[:2]:
            draw.text((cx, cy), line, font=F("serif", 8), fill=INK_SOFT)
            cy += 9
        if i:
            draw.line([cx - 7, y + 2, cx - 7, y + 42], fill=RULE, width=1)
    y += 46
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    y += 7

    # three illustrated leads
    gap = 13
    lead_w = (COLW - 2 * gap) // 3
    art_h = 104
    lead_bottom = 0
    for i, lead in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + gap)
        ART[lead["art"]](img, draw, [lx, y, lx + lead_w, y + art_h])
        ty = y + art_h + 5
        draw.text((lx, ty), lead["kicker"], font=F("sans_b", 9), fill=RED)
        ty += 13
        for line in wrap(draw, lead["headline"], F("cond_b", 19), lead_w)[:2]:
            draw.text((lx, ty), line, font=F("cond_b", 19), fill=INK)
            ty += 20
        ty += 2
        ty = draw_block(draw, (lx, ty), lead["deck"], F("serif", 9), lead_w, INK_SOFT, 11, 6)
        lead_bottom = max(lead_bottom, ty)
        if i:
            draw.line([lx - gap // 2, y, lx - gap // 2, y + art_h + 148], fill=RULE, width=1)

    y = lead_bottom + 8
    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=1)
    y += 6

    # second leads
    half = (COLW - 14) // 2
    sec_bottom = y
    for i, sec in enumerate(SECOND_LEADS):
        sx = MARGIN + i * (half + 14)
        draw.text((sx, y), sec["kicker"], font=F("sans_b", 8), fill=TEAL)
        ty = y + 11
        for line in wrap(draw, sec["headline"], F("cond_b", 16), half)[:2]:
            draw.text((sx, ty), line, font=F("cond_b", 16), fill=INK)
            ty += 17
        ty += 1
        ty = draw_block(draw, (sx, ty), sec["deck"], F("serif", 9), half, INK_SOFT, 10.5, 4)
        sec_bottom = max(sec_bottom, ty)
        if i:
            draw.line([sx - 7, y, sx - 7, y + 82], fill=RULE, width=1)
    y = sec_bottom + 7

    # region index, counted from the story list itself
    counts = dict((r, 0) for r in REGIONS)
    for lead in LEADS:
        counts[lead["region"]] += 1
    for sec in SECOND_LEADS:
        counts[sec["region"]] += 1
    for region, _, _ in BRIEFS:
        counts[region] += 1
    total = sum(counts.values())

    draw.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 6
    tx = MARGIN
    draw.text((tx, y + 1), "INSIDE:", font=F("sans_b", 10), fill=INK)
    tx += 50
    for region in REGIONS:
        label = "%s %d" % (region.upper(), counts[region])
        tw = draw.textlength(label, font=F("sans_cb", 10))
        draw.rectangle([tx, y, tx + tw + 11, y + 15], fill=REGION_COLOURS[region])
        draw.text((tx + 6, y + 2), label, font=F("sans_cb", 10), fill=(250, 248, 240))
        tx += tw + 18
    draw.text((W - MARGIN, y + 1), "%d STORIES" % total, font=F("sans_b", 10), fill=RED,
              anchor="ra")
    y += 22
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    y += 6

    # brief stack: fit the body size and column count to the space that is left
    footer_top = BOTTOM - 12
    avail = footer_top - y - 4
    best = None
    for cols in (5, 4):
        for size in (9, 8.5, 8, 7.5, 7, 6.5):
            trial = measure_briefs(draw, size, cols, y)
            if trial[2] <= avail:
                best = (cols, size, trial)
                break
        if best:
            break
    if best is None:
        best = (4, 6.5, measure_briefs(draw, 6.5, 4, y))

    cols, size, trial = best
    per_col, heights, tallest, cw, cgap, hl_font, body_font, hl_lead, body_lead = trial

    for ci in range(cols):
        cx = MARGIN + ci * (cw + cgap)
        by = y
        for region, hl, bl, height in per_col[ci]:
            draw.rectangle([cx, by + 1, cx + 2, by + 7], fill=REGION_COLOURS[region])
            for line in hl:
                draw.text((cx + 6, by), line, font=hl_font, fill=INK)
                by += hl_lead
            for line in bl:
                draw.text((cx + 6, by), line, font=body_font, fill=INK_SOFT)
                by += body_lead
            by += 5
        if ci:
            draw.line([cx - cgap // 2, y, cx - cgap // 2, footer_top - 3], fill=HAIR, width=1)

    # footer
    draw.line([MARGIN, footer_top - 3, W - MARGIN, footer_top - 3], fill=INK, width=1)
    draw.text((MARGIN, footer_top + 1),
              "Compiled from Xinhua, Reuters, AP, BBC, Al Jazeera and Kyodo reports of 19 November 2026",
              font=F("serif", 8), fill=INK_SOFT)
    draw.text((W - MARGIN, footer_top + 1), "19 NOVEMBER 2026", font=F("sans_cb", 8),
              fill=RED, anchor="ra")

    img.save(out_path, "PNG", optimize=True)
    return {"path": out_path, "bytes": os.path.getsize(out_path), "cols": cols,
            "body_size": size, "stories": total, "counts": counts,
            "tallest_column": round(tallest, 1), "avail": avail}


if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    info = build(dest)
    print(info)
