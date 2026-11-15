import asyncio,glob,os
from playwright.async_api import async_playwright
SITE='/home/claude/toshi-20260922.github.io/site/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();bad=0;n=0
        pages=sorted(glob.glob(SITE+'*/index.html'))+[SITE+'index.html']
        for w in (360,1280):
            for f in pages:
                pg=await b.new_page(viewport={'width':w,'height':800});errs=[]
                pg.on('pageerror',lambda e:errs.append(str(e)))
                await pg.goto('file://'+f);ov=await pg.evaluate('document.documentElement.scrollWidth-window.innerWidth');n+=1
                nan=await pg.evaluate('/NaN|undefined/.test(document.querySelector("main")?document.querySelector("main").innerText:"")')
                if errs or ov>0 or nan: bad+=1;print(w,f.replace(SITE,''),ov,errs,nan)
                await pg.close()
        print('開いた数',n,'問題',bad);await b.close()
asyncio.run(main())
