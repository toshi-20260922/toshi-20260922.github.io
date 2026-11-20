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
#  国税庁 No.1199 基礎控除(令和8年4月1日現在法令等。令和8年分・令和9年分の段) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#  国税庁 No.1410 給与所得控除(令和8年分・令和9年分 220万円まで74万円・注2の表) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
#  国税庁 No.1500 雑所得(業務に係る雑所得・損益通算できない) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1500.htm
#  所得税基本通達35-2(注)と解説(帳簿書類の保存・収入300万円・主たる収入の10%未満は僅少として個別判断)
#   https://www.nta.go.jp/law/tsutatsu/kihon/shotoku/04/09.htm https://www.nta.go.jp/law/tsutatsu/kihon/shotoku/kaisei/221007/pdf/02.pdf
#  国税庁 No.2795 原稿料や講演料等を支払ったとき(100万円以下10.21%) https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2795.htm
#  国税庁 No.1521 FXの課税関係(所得税15%・地方税5%・復興2.1%) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1521.htm
#  国税庁 No.3105(生活用動産は非課税・1個または1組30万円超の貴金属などは除く) https://www.nta.go.jp/taxes/shiraberu/taxanswer/joto/3105.htm
#  国税庁 No.2090 新たに事業を始めたときの届出など(開業届はその年分の確定申告期限まで・青色申告承認申請は開業から2月以内。1月15日までの開業は3月15日)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2090.htm
#  名古屋市「給与所得者で副収入がある場合、市民税・県民税の申告は?」(住民税には申告の省略範囲がない・確定申告をすれば住民税の申告は不要)
#   https://www.city.nagoya.jp/kurashi/zeikin/1035069/1012012/1012022/1033974/1012026.html
#  横浜市「市民税・県民税の申告」(期限3月15日・1月1日現在の住所地・2か所給与で20万円以下の人も申告が必要)
#   https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/zeikin/y-shizei/kojin-shiminzei-kenminzei/kojin-shiminzei-shosai/shiminzei-shinkoku.html
#  仙台市「令和9年度(令和8年分)から適用される個人市県民税の税制改正等について」(給与所得控除74万円・住民税の基礎控除は改正なし・単身の非課税は給与収入119万円=合計所得45万円)
#   https://www.city.sendai.jp/shiminze-kikaku/kurashi/tetsuzuki/zekin/kojin/kaisei/r8.html
#  日本年金機構「複数の事業所に雇用されるようになったときの手続き」(本人が届出・主たる事業所を選択・合算して按分)
#   https://www.nenkin.go.jp/service/kounen/tekiyo/hihokensha1/20131022.html
#  厚生労働省「雇用保険マルチジョブホルダー制度」(65歳以上・2つの事業所) https://www.mhlw.go.jp/content/11600000/000838542.pdf
# 最後に原本を確かめた日:2026-11-20
# 11-20 の申し送り:開業届の期限は「1か月以内」ではなく「その年分の確定申告期限まで」に変わっている(No.2090)。ほかのページの「開業届 1か月以内」も探す。
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
  vd:q("o-vd").textContent,vds:q("o-vds").textContent,ie:q("o-ie").textContent,o1:q("o-1").textContent,
  net:m?Math.round(parseFloat(m[1])*10):null}}'''

def words(a, s):
    """No.1900 の1(給与収入2,000万円超)と2(給与以外の所得20万円超)。申告しない人は住民税の申告(名古屋市・横浜市)。"""
    if a > 20000000: return '2,000万円を超える', '住民税の申告は確定申告で済みます', '令和8年分', '確定申告をすれば住民税の申告は別に要りません'
    if s > 200000: return '20万円を超える', '住民税の申告は確定申告で済みます', '令和8年分', '確定申告をすれば住民税の申告は別に要りません'
    return '20万円以下', '住民税の申告は必要です', '申告しないので増えない', '市区町村に住民税の申告をします'

# 手で書かれた表を、原本から自分で決めた答えと比べる
def judge_want(label):
    """(確定申告, 住民税申告)。No.1900:年収2,000万円超・給与以外の所得20万円超・年末調整されなかった給与の収入20万円超は申告が要る。
    確定申告をすれば住民税の申告は要らない。確定申告をしない人で給与以外の所得か2か所めの給与があれば住民税の申告が要る。"""
    if '赤字' in label and '雑所得' in label: return '不要', '不要'          # 所得が0(雑所得の赤字はほかと通算できない)
    if '取り戻したい' in label or '差し引きたい' in label: return '任意', '不要※'  # 還付の申告は義務でない
    if '確定申告をする' in label: return '要る', '不要※'
    if '2,000万円を超える' in label: return '要る', '不要※'
    if '20万円を超える' in label: return '要る', '不要※'
    if '20万円以下' in label: return '不要', '要る'
    return None, None


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
        w = words(a, s)
        ok = ok and w[0] in got['vds'] and w[1] in got['vds'] and got['ie'] == w[2] and w[3] in got['o1'] and '3月15日' in got['vds'] + got['o1']
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
    COLS = (3000000, 5000000, 7000000, 10000000)
    heads = await pg.evaluate('()=>[...document.getElementById("gtb").closest("table").querySelectorAll("thead th")].map(function(c){return c.textContent})')
    n += 1
    if len(heads) != 1 + len(COLS) or any('年収%s万円' % format(a // 10000, ',') not in heads[1 + j] for j, a in enumerate(COLS)):
        bad += 1; print('NG 早見表の列', heads)
    for r in rows:
        n += 1
        if len(r) != 1 + len(COLS):
            bad += 1; print('NG 早見表の列の数', r); continue
        for j, a in enumerate(COLS):
            exp = calc(a, r[0])['tbl']; n += 1
            if r[1 + j] != exp:
                bad += 1; print('NG 早見表', r[0], a, r[1 + j], exp)
    # ---- 手で書かれた表(判定の表・所得の種類・事業/雑所得・勤め先) ----
    tb = await pg.evaluate('''()=>[...document.querySelectorAll("main table")].map(function(t){return [...t.querySelectorAll("tbody tr")].map(function(tr){return [...tr.cells].map(function(c){return c.textContent.trim()})})})''')
    n += 1
    if len(tb) != 5:
        bad += 1; print('NG 表の数', len(tb)); return n, bad
    jt, kinds, jz, emp = tb[0], tb[2], tb[3], tb[4]
    n += 1
    if len(jt) != 9: bad += 1; print('NG 判定の表の行の数', len(jt))
    for r in jt:
        n += 1
        if (r[1], r[2]) != judge_want(r[0]):
            bad += 1; print('NG 判定の表', r, judge_want(r[0]))
    # アルバイト(給与)の行は収入、それ以外は所得で20万円を見る(No.1900 の3と2)
    for r in jt:
        if '20万円' in r[0]:
            n += 1
            if ('給料で' in r[0]) != ('収入' in r[0]) or ('給料以外' in r[0]) != ('所得が' in r[0]):
                if '取り戻したい' not in r[0]: bad += 1; print('NG 判定の表の収入と所得', r[0])
    # 所得の種類の表:率と金額を原本の数字から出して比べる
    gensen = F(10) * F(1021, 1000)                    # 所得税10%に復興特別所得税2.1%
    fx = F(15) * F(1021, 1000) + 5                    # 所得税15%+復興+住民税5%
    KIND = {'アルバイト': ('給与所得', ['20万円は収入の額']), '物販': ('事業所得か雑所得', []), 'アフィリエイト': ('事業所得か雑所得', []),
            '原稿料': ('事業所得か雑所得', ['%s%%' % float(gensen)]), '不用品': ('原則かからない', ['1個30万円を超える']),
            '暗号資産': ('雑所得', ['差し引くことはできません']), 'FX': ('雑所得（申告分離課税）', ['%s%%' % float(fx), '本業とは分けて']),
            '株式': ('譲渡所得など', ['特定口座']), '貸す': ('不動産所得', [])}
    n += 1
    if len(kinds) != len(KIND): bad += 1; print('NG 所得の種類の表の行の数', len(kinds))
    for r in kinds:
        k = [x for x in KIND if x in r[0]]; n += 1
        if len(k) != 1 or r[1] != KIND[k[0]][0] or any(w not in r[2] for w in KIND[k[0]][1]):
            bad += 1; print('NG 所得の種類の表', r)
    # 事業所得か雑所得か(通達35-2 の注と解説):帳簿あり→概ね事業所得(300万円以下で主たる収入の10%未満は僅少として個別判断)・帳簿なし→雑所得
    n += 1
    if len(jz) != 3: bad += 1; print('NG 事業/雑所得の表の行の数', len(jz))
    for r in jz:
        n += 1
        if 'つけていない' in r[0]: ok = '雑所得' in r[2] and '事業所得' not in r[2] and '300' not in r[1]
        elif r[1] == '300万円を超える': ok = r[2] == '原則として事業所得'
        elif r[1] == '300万円以下': ok = r[2].startswith('原則として事業所得') and '10%に満たない' in r[2] and '収入がわずか' in r[2] and '個別' in r[2] and '雑所得' in r[2]
        else: ok = False
        if not ok: bad += 1; print('NG 事業/雑所得の表', r)
    # 勤め先の表
    EMP = {'アルバイトを始めた': ['扶養控除等申告書', '年末調整はそのまま'], '副業先として': ['乙欄', '年末調整はしません'], '住民税の通知': ['通知どおり'],
           '社会保険': ['本人が届け出て', '主たる事業所を選びます', '合わせた額', '割合で分けて'], '雇用保険': ['1社だけ', '65歳以上']}
    n += 1
    if len(emp) != len(EMP): bad += 1; print('NG 勤め先の表の行の数', len(emp))
    for r in emp:
        k = [x for x in EMP if x in r[0]]; n += 1
        if len(k) != 1 or any(w not in r[1] for w in EMP[k[0]]):
            bad += 1; print('NG 勤め先の表', r)
    # ---- よくある質問と本文の数字 ----
    import datetime
    d = datetime.date(2027, 3, 15)                    # 令和8年分の期限。土日なら翌開庁日にずれる
    n += 1
    if d.weekday() >= 5: bad += 1; print('NG 2027年3月15日が土日。3月15日の文を見直す')
    qa = await pg.evaluate('''()=>{var h=document.getElementById("qa"),o=[],e=h.nextElementSibling,q=null;
      while(e&&e.tagName!=="H2"&&!e.classList.contains("src")){if(e.tagName==="H3"){q=[e.textContent,""];o.push(q)}else if(q&&e.tagName==="P"){q[1]+=e.textContent}e=e.nextElementSibling}return o}''')
    QA = {'売上ですか': ['経費を引いた所得', '収入の額で判定'], '何もしなくて': ['住民税の申告は要ります', '3月15日'], '医療費控除': ['書く必要があります', '含めて申告'],
          '30万円で': ['年収500万円'], '赤字で': ['雑所得なら', '相殺することはできません', '事業所得'], '知られず': ['普通徴収'],
          '開業届': ['確定申告の期限まで', '2か月以内', '1月15日まで', '3月15日まで']}
    n += 1
    if len(qa) != len(QA): bad += 1; print('NG よくある質問の数', len(qa))
    for q, ans in qa:
        k = [x for x in QA if x in q]; n += 1
        if len(k) != 1 or any(w not in ans for w in QA[k[0]]) or '1か月以内' in ans:
            bad += 1; print('NG よくある質問', q, ans)
    # 本文に過去の誤りの形が残っていないか
    txt = await pg.evaluate('()=>document.querySelector("main").innerText')
    for w in ('開業の日から1か月以内', '年金事務所を選びます', '営利性が低い'):
        n += 1
        if w in txt: bad += 1; print('NG 古い文', w)
    for w in ('20万円の決まりがあるのは所得税だけです', '期限は翌年の3月15日', '所得割10%', '令和8年分（復興特別所得税を含む）、住民税は令和9年度'):
        n += 1
        if w not in txt: bad += 1; print('NG 文が無い', w)
    return n, bad

run('fukugyo', body)
