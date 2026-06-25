#!/usr/bin/env python3
"""
Reorganize BMB GHL custom fields into a 6-folder structure (5 active + Deprecated).

Based on 30-day fill-rate audit 2026-05-19. Active fields go to their semantic folder;
dormant fields (0 writes in 30d) get parked in Deprecated. No deletions — fully rollbackable.

Prereq: Spencer has created these 6 folders in GHL UI:
  📞 Contact Info
  🔥 Project Snapshot
  🏠 Modular Details
  🪵 Decking Details
  📊 Attribution
  🗑️ Deprecated

Script:
  1. Reads all custom fields + extracts folder list (we infer folders by their `parentId` use)
  2. Asks Spencer to paste the 5 new folder IDs (since folder list isn't exposed cleanly)
  3. Moves each field via PUT /locations/{LOC}/customFields/{fieldId} with new parentId
  4. Logs old + new parent so we can roll back if needed
"""
import os, sys, json, time
from pathlib import Path
import requests

LOCATION_ID = "zPo4vLlEjjXCflgDSXlI"
BASE = "https://services.leadconnectorhq.com"

def load_key():
    for line in Path("/Volumes/T7/SPG/Claude Code/.env").read_text().splitlines():
        if line.startswith("BMB_GHL_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("BMB_GHL_API_KEY not in .env")

API_KEY = load_key()
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "curl/8.7.1",
}

# Field -> target folder. Based on 30-day fill-rate audit 2026-05-19.
# Active fields (>0 writes in last 30d) go to semantic folder.
# Dormant fields (0 writes) go to Deprecated — parked, not deleted.
FIELD_TO_TARGET = {
    # === 📞 Contact Info (active universals) ===
    "contact.preferred_contact_method": "Contact Info",      # 19 fills
    "contact.what_town_do_you_live_in": "Contact Info",      # 20 fills

    # === 🔥 Project Snapshot (active universals) ===
    "contact.project_type": "Project Snapshot",              # 11 fills
    "contact.project_timeframe": "Project Snapshot",         # 11 fills (decking timeline)
    "contact.when_are_you_looking_to_move_into_your_new_home": "Project Snapshot",  # 9 fills (modular timeline)
    "contact.home_type": "Project Snapshot",                 # 11 fills (decking sub-type)

    # === 🏠 Modular Details (active modular survey) ===
    "contact.what_best_describes_your_situation": "Modular Details",     # 9 fills
    "contact.what_are_you_looking_to_build": "Modular Details",          # 9 fills
    "contact.square_footage_youre_considering": "Modular Details",       # 8 fills
    "contact.estimated_square_footage": "Modular Details",               # 7 fills
    "contact.home_total_number": "Modular Details",                      # 7 fills
    "contact.home_cost_number": "Modular Details",                       # 7 fills
    "contact.number_of_bathrooms": "Modular Details",                    # 5 fills
    "contact.number_of_bedrooms": "Modular Details",                     # 4 fills

    # === 🪵 Decking Details ===
    # No active deck-specific fields. Active deck survey writes to universals.
    # Folder kept as placeholder for future.

    # === 📊 Attribution (active tracking) ===
    "contact.utm_source": "Attribution",     # 19 fills
    "contact.utm_medium": "Attribution",     # 19 fills
    "contact.utm_campaign": "Attribution",   # 19 fills
    "contact.utm_content": "Attribution",    # 19 fills
    "contact.utm_term": "Attribution",       # 19 fills

    # === 🗑️ Deprecated (0 fills in last 30d — parked, not deleted) ===
    # BMB_* dormant: bivianomodularbuilders.com not yet receiving paid traffic
    "contact.bmb_town": "Deprecated",
    "contact.bmb_source": "Deprecated",
    "contact.bmb_budget_range": "Deprecated",
    "contact.bmb_lot_status": "Deprecated",
    "contact.bmb_target_start": "Deprecated",
    "contact.bmb_project_description": "Deprecated",
    "contact.bmb_plant_partner": "Deprecated",
    "contact.bmb_home_size": "Deprecated",
    "contact.bmb_home_cost_calc": "Deprecated",
    "contact.bmb_estimate_total": "Deprecated",
    # lt_* + other redundant attribution — UTM_* covers all of this
    "contact.lt_source": "Deprecated",
    "contact.lt_medium": "Deprecated",
    "contact.lt_campaign": "Deprecated",
    "contact.lt_content": "Deprecated",
    "contact.fbclid": "Deprecated",
    "contact.contact_gclid": "Deprecated",
    "contact.ad_id": "Deprecated",
    "contact.adset_id": "Deprecated",
    "contact.campaign_id": "Deprecated",
    "contact.cbtn": "Deprecated",
    "contact.full_url": "Deprecated",
    "contact.placement": "Deprecated",
    "contact.platform": "Deprecated",
    "contact.referrer": "Deprecated",
    # Uncertain — kept until proven needed
    "contact.home_type_2": "Deprecated",
    "contact.what_best_describes_this_deck_job": "Deprecated",
    "contact.where_will_the_home_be_built": "Deprecated",
    "contact.when_do_you_hope_to_have_this_completed": "Deprecated",
    "contact.zip_code": "Deprecated",
    "contact.in_service_area": "Deprecated",
}

def fetch_fields():
    r = requests.get(f"{BASE}/locations/{LOCATION_ID}/customFields", headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json().get("customFields", [])

def folder_id_map(fields, args):
    """Build name->id map. Names need partial-match (e.g. '📞 Contact Info' contains 'Contact Info')."""
    # Try to read from --folders argv (key=id pairs) if provided
    if "--folders" in args:
        i = args.index("--folders") + 1
        m = {}
        for pair in args[i:]:
            if "=" in pair:
                k, v = pair.split("=", 1)
                m[k.strip()] = v.strip()
        return m
    # Otherwise: discover folders by listing all unique parentIds and asking user
    parents = sorted({f.get("parentId") for f in fields if f.get("parentId")})
    print("\nCURRENT FOLDER IDS in use:")
    for p in parents:
        sample = [f["name"] for f in fields if f.get("parentId") == p][:5]
        print(f"  {p}  e.g. {sample}")
    print("\nNEW FOLDER IDS — paste 5 folder IDs as args, format `--folders \"Contact Info=ID\" \"Project Snapshot=ID\" \"Modular Details=ID\" \"Decking Details=ID\" \"Attribution=ID\"`")
    sys.exit(1)

def move_field(field, new_parent):
    fid = field["id"]
    body = {
        "name": field["name"],
        "parentId": new_parent,
    }
    r = requests.put(
        f"{BASE}/locations/{LOCATION_ID}/customFields/{fid}",
        headers=HEADERS, json=body, timeout=30,
    )
    if r.status_code >= 400:
        print(f"    ERR {r.status_code}: {r.text[:200]}")
        return False
    return True

def main():
    args = sys.argv[1:]
    dry = "--apply" not in args
    fields = fetch_fields()
    print(f"Loaded {len(fields)} fields")

    name_to_folder = folder_id_map(fields, args)
    if len(name_to_folder) != 6:
        sys.exit(f"Expected 6 folder mappings, got {len(name_to_folder)}: {list(name_to_folder.keys())}")

    print(f"\nNew folder mapping: {json.dumps(name_to_folder, indent=2)}")
    print(f"\nMode: {'DRY RUN' if dry else 'APPLY'}")

    rollback = []
    skipped = []
    moved = 0
    for f in fields:
        key = f.get("fieldKey")
        target_name = FIELD_TO_TARGET.get(key)
        if not target_name:
            skipped.append(key)
            continue
        target_id = name_to_folder.get(target_name)
        if not target_id:
            print(f"  SKIP {f['name']} - no folder id for '{target_name}'")
            continue
        old_parent = f.get("parentId")
        if old_parent == target_id:
            continue
        print(f"  {f['name']:50}  {old_parent[:8]}... -> {target_id[:8]}...  [{target_name}]")
        if not dry:
            if move_field(f, target_id):
                rollback.append({"id": f["id"], "name": f["name"], "old_parent": old_parent})
                moved += 1
                time.sleep(0.25)

    print(f"\n{'DRY RUN — would have moved' if dry else 'Moved'} {moved} fields")
    if skipped:
        print(f"Skipped {len(skipped)} unmapped fields: {skipped}")

    if not dry and rollback:
        rb = Path("/tmp/bmb_field_reorg_rollback.json")
        rb.write_text(json.dumps(rollback, indent=2))
        print(f"\nRollback log: {rb}")

if __name__ == "__main__":
    main()
