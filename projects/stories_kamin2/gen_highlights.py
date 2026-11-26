#!/usr/bin/env python3
"""Cozy fireplace (Камін 2): «Актуальне» як у Flame — стиль F (темний люкс, золота світна іконка), 3 розділи ORDER / HOW IT WORKS / FAQ.
Факти: камін + зволожувач, холодна пара + LED, 7 кольорів, пульт, бак 150 мл, 5+ годин, чорний/білий, тихий. Цін не пишемо. Олії не показуємо."""
import os, sys, importlib.util
from PIL import Image, ImageDraw
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor"); os.chdir(ROOT)
import cards, pstory
_s = importlib.util.spec_from_file_location("hl", ROOT + "/projects/flame_dec/gen_hl_covers2.py")
src = open(ROOT + "/projects/flame_dec/gen_hl_covers2.py").read().split("flame_bg = ")[0]  # лише функції icon_layer/glow/label
ns = {"__file__": ROOT + "/projects/flame_dec/gen_hl_covers2.py"}; exec(src, ns)
P = "media/kamin2/photos_ai/"; O = "media/kamin2/highlights/final/"; os.makedirs(O, exist_ok=True)
W, H, R, CX, CY = ns["W"], ns["H"], ns["R"], ns["CX"], ns["CY"]

def cover(key, lab, name):
    f = Image.new("RGBA", (W, H), (24, 16, 12, 255))
    rad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(rad).ellipse([CX - 260, CY - 300, CX + 260, CY + 220], fill=(214, 98, 32, 120))
    from PIL import ImageFilter
    f = Image.alpha_composite(f, rad.filter(ImageFilter.GaussianBlur(120)))
    ImageDraw.Draw(f).ellipse([CX - R + 20, CY - R + 20, CX + R - 20, CY + R - 20], outline=(232, 182, 110, 255), width=5)
    f = ns["glow"](f, ns["icon_layer"](key, (240, 196, 120, 255), 14), 26, 2)
    ns["label"](f, lab, (240, 196, 120), CY + 175, 44)
    f.convert("RGB").save(O + f"0_cover_{name}.jpg", quality=95)

for key, lab, name in [("order", "Order", "ORDER"), ("howto", "How it works", "HOW_IT_WORKS"), ("faq", "FAQ", "FAQ")]:
    cover(key, lab, name)

CT = 'Reply "COZY" for the link'
C, PS = [], []
# ORDER
C.append({"type": "shop", "out": O + "ORDER_1.jpg", "photo": P + "ai15_xmas_coffee_table.jpg", "title": "Cozy Fireplace Humidifier", "sub": "Fireplace glow + humidifier in one · 7 colors", "cta": CT})
PS.append({"style": "list", "out": O + "ORDER_2.jpg", "photo": P + "ai01_white_bedroom_flames.jpg", "title": "how to order", "items": ['Reply "COZY"', "Tap the link we send", "Get cozy"], "cta": CT})
# HOW IT WORKS
PS.append({"style": "list", "out": O + "HOW_1.jpg", "photo": P + "ai04_white_bedroom_mist.jpg", "title": "how it works", "items": ["Pour water in the tank", "Press the button or remote", "Watch the mist flames"], "cta": CT})
PS.append({"style": "split", "out": O + "HOW_2.jpg", "photo": P + "ai05_window_snow_unlit.png", "photo2": P + "ai13_window_cocoa.jpg", "top": "off", "bottom": "on", "cta": CT})
PS.append({"style": "quote", "out": O + "HOW_3.jpg", "photo": P + "ai16_gaming_purple2.png", "lines": ["7 flame colors,", "one remote"], "small": "pick your mood", "cta": CT})
# FAQ
FAQ = [("Most asked", "Is it a real fire?", "No! It's cool water mist lit by LED light, so it looks like dancing flames. No smoke, no heat.", "Mist · Light · No fire", "ai03_black_xmas_flames.jpg"),
       ("Good to know", "Is it really a humidifier?", "Yes! A 150 ml tank puts out cool mist for 5+ hours on one fill.", "150 ml · Cool mist · 5+ hours", "ai18_bedroom_blue.png"),
       ("Colors", "Can I change the flame color?", "Yes, 7 flame colors, right from the remote.", "7 colors · Remote", "ai08_gaming_purple.jpg"),
       ("Safety", "Can I leave it on all night?", "Yes. No real fire and no heat, just cool mist and soft light. Quiet enough for bedrooms.", "No fire · No heat · Quiet", "ai01_white_bedroom_flames.jpg"),
       ("Where", "Where can I put it?", "Nightstand, desk, shelf or TV stand. It's small and fits anywhere.", "Bedroom · Desk · Living room", "ai14_desk_laptop.jpg"),
       ("Colors", "Black or white?", "Both! Pick the one that fits your room.", "Black · White", "ai20_white_movie_lit.png")]
for i, (cat, q, a, tag, ph) in enumerate(FAQ):
    C.append({"type": "faq", "out": O + f"FAQ_{i + 1}.jpg", "photo": P + ph, "n": i + 1, "total": 6, "cat": cat, "q": q, "a": a, "tag": tag, "cta": CT})
for s in C: cards.build(s)
for s in PS: pstory.build(s)
