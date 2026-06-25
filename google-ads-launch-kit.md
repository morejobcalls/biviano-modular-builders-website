# Google Ads Launch Kit — Biviano Modular Builders (FINAL Operator Playbook)

**Brand:** Biviano Modular Builders (BMB) · modular-only brand of Biviano General Contracting LLC, Marshfield MA
**Account:** **Biviano GC** (Google Ads contact / phone on file: **303-997-7029**)
**Objective:** Lead generation — booked **Free Modular Home Design & Budget Consultations**
**Final URL (all ads):** `https://www.bivianomodularbuilders.com/free-consultation/` (dedicated paid LP, `noindex,follow`)
**Geo:** Plymouth County / South Shore MA — **presence-only**
**Companion import file:** `google-ads-editor-import.csv` (this is the source of truth for campaigns, ad groups, keywords, RSAs, and campaign negatives)
**Built:** 2026-06-09 · Productionizes `google-ads-campaign-blueprint.md` + `keyword-map-modular-southshore.md`.

> ### 🔄 UPDATE 2026-06-25 — restructured to 3 campaigns (Spencer + Claude review)
> The original 2-campaign build was split into **3 campaigns** so the "New Construction / Custom Home Builder" bet runs on its **own isolated budget** — the strategic call is that broad new-build searchers want the *outcome* (a new home), and most would choose modular once they know it's faster + 20–25% cheaper. Isolating it gives a clean read on whether that awareness-arbitrage thesis books consults at a workable cost-per-booked-consult, without it starving the core high-intent modular terms. Also applied: **RSA H2/H3 unpinned** (only H1/offer stays pinned → better Ad Strength) and **"biviano contracting" keyword dropped** (parent-company term, message mismatch). The CSV `google-ads-editor-import.csv` reflects all of this; the pre-change file is saved as `google-ads-editor-import-2camp-backup-2026-06-25.csv`. Counts below updated to match.

> **How to use this doc.** Work it top to bottom. §1 is the final structure. §2 is the Editor import. §3 is the manual settings the CSV can't set. §4 is conversions (already live — IDs below). §5 is the ad ASSETS you build in the UI. §6 is the bid ramp. §7 is the pre-launch gate. §8 is the numbered LAUNCH CHECKLIST.

> ### ✅ BUILT VIA API 2026-06-25 — structure is live (PAUSED) in account **Biviano GC active (303-997-7029)**
> The full skeleton was created directly via the Google Ads API into customer `3039977029` — **NOT** via the Editor CSV import (§2 is now superseded for the initial build; the CSV remains the source of truth / re-import fallback). Created, all **PAUSED**, no spend:
> - **3 campaigns** — Search - Modular + ADU ($30/d), Search - New Construction ($28/d), Search - Brand - Biviano ($8/d). Each: Maximize Clicks with CPC ceiling ($15/$15/$4), **Search network only** (partners + Display OFF), **presence-only geo** = 7 town cities (Marshfield, Scituate, Duxbury, Pembroke, Norwell, Hanover, Hingham) + a **12-mi proximity around Marshfield 02050** (covers Humarock).
> - **4 ad groups · 105 keywords** (exact+phrase) · **342 campaign negative keywords** (broad) · **4 RSAs** (15 headlines, H1 pinned; 4 descriptions; all within length limits).
> - The pre-existing "Modular Lead Gen Campaign 1" was **left paused/untouched** per Spencer.
>
> **STILL TO DO before enabling (NOT built via API):** (a) §3d campaign **conversion-goal scoping** (Lead + Booked Consult primary, Phone secondary); (b) §5 **assets** (sitelinks, callouts, structured snippets, call asset + call reporting, location, images); (c) §7 **pre-launch gate** (advertiser verification, billing, live conversion test); (d) **ENABLE** the campaigns (§8 step 14). Build IDs: campaigns `23979586003` (Modular+ADU), `23979586006` (New Construction), `23979586009` (Brand).

---

## 1. Final campaign structure

**Three campaigns, four ad groups.** Everything below is in the CSV; this is the map.

```
Campaign A: Search - Modular + ADU   (NON-BRAND · core intent · Search only · Display+Partners OFF)
│   Budget $30/day · Bid: Maximize Clicks · Max CPC cap $15
├── Ad Group 1: Modular Home Builder                 (ENABLED · core modular intent)
└── Ad Group 2: Modular ADU In-Law                   (ENABLED · ADU / in-law suite intent)

Campaign B: Search - New Construction   (NON-BRAND · awareness bet · Search only · Display+Partners OFF)
│   Budget $28/day · Bid: Maximize Clicks · Max CPC cap $15
└── Ad Group: New Construction Custom Home Builder    (ENABLED · broad new-build intent)

Campaign C: Search - Brand - Biviano   (BRAND DEFENSE · Search only · Display+Partners OFF)
│   Budget $8/day · Bid: Maximize Clicks · Max CPC cap $4
└── Ad Group: Brand                                   (ENABLED · biviano* terms)
```

| Item | A (Modular + ADU) | B (New Construction) | C (Brand) |
|---|---|---|---|
| Daily budget | **$30** | **$28** | **$8** |
| Networks | Search only | Search only | Search only |
| Bid strategy | **Maximize Clicks** | **Maximize Clicks** | **Maximize Clicks** |
| Max CPC cap | **$15** | **$15** | **$4** |
| Ad groups | 2 | 1 | 1 |
| Keywords | 58 (exact + phrase) | 35 (exact + phrase) | 12 (exact + phrase) |
| RSAs | 2 (one per ad group) | 1 | 1 |
| Final URL | `…/free-consultation/` | `…/free-consultation/` | `…/free-consultation/` |
| Total/mo | ~$2,000 across all three (~$66/day) | | |

**Why this shape:** Campaign A holds the **highest-intent, cleanest message-match** terms — people already searching "modular" plus rising MA ADU/in-law demand (we have dedicated ADU pages). Campaign B is the **awareness bet on its own budget**: broad "new/custom home builder" searchers want a new home and most would choose modular once they learn it's faster + 20–25% cheaper — isolating this campaign means we get a clean cost-per-booked-consult read on whether that thesis pays, and can scale it independently if it does (or trim it if it doesn't) without touching the core. Campaign C is cheap brand defense so competitors can't bid on "biviano" and steal a warm searcher for pennies.

**Keyword counts by ad group (rows in the CSV, exact + phrase):**
- A · Modular Home Builder — **36 keyword rows**, incl. the 8-town "modular home builder [town] ma" expansion (Marshfield, Scituate, Duxbury, Pembroke, Norwell, Hanover, Hingham, Humarock).
- A · Modular ADU / In-Law — **22 keyword rows**: ADU/in-law terms + per-town ADU builder terms.
- B · New Construction / Custom Home Builder — **35 keyword rows**: core new-build terms + per-town custom/new-construction terms across the 5 highest-volume towns (Marshfield, Scituate, Duxbury, Hingham, Hanover).
- C · Brand — **12 keyword rows**: biviano, biviano modular, biviano modular builders, biviano builders, biviano homes, biviano marshfield (**"biviano contracting" dropped 2026-06-25** — parent-company term).
- **Totals:** A = 58 · B = 35 · C = 12 · grand total **105**. Campaign negatives: the 161-term modular negative set is applied to **both** A and B (322 rows) + 20 on C = **342 negative rows**.
- **Expansion idea (Campaign B, post-launch):** add a cost/speed-pain ad group — "cost to build a house," "how much to build a new home," "fastest way to build a house" — where the modular pitch lands hardest.

---

## 2. Import into Google Ads Editor (campaigns, ad groups, keywords, RSAs, negatives)

The CSV builds the **skeleton** — campaigns, ad groups, keywords (exact+phrase), the 4 RSAs (15 headlines + 4 descriptions each), and the **campaign-level negative keywords**. Assets and conversions are layered on after (they are NOT in the Editor CSV — see §4–§5).

1. Open **Google Ads Editor** and **Download** the latest version of the **Biviano GC** account (so Editor has current account data).
2. **Account → Import → From file…** → choose `google-ads-editor-import.csv`.
3. In the import preview, **map columns** (Editor usually auto-maps the standard headers). Confirm: Campaign, Ad Group, Max CPC, Keyword, Criterion Type, Campaign Negative Keyword, the 15 Headline + 4 Description columns, Path 1/2, Final URL.
4. **Review proposed changes** — you should see: **3 campaigns, 4 ad groups, 105 keywords, 4 responsive search ads, 342 campaign negative keyword rows** (the 161-term modular set lives on both non-brand campaigns). Resolve any warnings (e.g., a too-long headline flag — none expected; all are ≤30 chars, descriptions ≤90, paths ≤15).
5. Click **Keep / Apply** to accept the imported rows into the local draft.
6. **Post** (top-right) to push the changes live to the account — OR leave the campaigns **paused** in Editor first if you want to finish §3–§5 before any spend (recommended: post, then complete manual settings, then enable at §8 LAUNCH).

> If a row imports as the wrong type, check that empty fields stayed empty (the CSV pads every row to 42 columns). Re-export from this kit if needed — do not hand-edit column counts.

---

## 3. Post-import MANUAL settings (the CSV cannot set these — do in the Google Ads UI)

### 3a. Geo targeting — PRESENCE-ONLY
For **all three** campaigns: **Settings → Locations**.
- **Location options → Target = "Presence: People in or regularly in your targeted locations"** (NOT "Presence or interest"). This is the single biggest out-of-area leak-stopper.
- Add the **8 target towns**: **Marshfield, Scituate, Duxbury, Pembroke, Norwell, Hanover, Hingham, Humarock** — PLUS a **~12-mile radius around Marshfield, MA 02050** (2183 Ocean St) to catch the immediate Tier-2 fringe without sprawling into Boston.
- (Optional) Exclude obvious out-of-market metros if junk impressions appear later. The `boston` negative is in the list — radius around Marshfield already excludes most city-Boston traffic.

### 3b. Networks — confirm Partners + Display OFF
For **all three** campaigns: **Settings → Networks** → **uncheck "Include Google search partners"** AND **uncheck "Include Google Display Network."** Search only. (CSV sets "Google search" but always confirm in the UI — it's the #1 budget leak.)

### 3c. CPC caps
Confirm the **Maximize Clicks** bid strategy has a **Maximum CPC bid limit**: **$15** on Campaigns A (Modular + ADU) and B (New Construction), **$4** on Campaign C (Brand). (Editor imports the cap from Max CPC, but verify in Settings → Bidding.)

### 3d. Campaign optimization goals — Lead + Booked Consult ONLY
**Settings → Goals / Conversions** on **all three** campaigns → use **campaign-specific conversion goals** and include **only**:
- **Modular — LP Lead** (Primary)
- **Modular — Booked Consult** (Primary)

**EXCLUDE "Phone" / "Contact" from the bidding goals** — set the Phone action to **Secondary ("don't include in 'Conversions'")** so Smart Bidding does not optimize to cheap phone taps. Phone still *reports*, it just doesn't drive the algorithm. (See §4.)

### 3e. Ad schedule
- **Launch:** all days / all hours (gather data first).
- **After 2–4 wks:** review the "When consults book" + Day/Hour reports; weight up **Mon–Fri 8am–8pm, Sat 9am–5pm**, weight down dead overnight hours (modest ±10–50% — don't over-constrain a low-volume account).

### 3f. Apply negatives
The CSV adds the negatives as **campaign-level negative keywords** on each campaign. If you'd rather manage them as a **shared list** ("Modular - Master Negatives"), recreate the list in **Tools → Shared library → Negative keyword lists** and apply it to Campaign A — then you can delete the per-campaign rows to avoid duplication. Either way, **mine the Search Terms report 2–3×/wk for the first 2 months** and append junk.

---

## 4. Conversion actions — ALREADY LIVE (do not recreate)

Conversion ID + labels are already created in the account. Confirm they exist and are mapped correctly; they're already on the LP.

| # | Name | Value | Role | send_to (`AW-16742219835` + label) |
|---|---|---|---|---|
| 1 | **Modular — Booked Consult** | **$300** | **Primary** (the money metric) | `AW-16742219835/EiYqCPbT9rscELuAqK8-` |
| 2 | **Modular — Lead** | **$30** | **Primary** (volume at launch) | `AW-16742219835/yisSCKuX9rscELuAqK8-` |
| 3 | **Modular — Phone** | **$30** | **Secondary** (report only — NOT a bidding goal) | `AW-16742219835/xcCUCKrE97scELuAqK8-` |

- **Auto-tagging ON** (Settings → Account → Auto-tagging) — required for the offline Booked-Consult import keyed on **gclid**.
- **Enhanced Conversions for Leads** accepted (Settings → Enhanced conversions for leads, method = Google tag) — recovers conversions when the cookie/gclid degrades.
- **GHL custom field `contact.bmb_gclid`** must exist so the offline Booked-Consult import works (the LP posts gclid; GHL drops unmapped keys). This is the single most important tracking dependency — confirm before launch.
- Per §3d: Lead + Booked Consult are the bidding goals; **Phone is Secondary** (excluded from "Conversions"). Post-ramp (Day 90), demote **Lead → Secondary** so **Booked Consult** is the sole Primary and tCPA optimizes to real pipeline.

---

## 5. Ad ASSETS — build in the UI (NOT in the keyword CSV)

Build these at **campaign level on the two non-brand campaigns** (A Modular + ADU, B New Construction) and **reuse on the Brand campaign** where it makes sense (callouts/sitelinks/call/location). Assets lift CTR + Ad Rank for free.

**Sitelinks (5):**
| Text | URL |
|---|---|
| Why Modular | `…/free-consultation/#why` (or `/why-modular/`) |
| Our Process | `…/free-consultation/#how` (or `/process/`) |
| Pricing | `…/free-consultation/#pricing` (or `/pricing/`) |
| Gallery | `/gallery/` |
| Free Consultation | `…/free-consultation/` |

**Callouts (6):** 8–12 Week Build · 20–25% Less · 4th-Gen Family Builder · Licensed & Insured · One Builder Start-to-Finish · Free Design Consult

**Structured snippets — Header "Service Catalog":** Custom Modular Homes · ADUs · Teardown & Rebuild · Coastal/Flood-Zone Builds

**Call asset:** **(617) 678-6446** (`tel:+16176786446`) — **turn call reporting ON** (required for the Phone conversion). Schedule to business hours so taps reach a live phone.

**Location asset:** link the **Google Business Profile** (2183 Ocean St, Marshfield MA 02050).

**Image assets:** best finished-home + crane-set modular photos (1.91:1 + 1:1 crops). From `/photos`.

**(Optional) Promotion asset:** "Free Design & Budget Consultation."

---

## 6. Bid ramp (Maximize Clicks → Maximize Conversions → tCPA)

| Phase | Trigger | Strategy | Notes |
|---|---|---|---|
| **Phase 0 — Data gather** | Launch → ~15–30 tracked conversions | **Maximize Clicks**, CPC cap **$15** (A & B) / **$4** (C Brand) | Controlled spend; mine Search Terms hard; build negatives. Smart Bidding starves with no data. |
| **Phase 1 — Conversion learning** | ~15–30 conversions logged (~day 30–45) | **Maximize Conversions** (no tCPA yet) | Let the algorithm find converters before you constrain it. |
| **Phase 2 — Target CPA** | CPL stable + steady offline Booked-Consult import (~day 60–90) | **Maximize Conversions w/ tCPA** | Set tCPA from observed Cost/Booked-Consult. Demote Lead → Secondary so Booked Consult is sole Primary. |

**Expect a 2–4 week learning + negative-mining period** before CPL settles. Don't switch bid strategies or pass judgment before the account has the conversion volume above — judge on **consults booked, not clicks.**

---

## 7. Pre-launch gate (all must be ✅ before enabling)

- [ ] **Advertiser verification cleared** on the Biviano GC account (Google's identity/business verification — ads won't serve until it passes; start this early, it can take days).
- [ ] **Conversions confirmed firing** — submit a real test lead → Lead conversion records → `bmb_gclid` lands on the GHL contact → move contact to "Booked" stage → offline Booked-Consult import appears (≤24–48h).
- [ ] **Geo set** to presence-only on the 8 towns + 12-mi Marshfield radius (§3a).
- [ ] **Display + Search Partners OFF** on both campaigns (§3b).
- [ ] **CPC caps** $15 / $4 set (§3c).
- [ ] **Bidding goals** = Lead + Booked Consult only; **Phone = Secondary** (§3d).
- [ ] **Negatives applied** (§3f).
- [ ] **Assets built** — sitelinks, callouts, structured snippets, **Call asset + call reporting ON**, location, images (§5).
- [ ] **LP live**, mobile-tested, `noindex,follow`, sticky click-to-call present, final URL = `https://www.bivianomodularbuilders.com/free-consultation/`.
- [ ] **Billing** set on the account.

---

## 8. LAUNCH CHECKLIST (numbered — work top to bottom)

1. **Download** the Biviano GC account in Google Ads Editor.
2. **Import** `google-ads-editor-import.csv` (Account → Import → From file). Review: **3 campaigns, 4 ad groups, 105 keywords, 4 RSAs, 342 campaign negative rows**. (§2)
3. **Post** the changes to the account (leave campaigns ready; you'll enable at step 14).
4. **Geo:** set all three campaigns to **Presence-only** on the 8 towns + ~12-mi Marshfield 02050 radius. (§3a)
5. **Networks:** confirm **Search Partners OFF + Display OFF** on all three campaigns. (§3b)
6. **CPC caps:** confirm **$15** (A Modular + ADU / B New Construction) and **$4** (C Brand) on the Maximize Clicks strategy. (§3c)
7. **Goals:** set all three campaigns' bidding goals to **Lead + Booked Consult only**; set **Phone = Secondary**. (§3d)
8. **Negatives:** confirm the campaign negatives imported (or build + apply the shared list). (§3f)
9. **Conversions:** confirm the 3 live actions (Lead $30 Primary, Booked Consult $300 Primary, Phone $30 Secondary) and **auto-tagging ON**; confirm **`contact.bmb_gclid`** exists in GHL. (§4)
10. **Assets:** build the 5 sitelinks, 6 callouts, Service-Catalog structured snippets, **Call asset + call reporting ON**, location asset, image assets. (§5)
11. **Ad strength:** confirm all 4 RSAs show Good/Excellent and have **no policy disapprovals**.
12. **Test conversion:** submit a real test lead → Lead fires → gclid on GHL contact → Booked-Consult offline import appears. (§7)
13. **Pre-launch gate:** verify every box in §7 is ✅ — including **advertiser verification cleared**.
14. **ENABLE** both campaigns. Confirm impressions/clicks begin and conversions record within 24–48h.
15. **Weeks 1–2:** mine the **Search Terms report 2–3×/wk** → add negatives aggressively; pause zero-converting high-spend terms; confirm Lead + Booked Consult recording; confirm gclid flowing to GHL.
16. **Weeks 3–4:** assess CPL by ad group/keyword; shift budget to winners; add a 2nd RSA variant per ad group; apply device/geo/**ad-schedule** bid adjustments. (§3e)
17. **Day 30:** stable tracking + clean search terms + first CPL read (target Cost/Lead < $200); confirm offline Booked-Consult import flowing.
18. **Day 45–60:** at ~15–30 conversions, switch Campaign A to **Maximize Conversions** (§6 Phase 1).
19. **Day 90:** move to **tCPA** targeting **Booked Consult**; **demote Lead → Secondary** so Booked Consult is the sole Primary; evaluate Maximize Conversion Value / tROAS; consider Tier-2 towns.

**KPIs (judge on consults booked, not clicks):** Cost/Lead (target <$200) · **Cost/Booked Consult** (the real one) · Lead→Consult rate · Consult→Contract rate · ROAS on closed homes.
