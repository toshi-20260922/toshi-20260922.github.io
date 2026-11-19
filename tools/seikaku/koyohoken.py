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
# 照らすもの:結果の箱(本人負担・会社負担・合計・年間・料率・令和7年度の料率の額)・JS が作る早見表の全行(3つの事業×56行)・
#   HTML に手で書いた料率の表と令和7年度との比較の表の全行・本文の例の数字・JS が書き換える前の元の文
# 会社負担の円未満切り捨てと年間の額(0.1万円の位に四捨五入)は、原本の決まりではなくページが注に書いている目安の出し方。その書き方どおりかを見る。
# 最後に原本を確かめた日:2026-11-19
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

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, repr(got), repr(want))

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
        ('表の題', '<p class="cap" id="t-cap">一般の事業・月額</p>'),
    ]:
        chk('元の文 ' + label, want in raw, True)

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
        ('加入の条件', '1週間の決まった労働時間が20時間以上で31日以上続けて雇う見込みがある人'),
        ('マルチジョブ', '2つの会社でそれぞれ週5時間以上20時間未満働いて合計が週20時間以上になる65歳以上の人は、本人が申し出れば入れます。'),
        ('適用拡大', '令和10年10月から週の労働時間が10時間以上の人も入るようになります。'),
        ('端数の注', '本人負担は円未満の50銭以下を切り捨て、50銭を超えると切り上げています。'),
        ('QA 何%', '本人負担が0.5%・会社負担が0.85%で合わせて1.35%です。'),
        ('QA 0.6%', '農林水産・清酒製造と建設の事業は、本人負担が0.6%です。'),
        ('QA 30万円', '一般の事業で、本人負担は月%s円・会社負担は月%s円です。令和7年度の料率では、本人負担は%s円でした。'
            % (c(honnin(300000, g0[2])), c(kaisha(300000, g0[3])), c(honnin(300000, g0[5])))),
        ('QA 8万円', '一般の事業で月%s円です。' % c(honnin(80000, g0[2]))),
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
        for w in ws:
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
        chk('早見表の題 ' + name, await pg.inner_text('#t-cap'), name + '・月額')

        # JS が作る早見表の全行(5万円から60万円まで1万円ごと)
        await pg.fill('#pay', '300000')
        rows = await pg.eval_on_selector_all('#gtb tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
        want = [[c(v), c(honnin(v, me)), c(kaisha(v, co)), c(honnin(v, me) + kaisha(v, co))] for v in range(50000, 600001, 10000)]
        chk('早見表の行の数 ' + name, len(rows), 56)
        for r, e in zip(rows, want):
            chk('早見表 %s %s' % (name, e[0]), r, e)

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
