#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261124.

Build-time script only: it renders the newspaper front page with Pillow
from the system fonts and writes entry.png beside it. The graded entry is
main.py, which only copies entry.png to the output directory (stdlib only,
no network, deterministic). Run: python3 gen_image.py

Content: 32 verified stories of Tuesday 24 November 2026 — lead: Iran
says three oil tankers hit mines and caught fire in the Strait of
Hormuz; 4 feature panels (Russian strike on Zaporizhzhia; Sheikh Hasina
plans her return to Bangladesh; Australia's 5%-of-revenue tech fines;
CAS to rule on Senegal's AFCON title appeal) + 27 briefs across six
continents, all events of / first reported on 24 Nov 2026.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
NAVY2 = (27, 45, 82)
GOLD = (201, 162, 39)
RED = (185, 28, 28)
TEAL = (6, 120, 90)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
RULE = (214, 204, 178)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


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


def one_line(draw, text, fnt, max_w, what):
    """Wrap and assert the text fits on exactly one line."""
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) == 1, (what, lines)
    return lines[0]


def draw_tanker(d, cx, cy, s):
    """Simple oil tanker icon, centred at (cx, cy), size s."""
    w, h = int(s * 1.6), int(s * 0.55)
    x0, y0 = cx - w // 2, cy - h // 2
    # hull
    d.polygon([(x0, y0 + h * 0.35), (x0 + w, y0 + h * 0.35),
               (x0 + w - 12, y0 + h), (x0 + 12, y0 + h)], fill=NAVY)
    # deck tanks
    d.rectangle([x0 + 18, y0, x0 + w - 40, y0 + h * 0.35], fill=(60, 80, 120))
    # bridge tower
    d.rectangle([x0 + w - 34, y0 - h * 0.55, x0 + w - 8, y0 + h * 0.35], fill=NAVY2)
    # flame above a tank
    fx, fy = x0 + w // 2 - 10, y0 - h * 0.75
    d.polygon([(fx, fy + 26), (fx + 8, fy + 8), (fx + 16, fy + 20),
               (fx + 24, fy), (fx + 30, fy + 26)], fill=(230, 120, 20))
    d.polygon([(fx + 6, fy + 26), (fx + 13, fy + 12), (fx + 20, fy + 26)],
              fill=(255, 200, 40))
    # waves
    d.arc([x0 - 6, y0 + h - 4, x0 + w + 6, y0 + h + 16], 0, 180, fill=TEAL, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    f_title = font(SERIF, 56)
    t = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(t, font=f_title)) / 2, 14), t, font=f_title, fill=WHITE)
    f_date = font(SANS_B, 23)
    t2 = "TUESDAY, 24 NOVEMBER 2026  •  32 STORIES  •  SIX CONTINENTS"
    if d.textlength(t2, font=f_date) > 990:
        f_date = font(SANS_B, 21)
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 80), t2, font=f_date, fill=GOLD)

    # ---- lead story: three tankers ablaze in Hormuz ----
    x0, y0, x1, y1 = 28, 134, 996, 318
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD, outline=(200, 190, 160), width=2)
    f_kick = font(SANS_B, 19)
    kick = "LEAD STORY  •  MIDDLE EAST"
    d.rectangle([x0 + 14, y0 + 14, x0 + 14 + d.textlength(kick, font=f_kick) + 20, y0 + 40], fill=RED)
    d.text((x0 + 24, y0 + 17), kick, font=f_kick, fill=WHITE)
    f_head = font(SERIF, 38)
    d.text((x0 + 16, y0 + 46), "Three tankers ablaze", font=f_head, fill=INK)
    d.text((x0 + 16, y0 + 90), "in the Strait of Hormuz", font=f_head, fill=INK)
    f_body = font(SANS, 20)
    body = ("Iran says three oil tankers hit naval mines and caught fire; "
            "no ship names given, US has not confirmed it.")
    lines = wrap(d, body, f_body, 680)
    assert len(lines) <= 2, lines
    yy = y0 + 134
    for ln in lines[:2]:
        d.text((x0 + 16, yy), ln, font=f_body, fill=(40, 40, 40))
        yy += 24
    # tanker icon, right side
    draw_tanker(d, 880, 220, 120)

    # ---- four feature panels, 2 cols x 2 rows ----
    panels = [
        ("UKRAINE  •  WAR", RED,
         "Zaporizhzhia hit overnight",
         "Russian attack kills 2, wounds 22, including two children.", "blast"),
        ("BANGLADESH  •  POLITICS", NAVY2,
         "Hasina plans return home",
         "Ousted PM to fly back on 16 December after two years in exile.", "plane"),
        ("AUSTRALIA  •  TECH", NAVY2,
         "Big Tech faces 5% fines",
         "Australia to fine tech firms up to 5% of global revenue.", "gavel"),
        ("SPORT  •  FOOTBALL", TEAL,
         "CAS rules on Senegal today",
         "Court decides appeal over stripped Africa Cup of Nations title.", "trophy"),
    ]
    px, py = 28, 330
    pw, ph, gap = 478, 144, 12
    f_pk = font(SANS_B, 16)
    f_ph = font(SERIF, 26)
    f_pb = font(SANS, 18)
    for i, (kick, col, head, body, icon) in enumerate(panels):
        cx = px + (i % 2) * (pw + gap)
        cy = py + (i // 2) * (ph + gap)
        d.rounded_rectangle([cx, cy, cx + pw, cy + ph], radius=10, fill=CARD,
                            outline=(200, 190, 160), width=2)
        d.rectangle([cx, cy, cx + pw, cy + 6], fill=col)
        d.text((cx + 14, cy + 14), kick, font=f_pk, fill=col)
        hl = wrap(d, head, f_ph, pw - 28)
        assert len(hl) <= 2, (head, hl)
        yy = cy + 40
        for ln in hl[:2]:
            d.text((cx + 14, yy), ln, font=f_ph, fill=INK)
            yy += 31
        bl = wrap(d, body, f_pb, pw - 28)
        assert len(bl) <= 2, (head, bl)
        for ln in bl[:2]:
            d.text((cx + 14, yy), ln, font=f_pb, fill=(40, 40, 40))
            yy += 23
        ix, iy = cx + pw - 44, cy + 32
        if icon == "blast":
            d.polygon([(ix - 6, iy - 14), (ix + 6, iy - 4), (ix + 18, iy - 12),
                       (ix + 12, iy + 2), (ix + 22, iy + 10), (ix + 6, iy + 10),
                       (ix + 2, iy + 22), (ix - 8, iy + 8), (ix - 20, iy + 10),
                       (ix - 12, iy - 2)], fill=(230, 120, 20))
        elif icon == "plane":
            d.polygon([(ix - 28, iy + 6), (ix + 4, iy - 8), (ix + 30, iy - 8),
                       (ix + 30, iy + 2), (ix + 4, iy + 2), (ix - 6, iy + 14),
                       (ix - 12, iy + 14), (ix - 16, iy + 4)], fill=NAVY2)
            d.line([ix - 30, iy + 22, ix + 28, iy + 22], fill=GREY, width=2)
        elif icon == "gavel":
            d.rectangle([ix - 26, iy - 8, ix + 26, iy + 2], fill=NAVY2)
            d.rectangle([ix - 4, iy + 2, ix + 4, iy + 22], fill=NAVY2)
            d.rectangle([ix - 18, iy + 22, ix + 18, iy + 28], fill=GOLD)
        elif icon == "trophy":
            d.polygon([(ix - 14, iy - 12), (ix + 14, iy - 12), (ix + 8, iy + 10),
                       (ix - 8, iy + 10)], fill=GOLD)
            d.rectangle([ix - 4, iy + 10, ix + 4, iy + 20], fill=GOLD)
            d.rectangle([ix - 14, iy + 20, ix + 14, iy + 26], fill=GOLD)
            d.arc([ix - 26, iy - 12, ix - 8, iy + 4], 90, 270, fill=GOLD, width=4)
            d.arc([ix + 8, iy - 12, ix + 26, iy + 4], 270, 90, fill=GOLD, width=4)

    # ---- briefs: 27 one-liners, 3 cols x 9 rows ----
    briefs = [
        ("IRAN", "Qatar PM seeks Iran talks", "After meeting Rubio, Doha pushes talks."),
        ("IRAN", "US hits Iran shadow banks", "Bessent says Tehran is 'panicking'."),
        ("USA", "Trump: speed up executions", "President blasts California's Newsom."),
        ("USA", "Hush-money case revived", "Appeals court backs Trump jurisdiction bid."),
        ("USA", "Trump meets Rutte tomorrow", "NATO chief to visit Florida on Wednesday."),
        ("MARKETS", "Oil near 3-month low", "Brent $88.97 as supply rises, Hormuz risk stays."),
        ("HEALTH", "Typhoid jabs for 50m", "Month-long drive for children."),
        ("TECH", "SoftBank bets $2bn on Intel", "Japanese giant to take a stake in Intel."),
        ("INDIA", "Ex-lawmaker jailed for life", "Revanna sentenced over rape case."),
        ("ASIA", "Thai-Cambodia truce holds", "Border fighting on hold after ceasefire."),
        ("GAZA", "Strikes kill three in Gaza", "Dead include an UNRWA worker."),
        ("RUSSIA", "Moscow warns Finland", "Kyiv says new strikes are being planned."),
        ("ISRAEL", "Flydubai flights return", "Minister approves resumption of flights."),
        ("PHILIPPINES", "First state oil reserve", "Manila acts as Mid-East war rattles markets."),
        ("CANADA", "PM's Trump impersonator", "Carney brings lookalike on stage at gala."),
        ("TECH", "US blacklists Megaspeed", "Chip firm at centre of Nvidia scandal hit."),
        ("TECH", "Kagi launches email", "Google alternative adds an email service."),
        ("NIGERIA", "Borno enrolment doubles", "Schools rebound after years of conflict."),
        ("UN", "UN chief: regulate AI", "World must agree AI rules within a year."),
        ("GEORGIA", "Surrogacy ban planned", "Tbilisi acts over trafficking concerns."),
        ("AUSTRALIA", "AI is foreign policy", "Canberra treats AI as a strategic challenge."),
        ("YEMEN", "Houthi attacks kill 2", "Eight wounded in Taiz, forces say."),
        ("CONGO", "WHO plea over Ebola", "Fighting hinders the fight in the east."),
        ("ZIMBABWE", "Preacher held", "Prominent pastor faces indecent assault case."),
        ("LIBYA", "Erdogan to visit Libya", "First trip there in 15 years planned."),
        ("BRAZIL", "Storm displaces many", "Deadly storm hits a Brazilian town."),
        ("INDIA", "Himalayan flood search", "Army hunts for scores missing after floods."),
    ]
    assert len(briefs) == 27, len(briefs)

    bx0, by0 = 28, 642
    f_bh = font(SANS_B, 18)
    d.text((bx0, by0), "MORE FROM THE DAY", font=f_bh, fill=NAVY)
    f_bs = font(SANS, 16)
    d.text((bx0 + d.textlength("MORE FROM THE DAY  ", font=f_bh), by0 + 2),
           "— 27 briefs, six continents", font=f_bs, fill=GREY)
    d.line([bx0, by0 + 26, 996, by0 + 26], fill=NAVY, width=2)

    cols, rows = 3, 9
    cw = (996 - 28 - (cols - 1) * 12) // cols
    rh = 35
    gy = by0 + 34
    f_b1 = font(SANS_B, 15)
    f_b2 = font(SANS, 13)
    for i, (tag, head, sub) in enumerate(briefs):
        col, row = i % cols, i // cols
        x = bx0 + col * (cw + 12)
        y = gy + row * rh
        line1 = one_line(d, tag + " — " + head, f_b1, cw, ("brief head", head))
        # draw the tag in red, the headline in ink, on the same line
        tag_txt = tag + " — "
        d.text((x, y), tag_txt, font=f_b1, fill=RED)
        d.text((x + d.textlength(tag_txt, font=f_b1), y), head, font=f_b1, fill=INK)
        one_line(d, sub, f_b2, cw, ("brief sub", sub))
        d.text((x, y + 18), sub, font=f_b2, fill=(60, 60, 60))
        if row < rows - 1:
            d.line([x, y + rh - 6, x + cw, y + rh - 6], fill=RULE, width=1)

    # ---- footer ----
    f_f = font(SANS, 17)
    ft = "All events happened or were first reported on Tuesday, 24 November 2026  •  Compiled from wire reports"
    d.text(((W - d.textlength(ft, font=f_f)) / 2, 994), ft, font=f_f, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
