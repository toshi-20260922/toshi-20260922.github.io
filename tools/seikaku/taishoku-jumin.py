# /taishoku-jumin/ 退職後の住民税の計算(2025年の年収と2026年に辞める月から、令和8年度の残り・令和9年度の住民税・合計を出す)。
# 原本:
#  総務省「個人住民税」(所得割10%・非課税限度額の考え方) https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/149767_03.html
#  大田区「特別区民税・都民税（住民税）・森林環境税の計算のしくみ」(特別区民税6%・都民税4%・均等割 区3,000円+都1,000円+森林環境税1,000円・
#   課税所得1,000円未満切り捨て・税額100円未満切り捨て) https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/keisannosikumi.html
#  大田区「特別区民税・都民税（住民税）が課税されない方」(単身は合計所得45万円以下で均等割・所得割とも非課税)
#   https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/hikazei.html
#  大田区「令和8年度」(住民税の給与所得控除の最低保障65万円は令和8年度から・住民税の基礎控除と非課税の合計所得の基準は変わらない)
#   https://www.city.ota.tokyo.jp/seikatsu/zeikin/kaisei/r08_kaisei.html
#  大阪府「令和8年度の主な税制改正の紹介」(住民税の給与所得控除の最低保障74万円は令和9年度分から)
#   https://www.pref.osaka.lg.jp/o050030/zei/alacarte/reiwa8_zeikai.html
#  国税庁「令和8年度税制改正（所得税の基礎控除の引上げ等関係）Q&A」(74万円・219万1,000円から220万円未満の表)
#   https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf
#  江戸川区「所得控除」(住民税の基礎控除 43万・29万・15万・0円) https://www.city.edogawa.tokyo.jp/e013/kurashi/zeikin/juminzei/zei_gaiyo/shotokukojyo.html
#  練馬区「調整控除」(式・区3%と都2%・合計所得2,500万円超は無し・基礎控除の差は5万円)
#   https://www.city.nerima.tokyo.jp/kurashi/zei/jyuminzei/zeigakukojo/choseikojo.html
#  中央区「令和9年度から適用される個人住民税の主な改正」(給与所得控除の最低保障65万円→74万円・住民税の基礎控除は改正なし・単身の非課税は給与119万円以下)
#   https://www.city.chuo.lg.jp/a0009/kurashi/zeikin/juuminzei/r9kaisei.html
#  総務省「平成25年1月1日以降の退職所得に対する住民税の特別徴収について」(退職金の住民税は分離課税。区6%・都4%。退職所得は1,000円未満切り捨て・税額はそれぞれ100円未満切り捨て。
#   ページは「受け取るときに差し引かれるので含めていない」と書くだけで計算はしない) https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/65871.html
#  江東区「給与からの特別徴収」(1月1日から4月30日の異動は一括徴収が原則義務・6月1日から12月31日は本人の申し出で一括徴収) https://www.city.koto.lg.jp/060502/kurashi/zekin/kuminze/5111.html
#  目黒区「個人住民税の給与からの特別徴収」(6月から翌年5月の12回・新しい勤務先で続けるときは異動届出書を回付) https://www.city.meguro.tokyo.jp/zeimu/kurashi/juuminzei/kyuuyotokubetuchoushuu.html
#  中野区 納付方法の資料(普通徴収は6月・8月・10月・翌年1月の4回) https://www.city.tokyo-nakano.lg.jp/kurashi/zeikin/kakusyushiryo/minnanokuzei-r7.files/nouhuhouhou_r7.pdf
#  京都市「特別徴収の手引」(12分割・100円未満の端数は最初の月・均等割相当額以下は最初の月に全額)
#   https://www.city.kyoto.lg.jp/gyozai/cmsfiles/contents/0000085/85642/506_tebiki.pdf
#  京都府「事務の手引」(地方税法321条の5第2項:1月1日から4月30日の退職は申し出がなくても一括徴収・6月1日から12月31日は申し出で一括徴収・5月退職は最終月分)
#   https://www.pref.kyoto.jp/zeimu/documents/zimutebiki7_2.pdf
#  大阪市 特別徴収の案内(1月1日から4月30日は申し出に関係なく一括徴収。5月31日までの給与・退職手当等より残税額が多いときは普通徴収)
#   https://www.city.osaka.lg.jp/zaisei/cmsfiles/contents/0000076/76153/01_P1-8.pdf
#  協会けんぽ 令和7年度・令和8年度の保険料率(東京都 令和6年度9.98%・令和7年度9.91%・令和8年度9.85%はいずれも3月分から。子ども・子育て支援金0.23%は令和8年4月分から)
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r07
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  協会けんぽ 令和8年度 保険料額表(大阪府。等級表・厚生年金18.3%・50銭の端数処理) https://www.kyoukaikenpo.or.jp/~/media/Files/shared/hokenryouritu/r8/ippan/27osaka.pdf
#  厚生労働省 通知 T260216S0101(一般保険料率と支援金率を合算した率で計算し折半してから端数処理) https://www.mhlw.go.jp/hourei/doc/tsuchi/T260216S0101.pdf
#  雇用保険料率 労働者負担(一般の事業):令和6年度 6/1,000 https://www.mhlw.go.jp/content/001211914.pdf
#   令和7年度 5.5/1,000 https://jsite.mhlw.go.jp/yamagata-roudoukyoku/koyouhoken-20250213.html
#   令和8年度 5/1,000 https://jsite.mhlw.go.jp/tokyo-hellowork/list/tachikawa/kyushokusha/koyouhokenryouritu08.html
# 最後に原本を確かめた日:2026-11-20(本文を開いて確かめた日)
# 2026-11-21:係は原本の本文を開けなかった(web-fetch を呼べない)。検索結果に出た題名で確かめたのは次の4つだけ。
#  協会けんぽ「令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます」(題名は出典の文字と同じ)・協会けんぽ東京支部のお知らせ(健康保険料率9.85%)・
#  中央区「令和9年度から適用される個人住民税の主な改正」(題名)・東京労働局「令和8(2026)年度 雇用保険料率のご案内」(題名)。料率・控除額の数字は今日は取り直せていない。
# ページの前提:東京23区・単身・給与だけ・40歳未満・賞与なし。月給=2025年の年収÷12(円未満切り捨て)。2026年も同じ月給で、辞める月まで受け取る。
# 社会保険料は「その月分の料率」で1月分から(2026年は辞める月分まで)足す(ページに書いてある前提)。
import os, sys, random
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
import rates as zeiritsu

def kyuyo_r7(a):          # 令和7年分(令和8年度の住民税)の給与所得。最低保障65万円
    return zeiritsu.kyuyo_r7(a)

def kyuyo_r8(a):          # 令和8年分(令和9年度の住民税)の給与所得。最低保障74万円と特例の表
    return zeiritsu.kyuyo_r8(a)

# 健康保険の等級:(報酬月額の下限 千円, 標準報酬月額 千円)
GRADE = zeiritsu.tokyu_lower_std_sen()
def hyojun(m):
    s = 58
    for lo, v in GRADE:
        if m >= lo * 1000: s = v
    return s * 1000
def r50(v):
    q = v.numerator // v.denominator
    return q + 1 if v - q > F(1, 2) else q

def rates(year, k):
    """(健康保険+支援金の率, 雇用保険の本人の率) その年のk月分。"""
    if year == 2025:
        return (F(998, 10000) if k <= 2 else F(991, 10000)), (F(6, 1000) if k <= 3 else F(55, 10000))
    h = F(991, 10000) if k <= 2 else F(zeiritsu.TOKYO, 10000) if k == 3 else F(zeiritsu.TOKYO + zeiritsu.SIEN, 10000)
    return h, (F(55, 10000) if k <= 3 else F(zeiritsu.KOYO_PER_1000, 1000))

def shaho(m, year, n):
    s = hyojun(m); p = min(max(s, zeiritsu.NENKIN_MIN), zeiritsu.NENKIN_MAX); t = 0
    for k in range(1, n + 1):
        h, ko = rates(year, k)
        t += r50(F(s) * h / 2) + r50(F(p) * F(zeiritsu.NENKIN_PER_1000, 1000) / 2) + r50(F(m) * ko)
    return t

def kiso(g):
    return zeiritsu.kiso_jumin(g)

def jumin(g, sh):
    if g <= 450000: return 0                         # 単身の非課税(均等割・所得割とも)
    t = max(0, g - sh - kiso(g)) // 1000 * 1000
    if g > 25000000: c = 0
    elif t <= 2000000: c = min(50000, t)
    else: c = max(50000 - (t - 2000000), 50000)
    ku = max(0, t * 6 // 100 - c * 3 // 100) // 100 * 100     # 特別区民税 6%・調整控除3%
    to = max(0, t * 4 // 100 - c * 2 // 100) // 100 * 100     # 都民税 4%・調整控除2%
    return ku + to + 5000

def ref(a, m):
    mm = a // 12
    y8 = jumin(kyuyo_r7(a), shaho(mm, 2025, 12))
    if y8 <= 5000:                                   # 均等割相当額以下は最初の月(6月)に全額
        per, first = 0, y8
    else:
        per = y8 // 12 // 100 * 100; first = y8 - per * 11
    paid = first + per * (m - 6)
    a9 = mm * m
    y9 = jumin(kyuyo_r8(a9), shaho(mm, 2026, m))
    return {'y8': y8, 'paid': paid, 'rest': y8 - paid, 'n': 17 - m, 'a9': a9, 'y9': y9}

JS = '''([a,m])=>{var q=function(i){return document.getElementById(i)};
 var i=q("inc");i.value=String(a);i.dispatchEvent(new Event("input",{bubbles:true}));
 var s=q("mon");s.value=String(m);s.dispatchEvent(new Event("change",{bubbles:true}));
 var t=function(i){return q(i).textContent};
 return {a:t("o-a"),am:t("o-am"),b:t("o-b"),c:t("o-c"),o1:t("o-1"),o2:t("o-2"),cap:t("t-cap"),
  vd:t("o-vd"),vds:t("o-vds"),
  rows:[...document.querySelectorAll("#tb tr")].map(function(tr){return [tr.className,...[...tr.cells].map(function(c){return c.textContent})]})}}'''

def nums(s):
    import re
    return [int(x.replace(',', '')) for x in re.findall(r'[0-9][0-9,]*', s)]

def inputs():
    v = [0, 1, 650999, 651000, 1000000, 1099999, 1100000, 1100001, 1110000, 1190000, 1190001, 1300000, 1500000, 1899999,
         1900000, 2000000, 2500000, 3000000, 3599999, 3600000, 4000000, 4500000, 5000000, 5500000, 6000000, 6599999, 6600000,
         7000000, 8000000, 8499999, 8500000, 9000000, 10000000, 12000000, 15000000, 20000000, 30000000]
    for g in (24000000, 24500000, 25000000):          # 合計所得の境目(基礎控除・調整控除)
        for d in (-1, 0, 1, 12):
            v.append(g + 1950000 + d)
    for lo, _ in GRADE[1:]:                           # 標準報酬月額の等級の境目
        v += [lo * 12000 - 1, lo * 12000]
    # 課税所得200万円の前後(令和8年度)
    lo_, hi_ = 0, 30000000
    while lo_ < hi_:
        mid = (lo_ + hi_) // 2
        if kyuyo_r7(mid) - shaho(mid // 12, 2025, 12) - 430000 >= 2000000: hi_ = mid
        else: lo_ = mid + 1
    v += [lo_ - 12, lo_, lo_ + 12, lo_ + 1200]
    v += [50000000, 100000000]                        # 入力欄の max を超えた額でも頭打ちにならない
    return sorted(set(x for x in v if 0 <= x <= 100000000))

def check(got, a, m, tag):
    bad = 0
    e = ref(a, m)
    exp = {'a': e['rest'], 'am': e['n'], 'b': e['y9'], 'c': e['rest'] + e['y9']}
    for k, v in exp.items():
        if num(got[k]) != v:
            bad += 1; print('NG', tag, a, m, k, got[k], v)
    if nums(got['o1']) != [8, e['y8'], e['paid']]:
        bad += 1; print('NG', tag, a, m, 'o-1', got['o1'], e['y8'], e['paid'])
    if nums(got['o2']) != [9, 2026, e['a9']]:
        bad += 1; print('NG', tag, a, m, 'o-2', got['o2'], e['a9'])
    if got['vd'] != '退職後に払う住民税は合計{:,}円です'.format(e['rest'] + e['y9']) or got['vds'] != '令和8年度の残りと令和9年度の住民税の合計です':
        bad += 1; print('NG', tag, a, m, 'o-vd', got['vd'], got['vds'])
    if nums(got['cap']) != [2025, a, 23]:
        bad += 1; print('NG', tag, a, m, 't-cap', got['cap'])
    rows = got['rows']
    if [r[1] for r in rows] != ['%d月' % k for k in range(6, 13)]:
        bad += 1; print('NG 表の月', rows)
    for r in rows:
        k = int(r[1][:-1]); x = ref(a, k)
        if [num(r[2]), num(r[3]), num(r[4])] != [x['n'], x['rest'], x['y9']]:
            bad += 1; print('NG 表', a, k, r, x)
        if (r[0] == 'hit') != (k == m):
            bad += 1; print('NG 黄色の行', a, m, r)
    return 4 + 3 + 2 + 3 * len(rows) + len(rows), bad

async def body(pg):
    n = bad = 0
    # 既定の表示(年収500万円・9月)
    n0 = await pg.evaluate('''()=>({a:document.getElementById("inc").value,m:document.getElementById("mon").value})''')
    n += 1
    if n0 != {'a': '5000000', 'm': '9'}:
        bad += 1; print('NG 既定の入力', n0)
    for a in inputs():
        for m in range(6, 13):
            got = await pg.evaluate(JS, [a, m])
            c, b = check(got, a, m, '境目'); n += c; bad += b
    rnd = random.Random(20261120)
    for _ in range(400):
        a = rnd.choice([rnd.randrange(0, 3000000), rnd.randrange(0, 12000001), rnd.randrange(0, 30000001)])
        m = rnd.randrange(6, 13)
        got = await pg.evaluate(JS, [a, m])
        c, b = check(got, a, m, '乱数'); n += c; bad += b
    # 均等割だけの人(6月に全額)の例が入っていること
    n += 1
    if ref(1100001, 9)['y8'] != 5000 or ref(1100001, 9)['rest'] != 0:
        bad += 1; print('NG 均等割だけの例', ref(1100001, 9))
    # 年収別の表(#tb2。11-20 にほかのチャットが足した表):年額・毎月の額・9月と12月に辞めたときの残り
    t2 = await pg.evaluate('()=>[...document.querySelectorAll(":is(#nenshu ~ .tw):not(#nenshu ~ .tw ~ .tw) tbody tr")].map(tr=>[...tr.cells].map(c=>c.textContent))')
    th2 = await pg.evaluate('()=>[...document.querySelectorAll(":is(#nenshu ~ .tw):not(#nenshu ~ .tw ~ .tw) thead th")].map(c=>c.textContent)')
    n += 2
    if [r[0] for r in t2] != ['%s万円' % format(v, ',') for v in (200, 300, 400, 500, 600, 700, 800, 1000)]:
        bad += 1; print('NG 年収別の表の行', [r[0] for r in t2])
    if th2 != ['2025年の年収', '令和8年度の住民税（年・円）', '給料から毎月（円）', '9月に辞めたときの残り（円）', '12月に辞めたときの残り（円）']:
        bad += 1; print('NG 年収別の表の見出し', th2)
    for r in t2:
        a = num(r[0]) * 10000; s9 = ref(a, 9); s12 = ref(a, 12)
        per = 0 if s9['y8'] <= 5000 else s9['y8'] // 12 // 100 * 100
        exp = [s9['y8'], per, s9['rest'], s12['rest']]
        n += 5
        if [num(x) for x in r[1:]] != exp:
            bad += 1; print('NG 年収別の表', r, exp)
        if s9['rest'] != per * 8 or s12['rest'] != per * 5:      # 注記「毎月の額は7月から翌年5月の額」と残りの月数
            bad += 1; print('NG 年収別の表 残り=毎月×月数', r)
    # JS が書き換える前の元の文(HTML に直に書いた既定の結果)が、既定の入力(500万円・9月)の計算と同じ
    import re
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'taishoku-jumin', 'index.html'), encoding='utf-8').read()
    d = ref(5000000, 9)
    for name, pat in [
        ('o-vd', '<b id="o-vd">退職後に払う住民税は合計{:,}円です</b>'.format(d['rest'] + d['y9'])),
        ('o-a', '<b id="o-a">{:,}<i>円</i></b><em id="o-am">{}か月分</em>'.format(d['rest'], d['n'])),
        ('o-b', '<b id="o-b">{:,}<i>円</i></b>'.format(d['y9'])),
        ('o-c', '<b id="o-c">{:,}<i>円</i></b>'.format(d['rest'] + d['y9'])),
        ('o-1', '<li id="o-1">令和8年度の住民税は年{:,}円で、辞めるまでに給料から{:,}円引かれています</li>'.format(d['y8'], d['paid'])),
        ('o-2', '<li id="o-2">令和9年度は、2026年に辞めるまでの給与{:,}円で計算しています</li>'.format(d['a9'])),
        ('t-cap', '<p class="cap" id="t-cap">2025年の年収5,000,000円・東京23区・単身</p>'),
    ]:
        n += 1
        if pat not in src:
            bad += 1; print('NG 元の文(既定の結果)', name, pat)
    # 手で書いた文と数字
    txt = await pg.inner_text('main')
    head = await pg.evaluate('()=>document.title+"|"+document.querySelector("meta[name=description]").content')
    musts = [
        ('令和8年度' in head, 'title 令和8年度'),
        ('6月から翌年5月までの12か月' in txt, '12か月'),
        ('6月から12月に辞めた場合は' in txt, '6月から12月'),
        ('基礎控除43万円（合計所得2,400万円超は29万円・15万円・0円）' in txt, '基礎控除の文'),
        ('年額を12で割って100円未満を切り捨てた額で、端数は6月分に入ります' in txt, '12で割る文'),
        ('5,000円以下の人は6月分で全額' in txt, '均等割だけの文'),
        ('2025年は令和6・7年度、2026年は令和7・8年度の料率' in txt, '料率の年度'),
        ('1月から4月\t5月分までを最後の給料か退職金からまとめて引く（申し出がなくても引きます）' in txt, '1月から4月の行'),
        ('5月\t5月分をいつもどおり給料から引く' in txt, '5月の行'),
        ('6月から12月\t納付書で自分で払う（申し出れば最後の給料からまとめて引ける）' in txt, '6月から12月の行'),
        ('1月から4月に辞めた人は、5月分までを最後の給料か退職金からまとめて引かれます' in txt, 'FAQ 1月から4月'),
        ('給与所得控除の最低額が74万円に上がったあと' in txt, '74万円'),
        ('東京23区・単身・給与だけ' in txt, '地域の前提'),
        ('令和8年度税制改正（所得税の基礎控除の引上げ等関係）Q&A' in txt, '国税庁の出典の名前'),
        ('令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます' in txt, '協会けんぽの出典の名前'),
        ('総務省「個人住民税」' in txt, '総務省の出典の名前'),
        ('更新日：2026年11月21日' in txt, '更新日'),
        ('社会保険料は協会けんぽ東京都と一般の事業の雇用保険の料率で、40歳未満としています' in txt, '前提に料率の地域と年齢'),
        ('1月から5月' not in txt, '1月から5月が残っていない'),
        ('月給は2025年の年収を12で割った額で、賞与はないものとしています' in txt, '月給と賞与の前提'),
        ('毎月の額は7月から翌年5月の額です。6月は端数を足した額になります。' in txt, '年収別の表の注記'),
        ('退職金の住民税は受け取るときに差し引かれるので、翌年度の住民税には含まれません' in txt, 'FAQ 退職金'),
        ('協会けんぽ東京都・雇用保険は一般の事業・40歳未満です' in txt, '料率の地域'),
    ]
    for ok, name in musts:
        n += 1
        if not ok:
            bad += 1; print('NG 文', name)
    return n, bad

run('taishoku-jumin', body)
