# /kyuyo-meisai/ 給与明細の差引支給額。
# 原本:
#   国税庁「令和8年分 月額表の甲欄を適用する給与等に対する税額の電算機計算の特例」
#   https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/denshi_01.pdf
#   毎月の天引きは改正前の月額表。令和8年分の新しい基礎控除は12月の年末調整で精算する（年末調整のページと同じ式。2026-11-21 に第1〜4表と照合済み）。
#   全国健康保険協会 令和8年度都道府県料率（子ども・子育て支援金0.23%は料率に含めて折半。40〜64歳は介護1.62%も折半）
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#   厚生年金18.3%の半分。標準報酬月額は8.8万円以上65万円以下。
#   雇用保険 令和8年度 一般の本人5/1000・農林水産と清酒と建設は6/1000。50銭以下切り捨て・50銭超切り上げ。
#   https://www.mhlw.go.jp/content/001692566.pdf
# 通勤手当は所得税の対象に入れず、標準報酬と雇用保険の賃金には入れる。
# このファイルの式はページの JS を写していない。画面の数字と、下の整数の式を比べる。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

GR = [(58,63),(68,73),(78,83),(88,93),(98,101),(104,107),(110,114),(118,122),(126,130),(134,138),(142,146),(150,155),(160,165),(170,175),(180,185),(190,195),(200,210),(220,230),(240,250),(260,270),(280,290),(300,310),(320,330),(340,350),(360,370),(380,395),(410,425),(440,455),(470,485),(500,515),(530,545),(560,575),(590,605),(620,635),(650,665),(680,695),(710,730),(750,770),(790,810),(830,855),(880,905),(930,955),(980,1005),(1030,1055),(1090,1115),(1150,1175),(1210,1235),(1270,1295),(1330,1355),(1390,10**9)]
U = 120000
TAX = [(162500,5105,0),(275000,10210,8296),(579166,20420,36374),(750000,23483,54113),(1500000,33693,130688),(3333333,40840,237893),(0,45945,408061)]

def r50d(n, d):
    q, r = divmod(int(n), int(d))
    return q + (1 if r * 2 > d else 0)

def std(m):
    for s, hi in GR:
        if m < hi * 1000:
            return s * 1000
    return 1390000

def cl(n, d):
    r = n % d
    return (n - r) // d + (1 if r else 0)

def tax(monthly_after, hg):
    a = max(0, monthly_after) * 12 * 10000
    if a <= 158333 * U:
        ky = 54167
    elif a <= 299999 * U:
        ky = cl(a * 3 + 66670 * U, 10 * U)
    elif a <= 549999 * U:
        ky = cl(a * 2 + 366670 * U, 10 * U)
    elif a <= 708330 * U:
        ky = cl(a + 916670 * U, 10 * U)
    else:
        ky = 162500
    ki = 48334 if a <= 2120833 * U else 40000 if a <= 2162499 * U else 26667 if a <= 2204166 * U else 13334 if a <= 2245833 * U else 0
    b = max(a - (ky + ki + 31667 * hg) * U, 0)
    r = TAX[6]
    for i in range(6):
        if b <= TAX[i][0] * U:
            r = TAX[i]
            break
    dn = U * 100000
    n = b * r[1] - r[2] * dn
    if n < 0:
        n = 0
    return ((2 * n + 10 * dn) // (20 * dn)) * 10

def slip(pay, tsukin=0, rate=985, old=0, hg=0, ju=0, ei=50):
    base = max(0, pay) + max(0, tsukin)
    s = std(base)
    p = min(max(s, 88000), 650000)
    ken = r50d(s * (rate + 23 + (162 if old else 0)), 20000)
    nen = r50d(p * 1830, 20000)
    koy = r50d(base * ei, 10000)
    sha = ken + nen + koy
    zei = tax(max(0, pay) - sha, hg)
    net = pay + tsukin - sha - zei - ju
    return dict(std=s, ken=ken, nen=nen, koy=koy, sha=sha, zei=zei, net=net)

async def read(pg):
    ids = ('o-net', 'o-ken', 'o-nen', 'o-ei', 'o-zei', 'o-ju', 'o-std', 'o-sha')
    t = {}
    for i in ids:
        t[i] = num(await pg.inner_text('#' + i))
    return t

def same(got, exp):
    return (got['o-net'] == exp['net'] and got['o-ken'] == exp['ken'] and got['o-nen'] == exp['nen']
            and got['o-ei'] == exp['koy'] and got['o-zei'] == exp['zei'] and got['o-std'] == exp['std']
            and got['o-sha'] == exp['sha'])

async def body(pg):
    n = bad = 0
    cases = [
        dict(pay='300000', tsu='0', ju='0', pref='12', old='0', fuyo='0', ei='0', rate=985, oldn=0, hg=0, ein=50),
        dict(pay='250000', tsu='0', ju='0', pref='12', old='0', fuyo='0', ei='0', rate=985, oldn=0, hg=0, ein=50),
        dict(pay='200000', tsu='15000', ju='8000', pref='12', old='0', fuyo='1', ei='0', rate=985, oldn=0, hg=1, ein=50),
        dict(pay='300000', tsu='0', ju='0', pref='12', old='1', fuyo='0', ei='0', rate=985, oldn=1, hg=0, ein=50),
        dict(pay='300000', tsu='0', ju='0', pref='26', old='0', fuyo='2', ei='2', rate=1013, oldn=0, hg=2, ein=60),
        dict(pay='88000', tsu='0', ju='0', pref='12', old='0', fuyo='0', ei='0', rate=985, oldn=0, hg=0, ein=50),
        dict(pay='500000', tsu='20000', ju='15000', pref='0', old='1', fuyo='3', ei='1', rate=1028, oldn=1, hg=3, ein=60),
        dict(pay='1000000', tsu='0', ju='0', pref='12', old='0', fuyo='7', ei='0', rate=985, oldn=0, hg=7, ein=50),
    ]
    for c in cases:
        await pg.fill('#pay', c['pay'])
        await pg.fill('#tsukin', c['tsu'])
        await pg.fill('#ju', c['ju'])
        await pg.select_option('#pref', c['pref'])
        await pg.select_option('#fuyo', c['fuyo'])
        await pg.click('#s-old button[data-v="%s"]' % c['old'])
        await pg.click('#s-ei button[data-v="%s"]' % c['ei'])
        got = await read(pg)
        exp = slip(int(c['pay']), int(c['tsu']), c['rate'], c['oldn'], c['hg'], int(c['ju']), c['ein'])
        n += 7
        if not same(got, exp) or got['o-ju'] != int(c['ju']):
            bad += 1
            print('NG', c['pay'], got, exp)
    pays = [200000, 250000, 300000, 350000, 400000, 500000]
    for tid, old in (('tb0', 0), ('tb1', 1)):
        rows = await pg.evaluate("id=>[...document.querySelectorAll('#'+id+' tbody tr')].map(r=>[...r.cells].map(c=>c.innerText))", tid)
        n += 1
        if len(rows) != 6:
            bad += 1
            print('NG 行数', tid, len(rows))
            continue
        for row, pay in zip(rows, pays):
            exp = slip(pay, old=old)
            got = [num(x) for x in row]
            n += 5
            if got != [pay, exp['std'], exp['sha'], exp['zei'], exp['net']]:
                bad += 1
                print('NG 表', tid, pay, got, exp)
    return n, bad

if __name__ == '__main__':
    run('kyuyo-meisai', body)
