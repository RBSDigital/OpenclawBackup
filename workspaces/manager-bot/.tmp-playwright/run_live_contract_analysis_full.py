from __future__ import annotations

import concurrent.futures as cf
import csv
import json
import re
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from jobserve_contract_analysis import detail, parse_posted_age

BASE = 'https://it.jobserve.com'
TARGETS = [
    'Digital Business Analyst',
    'System Analyst',
    'Business Analyst',
    'Product Manager',
    'Product Owner',
    'Delivery Manager',
    'AI Agentic Analyst',
    'Agentic Engineer',
    'Solution Architect',
]
ALIASES = {
    'Digital Business Analyst': ['digital business analyst', 'data business analyst', 'junior business analyst'],
    'System Analyst': ['system analyst', 'systems analyst'],
    'Business Analyst': ['business analyst'],
    'Product Manager': ['product manager', 'technical product manager', 'product lead', 'head of product'],
    'Product Owner': ['product owner'],
    'Delivery Manager': ['delivery manager', 'service delivery manager', 'lead delivery manager', 'agile delivery manager', 'programme and delivery manager', 'product delivery manager'],
    'AI Agentic Analyst': ['ai agentic analyst', 'agentic analyst'],
    'Agentic Engineer': ['agentic engineer', 'ai agentic engineer'],
    'Solution Architect': ['solution architect', 'solutions architect', 'enterprise solution architect', 'solution architecture'],
}
OUT_CSV = Path('/home/vin/.openclaw/workspaces/manager-bot/contract_analysis_jobserve.csv')
OUT_JSON = Path('/home/vin/.openclaw/workspaces/manager-bot/contract_analysis_jobserve.json')
SHEET_VALUES = Path('/home/vin/.openclaw/workspaces/manager-bot/sheet_values.json')
SUMMARY_VALUES = Path('/home/vin/.openclaw/workspaces/manager-bot/summary_values.json')
TAG_RE = re.compile(r'<[^>]+>')


def clean(text: str) -> str:
    if not text:
        return ''
    return re.sub(r'\s+', ' ', TAG_RE.sub(' ', text)).strip()


def fetch(url: str) -> str:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw research bot)'})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')


def load_location_links() -> list[tuple[str, str]]:
    html = fetch('https://it.jobserve.com/SEOPage/SearchJobs?c=gb')
    links: list[tuple[str, str]] = []
    seen: set[str] = set()
    for m in re.finditer(r'<a href="([^"]*jobs-in-[^"]*/sl[^"]*/?)"[^>]*>(.*?)</a>', html, re.I | re.S):
        href = urljoin(BASE, m.group(1))
        label = clean(m.group(2))
        if href in seen:
            continue
        seen.add(href)
        # Keep leaf location pages and skip the county/region index buckets.
        if label.lower().startswith('jobs in '):
            continue
        links.append((label, href))
    return links


def parse_location_page(label: str, url: str) -> list[dict]:
    try:
        html = fetch(url)
    except Exception:
        return []
    items: list[dict] = []
    for m in re.finditer(r'<div class="jobItem">(.*?)</div>\s*</div>', html, re.S):
        block = m.group(1)
        href_m = re.search(r'<a href="([^"]+)"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
        title_m = re.search(r'<a href="[^"]+"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
        loc_m = re.search(r'<div class="jobSalLoc">(.*?)</div>', block, re.S)
        desc_m = re.search(r'<div class="jobDesc">(.*?)</div>', block, re.S)
        if not href_m or not title_m:
            continue
        title = clean(title_m.group(1))
        desc = clean(desc_m.group(1) if desc_m else '')
        blob = f'{title} {desc}'.lower()
        if not any(alias in blob for aliases in ALIASES.values() for alias in aliases):
            continue
        items.append(
            {
                'location_label': label,
                'location_url': url,
                'url': urljoin(BASE, href_m.group(1).split('?')[0]),
                'title': title,
                'location_text': clean(loc_m.group(1) if loc_m else ''),
                'snippet': desc,
            }
        )
    return items


def classify(row: dict) -> tuple[str | None, int]:
    title = (row.get('source_title') or row.get('title') or '').lower()
    desc = (row.get('description') or '').lower()
    blob = f'{title} {desc}'
    best = None
    best_score = 0
    for target in TARGETS:
        score = 0
        for idx, alias in enumerate(ALIASES[target]):
            if alias in title:
                score = max(score, 100 - idx)
            if alias in blob:
                score = max(score, 80 - idx)
        if score > best_score:
            best_score = score
            best = target
    return best, best_score


def main() -> None:
    links = load_location_links()
    print(f'links {len(links)}')

    candidates: list[dict] = []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        futs = [ex.submit(parse_location_page, label, url) for label, url in links]
        for fut in cf.as_completed(futs):
            try:
                candidates.extend(fut.result())
            except Exception:
                continue

    # Deduplicate early so the detail pass stays small.
    deduped: dict[str, dict] = {}
    for row in candidates:
        deduped.setdefault(row['url'], row)

    print(f'candidates {len(deduped)}')

    grouped: dict[str, list[dict]] = defaultdict(list)
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        fut_map = {ex.submit(detail, row['url']): row for row in deduped.values()}
        for fut in cf.as_completed(fut_map):
            row = fut_map[fut]
            try:
                d = fut.result()
            except Exception:
                continue
            text_blob = ' '.join([
                row.get('title', ''),
                row.get('snippet', ''),
                d.get('source_title', ''),
                d.get('description', ''),
                d.get('posted', ''),
            ]).lower()
            if 'outside ir35' not in text_blob:
                continue
            if (d.get('job_type') or '').lower() != 'contract' and 'contractor' not in (d.get('employment_type') or '').lower():
                continue
            age = parse_posted_age(d.get('posted'))
            if age is None or age > 5:
                continue
            merged = {**row, **d}
            target, score = classify(merged)
            if target is None or score <= 0:
                continue
            merged['requested_title'] = target
            merged['match_score'] = score
            merged['age_days'] = age
            grouped[target].append(merged)
            time.sleep(0.05)

    results: list[list] = []
    summary: list[list] = [["Requested Job Title", "Matching roles found", "Target roles requested", "Shortfall", "Notes"]]
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')

    for target in TARGETS:
        rows = grouped.get(target, [])
        rows.sort(key=[REDACTED_SECRET] r: (-r.get('match_score', 0), r.get('age_days', 999), r.get('source_title') or r.get('title') or '', r.get('url') or ''))
        rows = rows[:10]
        for idx, row in enumerate(rows, start=1):
            results.append([
                target,
                idx,
                row.get('source_title') or row.get('title') or '',
                row.get('company') or '',
                row.get('location') or row.get('location_text') or '',
                row.get('salary') or row.get('salary_location') or '',
                row.get('job_type') or row.get('employment_type') or '',
                row.get('posted') or '',
                'OUTSIDE IR35 found in role description',
                row.get('url') or '',
                row.get('description') or '',
                now,
            ])
        count = len(rows)
        shortfall = max(0, 10 - count)
        note = 'Target met' if shortfall == 0 else f'Only {count} matching Contract roles with OUTSIDE IR35 in the advert and posted within the last 5 days were available on JobServe at retrieval time.'
        summary.append([target, count, 10, shortfall, note])

    summary.append([
        'Source',
        'https://it.jobserve.com/JobSearch?q=business%20analysis&l=&dist=50',
        '',
        '',
        'Filtered from live UK location pages for Contract roles with OUTSIDE IR35 and posting age <= 5 days.',
    ])

    fields = [
        'Requested Job Title', 'Result #', 'Job Title', 'Company', 'Location', 'Salary', 'Job Type', 'Posted', 'IR35 Filter', 'JobServe URL', 'Role Description', 'Retrieved At UTC'
    ]
    with OUT_CSV.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(results)
    with OUT_JSON.open('w', encoding='utf-8') as f:
        json.dump([{field: value for field, value in zip(fields, row)} for row in results], f, ensure_ascii=False, indent=2)
    SHEET_VALUES.write_text(json.dumps([fields, *results], ensure_ascii=False, indent=2), encoding='utf-8')
    SUMMARY_VALUES.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')

    print('RESULTS', len(results))
    for target in TARGETS:
        print(target, len(grouped.get(target, [])))


if __name__ == '__main__':
    main()
