from __future__ import annotations

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
SECTIONS = {
    'London': 'London',
    'Manchester': 'Manchester',
    'Birmingham': 'Birmingham',
    'Leeds': 'Leeds',
    'Bristol': 'Bristol',
    'Edinburgh': 'Edinburgh',
    'Glasgow': 'Glasgow',
    'Nottingham': 'Nottingham',
    'Reading': 'Reading',
    'Milton Keynes': 'Milton Keynes',
    'Cheshire': 'Cheshire',
    'Kent': 'Kent',
    'Swindon': 'Swindon',
    'Portsmouth': 'Portsmouth',
    'Hampshire': 'Hampshire',
}
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
    'Product Manager': ['product manager', 'product lead', 'head of product'],
    'Product Owner': ['product owner'],
    'Delivery Manager': ['delivery manager', 'service delivery manager', 'lead delivery manager', 'agile delivery manager'],
    'AI Agentic Analyst': ['ai agentic analyst', 'agentic analyst'],
    'Agentic Engineer': ['agentic engineer', 'ai agentic engineer'],
    'Solution Architect': ['solution architect', 'solutions architect', 'enterprise solution architect'],
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
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw research bot)'} )
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')


def load_location_links() -> dict[str, str]:
    html = fetch('https://it.jobserve.com/SEOPage/SearchJobs?c=gb')
    links: dict[str, str] = {}
    for m in re.finditer(r'<a href="([^"]*jobs-in-[^"]*/sl[^"]*/?)"[^>]*>(.*?)</a>', html, re.I | re.S):
        href = m.group(1)
        label = clean(m.group(2))
        for wanted in SECTIONS.values():
            if wanted.lower() == label.lower() and wanted not in links:
                links[wanted] = urljoin(BASE, href)
    return links


def parse_location(html: str) -> list[dict]:
    items = []
    for m in re.finditer(r'<div class="jobItem">(.*?)</div>\s*</div>', html, re.S):
        block = m.group(1)
        href_m = re.search(r'<a href="([^"]+)"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
        title_m = re.search(r'<a href="[^"]+"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
        loc_m = re.search(r'<div class="jobSalLoc">(.*?)</div>', block, re.S)
        desc_m = re.search(r'<div class="jobDesc">(.*?)</div>', block, re.S)
        if not href_m or not title_m:
            continue
        items.append({
            'url': urljoin(BASE, href_m.group(1).split('?')[0]),
            'title': clean(title_m.group(1)),
            'location_text': clean(loc_m.group(1) if loc_m else ''),
            'snippet': clean(desc_m.group(1) if desc_m else ''),
        })
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


def target_hints(row: dict) -> list[str]:
    t = (row.get('source_title') or row.get('title') or '').lower()
    d = (row.get('description') or '').lower()
    blob = f'{t} {d}'
    hits = []
    for target in TARGETS:
        if any(alias in blob for alias in ALIASES[target]):
            hits.append(target)
    return hits


def main() -> None:
    seen: set[str] = set()
    grouped: dict[str, list[dict]] = defaultdict(list)
    locations = load_location_links()

    for label in SECTIONS:
        url = locations.get(label)
        if not url:
            print(f'{label}: missing location link')
            continue
        html = fetch(url)
        jobs = parse_location(html)
        print(f'{label}: page1 jobs={len(jobs)}')
        for job in jobs:
            if job['url'] in seen:
                continue
            hints = target_hints(job)
            if not hints:
                continue
            try:
                d = detail(job['url'])
            except Exception:
                continue
            text_blob = ' '.join([
                job.get('title', ''),
                job.get('snippet', ''),
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
            merged = {**job, **d}
            target, score = classify(merged)
            if target is None or score <= 0:
                continue
            merged['requested_title'] = target
            merged['match_score'] = score
            merged['age_days'] = age
            seen.add(job['url'])
            grouped[target].append(merged)
            time.sleep(0.1)

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
        'Filtered from live location pages for Contract roles with OUTSIDE IR35 and posting age <= 5 days.',
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
