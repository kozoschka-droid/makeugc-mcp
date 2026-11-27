"""Друкує info для updateScheduledPost рілса n (медіа з коміту SHA). python3 upd_json.py SHA n1 n2 ..."""
import json, sys, re
sha = sys.argv[1]; B = f"https://raw.githubusercontent.com/kozoschka-droid/makeugc-mcp/{sha}/media/steam/reels_dec/"
plan = {p["n"]: p for p in json.load(open("projects/steam_dec/reels_plan.json"))}
for a in sys.argv[2:]:
    n, _, pt = a.partition(":"); n = int(n); p = plan[n]; f = f"r{n:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"; dt = f"{p['date']}T{p['hour']:02d}:00:00"
    plain = re.sub(r"[^\w\s,'’?!.:-]", "", p["hook"]).strip()
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False, "media": [B + f], "mediaAltText": [],
            "providers": [{"network": x} for x in ["facebook","instagram","youtube","threads","tiktok","pinterest"]],
            "publicationDate": {"dateTime": dt, "timezone": "America/Chicago"}, "shortener": False, "smartLinkData": {"ids": []},
            "text": f"{p['hook']}\n{p['body']}\n\nComment \"STEAM\" for the link 👇\n\n{p['tags']}",
            "facebookData": {"type": "REEL", "title": plain}, "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": True},
            "youtubeData": {"title": p["hook"] + " #shorts", "type": "short", "privacy": "public", "madeForKids": False, "isAiGeneratedContent": True},
            "threadsData": {}, "tiktokData": {"title": p["hook"], "privacyOption": "PUBLIC_TO_EVERYONE", "isAigc": True},
            "pinterestData": {"boardId": "272890127360447057", "pinTitle": pt or plain[:95], "pinLink": "https://luvinor.store/products/handheld-steam-cleaner", "pinNewFormat": True, "isAiGenerated": True, "isAiGeneratedPerson": False}}
    print(n, dt); print(json.dumps(info, ensure_ascii=False))
