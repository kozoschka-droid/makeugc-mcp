#!/usr/bin/env python3
"""Камін 2: історії 07.12–01.01 (26 днів x 3). 09:00 і 13:00 фото (photos_ai), 19:00 відео (сирі кадри без олій).
02–06.12 уже зроблені раніше: photo14 p10–p14 + video14 d10–d14 (19:00). Святкові фото/кадри з ялинкою — лише до 25.12.
Факти: камін + зволожувач, холодна пара + LED, 7 кольорів, пульт, бак 150 мл, 5+ годин, чорний/білий. Цін не пишемо. CTA — Reply COZY."""
import os, sys
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor"); os.chdir(ROOT)
import cards, vstory, pstory
P = "media/kamin2/photos_ai/"; O = "media/kamin2/stories/dec/"
HPH = ["ai15_xmas_coffee_table.jpg", "ai03_black_xmas_flames.jpg", "ai12_gift_unwrapped.jpg", "ai02_black_xmas_mist.jpg", "ai25_white_xmas_unlit.png", "ai23_gift_box_unlit.png"]
NPH = ["ai01_white_bedroom_flames.jpg", "ai11_movie_couple.jpg", "ai13_window_cocoa.jpg", "ai10_reading_nook.jpg", "ai18_bedroom_blue.png", "ai16_gaming_purple2.png",
       "ai20_white_movie_lit.png", "ai14_desk_laptop.jpg", "ai07_kitchen_cookies.jpg", "ai04_white_bedroom_mist.jpg", "ai09_studio_apartment.jpg", "ai08_gaming_purple.jpg"]
UNLIT = ["ai05_window_snow_unlit.png", "ai06_bed_book_unlit.png", "ai17_kitchen_unlit.png", "ai19_white_studio_unlit.png", "ai21_white_shelf_unlit.png",
         "ai22_white_bath_unlit.png", "ai24_desk_snow_unlit.png"]
LIT = {"ai05_window_snow_unlit.png": "ai13_window_cocoa.jpg", "ai06_bed_book_unlit.png": "ai10_reading_nook.jpg", "ai17_kitchen_unlit.png": "ai07_kitchen_cookies.jpg",
       "ai19_white_studio_unlit.png": "ai20_white_movie_lit.png", "ai21_white_shelf_unlit.png": "ai01_white_bedroom_flames.jpg",
       "ai22_white_bath_unlit.png": "ai04_white_bedroom_mist.jpg", "ai24_desk_snow_unlit.png": "ai14_desk_laptop.jpg"}
CTA = ['Reply "COZY" for the link', 'Reply "COZY" and get the link', 'DM me "COZY" for the link', 'Reply "GLOW" for the link']
H_TXT = ["christmas mood, on", "the coziest gift this year", "under the tree, glowing", "hosting? set the mood", "snowy night, warm glow",
         "gift idea for the cozy one", "holiday evenings, sorted", "merry and cozy", "unwrap the cozy", "christmas list: done"]
N_TXT = ["a fireplace for any shelf", "no smoke, no ash", "just water and light", "lights off, flames on", "calm evenings at home", "cozy without firewood",
         "small room, big glow", "your nightly ritual", "dry air? fixed", "mist that looks like fire", "relax mode: on", "every room, a fireplace", "glow after work"]
FAQ = [("Most asked", "Is it a real fire?", "No! It's cool water mist lit by LED light, so it looks like dancing flames. No smoke, no heat.", "Mist · Light · No fire"),
       ("Good to know", "Is it really a humidifier?", "Yes! A 150 ml tank puts out cool mist for 5+ hours on one fill.", "150 ml · Cool mist · 5+ hours"),
       ("Colors", "Can I change the flame color?", "Yes, 7 flame colors, right from the remote.", "7 colors · Remote"),
       ("Safety", "Can I leave it on all night?", "Yes. No real fire and no heat, just cool mist and soft light. Quiet enough for bedrooms.", "No fire · No heat · Quiet"),
       ("Where", "Where can I put it?", "Nightstand, desk, shelf or TV stand. It's small and fits anywhere.", "Bedroom · Desk · Living room"),
       ("Colors", "Black or white?", "Both! Pick the one that fits your room.", "Black · White")]
POLL = [("Orange or blue flame?", ["1 · Classic orange", "2 · Calm blue"]), ("Bedroom or living room?", ["1 · Bedroom", "2 · Living room"]),
        ("Black or white?", ["1 · Black", "2 · White"]), ("Gift it or keep it?", ["1 · Gift it", "2 · Keep it"]),
        ("Coffee or cocoa by the fire?", ["1 · Coffee", "2 · Cocoa"]), ("Movie or book tonight?", ["1 · Movie", "2 · Book"])]
CHAT = [[["l", "wait is that a real fireplace?"], ["r", "nope, it's mist and light lol"], ["l", "it looks so real"], ["r", "reply COZY, I'll send the link"]],
        [["l", "what do I get my sister for christmas"], ["r", "this fireplace humidifier"], ["l", "she'd love that"], ["r", "reply COZY for the link"]],
        [["l", "your room looks so cozy"], ["r", "it's the little fireplace"], ["l", "I need one"], ["r", "reply COZY and I'll send it"]],
        [["l", "is that thing hot?"], ["r", "nope, cool mist"], ["l", "so cool"], ["r", "reply COZY for the link"]]]
LISTS = [("why I love it", ["Looks like real fire", "Humidifier too", "7 flame colors"]), ("perfect for", ["Bedroom", "Home office", "Movie night"]),
         ("cozy night checklist", ["Blanket", "Hot drink", "Flames on"]), ("gift for", ["Mom", "Best friend", "Yourself"]),
         ("how it works", ["Pour water", "Press a button", "Relax"])]
TYPE = [["evening plan:", "[x] blanket", "[x] tea", "[x] flames on", "[ ] go to bed"], ["things that make", "my home cozy:", "> soft lights", "> a good book", "> this fireplace"],
        ["holiday prep:", "[x] tree", "[x] gifts", "[x] flames on", "[ ] relax"], ["dear diary,", "I got a fireplace.", "it fits on my nightstand.", "no firewood needed."]]
QUOTE = [(["cozy is", "a feeling"], "flames on"), (["slow nights,", "warm glow"], "no smoke · no ash"), (["small fireplace,", "big mood"], "just water and light"),
         (["home is where", "the glow is"], "fireplace + humidifier in one")]
DAYS = [date(2026, 12, 7) + timedelta(k) for k in range(26)]

def photo_specs():
    fmts = ["pov", "faq", "split", "poll", "list", "shop", "serif", "chat", "typewriter", "quote", "captions", "polaroid", "cinema", "letters", "promo", "faq",
            "pov", "poll", "list", "chat", "serif", "typewriter", "quote", "captions", "split", "shop", "polaroid", "letters", "cinema", "promo"]
    hi = ni = ui = 0; cs, ps = [], []; k = 0; c = {x: 0 for x in set(fmts)}
    for d in DAYS:
        xmas = d <= date(2026, 12, 25)
        for slot in ("0900", "1300"):
            f = fmts[k % len(fmts)]; k += 1; j = c[f]; c[f] += 1
            hol = xmas and slot == "1300" and f != "faq"
            if hol: ph = HPH[hi % len(HPH)]; hi += 1
            else: ph = NPH[ni % len(NPH)]; ni += 1
            txt = H_TXT[j % len(H_TXT)] if hol else N_TXT[(k + j) % len(N_TXT)]
            out = f"{O}p_{d.isoformat()[5:]}_{slot}_{f}.jpg"; cta = CTA[k % 4]; base = {"out": out, "photo": P + ph}
            if f == "faq":
                a = FAQ[j % len(FAQ)]; cs.append({**base, "type": "faq", "n": j % 6 + 1, "total": 6, "cat": a[0], "q": a[1], "a": a[2], "tag": a[3], "cta": cta})
            elif f == "poll":
                q = POLL[j % len(POLL)]; cs.append({**base, "type": "poll", "q": q[0], "opts": q[1], "cta": "Reply 1 or 2"})
            elif f == "shop":
                cs.append({**base, "type": "shop", "title": txt.capitalize(), "sub": "Fireplace glow + humidifier in one", "cta": cta})
            elif f == "promo":
                cs.append({**base, "type": "promo", "kicker": "holiday glow" if xmas else "fresh start", "title": "NO FIRE", "sub": "just mist and light · 7 colors", "cta": cta})
            elif f == "split":
                u = UNLIT[ui % len(UNLIT)]; ui += 1
                ps.append({**base, "photo": P + u, "style": "split", "photo2": P + LIT[u], "top": ["off", "lights off", "work mode", "day"][j % 4],
                           "bottom": ["on", "flames on", "cozy mode", "night"][j % 4], "cta": cta})
            elif f == "pov":
                ps.append({**base, "style": "pov", "text": ["you finally have a fireplace in your apartment", "lights off and the flames are on",
                           "your evening routine just got cozier", "guests ask where your fireplace came from"][j % 4], "cta": cta})
            elif f == "chat":
                ps.append({**base, "style": "chat", "msgs": CHAT[j % len(CHAT)], "cta": cta, "cta_start": 99})
            elif f == "list":
                l = LISTS[j % len(LISTS)]; ps.append({**base, "style": "list", "title": l[0], "items": l[1], "cta": cta})
            elif f == "typewriter":
                t = TYPE[j % len(TYPE)] if (xmas or j % len(TYPE) != 2) else TYPE[0]; ps.append({**base, "style": "typewriter", "lines": t, "cta": cta})
            elif f == "quote":
                q = QUOTE[j % len(QUOTE)]; ps.append({**base, "style": "quote", "lines": q[0], "small": q[1], "cta": cta})
            elif f == "serif":
                w = txt.split(", ") if ", " in txt else [txt]; ps.append({**base, "style": "serif", "lines": w, "small": "cool mist · warm light · 7 colors", "y": 1150, "cta": cta})
            elif f == "captions":
                ps.append({**base, "style": "captions", "lines": [["pour water", "press on", "flames", "cozy"], ["lights off", "flames on", "blanket", "relax"],
                           ["mist", "light", "flames", "wow"]][j % 3], "gap": 0.8, "y": 330, "cta": cta})
            elif f == "polaroid":
                ps.append({**base, "style": "polaroid", "title": txt, "cta": cta})
            elif f == "cinema":
                ps.append({**base, "style": "cinema", "lines": [txt], "times": [[0, 99]], "cta": cta})
            elif f == "letters":
                w = txt.split(" "); ps.append({**base, "style": "letters", "phrases": [{"words": [" ".join(w[:2]), " ".join(w[2:4])] if len(w) > 2 else w,
                           "start": 0, "end": 99, "size": 115}], "cta": cta})
    return cs, ps

R = "assets/fireplace/raw/"
def c(v, s, d, mirror=False):
    x = {"src": R + (v + ".mov" if v == "v1" else v + ".mp4"), "start": s, "dur": d}
    if mirror: x["mirror"] = True
    return x
# кадри без олій (v3, v5 не беремо; v8 12–16, v9 7–11, v12 2–4 — олії)
WARM = [("v12", 5.7, 2.4), ("v12", 8.4, 2.8), ("v4", 12.4, 2.6), ("v4", 15.0, 2.6), ("v9", 13.2, 2.8), ("v10", 11.5, 2.6), ("v1", 1.3, 3.0), ("v7", 5.2, 2.8)]
COLOR = [("v6", 7.0, 2.4), ("v8", 21.7, 2.2), ("v8", 24.0, 2.2), ("v8", 27.0, 2.2), ("v8", 30.0, 2.2), ("v10", 17.0, 2.4), ("v10", 20.0, 2.0)]
XM = [("v2", 9.6, 2.4), ("v2", 8.0, 1.6)]
VST = ["bigword", "pov", "captions", "list", "reveal", "split", "cinema", "typewriter", "chat", "serif", "quote", "letters", "polaroid", "list2"]
MUS = ["t14_tiktok_654462780.mp3", "t13_tiktok_1293762064.mp3", "t03_rachel_rosie_home.mp3", "t06_tiktok_7318_b.mp3", "t04_tiktok_992951993.mp3",
       "t11_arabic_original.mp3", "t08_tiktok_7318_d.mp3", "t05_tiktok_7318_a.mp3", "t10_anastasia_original.mp3", "t07_tiktok_7318_c.mp3"]

def video_specs():
    out = []
    for i, d in enumerate(DAYS):
        xmas = d <= date(2026, 12, 25); st = VST[i % len(VST)]; j = i // len(VST)
        if st == "bigword" and j == 0: cl = [COLOR[(i + q) % len(COLOR)] for q in range(5)]
        else:
            cl = [WARM[(i * 3) % len(WARM)], (COLOR if i % 2 else WARM)[(i * 2 + 1) % (len(COLOR) if i % 2 else len(WARM))], WARM[(i * 3 + 4) % len(WARM)]]
            if xmas and i % 3 == 0: cl[1] = XM[i % 2]
        clips = [c(v, s, dur, mirror=(q == 1 and i % 2 == 0)) for q, (v, s, dur) in enumerate(cl)]
        m = MUS[i % len(MUS)]
        s = {"out": f"{O}v_{d.isoformat()[5:]}_1900_{st}.mp4", "style": st, "clips": clips, "music": "assets/music/" + m,
             "music_start": 2.25 if "7318_b" in m else (26 if "7318_c" in m else 0), "cta": CTA[i % 4], "cta_start": 5.0}
        if st == "bigword":
            s["words"] = [["ONE", 0.1, 1.8], ["CLICK", 1.9, 3.6], ["7", 3.7, 5.2], ["COLORS", 5.3, 12]] if j == 0 else \
                         [["NO", 0.1, 1.4], ["FIRE", 1.5, 2.8], ["JUST", 2.9, 4.0], ["GLOW", 4.1, 12]]; s["size"] = 220
        elif st == "pov": s["text"] = ["it's 9pm, lights off, and your room finally feels like a cabin", "the flames are on and the night is slow"][j % 2]
        elif st == "captions": s["lines"] = [["pour water", "switch on", "watch the mist", "cozy"], ["no smoke", "no ash", "no heat", "just glow"]][j % 2]; s["gap"] = 0.8
        elif st == "list": s["title"] = ["holiday glow list" if xmas else "cozy night list", "why it's on my nightstand"][j % 2]; s["items"] = [["Movie night", "Reading", "Slow evenings"], ["Cool mist for dry air", "Soft glow to fall asleep", "7 flame colors"]][j % 2]
        elif st == "reveal": s["before"] = ["is it fire?", "wait for it"][j % 2]; s["after"] = ["it's just mist", "so cozy"][j % 2]; s["on_at"] = 2.0
        elif st == "split": s["clips"] = clips[:2]; s["clips2"] = clips[2:]; s["top"] = ["mist", "on"][j % 2]; s["bottom"] = ["flames", "cozy"][j % 2]; s["cta_start"] = 3.5
        elif st == "cinema": s["lines"] = ["a quiet evening", "soft glow", "flames on"] if j % 2 == 0 else ["slow night", "warm light", "home"]; s["times"] = [[0.3, 2.4], [3.0, 4.6], [5.2, 8.0]]
        elif st == "typewriter": s["lines"] = ["tonight's plan:", "> blanket", "> cocoa", "> flames on"] if j % 2 == 0 else ["cozy fireplace:", "> water + light", "> humidifier too", "> 7 colors"]; s["cps"] = 18
        elif st == "chat": s["msgs"] = CHAT[(i + 1) % len(CHAT)] if xmas else CHAT[[0, 2, 3][j % 3]]; s["cta_start"] = 99
        elif st == "serif": s["lines"] = ["slow nights,", "warm glow"] if j % 2 == 0 else ["cozy is", "a feeling"]; s["small"] = "cool mist · warm light"
        elif st == "quote": s["lines"] = ["just water", "and light"] if j % 2 == 0 else ["the coziest", "corner"]; s["small"] = "fireplace + humidifier in one"
        elif st == "letters": s["phrases"] = [{"words": ["no", "fire"], "start": 0.3, "end": 3.4}, {"words": ["just", "glow"], "start": 4.0, "end": 8.6, "size": 170}]
        elif st == "polaroid": s["title"] = ["my cozy corner", "small but cozy"][j % 2]; s["cta_start"] = 3.5
        elif st == "list2": s["style"] = "list"; s["title"] = "3 reasons I love it"; s["items"] = ["Looks like real fire", "Cool mist, no smoke", "Remote control"]
        out.append(s)
    return out

if __name__ == "__main__":
    os.makedirs(O, exist_ok=True); what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "photo"):
        cs, ps = photo_specs(); print(len(cs) + len(ps), "photo", flush=True)
        for s in cs: cards.build(s)
        for s in ps: pstory.build(s)
    if what in ("all", "video"):
        vs = video_specs(); print(len(vs), "video", flush=True)
        for s in vs: vstory.build(s); print("OK", s["out"], flush=True)
