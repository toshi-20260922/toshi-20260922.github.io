# 2026-11-20 に足した最低賃金の5県(三重・静岡・宮城・新潟・長野)の突き合わせ。
# 原本:各労働局の発表(三重 002796736.pdf・静岡 newpage_00059・宮城 002764301.pdf と 002871763.pdf・新潟 R080828_2・長野 houdou8-32.pdf)。
# 自分の表(下の EXP)とページの判定を、時給・日給・月給のちょうどと1円下・発効日の前後で比べる。
import os, sys, asyncio, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import url, done
from playwright.async_api import async_playwright
# 県: (新しい額, 前の額, 発効日, 業種[(名前の一部, 12/15より前の額, 新しい額, 新しい額の発効日)])
EXP = {'mie': (1143, 1087, '2026-10-01', []), 'shizuoka': (1154, 1097, '2026-10-15', []),
       'miyagi': (1098, 1038, '2026-10-01', [('鉄鋼', 1125, 1187, '2026-12-15'), ('電子部品', 1077, 1138, '2026-12-15'), ('自動車小売', 1101, 1161, '2026-12-15')]),
       'niigata': (1108, 1050, '2026-10-01', []), 'nagano': (1117, 1061, '2026-10-02', [])}
DAYS = ['2026-09-30', '2026-10-14', '2026-11-20', '2026-12-14', '2026-12-15', '2027-01-10']
async def main():
    n = bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for slug, (m, o, eff, ind) in EXP.items():
            for day in DAYS:
                ctx = await b.new_context()
                await ctx.add_init_script("(()=>{const T=new Date('%sT12:00:00+09:00').getTime();const D=Date;class X extends D{constructor(...a){super(...(a.length?a:[T]))}static now(){return T}};window.Date=X;})()" % day)
                pg = await ctx.new_page(); await pg.goto(url('saitei-chingin-' + slug))
                reg = o if day < eff else m
                cases = [(0, None, reg)]
                for name, cur, new, d2 in ind:
                    lim = max(reg, new if day >= d2 else cur)
                    cases.append((name, None, lim))
                for nm, _, lim in cases:
                    if nm:
                        idx = await pg.evaluate("n=>[...document.querySelectorAll('#ind option')].findIndex(o=>o.text.includes(n))", nm)
                        await pg.select_option('#ind', str(idx))
                    # 時給
                    for pay, want in ((lim, '満たしています'), (lim - 1, '下回っています')):
                        await pg.fill('#pay', str(pay)); v = await pg.inner_text('#o-vd'); mm = await pg.inner_text('#o-m'); n += 2
                        if v != want or int(''.join(c for c in mm if c.isdigit())) != lim:
                            bad += 1; print('NG 時給', slug, day, nm, pay, v, mm)
                    # 月給(年間休日120日・8時間):最低の月給は lim×(245×8÷12) の円未満切り上げ
                    await pg.click('.seg button[data-k="2"]')
                    need = math.ceil(F(lim) * F(245 * 8, 12))
                    for pay, want in ((need, '満たしています'), (need - 1, '下回っています')):
                        await pg.fill('#pay', str(pay)); v = await pg.inner_text('#o-vd'); n += 1
                        if v != want: bad += 1; print('NG 月給', slug, day, nm, pay, v)
                    await pg.click('.seg button[data-k="0"]')
                # 本文の数字
                t = await pg.inner_text('main') if await pg.query_selector('main') else await pg.inner_text('body')
                for s in ('%s円' % format(m, ','), '%s円' % format(o, ',')):
                    n += 1
                    if s not in t: bad += 1; print('NG 本文に無い', slug, s)
                await ctx.close()
        await b.close()
    done(n, bad)
asyncio.run(main())
