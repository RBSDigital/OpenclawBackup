const { chromium } = require('/home/vin/.openclaw/workspaces/manager-bot/.tmp-playwright/node_modules/playwright');

(async() => {
  const browser = await chromium.launch({headless:true});
  const page = await browser.newPage();
  const slug = process.argv[2] || 'business-analyst-jobs';
  page.on('request', req => {
    console.log('REQ', req.method(), req.resourceType(), req.url());
  });
  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('jobserve.com')) {
      console.log('RESP', resp.status(), url);
    }
  });
  await page.goto(`https://it.jobserve.com/${slug}/`, {waitUntil:'networkidle', timeout: 90000});
  await page.waitForTimeout(10000);
  console.log('done');
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
