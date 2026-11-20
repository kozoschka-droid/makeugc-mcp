#!/usr/bin/env python3
"""Сторіз 1080x1920: фото або відео + стильні плашки (бренд-мітка, заголовок, кнопка-CTA).
python3 editor/story.py spec.json  (spec: {"out","src","start","dur","title","sub","cta","label"})"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import reel
W, H = 1080, 1920
F = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
EMBER = (255, 138, 61)

def pill(text, size, fill, color, pad=(44, 22)):
    f = ImageFont.truetype(F, size)
    tw = int(f.getlength(text)); th = size
    im = Image.new("RGBA", (tw + pad[0]*2, th + pad[1]*2), (0,0,0,0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,im.width-1,im.height-1], radius=im.height//2, fill=fill)
    d.text((pad[0], pad[1]-size*0.12), text, font=f, fill=color)
    return im

def overlay(spec, tmp):
    o = Image.new("RGBA", (W, H), (0,0,0,0))
    # градієнти зверху і знизу для читабельності
    g = Image.new("L", (1, H))
    for y in range(H):
        a = 0
        if y < 620: a = int(170 * (1 - y/620))
        if y > H-760: a = int(200 * ((y-(H-760))/760))
        g.putpixel((0, y), a)
    o.paste(Image.new("RGBA", (W, H), (12, 8, 6, 255)), (0,0), g.resize((W, H)))
    if spec.get("label", True):
        lab = pill("COZY FIREPLACE", 30, (255,255,255,40), (255,255,255,235), pad=(28,14))
        o.alpha_composite(lab, ((W-lab.width)//2, 270))
    y = 350
    if spec.get("title"):
        p = os.path.join(tmp, "t.png"); h = reel.render_text(spec["title"], p)
        o.alpha_composite(Image.open(p), (0, y)); y += h
    if spec.get("sub"):
        f = ImageFont.truetype(F, 40); d = ImageDraw.Draw(o)
        s = spec["sub"]; tw = f.getlength(s)
        d.text(((W-tw)/2, y-6), s, font=f, fill=(255, 214, 170, 255))
    if spec.get("cta"):
        c = pill(spec["cta"], 46, EMBER + (255,), (255,255,255,255))
        sh = Image.new("RGBA", (c.width+40, c.height+40), (0,0,0,0)); sh.alpha_composite(
            Image.new("RGBA", c.size, (0,0,0,120)), (20, 28)); sh = sh.filter(ImageFilter.GaussianBlur(12))
        x, yy = (W-c.width)//2, H-430
        o.alpha_composite(sh, (x-20, yy-20)); o.alpha_composite(c, (x, yy))
    if spec.get("hint"):
        f = ImageFont.truetype(F, 34); d = ImageDraw.Draw(o); tw = f.getlength(spec["hint"])
        d.text(((W-tw)/2, H-330), spec["hint"], font=f, fill=(255,255,255,210))
    return o

def build(spec):
    tmp = tempfile.mkdtemp()
    ov = overlay(spec, tmp); ovp = os.path.join(tmp, "ov.png"); ov.save(ovp)
    src = spec["src"]; out = spec["out"]; os.makedirs(os.path.dirname(out), exist_ok=True)
    if src.lower().endswith((".jpg", ".jpeg", ".png")):
        im = Image.open(src).convert("RGB")
        sc = max(W/im.width, H/im.height); im = im.resize((int(im.width*sc)+1, int(im.height*sc)+1))
        im = im.crop(((im.width-W)//2, (im.height-H)//2, (im.width-W)//2+W, (im.height-H)//2+H)).convert("RGBA")
        im.alpha_composite(ov); im.convert("RGB").save(out, quality=92)
    else:
        ss, dur = spec.get("start", 0), spec.get("dur", 7)
        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps=30[b];"
              f"[b][1:v]overlay=0:0,format=yuv420p[v]")
        cmd = ["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(dur),"-i",src,"-loop","1","-t",str(dur),"-i",ovp,
               "-filter_complex",vf,"-map","[v]","-map","0:a?","-c:v","libx264","-crf","20","-preset","medium",
               "-c:a","aac","-shortest","-movflags","+faststart",out]
        subprocess.run(cmd, check=True)
    print("OK", out)

if __name__ == "__main__":
    for s in json.load(open(sys.argv[1])):
        build(s)
