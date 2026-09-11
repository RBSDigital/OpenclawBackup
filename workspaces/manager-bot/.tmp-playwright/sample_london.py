from urllib.request import Request, urlopen
import re, json
from jobserve_contract_analysis import detail, parse_posted_age

TARGETS = {
    'Digital Business Analyst': ['digital business analyst', 'junior business analyst', 'business analyst'],
    'System Analyst': ['system analyst', 'systems analyst'],
    'Business Analyst': ['business analyst'],
    'Product Manager': ['product manager'],
    'Product Owner': ['product owner'],
    'Delivery Manager': ['delivery manager'],
    'AI Agentic Analyst': ['ai agentic analyst', 'agentic analyst'],
    'Agentic Engineer': ['agentic engineer', 'ai agentic engineer'],
    'Solution Architect': ['solution architect', 'solutions architect', 'enterprise solution architect'],
}

html = urlopen(Request('https://it.jobserve.com/jobs-in-London-London/sl134dc201d296cd/', headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read().decode('utf-8', errors='replace')
items = []
for m in re.finditer(r'<div class="jobItem">(.*?)</div>\s*</div>', html, re.S):
    block = m.group(1)
    href_m = re.search(r'<a href="([^"]+)"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
    desc_m = re.search(r'<div class="jobDesc">(.*?)</div>', block, re.S)
    if href_m:
        items.append({'url': 'https://it.jobserve.com' + href_m.group(1).split('?')[0], 'title': re.sub(r'<[^>]+>',' ',href_m.group(2)), 'desc': re.sub(r'<[^>]+>',' ',desc_m.group(1) if desc_m else '')})
print('items', len(items))
for item in items[:20]:
    hay = (item['title'] + ' ' + item['desc']).lower()
    hit = [t for t, aliases in TARGETS.items() if any(a in hay for a in aliases)]
    if hit:
        d = detail(item['url'])
        age = parse_posted_age(d.get('posted'))
        print(json.dumps({'title': item['title'], 'hit': hit, 'posted': d.get('posted'), 'job_type': d.get('job_type'), 'employment_type': d.get('employment_type'), 'desc_snip': item['desc'][:180]}, ensure_ascii=False))
