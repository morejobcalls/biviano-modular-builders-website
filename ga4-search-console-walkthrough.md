---
name: GA4 verification + Search Console submission walkthrough
created: 2026-05-27
status: ready-to-execute
owner: Spencer
related:
  - HANDOFF.md
---

# GA4 Verification + Search Console Submission

**Goal:** Confirm GA4 is firing on `bivianomodularbuilders.com`, then submit the sitemap to Google Search Console. Two short tasks.

**Confirmed by site audit (today):** GA4 snippet (`G-GW5Z0VVDEC`) appears twice on the homepage and twice on `/pricing/`. The plumbing is correct. We just need a human in a browser to verify Realtime is receiving hits.

**Total UI time:** 5-7 minutes.

---

## Part 1 — Verify GA4 Realtime (2 min)

1. **Open Chrome in an incognito window** (rules out ad blockers / Brave Shields / Privacy Badger from blocking the GA4 collect endpoint).
2. Open https://www.bivianomodularbuilders.com in tab A.
3. In tab B, open https://analytics.google.com → **Reports → Realtime**.
4. Confirm the property selector (top-left) shows `Biviano Modular Builders` (not `Biviano Contracting`).
5. Realtime should show **1 active user** within 30–90 seconds. Click around the site (homepage → /pricing/ → /why-modular/) and watch the "Users by page title" widget update.

### If Realtime is empty after 90 seconds
1. Hard-refresh the site: `Cmd+Shift+R`
2. DevTools → Network tab → filter `google` → reload. You should see:
   - `gtag/js?id=G-GW5Z0VVDEC` (the loader)
   - `g/collect?...` (the hit)
3. If neither fires → ad blocker is the cause. Try from your phone on cellular data.
4. If both fire but Realtime stays empty → check property selection in GA4. Easy to be on the wrong property.

---

## Part 2 — Submit sitemap to Search Console (5 min)

1. Open https://search.google.com/search-console
2. Top-left dropdown → **Add property**
3. Choose **URL prefix** type → enter `https://www.bivianomodularbuilders.com/` → Continue
   ⚠️ **Use the `www` host, NOT the apex.** Re-verified 2026-06-02: all 22 sitemap `<loc>` URLs use `www`. A URL-prefix property treats apex and `www` as different sites, so submitting this sitemap under an apex property triggers "URLs not under property" warnings. Match the property to the sitemap (`www`).
4. **Verify ownership** → choose **Google Analytics** as the verification method → Verify
   *(This works because you're signed into the same Google account that owns GA4 property `G-GW5Z0VVDEC`. If GA verification fails, fall back to DNS TXT record at GoDaddy or HTML tag.)*
5. Once verified → left sidebar → **Sitemaps**
6. Under "Add a new sitemap" → enter `sitemap.xml` → **Submit**
7. Status should show "Success" within seconds. Discovered URLs: 22.

> Alternative (cleaner long-term): add a **Domain property** (`bivianomodularbuilders.com`) instead of URL-prefix — it covers apex + `www` + all subdomains in one, so the host mismatch disappears entirely. Trade-off: Domain properties require **DNS TXT verification** (can't use the one-click GA method). For close-out speed, the `www` URL-prefix above is fine.

---

## Done state

- GA4 Realtime confirmed firing on at least one page
- `bivianomodularbuilders.com` property added in Search Console + verified
- `sitemap.xml` submitted + Success status

Both of these complete the "fully activated" deliverable for the modular rebrand close-out.
