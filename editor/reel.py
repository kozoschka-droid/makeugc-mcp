#!/usr/bin/env python3
"""Монтаж рілсів/тіктоків у стилі конкурентів (хук -> розкриття -> вау-кадр -> CTA).

Використання:
    python3 editor/reel.py project.json

project.json:
{
  "out": "out/video.mp4",
  "clips": [                                  # кліпи по черзі
    {"src": "raw/1.mp4", "start": 0.0, "end": 3.0},
    {"src": "raw/2.mp4", "start": 1.2, "end": 2.0, "speed": 1.0, "zoom": 1.08, "mirror": true}
  ],
  "texts": [                                  # текст поверх відео
    {"text": "This turns your room into the ocean 😲🌊", "start": 0, "end": 99, "pos": "top"},
    {"text": "Comment \"OCEAN\" to get yours", "start": 7, "end": 99, "pos": "bottom"}
  ],
  "audio": "music",                           # music | original | none
  "music": "music/track.mp3", "music_start": 0, "music_volume": 1.0
}
pos: top (≈30% висоти, як у конкурентів) | center | bottom (≈78%) | число 0..1.
end більший за довжину ролику = до кінця.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
FONT_SIZE = 62
MAX_TEXT_W = 900
POS = {"top": 0.30, "center": 0.50, "bottom": 0.78}

EMOJI_RE = re.compile(
    "(?:[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿]"
    "[️‍\U0001F3FB-\U0001F3FF]*"
    "(?:‍[\U0001F000-\U0001FAFF☀-➿][️]*)*)"
)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit(f"command failed: {' '.join(cmd[:4])} ...")
    return r.stdout


def probe_duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", path]).strip())


def has_audio(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
               "stream=index", "-of", "csv=p=0", path])
    return bool(out.strip())


# ---------- текст ----------
_font = ImageFont.truetype(FONT, FONT_SIZE)
_emoji_font = ImageFont.truetype(EMOJI_FONT, 109)  # Noto Color Emoji рендериться лише в 109


def tokens(text):
    """[(is_emoji, str)]"""
    out, i = [], 0
    for m in EMOJI_RE.finditer(text):
        if m.start() > i:
            out.append((False, text[i:m.start()]))
        out.append((True, m.group()))
        i = m.end()
    if i < len(text):
        out.append((False, text[i:]))
    return out


def emoji_img(e):
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), e, font=_emoji_font, embedded_color=True)
    bbox = im.getbbox() or (0, 0, 1, 1)
    im = im.crop(bbox)
    s = int(FONT_SIZE * 1.05)
    return im.resize((max(1, int(im.width * s / im.height)), s), Image.LANCZOS)


def word_width(tok):
    is_e, s = tok
    return emoji_img(s).width if is_e else _font.getlength(s)


def layout(text):
    """Розбиває текст на рядки за шириною. Повертає список рядків з токенів."""
    words = []
    for line in text.split("\n"):
        parts = []
        for is_e, s in tokens(line):
            if is_e:
                parts.append((True, s))
            else:
                parts += [(False, w) for w in re.split(r"(\s+)", s) if w]
        words.append(parts)
    lines = []
    space = _font.getlength(" ")
    for parts in words:
        # одиниці переносу: слово разом з емодзі, що йдуть одразу за ним
        units, unit = [], []
        for tok in parts:
            if not tok[0] and tok[1].isspace():
                if unit:
                    units.append(unit)
                    unit = []
            else:
                unit.append(tok)
        if unit:
            units.append(unit)
        # емодзі, відокремлені пробілом, теж не лишаємо самих на рядку
        merged = []
        for u in units:
            if merged and all(t[0] for t in u):
                merged[-1] = merged[-1] + [(False, " ")] + u
            else:
                merged.append(u)
        widths = [sum(word_width(t) if t[0] or not t[1].isspace() else space for t in u)
                  for u in merged]

        def greedy(limit):
            out, cur, cur_w = [], [], 0
            for u, w in zip(merged, widths):
                if cur and cur_w + space + w > limit:
                    out.append(cur)
                    cur, cur_w = [], 0
                if cur:
                    cur.append((False, " "))
                    cur_w += space
                cur += u
                cur_w += w
            out.append(cur)
            return out

        # вирівнювання: зменшуємо ширину, поки кількість рядків не зросте
        best = greedy(MAX_TEXT_W)
        limit = MAX_TEXT_W
        while limit > 200:
            limit -= 10
            trial = greedy(limit)
            if len(trial) > len(best):
                break
            best = trial
        lines += best
    return lines


def render_text(text, path):
    lines = layout(text)
    line_h = int(FONT_SIZE * 1.22)
    pad = 30
    img_h = line_h * len(lines) + pad * 2
    base = Image.new("RGBA", (W, img_h), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (W, img_h), (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(base), ImageDraw.Draw(shadow)
    for li, line in enumerate(lines):
        lw = sum(word_width(t) if not (not t[0] and t[1].isspace()) else _font.getlength(" ")
                 for t in line)
        x = (W - lw) / 2
        y = pad + li * line_h
        for is_e, s in line:
            if is_e:
                e = emoji_img(s)
                base.alpha_composite(e, (int(x), int(y + FONT_SIZE * 0.08)))
                x += e.width
            else:
                ds.text((x + 2, y + 3), s, font=_font, fill=(0, 0, 0, 170))
                d.text((x, y), s, font=_font, fill=(255, 255, 255, 255))
                x += _font.getlength(s)
    shadow = shadow.filter(ImageFilter.GaussianBlur(4))
    shadow.alpha_composite(base)
    shadow.save(path)
    return img_h


# ---------- монтаж ----------
def build(cfg_path):
    cfg = json.load(open(cfg_path))
    root = os.path.dirname(os.path.abspath(cfg_path))
    p = lambda f: f if os.path.isabs(f) else os.path.join(root, f)
    out = p(cfg["out"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="reel_")
    audio_mode = cfg.get("audio", "music" if cfg.get("music") else "original")

    inputs, fparts, vlabels, alabels = [], [], [], []
    total = 0.0
    for i, c in enumerate(cfg["clips"]):
        src = p(c["src"])
        start = float(c.get("start", 0))
        end = float(c.get("end", probe_duration(src)))
        speed = float(c.get("speed", 1.0))
        zoom = float(c.get("zoom", 1.0))
        inputs += ["-ss", f"{start}", "-t", f"{end - start}", "-i", src]
        dur = (end - start) / speed
        total += dur
        zw, zh = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
        flip = "hflip," if c.get("mirror") else ""
        fparts.append(
            f"[{i}:v]{flip}scale={zw}:{zh}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},setsar=1,fps={FPS},setpts=(PTS-STARTPTS)/{speed},"
            f"trim=duration={dur:.3f},format=yuv420p[v{i}]")
        vlabels.append(f"[v{i}]")
        if audio_mode == "original":
            if has_audio(src):
                fparts.append(f"[{i}:a]atempo={speed},asetpts=PTS-STARTPTS,"
                              f"atrim=duration={dur:.3f},aresample=48000[a{i}]")
            else:
                fparts.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={dur:.3f}[a{i}]")
            alabels.append(f"[a{i}]")
    n = len(cfg["clips"])
    if audio_mode == "original":
        fparts.append("".join(f"{v}{a}" for v, a in zip(vlabels, alabels))
                      + f"concat=n={n}:v=1:a=1[base][aout]")
    else:
        fparts.append("".join(vlabels) + f"concat=n={n}:v=1:a=0[base]")

    last = "[base]"
    idx = n
    for j, t in enumerate(cfg.get("texts", [])):
        png = os.path.join(tmp, f"t{j}.png")
        h = render_text(t["text"], png)
        pos = t.get("pos", "top")
        yc = POS.get(pos, pos if isinstance(pos, (int, float)) else 0.3)
        y = int(H * yc - h / 2)
        s, e = float(t.get("start", 0)), min(float(t.get("end", total)), total)
        inputs += ["-loop", "1", "-t", f"{total:.3f}", "-i", png]
        fparts.append(f"{last}[{idx}:v]overlay=0:{y}:enable='between(t,{s},{e})'[o{j}]")
        last = f"[o{j}]"
        idx += 1

    maps = ["-map", last]
    if audio_mode == "music":
        inputs += ["-ss", f"{cfg.get('music_start', 0)}", "-i", p(cfg["music"])]
        vol = cfg.get("music_volume", 1.0)
        fparts.append(f"[{idx}:a]atrim=duration={total:.3f},volume={vol},"
                      f"afade=t=out:st={max(0, total - 0.6):.3f}:d=0.6,aresample=48000[aout]")
        maps += ["-map", "[aout]"]
    elif audio_mode == "original":
        maps += ["-map", "[aout]"]

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs,
           "-filter_complex", ";".join(fparts), *maps,
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-r", str(FPS), "-movflags", "+faststart"]
    if audio_mode != "none":
        cmd += ["-c:a", "aac", "-b:a", "192k"]
    cmd += ["-t", f"{total:.3f}", out]
    run(cmd)
    print(f"OK {out}  {total:.2f}s  {W}x{H}@{FPS}")


if __name__ == "__main__":
    build(sys.argv[1])
