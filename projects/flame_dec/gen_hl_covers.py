#!/usr/bin/env python3
"""Сучасні обкладинки Актуального: A — фото-обкладинки (кроп AI-фото), B — розмите фото полум'я + тонка лінійна іконка, C — текст serif на кремовому."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
P = ROOT + "/media/flame/photos/"; O = ROOT + "/media/flame/highlights/covers/"; os.makedirs(O, exist_ok=True)
PF = ROOT + "/assets/fonts/PlayfairDisplay.ttf"; PFI = ROOT + "/assets/fonts/PlayfairDisplay-Italic.ttf"
W, H, R = 1080, 1920, 380
SEC = [("order", "Order", "p14"), ("howto", "How it works", "p18"), ("faq", "FAQ", "p15")]
def crop_center(im, cx, cy, size):
    return im.crop((cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 2))
def canvas(bg): return Image.new("RGB", (W, H), bg)
# A — фото
for key, label, ph in SEC:
    src = Image.open(P + ph + ".png").convert("RGB"); w, h = src.size
    sq = crop_center(src, w // 2, int(h * 0.52), int(w * 0.92)).resize((2 * R, 2 * R), Image.LANCZOS)
    sq = ImageEnhance.Contrast(sq).enhance(1.05)
    c = src.resize((W, H)).filter(ImageFilter.GaussianBlur(40)); c = ImageEnhance.Brightness(c).enhance(0.6)
    c.paste(sq, (W // 2 - R, H // 2 - R)); c.save(O + f"A_{key}.jpg", quality=95)
# B — розмите полум'я + тонка іконка
LW = 14; WH = (255, 255, 255)
def ic(d, key, x, y):
    if key == "order":
        d.rounded_rectangle([x - 110, y - 50, x + 110, y + 150], 26, outline=WH, width=LW); d.arc([x - 60, y - 150, x + 60, y - 20], 180, 360, fill=WH, width=LW)
    elif key == "howto":
        d.arc([x - 100, y - 30, x + 100, y + 170], -20, 200, fill=WH, width=LW); d.line([(x - 94, y + 36), (x, y - 160), (x + 94, y + 36)], fill=WH, width=LW, joint="curve")
    elif key == "colors":
        import math
        for i in range(7):
            a = 2 * math.pi * i / 7 - math.pi / 2; px, py = x + 120 * math.cos(a), y + 120 * math.sin(a)
            d.ellipse([px - 30, py - 30, px + 30, py + 30], outline=WH, width=LW - 4)
    elif key == "gift":
        d.rectangle([x - 120, y - 20, x + 120, y + 150], outline=WH, width=LW); d.rectangle([x - 140, y - 80, x + 140, y - 20], outline=WH, width=LW)
        d.line([(x, y - 80), (x, y + 150)], fill=WH, width=LW); d.arc([x - 90, y - 170, x, y - 80], 90, 360, fill=WH, width=LW); d.arc([x, y - 170, x + 90, y - 80], 180, 450, fill=WH, width=LW)
    elif key == "faq":
        f = ImageFont.truetype(PF, 300); tw = d.textlength("?", font=f); d.text((x - tw / 2, y - 210), "?", font=f, fill=WH)
    elif key == "cozy":
        f = ImageFont.truetype(PFI, 150); t = "cozy"; tw = d.textlength(t, font=f); d.text((x - tw / 2, y - 110), t, font=f, fill=WH)
bgsrc = Image.open(P + "p14.png").convert("RGB")
bg = bgsrc.resize((W, H)).filter(ImageFilter.GaussianBlur(60)); bg = ImageEnhance.Brightness(bg).enhance(0.85)
for key, label, ph in SEC:
    c = bg.copy(); d = ImageDraw.Draw(c); ic(d, key, W // 2, H // 2); c.save(O + f"B_{key}.jpg", quality=95)
# C — текст
for key, label, ph in SEC:
    c = canvas((236, 226, 214)); d = ImageDraw.Draw(c)
    d.ellipse([W // 2 - R, H // 2 - R, W // 2 + R, H // 2 + R], fill=(250, 246, 241))
    f = ImageFont.truetype(PFI, 170 if len(label) < 6 else 105); tw = d.textlength(label, font=f)
    d.text((W // 2 - tw / 2, H // 2 - 120), label, font=f, fill=(120, 70, 40))
    c.save(O + f"C_{key}.jpg", quality=95)
# прев'ю кружечками
prev = Image.new("RGB", (3 * 170 + 120, 3 * 190), (255, 255, 255)); dd = ImageDraw.Draw(prev)
for r, v in enumerate("ABC"):
    dd.text((10, r * 190 + 70), v, fill=(0, 0, 0), font=ImageFont.truetype(PF, 60))
    for i, (key, label, ph) in enumerate(SEC):
        im = Image.open(O + f"{v}_{key}.jpg").crop((W // 2 - R, H // 2 - R, W // 2 + R, H // 2 + R)).resize((150, 150))
        m = Image.new("L", (150, 150), 0); ImageDraw.Draw(m).ellipse([0, 0, 149, 149], fill=255)
        prev.paste(im, (100 + i * 170, r * 190 + 10), m)
        f = ImageFont.truetype(PF, 22); tw = dd.textlength(label, font=f); dd.text((100 + i * 170 + 75 - tw / 2, r * 190 + 162), label, fill=(30, 30, 30), font=f)
prev.save(O + "preview.png")
