"""Render the newspaper front page for Friday, 13 November 2026.

Deterministic: fixed layout, fixed fonts, no network, no randomness.
Reads assets/hero.png, writes assets/entry.png (1024x1024 PNG).
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (250, 247, 240)
INK = (15, 15, 15)
RED = (178, 34, 34)
GREY = (90, 88, 82)
MARGIN = 36
WIDTH = 1024
HEIGHT = 1024


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_width):
    """Wrap text into lines whose measured pixel width fits max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, lines, fnt, x, y, leading, fill):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hero_crop(img, target_w, target_h, bias_y=0.45):
    """Scale the whole image to target width, then crop vertically.

    Scaling first (rather than cropping the full-size image) is what keeps
    the chart and the chip in frame at the chosen bias.
    """
    scaled_w = target_w
    scaled_h = int(round(img.size[1] * target_w / img.size[0]))
    scaled = img.resize((scaled_w, scaled_h), Image.LANCZOS)
    top = int((scaled_h - target_h) * bias_y)
    return scaled.crop((0, top, target_w, top + target_h))


def main():
    page = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead and dateline
    masthead = font("DejaVuSerif-Bold.ttf", 92)
    dateline = font("DejaVuSans-Bold.ttf", 25)
    draw.text((WIDTH // 2, 14), "THE WORLD", font=masthead, fill=INK, anchor="ma")
    draw.text(
        (WIDTH // 2, 122),
        "FRIDAY, 13 NOVEMBER 2026  \u00b7  THE DAY IN ONE IMAGE",
        font=dateline,
        fill=INK,
        anchor="ma",
    )
    draw.line([(MARGIN, 160), (WIDTH - MARGIN, 160)], fill=INK, width=4)
    draw.line([(MARGIN, 166), (WIDTH - MARGIN, 166)], fill=INK, width=1)

    # Hero image: scale to width, crop vertically, bias keeps chart and chip in frame
    hero = Image.open(os.path.join(BASE, "assets", "hero.png")).convert("RGB")
    hero = hero_crop(hero, 952, 360, bias_y=0.45)
    page.paste(hero, (MARGIN, 176))
    draw.rectangle(
        [(MARGIN, 176), (MARGIN + 952 - 1, 176 + 360 - 1)], outline=INK, width=2
    )

    # Hero headline (max 2 lines) and caption
    hero_headline = font("DejaVuSans-Bold.ttf", 40)
    hero_caption = font("DejaVuSans.ttf", 20)
    headline_lines = wrap(
        draw, "NVIDIA CHIEF RESIGNS AS SHARES PLUNGE 16%", hero_headline, 952
    )
    y = 548
    y = draw_lines(draw, headline_lines, hero_headline, MARGIN, y, 46, INK)
    y += 6
    draw.text(
        (MARGIN, y),
        "Jensen Huang steps down as chief executive; Colette Kress named interim leader.",
        font=hero_caption,
        fill=GREY,
    )
    draw.line([(MARGIN, 686), (WIDTH - MARGIN, 686)], fill=INK, width=3)

    # Four stories in a 2x2 grid
    kicker_font = font("DejaVuSans-Bold.ttf", 19)
    headline_font = font("DejaVuSans-Bold.ttf", 27)
    body_font = font("DejaVuSans.ttf", 20)
    footer_font = font("DejaVuSans.ttf", 15)
    stories = [
        (
            "TECH OUTAGE",
            "MICROSOFT 365 GOES DARK",
            "Outlook, Teams and OneDrive fail worldwide; about 130,000 outage reports at the peak.",
        ),
        (
            "NO DEAL WITH IRAN",
            "TANKER HITS MINE IN HORMUZ",
            "Trump pulls Vance from Iran talks; an LNG tanker strikes a mine in the strait.",
        ),
        (
            "UKRAINE TALKS",
            "EUROPE WINS A SEAT AT THE TABLE",
            "Russia agrees to EU delegates at the next round; a large prisoner swap is agreed.",
        ),
        (
            "GAZA",
            "STRIKE HITS KHAN YOUNIS HOSPITAL",
            "Six killed, including a surgeon, and 20 wounded at Nasser Hospital in Khan Younis.",
        ),
    ]
    col_width = 462
    rows = (700, 846)
    cols = (MARGIN, 526)
    for i, (kicker, headline, body) in enumerate(stories):
        x = cols[i % 2]
        y = rows[i // 2]
        draw.text((x, y), kicker, font=kicker_font, fill=RED)
        y += 26
        head_lines = wrap(draw, headline, headline_font, col_width)
        y = draw_lines(draw, head_lines, headline_font, x, y, 31, INK)
        y += 4
        body_lines = wrap(draw, body, body_font, col_width)
        draw_lines(draw, body_lines, body_font, x, y, 25, GREY)

    # Footer
    draw.line([(MARGIN, 996), (WIDTH - MARGIN, 996)], fill=INK, width=1)
    draw.text(
        (WIDTH // 2, 1002),
        "All five stories reported on Friday, 13 November 2026.",
        font=footer_font,
        fill=GREY,
        anchor="ma",
    )

    out_path = os.path.join(BASE, "assets", "entry.png")
    page.save(out_path, format="PNG", optimize=True)
    print(out_path, os.path.getsize(out_path))


if __name__ == "__main__":
    main()
