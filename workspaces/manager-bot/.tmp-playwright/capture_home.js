const { chromium } = require('/home/vin/.openclaw/workspaces/manager-bot/.tmp-playwright/node_modules/playwright');

(async() => {
  const browser = await chromium.launch({headless:true});
  const page = await browser.newPage();
  page.on('response', async resp => {
    if (resp.url().includes('/Home/GetJobs')) {
      console.log('GETJOBS status', resp.status());
      try {
        const txt = await resp.text();
        console.log('GETJOBS len', txt.length);
        console.log(txt.slice(0,3000));
      } catch (e) {
        console.log('GETJOBS err', e.message);
      }
    }
  });
  await page.goto('https://it.jobserve.com/', {waitUntil:'networkidle', timeout: 90000});
  await page.waitForTimeout(8000);
  console.log('cookies', JSON.stringify(await page.context().cookies()));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
