"""Generate honest dated snapshots from public GitHub data; no third-party widgets."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen

USER = 'erenseret56-del'
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
API = 'https://api.github.com'

def get(url, json_data=True):
    request = Request(url, headers={'User-Agent': 'Ruthvik-Profile-Snapshot'})
    with urlopen(request, timeout=25) as response:
        body = response.read().decode('utf-8')
    return json.loads(body) if json_data else body

profile = get(f'{API}/users/{USER}')
repos = []
page = 1
while True:
    batch = get(f'{API}/users/{USER}/repos?per_page=100&page={page}')
    repos.extend(batch)
    if len(batch) < 100:
        break
    page += 1
owned = [repo for repo in repos if not repo['fork']]
languages = Counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(lambda repo: get(repo['languages_url']), owned):
        languages.update(result)

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = {}
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-date' in attrs and 'data-level' in attrs:
            self.days[attrs['data-date']] = int(attrs['data-level'])

calendar = Calendar()
calendar.feed(get(f'https://github.com/users/{USER}/contributions', False))
if len(calendar.days) < 90:
    raise RuntimeError('GitHub calendar structure changed; refusing to invent activity data.')
stamp = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime('%Y-%m-%d')

def card(title, height, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img">
<title>{escape(title)} — snapshot {stamp}</title>
<rect x="1" y="1" width="958" height="{height-2}" rx="14" fill="#080e1b" stroke="#203448"/>
<g font-family="Consolas,Menlo,monospace"><text x="30" y="40" fill="#64edb4" font-size="22">{escape(title)}</text>
<text x="930" y="40" text-anchor="end" fill="#8c9db5" font-size="14">SNAPSHOT / {stamp}</text>{body}</g></svg>'''

metrics = [('PUBLIC REPOS', profile['public_repos']), ('REPO STARS', sum(r['stargazers_count'] for r in owned)), ('FOLLOWERS', profile['followers'])]
body = ''
for i, (label, value) in enumerate(metrics):
    x = 30 + 310*i
    body += f'<text x="{x}" y="108" fill="#eef5fc" font-size="43">{value}</text><text x="{x}" y="143" fill="#8eb4d4" font-size="16">{label}</text>'
body += '<text x="30" y="186" fill="#8c9db5" font-size="14">Public GitHub API / stars across owned, non-fork repositories</text>'
stats = card('ACCOUNT / GITHUB', 214, body)

total = sum(languages.values())
if not total:
    raise RuntimeError('No language data returned; refusing to invent percentages.')
body = ''
for i, (language, count) in enumerate(languages.most_common(6)):
    y = 82 + i*39
    pct = count/total*100
    body += f'<text x="30" y="{y}" fill="#b9c9dc" font-size="18">{escape(language)}</text><rect x="250" y="{y-16}" width="560" height="15" rx="4" fill="#142235"/><rect x="250" y="{y-16}" width="{max(1,560*pct/100):.1f}" height="15" rx="4" fill="#64edb4"/><text x="930" y="{y}" text-anchor="end" fill="#55adff" font-size="17">{pct:.1f}%</text>'
body += '<text x="30" y="329" fill="#8c9db5" font-size="14">Share of code bytes in public, non-fork repositories / not proficiency</text>'
language_svg = card('LANGUAGES / CODE FOOTPRINT', 354, body)

days = sorted(calendar.days.items())[-91:]
palette = ['#142235', '#0b493a', '#107855', '#26bc82', '#64edb4']
body = ''
for i, (date, level) in enumerate(days):
    x, y = 30+(i//7)*69, 72+(i%7)*23
    body += f'<rect x="{x}" y="{y}" width="58" height="17" rx="3" fill="{palette[level]}"><title>{date}: GitHub activity level {level}/4</title></rect>'
body += f'<text x="30" y="264" fill="#b9c9dc" font-size="16">{days[0][0]} — {days[-1][0]} / 91 days</text>'
body += '<text x="30" y="295" fill="#8c9db5" font-size="14">Columns: consecutive 7-day blocks / public calendar intensity, not counts</text>'
for i, color in enumerate(palette):
    body += f'<rect x="{760+i*32}" y="249" width="24" height="16" rx="3" fill="{color}"/>'
activity = card('ACTIVITY / CONTRIBUTION SIGNAL', 320, body)

# Write only after every source has succeeded, keeping prior snapshots on failures.
for name, data in [('stats.svg',stats),('languages.svg',language_svg),('activity.svg',activity)]:
    (ASSETS/name).write_text(data, encoding='utf-8')
print(f'Generated real GitHub snapshots dated {stamp}: {len(repos)} public repositories, {len(languages)} languages, {len(days)} calendar days.')
