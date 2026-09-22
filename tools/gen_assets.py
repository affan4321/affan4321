"""Regenerates the SVG assets for the profile README, using smaffan.com's palette and fonts.
Requires: pip install fonttools brotli   Run: python tools/gen_assets.py"""
import os, io, base64, random, textwrap
from xml.sax.saxutils import escape
from fontTools.ttLib import TTFont
from fontTools import subset

# smaffan.com design tokens (:root CSS variables)
INK     = "#12151F"  # --c-ink
INK2    = "#1A1E2B"  # --c-ink-2
SLATE   = "#2B3143"  # --c-slate
BONE    = "#F1EDE8"  # --c-bone
MUTED   = "#8A90A0"  # --c-muted
SIGNAL  = "#2B8FE0"  # --c-signal
SKY     = "#64AFD2"  # --c-sky
EMBER   = "#C97B5A"  # --c-ember

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "assets")
FONTS = {  # family name -> (file, css weight)
    "Archivo":          ("archivo-latin-800-normal.woff2", 800),
    "Space Grotesk":    ("space-grotesk-latin-400-normal.woff2", 400),
    "Space Grotesk M":  ("space-grotesk-latin-500-normal.woff2", 500),
}
FALLBACK = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif"
_tt = {k: TTFont(os.path.join(HERE, "fonts", f)) for k, (f, _) in FONTS.items()}

def width(text, fam, size):
    f = _tt[fam]; cmap = f.getBestCmap(); hm = f["hmtx"]; upm = f["head"].unitsPerEm
    return sum(hm[cmap.get(ord(c), cmap[32])][0] for c in text) * size / upm

def fontface(used):  # used: {family: set(chars)} -> @font-face rules with subset, base64 woff2
    rules = []
    for fam, chars in used.items():
        fname, w = FONTS[fam]
        opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
        font = TTFont(os.path.join(HERE, "fonts", fname))
        s = subset.Subsetter(opts); s.populate(text="".join(chars) + " "); s.subset(font)
        buf = io.BytesIO(); font.flavor = "woff2"; font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        rules.append(f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "".join(rules)

class Doc:
    def __init__(self): self.used, self.parts = {}, []
    def text(self, x, y, s, fam, size, fill, extra=""):
        self.used.setdefault(fam, set()).update(s)
        w = FONTS[fam][1]
        self.parts.append(f'<text x="{x}" y="{y}" font-family="\'{fam}\', {FALLBACK}" font-weight="{w}" font-size="{size}" fill="{fill}" {extra}>{escape(s)}</text>')
    def raw(self, s): self.parts.append(s)

GRAD = f'<linearGradient id="merge" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="{SIGNAL}"/><stop offset="1" stop-color="{EMBER}"/></linearGradient>'

def hero():
    d, W = Doc(), 1200
    l1, l2 = "Something is broken.", "I build the thing that answers it."
    size = 58
    while width(l2, "Archivo", size) > W - 130: size -= 1
    d.text(60, 72, "Every project starts here", "Space Grotesk M", 15, MUTED)
    d.text(60, 152, l1, "Archivo", size, MUTED, 'class="t1" letter-spacing="-1"')
    d.text(60, 152 + size * 1.25, l2, "Archivo", size, BONE, 'class="t2" letter-spacing="-1"')
    ry = 152 + size * 1.25 + 26
    d.raw(f'<rect class="rule" x="60" y="{ry:.0f}" width="{width(l2,"Archivo",size)*.55:.0f}" height="3" rx="1.5" fill="url(#merge)"/>')
    d.text(60, ry + 44, "Voice agents, data pipelines and computer vision, shipped to production.", "Space Grotesk", 20, MUTED, 'class="t3"')
    random.seed(7); n = 96
    bars = []
    for i in range(n):
        x = 40 + i * (W - 80) / n; h = 6 + abs(random.gauss(0, 1)) * 20
        bars.append(f'<rect class="b" x="{x:.1f}" y="{372-h:.1f}" width="5" height="{h:.1f}" rx="2" style="animation-delay:{(i%12)*0.09:.2f}s"/>')
    d.raw(f'<g fill="url(#wave)">{"".join(bars)}</g>')
    css = f'''{fontface(d.used)}
 .t1,.t2,.t3{{animation:in .9s ease-out backwards}} .t1{{animation-delay:.2s}} .t2{{animation-delay:1.3s}} .t3{{animation-delay:2.3s}}
 .rule{{transform-box:fill-box;transform-origin:0 50%;animation:draw 1s ease-out 2s backwards}}
 .b{{opacity:.35;transform-box:fill-box;transform-origin:50% 100%;animation:talk 1.6s ease-in-out infinite}}
 @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
 @keyframes draw{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
 @keyframes talk{{0%,100%{{transform:scaleY(.35)}}50%{{transform:scaleY(1)}}}}
 @media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="400" viewBox="0 0 {W} 400" role="img" aria-label="Something is broken. I build the thing that answers it.">
<defs>{GRAD}<linearGradient id="wave" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{SIGNAL}"/><stop offset="1" stop-color="{EMBER}"/></linearGradient></defs>
<style>{css}</style>
<rect width="{W}" height="400" rx="18" fill="{INK}"/>
<rect x=".5" y=".5" width="{W-1}" height="399" rx="18" fill="none" stroke="{SLATE}"/>
{"".join(d.parts)}
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

def wrap(text, fam, size, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if width(t, fam, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]

def card(slug, kind, title, desc, tags):
    d = Doc()
    d.text(28, 40, kind, "Space Grotesk M", 13, SKY)
    d.text(372, 41, "\u2197", "Space Grotesk", 18, MUTED, 'text-anchor="end"')
    d.text(28, 80, title, "Archivo", 26, BONE, 'letter-spacing="-.4"')
    for i, l in enumerate(wrap(desc, "Space Grotesk", 15, 344)[:3]):
        d.text(28, 114 + i * 22, l, "Space Grotesk", 15, MUTED)
    x = 28
    for t in tags:
        tw = width(t, "Space Grotesk M", 12) + 22
        d.raw(f'<rect x="{x:.0f}" y="200" width="{tw:.0f}" height="26" rx="13" fill="none" stroke="{SLATE}"/>')
        d.text(round(x + 11), 217, t, "Space Grotesk M", 12, BONE)
        x += tw + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250" role="img" aria-label="{escape(title)}: {escape(desc)}">
<style>{fontface(d.used)}</style>
<rect width="400" height="250" rx="14" fill="{INK2}"/>
<rect x=".5" y=".5" width="399" height="249" rx="14" fill="none" stroke="{SLATE}"/>
{"".join(d.parts)}
</svg>'''
    open(os.path.join(ROOT, "cards", f"{slug}.svg"), "w").write(svg)

def closer():
    d, W = Doc(), 1200
    d.text(60, 86, "Something broken?", "Archivo", 46, BONE, 'letter-spacing="-1"')
    d.text(60, 128, "Email or WhatsApp is fastest. I usually answer the same day.", "Space Grotesk", 19, MUTED)
    d.text(W - 60, 78, "affan4321@gmail.com", "Space Grotesk M", 19, SKY, 'text-anchor="end"')
    d.text(W - 60, 112, "WhatsApp +92 314 4320292", "Space Grotesk M", 19, SKY, 'text-anchor="end"')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="180" viewBox="0 0 {W} 180" role="img" aria-label="Something broken? Email affan4321@gmail.com or WhatsApp +92 314 4320292">
<defs>{GRAD}</defs><style>{fontface(d.used)}</style>
<rect width="{W}" height="180" rx="18" fill="{INK}"/>
<rect x=".5" y=".5" width="{W-1}" height="179" rx="18" fill="none" stroke="{SLATE}"/>
<rect x="60" y="150" width="180" height="3" rx="1.5" fill="url(#merge)"/>
{"".join(d.parts)}
</svg>'''
    open(os.path.join(ROOT, "closer.svg"), "w").write(svg)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "cards"), exist_ok=True)
    hero(); closer()
    for p in PROJECTS: card(*p)
    print("assets written")
