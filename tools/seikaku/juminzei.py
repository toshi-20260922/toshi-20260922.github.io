# /juminzei/ 住民税の早見表(令和9年度の住民税・東京23区・単身・給与だけ)。
# 原本:
#  地方税法附則3条の3(所得割の非課税 35万円×(本人+同一生計配偶者+扶養親族)+10万円(+32万円)、
#   限度額を超えても所得割を引いたあとの所得が限度額を下回らないよう所得割を減らす。道府県分と市町村分は所得割の割合で分ける)
#   https://www.sn-hoki.co.jp/data/pickup_hourei/onct/CHIHOUZEI-HOU20240221-2.html
#   横浜市「税額控除(令和8年度課税以降)」(所得割の調整額=所得割非課税限度額−(総所得金額等−所得割額)、調整控除の式、2,500万円超は調整控除なし)
#   https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/zeikin/y-shizei/kojin-shiminzei-kenminzei/kojin-shiminzei-shosai/zeigakukoujoR8.html
#  練馬区「住民税が非課税になる基準」(均等割 45万円/35万円×人数+10万円+21万円、所得割 45万円/…+32万円、給与収入の目安)
#   https://www.city.nerima.tokyo.jp/kurashi/zei/jyuminzei/hikazeikijun/juuminzei-hikazei.html
#  総務省「個人住民税」(均等割の非課税限度額は級地で1.0・0.9・0.8。所得割は10%)
#   https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/149767_03.html
#  東京都主税局「個人住民税」(都民税1,000円・区民税3,000円・森林環境税1,000円、所得割4%・6%、調整控除2%・3%)
#   https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju
#  港区「特別区民税・都民税の計算」(課税標準1,000円未満切捨て・区民税と都民税を別々に100円未満切捨て)
#   https://www.city.minato.tokyo.jp/kazei/kurashi/zekin/juminze/tominze/kesan.html
#  中央区「令和9年度から適用される個人住民税の主な改正」(給与所得控除の最低保障額65万円→74万円・住民税の基礎控除は改正なし・単身の非課税119万円)
#   https://www.city.chuo.lg.jp/a0009/kurashi/zeikin/juuminzei/r9kaisei.html
#  大阪府「令和8年度の主な税制改正の紹介」(74万円のうち5万円は令和9・10年度分だけ) https://www.pref.osaka.lg.jp/o050030/zei/alacarte/reiwa8_zeikai.html
#  国税庁「令和8年度税制改正(所得税の基礎控除の引上げ等関係)Q&A」(219万1,000円から220万円未満の表) https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf
#  国税庁「所得税のしくみ」(令和8年分の基礎控除 489万円以下104万円) https://www.nta.go.jp/publication/pamph/koho/kurashi/html/01_1.htm
#  協会けんぽ 令和7年度・令和8年度の都道府県単位保険料率(東京9.91%→9.85%・介護1.59%→1.62%・3月分から、支援金0.23%は4月分から)
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r07
#  協会けんぽ 令和8年10月分からの保険料額表(東京・厚生年金18.3%・50銭以下切捨て) https://www.kyoukaikenpo.or.jp/assets/R8.10_13%E6%9D%B1%E4%BA%AC.pdf
#  厚生労働省「令和8(2026)年度 雇用保険料率のご案内」(労働者負担 令和7年度5.5/1,000・令和8年度5/1,000) https://www.mhlw.go.jp/content/001692566.pdf
# 最後に原本を確かめた日:2026-11-20
# ページの前提:健康保険・介護・支援金は合わせて1回の50銭処理(furusato.py と同じ)。2026年1〜12月の各月の料率。
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, SITE

def kyuyo9(a):   # 令和8年分の給与所得(令和9年度の住民税)
    if a < 741000: return 0
    if a < 2191000: return a - 740000
    if a < 2193000: return 1451000
    if a < 2196000: return 1453000
    if a < 2200000: return 1456000
    if a < 6600000:
        A = a // 4000 * 4000
        return A * 7 // 10 - 80000 if a < 3600000 else A * 8 // 10 - 440000
    if a < 8500000: return a * 9 // 10 - 1100000
    return a - 1950000

def kyuyo8(a):   # 令和7年分の給与所得(令和8年度の住民税)。最低保障65万円
    if a < 651000: return 0
    if a < 1900000: return a - 650000
    if a < 6600000:
        A = a // 4000 * 4000
        return A * 7 // 10 - 80000 if a < 3600000 else A * 8 // 10 - 440000
    if a < 8500000: return a * 9 // 10 - 1100000
    return a - 1950000

LO = [63, 73, 83, 93, 101, 107, 114, 122, 130, 138, 146, 155, 165, 175, 185, 195, 210, 230, 250, 270, 290, 310, 330, 350, 370, 395,
      425, 455, 485, 515, 545, 575, 605, 635, 665, 695, 730, 770, 810, 855, 905, 955, 1005, 1055, 1115, 1175, 1235, 1295, 1355]
STD = [58, 68, 78, 88, 98, 104, 110, 118, 126, 134, 142, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380,
       410, 440, 470, 500, 530, 560, 590, 620, 650, 680, 710, 750, 790, 830, 880, 930, 980, 1030, 1090, 1150, 1210, 1270, 1330, 1390]
def hyojun(m):
    i = sum(1 for lo in LO if m >= lo * 1000)
    return STD[i] * 1000
def r50(v):
    v = F(v); q = v.numerator // v.denominator
    return q + 1 if v - q > F(1, 2) else q
def shaho(a, old):
    m = a // 12; s = hyojun(m); p = min(max(s, 88000), 650000); t = 0
    for k in range(1, 13):
        ken = F(991, 10000) if k <= 2 else F(985, 10000) if k == 3 else F(985 + 23, 10000)
        if old: ken += F(159, 10000) if k <= 2 else F(162, 10000)
        t += r50(s * ken / 2) + r50(p * F(183, 1000) / 2) + r50(m * (F(55, 10000) if k <= 3 else F(5, 1000)))
    return t

def jumin(a, sh):
    g = kyuyo9(a)
    if g <= 450000: return (0, 0, 0)                  # 均等割・所得割とも非課税(単身・1級地)
    kiso = 430000 if g <= 24000000 else 290000 if g <= 24500000 else 150000 if g <= 25000000 else 0
    t = max(0, g - sh - kiso) // 1000 * 1000
    if g > 25000000: c = 0
    elif t <= 2000000: c = min(50000, t)              # 人的控除額の差(単身は基礎控除の差5万円)
    else: c = max(50000 - (t - 2000000), 50000)
    ku = max(F(0), F(t) * 6 / 100 - F(c) * 3 / 100)
    to = max(F(0), F(t) * 4 / 100 - F(c) * 2 / 100)
    cap = g - 450000                                  # 附則3条の3の減額
    if ku + to > cap:
        ex = ku + to - cap
        ku, to = ku - ex * ku / (ku + to), to - ex * to / (ku + to)
    ku = int(ku) // 100 * 100; to = int(to) // 100 * 100
    return (ku + to + 5000, 5000, ku + to)

JS = '''([a,sh,old])=>{var q=function(i){return document.getElementById(i)};
 q("inc").value=String(a);q("inc").dispatchEvent(new Event("input",{bubbles:true}));
 var on=function(id,v){var b=document.querySelector("#"+id+' button[data-v="'+v+'"]');if(!b.classList.contains("on"))b.click();};
 on("s-sh",sh);if(sh)on("s-age",old);
 var n=function(i){return parseInt(q(i).textContent.replace(/[^0-9]/g,""),10)};
 var br=q("o-br").textContent.match(/均等割([0-9,]+)円・所得割([0-9,]+)円/);
 return {y:n("o-y"),m:n("o-m"),kin:br?parseInt(br[1].replace(/,/g,"")):0,sho:br?parseInt(br[2].replace(/,/g,"")):0,
  kk:q("o-kk").textContent,cap:q("t-cap").textContent,
  rows:[...document.querySelectorAll("#jtb tr")].map(function(tr){return [...tr.cells].map(function(c){return parseInt(c.textContent.replace(/[^0-9]/g,""),10)})}),
  hit:[...document.querySelectorAll("#jtb tr")].findIndex(function(tr){return tr.classList.contains("hit")})}}'''

def cases():
    v = [0, 500000, 740999, 741000, 741001, 1000000, 1100000, 1189999, 1190000, 1190001, 1191000, 1500000, 1780000, 2000000,
         2190999, 2191000, 2192999, 2193000, 2195999, 2196000, 2199999, 2200000, 2203999, 2204000, 3000000, 3599999, 3600000,
         3600001, 5000000, 6599999, 6600000, 6600001, 8499999, 8500000, 8500001, 10000000, 15000000, 20000000, 30000000, 50000000]
    v += list(range(1190000, 1260001, 1000)) + list(range(1190001, 1240000, 337))     # 附則3条の3の減額がかかる所
    for g in (24000000, 24500000, 25000000):           # 合計所得の境目
        for d in (-1, 0, 1, 1000):
            v.append(g + 1950000 + d)
    for lo in LO:                                      # 標準報酬月額の境目
        v += [lo * 12000 - 1, lo * 12000, lo * 12000 + 11, lo * 12000 + 12]
    return sorted(set(v))

def tax_t(a, sh):
    g = kyuyo9(a)
    return max(0, g - sh - 430000) // 1000 * 1000

def sakai_200(sh_on, old):
    """課税所得がちょうど200万円・その前後になる年収(社会保険料も年収で変わるので探す)。"""
    out = set()
    for T in (2000000, 2001000):
        lo, hi = 0, 6000000
        while lo < hi:
            mid = (lo + hi) // 2
            if tax_t(mid, shaho(mid, old) if sh_on else 0) >= T: hi = mid
            else: lo = mid + 1
        out |= {lo - 1, lo, lo + 1}
    return out

ROWS = [1000000, 1100000, 1190000, 1250000, 1300000, 1500000, 1780000, 2000000, 2500000, 3000000, 3500000, 4000000,
        4500000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000]

def max_inc(kyuyo, L):
    lo, hi = 0, 5000000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if kyuyo(mid) <= L: lo = mid
        else: hi = mid - 1
    return lo

async def body(pg):
    n = bad = 0
    def ng(*x):
        nonlocal bad; bad += 1; print('NG', *x)
    for sh_on, old in ((0, 0), (1, 0), (1, 1)):
        cs = set(cases()) | sakai_200(sh_on, old)
        for a in sorted(cs):
            sh = shaho(a, old) if sh_on else 0
            y, kin, sho = jumin(a, sh)
            got = await pg.evaluate(JS, [a, sh_on, old]); n += 1
            if y > 0:
                ok = (got['y'], got['m'], got['kin'], got['sho']) == (y, y // 12, kin, sho)
            else:
                ok = got['y'] == 0 and got['m'] == 0
            kk = '住民税はかかりません' if y == 0 else '均等割だけかかります' if sho == 0 else '住民税がかかります'
            if not ok or got['kk'] != kk:
                ng(a, sh_on, old, got['y'], got['kin'], got['sho'], got['kk'], '自分', y, kin, sho, kk)
        # 早見表の全部の行と黄色の行
        got = await pg.evaluate(JS, [3210000, sh_on, old])
        n += 1
        if [r[0] for r in got['rows']] != ROWS: ng('早見表の行', [r[0] for r in got['rows']])
        for r in got['rows']:
            s = shaho(r[0], old) if sh_on else 0
            y = jumin(r[0], s)[0]; n += 1
            if r[1:] != [s, y, y // 12]: ng('早見表', sh_on, old, r, [s, y, y // 12])
        n += 1
        if got['hit'] != ROWS.index(3000000): ng('黄色の行', got['hit'])
    # 非課税の年収の表(手書き)
    html = open(os.path.join(SITE, 'juminzei', 'index.html'), encoding='utf-8').read()
    def tbl(cap):
        i = html.index(cap); body_ = html[html.index('<tbody>', i):html.index('</tbody>', i)]
        return [[int(c.replace(',', '')) for c in re.findall(r'<td>([0-9,]+)</td>', tr)] for tr in body_.split('</tr>')[:-1]]
    for cap, add in (('均等割も所得割もかからない年収', 210000), ('所得割がかからない年収（均等割だけかかる）', 320000)):
        for k, row in enumerate(tbl(cap)):
            L = 350000 * (k + 1) + 100000 + (add if k else 0)
            exp = [max_inc(kyuyo8, L), max_inc(kyuyo9, L)]; n += 1
            if row != exp: ng(cap, k, row, exp)
    # 本文・FAQ・メタの数字
    single8, single9 = max_inc(kyuyo8, 450000), max_inc(kyuyo9, 450000)
    single11 = 450000 + 690000                       # 令和11年度(最低保障69万円)
    shotoku0 = 740000 + 1040000                      # 所得税がかからない上限(給与所得控除74万円+基礎控除104万円)
    y150 = jumin(1500000, 0)
    checks = [
        (single8 == 1100000 and single9 == 1190000, '単身の非課税 %d %d' % (single8, single9)),
        ('令和8年度110万円、令和9年度119万円' in html, 'メタの文'),
        ('<b>119<i>万円</i></b><em>去年は110万円</em>' in html, '大きい箱の119万円'),
        ('令和9年度から9万円上がって119万円' in html and single9 - single8 == 90000, '冒頭の9万円'),
        ('年収178万円で住民税は119万円なので、59万円の差' in html and shotoku0 == 1780000 and shotoku0 - single9 == 590000, '所得税と住民税の差'),
        ('年収119万円までかかりません' in html, '判定の文'),
        ('令和9年度は年35,500円です。均等割5,000円と所得割30,500円' in html and y150 == (35500, 5000, 30500), 'FAQ 150万円 %s' % (y150,)),
        ('令和11年度に住民税がかからない年収は単身で114万円' in html and single11 == 1140000, 'FAQ 令和11年度'),
        ('区民税3,000円・都民税1,000円・森林環境税1,000円の年5,000円' in html, '均等割'),
        ('多くの場合2,500円が引かれます' in html and jumin(3000000, 0)[2] == (2020000 - 430000) // 1000 * 100 - 2500, '調整控除2,500円'),
    ]
    for ok, msg in checks:
        n += 1
        if not ok: ng(msg)
    # JS が動く前の文字(既定 年収300万円・社会保険あり・40歳未満)
    y, kin, sho = jumin(3000000, shaho(3000000, 0))
    pre = re.search(r'id="o-y">([0-9,]+)<i>', html).group(1), re.search(r'id="o-m">([0-9,]+)<i>', html).group(1), \
          re.search(r'id="o-br">([^<]+)<', html).group(1)
    n += 1
    if pre != ('{:,}'.format(y), '{:,}'.format(y // 12), '内訳は、均等割{:,}円・所得割{:,}円です'.format(kin, sho)):
        ng('JSの前の文字', pre, y, kin, sho)
    return n, bad

run('juminzei', body)
