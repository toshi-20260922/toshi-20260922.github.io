# /koyohoken/ 雇用保険料の早見表。
# 原本:厚生労働省「令和8年度 雇用保険料率のご案内」(令和8年4月1日から令和9年3月31日まで・単位は1,000分の1)
#   https://www.mhlw.go.jp/content/001692566.pdf
#   一般の事業 労働者5・事業主8.5(うち二事業3.5)・合計13.5(令和7年度は5.5・9・14.5)
#   農林水産・清酒製造の事業 労働者6・事業主9.5(うち二事業3.5)・合計15.5(令和7年度は6.5・10・16.5)
#   建設の事業 労働者6・事業主10.5(うち二事業4.5)・合計16.5(令和7年度は6.5・11・17.5)
# 大阪労働局「労働保険料の計算方法」(賃金から源泉控除する被保険者負担分は50銭以下切り捨て・50銭1厘以上切り上げ。特約があればこの限りでない)
#   https://jsite.mhlw.go.jp/osaka-roudoukyoku/hourei_seido_tetsuzuki/roudou_hoken/hourei_seido/keisan.html
# 厚生労働省「雇用保険法等の一部を改正する法律(令和6年法律第26号)の概要」(週10時間以上への拡大・令和10年10月1日施行)
#   https://www.mhlw.go.jp/content/11600000/001255172.pdf
# 厚生労働省「労働保険年度更新に係るお知らせ」(令和8年度の年度更新期間は6月1日から7月10日)
#   https://www.mhlw.go.jp/bunya/roudoukijun/roudouhoken21/index.html
# 厚生労働省「雇用保険事務手続きの手引き 第4章 被保険者について」(週20時間以上・31日以上・役員・昼間学生・高年齢被保険者)
#   https://www.mhlw.go.jp/content/11600000/000637955.pdf
# 厚生労働省「雇用保険マルチジョブホルダー制度について」(65歳以上・1つの事業所で週5時間以上20時間未満・合計20時間以上・本人の申出)
#   https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000136389_00001.html
# 神奈川労働局「労働保険料の算定基礎となる賃金早見表」(賞与・通勤手当・超過勤務手当・家族手当は賃金総額に算入する)
#   https://jsite.mhlw.go.jp/kanagawa-roudoukyoku/hourei_seido_tetsuzuki/roudou_hoken/hourei_seido/rouho_hayami.html
# 大阪労働局「支払い賃金の確認」(通勤手当は非課税の部分も含めて賃金総額に算入する・賞与も算入する)
#   https://jsite.mhlw.go.jp/osaka-roudoukyoku/hourei_seido_tetsuzuki/roudou_hoken/hourei_seido/kosin/keizoku/kakunin.html
# 愛知労働局「高年齢労働者に係る雇用保険料免除措置の終了について」(令和2年4月1日からは高年齢労働者も納付が必要)
#   https://jsite.mhlw.go.jp/aichi-roudoukyoku/hourei_seido_tetsuzuki/roudou_hoken/koureiroudousyamenjo.html
# 青森労働局「令和8年度労働保険年度更新のお知らせ」(6月1日(月)から7月10日(金)まで)
#   https://jsite.mhlw.go.jp/aomori-roudoukyoku/newpage_01580.html
# 照らすもの(2026-11-21 に足したものは下の「2026-11-21」の行):結果の箱(本人負担・会社負担・合計・年間・料率・令和7年度の料率の額)・
#   JS が作る早見表の全行(56行×8列。1つの表に3つの事業を並べる形。一般の事業は本人・会社・合計、ほかの2つは本人・会社)を
#   3つの事業のボタンごとに・選んだ事業の列の太字・よく見る月給の小さい表(6行×4列)を3つの事業ごとに・
#   HTML に手で書いた料率の表と令和7年度との比較の表の全行・本文の例の数字・JS が書き換える前の元の文
# 2026-11-20:ほかのチャットが早見表を「選んだ事業だけ4列」から「3つの事業を並べた8列」に変え、小さい表を足した。
#   突き合わせが古かったので今の形に合わせた(ページの数字に誤りは無かった)。
# 会社負担の円未満切り捨てと年間の額(0.1万円の位に四捨五入)は、原本の決まりではなくページが注に書いている目安の出し方。その書き方どおりかを見る。
# 2026-11-21:足したもの。(1)早見表と小さい表を1つのセルごとに数える形(56行×8列×3つの事業)
#   (2)端数の境目を式から出して全部当てる形(賃金×料率の円未満がちょうど50銭になる賃金と、その1円下・1円上。
#      令和8年度の本人の料率と令和7年度の本人の料率の両方。低い・中くらい・高い・入力の上限の近く)
#   (3)会社負担の切り捨ての境目(ちょうど割り切れる賃金とその1円下) (4)手で計算した額との照らし(自分の式の確かめ)
#   (5)開いた直後の画面 (6)空の入力 (7)スライダーを3つの事業で (8)題名・説明の文
# 2026-11-21 に開けた原本:厚生労働省「令和8年度 雇用保険料率のご案内」(料率・期間・注記)・山形労働局「令和8年度の雇用保険料率について」・
#   大阪労働局「労働保険料の計算方法」(源泉控除は50銭以下切り捨て・50銭1厘以上切り上げ。現金で払う場合は50銭未満切り捨て・50銭以上切り上げ)・
#   青森労働局「令和8年度労働保険年度更新のお知らせ」(6月1日(月)〜7月10日(金))。ほかの原本は 2026-11-20 に確かめたまま。
# 最後に原本を確かめた日: 2026-11-21
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from _lib import run

F = Fraction
# (ボタンの番号, 名前, 令和8年度の労働者負担, 事業主負担, うち二事業, 令和7年度の労働者負担, 令和7年度の合計) 単位は1,000分の1
GEN = [
    (0, '一般の事業', F(5), F(17, 2), F(7, 2), F(11, 2), F(29, 2)),
    (1, '農林水産・清酒製造の事業', F(6), F(19, 2), F(7, 2), F(13, 2), F(33, 2)),
    (2, '建設の事業', F(6), F(21, 2), F(9, 2), F(13, 2), F(35, 2)),
]

def honnin(w, r):
    """賃金×料率。円未満は50銭以下切り捨て・50銭1厘以上切り上げ。"""
    x = F(w) * r / 1000
    q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q

def kaisha(w, r):
    x = F(w) * r / 1000
    return x.numerator // x.denominator

def sen(r):
    """1,000分の1の単位の料率の書き方(5・8.5 など)。"""
    return str(r.numerator) if r.denominator == 1 else '%d.%d' % (r.numerator * 10 // r.denominator // 10, r.numerator * 10 // r.denominator % 10)

def nenkan(tot):
    k = (tot * 12 + 500) // 1000            # 0.1万円の位に四捨五入
    return '年間 約%d%s万円' % (k // 10, '.%d' % (k % 10) if k % 10 else '')

def c(v):
    return '{:,}'.format(v)

def sakai(r, bases):
    """賃金×料率(1,000分の r)の円未満がちょうど50銭になる賃金を、bases のそれぞれの額以上でいちばん近い所から2つずつ探し、
    その1円下・ちょうど・1円上を返す。"""
    out = []
    for b in bases:
        w = b; k = 0
        while k < 2:
            x = F(w) * r / 1000
            if x - (x.numerator // x.denominator) == F(1, 2):
                out += [w - 1, w, w + 1]; k += 1
            w += 1
    return out

def wari(r, bases):
    """賃金×料率がちょうど割り切れる賃金(1円以上の額になる所)と、その1円下。会社負担の切り捨ての境目。"""
    out = []
    for b in bases:
        w = max(b, 1)
        while (F(w) * r / 1000).denominator != 1 or F(w) * r / 1000 < 1:
            w += 1
        out += [w - 1, w]
    return out

BASES = [1, 5000, 87654, 299000, 654321, 999000, 9990000]

MINI = [200000, 250000, 300000, 350000, 400000, 500000]      # よく見る月給の小さい表の行
SHORT = ['一般の事業', '農林水産・清酒製造', '建設の事業']      # 表の中の短い名前

def row8(v):
    """早見表の1行。給料の額・一般(本人・会社・合計)・農林水産/清酒製造(本人・会社)・建設(本人・会社)。"""
    r = [c(v)]
    for j, (_, _, me, co, _, _, _) in enumerate(GEN):
        a = honnin(v, me); b = kaisha(v, co)
        r += [c(a), c(b)] + ([c(a + b)] if j == 0 else [])
    return r

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, repr(got), repr(want))

    # 自分の式の確かめ。原本の料率から手で計算した額(式を通さずに書いた数字)
    for w, r, want in [(300000, F(5), 1500), (300000, F(6), 1800), (300100, F(5), 1500), (300101, F(5), 1501), (300300, F(5), 1501), (300301, F(5), 1502),
                       (250, F(6), 1), (251, F(6), 2), (249, F(6), 1), (100, F(5), 0), (101, F(5), 1), (1000, F(11, 2), 5), (1001, F(11, 2), 6),
                       (1000, F(13, 2), 6), (1001, F(13, 2), 7), (123456, F(5), 617), (123456, F(6), 741), (300000, F(11, 2), 1650), (300000, F(13, 2), 1950)]:
        chk('手計算 本人 %d %s' % (w, r), honnin(w, r), want)
    for w, r, want in [(300000, F(17, 2), 2550), (300000, F(19, 2), 2850), (300000, F(21, 2), 3150), (123456, F(17, 2), 1049), (123456, F(19, 2), 1172),
                       (123456, F(21, 2), 1296), (1999, F(17, 2), 16), (2000, F(17, 2), 17)]:
        chk('手計算 会社 %d %s' % (w, r), kaisha(w, r), want)
    # 端数の境目の賃金が式から出ているか(一般は100円+200円ごと・6/1,000は250円+500円ごと・令和7年度は1,000円+2,000円ごと)
    chk('境目 5', sakai(F(5), [1])[:6], [99, 100, 101, 299, 300, 301])
    chk('境目 6', sakai(F(6), [1])[:6], [249, 250, 251, 749, 750, 751])
    chk('境目 5.5', sakai(F(11, 2), [1])[:6], [999, 1000, 1001, 2999, 3000, 3001])
    chk('境目 6.5', sakai(F(13, 2), [1])[:6], [999, 1000, 1001, 2999, 3000, 3001])

    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'koyohoken', 'index.html'), encoding='utf-8').read()

    # 原本の表の中の足し算(労働者+事業主=合計・令和7年度は労使とも0.5ずつ高い)
    for _, name, me, co, ni, me7, tot7 in GEN:
        chk('原本 合計 ' + name, me + co, {'一般の事業': F(27, 2), '農林水産・清酒製造の事業': F(31, 2), '建設の事業': F(33, 2)}[name])
        chk('原本 令和7年度の合計 ' + name, me7 + (co + F(1, 2)), tot7)
        chk('原本 事業主=労働者+二事業 ' + name, me + ni, co)

    # HTML に手で書いた料率の表(#rate)の全行
    rows = await pg.eval_on_selector_all('#rate ~ .tw', "ws=>[...ws[0].querySelectorAll('tbody tr')].map(r=>[...r.children].map(td=>td.innerText.replace(/\\s+/g,' ').trim()))")
    chk('料率の表の行の数', len(rows), 3)
    for (_, name, me, co, ni, me7, tot7), r in zip(GEN, rows):
        chk('料率の表 ' + name, [x.replace(' ', '') for x in r],
            [name, sen(me), sen(co) + sen(ni), sen(me + co), sen(tot7)])

    # HTML に手で書いた令和7年度との比較の表(#change)の全行
    rows = await pg.eval_on_selector_all('#change ~ .tw', "ws=>[...ws[0].querySelectorAll('tbody tr')].map(r=>[...r.children].map(td=>td.innerText.replace(/\\s+/g,'')))")
    chk('比較の表の行の数', len(rows), 3)
    for (_, name, me, co, ni, me7, tot7), r in zip(GEN, rows):
        chk('比較の表 ' + name, r, [name, sen(me7), sen(me), '%s円→%s円' % (c(honnin(300000, me7)), c(honnin(300000, me)))])

    # JS が書き換える前の元の文(ファイルの中身)。既定は30万円・一般の事業
    g = GEN[0]; a = honnin(300000, g[2]); b = kaisha(300000, g[3])
    for label, want in [
        ('既定の給料', 'id="pay" inputmode="numeric" min="0" max="10000000" step="1000" value="300000"'),
        ('本人の料率', '<b id="o-rme">1,000分の%s</b>' % sen(g[2])),
        ('会社の料率', '<b id="o-rco">1,000分の%s</b>' % sen(g[3])),
        ('本人負担', '<b id="o-me">%s<i>円</i></b>' % c(a)),
        ('会社負担', '<b id="o-co">%s<i>円</i></b>' % c(b)),
        ('合計', '<b id="o-all">%s<i>円</i></b>' % c(a + b)),
        ('年間', '<em id="o-year">%s</em>' % nenkan(a + b)),
        ('料率の文', '<li id="o-rate">一般の事業の料率は、本人1,000分の%s・会社1,000分の%sです</li>' % (sen(g[2]), sen(g[3]))),
        ('令和7年度の文', '<li id="o-old">令和7年度の料率なら、本人負担は%s円でした</li>' % c(honnin(300000, g[5]))),
        ('表の題', '<p class="cap" id="t-cap">月額・単位は円（太字は一般の事業）</p>'),
        ('小さい表の題', '<p class="subh" id="mini-h">よく見る月給の早見表<span class="nw">（一般の事業・令和8年度）</span></p>'),
    ]:
        chk('元の文 ' + label, want in raw, True)

    # HTML に手で書いた小さい表(JS が書き換える前の元の行)。一般の事業の6行
    import re
    m = re.search(r'<tbody id="minib">(.*?)</tbody>', raw, re.S)
    rawmini = [re.findall(r'<td>(.*?)</td>', tr) for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', m.group(1), re.S)]
    chk('元の小さい表', rawmini, [[c(v), c(honnin(v, g[2])), c(kaisha(v, g[3])), c(honnin(v, g[2]) + kaisha(v, g[3]))] for v in MINI])
    chk('元の小さい表の黄色の行', re.findall(r'<tr class="hit"><td>(.*?)</td>', m.group(1)), ['300,000'])

    # 題名・説明の文(ファイルの中身)
    chk('題名', '<title>【雇用保険料の早見表】給料から引かれる額と会社負担は？料率【令和8年度】</title>' in raw, True)
    chk('題名と og:title', raw.count('【雇用保険料の早見表】給料から引かれる額と会社負担は？料率【令和8年度】'), 2)
    chk('説明の文', raw.count('content="厚生労働省が公表している令和8年度の雇用保険料率にもとづき、月給5万円から60万円までの本人負担と会社負担を早見表にしました。給料や賞与の額を入力すると、その月の雇用保険料を表示します。"'), 2)

    # 開いた直後の画面(何も押す前)。一般の事業・30万円
    chk('開いた直後 入力欄', ''.join(ch for ch in await pg.input_value('#pay') if ch.isdigit()), '300000')
    chk('開いた直後 ボタン', await pg.eval_on_selector_all('.seg button.on', 'bs=>bs.map(b=>b.dataset.t)'), ['0'])
    for sel_, want in [('#o-me', c(a) + '円'), ('#o-co', c(b) + '円'), ('#o-all', c(a + b) + '円'), ('#o-year', nenkan(a + b)),
                       ('#o-rme', '1,000分の5'), ('#o-rco', '1,000分の8.5'), ('#o-rk', '一般の事業'),
                       ('#o-old', '令和7年度の料率なら、本人負担は1,650円でした'), ('#t-cap', '月額・単位は円（太字は一般の事業）')]:
        chk('開いた直後 ' + sel_, await pg.inner_text(sel_), want)
    chk('開いた直後 早見表の行の数', await pg.eval_on_selector_all('#gtb tr', 'rs=>rs.length'), 56)
    chk('開いた直後 黄色の行', await pg.eval_on_selector_all('#gtb tr.hit', "rs=>rs.map(r=>r.children[0].textContent)"), ['300,000'])

    # 早見表の頭の行(3つの事業を並べる形)
    head = await pg.eval_on_selector_all('table.ky3 thead tr', "rs=>rs.map(r=>[...r.children].map(th=>th.textContent+'/'+(th.colSpan||1)))")
    chk('早見表の頭の行', head, [['給料の額/1', '一般の事業/3', '農林水産・清酒製造/2', '建設の事業/2'],
                              ['本人/1', '会社/1', '合計/1', '本人/1', '会社/1', '本人/1', '会社/1']])
    chk('小さい表の頭の行', await pg.eval_on_selector_all('table.kmini thead th', 'ts=>ts.map(t=>t.textContent)'),
        ['給料の額（円）', '本人負担（円）', '会社負担（円）', '合計（円）'])

    # 本文の例の数字
    flat = ''.join((await pg.inner_text('main')).split())
    g0 = GEN[0]
    for label, want in [
        ('冒頭 料率', '令和8年4月から、一般の事業の本人負担は1,000分の%s（%s%%）に下がりました。' % (sen(g0[2]), str(float(g0[2] / 10)))),
        ('冒頭 30万円', '月給30万円なら、本人負担は月%s円です。' % c(honnin(300000, g0[2]))),
        ('期間', '令和8年4月1日から令和9年3月31日までの料率です。'),
        ('下がった幅', '本人も会社も1,000分の%sずつ下がりました。' % '0.5'),
        ('賞与50万円', '賞与50万円なら、一般の事業の本人負担は%s円です。' % c(honnin(500000, g0[2]))),
        ('年度更新', '会社は毎年6月1日から7月10日までの間に、労働保険の年度更新をします。'),
        ('加入の条件', '1週間の決まった労働時間が20時間以上で、31日以上続けて働く（雇用される）見込みがある人'),
        ('マルチジョブ', '2つの会社でそれぞれ週5時間以上20時間未満働いて合計が週20時間以上になる65歳以上の人は、本人が申し出れば入れます。'),
        ('適用拡大', '令和10年10月から週の労働時間が10時間以上の人も入るようになります。'),
        ('端数の注', '本人負担の円未満の端数は50銭以下を切り捨て、50銭を超える場合は切り上げています。'),
        ('QA 何%', '本人負担が0.5%・会社負担が0.85%で合わせて1.35%です。'),
        ('QA 0.6%', '農林水産・清酒製造と建設の事業は、本人負担が0.6%です。'),
        ('QA 30万円', '一般の事業で、本人負担は月%s円・会社負担は月%s円です。令和7年度の料率では、本人負担は%s円でした。'
            % (c(honnin(300000, g0[2])), c(kaisha(300000, g0[3])), c(honnin(300000, g0[5])))),
        ('QA 8万円', '一般の事業で月%s円です。' % c(honnin(80000, g0[2]))),
        ('QA 会社負担', '令和8年度の一般の事業では、給料の1,000分の%sです。月給30万円なら会社負担は月%s円で、本人負担の%s円より多くなります。'
            % (sen(g0[3]), c(kaisha(300000, g0[3])), c(honnin(300000, g0[2])))),
        ('QA 賞与', '一般の事業で賞与50万円なら、本人負担は%s円です。' % c(honnin(500000, g0[2]))),
        ('表の説明', '下の表では月給5万円から60万円まで1万円ごとに3つの事業の種類を並べています。'),
        ('65歳以上', '65歳以上の人も条件にあえば入り、保険料もかかります。'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('%の換算', (g0[2] / 10, g0[3] / 10, (g0[2] + g0[3]) / 10, GEN[1][2] / 10, GEN[2][2] / 10),
        (F(1, 2), F(85, 100), F(135, 100), F(6, 10), F(6, 10)))

    def d(t):
        return int(''.join(ch for ch in t if ch.isdigit()) or 0)

    # 結果の箱。低い・中くらい・高いと、50銭の境目の前後(ちょうど・1円下・1円上)
    ws = [0, 1, 99, 100, 101, 199, 200, 249, 250, 251, 299, 300, 301, 999, 1000, 1001, 50000, 80000, 88000, 123456,
          181818, 181819, 300000, 300099, 300100, 300101, 300249, 300250, 300251, 301000, 333333, 500000, 654321,
          999999, 1000000, 1000100, 1000101, 2345678, 10000000, 10000250, 10000251]
    for t, name, me, co, ni, me7, tot7 in GEN:
        await pg.click('.seg button[data-t="%d"]' % t)
        chk('選ばれたボタン ' + name, await pg.eval_on_selector_all('.seg button.on', 'bs=>bs.map(b=>b.dataset.t)'), [str(t)])
        # 式から出した境目:本人負担(令和8年度と令和7年度の料率)がちょうど50銭になる賃金の前後・会社負担が割り切れる賃金とその1円下
        ws2 = sorted(set(ws + sakai(me, BASES) + sakai(me7, BASES) + wari(co, BASES)))
        chk('境目の賃金の数 ' + name, len(ws2) >= len(ws) + 60, True)
        for w in ws2:
            await pg.fill('#pay', str(w))
            a = honnin(w, me); b = kaisha(w, co)
            chk('箱 本人負担 %s %d' % (name, w), await pg.inner_text('#o-me'), c(a) + '円')
            chk('箱 会社負担 %s %d' % (name, w), await pg.inner_text('#o-co'), c(b) + '円')
            chk('箱 合計 %s %d' % (name, w), await pg.inner_text('#o-all'), c(a + b) + '円')
            chk('箱 年間 %s %d' % (name, w), await pg.inner_text('#o-year'), nenkan(a + b))
            chk('箱 令和7年度 %s %d' % (name, w), await pg.inner_text('#o-old'), '令和7年度の料率なら、本人負担は%s円でした' % c(honnin(w, me7)))
        chk('箱 本人の料率 ' + name, await pg.inner_text('#o-rme'), '1,000分の' + sen(me))
        chk('箱 会社の料率 ' + name, await pg.inner_text('#o-rco'), '1,000分の' + sen(co))
        chk('箱 事業の名前 ' + name, await pg.inner_text('#o-rk'), name)
        chk('箱 料率の文 ' + name, await pg.inner_text('#o-rate'), '%sの料率は、本人1,000分の%s・会社1,000分の%sです' % (name, sen(me), sen(co)))
        chk('早見表の題 ' + name, await pg.inner_text('#t-cap'), '月額・単位は円（太字は%s）' % name)

        # JS が作る早見表の全行(5万円から60万円まで1万円ごと)。どのボタンでも3つの事業が全部並ぶ
        await pg.fill('#pay', '300000')
        rows = await pg.eval_on_selector_all('#gtb tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
        want = [row8(v) for v in range(50000, 600001, 10000)]
        chk('早見表の行の数 ' + name, len(rows), 56)
        HEAD8 = ['給料の額', '一般 本人', '一般 会社', '一般 合計', '農林水産・清酒製造 本人', '農林水産・清酒製造 会社', '建設 本人', '建設 会社']
        for r, e in zip(rows, want):
            chk('早見表の列の数 %s %s' % (name, e[0]), len(r), 8)
            for h8, x, y in zip(HEAD8, r, e):
                chk('早見表 %s %s %s' % (name, e[0], h8), x, y)
        # 太字の列は選んだ事業の列だけ(一般は2〜4列目・農林水産/清酒製造は5〜6列目・建設は7〜8列目)
        sel = await pg.eval_on_selector_all('#gtb tr', "rs=>rs.map(r=>[...r.children].map((td,i)=>td.classList.contains('sel')?i:-1).filter(i=>i>=0).join(','))")
        chk('太字の列 ' + name, sorted(set(sel)), [['1,2,3', '4,5', '6,7'][t]])

        # よく見る月給の小さい表(選んだ事業の額に変わる)
        chk('小さい表の題 ' + name, ''.join((await pg.inner_text('#mini-h')).split()), 'よく見る月給の早見表（%s・令和8年度）' % SHORT[t])
        rows = await pg.eval_on_selector_all('#minib tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
        chk('小さい表の行の数 ' + name, len(rows), len(MINI))
        for r, v in zip(rows, MINI):
            chk('小さい表の列の数 %s %d' % (name, v), len(r), 4)
            for h4, x, y in zip(['給料の額', '本人負担', '会社負担', '合計'], r, [c(v), c(honnin(v, me)), c(kaisha(v, co)), c(honnin(v, me) + kaisha(v, co))]):
                chk('小さい表 %s %d %s' % (name, v, h4), x, y)
        # 空の入力は0円
        await pg.fill('#pay', '')
        chk('空の入力 本人負担 ' + name, await pg.inner_text('#o-me'), '0円')
        chk('空の入力 会社負担 ' + name, await pg.inner_text('#o-co'), '0円')
        chk('空の入力 合計 ' + name, await pg.inner_text('#o-all'), '0円')
        # スライダー(5,000円きざみ)。6/1,000 と 5.5・6.5/1,000 は 5,000円きざみでも端数が出ない額と出る額がある
        for w in (50000, 255000, 505000, 1000000):
            await pg.evaluate("v=>{var e=document.getElementById('payr');e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}", str(w))
            chk('スライダー 入力欄 %s %d' % (name, w), d(await pg.input_value('#pay')), w)
            chk('スライダー 本人負担 %s %d' % (name, w), await pg.inner_text('#o-me'), c(honnin(w, me)) + '円')
            chk('スライダー 会社負担 %s %d' % (name, w), await pg.inner_text('#o-co'), c(kaisha(w, co)) + '円')
            chk('スライダー 令和7年度 %s %d' % (name, w), await pg.inner_text('#o-old'), '令和7年度の料率なら、本人負担は%s円でした' % c(honnin(w, me7)))
        chk('小さい表の黄色の行 ' + name, await pg.eval_on_selector_all('#minib tr.hit', "rs=>rs.map(r=>r.children[0].textContent)"), ['300,000'])

        # 黄色の行(入れた額にいちばん近い1万円の行)
        for w, near in [(300000, '300,000'), (304999, '300,000'), (305000, '310,000'), (54999, '50,000'), (600000, '600,000'), (44999, None), (700000, None)]:
            await pg.fill('#pay', str(w))
            hit = await pg.eval_on_selector_all('#gtb tr.hit', "rs=>rs.map(r=>r.children[0].textContent)")
            chk('黄色の行 %s %d' % (name, w), hit, [near] if near else [])

    # スライダーを動かしたときも同じ計算になる
    await pg.click('.seg button[data-t="0"]')
    for w in (50000, 255000, 1000000):
        await pg.evaluate("v=>{var e=document.getElementById('payr');e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}", str(w))
        chk('スライダー 入力欄 %d' % w, d(await pg.input_value('#pay')), w)
        chk('スライダー 本人負担 %d' % w, await pg.inner_text('#o-me'), c(honnin(w, GEN[0][2])) + '円')
        chk('スライダー 会社負担 %d' % w, await pg.inner_text('#o-co'), c(kaisha(w, GEN[0][3])) + '円')

    # 余った </span> が無い
    chk('span の開きと閉じの数', raw.count('<span'), raw.count('</span>'))
    return n, bad

run('koyohoken', body)
