# 2026-11-23 10時の回:5ページ(shakaihoken・koyohoken・zoyozei・yakuin-tedori・yatou-hiyou)を
# ページの JS を写さずに書いた計算(整数と分数)で、代表3例と境目の前後を画面の結果と比べる。
import os, sys, asyncio
from fractions import Fraction as F
from playwright.async_api import async_playwright
import rates
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def url(s): return 'file://' + os.path.join(ROOT, 'site', s, 'index.html')
def num(t):
    s = ''.join(c for c in t if c.isdigit()); v = int(s or 0)
    return -v if ('−' in t or t.strip().startswith('-')) else v

# 協会けんぽ 令和8年度(1/100%):東京9.85 大阪10.13 新潟9.21 佐賀10.55
RATE = rates.kenpo_picked()
SHIEN, KAIGO, NENKIN, KYO = rates.SIEN, rates.KAIGO, rates.NENKIN, rates.KYOSHUTSU
BOUND = rates.upper_sen()
STD = rates.std_sen()
def std(m):
    for b, s in zip(BOUND, STD):
        if m < b * 1000: return s * 1000
    return 1390000
def pen(s): return min(max(s, rates.NENKIN_MIN), rates.NENKIN_MAX)
def hb(x):  # 本人負担:50銭以下切り捨て・超は切り上げ(x は分数)
    q = x.numerator // x.denominator; r = x - q
    return q + 1 if r > F(1, 2) else q
def sh(s, r, old):
    hr = F(r + SHIEN + (KAIGO if old else 0), 10000)
    ken = hb(s * hr / 2); nen = hb(pen(s) * F(NENKIN, 10000) / 2)
    kyo = int(pen(s) * F(KYO, 10000))
    co = int(s * hr) - ken + int(pen(s) * F(NENKIN, 10000)) - nen + kyo
    return ken, nen, kyo, co

def kyuyo(x):
    return rates.kyuyo_r8(x)
def kiso(g):
    return rates.kiso_shotoku(g)
def itax(t):
    for lim, r, d in [(1950000,5,0),(3300000,10,97500),(6950000,20,427500),(9000000,23,636000),(18000000,33,1536000),(40000000,40,2796000),(10**15,45,4796000)]:
        if t <= lim: b = t * r // 100 - d; break
    return int(b * F(rates.FUKKO_NUM, rates.FUKKO_DEN)) // 100 * 100
def jumin(g, s):
    if g <= 450000: return 0
    jk = rates.kiso_jumin(g)
    t = max(0, g - s - jk) // 1000 * 1000
    adj = 0 if g > 25000000 else min(50000, t) if t <= 2000000 else 50000
    shi = max(0, t * 6 // 100 - adj * 3 // 100) // 100 * 100
    ken = max(0, t * 4 // 100 - adj * 2 // 100) // 100 * 100
    return shi + ken + 5000

def zoyo(g, ippan):
    k = max(0, g - 1100000) // 1000 * 1000
    T = [(2000000,10,0),(3000000,15,100000),(4000000,20,250000),(6000000,30,650000),(10000000,40,1250000),(15000000,45,1750000),(30000000,50,2500000),(10**18,55,4000000)] if ippan else \
        [(2000000,10,0),(4000000,15,100000),(6000000,20,300000),(10000000,30,900000),(15000000,40,1900000),(30000000,45,2650000),(45000000,50,4150000),(10**18,55,6400000)]
    for lim, r, d in T:
        if k <= lim: return max(0, k * r // 100 - d) // 100 * 100

def koyo_me(w, r):  # r は1,000分の(10倍)
    x = F(w * r, 10000); q = int(x)
    return q + 1 if x - q > F(1, 2) else q

async def main():
    n = bad = 0
    def ck(lab, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp:
            bad += 1; print('合わない', lab, '画面', got, '計算', exp)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 390, 'height': 800})
        # shakaihoken:4都道府県 × 50等級 × 本人2列・会社2列・健保・年金・拠出金
        await pg.goto(url('shakaihoken'))
        for pi, r in RATE.items():
            await pg.select_option('#pref', str(pi))
            rows = await pg.eval_on_selector_all('#gtb tr', 'rs=>rs.map(r=>[...r.cells].map(c=>c.textContent))')
            for i, row in enumerate(rows):
                s = STD[i] * 1000
                k0, n0, ky, c0 = sh(s, r, 0); k1, n1, _, c1 = sh(s, r, 1)
                exp = [s, k0, n0, k0 + n0, k1 + n1, c0, c1, ky]
                got = [num(x) for x in row[2:10]]
                ck('shakaihoken %d 等級%d' % (pi, i + 1), got, exp)
        # 境目の前後(月給で入力)
        await pg.select_option('#pref', '12')
        for m in [292999, 293000, 309999, 310000, 634999, 635000, 1355000, 0]:
            await pg.fill('#pay', str(m)); await pg.dispatch_event('#pay', 'input')
            k, nn, ky, c = sh(std(m), rates.TOKYO, 0)
            ck('shakaihoken 月給%d 本人' % m, num(await pg.inner_text('#o-me')), k + nn)
            ck('shakaihoken 月給%d 会社' % m, num(await pg.inner_text('#o-co')), c)
        # koyohoken
        await pg.goto(url('koyohoken'))
        for t, (rme, rco) in enumerate([(50, 85), (60, 95), (60, 105)]):
            await pg.click('.seg button[data-t="%d"]' % t)
            for w in [0, 1, 100, 101, 300000, 300100, 300101, 333333, 199999, 250000, 1234567]:
                await pg.fill('#pay', str(w)); await pg.dispatch_event('#pay', 'input')
                ck('koyohoken %d %d 本人' % (t, w), num(await pg.inner_text('#o-me')), koyo_me(w, rme))
                ck('koyohoken %d %d 会社' % (t, w), num(await pg.inner_text('#o-co')), w * rco // 10000)
        # zoyozei
        await pg.goto(url('zoyozei'))
        for kind in [0, 1]:
            await pg.click('#s-kind button[data-v="%d"]' % kind)
            for g in [0, 1100000, 1100999, 1101000, 2000000, 3100000, 4100000, 4101000, 5000000, 7100000, 11100000, 31100000, 46100000, 100000000]:
                await pg.fill('#amt', str(g)); await pg.dispatch_event('#amt', 'input')
                t = zoyo(g, kind)
                ck('zoyozei %d %d 税' % (kind, g), num(await pg.inner_text('#o-t')), t)
                ck('zoyozei %d %d 手元' % (kind, g), num(await pg.inner_text('#o-n')), g - t)
                need = (await pg.inner_text('#o-vd')).strip()
                ck('zoyozei %d %d 申告' % (kind, g), need, '贈与税の申告が必要です' if t > 0 else '贈与税の申告は不要です')
        # 本文の例(390万円×15%−10万円=48万5千円・兄から弟53万円)
        ck('zoyozei 本文 特例', zoyo(5000000, 0), 485000); ck('zoyozei 本文 一般', zoyo(5000000, 1), 530000)
        # yakuin-tedori:東京・大阪 × 2つの年齢 × 月額
        await pg.goto(url('yakuin-tedori'))
        for pi in [12, 26]:
            await pg.select_option('#pref', str(pi))
            for old in [0, 1]:
                await pg.click('.seg button[data-v="%d"]' % old)
                for mon in [300000, 500000, 1000000, 634999, 635000, 400000, 410000, 2000000]:
                    await pg.fill('#inc', str(mon)); await pg.dispatch_event('#inc', 'input')
                    a = mon * 12; s = std(mon)
                    k, nn, ky, c = sh(s, RATE[pi], old)
                    shy = (k + nn) * 12; g = kyuyo(a)
                    it = itax(max(0, g - shy - kiso(g)) // 1000 * 1000)
                    j = jumin(g, shy); t = a - shy - it - j
                    ck('yakuin-tedori %d %d %d 年手取り' % (pi, old, mon), num(await pg.inner_text('#o-y')), t)
                    ck('yakuin-tedori %d %d %d 会社' % (pi, old, mon), num(await pg.inner_text('#o-c')), a + c * 12)
        # 既定の文の例:東京・40歳未満 30万円→月あたり240,963円
        a = 3600000; k, nn, _, _ = sh(300000, rates.TOKYO, 0); shy = (k + nn) * 12; g = kyuyo(a)
        t = a - shy - itax(max(0, g - shy - kiso(g)) // 1000 * 1000) - jumin(g, shy)
        ck('yakuin-tedori FAQ 30万', round(F(t, 12)), 240963)
        # yatou-hiyou:会社の負担(月)
        await pg.goto(url('yatou-hiyou'))
        for pi in [12, 26]:
            await pg.select_option('#pref', str(pi))
            for old in [0, 1]:
                await pg.click('#s-age button[data-v="%d"]' % old)
                for m in [180000, 300000, 500000, 700000]:
                    await pg.fill('#pay', str(m)); await pg.dispatch_event('#pay', 'input')
                    k, nn, ky, c = sh(std(m), RATE[pi], old)
                    koy = int(F(m * 85, 10000) + F(1, 2)); rou = int(F(m * 30, 10000) + F(1, 2))
                    ck('yatou-hiyou %d %d %d 月' % (pi, old, m), num(await pg.inner_text('#o-a')), c + koy + rou)
                    ck('yatou-hiyou %d %d %d 年' % (pi, old, m), num(await pg.inner_text('#o-c')), (c + koy + rou + m) * 12)
        await b.close()
    print('照らした %d 合わない %d' % (n, bad)); sys.exit(1 if bad else 0)
asyncio.run(main())
