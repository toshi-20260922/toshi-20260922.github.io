# トップの「国保と任意継続の比較」の欄が、/kokuho/ のページと同じ額を出すかを照らす(2026-11-24 大阪府だけの計算をやめ、全国の市区町村を選べるようにした)
import asyncio, os, re, json
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INC = [0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 8000000, 10000000, 15000000]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        top = await b.new_page(); kok = await b.new_page()
        await top.goto('file://' + ROOT + '/site/index.html'); await kok.goto('file://' + ROOT + '/site/kokuho/index.html')
        RG = json.loads(re.search(r'var RG=(\[.*?\]);', open(ROOT + '/site/kokuho/index.html', encoding='utf-8').read(), re.S).group(1))
        nreg = await top.evaluate('document.getElementById("kreg").options.length')
        n0 = 1; bad0 = 0
        if nreg != len(RG): bad0 = 1; print('NG 市区町村の数', nreg, len(RG))
        n = bad = 0
        for r in range(nreg):
            pref = await kok.evaluate('(r)=>{var o=document.getElementById("reg");o.value=String(r);o.dispatchEvent(new Event("change",{bubbles:true}));return 0}', r)
            for old in (0, 1):
                for fam in (0, 1, 2, 3):
                    for a in INC:
                        t = await top.evaluate('''([r,old,fam,a])=>{var q=id=>document.getElementById(id);q("kreg").value=String(r);q("kf").value=String(fam);
                          document.querySelector('#kold button[data-v="'+old+'"]').click();q("ka").value=String(a);q("ka").dispatchEvent(new Event("input"));q("kreg").dispatchEvent(new Event("change"));
                          return [q("ko-k").textContent,q("ko-n").textContent]}''', [r, old, fam, a])
                        k = await kok.evaluate('''([r,old,fam,a])=>{var q=id=>document.getElementById(id);var R=q("reg");R.value=String(r);R.dispatchEvent(new Event("change",{bubbles:true}));
                          var x=[...document.querySelectorAll("#pref option")];return 0}''', [r, old, fam, a])
                        # /kokuho/ の任意継続は「会社の都道府県」の欄で選ぶので、市区町村の都道府県に合わせてから読む
                        k = await kok.evaluate('''([r,old,fam,a])=>{var q=id=>document.getElementById(id);var RGf=null;
                          var reg=q("reg");reg.value=String(r);reg.dispatchEvent(new Event("change",{bubbles:true}));
                          var f=FF;if(f!==null){q("pref").value=String(f);q("pref").dispatchEvent(new Event("change",{bubbles:true}));}
                          q("fam").value=String(fam);q("fam").dispatchEvent(new Event("change",{bubbles:true}));
                          var sb=document.querySelector('#s-age button[data-v="'+old+'"]')||document.querySelectorAll('.seg button')[old];if(sb)sb.click();
                          q("inc").value=String(a);q("inc").dispatchEvent(new Event("input",{bubbles:true}));
                          return [q("o-k").textContent,q("o-n").textContent]}'''.replace('FF', str(RG[r]['f'])), [r, old, fam, a])
                        n += 1
                        if [x.replace('円', '') for x in t] != [x.replace('円', '') for x in k]:
                            bad += 1
                            if bad < 6: print('NG', r, old, fam, a, t, k)
        print('照らした', n + n0, '合わない', bad + bad0)
        await b.close()
asyncio.run(main())
