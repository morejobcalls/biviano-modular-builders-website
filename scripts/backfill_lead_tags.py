#!/usr/bin/env python3
"""
Backfill triage tags on BMB contacts from the last 30 days.

Tags get added as chips visible at the top of the LeadConnector mobile contact card
without requiring any tap/expand. Lets Mike triage at a glance.

Namespacing (kept clean so they sort/group well):
  lead:<modular|decking|other>
  town:<duxbury|marshfield|...>
  timeline:<asap|6mo|12mo|planning|exploring>
  situation:<owns-land|searching|other>
  contact:<text|call|email>

Run:
  python3 backfill_lead_tags.py            # dry-run
  python3 backfill_lead_tags.py --apply
"""
import os, sys, json, time, re
from pathlib import Path
from datetime import datetime, timedelta, timezone
import requests

LOC = "zPo4vLlEjjXCflgDSXlI"
BASE = "https://services.leadconnectorhq.com"

def load_key():
    for line in Path("/Volumes/T7/SPG/Claude Code/.env").read_text().splitlines():
        if line.startswith("BMB_GHL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("BMB_GHL_API_KEY not in .env")

API_KEY = load_key()
H = {"Authorization": f"Bearer {API_KEY}", "Version": "2021-07-28",
     "Accept": "application/json", "Content-Type": "application/json", "User-Agent": "curl/8.7.1"}

# field_key -> {value_substring (lowercase): output tag}
TAG_RULES = {
    # Project type — derived from source AND home_type
    # Source is best signal; home_type adds sub-category
    "_source_to_lead_tag": {
        "modular": "lead:modular",
        "decking": "lead:decking",
        "deck":    "lead:decking",
    },
    # Town — direct value, slugify
    "contact.what_town_do_you_live_in": "_slugify_town",
    # Timeline buckets — modular uses one field, decking uses another; same buckets
    "contact.when_are_you_looking_to_move_into_your_new_home": {
        "asap":          "timeline:asap",
        "3-6":           "timeline:asap",
        "soon":          "timeline:6mo",
        "6-12":          "timeline:6mo",
        "planning":      "timeline:planning",
        "12+":           "timeline:planning",
        "exploring":     "timeline:exploring",
    },
    "contact.project_timeframe": {
        "asap":          "timeline:asap",
        "3-6":           "timeline:asap",
        "soon":          "timeline:6mo",
        "6-12":          "timeline:6mo",
        "planning":      "timeline:planning",
        "12+":           "timeline:planning",
        "exploring":     "timeline:exploring",
    },
    "contact.what_best_describes_your_situation": {
        "own land":      "situation:owns-land",
        "searching":     "situation:searching",
        "lot":           "situation:owns-land",
    },
    "contact.preferred_contact_method": {
        "text":          "contact:text",
        "call":          "contact:call",
        "phone":         "contact:call",
        "email":         "contact:email",
    },
}

def slugify(s):
    s = re.sub(r"[^\w\s-]", "", s or "").strip().lower()
    s = re.sub(r"\s+", "-", s)
    return s

def fetch_field_map():
    r = requests.get(f"{BASE}/locations/{LOC}/customFields", headers=H, timeout=30)
    r.raise_for_status()
    return {f["id"]: f.get("fieldKey", "") for f in r.json().get("customFields", [])}

def fetch_recent_contacts(days=30):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    contacts, after = [], None
    for _ in range(15):
        body = {"locationId": LOC, "pageLimit": 100, "sort": [{"field": "dateAdded", "direction": "desc"}]}
        if after: body["searchAfter"] = after
        r = requests.post(f"{BASE}/contacts/search", headers=H, json=body, timeout=30)
        j = r.json()
        batch = j.get("contacts", [])
        if not batch: break
        contacts.extend(batch)
        after = batch[-1].get("searchAfter")
        if not after: break
        if batch[-1].get("dateAdded", "") < cutoff: break
    return [c for c in contacts if c.get("dateAdded", "") >= cutoff]

def derive_tags(contact, field_id_to_key):
    tags = set()

    # 1. Lead type from GHL source field
    src = (contact.get("source") or "").lower()
    for needle, tag in TAG_RULES["_source_to_lead_tag"].items():
        if needle in src:
            tags.add(tag)
            break

    # 2. Custom-field-driven tags
    cf_values = {}
    for cf in contact.get("customFields", []):
        key = field_id_to_key.get(cf.get("id"))
        val = cf.get("value")
        if key and val not in (None, "", [], {}):
            if isinstance(val, list):
                val = val[0] if val else None
            if val:
                cf_values[key] = str(val).lower()

    # Town — direct slugify
    town_val = cf_values.get("contact.what_town_do_you_live_in")
    if town_val:
        # Extract just the town name (drop emoji + extra chars)
        t = re.sub(r"[^\w\s-]", "", town_val).strip()
        # Skip "other" / blanks / multi-word junk
        if t and "other" not in t.lower() and len(t) < 30:
            tags.add(f"town:{slugify(t.split()[0])}")  # first word only

    # Rule-based tags for timeline, situation, contact pref
    for fkey, rules in TAG_RULES.items():
        if fkey.startswith("_"):
            continue
        if rules == "_slugify_town":
            continue
        val = cf_values.get(fkey)
        if not val:
            continue
        for needle, tag in rules.items():
            if needle in val:
                tags.add(tag)
                break

    return sorted(tags)

def add_tags(contact_id, new_tags):
    r = requests.post(f"{BASE}/contacts/{contact_id}/tags", headers=H,
                      json={"tags": new_tags}, timeout=30)
    return r.status_code, (r.json() if r.text else {})

def main():
    apply = "--apply" in sys.argv
    print(f"Mode: {'APPLY' if apply else 'DRY RUN'}\n")

    field_id_to_key = fetch_field_map()
    contacts = fetch_recent_contacts(30)
    print(f"Last 30d contacts: {len(contacts)}\n")

    counts = {"tagged": 0, "skipped_no_data": 0, "skipped_already": 0, "failed": 0}
    tag_freq = {}

    for c in contacts:
        cid = c["id"]
        name = ((c.get("firstName") or "") + " " + (c.get("lastName") or "")).strip() or c.get("email","?")
        derived = derive_tags(c, field_id_to_key)
        if not derived:
            counts["skipped_no_data"] += 1
            continue

        existing = set(c.get("tags") or [])
        to_add = [t for t in derived if t not in existing]
        if not to_add:
            counts["skipped_already"] += 1
            continue

        for t in to_add:
            tag_freq[t] = tag_freq.get(t, 0) + 1

        if apply:
            status, _ = add_tags(cid, to_add)
            if status >= 300:
                counts["failed"] += 1
                print(f"  FAIL {name}: {status}")
            else:
                counts["tagged"] += 1
                print(f"  ✓ {name}: {to_add}")
            time.sleep(0.15)
        else:
            counts["tagged"] += 1
            print(f"  WOULD TAG {name}: {to_add}")

    print(f"\n--- {'Tagged' if apply else 'Would tag'}: {counts['tagged']}")
    print(f"--- Skipped (no data):        {counts['skipped_no_data']}")
    print(f"--- Skipped (all tags exist): {counts['skipped_already']}")
    if counts["failed"]:
        print(f"--- FAILED:                  {counts['failed']}")

    print("\n=== TAG FREQUENCY ===")
    for t, n in sorted(tag_freq.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {t}")

if __name__ == "__main__":
    main()
