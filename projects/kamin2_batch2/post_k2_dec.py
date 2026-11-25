import json, sys, re
# usage: python3 projects/kamin2_batch2/post_k2_dec.py SHA n [n...] -> date + JSON для createScheduledPost (бренд 8247119: FB, IG, Threads)
SHA = sys.argv[1]
B = f"https://raw.githubusercontent.com/kozoschka-droid/makeugc-mcp/{SHA}/media/kamin2/dec/"
plan = json.load(open("projects/kamin2_batch2/reels_k2_dec_plan.json"))
for n in map(int, sys.argv[2:]):
    p = plan[n - 1]; f = f"k{n:02d}_{p['date'][5:]}_{p['hour']:02d}.mp4"; dt = f"{p['date']}T{p['hour']:02d}:00:00"
    plain = re.sub(r"[^\w\s,'’?!.:&+$—-]", "", p["hook"]).strip()
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False, "media": [B + f], "mediaAltText": [],
            "providers": [{"network": "facebook"}, {"network": "instagram"}, {"network": "threads"}],
            "publicationDate": {"dateTime": dt, "timezone": "America/Chicago"}, "shortener": False, "smartLinkData": {"ids": []},
            "text": p["caption"], "facebookData": {"type": "REEL", "title": plain},
            "instagramData": {"type": "REEL", "showReelOnFeed": True, "isAiGenerated": False}, "threadsData": {}}
    print(n, dt + "-06:00"); print(json.dumps(info, ensure_ascii=False))
