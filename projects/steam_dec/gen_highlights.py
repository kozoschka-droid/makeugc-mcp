#!/usr/bin/env python3
"""Steam Cleaner: «Актуальне» ORDER / HOW IT WORKS / FAQ — стиль F (темний фон, світна іконка), колір бренду бірюзовий. Цін не пишемо."""
import os, sys
from PIL import Image, ImageDraw, ImageFilter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor"); os.chdir(ROOT)
import cards, vstory, pstory
TEAL = (18, 140, 150)
cards.EMBER, cards.BG, cards.PEACH, cards.INK, cards.MUTE = TEAL, (246, 249, 250), (221, 238, 240), (22, 42, 48), (92, 118, 124)
cards.BRAND = "Luvinor Steam"; cards.TAGLINE = "CLEAN HOME, NO CHEMICALS."; cards.POLL1 = (196, 228, 232)
vstory.EMBER = TEAL; vstory.BRAND = "Luvinor Steam"; vstory.FRAME = (246, 249, 250)
d = list(vstory.cta_pill.__defaults__); d[1] = TEAL + (255,); vstory.cta_pill.__defaults__ = tuple(d)
ns = {"__file__": ROOT + "/projects/flame_dec/gen_hl_covers2.py"}; exec(open(ROOT + "/projects/flame_dec/gen_hl_covers2.py").read().split("flame_bg = ")[0], ns)
W, H, R, CX, CY = ns["W"], ns["H"], ns["R"], ns["CX"], ns["CY"]
P = "media/steam/photos_ai/"; O = "media/steam/highlights/final/"; os.makedirs(O, exist_ok=True)
GLOW, LINE = (18, 140, 150, 130), (140, 225, 230, 255)
def cover(key, lab, name):
    f = Image.new("RGBA", (W, H), (12, 24, 28, 255))
    rad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(rad).ellipse([CX - 260, CY - 300, CX + 260, CY + 220], fill=GLOW)
    f = Image.alpha_composite(f, rad.filter(ImageFilter.GaussianBlur(120)))
    ImageDraw.Draw(f).ellipse([CX - R + 20, CY - R + 20, CX + R - 20, CY + R - 20], outline=(120, 210, 215, 255), width=5)
    f = ns["glow"](f, ns["icon_layer"](key, LINE, 14), 26, 2)
    ns["label"](f, lab, LINE[:3], CY + 175, 44)
    f.convert("RGB").save(O + f"0_cover_{name}.jpg", quality=95)
for key, lab, name in [("order", "Order", "ORDER"), ("howto", "How it works", "HOW_IT_WORKS"), ("faq", "FAQ", "FAQ")]: cover(key, lab, name)
CT = 'Comment "STEAM" for the link'
C, PS = [], []
C.append({"type": "shop", "out": O + "ORDER_1.jpg", "photo": P + "s09_product_kitchen.png", "title": "Handheld Steam Cleaner", "sub": "Kitchen · Bathroom · Sofa · Car · just water", "cta": CT})
PS.append({"style": "list", "out": O + "ORDER_2.jpg", "photo": P + "s10_stovetop.png", "title": "how to order", "items": ['Comment "STEAM"', "Tap the link we send", "Free US shipping"], "cta": CT})
PS.append({"style": "list", "out": O + "HOW_1.jpg", "photo": P + "s05_oven.png", "title": "how it works", "items": ["Fill with tap water", "Wait for the steam", "Point, steam, wipe"], "cta": CT})
PS.append({"style": "list", "out": O + "HOW_2.jpg", "photo": P + "s11_tile_grout.png", "title": "use it on", "items": ["Stovetop & oven", "Grout & shower glass", "Sofa & car seats"], "cta": CT})
PS.append({"style": "quote", "out": O + "HOW_3.jpg", "photo": P + "s02_faucet.png", "lines": ["no scrubbing,", "just steam"], "small": "water only · no chemicals", "cta": CT})
F6 = [("Most asked", "Do I need cleaning products?", "No! Just fill it with tap water. Hot steam loosens grease and grime on its own.", "Water only · No chemicals", "s09_product_kitchen.png"),
      ("Good to know", "Is it safe on fabric?", "Yes, use the cloth pad on sofas, mattresses and car seats. Test a small hidden spot first.", "Sofa · Mattress · Car seats", "s03_sofa.png"),
      ("Attachments", "What comes in the box?", "Brushes, nozzles, a hose, a scraper and a cloth pad, so you can reach every spot.", "Brushes · Nozzles · Hose", "s04_laundry_shelf.png"),
      ("Kitchen", "Does it work on grease?", "Yes! Hot steam softens baked-on grease on stovetops, ovens and range hoods. Wipe it away.", "Stovetop · Oven · Hood", "s10_stovetop.png"),
      ("Bathroom", "Can it clean grout and glass?", "Yes, use the small brush for grout and the window tool for shower glass and mirrors.", "Grout · Glass · Mirrors", "s11_tile_grout.png"),
      ("Family", "Is it safe around kids and pets?", "It uses only water, so no chemical residue on high chairs, toys or floors.", "Water only · No residue", "s08_car_seat.png")]
for i, (cat, q, a, tag, ph) in enumerate(F6):
    C.append({"type": "faq", "out": O + f"FAQ_{i + 1}.jpg", "photo": P + ph, "n": i + 1, "total": 6, "cat": cat, "q": q, "a": a, "tag": tag, "cta": CT})
for s in C: cards.build(s)
for s in PS: pstory.build(s)
