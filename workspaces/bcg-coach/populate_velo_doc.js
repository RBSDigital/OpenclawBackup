const fs = require('fs');
const https = require('https');

const docId = process.argv[2];
const tokenPath = process.argv[3];
const reportPath = process.argv[4];
const clientPath = '/home/vin/.config/gogcli/credentials.json';

function request(url, options, body) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        let parsed;
        try { parsed = JSON.parse(data); } catch { parsed = data; }
        if (res.statusCode >= 200 && res.statusCode < 300) resolve(parsed);
        else reject(new Error(`HTTP ${res.statusCode}: ${typeof parsed === 'string' ? parsed.slice(0, 300) : JSON.stringify(parsed).slice(0, 500)}`));
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

function plainReport(markdown) {
  return markdown
    .replace(/^---\n[\s\S]*?\n---\n/, '')
    .split('\n')
    .map(line => {
      if (/^\|---/.test(line)) return '';
      if (/^\|/.test(line)) return line.replace(/^\|\s*/, '').replace(/\s*\|$/, '').replace(/\s*\|\s*/g, '  •  ');
      return line.replace(/^#{1,6}\s*/, '').replace(/\*\*/g, '').replace(/`/g, '');
    })
    .join('\n')
    .replace(/\n{3,}/g, '\n\n');
}

(async () => {
  const rawClient = JSON.parse(fs.readFileSync(clientPath, 'utf8'));
  const client = rawClient.installed || rawClient.web || rawClient;
  const exported = JSON.parse(fs.readFileSync(tokenPath, 'utf8'));
  const refreshToken = [REDACTED_SECRET]
  const tokenBody = new URLSearchParams({
    client_id: client.client_id,
    client_secret: [REDACTED_SECRET],
    refresh_token: [REDACTED_SECRET],
    grant_type: 'refresh_token'
  }).toString();
  const token = [REDACTED_SECRET] request('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': Buffer.byteLength(tokenBody)}
  }, tokenBody);

  const text = plainReport(fs.readFileSync(reportPath, 'utf8')) + '\n';
  const lines = text.split('\n');
  const requests = [{insertText: {location: {index: 1}, text}}];
  let index = 1;
  for (const line of lines) {
    const start = index;
    const end = index + line.length;
    if (/^VELO UK Website/.test(line)) {
      requests.push({updateParagraphStyle: {range: {startIndex: start, endIndex: end + 1}, paragraphStyle: {namedStyleType: 'TITLE'}, fields: 'namedStyleType'}});
    } else if (/^\d+\. /.test(line) || /^Executive summary$/.test(line) || /^Recommendation$/.test(line) || /^Sources$/.test(line) || /^Portfolio analysis$/.test(line) || /^Website and digital experience assessment$/.test(line) || /^Consulting analysis using POPIT$/.test(line) || /^Options$/.test(line) || /^Recommendation and next steps$/.test(line) || /^Evidence gaps and validation plan$/.test(line) || /^Peer-review checklist and conclusion$/.test(line)) {
      requests.push({updateParagraphStyle: {range: {startIndex: start, endIndex: end + 1}, paragraphStyle: {namedStyleType: line.match(/^\d+\./) ? 'HEADING_1' : 'HEADING_1'}, fields: 'namedStyleType'}});
    } else if (/^### /.test(line)) {
      requests.push({updateParagraphStyle: {range: {startIndex: start, endIndex: end + 1}, paragraphStyle: {namedStyleType: 'HEADING_2'}, fields: 'namedStyleType'}});
    }
    index = end + 1;
  }
  const apiBody = JSON.stringify({requests});
  await request(`https://docs.googleapis.com/v1/documents/${docId}:batchUpdate`, {
    method: 'POST',
    headers: {'Authorization': `Bearer ${token.access_token}`, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(apiBody)}
  }, apiBody);
  console.log(JSON.stringify({status: 'updated', docId, characters: text.length, requests: requests.length}));
})().catch(err => { console.error(err.message); process.exit(1); });
