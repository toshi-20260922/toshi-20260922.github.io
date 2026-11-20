# /kani-kazei/ 簡易課税の事業区分と納める消費税。
# 原本:国税庁 No.6505(75%の特例・区分していない場合)・No.6509(事業区分とみなし仕入率)・No.6371(端数計算)・No.6303(税率)、
#      「消費税のあらまし」010.pdf(計算例)・申告書（簡易課税用）の書き方 202411_02.pdf(百円未満切捨て・22/78)。最後に確かめた日:2026-11-20
# ページの JS を見ずに書いた計算:控除できる額を、使える計算(原則・1業種75%・2業種75%)を全部並べて一番大きいものにする。
import os, sys, random, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
RT = [90, 80, 70, 60, 50, 40]
def mine(s):
    S = sum(s); T = (S - S % 1000) * 78 // 1000
    nz = [i for i in range(6) if s[i]]
    opts = [sum(s[i] * RT[i] for i in range(6)) * T // (100 * S)]          # 原則
    if len(nz) > 1:
        opts += [T * RT[i] // 100 for i in nz if s[i] * 100 >= 75 * S]     # 1業種で75%以上
    if len(nz) > 2:
        for x in nz:
            for y in nz:
                if RT[x] > RT[y] and (s[x] + s[y]) * 100 >= 75 * S:
                    opts.append((s[x] * RT[x] + (S - s[x]) * RT[y]) * T // (100 * S))
    d = max(opts); k = (T - d) // 100 * 100; ch = (k * 22 // 78) // 100 * 100
    return k + ch, T
CASES = [[0,0,0,0,9000000,0], [8000000,2000000,0,0,0,0], [4500000,3500000,0,0,2000000,0], [0,7000000,3000000,0,0,0],
         [0,0,0,7500000,2500000,0], [0,0,0,7499999,2500001,0], [0,0,0,0,0,999], [0,0,0,0,0,1000], [0,0,0,0,0,50000000],
         [3000000,4500000,0,0,2500000,0], [3000000,4499999,0,0,2500001,0], [1,1,1,1,1,1]]
random.seed(20261120)
for _ in range(400):
    CASES.append([random.choice([0, 0, random.choice([random.randint(1, 30000000), random.randint(1, 900000000)])]) for _ in range(6)])
async def body(pg):
    n = bad = 0
    for s in CASES:
        if sum(s) == 0: continue
        for i in range(6): await pg.fill('#s%d' % i, str(s[i]))
        tot, T = mine(s)
        got = num(await pg.inner_text('#o-t')); gk = num(await pg.inner_text('#o-k')); n += 2
        if got != tot or gk != T: bad += 1; print('NG', s, got, tot, gk, T)
    # 業種を選ぶと、表と同じ区分が出るか
    html = await pg.content()
    rows = dict(re.findall(r'<tr><td class="l">([^<]+)</td><td>(第\d種)</td>', html))
    opts = await pg.evaluate("[...document.querySelectorAll('#ex option')].map(o=>[o.value,o.text])")
    for v, t in opts:
        await pg.select_option('#ex', v); vd = await pg.inner_text('#o-vd'); n += 1
        if t not in rows or not vd.startswith(rows[t]): bad += 1; print('NG 区分', t, vd, rows.get(t))
    # 本文の手書きの数字(第5種900万円の例)
    for x in ('702,000円', '351,000円', '99,000円', '450,000円'):
        n += 1
        if x not in html: bad += 1; print('NG 本文', x)
    return n, bad
run('kani-kazei', body)
