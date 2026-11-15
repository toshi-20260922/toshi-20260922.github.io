import sys,asyncio,random
sys.path.insert(0,'.')
from regions import *
from playwright.async_api import async_playwright
SITE='/home/claude/toshi-20260922.github.io/site/'
PM_=None
G=[[58,63],[68,73],[78,83],[88,93],[98,101],[104,107],[110,114],[118,122],[126,130],[134,138],[142,146],[150,155],[160,165],[170,175],[180,185],[190,195],[200,210],[220,230],[240,250],[260,270],[280,290],[300,310],[320,330]]
def std(m):
    for a,b in G:
        if m<b*1000:return a*1000
    return 320000
def r50(n,d):
    q,rm=divmod(n,d);return q+1 if rm*2>d else q
def num(t): return int(''.join(ch for ch in t if ch.isdigit()) or 0)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        errs=[];bad=0;n=0
        for w in (360,1280):
            pg=await b.new_page(viewport={'width':w,'height':800})
            pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            # --- kokuho-keisan
            await pg.goto('file://'+SITE+'kokuho-keisan/index.html')
            ov=await pg.evaluate('document.documentElement.scrollWidth-window.innerWidth');print(w,'keisan はみ出し',ov)
            random.seed(1)
            for ri,r in enumerate(REG):
                await pg.select_option('#reg',str(ri))
                for a in [0,980000,1500000,2400000,4000000,6230000,9000000,15000000,25000000]+[random.randrange(0,12000000,10000) for _ in range(4)]:
                    for old in (0,1):
                        for fam,fo in ((0,0),(2,1),(3,3)):
                            await pg.evaluate('''([a,old,fam,fo])=>{var i=document.getElementById("inc");i.value=a;i.dispatchEvent(new Event("input"));document.querySelectorAll("#s-age button")[old].click();var f=document.getElementById("fam");f.value=fam;f.dispatchEvent(new Event("change"));var g=document.getElementById("famo");g.value=fo;g.dispatchEvent(new Event("change"));}''',[a,old,fam,fo])
                            got=num(await pg.inner_text('#o-y'));exp=kokuho(r,kyuyo7(a),old,fam,fo)[0];n+=1
                            if got!=exp: bad+=1;print('NG keisan',r['s'],a,old,fam,fo,got,exp)
            # 事業の所得
            await pg.evaluate('document.querySelectorAll("#s-k button")[1].click()')
            await pg.select_option('#reg','13')
            await pg.evaluate('''()=>{var i=document.getElementById("inc");i.value=0;i.dispatchEvent(new Event("input"));document.querySelectorAll("#s-age button")[0].click();["fam","famo"].forEach(function(k){var f=document.getElementById(k);f.value=0;f.dispatchEvent(new Event("change"));});}''')
            print(w,'名古屋 所得0 単身',await pg.inner_text('#o-y'),'(公式18,450)')
            # 料率を入れる
            await pg.select_option('#reg','x')
            vis=await pg.is_visible('#cust');v0=num(await pg.inner_text('#o-y'))
            await pg.fill('#c00','10');await pg.fill('#c01','50000');await pg.fill('#c02','30000')
            for k in ('c10','c11','c12','c20','c21','c22','c30','c31','c32'): await pg.fill('#'+k,'0')
            await pg.evaluate('''()=>{var i=document.getElementById("inc");i.value=3430000;i.dispatchEvent(new Event("input"));}''')
            print(w,'料率を入れる欄 表示',vis,'直前の地域の額',v0,'→ 所得343万・10%+5万+3万 =',await pg.inner_text('#o-y'),'(手計算 380,000)')
            ov=await pg.evaluate('document.documentElement.scrollWidth-window.innerWidth');print(w,'keisan 料率欄を開いたはみ出し',ov)
            await pg.screenshot(path=f'keisan_{w}.png',full_page=True)
            # --- kokuho
            await pg.goto('file://'+SITE+'kokuho/index.html')
            ov=await pg.evaluate('document.documentElement.scrollWidth-window.innerWidth');print(w,'kokuho はみ出し',ov)
            from build_pm import PM
            for ri,r in enumerate(REG):
                await pg.select_option('#reg',str(ri))
                pv=await pg.evaluate('document.getElementById("pref").selectedOptions[0].textContent')
                if not pv.startswith(PM[r['s']]): bad+=1;print('NG pref',r['s'],pv)
                rate=dict(PREF)[PM[r['s']]]
                for a in [1000000,2000000,3000000,4000000,5000000,7000000,12000000]+[random.randrange(1000000,12000000,10000) for _ in range(3)]:
                    for old in (0,1):
                        for hi in (0,1):
                            for fam in (0,2):
                                await pg.evaluate('''([a,old,hi,fam])=>{var i=document.getElementById("inc");i.value=a;i.dispatchEvent(new Event("input"));document.querySelectorAll("#s-age button")[old].click();document.querySelectorAll("#s-hi button")[hi].click();var f=document.getElementById("fam");f.value=fam;f.dispatchEvent(new Event("change"));}''',[a,old,hi,fam])
                                g=kyuyo7(a)
                                if hi: g=g*30//100
                                ek=kokuho(r,g,old,fam,fam if old else 0)[0];en=r50(std(a//12)*(rate+23+(162 if old else 0)),10000)*12
                                gk=num(await pg.inner_text('#o-k'));gn=num(await pg.inner_text('#o-n'));n+=1
                                if (gk,gn)!=(ek,en): bad+=1;print('NG kokuho',r['s'],a,old,hi,fam,gk,ek,gn,en)
            await pg.select_option('#pref','40');await pg.select_option('#reg','x')
            print(w,'kokuho 料率欄',await pg.is_visible('#cust'),await pg.inner_text('#e-k'),await pg.inner_text('#e-n'))
            await pg.screenshot(path=f'kokuho_{w}.png',full_page=True)
            await pg.close()
        print('照らした件数',n,'合わない',bad,'エラー',errs)
        await b.close()
asyncio.run(main())
