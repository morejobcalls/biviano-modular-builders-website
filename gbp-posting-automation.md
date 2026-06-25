# GBP Posting Automation — Biviano Modular Builders

**Purpose:** keep the BMB Google Business Profile posting 1–2×/week on autopilot (recency is a 2026 local-pack signal; 3 months of silence flags the profile as inactive).
**Status:** STAGED — connects the day the GBP exists (see `google-business-profile-kit.md` §12 + PICKUP-google-leadgen #2).
**Pipeline:** Claude (writes post in Mike's voice) → Make.com webhook → Google Business Profile.

---

## Why Make.com and not the GBP API directly
Google's Business Profile API requires an approval that takes up to ~14 days. Make.com's native GBP connection works the day the profile is verified. Start with Make; migrate to the API later only if volume demands it.

## One-time setup (≈15 min, after GBP is live)
1. make.com → new scenario: **Webhooks (Custom webhook) → Google My Business "Create a Post"**.
2. Connect the Google account that owns the BMB profile; select the BMB location.
3. Map webhook fields → post fields:
   - `summary` → post body
   - `cta_type` (LEARN_MORE / BOOK / CALL) → call-to-action button
   - `cta_url` → button link
   - `image_url` → post photo (must be a public URL — use images already hosted on bivianomodularbuilders.com, e.g. `/photos/gallery/...`)
4. Copy the webhook URL → store in `Clients/BIVIANO/env/.env` as `BMB_GBP_POST_WEBHOOK`.
5. Click "Run once" in Make, send a test payload, confirm the post appears, then schedule the scenario "immediately on data arrival."

Test payload:
```bash
curl -X POST "$BMB_GBP_POST_WEBHOOK" -H "Content-Type: application/json" -d '{
  "summary": "TEST — delete me.",
  "cta_type": "LEARN_MORE",
  "cta_url": "https://bivianomodularbuilders.com/",
  "image_url": "https://bivianomodularbuilders.com/hero-home.jpg"
}'
```

## Generating posts (the repeatable Claude workflow)
From the repo folder, prompt Claude Code:

> Read `reference/tone.md`, `reference/vocabulary.md`, `reference/beliefs.md`, `reference/business-context.md`. Write 1 Google Business Profile post (≤1,500 chars, hook in the first line — only ~1 line shows before "more"). Rotate type: offer → educational → proof/set-day → cost → trust (see the 5 exemplars in `google-business-profile-kit.md` §7). Use canonical numbers only. One CTA button. Then POST it as JSON to the Make webhook in .env (`BMB_GBP_POST_WEBHOOK`) with summary/cta_type/cta_url/image_url.

Rules:
- Photos: REAL BMB photos only (site-hosted gallery/set-day shots). Never stock. AI-generated images are a last resort and never for project "proof."
- Keyword-matching posts can earn the yellow query badge on Maps — work one natural phrase per post ("modular home builder South Shore", "modular ADU", a town name).
- Log each post (date + hook + type) at the bottom of this file to avoid repeats and keep the rotation honest.

## Cadence
- 1–2 posts/week, sustained. Batch-write 4 at a time if easier; Make can also schedule.
- 3–5 fresh photos/week uploaded to the profile (separate from posts — Mike's set-day shots).
- This pairs with the review cadence in `reviews-engine-setup.md` (2–4 fresh Google reviews/month).

## Post log
| Date | Type | Hook | |
|---|---|---|---|
| — | — | (log starts at GBP go-live) | |
