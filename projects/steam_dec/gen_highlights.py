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
# Стиль G (не як у Flame): світлий фон, суцільне бірюзове коло, біла іконка, підпис під колом
TEAL3 = (18, 140, 150)
def cover(key, lab, name):
    f = Image.new("RGBA", (W, H), (240, 248, 249, 255)); d = ImageDraw.Draw(f)
    d.ellipse([CX - R + 20, CY - R + 20, CX + R - 20, CY + R - 20], fill=TEAL3 + (255,))
    f = Image.alpha_composite(f, ns["icon_layer"](key, (255, 255, 255, 255), 18, 1.05))
    ns["label"](f, lab, TEAL3, CY + R + 40, 58)
    f.convert("RGB").save(O + f"0_cover_{name}.jpg", quality=95)
for key, lab, name in [("order", "Order", "ORDER"), ("howto", "How it works", "HOW_IT_WORKS"), ("faq", "FAQ", "FAQ")]: cover(key, lab, name)
CT = 'Comment "STEAM" for the link'
PS = []
# ORDER: до/після + як замовити
PS.append({"style": "split", "out": O + "ORDER_1.jpg", "photo": P + "s10_stovetop.png", "photo2": P + "s09_product_kitchen.png", "top": "before: grease", "bottom": "after: just steam", "cta": CT})
PS.append({"style": "captions", "out": O + "ORDER_2.jpg", "photo": P + "s02_faucet.png", "lines": ['comment "STEAM"', "get the link in DM", "free US shipping"], "gap": 0.8, "y": 330, "cta": CT})
# HOW IT WORKS: великі слова на фото
PS.append({"style": "captions", "out": O + "HOW_1.jpg", "photo": P + "s05_oven.png", "lines": ["1. fill with water", "2. wait for steam", "3. steam & wipe"], "gap": 0.8, "y": 330, "cta": CT})
PS.append({"style": "split", "out": O + "HOW_2.jpg", "photo": P + "s11_tile_grout.png", "photo2": P + "s03_sofa.png", "top": "grout & glass", "bottom": "sofa & car seats", "cta": CT})
PS.append({"style": "pov", "out": O + "HOW_3.jpg", "photo": P + "s08_car_seat.png", "text": "you clean the whole house with just water", "cta": CT})
# FAQ: як листування з покупцем
CH = [[["l", "do I need cleaning products?"], ["r", "nope! just tap water"], ["l", "and it really cleans grease?"], ["r", "hot steam does all the work"]],
      [["l", "can I use it on my sofa?"], ["r", "yes, with the cloth pad"], ["l", "car seats too?"], ["r", "yep, test a hidden spot first"]],
      [["l", "what's in the box?"], ["r", "brushes, nozzles, hose, scraper"], ["l", "and a cloth pad?"], ["r", "yes! every spot covered"]],
      [["l", "does it work on oven grease?"], ["r", "yes, it softens baked-on grease"], ["l", "range hood too?"], ["r", "steam, then wipe it away"]],
      [["l", "grout and shower glass?"], ["r", "small brush for grout"], ["l", "and the glass?"], ["r", "window tool, no streaks"]],
      [["l", "safe around my kids and dog?"], ["r", "it's only water"], ["l", "no chemical smell?"], ["r", "zero residue, zero smell"]]]
PH = ["s09_product_kitchen.png", "s03_sofa.png", "s04_laundry_shelf.png", "s10_stovetop.png", "s11_tile_grout.png", "s07_window.png"]
for i, (m, ph) in enumerate(zip(CH, PH)):
    PS.append({"style": "chat", "out": O + f"FAQ_{i + 1}.jpg", "photo": P + ph, "msgs": m, "cta": CT, "cta_start": 99})
for s_ in PS: pstory.build(s_)
