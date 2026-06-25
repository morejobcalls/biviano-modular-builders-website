# Reviews Engine — Biviano Modular Builders

**Goal:** ≥10 Google reviews fast, then steady velocity (2–4 fresh/month — recency now outranks raw count), every review answered within 48h, and zero bad surprises on the public profile.
**Stack:** /feedback/ page on bivianomodularbuilders.com + GHL workflows (location `zPo4vLlEjjXCflgDSXlI`).
**Status:** page BUILT (this repo, `/feedback/`); GHL workflows = build steps below; Google review link = placeholder until the GBP exists.

---

## ⚠️ Compliance note (deliberate deviation from the source video)
The Jono Catliff video teaches a review **gate**: 1–3 stars get diverted to a private form, only 4–5 stars are shown the Google link. **Do not build that.** Google's review policy explicitly prohibits review-gating, and the FTC's 2024 rule on consumer reviews bans suppressing negative ones — both can nuke the profile we're trying to build. The BMB GBP kit (§9) already says the same.

**What we build instead (keeps the upside, drops the violation):**
- EVERY respondent sees the Google review link on the thank-you screen — no gating.
- Low scores (1–3) ALSO fire an instant internal alert to Mike/Spencer so the problem gets a phone call within hours — most upset customers who get a fast, human call never post the 1-star. Service recovery, not suppression.

## Part 1 — The ask (GHL workflow: "BMB — Review Request")
Trigger: pipeline stage = **Project Complete / Move-In** (or tag `bmb-project-complete`).
1. **Day 0 — SMS from Mike's number:**
   > "Hey {{contact.first_name}} — Mike here. It was a pleasure building your home. If you've got 30 seconds, a quick Google review means the world to a family business like ours: {{REVIEW_LINK}} Thank you! — Mike Biviano"
2. **Day 2 — email if no review** (manual check or Birdeye signal): same link, one photo of *their* finished home.
3. **In-person:** Mike asks at final walkthrough + "I'll text you the link." Highest-converting combo.
4. Optional softer route: send `/feedback/` instead of the raw review link when the project had friction — Mike hears about problems first, and the happy majority still lands on Google (link is shown to everyone).

`{{REVIEW_LINK}}` = GBP dashboard → "Ask for reviews" → short link (`https://g.page/r/...`). Exists only after the profile is verified. Store as a GHL custom value `bmb_google_review_link` so every workflow/template updates in one place.

**Launch seed:** before paid traffic goes live, batch-text the last 5–10 happy completed clients the link (recency lift on day one). Ask everyone, not just the happy ones.

## Part 2 — The /feedback/ page (BUILT)
- URL: `https://bivianomodularbuilders.com/feedback/` — noindexed (robots meta + excluded from sitemap).
- 1–5 "how was your experience" + optional comment + name. Posts to the BMB GHL webhook with `bmb_source: 'Feedback page'`, tags `bmb-feedback` + `bmb-feedback-low` (≤3) or `bmb-feedback-high` (≥4), and the score+comment in `bmb_project_description`.
- Thank-you state shows the Google review button to ALL scores (button href = `REVIEW_LINK_PLACEHOLDER` — swap to the real g.page link at GBP go-live; until then it falls back to the site home).

## Part 3 — GHL workflow: "BMB — Feedback Triage"
Trigger: inbound webhook contact tagged `bmb-feedback-low`.
1. **Internal notification** (Internal Notification action — NOT SMS-to-contact) to Mike + Spencer: "⚠️ Low feedback ({{score}}) from {{name}} — {{comment}} — call within 24h: {{phone}}".
2. Task assigned to Mike, due 24h.
3. NO automated reply to the customer beyond a neutral "thanks, Mike will call you" — never an AI apology.
Tagged `bmb-feedback-high`: optional thank-you SMS; the page already showed them the review link.

## Part 4 — Respond to every review
- 5★: "Thank you, [Name] — it was a privilege to build your home in [Town]. Enjoy every minute of it. — Mike & the Biviano team." (Work the town/keyword in naturally; vary wording.)
- 1–3★: NEVER auto-reply, NEVER argue: "Thanks for the honest feedback, [Name]. This isn't the experience we want anyone to have — I'd like to make it right. Please call me directly at (617) 678-6446. — Mike Biviano"
- Make.com auto-reply scenario (per the video) is OPTIONAL for 4–5★ only, drafted from `reference/` voice files; manual is fine at current volume.

## Targets
10 reviews minimum (escape the no-show zone) → then 2–4/month sustained. A 4.7–4.9 average converts better than a suspicious 5.0 — don't sweat the occasional 4★.
