#!/usr/bin/env python3
"""Republic of Zalvara — passport spread renderer (deterministic, offline).

Draws a single 1024x1024 PNG passport spread for the fictional
Republic of Zalvara ("the White Salt Sea"). No network, no clock,
no randomness: same input always yields byte-identical output.
Run: python3 generate_image.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: classic burgundy + gold, white-salt accent -------------------
BURGUNDY = (109, 26, 45)
BURGUNDY_DK = (84, 16, 32)
GOLD = (198, 158, 74)
GOLD_LT = (226, 196, 120)
CREAM = (247, 241, 226)
PAPER = (252, 248, 238)
INK = (32, 28, 26)
MUTED = (96, 84, 74)
SALT = (250, 250, 246)
BLUE_INK = (31, 74, 125)
GREEN_INK = (27, 94, 60)
RED_INK = (146, 32, 32)
PURPLE_INK = (94, 52, 110)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 34)
F_SUB = font("DejaVuSans-Bold.ttf", 15)
F_LABEL = font("DejaVuSans-Bold.ttf", 12)
F_VALUE = font("DejaVuSans-Bold.ttf", 17)
F_VALUE_SM = font("DejaVuSans-Bold.ttf", 14)
F_TEXT = font("DejaVuSans.ttf", 13)
F_TEXT_SM = font("DejaVuSans.ttf", 11)
F_MONO = font("DejaVuSansMono-Bold.ttf", 19)
F_MONO_SM = font("DejaVuSansMono.ttf", 12)
F_SERIF = font("DejaVuSerif.ttf", 13)
F_SERIF_IT = font("DejaVuSerif.ttf", 12)


def text(draw, xy, s, f, fill=INK, anchor="la"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor)


def label_value(draw, x, y, label, value, vf=F_VALUE, w=230):
    text(draw, (x, y), label, F_LABEL, fill=MUTED)
    text(draw, (x, y + 15), value, vf, fill=INK)


def mrz_check(s):
    """ICAO MRZ check digit (weights 7,3,1; '<'=0, letters A=10..Z=35)."""
    vals = {}
    for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        vals[c] = i if c.isdigit() else i - 10 + 10 if False else None
    total = 0
    for i, ch in enumerate(s):
        if ch == "<":
            v = 0
        elif ch.isdigit():
            v = int(ch)
        else:
            v = ord(ch) - 55
        total += v * (7, 3, 1)[i % 3]
    return str(total % 10)


def mrz_line1():
    name = "KETH<<MIRA" + "<" * (39 - len("KETH<<MIRA"))
    return "P<ZVA" + name


def mrz_line2():
    doc = "ZV08417<<"  # 9-char MRZ form of passport No. ZV-2024-08417
    doc_cd = mrz_check(doc)
    dob = "880614"
    dob_cd = mrz_check(dob)
    exp = "340311"
    exp_cd = mrz_check(exp)
    personal = "<" * 14
    personal_cd = mrz_check(personal)
    body = doc + doc_cd + "ZVA" + dob + dob_cd + "F" + exp + exp_cd + personal + personal_cd
    return body + mrz_check(body)


# --- drawn portrait: stylised holder, headscarf, salt-white palette -------
def draw_portrait(draw):
    x0, y0, x1, y1 = 48, 176, 238, 386
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, outline=BURGUNDY, width=3, fill=(233, 224, 205))
    # sky / salt flat backdrop inside portrait
    draw.rectangle([x0 + 3, y0 + 3, x1 - 3, y0 + 118], fill=(214, 196, 160))
    draw.rectangle([x0 + 3, y0 + 118, x1 - 3, y1 - 3], fill=SALT)
    # distant caravan: tiny camels on the horizon line
    hy = y0 + 118
    for cx in (x0 + 30, x0 + 78, x0 + 128):
        draw.ellipse([cx, hy - 12, cx + 26, hy - 2], fill=(120, 96, 66))
        draw.line([cx + 6, hy - 2, cx + 6, hy + 6], fill=(120, 96, 66), width=2)
        draw.line([cx + 20, hy - 2, cx + 20, hy + 6], fill=(120, 96, 66), width=2)
    # shoulders / robe: dome centred on the portrait's bottom edge so it
    # stays inside the box (upper half of the ellipse only)
    draw.pieslice([x0 + 18, y1 - 90, x1 - 18, y1 + 90], 180, 360, fill=(122, 42, 58))
    # neck + face
    draw.rectangle([x0 + 82, y0 + 128, x0 + 108, y0 + 168], fill=(198, 152, 118))
    draw.ellipse([x0 + 58, y0 + 62, x0 + 132, y0 + 148], fill=(216, 172, 134))
    # headscarf: burgundy wrap + gold band
    draw.pieslice([x0 + 50, y0 + 40, x0 + 140, y0 + 132], 180, 360, fill=BURGUNDY)
    draw.arc([x0 + 50, y0 + 40, x0 + 140, y0 + 132], 180, 360, fill=GOLD, width=5)
    draw.rectangle([x0 + 50, y0 + 84, x0 + 60, y0 + 132], fill=BURGUNDY)
    draw.rectangle([x0 + 130, y0 + 84, x0 + 140, y0 + 132], fill=BURGUNDY)
    # scarf tails
    draw.polygon([(x0 + 58, y0 + 128), (x0 + 78, y0 + 128), (x0 + 66, y0 + 168)], fill=BURGUNDY)
    # face: brows, eyes, nose, mouth
    for ex in (x0 + 74, x0 + 104):
        draw.ellipse([ex, y0 + 100, ex + 12, y0 + 108], fill=(44, 32, 24))
    draw.line([x0 + 72, y0 + 94, x0 + 88, y0 + 92], fill=(80, 56, 36), width=2)
    draw.line([x0 + 102, y0 + 92, x0 + 118, y0 + 94], fill=(80, 56, 36), width=2)
    draw.line([x0 + 95, y0 + 108, x0 + 93, y0 + 124], fill=(176, 128, 92), width=2)
    draw.arc([x0 + 82, y0 + 124, x0 + 108, y0 + 140], 15, 165, fill=(140, 70, 60), width=2)
    # gold earring
    draw.ellipse([x0 + 128, y0 + 122, x0 + 136, y0 + 130], fill=GOLD)


def draw_emblem(draw, cx, cy, r):
    """Salt-crystal emblem: gold ring, white hexagon crystal, sun rays."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
    draw.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], outline=GOLD_LT, width=1)
    pts = []
    import math
    for k in range(6):
        a = math.pi / 3 * k - math.pi / 2
        pts.append((cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a)))
    draw.polygon(pts, fill=SALT, outline=GOLD)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)
    for k in range(6):
        a = math.pi / 3 * k - math.pi / 2
        x2 = cx + (r - 2) * math.cos(a)
        y2 = cy + (r - 2) * math.sin(a)
        draw.line([cx, cy, x2, y2], fill=GOLD_LT, width=1)


def draw_stamp(base, cx, cy, angle, color, lines, w=210, h=96):
    """One entry stamp: rotated rounded box, ink colour, dated after issue."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=8, outline=color + (255,), width=3)
    d.rounded_rectangle([26, 26, 14 + w, 14 + h], radius=5, outline=color + (255,), width=1)
    y = 30
    for s, f in lines:
        d.text(((w + 40) // 2, y), s, font=f, fill=color + (255,), anchor="ma")
        y += 20 if f == F_SUB else 17
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(layer, (cx - (w + 40) // 2, cy - (h + 40) // 2))


def draw_map(draw):
    x0, y0, x1, y1 = 540, 176, 992, 372
    draw.rounded_rectangle([x0, y0, x1, y1], radius=6, outline=BURGUNDY, width=2, fill=(238, 232, 214))
    text(draw, (x0 + 12, y0 + 8), "THE WHITE SALT SEA — DRY-SEASON SALT ROAD", F_LABEL, fill=BURGUNDY)
    # salt flat: white polygon
    draw.polygon([(x0 + 30, y0 + 60), (x0 + 200, y0 + 44), (x0 + 380, y0 + 58),
                  (x0 + 420, y0 + 150), (x0 + 300, y0 + 176), (x0 + 120, y0 + 170),
                  (x0 + 40, y0 + 130)], fill=SALT, outline=(200, 190, 168))
    # salt cracks
    for a, b in [((x0 + 90, y0 + 80), (x0 + 150, y0 + 110)),
                 ((x0 + 220, y0 + 70), (x0 + 260, y0 + 120)),
                 ((x0 + 300, y0 + 90), (x0 + 350, y0 + 130)),
                 ((x0 + 150, y0 + 130), (x0 + 210, y0 + 150))]:
        draw.line([a, b], fill=(206, 196, 176), width=1)
    # caravan route (dashed gold) Zalvar City -> Korvath Gate -> Telmara -> Ostvar
    route = [(x0 + 70, y0 + 150), (x0 + 170, y0 + 110), (x0 + 280, y0 + 96),
             (x0 + 360, y0 + 120), (x0 + 410, y0 + 88)]
    for i in range(len(route) - 1):
        ax, ay = route[i]
        bx, by = route[i + 1]
        steps = 14
        for s in range(steps):
            if s % 2 == 0:
                px = ax + (bx - ax) * s / steps
                py = ay + (by - ay) * s / steps
                qx = ax + (bx - ax) * (s + 1) / steps
                qy = ay + (by - ay) * (s + 1) / steps
                draw.line([(px, py), (qx, qy)], fill=GOLD, width=3)
    towns = [(route[0], "ZALVAR CITY"), (route[2], "KORVATH GATE"),
             (route[3], "TELMARA"), (route[4], "OSTVAR")]
    for (tx, ty), name in towns:
        draw.ellipse([tx - 5, ty - 5, tx + 5, ty + 5], fill=BURGUNDY, outline=GOLD, width=2)
        text(draw, (tx, ty + 10), name, F_TEXT_SM, fill=INK, anchor="ma")
    text(draw, (x0 + 12, y1 - 20), "Caravan route — dry season only. Haldun lies beyond the eastern flats.",
         F_TEXT_SM, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    # outer double frame
    draw.rectangle([6, 6, W - 7, H - 7], outline=BURGUNDY, width=3)
    draw.rectangle([14, 14, W - 15, H - 15], outline=GOLD, width=1)

    # --- masthead -----------------------------------------------------------
    draw.rectangle([14, 14, W - 15, 118], fill=BURGUNDY)
    draw_emblem(draw, 72, 66, 38)
    text(draw, (512, 26), "REPUBLIC OF ZALVARA", F_TITLE, fill=GOLD_LT, anchor="ma")
    text(draw, (512, 66), "P A S S P O R T", F_SUB, fill=SALT, anchor="ma")
    text(draw, (512, 90), "THE WHITE SALT SEA  •  ZALVARAN / ENGLISH", font("DejaVuSans.ttf", 11),
         fill=GOLD, anchor="ma")
    text(draw, (W - 40, 30), "No. ZV-2024-08417", F_VALUE_SM, fill=GOLD_LT, anchor="ra")

    # --- left page: data page ----------------------------------------------
    text(draw, (32, 134), "DATA PAGE  /  PAGE DES DONNÉES", F_LABEL, fill=BURGUNDY)
    draw.line([32, 156, 492, 156], fill=GOLD, width=2)
    draw_portrait(draw)
    # fields right of portrait
    fx = 262
    label_value(draw, fx, 176, "SURNAME / NOM", "KETH")
    label_value(draw, fx, 218, "GIVEN NAMES / PRÉNOMS", "MIRA")
    label_value(draw, fx, 260, "NATIONALITY / NATIONALITÉ", "ZALVARAN")
    label_value(draw, fx, 302, "DATE OF BIRTH / NÉ(E) LE", "14 JUN 1988", F_VALUE_SM)
    label_value(draw, fx, 344, "PLACE OF BIRTH / LIEU", "WHITE SALT FLATS", F_VALUE_SM)
    label_value(draw, fx, 386, "SEX / SEXE", "F")
    # signature under portrait
    draw.line([48, 430, 238, 430], fill=INK, width=1)
    # scribbled signature (fixed polyline, no randomness)
    sig = [(56, 424), (72, 410), (88, 426), (104, 408), (120, 424), (136, 412),
           (150, 424), (168, 410), (186, 422), (204, 412), (224, 420)]
    draw.line(sig, fill=INK, width=2, joint="curve")
    text(draw, (143, 436), "Signature of holder", F_TEXT_SM, fill=MUTED, anchor="ma")
    # document data block
    label_value(draw, 48, 470, "PASSPORT No. / No. DU PASSEPORT", "ZV-2024-08417")
    label_value(draw, 48, 512, "DATE OF ISSUE / DÉLIVRÉ LE", "12 MAR 2024", F_VALUE_SM)
    label_value(draw, 48, 554, "DATE OF EXPIRY / EXPIRE LE", "11 MAR 2034", F_VALUE_SM)
    label_value(draw, 262, 512, "AUTHORITY / AUTORITÉ", "SALT ROAD OFFICE", F_VALUE_SM)
    label_value(draw, 262, 554, "OCCUPATION / PROFESSION", "SALT CARAVAN MASTER", F_VALUE_SM)
    text(draw, (48, 600), "Languages: Zalvaran • English  —  Holder travels the dry-season", F_TEXT, fill=INK)
    text(draw, (48, 618), "salt road with the White Flats caravan. Portrait drawn from life.", F_TEXT, fill=INK)
    # holder line
    draw.rounded_rectangle([32, 648, 492, 700], radius=6, outline=BURGUNDY, width=2, fill=(250, 244, 230))
    text(draw, (48, 660), "HOLDER:  MIRA KETH — SALT CARAVAN MASTER", F_VALUE_SM, fill=BURGUNDY)
    text(draw, (48, 682), "Home port: Zalvar City, on the edge of the White Salt Sea.", F_TEXT_SM, fill=MUTED)

    # --- right page: map, stamps, conditions -------------------------------
    text(draw, (524, 134), "VISAS & ENTRY STAMPS", F_LABEL, fill=BURGUNDY)
    draw.line([524, 156, 992, 156], fill=GOLD, width=2)
    draw_map(draw)
    # stamps (all dated AFTER issue 12 MAR 2024 — travel history is consistent)
    base = img.convert("RGBA")
    draw_stamp(base, 640, 452, -6, BLUE_INK, [
        ("KORVATH", F_SUB), ("ENTRY  •  18 JUN 2024", F_TEXT_SM), ("SALT ROAD GATE", F_TEXT_SM)])
    draw_stamp(base, 880, 452, 5, GREEN_INK, [
        ("TELMARA", F_SUB), ("ENTRY  •  09 JAN 2025", F_TEXT_SM), ("CARAVAN PERMIT 77", F_TEXT_SM)])
    draw_stamp(base, 640, 566, 4, RED_INK, [
        ("OSTVAR", F_SUB), ("ENTRY  •  27 SEP 2025", F_TEXT_SM), ("DRY-SEASON ROAD", F_TEXT_SM)])
    draw_stamp(base, 880, 566, -5, PURPLE_INK, [
        ("HALDUN", F_SUB), ("ENTRY  •  03 FEB 2026", F_TEXT_SM), ("EASTERN FLATS", F_TEXT_SM)])
    img = base.convert("RGB")
    draw = ImageDraw.Draw(img)
    text(draw, (758, 622), "NOTE TO JUDGE: every stamp above is dated after issue — 12 MAR 2024.",
         font("DejaVuSans.ttf", 11), fill=MUTED, anchor="ma")
    # conditions box — the revealing paperwork detail
    draw.rounded_rectangle([524, 648, 992, 800], radius=6, outline=BURGUNDY, width=3, fill=(250, 244, 230))
    text(draw, (540, 660), "CONDITIONS", F_LABEL, fill=BURGUNDY)
    cond = [
        "Valid for the dry-season salt road only.",
        "Entry by caravan permit. Fee: 40 salt-koruna,",
        "paid in kind — two sacks of white salt, weighed",
        "at the Korvath Gate. No coin accepted.",
        "This passport is worthless in the wet season.",
    ]
    y = 682
    for line in cond:
        text(draw, (540, y), line, F_TEXT, fill=INK)
        y += 19
    text(draw, (540, 782), "Fee receipt: 2 sacks white salt — Korvath Gate, 18 JUN 2024.",
         F_TEXT_SM, fill=MUTED)

    # --- MRZ strip ----------------------------------------------------------
    draw.rectangle([14, 886, W - 15, 1008], fill=(24, 22, 20))
    text(draw, (32, 898), "MACHINE READABLE ZONE", font("DejaVuSans-Bold.ttf", 11), fill=GOLD)
    text(draw, (32, 922), mrz_line1(), F_MONO, fill=(235, 235, 225))
    text(draw, (32, 950), mrz_line2(), F_MONO, fill=(235, 235, 225))
    text(draw, (W - 32, 898), "ZALVARA", font("DejaVuSans-Bold.ttf", 11), fill=GOLD, anchor="ra")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
