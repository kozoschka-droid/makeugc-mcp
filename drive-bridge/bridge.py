#!/usr/bin/env python3
"""Клієнт Drive Bridge: передає відео між цим середовищем і папкою Shop Content.

URL і ключ беруться зі змінних середовища (їх читають з Google Doc
"05_brand/Drive Bridge" на початку кожної сесії, у репозиторії не зберігаються):
    DRIVE_BRIDGE_URL, DRIVE_BRIDGE_KEY

Команди:
    bridge.py list [FOLDER_ID]
    bridge.py get FILE_ID OUT_PATH
    bridge.py put LOCAL_PATH FOLDER_ID [MIME]
"""
import base64
import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request

URL = os.environ["DRIVE_BRIDGE_URL"]
KEY = os.environ["DRIVE_BRIDGE_KEY"]


def _call(req):
    with urllib.request.urlopen(req, timeout=300) as r:  # Apps Script робить redirect
        data = json.loads(r.read().decode())
    if "error" in data:
        raise SystemExit(f"bridge error: {data['error']}")
    return data


def list_(folder=None):
    q = {"key": KEY, "action": "list"}
    if folder:
        q["folder"] = folder
    return _call(URL + "?" + urllib.parse.urlencode(q))["files"]


def get(file_id, out):
    d = _call(URL + "?" + urllib.parse.urlencode({"key": KEY, "action": "get", "id": file_id}))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(base64.b64decode(d["data"]))
    return out


def put(path, folder, mime=None):
    mime = mime or mimetypes.guess_type(path)[0] or "application/octet-stream"
    body = json.dumps({"key": KEY, "folder": folder, "name": os.path.basename(path),
                       "mime": mime,
                       "data": base64.b64encode(open(path, "rb").read()).decode()}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    return _call(req)


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    if cmd == "list":
        for f in list_(*args):
            print(f"{f['id']}\t{f['mime']}\t{f.get('size', '')}\t{f['name']}")
    elif cmd == "get":
        print(get(*args))
    elif cmd == "put":
        print(json.dumps(put(*args), ensure_ascii=False))
    else:
        raise SystemExit(__doc__)
