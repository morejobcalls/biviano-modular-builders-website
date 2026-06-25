#!/usr/bin/env python3
"""
BMB hourly sync — runs on a schedule (launchd / cron / Apify) to enrich
new contacts with summary notes + triage tags.

Designed to be IDEMPOTENT and FAST:
- Pulls contacts created in last 90 minutes (with 30 min overlap buffer)
- Skips contacts that already have the "🔥 NEW LEAD SUMMARY" note
- Skips tags that already exist on the contact

Run manually:
  python3 bmb_hourly_sync.py            # dry-run
  python3 bmb_hourly_sync.py --apply    # actually write

Logs to /tmp/bmb_hourly_sync.log on every run.
"""
import os, sys, json, time, re, logging
from pathlib import Path
from datetime import datetime, timedelta, timezone
import requests

LOC = "zPo4vLlEjjXCflgDSXlI"
BASE = "https://services.leadconnectorhq.com"
NOTE_TAG = "🔥 NEW LEAD SUMMARY"
LOG_PATH = "/tmp/bmb_hourly_sync.log"

# Logging — append, with timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)
log = logging.getLogger(__name__)

def load_key():
    for line in Path("/Volumes/T7/SPG/Claude Code/.env").read_text().splitlines():
        if line.startswith("BMB_GHL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("BMB_GHL_API_KEY not in .env")

API_KEY = load_key()
H = {"Authorization": f"Bearer {API_KEY}", "Version": "2021-07-28",
     "Accept": "application/json", "Content-Type": "application/json", "User-Agent": "curl/8.7.1"}

# ---------- Note summary config ----------
SUMMARY_ROWS = [
    ("Project Type", ["contact.project_type", "contact.home_type"]),
    ("Town", ["contact.what_town_do_you_live_in"]),
    ("Timeline", ["contact.when_are_you_looking_to_move_into_your_new_home", "contact.project_timeframe"]),
    ("Situation", ["contact.what_best_describes_your_situation"]),
    ("What to build", ["contact.what_are_you_looking_to_build"]),
    ("Bedrooms", ["contact.number_of_bedrooms"]),
    ("Bathrooms", ["contact.number_of_bathrooms"]),
    ("Sqft", ["contact.estimated_square_footage", "contact.square_footage_youre_considering"]),
    ("Home cost (calc)", ["contact.home_cost_number", "contact.home_total_number"]),
    ("Contact preference", ["contact.preferred_contact_method"]),
    ("Source", ["contact.utm_source"]),
    ("Campaign", ["contact.utm_campaign"]),
    ("Creative", ["contact.utm_content"]),
]

# ---------- Tag derivation config ----------
SOURCE_TO_LEAD_TAG = {"modular": "lead:modular", "decking": "lead:decking", "deck": "lead:decking"}
# Source-classification tags
URL_TO_SOURCE_TAG = {
    "custom-design": "source:direct-booking",  # Direct calendar booking, no qualification
    "dream-home":    "source:modular-survey",
    "dream-decks":   "source:decking-survey",
    "deck-offer":    "source:decking-offer",
    "modular-homes": "source:modular-page",
}
TIMELINE_BUCKETS = {
    "asap": "timeline:asap", "3-6": "timeline:asap",
    "soon": "timeline:6mo", "6-12": "timeline:6mo",
    "planning": "timeline:planning", "12+": "timeline:planning",
    "exploring": "timeline:exploring",
}
SITUATION_TAGS = {"own land": "situation:owns-land", "searching": "situation:searching", "lot": "situation:owns-land"}
CONTACT_TAGS = {"text": "contact:text", "call": "contact:call", "phone": "contact:call", "email": "contact:email"}

def slugify(s):
    return re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", s or "").strip().lower())

# ---------- Helpers ----------
def fetch_field_map():
    r = requests.get(f"{BASE}/locations/{LOC}/customFields", headers=H, timeout=30)
    r.raise_for_status()
    return {f["id"]: f.get("fieldKey", "") for f in r.json().get("customFields", [])}

def fetch_recent_contacts(minutes=90):
    cutoff = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()
    contacts, after = [], None
    for _ in range(5):
        body = {"locationId": LOC, "pageLimit": 100, "sort": [{"field": "dateAdded", "direction": "desc"}]}
        if after: body["searchAfter"] = after
        r = requests.post(f"{BASE}/contacts/search", headers=H, json=body, timeout=30)
        batch = r.json().get("contacts", [])
        if not batch: break
        contacts.extend(batch)
        after = batch[-1].get("searchAfter")
        if not after: break
        if batch[-1].get("dateAdded", "") < cutoff: break
    return [c for c in contacts if c.get("dateAdded", "") >= cutoff]

def cf_values_for(contact, field_id_to_key):
    out = {}
    for cf in contact.get("customFields", []):
        key = field_id_to_key.get(cf.get("id"))
        val = cf.get("value")
        if key and val not in (None, "", [], {}):
            if isinstance(val, list):
                val = val[0] if val else None
            if val:
                out[key] = str(val).strip()
    return out

def build_note(contact, cf):
    lines = [NOTE_TAG, ""]
    has_data = False
    for label, keys in SUMMARY_ROWS:
        for k in keys:
            if k in cf:
                lines.append(f"{label}: {cf[k]}")
                has_data = True
                break
    src = contact.get("source")
    if src:
        lines.extend(["", f"GHL Source: {src}"])
        has_data = True
    addr = ", ".join(b for b in [contact.get("address"), contact.get("city"), contact.get("state"), contact.get("postalCode")] if b)
    if addr:
        lines.append(f"Address: {addr}")
        has_data = True
    return "\n".join(lines) if has_data else None

def derive_tags(contact, cf):
    tags = set()
    src = (contact.get("source") or "").lower()
    for needle, tag in SOURCE_TO_LEAD_TAG.items():
        if needle in src:
            tags.add(tag); break

    # Source-classification from landing URL
    url = (contact.get("lastAttributionSource",{}).get("url","")
           or contact.get("attributionSource",{}).get("url","") or "").lower()
    medium = (contact.get("attributionSource",{}).get("medium") or "").lower()
    has_utm = bool(contact.get("attributionSource",{}).get("utmSource"))

    if not src and medium == "manual":
        tags.add("source:manual-entry")
    else:
        for needle, tag in URL_TO_SOURCE_TAG.items():
            if needle in url:
                # For custom-design with no UTM, mark as direct-booking
                if needle == "custom-design" and has_utm:
                    continue  # paid traffic landing on custom-design tracked via UTMs
                tags.add(tag)
                break

    town = cf.get("contact.what_town_do_you_live_in", "").lower()
    if town:
        t = re.sub(r"[^\w\s-]", "", town).strip()
        if t and "other" not in t and len(t) < 30:
            tags.add(f"town:{slugify(t.split()[0])}")

    for field, rules in [
        ("contact.when_are_you_looking_to_move_into_your_new_home", TIMELINE_BUCKETS),
        ("contact.project_timeframe", TIMELINE_BUCKETS),
        ("contact.what_best_describes_your_situation", SITUATION_TAGS),
        ("contact.preferred_contact_method", CONTACT_TAGS),
    ]:
        v = cf.get(field, "").lower()
        if not v: continue
        for needle, tag in rules.items():
            if needle in v:
                tags.add(tag); break
    return sorted(tags)

def contact_has_summary_note(contact_id):
    r = requests.get(f"{BASE}/contacts/{contact_id}/notes", headers=H, timeout=30)
    if r.status_code >= 300:
        return False
    return any(NOTE_TAG in (n.get("body", "") or "") for n in r.json().get("notes", []))

def post_note(contact_id, body):
    r = requests.post(f"{BASE}/contacts/{contact_id}/notes", headers=H,
                      json={"body": body, "userId": ""}, timeout=30)
    return r.status_code < 300

def add_tags(contact_id, tags):
    r = requests.post(f"{BASE}/contacts/{contact_id}/tags", headers=H,
                      json={"tags": tags}, timeout=30)
    return r.status_code < 300

# ---------- Main ----------
def main():
    apply = "--apply" in sys.argv
    log.info(f"=== BMB hourly sync starting — mode={'APPLY' if apply else 'DRY RUN'} ===")

    field_id_to_key = fetch_field_map()
    contacts = fetch_recent_contacts(90)
    log.info(f"Pulled {len(contacts)} contacts created in last 90 min")

    stats = {"notes_added": 0, "tags_added": 0, "notes_existed": 0, "no_data": 0, "errors": 0}

    for c in contacts:
        cid = c["id"]
        name = ((c.get("firstName") or "") + " " + (c.get("lastName") or "")).strip() or c.get("email", "?")
        cf = cf_values_for(c, field_id_to_key)

        # 1. Note
        if contact_has_summary_note(cid):
            stats["notes_existed"] += 1
        else:
            note = build_note(c, cf)
            if note:
                if apply:
                    if post_note(cid, note):
                        stats["notes_added"] += 1
                        log.info(f"  + note: {name}")
                    else:
                        stats["errors"] += 1
                        log.warning(f"  ! note FAIL: {name}")
                else:
                    stats["notes_added"] += 1
                    log.info(f"  WOULD ADD note: {name}")
            else:
                stats["no_data"] += 1

        # 2. Tags
        derived = derive_tags(c, cf)
        existing = set(c.get("tags") or [])
        to_add = [t for t in derived if t not in existing]
        if to_add:
            if apply:
                if add_tags(cid, to_add):
                    stats["tags_added"] += len(to_add)
                    log.info(f"  + tags: {name} {to_add}")
                else:
                    stats["errors"] += 1
                    log.warning(f"  ! tag FAIL: {name}")
            else:
                stats["tags_added"] += len(to_add)
                log.info(f"  WOULD ADD tags: {name} {to_add}")

        time.sleep(0.1)

    log.info(f"=== Done. {json.dumps(stats)} ===")

if __name__ == "__main__":
    main()
