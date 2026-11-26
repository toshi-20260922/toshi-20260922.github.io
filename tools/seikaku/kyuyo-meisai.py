# /kyuyo-meisai/ 給与明細の差引支給額。
# 原本:
#   国税庁「令和8年分 月額表の甲欄を適用する給与等に対する税額の電算機計算の特例」
#   https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/denshi_01.pdf
#   毎月の天引きは改正前の月額表。令和8年分の新しい基礎控除は12月の年末調整で精算する（年末調整のページと同じ式。2026-11-21 に第1〜4表と照合済み）。
#   全国健康保険協会 令和8年度都道府県料率（子ども・子育て支援金0.23%は料率に含めて折半。40〜64歳は介護1.62%も折半）
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#   厚生年金18.3%の半分。標準報酬月額は8.8万円以上65万円以下。
#   上限の65万円は、報酬月額63万5千円以上で適用する（63万4,999円は62万円）。
#   雇用保険 令和8年度 一般の本人5/1000・農林水産と清酒と建設は6/1000。50銭以下切り捨て・50銭超切り上げ。
#   https://www.mhlw.go.jp/content/001692566.pdf
# 通勤手当は、電車・バスは月15万円まで所得税の対象に入れない。超えた分だけ月給に足す。
# 標準報酬と雇用保険の賃金には通勤手当の全額を入れる。
# このファイルの式はページの JS を写していない。画面の数字と、下の整数の式を比べる。
# 配偶者なし＋扶養n人は以前の扶養n人、配偶者あり＋扶養n人は以前の扶養n+1人と同じ式（hg=配偶者+扶養）。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
import rates

GR = rates.tokyu_meisai()
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

# 電車・バスの通勤手当の非課税限度（月15万円）。超えた分だけ所得税の対象。
TSU_MAX = 150000

def slip(pay, tsukin=0, rate=rates.TOKYO, old=0, hg=0, ju=0, ei=rates.KOYO):
    base = max(0, pay) + max(0, tsukin)
    s = std(base)
    p = min(max(s, rates.NENKIN_MIN), rates.NENKIN_MAX)
    ken = r50d(s * (rate + rates.SIEN + (rates.KAIGO if old else 0)), 20000)
    nen = r50d(p * rates.NENKIN, 20000)
    koy = r50d(base * ei, 10000)
    sha = ken + nen + koy
    tsu_k = max(0, tsukin - TSU_MAX)
    zei = tax(pay + tsu_k - sha, hg)
    net = pay + tsukin - sha - zei - ju
    return dict(std=s, ken=ken, nen=nen, koy=koy, sha=sha, zei=zei, net=net,
                tsuH=tsukin - tsu_k, tsuK=tsu_k, sou=pay + tsukin, kojo=sha + zei + ju, pay=pay, ju=ju)

def yen_cell(t):
    return num(t) * 10000 if '万' in t else num(t)

async def read(pg):
    ids = ('o-net', 'o-sha', 'o-zei', 'o-std', 's-pay', 's-tsuh', 's-tsuk', 's-sou',
           's-ken', 's-nen', 's-koy', 's-zei', 's-ju', 's-kojo', 's-net')
    t = {}
    for i in ids:
        t[i] = num(await pg.inner_text('#' + i))
    return t

def same(got, exp):
    return (got['o-net'] == exp['net'] and got['s-net'] == exp['net']
            and got['o-sha'] == exp['sha'] and got['o-zei'] == exp['zei'] and got['s-zei'] == exp['zei']
            and got['o-std'] == exp['std'] and got['s-ken'] == exp['ken'] and got['s-nen'] == exp['nen']
            and got['s-koy'] == exp['koy'] and got['s-ju'] == exp['ju']
            and got['s-pay'] == exp['pay'] and got['s-tsuh'] == exp['tsuH'] and got['s-tsuk'] == exp['tsuK']
            and got['s-sou'] == exp['sou'] and got['s-kojo'] == exp['kojo'])

async def body(pg):
    n = bad = 0
    # 以前の「扶養n人」は配偶者なし＋扶養n人。配偶者あり＋扶養n人は以前の n+1人。
    cases = [
        dict(pay='300000', tsu='0', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO),
        dict(pay='250000', tsu='0', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO),
        dict(pay='200000', tsu='15000', ju='8000', pref='12', old='0', sp='0', fam='1', ei='0', rate=rates.TOKYO, oldn=0, hg=1, ein=rates.KOYO),
        dict(pay='300000', tsu='0', ju='0', pref='12', old='1', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=1, hg=0, ein=rates.KOYO),
        dict(pay='300000', tsu='0', ju='0', pref='26', old='0', sp='0', fam='2', ei='2', rate=rates.kenpo('大阪府'), oldn=0, hg=2, ein=rates.D['koyo']['rows'][1]['r8_worker'][0] * 10),
        dict(pay='88000', tsu='0', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO),
        dict(pay='500000', tsu='20000', ju='15000', pref='0', old='1', sp='0', fam='3', ei='1', rate=rates.kenpo('北海道'), oldn=1, hg=3, ein=rates.D['koyo']['rows'][2]['r8_worker'][0] * 10),
        dict(pay='1000000', tsu='0', ju='0', pref='12', old='0', sp='0', fam='7', ei='0', rate=rates.TOKYO, oldn=0, hg=7, ein=rates.KOYO),
        dict(pay='300000', tsu='0', ju='0', pref='12', old='0', sp='1', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=1, ein=rates.KOYO),
        dict(pay='300000', tsu='0', ju='0', pref='12', old='0', sp='1', fam='1', ei='0', rate=rates.TOKYO, oldn=0, hg=2, ein=rates.KOYO),
        dict(pay='300000', tsu='200000', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO, zei=7070),
        dict(pay='300000', tsu='150000', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO, zei=5600),
        dict(pay='300000', tsu='150001', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO, zei=5600),
        # 報酬月額63万5千円未満は標準報酬62万円。63万5千円以上で厚生年金の上限（標準報酬65万円・59,475円）。
        dict(pay='634999', tsu='0', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO, nen=56730, std=620000),
        dict(pay='635000', tsu='0', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO, nen=59475, std=650000),
        dict(pay='700000', tsu='0', ju='0', pref='12', old='0', sp='0', fam='0', ei='0', rate=rates.TOKYO, oldn=0, hg=0, ein=rates.KOYO, nen=59475, std=710000),
    ]
    for c in cases:
        await pg.fill('#pay', c['pay'])
        await pg.fill('#tsukin', c['tsu'])
        await pg.fill('#ju', c['ju'])
        await pg.select_option('#pref', c['pref'])
        await pg.select_option('#fam', c['fam'])
        await pg.click('#s-sp button[data-v="%s"]' % c['sp'])
        await pg.click('#s-old button[data-v="%s"]' % c['old'])
        await pg.click('#s-ei button[data-v="%s"]' % c['ei'])
        got = await read(pg)
        exp = slip(int(c['pay']), int(c['tsu']), c['rate'], c['oldn'], c['hg'], int(c['ju']), c['ein'])
        n += 15
        if c.get('zei') is not None and exp['zei'] != c['zei']:
            bad += 1
            print('NG 期待する所得税', c['pay'], c['tsu'], exp['zei'], c['zei'])
        if c.get('nen') is not None and exp['nen'] != c['nen']:
            bad += 1
            print('NG 厚生年金の境', c['pay'], exp['nen'], c['nen'])
        if c.get('std') is not None and exp['std'] != c['std']:
            bad += 1
            print('NG 標準報酬の境', c['pay'], exp['std'], c['std'])
        if not same(got, exp):
            bad += 1
            print('NG', c['pay'], c['tsu'], 'sp', c['sp'], 'fam', c['fam'], got, exp)
    pays = list(range(150000, 1000001, 50000))
    for tid, old in (('tb0', 0), ('tb1', 1)):
        rows = await pg.evaluate("id=>[...document.querySelectorAll('#'+id+' tbody tr')].map(r=>[...r.cells].map(c=>c.innerText))", tid)
        n += 1
        if len(rows) != 18:
            bad += 1
            print('NG 行数', tid, len(rows))
            continue
        for row, pay in zip(rows, pays):
            exp = slip(pay, old=old)
            got = [yen_cell(x) for x in row]
            n += 4
            if got != [pay, exp['sha'], exp['zei'], exp['net']]:
                bad += 1
                print('NG 表', tid, pay, got, exp['sha'], exp['zei'], exp['net'])
    return n, bad

if __name__ == '__main__':
    run('kyuyo-meisai', body)
