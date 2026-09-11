from urllib.request import Request, urlopen
import re
from jobserve_contract_analysis import detail

html = urlopen(Request('https://it.jobserve.com/jobs-in-London-London/sl134dc201d296cd/', headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read().decode('utf-8', errors='replace')
for m in re.finditer(r'<div class="jobItem">(.*?)</div>\s*</div>', html, re.S):
    block = m.group(1)
    href_m = re.search(r'<a href="([^"]+)"[^>]*class="jobTitle">(.*?)</a>', block, re.S)
    title = re.sub(r'<[^>]+>', ' ', href_m.group(2)).strip() if href_m else ''
    if title == 'Data Business Analyst':
        url = 'https://it.jobserve.com' + href_m.group(1).split('?')[0]
        d = detail(url)
        print('URL', url)
        print(d['job_type'], d['employment_type'], d['posted'])
        print(d['description'][:1000])
        break
