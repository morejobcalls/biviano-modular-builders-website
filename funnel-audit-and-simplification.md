# BMB Funnel Audit + Simplification Proposal

**Filed:** 2026-05-19
**Trigger:** Shelagh O'Brien's contact has no address, no UTM, no custom fields. Spencer asked for a full cleanup.

---

## 🟥 The Diagnosis

### Shelagh O'Brien specifically
- Came in via `https://go.bivianocontracting.com/custom-design` (a GHL booking calendar)
- That calendar collects **only name + email + phone** — no address field, no survey, no UTMs
- She had no ad click, so attribution shows `medium: Manual`
- She booked an appointment successfully — she's not a broken lead, she's just a low-data lead. **The funnel didn't ask for more.**

### The system-wide pattern (last 90 days, 276 contacts)
| Symptom | Count | % |
|---|---|---|
| Contacts with **no address** | 82 | 29% |
| Contacts with **no custom field data** | 121 | 43% |
| Contacts with **no UTM attribution** | 160 | 57% |

**Nearly half of all BMB leads come in with zero qualifying data.** Mike opens them, sees blanks, gets frustrated. Shelagh isn't an exception — she's typical.

---

## 🗺️ Current state — 4 domains, 9 landing pages, 7 source labels

### Domains in active use
1. `bivianocontracting.com` — Mike's main GC site
2. `go.bivianocontracting.com` — GHL-hosted funnels (sub-domain)
3. `bivianocontractingroofs.com` — third domain, unclear purpose, capturing leads
4. `bivianomodularbuilders.com` — the new modular site we built, getting **0 leads** (ads not routed here)

### Landing pages capturing leads (last 90 days)
| URL | Leads | Notes |
|---|---|---|
| `go.bivianocontracting.com/custom-design` | 81 | 🟥 No survey, no address, anyone can book. Shelagh's path. |
| `bivianocontractingroofs.com/deck-offer` | 47 | On the third domain. Decking offer. |
| `go.bivianocontracting.com/dream-home` | 31 | ✅ Modular survey funnel — captures custom fields |
| `bivianocontractingroofs.com/custom-design` | 21 | Duplicate of #1 on the third domain |
| `go.bivianocontracting.com/dream-decks` | 10 | Decking equivalent of dream-home |
| `go.bivianocontracting.com/modular-homes` | 10 | Yet another modular page |
| `go.bivianocontracting.com/dream-home-booking` | 8 | Post-survey booking page |
| `go.bivianocontracting.com/custom-design-1907` | 7 | Variant URL of #1 |
| `bivianomodularbuilders.com/*` | **0** | The new site we built. Dead. |

### Source labels in use
| Source | Count | What it represents |
|---|---|---|
| Custom Design Meeting & Free Estimate | 62 | Calendar booking, no qualifying data |
| (no source) | 60 | Untagged — somewhere in the system isn't writing a source |
| Leads Survey | 59 | 🟥 Ambiguous — modular? decking? unknown |
| Leads Survey \| Modular | 42 | Clean |
| Leads Survey \| Decking | 39 | Clean |
| chat widget | 7 | Chat on bivianocontracting.com |
| Modular Opt-In Survey 1 | 7 | A different modular survey somewhere |

### GHL infrastructure inventory
- **6 Funnels:** META | DECKS, META Ads | Modular, Funnel | Decking | REQUEST, Funnel | Modular | Google PPC | Auto-Confirm Calendar, Biviano Contracting Website, Privacy Policy
- **3 Calendars:** Custom Design Meeting & Free Estimate (active), [INTERNAL USE] same (inactive), Dream Home Design Consultation (active)
- **5 Forms:** Modular Home Booking Calendar Form, Decking Simple Contact Form, 2 Pop-Up opt-ins, A2P Opt-In
- **14 Workflows** (8 active "new lead" type)
- **49 custom fields** (just cleaned up into 6 folders today)

---

## 🟢 Proposed simplified architecture

### Principle: One service line = one path

```
                  MODULAR PATH                          DECKING PATH
                  ────────────                          ────────────
Paid traffic   →  Facebook/Google ads (UTM tagged)  →   Facebook/Google ads (UTM tagged)
                       ↓                                       ↓
Landing page   →  bivianomodularbuilders.com         →   bivianocontracting.com/decks
                  (or go.biviano/dream-home)             (or go.biviano/dream-decks)
                       ↓                                       ↓
Survey         →  Required: Town, Timeline, Sqft,    →   Required: Town, Timeline, Project type,
                  Situation, BR/BA, Budget                Square footage, Material, Budget
                       ↓                                       ↓
Calendar       →  Dream Home Design Consultation     →   Dream Home Design Consultation
                  (single shared calendar, OK)           (same calendar)
                       ↓                                       ↓
Confirmation   →  Same confirmation flow             →   Same confirmation flow
                       ↓                                       ↓
Workflow       →  ONE master "Lead Intake" workflow tags + notes + SMS to Mike
                  (Contact Created trigger — fires regardless of source)
```

### What to KILL
1. **`bivianocontractingroofs.com`** — third domain, redundant, just splits traffic. Redirect to bivianocontracting.com.
2. **`/custom-design` direct booking page** — replace with "fill out a 60-second survey, then we'll show you the calendar" gate
3. **Duplicate landing pages** (`/custom-design-1907`, `/modular-homes`, multiple `/dream-*` variants) — pick ONE per service
4. **Untagged "Leads Survey" label** — every survey must specify modular or decking

### What to KEEP
- The `dream-home` and `dream-decks` GHL survey funnels — they ARE capturing custom field data (this is your golden path)
- The `Dream Home Design Consultation` calendar — single shared calendar after qualifying
- The custom field schema we cleaned up today
- Your existing ad-creative + targeting

### What to REWORK
1. **Route ALL paid traffic through a survey first.** Never link ads directly to a calendar. The survey step is what gives Mike data to triage.
2. **Embed UTM-capturing JavaScript on every landing page** so even organic visitors get tagged with a sensible default (`utm_source=organic&utm_medium=direct`).
3. **Add a "How did you hear about us?" field** to the direct-booking calendar — captures attribution for word-of-mouth (Shelagh-type) leads.
4. **One source label per intake path.** Modular ads → `Modular Ad`. Modular organic → `Modular Organic`. Decking ads → `Decking Ad`. Etc. Five sources max.

---

## 🎯 Recommended cleanup sequence

1. **Quick wins (this week, ~2 hours):**
   - Add "How did you hear about us?" + "Project address" to the Custom Design calendar form (fixes Shelagh-type leads)
   - Add UTM-capturing snippet to bivianocontracting.com landing pages (catches organic + direct traffic)
   - Pick ONE source label naming convention and update all funnels/forms

2. **Phase 2 (next 2 weeks):**
   - Audit which `bivianocontractingroofs.com` pages get traffic; sunset or redirect duplicates
   - Build a "deck survey" funnel that mirrors the modular `dream-home` quality of data capture
   - Migrate decking ads off `bivianocontractingroofs.com/deck-offer` onto the new deck funnel

3. **Phase 3 (longer-term):**
   - Decide on the future of `bivianomodularbuilders.com` — either route ads there (it has the calculator + town pages, better UX) or sunset it
   - Build a single "Master Lead Intake" workflow that replaces 5+ overlapping "new lead" workflows

---

## ❓ Decisions Spencer needs to make before I touch anything

1. **`bivianocontractingroofs.com`** — what is it, do you own it, can it be retired?
2. **`bivianomodularbuilders.com`** — kill it or activate it? It's currently dead but built with the calculator + better SEO structure.
3. **Decking funnel** — is `go.bivianocontracting.com/dream-decks` the canonical decking funnel, or is `bivianocontractingroofs.com/deck-offer` the one running ads?
4. **Calendar strategy** — should ALL bookings go through a survey first, or do you keep a "fast path" calendar for hot referrals like Shelagh?
5. **Mike's appetite for change** — this is a real cleanup. Some leads will be temporarily lost while ad flows are rerouted. Is he OK pausing/rebuilding ad campaigns to do it right?
