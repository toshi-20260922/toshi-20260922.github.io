# /juminzei-keisan/ の突き合わせ。式は juminzei_keisan_ref.py(ページを見ずに書いた Python・整数と分数)。
import os, sys, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
from juminzei_keisan_ref import jumin, shaho, tsuki, kyuyo

def c(n): return '{:,}'.format(n)

async def body(pg):
    n = bad = 0
    def ck(lab, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp:
            bad += 1; print('合わない', lab, '画面', got, '計算', exp)
    # 1 社会保険料(2026年・東京都)を年収の幅で
    AS = list(range(0, 20000001, 50000)) + [1190000, 1190001, 1750000, 1750001, 1860000, 1860001, 2100000, 2215999, 2216000, 8500001, 9999999, 25000000, 30000000]
    for a in AS:
        for old in (0, 1):
            ck('社会保険料 %d %d' % (a, old), await pg.evaluate('([a,o])=>window.__jsh(a,o)', [a, old]), shaho(a, old))
    # 2 住民税:家族の組み合わせ × 年収(境目を含む)
    FAM = []
    for sp in (0, 1):
        for n0 in (0, 1, 2):
            for n1 in (0, 1):
                for n2 in (0, 1, 2):
                    for n3 in (0, 1):
                        FAM.append(dict(sp=sp, n0=n0, n1=n1, n2=n2, n3=n3))
    AS2 = [0, 1000000, 1190000, 1190001, 1500000, 1750000, 1750001, 1860000, 1860001, 2000000, 2100000, 2100001, 2500000, 3000000, 4000000, 5000000, 6000000, 8000000, 8500000, 8500001, 9000000, 10000000, 10950000, 11450000, 11950000, 12000000, 15000000, 20000000, 26000000, 26500000, 27000000, 30000000]
    for a in AS2:
        sh = shaho(a)
        for fm in FAM:
            o = dict(fm, ide=0, iry=0)
            got = await pg.evaluate('([a,s,o])=>window.__jk(a,s,o)', [a, sh, o])
            exp = jumin(a, sh, **fm)
            for k in ('g', 'kin', 'shi', 'ken', 'y', 'tr', 'kind', 'ded'):
                ck('住民税 %d %s %s' % (a, fm, k), got[k], exp[k])
    # 3 乱数で控除(iDeCo・医療費控除・社会保険料の入力)
    random.seed(20261123)
    for _ in range(600):
        a = random.randint(0, 3000) * 10000 + random.choice([0, 1, 999, 4000])
        fm = dict(sp=random.randint(0, 1), n0=random.randint(0, 3), n1=random.randint(0, 2), n2=random.randint(0, 2), n3=random.randint(0, 2))
        ide = random.choice([0, 144000, 276000, 816000]); iry = random.choice([0, 1, 50000, 123456])
        sh = random.choice([shaho(a), 0, random.randint(0, 2000000)])
        got = await pg.evaluate('([a,s,o])=>window.__jk(a,s,o)', [a, sh, dict(fm, ide=ide, iry=iry)])
        exp = jumin(a, sh, ide=ide, iry=iry, **fm)
        for k in ('y', 'shi', 'ken', 'tr'):
            ck('乱数 %d %s %d %d %d %s' % (a, fm, sh, ide, iry, k), got[k], exp[k])
    # 4 箱の操作(既定・年収・家族・自分で入力)
    async def setv(sel, v):
        await pg.fill(sel, str(v)); await pg.dispatch_event(sel, 'input')
    async def box():
        return [num(await pg.inner_text(s)) for s in ('#o-y', '#o-6', '#o-m')]
    y = jumin(5000000, shaho(5000000))['y']
    ck('既定の箱', await box(), [y, *tsuki(y)])
    ck('既定の見出し', await pg.inner_text('#o-vd'), '住民税は1年%s円です' % c(y))
    for a in [0, 1190000, 1190001, 3000000, 7777777, 12000000]:
        await setv('#inc', a); yy = jumin(a, shaho(a))['y']
        ck('箱 %d' % a, await box(), [yy, *tsuki(yy)])
    await setv('#inc', 9000000)
    await pg.click('#s-sp button[data-v="1"]'); await pg.select_option('#n0', '1'); await pg.select_option('#n2', '1')
    await setv('#ide', 276000); await setv('#iry', 80000)
    await pg.click('#s-age button[data-v="1"]')
    yy = jumin(9000000, shaho(9000000, 1), sp=1, n0=1, n2=1, ide=276000, iry=80000)['y']
    ck('箱 家族と控除', await box(), [yy, *tsuki(yy)])
    await pg.click('#s-sh button[data-v="1"]'); await setv('#sh', 1000000)
    yy = jumin(9000000, 1000000, sp=1, n0=1, n2=1, ide=276000, iry=80000)['y']
    ck('箱 社会保険料を入力', await box(), [yy, *tsuki(yy)])
    # 5 早見表の全セル
    rows = await pg.eval_on_selector_all(':is(#hayami ~ .tw):not(#hayami ~ .tw ~ .tw) tbody tr', 'rs=>rs.map(r=>[...r.cells].map(c=>c.textContent))')
    CASES = [{}, {'sp': 1}, {'sp': 1, 'n1': 1}, {'sp': 1, 'n2': 1}]
    ck('早見表の行の数', len(rows), 15)
    for r in rows:
        a = num(r[0]) * 10000
        ck('早見表 %d' % a, [num(x) for x in r[1:]], [jumin(a, shaho(a), **k)['y'] for k in CASES])
    rows = await pg.eval_on_selector_all(':is(#tsuki ~ .tw):not(#tsuki ~ .tw ~ .tw) tbody tr', 'rs=>rs.map(r=>[...r.cells].map(c=>c.textContent))')
    ck('毎月の表の行の数', len(rows), 8)
    for r in rows:
        a = num(r[0]) * 10000; yy = jumin(a, shaho(a))['y']
        ck('毎月の表 %d' % a, [num(x) for x in r[1:]], [yy, *tsuki(yy)])
    # 6 本文とよく聞かれることの数字
    txt = await pg.inner_text('main')
    def has(lab, s):
        ck(lab, s in txt, True)
    y5 = jumin(5000000, shaho(5000000))['y']
    has('冒頭', '年収500万円で単身なら住民税は1年%s円で、7月からは毎月%s円です。' % (c(y5), c(tsuki(y5)[1])))
    y3 = jumin(3000000, shaho(3000000))['y']; y3s = jumin(3000000, shaho(3000000), sp=1)['y']
    has('FAQ300', '令和9年度の住民税は1年%s円です。給料からは6月に%s円、7月から翌年5月まで毎月%s円が引かれます。配偶者控除を受ける配偶者がいると1年%s円です。' % (c(y3), c(tsuki(y3)[0]), c(tsuki(y3)[1]), c(y3s)))
    y8 = jumin(8000000, shaho(8000000))['y']; y8f = jumin(8000000, shaho(8000000), sp=1, n2=1)['y']
    has('FAQ800', '単身なら1年%s円です。配偶者控除を受ける配偶者と大学生の子が1人いると、1年%s円です。' % (c(y8), c(y8f)))
    # 計算のしかたの例
    d = jumin(5000000, shaho(5000000))
    rows = await pg.eval_on_selector_all(':is(#shikata ~ .tw):not(#shikata ~ .tw ~ .tw) tbody tr', 'rs=>rs.map(r=>[...r.cells].map(c=>c.textContent))')
    ck('例の表', [num(r[1]) for r in rows], [5000000, d['g'], shaho(5000000), 430000, d['tr'], d['sho'], 5000, d['y']])
    # 住民税がかからない人の表(合計所得と年収)
    rows = await pg.eval_on_selector_all(':is(#hikazei ~ .tw):not(#hikazei ~ .tw ~ .tw) tbody tr', 'rs=>rs.map(r=>[...r.cells].map(c=>c.textContent))')
    for i, r in enumerate(rows):
        lim = 350000 * (i + 1) + 100000 + (210000 if i else 0)
        ck('非課税 合計所得 %d' % i, num(r[1]) * 10000, lim)
        a = num(r[2]) if '9,999' in r[2] else num(r[2]) * 10000
        ck('非課税 年収 %d' % i, (kyuyo(a) <= lim, kyuyo(a + 1) > lim), (True, True))
    return n, bad

run('juminzei-keisan', body)
