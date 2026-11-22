#!/usr/bin/env python3
"""Steam Cleaner: 18 фото-історій 23.11–01.12 (09:00 і 13:00 Chicago). Бірюзова палітра бренду.
Факти лише перевірені: працює на воді, без хімії, ручний, з насадками; ціна $49.99. Без вигаданих знижок."""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor")
import cards, vstory, pstory
TEAL = (18, 140, 150)
cards.EMBER, cards.BG, cards.PEACH, cards.INK, cards.MUTE = TEAL, (246, 249, 250), (221, 238, 240), (22, 42, 48), (92, 118, 124)
vstory.EMBER = TEAL; vstory.BRAND = cards.BRAND = "Luvinor Steam"; cards.TAGLINE = "CLEAN HOME, NO CHEMICALS."
cards.POLL1 = (196, 228, 232); vstory.FRAME = (246, 249, 250)
d = list(vstory.cta_pill.__defaults__); d[1] = TEAL + (255,); vstory.cta_pill.__defaults__ = tuple(d)

P = ROOT + "/media/steam/photos_ai/"; O = ROOT + "/media/steam/stories/photo/"
D = ["23", "24", "25", "26", "27", "28", "29", "30", "01"]
CTA = ['Reply "STEAM" for the link', 'Reply "STEAM" and get the link', 'DM me "STEAM" for the link', 'Reply "CLEAN" for the link']
def out(i, slot, name): return f"{O}s{i+1:02d}_{D[i]}_{slot}_{name}.jpg"
C, PS = [], []
def card(i, slot, typ, photo, **kw): C.append({"type": typ, "out": out(i, slot, typ), "photo": P + photo, **kw})
def pst(i, slot, style, photo, cta=0, **kw):
    if "photo2" in kw: kw["photo2"] = P + kw["photo2"]
    PS.append({"style": style, "out": out(i, slot, style), "photo": P + photo, "cta": CTA[cta], **kw})

pst(0, "0900", "pov", "s05_oven.png", text="you finally clean the oven without harsh chemicals")
card(0, "1300", "faq", "s09_product_kitchen.png", n=1, total=4, cat="Most asked", q="Do I need cleaning products?",
     a="No! Just fill it with tap water. Hot steam loosens grease and grime on its own.", tag="Water only · No chemicals", cta=CTA[0])
pst(1, "0900", "split", "s10_stovetop.png", photo2="s11_tile_grout.png", top="kitchen", bottom="bathroom", cta=1)
card(1, "1300", "poll", "s08_car_seat.png", q="What would you steam first?", opts=["1 · Kitchen", "2 · Car seats"], cta="Reply 1 or 2")
pst(2, "0900", "list", "s01_xmas_counter.png", title="steam these before the holidays", items=["Oven & stovetop", "Bathroom grout", "Sofa & car seats"])
card(2, "1300", "shop", "s06_gift_box.png", title="The gift every clean freak wants", sub="Handheld steam cleaner · water only", cta=CTA[2])
pst(3, "0900", "serif", "s10_stovetop.png", lines=["after the feast,", "steam does the rest"], small="grease off, no scrubbing", y=1150, cta=0)
pst(3, "1300", "chat", "s03_sofa.png", msgs=[["l", "how do you keep your couch so clean??"], ["r", "steam. no chemicals, just water"],
     ["l", "wait it works on fabric?"], ["r", "yep! reply STEAM and I'll send the link"]], cta_start=99)
pst(4, "0900", "typewriter", "s04_laundry_shelf.png", lines=["cleaning list:", "[x] kitchen", "[x] bathroom", "[x] car", "done before lunch"], cta=1)
card(4, "1300", "promo", "s07_window.png", kicker="holiday clean", title="$49.99", sub="handheld steam cleaner · water only", cta=CTA[0])
pst(5, "0900", "quote", "s02_faucet.png", lines=["limescale?", "not anymore"], small="just hot steam", cta=3)
pst(5, "1300", "captions", "s11_tile_grout.png", lines=["dirty grout", "hot steam", "no scrubbing", "fresh"], gap=0.8, y=330, cta=0)
pst(6, "0900", "polaroid", "s09_product_kitchen.png", title="small but mighty", cta=2)
card(6, "1300", "faq", "s03_sofa.png", n=2, total=4, cat="Good to know", q="Is it safe on fabric?",
     a="Yes, use the cloth pad on sofas, mattresses and car seats. Test a small hidden spot first.", tag="Sofa · Mattress · Car seats", cta=CTA[1])
pst(7, "0900", "pov", "s08_car_seat.png", text="your car seats look brand new again", cta=1)
pst(7, "1300", "cinema", "s01_xmas_counter.png", lines=["holiday reset"], times=[[0, 99]], cta=0)
pst(8, "0900", "letters", "s06_gift_box.png", phrases=[{"words": ["gift", "idea"], "start": 0, "end": 99}], cta=2)
card(8, "1300", "poll", "s07_window.png", q="Steam or scrub?", opts=["1 · Steam, obviously", "2 · I love scrubbing"], cta="Reply 1 or 2")

assert len(C) + len(PS) == 18
for s in C: cards.build(s)
for s in PS: pstory.build(s)
