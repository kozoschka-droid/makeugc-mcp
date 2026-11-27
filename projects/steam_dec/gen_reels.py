#!/usr/bin/env python3
"""Steam Cleaner: 93 рілси 02.12–01.01 (3/день 10/14/19 Chicago). До 24.12 — святкові тексти, з 25.12 — без свят
(і без кадру з ялинкою s5 13–15). Факти: лише вода, без хімії, ручний, насадки."""
import json, os, random, subprocess, sys
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
R = ROOT + "/assets/steam/raw/"; M = ROOT + "/assets/music/"; O = ROOT + "/media/steam/reels_dec/"
# сцени «брудно→чисто» (відео, початок, кінець)
SC = [("s1",0,3),("s1",3,6),("s1",6,9),("s1",9,11),("s1",11,13),("s2",0,3),("s2",3,6),("s2",6,9),("s2",9,12),("s2",12,14),
      ("s3",0,3),("s3",3,6),("s3",6,9),("s3",9,12),("s3",12,15),("s4",0,3),("s4",3,6),("s4",6,9),("s4",9,12),
      ("s5",3.2,6.2),("s5",6.2,9),("s5",9,12.8),("s6",0,4),("s6",4,8),("s6",8,11),("s6",11,15)]
END = [("s1",13,15),("s4",12,15),("s1",12.6,15)]          # фінальні кадри з товаром/людиною
XMAS_END = [("s5",13,15)]                                    # дівчина на фоні ялинки — лише до 24.12
UNBOX = ("s5",0,3.2)
TRACKS = [("t03_rachel_rosie_home.mp3",0),("t05_tiktok_7318_a.mp3",0),("t06_tiktok_7318_b.mp3",2.25),("t07_tiktok_7318_c.mp3",26),
          ("t08_tiktok_7318_d.mp3",0),("t11_arabic_original.mp3",0),("t13_tiktok_1293762064.mp3",0),("t14_tiktok_654462780.mp3",0),
          ("t04_tiktok_992951993.mp3",0.5),("t09_tiktok_7318_e.mp3",9),("t10_anastasia_original.mp3",0),("track2_ornament_136bpm.mp3",0)]
HOLI = ["Clean before the guests arrive 🎄","Holiday cooking mess? Gone in seconds 🍗","The gift that keeps the house clean 🎁",
 "Gift idea for the neat freak in your life 🎁","Pre-holiday deep clean, no scrubbing ✨","Hosting this year? You need this 👀",
 "After the holiday dinner… 😮‍💨","Your mom will love this gift 💝","Santa, I want this one 🎅","Holiday baking spills? No problem 🍪",
 "Clean home for the holidays, zero chemicals ❄️","Unwrap it. Fill with water. Clean everything 🎁","Gift for the person who has everything 🎁",
 "Christmas list: steam cleaner ✅","Guests are coming in 1 hour… ⏰","Last-minute gift that everyone uses 🎁",
 "Holiday kitchen reset in minutes 🎄","Before the family arrives 🏠","Stocking stuffer? More like home saver 🧦",
 "December deep clean checklist ✅","Make the holiday cleanup the easy part ✨","Who's hosting Christmas this year? 🙋‍♀️",
 "The most useful gift under the tree 🎄"]
GEN = ["No scrubbing, just steam 💨","Watch this grime disappear 👀","Oddly satisfying, right? 😌","Just water. No chemicals 💧",
 "Wait for it… 😮","Stubborn grease vs hot steam 🔥","Before and after in seconds ⏱","This is your sign to try steam cleaning ✨",
 "Small tool, big results 💪","The spots everyone forgets 👀","Why didn't I get this sooner 😭","Clean like a pro at home 🧽",
 "One tool, every mess 💨","Gross → fresh in seconds ✨","I could watch this all day 😍","Deep clean mode: ON 🧼",
 "Your oven door can look like this 👀","Grout looking sad? Watch this 😳","Bathroom glow up ✨","Kitchen reset, no chemicals 🍋",
 "Rate this transformation 1–10 👇","POV: cleaning is satisfying now 🫧","Things I stopped scrubbing by hand ✋","Car seat stain? Not anymore 🚗",
 "Sink drain glow up 😮","Steam does the hard part 💨","Mold in the fridge seal? Watch 👀","Range hood grease? Gone 🔥",
 "Small apartment, spotless home ✨","Cleaning hack you need to see 🤯","Pet-safe, kid-safe, just steam 🐶","Satisfying clean of the day ✨",
 "Microwave mess, meet hot steam 💨","Faucet limescale? Bye 👋","Tile grout before vs after 😳","The tool that lives in my kitchen now 🏠",
 "Weekend reset in 10 minutes ⏱","Chemical-free cleaning that actually works 🌿","My favorite cleaning tool, hands down 🫶",
 "Shower glass like new ✨","Burners look brand new again 🔥","Cabinet handles were gross 😬","Backsplash grease? Easy 💨",
 "Hot steam > scrubbing 💪","Clean home, calm mind 😌","This is so satisfying to watch 😍","Grime doesn't stand a chance 💥",
 "The cleaning tool everyone's asking about 👀","Every corner, every crevice 🔍","Heat + water = magic ✨"]
NEWYEAR_SAFE = ["Fresh start, fresh home ✨","New week, clean home 🧼","Reset your home without chemicals 🌿","Clean slate, literally ✨"]
BEN = ["Just fill it with water and go 💧","No chemicals, just hot steam 💨","Works on kitchen, bathroom and car 🚗","Comes with brushes and nozzles for every spot 🧽",
       "Handheld, light and powerful 💪","Safe for kids and pets — water only 🐶"]
CTA = 'Comment "STEAM" for the link 👇'
TAGS = ["#steamcleaner #cleaninghacks #cleantok #satisfyingclean #homehacks","#oddlysatisfying #steamcleaning #deepclean #cleaningasmr #cleanwithme",
        "#chemicalfree #ecocleaning #cleanhome #steamclean #cleaningmotivation","#kitchencleaning #bathroomcleaning #beforeandafter #cleaningtips #homecare"]
HTAGS = ["#holidaycleaning #christmascleaning #giftideas #steamcleaner #cleantok","#christmasgifts #giftsforher #steamcleaner #holidayhosting #cleanhome"]

# 27.11 аналітика IG: найменше гортають (skip 28–35%) рілси, що з 1-го кадру показують сильний бруд крупним планом;
# найбільше (64–70%) — ті, що починаються з вікна/скла/коробки/чистої поверхні. Тому перший кадр — лише «брудний».
STRONG = [("s3",3,6),("s2",0,3),("s6",0,4),("s3",0,3),("s2",12,14),("s4",0,3),("s5",6.2,9),("s1",9,11),("s6",11,15),("s4",9,12)]
HOOK_CLIP = {"oven door": ("s2",0,3), "Grout": ("s6",11,15), "Car seat": ("s4",0,3), "Sink drain": ("s3",3,6), "Range hood": ("s2",12,14),
             "Microwave": ("s3",0,3), "Burners": ("s6",0,4), "Backsplash": ("s6",11,15), "Tile grout": ("s6",11,15),
             "Stubborn grease": ("s6",0,4), "Mold in the fridge": ("s3",3,6), "Cabinet handles": ("s6",8,11), "Faucet": ("s4",6,9),
             "Shower glass": ("s4",3,6), "Holiday cooking": ("s6",0,4), "After the holiday dinner": ("s2",12,14), "Holiday baking": ("s3",0,3)}

def fix_opener(p, k):
    op = next((c for key, c in HOOK_CLIP.items() if key.lower() in p["hook"].lower()), STRONG[k % len(STRONG)])
    rest = [list(c) for c in p["scenes"] if tuple(c) != tuple(op) and tuple(c) != ("s5",0,3.2)]
    p["scenes"] = [list(op)] + rest[:max(2, len(p["scenes"]) - 1)]
    return p

def build_plan():
    days = [date(2026,12,2)+timedelta(d) for d in range(31)]
    rng = random.Random(77); hi = iter(HOLI); gi = iter(GEN + NEWYEAR_SAFE + GEN)
    plan = []; n = 0
    for d in days:
        xmas = d <= date(2026,12,24)
        for slot, hh in enumerate([10,14,19]):
            n += 1
            holiday_hook = xmas and slot == 1  # по одному святковому хуку на день
            hook = next(hi) if holiday_hook else next(gi)
            if not xmas and d.day == 1: hook = NEWYEAR_SAFE[slot] if slot < 3 else hook
            k = rng.choice([3,3,4])
            scenes = rng.sample(SC, k)
            if holiday_hook and rng.random() < 0.4: scenes[0] = UNBOX
            end = rng.choice(END + (XMAS_END if xmas else []))
            tr, ms = TRACKS[n % len(TRACKS)]
            body = BEN[n % len(BEN)]
            tags = HTAGS[n % 2] if holiday_hook else TAGS[n % 4]
            plan.append({"n": n, "date": d.isoformat(), "hour": hh, "hook": hook, "body": body, "tags": tags,
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
                      {"text": CTA.replace(" 👇", ""), "start": max(3.5, t - 4), "end": 99, "pos": "bottom"}]}
    os.makedirs(O, exist_ok=True); jp = f"/tmp/claude-0/steamreel_{p['n']}.json"; json.dump(proj, open(jp, "w"))
    subprocess.run(["python3", ROOT + "/editor/reel.py", jp], check=True, capture_output=True)
    return out

if __name__ == "__main__":
    plan = [fix_opener(p, i) for i, p in enumerate(build_plan())]; json.dump(plan, open(os.path.dirname(os.path.abspath(__file__)) + "/reels_plan.json", "w"), indent=1, ensure_ascii=False)
    only = [int(x) for x in sys.argv[1:]]
    for p in plan:
        if not only or p["n"] in only: print("OK", render(p), flush=True)
