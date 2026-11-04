// Print one book page (file URL) to PDF with Chromium: node print.js <file-url> <out.pdf>
const { chromium } = require('playwright');
(async () => {
  const [url, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const problems = [];
  page.on('pageerror', e => problems.push(String(e)));
  page.on('requestfailed', r => problems.push('failed: ' + r.url().slice(0, 120)));
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForSelector('body[data-ready="1"]', { timeout: 60000 });
  const check = await page.evaluate(() => ({
    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).filter((v, i, a) => a.indexOf(v) === i),
    overflow: [...document.querySelectorAll('.words,.card.end,.card.notes')].filter(w => w.scrollHeight > w.clientHeight + 1).length,
    cards: document.querySelectorAll('.card').length,
    broken: [...document.images].filter(i => !i.naturalWidth).map(i => i.src.slice(-60)),
  }));
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  console.log(JSON.stringify({ ...check, problems }));
  await browser.close();
  if (problems.length || check.broken.length || check.overflow) process.exitCode = 2;
})();
