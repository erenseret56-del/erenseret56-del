"""Check local profile assets; optionally probe external image services."""
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from pathlib import Path
import re
import sys
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
readme = (root / 'README.md').read_text(encoding='utf-8')
sources = re.findall(r'src="([^"]+)"', readme)
local = [s for s in sources if not s.startswith('https://')]
assert len(local) == 11, local
assert all((root / s).is_file() for s in local)
for path in (root / 'assets').glob('*.svg'):
    ET.parse(path)
assert len(re.findall(r'^## ', readme, re.M)) == 8
assert '<script' not in readme and '<style' not in readme
assert not re.search(r'https://[^\s"<>]*(?:YOUR_|example\.com)', readme)
workflow = (root / '.github/workflows/snake.yml').read_text(encoding='utf-8')
assert 'Platane/snk@v3' in workflow
assert 'publish_branch: output' in workflow
assert 'force_orphan: false' in workflow and 'keep_files: true' in workflow
assert 'contents: write' in workflow and 'workflow_dispatch:' in workflow
try:
    import yaml
except ImportError:
    print('YAML parser not installed; workflow configuration checked as text only.')
else:
    parsed = yaml.load(workflow, Loader=yaml.BaseLoader)
    assert parsed['on']['schedule'][0]['cron'] == '17 0 * * *'
    assert len(parsed['jobs']['generate']['steps']) == 3
    print('PASS: workflow YAML parsed.')
print('PASS: local assets, SVG XML, sections, image references, workflow configuration.')
print('Local image bytes:', sum(p.stat().st_size for p in (root / 'assets').iterdir()))

if '--online' in sys.argv:
    urls = list(dict.fromkeys(unescape(s) for s in sources
                if s.startswith('https://') and 'raw.githubusercontent.com' not in s))
    def probe(url):
        host = url.split('/')[2]
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Profile-Asset-Check'}), timeout=20) as response:
                data = response.read()
                is_svg = b'<svg' in data[:2000]
                return f'{host}: HTTP {response.status}, SVG={is_svg}, {len(data)} bytes'
        except Exception as error:
            return f'{host}: unavailable ({error})'
    with ThreadPoolExecutor(max_workers=6) as pool:
        for result in pool.map(probe, urls):
            print(result)
    print('Snake URLs require the first workflow run and were not probed.')
