import json, sys
# usage: post_story.py SHA path... -> date + JSON для createScheduledPost (STORY, FB+IG, бренд 8247119)
# ім'я файлу має містити MM-DD/день і слот HHMM; дату передаємо як path=YYYY-MM-DDTHH:MM
SHA = sys.argv[1]
for a in sys.argv[2:]:
    path, dt = a.split("=")
    ai = path.endswith(".jpg")
    info = {"autoPublish": True, "draft": False, "descendants": [], "firstCommentText": "", "hasNotReadNotes": False,
            "media": [f"https://raw.githubusercontent.com/kozoschka-droid/makeugc-mcp/{SHA}/{path}"], "mediaAltText": [],
            "providers": [{"network": "facebook"}, {"network": "instagram"}], "publicationDate": {"dateTime": dt + ":00", "timezone": "America/Chicago"},
            "shortener": False, "smartLinkData": {"ids": []}, "text": "", "facebookData": {"type": "STORY"},
            "instagramData": {"type": "STORY", "isAiGenerated": ai}}
    print(dt + ":00-06:00"); print(json.dumps(info, ensure_ascii=False))
