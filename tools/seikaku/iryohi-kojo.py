# /iryohi-kojo/ 医療費控除の計算(戻る所得税と翌年度に減る住民税)。
# 原本:
#  国税庁 No.1120 医療費を支払ったとき(医療費控除) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1120.htm
#   (支払った医療費 − 保険金などで補てんされる金額) − 10万円(総所得金額等が200万円未満の人は5%)。最高200万円
#  国税庁 No.1410 給与所得控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
#   令和8年分・9年分:220万円まで74万円。660万円未満は別表第五(4,000円刻みの切り捨て。220万円未満は注2の表)
#  国税庁 No.1199 基礎控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#   令和8年分:489万円以下104万円・655万円以下67万円・2,350万円以下62万円・48万円・32万円・16万円・0円
#  国税庁 No.2260 所得税の税率 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
#   課税される所得金額は1,000円未満切り捨て。復興特別所得税は基準所得税額の2.1%
#  国税庁 令和8年分 年末調整のしかた https://www.nta.go.jp/users/gensen/nencho/index/shikata.htm
#   年調年税額=年調所得税額×102.1%(100円未満切り捨て)
#  全国健康保険協会 令和8年3月分からの保険料額表(東京都) https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#   健康保険9.85%・子ども・子育て支援金0.23%・厚生年金18.3%(88,000円から650,000円)・等級の境目
#  厚生労働省 令和8年度 雇用保険料率のご案内 https://www.mhlw.go.jp/content/001692566.pdf  労働者負担 5/1,000
#  住民税は、ページの注記どおり「医療費控除の額の10%」(所得割の標準税率 市6%・県4%)で照らす。
# 最後に原本を確かめた日:2026-11-19
# 社会保険料は、ページの注記の前提(毎月同じ額・賞与なし・令和8年度の料率を12か月)で1年分を分数で出し、1円未満を四捨五入する。
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

# 保険料額表の等級(標準報酬月額, 報酬月額の下の境目)。協会けんぽの表のとおり手で写したもの。
GRADE = [(58000, 0), (68000, 63000), (78000, 73000), (88000, 83000), (98000, 93000), (104000, 101000),
         (110000, 107000), (118000, 114000), (126000, 122000), (134000, 130000), (142000, 138000),
         (150000, 146000), (160000, 155000), (170000, 165000), (180000, 175000), (190000, 185000),
         (200000, 195000), (220000, 210000), (240000, 230000), (260000, 250000), (280000, 270000),
         (300000, 290000), (320000, 310000), (340000, 330000), (360000, 350000), (380000, 370000),
         (410000, 395000), (440000, 425000), (470000, 455000), (500000, 485000), (530000, 515000),
         (560000, 545000), (590000, 575000), (620000, 605000), (650000, 635000), (680000, 665000),
         (710000, 695000), (750000, 730000), (790000, 770000), (830000, 810000), (880000, 855000),
         (930000, 905000), (980000, 955000), (1030000, 1005000), (1090000, 1055000), (1150000, 1115000),
         (1210000, 1175000), (1270000, 1235000), (1330000, 1295000), (1390000, 1355000)]

def hyojun(m):
    h = GRADE[0][0]
    for g, lo in GRADE:
        if m >= lo:
            h = g
    return h

def shaho_nen(s):
    m = F(s, 12)
    h = hyojun(m)
    k = min(max(h, 88000), 650000)
    nen = 12 * (F(h * (985 + 23), 20000) + F(k * 183, 2000)) + F(s * 5, 1000)
    return int(nen + F(1, 2))                     # 1円未満四捨五入

def kyuyo_shotoku(s):
    if s < 741000:
        return 0
    if s < 2191000:
        return s - 740000
    if s < 2193000:
        return 1451000
    if s < 2196000:
        return 1453000
    if s < 2200000:
        return 1456000
    if s < 6600000:
        a = s // 4000 * 4000                      # 別表第五:4,000円刻みで切り捨て
        return a * 7 // 10 - 80000 if s < 3600000 else a * 8 // 10 - 440000
    if s < 8500000:
        return s * 9 // 10 - 1100000
    return s - 1950000

def kiso(x):
    for top, v in ((4890000, 1040000), (6550000, 670000), (23500000, 620000), (24000000, 480000),
                   (24500000, 320000), (25000000, 160000)):
        if x <= top:
            return v
    return 0

SOKUSAN = [(1949000, 5, 0), (3299000, 10, 97500), (6949000, 20, 427500), (8999000, 23, 636000),
           (17999000, 33, 1536000), (39999000, 40, 2796000), (None, 45, 4796000)]

def zei(k):
    k = max(k, 0) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or k <= top:
            return k * r // 100 - d               # 1,000円単位なので割り切れる

def ref(s, med, hot):
    sh = kyuyo_shotoku(s)
    sa = shaho_nen(s)
    ashi = 100000 if sh >= 2000000 else sh * 5 // 100
    kj = min(max(med - hot - ashi, 0), 2000000)
    nencho = zei(sh - sa - kiso(sh)) * 1021 // 1000 // 100 * 100      # 年末調整で決まった額
    t = zei(sh - sa - kiso(sh) - kj)
    shinkoku = t + t * 21 // 1000                                      # 確定申告:基準所得税額+復興特別所得税
    st = max(nencho - shinkoku, 0) if kj > 0 else 0
    jm = kj // 10
    return {'kojo': kj, 'shotoku': st, 'jumin': jm, 'total': st + jm}

def digits(t):
    return int(''.join(c for c in t if c.isdigit()) or 0)

async def body(pg):
    n = bad = 0
    # 1) 関数を呼んで比べる。年収は画面で入れられる300万円から2,000万円。
    incomes = [3000000, 3000001, 3003999, 3004000, 3599999, 3600000, 3600001, 4000000, 4500000, 5000000,
               5000100, 5000300, 5555555, 6000000, 6599999, 6600000, 6600001, 7000000, 7777777, 8000000,
               8499999, 8500000, 8500001, 9000000, 10000000, 12000000, 15000000, 18000000, 20000000]
    # 等級の境目(月額がちょうど・1円下・1円上になる年収)。上のほうの等級を全部入れる。
    for g, lo in GRADE:
        if 250000 <= lo <= 1660000:
            incomes += [lo * 12 - 12, lo * 12, lo * 12 + 12]
    # 基礎控除の境目(給与所得が489万円・655万円をまたぐ年収)と、所得税の税率の境目をまたぐ年収
    for target in (4890000, 6550000):
        for s in range(6000000, 9000000, 4000):
            if kyuyo_shotoku(s) <= target < kyuyo_shotoku(s + 4000):
                incomes += [s - 1, s, s + 3999, s + 4000, s + 4001]
    for top, _, _ in SOKUSAN[:-2]:
        lo_s, hi_s = 3000000, 20000000
        while hi_s - lo_s > 1:                    # 課税所得がちょうど境目になる年収を二分で探す
            mid = (lo_s + hi_s) // 2
            if kyuyo_shotoku(mid) - shaho_nen(mid) - kiso(kyuyo_shotoku(mid)) > top + 1000:
                hi_s = mid
            else:
                lo_s = mid
        incomes += [lo_s - 5000, lo_s - 1, lo_s, hi_s, hi_s + 5000]
    incomes = sorted(set(s for s in incomes if 3000000 <= s <= 20000000))
    meds = [0, 99999, 100000, 100001, 100999, 101000, 150000, 200000, 300000, 500000, 1000000, 1234567,
            2099999, 2100000, 2100001, 3000000, 10000000]
    cases = [(s, m, 0) for s in incomes for m in meds]
    cases += [(s, 500000, h) for s in (3000000, 5000000, 7000000, 12000000) for h in (1, 100000, 399999, 400000, 400001, 500000, 600000)]
    # 給与所得が200万円をまたぐ年収(画面では入れられないが、関数の5%の枝を確かめる)
    for s in (1000000, 2000000, 2190999, 2200000, 2971999, 2972000, 2999999):
        cases += [(s, m, 0) for m in (50000, 74999, 75000, 75001, 99999, 100000, 100001, 150000, 300000)]
    for s, m, h in cases:
        got = await pg.evaluate('([s,m,h])=>window.__iryo(s,m,h)', [s, m, h])
        exp = ref(s, m, h); n += 1
        if any(got[k] != exp[k] for k in exp):
            bad += 1; print('NG 関数', s, m, h, got, exp)
    # 2) 入力欄に入れて結果の箱を読む
    for s, m, h in [(5000000, 300000, 0), (3000000, 150000, 0), (7000000, 500000, 120000), (15000000, 1000000, 0),
                    (20000000, 10000000, 0), (5000000, 100000, 0), (9000000, 2500000, 300000)]:
        for i, v in (('#inc', s), ('#med', m), ('#hot', h)):
            await pg.fill(i, str(v))
        exp = ref(s, m, h)
        for box, key in (('#o-k', 'total'), ('#o-t', 'shotoku'), ('#o-z', 'jumin')):
            n += 1
            shown = digits(await pg.inner_text(box))
            if shown != exp[key]:
                bad += 1; print('NG 画面', s, m, h, box, shown, exp[key])
        n += 1
        e = await pg.inner_text('#o-e')
        want = ('医療費控除の額は%s円' % format(exp['kojo'], ',')) if exp['kojo'] > 0 else '10万円を超えた分が対象です'
        if e != want:
            bad += 1; print('NG 画面の控除額の文', s, m, h, e, want)
    # 3) 手で書いた早見表の全行(合計と住民税)
    html = await pg.content()
    tb = re.search(r'<tbody id="tb">(.*?)</tbody>', html, re.S).group(1)
    cols = [150000, 200000, 300000, 500000, 1000000]
    rows = re.findall(r'<tr data-s="(\d+)"[^>]*>(.*?)</tr>', tb, re.S)
    if len(rows) != 10:
        bad += 1; print('NG 早見表の行の数', len(rows))
    for ds, tr in rows:
        cells = re.findall(r'<b>([\d,]+)</b><br><small>([\d,]+)</small>', tr)
        first = digits(re.search(r'<td>([\d,]+)</td>', tr).group(1))
        n += 1
        if first != int(ds) or len(cells) != 5:
            bad += 1; print('NG 早見表の行', ds, first, len(cells))
        for (tot, jm), m in zip(cells, cols):
            exp = ref(int(ds) * 10000, m, 0); n += 2
            if digits(tot) != exp['total']:
                bad += 1; print('NG 早見表 合計', ds, m, tot, exp['total'])
            if digits(jm) != exp['jumin']:
                bad += 1; print('NG 早見表 住民税', ds, m, jm, exp['jumin'])
    # 4) 本文に手で書いた例の数字
    text = await pg.inner_text('main')
    for s, m, where in ((5000000, 300000, '合わせて%s円が目安です'), (5000000, 300000, '年収500万円は%s円'),
                        (7000000, 300000, '年収700万円は%s円')):
        n += 1
        w = where % format(ref(s, m, 0)['total'], ',')
        if w not in text:
            bad += 1; print('NG 本文の例', w)
    # よく聞かれること:給与所得150万円なら5%は7万5,000円/令和8年分の還付申告は令和13年12月31日まで
    n += 1
    if 1500000 * 5 // 100 != 75000 or '7万5,000円を超えた分' not in text:
        bad += 1; print('NG 5%の例')
    n += 1
    if '令和%d年12月31日までです' % (8 + 5) not in text:
        bad += 1; print('NG 還付申告の期限の例')
    return n, bad

run('iryohi-kojo', body)
