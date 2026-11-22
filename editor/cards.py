#!/usr/bin/env python3
"""Брендовані сторіз-картки Cozy Fireplace (стиль конкурентів: кремовий фон, serif, рамки).
Типи: shop, faq, promo, poll, deadline. python3 editor/cards.py spec.json"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
W, H = 1080, 1920
BG=(251,244,236); INK=(58,34,22); EMBER=(217,101,43); PEACH=(246,222,205); MUTE=(156,107,85); WHITE=(255,255,255)
PF = ROOT+"/assets/fonts/PlayfairDisplay.ttf"; IN="/usr/share/fonts/opentype/inter/Inter-Bold.otf"
INR="/usr/share/fonts/opentype/inter/Inter-Regular.otf" if os.path.exists("/usr/share/fonts/opentype/inter/Inter-Regular.otf") else IN
EMO="/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
def serif(size, w=700):
    f=ImageFont.truetype(PF,size)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def sans(size, bold=True): return ImageFont.truetype(IN if bold else INR, size)
def wrap(d, text, font, maxw):
    out=[]
    for para in text.split("\n"):
        line=""
        for w in para.split(" "):
            t=(line+" "+w).strip()
            if d.textlength(t,font=font)<=maxw: line=t
            else: out.append(line); line=w
        out.append(line)
    return out
def emoji(e, size):
    f=ImageFont.truetype(EMO,109); im=Image.new("RGBA",(160,160)); ImageDraw.Draw(im).text((0,0),e,font=f,embedded_color=True)
    im=im.crop(im.getbbox()); return im.resize((int(im.width*size/im.height),size),Image.LANCZOS)
def text_block(d, lines, font, y, color, x=None, lh=1.18, center=True):
    for ln in lines:
        tw=d.textlength(ln,font=font); xx=(W-tw)/2 if center else x
        d.text((xx,y),ln,font=font,fill=color); y+=int(font.size*lh)
    return y
def rounded_photo(path, w, h, r=36):
    im=Image.open(path).convert("RGB"); sc=max(w/im.width,h/im.height)
    im=im.resize((int(im.width*sc)+1,int(im.height*sc)+1)); im=im.crop(((im.width-w)//2,(im.height-h)//2,(im.width-w)//2+w,(im.height-h)//2+h))
    m=Image.new("L",(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],r,fill=255)
    out=Image.new("RGBA",(w,h)); out.paste(im,(0,0),m); return out
def shadow(canvas, box, r=36, off=18, blur=24, alpha=70):
    s=Image.new("RGBA",canvas.size,(0,0,0,0)); ImageDraw.Draw(s).rounded_rectangle([box[0],box[1]+off,box[2],box[3]+off],r,fill=(60,30,10,alpha))
    canvas.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))
def pill(d, cx, y, text, font, fill, color, padx=46, pady=24):
    tw=d.textlength(text,font=font); w=tw+padx*2; h=font.size+pady*2
    d.rounded_rectangle([cx-w/2,y,cx+w/2,y+h],h/2,fill=fill); d.text((cx-tw/2,y+pady-font.size*0.1),text,font=font,fill=color); return y+h
def brand(d, y=300, small=False):
    f=serif(46 if not small else 40); t="Cozy Fireplace"; d.text(((W-d.textlength(t,font=f))/2,y),t,font=f,fill=INK)

def shop(s, c, d):
    brand(d, 290)
    y=text_block(d, wrap(d,s["title"],serif(82),900), serif(82), 400, INK)
    y=text_block(d, wrap(d,s.get("sub",""),sans(38,False),880), sans(38,False), y+18, MUTE)
    ph=rounded_photo(s["photo"],760,760); x=(W-760)//2; yy=y+50
    shadow(c,(x,yy,x+760,yy+760)); c.alpha_composite(ph,(x,yy))
    if s.get("link_slot"):  # місце під наліпку-посилання (власниця додає сама)
        t="Tap the link to shop"; f=sans(36,False); d.text(((W-d.textlength(t,font=f))/2,yy+800),t,font=f,fill=MUTE)
        d.text((W/2-14,yy+850),"↓",font=sans(48),fill=MUTE)
    else:
        pill(d,W/2,yy+810,s.get("cta",'Reply "COZY" for the link'),sans(42),EMBER,WHITE)
    if s.get("hint"): f=sans(32,False); t=s["hint"]; d.text(((W-d.textlength(t,font=f))/2,1630),t,font=f,fill=MUTE)

def faq(s, c, d):
    m=90; f=serif(54,600); d.text((m,300),"Cozy Fireplace",font=f,fill=INK)
    t=f"FAQ / {s['n']:02d}"; fs=sans(30,False); d.text((W-m-d.textlength(t,font=fs),318),t,font=fs,fill=MUTE)
    d.line([m,395,W-m,395],fill=(214,180,160),width=3)
    d.text((m,470),s["cat"].upper(),font=sans(32,False),fill=EMBER)
    y=text_block(d, wrap(d,s["q"],serif(76,500),W-2*m), serif(76,500), 530, INK, x=m, center=False)
    fa=sans(42,False); lines=wrap(d,s["a"],fa,W-2*m-90); bh=len(lines)*int(42*1.3)+190
    d.rounded_rectangle([m,y+50,W-m,y+50+bh],40,fill=PEACH)
    yy=text_block(d,lines,fa,y+95,INK,x=m+45,lh=1.3,center=False)
    d.line([m+45,y+50+bh-95,W-m-45,y+50+bh-95],fill=(214,170,150),width=2)
    d.text((m+45,y+50+bh-70),s["tag"],font=sans(32,False),fill=MUTE)
    if s.get("photo"):  # фото в порожньому місці між відповіддю і нижньою лінією
        top=y+50+bh+40; h=1490-40-top
        if h>200:
            ph=rounded_photo(s["photo"],W-2*m,h,36); shadow(c,(m,top,W-m,top+h)); c.alpha_composite(ph,(m,top))
    d.line([m,1490,W-m,1490],fill=(214,180,160),width=3)
    d.text((m,1520),"COZY NIGHTS, ANYWHERE.",font=sans(28,False),fill=MUTE)
    for i in range(s.get("total",7)):
        x=W-m-(s.get("total",7)-i)*44; d.rounded_rectangle([x,1530,x+32,1538],4,fill=INK if i==s["n"]-1 else (214,170,150))
    if s.get("cta"): pill(d,W/2,1600,s["cta"],sans(38),EMBER,WHITE)

def promo(s, c, d):
    ph=rounded_photo(s["photo"],900,1150,44); x=(W-900)//2; y=330
    shadow(c,(x,y,x+900,y+1150)); c.alpha_composite(ph,(x,y))
    g=Image.new("RGBA",(900,1150)); gd=ImageDraw.Draw(g)
    for i in range(520): gd.line([0,i,900,i],fill=(20,10,5,int(150*(1-i/520))))
    m=Image.new("L",(900,1150),0); ImageDraw.Draw(m).rounded_rectangle([0,0,899,1149],44,fill=255)
    c.paste(Image.alpha_composite(c.crop((x,y,x+900,y+1150)),g),(x,y),m)
    f1=serif(78); t=s.get("kicker","CHRISTMAS SALE"); d.text(((W-d.textlength(t,font=f1))/2,y+70),t,font=f1,fill=(255,196,140))
    f2=sans(84); t=s.get("title","50% OFF"); d.text(((W-d.textlength(t,font=f2))/2,y+170),t,font=f2,fill=WHITE)
    if s.get("sub"): f3=sans(38,False); t=s["sub"]; d.text(((W-d.textlength(t,font=f3))/2,y+285),t,font=f3,fill=WHITE)
    d.text((x+40,y+1150-90),"Cozy Fireplace",font=serif(44),fill=WHITE)
    pill(d,W/2,y+1150+60,s.get("cta",'Reply "COZY" for the link'),sans(42),EMBER,WHITE)

def poll(s, c, d):
    ph=rounded_photo(s["photo"],640,800,36); x=70; y=300
    shadow(c,(x,y,x+640,y+800)); c.alpha_composite(ph,(x,y))
    bx=(290,1000,W-50,1110); d.rounded_rectangle(bx,34,fill=EMBER); d.rectangle([bx[0],bx[1]+40,bx[2],bx[3]],fill=EMBER)
    f=sans(48); t=s["q"]; d.text(((bx[0]+bx[2])/2-d.textlength(t,font=f)/2,bx[1]+28),t,font=f,fill=WHITE)
    d.rectangle([bx[0],bx[3],bx[2],bx[3]+300],fill=WHITE)
    yy=bx[3]+40
    for i,o in enumerate(s["opts"]):
        d.rounded_rectangle([bx[0]+40,yy,bx[2]-40,yy+100],50,fill=PEACH if i else (250,214,190))
        d.text((bx[0]+80,yy+28),o,font=sans(40),fill=INK); yy+=125
    d.text(((W-d.textlength(s.get("cta","Reply 1 or 2 👇"[:-2]),font=sans(36,False)))/2,1520),s.get("cta","Reply 1 or 2"),font=sans(36,False),fill=MUTE)

def deadline(s, c, d):
    brand(d, 290)
    f=serif(96); y=text_block(d, wrap(d,s["title"],f,900), f, 420, INK)
    d.rounded_rectangle([140,y+40,W-140,y+300],40,fill=PEACH)
    text_block(d, wrap(d,s["box"],sans(46),720), sans(46), y+90, INK)
    ph=rounded_photo(s["photo"],620,620,310); c.alpha_composite(ph,((W-620)//2,y+360))
    pill(d,W/2,y+1010,s.get("cta",'Reply "COZY" for the link'),sans(42),EMBER,WHITE)

def build(s):
    c=Image.new("RGBA",(W,H),BG+(255,)); d=ImageDraw.Draw(c)
    {"shop":shop,"faq":faq,"promo":promo,"poll":poll,"deadline":deadline}[s["type"]](s,c,d)
    # емодзі-акценти (за бажанням)
    for e,x,y,sz in s.get("emoji",[]): c.alpha_composite(emoji(e,sz),(x,y))
    os.makedirs(os.path.dirname(s["out"]),exist_ok=True); c.convert("RGB").save(s["out"],quality=93); print("OK",s["out"])
if __name__=="__main__":
    for s in json.load(open(sys.argv[1])): build(s)
