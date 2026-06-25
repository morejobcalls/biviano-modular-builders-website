# BMB Review Farming — GHL Build Instructions (v2, full system)
Updated 2026-06-10. Sub-account: Biviano (`zPo4vLlEjjXCflgDSXlI`). Master SOP: `Fulfillment/Operations/SOPs/review-farming-system.md`.

## ✅ Pre-staged via API (done — nothing to create here)
| Asset | Detail |
|---|---|
| Custom value | `BMB Google Review Link` = PENDING → `{{ custom_values.bmb_google_review_link }}` |
| Custom value | `BMB Feedback Page URL` = https://www.bivianomodularbuilders.com/feedback/ → `{{ custom_values.bmb_feedback_page_url }}` |
| Email template | **BMB — Reviews 1 — How Did We Do (Day 2)** → feedback page |
| Email template | **BMB — Reviews 2 — Make It Public (High Score)** → Google link + guided questions |
| Email template | **BMB — Reviews 3 — Direct Ask (Day 10)** → Google link + guided questions |
| Email template | **BMB — Reviews 4 — Last Call (Day 21)** → Google link |
| | (all in email folder **Modular \| Reviews**) |
| Feedback page | LIVE at /feedback/ — tags `bmb-feedback-low` (≤3) / `bmb-feedback-high` (≥4); high scorers see guided questions + review button |
| Tags in play | `bmb-feedback-low` · `bmb-feedback-high` · `bmb-project-complete` (you create) · `google-review-left` (you create) |

---

## WF1 — "BMB — Feedback Triage" (PUBLISH immediately)
AI builder prompt:
> When the tag "bmb-feedback-low" is added to a contact, send an internal notification email to the team, then create a task assigned to Mike Biviano due in 1 day reminding him to call the contact about their low feedback score.

Verify after generation:
- Trigger: Contact Tag → Added → `bmb-feedback-low`
- Internal Notification → Email → recipients: Spencer + Mike → subject `⚠️ Low BMB feedback — call within 24h` → body:
```
{{contact.name}} left a low score on the feedback page.
Phone: {{contact.phone}}
What they said: {{contact.bmb_project_description}}
A fast personal call from Mike usually saves the relationship — and the review.
```
- Task: `Call re: low feedback — {{contact.name}}` → Mike → due 1 day
- **Add one more action:** Remove From Workflow → "BMB — Review Chase" (never chase an unhappy customer toward Google)

## WF2 — "BMB — Review Chase" (build now, PUBLISH when review link is real)
AI builder prompt:
> When the tag "bmb-project-complete" is added to a contact, send an SMS, then wait 2 days and send an email, then wait 4 days and send another SMS, then wait 4 days and send an email, then wait 11 days and send a final email.

Map each node:
1. Trigger: Contact Tag → Added → `bmb-project-complete` (create the tag)
2. **SMS 1 (Day 0)** — paste:
```
Hey {{contact.first_name}} — Mike here. It was a pleasure building your home. Quick favor: 60 seconds, how did we do? {{ custom_values.bmb_feedback_page_url }} Your honest answer goes straight to me, not a call center. — Mike
```
3. Wait 2 days → **Email** → template **BMB — Reviews 1 — How Did We Do (Day 2)** · From Name `Mike Biviano`
4. Wait 4 days → **SMS 2 (Day 6)** — paste:
```
Hey {{contact.first_name}}, Mike again. If you've got 30 seconds, a quick Google review helps the next South Shore family find us: {{ custom_values.bmb_google_review_link }} It means the world to a 4th-generation family business. — Mike
```
5. Wait 4 days → **Email** → template **BMB — Reviews 3 — Direct Ask (Day 10)**
6. Wait 11 days → **Email** → template **BMB — Reviews 4 — Last Call (Day 21)**
7. Settings: Allow re-entry = OFF.
8. **Save UNPUBLISHED** until the Google link is real.

## WF3 — "BMB — Make It Public" (build now, PUBLISH with WF2)
AI builder prompt:
> When the tag "bmb-feedback-high" is added to a contact, wait 1 day, then if the contact does not have the tag "google-review-left", send an email.

Map:
- Trigger: tag Added → `bmb-feedback-high`
- Wait 1 day → If/Else: contact tag DOES NOT include `google-review-left` → **Email** → template **BMB — Reviews 2 — Make It Public (High Score)**
- Save unpublished until link is real.

## WF4 — "BMB — Review Received / Exit" (PUBLISH immediately)
AI builder prompt:
> When the tag "google-review-left" is added to a contact, remove them from the workflow "BMB — Review Chase" and remove them from the workflow "BMB — Make It Public".

Optional extra action: SMS from Mike — `Just saw your review, {{contact.first_name}} — thank you. Means a lot. — Mike`

## WF5 — Detection (after GBP is live + connected)
1. Settings → **Reputation Management** → connect the BMB Google Business Profile (needs Mike's Google auth once)
2. New workflow → Trigger: **Review Received** (filter: rating ≥ 4 if offered) → Action: Add tag `google-review-left`
   - GHL fuzzy-matches the reviewer name to a contact; matched = automatic exit from the chase via WF4
3. Weekly 2-min sweep (until volume justifies more): open Reputation → new reviews → any reviewer not auto-matched → find contact → add `google-review-left` manually

## 🚀 Go-live sequence (the moment Mike texts the g.page review link)
1. Update custom value `BMB Google Review Link`: PENDING → real link (Claude does via API, or Settings → Custom Values)
2. Claude swaps `REVIEW_LINK_PLACEHOLDER` in site `/feedback/index.html` + pushes
3. Publish WF2 + WF3
4. Connect Reputation Management + build WF5
5. Seed: batch-text the last 5–10 happy completed clients the direct link
6. From then on: **job finishes → add tag `bmb-project-complete` → machine runs itself**

## Test plan (say "workflows built")
Claude fires a 2/5 score through the live /feedback/ page → expect WF1 internal email + Mike task within ~1 min. Then a 5/5 score → expect `bmb-feedback-high` tag + WF3 queue (email won't send while unpublished — verified in the contact's workflow tab).
