from common import *


def tiles(p, names):
    """Tile symbols centered at 0,0 (44px). Official icons where they exist, labelled monograms elsewhere."""
    icons = {
        'csharp': ('devicon/icons/csharp/csharp-original.svg', None),
        'sql': ('devicon/icons/microsoftsqlserver/microsoftsqlserver-plain.svg', None),
        'html': ('devicon/icons/html5/html5-original.svg', None),
        'css': ('devicon/icons/css3/css3-original.svg', None),
        'github': ('simple-icons/icons/github.svg', OW),
        'jwt': ('simple-icons/icons/jsonwebtokens.svg', OW),
    }
    mono = {'linq': 'LINQ', 'ef': 'EF', 'mvc': 'MVC', 'api': 'API', 'rest': 'REST'}
    out = ''
    for n in names:
        tile = f'<rect x="-22" y="-22" width="44" height="44" rx="12" fill="#0b1226" stroke="url(#{p}-edge)" stroke-width="1.6"/>'
        if n in icons:
            path, fill = icons[n]
            out += f'<g id="{p}-t-{n}">{tile}<g transform="translate(-13 -13)">{symbol(f"{p}-i-{n}", path, f"{p}{n}", fill).replace("<symbol", "<svg width=\"26\" height=\"26\"").replace("</symbol>", "</svg>")}</g></g>'
        else:
            t = mono[n]; fs = 10 if len(t) > 3 else 12.5
            out += f'<g id="{p}-t-{n}">{tile}<text y="{fs*.36:.1f}" text-anchor="middle" class="jb" font-size="{fs}" fill="url(#{p}-grad)">{t}</text></g>'
    return out


def keypts(rx, ry, th0, N=72, sg=1):
    def s(d, M=400):
        return sum(math.hypot(rx * math.sin(th0 + sg * d * (i + .5) / M), ry * math.cos(th0 + sg * d * (i + .5) / M)) for i in range(M)) * d / M
    L = s(2 * math.pi)
    kp = [s(2 * math.pi * k / N) / L for k in range(N + 1)]; kp[-1] = 1.0
    return ';'.join(f'{v:.5f}' for v in kp), ';'.join(f'{k/N:.5f}' for k in range(N + 1))


def stack():
    p = 'stk'; W, H = 900, 828
    fd, bg, border = frame(p, W, H)
    css = base_css(['SG7', 'SG5', 'IN4', 'IN6', 'JB5'], """
.pop{animation:pop .9s cubic-bezier(.2,.9,.3,1.2) both;transform-box:fill-box;transform-origin:center}
@keyframes pop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:scale(1)}}
""")
    names = ['csharp', 'linq', 'ef', 'mvc', 'api', 'rest', 'jwt', 'sql', 'html', 'css', 'github']
    labels = {'csharp': ['C#'], 'linq': ['LINQ'], 'ef': ['Entity Framework', 'Core'], 'mvc': ['ASP.NET Core', 'MVC'], 'api': ['ASP.NET Core', 'Web API'],
              'rest': ['REST APIs'], 'jwt': ['JWT', 'Authentication'], 'sql': ['SQL Server'], 'html': ['HTML'], 'css': ['CSS'], 'github': ['GitHub']}
    cx, cy = 450, 302
    def ang(*a): return [math.radians(x) for x in a]
    orbits = [(132, 92, ['csharp', 'linq', 'ef'], ang(0, 120, 240), 30, 1), (262, 132, ['mvc', 'api', 'rest', 'jwt'], ang(285, 15, 105, 195), 44, -1), (392, 170, ['sql', 'html', 'css', 'github'], ang(51, 141, 231, 321), 60, 1)]
    defs = fd + tiles(p, names) + symbol(f'{p}-net', 'simple-icons/icons/dotnet.svg', f'{p}net', OW)
    defs += f'<radialGradient id="{p}-core" cx=".5" cy=".4" r=".7"><stop offset="0" stop-color="#7a52ff"/><stop offset="1" stop-color="#512BD4"/></radialGradient>'
    orb_svg = ''; nodes_anim = ''; nodes_stat = ''
    for (rx, ry, items, angs, dur, sgn) in orbits:
        orb_svg += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry:.1f}" fill="none" stroke="url(#{p}-edge)" stroke-width="1.4" stroke-dasharray="2 7" stroke-linecap="round" opacity=".9"/>'
        n = len(items)
        for i, it in enumerate(items):
            th = angs[i]
            x0, y0 = cx + rx * math.cos(th), cy + ry * math.sin(th)
            x1, y1 = cx - rx * math.cos(th), cy - ry * math.sin(th)
            sw = 1 if sgn > 0 else 0
            path = f'M{x0:.1f} {y0:.1f}A{rx} {ry:.2f} 0 1 {sw} {x1:.1f} {y1:.1f}A{rx} {ry:.2f} 0 1 {sw} {x0:.1f} {y0:.1f}Z'
            lw = max(tw(t, 'IN6', 11.5) for t in labels[it]) + 12
            lab = f'<rect x="{-lw/2:.1f}" y="29" width="{lw:.1f}" height="{13*len(labels[it])+6}" rx="8" fill="{BG}" fill-opacity=".85"/>' + ''.join(f'<text y="{42+j*13}" text-anchor="middle" class="in6" font-size="11.5" fill="{OW}">{esc(t)}</text>' for j, t in enumerate(labels[it]))
            node = f'<use href="#{p}-t-{it}"/>{lab}'
            kp, kt = keypts(rx, ry, th, 72, sgn)
            nodes_anim += f'<g><animateMotion path="{path}" dur="{dur}s" begin="0s" repeatCount="indefinite" calcMode="linear" keyPoints="{kp}" keyTimes="{kt}"/>{node}</g>'
            nodes_stat += f'<g transform="translate({x0:.1f} {y0:.1f})">{node}</g>'
    # groups
    groups = [('LANGUAGE', ['csharp', 'linq']), ('BACKEND', ['mvc', 'api', 'rest']), ('DATA & SECURITY', ['ef', 'sql', 'jwt']), ('FRONTEND & TOOLS', ['html', 'css', 'github'])]
    names_full = {'csharp': 'C#', 'linq': 'LINQ', 'ef': 'Entity Framework Core', 'mvc': 'ASP.NET Core MVC', 'api': 'ASP.NET Core Web API', 'rest': 'REST APIs',
                  'jwt': 'JWT Authentication', 'sql': 'SQL Server', 'html': 'HTML', 'css': 'CSS', 'github': 'GitHub'}
    gsvg = ''
    gw, gh = 400, 118
    for gi, (gt, its) in enumerate(groups):
        gx = 40 + (gi % 2) * (gw + 20); gy = 542 + (gi // 2) * (gh + 16)
        gsvg += f'<g class="fu" style="animation-delay:{0.7+gi*0.18}s"><rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="20" fill="#0b1226" fill-opacity=".85" stroke="url(#{p}-edge)" stroke-width="1.4"/>'
        gsvg += f'<text x="{gx+22}" y="{gy+30}" class="jb" font-size="12" fill="{BL if gi%2==0 else CR}" letter-spacing="1">{esc(gt)}</text>'
        x, y = gx + 22, gy + 46
        for it in its:
            lab = names_full[it]; w = tw(lab, 'IN6', 13) + 52
            if x + w > gx + gw - 18: x = gx + 22; y += 38
            gsvg += f'<g><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="32" rx="16" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".14"/><g transform="translate({x+18:.0f} {y+16}) scale(.55)"><use href="#{p}-t-{it}"/></g><text x="{x+36:.0f}" y="{y+21}" class="in6" font-size="13" fill="{OW}">{esc(lab)}</text></g>'
            x += w + 10
        gsvg += '</g>'
    center = f'''<circle class="ring" cx="{cx}" cy="{cy}" r="38" fill="none" stroke="{BL}" stroke-width="2"/>
<circle cx="{cx}" cy="{cy}" r="56" fill="url(#{p}-gB)"/>
<circle cx="{cx}" cy="{cy}" r="38" fill="url(#{p}-core)" stroke="{OW}" stroke-opacity=".35" stroke-width="1.5"/>
<use href="#{p}-net" x="{cx-23}" y="{cy-23}" width="46" height="46"/>'''
    body = f'''{bg}
<g class="fu"><text x="52" y="62" class="jb" font-size="13" fill="{CR}">// 03</text><text x="52" y="102" class="sg7" font-size="38" fill="{OW}">Technology Stack</text><rect x="54" y="114" width="96" height="4" rx="2" fill="url(#{p}-grad)"/></g>
{orb_svg}
<g class="anim">{nodes_anim}</g><g class="stat">{nodes_stat}</g>
<g class="pop" style="animation-delay:.3s">{center}</g>
{gsvg}
{border}'''
    return svg_wrap(p, W, H, 'Technology stack', 'Animated technology orbit around .NET: C#, LINQ, Entity Framework Core, ASP.NET Core MVC, ASP.NET Core Web API, REST APIs, JWT authentication, SQL Server, HTML, CSS and GitHub.', css, defs, body)


def damped():
    pts = []; T = 13.5; t0 = 1.05; n = 90
    for k in range(n + 1):
        t = T * k / n
        a = 0 if t < t0 else 8.5 * math.exp(-(t - t0) / 3.0) * math.sin(2 * math.pi * (t - t0) / 3.6)
        if k == n: a = 0
        pts.append((t / T, a))
    return ';'.join(f'{a:.3f} 450 0' for _, a in pts), ';'.join(f'{t:.4f}' for t, _ in pts), T


def idcard():
    p = 'idc'; W, H = 900, 850
    fd, bg, border = frame(p, W, H)
    css = base_css(['SG7', 'SG5', 'IN4', 'IN6', 'JB5'], """
.drop{animation:drop 1.4s cubic-bezier(.3,.7,.4,1) both}
@keyframes drop{0%{opacity:0;transform:translateY(-760px)}8%{opacity:1}52%{transform:translateY(16px)}72%{transform:translateY(-7px)}88%{transform:translateY(3px)}100%{transform:translateY(0)}}
.sweep{animation:sweep 5.5s 1.6s ease-in-out infinite both}
@keyframes sweep{0%{transform:translateX(-460px)}38%{transform:translateX(460px)}100%{transform:translateX(460px)}}
.pan{animation:fu .9s both}
""")
    cx0, cy0, cw, ch = 285, 196, 330, 584
    cardimg = f'<image href="data:image/png;base64,{IM["card"]}" x="0" y="0" width="280" height="{280*286/340:.1f}"/>'
    ph = 280 * 286 / 340
    bars = ''; x = 0; import random; rnd = random.Random(21)
    while x < 270:
        w = rnd.choice([2, 2, 3, 4]); bars += f'<rect x="{x}" y="0" width="{w}" height="40"/>'; x += w + rnd.choice([2, 3, 3, 5])
    def card(anim):
        sweep = f'<g clip-path="url(#{p}-cc)"><g class="sweep"><polygon points="120,-20 190,-20 130,{ch+20} 60,{ch+20}" fill="url(#{p}-foil)"/></g></g>' if anim else ''
        return f'''<g transform="translate({cx0} {cy0})">
<rect width="{cw}" height="{ch}" rx="24" fill="url(#{p}-body)" stroke="url(#{p}-edge)" stroke-width="2.4"/>
<rect x="2" y="2" width="{cw-4}" height="{ch-4}" rx="22" fill="url(#{p}-dots)"/>
<rect x="{cw/2-36}" y="16" width="72" height="12" rx="6" fill="{BG}" stroke="#fff" stroke-opacity=".18"/>
<text x="{cw/2}" y="56" text-anchor="middle" class="jb" font-size="11" fill="{OW}" fill-opacity=".6" letter-spacing="3">DEVELOPER ID</text>
<g transform="translate(25 70)"><clipPath id="{p}-ph{int(anim)}"><rect width="280" height="{ph:.1f}" rx="16"/></clipPath>
<g clip-path="url(#{p}-ph{int(anim)})"><rect width="280" height="{ph:.1f}" fill="url(#{p}-pbg)"/><rect width="280" height="{ph:.1f}" fill="url(#{p}-dots)"/>{cardimg}</g>
<rect width="280" height="{ph:.1f}" rx="16" fill="none" stroke="url(#{p}-edge)" stroke-width="1.6"/></g>
<text x="{cw/2}" y="{70+ph+46:.0f}" text-anchor="middle" class="sg7" font-size="31" fill="{OW}">AKASH YADAV</text>
<text x="{cw/2}" y="{70+ph+72:.0f}" text-anchor="middle" class="in6" font-size="15" fill="{BL}">Junior .NET Developer</text>
<rect x="{cw/2-95}" y="{70+ph+88:.0f}" width="190" height="26" rx="13" fill="{BL}" fill-opacity=".14" stroke="{BL}" stroke-opacity=".6"/>
<circle cx="{cw/2-76}" cy="{70+ph+101:.0f}" r="4" fill="{BL}"/><text x="{cw/2-64}" y="{70+ph+106:.0f}" class="in6" font-size="12" fill="{OW}">Open to Opportunities</text>
<g class="jb" font-size="10.5"><text x="32" y="{70+ph+140:.0f}" fill="{OW}" fill-opacity=".5">BASE</text><text x="86" y="{70+ph+140:.0f}" fill="{OW}">Ghazipur, Uttar Pradesh, India</text>
<text x="32" y="{70+ph+160:.0f}" fill="{OW}" fill-opacity=".5">ZONE</text><text x="86" y="{70+ph+160:.0f}" fill="{OW}">Asia/Kolkata</text></g>
<g transform="translate(30 {ch-86})" fill="{OW}" fill-opacity=".9">{bars}</g>
<text x="{cw/2}" y="{ch-24}" text-anchor="middle" class="jb" font-size="11" fill="{OW}" fill-opacity=".65" letter-spacing="1.5">aakashh-yadavv</text>
{sweep}</g>'''
    lan = f'''<polygon points="341,-70 382,-70 462,126 436,126" fill="url(#{p}-strap)"/><polygon points="559,-70 518,-70 438,126 464,126" fill="url(#{p}-strap)" opacity=".92"/>
<g fill="{OW}" fill-opacity=".85" class="jb" font-size="8"><text transform="translate(388 14) rotate(66)" >AKASH · .NET</text></g>
<ellipse cx="450" cy="188" rx="11" ry="26" fill="none" stroke="url(#{p}-metal)" stroke-width="5"/>
<rect x="428" y="116" width="44" height="40" rx="10" fill="url(#{p}-metal)" stroke="#fff" stroke-opacity=".4"/><rect x="436" y="124" width="28" height="8" rx="4" fill="#000" fill-opacity=".25"/><circle cx="450" cy="146" r="4" fill="#000" fill-opacity=".3"/>'''
    dr, kt, T = damped()
    swing = f'''<g>
<animateTransform attributeName="transform" type="rotate" values="{dr}" keyTimes="{kt}" calcMode="linear" dur="{T}s" begin="0s" repeatCount="1" additive="sum" fill="freeze"/>
<animateTransform attributeName="transform" type="rotate" values="0 450 0;1.2 450 0;1.7 450 0;1.2 450 0;0 450 0;-1.2 450 0;-1.7 450 0;-1.2 450 0;0 450 0" keyTimes="0;.125;.25;.375;.5;.625;.75;.875;1" calcMode="linear" dur="3.6s" begin="0s" repeatCount="indefinite" additive="sum"/>
{{CARD}}</g>'''
    def hang(anim):
        c = card(anim)
        return lan + c
    defs = fd + f'''<clipPath id="{p}-cc"><rect width="{cw}" height="{ch}" rx="24"/></clipPath>
<linearGradient id="{p}-body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101a36"/><stop offset="1" stop-color="#090e1d"/></linearGradient>
<linearGradient id="{p}-pbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BL}" stop-opacity=".55"/><stop offset="1" stop-color="{CR}" stop-opacity=".45"/></linearGradient>
<linearGradient id="{p}-foil" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<linearGradient id="{p}-strap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BL}"/><stop offset="1" stop-color="{CR}"/></linearGradient>
<linearGradient id="{p}-metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f6fb"/><stop offset=".45" stop-color="#8d96ab"/><stop offset=".6" stop-color="#d9deea"/><stop offset="1" stop-color="#6c7590"/></linearGradient>'''
    def panel(x, title, sub, content, delay):
        return f'<g class="pan" style="animation-delay:{delay}s"><rect x="{x}" y="250" width="214" height="330" rx="20" fill="#0b1226" fill-opacity=".85" stroke="url(#{p}-edge)" stroke-width="1.4"/><text x="{x+20}" y="282" class="jb" font-size="11.5" fill="{BL}" letter-spacing="1">{title}</text><text x="{x+20}" y="300" class="jb" font-size="10.5" fill="{CR}">{sub}</text>{content}</g>'
    left = f'''<text x="56" y="372" class="sg7" font-size="76" fill="url(#{p}-grad)">8</text>
<text x="56" y="400" class="in6" font-size="14" fill="{OW}">Public repositories</text>
<rect x="56" y="420" width="170" height="1" fill="#fff" fill-opacity=".14"/>
<text x="56" y="448" class="jb" font-size="10.5" fill="{OW}" fill-opacity=".55">LoanManagmentSystem</text><text x="56" y="466" class="in6" font-size="14" fill="{OW}">2 commits</text>
<text x="56" y="498" class="jb" font-size="10.5" fill="{OW}" fill-opacity=".55">CoachingManagmentSystem</text><text x="56" y="516" class="in6" font-size="14" fill="{OW}">5 commits</text>
<text x="56" y="552" class="in4" font-size="10" fill="{OW}" fill-opacity=".5">Source: github.com/aakashh-yadavv</text>'''
    rows = [('Loan Management System', 'Backend completed'), ('Coaching Management System', 'ASP.NET Core Web API'), ('Employee Management System', 'ASP.NET Core MVC'), ('Shop Management', 'Live web app')]
    right = ''.join(f'<g><circle cx="{666+0}" cy="{334+i*60}" r="4" fill="{BL if i%2==0 else CR}"/><text x="680" y="{338+i*60}" class="in6" font-size="12.5" fill="{OW}">{esc(a)}</text><text x="680" y="{356+i*60}" class="jb" font-size="10.5" fill="{OW}" fill-opacity=".55">{esc(b)}</text></g>' for i, (a, b) in enumerate(rows))
    body = f'''{bg}
<g class="fu"><text x="52" y="62" class="jb" font-size="13" fill="{CR}">// 04</text><text x="52" y="102" class="sg7" font-size="38" fill="{OW}">Developer ID</text><rect x="54" y="114" width="96" height="4" rx="2" fill="url(#{p}-grad)"/></g>
{panel(40, 'GITHUB SNAPSHOT', 'VERIFIED 19 NOV 2026', left, 1.5)}
{panel(646, 'FEATURED BUILDS', 'SEE PROJECTS BELOW', right, 1.7)}
<g class="anim"><g class="drop"><g>{swing.replace('{CARD}', hang(True))}</g></g></g>
<g class="stat">{hang(False)}</g>
{border}'''
    return svg_wrap(p, W, H, 'Developer ID dashboard', 'A hanging developer ID card for Akash Yadav, Junior .NET Developer, with a swinging pendulum animation and a dated GitHub snapshot.', css, defs, body)


def connect():
    p = 'con'; W, H = 900, 440
    fd, bg, border = frame(p, W, H)
    css = base_css(['SG7', 'SG5', 'IN4', 'IN6', 'JB5'], """
.nudge{animation:nudge 1.4s ease-in-out infinite both}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(9px)}}
.ch{animation:chev 1.5s ease-in-out infinite both}
@keyframes chev{0%{opacity:.15;transform:translateX(-6px)}50%{opacity:1;transform:translateX(2px)}100%{opacity:.15;transform:translateX(8px)}}
.slide{animation:slide .9s cubic-bezier(.2,.7,.2,1) both}
@keyframes slide{from{opacity:0;transform:translateX(40px)}to{opacity:1;transform:translateX(0)}}
""")
    defs = fd + symbol(f'{p}-gh', 'simple-icons/icons/github.svg', f'{p}gh', OW) + symbol(f'{p}-li', 'devicon/icons/linkedin/linkedin-original.svg', f'{p}li') + symbol(f'{p}-ig', 'simple-icons/icons/instagram.svg', f'{p}ig', f'url(#{p}-igg)')
    defs += f'<linearGradient id="{p}-igg" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#feda75"/><stop offset=".25" stop-color="#fa7e1e"/><stop offset=".5" stop-color="#d62976"/><stop offset=".75" stop-color="#962fbf"/><stop offset="1" stop-color="#4f5bd5"/></linearGradient>'
    defs += f'<radialGradient id="{p}-halo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{BL}" stop-opacity=".5"/><stop offset=".6" stop-color="{CR}" stop-opacity=".18"/><stop offset="1" stop-color="{CR}" stop-opacity="0"/></radialGradient>'
    cards = [('gh', 'GitHub', 'github.com/aakashh-yadavv'), ('li', 'LinkedIn', 'linkedin.com/in/akash-yadav2135'), ('ig', 'Instagram', 'instagram.com/aakashhx21')]
    csvg = ''
    for i, (k, name, url) in enumerate(cards):
        y = 92 + i * 112
        csvg += f'''<g class="slide" style="animation-delay:{0.4+i*0.18}s"><rect x="390" y="{y}" width="468" height="92" rx="22" fill="#0b1226" fill-opacity=".9" stroke="url(#{p}-edge)" stroke-width="1.6"/>
<rect x="414" y="{y+18}" width="56" height="56" rx="15" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".12"/><use href="#{p}-{k}" x="{428}" y="{y+32}" width="28" height="28"/>
<text x="490" y="{y+42}" class="sg7" font-size="25" fill="{OW}">{name}</text><text x="490" y="{y+66}" class="jb" font-size="13" fill="{OW}" fill-opacity=".7">{url}</text>
<g class="nudge" style="animation-delay:{-i*0.3}s"><circle cx="824" cy="{y+46}" r="19" fill="url(#{p}-grad)"/><g transform="translate(824 {y+46}) scale(.85)">{ico('arrow', OW, 2.4)}</g></g></g>'''
    chev = ''.join(f'<g class="ch" style="animation-delay:{i*0.22}s"><path d="M{300+i*24} 214l14 14-14 14" fill="none" stroke="{CR if i%2 else BL}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></g>' for i in range(3))
    img_w = 262; img_h = img_w * 482 / 300
    body = f'''{bg}
<g clip-path="url(#{p}-clip)"><circle cx="150" cy="240" r="190" fill="url(#{p}-halo)"/>
<image class="fi" href="data:image/png;base64,{IM['point']}" x="22" y="{H-img_h:.1f}" width="{img_w}" height="{img_h:.1f}" preserveAspectRatio="xMidYMax meet"/></g>
<g class="fu" style="animation-delay:.1s"><text x="390" y="54" class="jb" font-size="13" fill="{CR}">// 05</text></g>
<g class="fu" style="animation-delay:.1s"><text x="440" y="54" class="sg7" font-size="22" fill="{OW}">Let’s Connect</text></g>
{chev}
{csvg}
{border}'''
    return svg_wrap(p, W, H, 'Connect with Akash Yadav', 'Social cards for GitHub, LinkedIn and Instagram with animated arrows.', css, defs, body)
