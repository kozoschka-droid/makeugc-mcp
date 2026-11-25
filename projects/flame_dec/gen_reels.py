#!/usr/bin/env python3
"""Flame Fireplace (Камін 1): рілси 02.12–24.12 (3/день 10/14/19 Chicago). Сирі відео assets/flame/raw/f1–f7:
f1 1–10 камін з парою, без свят (горизонтальне, 0–1 = скрін картки товару — не брати);
f2 наливають воду (ялинка); f3 крапають олію — НЕ брати; f4 пульт вмикає (ялинка); f5 темна кімната, полум'я (ялинка);
f6 розпаковка (ялинка); f7: 0–2.5 дістають з коробки, 2.5–5 ставлять на стіл, 5–7.5 наливають воду, 7.5–10 олія (НЕ брати),
10–12.4 пульт, 12.4–15 вмикається полум'я біля ялинки. Факти: 3D полум'я, пара/аромат, 7 кольорів, пульт. Ціну не пишемо."""
import json, os, random, subprocess, sys
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
R = ROOT + "/assets/flame/raw/"; M = ROOT + "/assets/music/"; O = ROOT + "/media/flame/reels_dec/"
SC = [("f1",1,4),("f1",4,7),("f1",7,10),("f2",0,3),("f4",0,3),("f5",0,3),("f6",0,3),
      ("f7",0,2.5),("f7",2.5,5),("f7",5,7.5),("f7",10,12.4),("f7",12.4,15)]
END = [("f5",0,3),("f7",12.4,15),("f1",7,10)]
OPEN = [("f7",0,2.5),("f6",0,3)]
TRACKS = [("t03_rachel_rosie_home.mp3",0),("t05_tiktok_7318_a.mp3",0),("t06_tiktok_7318_b.mp3",2.25),("t07_tiktok_7318_c.mp3",26),
          ("t08_tiktok_7318_d.mp3",0),("t12_meghan_trainor_christmas.mp3",0),("t13_tiktok_1293762064.mp3",0),("t14_tiktok_654462780.mp3",0),
          ("t04_tiktok_992951993.mp3",0.5),("t09_tiktok_7318_e.mp3",9),("t10_anastasia_original.mp3",0),("track2_ornament_136bpm.mp3",0)]
HOOKS = [
 "A fireplace that fits on your table 🔥","No chimney? No problem 🏠","The coziest gift of the season 🎁","POV: your living room in December 🎄",
 "Real-looking flame. Zero heat. Zero smoke ✨","Fill with water, press a button 💧","Unboxing the gift I'm giving everyone 🎁","This is your sign to get cozy 🕯️",
 "Christmas mood in 3 seconds 🎄","Wait for the flame… 😍","Gift idea for the cozy girl in your life 🤍","Tiny fireplace, huge vibe 🔥",
 "Watch the mist turn into flame ✨","My favorite thing in my apartment right now 🏠","Evening routine: lights off, fireplace on 🌙","They'll use this gift every single night 🎁",
 "Renters, this one's for you 🔑","Cozy without the firewood 🪵","When the apartment has no fireplace… 😌","Secret Santa sorted 🎅",
 "Christmas movie night upgrade 🎬","Is it fire? Is it mist? Both ✨","Hot cocoa + this = perfect night ☕","Remote on. Flame on. 🔥",
 "Gift that looks way more expensive 👀","Makes any room feel like a cabin 🏔️","Your cozy corner is missing this 🛋️","Christmas is coming, get cozy 🎄",
 "I can't stop watching this flame 😍","Small table, big holiday glow ✨","Turn your nightstand into a fireplace 🌙","December nights hit different 🔥",
 "From box to cozy in 30 seconds 📦","Aroma, mist and a flame you can touch ✋","Gift for mom she'll actually use 💝","The cozy gift everyone's asking about 👀",
 "Living room glow up 🔥","Adds instant Christmas vibes ✨","Who needs a real fireplace? 🤷‍♀️","Under-the-tree gift idea 🎁",
 "This is how I relax after work 😌","Cozy season essential 🕯️","Calm, warm, glowing 🔥","Gift for the person who has everything 🎁",
 "That moment the flame turns on 😍","No smoke, no ashes, just cozy ✨","Fireplace vibes in a small apartment 🏠","Holiday hosting? Put this on the table 🍽️",
 "Pure cozy in one box 📦","A gift that sets the mood 🔥","Make your home smell and look cozy 🌲","Stocking stuffer? More like room changer 🧦",
 "Plug in. Pour water. Relax 💧","Bedroom, office, living room — anywhere 🔥","Christmas wishlist: this ✅","Why didn't I get this sooner 😭",
 "The flame that never burns 🔥","Winter evenings sorted ❄️","It's giving cabin in the woods 🪵","Last-minute gift that wows 🎁",
 "Cozy corner, finished ✅","Instant Christmas atmosphere 🎄","Lights off. Fireplace on. 🌙","The gift that keeps glowing ✨",
 "Holiday vibes without the mess 🧹","Most cozy thing I own 🤍","Merry & cozy 🔥","Christmas Eve mood 🎄","Cozy Christmas Eve vibes ✨"]
HOOKS2 = [
 "Holiday week, slow evenings 🔥","Cozy days between the holidays 🛋️","Christmas leftovers + flame on 🍪","Post-holiday reset mode 😌",
 "Movie marathon week needs this 🎬","Hot cocoa season isn't over ☕","The coziest week of the year ✨","Pajamas all day, flame all night 🌙",
 "Winter is just getting started ❄️","Ending the year by the fire 🔥","NYE plans: blanket, snacks, flame ✨","Countdown to 2027, cozy edition ⏳",
 "New Year's Eve at home? Same 🥂","Cozy goals for 2027 ✅","Treat yourself this new year 🤍","Ring in the new year warm 🔥",
 "Two days left of 2026 🔥","Goodbye 2026, hello cozy 2027 🎉","Last day of 2026, slow morning ☕","Last sunset of 2026, then this 🌅",
 "Midnight glow 🥂","Happy New Year from my cozy corner 🎆","Starting 2027 slow and warm ✨","First night of the year, flame on 🌙"]
BODY = ["Realistic 3D flame with soft mist and aroma.","Just add water and turn it on with the remote.","No heat, no smoke — safe for any room.",
        "7 flame colors to match your mood.","A cozy fireplace look for any table.","Perfect gift for cozy lovers this Christmas."]
BODY2 = ["Realistic 3D flame with soft mist and aroma.","Just add water and turn it on with the remote.","No heat, no smoke — safe for any room.",
        "7 flame colors to match your mood.","A cozy fireplace look for any table.","Cozy evenings all winter long."]
CTA_TEXT = "Link in bio 🔥"
TAGS = ["#flamediffuser #fireplace #cozyhome #christmasgift #fyp","#cozyvibes #aromadiffuser #christmasdecor #giftideas #fyp",
        "#fireplacedecor #cozyseason #homedecor #christmasgifts #fyp","#flamehumidifier #cozyroom #giftsforher #holidaydecor #fyp"]

def build_plan():
    days = [date(2026,12,2)+timedelta(d) for d in range(31)]
    rng = random.Random(41); plan = []; n = 0
    for d in days:
        for hh in [10,14,19]:
            hook = (HOOKS + HOOKS2)[n]; n += 1
            k = rng.choice([2,3,3])
            first = rng.choice(OPEN) if ("Unbox" in hook or "box" in hook) else None
            pool = [s for s in SC if s not in END and (first is None or s not in OPEN)]
            scenes = ([first] if first else []) + rng.sample(pool, k - (1 if first else 0))
            end = rng.choice(END)
            tr, ms = TRACKS[n % len(TRACKS)]
            if d > date(2026,12,24) and "christmas" in tr: tr, ms = TRACKS[0]
            plan.append({"n": n, "date": d.isoformat(), "hour": hh, "hook": hook, "body": (BODY if d <= date(2026,12,24) else BODY2)[n % len(BODY)], "tags": TAGS[n % 4],
                         "scenes": scenes, "end": end, "track": tr, "ms": ms, "mirror": n % 3 == 0})
    return plan

def render(p):
    out = f"{O}r{p['n']:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"
    clips = []; t = 0
    for i, (v, s, e) in enumerate(p["scenes"]):
        clips.append({"src": R + v + ".mp4", "start": s, "end": e, **({"mirror": True} if p["mirror"] and i == 1 else {})}); t += e - s
    v, s, e = p["end"]; clips.append({"src": R + v + ".mp4", "start": s, "end": e}); t += e - s
    proj = {"out": out, "clips": clips, "audio": "music", "music": M + p["track"], "music_start": p["ms"],
            "texts": [{"text": p["hook"], "start": 0, "end": 99, "pos": "top"},
                      {"text": CTA_TEXT, "start": max(3.0, t - 3.5), "end": 99, "pos": "bottom"}]}
    os.makedirs(O, exist_ok=True); jp = f"/tmp/claude-0/flamereel_{p['n']}.json"; json.dump(proj, open(jp, "w"))
    subprocess.run(["python3", ROOT + "/editor/reel.py", jp], check=True, capture_output=True)
    return out

if __name__ == "__main__":
    plan = build_plan(); assert len(plan) == 93 and len(set(p["hook"] for p in plan)) == 93
    json.dump(plan, open(os.path.dirname(os.path.abspath(__file__)) + "/reels_plan.json", "w"), indent=1, ensure_ascii=False)
    only = [int(x) for x in sys.argv[1:]]
    for p in plan:
        if not only or p["n"] in only: print("OK", render(p), flush=True)
