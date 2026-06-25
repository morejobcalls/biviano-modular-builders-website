# BMB GHL Custom Field Reorg — Plan

**Filed:** 2026-05-15
**Goal:** One clear, simple field layout that works for modular AND decking leads.
**Approach:** Light touch — reorg into 5 new folders, no field deletes, no data migrations.

---

## Today's mess (49 fields, 5 folders)

| Folder ID | Likely current name | Field count | What's wrong |
|---|---|---|---|
| `rYKLOFeX1c2QHgaNKrvB` | (BMB / Modular?) | 24 | Mixes BMB_* fields with 14 attribution fields (Ad_ID, lt_*, Fbclid, etc.) |
| `091WrhRpvAjRDaam2ZbT` | (Modular Survey) | 10 | Modular survey questions — Tim's data lives here |
| `yJmbk3bpaq763J9Fkvv2` | (Lead Info?) | 9 | Mixed decking + modular + universal fields |
| `yO84G7LRPmvbusJfQd0N` | (UTM Tracking) | 5 | UTM_* fields (also duplicated in folder 1 as `lt_*`) |
| `cWxx3jVcpQhe4pRDp0Qm` | (?) | 1 | Orphan — single `Project Type` field |

---

## New structure (5 folders)

```
📞 Contact Info          (7 fields, universal)
🔥 Project Snapshot      (8 fields, universal)
🏠 Modular Details      (14 fields, modular leads)
🪵 Decking Details       (1 field, decking leads — placeholder for growth)
📊 Attribution           (19 fields, hidden from Mike's daily view)
```

---

## Step 1 — Spencer creates folders (5 min in GHL UI)

In the Biviano sub-account (`zPo4vLlEjjXCflgDSXlI`):

1. **Settings → Custom Fields**
2. Click **+ Add Folder** five times. Create these EXACT names (emoji included):

   - `📞 Contact Info`
   - `🔥 Project Snapshot`
   - `🏠 Modular Details`
   - `🪵 Decking Details`
   - `📊 Attribution`

3. Tell Claude when done. The migration script will read these folders by name and move all 49 fields into the right places via API.

---

## Step 2 — Migration script (Claude runs)

Once Spencer confirms folders exist, run:
```
python3 /tmp/reorg_bmb_fields.py
```

Script behavior:
- Pulls all custom fields + their current parentIds
- Pulls list of folders, maps the 5 new ones by exact name
- For each field, looks up target folder from the mapping table below
- PUTs the field with new `parentId`
- Reports moves + any errors

---

## Step 3 — Spencer reorders folder display (2 min in UI)

In **Settings → Custom Fields**, drag folders into this order top-to-bottom:

1. 📞 Contact Info
2. 🔥 Project Snapshot
3. 🏠 Modular Details
4. 🪵 Decking Details
5. 📊 Attribution

(Old empty folders can be deleted or left at the bottom — they'll have zero fields after migration.)

---

## Step 4 — Spencer builds lead-summary Note workflow (10 min in UI)

In **Automation → Workflows**, build:

**Trigger:** Contact Created
**Filter:** (none — fires on every new contact)

**Action: Add Note to Contact**
Body:
```
🔥 NEW LEAD SUMMARY

Project Type: {{contact.project_type}}{{contact.what_are_you_looking_to_build}}
Town: {{contact.what_town_do_you_live_in}}{{contact.bmb_town}}
Timeline: {{contact.when_are_you_looking_to_move_into_your_new_home}}{{contact.bmb_target_start}}{{contact.project_timeframe}}{{contact.when_do_you_hope_to_have_this_completed}}
Budget: {{contact.bmb_budget_range}}
Situation: {{contact.what_best_describes_your_situation}}{{contact.bmb_lot_status}}

Modular: {{contact.number_of_bedrooms}}br / {{contact.number_of_bathrooms}}ba @ {{contact.estimated_square_footage}}{{contact.bmb_home_size}} sqft
Deck: {{contact.what_best_describes_this_deck_job}}

Contact: {{contact.preferred_contact_method}}
Source: {{contact.bmb_source}}{{contact.utm_source}} → {{contact.utm_campaign}} → {{contact.utm_content}}
```

(GHL ignores merge tags that are empty, so this template adapts to whichever fields are populated for the lead path — modular survey, BMB site, or decking.)

**Optional: also send Mike an SMS or in-app notification with the same content** so he triages from the notification without opening the app.

---

## Field-to-Folder Mapping (full table)

### 📞 Contact Info (7 fields)
| Field | Current folder | Notes |
|---|---|---|
| Preferred Contact Method | yJmbk... | Universal |
| Zip Code | yJmbk... | Universal |
| BMB Town | rYKLOF... | Universal — kept as duplicate of survey town for now |
| What town do you live in? | yJmbk... | Universal — Tim's lives here |
| Home Type | yJmbk... | Universal |
| Home Type 2 | yJmbk... | Universal (figure out what this duplicates later) |
| In service area? | yJmbk... | Universal |

### 🔥 Project Snapshot (8 fields)
| Field | Current folder | Notes |
|---|---|---|
| Project Type | cWxx... | Universal — most important triage field |
| BMB Source | rYKLOF... | Source path |
| BMB Budget Range | rYKLOF... | Universal |
| BMB Target Start | rYKLOF... | Universal timeline |
| BMB Project Description | rYKLOF... | Universal notes |
| BMB Lot Status | rYKLOF... | Modular-leaning but applies to additions/ADU |
| Project Timeframe | yJmbk... | Universal timeline (duplicate) |
| When do you hope to have this completed? | yJmbk... | Universal timeline (duplicate) |

### 🏠 Modular Details (14 fields)
| Field | Current folder |
|---|---|
| BMB Home Size | rYKLOF... |
| BMB Home Cost Calc | rYKLOF... |
| BMB Estimate Total | rYKLOF... |
| BMB Plant Partner | rYKLOF... |
| When are you looking to move into your new home? | 091Wrh... |
| Where will the home be built? | 091Wrh... |
| Home Total (Number) | 091Wrh... |
| Estimated Square Footage | 091Wrh... |
| What best describes your situation? | 091Wrh... |
| Number of bathrooms: | 091Wrh... |
| What are you looking to build? | 091Wrh... |
| Number of bedrooms: | 091Wrh... |
| Square footage you're considering: | 091Wrh... |
| Home Cost (Number) | 091Wrh... |

### 🪵 Decking Details (1 field)
| Field | Current folder |
|---|---|
| What best describes this deck job? | yJmbk... |

### 📊 Attribution (19 fields)
| Field | Current folder |
|---|---|
| UTM_Source, UTM_Medium, UTM_Campaign, UTM_Content, UTM_Term | yO84G7... |
| Ad_ID, Adset_ID, campaign_id, Platform, Placement | rYKLOF... |
| Fbclid, Contact_gclid, Referrer, Full_URL, CBTN | rYKLOF... |
| lt_Source, lt_Medium, lt_Campaign, lt_content | rYKLOF... |

---

## Risks

- **Forms / funnels reference fields by ID, not by folder** → folder reorg should NOT break the current GHL survey, the bivianomodularbuilders.com webhooks, or any automation.
- **Workflow merge tags use `{{contact.field_key}}`** → field key isn't tied to folder either, so existing tags keep working.
- **Worst case rollback:** Run a reverse script with the old parentId mapping (script logs original parentId for each move).

---

## Outstanding items (parking lot — for future sessions)

- **Consolidate duplicate timeline fields** (4 of them) into one canonical field
- **Figure out `Home Type` vs `Home Type 2`** — pick one, deprecate the other
- **Sunset `lt_*` attribution fields** in favor of standard `UTM_*` (they appear redundant)
- **Migrate the GHL survey funnel** at go.bivianocontracting.com to write into `bmb_*` canonical fields, so scorecard works
