const { chromium } = require('/home/vin/.openclaw/workspaces/manager-bot/.tmp-playwright/node_modules/playwright');

(async() => {
  const browser = await chromium.launch({headless:true});
  const page = await browser.newPage();
  const slug = process.argv[2] || 'business-analyst-jobs';
  await page.goto(`https://it.jobserve.com/${slug}/`, {waitUntil:'networkidle', timeout: 90000});
  await page.waitForTimeout(5000);
  const html = await page.content();
  console.log('len', html.length);
  for (const pat of ['jobResultItem','jobTitle','jobDetails','jobViewItem','page 1 of','posted']) {
    console.log(pat, html.includes(pat));
  }
  console.log(html.slice(0,3000));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
