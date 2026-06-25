---
title: BMB Google Ads — Measurement & Conversions Playbook
client: Biviano Modular Builders (bivianomodularbuilders.com)
created: 2026-06-09
owner: Spencer
status: execution playbook (do these steps in order)
pairs_with:
  - google-ads-campaign-blueprint.md  (§8 conversion tracking, §11 launch checklist — THE SPEC)
  - keyword-map-modular-southshore.md
  - CLAUDE.md (design system, GHL integration)
constants:
  GA4: G-GW5Z0VVDEC
  Google_Ads_ID: AW-XXXXXXXXXX  (NOT created yet — created in STEP 1, then swapped into the site)
  Phone: (617) 678-6446  ·  tel:+16176786446
  GHL_booking_calendar: "Dream Home Design Consultation" id ML9NOoDw8ikmz2rAVnPA
  LP: /free-consultation/  (paid landing page — noindex)
---

# BMB Measurement & Conversions Playbook

This is the **human execution playbook** that turns the tracking spec into clicks-and-screens steps Spencer runs.
The build agents have already pasted the gtag snippets, the GCLID/UTM capture, and the conversion event calls into
the landing page using **placeholders** (`AW-XXXXXXXXXX`, `/LEAD_LABEL_xxx`, `/BOOKED_LABEL_xxx`, `/PHONE_LABEL_xxx`).
**Your job here is to (1) create the real account-side objects in Google Ads / GHL, (2) get the real ID + labels,
(3) swap the placeholders, and (4) verify.**

> **Do the steps IN ORDER.** Step 6 (offline import) and the value-based bidding payoff depend on Step 5 (GCLID capture +
> the `contact.bmb_gclid` field existing in GHL). Step 5's GHL field is the single most important pre-launch dependency —
> if the field doesn't exist, GHL silently drops the gclid and the whole pipeline-optimization loop breaks.

---

## 🚩 MASTER FLAG LIST — everything that must be created in the GHL UI (no agent can do these for you)

These are account-config actions that cannot be done from the codebase. Each is called out again inline at the relevant step.

| # | What | Where | Blocks |
|---|------|-------|--------|
| F1 | **Create custom field `contact.bmb_gclid`** (single-line text) | GHL → Settings → Custom Fields | Offline Booked-Consult import (Step 6). **#1 pre-launch blocker.** |
| F2 | (Optional but recommended) Create `contact.bmb_utm_source/medium/campaign/term/content` single-line text fields | GHL → Settings → Custom Fields | Clean UTM reporting (else UTMs concat into `bmb_source`) |
| F3 | **Pipeline stage named exactly `Booked Consult`** exists on the modular pipeline | GHL → Opportunities → Pipelines | Offline import trigger (Step 6) |
| F4 | (Optional) Pipeline stage `Closed - Won` / contract signed | GHL → Opportunities → Pipelines | Value-based "real money" import (Step 6 advanced) |
| F5 | **Booking-confirmed redirect / thank-you state** wired so the online `booked_consult` proxy can fire | GHL calendar `ML9NOoDw8ikmz2rAVnPA` settings → Confirmation / Redirect URL | Online Booked proxy (Step 6 / event snippet) |
| F6 | GHL → Google Ads offline conversion connection (native) OR Google Ads API access for scheduled upload / n8n | GHL → Settings → Integrations (Google Ads) | Offline import transport (Step 6) |

Everything else below is done in the **Google Ads UI** (Steps 1–4, 7) — also account-side, also only you.

---

## STEP 1 — Create the 3 conversion actions in Google Ads (get the AW ID + 3 labels)

You create three conversion actions: **LP Lead**, **Booked Consult** (the money metric), and **Phone Call**.
All three live under the SAME Google Ads conversion ID (`AW-XXXXXXXXXX`); each has its OWN label.

### 1A. Get into the right place
1. Sign in to **Google Ads** → top-right **Tools** (wrench) → **Measurement** → **Conversions**.
2. Click **+ New conversion action**.

### 1B. Conversion action #1 — "Modular — LP Lead" (website, gtag)
1. Choose **Website**.
2. When prompted to scan, you can skip the URL scan and choose **"Add a conversion action manually"** (we fire it via our own gtag event, not auto-detect).
3. Fill in:
   - **Goal / category:** **Submit lead form**
   - **Conversion name:** `Modular — LP Lead`
   - **Value:** **Use the same value for each** → **$30 USD** (placeholder weight).
   - **Count:** **One** (one valued lead per person — high-ticket, dedupe repeat submits).
   - **Click-through conversion window:** 30 days. **View-through:** 1 day (search, mostly irrelevant).
   - **Attribution model:** **Data-driven** (fallback: last click).
   - **Primary action:** set as **PRIMARY ("Account default" / Include in 'Conversions')** at launch — Smart Bidding needs early volume. (Roadmap below demotes it later.)
   - **Enhanced conversions:** turn **ON** here if offered → method **Google tag** (full setup in Step 3).
4. **Create and continue** → choose **"Use Google tag"** (NOT GTM — the site uses gtag directly).
5. On the tag screen, **copy the two values**:
   - **Conversion ID** → looks like `AW-XXXXXXXXXX`. ← this is THE account ID, same for all three.
   - **Conversion label** → looks like `AbC-D_efGh12`. ← this is the LP Lead label.
   - **Record both** (see the swap table at the end of Step 1).

### 1C. Conversion action #2 — "Modular — Booked Consult" (the money metric — value-based, PRIMARY)
1. **+ New conversion action** → **Import** (because the authoritative source is an OFFLINE upload from GHL keyed on gclid).
   - Choose **Other data sources or CRMs** → **Track conversions from clicks** (gclid-based offline import).
   - *(If you prefer to ALSO have an online proxy now, additionally create it as a Website action — see note below. The online proxy fires from the booking-confirmed page via the `booked_consult` event the build agent placed; mark it Secondary to avoid double-count.)*
2. Fill in:
   - **Goal / category:** **Submit lead form** → sub-type **Qualified lead** / **Booked appointment** (pick "Qualified lead" if "Booked appointment" isn't offered).
   - **Conversion name:** `Modular — Booked Consult`
   - **Value:** **$150 USD** (placeholder, value-based bidding — a booked Dream Home Design Consultation is the money metric).
   - **Count:** **One**.
   - **Click-through window:** **90 days** (modular sales cycle is long — a click can book weeks later; the offline upload arrives late).
   - **Primary action:** set **PRIMARY** but see the roadmap — at launch let **Lead** carry early optimization until Booked-Consult has ~15–30 conversions, then make Booked-Consult the SOLE primary.
3. **Create.** Because it's import-based there's **no label to paste into the site for the offline path** — the upload references the conversion by **name** (`Modular — Booked Consult`). 
   - **IF** you also created the online Website proxy version, copy ITS label → that's `/BOOKED_LABEL_xxx` for the `booked_consult` event on the confirmation page.

### 1D. Conversion action #3 — "Modular — Phone Call"
You'll actually create call tracking in **Step 7** (forwarding number + call asset). For the **click-to-call gtag proxy** the build agent wired, create one website action now:
1. **+ New conversion action** → **Website** → **manually**.
   - **Goal / category:** **Contact** (Phone call lead).
   - **Conversion name:** `Modular — Phone Call (click)`
   - **Value:** **$30 USD**. **Count:** **One**.
   - **Primary action:** **Secondary** ("Don't include in 'Conversions'") — it's an engagement proxy; the GFN/call-reporting action in Step 7 is the billed source of truth.
2. **Use Google tag** → copy the **label** → that's `/PHONE_LABEL_xxx`.

> Note: the Google-forwarding-number "calls from website" and "calls from ads" conversions are created in **Step 7** and need **no on-page snippet**.

### 1E. ▶ SWAP THE PLACEHOLDERS INTO THE SITE
Now you have the real values. Find-and-replace across the LP (and any funnel page carrying the global tag):

| Placeholder in code | Replace with | Source |
|---|---|---|
| `AW-XXXXXXXXXX` (global tag + every `send_to`) | your real Conversion ID, e.g. `AW-1234567890` | Step 1B |
| `AW-XXXXXXXXXX/LEAD_LABEL_xxx` | `AW-1234567890/<LP Lead label>` | Step 1B |
| `AW-XXXXXXXXXX/BOOKED_LABEL_xxx` | `AW-1234567890/<Booked online-proxy label>` (online proxy only) | Step 1C |
| `AW-XXXXXXXXXX/PHONE_LABEL_xxx` | `AW-1234567890/<Phone Call click label>` | Step 1D |

> The global tag has TWO spots for `AW-XXXXXXXXXX`: the `gtag('config','AW-XXXXXXXXXX',{...})` line AND every event `send_to`. Replace **all** instances. Do a grep for `AW-XXXXXXXXXX` and `_LABEL_xxx` after editing to confirm zero remain.

**Record card (fill in, keep private):**
```
Google Ads ID         : AW-__________
LP Lead label         : __________
Booked (online proxy) : __________   (blank if offline-only)
Phone Call click label: __________
```

---

## STEP 2 — Auto-tagging ON · link Google Ads ↔ GA4 · import GA4 key events (backup)

### 2A. Confirm auto-tagging is ON (appends `gclid` to every ad click — Step 5 depends on this)
1. Google Ads → **Admin** → **Account settings** → **Auto-tagging**.
2. Ensure **"Tag the URL that people click through from my ad"** is **CHECKED**. (On by default for newer accounts — verify, don't assume.)

### 2B. Link Google Ads ↔ GA4 (G-GW5Z0VVDEC)
1. Google Ads → **Tools** → **Data manager** (or **Linked accounts**) → **Google Analytics (GA4)**.
2. Find property **G-GW5Z0VVDEC** → **Link** → enable **personalized advertising** + **auto-tagging** + **site engagement metrics import**.
3. In **GA4** confirm: Admin → **Product Links** → **Google Ads** shows the link (accept from GA4 side if pending). You must have Editor on GA4 + Admin on Ads.

### 2C. Import GA4 key events as BACKUP conversions
The gtag GA4 mirrors (`generate_lead`, `schedule`) already fire from the LP. Mark them as **key events** in GA4 and import into Ads so you have a backup if a native Ads action ever misfires.
1. **GA4** → Admin → **Events** (or **Key events**) → after a test lead, find `generate_lead` and `schedule` → toggle **Mark as key event**.
2. **Google Ads** → Tools → Conversions → **+ New conversion action** → **Import** → **Google Analytics 4 (GA4) properties** → **Web**.
3. Select `generate_lead` and `schedule` → **Import**.
4. **Set these GA4-imported actions to SECONDARY** ("Don't include in 'Conversions'") so they don't double-count against the native gtag Lead/Booked actions. They're a safety net + audience source, not the billed metric.

> Why both: native gtag actions (Step 1) = fast + Enhanced-Conversions-capable + the billed metric. GA4-imported = backup + powers GA4 audiences/remarketing. Keeping GA4 ones Secondary is the double-count guard.

---

## STEP 3 — Enhanced Conversions for Leads (hashed first-party data from the form)

June-2026 best practice: first-party hashed email/phone beats cookies and recovers conversions when the gclid/cookie is missing (iOS, cookie loss). The LP form already passes raw email + phone; gtag SHA-256-hashes them **in the browser** before sending. **Do NOT pre-hash. Never store raw PII server-side for this.**

### 3A. Accept the EC for Leads terms
1. Google Ads → Tools → **Conversions** → **Settings** (gear at top of Conversions page) → **Enhanced conversions**.
2. Check **"Turn on enhanced conversions for leads."**
3. Agree to the **customer data terms** (you must accept; one-time).
4. **Setup method:** choose **Google tag** (gtag). *(NOT "Google Tag Manager", NOT "API" — the site uses gtag directly.)*
5. Confirm the implementation domain = `bivianomodularbuilders.com`.

### 3B. Confirm the page is feeding user_data (already coded — verify, don't re-add)
- The global tag has `gtag('config','AW-XXXXXXXXXX',{ 'allow_enhanced_conversions': true })`.
- The Lead event calls `gtag('set','user_data',{ email, phone_number })` with RAW values right before the conversion fires.
- **Phone must be E.164** (`+1XXXXXXXXXX`) — the form's auto-format already produces this; the snippet strips to digits+`+`.
- Email is trimmed + lowercased by gtag.

### 3C. Verify EC is landing (after launch test lead)
1. Submit a real test lead on the LP.
2. Google Ads → Conversions → open **Modular — LP Lead** → **Diagnostics** tab → look for **"Enhanced conversions: Recording"** and a healthy **match rate** (can take 24–48h to populate).
3. Tag Assistant (Step 8) should show the `user_data` with hashed (not raw) values in the conversion ping.

> Also set `user_data` on the booking-confirmed event when email/phone are available there, so the online Booked proxy is EC-enhanced too (the build agent included this; just confirm in Tag Assistant).

---

## STEP 4 — Consent Mode v2 (US-only stance: default GRANTED, no banner + EEA note)

This campaign targets South Shore MA only → **US-only traffic → default GRANTED, NO cookie banner.** The Consent Mode v2 **API is present** (so the account is v2-compliant and EEA-ready) but defaults all four signals to granted, so no pings are throttled.

### 4A. Verify the default-consent block is correct (already coded — verify)
The global tag's FIRST script (runs BEFORE `gtag.js` loads) must contain:
```js
gtag('consent', 'default', {
  'ad_storage':         'granted',
  'analytics_storage':  'granted',
  'ad_user_data':       'granted',     // v2 addition (required since Mar-2024)
  'ad_personalization': 'granted'      // v2 addition
});
```
Checklist:
- [ ] This `consent default` call runs **before** the `<script ... gtag/js?id=...>` library load. (Order matters — if it loads after, early pings are missed.)
- [ ] All FOUR keys present (the two v2 additions `ad_user_data` + `ad_personalization` are what make it v2-compliant).
- [ ] No CMP/cookie banner on the page (correct for US-only).

### 4B. EEA note (do NOT implement now — documented for future)
If BMB ever runs EEA traffic, you must, ABOVE the granted default, add a region-scoped denied default + a CMP banner that calls `gtag('consent','update',{...})` on accept:
```js
// EEA visitors: deny until they accept in a CMP banner
gtag('consent','default',{
  'ad_storage':'denied','analytics_storage':'denied',
  'ad_user_data':'denied','ad_personalization':'denied',
  'region':['EEA','GB'], 'wait_for_update': 500
});
// then your existing all-'granted' default (acts as the rest-of-world fallback) stays BELOW this.
```
Not needed for this US-only South Shore campaign. No `consent update` call is required while default is granted.

### 4C. Verify in Google Ads
- Google Ads → Conversions → **Diagnostics** should NOT show a "Consent mode not detected / conversions may be impacted" warning. If it does, the default block is loading too late or is missing the v2 keys.

---

## STEP 5 — GCLID capture → create `contact.bmb_gclid` in GHL → store on the contact

This is the bridge that makes Step 6 (offline import) possible. The form captures the gclid; GHL must have a field to land it in.

### 5A. 🚩 F1 — Create the GHL custom field (THE #1 pre-launch blocker)
1. **GHL → Settings → Custom Fields → + Add Field.**
2. **Field type:** **Single Line / Text.**
3. **Name:** `BMB GCLID` → confirm the generated **field key is exactly `contact.bmb_gclid`** (rename the key if GHL auto-generates something else; the form posts to this exact key, and **GHL silently drops unmapped keys**).
4. Save.
5. (🚩 F2, optional) Repeat for `contact.bmb_utm_source`, `_medium`, `_campaign`, `_term`, `_content` if you want clean UTM reporting instead of concatenating into `bmb_source`.

### 5B. Confirm the LP form is wired (already coded — verify)
- Hidden fields exist: `gclid, gbraid, wbraid, utm_source, utm_medium, utm_campaign, utm_term, utm_content`.
- On-load inline script reads `location.search`, populates the hidden fields, and **persists gclid to `localStorage` (90-day window)** so a return visit that lost the query string still attributes.
- The no-cors webhook payload includes:
  ```js
  customField: {
    'contact.bmb_home_size': ...,
    'contact.bmb_town': ...,
    'contact.bmb_project_description': ...,
    'contact.bmb_source': utm_source || 'google-ads',
    'contact.bmb_gclid': <hidden gclid value>     // <-- lands in the F1 field
  }
  ```

### 5C. Verify the gclid lands on the contact (test)
1. Visit the LP with a fake gclid: `https://bivianomodularbuilders.com/free-consultation/?gclid=TEST_GCLID_123&utm_source=google&utm_medium=cpc&utm_campaign=modular-southshore`
2. Submit a test lead.
3. **GHL → Contacts** → open the test contact → confirm **`BMB GCLID` = `TEST_GCLID_123`** and the UTM/source fields populated.
4. If blank → the field key doesn't match `contact.bmb_gclid` (fix F1) OR the form isn't posting the key. **This MUST pass before launch** — blueprint §11 "gclid capture verified."

---

## STEP 6 — OFFLINE CONVERSION IMPORT (the value-based-bidding payoff)

**The whole point:** stop optimizing to raw form-fills; optimize Smart Bidding to **real booked consults (and ultimately closed contracts) = pipeline**.
GHL stores `bmb_gclid` on the contact → when the contact's pipeline stage hits **`Booked Consult`**, push `{gclid, conversion name, time, value, currency}` back to Google Ads. Google matches on gclid and credits the click that produced the booking — even days/weeks later.

### 6A. 🚩 F3 — Confirm the pipeline stage exists
- GHL → **Opportunities → Pipelines** → the modular pipeline must have a stage named **exactly `Booked Consult`**. (And, for the advanced step, a `Closed - Won` stage = F4.)

### 6B. Pick ONE transport (in order of preference)

**Option A — GHL-native Google Ads conversion action (preferred, lowest maintenance):**
1. 🚩 F6 — GHL → **Settings → Integrations → Google Ads** → connect the BMB Google Ads account (OAuth).
2. GHL → **Automation → Workflows** → new workflow:
   - **Trigger:** *Opportunity Stage Changed* → Pipeline = modular, Stage = **Booked Consult**.
   - **Filter:** `contact.bmb_gclid` **is not empty** (skip non-paid leads so you don't upload junk).
   - **Action:** *Google Ads — Report Conversion* (a.k.a. "Create Google Ads Conversion"):
     - **Conversion action:** `Modular — Booked Consult`
     - **GCLID:** `{{contact.bmb_gclid}}`
     - **Value:** `150` · **Currency:** `USD`
     - **Conversion time:** stage-change timestamp.
3. (Advanced value-based) Add a SECOND workflow on stage = `Closed - Won` (F4) that reports `Modular — Booked Consult` (or a separate "Closed" action) with the **actual contract value** so bidding learns toward real revenue, not just bookings.

**Option B — Scheduled offline-conversion upload (if GHL-native action isn't available):**
1. Build a GHL/Smart-List export (or a scheduled report) of contacts that entered `Booked Consult` with columns: `Google Click ID, Conversion Name, Conversion Time, Conversion Value, Conversion Currency`.
   - `Conversion Name` = `Modular — Booked Consult` (must match Step 1C name exactly).
   - `Conversion Time` format = `yyyy-MM-dd HH:mm:ss±hh:mm` (or use the timezone column).
2. Google Ads → Tools → **Conversions → Uploads → + (Upload)** → upload the CSV (or connect Google Sheets for a recurring schedule).
3. Do this **2–3×/week** during ramp; weekly once stable. (Uploads must land within the 90-day click window.)

**Option C — n8n automation (most flexible / fully automated):**
1. n8n workflow: **GHL trigger** (Opportunity stage → `Booked Consult`, via GHL webhook/trigger node) → **Filter** (`bmb_gclid` not empty) → **Google Ads node** → *Upload Click Conversion* (`uploadClickConversions`):
   - `gclid` = `{{$json.contact.bmb_gclid}}`
   - `conversionAction` = resource name of `Modular — Booked Consult`
   - `conversionDateTime`, `conversionValue` = 150, `currencyCode` = USD.
2. Requires Google Ads API access (developer token + OAuth on the BMB account). Reuse the SPG n8n instance + the `/n8n` skill if building this.
3. Best when you want the closed-contract value loop fully hands-off and de-duped in code.

### 6C. Double-count guard (critical)
- The online booking-confirmed `booked_consult` web event is a **proxy** so you have a signal before offline import is live.
- Once offline import (6B) is running, EITHER:
  - set the **online Booked web action to Secondary** ("Don't include in 'Conversions'"), OR
  - dedupe in the uploader (don't upload gclids that already fired the web proxy).
- Net: **exactly one** Booked-Consult conversion is counted per booking.

### 6D. Verify the loop (24–48h)
1. Move your Step-5 test contact into `Booked Consult`.
2. Wait 24–48h → Google Ads → Conversions → **Modular — Booked Consult** → confirm the import appears (Diagnostics → recent conversions / "Imported"). Check for "Unattributed" errors (means gclid was missing/expired → revisit Step 5 / window length).

### 6E. Primary/Secondary roadmap (so bidding optimizes to pipeline, not form-fills — blueprint §8C & §11)
- **Launch:** Lead = Primary, Booked Consult = Primary (volume), Phone + online-Booked-proxy + GA4-imports = Secondary.
- **After ~30 conversions / steady offline import:** demote **Lead → Secondary**; make **`Modular — Booked Consult` (offline) the SOLE Primary** so tCPA/Max-Conversions optimizes to booked pipeline. (Matches blueprint §10 bid ramp + §11 Day-60/90.)

---

## STEP 7 — Call tracking (call-from-ad + a number on the LP + call conversions)

Three call paths, two of which need NO snippet (Google handles them), one is the gtag click proxy from Step 1D.

### 7A. Calls from the ad (Call asset / call-only) — call reporting
1. Google Ads → **Ads & assets → Assets → + → Call asset** → phone **(617) 678-6446**.
2. **Turn ON "Call reporting"** (uses a Google forwarding number to count calls).
3. **Conversion action for these:** Google Ads → Conversions → **+ New** → **Phone calls** → **"Calls from ads using call extensions or call-only ads"** → name `Modular — Call from Ad` → category **Contact** → **min call length 60s counts** → value **$30** → Count **One** → **Primary** (this is a billed source-of-truth call conversion). No website snippet needed.

### 7B. Calls from the landing page — Google Forwarding Number (call-from-website)
1. Google Ads → Conversions → **+ New** → **Phone calls** → **"Calls to a phone number on your website"**.
2. Name `Modular — Call from Website` → category **Contact** → **min length 60s** → value **$30** → Count **One** → **Primary**.
3. Google gives you a **phone snippet (the GFN wrapper)** that dynamically swaps the on-page number for a Google forwarding number to measure calls. 🚩 The build agent's LP shows the **static** `tel:+16176786446`. To enable GFN measurement you must add this Google-provided phone snippet so the displayed number is swapped. (If you skip GFN, you still get the **click-to-call gtag proxy** from Step 1D — but that counts taps, not connected calls, and is Secondary.)
4. Verify in Diagnostics that the forwarding number is provisioned for your area.

### 7C. Click-to-call proxy (already coded — Step 1D)
- Every `tel:` link (and the sticky mobile call button) has `onclick="return firePhoneConversion();"` firing the **`Modular — Phone Call (click)`** action (Secondary).
- **Source of truth = GFN/call-reporting (7A/7B). The click event is a Secondary engagement signal** — do not let it double-count against the GFN conversions (keeping it Secondary handles this).

---

## STEP 8 — Weekly QA checklist (confirm conversions are recording)

Run this every week (2–3×/week during Weeks 1–2 ramp). Tools: **Google Tag Assistant**, **Google Ads → Conversions → Diagnostics / "recent conversions"**, **GA4 → DebugView/Realtime**, **GHL Contacts**.

**A. Tag health (Tag Assistant on the live LP)**
- [ ] Global tag fires: GA4 `G-GW5Z0VVDEC` + Ads `AW-__________` both load.
- [ ] Consent Mode default = all four signals **granted**, fires **before** gtag.js.
- [ ] No remaining `AW-XXXXXXXXXX` or `_LABEL_xxx` placeholders (grep the deployed LP).

**B. Lead conversion (submit a real test lead weekly)**
- [ ] On submit: `Modular — LP Lead` conversion ping fires (Tag Assistant) with hashed `user_data` (email/phone hashed, NOT raw).
- [ ] GA4 DebugView shows `generate_lead`.
- [ ] Google Ads → Conversions → `Modular — LP Lead` shows the test within ~24–48h; status **Recording**; EC **Recording** with a healthy match rate.

**C. GCLID capture (the pipeline blocker)**
- [ ] Test lead with `?gclid=TEST_...` → GHL contact shows `BMB GCLID` populated (Step 5C).
- [ ] `contact.bmb_gclid` field still exists + key unchanged (F1).

**D. Booked Consult / offline import**
- [ ] Pipeline stage `Booked Consult` still exists (F3).
- [ ] Move a test contact to `Booked Consult` → within 24–48h `Modular — Booked Consult` shows an imported conversion (Step 6D); no spike in "Unattributed".
- [ ] Exactly one Booked conversion per booking (double-count guard, 6C).

**E. Calls**
- [ ] `Modular — Call from Ad` + `Modular — Call from Website` show conversions when test-calling ≥60s.
- [ ] GFN forwarding number is live on the LP (7B) if GFN measurement is enabled.
- [ ] Click-to-call proxy stays **Secondary**.

**F. Account links + bidding hygiene**
- [ ] Auto-tagging still ON (2A).
- [ ] Google Ads ↔ GA4 link healthy (2B); GA4-imported actions still **Secondary**.
- [ ] Primary/Secondary matches the current roadmap phase (6E) — once ≥30 conversions + steady import, Lead is demoted and Booked Consult is sole Primary.

**G. Search terms / spend protection (cross-ref blueprint §5/§11)**
- [ ] Mined Search Terms report; added junk negatives to "Modular — Master Negatives" shared list.

---

## Pre-launch dependency order (one-screen recap — blueprint §11)
1. **STEP 1** — create 3 conversion actions → get `AW-__________` + labels → **swap placeholders** (grep for leftovers).
2. **STEP 5 / F1** — create `contact.bmb_gclid` in GHL (**#1 blocker**) + verify gclid lands on a test contact.
3. **STEP 2A** — auto-tagging ON.
4. **STEP 2B** — link Google Ads ↔ GA4; import GA4 key events as Secondary backup.
5. **STEP 3** — accept Enhanced Conversions for Leads (method = Google tag).
6. **STEP 7** — call reporting (Call asset) + Google Forwarding Number for LP calls.
7. **STEP 6 / F3, F6** — wire GHL → Google Ads offline import for Booked Consult keyed on gclid.
8. **STEP 4** — confirm Consent Mode v2 default-granted block (no banner).
9. **STEP 8** — run the QA checklist with a real test lead end-to-end before spending.

> Reminder for the build agents' output: the LP must also carry `<meta name="robots" content="noindex,follow">` (paid LP stays out of organic), and all on-page handlers are inline (GHL-safe), no `addEventListener` on GHL-touched elements.
