#!/usr/bin/env python3
"""Flame Fireplace: історії 02.12–01.01 — 09:00 і 13:00 фото, 19:00 відео. Щодня різні формати.
Фото media/flame/photos p01–p10 святкові (лише до 24.12), p11–p20 без свят. Відео з 25.12 лише f1 (без ялинки).
Факти: 3D полум'я з пари, підсвітка, 7 кольорів, пульт, наливаєш воду. Ціни/знижок не пишемо. CTA — Link in bio."""
import os, sys
from datetime import date, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, ROOT + "/editor")
import cards, vstory, pstory
EMB = (214, 98, 32)
cards.EMBER, cards.BG, cards.PEACH, cards.INK, cards.MUTE = EMB, (250, 246, 241), (246, 226, 208), (40, 28, 22), (120, 98, 86)
cards.BRAND = "Flame Fireplace"; cards.TAGLINE = "COZY FLAME, ZERO FIRE."; cards.POLL1 = (246, 214, 186)
vstory.EMBER = EMB; vstory.BRAND = "Flame Fireplace"; vstory.FRAME = (250, 246, 241)
d = list(vstory.cta_pill.__defaults__); d[1] = EMB + (255,); vstory.cta_pill.__defaults__ = tuple(d)
P = ROOT + "/media/flame/photos/"; O = ROOT + "/media/flame/stories_dec/"
HPH = [f"p{i:02d}.png" for i in range(1, 11)]
NPH = [f"p{i:02d}.png" for i in range(11, 21)]
CTA = ["Link in bio", "Tap the link in bio", "Shop via link in bio", "Find it via link in bio"]
H_TXT = ["christmas mood, on","the coziest gift this year","under the tree, glowing","hosting? set the mood",
         "snowy night, warm glow","gift idea for the cozy one","holiday evenings, sorted","merry and cozy",
         "unwrap the cozy","christmas list: done","cozy before the guests","silent night, soft glow"]
N_TXT = ["a fireplace for any table","no smoke, no ashes","just water and light","lights off, flame on","calm evenings at home",
         "cozy without firewood","small room, big glow","your nightly ritual","warm vibes, zero heat","mist that looks like fire",
         "relax mode: on","every room, a fireplace","glow after work","soft light, slow night"]
FAQ = [("Most asked","Is it a real fire?","No! It's cool mist lit from below, so it looks like a flickering flame. No smoke, no ashes.","Mist · Light · No fire"),
       ("How it works","How do I use it?","Fill the tank with water and switch it on with the button or the remote. That's it.","Water · Button · Remote"),
       ("Colors","Can I change the flame color?","Yes, there are 7 flame colors, from classic orange to calm blue.","7 colors"),
       ("Where","Where can I put it?","Coffee table, nightstand, desk or shelf. It's small and fits anywhere.","Bedroom · Office · Living room"),
       ("Gift","Is it a good gift?","It's one of those gifts people use every single evening. Cozy for any home.","Cozy gift idea"),
       ("Mood","Does it make the room cozy?","The soft flame glow and mist turn any corner into a calm, cozy spot.","Calm · Cozy · Warm glow")]
POLL = [("Where would you put it?",["1 · Bedroom","2 · Living room"]),("Orange or blue flame?",["1 · Classic orange","2 · Calm blue"]),
        ("Cozy night plan?",["1 · Movie","2 · Book"]),("Who would you gift it to?",["1 · Mom","2 · Myself"]),
        ("Lights on or off?",["1 · Lights off","2 · Lamp on"]),("Coffee or cocoa?",["1 · Coffee","2 · Cocoa"])]
CHAT = [[["l","wait you have a fireplace??"],["r","it's mist and light lol"],["l","it looks so real"],["r","link in bio!"]],
        [["l","what should I get my sister for christmas"],["r","this little flame fireplace"],["l","she'd love that"],["r","link's in my bio"]],
        [["l","your room looks so cozy"],["r","it's the flame diffuser"],["l","I need one"],["r","check the link in bio"]],
        [["l","is that thing hot?"],["r","nope, it's cool mist"],["l","so cool"],["r","link in bio :)"]]]
LISTS = [("why I love it",["Looks like real fire","No smoke, no ashes","7 flame colors"]),("perfect for",["Bedroom","Home office","Movie night"]),
         ("cozy night checklist",["Blanket","Hot drink","Flame on"]),("gift for",["Mom","Best friend","Yourself"]),
         ("how it works",["Pour water","Press a button","Relax"])]
TYPE = [["evening plan:","[x] blanket","[x] tea","[x] flame on","[ ] go to bed"],["things that make","my home cozy:","> soft lights","> a good book","> this flame"],
        ["holiday prep:","[x] tree","[x] gifts","[x] flame on","[ ] relax"],["dear diary,","I got a fireplace.","it fits on my desk.","no firewood needed."]]
QUOTE = [(["cozy is","a feeling"],"flame on"),(["slow nights,","warm glow"],"no smoke, no ashes"),(["small flame,","big mood"],"just water and light"),
         (["home is where","the glow is"],"flame fireplace")]

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
                cards_s.append({**base, "type": "shop", "title": txt.capitalize(), "sub": "Flame fireplace diffuser · 7 colors", "cta": cta})
            elif f == "promo":
                cards_s.append({**base, "type": "promo", "kicker": "holiday glow" if xmas else "fresh start", "title": "NO FIRE", "sub": "just mist and light · 7 colors", "cta": cta})
            elif f == "split":
                ph2 = NPH[ni % len(NPH)]; ni += 1
                ps_s.append({**base, "style": "split", "photo2": P + ph2, "top": ["day","bedroom","orange","desk"][j % 4], "bottom": ["night","living room","blue","nightstand"][j % 4], "cta": cta})
            elif f == "pov":
                ps_s.append({**base, "style": "pov", "text": ["you finally have a fireplace in your apartment","lights off and the flame is on","your evening routine just got cozier","guests ask where your fireplace came from"][j % 4], "cta": cta})
            elif f == "chat":
                ps_s.append({**base, "style": "chat", "msgs": CHAT[j % len(CHAT)], "cta": cta, "cta_start": 99})
            elif f == "list":
                l = LISTS[j % len(LISTS)]; ps_s.append({**base, "style": "list", "title": l[0], "items": l[1], "cta": cta})
            elif f == "typewriter":
                t = TYPE[j % len(TYPE)] if (xmas or j % len(TYPE) != 2) else TYPE[0]; ps_s.append({**base, "style": "typewriter", "lines": t, "cta": cta})
            elif f == "quote":
                q = QUOTE[j % len(QUOTE)]; ps_s.append({**base, "style": "quote", "lines": q[0], "small": q[1], "cta": cta})
            elif f == "serif":
                w = txt.split(", ") if ", " in txt else [txt]; ps_s.append({**base, "style": "serif", "lines": w, "small": "no smoke · no ashes · 7 colors", "y": 1150, "cta": cta})
            elif f == "captions":
                ps_s.append({**base, "style": "captions", "lines": [["pour water","press on","flame","cozy"],["lights off","flame on","blanket","relax"],["mist","light","flame","wow"]][j % 3], "gap": 0.8, "y": 330, "cta": cta})
            elif f == "polaroid":
                ps_s.append({**base, "style": "polaroid", "title": txt, "cta": cta})
            elif f == "cinema":
                ps_s.append({**base, "style": "cinema", "lines": [txt], "times": [[0, 99]], "cta": cta})
            elif f == "letters":
                w = txt.split(" "); ps_s.append({**base, "style": "letters", "phrases": [{"words": [" ".join(w[:2]), " ".join(w[2:4])] if len(w) > 2 else w, "start": 0, "end": 99, "size": 115}], "cta": cta})
    return cards_s, ps_s

R = "assets/flame/raw/"
XSC = [("f2",0,3),("f4",0,3),("f5",0,3),("f6",0,3),("f7",0,2.5),("f7",2.5,5),("f7",5,7.5),("f7",10,12.4),("f7",12.4,15),("f1",1,4),("f1",4,7),("f1",7,10)]
NSC = [("f1",1,3.8),("f1",3.8,6.6),("f1",6.6,9.6)]
VST = ["bigword","pov","captions","list","reveal","split","cinema","typewriter","chat","serif","quote","letters","polaroid","list2"]
MUS = ["t14_tiktok_654462780.mp3","t13_tiktok_1293762064.mp3","t03_rachel_rosie_home.mp3","t06_tiktok_7318_b.mp3","t04_tiktok_992951993.mp3",
       "t11_arabic_original.mp3","t08_tiktok_7318_d.mp3","t05_tiktok_7318_a.mp3","t10_anastasia_original.mp3","t07_tiktok_7318_c.mp3"]
def video_specs():
    days = [date(2026,12,2)+timedelta(k) for k in range(31)]; out = []
    for i, d in enumerate(days):
        xmas = d <= date(2026,12,24); st = VST[i % len(VST)]; j = i // len(VST)
        if xmas:
            cl = [XSC[(i * 3 + q * 5) % len(XSC)] for q in range(3)]; end = [("f5",0,3),("f7",12.4,15)][i % 2]
        else:
            r = i % 3; cl = [NSC[r], NSC[(r + 1) % 3], NSC[(r + 2) % 3]]; end = None
        clips = [{"src": R + f"{v}.mp4", "start": s, "dur": round(min(e - s, 2.8), 2), **({"mirror": True} if (not xmas and q == 1) else {})} for q, (v, s, e) in enumerate(cl)]
        if end: clips.append({"src": R + f"{end[0]}.mp4", "start": end[1], "dur": 2.0})
        m = MUS[i % len(MUS)]
        s = {"out": f"{O}v_{d.isoformat()[5:]}_1900_{st}.mp4", "style": st, "clips": clips, "music": "assets/music/" + m,
             "music_start": 2.25 if "7318_b" in m else (26 if "7318_c" in m else 0), "cta": CTA[i % 4], "cta_start": 5.5}
        if st == "bigword": s["words"] = [["MIST",0.1,1.6],["LIGHT",1.7,3.2],["FLAME",3.3,5.0],["COZY",5.1,10]] if j == 0 else [["NO",0.1,1.4],["FIRE",1.5,2.8],["JUST",2.9,4.0],["GLOW",4.1,10]]; s["size"] = 230
        elif st == "pov": s["text"] = ["you finally got a fireplace for your apartment","the flame is on and the night is slow","you can't stop staring at the flame"][j % 3]
        elif st == "captions": s["lines"] = [["pour water","switch on","watch the mist","cozy"],["no smoke","no ashes","no firewood","just glow"],["lights off","flame on","blanket","perfect"]][j % 3]; s["gap"] = 0.8
        elif st == "list": s["title"] = ["holiday glow list" if xmas else "cozy night list","why it's on my table","it's perfect for"][j % 3]; s["items"] = [["Movie night","Reading","Slow evenings"],["Looks like real fire","No smoke","7 colors"],["Bedroom","Desk","Living room"]][j % 3]
        elif st == "reveal": s["before"] = ["is it fire?","wait for it","watch this"][j % 3]; s["after"] = ["it's just mist","so cozy","so satisfying"][j % 3]; s["on_at"] = 2.0
        elif st == "split":
            s["clips"] = clips[:2]; s["clips2"] = clips[2:] if len(clips) > 2 else clips[:1]; s["top"] = ["mist","on","calm"][j % 3]; s["bottom"] = ["flame","cozy","glow"][j % 3]; s["cta_start"] = 3.5
        elif st == "cinema": s["lines"] = ["a quiet evening","soft glow","flame on"] if j % 2 == 0 else ["slow night","warm light","home"]; s["times"] = [[0.3,2.4],[3.0,4.6],[5.2,8.0]]
        elif st == "typewriter": s["lines"] = ["tonight's plan:","> blanket","> cocoa","> flame on"] if j % 2 == 0 else ["flame fireplace:","> water + light","> no smoke","> 7 colors"]; s["cps"] = 18
        elif st == "chat": s["msgs"] = CHAT[(i + 1) % len(CHAT)] if xmas else CHAT[[0, 2, 3][j % 3]]; s["cta_start"] = 99
        elif st == "serif": s["lines"] = ["slow nights,","warm glow"] if j % 2 == 0 else ["cozy is","a feeling"]; s["small"] = "no smoke · no ashes"
        elif st == "quote": s["lines"] = ["just water","and light"] if j % 2 == 0 else ["the coziest","corner"]; s["small"] = "flame fireplace diffuser"
        elif st == "letters": s["phrases"] = [{"words": ["no", "fire"], "start": 0.3, "end": 3.4}, {"words": ["just", "glow"], "start": 4.0, "end": 8.6, "size": 170}]
        elif st == "polaroid": s["title"] = ["my cozy corner","small but cozy"][j % 2]; s["cta_start"] = 3.5
        elif st == "list2": s["style"] = "list"; s["title"] = "3 reasons I love it"; s["items"] = ["Looks like real fire","Cool mist, no smoke","Remote control"]
        out.append(s)
    return out

if __name__ == "__main__":
    os.makedirs(O, exist_ok=True)
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "photo"):
        cs, ps = photo_specs(); print(len(cs) + len(ps), "photo stories", flush=True)
        for s in cs: cards.build(s)
        for s in ps: pstory.build(s)
    if what in ("all", "video"):
        vs = video_specs(); print(len(vs), "video stories", flush=True)
        for s in vs: vstory.build(s)
