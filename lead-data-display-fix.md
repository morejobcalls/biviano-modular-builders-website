# Mike's "leads not coming through with info" — diagnosis + fix

**Filed:** 2026-05-15
**Reported by:** Mike Biviano
**Example lead:** Tim Leedom (`leedom.tim@gmail.com`, +1 503-412-8544)

## TL;DR
Mike's leads ARE coming through with full info. The data lives in custom fields that aren't surfacing on his GHL contact view. **Fix is a 5-minute reorder in GHL Settings → Custom Fields.**

## What's actually in Tim's record

| Field | Value |
|---|---|
| First / Last | Tim Leedom |
| Email | leedom.tim@gmail.com |
| Phone | +1 503-412-8544 |
| Address | 74 Bay Road, Duxbury, MA 02332 |
| **Town (survey)** | Duxbury |
| **Situation** | 🏡 I own land and want to build |
| **Move-in timeline** | ⚡ ASAP – Within 3–6 months |
| **Bedrooms** | 2 |
| **Bathrooms** | 1.5 |
| **Square footage** | 1,000–1,500 sq ft |
| **What to build** | Other / not sure yet |
| **Preferred contact** | 📱 Text Message |
| **Ad source** | Facebook → SPG \| Modular Homes campaign → "Million Dollar Lie" creative |
| **Landing page** | go.bivianocontracting.com/dream-home |
| **Booked** | Yes — opportunity in pipeline `81G5v6w6GkW8yzQtjj2H` |
| **Created** | 2026-05-13 (2 days ago) |

This is a qualified lead with strong intent (owns land, ready in 3–6 months).

## Why Mike doesn't see this on his contact card

GHL custom fields are grouped into **field folders**. Tim's data is sitting in the **Modular Survey** folder (internal ID `091WrhRpvAjRDaam2ZbT`). That folder isn't pinned to the top of the contact card layout, so it falls below `Actions` and `DND` — Mike has to scroll past those to see anything useful.

The `bmb_*` folder we set up for the **bivianomodularbuilders.com** website (`rYKLOFeX1c2QHgaNKrvB`) is currently empty for every lead because **none of the recent paid traffic is hitting that site** — it's all going to the GHL `go.bivianocontracting.com` survey funnel.

## Lead source breakdown (last 50 contacts)

| Path | Leads |
|---|---|
| GHL survey funnels (Modular + Decking) at `go.bivianocontracting.com` | 18 |
| `Custom Design Meeting & Free Estimate` calendar booking | 17 |
| No source tagged | 12 |
| Chat widget on `bivianocontracting.com` | 3 |
| **`bivianomodularbuilders.com` (the new site)** | **0** |

## Fix — 5 minutes in GHL UI

In the Biviano sub-account (`zPo4vLlEjjXCflgDSXlI`):

1. Go to **Settings → Custom Fields** (left nav).
2. Find the field folder containing **"What town do you live in?"**, **"Number of bedrooms:"**, **"What are you looking to build?"**, etc. — that's the Modular Survey folder.
3. Drag it to the top of the folder list (above the BMB folder and UTM folder).
4. Inside that folder, reorder fields so the most useful ones surface first: Town → Situation → Move-in timeline → Bedrooms/Bathrooms/Sqft → Preferred contact.
5. Open Tim's contact (`VrHcvsc19JbQ8wiika1U`) to verify the survey block now appears near the top.

**Bonus:** also drag the BMB folder up so when leads do start coming through the new site, those fields display too.

If Mike still doesn't see the data in the **mobile app** after this, toggle "Hide Empty Fields" OFF temporarily — the mobile app sometimes hides custom field groups by default until a contact has at least one value in them.

## Recommended follow-up (not done yet)

- **Field-unification workflow:** auto-copy values from the Modular Survey fields into the canonical `bmb_*` fields when contacts are created via the survey funnel. Once done, the monthly scorecard and any future automations work regardless of intake path. ~30 min to build.
- **Update HANDOFF.md:** note that all current paid traffic goes through the GHL survey funnel, not bivianomodularbuilders.com. The new site's `bmb_*` schema is dormant until ads are migrated.

## Lead notification template (likely root cause if fix above doesn't satisfy Mike)

Mike may be reacting to a **new-lead SMS or email notification** that doesn't include the survey field values. If he gets a ping like "New lead: Tim Leedom, +1 503-412-8544" with nothing else, he'll assume the lead came in bare. Check **Automation → Workflows** for an active "New Lead" notification to Mike and add the Modular Survey merge tags to that template.
