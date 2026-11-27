#!/usr/bin/env python3
"""Steam Cleaner: відео-історії 19:00 (02.12–01.01) у стилі «стікери» — як фото-історії v2 і «Актуальне».
Відео грає у віконці-наліпці, зверху блакитний фон з бульбашками, знизу жовта хвиля, заголовок Fredoka + рукописна приписка, CTA."""
import os, sys, subprocess, importlib.util
from datetime import date, timedelta
from PIL import Image, ImageDraw
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("hl", ROOT + "/projects/steam_dec/gen_highlights.py"); hl = importlib.util.module_from_spec(spec); spec.loader.exec_module(hl)
src = open(ROOT + "/projects/steam_dec/gen_stories.py").read()
ns = {}; exec(src[src.index("SC = "):src.index("def video_specs")], ns)
SC, MUS = ns.get("SC"), ns.get("MUS")
O = "media/steam/stories_v2/"; TMP = "/tmp/claude-0/vs2/"; os.makedirs(O, exist_ok=True); os.makedirs(TMP, exist_ok=True)
W, H = hl.W, hl.H; WX, WY, WS = 160, 260, 760   # віконце для відео
TITLES = [("grime, meet hot steam", "watch this!"), ("no scrubbing, just steam", "just tap water"), ("the gross part 😳", "then... gone"),
          ("oven door glow up", "no chemicals"), ("sunday reset", "every corner"), ("grout before & after", "so satisfying"),
          ("stovetop in seconds", "steam does it"), ("holiday mess? done", "free US shipping"), ("bye bye limescale", "water only"),
          ("my favorite tool", "small but mighty")]
XT = [("clean before the guests", "holiday ready"), ("the gift that cleans", "best gift ever")]
EMO = ["✨", "💧", "🫧", "🧽", "🔥", "😍", "🙌", "🏠"]

def design(i, title, note, emo):
    im = hl.bg(100 + i); d = ImageDraw.Draw(im)
    d.rounded_rectangle([WX - 20, WY - 20, WX + WS + 20, WY + WS + 20], 50, fill=hl.WHITE + (255,))
    hole = Image.new("L", (W, H), 255); ImageDraw.Draw(hole).rounded_rectangle([WX, WY, WX + WS, WY + WS], 36, fill=0)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (W, H), 0), hole))
    im.alpha_composite(hl.emoji(emo, 170), (W - 280, 170)); d = ImageDraw.Draw(im)
    y = hl.center(d, 1120, title, hl.fr(88, 700), hl.NAVY)
    f = hl.cv(84); d.text(((W - d.textlength(note, font=f)) / 2, y + 10), note, font=f, fill=(220, 60, 110))
    hl.cta(im); p = f"{TMP}ov_{i}.png"; im.save(p); return p

def render(i, d_, clips, music, ms, title, note, emo):
    ov = design(i, title, note, emo); out = f"{O}v_{d_.isoformat()[5:]}_1900_sticker.mp4"
    args = ["ffmpeg", "-y", "-loglevel", "error"]; fl = []
    for k, (v, s, e) in enumerate(clips):
        dur = round(min(e - s, 2.8), 2); args += ["-ss", str(s), "-t", str(dur), "-i", f"assets/steam/raw/{v}.mp4"]
        fl.append(f"[{k}:v]scale={WS}:{WS}:force_original_aspect_ratio=increase,crop={WS}:{WS},setsar=1,fps=30[c{k}]")
    n = len(clips); args += ["-i", ov, "-ss", str(ms), "-i", music]
    fl.append("".join(f"[c{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[vid]")
    fl.append(f"color=c=white:s={W}x{H}:r=30[bgc];[bgc][vid]overlay={WX}:{WY}:shortest=1[b1];[b1][{n}:v]overlay=0:0[outv]")
    args += ["-filter_complex", ";".join(fl), "-map", "[outv]", "-map", f"{n + 1}:a", "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21",
             "-c:a", "aac", "-af", "afade=t=out:st=7.5:d=0.8", out]
    subprocess.run(args, check=True); return out

if __name__ == "__main__":
    days = [date(2026, 12, 2) + timedelta(k) for k in range(31)]
    only = sys.argv[1:]
    for i, d_ in enumerate(days):
        if only and d_.isoformat()[5:] not in only: continue
        xmas = d_ <= date(2026, 12, 24)
        cl = [SC[(i * 3 + q * 7) % len(SC)] for q in range(3)] + [("s5", 13, 15) if xmas and i % 3 == 0 else ("s1", 13, 15)]
        m = MUS[i % len(MUS)]; ms = 2.25 if "7318_b" in m else (26 if "7318_c" in m else 0)
        t, nt = (XT[i % 2] if xmas and i % 4 == 0 else TITLES[i % len(TITLES)])
        print("OK", render(i, d_, cl, "assets/music/" + m, ms, t, nt, EMO[i % len(EMO)]), flush=True)
