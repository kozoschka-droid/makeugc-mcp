#!/usr/bin/env python3
"""Прибирає вшитий у відео білий текст (як у TikTok/Instagram) через інпейнтинг.

    python3 editor/detext.py in.mp4 out.mp4 [--band 0.18 0.42] [--thr 200]

--band  смуга по висоті (частки 0..1), де шукати текст (за замовчуванням уся висота)
--thr   поріг яскравості білих літер (0..255)
Ідея: літери білі й нерухомі, а фон рухається/мерехтить. Піксель вважається текстом,
якщо він яскравий у ≥85% кадрів у вікні ±0,5 с. Маску розширюємо (тінь/обводка) і
домальовуємо фон з сусідніх пікселів (OpenCV Telea).
"""
import argparse
import subprocess
import sys

import cv2
import numpy as np


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip().split(",")
    w, h = int(out[0]), int(out[1])
    num, den = out[2].split("/")
    return w, h, float(num) / float(den)


def frames(path, w, h):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE)
    size = w * h * 3
    while True:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("out")
    ap.add_argument("--band", nargs=2, type=float, default=[0.0, 1.0])
    ap.add_argument("--thr", type=int, default=200)
    ap.add_argument("--dilate", type=int, default=5)
    a = ap.parse_args()

    w, h, fps = probe(a.inp)
    y0, y1 = int(h * a.band[0]), int(h * a.band[1])

    # прохід 1: маска «яскраві й майже білі» для кожного кадру в смузі
    bright, edge, grays = [], [], []
    for f in frames(a.inp, w, h):
        band = f[y0:y1]
        mn = band.min(axis=2)
        bright.append(mn > a.thr)
        hsv = cv2.cvtColor(band, cv2.COLOR_BGR2HSV)
        edge.append((hsv[..., 1] > 110) & (hsv[..., 2] > 140))   # яскраві насичені (емодзі)
        grays.append(cv2.cvtColor(band, cv2.COLOR_BGR2GRAY).astype(np.int16))
    bright = np.stack(bright)
    edge = np.stack(edge)
    grays = np.stack(grays)
    n = len(bright)
    win = max(3, int(fps * 0.5))

    def roll(x):
        return np.cumsum(np.concatenate([np.zeros((1,) + x.shape[1:], np.float32), x.astype(np.float32)]), axis=0)

    cb, ce, cg, cg2 = roll(bright), roll(edge), roll(grays), roll(grays.astype(np.float32) ** 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.dilate + 1, 2 * a.dilate + 1))
    masks = []
    for i in range(n):
        lo, hi = max(0, i - win), min(n, i + win + 1)
        k = hi - lo
        stable_bright = (cb[hi] - cb[lo]) >= 0.85 * k
        mean = (cg[hi] - cg[lo]) / k
        std = np.sqrt(np.maximum(0, (cg2[hi] - cg2[lo]) / k - mean ** 2))
        static_color = ((ce[hi] - ce[lo]) >= 0.9 * k) & (std < 6)    # нерухомі кольорові емодзі
        m = ((stable_bright & bright[i]) | (static_color & edge[i])).astype(np.uint8) * 255
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
        masks.append(cv2.dilate(m, kernel))

    # прохід 2: інпейнтинг і запис
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
                            "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-", "-i", a.inp,
                            "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", a.out],
                           stdin=subprocess.PIPE)
    for i, f in enumerate(frames(a.inp, w, h)):
        f = f.copy()
        if i < n and masks[i].any():
            band = f[y0:y1]
            fixed = cv2.inpaint(band, masks[i], 6, cv2.INPAINT_TELEA)
            # м'яко розмиваємо зону маски, щоб сховати залишкові «тіні» літер
            soft = cv2.GaussianBlur(cv2.dilate(masks[i], kernel), (0, 0), 4).astype(np.float32)[..., None] / 255
            blur = cv2.GaussianBlur(fixed, (0, 0), 5)
            f[y0:y1] = (fixed * (1 - soft) + blur * soft).astype(np.uint8)
        enc.stdin.write(f.tobytes())
    enc.stdin.close()
    enc.wait()
    print(f"OK {a.out}  frames={n}  masked_px_avg={np.mean([m.mean() for m in masks]) / 255:.3%}")


if __name__ == "__main__":
    sys.exit(main())
