const { chromium } = require('/home/vin/.openclaw/workspaces/manager-bot/.tmp-playwright/node_modules/playwright');

(async() => {
  const browser = await chromium.launch({headless:true});
  const pages = ['business-analyst-jobs','product-manager-jobs','solution-architecture-jobs','delivery-manager-jobs'];
  for (const slug of pages) {
    const page = await browser.newPage();
    await page.goto(`https://it.jobserve.com/${slug}/`, {waitUntil:'networkidle', timeout: 90000});
    await page.waitForTimeout(5000);
    console.log('###', slug, page.url());
    const body = await page.locator('body').innerText().catch(e => 'ERR:' + e.message);
    console.log(body.slice(0,4000));
    await page.close();
  }
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
