#!/usr/bin/env python3
"""Відео-сторіз з анімованим текстом (як Canva «day in my life»): літери з'являються по одній
(підйом + проявлення), фраза відлітає вгору, далі наступна фраза; кліпи міняються з наїздом.
python3 editor/animtext.py spec.json
spec: {"out","music","clips":[{"src","start","dur"}],"phrases":[{"words":["cozy","night","in"],"start":0.2,"end":3.4}],
       "cta":"reply \"COZY\" for the link","cta_start":4.0}"""
import json, os, subprocess, sys, tempfile, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
FONT="/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf"; SMALL="/usr/share/fonts/opentype/inter/Inter-Regular.otf"
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def frame(t, spec, f, fs):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for ph in spec["phrases"]:
        s,e=ph["start"],ph["end"]
        if t<s or t>e+0.5: continue
        words=ph["words"]; size=ph.get("size",200); lh=int(size*1.0)
        fnt=ImageFont.truetype(FONT,size)
        y0=(H-lh*len(words))//2-60
        out=ease((t-e)/0.45) if t>e else 0      # вихід: вгору + зникання
        k=0
        for i,w in enumerate(words):
            tw=d.textlength(w,font=fnt); x=(W-tw)/2; y=y0+i*lh
            for ch in w:
                cw=d.textlength(ch,font=fnt)
                p=ease((t-s-k*0.07)/0.3); k+=1
                if p<=0: x+=cw; continue
                a=int(255*p*(1-out)); dy=int(40*(1-p))-int(120*out)
                if a>0:
                    d.text((x+3,y+dy+4),ch,font=fnt,fill=(0,0,0,int(a*0.35)))
                    d.text((x,y+dy),ch,font=fnt,fill=(255,255,255,a))
                x+=cw
            k+=2
    if spec.get("cta") and t>=spec.get("cta_start",99):
        p=ease((t-spec["cta_start"])/0.5); txt=spec["cta"]; tw=d.textlength(txt,font=fs)
        d.text(((W-tw)/2,H-420+int(20*(1-p))),txt,font=fs,fill=(255,255,255,int(235*p)))
    return im
def build(spec):
    tmp=tempfile.mkdtemp(); f=None; fs=ImageFont.truetype(SMALL,42)
    total=sum(c["dur"] for c in spec["clips"]); n=int(total*FPS)
    for i in range(n):
        frame(i/FPS,spec,f,fs).save(f"{tmp}/o{i:04d}.png")
    # кліпи з легким наїздом (zoom-in) і швидким переходом-спалахом між ними
    inp=[]; parts=[]
    for j,c in enumerate(spec["clips"]):
        inp+=["-ss",str(c["start"]),"-t",str(c["dur"]),"-i",c["src"]]
        nfr=int(c["dur"]*FPS)
        parts.append(f"[{j}:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,setsar=1,fps={FPS},"
                     f"zoompan=z='1+0.10*on/{nfr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                     f"trim=duration={c['dur']},setpts=PTS-STARTPTS[c{j}]")
    k=len(spec["clips"])
    fc=";".join(parts)+";"+"".join(f"[c{j}]" for j in range(k))+f"concat=n={k}:v=1:a=0[bg];"
    fc+=f"[{k}:v]format=rgba[ov];[bg][ov]overlay=0:0,format=yuv420p[v]"
    cmd=["ffmpeg","-v","error","-y",*inp,"-framerate",str(FPS),"-i",f"{tmp}/o%04d.png"]
    maps=["-map","[v]"]
    if spec.get("music"):
        cmd+=["-ss",str(spec.get("music_start",0)),"-i",spec["music"]]
        fc+=f";[{k+1}:a]atrim=duration={total},afade=t=out:st={total-0.7}:d=0.7[a]"; maps+=["-map","[a]"]
    cmd+=["-filter_complex",fc,*maps,"-c:v","libx264","-crf","20","-preset","medium","-c:a","aac","-t",str(total),"-movflags","+faststart",spec["out"]]
    subprocess.run(cmd,check=True); print("OK",spec["out"])
if __name__=="__main__":
    for s in json.load(open(sys.argv[1])): build(s)
