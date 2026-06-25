#!/usr/bin/env python3
"""
Rename the 12 BMB modular-nurture email templates to a clean, consistent
convention:  `Modular Nurture NN · Topic`

GHL has no rename endpoint (PUT 404s, POST-with-id creates a duplicate), so
for each template we:
  1. fetch the LIVE rendered HTML from its previewUrl (this preserves the
     real booking-link CTAs that were applied via API — the source markdown
     still has [[BOOK_CALL_URL]] placeholders, so we must NOT regenerate
     from markdown),
  2. create a new shell under the clean name (subject + previewText from the
     locked markdown frontmatter),
  3. save the fetched HTML to the new shell,
  4. verify the new template exists with the right name,
  5. only then delete the old template.

Idempotent-ish: skips any template whose name already matches the convention.
"""
import re, sys, time, json
from pathlib import Path
import requests

API_BASE = "https://services.leadconnectorhq.com"
LOCATION_ID = "zPo4vLlEjjXCflgDSXlI"
FOLDER_ID = "6a072d9406376ac2d680fcf2"          # canonical "Nurture - Modular Lead 8 Week"
NURTURE_DIR = Path("/Volumes/T7/SPG/3. FULFILLMENT/Clients/BIVIANO/Marketing/Nurture Sequences/Email - 8 Week Modular Lead")

# stem -> short topic label for the new name
TOPIC = {
    "01-welcome":            "Welcome",
    "02-mike-intro":         "Meet Mike",
    "03-myth-cheap-looking": "The Cheap Myth",
    "04-financing":          "Financing",
    "05-the-numbers":        "The Numbers",
    "06-set-day":            "Set Day",
    "07-your-lot":           "Your Lot",
    "08-timeline":           "Timeline",
    "09-still-thinking":     "Still Thinking",
    "10-social-proof":       "Social Proof",
    "11-design-custom":      "Custom Design",
    "12-final-check-in":     "Final Check-In",
}

def load_key():
    for line in Path("/Volumes/T7/SPG/Claude Code/.env").read_text().splitlines():
        if line.startswith("BMB_GHL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("BMB_GHL_API_KEY not found")

KEY = load_key()
H = {
    "Authorization": f"Bearer {KEY}",
    "Version": "2021-07-28",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "curl/8.7.1",
}

def api(method, path, **kw):
    r = requests.request(method, f"{API_BASE}{path}", headers=H, timeout=30, **kw)
    if r.status_code >= 400:
        print(f"  ERR {method} {path}: {r.status_code} {r.text[:300]}")
        r.raise_for_status()
    return r.json() if r.text else {}

def frontmatter(stem):
    txt = (NURTURE_DIR / f"{stem}.md").read_text()
    m = re.match(r"^---\n(.*?)\n---", txt, re.DOTALL)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta

def list_folder():
    res = api("GET", f"/emails/builder?locationId={LOCATION_ID}&limit=200&parentId={FOLDER_ID}")
    return res.get("builders", [])

def stem_from_name(name):
    m = re.match(r"^(\d{2}-[a-z-]+?)\s+—", name)
    return m.group(1) if m else None

def main():
    items = list_folder()
    print(f"Found {len(items)} templates in folder\n")
    by_stem = {}
    for t in items:
        st = stem_from_name(t.get("name", ""))
        if st:
            by_stem[st] = t

    for stem in sorted(TOPIC):
        num = stem[:2]
        new_name = f"Modular Nurture {num} · {TOPIC[stem]}"
        old = by_stem.get(stem)
        if not old:
            print(f"[{num}] SKIP — no live template matched stem {stem}")
            continue
        if old.get("name") == new_name:
            print(f"[{num}] already named correctly")
            continue

        # 1. fetch live HTML
        html = requests.get(old["previewUrl"], timeout=30).text
        if len(html) < 200:
            print(f"[{num}] ABORT — fetched HTML too short ({len(html)} chars), skipping")
            continue
        meta = frontmatter(stem)
        subject = meta.get("subject", TOPIC[stem])
        preview = meta.get("preview", "")

        # 2. create new shell
        shell = api("POST", "/emails/builder", json={
            "locationId": LOCATION_ID, "title": new_name,
            "type": "html", "templateType": "html", "editorType": "html",
            "subject": subject, "previewText": preview, "parentId": FOLDER_ID,
        })
        new_id = shell.get("id") or shell.get("redirect")
        if not new_id:
            print(f"[{num}] ABORT — no new id from shell: {json.dumps(shell)[:200]}")
            continue

        # 3. save body
        api("POST", "/emails/builder/data", json={
            "locationId": LOCATION_ID, "templateId": new_id,
            "editorType": "html", "html": html, "updatedBy": "api",
        })
        time.sleep(0.5)

        # 4. verify new one exists with right name
        ok = any(b.get("id") == new_id and b.get("name") == new_name for b in list_folder())
        if not ok:
            print(f"[{num}] ABORT — new template {new_id} not verified; OLD LEFT INTACT")
            continue

        # 5. delete old
        api("DELETE", f"/emails/builder/{LOCATION_ID}/{old['id']}")
        print(f"[{num}] '{old['name']}'\n       -> '{new_name}'  (new id {new_id}, old deleted)")
        time.sleep(0.4)

    print("\n--- FINAL STATE ---")
    for t in sorted(list_folder(), key=lambda x: x.get("name", "")):
        print(" ", t.get("name"))

if __name__ == "__main__":
    main()
