#!/usr/bin/env python3
"""Flame Fireplace: Актуальне (Highlights) IG+FB — 6 обкладинок + історії для кожного розділу.
Розділи за конкурентами (lumena.lamps, memora50_, nooksnet: Reviews / Shop / Gift / категорії). Reviews і Free Gift — НЕ робимо, поки нема реальних відгуків/акції."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor")
import cards, pstory, vstory
exec(open(ROOT + "/projects/flame_dec/gen_stories.py").read().split("P = ROOT")[0].split("import cards, vstory, pstory")[1])  # палітра бренду
P = ROOT + "/media/flame/photos/"; O = ROOT + "/media/flame/highlights/"; os.makedirs(O, exist_ok=True)
CREAM, ORANGE, WHITE = (250, 246, 241), (214, 98, 32), (255, 255, 255)
IN = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"

def cover(name, label, draw_icon):
    W, H = 1080, 1920; im = Image.new("RGB", (W, H), CREAM); d = ImageDraw.Draw(im)
    cx, cy, r = W // 2, H // 2, 330
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE)
    draw_icon(d, cx, cy)
    f = ImageFont.truetype(IN, 70); tw = d.textlength(label, font=f)
    d.text((cx - tw / 2, cy + r + 70), label, font=f, fill=ORANGE)
    im.save(O + f"cover_{name}.png")

def bag(d, x, y):
    d.rounded_rectangle([x - 140, y - 80, x + 140, y + 170], 30, fill=WHITE)
    d.arc([x - 80, y - 200, x + 80, y - 20], 180, 360, fill=WHITE, width=28)
def drop(d, x, y):
    d.polygon([(x, y - 190), (x - 120, y + 20), (x + 120, y + 20)], fill=WHITE)
    d.ellipse([x - 125, y - 60, x + 125, y + 190], fill=WHITE)
def palette(d, x, y):
    cols = [(255, 120, 40), (255, 200, 40), (90, 200, 90), (60, 170, 255), (70, 90, 255), (180, 90, 255), (255, 80, 140)]
    d.ellipse([x - 70, y - 70, x + 70, y + 70], fill=WHITE)
    for i, c in enumerate(cols):
        a = 2 * math.pi * i / 7 - math.pi / 2; px, py = x + 175 * math.cos(a), y + 175 * math.sin(a)
        d.ellipse([px - 52, py - 52, px + 52, py + 52], fill=c, outline=WHITE, width=10)
def gift(d, x, y):
    d.rectangle([x - 160, y - 40, x + 160, y + 180], fill=WHITE); d.rectangle([x - 180, y - 110, x + 180, y - 30], fill=WHITE)
    d.rectangle([x - 22, y - 110, x + 22, y + 180], fill=ORANGE); d.rectangle([x - 180, y - 80, x + 180, y - 60], fill=WHITE)
    d.ellipse([x - 130, y - 210, x - 10, y - 110], outline=WHITE, width=24); d.ellipse([x + 10, y - 210, x + 130, y - 110], outline=WHITE, width=24)
def faq(d, x, y):
    f = ImageFont.truetype(IN, 420); tw = d.textlength("?", font=f); d.text((x - tw / 2, y - 290), "?", font=f, fill=WHITE)
def flame(d, x, y):
    pts = [(x, y - 220), (x + 60, y - 110), (x + 150, y - 20), (x + 150, y + 80), (x + 90, y + 170), (x, y + 200), (x - 90, y + 170),
           (x - 150, y + 80), (x - 140, y - 30), (x - 70, y - 60), (x - 50, y - 140)]
    d.polygon(pts, fill=WHITE); d.ellipse([x - 70, y + 30, x + 70, y + 180], fill=ORANGE)

def heart(d, x, y):
    d.ellipse([x - 170, y - 150, x + 10, y + 30], fill=WHITE); d.ellipse([x - 10, y - 150, x + 170, y + 30], fill=WHITE)
    d.polygon([(x - 165, y - 20), (x + 165, y - 20), (x, y + 180)], fill=WHITE)

for n, l, fn in [("1_shop", "SHOP", bag), ("2_howto", "HOW TO", drop), ("3_colors", "COLORS", palette),
                 ("4_gift", "GIFT", gift), ("5_faq", "FAQ", faq), ("6_cozy", "COZY", heart)]:
    cover(n, l, fn)

C, PS = [], []
def o(sec, i, s): return f"{O}{sec}_{i}_{s}.jpg"
CT = "Link in bio"
# SHOP
C.append({"type": "shop", "out": o("1_shop", 1, "shop"), "photo": P + "p14.png", "title": "Flame Fireplace Diffuser", "sub": "3D flame · cool mist · 7 colors", "cta": CT})
PS.append({"style": "list", "out": o("1_shop", 2, "list"), "photo": P + "p17.png", "title": "how to order", "items": ["Tap the link in bio", "Add to cart", "Get cozy"], "cta": CT})
# HOW TO
PS.append({"style": "list", "out": o("2_howto", 1, "list"), "photo": P + "p18.png", "title": "how it works", "items": ["Pour water in the tank", "Press the button or remote", "Watch the mist flame"], "cta": CT})
PS.append({"style": "captions", "out": o("2_howto", 2, "captions"), "photo": P + "p11.png", "lines": ["pour water", "switch on", "mist rises", "cozy"], "gap": 0.8, "y": 330, "cta": CT})
# COLORS
PS.append({"style": "split", "out": o("3_colors", 1, "split"), "photo": P + "p14.png", "photo2": P + "p20.png", "top": "classic orange", "bottom": "calm blue", "cta": CT})
PS.append({"style": "quote", "out": o("3_colors", 2, "quote"), "photo": P + "p20.png", "lines": ["7 flame colors,", "one for every mood"], "small": "switch with the remote", "cta": CT})
# GIFT
PS.append({"style": "polaroid", "out": o("4_gift", 1, "polaroid"), "photo": P + "p02.png", "title": "the coziest gift", "cta": CT})
PS.append({"style": "list", "out": o("4_gift", 2, "list"), "photo": P + "p08.png", "title": "a gift for", "items": ["Mom", "Best friend", "Yourself"], "cta": CT})
# FAQ (6 карток)
FAQ = [("Most asked","Is it a real fire?","No! It's cool mist lit from below, so it looks like a flickering flame. No smoke, no ashes.","Mist · Light · No fire","p14"),
       ("How it works","How do I use it?","Fill the tank with water and switch it on with the button or the remote. That's it.","Water · Button · Remote","p18"),
       ("Colors","Can I change the flame color?","Yes, there are 7 flame colors, from classic orange to calm blue.","7 colors","p20"),
       ("Where","Where can I put it?","Coffee table, nightstand, desk or shelf. It's small and fits anywhere.","Bedroom · Office · Living room","p15"),
       ("Safety","Does it get hot?","The flame is mist and light, so there is no fire and no smoke.","No fire · No smoke","p13"),
       ("Gift","Is it a good gift?","It's one of those gifts people use every single evening. Cozy for any home.","Cozy gift idea","p02")]
for i, (cat, q, a, tag, ph) in enumerate(FAQ):
    C.append({"type": "faq", "out": o("5_faq", i + 1, "faq"), "photo": P + ph + ".png", "n": i + 1, "total": 6, "cat": cat, "q": q, "a": a, "tag": tag, "cta": CT})
# COZY
PS.append({"style": "serif", "out": o("6_cozy", 1, "serif"), "photo": P + "p13.png", "lines": ["slow nights,", "warm glow"], "small": "no smoke · no ashes", "y": 1150, "cta": CT})
PS.append({"style": "cinema", "out": o("6_cozy", 2, "cinema"), "photo": P + "p07.png", "lines": ["bedtime ritual"], "times": [[0, 99]], "cta": CT})
PS.append({"style": "quote", "out": o("6_cozy", 3, "quote"), "photo": P + "p12.png", "lines": ["home is where", "the glow is"], "small": "flame fireplace", "cta": CT})
for s in C: cards.build(s)
for s in PS: pstory.build(s)
