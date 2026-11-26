import json, sys, re
# usage: pin_seo.py file.json  -> печатає (id, uuid, info) для updateScheduledPost з SEO-назвою піна
def title(text):
    t = " " + re.sub(r"[^a-z ]", " ", text.lower()) + " "
    if any(" " + w in t for w in ("gift", "black friday", "deal", "cyber monday")): return "Christmas Gift Idea: Handheld Steam Cleaner for Home"
    if any(" " + w in t for w in ("car ", "cars ", "seat", "carcleaning", "cardetailing")): return "Handheld Steam Cleaner for Car Interior and Seats"
    if any(" " + w in t for w in ("bathroom", "grout", "tile", "shower")): return "Steam Cleaner for Bathroom Grout and Tile, No Scrubbing"
    if any(" " + w in t for w in ("kitchen", "grease", "stove", "oven", "cooking", "thanksgiving", "holiday", "guests")): return "Handheld Steam Cleaner for Kitchen Grease and Stovetop"
    if any(" " + w in t for w in ("chemical", "water", "eco", "kids", "pets")): return "Chemical-Free Cleaning: Steam Cleaner With Just Water"
    if any(" " + w in t for w in ("before", "after", "grime", "stain")): return "Steam Cleaning Before and After: Grime and Stains Gone"
    return "Handheld Steam Cleaner: Deep Clean Kitchen, Bathroom and Car"
DESC = "\n\nHandheld steam cleaner for kitchen grease, bathroom grout, sofa and car seats. Kills germs with just water, no chemicals. Free shipping USA."
raw = open(sys.argv[1]).read()
d = json.loads(raw); d = d["data"] if isinstance(d, dict) else json.loads(d[0]["text"])["data"]
for p in d:
    if not any(x["network"] == "pinterest" for x in p["providers"]): continue
    info = {k: v for k, v in p.items() if k not in ("id", "uuid", "creationDate", "creatorUserMail", "creatorUserId", "brandTags", "plannerUrl")}
    info["providers"] = [{"network": x["network"]} for x in p["providers"]]
    if len(info["providers"]) == 1: info.pop("instagramData", None); info.pop("twitterData", None)
    info["pinterestData"]["pinTitle"] = title(p["text"])
    if len(info["providers"]) == 1 and "Free shipping USA" not in info["text"]: info["text"] = info["text"] + DESC
    print(json.dumps({"id": str(p["id"]), "uuid": p["uuid"], "info": json.dumps(info, ensure_ascii=False)}, ensure_ascii=False))
