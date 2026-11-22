#!/usr/bin/env python3
"""Steam Cleaner: 9 відео-історій 23.11–01.12 о 19:00 Chicago, 9 різних стилів, бірюзова палітра.
Сирі відео (по 15 с, сюжети по ~3 с «брудно→чисто»):
s1: вікно 0–3, лійка душу 3–6, конфорка 6–9, сидіння авто 9–11, кран 11–13, товар 13–15
s2: дверцята духовки 0–3, унітаз 3–6, шви плитки 6–9, витяжка 9–12, напрямна вікна 12–14, товар 14–15
s3: мікрохвильовка 0–3, злив мийки 3–6, ущільнювач холодильника 6–9, ручка шафи 9–12, конфорка крупно 12–15"""
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor")
import vstory
TEAL = (18, 140, 150)
vstory.EMBER = TEAL; vstory.BRAND = "Luvinor Steam"; vstory.FRAME = (246, 249, 250)
d = list(vstory.cta_pill.__defaults__); d[1] = TEAL + (255,); vstory.cta_pill.__defaults__ = tuple(d)
R = "assets/steam/raw/"; M = "assets/music/"; O = "media/steam/stories/video/"
def c(v, s, e): return {"src": R + v + ".mp4", "start": s, "dur": round(e - s, 2)}
CTA = ['Reply "STEAM" for the link', 'Reply "STEAM" and get the link', 'DM me "STEAM" for the link', 'Reply "CLEAN" for the link']
S = []
def add(day, style, clips, music, cta=0, cta_start=4.5, music_start=0, **kw):
    S.append({"out": f"{O}v{len(S)+1:02d}_{day}_1900_{style}.mp4", "style": style, "clips": clips, "music": M + music,
              "music_start": music_start, "cta": CTA[cta], "cta_start": cta_start, **kw})

add("23", "bigword", [c("s2", 0, 3), c("s2", 6.1, 9), c("s1", 13.1, 15)], "t14_tiktok_654462780.mp3", 0, 6.0,
    words=[["GREASE", 0.1, 1.5], ["STEAM", 1.6, 3.0], ["GRIME", 3.1, 4.5], ["GONE", 4.6, 8.0]], size=230)
add("24", "pov", [c("s2", 9, 12), c("s3", 0.1, 3)], "t13_tiktok_1293762064.mp3", 1, 3.6,
    text="cleaning the gross stuff is actually satisfying now")
add("25", "captions", [c("s2", 3.1, 6), c("s3", 3.1, 6)], "t03_rachel_rosie_home.mp3", 0, 3.8,
    lines=["toilet ring", "sink drain", "just steam", "no chemicals"], gap=0.8)
add("26", "list", [c("s1", 6.1, 9), c("s3", 9.1, 12), c("s3", 12.1, 15)], "t06_tiktok_7318_b.mp3", 2, 4.5, music_start=2.25,
    title="post-feast cleanup", items=["Stovetop burners", "Greasy handles", "No scrubbing"])
add("27", "reveal", [c("s3", 6.1, 9), c("s1", 13.1, 15), c("s2", 14, 15)], "t04_tiktok_992951993.mp3", 0, 3.6, music_start=3.2,
    before="moldy fridge seal", after="gone.", on_at=1.8)
add("28", "split", [c("s1", 3.1, 6), c("s2", 6.1, 9)], "t11_arabic_original.mp3", 0, 3.4,
    clips2=[c("s3", 12.1, 15), c("s1", 11.1, 13), c("s1", 13.1, 14.1)], top="bathroom", bottom="kitchen")
add("29", "cinema", [c("s1", 0.1, 3), c("s2", 12.1, 14), c("s1", 13.1, 15)], "t08_tiktok_7318_d.mp3", 3, 5.0,
    lines=["sunday reset", "windows", "and the tracks too"], times=[[0.3, 2.3], [3.0, 4.5], [5.2, 7.0]])
add("30", "typewriter", [c("s3", 0.1, 3), c("s3", 9.1, 12), c("s2", 14, 15)], "t05_tiktok_7318_a.mp3", 1, 5.0,
    lines=["things I stopped", "scrubbing by hand:", "> microwave", "> cabinet handles", "> oven door"], cps=20)
add("01", "chat", [c("s2", 9.1, 12), c("s2", 0.1, 3), c("s1", 9.1, 11)], "t10_anastasia_original.mp3", 0, 99,
    msgs=[["l", "how did you clean the range hood??"], ["r", "steam. no soaking, no chemicals"], ["l", "ok I need that before the holidays"],
          ["r", "reply STEAM and I'll send the link"]])

only = sys.argv[1:]
for s in S:
    if not only or any(x in s["out"] for x in only): vstory.build(s)
