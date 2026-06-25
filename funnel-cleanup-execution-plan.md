# BMB Funnel Cleanup — Execution Plan

**Filed:** 2026-05-19
**Status:** Phase 1 in flight. Decisions locked.

---

## ✅ Done today (via API)

1. Created custom field `How did you hear about us?` (RADIO, options below) in 📞 Contact Info folder
   - Options: Google search · Facebook / Instagram ad · YouTube · Referral from friend or family · Drove by a Biviano build · Past customer · Other
   - Field ID: `hwKp6wl6JSeOMUjzKjwP`
   - Field key: `contact.how_did_you_hear_about_us`
2. Tagged 57 existing contacts with `source:manual-entry` (no source, no URL, medium=Manual)
3. Tagged 72 existing contacts with `source:direct-booking` (landed on /custom-design with no UTM)
4. Updated the hourly cron script to auto-tag future leads with source-classification tags

Result: Mike's contact view now shows source-of-traffic chips for every lead automatically going forward. Shelagh O'Brien now has `source:direct-booking` so Mike knows to ask her in the meeting where she heard about Biviano.

---

## 🎯 Decisions locked

| Decision | Locked answer |
|---|---|
| `bivianocontractingroofs.com` | Retire. Redirect to bivianocontracting.com. |
| `bivianomodularbuilders.com` | Keep for organic only (current state). Eventually migrate ads. Not now. |
| Survey gate | Hybrid — paid ads gated, organic/referrals can go direct |
| Mike buy-in | Full send. Spencer is executing. |

---

## 📋 What's left — your action items (UI work)

### Priority 1: Update the `Custom Design Meeting & Free Estimate` calendar form (~5 min)

This is the calendar Shelagh booked through and where 81+ leads land without qualification.

In **GHL → Calendars → Custom Design Meeting & Free Estimate → Form / Customizations**:
1. **Add field:** Address (standard GHL field) — required
2. **Add field:** City — required
3. **Add field:** State — required (default Massachusetts)
4. **Add field:** Postal Code — required
5. **Add field:** `How did you hear about us?` (custom field — already created today) — required
6. **Add field:** `What town do you live in?` (existing field) — optional
7. Save.

After this, every direct-calendar booking captures address + attribution.

### Priority 2: Retire `bivianocontractingroofs.com` (~10 min)

You said this domain is old/should be retired. Steps:
1. Find where the domain is registered (GoDaddy / Namecheap / etc.)
2. In DNS: set up a 301 redirect to `bivianocontracting.com` (or wherever you want decking traffic to land — see Priority 3)
3. Specifically:
   - `bivianocontractingroofs.com/deck-offer` → wherever decking ads should go now
   - `bivianocontractingroofs.com/custom-design` → `go.bivianocontracting.com/custom-design`
   - everything else `*` → `bivianocontracting.com`
4. Update any active Meta/Google ads currently pointing at `bivianocontractingroofs.com/deck-offer` (47 leads in last 90 days) to use the new destination
5. Wait 7-14 days for DNS propagation + ad delivery to migrate, then confirm zero new traffic on the old domain

### Priority 3: Pick ONE decking landing page going forward

Currently splitting decking traffic across:
- `bivianocontractingroofs.com/deck-offer` (47 leads, being retired)
- `go.bivianocontracting.com/dream-decks` (10 leads, captures survey data)

**Recommendation:** Migrate all decking ads to `go.bivianocontracting.com/dream-decks` (the survey funnel) so you get qualifying data on every lead, same way modular works.

In **GHL → Funnels → "META | DECKS"** or the equivalent decking funnel:
1. Verify `dream-decks` is the canonical URL
2. Verify the decking survey captures: project type, town, timeline, square footage, budget range, material preference
3. If any of those are missing, add them (use existing custom fields from `🪵 Decking Details` folder)

### Priority 4: Normalize source labels going forward

Current source labels are inconsistent. Pick a clean scheme and update every funnel/form/calendar to use it. Suggested scheme:

| Path | Source label |
|---|---|
| Modular paid ad → survey | `Modular | Paid Ad` |
| Decking paid ad → survey | `Decking | Paid Ad` |
| Direct calendar booking (no qualification) | `Direct Booking` |
| Manual entry by staff | `Manual Entry` |
| Chat widget | `Chat Widget` |
| Organic / website | `Organic` |

In **GHL → each funnel → Settings → Source Tracking**, update the source field on each capture step to use one of these 6 labels.

### Priority 5: Verify UTM capture on direct domain (~5 min)

The 60 leads with NO UTM are mostly manual entries, but some are organic visitors who hit the site without UTM params.

**Recommendation:** Add a default UTM-capture snippet to the head of bivianocontracting.com so any visitor without UTMs gets tagged `utm_source=organic&utm_medium=direct` server-side. I can write this snippet if Mike's website team can paste it in.

---

## 📅 Phase 2 (next 2 weeks — once Phase 1 is stable)

- Build a "deck survey" that mirrors `dream-home` data quality (if `dream-decks` isn't already doing this — needs review)
- Consolidate the 5+ "new lead" workflows into ONE master "Lead Intake Summary" workflow (specs in `lead-summary-workflow-walkthrough.md`)
- Set up source-label backfill so Mike's existing reports/views show normalized labels

---

## 📅 Phase 3 (longer term — 1-2 months)

- Migrate paid modular ads off `go.bivianocontracting.com/dream-home` onto `bivianomodularbuilders.com`
  - The new site has calculator, town pages, GA4 — better lead-capture surface
  - Use a phased ad split-test to validate conversion before full migration

---

## 🛡️ Safety net

Everything I did today is reversible:
- The new custom field can be deleted via API
- Tags can be removed in bulk via API
- The hourly cron is fully isolated — disable via `launchctl unload ~/Library/LaunchAgents/com.spg.bmb-hourly-sync.plist`

Nothing destructive has been done. We're additive only.
