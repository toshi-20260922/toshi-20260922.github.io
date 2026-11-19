# /shotokuzei/ 所得税の計算(年収から1年間の所得税と税率を出す・速算表・課税される所得ごとの表・年収別の表)。
# 原本:
#  国税庁 No.2260 所得税の税率 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
#   (11/19 は開けなかった。速算表・2.1%・1,000円未満と100円未満の切り捨ては、下の「暮らしの税情報」で確かめた)
#  国税庁「暮らしの税情報 給与所得者と税」(令和8年分の速算表・給与所得控除後の金額の表・端数処理)
#   https://www.nta.go.jp/publication/pamph/koho/kurashi/html/02_1.htm
#  国税庁 No.1199 基礎控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#  国税庁「令和8年度税制改正による基礎控除の引上げ等」(令和8・9年分の基礎控除の加算42万円・5万円、給与所得の特例の表)
#   https://www.nta.go.jp/publication/pamph/gensen/2026kaisei.pdf
#  財務省「令和8年度の税制改正」(合計所得489万円以下の上乗せ42万円・課税最低限178万円)
#   https://www.mof.go.jp/tax_policy/publication/brochure/zeisei2026_pdf/zeisei26_all.pdf
#  国税庁「防衛特別所得税・復興特別所得税 Q&A」(令和9年から1%+1.1%で合計2.1%のまま)
#   https://www.nta.go.jp/publication/pamph/pdf/0026005-024_03.pdf
#  協会けんぽ 令和8年3月分からの保険料額表(東京都 9.85%・介護1.62%・支援金0.23%・厚生年金18.3%・等級・50銭以下切り捨て)
#   https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#  厚生労働省 令和8年度の雇用保険料率(一般の事業 労働者負担 5/1,000)
#   https://www.mhlw.go.jp/content/001692566.pdf
# 最後に原本を確かめた日:2026-11-19
import os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

# 速算表(課税される所得は1,000円単位。下限・率・控除額)
SOKUSAN = [(1000, 5, 0), (1950000, 10, 97500), (3300000, 20, 427500), (6950000, 23, 636000),
           (9000000, 33, 1536000), (18000000, 40, 2796000), (40000000, 45, 4796000)]

def kyuyo(x):
    """令和8年分の給与所得(給与所得控除後の給与等の金額の表)。"""
    if x <= 740999: return 0
    if x <= 2190999: return x - 740000
    if x <= 2192999: return 1451000
    if x <= 2195999: return 1453000
    if x <= 2199999: return 1456000
    if x <= 3599999: return (x // 4 // 1000 * 1000) * 28 // 10 - 80000
    if x <= 6599999: return (x // 4 // 1000 * 1000) * 32 // 10 - 440000
    if x <= 8499999: return x * 9 // 10 - 1100000
    return x - 1950000

def kiso(gokei):
    """令和8年分の基礎控除(合計所得金額ごと)。"""
    if gokei <= 4890000: return 1040000      # 62万円+加算42万円
    if gokei <= 6550000: return 670000       # 62万円+加算5万円
    if gokei <= 23500000: return 620000
    if gokei <= 24000000: return 480000
    if gokei <= 24500000: return 320000
    if gokei <= 25000000: return 160000
    return 0

# 標準報酬月額の等級(健康保険 1〜50級。報酬月額の上の区切り・千円)
TOKYU = [(58, 63), (68, 73), (78, 83), (88, 93), (98, 101), (104, 107), (110, 114), (118, 122), (126, 130),
         (134, 138), (142, 146), (150, 155), (160, 165), (170, 175), (180, 185), (190, 195), (200, 210),
         (220, 230), (240, 250), (260, 270), (280, 290), (300, 310), (320, 330), (340, 350), (360, 370),
         (380, 395), (410, 425), (440, 455), (470, 485), (500, 515), (530, 545), (560, 575), (590, 605),
         (620, 635), (650, 665), (680, 695), (710, 730), (750, 770), (790, 810), (830, 855), (880, 905),
         (930, 955), (980, 1005), (1030, 1055), (1090, 1115), (1150, 1175), (1210, 1235), (1270, 1295),
         (1330, 1355)]

def hyojun(m):
    for s, top in TOKYU:
        if m < top * 1000: return s * 1000
    return 1390000

def gojussen(v):
    """本人の負担分の端数:50銭以下は切り捨て・50銭を超えると1円に切り上げ。"""
    f = v.numerator // v.denominator
    return f + 1 if v - f > F(1, 2) else f

def shaho(a, kaigo):
    """賞与なし。月の給料は年収÷12(1円未満切り捨て)。いまの料率で12か月分。"""
    m = a // 12
    s = hyojun(m)
    nen = min(max(s, 88000), 650000)
    kenpo = F(985 + 23 + (162 if kaigo else 0), 10000) / 2     # 健康保険+支援金(+介護)の半分
    return (gojussen(s * kenpo) + gojussen(nen * F(183, 1000) / 2) + gojussen(m * F(5, 1000))) * 12

def ritsu(t):
    r = None
    for lo, p, d in SOKUSAN:
        if t >= lo: r = (p, d)
    return r

def zei_kazei(t):
    """課税される所得(1,000円単位)から、所得税と復興特別所得税を足した額。"""
    if t < 1000: return 0, 0, 0
    p, d = ritsu(t)
    base = F(t * p, 100) - d
    assert base.denominator == 1
    base = int(base)
    goukei = base * 1021 // 1000 // 100 * 100      # 2.1%を足して100円未満切り捨て
    return p, base, goukei

def ref(a, kaigo=0):
    g = kyuyo(a); sh = shaho(a, kaigo); k = kiso(g)
    t = max(0, g - sh - k) // 1000 * 1000
    p, base, x = zei_kazei(t)
    return {'g': g, 'sh': sh, 'k': k, 't': t, 'p': p, 'x': x, 'm': x // 12}

def man(s):
    return int(s.replace(',', '').replace('万円', '')) * 10000

async def body(pg):
    n = bad = 0
    def ng(*a):
        nonlocal bad
        bad += 1; print('NG', *a)

    # 1 計算の箱(入力欄に年収を入れて結果の箱を読む)
    cases = [0, 1, 740999, 741000, 741001, 1000000, 1779999, 1780000, 1780001, 2000000,
             2190999, 2191000, 2192999, 2193000, 2195999, 2196000, 2199999, 2200000, 2200001, 2203999, 2204000,
             3000000, 3599999, 3600000, 3600001, 5000000, 6599999, 6600000, 6600001,
             6655555, 6655556, 6655557, 7000000, 8499999, 8500000, 8500001, 10000000, 15000000, 20000000,
             25449999, 25450000, 25450001, 25950000, 25950001, 26450000, 26450001, 26950000, 26950001, 30000000]
    for kaigo in (0, 1):
        # 所得税がかかり始める年収と、速算表の境目に課税される所得がちょうど乗る年収を自分の計算で探す
        lows = [1000] + [lo for lo, _, _ in SOKUSAN[1:]]
        for lo in lows:
            lo_a, hi_a = 0, 30000000
            while lo_a < hi_a:                      # 課税される所得が lo 以上になる最初の年収(千円きざみ)
                mid = (lo_a + hi_a) // 2 // 1000 * 1000
                if ref(mid, kaigo)['t'] >= lo: hi_a = mid
                else: lo_a = mid + 1000
            if ref(lo_a, kaigo)['t'] >= lo:
                a0 = lo_a
                while a0 > 0 and ref(a0 - 1, kaigo)['t'] >= lo: a0 -= 1
                cases_k = [a0 - 1000, a0 - 1, a0, a0 + 1, a0 + 1000]
            else:
                cases_k = []
            for a in sorted(set(cases + cases_k)) if lo == lows[0] else cases_k:
                await pg.click('#s-age button[data-v="%d"]' % kaigo)
                await pg.fill('#inc', str(a))
                e = ref(a, kaigo); n += 1
                got = {'x': num(await pg.inner_text('#o-y')), 'm': num(await pg.inner_text('#o-m')),
                       't': num(await pg.inner_text('#o-d'))}
                for key in got:
                    if got[key] != e[key]: ng('箱', a, kaigo, key, got[key], e[key])
                tt = (await pg.inner_text('#o-t')).strip()
                want = ('税率%d%%' % e['p']) if e['t'] > 0 else '所得税はかかりません'
                if tt != want: ng('箱の税率', a, kaigo, tt, want)
                br = (await pg.inner_text('#o-br')).strip()
                wbr = '給与所得{:,}円から、社会保険料{:,}円と基礎控除{:,}円を引いて計算しています'.format(e['g'], e['sh'], e['k'])
                if br != wbr: ng('箱の内訳', a, kaigo, br, wbr)
                rr = (await pg.inner_text('#o-r')).strip()
                pct = F(e['x'] * 1000, a) if a else F(0)
                pct = F((pct.numerator * 2 + pct.denominator) // (2 * pct.denominator), 10)
                wr = '年収の%s%%' % (str(pct.numerator // pct.denominator) if pct.denominator == 1 else '%.1f' % float(pct))
                if rr != wr: ng('箱の割合', a, kaigo, rr, wr)

    tabs = await pg.evaluate('''()=>[...document.querySelectorAll("main table")].map(t=>[...t.querySelectorAll("tbody tr")].map(r=>[...r.cells].map(c=>c.innerText.trim())))''')
    # 2 速算表の全行
    t1 = tabs[0]
    names = ['195万円未満', '195万円以上 330万円未満', '330万円以上 695万円未満', '695万円以上 900万円未満',
             '900万円以上 1,800万円未満', '1,800万円以上 4,000万円未満', '4,000万円以上']
    if len(t1) != 7: ng('速算表の行数', len(t1))
    for i, row in enumerate(t1):
        n += 1
        lo, p, d = SOKUSAN[i]
        want = [names[i], '%d%%' % p, '{:,}円'.format(d)]
        if row != want: ng('速算表', row, want)
    # 3 課税される所得ごとの表の全行
    for row in tabs[1]:
        n += 1
        t = man(row[0]); p, base, x = zei_kazei(t)
        want = [row[0], '%d%%' % p, '{:,}'.format(base), '{:,}'.format(x)]
        if row != want: ng('課税される所得の表', row, want)
    if len(tabs[1]) != 19: ng('課税される所得の表の行数', len(tabs[1]))
    # 4 年収別の表の全行(40歳未満)
    for row in tabs[2]:
        n += 1
        a = man(row[0]); e = ref(a, 0)
        last = re.sub(r'\s+', ' ', row[6])
        want = [row[0], '{:,}'.format(e['g']), '{:,}'.format(e['sh']), '{:,}'.format(e['k']), '{:,}'.format(e['t']),
                ('%d%%' % e['p']) if e['t'] > 0 else '—', '{:,} 月 {:,}'.format(e['x'], e['m'])]
        if row[:6] + [last] != want: ng('年収別の表', row, want)
    if len(tabs[2]) != 25: ng('年収別の表の行数', len(tabs[2]))
    # 5 文の中の数字
    txt = await pg.inner_text('main')
    e5 = ref(5000000, 0)
    p7, b7, x7 = zei_kazei(7000000)
    checks = [
        '課税される所得は{:,}円で税率は{}%です。所得税は年{:,}円です'.format(e5['t'], e5['p'], e5['x']),
        '700万円 × {}% − 636,000円 = {:,}円。これに復興特別所得税2.1%を足して、{:,}円です'.format(p7, b7, x7),
        '年収500万円の会社員（単身）なら課税される所得は{:,}円で、税率は{}%です'.format(e5['t'], e5['p']),
        '給与所得控除74万円と基礎控除104万円の合計が178万円',
        '年収220万円までは74万円で、850万円以上は195万円です',
        '合計所得が489万円以下なら104万円です。489万円を超えて655万円以下なら67万円・655万円を超えて2,350万円以下なら62万円です',
        '給与だけの人は、年収178万円までは所得税がかかりません',
        '復興特別所得税（所得税額の2.1%）',
    ]
    for c in checks:
        n += 1
        if c not in txt: ng('文の数字', c)
    # 文の裏づけ:給与だけ(社会保険料なし)なら178万円まで0・178万1千円で課税される所得が出る/控除額は220万円で74万円・850万円で195万円
    n += 4
    if kyuyo(1780000) - kiso(kyuyo(1780000)) != 0: ng('178万円で0にならない')
    if (kyuyo(1781000) - kiso(kyuyo(1781000))) // 1000 * 1000 <= 0: ng('178万1千円で課税される所得が出ない')
    if 2200000 - kyuyo(2200000) != 740000: ng('220万円の給与所得控除')
    if 8500000 - kyuyo(8500000) != 1950000: ng('850万円の給与所得控除')
    return n, bad

run('shotokuzei', body)
