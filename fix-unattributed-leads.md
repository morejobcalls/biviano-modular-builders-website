---
title: BMB — Three fixes to reduce the "Needs Triage" bucket
created: 2026-05-27
status: recommendations
owner: Spencer + Mike
related:
  - scorecard/Code.gs (where the classifier reads from)
---

# Fixes to reduce "Needs Triage" leads to zero

**Context:** The monthly scorecard breaks leads into Modular / Decking / Needs Triage. Today (May 2026), 60% of leads land in Needs Triage — meaning the system can't tell what service line they want.

This isn't a scorecard bug. It's a real data-capture gap at the intake level. Three fixes close the gap:

---

## Fix 1 — Add "What are you looking to build?" to the Custom Design Meeting booking form

**Impact:** ~20 leads/month auto-classify (40% of current Needs Triage)

**Why it's broken:** The `Custom Design Meeting & Free Estimate` calendar at `go.bivianocontracting.com/custom-design` collects name, email, phone, and address — but **no service-line question**. Anyone can book without saying whether they want a deck, modular home, ADU, or renovation. Mike books their time without knowing what they want until the call.

**The fix:**
1. GHL → Sites → Forms → open form `KxKSaYRrnqKySmPyD0tf` (Modular Home Booking Calendar Form - V1)
2. Add a **RADIO** custom field: `project_type` (or use existing `bmb_project_description` if appropriate)
3. Required: YES
4. Options (in this order):
   - Custom modular home
   - ADU / in-law / detached studio
   - Deck (new build)
   - Deck (repair / replace)
   - Renovation / addition
   - Other / not sure yet
5. Place above the address field on the form
6. Save

**Bonus:** Renaming the form from "Modular Home Booking Calendar Form - V1" to something more accurate (e.g., "Custom Design Intake Form V2") would prevent future confusion.

**Classifier behavior after this fix:**
- Any value containing "modular", "ADU" → service line = Modular
- Any value containing "deck" → service line = Decking
- "Renovation / addition" → service line = Renovation (new category, low volume, easy to add)
- "Other / not sure yet" → service line = Needs Triage (legitimately ambiguous — Mike triages on the call)

---

## Fix 2 — Standardize the manual-entry workflow

**Impact:** ~10 leads/month auto-classify (20% of current Needs Triage)

**Why it's broken:** When VA or Mike adds a contact by hand (phone call, walk-in, referral, social DM), no source field is set. Today these all land in Needs Triage with no detail.

**The fix:**
Create a GHL workflow that fires on **Contact Created with `tag: source:manual-entry`** (the hourly cron already tags manual contacts this way) and triggers a prompt requiring the operator to set:
1. `lead_source` (RADIO): Phone call / Referral / Walk-in / Social DM / Trade show / Other
2. `service_interest` (RADIO): Modular / Deck / Both / Unknown
3. (Optional) Free-text notes field

OR — simpler workflow change: train Mike + VA to set the GHL native `source` field manually when adding a contact. The dropdown supports custom values. Mike picks one of:
- `Referral - <name>`
- `Phone call - inquiry`
- `Walk-in`
- `Social DM`

The classifier already reads the source field and can be extended with these patterns.

**Lighter-touch alternative:** add a "lead_source" required field on the manual-add form layout. Same result, fewer workflows.

---

## Fix 3 — Audit the "bare contact" leak

**Impact:** ~7 leads/month (likely fewer once fixes 1 + 2 land)

**Why it's broken:** Some contacts have NO source field, NO UTMs, NO tags — they just appear with name/email/phone. These are usually:
- Form submissions where the form didn't include a source tag
- API integrations (e.g., third-party intake) that don't write source
- Imports from a CSV that didn't include source

**The fix:**
1. Find a few recent "bare" contacts (the scorecard surfaces them under Triage Queue → Bare contact).
2. Look at their `dateAdded` timestamp + `createdBy` field.
3. Trace back: which integration/form/import created them?
4. Add a source tag at that intake point.

Likely culprits to check:
- GHL chat widget (sets source=`chat widget` for some but not all)
- Facebook lead form integration (should set source but may not be wired)
- The pop-up opt-in forms (POP-UP-1, POP-UP-2)

---

## After all three fixes

Expected Triage count drops from ~37/month → ~0-3/month. The remaining triage leads are legitimately ambiguous ("not sure yet" responders) and warrant Mike's personal touch.

## Order of operations (recommended)

1. **Fix 1 first** — biggest impact, easiest to implement (form edit in GHL Forms Builder, ~5 min)
2. **Fix 2 next** — train Mike + VA on the manual-entry checklist
3. **Fix 3 last** — diagnostic work, lower priority since volume is small

Once Fix 1 ships, re-run `refreshScorecard()` and the Needs Triage column should drop noticeably within a few days.
