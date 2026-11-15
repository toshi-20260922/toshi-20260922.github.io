import asyncio,re
from playwright.async_api import async_playwright
SITE='/home/claude/toshi-20260922.github.io/site/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();errs=[]
        old=await b.new_page();await old.goto('file:///home/claude/pub/kokuho1116/old_houjinnari.html')
        for w in (360,1280):
            pg=await b.new_page(viewport={'width':w,'height':800});pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('file://'+SITE+'houjinnari/index.html')
            print(w,'はみ出し',await pg.evaluate('document.documentElement.scrollWidth-window.innerWidth'),await pg.inner_text('#o-reg'))
            print(' 既定800万',await pg.inner_text('#o-k'),await pg.inner_text('#o-h'),await pg.inner_text('#o-d'))
            # 表の「全額を報酬」と計算が合うか
            rows=await pg.evaluate('[...document.querySelectorAll("table.x7t13")[0].querySelectorAll("tr")].slice(1).map(r=>[r.children[0].textContent,r.children[12].childNodes[0].textContent])')
            bad=0
            for name,cell in rows:
                a=int(name.replace('万円','').replace(',',''))*10000
                await pg.evaluate('(a)=>{var i=document.getElementById("inc");i.value=a;i.dispatchEvent(new Event("input"));}',a)
                d=await pg.inner_text('#o-d');v=int(re.sub(r'[^0-9]','',d));v=-v if '−' in d else v
                exp=round(v/10000);got=int(cell.replace('−','-').replace('+',''))
                if exp!=got: bad+=1;print('  NG',name,cell,d)
            print(' 表の全額の列と計算',len(rows),'行 合わない',bad)
            # 大阪を選ぶと直す前と同じか
            await pg.select_option('#reg','15');print(' 大阪を選んだときの都道府県',await pg.evaluate('document.getElementById("pref").selectedOptions[0].textContent'))
            bad=0
            for o in (0,1):
                for a in range(3000000,20000001,430000):
                    for q in (pg,old): await q.evaluate('([a,o])=>{var i=document.getElementById("inc");i.value=a;i.dispatchEvent(new Event("input"));document.querySelectorAll("#s-age button")[o].click();}',[a,o])
                    x=[await pg.inner_text('#o-k'),await pg.inner_text('#o-h')];y=[await old.inner_text('#o-k'),await old.inner_text('#o-h')]
                    if x!=y: bad+=1;print('  NG',a,o,x,y)
            print(' 大阪で直す前と照らす 合わない',bad)
            await pg.select_option('#reg','x');await pg.select_option('#pref','40');print(' 料率欄',await pg.is_visible('#cust'),await pg.inner_text('#o-reg'))
            await pg.select_option('#reg','0');await pg.evaluate('document.querySelectorAll("#s-age button")[0].click()')
            await pg.screenshot(path=f'houjinnari_{w}.png',full_page=True);await pg.close()
        print('エラー',errs);await b.close()
asyncio.run(main())
