#!/usr/bin/env python3
"""Steam Cleaner: фото-історії 02.12–01.01 (09:00 і 13:00) у стилі «стікери», як «Актуальне» (затверджено власницею 26.11).
Формати: title / faq / poll / chat / list / quote. Святкові фото лише до 24.12. Цін не пишемо."""
import os, sys, importlib.util
from datetime import date, timedelta
from PIL import ImageDraw
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("hl", ROOT + "/projects/steam_dec/gen_highlights.py"); hl = importlib.util.module_from_spec(spec); spec.loader.exec_module(hl)
src = open(ROOT + "/projects/steam_dec/gen_stories.py").read()
data = src[src.index("HPH = "):src.index("def photo_specs")]
ns = {"P": ""}; exec(data, ns)
HPH, NPH, H_TXT, N_TXT, FAQ, POLL, CHAT, LISTS, QUOTE = (ns[k] for k in ("HPH", "NPH", "H_TXT", "N_TXT", "FAQ", "POLL", "CHAT", "LISTS", "QUOTE"))
O = "media/steam/stories_v2/"; os.makedirs(O, exist_ok=True)
W, H, NAVY, WHITE, YEL, PINK = hl.W, hl.H, hl.NAVY, hl.WHITE, hl.YEL, hl.PINK
P = "media/steam/photos_ai/"
EMO_T = ["✨", "💧", "🧽", "🫧", "🔥", "🏠", "🙌", "😍"]; EMO_H = ["🎄", "🎁", "⛄", "🍪", "🦌"]

def base(seed, photo, angle, emo, small=False):
    im = hl.bg(seed); hl.sticker(im, P + photo, W // 2, 560 if small else 640, 640 if small else 760, 640 if small else 760, angle)
    im.alpha_composite(hl.emoji(emo, 160), (W - 270, 200)); return im

def bubble(d, x, y, text, right, f):
    tw = d.textlength(text, font=f); w = tw + 70; h = f.size + 46
    x0 = W - 80 - w if right else 80
    d.rounded_rectangle([x0, y, x0 + w, y + h], 40, fill=NAVY if right else WHITE)
    d.text((x0 + 35, y + 18), text, font=f, fill=YEL if right else NAVY); return y + h + 22

def build(kind, out, seed, photo, angle, emo, **k):
    small = kind in ("poll", "chat", "list")
    im = base(seed, photo, angle, emo, small); d = ImageDraw.Draw(im)
    if kind == "title":
        y = hl.center(d, 1120, k["title"], hl.fr(88, 700), NAVY)
        if k.get("note"): f = hl.cv(84); d.text(((W - d.textlength(k["note"], font=f)) / 2, y + 10), k["note"], font=f, fill=(220, 60, 110))
    elif kind == "faq":
        d.text((80, 120), f"FAQ {k['n']}/6", font=hl.fr(40, 700), fill=NAVY)
        y = hl.center(d, 1120, k["q"], hl.fr(80, 700), NAVY); hl.center(d, y + 30, k["a"], hl.fr(46, 500), NAVY, 1.3)
    elif kind == "poll":
        y = hl.center(d, 1000, k["q"], hl.fr(80, 700), NAVY) + 30
        for o_ in k["opts"]:
            d.rounded_rectangle([160, y, W - 160, y + 120], 60, fill=WHITE); f = hl.fr(52, 600)
            d.text(((W - d.textlength(o_, font=f)) / 2, y + 30), o_, font=f, fill=NAVY); y += 150
    elif kind == "chat":
        y = 1000; f = hl.fr(44, 600)
        for side, t in k["msgs"]: y = bubble(d, 0, y, t, side == "r", f)
    elif kind == "list":
        y = hl.center(d, 990, k["title"], hl.fr(76, 700), NAVY) + 20
        for i, it in enumerate(k["items"], 1):
            d.text((200, y), f"{i}.", font=hl.fr(64, 700), fill=(220, 60, 110)); d.text((290, y + 6), it, font=hl.fr(58, 600), fill=NAVY); y += 95
    elif kind == "quote":
        y = 1110
        for ln in k["lines"]: y = hl.center(d, y, ln, hl.fr(96, 700), NAVY)
        f = hl.cv(80); d.text(((W - d.textlength(k["small"], font=f)) / 2, y + 10), k["small"], font=f, fill=(220, 60, 110))
    if kind != "poll": hl.cta(im)
    else:
        f = hl.fr(46, 700); t = "reply 1 or 2"; tw = d.textlength(t, font=f)
        d.rounded_rectangle([(W - tw) / 2 - 50, H - 270, (W + tw) / 2 + 50, H - 160], 55, fill=NAVY); d.text(((W - tw) / 2, H - 248), t, font=f, fill=YEL)
    im.convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    days = [date(2026, 12, 2) + timedelta(k) for k in range(31)]
    fmts = ["title", "faq", "poll", "chat", "list", "quote", "title", "faq", "chat", "poll", "title", "list", "quote"]
    hi = ni = 0; k = 0; c = {x: 0 for x in fmts}
    for dd in days:
        xmas = dd <= date(2026, 12, 24)
        for slot in ("0900", "1300"):
            f = fmts[k % len(fmts)]; k += 1; j = c[f]; c[f] += 1
            hol = xmas and slot == "1300" and f in ("title", "quote", "list")
            if hol: ph = HPH[hi % len(HPH)]; hi += 1
            else: ph = NPH[ni % len(NPH)]; ni += 1
            emo = (EMO_H if hol else EMO_T)[k % (5 if hol else 8)]
            out = f"{O}p_{dd.isoformat()[5:]}_{slot}_{f}.jpg"; ang = (-4, 3, -2, 4)[k % 4]
            if f == "title":
                t = H_TXT[j % len(H_TXT)] if hol else N_TXT[(k + j) % len(N_TXT)]
                build(f, out, k, ph, ang, emo, title=t, note=["just tap water!", "no chemicals", "free US shipping", "try it ✨"][j % 4].replace(" ✨", ""))
            elif f == "faq":
                a = FAQ[j % len(FAQ)]; build(f, out, k, ph, ang, emo, n=j % 6 + 1, q=a[1].lower(), a=a[2])
            elif f == "poll":
                q = POLL[j % len(POLL)]; build(f, out, k, ph, ang, emo, q=q[0].lower(), opts=q[1])
            elif f == "chat":
                m = [[s, t.replace("reply STEAM", 'comment "STEAM"')] for s, t in CHAT[j % len(CHAT)]]; build(f, out, k, ph, ang, emo, msgs=m)
            elif f == "list":
                l = LISTS[j % len(LISTS)]; build(f, out, k, ph, ang, emo, title=l[0], items=[x.lower() for x in l[1]])
            elif f == "quote":
                q = QUOTE[j % len(QUOTE)]; build(f, out, k, ph, ang, emo, lines=q[0], small=q[1])
    print(len(os.listdir(O)), "stories")
