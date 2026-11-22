#!/usr/bin/env python3
"""28 фото-історій Каміна 2 (23.11–06.12), 09:00 і 13:00 Chicago; 19:00 — відео (video14).
Формати: картки cards.py (shop/faq/promo/poll) + стилі vstory статично (pstory.py)."""
import json, os
P = "media/kamin2/photos_ai/"; O = "media/kamin2/stories/photo14/"
D = ["23", "24", "25", "26", "27", "28", "29", "30", "01", "02", "03", "04", "05", "06"]
def out(i, slot, name): return f"{O}p{i+1:02d}_{D[i]}_{slot}_{name}.jpg"
CTA = ['Reply "COZY" for the link', 'Reply "COZY" and get the link', 'DM me "COZY" for the link', 'Reply "FIRE" for the link',
       'Reply "LINK" and I\'ll send it', 'Reply "GLOW" for the link']
cards, ps = [], []
def card(i, slot, typ, photo, **kw): cards.append({"type": typ, "out": out(i, slot, typ), "photo": P + photo, **kw})
def pst(i, slot, style, photo, cta=0, **kw):
    if "photo2" in kw: kw["photo2"] = P + kw["photo2"]
    ps.append({"style": style, "out": out(i, slot, style), "photo": P + photo, "cta": CTA[cta], **kw})

# 1 — 23.11
pst(0, "0900", "pov", "ai11_movie_couple.jpg", text="movie night, but make it cozy")
card(0, "1300", "promo", "ai15_xmas_coffee_table.jpg", kicker="cozy season sale", title="50% OFF", sub="$139.95 → $69.95 · free US shipping")
# 2 — 24.11
pst(1, "0900", "split", "ai05_window_snow_unlit.png", photo2="ai13_window_cocoa.jpg", top="lights off", bottom="flames on", cta=3)
card(1, "1300", "faq", "ai18_bedroom_blue.png", n=1, total=4, cat="Most asked", q="Is it safe to leave on all night?",
     a="Yes! There's no real fire and no heat, just cool water mist and LED light. One fill lasts 5+ hours.", tag="No fire · No heat · 5+ hours", cta=CTA[0])
# 3 — 25.11
pst(2, "0900", "quote", "ai10_reading_nook.jpg", lines=["a book, a blanket", "and this glow"], small="that's the whole plan tonight", cta=0)
card(2, "1300", "poll", "ai16_gaming_purple2.png", q="Which flame is your mood?", opts=["1 · Classic orange", "2 · Purple vibes"], cta="Reply 1 or 2")
# 4 — 26.11
pst(3, "0900", "typewriter", "ai14_desk_laptop.jpg", lines=["to-do:", "> finish work", "> light the fireplace", "> relax"], cta=1)
card(3, "1300", "shop", "ai12_gift_unwrapped.jpg", title="The gift that gets a \"wow\"", sub="Fireplace glow + humidifier in one", cta=CTA[0])
# 5 — 27.11
pst(4, "0900", "captions", "ai07_kitchen_cookies.jpg", lines=["baking day", "cookies in the oven", "fireplace on", "perfect"], gap=0.8, y=330, cta=0)
pst(4, "1300", "sticker", "ai09_studio_apartment.jpg", title="Small apartment? Still cozy.", badge="-50%", old="$139.95", new="$69.95", small="free US shipping", cta=4)
# 6 — 28.11
pst(5, "0900", "serif", "ai13_window_cocoa.jpg", lines=["snow outside,", "glow inside"], small="cool mist · warm light", y=1150, cta=0)
pst(5, "1300", "chat", "ai20_white_movie_lit.png", msgs=[["l", "wait is that a real fireplace on your TV stand?"], ["r", "nope, it's a humidifier with LED flames"],
     ["l", "that's genius. I need it"], ["r", "reply COZY and I'll send the link"]], cta_start=99)
# 7 — 29.11
pst(6, "0900", "list", "ai18_bedroom_blue.png", title="why it's on my nightstand", items=["Cool mist for dry air", "Soft glow to fall asleep", "7 flame colors"], cta=0)
pst(6, "1300", "polaroid", "ai25_white_xmas_unlit.png", title="the white edition", cta=5)
# 8 — 30.11
pst(7, "0900", "cinema", "ai01_white_bedroom_flames.jpg", lines=["goodnight, cozy"], times=[[0, 99]], cta=0)
pst(7, "1300", "split", "ai17_kitchen_unlit.png", photo2="ai07_kitchen_cookies.jpg", top="off", bottom="on", cta=3)
# 9 — 01.12
pst(8, "0900", "pov", "ai16_gaming_purple2.png", text="your gaming setup finally has a fireplace", cta=1)
card(8, "1300", "faq", "ai22_white_bath_unlit.png", n=2, total=4, cat="Good to know", q="Is it really a humidifier?",
     a="Yes! It has a 150 ml water tank and puts out cool mist for 5+ hours. The flame effect is just LED light.", tag="150 ml tank · Cool mist · Quiet", cta=CTA[2])
# 10 — 02.12
pst(9, "0900", "letters", "ai03_black_xmas_flames.jpg", phrases=[{"words": ["merry", "& cozy"], "start": 0, "end": 99}], cta=0)
card(9, "1300", "promo", "ai21_white_shelf_unlit.png", kicker="still on sale", title="HALF PRICE", sub="now $69.95 · was $139.95")
# 11 — 03.12
pst(10, "0900", "quote", "ai02_black_xmas_mist.jpg", lines=["christmas looks", "a little like this"], small="fireplace glow + humidifier in one", cta=2)
card(10, "1300", "shop", "ai19_white_studio_unlit.png", title="Black or white?", sub="Both fit any room. Both $69.95.", cta=CTA[1])
# 12 — 04.12
pst(11, "0900", "split", "ai24_desk_snow_unlit.png", photo2="ai14_desk_laptop.jpg", top="work mode", bottom="cozy mode", cta=0)
pst(11, "1300", "typewriter", "ai23_gift_box_unlit.png", lines=["gift list:", "[x] mom", "[x] sister", "[x] me, obviously"], cta=4)
# 13 — 05.12
pst(12, "0900", "captions", "ai04_white_bedroom_mist.jpg", lines=["bedtime routine:", "tea", "a good book", "fireplace on"], gap=0.8, y=330, cta=0)
card(12, "1300", "poll", "ai11_movie_couple.jpg", q="Movie night pick?", opts=["1 · Rom-com", "2 · Thriller"], cta="Reply 1 or 2")
# 14 — 06.12
pst(13, "0900", "serif", "ai06_bed_book_unlit.png", lines=["slow evenings", "are underrated"], small="5+ hours of mist on one fill", y=1150, cta=5)
pst(13, "1300", "sticker", "ai08_gaming_purple.jpg", title="Gamer gift idea under $70", badge="$69", badge2="ONLY", old="$139.95", new="$69.95", small="7 flame colors + remote", cta=3)

assert len(cards) + len(ps) == 28, len(cards) + len(ps)
d = os.path.dirname(os.path.abspath(__file__))
json.dump(cards, open(d + "/cards.json", "w"), indent=1, ensure_ascii=False); json.dump(ps, open(d + "/pstory.json", "w"), indent=1, ensure_ascii=False)
print(len(cards), "cards,", len(ps), "pstory")
