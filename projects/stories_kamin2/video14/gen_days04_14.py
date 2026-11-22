#!/usr/bin/env python3
"""Дні 4–14 відео-історій Каміна 2 (26.11–06.12), 3 на день, 14 стилів без повторів у межах дня.
Кадри лише там, де камін світиться; без олій (v3, v5 не використовуємо; v8 12–16, v9 7–11, v12 2–4 — олії/піпетка)."""
import json, os
R = "assets/fireplace/raw/"; M = "assets/music/"; O = "media/kamin2/stories/video14/"
def c(v, s, d, mirror=False):
    x = {"src": R + (v + ".mov" if v == "v1" else v + ".mp4"), "start": s, "dur": d}
    if mirror: x["mirror"] = True
    return x
CTA = ['Reply "COZY" for the link', 'Reply "COZY" and get the link', 'DM me "COZY" for the link', 'Reply "FIRE" for the link',
       'Reply "LINK" and I\'ll send it', 'Reply "GLOW" for the link']
S = []
def add(day, slot, style, clips, music, cta_i=0, cta_start=4.2, music_start=0, **kw):
    sp = {"out": f"{O}d{day:02d}_{slot}_{style}.mp4", "style": style, "clips": clips, "music": M + music, "music_start": music_start,
          "cta": CTA[cta_i], "cta_start": cta_start}
    sp.update(kw); S.append(sp)

# День 4
add(4, "0900", "typewriter", [c("v12", 8.4, 3.0), c("v2", 9.6, 2.4), c("v1", 1.3, 3.0)], "t06_tiktok_7318_b.mp3", 1, 5.0, 2.25,
    lines=["things that make", "winter better:", "> blanket", "> cocoa", "> this fireplace"], cps=18)
add(4, "1300", "polaroid", [c("v4", 13.0, 3.0), c("v9", 14.0, 2.5), c("v7", 5.5, 2.5)], "t08_tiktok_7318_d.mp3", 0, 3.5,
    title="our coziest corner this winter")
add(4, "1900", "bigword", [c("v8", 21.0, 1.6), c("v8", 24.0, 1.6), c("v8", 27.0, 1.6), c("v6", 9.5, 1.6), c("v10", 17.0, 1.6)], "t14_tiktok_654462780.mp3", 3, 5.0,
    words=[["ORANGE", 0.1, 1.5], ["PINK", 1.6, 3.1], ["GREEN", 3.2, 4.7], ["BLUE", 4.8, 6.3], ["YOURS?", 6.4, 8.0]], size=220)
# День 5
add(5, "0900", "quote", [c("v1", 1.2, 3.3), c("v12", 10.0, 2.6), c("v4", 16.0, 2.4)], "t10_anastasia_original.mp3", 0, 4.6,
    lines=["home is where", "the glow is"], small="no smoke · no ash · no heat")
add(5, "1300", "letters", [c("v6", 7.0, 2.4), c("v8", 30.0, 2.4), c("v10", 20.0, 3.0)], "t13_tiktok_1293762064.mp3", 2, 5.0,
    phrases=[{"words": ["pick", "a mood"], "start": 0.3, "end": 3.4}, {"words": ["any", "color"], "start": 4.0, "end": 7.8, "size": 180}])
add(5, "1900", "pov", [c("v7", 5.2, 3.0), c("v1", 1.6, 2.8), c("v9", 13.2, 2.6)], "t05_tiktok_7318_a.mp3", 0, 4.4,
    text="it's 9pm, lights off, and your room finally feels like a cabin")
# День 6
add(6, "0900", "sticker", [c("v4", 14.5, 3.0), c("v12", 11.0, 2.4), c("v2", 10.0, 2.0)], "t11_arabic_original.mp3", 4, 4.0,
    title="Half price. Full cozy.", badge="-50%", old="$139.95", new="$69.95", small="free US shipping")
add(6, "1300", "chat", [c("v2", 9.6, 2.4), c("v4", 12.4, 3.4), c("v9", 14.5, 2.4)], "t07_tiktok_7318_c.mp3", 0, 99, music_start=26,
    msgs=[["l", "what should I get my mom for christmas"], ["r", "this fireplace humidifier"], ["l", "omg she'd love that"], ["r", "reply COZY, I'll send you the link"]])
add(6, "1900", "cinema", [c("v9", 13.0, 3.2), c("v12", 8.6, 2.8), c("v7", 6.0, 2.4)], "t09_tiktok_7318_e.mp3", 0, 5.8, music_start=9,
    lines=["sunday night", "soft music", "softer light"], times=[[0.3, 2.8], [3.2, 5.0], [5.4, 8.4]])
# День 7
add(7, "0900", "list", [c("v10", 12.0, 3.0), c("v4", 15.5, 3.0), c("v1", 1.4, 3.0)], "t03_rachel_rosie_home.mp3", 5, 4.0,
    title="how to make any room cozy", items=["Lights off", "Flames on", "Blanket + tea"])
add(7, "1300", "serif", [c("v2", 9.5, 2.5), c("v4", 13.2, 2.8), c("v12", 9.8, 2.6)], "t08_tiktok_7318_d.mp3", 0, 4.6,
    lines=["a little fireplace", "for a big winter"], small="fits any shelf or nightstand")
add(7, "1900", "reveal", [c("v12", 4.6, 3.4), c("v6", 8.0, 2.6), c("v1", 2.0, 2.4)], "t04_tiktok_992951993.mp3", 0, 4.6, music_start=3.9,
    before="one click", after="and it's cozy", on_at=1.1)
# День 8
add(8, "0900", "captions", [c("v4", 4.0, 1.8), c("v4", 13.0, 2.6), c("v9", 13.5, 3.0)], "t13_tiktok_1293762064.mp3", 1, 4.0,
    lines=["add water", "press the button", "that's it", "5+ hours of cozy"], gap=0.75)
add(8, "1300", "split", [c("v6", 6.5, 4.0), c("v8", 22.0, 4.0)], "t11_arabic_original.mp3", 3, 3.5,
    clips2=[c("v10", 12.0, 4.0), c("v8", 29.0, 4.0)], top="warm orange", bottom="or any color")
add(8, "1900", "typewriter", [c("v1", 1.2, 3.2), c("v7", 5.0, 3.0), c("v12", 11.5, 1.8)], "t10_anastasia_original.mp3", 0, 5.4,
    lines=["dear diary,", "I bought a fireplace", "for my bedroom.", "best decision."], cps=17)
# День 9
add(9, "0900", "polaroid", [c("v2", 9.5, 2.5), c("v2", 10.5, 1.5), c("v4", 16.5, 2.0), c("v9", 14.9, 1.6)], "t05_tiktok_7318_a.mp3", 5, 3.5,
    title="christmas tree + fireplace = done")
add(9, "1300", "bigword", [c("v4", 12.4, 1.6), c("v9", 13.0, 1.6), c("v1", 1.5, 1.6), c("v12", 9.0, 1.6), c("v7", 6.0, 1.6)], "t07_tiktok_7318_c.mp3", 0, 5.0, music_start=26,
    words=[["NO", 0.1, 1.2], ["SMOKE", 1.3, 2.6], ["NO", 2.7, 3.6], ["ASH", 3.7, 5.0], ["JUST", 5.1, 6.2], ["COZY", 6.3, 8.0]], size=250)
add(9, "1900", "quote", [c("v7", 5.0, 3.4), c("v9", 13.6, 2.6), c("v4", 17.0, 1.6)], "t06_tiktok_7318_b.mp3", 2, 4.6, music_start=2.25,
    lines=["slow nights", "are the best nights"], small="7 flame colors · remote included")
# День 10
add(10, "0900", "letters", [c("v4", 13.5, 2.8), c("v2", 10.2, 1.8), c("v12", 8.3, 3.2)], "t03_rachel_rosie_home.mp3", 0, 5.0,
    phrases=[{"words": ["good", "morning"], "start": 0.3, "end": 3.4}, {"words": ["cozy", "edition"], "start": 4.0, "end": 7.8, "size": 180}])
add(10, "1300", "pov", [c("v8", 19.6, 2.6), c("v8", 25.5, 2.4), c("v6", 12.0, 2.8)], "t14_tiktok_654462780.mp3", 3, 4.4,
    text="you change the flame color every night depending on your mood")
add(10, "1900", "sticker", [c("v1", 1.2, 3.3), c("v7", 6.4, 2.0), c("v9", 12.6, 2.9)], "t09_tiktok_7318_e.mp3", 0, 4.0, music_start=9,
    title="Gift idea under $70", badge="$69", badge2="ONLY", old="$139.95", new="$69.95", small="30-day money back guarantee")
# День 11
add(11, "0900", "chat", [c("v12", 9.0, 3.0), c("v1", 1.3, 3.0), c("v4", 14.0, 3.0)], "t05_tiktok_7318_a.mp3", 0, 99,
    msgs=[["l", "is it safe to leave on all night?"], ["r", "yes! no real fire, no heat. it's just mist + light"], ["l", "ok I need one for my bedroom"], ["r", "reply COZY for the link"]])
add(11, "1300", "cinema", [c("v10", 13.0, 3.0), c("v6", 7.5, 3.0), c("v8", 27.5, 2.6)], "t13_tiktok_1293762064.mp3", 1, 5.8,
    lines=["seven colors", "one remote", "endless moods"], times=[[0.3, 2.8], [3.2, 5.0], [5.4, 8.6]])
add(11, "1900", "list", [c("v1", 1.2, 3.0), c("v12", 10.4, 3.0), c("v7", 5.4, 2.8)], "t08_tiktok_7318_d.mp3", 0, 4.0,
    title="perfect for", items=["Movie nights", "Reading in bed", "Falling asleep"])
# День 12
add(12, "0900", "serif", [c("v9", 12.8, 3.4), c("v2", 9.7, 2.2), c("v4", 17.0, 1.6)], "t10_anastasia_original.mp3", 0, 4.6,
    lines=["cozy isn't a season,", "it's a feeling"], small="fireplace glow + humidifier in one")
add(12, "1300", "reveal", [c("v4", 9.6, 3.9), c("v4", 15.0, 2.0), c("v9", 14.0, 2.4)], "t09_tiktok_7318_e.mp3", 4, 5.0, music_start=8.15,
    before="lights off…", after="flames on", on_at=1.85)
add(12, "1900", "captions", [c("v7", 5.0, 3.2), c("v1", 1.3, 2.8), c("v12", 11.0, 2.2)], "t06_tiktok_7318_b.mp3", 0, 4.4, music_start=2.25,
    lines=["quiet", "warm light", "cool mist", "zero noise"], gap=0.8)
# День 13
add(13, "0900", "split", [c("v4", 12.3, 4.0), c("v9", 13.0, 4.0)], "t03_rachel_rosie_home.mp3", 0, 3.5,
    clips2=[c("v12", 8.4, 4.0), c("v1", 1.2, 3.3), c("v7", 5.0, 0.7)], top="white", bottom="or black")
add(13, "1300", "typewriter", [c("v6", 8.0, 3.0), c("v10", 18.0, 2.6), c("v8", 31.0, 2.6)], "t11_arabic_original.mp3", 3, 5.0,
    lines=["FAQ: real fire?", "> no, LED + mist", "FAQ: oils included?", "> no, water only"], cps=20)
add(13, "1900", "polaroid", [c("v1", 1.2, 3.2), c("v12", 9.4, 2.8), c("v9", 14.9, 1.6)], "t08_tiktok_7318_d.mp3", 0, 3.5,
    title="tonight's view")
# День 14
add(14, "0900", "bigword", [c("v2", 9.5, 1.6), c("v4", 13.0, 1.6), c("v9", 14.0, 1.6), c("v12", 10.0, 1.6), c("v1", 2.0, 1.6)], "t14_tiktok_654462780.mp3", 5, 5.0,
    words=[["FIREPLACE", 0.1, 1.6], ["+", 1.7, 2.6], ["HUMIDIFIER", 2.7, 4.4], ["=", 4.5, 5.3], ["COZY", 5.4, 8.0]], size=200)
add(14, "1300", "quote", [c("v4", 12.6, 3.0), c("v2", 10.0, 2.0), c("v8", 23.0, 3.0)], "t05_tiktok_7318_a.mp3", 0, 4.6,
    lines=["the gift", "they'll use every night"], small="$69.95 · free US shipping")
add(14, "1900", "letters", [c("v7", 5.0, 3.0), c("v1", 1.2, 3.0), c("v12", 9.5, 2.6)], "t04_tiktok_992951993.mp3", 1, 5.0, music_start=0.5,
    phrases=[{"words": ["sweet", "dreams"], "start": 0.3, "end": 3.4}, {"words": ["cozy", "edition"], "start": 4.0, "end": 8.2, "size": 180}])

assert len(S) == 33
json.dump(S, open(os.path.join(os.path.dirname(__file__), "days04_14.json"), "w"), indent=1, ensure_ascii=False)
print(len(S), "specs")
