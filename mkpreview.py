from markdown_it import MarkdownIt
md=MarkdownIt('commonmark').enable('table')
body=md.render(open('pkg/README.md').read())
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Akash Yadav — README preview</title>
<style>
:root{{color-scheme:dark}}
body{{margin:0;background:#0d1117;color:#e6edf3;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
.bar{{position:sticky;top:0;z-index:5;background:#161b22;border-bottom:1px solid #30363d;padding:10px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;font-size:14px}}
.bar b{{margin-right:auto}}
.bar button{{background:#21262d;color:#e6edf3;border:1px solid #30363d;border-radius:8px;padding:6px 12px;cursor:pointer}}
.bar button.on{{background:#1f6feb;border-color:#1f6feb}}
#frame{{margin:24px auto;max-width:888px;padding:32px;background:#0d1117;border:1px solid #30363d;border-radius:12px;box-sizing:border-box;transition:max-width .25s}}
#frame.mobile{{max-width:390px;padding:16px}}
#frame img{{max-width:100%;display:block;margin:0 0 16px}}
#frame p{{margin:0 0 16px}}
#frame h2{{padding-bottom:.3em;border-bottom:1px solid #30363d;font-size:1.5em;margin:24px 0 16px}}
#frame a{{color:#4493f8;text-decoration:none}}#frame a:hover{{text-decoration:underline}}
#frame table{{border-collapse:collapse;display:block;overflow:auto;width:100%;margin-bottom:16px}}
#frame th,#frame td{{border:1px solid #30363d;padding:6px 13px;vertical-align:top;font-size:14px}}
#frame tr:nth-child(2n){{background:#151b23}}
#frame li{{margin:4px 0}}
</style></head><body>
<div class="bar"><b>README preview (GitHub-style dark)</b>
<button id="d" class="on">Desktop 888px</button><button id="m">Mobile 390px</button><button id="r">Replay animations</button></div>
<main id="frame">{body}</main>
<script>
const f=document.getElementById('frame'),d=document.getElementById('d'),m=document.getElementById('m');
d.onclick=()=>{{f.classList.remove('mobile');d.classList.add('on');m.classList.remove('on')}};
m.onclick=()=>{{f.classList.add('mobile');m.classList.add('on');d.classList.remove('on')}};
document.getElementById('r').onclick=()=>{{document.querySelectorAll('#frame img').forEach(i=>{{const s=i.getAttribute('src').split('?')[0];i.src=s+'?v='+Date.now()}})}};
</script></body></html>'''
open('pkg/preview.html','w').write(html)
print(len(html))
