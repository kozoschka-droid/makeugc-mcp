#!/usr/bin/env python3
"""Steam Cleaner: «Актуальне» — стиль «журнал»: обкладинки = справжнє фото товару в дії (без іконок),
історії = фото на весь екран + біла картка знизу з чорним текстом Playfair (як сторінка журналу).
Розділи ORDER / HOW IT WORKS / FAQ. Цін не пишемо."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
os.chdir(ROOT)
P = "media/steam/photos_ai/"; O = "media/steam/highlights/final/"; os.makedirs(O, exist_ok=True)
W, H = 1080, 1920
PF = "assets/fonts/PlayfairDisplay.ttf"; PFI = "assets/fonts/PlayfairDisplay-Italic.ttf"; IN = "/usr/share/fonts/opentype/inter/"
def pf(s, it=False): return ImageFont.truetype(PFI if it else PF, s)
def inter(s, w="Regular"): return ImageFont.truetype(f"{IN}Inter-{w}.otf", s)
INK, GREY, CREAM = (20, 20, 20), (110, 110, 110), (250, 248, 244)
CTA = 'comment "STEAM" for the link'

def fill(path, w=W, h=H, fy=0.5):
    im = Image.open(path).convert("RGB"); iw, ih = im.size; s = max(w / iw, h / ih)
    im = im.resize((int(iw * s) + 1, int(ih * s) + 1)); x = (im.width - w) // 2; y = int((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))

def wrap(d, text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: line = t
        else: out.append(line); line = w
    return out + [line]

def page(name, photo, kicker, title, body, n=None, fy=0.45):
    im = fill(P + photo, fy=fy); d = ImageDraw.Draw(im)
    tf, bf = pf(80), inter(42)
    tl = wrap(d, title, tf, W - 220); bl = wrap(d, body, bf, W - 220) if body else []
    ch = 120 + len(tl) * 96 + (30 + len(bl) * 58 if bl else 0) + 150
    top = H - 120 - ch
    d.rectangle([60, top, W - 60, H - 120], fill=CREAM)
    y = top + 60
    k = kicker.upper() + (f"  ·  {n}/6" if n else ""); d.text((110, y), k, font=inter(30, "Bold"), fill=GREY); y += 70
    for ln in tl: d.text((110, y), ln, font=tf, fill=INK); y += 96
    if bl:
        y += 30
        for ln in bl: d.text((110, y), ln, font=bf, fill=(60, 60, 60)); y += 58
    d.line([(110, H - 220), (W - 110, H - 220)], fill=(200, 196, 188), width=2)
    d.text((110, H - 195), CTA, font=pf(40, True), fill=INK)
    im.save(O + f"{name}.jpg", quality=93)

def cover(name, photo, fy):
    im = fill(P + photo, fy=fy)
    im.save(O + f"0_cover_{name}.jpg", quality=95)

if __name__ == "__main__":
    for f in os.listdir(O): os.remove(O + f)
    cover("ORDER", "s09_product_kitchen.png", 0.5); cover("HOW_IT_WORKS", "s10_stovetop.png", 0.5); cover("FAQ", "s11_tile_grout.png", 0.5)
    page("ORDER_1", "s09_product_kitchen.png", "Steam cleaner", "One tool for every mess", "Kitchen, bathroom, sofa and car. Just tap water.")
    page("ORDER_2", "s02_faucet.png", "How to order", "Comment STEAM, get the link", "We send it in DM. Free US shipping.")
    page("HOW_1", "s05_oven.png", "How it works", "Fill. Steam. Wipe.", "Pour in tap water, wait for the steam, point and wipe.")
    page("HOW_2", "s11_tile_grout.png", "Use it on", "Grout, glass, stovetops, sofas", "Brushes and nozzles for every spot.")
    page("HOW_3", "s08_car_seat.png", "Why steam", "No scrubbing. No chemicals.", "")
    FAQ = [("Do I need cleaning products?", "No. Just tap water. Hot steam loosens grease and grime on its own.", "s09_product_kitchen.png"),
           ("Is it safe on fabric?", "Yes, with the cloth pad on sofas, mattresses and car seats. Test a hidden spot first.", "s03_sofa.png"),
           ("What comes in the box?", "Brushes, nozzles, a hose, a scraper and a cloth pad.", "s04_laundry_shelf.png"),
           ("Does it work on grease?", "Yes. Steam softens baked-on grease on stovetops, ovens and range hoods.", "s10_stovetop.png"),
           ("Grout and shower glass?", "Small brush for grout, window tool for glass and mirrors.", "s11_tile_grout.png"),
           ("Safe around kids and pets?", "It uses only water, so no chemical residue on high chairs, toys or floors.", "s07_window.png")]
    for i, (q, a, ph) in enumerate(FAQ, 1): page(f"FAQ_{i}", ph, "FAQ", q, a, n=i)
    print("ok")
