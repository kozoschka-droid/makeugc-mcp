import json, sys, re
SHA = "3281a4ccaea899c90d0e845a5a4afa738424fdc2"
B = f"https://raw.githubusercontent.com/kozoschka-droid/makeugc-mcp/{SHA}/media/flame/reels_v2/"
LINK = "https://luvinor.store/products/new-flame-aromatherapy-machine-colorful-essential-oil-diffuser-home-large-fog-volume-flame-humidifier-3d-flame-fireplace-machine"
plan = json.load(open("projects/flame_dec/reels_v2_plan.json"))
for n in map(int, sys.argv[1:]):
    p = plan[n - 1]; f = f"v{n:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"; dt = f"{p['date']}T{p['hour']:02d}:00:00"
    plain = re.sub(r"[^\w\s,'’?!.:&+—-]", "", p["hook"]).strip()
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False, "media": [B + f], "mediaAltText": [],
            "providers": [{"network": x} for x in ["facebook","instagram","youtube","tiktok","pinterest"]],
            "publicationDate": {"dateTime": dt, "timezone": "America/Chicago"}, "shortener": False, "smartLinkData": {"ids": []},
            "text": f"{p['hook']}\n{p['body']}\n\nLink in bio 🔥\n\n{p['tags']}",
            "facebookData": {"type": "REEL", "title": plain}, "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": True},
            "youtubeData": {"title": p["hook"] + " #shorts", "type": "short", "privacy": "public", "madeForKids": False, "isAiGeneratedContent": True},
            "tiktokData": {"title": p["hook"], "privacyOption": "PUBLIC_TO_EVERYONE", "isAigc": True},
            "pinterestData": {"boardId": "905927349984171958", "pinTitle": plain[:95], "pinLink": LINK, "pinNewFormat": True, "isAiGenerated": True, "isAiGeneratedPerson": False}}
    print(n, dt); print(json.dumps(info, ensure_ascii=False))
