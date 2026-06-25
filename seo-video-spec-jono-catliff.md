# Source Spec — "Claude Code Local SEO" (Jono Catliff)

Video: https://youtu.be/BTnU_cCx36Y (~70 min, extracted 2026-06-10). This is the methodology the 2026-06-10 BMB SEO build implements. Where BMB's implementation deviates, the deviation + reason is noted ⚠️.

## The system (4 parts)
1. **AI-optimized Google Business Profile** — categories + services + service areas + reviews = ~80% of GBP local SEO. Goal = top-3 map pack (~50% of map clicks).
2. **Automated GBP posting** — Claude writes → Make.com webhook → GBP. Converts profile views to clicks; keyword posts earn the Maps yellow badge; 3 months silent = inactive flag.
3. **Review engine** — minimum 10 reviews, then VELOCITY (~8/mo per video; BMB targets 2–4/mo realistic for big-ticket builds). 4.7–4.9 avg more trusted than 5.0. ⚠️ Video teaches a review GATE (1–3★ diverted, 4–5★ to Google) — **NOT implemented**: violates Google review policy + FTC 2024 rule. BMB version: everyone gets the review link; ≤3 scores ALSO fire an instant private alert to Mike (service recovery). See `reviews-engine-setup.md`.
4. **Programmatic local pages** — `[service] × [city]` matrix (10–400 pages; BMB launch ≈ 52) + city-appended blog/guide content, each on-page optimized + Lighthouse-iterated. MUST be static (SSG) — BMB is static HTML on GitHub Pages ✅.

## Key numbers from the video
- #1 organic ≈ 30% of clicks; #10 ≈ 2.4%; map top-3 ≈ 50% of map clicks
- GBP: 1 primary + 9 secondary categories (use all 10 if legit) · 30–50 services (Semrush-validated, skip zero-volume) · up to 20 service areas, ≤2hr drive rule · 100+ real photos (claimed +520% calls; NEVER stock) · accurate hours
- Citations: Yelp/Facebook/Bing/BBB/YellowPages, byte-identical NAP
- Keyword research: Semrush Keyword Magic — money pages sorted by CPC desc; blog topics sorted by volume, ALWAYS city-appended
- Each page: 1 primary + 4–5 secondary keyword cluster; never two pages for the same keyword (cannibalization)
- Competitor reverse-engineering: average word count / H2 count / image count of the top-3 ranking pages per keyword
- Technical: Lighthouse (DevTools, ALWAYS mobile) → paste full report to Claude → iterate toward ~100
- Voice files (tone/vocabulary/beliefs/humor/business-context from real writing samples) on EVERY content generation — engagement signals (dwell/bounce) are what actually rank; "AI slop" fails regardless of optimization

## Warnings adopted
No fake categories/services/areas (BS test) · no stock photos on GBP · thin-content guard above ~400 pages · never auto-reply to 1–3★ reviews · CSR never ranks, SSG mandatory · review velocity > bulk · GBP suspension traps (PO boxes, duplicate NAP at same address — see kit §0).

## BMB implementation map
| Video phase | BMB artifact |
|---|---|
| GBP setup + optimization | `google-business-profile-kit.md` (incl. §13 services-expansion addendum) |
| Voice/reference files | `reference/tone.md, vocabulary.md, beliefs.md, business-context.md` |
| GBP posting automation | `gbp-posting-automation.md` (Make.com pipeline, staged) |
| Review engine | `reviews-engine-setup.md` + `/feedback/` page (compliant variant) |
| Service×city pages + blogs | town pages, `/[town]/adu/`, `/[town]/modular-vs-stick-built/`, `/modular-vs-stick-built/`, `/financing/`, `/guides/*` |
| Repeatable "skill" | `seo-content-engine.md` + `seo-page-generation-facts.md` |
| Keyword research | `keyword-map-modular-southshore.md` (intent-rated; Semrush trial validates) |
| Deployment | GitHub Pages (already live) ✅ |

Full transcript (if ever needed): re-pull captions from the YouTube URL with yt-dlp.
