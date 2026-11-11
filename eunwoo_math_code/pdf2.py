import json, re, sys
from playwright.sync_api import sync_playwright
P='out2/project/'
cv=json.load(open(P+'canvas.json',encoding='utf-8'))
pages=[]
for fn in cv['order']:
    h=open(P+fn,encoding='utf-8').read()
    m=re.search(r'<x-dc>(.*)</x-dc>',h,re.S)
    inner=re.sub(r'<helmet>.*?</helmet>','',m.group(1),flags=re.S)
    pages.append(f'<section style="width:794px;height:1123px;page-break-after:always;break-after:page;overflow:hidden">{inner}</section>')
html='<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>@page{size:794px 1123px;margin:0}body{margin:0;-webkit-print-color-adjust:exact;print-color-adjust:exact}</style></head><body>'+''.join(pages)+'</body></html>'
open('book2.html','w',encoding='utf-8').write(html)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':794,'height':1123})
    pg.goto('file:///home/claude/gen/book2.html')
    pg.wait_for_timeout(800)
    pg.pdf(path='/home/claude/gen/eunwoo_math_book2.pdf',width='794px',height='1123px',print_background=True,prefer_css_page_size=True)
    # overflow report
    res=pg.evaluate('''()=>[...document.querySelectorAll('section')].map((s,i)=>{let bad=[];s.querySelectorAll('div').forEach(d=>{if(d.scrollHeight>d.clientHeight+3&&getComputedStyle(d).overflow==='hidden'&&d.clientHeight>0)bad.push(d.clientHeight+'/'+d.scrollHeight)});const r=s.firstElementChild;if(r.scrollHeight>r.clientHeight+1)bad.push('ROOT '+r.clientHeight+'/'+r.scrollHeight);return [i+1,bad.length,bad.slice(0,3).join(',')]}).filter(x=>x[1])''')
    print(res)
    b.close()
