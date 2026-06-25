# BMB Monthly Scorecard

Automated one-pager for Mike Biviano. Pulls live data from GHL once a day and renders a side-by-side current-month vs. previous-month dashboard in a Google Sheet.

## What it shows

For both the current month and the previous month:

- **Leads (by source)** — count of contacts created in the month, grouped by `bmb_source` (Calculator, Consultation form, Town page, Direct). Plus a TOTAL row.
- **Funnel** — current count of opportunities in the `Modular Pipeline` at the `Discovery Call Booked`, `Site Visit Done`, and `Contract Signed` stages.
- **Revenue** —
  - Pipeline $ = sum of `bmb_estimate_total` for contacts created in the month who are NOT in a lost stage.
  - Closed $ = sum of `bmb_estimate_total` for contacts created in the month who are in the `Contract Signed` stage.
- **Last updated** timestamp at the bottom.

## Files

| File | Purpose |
|---|---|
| `Code.gs` | The Apps Script. Paste into Extensions → Apps Script in the Google Sheet. |
| `SETUP.md` | Step-by-step install for Spencer. |
| `README.md` | This file. |

## How the daily refresh works

`setup()` creates a time-driven trigger that fires `refreshScorecard()` once per day around 6am ET. The function:

1. Reads `GHL_API_KEY` from Script Properties (never hardcoded).
2. Pulls contacts created since the start of the previous month via `POST /contacts/search` (falls back to `GET /contacts` pagination if v2 search rejects the filter).
3. Looks up the pipeline named exactly `Modular Pipeline` via `GET /opportunities/pipelines`. If not found, the funnel + closed-revenue cells render `"Pipeline not yet created"` and the script returns successfully.
4. Pulls all opportunities for that pipeline via `GET /opportunities/search`.
5. Groups leads by source, counts opps per stage, and sums `bmb_estimate_total` per contact (matched to opp by contactId to determine stage).
6. Writes the `Dashboard` sheet and appends a row to the `Log` sheet.

Any GHL error is caught, logged with stack trace to the `Log` tab, and re-thrown so it shows up in Apps Script execution history.

## Known gotchas

- **Pipeline must be created in GHL UI before funnel/revenue numbers populate.** PIT scope blocks pipeline writes via API. Stages must be named exactly: `Discovery Call Booked`, `Site Visit Done`, `Contract Signed`. Lost stages are auto-detected by name containing "lost" or "unqualified" and are excluded from Pipeline $.
- **Daily refresh window is ~6am ET.** Numbers can be up to 24 hours stale. Force a refresh by running `refreshScorecard` manually from the Apps Script editor.
- **"Pipeline $" uses the calculator estimate, not a manually-set opp value.** Contacts who came in via the Consultation form (not the calculator) won't have `bmb_estimate_total` set and will contribute $0 to Pipeline $ unless Mike fills it in manually on the contact record.
- **Source bucket spelling matters.** The four canonical values are `Calculator`, `Consultation form`, `Town page`, `Direct`. Any other string (typo, manual entry, legacy) gets its own row in the Leads breakdown. If you see an unexpected source label, audit the contact + the webhook payload.
- **Time zone.** The script uses the Sheet's script time zone (usually America/New_York) to determine "current month." If you copy this script to a sheet in a different time zone, set it via Apps Script → Project Settings → Time zone.

## If the numbers look wrong

1. Open the `Log` tab. If the last row is `ERROR`, the message is there.
2. In Apps Script: View → Executions. Drill into the most recent `refreshScorecard` run.
3. Confirm `GHL_API_KEY` is still valid (PITs can be revoked). Test it with:
   ```bash
   curl -H "Authorization: Bearer $KEY" -H "Version: 2021-07-28" \
     "https://services.leadconnectorhq.com/opportunities/pipelines?locationId=zPo4vLlEjjXCflgDSXlI"
   ```
4. Confirm the pipeline name in GHL UI is still exactly `Modular Pipeline` (case-insensitive match, but no extra whitespace).
5. Spot-check one contact in GHL — does the `bmb_source` custom field actually have a value? Does `bmb_estimate_total` look right? The webhook wiring is documented in `../HANDOFF.md`.
