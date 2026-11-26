#!/usr/bin/env python3
"""Steam Cleaner: «Актуальне» — стиль «стікери»: пастельний жовто-блакитний фон, бульбашки,
круглий шрифт Fredoka + рукописний Caveat, 3D-емодзі замість іконок, фото як наліпка з поворотом.
Розділи ORDER / HOW IT WORKS / FAQ. Цін не пишемо."""
import os, random
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
os.chdir(ROOT)
P = "media/steam/photos_ai/"; O = "media/steam/highlights/final/"; os.makedirs(O, exist_ok=True)
W, H = 1080, 1920
FR, CV, EMO = "assets/fonts/Fredoka.ttf", "assets/fonts/Caveat.ttf", "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
def fr(s, wght=600):
    f = ImageFont.truetype(FR, s)
    try: f.set_variation_by_axes([wght, 100])
    except Exception: pass
    return f
def cv(s):
    f = ImageFont.truetype(CV, s)
    try: f.set_variation_by_axes([700])
    except Exception: pass
    return f
NAVY, YEL, SKY, PINK, WHITE = (28, 40, 92), (255, 226, 120), (176, 222, 255), (255, 182, 206), (255, 255, 255)
CTA = 'comment "STEAM" 👉 link in DM'

def emoji(ch, size):
    f = ImageFont.truetype(EMO, 109); im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox()); return im.resize((size, int(size * im.height / im.width)), Image.LANCZOS)

def bg(seed, top=SKY):
    im = Image.new("RGBA", (W, H), top + (255,)); d = ImageDraw.Draw(im)
    d.rectangle([0, int(H * 0.62), W, H], fill=YEL + (255,))
    d.ellipse([-200, int(H * 0.55), W + 200, int(H * 0.69)], fill=YEL + (255,))
    rnd = random.Random(seed)
    for _ in range(16):
        r = rnd.randint(18, 70); x, y = rnd.randint(0, W), rnd.randint(0, int(H * 0.55))
        d.ellipse([x - r, y - r, x + r, y + r], outline=WHITE + (230,), width=5)
        d.ellipse([x - r * 0.45, y - r * 0.6, x - r * 0.15, y - r * 0.3], fill=WHITE + (200,))
    return im

def sticker(im, path, cx, cy, w, h, angle):
    src = Image.open(path).convert("RGB"); iw, ih = src.size; s = max(w / iw, h / ih)
    src = src.resize((int(iw * s) + 1, int(ih * s) + 1)); x = (src.width - w) // 2; y = (src.height - h) // 2
    ph = src.crop((x, y, x + w, y + h))
    card = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, w + 39, h + 39], 50, fill=WHITE)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 36, fill=255)
    card.paste(ph, (20, 20), m); card = card.rotate(angle, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(card, (cx - card.width // 2, cy - card.height // 2))

def wrap(d, text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: line = t
        else: out.append(line); line = w
    return out + [line]

def center(d, y, text, f, fill, lh=1.1):
    for ln in wrap(d, text, f, W - 160):
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=fill); y += int(f.size * lh)
    return y

def cta(im):
    d = ImageDraw.Draw(im); f = fr(46, 700); t = 'comment "STEAM"'; e = emoji("👉", 50)
    tw = d.textlength(t, font=f) + 20 + e.width + 20 + d.textlength("link in DM", font=f)
    x0 = (W - tw) / 2 - 50; d.rounded_rectangle([x0, H - 270, W - x0, H - 160], 55, fill=NAVY)
    x = x0 + 50; d.text((x, H - 248), t, font=f, fill=WHITE); x += d.textlength(t, font=f) + 20
    im.alpha_composite(e, (int(x), H - 245)); x += e.width + 20; d.text((x, H - 248), "link in DM", font=f, fill=YEL)

def story(name, seed, photo, angle, emo, title, note, body=None, n=None):
    im = bg(seed); d = ImageDraw.Draw(im)
    if n: d.text((80, 120), f"FAQ {n}/6", font=fr(40, 700), fill=NAVY)
    sticker(im, P + photo, W // 2, 640, 760, 760, angle)
    im.alpha_composite(emoji(emo, 170), (W - 280, 230))
    d = ImageDraw.Draw(im)
    y = center(d, 1120, title, fr(88, 700), NAVY)
    if note: f_ = cv(84); d.text(((W - d.textlength(note, font=f_)) / 2, y + 10), note, font=f_, fill=(220, 60, 110)); y += 100
    if body: center(d, y + 30, body, fr(46, 500), NAVY, 1.3)
    cta(im); im.convert("RGB").save(O + f"{name}.jpg", quality=93)

def cover(name, emo, col):
    im = Image.new("RGBA", (W, H), col + (255,)); d = ImageDraw.Draw(im)
    rnd = random.Random(name)
    for _ in range(10):
        r = rnd.randint(20, 60); x, y = rnd.randint(0, W), rnd.randint(0, H)
        d.ellipse([x - r, y - r, x + r, y + r], outline=WHITE + (220,), width=5)
    e = emoji(emo, 420); im.alpha_composite(e, ((W - e.width) // 2, (H - e.height) // 2))
    im.convert("RGB").save(O + f"0_cover_{name}.jpg", quality=95)

if __name__ == "__main__":
    for f in os.listdir(O): os.remove(O + f)
    cover("ORDER", "🛒", YEL); cover("HOW_IT_WORKS", "🫧", SKY); cover("FAQ", "💬", PINK)
    story("ORDER_1", 1, "s09_product_kitchen.png", -4, "✨", "one tool for every mess", "kitchen · bath · sofa · car")
    story("ORDER_2", 2, "s02_faucet.png", 3, "📦", "how to get yours", None, 'comment "STEAM" under any video, we send the link. free US shipping')
    story("HOW_1", 3, "s05_oven.png", -3, "💧", "fill. steam. wipe.", "just tap water!")
    story("HOW_2", 4, "s11_tile_grout.png", 4, "🧽", "grout, glass, stovetop", "brushes for every spot")
    story("HOW_3", 5, "s08_car_seat.png", -2, "🚗", "even your car seats", "no chemicals")
    FAQ = [("need cleaning products?", "nope! just tap water. hot steam does the work", "s09_product_kitchen.png", "🙅"),
           ("safe on fabric?", "yes, with the cloth pad. test a hidden spot first", "s03_sofa.png", "🛋️"),
           ("what's in the box?", "brushes, nozzles, hose, scraper and a cloth pad", "s04_laundry_shelf.png", "🎁"),
           ("works on grease?", "yes! it softens baked-on grease on stove and oven", "s10_stovetop.png", "🍳"),
           ("grout & shower glass?", "small brush for grout, window tool for glass", "s11_tile_grout.png", "🚿"),
           ("safe for kids & pets?", "only water, so no chemical residue anywhere", "s07_window.png", "🐶")]
    for i, (q, a, ph, e) in enumerate(FAQ, 1): story(f"FAQ_{i}", 10 + i, ph, (-3, 3)[i % 2], e, q, None, a, n=i)
    print("ok")
