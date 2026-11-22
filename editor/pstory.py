#!/usr/bin/env python3
"""Фото-сторіз 1080x1920: AI-фото на весь екран + накладка в одному зі стилів vstory (статичний кадр).
python3 editor/pstory.py spec.json
spec: {"out","style","photo" (або "photo2" для split),"t": момент анімації (типово 9), ...поля стилю vstory}"""
import json, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import vstory
W, H, ROOT = vstory.W, vstory.H, vstory.ROOT

def cover(path, w, h):
    im = Image.open(path if path.startswith("/") else ROOT + "/" + path).convert("RGB")
    sc = max(w / im.width, h / im.height); im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    return im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))

def build(s):
    s = dict(s); s.setdefault("cta_start", 0)
    if s["style"] == "split":
        bg = Image.new("RGB", (W, H)); bg.paste(cover(s["photo"], W, H // 2), (0, 0)); bg.paste(cover(s["photo2"], W, H // 2), (0, H // 2))
    else:
        bg = cover(s["photo"], W, H)
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); vstory.STYLES[s["style"]](o, s, s.get("t", 9.0))
    out = Image.alpha_composite(bg.convert("RGBA"), o).convert("RGB")
    p = s["out"] if s["out"].startswith("/") else ROOT + "/" + s["out"]; os.makedirs(os.path.dirname(p), exist_ok=True)
    out.save(p, quality=93); print("OK", p)

if __name__ == "__main__":
    for s in json.load(open(sys.argv[1])): build(s)
