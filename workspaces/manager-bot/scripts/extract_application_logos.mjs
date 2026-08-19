#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { execFileSync } from 'node:child_process';
import sharp from 'sharp';

const OUT_DIR = process.env.OUT_DIR || path.resolve('application-logos-out');
const MANIFEST = process.argv[2];

if (!MANIFEST) {
  console.error('usage: extract_application_logos.mjs <manifest.json>');
  process.exit(1);
}

const manifest = JSON.parse(await fs.readFile(MANIFEST, 'utf8'));
await fs.mkdir(OUT_DIR, { recursive: true });

function slugify(name) {
  return name
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-');
}

function uniq(arr) {
  return [...new Set(arr.filter(Boolean))];
}

function fallbackText(entry) {
  if (/amasty/i.test(entry.name)) return 'AM';
  if (/ucc/i.test(entry.name)) return 'UCC';
  if (/microsoft fabric/i.test(entry.name)) return 'MF';
  if (/azure data factory/i.test(entry.name)) return 'ADF';
  if (/azure integration services/i.test(entry.name)) return 'AIS';
  return entry.fileName
    .split('-')
    .filter(Boolean)
    .map(part => part[0])
    .join('')
    .slice(0, 3)
    .toUpperCase();
}

async function writeFallbackBadge(entry, outPath) {
  const label = fallbackText(entry);
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
      <rect width="256" height="256" rx="52" fill="#111827"/>
      <rect x="16" y="16" width="224" height="224" rx="40" fill="#1f2937"/>
      <text x="128" y="148" font-family="Arial, Helvetica, sans-serif" font-size="70" font-weight="700" text-anchor="middle" fill="#ffffff">${label}</text>
    </svg>
  `;
  await toPng(Buffer.from(svg), `${entry.fileName}.svg`, outPath);
}

function scoreCandidate(url, context = '') {
  const s = `${url} ${context}`.toLowerCase();
  let score = 0;
  const preferred = [
    'logo', 'brand', 'wordmark', 'lockup', 'banner', 'mark', 'primary',
  ];
  const good = [
    'logos', 'brand-assets', 'brandassets', 'identity', 'official', 'download',
  ];
  const bad = [
    'favicon', 'touchicon', 'apple-touch', 'icon', 'social', 'ogimage', 'placeholder',
    'hero', 'thumbnail', 'sprite', 'avatar', 'spinner', 'motion', 'video', 'close',
    'arrow', 'play', 'pause', 'poster', 'bg-', 'background', 'ad-', 'banner-',
  ];
  for (const token of preferred) {
    if (s.includes(token)) score += 20;
  }
  for (const token of good) if (s.includes(token)) score += 10;
  for (const token of bad) if (s.includes(token)) score -= 20;
  if (s.includes('.png')) score += 4;
  if (s.includes('.webp')) score += 2;
  if (s.includes('.svg')) score += 5;
  if (s.includes('.zip')) score += 3;
  if (s.includes('logo')) score += 5;
  return score;
}

async function fetchText(url) {
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), 30000);
  try {
    const res = await fetch(url, {
      redirect: 'follow',
      signal: ac.signal,
      headers: {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',
        accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
    return await res.text();
  } finally {
    clearTimeout(timer);
  }
}

async function fetchBuffer(url) {
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), 30000);
  try {
    const res = await fetch(url, {
      redirect: 'follow',
      signal: ac.signal,
      headers: {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',
      },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
    const ab = await res.arrayBuffer();
    return Buffer.from(ab);
  } finally {
    clearTimeout(timer);
  }
}

function extractCandidates(html, pageUrl) {
  const urls = [];
  const patterns = [
    /https?:\/\/[^"'\\s>]+?\.(?:png|svg|webp|jpg|jpeg|zip)(?:\?[^"'\\s>]*)?/gi,
    /\/\/[^"'\\s>]+?\.(?:png|svg|webp|jpg|jpeg|zip)(?:\?[^"'\\s>]*)?/gi,
    /(?:src|href)=["']([^"']+\.(?:png|svg|webp|jpg|jpeg|zip)(?:\?[^"']*)?)["']/gi,
    /url\(["']?([^"')]+\.(?:png|svg|webp|jpg|jpeg|zip)(?:\?[^"')]+)?)["']?\)/gi,
  ];
  for (const re of patterns) {
    for (const m of html.matchAll(re)) {
      const raw = m[1] || m[0];
      if (raw.startsWith('data:')) continue;
      let url = raw;
      if (url.startsWith('//')) url = 'https:' + url;
      else if (url.startsWith('/')) url = new URL(url, pageUrl).href;
      else if (!/^https?:/i.test(url)) url = new URL(url, pageUrl).href;
      urls.push(url);
    }
  }
  const metaMatches = [...html.matchAll(/<meta[^>]+(?:content|value)=["']([^"']+)["'][^>]+(?:property|name)=["'](?:og:image|twitter:image)["'][^>]*>/gi)];
  for (const m of metaMatches) {
    let url = m[1];
    if (!/^https?:/i.test(url)) url = new URL(url, pageUrl).href;
    urls.push(url);
  }
  return uniq(urls);
}

function extractInlineSvgs(html) {
  const svgs = [];
  const re = /<svg\b[^>]*[\s\S]*?<\/svg>/gi;
  for (const m of html.matchAll(re)) {
    const svg = m[0];
    const head = svg.slice(0, 1000).toLowerCase();
    if (/(logo|wordmark|brand|lockup|mark)/.test(head) || svg.length < 10000) {
      svgs.push({ svg, score: scoreCandidate(svg, head) + 15 });
    }
  }
  return svgs;
}

async function unzipCandidates(zipBuffer, workDir) {
  const zipPath = path.join(workDir, 'bundle.zip');
  await fs.writeFile(zipPath, zipBuffer);
  const listJson = execFileSync('python3', ['-c', `
import io, json, sys, zipfile
with zipfile.ZipFile(sys.argv[1]) as z:
    print(json.dumps(z.namelist()))
`, zipPath], { encoding: 'utf8' });
  const list = JSON.parse(listJson);
  const interesting = list.filter(x => /\.(png|svg|webp|jpg|jpeg)$/i.test(x) && !/^__MACOSX\//i.test(x));
  const scored = interesting
    .map(x => ({
      x,
      score:
        scoreCandidate(x) +
        (/\.(png)$/i.test(x) ? 30 : 0) +
        (/\.(svg)$/i.test(x) ? 10 : 0) +
        (/\b(black|color|blue)\b/i.test(x) ? 8 : 0) -
        (/\bwhite\b/i.test(x) ? 4 : 0),
    }))
    .sort((a, b) => b.score - a.score || a.x.length - b.x.length);
  const chosen = scored[0]?.x || interesting[0];
  if (!chosen) throw new Error('no image files in zip');
  const out = execFileSync('python3', ['-c', `
import sys, zipfile
zip_path, member = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(zip_path) as z:
    sys.stdout.buffer.write(z.read(member))
`, zipPath, chosen]);
  return { buffer: Buffer.from(out), source: chosen };
}

async function toPng(inputBuffer, sourceName, outPath) {
  const ext = path.extname(sourceName).toLowerCase();
  let img = sharp(inputBuffer, { animated: false });
  if (ext === '.svg' || inputBuffer.toString('utf8', 0, 50).includes('<svg')) {
    img = sharp(inputBuffer, { density: 384 });
  }
  await img
    .resize(48, 48, {
      fit: 'contain',
      background: { r: 0, g: 0, b: 0, alpha: 0 },
      withoutEnlargement: false,
    })
    .png()
    .toFile(outPath);
}

function normalizeSvgBuffer(buffer) {
  let svg = buffer.toString('utf8');
  if (/xlink:href=/i.test(svg) && !/xmlns:xlink=/i.test(svg)) {
    svg = svg.replace(
      /<svg\b([^>]*)>/i,
      '<svg$1 xmlns:xlink="http://www.w3.org/1999/xlink">'
    );
  }
  svg = svg.replace(/\bxlink:href=/gi, 'href=');
  return Buffer.from(svg);
}

async function processEntry(entry) {
  const name = entry.name;
  const pageUrl = entry.url;
  const base = slugify(entry.fileName || name);
  const workDir = await fs.mkdtemp(path.join(os.tmpdir(), `${base}-`));
  try {
    if (/\.zip(?:\?|$)/i.test(pageUrl)) {
      const zipBuf = await fetchBuffer(pageUrl);
      const extracted = await unzipCandidates(zipBuf, workDir);
      const outPath = path.join(OUT_DIR, `${base}.png`);
      await toPng(extracted.buffer, extracted.source, outPath);
      return { name, pageUrl, chosen: extracted.source, outPath };
    }
    if (/\.(svg|png|webp|jpg|jpeg)(?:\?|$)/i.test(pageUrl) || /favicon(?:\?|$)/i.test(pageUrl)) {
      const buffer = await fetchBuffer(pageUrl);
      const outPath = path.join(OUT_DIR, `${base}.png`);
      const safeBuffer = pageUrl.includes('.svg') ? normalizeSvgBuffer(buffer) : buffer;
      await toPng(safeBuffer, pageUrl, outPath);
      return { name, pageUrl, chosen: 'direct-file', outPath };
    }

    const html = await fetchText(pageUrl);
    const candidates = extractCandidates(html, pageUrl)
      .map(url => ({ url, score: scoreCandidate(url, html) }))
      .sort((a, b) => b.score - a.score || a.url.length - b.url.length);
    const inlineSvgs = extractInlineSvgs(html);
    const preferredCandidates = candidates.filter(c => /logo|brand|wordmark|lockup|mark/i.test(c.url));
    const bestInlineSvg = inlineSvgs.sort((a, b) => b.score - a.score || a.svg.length - b.svg.length)[0];
    const bestCandidate = candidates[0];

    let chosen = null;
    let sourceName = null;
    let buffer = null;

    if (bestInlineSvg && (!bestCandidate || bestInlineSvg.score >= bestCandidate.score + 5)) {
      buffer = Buffer.from(bestInlineSvg.svg);
      sourceName = `${base}.svg`;
      chosen = 'inline-svg';
    } else if (preferredCandidates.length) {
      chosen = preferredCandidates[0].url;
    } else if (candidates.length) {
      chosen = candidates[0].url;
    }

    if (!buffer && chosen) {
      sourceName = chosen;
      if (/\.zip(?:\?|$)/i.test(chosen)) {
        const zipBuf = await fetchBuffer(chosen);
        const extracted = await unzipCandidates(zipBuf, workDir);
        buffer = extracted.buffer;
        sourceName = extracted.source;
      } else {
        buffer = await fetchBuffer(chosen);
      }
    }

    if (!buffer) {
      throw new Error(`no logo candidate found on ${pageUrl}`);
    }

    const outPath = path.join(OUT_DIR, `${base}.png`);
    const safeBuffer = sourceName && /\.svg(?:\?|$)/i.test(sourceName) ? normalizeSvgBuffer(buffer) : buffer;
    await toPng(safeBuffer, sourceName, outPath);
    return { name, pageUrl, chosen: chosen || 'inline-svg', outPath };
  } finally {
    await fs.rm(workDir, { recursive: true, force: true });
  }
}

const results = [];
const failures = [];

for (const entry of manifest) {
  try {
    const res = await processEntry(entry);
    results.push(res);
    console.log(`ok ${entry.name} -> ${path.basename(res.outPath)} via ${res.chosen}`);
  } catch (err) {
    const canFallback = /amasty|ucc/i.test(entry.name);
    if (canFallback) {
      const outPath = path.join(OUT_DIR, `${slugify(entry.fileName || entry.name)}.png`);
      await writeFallbackBadge(entry, outPath);
      results.push({ name: entry.name, pageUrl: entry.url, chosen: 'fallback-badge', outPath });
      console.log(`fallback ${entry.name} -> ${path.basename(outPath)} after ${err?.message || err}`);
      continue;
    }
    failures.push({ entry, error: String(err?.message || err) });
    console.error(`fail ${entry.name}: ${err?.message || err}`);
  }
}

await fs.writeFile(path.join(OUT_DIR, 'manifest.json'), JSON.stringify({ results, failures }, null, 2));
if (failures.length) {
  console.error(`completed with ${failures.length} failures`);
  process.exitCode = 2;
} else {
  console.log(`completed ${results.length} files`);
}
