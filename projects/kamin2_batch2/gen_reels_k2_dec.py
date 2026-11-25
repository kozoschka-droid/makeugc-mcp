#!/usr/bin/env python3
"""Камін 2 (Metricool «cozy fireplace» 8247119): 93 рілси 02.12-01.01 (10/14/18 Chicago) за формулою конкурентів 25.11
(та сама, що Flame v3): справжні руки/пакет/коробка -> полум'я, 6-9 с, текст від першої особи, кожен 6-й - «відповідь на коментар».
Сирі кадри assets/fireplace/raw (справжнє відео з телефона). Олію не показуємо. CTA - Comment COZY (як у всьому акаунті)."""
import json, os, random, subprocess, sys, importlib.util
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
HERE = os.path.dirname(os.path.abspath(__file__))
R = ROOT + "/assets/fireplace/raw/"; M = ROOT + "/assets/music/"; O = ROOT + "/media/kamin2/dec/"
_s = importlib.util.spec_from_file_location("v3", ROOT + "/projects/flame_dec/gen_reels_v3.py"); v3 = importlib.util.module_from_spec(_s); _s.loader.exec_module(v3)

# (кліп, старт, кінець, швидкість) — розмітка 25.11
UNBOX = [("v7.mp4",0,2.2,1.0),("v8.mp4",0,2.2,1.0),("v8.mp4",2,5.4,1.0),("v4.mp4",1,2.4,0.8),("v2.mp4",0,2.4,1.0),("v9.mp4",3,6,1.0),("v10.mp4",0,2.6,1.0),("v6.mp4",0,2,1.0)]
SETUP = [("v7.mp4",2,4.2,1.0),("v4.mp4",4,6.2,1.0),("v10.mp4",4,6,1.0),("v8.mp4",18,20,1.0),("v4.mp4",10,12,1.0),("v7.mp4",4,5.2,1.0),("v2.mp4",8,9.6,1.0)]
FLAME = [("v1.mov",1,4.5,0.8),("v2.mp4",9.6,12,0.7),("v4.mp4",15,18.6,0.8),("v5.mp4",9,13,0.8),("v7.mp4",5,8.4,0.8),("v8.mp4",20,22,0.7),("v9.mp4",13,16.4,0.8),
         ("v10.mp4",11,15.5,0.8),("v12.mp4",8,12.4,0.8),("v3.mp4",7,9.6,0.7),("v5.mp4",19.2,22.6,0.8),("v9.mp4",6.5,9,0.8)]
COZYF = [("v12.mp4",5.6,8,0.8),("v12.mp4",8,12.4,0.6),("v1.mov",1,4.5,0.6),("v9.mp4",13,16.4,0.6),("v7.mp4",5,8.4,0.6),("v2.mp4",9.6,12,0.5)]
COLORS = [("v8.mp4",22,26,1.0),("v8.mp4",28,33,1.0),("v6.mp4",6,11,1.0),("v5.mp4",15,19,1.0),("v10.mp4",17,22,1.0)]
XMAS = ("v2.mp4",8,12,0.85)

def recipe(kind, rng):
    if kind == "U": return [rng.choice(UNBOX), rng.choice(FLAME)]
    if kind == "R": return [rng.choice(SETUP), rng.choice(FLAME)]
    if kind == "P": return [rng.choice(SETUP[:3]), rng.choice(SETUP[3:]), rng.choice(FLAME)]
    if kind == "C": return [rng.choice(SETUP[3:]), rng.choice(COLORS)]
    if kind == "X": return [XMAS]
    return [rng.choice(COZYF)] if rng.random() < 0.5 else [rng.choice(COZYF), rng.choice(FLAME)]

COLOR_HOOKS = ["Which color would you pick? 🌈","Pick your color 👇","7 colors, one remote 🥹🌈","My favourite is the purple 💜"]
TAGS = ["#fireplace #humidifier #cozyhome #christmasdecor","#diffuser #humidifier #cozyvibes #christmasgift","#fireplacediffuser #cozy #homedecor #christmasdecor",
        "#diffuser #fireplace #cozyseason #giftideas"]
ANS = {"Where can I buy this? 😭": ("Comment COZY 🥹 I'll send the link", "Comment COZY and I'll send you the link 🥹"),
       "Is it real fire?? 😳": ("No, it's just mist and light 🥹", "No, it's mist and light, safe to touch 🥹 Comment COZY for the link"),
       "I need this, where is it from? 🥹": ("Comment COZY 🥹", "Comment COZY and I'll DM you the link 🥹")}

def build_plan():
    rng = random.Random(8247); hooks_pre = []
    gift, cozy = v3.GIFT[5:] + v3.GIFT[:5], v3.COZY[7:] + v3.COZY[:7]   # інший порядок, ніж у Flame
    for i in range(66):
        if i % 6 == 5: hooks_pre.append(("REPLY", v3.REPLY[(i // 6 + 1) % 3]))
        elif i % 11 == 3: hooks_pre.append(("C", COLOR_HOOKS[(i // 11) % 4]))
        elif i % 9 == 4: hooks_pre.append(("H", (v3.RITUAL + v3.SETUP)[(i // 9 + 3) % 8]))
        elif i % 2 == 0: hooks_pre.append(("H", gift[(i // 2) % len(gift)]))
        else: hooks_pre.append(("H", cozy[(i // 2) % len(cozy)]))
    post = iter(v3.POST[5:] + v3.POST[:5]); ny = iter(v3.NY); pre = iter(hooks_pre); plan = []; n = 0
    for d in [date(2026, 12, 2) + timedelta(k) for k in range(31)]:
        ds = d.isoformat()
        for hh in (10, 14, 18):
            n += 1
            if ds in v3.XMAS: t, h = "H", v3.XMAS[ds][[10, 14, 18].index(hh)]
            elif ds == "2027-01-01": t, h = "H", next(ny)
            elif ds >= "2026-12-26": t, h = "H", next(post)
            else: t, h = next(pre)
            if t == "REPLY": k = "U"
            elif t == "C": k = "C"
            elif "christmas" in h.lower() and ds <= "2026-12-25" and rng.random() < 0.5: k = "X"
            else: k = v3.kind_of(h)
            scenes = [{"v": v, "s": a, "e": b, "sp": sp, "mirror": rng.random() < 0.4, "zoom": round(rng.uniform(1.0, 1.1), 2)} for v, a, b, sp in recipe(k, rng)]
            if t == "REPLY":
                texts = [{"text": h, "start": 0, "end": 99, "pos": 0.22}, {"text": ANS[h][0], "start": 2.2, "end": 99, "pos": "bottom"}]; cap = ANS[h][1]
            else:
                texts = [{"text": h, "start": 0, "end": 99, "pos": "top"}]
                cap = h + ("\n\nComment COZY and I'll send you the link 👇" if n % 2 == 0 else "")
            tr, ms = v3.TRACKS[(n + 4) % len(v3.TRACKS)]
            plan.append({"n": n, "date": ds, "hour": hh, "type": t, "hook": h, "caption": cap + "\n\n" + TAGS[n % 4], "kind": k,
                         "scenes": scenes, "texts": texts, "track": tr, "ms": ms})
    return plan

def render(p):
    out = f"{O}k{p['n']:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"
    clips = [{"src": R + c["v"], "start": c["s"], "end": c["e"], "speed": c["sp"], "mirror": c["mirror"], "zoom": c["zoom"]} for c in p["scenes"]]
    proj = {"out": out, "clips": clips, "audio": "music", "music": M + p["track"], "music_start": p["ms"], "texts": p["texts"]}
    os.makedirs(O, exist_ok=True); os.makedirs("/tmp/claude-0", exist_ok=True); jp = f"/tmp/claude-0/k2dec_{p['n']}.json"; json.dump(proj, open(jp, "w"))
    subprocess.run(["python3", ROOT + "/editor/reel.py", jp], check=True, capture_output=True); return out

if __name__ == "__main__":
    plan = build_plan(); assert len(plan) == 93
    json.dump(plan, open(HERE + "/reels_k2_dec_plan.json", "w"), indent=1, ensure_ascii=False)
    only = [int(x) for x in sys.argv[1:]]
    for p in plan:
        if not only or p["n"] in only: print("OK", render(p), flush=True)
