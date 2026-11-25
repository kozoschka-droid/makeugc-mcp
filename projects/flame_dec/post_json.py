import json, sys, re
B = "https://raw.githubusercontent.com/kozoschka-droid/makeugc-mcp/claude/funny-brahmagupta-8q735p/media/flame/reels_dec/"
plan = json.load(open("projects/flame_dec/reels_plan.json"))
a, b = int(sys.argv[1]), int(sys.argv[2])
for p in plan:
    if not a <= p["n"] <= b: continue
    f = f"r{p['n']:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"; dt = f"{p['date']}T{p['hour']:02d}:00:00"
    plain = re.sub(r"[^\w\s,'’?!.:-]", "", p["hook"]).strip()
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False, "media": [B + f], "mediaAltText": [],
            "providers": [{"network": n} for n in ["facebook","instagram","youtube","tiktok","pinterest"]],
            "publicationDate": {"dateTime": dt, "timezone": "America/Chicago"}, "shortener": False, "smartLinkData": {"ids": []},
            "text": f"{p['hook']}\n{p['body']}\n\nLink in bio 🔥\n\n{p['tags']}",
            "facebookData": {"type": "REEL", "title": plain}, "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": True},
            "youtubeData": {"title": p["hook"] + " #shorts", "type": "short", "privacy": "public", "madeForKids": False, "isAiGeneratedContent": True},
            "tiktokData": {"title": p["hook"], "privacyOption": "PUBLIC_TO_EVERYONE", "isAigc": True},
            "pinterestData": {"boardId": "905927349984171958", "pinTitle": plain[:95], "pinLink": "https://luvinor.store/products/new-flame-aromatherapy-machine-colorful-essential-oil-diffuser-home-large-fog-volume-flame-humidifier-3d-flame-fireplace-machine", "pinNewFormat": True, "isAiGenerated": True, "isAiGeneratedPerson": False}}
    print(dt + "-06:00"); print(json.dumps(info, ensure_ascii=False))
