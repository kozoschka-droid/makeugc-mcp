#!/usr/bin/env python3
"""Flame Fireplace: рілси v2 за аналітикою 25.11 (переможці: дія в 1-й секунді + хук-інтрига; провал: настрій/подарунок зі статичним початком).
Структура: OPENER (дія: розпаковка / вмикання / пульт / пара піднімається) ~2.2 с → 1–2 сцени → кінцівка. Довжина ~8 с (менше гортають).
Олію НЕ показуємо (f3, f7 7.5–10), поки власниця не дозволить. Дати/слоти ті самі, що у v1 (93 рілси 02.12–01.01)."""
import json, os, random, subprocess, sys
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
R = ROOT + "/assets/flame/raw/"; M = ROOT + "/assets/music/"; O = ROOT + "/media/flame/reels_v2/"
OPEN = [("f7",12.4,14.8),("f4",0.2,2.6),("f7",0,2.4),("f6",0,2.4),("f5",0,2.4),("f1",1.2,3.6),("f2",0,2.4),("f7",10,12.4)]
MID = [("f1",3.6,6.2),("f1",6.2,8.8),("f5",0.4,3),("f7",2.5,5),("f7",5,7.1),("f4",0.4,3),("f2",0.3,2.9),("f6",0.4,3)]
END = [("f5",0.5,3),("f7",12.6,15),("f1",7.4,10)]
TRACKS = [("t03_rachel_rosie_home.mp3",0),("t05_tiktok_7318_a.mp3",0),("t06_tiktok_7318_b.mp3",2.25),("t07_tiktok_7318_c.mp3",26),
          ("t08_tiktok_7318_d.mp3",0),("t13_tiktok_1293762064.mp3",0),("t14_tiktok_654462780.mp3",0),
          ("t04_tiktok_992951993.mp3",0.5),("t09_tiktok_7318_e.mp3",9),("t10_anastasia_original.mp3",0),("track2_ornament_136bpm.mp3",0)]
# хуки за формулою переможців: інтрига / «дивись що буде» / процес
HOOKS = [
 "Guests always ask what this is 👀","Watch it turn on 😮","From box to flames in 30 seconds 📦🔥","Wait… that's not real fire? 😳","It fills the room with warm mist 😮",
 "Press one button and watch 👀","Nobody believes this is mist 😳","What happens when you press this? 🔥","This is not a fireplace… 👀","POV: you turn it on for the first time 😮",
 "Unboxing the thing everyone asks about 📦","Look closer… it's water 💧😳","My guests tried to touch the flame 😳","Turn the lights off and watch 🌙🔥","It took 10 seconds to set up ⏱️🔥",
 "The remote does this 😮","Wait for the flame… 👀","I didn't expect it to look this real 😳","Fill it with water, then this happens 💧🔥","Everyone stops at this table 👀",
 "Real fire or not? Comment your guess 👇","This is what $0 firewood looks like 🔥","My cat stared at it for 10 minutes 😳","Box → water → fire ✨","That glow though 😮",
 "What is this thing on my table? 👀","Watch the mist turn into flame 🔥","The first click is the best part 😮","I can't stop turning it on 😳","Is it fire? Is it mist? Watch 👀",
 "Opening the cozy box 📦","Christmas glow in one click 🎄😮","Lights off… now look 🌙","It looks hot. It's not 😳","Hands-on test: can you touch the flame? 👀",
 "Setting up my mini fireplace ⏱️","This is my most asked-about decor 👀","It's water and light. Seriously 😳","The flame changes color too 🌈😮","Wait until it's dark 🌙👀",
 "Unbox it with me 📦🔥","No plug for firewood needed 😅🔥","One button. Whole room changes 😮","Guess what this is before the end 👀","Mist that looks like fire 😳🔥",
 "Watch my living room change 😮","This made my guests go quiet 😳","Tiny fireplace, real reaction 😮","How it actually works 👀","Turn it on with me 🔥",
 "The thing on my coffee table everyone films 📱","Christmas tree + this = 😮","It's not smoke. It's mist 😳","Unboxing → first flame 🔥","Would you guess this is fake? 👀",
 "Watch the room light up 🔥","Pour water. Press. Wow 💧😮","Dark room test 🌙🔥","See it in real life 👀","Can't believe this is mist 😳",
 "Setting the mood in 3 seconds ⏱️","Watch the remote trick 😮","The flame at night 🌙👀","This is why my guests stay longer 😅","Last unboxing before Christmas 📦🎄",
 "Wait for the first flame… 😮","Christmas Eve glow test 🎄🔥","It glows. It mists. It's not fire 😳","Merry & glowing 🔥",
 "Holiday week glow test 🔥","Leftovers, movie, flame on 😮","Still can't believe it's mist 😳",
 "Lights off after Christmas 🌙","Watch it light up the room 👀","The best thing I unboxed this year 📦",
 "Winter nights look like this now 😮","Everyone asked about it at Christmas 👀","Turning it on again… 🔥",
 "Last week of the year, flame on 😮","Is it real fire? Final answer 👀","Cozy check: lights off, flame on 🌙",
 "Countdown mode: on 🔥","NYE setup in 10 seconds ⏱️","Watch the flame change color 🌈",
 "Pre-party glow test 🥂","Two days left of 2026 — flame on 😮","Goodbye 2026, hello glow 🔥",
 "Last morning of 2026 ☕🔥","Last sunset of 2026, then this 🌅","Midnight glow test 🥂",
 "Happy New Year from my glowing corner 🎆","First flame of 2027 🔥","First night of the year, lights off 🌙"]
BODY = ["Realistic 3D flame made of mist and light.","Just add water and turn it on with the remote.","No heat, no smoke — safe for any room.",
        "7 flame colors to match your mood.","A cozy fireplace look for any table."]
TAGS = ["#flamediffuser #fireplace #cozyhome #satisfying #fyp","#cozyvibes #aromadiffuser #homedecor #oddlysatisfying #fyp",
        "#fireplacedecor #cozyseason #roomdecor #viral #fyp","#flamehumidifier #cozyroom #homeinspo #satisfyingvideos #fyp"]

def build_plan():
    days = [date(2026,12,2)+timedelta(d) for d in range(31)]; rng = random.Random(2025); plan = []; n = 0
    for d in days:
        for hh in [10,14,19]:
            hook = HOOKS[n]; n += 1
            low = hook.lower()
            if any(w in low for w in ("unbox","box","opening")): op = rng.choice([OPEN[2], OPEN[3]])
            elif any(w in low for w in ("remote","press","button","click")): op = OPEN[1]
            elif any(w in low for w in ("water","pour")): op = OPEN[6]
            elif any(w in low for w in ("dark","night","lights off","midnight")): op = OPEN[4]
            else: op = rng.choice(OPEN)
            mids = rng.sample([m for m in MID if m[0] != op[0] or abs(m[1] - op[1]) > 2], 2 if rng.random() < 0.5 else 1)
            end = rng.choice(END); tr, ms = TRACKS[n % len(TRACKS)]
            plan.append({"n": n, "date": d.isoformat(), "hour": hh, "hook": hook, "body": BODY[n % len(BODY)], "tags": TAGS[n % 4],
                         "scenes": [op] + mids, "end": end, "track": tr, "ms": ms})
    return plan

def render(p):
    out = f"{O}v{p['n']:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"
    clips = [{"src": R + v + ".mp4", "start": s, "end": e} for v, s, e in p["scenes"]]; t = sum(e - s for _, s, e in p["scenes"])
    v, s, e = p["end"]; clips.append({"src": R + v + ".mp4", "start": s, "end": e}); t += e - s
    proj = {"out": out, "clips": clips, "audio": "music", "music": M + p["track"], "music_start": p["ms"],
            "texts": [{"text": p["hook"], "start": 0, "end": 99, "pos": "top"},
                      {"text": "Link in bio 🔥", "start": max(3.0, t - 3.0), "end": 99, "pos": "bottom"}]}
    os.makedirs(O, exist_ok=True); jp = f"/tmp/claude-0/flamev2_{p['n']}.json"; json.dump(proj, open(jp, "w"))
    subprocess.run(["python3", ROOT + "/editor/reel.py", jp], check=True, capture_output=True); return out

if __name__ == "__main__":
    plan = build_plan(); assert len(plan) == 93 and len(set(p["hook"] for p in plan)) == 93, (len(HOOKS), len(set(HOOKS)))
    json.dump(plan, open(os.path.dirname(os.path.abspath(__file__)) + "/reels_v2_plan.json", "w"), indent=1, ensure_ascii=False)
    only = [int(x) for x in sys.argv[1:]]
    for p in plan:
        if not only or p["n"] in only: print("OK", render(p), flush=True)
