/* ═══════════════════════════════════════════════════════════════════════════
   BMB shared ad-attribution + lead-conversion module          (2026-07-31)

   WHY THIS EXISTS
   The content pages (/adu/, /pricing/, /process/, /modular-vs-stick-built/)
   all had working lead forms that POST to GHL — but they captured no click ID
   and fired no conversion event. So a lead from any of them was invisible to
   Google Ads and unattributable in GHL. Meanwhile /free-consultation/ did all
   of this correctly. This module lifts that logic into one place so every page
   behaves identically.

   Google grades Landing Page Experience BELOW_AVERAGE on every non-brand
   keyword and ABOVE_AVERAGE on brand — same URL. The plan is to route
   research-intent ad groups to these content pages instead of the booking
   gate. That only works if the content pages can actually be measured.

   USAGE
     <script src="/js/bmb-attribution.js"></script>
     ...
     var payload = Object.assign({ firstName: ..., }, bmbAttr());
     bmbFireLead(email, phone);

   Exposes: window.bmbAttr()  window.bmbFireLead()  window.bmbAttrCustomFields()
   ═══════════════════════════════════════════════════════════════════════════ */
(function (w, d) {
  'use strict';

  var AW_ID       = 'AW-16742219835';
  var LEAD_LABEL  = 'AW-16742219835/yisSCKuX9rscELuAqK8-';  // "Modular — LP Lead" ($300)
  var STORE_KEY   = 'bmb_attr';
  var TTL_DAYS    = 90;

  var CLICK_IDS = ['gclid', 'gbraid', 'wbraid'];
  var UTMS      = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  var ALL       = CLICK_IDS.concat(UTMS);

  function readStore() {
    try {
      var raw = w.localStorage.getItem(STORE_KEY);
      if (!raw) return null;
      var o = JSON.parse(raw);
      if (!o || !o.t) return null;
      if (Date.now() - o.t > TTL_DAYS * 864e5) { w.localStorage.removeItem(STORE_KEY); return null; }
      return o.v || null;
    } catch (e) { return null; }
  }

  function writeStore(v) {
    try { w.localStorage.setItem(STORE_KEY, JSON.stringify({ t: Date.now(), v: v })); } catch (e) {}
  }

  /* Capture on load. A fresh click ID in the URL always wins; otherwise fall
     back to whatever we stored (visitor clicked an ad, browsed, then converted
     on a different page — the click ID is only ever in the first URL). */
  var captured = (function () {
    var qs = {}, stored = readStore() || {}, out = {}, sawClickId = false;
    try {
      new URLSearchParams(w.location.search).forEach(function (v, k) { qs[k.toLowerCase()] = v; });
    } catch (e) {}

    CLICK_IDS.forEach(function (k) { if (qs[k]) sawClickId = true; });

    ALL.forEach(function (k) {
      // On a fresh ad click, take the whole URL set (don't blend with a stale session).
      out[k] = sawClickId ? (qs[k] || '') : (qs[k] || stored[k] || '');
    });

    if (sawClickId || Object.keys(stored).length === 0) {
      if (ALL.some(function (k) { return out[k]; })) writeStore(out);
    }
    return out;
  })();

  /* Flat top-level keys — matches what /free-consultation/ sends.
     NOTE: deliberately does NOT set bmb_source. That maps to a RADIO field
     (contact.bmb_source) whose value each page already sets explicitly
     ("ADU page", "Consultation form", …). Overwriting it with a free-text
     value would clobber a controlled vocabulary. */
  w.bmbAttr = function () {
    var o = {};
    ALL.forEach(function (k) { o[k] = captured[k] || ''; });
    o.page_path = d.location.pathname;
    return o;
  };

  /* GHL customField form, so the click ID lands even if the inbound-webhook
     workflow maps customField rather than top-level keys. Belt and braces —
     whichever the workflow reads, it's present.

     Field keys verified against the BMB location's 58 custom fields on
     2026-07-31 — every key below exists as a TEXT field. Do not invent keys
     here; an unknown fieldKey risks the whole payload being rejected.

     ⚠️ VERIFIED 2026-07-31 — THESE DO NOT LAND YET. A live end-to-end submit
     created the contact with name/email/phone only: source was null, tags came
     back as ['source:manual-entry'] instead of what was sent, and ZERO custom
     fields were populated. The inbound-webhook workflow behind hook
     0eba93d2-0fb2-4770-9af2-4e912dc84502 maps only the four standard fields and
     discards the rest of the payload — which is why every lead from these pages
     has always arrived with no town, no project details and no source.
     Someone must map these in the GHL workflow UI (Forms+Workflows API is
     IAM-blocked in this sub-account). Sending them here is harmless and is the
     prerequisite for that mapping — the keys must appear in a captured sample
     before GHL's field picker will offer them.

     The Google Ads conversion below is NOT affected by any of this — it is
     client-side and works the moment this ships. */
  w.bmbAttrCustomFields = function () {
    var cf = {};
    if (captured.gclid)        cf['contact.contact_gclid'] = captured.gclid;
    if (captured.utm_source)   cf['contact.utm_source']    = captured.utm_source;
    if (captured.utm_medium)   cf['contact.utm_medium']    = captured.utm_medium;
    if (captured.utm_campaign) cf['contact.utm_campaign']  = captured.utm_campaign;
    if (captured.utm_term)     cf['contact.utm_term']      = captured.utm_term;
    if (captured.utm_content)  cf['contact.utm_content']   = captured.utm_content;
    return cf;
  };

  /* Fire the Google Ads lead conversion + GA4 event. Safe to call when gtag
     hasn't loaded (ad blocker, script failure) — never throws into the caller,
     and never blocks the form's own success path. Deduped per page view. */
  w.bmbFireLead = function (email, phone) {
    if (w.__bmbLeadFired) return;
    w.__bmbLeadFired = true;
    try {
      if (typeof w.gtag !== 'function') return;

      // Enhanced conversions — improves match rate when cookies are missing.
      if (email || phone) {
        try { w.gtag('set', 'user_data', { email: email || undefined, phone_number: phone || undefined }); } catch (e) {}
      }

      var payload = { send_to: LEAD_LABEL, value: 300.0, currency: 'USD' };
      if (captured.gclid) payload.transaction_id = captured.gclid;
      w.gtag('event', 'conversion', payload);
      w.gtag('event', 'generate_lead', { currency: 'USD', value: 300.0 });
    } catch (e) {}
  };

  /* Expose for debugging: bmbAttrDebug() in the console shows what was captured. */
  w.bmbAttrDebug = function () { return { captured: captured, stored: readStore() }; };
})(window, document);
