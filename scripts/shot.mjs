#!/usr/bin/env node
// Reliable full-page mobile screenshot using puppeteer-core + the installed Chrome.
// Usage: node shot.mjs <url> <outPath> [width=390] [--full|--clip=SELECTOR]
//   default: full-page capture at the given mobile width.
//   --clip=SELECTOR: capture only the element matching SELECTOR (great for one section).
import puppeteer from 'puppeteer-core';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const args = process.argv.slice(2);
const url = args[0];
const outPath = args[1];
const width = parseInt(args.find(a => /^\d+$/.test(a)) || '390', 10);
const clipSel = (args.find(a => a.startsWith('--clip=')) || '').split('=')[1] || null;
if (!url || !outPath) { console.error('usage: node shot.mjs <url> <out.png> [width] [--clip=SELECTOR]'); process.exit(2); }

const browser = await puppeteer.launch({
  executablePath: CHROME,
  headless: 'shell',
  args: ['--no-sandbox', '--hide-scrollbars', '--disable-gpu'],
});
try {
  const page = await browser.newPage();
  await page.emulate({
    viewport: { width, height: 800, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 }).catch(() => {});
  // Force reveals visible + eager-load all images, then let layout settle
  await page.evaluate(async () => {
    document.querySelectorAll('.reveal').forEach(e => { e.style.opacity = '1'; e.style.transform = 'none'; });
    document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; if (i.dataset.src) i.src = i.dataset.src; });
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(r => setTimeout(r, 800));
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 300));
  });
  try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch {}
  if (clipSel) {
    const el = await page.$(clipSel);
    if (!el) { console.error('clip selector not found: ' + clipSel); process.exit(1); }
    await el.screenshot({ path: outPath });
  } else {
    await page.screenshot({ path: outPath, fullPage: true });
  }
  console.log(`OK ${outPath} (w=${width}${clipSel ? ', clip=' + clipSel : ', full'})`);
} finally {
  await browser.close();
}
