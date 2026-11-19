import sys; sys.path.insert(0,'/home/claude/work')
import xml.dom.minidom as md
import gen_a, gen_b
out={'hero':gen_a.hero(),'about-life':gen_a.about(),'stack':gen_b.stack(),'id-dashboard':gen_b.idcard(),'connect':gen_b.connect()}
for k,v in out.items():
    md.parseString(v.encode())
    open(f'/home/claude/work/pkg/assets/{k}.svg','w').write(v)
    print(k,len(v)//1024,'KB')
