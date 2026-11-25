import json, sys, re
# usage: python3 projects/flame_dec/post_v3.py SHA n [n...]  -> JSON для updateScheduledPost (ті самі слоти/uuid, що v1/v2)
SHA = sys.argv[1]
B = f"https://raw.githubusercontent.com/kozoschka-droid/makeugc-mcp/{SHA}/media/flame/reels_v3/"
LINK = "https://luvinor.store/products/new-flame-aromatherapy-machine-colorful-essential-oil-diffuser-home-large-fog-volume-flame-humidifier-3d-flame-fireplace-machine"
plan = json.load(open("projects/flame_dec/reels_v3_plan.json"))
ids = {int(l.split()[0]): l.split()[1:] for l in open("projects/flame_dec/v1_ids.txt")}
for n in map(int, sys.argv[2:]):
    p = plan[n - 1]; f = f"v{n:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"; dt = f"{p['date']}T{p['hour']:02d}:00:00"
    plain = re.sub(r"[^\w\s,'’?!.:&+$—-]", "", p["hook"]).strip()
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False, "media": [B + f], "mediaAltText": [],
            "providers": [{"network": x} for x in ["facebook", "instagram", "youtube", "tiktok", "pinterest"]],
            "publicationDate": {"dateTime": dt, "timezone": "America/Chicago"}, "shortener": False, "smartLinkData": {"ids": []},
            "text": p["caption"],
            "facebookData": {"type": "REEL", "title": plain}, "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": True},
            "youtubeData": {"title": p["hook"] + " #shorts", "type": "short", "privacy": "public", "madeForKids": False, "isAiGeneratedContent": True},
            "tiktokData": {"title": p["caption"], "privacyOption": "PUBLIC_TO_EVERYONE", "isAigc": True},
            "pinterestData": {"boardId": "905927349984171958", "pinTitle": (plain + " – Flame Fireplace Diffuser")[:95], "pinLink": LINK, "pinNewFormat": True,
                              "isAiGenerated": True, "isAiGeneratedPerson": False}}
    print(n, ids[n][0], ids[n][1], dt); print(json.dumps(info, ensure_ascii=False))
