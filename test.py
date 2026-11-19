import re, math, json, glob, os
from playwright.sync_api import sync_playwright
from PIL import Image
names=['hero','about-life','stack','id-dashboard','connect']
A='/home/claude/work/pkg/assets/'
rep={}
times=[0,2,5,9,13]
with sync_playwright() as p:
    b=p.chromium.launch()
    # 1 + text clipping + external requests
    for n in names:
        reqs=[]
        pg=b.new_page(viewport={'width':900,'height':900})
        pg.on('request',lambda r:reqs.append(r.url))
        pg.goto(f'file://{A}{n}.svg')
        W,H=pg.evaluate("[document.documentElement.viewBox.baseVal.width,document.documentElement.viewBox.baseVal.height]")
        bad=[]
        for t in times:
            pg.evaluate("t=>{const s=document.documentElement;s.pauseAnimations();s.setCurrentTime(t);document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});}",t)
            pg.wait_for_timeout(80)
            pg.screenshot(path=f'shots/{n}_{t}.png',clip={'x':0,'y':0,'width':W,'height':H})
        # clipping check at end state (all css anims finished -> t=14s)
        pg.evaluate("t=>{document.documentElement.setCurrentTime(t);document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});}",14)
        res=pg.evaluate("""()=>{const out=[];document.querySelectorAll('text').forEach(t=>{const r=t.getBoundingClientRect();if(r.width==0)return;
          if(r.left<8||r.top<2||r.right>892||r.bottom>document.documentElement.viewBox.baseVal.height-2)out.push([t.textContent.slice(0,30),Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)])});return out}""")
        ext=[u for u in reqs if not u.startswith('file://') and not u.startswith('data:')]
        rep[n]={'size':(W,H),'text_out_of_bounds':res,'external_requests':ext}
        pg.close()
    # reduced motion render
    for n in names:
        ctx=b.new_context(reduced_motion='reduce',viewport={'width':900,'height':900}); pg=ctx.new_page()
        pg.goto(f'file://{A}{n}.svg'); pg.wait_for_timeout(300)
        H=pg.evaluate("document.documentElement.viewBox.baseVal.height")
        pg.screenshot(path=f'shots/{n}_reduced.png',clip={'x':0,'y':0,'width':900,'height':H}); ctx.close()
    # img element tests desktop + mobile
    for label,w in [('img830',830),('img390',390)]:
        for n in names:
            pg=b.new_page(viewport={'width':w+40,'height':900})
            open('/home/claude/work/pkg/_t.html','w').write(f'<body style="margin:0;background:#0d1117;padding:20px"><img id=i src="assets/{n}.svg" style="width:{w}px;display:block"></body>')
            pg.goto('file:///home/claude/work/pkg/_t.html')
            pg.wait_for_timeout(1800)
            el=pg.query_selector('#i'); ok=pg.evaluate("document.getElementById('i').naturalWidth>0")
            el.screenshot(path=f'shots/{n}_{label}.png'); rep[n][label+'_loaded']=ok; pg.close()
    # pendulum angle sampling
    pg=b.new_page(viewport={'width':900,'height':900}); pg.goto(f'file://{A}id-dashboard.svg')
    angs=pg.evaluate("""()=>{const s=document.documentElement;s.pauseAnimations();const g=document.querySelector('animateTransform').parentNode; const r=[];
      for(let t=0;t<=40;t+=0.1){s.setCurrentTime(t);const m=g.getCTM();const a=Math.atan2(m.b,m.a)*180/Math.PI;r.push([t,a])}return r}""")
    rep['pendulum']={'max_0_1.0s':max(abs(a) for t,a in angs if t<1.0),'peak_2_4s':max(abs(a) for t,a in angs if 1.5<t<4),'peak_30_40s':max(abs(a) for t,a in angs if t>30),'max_after_30':max(a for t,a in angs if t>30),'min_after_30':min(a for t,a in angs if t>30)}
    pg.close()
    # orbit collisions
    pg=b.new_page(viewport={'width':900,'height':900}); pg.goto(f'file://{A}stack.svg')
    col=pg.evaluate("""()=>{const s=document.documentElement;s.pauseAnimations();const gs=[...document.querySelectorAll('g.anim > g')];let worst=[];
      for(let t=0;t<44;t+=1){s.setCurrentTime(t);const bb=gs.map(g=>g.getBoundingClientRect());
        for(let i=0;i<bb.length;i++)for(let j=i+1;j<bb.length;j++){const a=bb[i],b=bb[j];const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left),oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);if(ox>0&&oy>0)worst.push([t,i,j,Math.round(ox),Math.round(oy)])}}
      return {n:gs.length,overlaps:worst.length,sample:worst.slice(0,8)}}""")
    rep['orbit_collisions']=col
    b.close()
# static checks
svgs={n:open(f'{A}{n}.svg').read() for n in names}
for n,s in svgs.items():
    chk={}
    chk['script']='<script' in s; chk['foreignObject']='foreignObject' in s.lower()
    urls=set(re.findall(r'(?:href|src)="(?!data:|#)([^"]+)"',s)); chk['external_hrefs']=sorted(urls)
    chk['http_urls_outside_xmlns']=[u for u in re.findall(r'https?://[^\s"\')]+',s) if 'www.w3.org' not in u]
    chk['url_refs_http']=len(re.findall(r'url\(\s*["\']?https?:',s))
    chk['has_reduced_motion']='prefers-reduced-motion' in s
    chk['fill_mode_both_css']=len(re.findall(r'animation:[^;}]*\bboth\b',s))
    ids=re.findall(r'\bid="([^"]+)"',s); chk['dup_ids']=[i for i in set(ids) if ids.count(i)>1]
    chk['id_prefixes']=sorted({i.split('-')[0] for i in ids})
    chk['smil_begin_nonzero']=re.findall(r'begin="(?!0s")[^"]*"',s)
    chk['kb']=len(s)//1024
    rep[n].update(chk)
# PNG alpha
for f in ['id.png','right_pointing.png']:
    im=Image.open('/home/claude/work/pkg/assets/'+f); import numpy as np; a=np.array(im)[...,3]
    rep['png_'+f]={'mode':im.mode,'transparent_frac':round(float((a==0).mean()),3),'corners':[int(a[0,0]),int(a[0,-1]),int(a[-1,0]),int(a[-1,-1])],'size':im.size}
# README link check
rd=open('/home/claude/work/pkg/README.md').read()
rep['readme']={'links':sorted(set(re.findall(r'https?://[^\s)>\]]+',rd))),'youtube':'youtube' in rd.lower(),'img_order':re.findall(r'!\[(\w[\w ]*)\]\(([^)]+)\)',rd)}
json.dump(rep,open('report.json','w'),indent=1,default=str)
print(json.dumps(rep,indent=1,default=str)[:6500])
