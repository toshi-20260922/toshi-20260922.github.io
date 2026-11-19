# 毎日の全ツール点検で使う共通の部品。
# 1ページにつき1つ tools/seikaku/<ページの住所>.py を置く(最低賃金の県ページは saitei.py の1つで全県を見る)。
# 決まり:ページの JS を見ずに書いた自分の計算(Python・整数か分数)と、画面の結果を同じ入力で比べる。
# 最後に done(照らした件数, 合わない件数) を呼ぶ。合わない件数が1以上なら終了コード1。
import os, sys, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, 'site')

def url(slug):
    return 'file://' + os.path.join(SITE, slug, 'index.html')

def num(t):
    s = ''.join(ch for ch in t if ch.isdigit())
    v = int(s or 0)
    return -v if ('−' in t or t.strip().startswith('-')) else v

def done(n, bad):
    print('照らした %d 合わない %d' % (n, bad))
    sys.exit(1 if bad else 0)

def run(slug, body, width=390):
    """body(pg) は (照らした件数, 合わない件数) を返す async 関数。"""
    async def main():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page(viewport={'width': width, 'height': 800})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(url(slug))
            n, bad = await body(pg)
            await b.close()
            for e in errs:
                print('画面のエラー', e[:120]); bad += 1
            return n, bad
    n, bad = asyncio.run(main())
    done(n, bad)
