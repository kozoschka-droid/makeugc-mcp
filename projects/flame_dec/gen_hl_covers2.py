#!/usr/bin/env python3
"""Цікавіші обкладинки: D — «скло» на полум'ї + світна іконка; E — фото з золотим градієнтним кільцем і значком; F — темний люкс із золотою світною іконкою."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
P = ROOT + "/media/flame/photos/"; O = ROOT + "/media/flame/highlights/covers2/"; os.makedirs(O, exist_ok=True)
PF = ROOT + "/assets/fonts/PlayfairDisplay.ttf"; PFI = ROOT + "/assets/fonts/PlayfairDisplay-Italic.ttf"; IN = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
W, H, R = 1080, 1920, 380; CX, CY = W // 2, H // 2
SEC = [("order", "Order", "p14"), ("howto", "How it works", "p18"), ("faq", "FAQ", "p15")]

def icon_layer(key, color, lw=16, scale=1.0):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x, y = CX, CY - 30; s = scale
    if key == "order":
        d.rounded_rectangle([x - 115*s, y - 45*s, x + 115*s, y + 150*s], int(28*s), outline=color, width=lw)
        d.arc([x - 62*s, y - 150*s, x + 62*s, y - 15*s], 180, 360, fill=color, width=lw)
        d.line([(x - 45*s, y + 20*s), (x + 45*s, y + 20*s)], fill=color, width=lw)
    elif key == "howto":  # полум'я (згладжена крива)
        def spline(cp, n=24):
            out = []; cp = [cp[-1]] + cp + cp[:2]
            for i in range(1, len(cp) - 2):
                p0, p1, p2, p3 = cp[i - 1], cp[i], cp[i + 1], cp[i + 2]
                for k in range(n):
                    t = k / n; t2, t3 = t * t, t * t * t
                    out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
            return out
        outer = [(0, 135), (-95, 95), (-112, 10), (-70, -70), (-25, -120), (5, -185), (30, -110), (75, -60), (112, 15), (95, 95)]
        inner = [(0, 120), (-45, 90), (-50, 40), (-15, -10), (5, -50), (25, 0), (50, 45), (45, 90)]
        for shape in (outer, inner):
            pts = spline([(x + px * s, y + py * s) for px, py in shape]); d.line(pts + [pts[0]], fill=color, width=lw, joint="curve")
    elif key == "faq":
        f = ImageFont.truetype(PF, int(290*s)); tw = d.textlength("?", font=f); d.text((x - tw / 2, y - 190*s), "?", font=f, fill=color)
    return L

def glow(base, layer, radius=28, strength=2):
    g = layer.filter(ImageFilter.GaussianBlur(radius))
    for _ in range(strength): base = Image.alpha_composite(base, g)
    return Image.alpha_composite(base, layer)

def label(img, text, color, y, size=64, font=IN, spacing=6):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(font, size); t = text.upper(); w = sum(d.textlength(c, font=f) + spacing for c in t) - spacing
    x = CX - w / 2
    for c in t: d.text((x, y), c, font=f, fill=color); x += d.textlength(c, font=f) + spacing

flame_bg = Image.open(P + "p14.png").convert("RGB").resize((W, H))
for key, lab, ph in SEC:
    # D — glass
    bg = flame_bg.filter(ImageFilter.GaussianBlur(35)).convert("RGBA")
    blur = flame_bg.filter(ImageFilter.GaussianBlur(70)).convert("RGBA")
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([CX - 265, CY - 265, CX + 265, CY + 265], 80, fill=255)
    glass = Image.composite(ImageEnhance.Brightness(blur.convert("RGB")).enhance(1.25).convert("RGBA"), bg, m)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([CX - 265, CY - 265, CX + 265, CY + 265], 80, fill=(255, 255, 255, 46), outline=(255, 255, 255, 150), width=4)
    glass = Image.alpha_composite(glass, ov)
    glass = glow(glass, icon_layer(key, (255, 236, 210, 255)), 22, 2)
    label(glass, lab, (255, 240, 225), CY + 175, 44)
    glass.convert("RGB").save(O + f"D_{key}.jpg", quality=95)
    # E — photo + gradient ring + badge
    src = Image.open(P + ph + ".png").convert("RGB"); w, h = src.size; sz = int(w * 0.9)
    sq = src.crop((w // 2 - sz // 2, int(h * 0.52) - sz // 2, w // 2 + sz // 2, int(h * 0.52) + sz // 2)).resize((2 * R - 60, 2 * R - 60))
    e = Image.new("RGB", (W, H), (34, 22, 16))
    ring = Image.new("RGB", (2 * R, 2 * R)); rd = ImageDraw.Draw(ring)
    for i in range(2 * R):  # градієнт оранж→золото
        t = i / (2 * R); rd.line([(0, i), (2 * R, i)], fill=(int(214 + 41 * t), int(98 + 120 * t), int(32 + 60 * t)))
    rm = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(rm).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
    e.paste(ring, (CX - R, CY - R), rm)
    im_ = Image.new("L", sq.size, 0); ImageDraw.Draw(im_).ellipse([0, 0, sq.size[0] - 1, sq.size[1] - 1], fill=255)
    e.paste(sq, (CX - R + 30, CY - R + 30), im_)
    e = e.convert("RGBA"); bd = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bdd = ImageDraw.Draw(bd)
    bx, by = CX, CY + R - 95
    bdd.ellipse([bx - 95, by - 95, bx + 95, by + 95], fill=(255, 248, 240, 255), outline=(214, 98, 32, 255), width=8)
    e = Image.alpha_composite(e, bd)
    il = icon_layer(key, (214, 98, 32, 255), 12, 0.42); il = il.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -(by - CY + 30 * 0.42 + 0)), resample=Image.BICUBIC)
    e = Image.alpha_composite(e, il)
    e.convert("RGB").save(O + f"E_{key}.jpg", quality=95)
    # F — dark luxe gold glow
    f = Image.new("RGBA", (W, H), (24, 16, 12, 255)); fd = ImageDraw.Draw(f)
    rad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(rad).ellipse([CX - 260, CY - 300, CX + 260, CY + 220], fill=(214, 98, 32, 120))
    f = Image.alpha_composite(f, rad.filter(ImageFilter.GaussianBlur(120)))
    ImageDraw.Draw(f).ellipse([CX - R + 20, CY - R + 20, CX + R - 20, CY + R - 20], outline=(232, 182, 110, 255), width=5)
    f = glow(f, icon_layer(key, (240, 196, 120, 255), 14), 26, 2)
    label(f, lab, (240, 196, 120), CY + 175, 44)
    f.convert("RGB").save(O + f"F_{key}.jpg", quality=95)

prev = Image.new("RGB", (3 * 200 + 120, 3 * 225), (255, 255, 255)); dd = ImageDraw.Draw(prev)
for r, v in enumerate("DEF"):
    dd.text((15, r * 225 + 70), v, fill=(0, 0, 0), font=ImageFont.truetype(PF, 70))
    for i, (key, lab, ph) in enumerate(SEC):
        im = Image.open(O + f"{v}_{key}.jpg").crop((CX - R, CY - R, CX + R, CY + R)).resize((180, 180), Image.LANCZOS)
        m = Image.new("L", (180, 180), 0); ImageDraw.Draw(m).ellipse([0, 0, 179, 179], fill=255)
        prev.paste(im, (100 + i * 200, r * 225 + 8), m)
        fnt = ImageFont.truetype(PF, 24); tw = dd.textlength(lab, font=fnt); dd.text((100 + i * 200 + 90 - tw / 2, r * 225 + 192), lab, fill=(30, 30, 30), font=fnt)
prev.save(O + "preview.png")
