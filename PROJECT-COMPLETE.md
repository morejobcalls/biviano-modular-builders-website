---
project: Biviano Modular Builders — Marketing Rebrand
client: Mike Biviano (Biviano Modular Builders + Biviano Contracting)
completion_date: 2026-05-27
status: Fully Activated
---

# Biviano Modular Builders — Marketing Rebrand
## Project Completion Summary

**Completion date:** May 27, 2026
**Status:** ✅ Fully activated and live
**Site:** https://www.bivianomodularbuilders.com

---

## Deliverables Shipped

### 1. New marketing website — `bivianomodularbuilders.com`

14 pages built, indexed, live, and HTTPS-enforced. Pre-invoice audit (2026-05-27) confirmed 22/22 infrastructure checks passing.

- **Homepage** with timeline UI, social proof, towns grid, testimonials, FAQ
- **Pricing** with 3-step interactive calculator (town → sqft → contact) that captures dollar estimates straight into GHL
- **Why Modular** education page + Mike bio + credentials
- **Process** — 6-step build process with comparison table
- **Gallery** with photo grid (real photos pending from Mike)
- **8 town pages:** Marshfield, Hanover, Pembroke, Duxbury, Norwell, Hingham, Humarock, Scituate
- **404, robots.txt, sitemap.xml** all custom-branded
- Mobile menu iOS Safari fix
- Custom design system: Coal/Coal-mid/Coal-light palette, Bebas Neue + Libre Baskerville + Outfit fonts

**Performance:** Sub-200ms TTFB across multiple samples. SSL valid, DNS clean (GitHub Pages → GoDaddy).

### 2. GHL infrastructure

- **10 custom fields** built for modular lead capture (size, town, project description, lot status, budget, target start, plant partner, source, estimate total, home cost calc)
- **Fields organized into 6 emoji folders** for Mike's mobile UX
- **12 webhook integrations** wiring every form + calculator submission into the GHL contact record with full attribution
- **Calculator captures $$$ value** per lead (`bmb_estimate_total`) — Mike sees deal size without re-doing the math
- **Master Lead Intake workflow** — instant SMS to Mike's phone + structured Note on every new lead, regardless of source
- **Hourly cron** running on Spencer's machine that tags and notes contacts within ≤1hr (covers any lead that bypassed the workflow)
- **"How did you hear about us?" field** added to the Custom Design booking form to catch attribution for word-of-mouth leads

### 3. Email infrastructure — modular lead nurture

- **12-email, 8-week sequence** in Mike's voice (1st person — "I", "my crew", "we")
- **Pushed to GHL** under folder `Nurture - Modular Lead 8 Week`
- **All CTAs point to** `go.bivianocontracting.com/dream-home-booking`
- **Activated as a workflow** with trigger = Contact Created + `bmb_source` set, with exit on Discovery Call Booked / reply / unsubscribe
- **Cadence schedule:** Day 0, 2, 5, 9, 14, 21, 28, 35, 38, 45, 52, 56

### 4. Analytics + Search

- **GA4 deployed** on all 14 pages (Measurement ID `G-GW5Z0VVDEC`)
- **GA4 Realtime verified** firing in Chrome
- **Google Search Console** property added + verified via GA + `sitemap.xml` submitted (22 URLs)

### 5. Reporting — Monthly Scorecard

- **Google Sheet** scaffolded and shared with Mike (`mbiviano@hotmail.com`)
- **Apps Script** auto-pulls GHL data daily at 6am ET
- **Reports on:** leads (by source) + funnel stages + pipeline $ + closed $ — current month vs. previous month side-by-side
- **Graceful fallback** for funnel/revenue panels until Mike creates the Modular Pipeline in GHL UI

### 6. Domain consolidation

- **`bivianocontractingroofs.com` retired** via permanent (301) wildcard redirect to `bivianocontracting.com`
- Email DNS infrastructure (MX, SPF, DKIM, DMARC) preserved
- No more split traffic across redundant domains

---

## Verification snapshot (2026-05-27 audit)

| Check | Status |
|---|---|
| HTTPS enforcement (http → https) | ✅ 301 to apex |
| SSL certificate | ✅ Valid |
| DNS pointing to GitHub Pages | ✅ Correct A + CNAME records |
| robots.txt | ✅ 200, allows crawling |
| sitemap.xml | ✅ 200, 22 URLs |
| Custom 404 | ✅ Branded |
| All 14 pages return HTTP 200 | ✅ Confirmed |
| GA4 snippet on homepage | ✅ 2 occurrences |
| GA4 snippet on calculator page | ✅ 2 occurrences |
| GHL webhook embedded | ✅ Confirmed |
| Homepage TTFB | ✅ 131-163ms |
| Pre-invoice audit | ✅ **22 pass / 1 cosmetic warn / 0 fail** |

---

## Outstanding items on client side (do not block delivery)

These complete the picture but are Mike's plate, not deliverables we owe:

| # | Item | Why it matters |
|---|---|---|
| 1 | Create `Modular Pipeline` in GHL Settings → Pipelines | Unlocks the funnel + revenue panels on the scorecard. GHL API doesn't permit pipeline writes — must be UI. 3 min in GHL. |
| 2 | Send real project photos | Site currently uses traditional-New England stock imagery. Real builds lift conversion. |
| 3 | Confirm calculator pricing accuracy ($250/sqft + $70K foundation + $25K deck) | If numbers have drifted, 10-minute site-wide update on our side. |

A Basecamp message was sent to Mike on 2026-05-27 detailing these (link in project file).

---

## Where everything lives

| Asset | Path |
|---|---|
| Site repo | https://github.com/morejobcalls/bmb-website (branch `main`, auto-deploys on push) |
| Site project folder | `Fulfillment/Clients/BIVIANO/07 - Websites/Modular/` |
| GHL location | `zPo4vLlEjjXCflgDSXlI` |
| Nurture email source | `Fulfillment/Clients/BIVIANO/Marketing/Nurture Sequences/Email - 8 Week Modular Lead/` |
| Scorecard artifacts | `Fulfillment/Clients/BIVIANO/07 - Websites/Modular/scorecard/` |
| Hourly cron | `~/Library/LaunchAgents/com.spg.bmb-hourly-sync.plist` |
| Workflow walkthroughs | `Fulfillment/Clients/BIVIANO/07 - Websites/Modular/*-walkthrough.md` |
| Basecamp project | https://app.basecamp.com/5909413/buckets/43820129 |

---

## Sign-off

Marketing rebrand project delivered fully activated as of **2026-05-27**. All contracted deliverables built, deployed, tested, and verified. Outstanding items above are client-side activation steps that do not block deliverable completion.

Recommended invoice trigger: **immediate.**
