# BMB SEO Build — Shared Facts & Conventions (read fully before writing any page)

## Repo + exemplars (READ these, do not modify them)
- Repo root: `/Volumes/T7/SPG/3. FULFILLMENT/Clients/BIVIANO/07 - Websites/Modular/`
- Town page exemplar: `scituate/index.html` (clone structure for new town pages)
- ADU page exemplar: `marshfield/adu/index.html`
- Article exemplar: `/tmp/bmb-build/out/marshfield/modular-vs-stick-built/index.html` (clone structure for articles/guides)
- Shared stylesheet: `towns.css` at site root (link as `../towns.css` from depth-1, `../../towns.css` from depth-2)
- Design system + tone: repo `CLAUDE.md` (colors, fonts, tone — DO NOT deviate)

## Output location (agents CANNOT write to the repo — write here)
`/tmp/bmb-build/out/<url-path>/index.html` — e.g. `/tmp/bmb-build/out/cohasset/index.html`, `/tmp/bmb-build/out/guides/what-is-a-modular-home/index.html`

## Business facts (use exactly — never invent numbers)
- Brand: Biviano Modular Builders (BMB), modular brand of Biviano General Contracting LLC
- Mike Biviano Jr., 4th-generation contractor, lifelong Marshfield MA resident, family building on the South Shore since the 1960s, 40+ years
- Former Marshfield Planning Board Chair
- Address: 2183 Ocean Street, Marshfield, MA 02050 · Phone (617) 678-6446 · tel:+16176786446 · email mbiviano@hotmail.com
- Pitch: custom dream home in 8–12 weeks for ~25% less than stick-built
- $250/sq ft (BMB) vs $400–$600/sq ft stick-built locally → typical savings $200,000–$300,000
- Custom plans ~$2,500 with BMB vs $20,000–$30,000 traditional architect
- Stick-built timeline locally: 12–15 months; BMB: 8–12 weeks from groundbreaking (factory build + site prep run simultaneously)
- ADUs: 900 sq ft & under, same $250/sq ft, same 8–12 weeks
- Proof: 21 five-star reviews (Birdeye) · BuildZoom Score 101 (Top 12% of 139,240 MA licensed contractors) · MA CSL #CS-108728 · MA HIC Reg. #181337
- Free consultation: 60 min with Mike, full cost breakdown, 8 slots/month
- Avatar: married couple 35–55, $150K+ HH income, Plymouth County, quoted $1M+ stick-built, scared of 12+ month timeline, worried "modular = trailer", has land or close to buying

## Tone (from CLAUDE.md)
Direct, no-BS, human. Specific numbers always ("8–12 weeks", never "fast"). Never agency-speak. Write like a contractor-side partner. Address the "modular = trailer" stigma head-on with facts (built to MA state building code 780 CMR, same as stick-built; appraised and financed like site-built homes). Dry, light humor welcome; never hypey.

## Head boilerplate (every page, in this order)
1. GA4 + Google Ads gtag block (copy verbatim from scituate/index.html lines 4–12: `G-GW5Z0VVDEC` + `AW-16742219835`)
2. charset, viewport, favicons block, theme-color (copy verbatim)
3. `<title>` ≤60 chars: primary keyword + brand, e.g. `Modular vs Stick-Built in Scituate, MA | Biviano Modular Builders` (brand may be shortened to "Biviano Modular" if long)
4. meta description 140–160 chars, includes primary keyword + a number + CTA
5. canonical: `https://www.bivianomodularbuilders.com/<path>/` (always www, always trailing slash)
6. OG tags (title/description/url/type=article for articles, website for town pages/guides ok as article when editorial; image: reuse an existing site image URL from the exemplar)
7. Google Fonts links (verbatim from exemplar)
8. towns.css link (correct relative depth)
9. JSON-LD (see below)

## JSON-LD
- Town + ADU pages: LocalBusiness (copy marshfield pattern, swap locality/areaServed/wikipedia sameAs) + FAQPage matching the on-page FAQ
- Articles/guides: `Article` (headline, description, author = Person Mike Biviano, publisher Organization Biviano Modular Builders, mainEntityOfPage canonical) + FAQPage if the page has an FAQ + BreadcrumbList (Home › [Town] › Article, or Home › Guides › Article)

## Page structure
### New town pages (clone scituate exemplar exactly, swap content)
Sections in order: nav → mobile menu → hero (town breadcrumb) → cred bar (verbatim) → town intro (3 paragraphs, LOCAL) → why BMB 6 tiles (keep tiles, localize 1–2 mentions) → process 5 steps (keep, localize town name) → local FAQ (4 town-specific Q&As, mirrored in FAQPage JSON-LD) → ADU cross-link section (NOTE: use SINGLE braces `{` `}` in its inline CSS — the exemplar had a doubled-brace bug that is now fixed) → CTA form (verbatim, swap town references; form JS `'contact.bmb_source':'Town page'`) → towns strip (use the 14-town list below, mark current town `active`) → footer (verbatim) → JS block (verbatim)

### Articles / guides (clone the article exemplar structure)
nav → editorial hero (breadcrumb, eyebrow, H1 with primary keyword, sub) → article body (~1,400–2,000 words, 5–8 H2s, one comparison table where natural, specific local costs/math, pull quote from Mike in Libre Baskerville) → FAQ (3–4 Q&As + FAQPage JSON-LD) → CTA form section (same GHL form, `bmb_source`: 'Article') → towns strip → footer → JS

## Towns strip (14 towns — use on ALL new pages)
Marshfield, Scituate, Humarock, Duxbury, Hanover, Pembroke, Norwell, Hingham, Cohasset, Hull, Kingston, Plymouth, Hanson, Halifax — each linking `/<town>/` (root-relative OK in strip: use `/marshfield/` style absolute paths on new pages).

## Internal links (every page MUST include, naturally in body copy)
- Articles: its town page, `/pricing/`, `/financing/`, `/modular-vs-stick-built/` (pillar), `/process/`
- Town pages: `/why-modular/`, `/pricing/`, its `/[town]/adu/`, `/process/`
- Guides: `/modular-vs-stick-built/`, `/pricing/`, `/financing/`, ≥1 town page, `/process/`
Anchor text = descriptive ("what modular costs per square foot in Massachusetts"), never "click here".

## External links (1–3 per article/guide, rel="noopener", target="_blank")
Authoritative only: town .gov sites, mass.gov (780 CMR building code, ADU law), FEMA flood maps, registry of deeds. No competitors.

## On-page checklist (apply to every page)
- ONE H1 containing the primary keyword + town/state
- Primary keyword in title, H1, first 100 words, one H2, meta description, URL
- 4–5 secondary keywords from the cluster woven naturally (no stuffing)
- Images: descriptive alt with town/keyword where honest; loading="lazy" except hero (eager)
- No keyword cannibalization: each page targets its OWN primary keyword only — articles must NOT read like town pages
- Genuinely differentiated local content (zoning, geography, housing stock, flood zones, specific neighborhoods) — NO near-duplicate paragraphs between sibling pages

## Per-town local angles
**Tier 1 (articles):**
- Marshfield: Mike's hometown; coastal/flood zones (Brant Rock, Green Harbor, Ocean Bluff, Humarock line), conservation land, every inspector known personally
- Scituate: coastal, harbor town, flood-zone rebuilds, ledge, historic districts, teardown-rebuild demand
- Duxbury: affluent, large lots, historic character, Duxbury Beach, strict design expectations, $1M+ stick quotes common
- Pembroke: inland, ponds (Furnace/Oldham), more affordable lots, growing families, Route 3 commuters
- Norwell: wooded large lots, North River, septic/Title 5 considerations, high-end expectations
- Hanover: suburban, Route 53 corridor, established neighborhoods, teardown + infill lots
- Hingham: most affluent, harbor, historic districts, strict review, Boston commuter ferry, highest land costs
- Humarock: barrier-beach village of Scituate, FEMA velocity zones, elevated/pile foundations, cottage teardowns, seasonal-to-yearround conversions
**Tier 2 (town pages):**
- Cohasset: small affluent coastal town, rocky ledge coastline, Sandy Beach, strict conservation/historic, limited buildable lots, Boston ferry
- Hull: Nantasket peninsula, dense small lots, FEMA velocity/flood zones, elevated foundations, teardown-rebuild is THE play, sea-facing weather exposure
- Kingston: Kingston Bay, Route 3/commuter rail, more attainable land than Duxbury next door, growing town, mix of woods + coast
- Plymouth: largest land-area town in MA, America's Hometown, Pinehills, abundant buildable lots, 60k+ residents, strong new-construction market, Manomet/Cedarville villages
- Hanson: inland, rural-suburban, Wampatuck Pond, commuter rail, affordable acreage — best $/acre in the area
- Halifax: small rural town, Monponsett Ponds, affordable larger lots, quiet, septic/well common
(If you state a town-specific regulatory claim, keep it general and verifiable — "coastal lots in Hull often sit in FEMA velocity zones" — never invent bylaw numbers.)

## Primary keywords
- Town pages: `modular home builder [Town] MA` (+cluster: custom modular homes [town], prefab home builder [town] MA, modular home construction [town], new modular home [town])
- ADU pages: `modular ADU [Town] MA`
- Articles: `modular vs stick-built in [Town]` (+cluster: modular home cost [town], are modular homes cheaper, modular vs traditional cost, modular home quality)
- Pillar: `modular vs stick-built Massachusetts (cost & quality)`
- Financing: `modular home financing Massachusetts` (+appraisal, construction loan, do banks finance modular)
- Guides: slug = keyword (e.g. `what is a modular home`, localized to Massachusetts/South Shore in title + content)

## Do-nots
- NEVER invent reviews, project counts, named clients, or specific past-project addresses
- NEVER use `{{ }}` doubled braces in inline CSS
- NEVER include the noindexed funnel pages (/free-consultation/, /booking/, /thank-you/, /booking-confirmed/, /scorecard/) in internal links or sitemaps
- Form webhook URL, GA4/AW IDs, phone, email: copy EXACTLY from exemplar
