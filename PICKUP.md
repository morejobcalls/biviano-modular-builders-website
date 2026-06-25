---
client: "Biviano Modular Builders (Mike Biviano)"
project: "BMB modular rebrand — close-out + full activation"
status: "Active — close-out in progress"
percent_complete: 95
last_touched: "2026-06-02"
current_blocker: "Task B: nurture workflow skeleton built via GHL AI builder; Spencer swapping the 12 Send-Email nodes from quick-compose → saved templates (GHL AI can't auto-attach templates), then manual checklist + publish + smoke test. Task C: GA4 ✅ verified; Search Console BLOCKED — apex-property verification kicked to GoDaddy domain verification, code was emailed to Mike Biviano (awaiting forward)."
next_action: "Finish Task B: swap 12 template nodes, set trigger/filter/settings per nurture-workflow-walkthrough.md, publish, then Claude stages test contact (tag `lead:modular` + Spencer's email). Search Console parked until Mike forwards the GoDaddy code."
owner: "Spencer"
summary_oneline: "Modular rebrand close-out: scorecard ✅, GA4 ✅; nurture workflow skeleton built (template-node swap + publish remaining); Search Console blocked on a GoDaddy verification code sent to Mike."
---

# BMB — PICKUP

**Last touched:** 2026-06-02 (GA4 ✅; nurture skeleton built — template swap+publish remain; Search Console blocked on GoDaddy code sent to Mike)
**Client:** Biviano Modular Builders (Mike Biviano)
**GHL Location:** `zPo4vLlEjjXCflgDSXlI`
**How to resume:** Open this file. Tell Claude "pick up BMB from PICKUP.md."

---

## 🔴 RESUME HERE (next session)

Driving 3 close-out tasks (A/B/C) to fully activate the modular rebrand for final invoice (Option B framing).

**Task A — Scorecard: ✅ DONE.** v3 live + running daily.
**Task B — Nurture workflow: 🟡 MID-BUILD.** Skeleton built in GHL AI builder; template-node swap + publish + smoke test remain. Resume point below.
**Task C — GA4: ✅ DONE / Search Console: 🅿️ BLOCKED on Mike (GoDaddy code).** Detail below.

### Task B resume (the active thread)
- ✅ **Reply-to DONE (2026-06-02):** set location-level to `mbiviano@hotmail.com` — no per-template editing needed.
- ✅ **Templates renamed (2026-06-02):** all 12 now `Modular Nurture NN · Topic` (clean, sortable). Done via `scripts/rename_bmb_nurture.py` (GHL has no rename endpoint → clone-with-live-HTML + delete-old, so the real booking CTAs were preserved; verified no `[[BOOK_CALL_URL]]` leaks). **Template IDs changed** — nothing referenced them yet so no breakage.
- ✅ **Cleanup:** deleted the empty duplicate `Nurture - Modular Lead 8 Week` folder (`6a072d78c166dffe850065b6`). Canonical folder `6a072d9406376ac2d680fcf2` holds all 12.
- ✅ Already done (earlier): all 12 CTAs point to `go.bivianocontracting.com/dream-home-booking`.

**Decisions locked (2026-06-02):**
- **Trigger = tag `lead:modular` added** (NOT "Contact Created + bmb_source" — that has a cron-timing bug; `lead:modular` is the only modular tag that reliably fires, confirmed on 9/100 sampled contacts; `source:modular-survey`/`-page` never populated).
- **Entry filter:** contact does NOT have `appointment-confirmed` (don't nurture-to-book someone already booked).
- **Exits:** books a call (`appointment-confirmed` added — handled via the booking-confirmation workflow's Remove-from-Workflow action) + reply (Stop-on-Reply ON) + unsubscribe. Otherwise completes all 12 then ends.
- **From:** default location sender (reply-to inherits `mbiviano@hotmail.com`). **Send anytime** (no business-hours gate).
- **v1 is EMAIL-ONLY.** SMS companion deferred to the 30-day v2 (already in the sequence README's v2 list).

**GHL AI builder gotcha (confirmed live):** the AI builder scaffolds trigger + Send/Wait chain but will NOT attach saved templates — it defaults every Send Email to inline "quick compose." No prompt fixes this (Workflows API is IAM-blocked, so no programmatic attach either). **Manual swap required:** open each of the 12 Send Email nodes → switch to the saved template (`Modular Nurture 01..12`). Paste-in prompt + node→template map are in the chat / walkthrough.

**Remaining steps:**
1. Swap the 12 Send-Email nodes to their templates (in order, `Modular Nurture 01 · Welcome` … `12 · Final Check-In`).
2. Set trigger filter + Settings (re-entry OFF, Stop-on-Reply ON), confirm default sender, wire booking-removal, publish.
3. Smoke test: Claude stages a test contact via API (tag `lead:modular` + Spencer's email) → confirm `01 · Welcome` lands → Claude deletes it.

⚠️ **Source-markdown caveat:** the locked markdown at `Marketing/Nurture Sequences/Email - 8 Week Modular Lead/` still uses `[[BOOK_CALL_URL]]` placeholders. The correct booking URL lives ONLY in the live GHL templates. Do NOT re-run `create_bmb_nurture.py` (it would reintroduce placeholders) without first swapping the URL in markdown.

### Task C resume
- **GA4: ✅ DONE (2026-06-02).** Property `Biviano Modular Builders` (a373538036p536260258), stream `BMB` → Measurement ID `G-GW5Z0VVDEC` (matches live site, x2 home + x2 /pricing/), "receiving traffic in past 48 hours." Realtime showed 0 live (browser blocker/consent — non-issue; 48h-traffic line is the proof).
- **Search Console: 🅿️ BLOCKED on Mike.** Site canonical = **apex** (`bivianomodularbuilders.com`); `www` 301-redirects to apex, so the `www`-property sitemap submit returned "Couldn't fetch." Fix = use the **apex** URL-prefix property. BUT adding apex triggered GoDaddy **domain verification** (DNS at `domaincontrol.com` = GoDaddy, NOT Porkbun — can't self-serve the TXT), and the verification **code was emailed to Mike Biviano**. **Resume when Mike forwards the code** → finish verification → submit `sitemap.xml` at apex.
- 🔧 Future cleanup (non-blocking): sitemap `<loc>` entries are all `www` while pages canonicalize to apex — fix the sitemap source to apex hostname for perfect consistency.

---

## 📊 Scorecard — what shipped (Task A, DONE 2026-05-28)

- **Live Sheet:** https://docs.google.com/spreadsheets/d/1JV9v97g3t94tDAGbzMTveg_9MXRsvjIWP5ao495RclE/edit
- **Apps Script source of truth:** `scorecard/Code.gs` (v3). Daily 6am refresh trigger set. API key in Script Properties.
- **v3 design:** Leads = Channel (Meta/FB Ads, Google Ads, Google Organic, Email, Direct, Chat widget, Manual entry, Other) × Service Line (Modular / Decking / Needs Triage), current vs previous month side-by-side. Plus a **Triage Queue** section, a **Sales (2026)** funnel (Meetings Booked / Completed / Jobs Won), and Revenue (Pipeline $ / Closed $ from `opp.monetaryValue`).
- **Pipeline:** Repointed from the never-created "Modular Pipeline" → existing **Sales (2026)** (`81G5v6w6GkW8yzQtjj2H`). Mike does NOT need to create a new pipeline.
- **Shared with:** `sheets-mcp@spg-sheets-mcp.iam.gserviceaccount.com` (Editor, so Claude can verify via Sheets MCP). **NOT yet shared with Mike** (Spencer parked that).
- **Parked cleanup:** delete the leftover placeholder tab named `BMB Monthly Scorecard` (index 0) so Dashboard shows first; share with `mbiviano@hotmail.com` as Viewer when ready.
- **First-data signal:** 60% of leads land in "Needs Triage" — root cause + 3 fixes documented in **`fix-unattributed-leads.md`** (Fix 1 = add a "What are you looking to build?" field to the Custom Design booking form — biggest impact).

---

## 🟢 Earlier in the close-out (shipped 2026-05-26)

Shipped Tasks 2, 3, 5 (Master Lead Intake workflow, domain retirement, "How did you hear" field).

### ✅ Task 1 — Calendar form leak (shipped 2026-05-22)
- Swapped Custom Design calendar's blank formId → `KxKSaYRrnqKySmPyD0tf` via API.
- Future direct bookings now capture address + name + email + phone.

### ✅ Task 2 — Master Lead Intake Workflow (shipped 2026-05-26)
- 2-action workflow built in GHL UI: Contact Created → Send SMS to Mike → Add Note.
- Tested with two API contacts: SMS hit Spencer's phone (he routed the Mike user to his own number for the test), Note rendered in <5s.
- Action 1 (tag If/Else) deliberately skipped — hourly cron handles tags.
- Cosmetic quirk filed: `{{contact.address1}}` renders literal "undefined" for contacts with no address1 — only affects bare/manual contacts; real form leads render clean.

### ✅ Task 3 — Retire `bivianocontractingroofs.com` (shipped 2026-05-26)
- Registrar = Porkbun; Spencer enabled API access for the domain.
- Replaced stale parking forward + deleted apex A record (Cloudflare→GHL) and `www` CNAME (GHL).
- Added permanent (301) URL forward, wildcard ON, includePath OFF → `https://bivianocontracting.com`.
- Verified live: `bivianocontractingroofs.com/*` → 301 → `bivianocontracting.com` → 200.
- Preserved: MX (Mailgun), SPF, DKIM, DMARC, `_acme-challenge`, NS records.
- ⚠️ Domain expires `2026-09-03` — decide before then: renew (keeps 301 alive for SEO/bookmarks) or let lapse.

### ⚪ Task 4 — Migrate decking ads off old domain (OBSOLETE 2026-05-26)
- Confirmed via Meta Ads MCP: all 3 active BMB ads UTM to `go.bivianocontracting.com/*` already.
- Zero contacts in last 30d referenced `bivianocontractingroofs.com` in any URL field.
- The 301 redirect from Task 3 catches any stale/legacy traffic.

### ✅ Task 5 — "How did you hear about us?" added to Custom Design form (shipped 2026-05-26)
- Spencer dragged field `hwKp6wl6JSeOMUjzKjwP` (RADIO, 7 options) onto `KxKSaYRrnqKySmPyD0tf` via Form Builder.

### 🅿️ Task 6 — Monthly scorecard (PARKED 2026-05-26)
- All three paths parked by Spencer today (Google Sheet via Apps Script, local cron + Sheets MCP, custom GHL dashboard).
- Recommendation for resume: revisit when Mike has (a) created the `Modular Pipeline` and (b) wired `bmb_estimate_total` → `opp.monetaryValue` at opp creation. Until then the funnel + revenue widgets render zero.
- Spec already drafted (in conversation history): 8-widget GHL custom dashboard — counter for MTD leads, pie for sources, funnel for pipeline, counters for new opps / pipeline$ / closed$ / bookings, period-comparison toggle.
- GHL Dashboards API is scope-blocked — build must be UI drag-and-drop (~15-20 min).

### ⏳ Task 7 — Mike's homework (BLOCKED ON MIKE)
- ⭐ **NEW (2026-06-02): forward the GoDaddy domain-verification code** for `bivianomodularbuilders.com` (Google sent it to Mike's email during Search Console apex-property setup). Blocks finishing Search Console.
- Create `Modular Pipeline` in GHL Settings → Pipelines. Stages: New Lead → Discovery Call Booked → Site Visit Done → Budget Range Agreed → LOI Signed → Contract Signed. Required for funnel + revenue tracking.
- ~~Confirm GA4 wired on `bivianomodularbuilders.com`~~ ✅ DONE 2026-06-02 (verified firing, ID `G-GW5Z0VVDEC`).
- Send real project photos (replace stock).
- Confirm calculator pricing is current.

---

## 🛠️ What's running autonomously right now

| System | Status | Where |
|---|---|---|
| Hourly cron — tags + notes for new BMB leads | ✅ Live | `~/Library/LaunchAgents/com.spg.bmb-hourly-sync.plist` (fires :07 every hour) |
| 12-email modular nurture in GHL | ✅ Templates pushed | GHL folder `6a072d9406376ac2d680fcf2` (workflow not wired yet) |
| 49 custom fields organized into 6 emoji folders | ✅ Done | 📞 Contact / 🔥 Project Snapshot / 🏠 Modular / 🪵 Decking / 📊 Attribution / 🗑️ Deprecated |
| 57 existing contacts tagged `source:manual-entry` + 72 `source:direct-booking` | ✅ Done | Backfilled via API |
| Calendar form leak | ✅ Fixed | Custom Design calendar now uses `KxKSaYRrnqKySmPyD0tf` |

**Disable cron if needed:** `launchctl unload ~/Library/LaunchAgents/com.spg.bmb-hourly-sync.plist`

---

## 🔑 Key IDs (don't re-discover)

| Thing | ID |
|---|---|
| BMB Location | `zPo4vLlEjjXCflgDSXlI` |
| API key env var | `BMB_GHL_API_KEY` in `/Volumes/T7/SPG/Claude Code/.env` |
| Good form | `KxKSaYRrnqKySmPyD0tf` |
| Custom Design calendar | `3tdEhe7RsxzwiW5on2oB` |
| Dream Home Design Consultation calendar | `ML9NOoDw8ikmz2rAVnPA` |
| "How did you hear" field | `hwKp6wl6JSeOMUjzKjwP` (key: `contact.how_did_you_hear_about_us`) |
| Mike Biviano user | `dyTkoHhXITCOaSm1ZC4t` (phone +16176786446) |
| Nurture folder | `6a072d9406376ac2d680fcf2` |
| Custom field folders | 📞 `SLPZHZhuWzN8GBjYinip` / 🔥 `PhNJ6aiHgxvytROSpAHn` / 🏠 `GlAtMqtG96QnwYAW0jTR` / 🪵 `xcCN79eGNa1rC3zdij1R` / 📊 `tdAJNG0jMTZlm8I0EVM9` / 🗑️ `KoPnOQ0jMCcD55aknJGO` |

---

## 📂 Source-of-truth docs (in this folder)

- `HANDOFF.md` — full project state, what shipped
- `funnel-audit-and-simplification.md` — diagnosis: 4 domains, 9 LPs, 7 source labels, 29% blank-address leads
- `funnel-cleanup-execution-plan.md` — locked decisions + action items
- `lead-summary-workflow-walkthrough.md` — Task 2 step-by-step (use when picking up Task 2)
- `lead-data-display-fix.md` — Tim Leedom diagnosis
- `ghl-field-reorg-plan.md` — field mapping
- `scripts/bmb_hourly_sync.py` — cron source (deployed copy lives at `~/bin/bmb-cron/`)
- `scripts/create_bmb_nurture.py` — nurture email pusher
- `scripts/reorg_bmb_fields.py` — field-folder mover
- `scripts/backfill_lead_summary_notes.py` — one-shot note backfill
- `scripts/backfill_lead_tags.py` — one-shot tag backfill

---

## 🎯 How to resume

Spencer says: **"pick up BMB from PICKUP.md"**

Claude should:
1. Read this file + `lead-summary-workflow-walkthrough.md`
2. Confirm hourly cron still running: `launchctl list | grep bmb-hourly-sync`
3. Continue from Task 2 (Master Lead Intake Workflow) unless Spencer redirects
4. One task at a time. No 5-page dumps. Spencer flagged overwhelm — pace matters.

---

## ⚠️ Constraints to remember

- Spencer wants **maximum autonomous execution** — "ideally, nothing" on his plate
- **Don't delete anything in GHL** — move dormant stuff to 🗑️ Deprecated folder instead
- Mike sees leads on **LeadConnector mobile** — Notes are buried on a separate tab. Tags + SMS are the primary visibility layer
- **Forms + Workflows APIs are IAM-blocked** in this sub-account — anything that touches them needs UI walkthrough
- Hourly cron handles tags + notes for new contacts. SMS notification to Mike happens via GHL workflow (the one Task 2 builds)
