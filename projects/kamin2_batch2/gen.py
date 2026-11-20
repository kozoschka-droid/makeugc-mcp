#!/usr/bin/env python3
"""Генерує 26 проєктів роликів Каміна 2 (партія 2). Слово-тригер для всіх: COZY."""
import json, random, os
R = "../../assets/fireplace/raw/"
M = "../../assets/music/"
# НЕ показувати набір олій з коробки (v5 2–8.6 с, v8 12–16 с): олії не входять у комплект
UNLIT = {  # полум'я ще НЕ горить
 "box": [("v8",0,1.5),("v8",2.0,3.2),("v8",4.0,5.4),("v8",6.0,8.0),("v8",9.0,11.5),
         ("v2",0,1.67),("v2",1.67,3.13),("v5",0.2,1.8),("v6",0.3,1.8),("v7",0,1.0),("v9",3.0,4.3),("v9",4.3,5.6),("v4",1.1,2.6)],
 "fill":[("v2",3.2,4.7),("v2",4.5,6.0),("v2",6.8,8.03),("v4",2.3,3.6),("v4",4.0,5.5),("v4",6.0,7.03),
         ("v6",2.0,3.0),("v6",3.0,4.5),("v7",1.2,2.4),("v7",2.4,3.4),("v3",2.4,3.4),("v3",3.6,4.8),("v3",4.8,6.3),("v8",9.0,11.5),],
 "remote":[("v8",17.5,18.9),("v2",8.03,8.75),("v4",9.4,11.4),("v7",3.8,4.75),("v6",4.6,5.6)],
}
LIT = {  # полум'я горить
 "warm":[("v1",1.17,4.58),("v2",9.8,12.07),("v3",0,1.5),("v3",7.0,9.4),("v4",0,0.9),("v4",12.0,14.0),("v4",14.8,16.8),("v4",17.0,18.7),
         ("v5",9.0,10.3),("v5",10.3,12.5),("v5",12.5,14.5),("v5",19.0,20.5),("v5",20.5,22.7),("v7",4.8,6.6),("v7",6.6,8.5),
         ("v8",20.0,21.6),("v9",0,1.9),("v9",6.0,7.0),("v9",7.0,9.0),("v9",9.0,11.0),("v9",11.0,12.8),("v9",13.0,16.5)],
 "dark":[("v1",1.17,4.58),("v7",4.8,6.6),("v7",6.6,8.5),("v4",14.8,16.8),("v4",17.0,18.7),("v9",13.0,16.5),("v3",0,1.5)],
 "color":[("v3",9.43,10.27),("v3",10.3,11.0),("v3",13.0,14.9),("v5",15.0,17.0),("v5",17.0,19.0),("v6",6.3,8.0),("v6",8.0,10.5),
          ("v6",10.6,13.6),("v6",14.0,15.8),("v8",21.7,24.0),("v8",24.0,26.5),("v8",26.5,28.5),("v8",28.5,30.5),("v8",30.5,32.5),("v8",32.5,35.0)],
 "xmas":[("v2",9.8,12.07)],
 "hand":[("v9",9.0,11.0),("v3",11.0,12.8),("v9",0,1.9)],
}
TR = {  # трек: (файл, bpm, music_start, drop у ролику або None)
 "track1":("track1_vapurly_drop10s.mp3",117,0,10.0), "t04":("t04_tiktok_992951993.mp3",72,0,5.0),
 "t05":("t05_tiktok_7318_a.mp3",81,0,7.3), "t09":("t09_tiktok_7318_e.mp3",63,9.0,10.0),
 "t03":("t03_rachel_rosie_home.mp3",144,0,None), "t06":("t06_tiktok_7318_b.mp3",65,2.25,None),
 "t07":("t07_tiktok_7318_c.mp3",144,26.0,None), "t08":("t08_tiktok_7318_d.mp3",76,0,None),
 "t10":("t10_anastasia_original.mp3",57,0,None), "t11":("t11_arabic_original.mp3",108,0,None),
 "t13":("t13_tiktok_1293762064.mp3",136,0,None), "t14":("t14_tiktok_654462780.mp3",152,0,None),
 "track2":("track2_ornament_136bpm.mp3",136,0,None),
}
CTA = ['Comment "COZY" for the link 🕯️', 'Comment "COZY" and I\'ll send you the link 🔥', 'Comment "COZY" to get yours ✨']

# (назва, трек, тип, пули до дропу, пули після/основні, хук, текст після дропу, загальна довжина)
REELS = [
 ("11_pov_coziest","t14","B",None,["warm","color","warm"],"POV: you found the coziest thing on the internet 🔥",None,10),
 ("12_homebody","t11","B",None,["warm","dark","warm"],"Tell me you're a homebody without telling me 🏠🔥",None,10),
 ("13_sign_winter","t04","A",["box","fill","remote"],["warm","warm"],"This is your sign to make your room cozy this winter ❄️","Fireplace + humidifier in one 😍",11),
 ("14_makes_sense","t13","B",None,["warm","color","warm"],"A fireplace that's also a humidifier? Makes sense 💧🔥",None,10),
 ("15_wait_flames","track1","A",["box","fill","fill","remote"],["warm","dark"],"Wait for the flames… 👀","Okay this is SO cozy 😍",13.5),
 ("16_pretend","t06","B",None,["warm","dark","warm"],"Me pretending I have a real fireplace 😌🔥",None,11),
 ("17_essential","t05","A",["box","fill","remote"],["warm","warm"],"The cozy season essential you didn't know you needed 🍂","It's a humidifier too 💧",12),
 ("18_not_fire","t09","A",["fill","fill","remote"],["dark","hand"],"It's not real fire… 🤯","It's cool mist + light 💨✨",13),
 ("19_always_cold","t08","B",None,["warm","warm","xmas"],"Gift idea for the person who's always cold 🥶🎁",None,11),
 ("20_small_apartment","t03","B",None,["warm","color","warm"],"Small apartment, big cozy energy 🏙️🔥",None,9.5),
 ("21_started_going","track1","A",["box","box","fill","remote"],["warm","color"],"How it started 📦","How it's going 🔥",13.5),
 ("22_rate_setup","t14","B",None,["warm","color","dark"],"Rate this cozy setup 1–10 👇",None,10),
 ("23_unboxing_gift","t05","A",["box","box","remote"],["warm","warm"],"Unboxing the coziest gift of the year 🎁","And then… 🤯",12),
 ("24_nightstand","t06","B",None,["dark","warm","dark"],"Your nightstand needs this 🌙",None,11),
 ("25_two_drops","t04","A",["fill","fill","remote"],["warm","warm"],"Just add water and… 💧","Instant cabin vibes 🌲🔥",11),
 ("26_which_color","t07","B",None,["color","color","color"],"Which color would you pick? 🌈",None,10),
 ("27_xmas_lights","track1","A",["box","fill","fill","remote"],["xmas","warm"],"When the Christmas lights aren't enough 🎄","Now THAT's cozy 🔥",13.5),
 ("28_reading_nook","t10","B",None,["warm","dark","warm"],"Reading nook upgrade 📖🔥",None,11),
 ("29_five_min_calm","t06","B",None,["dark","dark","warm"],"This is what 5 minutes of calm looks like 😮‍💨",None,11),
 ("30_quiet","t11","B",None,["warm","hand","warm"],"Looks like fire. Smells like heaven. Quiet as a whisper 🤫",None,10),
 ("31_guests_ask","t13","B",None,["warm","color","warm"],"Guests always ask where I got this 👀",None,10),
 ("32_starter_pack","t03","B",None,["warm","warm","color"],"Cozy girl starter pack ✅🔥",None,9.5),
 ("33_dark_room","t09","A",["box","fill","remote"],["dark","dark"],"Dark room + this = …","Instant cabin vibes 🌲🔥",13),
 ("34_best_purchase","track2","B",None,["warm","color","warm"],"Best purchase I made this winter 🔥",None,9),
 ("35_lights_off","t04","A",["fill","fill","remote"],["dark","dark"],"Turn the lights off for this one 🔦","😍🔥",11),
 ("36_cold_outside","t08","B",None,["warm","dark","warm"],"Cold outside, cozy inside ❄️🔥",None,11),
]

def pick(rng, pool, used, want):
    cands=[c for c in pool if c not in used] or pool
    c=rng.choice(cands); used.add(c)
    s,e=c[1],c[2]
    if e-s>want+0.05:
        off=rng.uniform(0,(e-s)-want); s=s+off; e=s+want
    return c[0],round(s,2),round(e,2)

for i,(name,tr,kind,pre,post,hook,after,total) in enumerate(REELS):
    rng=random.Random(1000+i)
    f,bpm,ms,drop=TR[tr]; beat=60/bpm
    while beat<0.45: beat*=2
    used=set(); clips=[]; t=0
    def add(pool,dur,last_lit=False):
        global t
        v,s,e=pick(rng,pool,used,dur)
        clip={"src":R+{"v1":"v1.mov"}.get(v,v+".mp4"),"start":s,"end":e}
        if rng.random()<0.3: clip["mirror"]=True
        if rng.random()<0.25: clip["zoom"]=round(rng.uniform(1.04,1.12),2)
        clips.append(clip); return e-s
    if kind=="A":
        # до дропу: кліпи по 2 удари, останній — пульт, щоб закінчитись рівно на дропі
        n=len(pre); seg=drop/n
        mk=lambda v,s_,e_: {"src":R+{"v1":"v1.mov"}.get(v,v+".mp4"),"start":s_,"end":e_,**({"mirror":True} if rng.random()<0.3 else {})}
        body=[]
        for p in pre[:-1]:
            v,s_,e_=pick(rng,UNLIT[p],used,round(max(0.6,min(2.2,seg)),2)); body.append(mk(v,s_,e_))
        v,s_,e_=pick(rng,UNLIT[pre[-1]],used,1.3); last=mk(v,s_,e_)
        cur=sum(c["end"]-c["start"] for c in body)+(last["end"]-last["start"])
        tries=0
        while drop-cur>0.02 and tries<10:
            gap=drop-cur
            v,s_,e_=pick(rng,UNLIT["fill"],used,min(gap,2.0))
            if gap<0.5:  # подовжуємо останній кліп перед пультом
                c=body[-1]; c["end"]=round(c["end"]+gap,2); cur+=gap; break
            body.append(mk(v,s_,e_)); cur+=e_-s_; tries+=1
        if cur>drop+0.02:  # обрізаємо перший кліп
            body[0]["end"]=round(body[0]["end"]-(cur-drop),2)
        clips+=body+[last]; t=sum(c["end"]-c["start"] for c in clips)
        dropt=t; j=0
        while t<total-0.3 and j<8:
            left=total-t
            d=left if left<3.0 else min(2.5,left/2)
            got=add(LIT[post[j%len(post)]],d); t+=got; j+=1
        texts=[{"text":hook,"start":0,"end":round(drop,2),"pos":"top"},
               {"text":after,"start":round(drop,2),"end":99,"pos":"top"},
               {"text":CTA[i%3],"start":round(drop+1.0,2),"end":99,"pos":"bottom"}]
        assert abs(dropt-drop)<0.05,(name,dropt)
    else:
        # естетика: склейки в такт, останній кліп довший
        k=len(post)
        while t<total-0.3:
            left=total-t
            if left<3.2: d=left
            else: d=beat*rng.choice([2,2,3,4])
            p=post[len(clips)%k]
            got=add(LIT[p],d); t+=got
            if len(clips)>12: break
        texts=[{"text":hook,"start":0,"end":round(min(6.0,t-3.5),2),"pos":"top"},
               {"text":CTA[i%3],"start":round(t-4.0,2),"end":99,"pos":"bottom"}]
        if name=="26_which_color":
            texts[0]["end"]=99
    proj={"out":f"../../out/kamin2_b2/{name}.mp4","audio":"music","music":M+f,"music_start":ms,"clips":clips,"texts":texts}
    json.dump(proj,open(os.path.join(os.path.dirname(__file__),name+".json"),"w"),ensure_ascii=False,indent=1)
    print(name, round(t,2), len(clips))
