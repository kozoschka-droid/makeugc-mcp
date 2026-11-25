#!/usr/bin/env python3
"""Flame Fireplace: рілси v3 за розбором конкурентів 25.11 (myfirehome 11.6M, vitraflame 7.2M, thesolume 5.4M, coseason 2.6M).
Формула хітів: перша секунда = справжні руки/кімната (розпаковка -> на тумбочку -> полум'я), 6-8 с,
текст від першої особи про емоцію / подарунок ("Every home needs this 🥹❤️"), без вигаданих історій,
опис = 1 коротке речення + 4 хештеги. Олію НЕ показуємо (f3, f7 7.5-10). Ті самі 93 слоти, що v2 (02.12-01.01)."""
import json, os, random, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
HERE = os.path.dirname(os.path.abspath(__file__))
R = ROOT + "/assets/flame/raw/"; M = ROOT + "/assets/music/"; O = ROOT + "/media/flame/reels_v3/"

# рецепти сцен: (кліп, старт, кінець, швидкість)
REC = {
 "U": [[("f6",0,3,1.0),("f5",0,3,0.75)],                       # руки дістають з коробки -> полум'я
       [("f7",0,2.5,1.0),("f7",2.5,5,1.0),("f7",12.4,15,0.8)],    # коробка -> ставить -> полум'я з ялинкою
       [("f6",0.3,3,1.0),("f7",12.4,15,0.8)]],
 "A": [[("f5",0,3,0.5)],                                           # атмосфера: темна спальня, лампа, полум'я
       [("f5",0,3,0.6),("f7",12.4,15,0.7)],
       [("f7",12.4,15,0.5),("f5",0.5,3,0.7)]],
 "R": [[("f4",0,3,1.0),("f5",0,3,0.75)],                         # пульт -> полум'я
       [("f7",10,12.4,1.0),("f7",12.4,15,0.7)]],
 "P": [[("f2",0,3,1.0),("f4",0.3,3,1.0),("f5",0.5,3,0.9)]],     # вода -> пульт -> полум'я
}
TRACKS = [("t03_rachel_rosie_home.mp3",0),("t05_tiktok_7318_a.mp3",0),("t06_tiktok_7318_b.mp3",2.25),("t07_tiktok_7318_c.mp3",26),
          ("t08_tiktok_7318_d.mp3",0),("t13_tiktok_1293762064.mp3",0),("t14_tiktok_654462780.mp3",0),
          ("t04_tiktok_992951993.mp3",0.5),("t09_tiktok_7318_e.mp3",9),("t10_anastasia_original.mp3",0),("track2_ornament_136bpm.mp3",0)]

GIFT = ["The best gift I gave my mom 🥹🎁","Christmas gift for the friend who's always cold 🎁❄️","Gift idea for the girl who has everything 🎁🥹",
        "My sister's Christmas gift is sorted 🎁","Unboxing my favourite Christmas gift 🥹📦","Cutest gift under $70 🎁","Opening it like it's Christmas morning 🎄📦",
        "For the cozy girl in your life 🎁🥹","Secret Santa? Sorted 🎅🎁","Gift for someone who loves cozy nights 🎁🌙","Early Christmas present to myself 🥹🎁",
        "Every mom needs this 🥹❤️","Bought one for my mom… now I want one too 🥹","Finally got it 😭📦","It's even prettier in real life 🥹","Unbox it with me 🥹📦",
        "Worth every penny 🥹","Took 1 minute to set up 🥹","The gift that made her say wow 🥹"]
COZY = ["Every home needs this 🥹❤️","Every room needs this 🥹🌙","Officially my favourite Christmas decoration 🎄🥹","It's so cozy 🥰","My mini fireplace 🥹🔥",
        "The coziest thing I own 🥰","My new bedtime routine 🌙🥹","Can't fall asleep without it now 😴🔥","I'm obsessed 😭🔥","Literally perfect 🥹🤍","So calming… 🥹",
        "Lights off, flame on 🌙🔥","Cold outside, cozy inside ❄️🥹","This is my happy place 🥹","Didn't know I needed this 😭","POV: your room at 10 pm 🌙",
        "Winter nights hit different now ❄️🔥","Christmas vibes in my bedroom 🎄🥹","The glow I needed this winter 🥹","Small apartment, big cozy 🥹🔥",
        "No fireplace? No problem 🥹🔥","Best purchase this winter 🥹","The vibe in my room right now 🥹","My nightstand, but cozier 🌙","Reading by the fire 📖🔥",
        "Hot cocoa + this 🥹☕","Tell me this isn't the coziest 🥹","It feels like a cabin 🥹🪵","Tag someone who needs this 🥹❤️","Cozy season is my favourite season 🥰"]
RITUAL = ["One click and my room feels like a cabin 🥹🪵","My favourite button in the house 🥹","End of the day ritual 🌙🔥","The moment I get home ❄️🔥","Press… and relax 🥹"]
SETUP = ["Just water and a few seconds 🥹💧","It's actually mist, not fire 🥹","No smoke, no ash, just cozy 🥹"]
REPLY = ["Where can I buy this? 😭", "Is it real fire?? 😳", "I need this, where is it from? 🥹"]   # «відповідь на коментар»
XMAS = {"2026-12-24": ["Christmas Eve by the fire 🎄🥹","Waiting for Santa like 🥹🔥","Christmas Eve, lights off 🌙🎄"],
        "2026-12-25": ["Merry Christmas from my cozy corner 🎄🔥","Christmas morning, flame on 🎁🥹","Our first Christmas with it 🥹❤️"]}
POST = ["Best gift I got this year 🥹","Still obsessed after Christmas 🥹","Leftovers, movie, flame on 🥹","The coziest week of the year 🥹","Lights off after Christmas 🌙🥹",
        "Every home needs this 🥹❤️","It's so cozy 🥰","My mini fireplace 🥹🔥","Lights off, flame on 🌙🔥","Cold outside, cozy inside ❄️🥹","I'm obsessed 😭🔥",
        "My new bedtime routine 🌙🥹","Literally perfect 🥹🤍","Winter nights hit different now ❄️🔥","Tag someone who needs this 🥹❤️",
        "New Year's Eve, cozy edition 🥂🔥","Goodbye 2026 🥹🔥","Last night of the year by the fire 🥂🥹"]
NY = ["Happy New Year from my cozy corner 🎆🥹","First night of 2027 🌙🔥","New year, same cozy 🥹"]
TAGS_PRE = ["#diffuser #humidifier #fireplace #christmasdecor","#diffuser #humidifier #cozyhome #christmasgift",
            "#fireplacediffuser #humidifier #cozy #christmasdecor","#diffuser #aromatherapy #fireplace #cozyvibes"]
TAGS_POST = ["#diffuser #humidifier #fireplace #cozyhome","#diffuser #humidifier #cozy #newyear","#fireplacediffuser #humidifier #cozyvibes #winter"]

def kind_of(h):
    l = h.lower()
    if any(w in l for w in ("gift","unbox","opening","got it","prettier","penny","set up","santa","sister","mom")): return "U"
    if any(w in l for w in ("click","button","ritual","get home","press")): return "R"
    if any(w in l for w in ("water","mist, not","smoke")): return "P"
    return "A"

def build_plan():
    v2 = json.load(open(HERE + "/reels_v2_plan.json")); rng = random.Random(2611)
    pre = []
    for i in range(66):   # 02.12-23.12: чергуємо подарунок / затишок, кожен 6-й - «відповідь на коментар», кожен 9-й - ритуал/вода
        if i % 6 == 5: pre.append(("REPLY", REPLY[(i // 6) % 3]))
        elif i % 9 == 4: pre.append(("H", (RITUAL + SETUP)[(i // 9) % 8]))
        elif i % 2 == 0: pre.append(("H", GIFT[(i // 2) % len(GIFT)]))
        else: pre.append(("H", COZY[(i // 2) % len(COZY)]))
    plan = []; q = iter(pre); post = iter(POST); ny = iter(NY); used = set()
    for n, s in enumerate(v2, 1):
        d = s["date"]
        if d in XMAS: t, h = "H", XMAS[d][[10, 14, 19].index(s["hour"])]
        elif d == "2027-01-01": t, h = "H", next(ny)
        elif d >= "2026-12-26": t, h = "H", next(post)
        else: t, h = next(q)
        k = "U" if t == "REPLY" else kind_of(h)
        rec = REC[k][rng.randrange(len(REC[k]))]
        scenes = [{"v": v, "s": a, "e": b, "sp": sp, "mirror": rng.random() < 0.5, "zoom": round(rng.uniform(1.0, 1.12), 2)} for v, a, b, sp in rec]
        tr, ms = TRACKS[n % len(TRACKS)]
        if t == "REPLY":
            texts = [{"text": h, "start": 0, "end": 99, "pos": 0.22}, {"text": "Yes, we sell them 🥹 link in bio", "start": 2.2, "end": 99, "pos": "bottom"}]
            cap = f"Yes, we sell them 🥹 Link in bio"
        else:
            texts = [{"text": h, "start": 0, "end": 99, "pos": "top"}]
            cap = h + (" Link in bio" if n % 3 == 0 else "")
        tags = (TAGS_POST if d >= "2026-12-26" else TAGS_PRE)[n % (3 if d >= "2026-12-26" else 4)]
        plan.append({"n": n, "date": d, "hour": s["hour"], "type": t, "hook": h, "caption": cap + " " + tags, "kind": k,
                     "scenes": scenes, "texts": texts, "track": tr, "ms": ms})
    return plan

def render(p):
    out = f"{O}v{p['n']:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"
    clips = [{"src": R + c["v"] + ".mp4", "start": c["s"], "end": c["e"], "speed": c["sp"], "mirror": c["mirror"], "zoom": c["zoom"]} for c in p["scenes"]]
    proj = {"out": out, "clips": clips, "audio": "music", "music": M + p["track"], "music_start": p["ms"], "texts": p["texts"]}
    os.makedirs(O, exist_ok=True); jp = f"/tmp/claude-0/flamev3_{p['n']}.json"; os.makedirs("/tmp/claude-0", exist_ok=True); json.dump(proj, open(jp, "w"))
    subprocess.run(["python3", ROOT + "/editor/reel.py", jp], check=True, capture_output=True); return out

if __name__ == "__main__":
    plan = build_plan(); assert len(plan) == 93
    json.dump(plan, open(HERE + "/reels_v3_plan.json", "w"), indent=1, ensure_ascii=False)
    only = [int(x) for x in sys.argv[1:]]
    for p in plan:
        if not only or p["n"] in only: print("OK", render(p), flush=True)
