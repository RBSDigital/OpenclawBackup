from __future__ import annotations

import concurrent.futures as cf
import re
from collections import defaultdict
from urllib.parse import urljoin
from urllib.request import Request, urlopen

BASE = 'https://it.jobserve.com'
TARGETS = {
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
TAG_RE = re.compile(r'<[^>]+>')


def clean(text: str) -> str:
    return re.sub(r'\s+', ' ', TAG_RE.sub(' ', text)).strip() if text else ''


def fetch(url: str) -> str:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw research bot)'})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')


def extract_links() -> list[tuple[str, str]]:
    html = fetch('https://it.jobserve.com/SEOPage/SearchJobs?c=gb')
    links = []
    seen = set()
    for m in re.finditer(r'<a href="([^"]*jobs-in-[^"]*/sl[^"]*/?)"[^>]*>(.*?)</a>', html, re.I | re.S):
        href = urljoin(BASE, m.group(1))
        label = clean(m.group(2))
        if href not in seen and not label.lower().startswith('jobs in '):
            seen.add(href)
            links.append((label, href))
    return links


def parse_page(url: str) -> dict[str, list[dict]]:
    try:
        html = fetch(url)
    except Exception:
        return {}
    out: dict[str, list[dict]] = defaultdict(list)
    for m in re.finditer(r'<div class="jobItem">(.*?)</div>\s*</div>', html, re.S):
        block = m.group(1)
        href_m = re.search(r'<a href="([^"]+)"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
        title_m = re.search(r'<a href="[^"]+"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
        desc_m = re.search(r'<div class="jobDesc">(.*?)</div>', block, re.S)
        if not href_m or not title_m:
            continue
        title = clean(title_m.group(1))
        desc = clean(desc_m.group(1) if desc_m else '')
        blob = f'{title} {desc}'.lower()
        for target, aliases in TARGETS.items():
            if any(alias in blob for alias in aliases):
                out[target].append({'title': title, 'url': urljoin(BASE, href_m.group(1).split('?')[0]), 'desc': desc[:200]})
                break
    return out


def main() -> None:
    links = extract_links()
    print('links', len(links))
    results: dict[str, list[dict]] = defaultdict(list)
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(parse_page, url): (label, url) for label, url in links}
        for fut in cf.as_completed(futs):
            label, url = futs[fut]
            try:
                matched = fut.result()
            except Exception:
                continue
            for target, items in matched.items():
                results[target].extend([{'location': label, **item} for item in items])
    for target in TARGETS:
        items = results.get(target, [])
        print('\n###', target, len(items))
        seen = set()
        for item in items:
            if item['url'] in seen:
                continue
            seen.add(item['url'])
            print(item['location'], '|', item['title'], '|', item['url'])
            if len(seen) >= 25:
                break

if __name__ == '__main__':
    main()
