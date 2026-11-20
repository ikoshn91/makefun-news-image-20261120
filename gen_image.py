#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page (1024x1024 PNG).

One-page newspaper front page, drawn programmatically with Pillow:
no downloaded images, no AI generation, every word is real text
rendered from the strings below. Deterministic: same input bytes
every run (Pillow writes no timestamps into the PNG).

Stories (all reported on Friday 20 November 2026):
 1. Russia's massive overnight missile/drone attack on Kyiv (CNN)
 2. North Korea fires a ballistic missile into the Sea of Japan (S. Korea JCS)
 3. ICJ: Myanmar committed genocide against the Rohingya (ICJ, The Hague)
 4. Trump, Xi and Putin sign a joint peace declaration in Shenzhen
 5. Asian markets plunge on AI-bubble fears (Taiwan -2,200 pts, Nikkei -4.8%)
 Ticker: Senegal migrant boat sinks; Van Gogh sells for $190.4m;
         Kenya discharges its last Ebola patient.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
CARD = (255, 253, 246)
INK = (22, 19, 14)
MUTED = (107, 99, 85)
RED = (166, 30, 30)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
AMBER = (146, 64, 14)
ORANGE = (217, 119, 6)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, label, fill):
    fnt = font(SANS_B, 19)
    w = int(draw.textlength(label, font=fnt)) + 24
    h = 32
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=fill)
    draw.text((x + 12, y + 6), label, font=fnt, fill=WHITE)
    return x + w + 10


def burst(draw, cx, cy, r1, r2, fill):
    pts = []
    for i in range(24):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / 12 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def skyline(draw, x, y, w, h, fill):
    """Dark city silhouette with lit windows, inside box (x, y, w, h)."""
    base = y + h
    heights = [0.55, 0.8, 0.45, 1.0, 0.65, 0.9, 0.5, 0.75, 0.4, 0.85]
    bw = w / len(heights)
    for i, f in enumerate(heights):
        bh = h * f
        draw.rectangle([x + i * bw + 1, base - bh, x + (i + 1) * bw - 1, base],
                       fill=fill)
    # lit windows
    for i, f in enumerate(heights):
        bh = h * f
        for wy in range(2):
            wx = x + i * bw + bw / 2 - 2
            wyy = base - bh + 8 + wy * 16
            if wyy < base - 6:
                draw.rectangle([wx, wyy, wx + 4, wyy + 5], fill=(255, 214, 90))


def icon_missile(draw, x, y, s, color):
    # diagonal missile: body + flame trail
    draw.line([x, y + s, x + s * 0.55, y + s * 0.45], fill=color, width=4)
    pts = [(x + s * 0.55, y + s * 0.15), (x + s * 0.95, y + s * 0.05),
           (x + s * 0.75, y + s * 0.5), (x + s * 0.45, y + s * 0.55)]
    draw.polygon(pts, fill=color)
    burst(draw, x + s * 0.42, y + s * 0.62, 10, 4, ORANGE)


def icon_scales(draw, x, y, s, color):
    cx, cy = x + s / 2, y + s / 2
    draw.line([cx, y + 4, cx, y + s - 8], fill=color, width=4)
    draw.line([x + 4, y + 14, x + s - 4, y + 14], fill=color, width=4)
    for sx in (x + 6, x + s - 22):
        draw.polygon([(sx, y + 16), (sx + 16, y + 16), (sx + 8, y + 34)],
                     outline=color, width=3)
    draw.ellipse([cx - 5, y + s - 10, cx + 5, y + s], fill=color)


def icon_summit(draw, x, y, s, color):
    # three leaders: three circles over a table line
    cols = [RED, NAVY, TEAL]
    for i, c in enumerate(cols):
        cx = x + 10 + i * (s - 20) / 2
        draw.ellipse([cx - 9, y + 6, cx + 9, y + 24], fill=c)
        draw.rectangle([cx - 9, y + 26, cx + 9, y + 40], fill=c)
    draw.line([x, y + s - 6, x + s, y + s - 6], fill=color, width=4)


def icon_chart(draw, x, y, s, color):
    draw.line([x + 4, y + s - 8, x + s - 4, y + s - 8], fill=color, width=3)
    draw.line([x + 4, y + 4, x + 4, y + s - 8], fill=color, width=3)
    pts = [(x + 8, y + 12), (x + s * 0.4, y + 22),
           (x + s * 0.65, y + 16), (x + s - 8, y + s - 16)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
                 fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40  # margin

    # ---------- masthead ----------
    d.line([M, 30, W - M, 30], fill=INK, width=3)
    d.line([M, 36, W - M, 36], fill=INK, width=1)
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 46), title, font=tf, fill=INK)
    date = "FRIDAY  20  NOVEMBER  2026"
    df = font(SANS_B, 27)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 122), date, font=df, fill=RED)
    d.line([M, 158, W - M, 158], fill=INK, width=3)

    # ---------- lead story: Ukraine ----------
    lx, ly, lw, lh = M, 172, W - 2 * M, 248
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=INK, width=2)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    tx = lx + 26
    kf = font(SANS_B, 21)
    d.text((tx, ly + 12), "LEAD  ·  UKRAINE", font=kf, fill=RED)
    hf = font(SANS_B, 40)
    headline = "Russia strikes Kyiv in massive overnight attack"
    lines = wrap(d, headline, hf, 700)
    y = text_block(d, tx, ly + 42, lines, hf, INK, 46)
    bf = font(SANS, 22)
    body = ("Missiles and drones struck hours after the Shenzhen summit. "
            "Three Dnipro bridges damaged; grid “extremely critical”.")
    blines = wrap(d, body, bf, 700)
    y = text_block(d, tx, y + 6, blines, bf, INK, 28)
    cy = y + 10
    cx = tx
    for label in ("AT LEAST 5 KILLED", "3 BRIDGES HIT", "6+ HOURS OF STRIKES"):
        cx = chip(d, cx, cy, label, NAVY)
    # skyline visual, right side
    vx, vy, vw, vh = lx + lw - 200, ly + 16, 178, 120
    burst(d, vx + vw - 40, vy + 26, 26, 10, ORANGE)
    burst(d, vx + vw - 40, vy + 26, 16, 6, RED)
    skyline(d, vx, vy + 44, vw, vh - 44, NAVY)

    # ---------- 2x2 grid ----------
    cards = [
        ("NORTH KOREA", RED, icon_missile,
         "Pyongyang fires missile into the Sea of Japan",
         "South Korea’s military says a ballistic missile was launched "
         "on Friday morning."),
        ("THE HAGUE", NAVY, icon_scales,
         "World Court: Myanmar committed genocide",
         "The ICJ finds Myanmar responsible for genocide against the "
         "Rohingya — a first against a state."),
        ("SHENZHEN", TEAL, icon_summit,
         "Trump, Xi and Putin sign joint peace declaration",
         "First-ever US–China–Russia summit ends in a four-point "
         "declaration — signed Thursday, before the Kyiv strikes."),
        ("MARKETS", AMBER, icon_chart,
         "Asian markets plunge on AI-bubble fears",
         "Taiwan’s index sheds 2,200+ points in a day; Japan’s Nikkei "
         "falls 4.8%."),
    ]
    gx, gy = M, 436
    cw, ch, gap = 462, 196, 16
    ckf = font(SANS_B, 19)
    chf = font(SANS_B, 25)
    cbf = font(SANS, 19)
    for i, (kick, color, icon, head, body) in enumerate(cards):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (ch + gap)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CARD, outline=INK, width=2)
        d.rectangle([x, yy, x + cw, yy + 6], fill=color)
        ix = x + cw - 62
        icon(d, ix, yy + 16, 46, color)
        d.text((x + 18, yy + 18), kick, font=ckf, fill=color)
        hlines = wrap(d, head, chf, cw - 36 - 58)
        y = text_block(d, x + 18, yy + 48, hlines, chf, INK, 30)
        blines = wrap(d, body, cbf, cw - 36)
        text_block(d, x + 18, y + 4, blines, cbf, INK, 24)

    # ---------- ticker ----------
    tx0, ty0, tw_, th = M, 858, W - 2 * M, 88
    d.rectangle([tx0, ty0, tx0 + tw_, ty0 + th], fill=NAVY)
    tf2 = font(SANS_B, 20)
    d.text((tx0 + 16, ty0 + 8), "ALSO TODAY", font=tf2, fill=(255, 214, 90))
    tick = ("Migrant boat sinks off Senegal — dozens missing   •   "
            "Van Gogh sells for $190.4m, an artist record   •   "
            "Kenya discharges its last Ebola patient")
    tkf = font(SANS, 20)
    tlines = wrap(d, tick, tkf, tw_ - 32)
    text_block(d, tx0 + 16, ty0 + 34, tlines, tkf, WHITE, 22)

    # ---------- footer ----------
    d.line([M, 958, W - M, 958], fill=MUTED, width=1)
    ff = font(SANS, 17)
    foot = "Compiled from reports published Friday 20 November 2026  ·  Sources: CNN, Reuters, Le Monde, AP"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 968), foot, font=ff, fill=MUTED)
    foot2 = "One day. Six stories. The world in one page."
    fw2 = d.textlength(foot2, font=ff)
    d.text(((W - fw2) / 2, 990), foot2, font=ff, fill=MUTED)

    out = os.environ.get("OUT", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
