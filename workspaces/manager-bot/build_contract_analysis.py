#!/usr/bin/env python3
from jobserve_contract_analysis import fetch, parse_listing, detail, BASE, TARGETS
from urllib.parse import quote_plus
from datetime import datetime, timezone
import csv, json, re, time

OUT_CSV='Contract_Analysis_Discord_results.csv'
OUT_JSON='Contract_Analysis_Discord_results.json'
queries = ['Outside IR35'] + [f'{t} Outside IR35' for t in TARGETS] + TARGETS
pool=[]; seen=set()
for q in queries:
    first=fetch(f'{BASE}/JobSearch?q={quote_plus(q)}&l=&dist=50&jt=c')
    m=re.search(r'Page\s+1\s+of\s+(\d+)', first)
    pages=min(int(m.group(1)) if m else 1, 12)
    for page in range(1,pages+1):
        html= first if page==1 else fetch(f'{BASE}/JobSearch?q={quote_plus(q)}&l=&dist=50&jt=c&page={page}')
        for it in parse_listing(html):
            if it['url'] in seen: continue
            seen.add(it['url'])
            try:
                d=detail(it['url'])
            except Exception:
                continue
            desc=(d.get('description') or '')
            if 'outside ir35' not in desc.lower():
                continue
            if (d.get('job_type') or '').lower() != 'contract' and 'contractor' not in (d.get('employment_type') or '').lower():
                continue
            pool.append({**it, **d, 'source_query': q})
            time.sleep(0.12)

rows=[]
now=datetime.now(timezone.utc).isoformat(timespec='seconds')
for t in TARGETS:
    matches=[]
    for r in pool:
        hay=((r.get('source_title') or r.get('title') or '')+' '+(r.get('description') or '')).lower()
        if t.lower() in hay:
            matches.append(r)
    # Prefer exact phrase in displayed title, then any title, then description-only matches.
    matches.sort(key=[REDACTED_SECRET] r: (0 if t.lower() in (r.get('source_title') or r.get('title') or '').lower() else 1, r.get('source_title') or r.get('title') or ''))
    used=set()
    count=0
    for r in matches:
        if r['url'] in used: continue
        used.add(r['url'])
        count+=1
        rows.append({
            'Requested Job Title': t,
            'Result #': count,
            'Job Title': r.get('source_title') or r.get('title') or '',
            'Company': r.get('company') or '',
            'Location': r.get('location') or '',
            'Salary': r.get('salary') or r.get('salary_location') or '',
            'Job Type': r.get('job_type') or r.get('employment_type') or '',
            'Posted': r.get('posted') or '',
            'IR35 Filter': 'OUTSIDE IR35 found in role description',
            'JobServe URL': r.get('url') or '',
            'Role Description': r.get('description') or '',
            'Retrieved At UTC': now,
        })
        if count>=10: break
    print(f'{t}: {count}')

with open(OUT_CSV,'w',newline='',encoding='utf-8') as f:
    fields=list(rows[0].keys()) if rows else []
    w=csv.DictWriter(f,fieldnames=fields)
    w.writeheader(); w.writerows(rows)
with open(OUT_JSON,'w',encoding='utf-8') as f:
    json.dump(rows,f,ensure_ascii=False,indent=2)
print(f'wrote {OUT_CSV} rows={len(rows)}')
