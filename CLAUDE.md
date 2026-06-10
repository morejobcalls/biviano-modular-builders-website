# Biviano Modular Builders (BMB) — Site Build Context

**Live domain:** bivianomodularbuilders.com  
**GitHub repo:** https://github.com/morejobcalls/Biviano-Modular-Website  
**Local path:** `/Volumes/T7/SPG/3. FULFILLMENT/Clients/BIVIANO/07 - Websites/Modular/`

---

## Business Context

**Client:** Mike Biviano Jr., Owner — Biviano General Contracting LLC  
**Brand:** Biviano Modular Builders (BMB) — separate modular-only brand  
**Address:** 2183 Ocean Street, Marshfield, MA 02050  
**Phone:** (617) 678-6446 · `tel:+16176786446`  
**Email:** info@bivianocontracting.com  
**Main site:** bivianocontracting.com  

**The pitch:** "Move into your custom dream home in 12 weeks for 25% less than traditional construction."  
- $300/sq ft vs $400+ stick-built  
- 8–12 week build time vs 12–15 months  
- One GC handles everything: design, permits, foundation, factory build, crane, finish work, inspection  
- 4th-generation family contractor, South Shore MA since the 1960s  
- Serving: Marshfield, Scituate, Duxbury, Hanover, Pembroke, Norwell, Hingham, Humarock, Plymouth County  

**Core mechanism:** "The 12-Week Dream Home System" — factory precision + site prep happen simultaneously, eliminating weather delays and contractor chaos.

**Proof/credentials:**
- 21 five-star reviews (Birdeye)  
- MA CSL #CS-108728 (Construction Supervisor)  
- MA HIC Reg. #181337  
- BuildZoom Score 101 (Top 12% of 139,240 MA licensed contractors)  
- Former Marshfield Planning Board Chair — knows every inspector  

**Avatar:** Married couple 35–55, $150K+ HH income, Plymouth County MA, been quoted $1M+ by stick-built contractors, scared of 12+ month timeline, worried "modular = trailer," has land or is close to buying  

---

## Design System

**DO NOT deviate from this.** All new pages must match exactly.

### Colors
```css
--coal:        #111110;   /* page background */
--coal-mid:    #1C1C1A;   /* card/section backgrounds */
--coal-light:  #2A2A27;   /* elevated elements */
--stone:       #8C7B6B;   /* secondary text */
--stone-light: #BBA898;   /* subtle text */
--stone-pale:  #E8DDD5;   /* very light accent */
--sand:        #F0E8DF;
--cream:       #FAF7F4;
--blue:        #4A90C4;   /* PRIMARY accent — CTAs, highlights */
--blue-mid:    #3A7EBF;
--blue-pale:   rgba(74,144,196,0.12);
--white:       #FFFFFF;
--rule-dark:   rgba(255,255,255,0.07);
--rule-light:  rgba(0,0,0,0.08);
```

### Typography
```
Bebas Neue      — display headings, CTAs, labels (ALL CAPS feel)
Libre Baskerville — editorial serif, pull quotes, emphasis italic
Outfit          — body copy, UI, nav, small text (weights: 200, 300, 400, 500)
```

Google Fonts link (copy into every `<head>`):
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Outfit:wght@200;300;400;500&display=swap" rel="stylesheet">
```

### Tone
- Direct, no-BS, human
- Specific numbers always (not "faster" — "8–12 weeks")
- Never "agency speak" — write like a contractor-side partner
- Oxford commas, em dashes OK, but don't overuse

---

## File Structure — Current Status

```
Modular/
├── index.html           ✅ COMPLETE — homepage (hero, what-is, advantages, process, testimonials, FAQ, CTA form, footer)
├── towns.css            ✅ COMPLETE — shared stylesheet for all 8 town pages
├── logo.png             ✅ present
├── logo-crest.png       ✅ present
├── sitemap.xml          ⚠️  needs updating — missing 4 new pages
├── CNAME                ✅ bivianomodularbuilders.com
│
├── marshfield/index.html  ✅ COMPLETE
├── scituate/index.html    ✅ COMPLETE
├── humarock/index.html    ✅ COMPLETE
├── duxbury/index.html     ✅ COMPLETE
├── hanover/index.html     ✅ COMPLETE
├── pembroke/index.html    ✅ COMPLETE
├── norwell/index.html     ✅ COMPLETE
├── hingham/index.html     ✅ COMPLETE
│
├── why-modular/index.html  ❌ NOT YET BUILT
├── process/index.html      ❌ NOT YET BUILT
├── pricing/index.html      ❌ NOT YET BUILT
├── gallery/index.html      ❌ NOT YET BUILT
│
└── content/                ❌ NOT YET CREATED (scraped content folder)
```

---

## GHL Integration

**Webhook (form submissions go here):**
```
https://services.leadconnectorhq.com/hooks/zPo4vLlEjjXCflgDSXlI/webhook-trigger/0eba93d2-0fb2-4770-9af2-4e912dc84502
```

**Custom field keys:**
- `contact.bmb_home_size` — home size (sqft range)
- `contact.bmb_town` — town/city
- `contact.bmb_project_description` — project description

**Payload format for all forms:**
```javascript
{
  firstName: "...",
  lastName: "...",
  email: "...",
  phone: "...",
  customField: {
    'contact.bmb_home_size': "...",
    'contact.bmb_town': "...",
    'contact.bmb_project_description': "..."
  },
  source: 'BMB Website',
  tags: ['bmb-website', 'consultation-request']
}
```

---

## Nav HTML (copy exactly into every new page — update href paths for depth)

For root-level pages (`/why-modular/`, `/process/`, etc.) — all links point to `/#anchor`:

```html
<nav id="navbar" role="navigation" aria-label="Main navigation">
  <a href="/" class="nav-logo" aria-label="Biviano Modular Builders — home">
    <img src="/logo-crest.png" class="nav-crest-img" alt="" aria-hidden="true">
    <div>
      <div class="nav-name">Biviano</div>
      <div class="nav-sub">Modular Builders</div>
    </div>
  </a>
  <ul class="nav-links">
    <li><a href="/#what-is">What Is Modular</a></li>
    <li><a href="/#advantages">Why BMB</a></li>
    <li><a href="/process/">Process</a></li>
    <li><a href="/why-modular/">Why Modular</a></li>
    <li><a href="/pricing/">Pricing</a></li>
    <li class="has-dropdown">
      <a href="#" aria-haspopup="true" aria-expanded="false">Service Areas</a>
      <div class="nav-dropdown" role="menu">
        <a href="/marshfield/" role="menuitem">Marshfield</a>
        <a href="/scituate/" role="menuitem">Scituate</a>
        <a href="/humarock/" role="menuitem">Humarock</a>
        <a href="/duxbury/" role="menuitem">Duxbury</a>
        <a href="/hanover/" role="menuitem">Hanover</a>
        <a href="/pembroke/" role="menuitem">Pembroke</a>
        <a href="/norwell/" role="menuitem">Norwell</a>
        <a href="/hingham/" role="menuitem">Hingham</a>
      </div>
    </li>
  </ul>
  <a href="/#consult" class="nav-cta">Begin Your Build</a>
  <button class="nav-hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
    <span></span><span></span><span></span>
  </button>
</nav>
<nav class="mobile-menu" id="mobile-menu" aria-label="Mobile navigation" aria-hidden="true">
  <a href="/#what-is">What Is Modular</a>
  <a href="/#advantages">Why BMB</a>
  <a href="/process/">Our Process</a>
  <a href="/why-modular/">Why Modular</a>
  <a href="/pricing/">Pricing</a>
  <div class="mobile-section-label">Service Areas</div>
  <a href="/marshfield/" class="mobile-town-link">Marshfield</a>
  <a href="/scituate/" class="mobile-town-link">Scituate</a>
  <a href="/duxbury/" class="mobile-town-link">Duxbury</a>
  <a href="/hanover/" class="mobile-town-link">Hanover</a>
  <a href="/pembroke/" class="mobile-town-link">Pembroke</a>
  <a href="/norwell/" class="mobile-town-link">Norwell</a>
  <a href="/hingham/" class="mobile-town-link">Hingham</a>
  <a href="/#consult" class="mobile-cta">Begin Your Build →</a>
</nav>
```

## Footer HTML (copy exactly — same for all new pages)

```html
<footer>
  <div class="footer-inner">
    <div class="footer-top">
      <div>
        <div class="footer-brand-name">Biviano</div>
        <div class="footer-brand-sub">Modular Builders</div>
        <p class="footer-tagline">Precision-built custom homes for Plymouth County families — delivered in 12 weeks, for 25% less, by a contractor family serving the South Shore since the 1960s.</p>
        <div class="footer-areas">
          <strong>Service Areas</strong>
          Marshfield · Hanover · Pembroke · Scituate<br>
          Duxbury · Kingston · Hull · Humarock<br>
          Plymouth County, MA
        </div>
      </div>
      <div>
        <div class="footer-col-title">Explore</div>
        <ul class="footer-links">
          <li><a href="/why-modular/">Why Modular</a></li>
          <li><a href="/process/">Our 5-Step Process</a></li>
          <li><a href="/pricing/">Pricing & Timelines</a></li>
          <li><a href="/gallery/">Project Gallery</a></li>
          <li><a href="/#faq">FAQ</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Build With Us</div>
        <ul class="footer-links">
          <li><a href="/#consult">Free Consultation</a></li>
          <li><a href="/#consult">Cost Breakdown Report</a></li>
          <li><a href="https://www.bivianocontracting.com/gallery" target="_blank" rel="noopener noreferrer">All Projects</a></li>
          <li><a href="https://www.bivianocontracting.com/testimonials" target="_blank" rel="noopener noreferrer">All Testimonials</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Contact</div>
        <ul class="footer-links">
          <li><a href="tel:+16176786446">(617) 678-6446</a></li>
          <li><a href="mailto:info@bivianocontracting.com">info@bivianocontracting.com</a></li>
          <li><a href="https://www.bivianocontracting.com" target="_blank" rel="noopener noreferrer">bivianocontracting.com</a></li>
          <li><a href="https://reviews.birdeye.com/biviano-general-contracting-llc-167479265849097" target="_blank" rel="noopener noreferrer">Read Our Reviews</a></li>
          <li><a href="https://www.facebook.com/bivianocontracting" target="_blank" rel="noopener noreferrer">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">© 2025 Biviano General Contracting LLC. All rights reserved. &nbsp;·&nbsp; Marshfield, MA 02050</div>
      <div class="footer-lic">MA HIC Reg. #181337 · MA CSL #CS-108728 &nbsp;·&nbsp; HIC Registered &nbsp;·&nbsp; Licensed · Bonded · Insured</div>
    </div>
  </div>
</footer>
```

## Standard JavaScript (copy into every new page)

```html
<script>
  const revealEls = document.querySelectorAll('.reveal');
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); revealObs.unobserve(e.target); }
    });
  }, { threshold: 0.08 });
  revealEls.forEach(el => revealObs.observe(el));

  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 72;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });

  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');
  if (hamburger) {
    hamburger.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      hamburger.classList.toggle('open', isOpen);
      hamburger.setAttribute('aria-expanded', String(isOpen));
      mobileMenu.setAttribute('aria-hidden', String(!isOpen));
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      });
    });
  }
</script>
```

## Reveal Animation Class

Any element with class `reveal` will fade-in-up on scroll. Add this CSS to new pages:
```css
.reveal { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
.reveal.visible { opacity: 1; transform: none; }
```

---

## Key Copy / Numbers (use exactly — do not invent)

| Stat | Value |
|------|-------|
| Build time | 8–12 weeks |
| Cost savings | 20–25% less than stick-built |
| Dollar savings | $200,000–$300,000 |
| BMB cost | ~$300/sq ft |
| Stick-built cost | $400–$600/sq ft |
| Design plan cost (BMB) | ~$2,500 |
| Stick-built arch plans | $20,000–$30,000 |
| Reviews | 21 five-star reviews |
| Experience | 40+ years, 4th generation |

## Top Objections to Address in Copy

1. "Modular = trailer / low quality" — they look identical to custom stick-built, built to same codes, permanent foundations
2. "Can't finance it" — standard construction loans, same banks, same process
3. "Timeline seems too good" — parallel build (factory + site simultaneously) explains it
4. "What if something goes wrong?" — single GC, local family, 40 years reputation, everyone in town knows Mike
5. "Resale value" — appraises identically, appreciates normally, no stigma on permanent foundation

## Testimonials (use in pages)

1. **Speed/Emergency:** "After a snowstorm, my porch collapsed and town officials said my house was unsafe. I called Mike and he immediately took action. One day later his crew completed everything required by the town to allow me to return to my house. I have found a contractor for life!"
2. **Quality/Service:** "From the suggestions Mike comes up with that I never would have thought of, to the handholding throughout the process I can't thank you enough. My dream kitchen and baths are complete. Honest, knowledgeable and prompt are the words I use to describe Mike Biviano and his crew." — Susan R.
3. **Trust/Single Mother:** "As a single mother, it can be difficult to find a contractor I can truly trust, but Mike and his team have consistently come through for me, even during tough times. Their work is top-notch."
4. **Speed on smaller job:** "Mike and his company took exceptional care of my father's house and did it so fast I couldn't believe it! We needed laundry moved from basement to 2nd floor. Mike made this happen in under 2 weeks during the holidays."
5. **Referral proof:** "We asked our excellent electrician Kevin Litchfield who he would recommend. He said, 'Call Mike Biviano...he's the man for the job!' We did, and are so glad that we trusted Mike and his crew."
6. **Full home build:** "Building our new house in Humarock with Mike Biviano was a happily ever after journey." — Joanne Keogh
7. **Deck:** "Mike and his crew did a great job expanding and remodeling our kitchen. We love it!" — Jenny Hol

---

## The 12-Week Dream Home System (5 Steps)

**Step 1 — Design Your Dream**
Free consultation → custom modular plans for ~$2,500 (vs $20–30K for traditional architectural plans). 100% custom layouts, not cookie-cutter.

**Step 2 — Lock In Your Price & Timeline**
Detailed, itemized quote covering everything — design, permits, site work, foundation, crane, assembly, final inspection. Price and 8–12 week timeline locked in writing.

**Step 3 — Factory-Build While We Prep Your Site**
Modules precision-built in climate-controlled factory simultaneously with site work, foundation, permits. That's why 12 weeks instead of 12 months.

**Step 4 — Crane, Assemble & Finish**
Modules delivered and craned into place in one day. Crew completes all finishes, utilities hookup, final touches. Mike manages every detail.

**Step 5 — Move Into Your Forever Home**
Final inspection → keys in hand → you're in while neighbors with stick-built are still 9+ months out.

---

## Agent Task Map

| Agent | Task | Files to Create/Edit |
|-------|------|---------------------|
| Agent 1 | Build `/why-modular/` page | `why-modular/index.html` |
| Agent 2 | Build `/process/` page | `process/index.html` |
| Agent 3 | Build `/pricing/` page | `pricing/index.html` |
| Agent 4 | Build `/gallery/` page | `gallery/index.html` |
| Agent 5 | Scrape content → `content/` folder | `content/` directory |
| Agent 6 | GitHub deployment | git push, Pages config |

**CRITICAL — no agent touches a file another agent owns. Each agent works only on their assigned files.**

---

## How to Build a New Page

1. Copy the `<head>` from `index.html` (lines 1–122) — update title, description, canonical URL, OG tags
2. Copy the design system CSS from `index.html` (lines 123–1599) — it contains all CSS needed
3. Copy the nav HTML (see above)
4. Write your page-specific content sections
5. Copy the footer HTML (see above)
6. Copy the standard JS (see above)
7. Each section: use class `reveal` on key elements for scroll animation

**Page structure to follow:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- SEO meta (page-specific) -->
  <!-- Fonts link -->
  <!-- Schema markup (page-specific LocalBusiness) -->
  <style>
    /* Paste full CSS from index.html */
    /* Add any page-specific styles at bottom */
  </style>
</head>
<body>
  <!-- Nav (from above) -->
  <!-- Mobile Menu (from above) -->
  
  <!-- PAGE HERO -->
  <section class="interior-hero" style="padding: 160px 56px 80px; background: var(--coal-mid); border-bottom: 1px solid var(--rule-dark);">
    ...
  </section>
  
  <!-- CONTENT SECTIONS -->
  ...
  
  <!-- CTA SECTION — copy from index.html (the consult section) -->
  
  <!-- Footer (from above) -->
  <!-- JS (from above) -->
</body>
</html>
```

---

## Images

All images currently use Unsplash. Use these sources for modular/home photos:
- `https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=1200&q=80` — suburban home
- `https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=1200&q=80` — modern home interior
- `https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1200&q=80` — house exterior
- `https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=1200&q=80` — construction/building
- `https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=1200&q=80` — modern house
- `https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1200&q=80` — luxury home

Add `?w=1200&q=80&auto=format&fit=crop` to all Unsplash URLs. Always add `loading="lazy"` except hero (use `fetchpriority="high"`).
