import json, sys, re
B = "https://raw.githubusercontent.com/kozoschka-droid/makeugc-mcp/claude/funny-brahmagupta-8q735p/media/steam/reels_dec/"
plan = json.load(open("projects/steam_dec/reels_plan.json"))
a, b = int(sys.argv[1]), int(sys.argv[2])
for p in plan:
    if not a <= p["n"] <= b: continue
    f = f"r{p['n']:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"; dt = f"{p['date']}T{p['hour']:02d}:00:00"
    plain = re.sub(r"[^\w\s,'’?!.:-]", "", p["hook"]).strip()
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False, "media": [B + f], "mediaAltText": [],
            "providers": [{"network": n} for n in ["facebook","instagram","youtube","threads","tiktok","pinterest"]],
            "publicationDate": {"dateTime": dt, "timezone": "America/Chicago"}, "shortener": False, "smartLinkData": {"ids": []},
            "text": f"{p['hook']}\n{p['body']}\n\nComment \"STEAM\" for the link 👇\n\n{p['tags']}",
            "facebookData": {"type": "REEL", "title": plain}, "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": True},
            "youtubeData": {"title": p["hook"] + " #shorts", "type": "short", "privacy": "public", "madeForKids": False, "isAiGeneratedContent": True},
            "threadsData": {}, "tiktokData": {"title": p["hook"], "privacyOption": "PUBLIC_TO_EVERYONE", "isAigc": True},
            "pinterestData": {"boardId": "272890127360447057", "pinTitle": plain[:95], "pinLink": "https://luvinor.store/products/handheld-steam-cleaner", "pinNewFormat": True, "isAiGenerated": True, "isAiGeneratedPerson": False}}
    print(dt + "-06:00"); print(json.dumps(info, ensure_ascii=False))
