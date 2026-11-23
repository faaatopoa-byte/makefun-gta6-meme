#!/usr/bin/env python3
"""Deterministic renderer for the gta6-meme-x-01 entry memes.

Draws two 1200x675 meme options with Pillow, compositing the official
make.fun press-pack ghost illustrations and brand badge AS-IS.
No randomness, no network, fixed fonts -> same inputs, same bytes.

Run:  python3 render.py [output-dir]     (default: this file's directory)
Writes: meme-option-a.png, meme-option-b.png
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
HOME = Path.home()
PRESS = HOME / "workspace/makefun-tiktok-ad/presspack/make-fun-press-kit"
GHOST_LAPTOP = PRESS / "illustrations/ghost-laptop-recording.png"
GHOST_TROPHY = PRESS / "illustrations/ghost-pile-trophy.png"
BADGE = PRESS / "brand-badge/makefun-badge.png"

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def font(size):
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def gradient(top, bottom):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img


def paste_h(img, path, height, xy):
    """Paste an RGBA asset scaled to `height`, top-left at xy."""
    a = Image.open(path).convert("RGBA")
    w = round(a.width * height / a.height)
    a = a.resize((w, height), Image.LANCZOS)
    img.paste(a, xy, a)
    return w


def text_c(d, cx, y, s, fnt, fill, stroke=0, stroke_fill=(0, 0, 0)):
    w = d.textlength(s, font=fnt)
    d.text((cx - w / 2, y), s, font=fnt, fill=fill, stroke_width=stroke,
           stroke_fill=stroke_fill)
    return w


def wrap(d, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def hud_box(img, box, border=(0, 229, 255), fill=(0, 0, 0, 168), radius=18):
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=border, width=3)
    img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"),
              (0, 0))
    return ImageDraw.Draw(img)


def badge_br(img, height=64, margin=22):
    a = Image.open(BADGE).convert("RGBA")
    w = round(a.width * height / a.height)
    a = a.resize((w, height), Image.LANCZOS)
    img.paste(a, (W - w - margin, H - height - margin), a)


# ---------------------------------------------------------------- option A
def option_a():
    img = gradient((16, 10, 48), (88, 20, 92))          # night Vice City
    d = ImageDraw.Draw(img)
    # headline
    text_c(d, W // 2, 26, "GTA VI", font(118), (255, 255, 255),
           stroke=4, stroke_fill=(255, 45, 149))
    text_c(d, W // 2, 158, "-  L A U N C H   W E E K  -", font(34),
           (0, 229, 255))
    # ghost at laptop, left
    paste_h(img, GHOST_LAPTOP, 330, (56, 250))
    # HUD status box, right
    d = hud_box(img, (520, 238, 1152, 514))
    d.text((552, 262), "MISSION STATUS", font=font(26), fill=(0, 229, 255))
    y = 306
    for line in wrap(d, "My AI agent is entering make.fun bounties for me",
                     font(40), 560):
        d.text((552, y), line, font=font(40), fill=(255, 255, 255))
        y += 52
    # fake progress bar
    d.rounded_rectangle((552, y + 8, 1112, y + 36), radius=12,
                        outline=(255, 255, 255), width=3)
    d.rounded_rectangle((558, y + 14, 940, y + 30), radius=8,
                        fill=(57, 255, 20))
    d.text((952, y + 2), "24/7", font=font(26), fill=(57, 255, 20))
    # bottom punchline bar
    d.rectangle((0, 556, W, H), fill=(0, 0, 0))
    text_c(d, W // 2 - 90, 578,
           "I waited 13 years for this game.", font(38), (255, 255, 255))
    text_c(d, W // 2 - 90, 624,
           "My agent didn't wait at all.", font(38), (255, 213, 74))
    badge_br(img, 74, 18)
    return img


# ---------------------------------------------------------------- option B
def star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def option_b():
    img = gradient((255, 122, 26), (64, 14, 92))        # sunset Vice City
    d = ImageDraw.Draw(img)
    # skyline silhouette
    for x, w, h in [(0, 90, 150), (100, 60, 210), (170, 110, 120),
                    (290, 70, 180), (880, 80, 160), (970, 120, 230),
                    (1100, 100, 140)]:
        d.rectangle((x, 556 - h, x + w, 556), fill=(24, 8, 40))
    d.rectangle((0, 556, W, H), fill=(10, 4, 24))
    # mission box, top-left
    d = hud_box(img, (36, 30, 640, 224), border=(255, 213, 74))
    d.text((62, 48), "MISSION", font=font(26), fill=(255, 213, 74))
    y = 86
    for line in wrap(d, "While you 100% Vice City, your agent completes "
                        "make.fun bounties.", font(33), 545):
        d.text((62, y), line, font=font(33), fill=(255, 255, 255))
        y += 42
    # wanted stars + health bar, top-right
    for i in range(5):
        star(d, 880 + i * 52, 58, 20, (255, 255, 255) if i < 2 else (90, 90, 90))
    d.rectangle((830, 96, 1130, 118), outline=(255, 255, 255), width=3)
    d.rectangle((834, 100, 1040, 114), fill=(57, 255, 20))
    d.text((830, 128), "$ 013370", font=font(30), fill=(57, 255, 20))
    # minimap, bottom-left
    d.ellipse((36, 380, 196, 540), fill=(18, 24, 18), outline=(255, 255, 255),
              width=3)
    d.line((56, 470, 176, 440), fill=(120, 120, 120), width=5)
    d.line((110, 392, 96, 528), fill=(120, 120, 120), width=5)
    d.ellipse((106, 450, 126, 470), fill=(0, 229, 255))
    # ghost with trophy pile, right
    paste_h(img, GHOST_TROPHY, 320, (760, 216))
    # bottom caption
    text_c(d, W // 2 - 80, 578, "Main quest: GTA VI.", font(40),
           (255, 255, 255))
    text_c(d, W // 2 - 80, 626, "Side quest that pays: make.fun", font(40),
           (255, 213, 74))
    badge_br(img, 74, 18)
    return img


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    out.mkdir(parents=True, exist_ok=True)
    option_a().save(out / "meme-option-a.png")
    option_b().save(out / "meme-option-b.png")
    print("wrote", out / "meme-option-a.png", out / "meme-option-b.png")


if __name__ == "__main__":
    main()
