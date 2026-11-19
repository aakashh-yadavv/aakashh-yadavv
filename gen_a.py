from common import *


def spin(cx, cy, dur, rev=False):
    a, b = (360, 0) if rev else (0, 360)
    return f'<animateTransform attributeName="transform" type="rotate" from="{a} {cx} {cy}" to="{b} {cx} {cy}" dur="{dur}s" begin="0s" repeatCount="indefinite"/>'


def hero():
    p = 'hro'; W, H = 900, 540
    fd, bg, border = frame(p, W, H)
    css = base_css(['SG7', 'SG5', 'IN4', 'IN6', 'JB5'], """
.rise{animation:rise 1.1s cubic-bezier(.16,.84,.24,1) both}
@keyframes rise{from{transform:translateY(125px)}to{transform:translateY(0)}}
.rl{opacity:0;animation:rl 10s infinite both}
.r0{opacity:1}
@keyframes rl{0%{opacity:0;transform:translateY(16px)}3%{opacity:1;transform:translateY(0)}22%{opacity:1;transform:translateY(0)}25%{opacity:0;transform:translateY(-16px)}100%{opacity:0;transform:translateY(-16px)}}
.line{transform-box:fill-box;transform-origin:left center;animation:ln 1s .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes ln{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.port{animation:port 1.1s .35s cubic-bezier(.2,.7,.2,1) both}
@keyframes port{from{opacity:0;transform:translateX(40px)}to{opacity:1;transform:translateX(0)}}
.scan{animation:scan 9s linear infinite both}
@keyframes scan{from{transform:translateX(-200px)}to{transform:translateX(1100px)}}
""")
    roles = ['.NET Developer', 'ASP.NET Core Developer', 'REST API Developer', 'SQL Server Developer']
    role_svg = ''.join(
        f'<g class="rl r{i}" style="animation-delay:{i*2.5}s"><text x="132" y="352" class="sg5" font-size="27" fill="{OW}">{esc(r)}</text></g>'
        for i, r in enumerate(roles))
    pitch = wrap('Passionate .NET Developer focused on building secure, scalable and maintainable web applications using ASP.NET Core.', 'IN4', 15, 480)
    pitch_svg = ''.join(f'<text x="52" y="{452+i*23}" class="in4" font-size="15" fill="{OW}" fill-opacity=".86">{esc(l)}</text>' for i, l in enumerate(pitch))
    pill_txt = 'Junior .NET Developer  |  Open to Opportunities'
    pill_w = int(tw(pill_txt, 'IN6', 14) + 64)
    defs = fd + f'''
<clipPath id="{p}-n1"><rect x="30" y="112" width="560" height="96"/></clipPath>
<clipPath id="{p}-n2"><rect x="30" y="206" width="560" height="96"/></clipPath>
<linearGradient id="{p}-nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BL}"/><stop offset="1" stop-color="{CR}"/></linearGradient>
<linearGradient id="{p}-sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="{p}-halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{BL}" stop-opacity=".55"/><stop offset=".6" stop-color="{CR}" stop-opacity=".22"/><stop offset="1" stop-color="{CR}" stop-opacity="0"/></radialGradient>
<linearGradient id="{p}-rg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BL}"/><stop offset="1" stop-color="{CR}"/></linearGradient>'''
    def ring(cx, cy, anim):
        inner = f'<circle cx="{cx}" cy="{cy}" r="172" fill="none" stroke="url(#{p}-rg)" stroke-width="1.6" stroke-dasharray="3 11" stroke-linecap="round" opacity=".9"/><circle cx="{cx+172}" cy="{cy}" r="6" fill="{CR}"/><circle cx="{cx-172}" cy="{cy}" r="4" fill="{BL}"/>'
        return f'<g class="anim">{inner.replace("<circle", "<circle", 1)}</g>' if False else inner
    cx, cy = 704, 250
    ring_anim = f'<g class="anim"><g>{spin(cx, cy, 36)}{ring(cx, cy, 1)}</g></g><g class="stat">{ring(cx, cy, 0)}</g>'
    tags = ''
    for i, (t, x, y) in enumerate([('C#', 548, 292), ('ASP.NET', 790, 196), ('SQL', 806, 372)]):
        w = int(tw(t, 'JB5', 13) + 24)
        tags += f'<g class="fl" style="animation-delay:{-i*1.3}s"><g transform="translate({x} {y})"><rect width="{w}" height="28" rx="14" fill="#0b1226" stroke="url(#{p}-rg)" stroke-width="1.3"/><text x="{w/2}" y="18.5" text-anchor="middle" class="jb" font-size="13" fill="{OW}">{t}</text></g></g>'
    body = f'''{bg}
<g clip-path="url(#{p}-clip)">
<g class="scan"><rect x="0" y="0" width="200" height="{H}" fill="url(#{p}-sw)"/></g>
<circle cx="{cx}" cy="{cy}" r="205" fill="url(#{p}-halo)"/>
{ring_anim}
<g class="port"><image href="data:image/png;base64,{IM['hero']}" x="524" y="129" width="360" height="411" preserveAspectRatio="xMidYMax meet"/></g>
</g>
{tags}
<g class="fu" style="animation-delay:.1s"><text x="52" y="92" class="jb" font-size="16" fill="{CR}">&gt; Hello, World! I’m</text><rect class="blink" x="{52+tw("> Hello, World! I’m","JB5",16)+5:.0f}" y="78" width="9" height="17" fill="{CR}"/></g>
<g clip-path="url(#{p}-n1)"><g class="rise" style="animation-delay:.25s"><text x="48" y="200" class="sg7" font-size="100" fill="{OW}" letter-spacing="-1">AKASH</text></g></g>
<g clip-path="url(#{p}-n2)"><g class="rise" style="animation-delay:.5s"><text x="48" y="294" class="sg7" font-size="100" fill="url(#{p}-nm)" letter-spacing="-1">YADAV</text></g></g>
<rect class="line" x="52" y="312" width="150" height="4" rx="2" fill="url(#{p}-grad)"/>
<g class="fu" style="animation-delay:1.1s"><text x="52" y="351" class="jb" font-size="13" fill="{OW}" fill-opacity=".55">ROLE //</text></g>
<g class="fu" style="animation-delay:1.1s">{role_svg}</g>
<g class="fu" style="animation-delay:1.4s"><rect x="52" y="378" width="{pill_w}" height="38" rx="19" fill="#0b1226" stroke="url(#{p}-grad)" stroke-width="1.4"/>
<circle cx="76" cy="397" r="5" fill="{BL}"/><circle class="ring" cx="76" cy="397" r="5" fill="none" stroke="{BL}" stroke-width="2"/>
<text x="94" y="402" class="in6" font-size="14" fill="{OW}" xml:space="preserve">{esc(pill_txt)}</text></g>
<g class="fu" style="animation-delay:1.6s">{pitch_svg}</g>
<g class="fu" style="animation-delay:1.8s"><g transform="translate(66 506)">{ico('pin', CR, 1.8)}</g>
<text x="88" y="511" class="in6" font-size="14" fill="{OW}">Ghazipur, Uttar Pradesh, India</text>
<text x="{88+tw('Ghazipur, Uttar Pradesh, India','IN6',14)+14:.0f}" y="511" class="jb" font-size="12.5" fill="{OW}" fill-opacity=".55">· Asia/Kolkata</text></g>
{border}'''
    return svg_wrap(p, W, H, 'Akash Yadav — Junior .NET Developer', 'Animated hero banner for Akash Yadav, Junior .NET Developer from Ghazipur, Uttar Pradesh, open to opportunities.', css, defs, body)


def about():
    p = 'abt'; W, H = 900, 600
    fd, bg, border = frame(p, W, H)
    css = base_css(['SG7', 'SG5', 'IN4', 'IN6', 'JB5'], """
.sl{opacity:0;animation:sl 12s infinite both}
.s1{opacity:1}
@keyframes sl{0%{opacity:0;transform:translateX(30px)}3.5%{opacity:1;transform:translateX(0)}29.8%{opacity:1;transform:translateX(0)}33.3%{opacity:0;transform:translateX(-30px)}100%{opacity:0;transform:translateX(-30px)}}
.pb{transform-box:fill-box;transform-origin:left center;animation:12s linear infinite both}
.pb1{animation-name:pb1}.pb2{animation-name:pb2}.pb3{animation-name:pb3}
@keyframes pb1{0%{transform:scaleX(0)}33.3%{transform:scaleX(1)}100%{transform:scaleX(1)}}
@keyframes pb2{0%{transform:scaleX(0)}33.3%{transform:scaleX(0)}66.6%{transform:scaleX(1)}100%{transform:scaleX(1)}}
@keyframes pb3{0%{transform:scaleX(0)}66.6%{transform:scaleX(0)}100%{transform:scaleX(1)}}
.cn{opacity:0;animation:cn 12s infinite both}
.c1{opacity:1}
@keyframes cn{0%{opacity:0}3.5%{opacity:1}29.8%{opacity:1}33.3%{opacity:0}100%{opacity:0}}
.only-static{display:none}
@media (prefers-reduced-motion:reduce){.only-static{display:inline}}
""")
    intro = wrap('I’m Akash, a Junior .NET Developer from Ghazipur, Uttar Pradesh. I build secure, scalable and maintainable web applications with ASP.NET Core, from clean REST APIs to well-structured SQL Server databases.', 'IN4', 15, 400)
    intro_svg = ''.join(f'<text x="52" y="{176+i*24}" class="in4" font-size="15" fill="{OW}" fill-opacity=".85">{esc(l)}</text>' for i, l in enumerate(intro))
    caps = ['REST API design with ASP.NET Core Web API', 'Authentication with ASP.NET Core Identity and JWT',
            'Data access with Entity Framework Core and SQL Server', 'Layered architecture with a service layer', 'MVC web applications with ASP.NET Core MVC']
    cy0 = 176 + len(intro) * 24 + 56
    caps_svg = ''
    y = cy0
    for i, c in enumerate(caps):
        ls = wrap(c, 'IN6', 14, 366)
        caps_svg += f'<g class="fu" style="animation-delay:{0.9+i*0.15}s"><circle cx="82" cy="{y-5}" r="11" fill="{BL}" fill-opacity=".16" stroke="{BL}" stroke-width="1.2"/><g transform="translate(82 {y-5}) scale(.5)">{ico("check", OW, 3)}</g>'
        for j, l in enumerate(ls):
            caps_svg += f'<text x="104" y="{y+j*19}" class="in6" font-size="14" fill="{OW}">{esc(l)}</text>'
        caps_svg += '</g>'
        y += 19 * len(ls) + 17
    # carousel
    def slide(cls, items, delay):
        out = f'<g class="sl {cls}" style="animation-delay:{delay}s">'
        n = len(items)
        ys = [250, 360] if n == 2 else [305]
        for (ic, label, sub), yy in zip(items, ys):
            out += f'<g transform="translate(560 {yy})"><circle r="38" fill="#0b1226" stroke="url(#{p}-grad)" stroke-width="1.6"/><circle r="38" fill="none" stroke="{BL}" stroke-opacity=".35" stroke-width="8" filter="url(#{p}-blur)"/><g transform="scale(1.35)">{ico(ic)}</g></g>'
            ls = wrap(label, 'SG7', 22, 210)
            for j, l in enumerate(ls):
                out += f'<text x="620" y="{yy+(-4 if len(ls)==1 else -14)+j*27+ (7 if len(ls)==1 else 0)}" class="sg7" font-size="22" fill="{OW}">{esc(l)}</text>'
        return out + '</g>'
    s1 = [('code', 'Coding & Learning New Technologies', ''), ('ai', 'Exploring AI Tools', '')]
    s2 = [('game', 'Gaming', ''), ('travel', 'Travelling', '')]
    s3 = [('movie', 'Watching Movies', '')]
    slides = slide('s1', s1, 0) + slide('s2', s2, 4) + slide('s3', s3, 8)
    prog = ''
    for i in range(3):
        x = 540 + i * 100
        prog += f'<rect x="{x}" y="470" width="88" height="5" rx="2.5" fill="#fff" fill-opacity=".12"/><rect class="pb pb{i+1}" x="{x}" y="470" width="88" height="5" rx="2.5" fill="url(#{p}-grad)"/>'
    counters = ''.join(f'<text class="cn c{i+1} jb" style="animation-delay:{i*4}s" x="820" y="466" text-anchor="end" font-size="13" fill="{OW}" fill-opacity=".7">0{i+1} / 03</text>' for i in range(3))
    defs = fd
    body = f'''{bg}
<g class="fu" style="animation-delay:.1s"><text x="52" y="82" class="jb" font-size="13" fill="{CR}">// 01</text>
<text x="52" y="124" class="sg7" font-size="42" fill="{OW}">About Me</text><rect x="54" y="136" width="96" height="4" rx="2" fill="url(#{p}-grad)"/></g>
<g class="fu" style="animation-delay:.35s">{intro_svg}</g>
<g class="fu" style="animation-delay:.6s"><text x="52" y="{cy0-26}" class="jb" font-size="13" fill="{BL}">PROFESSIONAL CAPABILITIES</text></g>
{caps_svg}
<g class="fu" style="animation-delay:.5s"><rect x="500" y="46" width="352" height="508" rx="24" fill="#0b1226" fill-opacity=".85" stroke="url(#{p}-edge)" stroke-width="1.6"/>
<text x="528" y="86" class="jb" font-size="13" fill="{CR}">// 02</text><text x="528" y="124" class="sg7" font-size="32" fill="{OW}">Interests</text></g>
<g class="fu" style="animation-delay:.9s"><g clip-path="url(#{p}-cc)">{slides}</g>{prog}{counters}
<text class="only-static in6" x="528" y="440" font-size="13" fill="{OW}" fill-opacity=".8">Also: Gaming · Travelling · Watching Movies</text></g>
{border}'''
    defs += f'<clipPath id="{p}-cc"><rect x="512" y="150" width="328" height="290"/></clipPath>'
    return svg_wrap(p, W, H, 'About Akash Yadav and interests', 'About me, professional capabilities and an animated three-slide interests carousel: coding and learning new technologies, exploring AI tools, gaming, travelling and watching movies.', css, defs, body)
