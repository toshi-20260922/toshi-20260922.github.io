import sys,asyncio
from playwright.async_api import async_playwright
SITE='/home/claude/toshi-20260922.github.io/site/'
def num(t): return int(''.join(ch for ch in t if ch.isdigit()) or 0)
async def main(page,checks):
    async with async_playwright() as p:
        b=await p.chromium.launch();errs=[]
        for w in (360,1280):
            pg=await b.new_page(viewport={'width':w,'height':800})
            pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('file://'+SITE+page+'/index.html')
            print(w,'はみ出し',await pg.evaluate('document.documentElement.scrollWidth-window.innerWidth'))
            await checks(pg,w)
            await pg.screenshot(path=f'{page}_{w}.png',full_page=True)
            await pg.close()
        print('エラー',errs);await b.close()
async def kojin(pg,w):
    print(' 既定 500万 手取り',await pg.inner_text('#o-n'),'表の500万行',await pg.evaluate('[...document.querySelectorAll("tr.x7hl")].map(r=>r.children[7].textContent).join(" / ")'),await pg.inner_text('#o-reg'),await pg.inner_text('#t-cap'))
    await pg.select_option('#reg','15');print(' 大阪を選ぶ',await pg.inner_text('#o-n'),'(直す前 3,615,257)',await pg.inner_text('#o-sh'))
    await pg.evaluate('document.querySelectorAll("#s-age button")[1].click()');print(' 大阪 40〜59歳',await pg.inner_text('#o-n'),'(直す前 3,518,855)')
    await pg.select_option('#reg','0');print(' 東京 40〜59歳',await pg.inner_text('#o-n'),'表',await pg.evaluate('document.querySelectorAll("tr.x7hl")[1].children[7].textContent'))
    await pg.select_option('#reg','x');print(' 料率欄',await pg.is_visible('#cust'),await pg.inner_text('#o-n'),await pg.inner_text('#o-reg'))
    await pg.fill('#c00','9.5');print(' 医療分の所得割を9.5%に',await pg.inner_text('#o-n'))
if __name__=='__main__':
    asyncio.run(main('kojin-zei',kojin))
