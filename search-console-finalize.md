---
name: Search Console finalize — verify property, submit sitemap, monitor
created: 2026-06-09
status: ready-to-execute
owner: Spencer
related:
  - sitemap.xml
  - robots.txt
  - ga4-search-console-walkthrough.md
  - google-ads-campaign-blueprint.md
---

# Search Console — Finalize for the Google Paid Launch

**Goal:** Get `bivianomodularbuilders.com` verified in Google Search Console (GSC), submit the
refreshed `sitemap.xml`, and confirm the 4 paid-funnel pages stay out of the organic index while
remaining fully crawlable for Google Ads landing-page checks.

**What changed today (2026-06-09):**
- `sitemap.xml` refreshed — `lastmod` bumped to `2026-06-09` on all 22 organic URLs.
- `sitemap.xml` confirmed to contain **only** the 22 real SEO pages (home, why-modular, process,
  pricing, gallery, adu, 8 towns, 8 town/adu). Validated well-formed (`xmllint`), serves HTTP 200 locally.
- The 4 paid-funnel pages — `/free-consultation/`, `/booking/`, `/thank-you/`, `/booking-confirmed/`
  — are **deliberately NOT in the sitemap** and are kept out of organic via page-level
  `<meta name="robots" content="noindex,follow">`.
- `robots.txt` kept at `Allow: /` (full crawl). A comment block documents *why* we do not Disallow
  the funnel pages.

**Total UI time:** ~8-10 minutes (most of it is verify + submit; the rest is one-time monitoring setup).

---

## Why the funnel pages are noindex-but-crawlable (read once, then trust it)

Paid landing pages should not compete in organic search (thin, message-matched, duplicative), so they
carry an in-page `noindex,follow`. But they must stay **crawlable**:

- Google Ads evaluates **landing-page experience** (a Quality Score input) by fetching and rendering
  the actual page. If `robots.txt` Disallowed these paths, Google's crawler couldn't render them →
  risk of "destination not working / low landing-page experience" flags and higher CPCs.
- A `robots.txt` Disallow also does **not** reliably de-index — Google can still index a
  Disallowed URL it discovers via links, and because it's blocked it can't even *see* the noindex tag.
- Correct lever: **page-level `noindex`** (Google must crawl the page to read it — which `Allow: /`
  permits) + **omission from the sitemap**. That keeps them out of organic without hurting Ads.

Net: do **not** add a `Disallow` for the funnel paths. Leave `robots.txt` as-is.

---

## Part 1 — Confirm GA4 is firing (prereq for one-click verification) — 2 min

GA-based GSC verification only works if GA4 is live and you're signed in with the account that owns it.

1. Open Chrome **incognito** (rules out ad blockers).
2. Tab A: https://www.bivianomodularbuilders.com
3. Tab B: https://analytics.google.com → **Reports → Realtime**.
4. Confirm the property selector reads **Biviano Modular Builders** (NOT "Biviano Contracting"),
   property ID `G-GW5Z0VVDEC`.
5. You should see **1 active user** within 30-90s. Click home → /pricing/ → /why-modular/ and watch
   "Users by page title" update.
6. If Realtime stays empty after 90s: hard-refresh (`Cmd+Shift+R`); DevTools → Network → filter
   `google` → confirm both `gtag/js?id=G-GW5Z0VVDEC` and `g/collect?...` fire. If they fire but
   Realtime is empty, you're on the wrong GA4 property. If nothing fires, an ad blocker is the cause —
   test from a phone on cellular.

---

## Part 2 — Verify the GSC property — 3 min

**Use the `www` URL-prefix property** so it matches the sitemap host. All 22 `<loc>` URLs use the
`www` host; a URL-prefix property treats apex and `www` as different sites, so an apex property would
throw "URLs not under property" warnings against this sitemap.

1. https://search.google.com/search-console → top-left dropdown → **Add property**.
2. Choose **URL prefix** → enter exactly `https://www.bivianomodularbuilders.com/` → **Continue**.
3. **Verify ownership → Google Analytics** method → **Verify**. (Works because you own GA4
   `G-GW5Z0VVDEC` on the same Google account.)
4. If GA verification fails, fall back to **HTML tag** (paste a `<meta>` into the homepage `<head>` —
   flag to the dev to add it) or **DNS TXT** at the registrar.

> **Optional, cleaner long-term:** also add a **Domain property** (`bivianomodularbuilders.com`) which
> covers apex + `www` + all subdomains in one. It requires **DNS TXT** verification (no one-click GA
> method). For launch speed the `www` URL-prefix above is sufficient; add the Domain property later
> if you want apex+www unified reporting.

---

## Part 3 — Submit the sitemap — 1 min

1. In the **`www` URL-prefix property** → left sidebar → **Sitemaps**.
2. Under "Add a new sitemap" enter `sitemap.xml` → **Submit**.
3. Status should read **Success** within seconds. **Discovered URLs: 22.**
   - If it reads anything other than 22, re-check that the deploy is live (the lastmod should be
     `2026-06-09`) and that you're in the `www` property.

---

## Part 4 — Confirm funnel pages are correctly excluded — 2 min

Do this **after the funnel pages are deployed** (they're built by sibling agents; confirm they're live first).

1. **URL Inspection** (top search bar in GSC) for each:
   - `https://www.bivianomodularbuilders.com/free-consultation/`
   - `https://www.bivianomodularbuilders.com/booking/`
   - `https://www.bivianomodularbuilders.com/thank-you/`
   - `https://www.bivianomodularbuilders.com/booking-confirmed/`
2. For each, expect: **"URL is on Google" = No** (or "Excluded by 'noindex' tag" once crawled), and
   under **Coverage** the page should be **crawlable / fetch allowed** (robots.txt = Allowed).
   - "Excluded by noindex tag" is the CORRECT, desired state — not an error.
   - If a funnel page instead shows "Blocked by robots.txt," something added a Disallow — remove it.
3. Spot-check the live tags from a terminal once deployed:
   ```
   curl -s https://www.bivianomodularbuilders.com/free-consultation/ | grep -i 'name="robots"'
   # expect: <meta name="robots" content="noindex,follow">
   curl -s https://www.bivianomodularbuilders.com/robots.txt
   # expect: Allow: /   and NO Disallow lines for the funnel paths
   ```
4. (Optional) In GSC → **Settings → robots.txt** → confirm the live `robots.txt` is fetched, returns
   200, and has no funnel Disallows.

---

## Part 5 — Link GA4 ↔ Search Console (5 min, recommended)

So organic query data shows up alongside GA4 behavior reports:

1. GA4 → **Admin** → (Property column) **Search Console links** → **Link**.
2. Pick the `bivianomodularbuilders.com` GSC property you just verified → choose a **Web stream** →
   **Submit**.
3. After ~48h, GA4 → **Reports → Search Console** collection populates (you may need to publish the
   Search Console report collection from the Library the first time).

*(Separate from the Google Ads ↔ GA4 link, which the conversion-tracking agent owns. Both should
exist before scaling spend.)*

---

## Done state

- [ ] GA4 Realtime confirmed firing on the live site (`G-GW5Z0VVDEC`).
- [ ] `www` URL-prefix property added + verified in GSC.
- [ ] `sitemap.xml` submitted → **Success**, **22 discovered URLs**.
- [ ] All 4 funnel pages inspect as **Excluded by noindex** AND **crawl-Allowed** (not robots-blocked).
- [ ] GA4 ↔ Search Console link created.

---

## What to monitor (first 30 days, then monthly)

**Weekly for the first month:**
- **Pages → Indexing report:** organic page count should climb toward **22 indexed**. Investigate any
  "Discovered – currently not indexed" or "Crawled – not indexed" on the 22 real pages.
- **Funnel pages must stay "Excluded by noindex tag"** — if any of the 4 flips to "Indexed," the
  noindex tag was dropped in a deploy. Re-add it.
- **Sitemaps tab:** status stays **Success**; couldn't-fetch or parse errors mean a bad deploy.
- **Page experience / Core Web Vitals:** watch the town pages and funnel LPs — slow LPs hurt both SEO
  and Google Ads Quality Score.

**Monthly:**
- **Performance report:** track impressions/clicks/avg-position for the town + town/adu keyword
  clusters (cross-ref `keyword-map-modular-southshore.md`). This is the organic complement to the
  paid Search campaign.
- **Manual Actions / Security Issues:** should stay empty.
- **Links report:** sanity-check inbound/internal links.
- Re-bump sitemap `lastmod` whenever real SEO pages get a content refresh, then resubmit (or just let
  Google re-crawl — resubmit only after meaningful changes).

**Tie-in to paid:** the funnel pages will get traffic from Google Ads but should generate **zero**
organic impressions in the Performance report. If they start showing organic impressions/clicks,
the noindex isn't being honored — fix before it dilutes the brand's organic footprint.
