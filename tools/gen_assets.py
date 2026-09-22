"""Regenerates the SVG assets for the profile README.
Change ACCENT / BG below to match smaffan.com exactly, then: python tools/gen_assets.py"""
import os, random, textwrap
from xml.sax.saxutils import escape

BG      = "#12151F"   # smaffan.com theme-color
PANEL   = "#181C29"
LINE    = "#2A3042"
TEXT    = "#E9ECF4"
MUTED   = "#8A93A8"
ACCENT  = "#F2B84B"   # swap for your site's accent

SANS = "-apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"
ROOT = os.path.join(os.path.dirname(__file__), "..", "assets")

def hero():
    random.seed(7)
    bars, n, w = [], 96, 1200
    for i in range(n):
        x = 40 + i * (w - 80) / n
        h = 6 + abs(random.gauss(0, 1)) * 22
        d = (i % 12) * 0.09
        bars.append(f'<rect class="b" x="{x:.1f}" y="{360-h:.1f}" width="5" height="{h:.1f}" rx="2" style="animation-delay:{d:.2f}s"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400" role="img" aria-label="Something is broken. I build the thing that answers it.">
<style>
 .t1,.t2,.t3{{animation:in .9s ease-out backwards}}
 .t1{{animation-delay:.2s}} .t2{{animation-delay:1.3s}} .t3{{animation-delay:2.3s}}
 .rule{{stroke-dasharray:520;animation:draw 1s ease-out 2s backwards}}
 .b{{fill:{ACCENT};opacity:.22;transform-box:fill-box;transform-origin:50% 100%;animation:talk 1.6s ease-in-out infinite}}
 @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
 @keyframes draw{{from{{stroke-dashoffset:520}}to{{stroke-dashoffset:0}}}}
 @keyframes talk{{0%,100%{{transform:scaleY(.35)}}50%{{transform:scaleY(1)}}}}
 @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<rect width="1200" height="400" rx="18" fill="{BG}"/>
<rect x=".5" y=".5" width="1199" height="399" rx="18" fill="none" stroke="{LINE}"/>
<text x="60" y="72" font-family="{MONO}" font-size="14" fill="{MUTED}">Every project starts here</text>
<text class="t1" x="60" y="150" font-family="{SANS}" font-size="56" font-weight="700" fill="{MUTED}" letter-spacing="-1.5">Something is broken.</text>
<text class="t2" x="60" y="222" font-family="{SANS}" font-size="56" font-weight="700" fill="{TEXT}" letter-spacing="-1.5">I build the thing that answers it.</text>
<line class="rule" x1="60" y1="248" x2="580" y2="248" stroke="{ACCENT}" stroke-width="3"/>
<text class="t3" x="60" y="292" font-family="{SANS}" font-size="20" fill="{MUTED}">Voice agents, data pipelines and computer vision, shipped to production.</text>
{''.join(bars)}
</svg>'''
    open(os.path.join(ROOT, "hero.svg"), "w").write(svg)

PROJECTS = [
 ("splendor",      "Vision", "Splendor", "Fashion store with AI virtual try-on and body measurement, so shoppers pick a size without guessing.", ["React","Node.js","CV"]),
 ("voice-agent",   "Voice",  "AI Voice Assistant", "Real-time voice agents over live audio, with FAQ grounding and handoff to a human.", ["LiveKit","React","GPT-4o"]),
 ("disastershield","Platform","DisasterShield", "Connects homeowners, contractors and insurers after a disaster: matching, FNOL claims, payments.", ["React","CV","Payments"]),
 ("newslake",      "Data",   "NewsLake", "News lakehouse: MinIO, Spark bronze/silver/gold, Airflow, dbt, served by Next.js with an AI chatbot.", ["Airflow","Spark","dbt"]),
 ("stories",       "LLM",    "Stories We Tell", "Pulls structured entities out of free-form conversation and streams them back live.", ["LLM","Streaming","Auth"]),
 ("dark-tunnel",   "3D",     "Dark Tunnel", "An explorable 3D tunnel where projects hide down branching paths, with positional audio.", ["Three.js","GSAP","Next.js"]),
 ("clipsmith",     "Web",    "ClipSmith Studios", "Agency site whose whole work grid is generated from one Google Drive folder, CDN-delivered.", ["TanStack","React 19","Drive API"]),
 ("abdullah",      "Web",    "Abdullah Chughtai", "Scroll-choreographed client portfolio with WebGL transitions tuned not to stutter.", ["React","WebGL","Motion"]),
 ("motion",        "Web",    "Motion Showcase", "Media-heavy showcase built on lazy-loaded streaming and generated poster frames.", ["React","Streaming","Lazy load"]),
]

def card(slug, kind, title, desc, tags):
    lines = textwrap.wrap(desc, 40)[:3]
    body = "".join(f'<text x="28" y="{112+i*22}" font-family="{SANS}" font-size="15" fill="{MUTED}">{escape(l)}</text>' for i, l in enumerate(lines))
    x, chips = 28, []
    for t in tags:
        tw = len(t) * 7.4 + 20
        chips.append(f'<rect x="{x}" y="200" width="{tw:.0f}" height="26" rx="13" fill="none" stroke="{LINE}"/>'
                     f'<text x="{x+10}" y="217" font-family="{MONO}" font-size="12" fill="{TEXT}">{escape(t)}</text>')
        x += tw + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250" role="img" aria-label="{escape(title)}: {escape(desc)}">
<rect width="400" height="250" rx="14" fill="{PANEL}"/>
<rect x=".5" y=".5" width="399" height="249" rx="14" fill="none" stroke="{LINE}"/>
<text x="28" y="40" font-family="{MONO}" font-size="12" fill="{ACCENT}">{escape(kind)}</text>
<text x="372" y="40" text-anchor="end" font-family="{SANS}" font-size="18" fill="{MUTED}">&#8599;</text>
<text x="28" y="78" font-family="{SANS}" font-size="25" font-weight="700" fill="{TEXT}" letter-spacing="-.5">{escape(title)}</text>
{body}
{''.join(chips)}
</svg>'''
    open(os.path.join(ROOT, "cards", f"{slug}.svg"), "w").write(svg)

def closer():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-label="Something broken? Email affan4321@gmail.com">
<rect width="1200" height="180" rx="18" fill="{BG}"/>
<rect x=".5" y=".5" width="1199" height="179" rx="18" fill="none" stroke="{LINE}"/>
<text x="60" y="88" font-family="{SANS}" font-size="44" font-weight="700" fill="{TEXT}" letter-spacing="-1">Something broken?</text>
<text x="60" y="130" font-family="{SANS}" font-size="19" fill="{MUTED}">Email or WhatsApp is fastest. I usually answer the same day.</text>
<text x="1140" y="88" text-anchor="end" font-family="{MONO}" font-size="18" fill="{ACCENT}">affan4321@gmail.com</text>
</svg>'''
    open(os.path.join(ROOT, "closer.svg"), "w").write(svg)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "cards"), exist_ok=True)
    hero(); closer()
    for p in PROJECTS: card(*p)
    print("assets written")
