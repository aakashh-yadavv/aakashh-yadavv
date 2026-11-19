import json, re, math
from fontTools.ttLib import TTFont

BG = '#070b16'; BL = '#247bff'; CR = '#ff354f'; OW = '#f5f5f5'
FONTS_B64 = json.load(open('/home/claude/work/build/fonts.json'))
IM = json.load(open('/home/claude/work/build/imgs.json'))
FM = {k: TTFont(f'/home/claude/work/fonts/{k}.woff2') for k in FONTS_B64}
NPM = '/home/claude/work/npm/node_modules/'
FACE = {'SG7': ('AkSG', 700), 'SG5': ('AkSG', 500), 'IN4': ('AkIN', 400), 'IN6': ('AkIN', 600), 'JB5': ('AkJB', 500)}
FAM = {'AkSG': "'AkSG','Space Grotesk','Segoe UI',Arial,sans-serif",
       'AkIN': "'AkIN','Inter','Segoe UI',Arial,sans-serif",
       'AkJB': "'AkJB','JetBrains Mono',Consolas,'Courier New',monospace"}


def tw(s, k, size, ls=0.0):
    f = FM[k]; cmap = f.getBestCmap(); hm = f['hmtx']; upm = f['head'].unitsPerEm
    return sum(hm[cmap.get(ord(c), cmap[32])][0] for c in s) * size / upm + ls * len(s)


def wrap(s, k, size, maxw):
    lines, cur = [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if tw(t, k, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fontface(keys):
    out = ''
    for k in keys:
        fam, wt = FACE[k]
        out += f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;src:url(data:font/woff2;base64,{FONTS_B64[k]}) format('woff2');}}\n"
    return out


def load_icon(path, prefix):
    s = open(NPM + path).read()
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    inner = re.sub(r'^.*?<svg[^>]*>', '', s, count=1, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner)
    inner = re.sub(r'<title>.*?</title>', '', inner)
    for i in re.findall(r'\bid="([^"]+)"', inner):
        inner = inner.replace(f'id="{i}"', f'id="{prefix}-{i}"').replace(f'url(#{i})', f'url(#{prefix}-{i})')
        inner = inner.replace(f'href="#{i}"', f'href="#{prefix}-{i}"')
    return vb, inner


def symbol(sid, path, prefix, fill=None):
    vb, inner = load_icon(path, prefix)
    if fill: inner = f'<g fill="{fill}">{inner}</g>'
    return f'<symbol id="{sid}" viewBox="{vb}">{inner}</symbol>'


def base_css(keys, extra=''):
    return (fontface(keys) + """
.sg7{font-family:@SG;font-weight:700}.sg5{font-family:@SG;font-weight:500}
.in4{font-family:@IN;font-weight:400}.in6{font-family:@IN;font-weight:600}
.jb{font-family:@JB;font-weight:500}
.stat{display:none}
.fu{animation:fu .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes fu{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
.fi{animation:fi 1s ease both}
@keyframes fi{from{opacity:0}to{opacity:1}}
.d1{animation:drift1 14s ease-in-out infinite alternate both}
.d2{animation:drift2 17s ease-in-out infinite alternate both}
@keyframes drift1{from{transform:translate(0,0)}to{transform:translate(50px,34px)}}
@keyframes drift2{from{transform:translate(0,0)}to{transform:translate(-56px,-30px)}}
.blink{animation:blink 1s steps(1) infinite both}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
.ring{opacity:0;transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite both}
@keyframes pulse{0%{transform:scale(1);opacity:.7}100%{transform:scale(2.8);opacity:0}}
.fl{animation:fl 4.2s ease-in-out infinite alternate both}
@keyframes fl{from{transform:translateY(0)}to{transform:translateY(-9px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.anim{display:none}.stat{display:inline}}
""").replace("@SG",FAM['AkSG']).replace("@IN",FAM['AkIN']).replace("@JB",FAM['AkJB']) + extra


def frame(p, W, H, r=28):
    defs = f'''
<pattern id="{p}-dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" opacity=".08"/></pattern>
<linearGradient id="{p}-edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BL}"/><stop offset=".5" stop-color="{BL}" stop-opacity=".25"/><stop offset="1" stop-color="{CR}"/></linearGradient>
<linearGradient id="{p}-grad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BL}"/><stop offset="1" stop-color="{CR}"/></linearGradient>
<radialGradient id="{p}-gB"><stop offset="0" stop-color="{BL}" stop-opacity=".38"/><stop offset="1" stop-color="{BL}" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}-gR"><stop offset="0" stop-color="{CR}" stop-opacity=".30"/><stop offset="1" stop-color="{CR}" stop-opacity="0"/></radialGradient>
<clipPath id="{p}-clip"><rect width="{W}" height="{H}" rx="{r}"/></clipPath>
<filter id="{p}-blur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>'''
    bg = f'''<g clip-path="url(#{p}-clip)"><rect width="{W}" height="{H}" fill="{BG}"/>
<g class="d1"><circle cx="120" cy="90" r="260" fill="url(#{p}-gB)"/></g>
<g class="d2"><circle cx="{W-90}" cy="{H-70}" r="270" fill="url(#{p}-gR)"/></g>
<rect width="{W}" height="{H}" fill="url(#{p}-dots)"/></g>'''
    border = f'''<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="{r-1}" fill="none" stroke="url(#{p}-edge)" stroke-width="5" opacity=".45" filter="url(#{p}-blur)"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{r-1}" fill="none" stroke="url(#{p}-edge)" stroke-width="2"/>'''
    return defs, bg, border


def svg_wrap(p, W, H, title, desc, css, defs, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="{p}-t {p}-d">
<title id="{p}-t">{esc(title)}</title><desc id="{p}-d">{esc(desc)}</desc>
<style>{css}</style>
<defs>{defs}</defs>
{body}
</svg>'''


# --- custom stroke icons (centered at 0,0, ~28px) ---
def ico(name, stroke=OW, sw=2):
    s = f'fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    d = {
        'code': f'<g {s}><path d="M-8-7-15 0l7 7M8-7l7 7-7 7M3-10-3 10"/></g>',
        'ai': f'<g {s}><path d="M0-13C1.5-5 5-1.5 13 0 5 1.5 1.5 5 0 13-1.5 5-5 1.5-13 0-5-1.5-1.5-5 0-13Z"/><path d="M11-12v6M8-9h6"/></g>',
        'game': f'<g {s}><rect x="-14" y="-8" width="28" height="17" rx="8.5"/><path d="M-7-3v6M-10 0h6"/><circle cx="6" cy="-2" r=".8" fill="{stroke}"/><circle cx="9.5" cy="2" r=".8" fill="{stroke}"/></g>',
        'travel': f'<g {s}><path d="M13-11-13-2l9 4 4 9Z"/><path d="M-4 2 13-11"/></g>',
        'movie': f'<g {s}><rect x="-13" y="-9" width="26" height="18" rx="3.5"/><path d="M-3-4.5 5 0l-8 4.5Z"/></g>',
        'check': f'<g {s}><path d="M-6 0l4 4 8-8"/></g>',
        'pin': f'<g {s}><path d="M0 11C-7 3-8-1-8-4a8 8 0 0 1 16 0c0 3-1 7-8 15Z"/><circle cx="0" cy="-4" r="2.6"/></g>',
        'arrow': f'<g {s}><path d="M-8 0h16M3-6l6 6-6 6"/></g>',
    }
    return d[name]
