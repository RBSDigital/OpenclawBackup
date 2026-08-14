#!/usr/bin/env python3
import csv, html, json, re, time
from datetime import datetime, timezone
from urllib.parse import quote_plus, urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

BASE = 'https://it.jobserve.com'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw research bot; +https://openclaw.ai)'}
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
OUT_CSV = 'contract_analysis_jobserve.csv'
OUT_JSON = 'contract_analysis_jobserve.json'

TAG_RE = re.compile(r'<[^>]+>')
SPACE_RE = re.compile(r'\s+')
TITLE_ALIASES = {
    'Digital Business Analyst': ['digital business analyst'],
    'System Analyst': ['system analyst', 'systems analyst'],
    'Business Analyst': ['business analyst'],
    'Product Manager': ['product manager', 'technical product manager', 'agentic ai product manager'],
    'Product Owner': ['product owner'],
    'Delivery Manager': ['delivery manager', 'agile delivery manager'],
    'AI Agentic Analyst': ['ai agentic analyst', 'agentic analyst', 'agentic ai analyst'],
    'Agentic Engineer': ['agentic engineer', 'agentic ai engineer', 'ai agentic engineer'],
    'Solution Architect': ['solution architect', 'solutions architect', 'enterprise solution architect'],
}


def clean(s):
    if not s:
        return ''
    s = re.sub(r'(?i)<\s*br\s*/?>', ' ', s)
    s = re.sub(r'(?i)</\s*(p|li|div|h\d|tr)\s*>', ' ', s)
    s = TAG_RE.sub(' ', s)
    return SPACE_RE.sub(' ', html.unescape(s)).strip()


def parse_posted_age(posted):
    if not posted:
        return None
    text = posted.strip().lower()
    if text == 'today':
        return 0
    if text == 'yesterday':
        return 1
    m = re.match(r'(\d+)\s+days?\s+ago', text)
    if m:
        return int(m.group(1))
    for fmt in ('%a, %d %b %Y', '%d %b %Y', '%d %B %Y'):
        try:
            dt = datetime.strptime(posted.strip(), fmt)
            return (datetime.now(timezone.utc).date() - dt.date()).days
        except ValueError:
            pass
    return None


def title_aliases(target):
    return TITLE_ALIASES.get(target, [target.lower()])


def fetch(url, tries=3):
    last = None
    for i in range(tries):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=25) as r:
                return r.read().decode('utf-8', errors='replace')
        except (HTTPError, URLError, TimeoutError) as e:
            last = e
            time.sleep(1.5 * (i + 1))
    raise last


def parse_listing(page_html):
    items = []
    for m in re.finditer(r'<li class="jobResultItem">(.*?)</li>\s*(?=<li class="jobResultItem">|\s*</ul>)', page_html, re.S):
        block = m.group(1)
        href_m = re.search(r'<a href="([^"]+)"', block)
        title_m = re.search(r'<div class="jobTitle">(.*?)</div>', block, re.S)
        comp_m = re.search(r'<div class="company">(.*?)</div>', block, re.S)
        loc_m = re.search(r'<div class="salaryLocation">(.*?)</div>', block, re.S)
        det_m = re.search(r'<div class="jobDetails">(.*?)</div>', block, re.S)
        if href_m and title_m:
            items.append({
                'url': urljoin(BASE, html.unescape(href_m.group(1))),
                'title': clean(title_m.group(1)),
                'company': clean(comp_m.group(1) if comp_m else ''),
                'salary_location': clean(loc_m.group(1) if loc_m else ''),
                'snippet': clean(det_m.group(1) if det_m else ''),
            })
    return items


def pages_for_query(q):
    url = f"{BASE}/JobSearch?q={quote_plus(q)}&l=&dist=50&jt=c"
    text = fetch(url)
    m = re.search(r'Page\s+1\s+of\s+(\d+)', text)
    return int(m.group(1)) if m else 1


def detail(url):
    text = fetch(url)
    ld_m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', text, re.S)
    data = {}
    if ld_m:
        try:
            data = json.loads(ld_m.group(1))
        except Exception:
            data = {}
    def css(cls):
        m = re.search(rf'<span class="jobViewItem {cls}">(.*?)</span>', text, re.S)
        return clean(m.group(1)) if m else ''
    desc_html = data.get('description') or ''
    if not desc_html:
        m = re.search(r'<div class="m-3 jobDescription"><div class="jobdescWrapper">(.*?)</div></div>', text, re.S)
        desc_html = m.group(1) if m else ''
    return {
        'source_title': clean(data.get('title') or css('titleWrapper') or ''),
        'employment_type': data.get('employmentType') or '',
        'company': (data.get('hiringOrganization') or {}).get('name') or css('jobViewCompanyItem'),
        'location': (((data.get('jobLocation') or {}).get('address') or {}).get('addressLocality')) or css('jobViewLocItem'),
        'salary': css('jobViewSalaryItem'),
        'job_type': css('jobViewTypeItem'),
        'posted': css('jobViewDateItem'),
        'description': clean(desc_html),
    }


def matches_role(target, row):
    hay = (row.get('source_title') or row.get('title') or '') + ' ' + row.get('description','')
    # phrase match is preferred, but allow roles where description explicitly names the role.
    return target.lower() in hay.lower()


def main():
    seen = set()
    results = []
    for target in TARGETS:
        found = []
        # Search title plus outside IR35 first, then the plain title to avoid missing roles whose detail contains Outside IR35.
        queries = [f'{target} "Outside IR35"', f'{target} Outside IR35', target]
        for q in queries:
            if len(found) >= 10:
                break
            pages = min(pages_for_query(q), 12)
            for page in range(1, pages + 1):
                if len(found) >= 10:
                    break
                url = f"{BASE}/JobSearch?q={quote_plus(q)}&l=&dist=50&jt=c&page={page}"
                listing = fetch(url)
                candidates = parse_listing(listing)
                for item in candidates:
                    if len(found) >= 10:
                        break
                    if item['url'] in seen:
                        continue
                    # Cheap prefilter: if outside/ir35 absent from listing, still fetch only when q is plain target.
                    pre = (item['title'] + ' ' + item['snippet'] + ' ' + item['salary_location']).lower()
                    if q == target and not ('outside' in pre or 'ir35' in pre):
                        continue
                    time.sleep(0.25)
                    try:
                        d = detail(item['url'])
                    except Exception as e:
                        continue
                    desc_lower = d['description'].lower()
                    if 'outside ir35' not in desc_lower:
                        continue
                    if (d.get('job_type') and d['job_type'].lower() != 'contract') and ('contractor' not in str(d.get('employment_type','')).lower()):
                        continue
                    row = {**item, **d}
                    if not matches_role(target, row):
                        continue
                    seen.add(item['url'])
                    row['requested_title'] = target
                    row['retrieved_at_utc'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
                    found.append(row)
        results.extend(found)
        print(f'{target}: {len(found)}')

    fields = ['requested_title','source_title','company','location','salary','job_type','employment_type','posted','url','description','retrieved_at_utc']
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k,'') for k in fields})
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f'wrote {OUT_CSV} rows={len(results)}')

if __name__ == '__main__':
    main()
