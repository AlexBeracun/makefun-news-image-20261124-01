"""Build the 24 November 2026 front page: THE WORLD IN ONE PAGE.

Draws one 1024x1024 PNG with Pillow. All strings are fixed, there is no
clock, no randomness and no network access, so every run is identical.
Run:  python3 gen_image.py
Output: entry.png, written beside this script.
"""

import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# --- palette -------------------------------------------------------------
PAPER = (248, 244, 233)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
NAVY2 = (27, 45, 82)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
TEAL = (6, 120, 90)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
BODY_GREY = (60, 60, 60)
TAN = (214, 204, 178)
STEEL = (96, 122, 150)
ORANGE = (230, 120, 20)
YELLOW = (245, 200, 40)

W = 1024
H = 1024


def serif(size, bold=True):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that all fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line in lines:
        assert draw.textlength(line, font=font) <= max_width, line
    return lines


def draw_lines(draw, lines, x, y, font, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=font, fill=fill)


def star_points(cx, cy, outer, inner):
    points = []
    for i in range(10):
        radius = outer if i % 2 == 0 else inner
        angle = -math.pi / 2 + i * math.pi / 5
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    return points


def draw_tanker(draw):
    """Flat oil tanker with a flame above one tank and a wave below."""
    # flame above the forward tank
    draw.polygon([(812, 196), (826, 158), (840, 196)], fill=ORANGE)
    draw.polygon([(820, 196), (826, 172), (832, 196)], fill=YELLOW)
    # bridge tower on the right
    draw.rectangle([930, 168, 960, 238], fill=NAVY2)
    draw.rectangle([934, 176, 956, 188], fill=STEEL)
    draw.rectangle([934, 196, 956, 208], fill=STEEL)
    # deck tanks
    draw.rectangle([798, 208, 862, 238], fill=STEEL)
    draw.rectangle([868, 208, 924, 238], fill=STEEL)
    # hull
    draw.polygon([(788, 238), (968, 238), (950, 276), (806, 276)],
                 fill=NAVY)
    # teal wave arc under the hull
    draw.arc([782, 280, 972, 302], 0, 180, fill=TEAL, width=4)


def draw_star_icon(draw, cx, cy):
    draw.polygon(star_points(cx, cy, 26, 11), fill=ORANGE)


def draw_plane_icon(draw, cx, cy):
    draw.polygon([(cx - 30, cy + 4), (cx + 16, cy - 8), (cx + 32, cy - 4),
                  (cx + 16, cy + 2), (cx - 28, cy + 10)], fill=NAVY2)
    draw.polygon([(cx - 8, cy - 2), (cx + 6, cy - 18), (cx + 14, cy - 16),
                  (cx + 2, cy + 0)], fill=NAVY2)
    draw.polygon([(cx - 28, cy + 6), (cx - 20, cy - 8), (cx - 14, cy - 6),
                  (cx - 20, cy + 8)], fill=NAVY2)
    draw.line([(cx - 30, cy + 18), (cx + 30, cy + 18)], fill=NAVY2, width=3)
    draw.line([(cx - 22, cy + 24), (cx + 22, cy + 24)], fill=STEEL, width=2)


def draw_t_icon(draw, cx, cy):
    draw.rectangle([cx - 24, cy - 18, cx + 24, cy - 6], fill=NAVY2)
    draw.rectangle([cx - 7, cy - 6, cx + 7, cy + 16], fill=NAVY2)
    draw.rectangle([cx - 16, cy + 22, cx + 16, cy + 28], fill=GOLD)


def draw_trophy_icon(draw, cx, cy):
    draw.polygon([(cx - 17, cy - 20), (cx + 17, cy - 20),
                  (cx + 11, cy + 2), (cx - 11, cy + 2)], fill=GOLD)
    draw.rectangle([cx - 3, cy + 2, cx + 3, cy + 12], fill=GOLD)
    draw.rectangle([cx - 13, cy + 12, cx + 13, cy + 18], fill=GOLD)
    draw.arc([cx - 30, cy - 22, cx - 8, cy + 2], 90, 270, fill=GOLD, width=4)
    draw.arc([cx + 8, cy - 22, cx + 30, cy + 2], 270, 90, fill=GOLD, width=4)


PANELS = [
    {
        "tag": "UKRAINE \u2022 WAR",
        "tag_color": RED,
        "rule_color": RED,
        "headline": "Zaporizhzhia hit overnight",
        "summary": "Russian attack kills 2, wounds 22, including two children.",
        "icon": "star",
    },
    {
        "tag": "BANGLADESH \u2022 POLITICS",
        "tag_color": NAVY,
        "rule_color": NAVY,
        "headline": "Hasina plans return home",
        "summary": "Ousted PM to fly back on 16 December after two years in exile.",
        "icon": "plane",
    },
    {
        "tag": "AUSTRALIA \u2022 TECH",
        "tag_color": NAVY,
        "rule_color": NAVY,
        "headline": "Big Tech faces 5% fines",
        "summary": "Australia to fine tech firms up to 5% of global revenue.",
        "icon": "tee",
    },
    {
        "tag": "SPORT \u2022 FOOTBALL",
        "tag_color": TEAL,
        "rule_color": TEAL,
        "headline": "CAS rules on Senegal today",
        "summary": "Court decides appeal over stripped Africa Cup of Nations title.",
        "icon": "trophy",
    },
]

ICON_DRAWERS = {
    "star": draw_star_icon,
    "plane": draw_plane_icon,
    "tee": draw_t_icon,
    "trophy": draw_trophy_icon,
}

# tag, headline, summary -- 27 briefs in reading order, column by column
BRIEFS = [
    ("IRAN", "Qatar PM seeks Iran talks",
     "After meeting Rubio, Doha pushes talks."),
    ("USA", "Hush-money case revived",
     "Appeals court backs Trump jurisdiction bid."),
    ("HEALTH", "Typhoid jabs for 50m",
     "Month-long drive for children."),
    ("ASIA", "Thai-Cambodia truce holds",
     "Border fighting on hold after ceasefire."),
    ("ISRAEL", "Flydubai flights return",
     "Minister approves resumption of flights."),
    ("TECH", "US blacklists Megaspeed",
     "Chip firm at centre of Nvidia scandal hit."),
    ("UN", "UN chief: regulate AI",
     "World must agree AI rules within a year."),
    ("YEMEN", "Houthi attacks kill 2",
     "Eight wounded in Taiz, forces say."),
    ("LIBYA", "Erdogan to visit Libya",
     "First trip there in 15 years planned."),
    ("IRAN", "US hits Iran shadow banks",
     "Bessent says Tehran is \u201cpanicking\u201d."),
    ("USA", "Trump meets Rutte tomorrow",
     "NATO chief to visit Florida on Wednesday."),
    ("TECH", "SoftBank bets $2bn on Intel",
     "Japanese giant to take a stake in Intel."),
    ("GAZA", "Strikes kill three in Gaza",
     "Dead include an UNRWA worker."),
    ("PHILIPPINES", "First state oil reserve",
     "Manila acts as Mid-East war rattles trade."),
    ("TECH", "Kagi launches email",
     "Google alternative adds an email service."),
    ("GEORGIA", "Surrogacy ban planned",
     "Tbilisi acts over trafficking concerns."),
    ("CONGO", "WHO plea over Ebola",
     "Fighting hinders the fight in the east."),
    ("BRAZIL", "Storm displaces many",
     "Deadly storm hits a Brazilian town."),
    ("USA", "Trump: speed up executions",
     "President blasts California\u2019s Newsom."),
    ("MARKETS", "Oil near 3-month low",
     "Brent $88.97; supply up, Hormuz risk stays."),
    ("INDIA", "Ex-lawmaker jailed for life",
     "Revanna sentenced over rape case."),
    ("RUSSIA", "Moscow warns Finland",
     "Kyiv says new strikes are being planned."),
    ("CANADA", "PM\u2019s Trump impersonator",
     "Carney brings lookalike on stage at gala."),
    ("NIGERIA", "Borno enrolment doubles",
     "Schools rebound after years of conflict."),
    ("AUSTRALIA", "AI is foreign policy",
     "Canberra treats AI as a strategic challenge."),
    ("ZIMBABWE", "Preacher held",
     "Pastor faces indecent assault case."),
    ("INDIA", "Himalayan flood search",
     "Army hunts for scores missing after floods."),
]


def build():
    assert len(BRIEFS) == 27, len(BRIEFS)
    assert len(PANELS) == 4, len(PANELS)

    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)

    # --- masthead ------------------------------------------------------
    draw.rectangle([0, 0, W, 118], fill=NAVY)
    draw.rectangle([0, 118, W, 122], fill=GOLD)
    title_font = serif(62)
    title = "THE WORLD IN ONE PAGE"
    assert draw.textlength(title, font=title_font) <= W - 40
    draw.text((W // 2, 20), title, font=title_font, fill=WHITE,
              anchor="ma")
    dateline_font = sans(19, bold=True)
    dateline = ("TUESDAY, 24 NOVEMBER 2026 \u2022 32 STORIES "
                "\u2022 SIX CONTINENTS")
    assert draw.textlength(dateline, font=dateline_font) <= W - 40
    draw.text((W // 2, 88), dateline, font=dateline_font, fill=GOLD,
              anchor="ma")

    # --- lead story ----------------------------------------------------
    draw.rounded_rectangle([28, 134, 996, 310], radius=10,
                           fill=WHITE, outline=TAN, width=1)
    tag_font = sans(15, bold=True)
    tag_text = "LEAD STORY \u2022 MIDDLE EAST"
    tag_w = draw.textlength(tag_text, font=tag_font)
    draw.rectangle([40, 146, 40 + tag_w + 24, 174], fill=RED)
    draw.text((52, 151), tag_text, font=tag_font, fill=WHITE)

    head_font = serif(38)
    head_lines = ["Three tankers ablaze", "in the Strait of Hormuz"]
    for line in head_lines:
        assert draw.textlength(line, font=head_font) <= 700, line
    draw.text((44, 178), head_lines[0], font=head_font, fill=INK)
    draw.text((44, 222), head_lines[1], font=head_font, fill=INK)

    body_font = sans(17)
    body = ("Iran says three oil tankers hit naval mines and caught fire; "
            "no ship names given, US has not confirmed it.")
    body_lines = wrap(draw, body, body_font, 690)
    assert len(body_lines) <= 2, body_lines
    draw_lines(draw, body_lines, 44, 270, body_font, BODY_GREY, 22)

    draw_tanker(draw)

    # --- four feature panels -------------------------------------------
    panel_w = 474
    panel_h = 134
    panel_x = [28, 522]
    panel_y = [322, 468]
    panel_tag_font = sans(14, bold=True)
    panel_head_font = serif(23)
    panel_body_font = sans(16)
    for i, panel in enumerate(PANELS):
        x = panel_x[i % 2]
        y = panel_y[i // 2]
        draw.rounded_rectangle([x, y, x + panel_w, y + panel_h], radius=10,
                               fill=WHITE, outline=TAN, width=1)
        draw.rectangle([x + 10, y, x + panel_w - 10, y + 5],
                       fill=panel["rule_color"])
        draw.text((x + 16, y + 14), panel["tag"], font=panel_tag_font,
                  fill=panel["tag_color"])
        head = panel["headline"]
        assert draw.textlength(head, font=panel_head_font) <= 380, head
        draw.text((x + 16, y + 40), head, font=panel_head_font, fill=INK)
        summary_lines = wrap(draw, panel["summary"], panel_body_font, 442)
        assert len(summary_lines) <= 2, summary_lines
        draw_lines(draw, summary_lines, x + 16, y + 76, panel_body_font,
                   BODY_GREY, 21)
        ICON_DRAWERS[panel["icon"]](draw, x + panel_w - 42, y + 40)

    # --- more from the day ----------------------------------------------
    section_font = sans(20, bold=True)
    section = "MORE FROM THE DAY"
    draw.text((28, 618), section, font=section_font, fill=NAVY)
    suffix_font = sans(18)
    suffix_x = 28 + draw.textlength(section, font=section_font) + 10
    draw.text((suffix_x, 619), "\u2014 27 briefs, six continents",
              font=suffix_font, fill=GREY)
    draw.rectangle([28, 646, 996, 648], fill=NAVY)

    brief_head_font = sans(14, bold=True)
    brief_body_font = sans(12)
    col_x = [28, 354, 680]
    col_w = 316
    row_h = 37
    top = 658
    for idx, (tag, headline, summary) in enumerate(BRIEFS):
        col = idx // 9
        row = idx % 9
        x = col_x[col]
        y = top + row * row_h
        head_text = tag + " \u2014 " + headline
        assert draw.textlength(head_text, font=brief_head_font) <= col_w, \
            head_text
        assert draw.textlength(summary, font=brief_body_font) <= col_w, \
            summary
        draw.text((x, y), tag, font=brief_head_font, fill=RED)
        tag_w = draw.textlength(tag, font=brief_head_font)
        draw.text((x + tag_w, y), " \u2014 " + headline,
                  font=brief_head_font, fill=INK)
        draw.text((x, y + 18), summary, font=brief_body_font, fill=GREY)

    # --- footer ---------------------------------------------------------
    footer_font = sans(13)
    footer = ("All events happened or were first reported on Tuesday, "
              "24 November 2026 \u2022 Compiled from wire reports")
    assert draw.textlength(footer, font=footer_font) <= W - 40
    draw.text((W // 2, 998), footer, font=footer_font, fill=GREY,
              anchor="ma")

    out_path = os.path.join(HERE, "entry.png")
    image.save(out_path, "PNG")
    data = open(out_path, "rb").read()
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%d bytes) sha256=%s" % (out_path, len(data), digest))


if __name__ == "__main__":
    build()
