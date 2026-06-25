# BMB Monthly Scorecard — Setup

One-time install. ~5 minutes.

## Steps

1. **Create the Sheet**
   Go to https://sheets.new and name it `BMB Monthly Scorecard`. Save it in the SPG Drive (or wherever you keep client deliverables).

2. **Open Apps Script**
   `Extensions → Apps Script`. A new project tab opens. Delete the default `function myFunction() {}` stub.

3. **Paste the script**
   Open `Code.gs` from this folder, copy the entire contents, paste into the Apps Script editor. Save (Cmd+S). Name the project `BMB Scorecard` when prompted.

4. **Add the API key to Script Properties**
   In Apps Script: `Project Settings (gear icon, left sidebar) → Script properties → Add script property`.
   - Property: `GHL_API_KEY`
   - Value: paste the value of `BMB_GHL_API_KEY` from `/Volumes/T7/SPG/Claude Code/.env`

   (The `setup()` flow below will also prompt for this and save it, but doing it here means you can skip the prompt and just trust the script.)

5. **Run `setup()` once**
   Back in the editor, pick `setup` from the function dropdown next to the Run button → click Run. Google will ask you to accept OAuth scopes — accept them (this script needs Sheets + UrlFetch access).

   `setup()` does three things:
   - Saves the API key to Script Properties (if you skipped step 4)
   - Creates a daily time-driven trigger to refresh around 6am
   - Runs `refreshScorecard()` once so the Dashboard is populated immediately

6. **Verify the Dashboard tab**
   Switch back to the Sheet. You should see a `Dashboard` tab with the current month + previous month side-by-side, plus a `Log` tab tracking each run.

   If funnel rows say `"Pipeline not yet created"`, that's expected until you create the `Modular Pipeline` in GHL UI (Settings → Pipelines → +Create New Pipeline; stages: New Lead → Discovery Call Booked → Site Visit Done → Budget Range Agreed → LOI Signed → Contract Signed).

7. **Share with Mike**
   `File → Share`. Add `mbiviano@hotmail.com` as Viewer. Copy the shareable link.

8. **Drop the link in Basecamp**
   Post it to the BMB Basecamp project so Mike has it bookmarked. Optional but recommended.

## Re-running manually

Open Apps Script → pick `refreshScorecard` from the function dropdown → Run. Or wait for the daily 6am trigger.

## Updating the API key later

`Project Settings → Script properties → edit `GHL_API_KEY`. No code change needed.
