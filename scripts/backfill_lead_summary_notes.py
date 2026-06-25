#!/usr/bin/env python3
"""
Backfill "🔥 NEW LEAD SUMMARY" notes onto BMB contacts from the last 30 days.

Run:
  python3 backfill_lead_summary_notes.py            # dry-run
  python3 backfill_lead_summary_notes.py --apply    # actually write notes
"""
import os, sys, json, time
from pathlib import Path
from datetime import datetime, timedelta, timezone
import requests

LOC = "zPo4vLlEjjXCflgDSXlI"
BASE = "https://services.leadconnectorhq.com"
NOTE_TAG = "🔥 NEW LEAD SUMMARY"

def load_key():
    for line in Path("/Volumes/T7/SPG/Claude Code/.env").read_text().splitlines():
        if line.startswith("BMB_GHL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("BMB_GHL_API_KEY not in .env")

API_KEY = load_key()
H = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "curl/8.7.1",
}

# Field-key -> display config (label + optional formatter)
# Multiple keys can map to the same row; first non-empty wins.
SUMMARY_ROWS = [
    ("Project Type", ["contact.project_type", "contact.home_type"]),
    ("Town", ["contact.what_town_do_you_live_in"]),
    ("Timeline", [
        "contact.when_are_you_looking_to_move_into_your_new_home",
        "contact.project_timeframe",
    ]),
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

def fetch_field_map():
    r = requests.get(f"{BASE}/locations/{LOC}/customFields", headers=H, timeout=30)
    r.raise_for_status()
    return {f["id"]: f.get("fieldKey", "") for f in r.json().get("customFields", [])}

def fetch_recent_contacts(days=30):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
    contacts = []
    page_after = None
    for _ in range(15):
        body = {"locationId": LOC, "pageLimit": 100, "sort": [{"field": "dateAdded", "direction": "desc"}]}
        if page_after:
            body["searchAfter"] = page_after
        r = requests.post(f"{BASE}/contacts/search", headers=H, json=body, timeout=30)
        j = r.json()
        batch = j.get("contacts", [])
        if not batch:
            break
        contacts.extend(batch)
        last = batch[-1]
        page_after = last.get("searchAfter")
        if not page_after:
            break
        if last.get("dateAdded", "") < cutoff:
            break
    return [c for c in contacts if c.get("dateAdded", "") >= cutoff]

def build_summary(contact, field_id_to_key):
    """Render a Note body. Skip empty rows. Return None if nothing useful to show."""
    # contact's custom field values, keyed by field_key
    cf_values = {}
    for cf in contact.get("customFields", []):
        fid = cf.get("id")
        val = cf.get("value")
        key = field_id_to_key.get(fid)
        if key and val not in (None, "", [], {}):
            # arrays -> first value
            if isinstance(val, list):
                val = val[0] if val else None
            if val:
                cf_values[key] = str(val).strip()

    lines = [NOTE_TAG, ""]
    found_any = False
    for label, keys in SUMMARY_ROWS:
        for k in keys:
            if k in cf_values:
                v = cf_values[k]
                lines.append(f"{label}: {v}")
                found_any = True
                break

    # add lead source / type from standard fields
    src = contact.get("source")
    if src:
        lines.append(f"")
        lines.append(f"GHL Source: {src}")
    addr_bits = [contact.get("address"), contact.get("city"), contact.get("state"), contact.get("postalCode")]
    addr = ", ".join([b for b in addr_bits if b])
    if addr:
        lines.append(f"Address: {addr}")

    if not found_any and not src and not addr:
        return None
    return "\n".join(lines)

def existing_summary_note(contact_id):
    r = requests.get(f"{BASE}/contacts/{contact_id}/notes", headers=H, timeout=30)
    if r.status_code >= 300:
        return False
    notes = r.json().get("notes", [])
    return any(NOTE_TAG in (n.get("body", "") or "") for n in notes)

def post_note(contact_id, body):
    r = requests.post(
        f"{BASE}/contacts/{contact_id}/notes",
        headers=H,
        json={"body": body, "userId": ""},
        timeout=30,
    )
    return r.status_code, (r.json() if r.text else {})

def main():
    apply = "--apply" in sys.argv
    print(f"Mode: {'APPLY' if apply else 'DRY RUN'}")

    print("Fetching field map...")
    field_id_to_key = fetch_field_map()

    print("Fetching last 30 days of contacts...")
    contacts = fetch_recent_contacts(30)
    print(f"  -> {len(contacts)} contacts")

    skipped_existing = skipped_empty = wrote = failed = 0
    for i, c in enumerate(contacts, 1):
        cid = c["id"]
        name = (c.get("firstName") or "") + " " + (c.get("lastName") or "")
        name = name.strip() or c.get("email", "(no name)")

        summary = build_summary(c, field_id_to_key)
        if not summary:
            skipped_empty += 1
            continue

        if existing_summary_note(cid):
            skipped_existing += 1
            continue

        if apply:
            status, resp = post_note(cid, summary)
            if status >= 300:
                failed += 1
                print(f"  [{i:3d}] FAIL {name}: {status} {str(resp)[:100]}")
            else:
                wrote += 1
                print(f"  [{i:3d}] ✓ {name}")
            time.sleep(0.15)
        else:
            wrote += 1
            print(f"  [{i:3d}] WOULD WRITE: {name}")
            print("       " + summary.replace("\n", "\n       ")[:400])
            print()

    print(f"\n--- {'WOULD WRITE' if not apply else 'WROTE'}: {wrote}")
    print(f"--- Skipped (already has summary note): {skipped_existing}")
    print(f"--- Skipped (no useful data): {skipped_empty}")
    if failed:
        print(f"--- FAILED: {failed}")

if __name__ == "__main__":
    main()
