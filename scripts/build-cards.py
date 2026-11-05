"""Rebuild small, self-contained SVG assets using Python's standard library."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)

def svg(body, height, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs><linearGradient id="bg"><stop stop-color="#0c1b29"/><stop offset="1" stop-color="#060c15"/></linearGradient></defs>
<rect x="1" y="1" width="958" height="{height-2}" rx="14" fill="url(#bg)" stroke="#24394c"/>
<g font-family="Consolas,Menlo,monospace">{body}</g></svg>'''

projects = [
    ('aster', '01', 'ASTER', 'AI-powered assistant and voice interaction platform.', ['STACK / awaiting confirmation'], 'VOICE / INTELLIGENCE'),
    ('peoplix', '02', 'PEOPLIX', 'Digital platform.', ['React / TypeScript / Tailwind CSS', 'Node.js / Fastify / MongoDB'], 'PLATFORM / PRODUCT'),
    ('synthora', '03', 'SYNTHORA', 'Clinical Synthetic Data Lab.', ['React / TypeScript / Supabase / Python'], 'DATA / RESEARCH'),
    ('jarvis', '04', 'JARVIS', 'AI assistant project.', ['React / TypeScript / Three.js / Vite'], 'ASSISTANT / INTERFACE'),
    ('prime-flex', '05', 'PRIME FLEX', 'Fitness platform.', ['STACK / awaiting confirmation'], 'FITNESS / EXPERIENCE'),
]

for slug, number, name, description, stack, category in projects:
    body = f'''<path d="M1 40V15Q1 1 15 1H220" fill="none" stroke="#64edb4" stroke-width="2"/>
<text x="30" y="37" fill="#64edb4" font-size="14">PROJECT / {number}</text>
<text x="925" y="37" text-anchor="end" fill="#7294af" font-size="13">{category}</text>
<text x="30" y="86" fill="#eef5fc" font-size="34" font-weight="700">{name}</text>
<text x="30" y="124" fill="#b9c9dc" font-size="19">{escape(description)}</text>
<path d="M30 148H930" stroke="#203448"/>
<text x="900" y="107" fill="#55adff" font-size="42">↗</text>'''
    for i, line in enumerate(stack):
        body += f'<text x="30" y="{180+i*27}" fill="#8eb4d4" font-size="17">{escape(line)}</text>'
    (ASSETS / f'project-{slug}.svg').write_text(svg(body, 232, f'{name} — {description}'), encoding='utf-8')

footer = '''<text x="28" y="47" fill="#64edb4" font-size="18">&gt; build with intent_</text>
<text x="930" y="47" text-anchor="end" fill="#8eb4d4" font-size="14">SAI RUTHVIK REDDY / END OF SESSION</text>'''
(ASSETS / 'footer.svg').write_text(svg(footer, 80, 'Build with intent — Sai Ruthvik Reddy'), encoding='utf-8')
print('Generated five project cards and footer.')
