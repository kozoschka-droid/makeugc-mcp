#!/usr/bin/env python3
"""Відео-сторіз 1080x1920 у 14 різних стилях (щоб історії не були схожі між собою).
python3 editor/vstory.py spec.json   (список спеків)
spec: {"out","style","clips":[{"src","start","dur"}],"music","music_start","cta", ...поля стилю}
Стилі: letters, serif, typewriter, captions, pov, polaroid, cinema, bigword, list, chat, sticker, quote, reveal, split"""
import json, os, subprocess, sys, tempfile, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
W, H, FPS = 1080, 1920, 30
IN = "/usr/share/fonts/opentype/inter/"; MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Medium.ttf"
PF = ROOT + "/assets/fonts/PlayfairDisplay.ttf"; PFI = ROOT + "/assets/fonts/PlayfairDisplay-Italic.ttf"
EMBER = (255, 138, 61); CREAM = (251, 244, 236); INK = (40, 24, 16); WARM = (255, 214, 170)

def font(name, size, wght=None):
    path = {"display": IN + "InterDisplay-Regular.otf", "displaybold": IN + "InterDisplay-Bold.otf", "black": IN + "Inter-Black.otf",
            "bold": IN + "Inter-Bold.otf", "semi": IN + "Inter-SemiBold.otf", "reg": IN + "Inter-Regular.otf", "light": IN + "InterDisplay-Light.otf",
            "mono": MONO, "serif": PF, "serifi": PFI}[name]
    f = ImageFont.truetype(path, size)
    if wght and name.startswith("serif"):
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
def ease(t): t = max(0., min(1., t)); return 1 - (1 - t) ** 3
def back(t):  # ease-out-back (невеликий «відскок»)
    t = max(0., min(1., t)); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def fade(t, s, e=None, fin=0.4, fout=0.35):
    a = ease((t - s) / fin)
    if e is not None and t > e: a *= 1 - ease((t - e) / fout)
    return a
def ctext(d, y, txt, f, fill, x=None, stroke=0, sfill=(0, 0, 0)):
    tw = d.textlength(txt, font=f); xx = (W - tw) / 2 if x is None else x
    d.text((xx, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill); return tw
def wrap(d, text, f, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=f) <= maxw: line = t
            else: out.append(line); line = w
        out.append(line)
    return out
def grad(o, top=0, bottom=0, color=(10, 6, 4)):
    g = Image.new("L", (1, H))
    for y in range(H):
        a = 0
        if top and y < top: a = int(170 * (1 - y / top))
        if bottom and y > H - bottom: a = max(a, int(200 * ((y - (H - bottom)) / bottom)))
        g.putpixel((0, y), a)
    o.paste(Image.new("RGBA", (W, H), color + (255,)), (0, 0), g.resize((W, H)))
def alpha(im, a):
    if a >= 1: return im
    r = im.copy(); r.putalpha(r.getchannel("A").point(lambda v: int(v * a))); return r
def pill_img(txt, f, fill, color, pad=(44, 22), r=None):
    tw = int(f.getlength(txt)); im = Image.new("RGBA", (tw + pad[0] * 2, f.size + pad[1] * 2))
    d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], r if r is not None else im.height // 2, fill=fill)
    d.text((pad[0], pad[1] - f.size * 0.12), txt, font=f, fill=color); return im
def paste_center(o, im, cx, cy, scale=1.0, a=1.0, rot=0):
    if scale != 1.0 and scale > 0: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if rot: im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    im = alpha(im, a); o.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

# ---------- CTA (у кожного стилю свій вигляд) ----------
def cta_pill(o, s, t, y=H - 430, fill=EMBER + (255,), color=(255, 255, 255, 255)):
    if not s.get("cta") or t < s.get("cta_start", 4.5): return
    p = back((t - s["cta_start"]) / 0.45); im = pill_img(s["cta"], font("bold", 44), fill, color)
    paste_center(o, im, W / 2, y, 0.6 + 0.4 * p, ease((t - s["cta_start"]) / 0.3))
def cta_line(o, s, t, y=H - 400, f=None, color=(255, 255, 255)):
    if not s.get("cta") or t < s.get("cta_start", 4.5): return
    a = ease((t - s["cta_start"]) / 0.5); d = ImageDraw.Draw(o); f = f or font("reg", 42)
    ctext(d, y + int(20 * (1 - a)), s["cta"], f, color + (int(240 * a),))

# ---------- стилі ----------
def st_letters(o, s, t):
    grad(o, 0, 700); d = ImageDraw.Draw(o)
    for ph in s["phrases"]:
        st, en = ph["start"], ph["end"]
        if t < st or t > en + 0.5: continue
        size = ph.get("size", 190); fnt = font("display", size); words = ph["words"]
        y0 = (H - size * len(words)) // 2 - 80; out = ease((t - en) / 0.45) if t > en else 0; k = 0
        for i, w in enumerate(words):
            x = (W - d.textlength(w, font=fnt)) / 2; y = y0 + i * size
            for ch in w:
                cw = d.textlength(ch, font=fnt); p = ease((t - st - k * 0.07) / 0.3); k += 1
                if p > 0:
                    a = int(255 * p * (1 - out)); dy = int(40 * (1 - p)) - int(120 * out)
                    d.text((x + 3, y + dy + 4), ch, font=fnt, fill=(0, 0, 0, int(a * .35))); d.text((x, y + dy), ch, font=fnt, fill=(255, 255, 255, a))
                x += cw
            k += 2
    cta_line(o, s, t)

def st_serif(o, s, t):
    grad(o, 0, 1100); d = ImageDraw.Draw(o)
    f = font("serifi", s.get("size", 96)); y = s.get("y", 1080); k = 0
    for line in s["lines"]:
        words = line.split(" "); x = (W - d.textlength(line, font=f)) / 2
        for w in words:
            a = fade(t, 0.4 + k * 0.28, None, 0.6); k += 1
            d.text((x, y + int(18 * (1 - a))), w, font=f, fill=CREAM + (int(255 * a),)); x += d.textlength(w + " ", font=f)
        y += int(f.size * 1.15)
    if s.get("small"):
        a = fade(t, 0.4 + k * 0.28 + 0.2); ctext(d, y + 20, s["small"], font("reg", 36), WARM + (int(230 * a),))
    if s.get("cta") and t >= s["cta_start"]:
        a = ease((t - s["cta_start"]) / 0.5); fc = font("semi", 40); tw = d.textlength(s["cta"], font=fc)
        d.line([(W - tw) / 2, H - 330, (W + tw) / 2, H - 330], fill=CREAM + (int(200 * a),), width=2)
        ctext(d, H - 395, s["cta"], fc, CREAM + (int(255 * a),))

def st_typewriter(o, s, t):
    d = ImageDraw.Draw(o); f = font("mono", 58); x0, y0 = 90, 360
    full = "\n".join(s["lines"]); n = int(max(0, t - 0.3) * s.get("cps", 16)); shown = full[:n]
    lines = shown.split("\n"); maxw = max(d.textlength(l, font=f) for l in s["lines"])
    box = [x0 - 40, y0 - 40, x0 + maxw + 60, y0 + len(s["lines"]) * 80 + 30]
    d.rounded_rectangle(box, 24, fill=(14, 10, 8, 175))
    for i, l in enumerate(lines): d.text((x0, y0 + i * 80), l, font=f, fill=(255, 240, 225, 255))
    if int(t * 2.4) % 2 == 0 or n < len(full):
        cx = x0 + d.textlength(lines[-1], font=f) + 6; cy = y0 + (len(lines) - 1) * 80
        d.rectangle([cx, cy + 6, cx + 26, cy + 64], fill=EMBER + (255,))
    cta_pill(o, s, t, fill=(255, 255, 255, 235), color=INK + (255,))

def st_captions(o, s, t):
    f = font("bold", 64); y = s.get("y", 420)
    for i, line in enumerate(s["lines"]):
        st = 0.3 + i * s.get("gap", 0.9)
        if t < st: break
        im = pill_img(line, f, (255, 255, 255, 255), (12, 12, 12, 255), pad=(30, 16), r=18)
        paste_center(o, im, W / 2, y + im.height / 2, 0.7 + 0.3 * back((t - st) / 0.35), ease((t - st) / 0.2), rot=s.get("tilt", [-2, 1.5, -1, 2])[i % 4])
        y += im.height + 14
    cta_pill(o, s, t)

def st_pov(o, s, t):
    grad(o, 700, 600); d = ImageDraw.Draw(o)
    a = fade(t, 0.2); tag = pill_img("POV:", font("black", 46), EMBER + (255,), (255, 255, 255, 255), pad=(30, 14), r=14)
    paste_center(o, tag, 90 + tag.width / 2, 330, 1, a)
    f = font("black", 78); y = 400
    for i, l in enumerate(wrap(d, s["text"], f, 900)):
        a2 = fade(t, 0.45 + i * 0.12)
        d.text((90, y + int(14 * (1 - a2))), l, font=f, fill=(255, 255, 255, int(255 * a2)), stroke_width=4, stroke_fill=(0, 0, 0, int(200 * a2))); y += 92
    cta_pill(o, s, t)

def st_polaroid(o, s, t):
    m = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(m)
    win = [90, 250, W - 90, 1450]; d.rounded_rectangle(win, 10, fill=(0, 0, 0, 0))
    sh = Image.new("RGBA", (W, H)); ImageDraw.Draw(sh).rounded_rectangle([win[0], win[1] + 14, win[2], win[3] + 14], 10, fill=(70, 40, 20, 90))
    o.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16))); o.alpha_composite(m)
    # «вирізаємо» вікно знову поверх тіні
    hole = Image.new("L", (W, H), 255); ImageDraw.Draw(hole).rounded_rectangle(win, 10, fill=0)
    o.putalpha(Image.composite(o.getchannel("A"), Image.new("L", (W, H), 0), hole))
    d = ImageDraw.Draw(o); ctext(d, 150, "Cozy Fireplace", font("serif", 44), INK + (255,))
    a = fade(t, 0.5); f = font("serifi", 76); y = 1495
    for l in wrap(d, s["title"], f, 900): ctext(d, y + int(16 * (1 - a)), l, f, INK + (int(255 * a),)); y += 88
    if s.get("cta") and t >= s["cta_start"]:
        a = ease((t - s["cta_start"]) / 0.5); ctext(d, H - 190, s["cta"], font("semi", 38), (176, 84, 36, int(255 * a)))

def st_cinema(o, s, t):
    d = ImageDraw.Draw(o); bar = 300
    d.rectangle([0, 0, W, bar], fill=(0, 0, 0, 255)); d.rectangle([0, H - bar, W, H], fill=(0, 0, 0, 255))
    ctext(d, bar - 80, " ".join("COZY FIREPLACE"), font("light", 28), (255, 255, 255, int(170 * fade(t, 0.2))))
    for i, l in enumerate(s["lines"]):
        st, en = s["times"][i]
        a = fade(t, st, en, 0.7, 0.5)
        if a > 0: ctext(d, H - bar + 70, " ".join(l.upper()), font("serif", 44, 500), (255, 240, 220, int(255 * a)))
    if s.get("cta") and t >= s["cta_start"]:
        a = ease((t - s["cta_start"]) / 0.6); ctext(d, H - bar + 170, s["cta"], font("reg", 34), (255, 214, 170, int(230 * a)))

def st_bigword(o, s, t):
    grad(o, 0, 600)
    for i, (w, st, en) in enumerate(s["words"]):
        if not (st <= t <= en): continue
        p = back((t - st) / 0.25); outline = i % 2 == 1
        f = font("black", s.get("size", 230)); tw = int(f.getlength(w)); sc = min(1, 960 / max(tw, 1))
        im = Image.new("RGBA", (tw + 40, int(f.size * 1.3))); dd = ImageDraw.Draw(im)
        if outline: dd.text((20, 0), w, font=f, fill=(0, 0, 0, 0), stroke_width=6, stroke_fill=(255, 255, 255, 255))
        else: dd.text((20, 0), w, font=f, fill=(255, 255, 255, 255))
        paste_center(o, im, W / 2, H * 0.42, sc * (1.25 - 0.25 * p))
    cta_pill(o, s, t)

def st_list(o, s, t):
    grad(o, 1000, 600); d = ImageDraw.Draw(o)
    a = fade(t, 0.2); f = font("black", 70)
    y = 330
    for l in wrap(d, s["title"], f, 900): d.text((90, y + int(14 * (1 - a))), l, font=f, fill=(255, 255, 255, int(255 * a))); y += 82
    y += 40
    for i, it in enumerate(s["items"]):
        st = 0.8 + i * 0.75; a = fade(t, st, None, 0.35)
        if a <= 0: continue
        x = 90 - int(60 * (1 - a))
        d.ellipse([x, y, x + 74, y + 74], fill=EMBER + (int(255 * a),)); ctext(d, y + 10, str(i + 1), font("black", 44), (255, 255, 255, int(255 * a)), x=x + 37 - d.textlength(str(i + 1), font=font("black", 44)) / 2)
        d.text((x + 100, y + 8), it, font=font("semi", 50), fill=(255, 255, 255, int(255 * a)), stroke_width=2, stroke_fill=(0, 0, 0, int(120 * a))); y += 108
    cta_pill(o, s, t)

def st_chat(o, s, t):
    grad(o, 0, 0); d = ImageDraw.Draw(o); y = 380; f = font("reg", 46)
    for i, (side, txt) in enumerate(s["msgs"]):
        st = 0.4 + i * 1.1
        if t < st: break
        lines = wrap(d, txt, f, 640); w = max(d.textlength(l, font=f) for l in lines) + 70; h = len(lines) * 58 + 44
        im = Image.new("RGBA", (int(w), h)); dd = ImageDraw.Draw(im)
        fill = (233, 233, 235, 245) if side == "l" else (10, 132, 255, 255); col = (0, 0, 0) if side == "l" else (255, 255, 255)
        dd.rounded_rectangle([0, 0, w - 1, h - 1], 36, fill=fill)
        for j, l in enumerate(lines): dd.text((35, 20 + j * 58), l, font=f, fill=col)
        cx = 70 + w / 2 if side == "l" else W - 70 - w / 2
        paste_center(o, im, cx, y + h / 2, 0.6 + 0.4 * back((t - st) / 0.3), ease((t - st) / 0.15)); y += h + 26
    if s.get("cta") and t >= s["cta_start"]:
        cta_pill(o, s, t, fill=(255, 255, 255, 240), color=INK + (255,))

def st_sticker(o, s, t):
    grad(o, 800, 700); d = ImageDraw.Draw(o)
    a = fade(t, 0.2); f = font("displaybold", 84)
    y = 330
    for l in wrap(d, s["title"], f, 940): ctext(d, y + int(16 * (1 - a)), l, f, (255, 255, 255, int(255 * a))); y += 96
    st = 1.0
    if t >= st:
        p = back((t - st) / 0.4); r = 190; im = Image.new("RGBA", (2 * r + 20, 2 * r + 20)); dd = ImageDraw.Draw(im)
        pts = [(r + 10 + (r if k % 2 == 0 else r * 0.88) * math.cos(math.pi * k / 16), r + 10 + (r if k % 2 == 0 else r * 0.88) * math.sin(math.pi * k / 16)) for k in range(32)]
        dd.polygon(pts, fill=EMBER + (255,))
        f1 = font("black", 96); t1 = s["badge"]; dd.text((r + 10 - dd.textlength(t1, font=f1) / 2, r - 70), t1, font=f1, fill=(255, 255, 255))
        f2 = font("bold", 40); t2 = s.get("badge2", "OFF"); dd.text((r + 10 - dd.textlength(t2, font=f2) / 2, r + 40), t2, font=f2, fill=(255, 255, 255))
        paste_center(o, im, W - 260, 900, p, ease((t - st) / 0.2), rot=12 + 4 * math.sin(t * 3))
    st2 = 1.8
    if t >= st2:
        a = ease((t - st2) / 0.4); fo = font("semi", 54); fn = font("black", 120)
        x = 110; tw = d.textlength(s["old"], font=fo)
        d.text((x, 1130), s["old"], font=fo, fill=(255, 255, 255, int(200 * a))); d.line([x - 6, 1165, x + tw + 6, 1160], fill=EMBER + (int(255 * a),), width=7)
        d.text((x, 1190 + int(20 * (1 - a))), s["new"], font=fn, fill=(255, 255, 255, int(255 * a)), stroke_width=3, stroke_fill=(0, 0, 0, int(90 * a)))
        if s.get("small"): d.text((x, 1340), s["small"], font=font("reg", 40), fill=WARM + (int(240 * a),))
    cta_pill(o, s, t)

def st_quote(o, s, t):
    o.alpha_composite(Image.new("RGBA", (W, H), (12, 8, 6, 95))); d = ImageDraw.Draw(o)
    a = fade(t, 0.2); ctext(d, 470, "“", font("serif", 300), EMBER + (int(255 * a),))
    f = font("serifi", 82); y = 800
    for i, l in enumerate(s["lines"]):
        a2 = fade(t, 0.6 + i * 0.35, None, 0.6); ctext(d, y + int(16 * (1 - a2)), l, f, CREAM + (int(255 * a2),)); y += 100
    if s.get("small"): a3 = fade(t, 0.8 + len(s["lines"]) * 0.35); ctext(d, y + 30, s["small"], font("light", 38), WARM + (int(230 * a3),))
    cta_line(o, s, t, H - 380, font("semi", 42))

def st_reveal(o, s, t):
    grad(o, 700, 600); d = ImageDraw.Draw(o); on = s["on_at"]
    if t < on + 0.1:
        a = fade(t, 0.2); ctext(d, 380, s["before"], font("bold", 72), (255, 255, 255, int(255 * a)), stroke=3, sfill=(0, 0, 0, 160))
        dots = "." * (1 + int(t * 3) % 3); ctext(d, 480, dots, font("bold", 90), EMBER + (int(255 * a),))
    else:
        fl = max(0, 1 - (t - on) / 0.35)
        if fl > 0: o.alpha_composite(Image.new("RGBA", (W, H), (255, 220, 180, int(150 * fl))))
        p = back((t - on) / 0.4); im = Image.new("RGBA", (W, 200)); dd = ImageDraw.Draw(im)
        f = font("black", 110); dd.text(((W - dd.textlength(s["after"], font=f)) / 2, 20), s["after"], font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
        paste_center(o, im, W / 2, 470, 0.5 + 0.5 * p, ease((t - on) / 0.2))
    cta_pill(o, s, t)

def st_split(o, s, t):
    d = ImageDraw.Draw(o); d.rectangle([0, H // 2 - 4, W, H // 2 + 4], fill=(255, 255, 255, 255))
    for i, (lab, yy) in enumerate([(s["top"], 120), (s["bottom"], H // 2 + 60)]):
        a = fade(t, 0.3 + i * 0.6); im = pill_img(lab, font("bold", 50), (0, 0, 0, 150), (255, 255, 255, 255), pad=(34, 16))
        paste_center(o, im, W / 2, yy + 40, 0.8 + 0.2 * back((t - 0.3 - i * 0.6) / 0.35), a)
    cta_pill(o, s, t, y=H // 2 - 2)

STYLES = {k[3:]: v for k, v in globals().items() if k.startswith("st_")}

def bg_chain(clips, base, label, w=W, h=H, zoom=0.08):
    parts = []
    for j, c in enumerate(clips):
        nfr = int(c["dur"] * FPS); i = base + j
        sw, sh = int(w * 1.1) // 2 * 2, int(h * 1.1) // 2 * 2
        mirror = ",hflip" if c.get("mirror") else ""
        parts.append(f"[{i}:v]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},setsar=1,fps={FPS}{mirror},"
                     f"zoompan=z='1+{zoom}*on/{nfr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={w}x{h}:fps={FPS},"
                     f"trim=duration={c['dur']},setpts=PTS-STARTPTS[{label}{j}]")
    k = len(clips)
    return ";".join(parts) + ";" + "".join(f"[{label}{j}]" for j in range(k)) + f"concat=n={k}:v=1:a=0[{label}]"

def build(s):
    s = dict(s); s.setdefault("cta_start", 4.5); tmp = tempfile.mkdtemp()
    total = sum(c["dur"] for c in s["clips"]); n = int(total * FPS); fn = STYLES[s["style"]]
    for i in range(n):
        o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fn(o, s, i / FPS); o.save(f"{tmp}/o{i:04d}.png", compress_level=1)
    inp = []; allc = s["clips"] + s.get("clips2", [])
    for c in allc: inp += ["-ss", str(c["start"]), "-t", str(c["dur"]), "-i", ROOT + "/" + c["src"] if not c["src"].startswith("/") else c["src"]]
    if s["style"] == "split":
        fc = bg_chain(s["clips"], 0, "a", W, H // 2) + ";" + bg_chain(s["clips2"], len(s["clips"]), "b", W, H // 2) + ";[a][b]vstack[bg]"
    else:
        fc = bg_chain(s["clips"], 0, "c") + ";[c]null[bg]"
    k = len(allc)
    fc += f";[{k}:v]format=rgba[ov];[bg][ov]overlay=0:0,format=yuv420p[v]"
    cmd = ["ffmpeg", "-v", "error", "-y", *inp, "-framerate", str(FPS), "-i", f"{tmp}/o%04d.png"]; maps = ["-map", "[v]"]
    if s.get("music"):
        cmd += ["-ss", str(s.get("music_start", 0)), "-i", ROOT + "/" + s["music"]]
        fc += f";[{k+1}:a]atrim=duration={total},afade=t=in:d=0.3,afade=t=out:st={total-0.8}:d=0.8,loudnorm=I=-13:TP=-1:LRA=11[a]"; maps += ["-map", "[a]"]
    out = s["out"] if s["out"].startswith("/") else ROOT + "/" + s["out"]; os.makedirs(os.path.dirname(out), exist_ok=True)
    cmd += ["-filter_complex", fc, *maps, "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-t", str(total), "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); subprocess.run(["rm", "-rf", tmp]); print("OK", out)

if __name__ == "__main__":
    specs = json.load(open(sys.argv[1])); only = sys.argv[2:]
    for s in specs:
        if not only or any(x in s["out"] for x in only): build(s)
