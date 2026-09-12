const fs = require('fs');
const https = require('https');

const tokenPath = process.argv[2];
const docxPath = process.argv[3];
const parentId = process.argv[4];
const title = process.argv[5];

function request(url, options, body) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        let parsed;
        try { parsed = JSON.parse(data); } catch { parsed = data; }
        if (res.statusCode >= 200 && res.statusCode < 300) resolve(parsed);
        else reject(new Error(`HTTP ${res.statusCode}: ${typeof parsed === 'string' ? parsed.slice(0, 300) : JSON.stringify(parsed).slice(0, 600)}`));
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

(async () => {
  const exported = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
  const creds = JSON.parse(fs.readFileSync('/home/vin/.config/gogcli/credentials.json', 'utf8'));
  const form = new URLSearchParams({
    client_id: creds.client_id,
    client_secret: [REDACTED_SECRET],
    refresh_token: [REDACTED_SECRET],
    grant_type: 'refresh_token'
  }).toString();
  const tok = await request('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': Buffer.byteLength(form)}
  }, form);

  const boundary = `velo_${Date.now()}`;
  const metadata = JSON.stringify({name: title, mimeType: 'application/vnd.google-apps.document', parents: [parentId]});
  const media = fs.readFileSync(docxPath);
  const pre = Buffer.from(`--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${metadata}\r\n--${boundary}\r\nContent-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document\r\n\r\n`);
  const post = Buffer.from(`\r\n--${boundary}--\r\n`);
  const body = Buffer.concat([pre, media, post]);
  const result = await request('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,mimeType,parents,webViewLink', {
    method: 'POST',
    headers: {'Authorization': `Bearer ${tok.access_token}`, 'Content-Type': `multipart/related; boundary=${boundary}`, 'Content-Length': body.length}
  }, body);
  console.log(JSON.stringify(result));
})().catch(err => { console.error(err.message); process.exit(1); });
