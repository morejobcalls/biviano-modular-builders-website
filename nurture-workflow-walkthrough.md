---
name: BMB Modular Nurture — GHL Workflow Walkthrough
created: 2026-05-27
status: ready-to-activate
owner: Spencer
related:
  - ../../Marketing/Nurture Sequences/Email - 8 Week Modular Lead/README.md
---

# BMB Modular Nurture — GHL Workflow Walkthrough

**Goal:** Activate the 12-email, 8-week modular lead nurture sequence in BMB GHL.

**Prerequisites already met (today):**
- ✅ All 12 templates live in folder `Nurture - Modular Lead 8 Week` (folder id `6a072d9406376ac2d680fcf2`)
- ✅ Every CTA points to `https://go.bivianocontracting.com/dream-home-booking` (booking URL is baked in — no swap needed)
- ✅ Source markdown locked in at `Marketing/Nurture Sequences/Email - 8 Week Modular Lead/`

**Estimated UI time:** 15 minutes.

---

## Step 1 — Reply-to + from-name — ✅ DONE (location-level, 2026-06-02)

Spencer set reply-to at the **location level** (`mbiviano@hotmail.com`), so the per-template editing originally described here is **no longer needed** — every nurture email inherits it. Skip straight to Step 2.

> Templates were also renamed to a clean convention on 2026-06-02: `Modular Nurture NN · Topic` (e.g. `Modular Nurture 01 · Welcome`). Use these exact names in the Send Email steps below. Rename script: `scripts/rename_bmb_nurture.py`.

---

## Step 2 — Build the workflow (10 min)

GHL → **Automation → Workflows → + Create Workflow → Start from Scratch**

### Name + trigger
- **Name:** `🏠 Modular Lead Nurture (8 Week)`
- **Add Trigger → Contact Created**
- **Filters on the trigger:**
  - `Custom Field → bmb_source → IS NOT EMPTY`

  *(This ensures only contacts who came in through the modular site enter the sequence. The cron writes bmb_source within 1hr if it's missing.)*

### Actions (in this exact order)

The pattern is: **Wait → Send Email → Wait → Send Email → ...** for 12 emails.

| Step | Action | Setting |
|---|---|---|
| 1 | **Send Email** | Template: `Modular Nurture 01 · Welcome` |
| 2 | **Wait** | 2 days |
| 3 | **Send Email** | Template: `Modular Nurture 02 · Meet Mike` |
| 4 | **Wait** | 3 days |
| 5 | **Send Email** | Template: `Modular Nurture 03 · The Cheap Myth` |
| 6 | **Wait** | 4 days |
| 7 | **Send Email** | Template: `Modular Nurture 04 · Financing` |
| 8 | **Wait** | 5 days |
| 9 | **Send Email** | Template: `Modular Nurture 05 · The Numbers` |
| 10 | **Wait** | 7 days |
| 11 | **Send Email** | Template: `Modular Nurture 06 · Set Day` |
| 12 | **Wait** | 7 days |
| 13 | **Send Email** | Template: `Modular Nurture 07 · Your Lot` |
| 14 | **Wait** | 7 days |
| 15 | **Send Email** | Template: `Modular Nurture 08 · Timeline` |
| 16 | **Wait** | 3 days |
| 17 | **Send Email** | Template: `Modular Nurture 09 · Still Thinking` |
| 18 | **Wait** | 7 days |
| 19 | **Send Email** | Template: `Modular Nurture 10 · Social Proof` |
| 20 | **Wait** | 7 days |
| 21 | **Send Email** | Template: `Modular Nurture 11 · Custom Design` |
| 22 | **Wait** | 4 days |
| 23 | **Send Email** | Template: `Modular Nurture 12 · Final Check-In` |

> Cadence math: emails land at days 0, 2, 5, 9, 14, 21, 28, 35, 38, 45, 52, 56. Matches the README's 8-week schedule.

### Exit conditions (set on the workflow, top right → Settings)
- **Exit on:** Pipeline stage changes to `Discovery Call Booked` or later (once the Modular Pipeline exists)
- **Exit on:** Contact replies to any email (GHL handles this natively when "Stop on reply" is toggled at the workflow level)
- **Exit on:** Contact unsubscribes

### Publish
Top right → toggle **Draft → Published**.

---

## Step 3 — Smoke test (2 min)

1. **Contacts → + Add Contact**
2. Fill in:
   - First name: `Test`
   - Last name: `Nurture`
   - Email: **your own email** (so you receive the welcome)
3. Set custom field `bmb_source` to `Calculator` (any value works)
4. Save
5. Within ~2 minutes, you should receive the `01-welcome` email at your inbox
6. Delete the test contact after confirming

---

## Notes

- **v2 revisions** are scoped for after 30 days of real data — see README "Open items for v2"
- **Reply handling:** When a contact replies, GHL forwards to the reply-to address. Mike sees the conversation in his inbox + GHL marks the contact as replied (exits sequence).
- **Booking link** is `go.bivianocontracting.com/dream-home-booking`. If Mike wants a different booking page later, the source-of-truth `[[BOOK_CALL_URL]]` placeholder pattern is preserved in `/tmp/update_bmb_nurture_v2.py` for an easy bulk swap.
