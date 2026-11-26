#!/usr/bin/env python3
"""Steam Cleaner: «Актуальне» — власний стиль «інфографіка», не схожий ні на Flame, ні на щоденні сторіз Steam:
суцільний бірюзовий градієнт, великі цифри/заголовки Inter Black, фото товару в колі, нижня біла плашка з CTA.
Розділи ORDER / HOW IT WORKS / FAQ. Цін не пишемо."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
os.chdir(ROOT)
P = "media/steam/photos_ai/"; O = "media/steam/highlights/final/"; os.makedirs(O, exist_ok=True)
W, H = 1080, 1920
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + {"black": "Inter-Black.otf", "bold": "Inter-Bold.otf", "reg": "Inter-Regular.otf", "light": "Inter-Light.otf"}[w], s)
TOP, BOT = (8, 92, 104), (40, 180, 186)
WHITE, INK, PALE = (255, 255, 255), (10, 60, 68), (210, 240, 242)
CTA = 'Comment "STEAM" for the link'

def bg():
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(TOP[i] + (BOT[i] - TOP[i]) * t) for i in range(3)))
    # м'які «хмарки пари»
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for cx, cy, r in [(160, 260, 220), (930, 520, 260), (120, 1500, 240), (980, 1700, 200)]:
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 22))
    return Image.alpha_composite(im.convert("RGBA"), ov.filter(ImageFilter.GaussianBlur(40)))

def wrap(d, text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: line = t
        else: out.append(line); line = w
    out.append(line); return out

def circle_photo(im, path, cx, cy, r, ring=12):
    src = Image.open(path).convert("RGB"); w, h = src.size; s = min(w, h)
    sq = src.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)).resize((2 * r, 2 * r))
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=255)
    d = ImageDraw.Draw(im); d.ellipse([cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring], fill=WHITE)
    im.paste(sq, (cx - r, cy - r), m)

def header(d, kicker, n=None, total=None):
    d.text((80, 150), kicker.upper(), font=F("bold", 34), fill=PALE)
    if n:
        t = f"{n:02d}/{total:02d}"; f = F("bold", 34); d.text((W - 80 - d.textlength(t, font=f), 150), t, font=f, fill=PALE)
    d.line([(80, 210), (W - 80, 210)], fill=PALE, width=3)

def cta_bar(im):
    d = ImageDraw.Draw(im); d.rounded_rectangle([80, H - 300, W - 80, H - 170], 65, fill=WHITE)
    f = F("bold", 44); tw = d.textlength(CTA, font=f); d.text(((W - tw) / 2, H - 262), CTA, font=f, fill=INK)

def text_block(d, lines, f, y, fill, lh=1.18, x=80):
    for ln in lines: d.text((x, y), ln, font=f, fill=fill); y += int(f.size * lh)
    return y

def faq(i, q, a, ph):
    im = bg(); d = ImageDraw.Draw(im); header(d, "Steam cleaner · FAQ", i, 6)
    y = text_block(d, wrap(d, q, F("black", 92), W - 160), F("black", 92), 290, WHITE)
    circle_photo(im, P + ph, W // 2, y + 330, 270)
    d = ImageDraw.Draw(im); text_block(d, wrap(d, a, F("reg", 50), W - 160), F("reg", 50), y + 680, WHITE, 1.3)
    cta_bar(im); im.convert("RGB").save(O + f"FAQ_{i}.jpg", quality=93)

def steps(name, kicker, title, items, ph):
    im = bg(); d = ImageDraw.Draw(im); header(d, kicker)
    y = text_block(d, wrap(d, title, F("black", 110), W - 160), F("black", 110), 290, WHITE)
    circle_photo(im, P + ph, W - 330, y + 250, 210)
    d = ImageDraw.Draw(im); yy = y + 560
    for k, it in enumerate(items):
        d.text((80, yy - 10), str(k + 1), font=F("black", 150), fill=PALE)
        text_block(d, wrap(d, it, F("bold", 58), W - 300), F("bold", 58), yy + 40, WHITE, 1.15, x=230); yy += 230
    cta_bar(im); im.convert("RGB").save(O + f"{name}.jpg", quality=93)

def statement(name, kicker, big, small, ph):
    im = bg(); d = ImageDraw.Draw(im); header(d, kicker)
    circle_photo(im, P + ph, W // 2, 720, 330)
    d = ImageDraw.Draw(im); y = text_block(d, wrap(d, big, F("black", 104), W - 160), F("black", 104), 1150, WHITE)
    text_block(d, wrap(d, small, F("reg", 48), W - 160), F("reg", 48), y + 20, PALE)
    cta_bar(im); im.convert("RGB").save(O + f"{name}.jpg", quality=93)

# --- обкладинки: суцільний градієнт, біла «пігулка» з іконкою, назва великими літерами
def icon(d, key, cx, cy, c):
    lw = 20
    if key == "order":   # кошик
        d.line([(cx - 170, cy - 110), (cx - 120, cy - 110), (cx - 70, cy + 70), (cx + 130, cy + 70), (cx + 170, cy - 60), (cx - 95, cy - 60)], fill=c, width=lw, joint="curve")
        for x in (cx - 40, cx + 100): d.ellipse([x - 26, cy + 105, x + 26, cy + 157], fill=c)
    elif key == "howto":  # хмарка пари з трьома хвильками
        for x, y, r in [(cx - 90, cy + 40, 80), (cx + 10, cy - 10, 110), (cx + 110, cy + 45, 75)]: d.ellipse([x - r, y - r, x + r, y + r], fill=c)
        d.rectangle([cx - 170, cy + 40, cx + 185, cy + 120], fill=c)
        for k in range(3):
            x = cx - 80 + k * 80
            d.arc([x - 25, cy + 140, x + 25, cy + 200], 270, 90, fill=c, width=12); d.arc([x - 25, cy + 190, x + 25, cy + 250], 90, 270, fill=c, width=12)
    else:                 # бульбашка чату з «?»
        d.rounded_rectangle([cx - 170, cy - 140, cx + 170, cy + 100], 60, fill=c); d.polygon([(cx - 90, cy + 90), (cx - 130, cy + 180), (cx - 20, cy + 95)], fill=c)
        f = F("black", 210); t = "?"; d.text((cx - d.textlength(t, font=f) / 2, cy - 175), t, font=f, fill=(24, 120, 130))

def cover(key, lab, name):
    im = bg(); cx, cy = W // 2, H // 2 - 40
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle([cx - 300, cy - 300, cx + 300, cy + 300], 120, fill=(255, 255, 255, 45), outline=WHITE, width=6)
    im = Image.alpha_composite(im, ov); d = ImageDraw.Draw(im)
    icon(d, key, cx, cy - 10, WHITE)
    f = F("black", 64); tw = d.textlength(lab.upper(), font=f); d.text(((W - tw) / 2, cy + 340), lab.upper(), font=f, fill=WHITE)
    im.convert("RGB").save(O + f"0_cover_{name}.jpg", quality=95)

if __name__ == "__main__":
    for f in os.listdir(O): os.remove(O + f)
    cover("order", "Order", "ORDER"); cover("howto", "How it works", "HOW_IT_WORKS"); cover("faq", "FAQ", "FAQ")
    statement("ORDER_1", "Steam cleaner", "One tool. Every mess.", "Kitchen · bathroom · sofa · car — with just tap water", "s09_product_kitchen.png")
    steps("ORDER_2", "How to order", "Get yours", ['Comment "STEAM" under any video', "We send the link in DM", "Free US shipping"], "s02_faucet.png")
    steps("HOW_1", "How it works", "3 steps", ["Fill with tap water", "Wait for the steam", "Point, steam, wipe"], "s05_oven.png")
    steps("HOW_2", "Use it on", "Every room", ["Stovetop & oven", "Grout & shower glass", "Sofa & car seats"], "s11_tile_grout.png")
    statement("HOW_3", "Why steam", "No scrubbing. No chemicals.", "Hot steam lifts grease and grime, you just wipe", "s10_stovetop.png")
    FAQ = [("Do I need cleaning products?", "No! Just tap water. Hot steam loosens grease and grime on its own.", "s09_product_kitchen.png"),
           ("Is it safe on fabric?", "Yes, use the cloth pad on sofas, mattresses and car seats. Test a hidden spot first.", "s03_sofa.png"),
           ("What comes in the box?", "Brushes, nozzles, a hose, a scraper and a cloth pad, so you reach every spot.", "s04_laundry_shelf.png"),
           ("Does it work on grease?", "Yes! Steam softens baked-on grease on stovetops, ovens and range hoods.", "s10_stovetop.png"),
           ("Grout and shower glass?", "Small brush for grout, window tool for glass and mirrors. No streaks.", "s11_tile_grout.png"),
           ("Safe around kids and pets?", "It uses only water, so no chemical residue on high chairs, toys or floors.", "s08_car_seat.png")]
    for i, (q, a, ph) in enumerate(FAQ, 1): faq(i, q, a, ph)
    print("ok")
