#!/usr/bin/env python3
"""Steam Cleaner: історії 02.12–01.01 — 09:00 і 13:00 фото, 19:00 відео. Щодня різні формати.
До 24.12 можна святкові фото/тексти; з 25.12 лише нейтральні (без ялинок, без кадру s5 13–15)."""
import json, os, sys
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor")
import cards, vstory, pstory
TEAL = (18, 140, 150)
cards.EMBER, cards.BG, cards.PEACH, cards.INK, cards.MUTE = TEAL, (246, 249, 250), (221, 238, 240), (22, 42, 48), (92, 118, 124)
cards.BRAND = "Luvinor Steam"; cards.TAGLINE = "CLEAN HOME, NO CHEMICALS."; cards.POLL1 = (196, 228, 232)
vstory.EMBER = TEAL; vstory.BRAND = "Luvinor Steam"; vstory.FRAME = (246, 249, 250)
d = list(vstory.cta_pill.__defaults__); d[1] = TEAL + (255,); vstory.cta_pill.__defaults__ = tuple(d)
P = ROOT + "/media/steam/photos_ai/"; O = ROOT + "/media/steam/stories_dec/"
HPH = ["s01_xmas_counter.png","s06_gift_box.png"] + [f"new/{x}" for x in ["x01_christmas_gift.png","x02_unwrapping_gift.png","x03_christmas_cookies.png",
      "x04_holiday_stovetop.png","x05_bathroom_sink.png","x06_dining_table.png","x07_snowy_window.png","x08_entryway_floor.png","x09_christmas_sofa.png","x10_presents_fireplace.png"]]
NPH = ["s02_faucet.png","s03_sofa.png","s04_laundry_shelf.png","s05_oven.png","s07_window.png","s08_car_seat.png","s09_product_kitchen.png",
       "s10_stovetop.png","s11_tile_grout.png"] + [f"new/{x}" for x in ["n11_glass_shower.png","n12_sunny_window.png","n13_window_blinds.png",
       "n14_car_dashboard.png","n15_sofa_stain.png","n16_mattress.png","n17_carpet_stain.png","n18_microwave.png","n19_refrigerator.png",
       "n20_sink_faucet.png","n21_high_chair.png","n22_bathroom_mirror.png","n23_toilet_base.png","n24_balcony_track.png","n25_accessories.png"]]
CTA = ['Reply "STEAM" for the link', 'Reply "STEAM" and get the link', 'DM me "STEAM" for the link', 'Reply "CLEAN" for the link']
# фото-формати: (тип, функція(i, фото, свято) -> поля)
H_TXT = ["clean before the guests arrive","the gift that cleans everything","holiday mess? just steam","hosting this year?",
         "after the holiday dinner","the most useful gift under the tree","santa, bring me this","clean home for the holidays",
         "unwrap. fill with water. clean.","christmas list: done","pre-holiday deep clean","stress-free hosting"]
N_TXT = ["no scrubbing, just steam","water only. no chemicals.","grime, meet hot steam","small tool, big results","every corner, every crevice",
         "fresh home, calm mind","clean like a pro","the spots everyone forgets","bye bye limescale","steam does the hard part",
         "weekend reset in 10 minutes","gross to fresh in seconds","safe for kids and pets","one tool, every room"]
FAQ = [("Most asked","Do I need cleaning products?","No! Just fill it with tap water. Hot steam loosens grease and grime on its own.","Water only · No chemicals"),
       ("Good to know","Is it safe on fabric?","Yes, use the cloth pad on sofas, mattresses and car seats. Test a small hidden spot first.","Sofa · Mattress · Car seats"),
       ("Attachments","What comes in the box?","Brushes, nozzles, a hose, a scraper and a cloth pad, so you can reach every spot.","Brushes · Nozzles · Hose"),
       ("Kitchen","Does it work on grease?","Yes! Hot steam softens baked-on grease on stovetops, ovens and range hoods. Wipe it away.","Stovetop · Oven · Hood"),
       ("Bathroom","Can it clean grout and glass?","Yes, use the small brush for grout and the window tool for shower glass and mirrors.","Grout · Glass · Mirrors"),
       ("Family","Is it safe around kids and pets?","It uses only water, so no chemical residue on high chairs, toys or floors.","Water only · No residue")]
POLL = [("What would you steam first?",["1 · Kitchen","2 · Bathroom"]),("Steam or scrub?",["1 · Steam, obviously","2 · I love scrubbing"]),
        ("Grossest spot at home?",["1 · Oven door","2 · Shower glass"]),("Clean the car or the couch?",["1 · Car seats","2 · Couch"]),
        ("Who would you gift it to?",["1 · Mom","2 · Myself"]),("Weekend plans?",["1 · Deep clean","2 · Nap"])]
CHAT = [[["l","how is your oven so clean??"],["r","steam. no chemicals, just water"],["l","wait seriously?"],["r","yep! reply STEAM for the link"]],
        [["l","what should I get my mom for christmas"],["r","this handheld steam cleaner"],["l","she'd actually use that"],["r","reply STEAM, I'll send it"]],
        [["l","your bathroom looks brand new"],["r","just steamed the grout lol"],["l","I need that"],["r","reply STEAM for the link"]],
        [["l","how did you get the stain out of the car seat?"],["r","hot steam + the cloth pad"],["l","sending me the link?"],["r","reply STEAM 👇"]]]
LISTS = [("3 spots to steam this week",["Oven door","Shower glass","Car seats"]),("why it's always in my kitchen",["Grease off in seconds","Water only","Small and light"]),
         ("steam these before guests",["Stovetop","Bathroom sink","Entryway floor"]),("perfect for",["Grout","Mattresses","High chairs"]),
         ("no more scrubbing",["Burners","Faucets","Window tracks"])]
TYPE = [["cleaning list:","[x] kitchen","[x] bathroom","[x] car","done before lunch"],["things I stopped","scrubbing by hand:","> oven door","> grout","> burners"],
        ["holiday prep:","[x] cookies","[x] gifts","[x] steam clean","[ ] relax"],["dear diary,","I steamed the fridge.","it's spotless.","no chemicals."]]
QUOTE = [(["limescale?","not anymore"],"just hot steam"),(["clean home,","calm mind"],"water only, no chemicals"),(["less scrubbing,","more living"],"steam does the hard part"),
         (["fresh start,","fresh home"],"small tool, big results")]

def photo_specs():
    days = [date(2026,12,2)+timedelta(k) for k in range(31)]
    fmts = ["pov","faq","split","poll","list","shop","serif","chat","typewriter","quote","captions","polaroid","cinema","letters","promo","faq",
            "pov","poll","list","chat","serif","typewriter","quote","captions","split","shop","polaroid","letters","cinema","promo"]
    hi = ni = 0; cards_s, ps_s = [], []; k = 0; c = {x: 0 for x in set(fmts)}
    for d in days:
        xmas = d <= date(2026,12,24)
        for slot in ("0900","1300"):
            f = fmts[k % len(fmts)]; k += 1; j = c[f]; c[f] += 1
            hol = xmas and slot == "1300" and f not in ("faq",)
            if hol: ph = HPH[hi % len(HPH)]; hi += 1
            else: ph = NPH[ni % len(NPH)]; ni += 1
            txt = (H_TXT[j % len(H_TXT)] if hol else N_TXT[(k + j) % len(N_TXT)])
            out = f"{O}p_{d.isoformat()[5:]}_{slot}_{f}.jpg"; cta = CTA[k % 4]; base = {"out": out, "photo": P + ph}
            if f == "faq":
                a = FAQ[j % len(FAQ)]; cards_s.append({**base, "type": "faq", "n": j % 6 + 1, "total": 6, "cat": a[0], "q": a[1], "a": a[2], "tag": a[3], "cta": cta})
            elif f == "poll":
                q = POLL[j % len(POLL)]; cards_s.append({**base, "type": "poll", "q": q[0], "opts": q[1], "cta": "Reply 1 or 2"})
            elif f == "shop":
                cards_s.append({**base, "type": "shop", "title": txt.capitalize(), "sub": "Handheld steam cleaner · water only", "cta": cta})
            elif f == "promo":
                cards_s.append({**base, "type": "promo", "kicker": "holiday clean" if xmas else "fresh start", "title": "WATER ONLY", "sub": "no chemicals · no scrubbing", "cta": cta})
            elif f == "split":
                ph2 = NPH[ni % len(NPH)]; ni += 1
                ps_s.append({**base, "style": "split", "photo2": P + ph2, "top": ["kitchen","before","bathroom","car"][j % 4], "bottom": ["bathroom","after","bedroom","couch"][j % 4], "cta": cta})
            elif f == "pov":
                ps_s.append({**base, "style": "pov", "text": ["you clean the oven without harsh chemicals","your bathroom finally sparkles","your car seats look brand new","guests arrive and everything is spotless"][j % 4], "cta": cta})
            elif f == "chat":
                ps_s.append({**base, "style": "chat", "msgs": CHAT[j % len(CHAT)], "cta": cta, "cta_start": 99})
            elif f == "list":
                l = LISTS[j % len(LISTS)]; ps_s.append({**base, "style": "list", "title": l[0], "items": l[1], "cta": cta})
            elif f == "typewriter":
                t = TYPE[j % len(TYPE)] if (xmas or j % len(TYPE) != 2) else TYPE[0]; ps_s.append({**base, "style": "typewriter", "lines": t, "cta": cta})
            elif f == "quote":
                q = QUOTE[j % len(QUOTE)]; ps_s.append({**base, "style": "quote", "lines": q[0], "small": q[1], "cta": cta})
            elif f == "serif":
                w = txt.split(", ") if ", " in txt else [txt]; ps_s.append({**base, "style": "serif", "lines": w, "small": "water only · no chemicals", "y": 1150, "cta": cta})
            elif f == "captions":
                ps_s.append({**base, "style": "captions", "lines": [["dirty","hot steam","no scrubbing","fresh"],["grease","steam","wipe","done"],["stain","steam","clean","wow"]][j % 3], "gap": 0.8, "y": 330, "cta": cta})
            elif f == "polaroid":
                ps_s.append({**base, "style": "polaroid", "title": txt, "cta": cta})
            elif f == "cinema":
                ps_s.append({**base, "style": "cinema", "lines": [txt], "times": [[0, 99]], "cta": cta})
            elif f == "letters":
                w = txt.split(" "); ps_s.append({**base, "style": "letters", "phrases": [{"words": [" ".join(w[:2]), " ".join(w[2:4])] if len(w) > 2 else w, "start": 0, "end": 99, "size": 150}], "cta": cta})
    return cards_s, ps_s

SC = [("s1",0,3),("s1",3,6),("s1",6,9),("s1",9,11),("s2",0,3),("s2",3,6),("s2",6,9),("s2",9,12),("s3",0,3),("s3",3,6),("s3",6,9),("s3",9,12),
      ("s3",12,15),("s4",0,3),("s4",3,6),("s4",6,9),("s4",9,12),("s5",3.2,6.2),("s5",9,12.8),("s6",0,4),("s6",4,8),("s6",8,11),("s6",11,15)]
VST = ["bigword","pov","captions","list","reveal","split","cinema","typewriter","chat","serif","quote","letters","polaroid","sticker"]
MUS = ["t14_tiktok_654462780.mp3","t13_tiktok_1293762064.mp3","t03_rachel_rosie_home.mp3","t06_tiktok_7318_b.mp3","t04_tiktok_992951993.mp3",
       "t11_arabic_original.mp3","t08_tiktok_7318_d.mp3","t05_tiktok_7318_a.mp3","t10_anastasia_original.mp3","t07_tiktok_7318_c.mp3"]
def video_specs():
    days = [date(2026,12,2)+timedelta(k) for k in range(31)]; out = []
    for i, d in enumerate(days):
        xmas = d <= date(2026,12,24); st = VST[i % len(VST)]; j = i // len(VST)
        cl = [SC[(i * 3 + q * 7) % len(SC)] for q in range(3)]
        end = ("s5",13,15) if xmas and i % 3 == 0 else ("s1",13,15)
        clips = [{"src": f"assets/steam/raw/{v}.mp4", "start": s, "dur": round(min(e - s, 2.8), 2)} for v, s, e in cl] + [{"src": f"assets/steam/raw/{end[0]}.mp4", "start": end[1], "dur": 2.0}]
        s = {"out": f"{O}v_{d.isoformat()[5:]}_1900_{st}.mp4", "style": st, "clips": clips, "music": "assets/music/" + MUS[i % len(MUS)],
             "music_start": 2.25 if "7318_b" in MUS[i % len(MUS)] else (26 if "7318_c" in MUS[i % len(MUS)] else 0), "cta": CTA[i % 4], "cta_start": 5.5}
        if st == "bigword": s["words"] = [["GRIME",0.1,1.6],["STEAM",1.7,3.2],["GONE",3.3,5.0],["WOW",5.1,10]] if j == 0 else [["GREASE",0.1,1.6],["HOT",1.7,2.8],["STEAM",2.9,4.4],["CLEAN",4.5,10]]; s["size"] = 230
        elif st == "pov": s["text"] = ["you finally stopped scrubbing by hand","cleaning the gross stuff is satisfying now","your kitchen is guest-ready in minutes"][j % 3]
        elif st == "captions": s["lines"] = [["burnt-on mess","hot steam","no chemicals","spotless"],["sink drain","grout","oven door","all clean"],["stains","steam","wipe","fresh"]][j % 3]; s["gap"] = 0.8
        elif st == "list": s["title"] = ["holiday cleanup list" if xmas else "weekend cleanup list","things steam can clean","before guests arrive" if xmas else "fresh start list"][j % 3]; s["items"] = [["Stovetop","Microwave","Shower glass"],["Grout","Car seats","Fridge seals"],["Oven door","Sink","Cabinet handles"]][j % 3]
        elif st == "reveal": s["before"] = ["watch this grime","wait for it","the gross part"][j % 3]; s["after"] = ["gone.","spotless ✨","so satisfying"][j % 3]; s["on_at"] = 2.0
        elif st == "split":
            s["clips"] = clips[:2]; s["clips2"] = clips[2:]; s["top"] = ["kitchen","before","grease"][j % 3]; s["bottom"] = ["bathroom","after","grime"][j % 3]; s["cta_start"] = 3.5
        elif st == "cinema": s["lines"] = ["a quiet clean","no chemicals","just steam"] if j % 2 == 0 else ["sunday reset","every corner","fresh home"]; s["times"] = [[0.3,2.4],[3.0,4.6],[5.2,8.0]]
        elif st == "typewriter": s["lines"] = ["things I don't","scrub anymore:","> burners","> grout","> oven door"] if j % 2 == 0 else ["steam cleaning:","> water only","> no chemicals","> no scrubbing"]; s["cps"] = 18
        elif st == "chat": s["msgs"] = CHAT[(i + 1) % len(CHAT)] if xmas else CHAT[[0, 2, 3][j % 3]]; s["cta_start"] = 99
        elif st == "serif": s["lines"] = ["less scrubbing,","more living"] if j % 2 == 0 else ["clean home,","calm mind"]; s["small"] = "water only · no chemicals"
        elif st == "quote": s["lines"] = ["just water","and heat"] if j % 2 == 0 else ["grime never","stood a chance"]; s["small"] = "handheld steam cleaner"
        elif st == "letters": s["phrases"] = [{"words": ["just", "steam"], "start": 0.3, "end": 3.4}, {"words": ["no", "chemicals"], "start": 4.0, "end": 8.6, "size": 170}]
        elif st == "polaroid": s["title"] = ["small but mighty","my favorite tool"][j % 2]; s["cta_start"] = 3.5
        elif st == "sticker": st2 = "list"; s["style"] = "list"; s["title"] = "why I love it"; s["items"] = ["Water only","Brushes for every spot","Light and handheld"]; s["out"] = s["out"].replace("sticker", "list2")
        out.append(s)
    return out

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "photo"):
        cs, ps = photo_specs(); print(len(cs) + len(ps), "photo stories")
        for s in cs: cards.build(s)
        for s in ps: pstory.build(s)
    if what in ("all", "video"):
        vs = video_specs(); print(len(vs), "video stories", flush=True)
        for s in vs: vstory.build(s)
