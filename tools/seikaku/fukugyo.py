# /fukugyo/ 副業の税金の計算(確定申告が要るかの判定・副業で増える所得税と住民税・早見表)。
# 原本:
#  国税庁 No.1900 給与所得者で確定申告が必要な人(令和8年4月1日現在法令等。年収2,000万円超・給与以外の所得の合計20万円超・2か所給与)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm
#  国税庁 No.2260 所得税の税率(速算表・復興特別所得税2.1%) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
#  国税庁 令和8年分 年末調整のしかた(基礎控除 489万円以下104万円・655万円以下67万円・2,350万円以下62万円・48・32・16万円・0円)
#   https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/302.pdf
#  国税庁「暮らしの税情報 給与所得者と税」(令和8年分の給与所得控除後の金額の表・課税所得1,000円未満切捨て・所得税等100円未満切捨て)
#   https://www.nta.go.jp/publication/pamph/koho/kurashi/html/02_1.htm
#  千葉市「令和9年度から適用される個人市・県民税の主な改正点」(給与所得控除の最低保障74万円は令和9・10年度。住民税の基礎控除は改正なし)
#   https://www.city.chiba.jp/zaiseikyoku/zeimu/kazeikanri/zeiseikaiseijuminzei2027.html
#  江戸川区「所得控除」(住民税の基礎控除 43万・29万・15万円・2,500万円超は適用なし)
#   https://www.city.edogawa.tokyo.jp/e013/kurashi/zeikin/juminzei/zei_gaiyo/shotokukojyo.html
#  練馬区「調整控除」(式・合計所得2,500万円超は適用なし・基礎控除の差5万円)
#   https://www.city.nerima.tokyo.jp/kurashi/zei/jyuminzei/zeigakukojo/choseikojo.html
#  大田区「特別区民税・都民税(住民税)が課税されない方」(単身は合計所得45万円以下で均等割・所得割とも非課税)
#   https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/hikazei.html
#  大田区「住民税の計算のしくみ」(均等割 特別区民税3,000円+都民税1,000円+森林環境税1,000円・6%と4%・100円未満切捨て)
#   https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/keisannosikumi.html
#  協会けんぽ 令和8年度 都道府県単位保険料率(東京都9.85%・子ども子育て支援金0.23%) https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  協会けんぽ 東京都の保険料額表(50銭以下切捨て・50銭超切上げ) https://www.kyoukaikenpo.or.jp/assets/R8.10_13%E6%9D%B1%E4%BA%AC.pdf
#  厚生労働省「令和8年度 雇用保険料率のご案内」(一般の事業 労働者負担 5/1,000) https://www.mhlw.go.jp/content/001692566.pdf
#  川口市「申告フローチャート」(給与・年金以外に所得があれば市民税・県民税の申告) https://www.city.kawaguchi.lg.jp/material/files/group/23/sinkoku3.pdf
# 最後に原本を確かめた日:2026-11-20
# 前提(ページの記載どおり):単身・本業は年末調整あり・協会けんぽ東京都・40歳未満・賞与なしで月給=年収÷12・住民税は東京23区。
import os, re, sys, random
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num, SITE

def fl(v):
    return v.numerator // v.denominator

def kyuyo(x):
    if x <= 740999: return 0
    if x <= 2190999: return x - 740000
    if x <= 2192999: return 1451000
    if x <= 2195999: return 1453000
    if x <= 2199999: return 1456000
    q = x // 4 // 1000 * 1000
    if x <= 3599999: return q * 28 // 10 - 80000
    if x <= 6599999: return q * 32 // 10 - 440000
    if x <= 8499999: return x * 9 // 10 - 1100000
    return x - 1950000

# 標準報酬月額(健康保険)。報酬月額の下限(千円)と標準報酬月額(千円)
LOW = [0, 63, 73, 83, 93, 101, 107, 114, 122, 130, 138, 146, 155, 165, 175, 185, 195, 210, 230, 250, 270, 290, 310, 330,
       350, 370, 395, 425, 455, 485, 515, 545, 575, 605, 635, 665, 695, 730, 770, 810, 855, 905, 955, 1005, 1055, 1115,
       1175, 1235, 1295, 1355]
STD = [58, 68, 78, 88, 98, 104, 110, 118, 126, 134, 142, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 320, 340,
       360, 380, 410, 440, 470, 500, 530, 560, 590, 620, 650, 680, 710, 750, 790, 830, 880, 930, 980, 1030, 1090, 1150,
       1210, 1270, 1330, 1390]
assert len(LOW) == len(STD) == 50

def hyojun(m):
    v = STD[0]
    for lo, s in zip(LOW, STD):
        if m >= lo * 1000: v = s
    return v * 1000

def r50(v):
    q = fl(v)
    return q + 1 if v - q > F(1, 2) else q

def shaho(a):
    m = a // 12
    s = hyojun(m)
    kenpo = r50(F(s) * (F(985, 10000) + F(23, 10000)) / 2)
    nenkin = r50(F(min(max(s, 88000), 650000)) * F(183, 1000) / 2)
    koyo = r50(F(m) * F(5, 1000))
    return (kenpo + nenkin + koyo) * 12

def kiso_i(g):
    for top, v in ((4890000, 1040000), (6550000, 670000), (23500000, 620000), (24000000, 480000),
                   (24500000, 320000), (25000000, 160000)):
        if g <= top: return v
    return 0

def zei(t):
    """所得税法89条:195万円以下5%、330万円以下10%…(超過累進)。税率は t が入る段の率。"""
    tops = [(1950000, 5), (3300000, 10), (6950000, 20), (9000000, 23), (18000000, 33), (40000000, 40), (None, 45)]
    tax, prev, rate = F(0), 0, 5
    for top, r in tops:
        hi = t if top is None else min(t, top)
        if hi > prev: tax += F(hi - prev) * r / 100
        if top is None or t <= top:
            rate = r; break
        prev = top
    return fl(tax), rate

def itax(a, s):
    g = kyuyo(a) + s
    t = max(0, g - shaho(a) - kiso_i(g)) // 1000 * 1000
    b, r = zei(t)
    return fl(F(b) * F(1021, 1000)) // 100 * 100, r

def jumin(a, s):
    g = kyuyo(a) + s
    if g <= 450000: return 0
    k = 430000 if g <= 24000000 else 290000 if g <= 24500000 else 150000 if g <= 25000000 else 0
    t = max(0, g - shaho(a) - k) // 1000 * 1000
    if g > 25000000: adj = F(0)
    elif t <= 2000000: adj = F(min(50000, t))
    else: adj = F(max(50000 - (t - 2000000), 50000))
    shi = max(0, fl(F(t) * 6 / 100 - adj * 3 / 100)) // 100 * 100
    ken = max(0, fl(F(t) * 4 / 100 - adj * 2 / 100)) // 100 * 100
    return shi + ken + 5000

def calc(a, s):
    i = itax(a, s)[0] - itax(a, 0)[0]
    j = jumin(a, s) - jumin(a, 0)
    need = a > 20000000 or s > 200000
    xi = i if need else 0
    tot = xi + j
    net = fl(F(s - tot, 1000) + F(1, 2))      # 0.1万円単位(JSの Math.round と同じ向き)
    return {'all': tot, 'i': xi, 'j': j, 'rate': itax(a, s)[1], 'need': need, 'net': net, 'tbl': i + j}

JS = '''([a,s])=>{var q=function(i){return document.getElementById(i)};
 var x=q("inc");x.value=String(a);x.dispatchEvent(new Event("input",{bubbles:true}));
 var y=q("sid");y.value=String(s);y.dispatchEvent(new Event("input",{bubbles:true}));
 var n=function(i){var t=q(i).textContent;var v=parseInt(t.replace(/[^0-9]/g,""),10);return /[-−]/.test(t)?-v:v};
 var m=q("o-net").textContent.match(/約(-?[0-9.]+)万円/);
 return {all:n("o-all"),i:n("o-i"),j:n("o-j"),rate:parseInt(q("o-2").textContent.match(/税率は([0-9]+)%/)[1],10),
  vd:q("o-vd").textContent,net:m?Math.round(parseFloat(m[1])*10):null}}'''

def cases():
    A = [0, 1000000, 1500000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 8500000, 10000000,
         12000000, 15000000, 19990000, 20000000, 20000001, 20010000, 25000000, 30000000]
    for x in (741000, 2191000, 2193000, 2196000, 2200000, 3600000, 6600000, 8500000):
        A += [x - 1, x, x + 1]
    for lo in LOW[1:]:
        A += [lo * 12000 - 1, lo * 12000, lo * 12000 + 11]
    S = [0, 1, 10000, 100000, 199999, 200000, 200001, 210000, 300000, 500000, 1000000, 2000000, 5000000, 10000000,
         20000000, 30000000]
    out = {(a, s) for a in A[:20] for s in S}
    out |= {(a, s) for a in A[20:] for s in (0, 200000, 200001, 300000)}
    # 合計所得の境目(基礎控除の段・住民税の基礎控除・調整控除・住民税の非課税)。本業500万円・1,500万円・0円に副業を足して当てる
    for a in (0, 5000000, 15000000, 30000000):
        for G in (450000, 4890000, 6550000, 23500000, 24000000, 24500000, 25000000):
            for d in (-1, 0, 1, 1000):
                s = G - kyuyo(a) + d
                if 0 <= s <= 30000000: out.add((a, s))
    # 課税所得が税率の境目になる副業の所得
    for a in (3000000, 5000000, 7000000):
        base = kyuyo(a)
        for T in (1950000, 3300000, 6950000, 9000000, 18000000):
            for s0 in range(max(0, T - base), max(0, T - base) + 2000000, 1000):
                g = base + s0
                if max(0, g - shaho(a) - kiso_i(g)) // 1000 * 1000 >= T:
                    for d in (-1000, -1, 0, 1, 999, 1000):
                        if 0 <= s0 + d <= 30000000: out.add((a, s0 + d))
                    break
    return sorted(out)

async def body(pg):
    n = bad = 0
    # 書き換え前の HTML に書かれた数字(既定 年収500万円・副業30万円)
    html = open(os.path.join(SITE, 'fukugyo', 'index.html'), encoding='utf-8').read()
    e = calc(5000000, 300000)
    pre = {'o-all': e['all'], 'o-i': e['i'], 'o-j': e['j']}
    for k, v in pre.items():
        m = re.search(r'id="%s">([0-9,]+)<i>' % k, html); n += 1
        if not m or num(m.group(1)) != v:
            bad += 1; print('NG 書き換え前の数字', k, m and m.group(1), v)
    n += 1
    if '約%s万円' % ('%g' % (e['net'] / 10)) not in html or '所得税率は%d%%' % e['rate'] not in html:
        bad += 1; print('NG 書き換え前の手元・税率', e)
    # Q&A「副業30万円で税金はいくら増える?」
    n += 1
    want = '所得税が約%s万円・住民税が約%s万円で合わせて約%s万円' % tuple(
        '%g' % (round(F(v, 1000)) / 10) for v in (e['i'], e['j'], e['all']))
    if want not in html:
        bad += 1; print('NG Q&Aの文', want)
    # 画面の結果
    for a, s in cases():
        got = await pg.evaluate(JS, [a, s])
        exp = calc(a, s); n += 1
        ok = (got['all'], got['i'], got['j'], got['rate'], got['net']) == (exp['all'], exp['i'], exp['j'], exp['rate'], exp['net'])
        ok = ok and (got['vd'] == ('確定申告が必要です' if exp['need'] else '確定申告は不要です'))
        if not ok:
            bad += 1; print('NG', a, s, got, exp)
    rnd = random.Random(20261120)
    for _ in range(1500):
        a = rnd.choice([rnd.randrange(0, 30000001), rnd.randrange(1000000, 15000001)])
        s = rnd.choice([rnd.randrange(0, 400001), rnd.randrange(0, 5000001), rnd.randrange(0, 30000001)])
        got = await pg.evaluate(JS, [a, s]); exp = calc(a, s); n += 1
        if (got['all'], got['i'], got['j'], got['rate'], got['net']) != (exp['all'], exp['i'], exp['j'], exp['rate'], exp['net']):
            bad += 1; print('NG', a, s, got, exp)
    # 早見表(副業の所得を確定申告に入れた場合の所得税+住民税)
    rows = await pg.evaluate('''()=>[...document.querySelectorAll("#gtb tr")].map(function(tr){return [...tr.cells].map(function(c){return parseInt(c.textContent.replace(/[^0-9]/g,""),10)})})''')
    n += 1
    if [r[0] for r in rows] != [x * 10000 for x in (10, 20, 30, 50, 80, 100, 150, 200, 300, 500)]:
        bad += 1; print('NG 早見表の行', [r[0] for r in rows])
    for r in rows:
        for j, a in enumerate((3000000, 5000000, 7000000)):
            exp = calc(a, r[0])['tbl']; n += 1
            if r[1 + j] != exp:
                bad += 1; print('NG 早見表', r[0], a, r[1 + j], exp)
    return n, bad

run('fukugyo', body)
