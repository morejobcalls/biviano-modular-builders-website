# SEO Content Engine — Biviano Modular Builders

The repeatable workflow for adding optimized pages to bivianomodularbuilders.com (the video's "/blogpost skill" equivalent). One page ≈ one short Claude Code session.

## To generate a new page
Prompt Claude Code from this repo folder:

> Read `seo-page-generation-facts.md` and the `reference/` voice files. Pick the next unbuilt keyword from `keyword-map-modular-southshore.md` that is NOT in the Page Log below (never duplicate a keyword — cannibalization). Use the matching exemplar: town page → `scituate/index.html` · ADU → `marshfield/adu/index.html` · article/guide → `marshfield/modular-vs-stick-built/index.html`. Research the top 3 Google results for the keyword and match/beat their average word count, H2 count, and image count. Build the page with: 1 primary + 4–5 secondary keywords, town-genuine content (no near-duplicate paragraphs vs sibling pages), Article/LocalBusiness + FAQPage + BreadcrumbList JSON-LD, internal links per the facts doc, 1–3 authoritative external links, the standard CTA form. Then: add the URL to `sitemap.xml`, add the page to the towns strip/footers where relevant, log it in the Page Log, and run a Lighthouse mobile check (target ≥90).

## Launch-state inventory (2026-06-10 build)
- 14 town pages (8 Tier-1 + Cohasset, Hull, Kingston, Plymouth, Hanson, Halifax) + 14 ADU pages
- 8 town comparison articles `/[town]/modular-vs-stick-built/` + 1 state pillar `/modular-vs-stick-built/`
- `/financing/` + 8 `/guides/*` informational pages
- Core: home, why-modular, process, pricing, gallery, adu
- Noindexed utility: funnel pages + `/feedback/`

## Expansion queue — REVISED 2026-06-10 from Semrush validation (3 rounds, MA-localized; raw lists in semrush-*-list.txt)
Ranked by volume ÷ difficulty. The big learning: style/size/ADU content has 10–100x the volume of town keywords; town demand flows through "near me" + map pack (= the GBP).
1. **Style pages:** modular ranch homes (1,300/mo), modular farmhouse (1,000 KD12), modular cape cod homes (260 KD0), modular beach house (170 KD3)
2. **ADU content cluster:** granny pod (6,600!), prefab adu (5,400 KD~23), adu floor plans (1,900 KD21), backyard adu (1,600), granny flat + cost (2,900 + 170 KD4), size pages 400/600/800/900 sq ft adu (110–260 each, KD 1–12), adu cost guide (cost-to-build 170 KD10, cost/sq ft 110 KD9)
3. **Size pages:** 2 bedroom modular homes (880 KD29), 3 bedroom modular homes (480 KD18)
4. **High-value guides:** second story addition cost (1,300 KD13), manufactured vs modular home (880 KD30 — dedicated guide), build a house on my land (480 KD9), modular garage with apartment (480 KD11), cost to build a 2000 sq ft house (320 KD16) / cost to build a house in massachusetts (70)
5. Tier-2 town comparison articles + Tier-3 towns — AFTER the above; town keywords showed ~0 Semrush volume (they convert via maps/near-me, pages support relevance + landing quality)
6. Re-validate with Search Console real-query data once verified (beats Semrush estimates)
**Deprioritized by data:** land-for-sale adjacent content (20/mo), county/south-shore-modified builder terms (0–20/mo).

## Rules that never bend
- One primary keyword = one page, forever
- Real numbers from `reference/business-context.md` only
- Mike's residency/inspector claims: Marshfield ONLY
- New pages → sitemap.xml + Page Log, same session
- Thin-content check: if a new page would share >30% of its copy with a sibling, differentiate or don't build it

## Page Log
| Date | URL | Primary keyword |
|---|---|---|
| pre-2026-06-10 | / + core pages + 8 town + 8 ADU | per keyword map |
| 2026-06-10 | 30 new pages (see inventory above) | per keyword map |
