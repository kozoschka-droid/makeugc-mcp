#!/usr/bin/env python3
"""48 сторіз Каміна 2 (12 днів x 4). Слоти Chicago: 09 фото-перевага, 12 відео, 16 питання, 19 нічне відео."""
import json, os, random, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RAW = ROOT + "/assets/fireplace/raw/"; MUS = ROOT + "/assets/music/"; OUT = ROOT + "/media/kamin2/stories/"
sys.path.insert(0, ROOT + "/editor"); import story
CTA = 'Reply "COZY" for the link'
BEN = [("Your coziest winter nights 🔥","Fireplace + humidifier in one"),("Real fire vibes. Zero real fire 🔥","Cool mist + warm light"),
 ("Dry winter air? Fixed 💧","Built-in humidifier"),("Change the flame color 🌈","Right from the remote"),("So calm, so quiet 🤫","Perfect for bedrooms"),
 ("The gift everyone wants 🎁","Cozy for the holidays"),("No real flame 🔥","Just mist & light"),("Cabin vibes anywhere 🌲","Bedroom, desk, living room"),
 ("Fill with water. Press. Relax 💧","Easy as that"),("Your new evening ritual 🌙","Lights off, flames on"),("Small but SO cozy 🏠","Fits any shelf or nightstand"),
 ("Christmas Eve upgrade 🎄","Order in time for the holidays")]
Q = ["Orange or blue flame? 🧡💙","Bedroom or living room? 🛏️🛋️","Rate this vibe 1–10 🔥","Gift it or keep it? 🎁🏠","White or black? 🤍🖤",
 "Who would you gift this to? 🎁","Cozy night in or night out? 🌙","Which color is your mood? 🌈","Coffee or cocoa by the fire? ☕",
 "Christmas movie + this = ? 🎄","Would you fall asleep to this? 😴","Rate our setup 1–10 ✨"]
NOON = ["POV: your new favorite corner 🔥","Watch the flames dance 🔥","Color mode: ON 🌈","Instant cozy ✨","It's not fire… it's mist 🤯",
 "So satisfying 😌","Cozy check ✅","Desk vibes 💻🔥","Weekend mood 🛋️","Christmas mode 🎄","Just look at this glow ✨","Cozy season is here 🍂"]
NIGHT = ["Tonight's mood 🌙🔥","Lights off. Flames on 🔥","Movie night essential 🍿","Wind down with me 🌙","Sweet dreams 🔥😴","Date night setup 🥰",
 "Rainy night + this 🌧️","Reading by the fire 📖","Self-care night 🛁🔥","Cozy Sunday night 🔥","Calm mode: ON 😮‍💨","Good night from our cozy corner 🌙"]
WARM=[("v12",5.7,7.4),("v12",7.5,9.4),("v12",11.5,13.4),("v2",9.8,12.07),("v4",12.0,14.0),("v4",14.8,16.8),("v4",17.0,18.7),
 ("v9",6.0,9.0),("v9",9.0,11.0),("v9",13.0,16.5),("v10",11.5,14.0),("v8",20.0,21.6)]
COLOR=[("v6",6.3,8.0),("v6",8.0,10.5),("v6",10.6,13.6),("v8",21.7,24.0),
 ("v8",24.0,26.5),("v8",26.5,28.5),("v8",28.5,30.5),("v8",30.5,32.5),("v10",15.5,17.0),("v10",18.0,20.0)]
DARK=[("v1",1.17,4.58),("v7",4.8,6.6),("v7",6.6,8.5),("v12",9.5,11.3),("v12",0,1.0),("v4",14.8,16.8),("v9",13.0,16.5),("v12",11.5,13.4),("v12",7.5,9.4)]
TRACKS=["t06_tiktok_7318_b.mp3","t08_tiktok_7318_d.mp3","t10_anastasia_original.mp3","t05_tiktok_7318_a.mp3","t13_tiktok_1293762064.mp3","t11_arabic_original.mp3"]
# без p07, p08, p14: там видно набір олій
PHOTOS=["p01","p02","p03","p04","p05","p06","p09","p10","p11","p12","p13"]
def fn(v): return RAW+("v1.mov" if v=="v1" else v+".mp4")
def video(name, pools, rng, track):
    clips=[]; t=0; used=set()
    while t<6.5:
        pool=pools[len(clips)%len(pools)]; c=rng.choice([x for x in pool if x not in used] or pool); used.add(c)
        d=min(c[2]-c[1], 7.0-t, 2.6); s=round(c[1]+rng.uniform(0,max(0,(c[2]-c[1])-d)),2)
        clips.append({"src":fn(c[0]),"start":s,"end":round(s+d,2),**({"mirror":True} if rng.random()<0.3 else {})}); t+=d
    proj={"out":f"/tmp/claude-0/sv/{name}.mp4","audio":"music","music":MUS+track,"music_start":0,"clips":clips,"texts":[]}
    os.makedirs("/tmp/claude-0/sv",exist_ok=True); p=f"/tmp/claude-0/sv/{name}.json"; json.dump(proj,open(p,"w"))
    subprocess.run(["python3",ROOT+"/editor/reel.py",p],check=True,capture_output=True); return proj["out"]
specs=[]; plan=[]
for d in range(12):
    rng=random.Random(500+d)
    specs.append({"out":OUT+f"d{d+1:02d}_1.jpg","src":ROOT+f"/media/kamin2/photos/{PHOTOS[d%len(PHOTOS)]}.jpg","title":BEN[d][0],"sub":BEN[d][1],"cta":CTA,"hint":"Free US shipping"})
    specs.append({"out":OUT+f"d{d+1:02d}_2.mp4","src":video(f"d{d+1:02d}_2",[WARM,COLOR] if d%2 else [COLOR,WARM],rng,TRACKS[d%6]),"start":0,"dur":6.5,"title":NOON[d],"cta":CTA})
    specs.append({"out":OUT+f"d{d+1:02d}_3.jpg","src":ROOT+f"/media/kamin2/photos/{PHOTOS[(d+5)%len(PHOTOS)]}.jpg","title":Q[d],"cta":"Reply with your answer"})
    specs.append({"out":OUT+f"d{d+1:02d}_4.mp4","src":video(f"d{d+1:02d}_4",[DARK],rng,TRACKS[(d+3)%6]),"start":0,"dur":6.5,"title":NIGHT[d],"cta":CTA})
for s in specs: story.build(s)
