"""Build assets/entry.png (1024x1024 front-page collage) from assets/hero.png.

Deterministic: fixed layout, fixed fonts, fixed text. No network, no
randomness. Run: python3 build_image.py  (from this directory).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
HERO = BASE / "assets" / "hero.png"
OUT = BASE / "assets" / "entry.png"

W, H = 1024, 1024
PAPER = (250, 247, 240)   # newsprint off-white
INK = (15, 15, 15)
RED = (178, 34, 34)
GREY = (90, 88, 82)
RULE = (15, 15, 15)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    cw = W - 2 * mx              # content width = 952

    # ---- Masthead -------------------------------------------------------
    mast = font(SERIF_B, 92)
    d.text((W / 2, 14), "THE WORLD", font=mast, fill=INK, anchor="ma")
    date_f = font(SANS_B, 25)
    d.text((W / 2, 122), "FRIDAY, 13 NOVEMBER 2026  ·  THE DAY IN ONE IMAGE",
           font=date_f, fill=INK, anchor="ma")
    d.line([(mx, 160), (W - mx, 160)], fill=RULE, width=4)
    d.line([(mx, 166), (W - mx, 166)], fill=RULE, width=1)

    # ---- Hero image (cropped to 952 x 360, biased to the lower half
    #      so the chip stays in frame) -----------------------------------
    hero = Image.open(HERO).convert("RGB")
    target_w, target_h = cw, 360
    scale = max(target_w / hero.width, target_h / hero.height)
    nw, nh = int(hero.width * scale + 0.5), int(hero.height * scale + 0.5)
    hero = hero.resize((nw, nh), Image.LANCZOS)
    ox = (nw - target_w) // 2
    oy = int((nh - target_h) * 0.45)
    img.paste(hero.crop((ox, oy, ox + target_w, oy + target_h)), (mx, 176))
    d.rectangle([mx, 176, mx + target_w - 1, 176 + target_h - 1],
                outline=INK, width=2)

    # ---- Hero headline + caption ----------------------------------------
    y = 548
    hl = font(SANS_B, 40)
    y = draw_lines(d, wrap(d, "NVIDIA CHIEF RESIGNS AS SHARES PLUNGE 16%",
                           hl, cw), mx, y, hl, INK, 46)
    cap = font(SANS, 20)
    y = draw_lines(d, wrap(d, "Jensen Huang steps down as chief executive; "
                           "Colette Kress named interim leader.",
                           cap, cw), mx, y + 6, cap, GREY, 26)
    d.line([(mx, 686), (W - mx, 686)], fill=RULE, width=3)

    # ---- Four stories, 2 x 2 grid ---------------------------------------
    stories = [
        ("TECH OUTAGE", "MICROSOFT 365 GOES DARK",
         "Outlook, Teams and OneDrive fail worldwide; about 130,000 "
         "outage reports at the peak."),
        ("NO DEAL WITH IRAN", "TANKER HITS MINE IN HORMUZ",
         "Trump pulls Vance from Iran talks; an LNG tanker strikes a mine "
         "in the strait."),
        ("UKRAINE TALKS", "EUROPE WINS A SEAT AT THE TABLE",
         "Russia agrees to EU delegates at the next round; a large "
         "prisoner swap is agreed."),
        ("GAZA", "STRIKE HITS KHAN YOUNIS HOSPITAL",
         "Six killed, including a surgeon, and 20 wounded at Nasser "
         "Hospital in Khan Younis."),
    ]
    kick_f = font(SANS_B, 19)
    head_f = font(SANS_B, 27)
    body_f = font(SANS, 20)
    col_w = (cw - 28) // 2
    xs = [mx, mx + col_w + 28]
    ys = [700, 846]
    for i, (kick, head, body) in enumerate(stories):
        x, y = xs[i % 2], ys[i // 2]
        d.text((x, y), kick, font=kick_f, fill=RED)
        y += 26
        y = draw_lines(d, wrap(d, head, head_f, col_w), x, y, head_f, INK, 31)
        draw_lines(d, wrap(d, body, body_f, col_w), x, y + 4, body_f, GREY, 25)

    # ---- Footer ----------------------------------------------------------
    d.line([(mx, 996), (W - mx, 996)], fill=RULE, width=1)
    foot = font(SANS, 15)
    d.text((W / 2, 1002), "All five stories reported on Friday, 13 November 2026.",
           font=foot, fill=GREY, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
