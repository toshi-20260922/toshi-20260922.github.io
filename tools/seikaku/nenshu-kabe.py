# /nenshu-kabe/ 年収の壁の早見表と計算。
# 原本:国税庁 No.1410 給与所得控除(令和8・9年分は最低74万円・220万円まで一律。220万円未満の給与所得の表。令和7年分は65万円・190万円まで。令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
# 国税庁 No.1800 パート収入はいくらまで所得税がかからないか(74万円+基礎控除104万円=178万円・配偶者控除は収入136万円以下・令和7年分は160万円と123万円)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1800.htm
# 国税庁 No.1195 配偶者特別控除(配偶者の合計所得62万円超133万円以下・9つの段×本人の所得3つの段。令和7年分は58万円超)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1195.htm
# 国税庁 No.1177 特定親族特別控除(19歳以上23歳未満・合計所得62万円超123万円以下・給与だけなら197万円以下。令和7年分は188万円以下・9つの段)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1177.htm
# 国税庁「令和8年度税制改正(所得税の基礎控除の引上げ等関係)Q&A」(扶養親族等の所得要件58万円→62万円・令和8年12月1日施行で令和8年分から・ひとり親控除38万円は令和9年分から)
#   https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf
# 財務省「令和8年度税制改正の大綱」(基礎控除の本則62万円・特例加算は令和8・9年分が489万円以下42万円と655万円以下5万円・令和10年分以後は132万円以下37万円。
#   給与所得控除の本則69万円+令和8・9年の特例5万円。住民税の給与所得控除は69万円で令和9・10年度分は+5万円。勤労学生89万円)
#   https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2026/20251226taikou.pdf
# 総務省「令和8年度地方税制改正・地方税務行政の運営に当たっての留意事項等について」(令和8年1月21日 事務連絡。住民税の給与所得控除74万円は令和9年度分と令和10年度分・非課税限度額の改正は無し)
#   https://www.soumu.go.jp/main_content/001053325.pdf
# 総務省「令和8年度地方税制改正(案)について」 https://www.soumu.go.jp/main_content/001047636.pdf
# 住民税の非課税の基準(地方税法295条・附則3条の3):単身は所得割45万円以下(35万円+10万円)・均等割は1級地で45万円以下・ひとり親などは合計所得135万円以下
# 日本年金機構「2026(令和8)年10月に社会保険の短時間労働者に係る賃金要件が撤廃されました」(2026年10月1日・残る要件は週20時間以上・51人以上・学生でない)
#   https://www.nenkin.go.jp/oshirase/taisetu/jigyosho/2026/202610/100104.html
# 厚生労働省「短時間労働者の社会保険の加入拡大のポイント」(企業規模要件は2027年10月36人以上・2029年10月21人以上・2032年10月11人以上・2035年10月10人以下)
#   https://www.mhlw.go.jp/content/12500000/001633788.pdf
# 日本年金機構「従業員(健康保険・厚生年金保険の被保険者)が家族を被扶養者にするとき、被扶養者に異動があったときの手続き」(130万円未満・60歳以上と障害者は180万円未満・19歳以上23歳未満は150万円未満)
#   https://www.nenkin.go.jp/service/kounen/tekiyo/hihokensha1/20141202.html
# 日本年金機構「19歳以上23歳未満の方の被扶養者認定における年間収入要件が変わります」(令和7年10月1日から・配偶者を除く) https://www.nenkin.go.jp/oshirase/taisetu/2025/202508/0819.html
# 日本年金機構 年金Q&A(年齢はその年の12月31日で判定・23歳になる年から130万円未満) https://www.nenkin.go.jp/section/faq/kounen/dependents/aged19to22/timing.html
# 照らすもの:計算の箱(年収×働く人3つ。4つの判定と結論の文)・早見表の全行・結論の3つの数字・立場ごとの6枚の一覧と目盛りの位置・
#   配偶者特別控除の表の全行・178万円の式・基礎控除の表・給与所得控除の2つの表と図の折れ線・パートの表・本文とよくある質問の数字・出典の文字・id の重なり
# 2026-11-20 の直し(ページの誤り):所得税の判定を「178万円を超えたらかかる」から「課税所得が1,000円以上(年収178万1,000円以上)でかかる」に直した。
#   住民税の欄「令和9年度以降」→「令和9・10年度」。「201.6万円は正確には201万6千円」→「201万5,999円」。ひとり親控除の上限「678万円」→「677.7万円」(合計所得500万円は年収677万7,778円)。
# 申し送り:国税庁 No.1800 は配偶者特別控除を「136万円を超え207万円未満」と書く。No.1410 の表では年収207万円ちょうどの給与所得は133万円で、No.1195 の「133万円以下」に入る。ページは207万円以下のまま。
# 2026-11-21 の直し(ページの誤り):所得税の判定を178万1,000円以上から178万2,000円以上に直した(申し送りの形8。課税所得1,000円は所得税50円で、
#   復興特別所得税を足した51円は100円未満切り捨てで0円。税額が出るのは課税所得2,000円=年収178万2,000円から。/gakusei-kabe/ と同じ境目)。
#   計算の箱に直に書いた既定の結果が空だったので、既定(年収130万円・配偶者)の結果を HTML に書いた(形16・26)。
#   よくある質問「所得税がかかるのは178万円からです」→「年収178万円までは自分に所得税がかかりません」(178万円ちょうどはかからない。No.1800 は178万円以下)。
# 国税庁「暮らしの税情報 高齢者と税(年金と税)」(令和8年分・65歳以上の公的年金等控除は110万円) https://www.nta.go.jp/publication/pamph/koho/kurashi/html/03_1.htm
# 最後に原本を確かめた日:2026-11-21(国税庁 No.1800・No.1410・No.1195・No.1177・令和8年度税制改正Q&A・暮らしの税情報03_1・財務省 令和8年度税制改正の大綱の概要・
#   総務省 令和8年度地方税制改正(案)・日本年金機構 賃金要件の撤廃のリーフレット(100104.files/1.pdf)と被扶養者の手続き・厚生労働省 加入拡大のポイントと「年収の壁」への対応)
#   2026-11-21 に開けなかった原本(2026-11-20 に確かめたまま):財務省の大綱の PDF・総務省の留意事項(001053325.pdf)・総務省「個人住民税」・日本年金機構 100104.html と 0819.html と年金Q&A
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run
import rates
M = 10000

# ---- 原本の数字 ----
def shotoku8(x):
    """令和8・9年分の給与所得(No.1410)。"""
    return rates.kyuyo_r8(x)
def shotoku7(x):
    """令和7年分の給与所得(No.1410・別表第五は4,000円きざみ)。"""
    return rates.kyuyo_r7(x)
def kojo_shiki(x, r8):
    """給与所得控除の額(式どおり。早見表の式の列と年収ごとの表)。"""
    if x <= (2200000 if r8 else 1900000): return 740000 if r8 else 650000
    if x <= 3600000: return x * 3 // 10 + 80000
    if x <= 6600000: return x * 2 // 10 + 440000
    if x <= 8500000: return x // 10 + 1100000
    return 1950000
def kiso8(s):
    return rates.kiso_shotoku(s)
KISO7 = [(132, 95), (336, 88), (489, 68), (655, 63), (2350, 58)]
KISO8 = [(132, 104), (336, 104), (489, 104), (655, 67), (2350, 62)]
FUYO7, FUYO8 = 580000, 620000                       # 同一生計配偶者・扶養親族の所得要件
# No.1195:配偶者の合計所得の上限と控除額(本人900万円以下・950万円以下・1,000万円以下)
HAITOKU = [(95, 38, 26, 13), (100, 36, 24, 12), (105, 31, 21, 11), (110, 26, 18, 9), (115, 21, 14, 7),
           (120, 16, 11, 6), (125, 11, 8, 4), (130, 6, 4, 2), (133, 3, 2, 1)]
# No.1177:特定親族の合計所得の上限と控除額
TOKUTEI = [(85, 63), (90, 61), (95, 51), (100, 41), (105, 31), (110, 21), (115, 11), (120, 6), (123, 3)]
JUMIN_TANSHIN = 350000 + 100000                      # 単身の住民税の非課税の限度(所得)
JUMIN_HITORIOYA = 1350000
SHAHO = [1300000, 1500000, 1800000]                  # 配偶者・19〜22歳・60歳以上

def saidai(f, lim):
    """給与所得が lim 以下になる一番大きい年収。"""
    lo, hi = 0, 30000000
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if f(mid) <= lim: lo = mid
        else: hi = mid - 1
    return lo
def man1(v):
    """円→0.1万円の位に四捨五入した10倍の整数。"""
    return (v + 500) // 1000
def mstr(t):
    return '%d万円' % (t // 10) if t % 10 == 0 else '%d.%d万円' % (t // 10, t % 10)
def kabe(lim):
    return man1(saidai(shotoku7, lim)), man1(saidai(shotoku8, lim))

def tool(x, who):
    s = shotoku8(x)
    kz = max(0, s - kiso8(s)) // 1000 * 1000
    zei = kz * 5 // 100 * rates.FUKKO_NUM // rates.FUKKO_DEN // 100 * 100     # いちばん低い率5%・復興特別所得税2.1%・100円未満切り捨て(0円かどうかだけを見る)
    lim = SHAHO[who]
    si = x < lim
    ti = s <= FUYO8
    a = 0
    if ti:
        j3, j3e = '入れる', ['配偶者控除38万円', '扶養控除63万円', '扶養控除の対象'][who]
    else:
        if who == 0:
            a = next((r[1] for r in HAITOKU if s <= r[0] * M), 0)
        elif who == 1:
            a = next((r[1] for r in TOKUTEI if s <= r[0] * M), 0)
        if a:
            j3, j3e = '特別控除に', ('配偶者特別控除' if who == 0 else '特定親族特別控除') + '%d万円' % a
        else:
            j3, j3e = '外れる', '家族の控除なし'
    if not si:
        vd = ('社会保険の扶養から外れます', '年収が%d万円以上なので自分で社会保険に入ります。勤め先の社会保険に入らない場合は、国民年金と国民健康保険に加入します。' % (lim // M))
    elif ti:
        vd = ('扶養のままでいられます', '税金の扶養にも社会保険の扶養にも入れます')
    else:
        vd = ('社会保険の扶養には入れます', ('家族の控除は%s%d万円になります' % ('特定親族特別控除' if who else '配偶者特別控除', a)) if a else '家族の扶養控除は使えなくなります')
    return {'j1': 'かかる' if zei > 0 else 'かからない', 'j2': 'かかる' if s > JUMIN_TANSHIN else 'かからない',
            'j3': j3, 'j3e': j3e, 'j4': '入れる' if si else '外れる', 'j4e': '%d万円未満まで' % (lim // M),
            'o-vd': vd[0], 'o-vds': vd[1]}

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)

    # ---- 壁の金額(原本の数字から) ----
    zei7 = man1(saidai(lambda x: shotoku7(x) - 950000, 0)); zei8 = man1(saidai(lambda x: shotoku8(x) - kiso8(shotoku8(x)), 0))
    jm7, jm8 = kabe(JUMIN_TANSHIN)
    fy7 = man1(saidai(shotoku7, FUYO7)); fy8 = man1(saidai(shotoku8, FUYO8))
    hm7, hm8 = kabe(95 * M); hn7, hn8 = kabe(133 * M)
    tm7, tm8 = kabe(85 * M); tn7, tn8 = kabe(123 * M)
    ho7, ho8 = kabe(JUMIN_HITORIOYA)
    chk('壁の金額', [zei7, zei8, jm7, jm8, fy7, fy8, hm7, hm8, hn7, hn8, tm7, tm8, tn7, tn8, ho7, ho8],
        [1600, 1780, 1100, 1190, 1230, 1360, 1600, 1690, 2016, 2070, 1500, 1590, 1880, 1970, 2044, 2090])
    chk('正確な額', [saidai(shotoku7, 133 * M), saidai(shotoku7, JUMIN_HITORIOYA), saidai(shotoku8, 500 * M)], [2015999, 2043999, 6777778])

    # ---- 計算の箱 ----
    xs = {0, 1, 500000, 740999, 741000, 1000000, 1234567, 2190999, 2191000, 2199999, 2200000, 2500000, 3000000, 5000000, 6650000, 10000000}
    for b in [JUMIN_TANSHIN + 740000, FUYO8 + 740000, 1300000, 1500000, 1800000, 1780000, 1781000, 1782000] + \
             [r[0] * M + 740000 for r in HAITOKU] + [r[0] * M + 740000 for r in TOKUTEI]:
        xs |= {b - 1000, b - 1, b, b + 1, b + 999, b + 1000}
    ids = ['j1', 'j2', 'j3', 'j3e', 'j4', 'j4e', 'o-vd', 'o-vds']
    for who in (0, 1, 2):
        await pg.click('#s-who button[data-v="%d"]' % who)
        for x in sorted(xs):
            await pg.fill('#inc', str(x))
            got = await pg.evaluate('ids=>{var o={};ids.forEach(i=>o[i]=document.getElementById(i).textContent);return o}', ids)
            exp = tool(x, who)
            for k in ids:
                chk('箱 %d who%d %s' % (x, who, k), got[k], exp[k])
            chk('箱 %d who%d 色' % (x, who), await pg.get_attribute('#vd', 'class'), 'vd' if exp['j4'] == '外れる' else 'vd no')   # 外れるときだけ注意の色
    chk('税額が出る境目', (tool(1781999, 0)['j1'], tool(1782000, 0)['j1'], 1000 * 5 // 100 * rates.FUKKO_NUM // rates.FUKKO_DEN, 2000 * 5 // 100 * rates.FUKKO_NUM // rates.FUKKO_DEN), ('かからない', 'かかる', 51, 102))
    chk('箱の注 所得税', await pg.eval_on_selector_all('.jdg em', 'es=>es.slice(0,2).map(e=>e.textContent)'),
        [mstr(zei8) + 'まで0円', mstr(jm8) + 'まで0円（目安）'])
    chk('働く人の選択肢', await pg.eval_on_selector_all('#s-who button', 'bs=>bs.map(b=>b.textContent)'), ['配偶者', '19〜22歳の子', '60歳以上'])

    # ---- 早見表(全行) ----
    def up(a, b):
        return mstr(b - a) + '上がった'
    def row(a, b):
        return [mstr(a), mstr(b), up(a, b)]
    want = [row(zei7, zei8), row(jm7, jm8), row(fy7, fy8), row(hm7, hm8), row(hn7, hn8), row(fy7, fy8), row(tm7, tm8), row(tn7, tn8),
            row(ho7, ho8), row(fy7, fy8), ['106万円', 'なし', '撤廃'], ['130万円', '130万円', '変わらず'], ['150万円', '150万円', '変わらず'], ['180万円', '180万円', '変わらず']]
    rows = await pg.eval_on_selector_all('table.wl tbody tr:not(.g)', """rs=>rs.map(r=>[r.children[0].firstChild.textContent,
        r.children[1].textContent,r.children[2].firstChild.textContent,r.children[2].querySelector('small').textContent,r.children[0].textContent])""")
    names = ['所得税', '住民税（所得割）', '配偶者控除', '配偶者特別控除が満額', '配偶者特別控除がなくなる', '扶養控除', '19〜22歳の特定親族特別控除が満額',
             '19〜22歳の特定親族特別控除がなくなる', '住民税がかからない上限', '子の年収の上限', '106万円の壁', '家族の扶養（下の2つ以外）', '19〜22歳の扶養', '60歳以上・障害のある人の扶養']
    chk('早見表の行', [r[0] for r in rows], names)
    for r, w in zip(rows, want):
        chk('早見表 ' + r[0], r[1:4], w)
    chk('早見表 住民税の年度', '令和7年の欄は令和8年度の住民税で、令和8・9年の欄はそれぞれ令和9・10年度の住民税です。' in rows[1][4], True)
    chk('早見表 106万円の注', '2026年10月に賃金の要件がなくなった。従業員51人以上の会社で週20時間以上働く学生でない人は、勤め先の社会保険に入る' in rows[10][4], True)
    chk('早見表 配偶者を除く', '配偶者は除く' in rows[12][4], True)

    # ---- 結論の3つ ----
    chk('結論', await pg.eval_on_selector_all('.sum > .amt > div', "ds=>ds.map(d=>[d.querySelector('b').textContent,d.querySelector('em').textContent])"),
        [[mstr(zei8), '去年は' + mstr(zei7)], [mstr(fy8), '去年は' + mstr(fy7)], ['130万円', '変わらず']])

    # ---- 立場ごとの一覧と目盛り ----
    nenkin65 = 1100000 + 1040000                     # 65歳以上・年金だけ(公的年金等控除110万円+基礎控除104万円)
    hitori = saidai(shotoku8, 500 * M)
    P = {'p1': ([jm8, 1300, fy8, hm8, zei8, hn8], None), 'p2': ([jm8, fy8, 1500, tm8, zei8, tn8], None),
         'p3': ([1300, fy8, tm8, tn8], [1300, fy8, 1500, tm8, tn8]), 'p4': ([zei8, 1800, man1(nenkin65)], None),
         'p5': ([fy8, zei8, ho8, hitori // 1000], [fy8, zei8, ho8]), 'p6': ([jm7, jm8, zei8], None)}
    def pos(t):
        v = (t - 1000) * 10000 // 1200               # 100万円〜220万円を 0〜100% に。0.01% 単位
        v = (v + 5) // 10
        return '%d%%' % (v // 10) if v % 10 == 0 else '%d.%d%%' % (v // 10, v % 10)
    for pid, (dts, marks) in P.items():
        marks = marks or dts
        chk(pid + ' 金額', await pg.eval_on_selector_all('#%s dl.st dt' % pid, 'ds=>ds.map(d=>d.textContent)'), [mstr(t) for t in dts])
        got = await pg.eval_on_selector_all('#%s .ruler .m' % pid, "ms=>ms.map(m=>[m.textContent,m.style.left])")
        chk(pid + ' 目盛り', got, [[mstr(t)[:-2], pos(t)] for t in marks])
    dd = ''.join((await pg.inner_text('main')).split())
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'nenshu-kabe', 'index.html'), encoding='utf-8').read()
    for label, w in [
        ('p4 年金', '65歳以上で年金だけなら、所得税がかかり始める（公的年金等控除110万円＋基礎控除104万円）'),
        ('p5 住民税', 'ここまでなら令和9年度の住民税がかからない（合計所得135万円以下。令和8年度は204万3,999円まで）'),
        ('p5 ひとり親控除', 'ひとり親控除が使える上限（合計所得500万円以下）。令和9年分から控除額が35万円から38万円になる'),
        ('p2 23歳', '親の社会保険の扶養から外れる（23歳になる年からは130万円）'),
        ('p1 38万円', '配偶者控除から配偶者特別控除に変わる（控除額38万円は同じ）'),
    ]:
        chk('一覧の文 ' + label, w in raw, True)

    # ---- 配偶者特別控除の表(全行) ----
    rows = await pg.eval_on_selector_all(':is(#haigusha ~ .tw):not(#haigusha ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    lo = FUYO8
    want = []
    for r in HAITOKU:
        a = man1(saidai(shotoku8, lo)); b = man1(saidai(shotoku8, r[0] * M)); lo = r[0] * M
        want.append(['%s超 %s以下' % (mstr(a), mstr(b)), str(r[1]), str(r[2]), str(r[3])])
    chk('配偶者特別控除の表', rows, want)

    # ---- 178万円の式・基礎控除の表 ----
    chk('式', await pg.eval_on_selector_all('.eq b', 'bs=>bs.map(b=>b.textContent)'), ['74万', '104万', '%d万' % (zei8 // 10)])
    chk('式 令和7年', await pg.inner_text('p.was'), '令和7年分は 65万＋95万＝%d万円でした' % (zei7 // 10))
    chk('式の足し算', (74 + 104, 65 + 95), (zei8 // 10, zei7 // 10))
    rows = await pg.eval_on_selector_all('table.dd tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    want = []; prev = None
    for (top, k7), (_, k8) in zip(KISO7, KISO8):
        want.append([('%s万円以下' % '{:,}'.format(top)) if prev is None else '%s万円超〜%s万円以下' % ('{:,}'.format(prev), '{:,}'.format(top)), '%d万円' % k7, '%d万円' % k8]); prev = top
    want.append(['2,350万円超〜2,500万円以下', '48〜16万円', '48〜16万円'])
    chk('基礎控除の表', rows, want)
    chk('基礎控除 489万円の年収', (shotoku8(6650000) <= 4890000, shotoku8(6660000) > 4890000), (True, True))

    # ---- 給与所得控除の早見表 ----
    chk('控除のカード', await pg.eval_on_selector_all('.gk-cards > div', "ds=>ds.map(d=>d.textContent)"), ['控除の最低額65万円74万円', '一律で引ける年収190万円まで220万円まで', '年収220万円超変わらず'])
    chk('一律で引ける年収', (kojo_shiki(1900000, 0), kojo_shiki(1910000, 0) > 650000, kojo_shiki(2200000, 1), kojo_shiki(2210000, 1) > 740000, 2200000 * 3 // 10 + 80000), (650000, True, 740000, True, 740000))
    t = await pg.eval_on_selector_all('.gk-tw table.gk', "ts=>ts.map(t=>[...t.querySelectorAll('tbody tr')].map(r=>[...r.children].map(td=>td.textContent)))")
    chk('控除の式の表', t[0], [['190万円以下', '65万円', '74万円'], ['190万円超220万円以下', '収入×30％＋8万円', '74万円'],
        ['220万円超360万円以下', '収入×30％＋8万円', '収入×30％＋8万円'], ['360万円超660万円以下', '収入×20％＋44万円', '収入×20％＋44万円'],
        ['660万円超850万円以下', '収入×10％＋110万円', '収入×10％＋110万円'], ['850万円超', '195万円', '195万円']])
    want = []
    for y in (100, 150, 178, 200, 220, 300, 400, 500, 600, 700, 850, 1000):
        x = y * M
        want.append(['{:,}万円'.format(y), '%d万円' % (kojo_shiki(x, 0) // M), '%d万円' % (kojo_shiki(x, 1) // M), '%d万円' % ((x - kojo_shiki(x, 1)) // M)])
    chk('年収ごとの表', t[1], want)
    # 図の折れ線(横:年収100万円=40・1万円=1 縦:65万円=147.5・1万円=1.5)
    def pt(y, k):
        v = 1475 - (k - 65) * 15
        return '%d,%s' % (40 + y - 100, '%d' % (v // 10) if v % 10 == 0 else '%d.%d' % (v // 10, v % 10))
    lines = await pg.eval_on_selector_all('.gk-fig polyline', "ps=>ps.map(p=>p.getAttribute('points'))")
    chk('図 令和7年', lines[0], ' '.join(pt(y, kojo_shiki(y * M, 0) // M) for y in (100, 190, 360, 400)))
    chk('図 令和8年', lines[1], ' '.join(pt(y, kojo_shiki(y * M, 1) // M) for y in (100, 220, 360, 400)))

    # ---- パートの表 ----
    chk('パートの表', await pg.eval_on_selector_all('#emp + table tbody tr', "rs=>rs.map(r=>[...r.children].slice(1).map(td=>td.textContent))"),
        [[mstr(fy7), mstr(fy8)], ['130万円', '130万円']])

    # ---- 本文・よくある質問の数字 ----
    for label, w in [
        ('早見表の注', '表の201.6万円は正確には201万5,999円、204.4万円は204万3,999円を指します。'),
        ('要点', '自分に所得税がかかり始める年収は160万円から178万円に、配偶者控除・扶養控除を受けられる家族の年収は123万円から136万円になりました。'),
        ('130万円超136万円', '令和8年から130万円超〜136万円では、税金の扶養には入れるのに社会保険の扶養からは外れるようになりました。'),
        ('配特の前文', '配偶者の年収が136万円を超えても、207万円までは配偶者特別控除を受けられます。'),
        ('配特の注', '配偶者の年収136万円以下は配偶者控除です。本人の所得が900万円以下なら38万円です。本人の所得が1,000万円を超えると、どちらの控除も受けられません。年収は、給与所得控除74万円を引く前の金額です。'),
        ('上乗せ', '給与所得控除の74万円のうち5万円と基礎控除の104万円のうち42万円は、2年だけの特例です。'),
        ('令和10年', '令和10年分からは、基礎控除の上乗せを受けられるのは合計所得132万円以下の人だけになります。上乗せ額は37万円になります。'),
        ('489万円', '合計所得489万円は、給与だけならおよそ年収665万円です。'),
        ('控除の前文', '令和8年分から最低額が74万円に上がり、年収220万円までは一律で74万円を引けます。'),
        ('控除の注', '74万円のうち5万円は令和8年分と令和9年分だけの特例で、今の法律のままなら令和10年分から最低額は69万円になります。'),
        ('178万円の給与所得', '年収178万円の人は給与所得が104万円になり、基礎控除の104万円と同じ額なので所得税はかかりません。'),
        ('別表第五', '年収660万円未満の給与所得は、所得税法の別表第五で求めます。'),
        ('年度', '2026年に働いた分の所得税は令和8年分、住民税は令和9年度にかかります。'),
        ('51人', '2026年10月より、従業員51人以上の会社で週20時間以上働く人（学生を除く）は年収にかかわらず勤め先の社会保険に入ります。'),
        ('箱の注', '従業員51人以上の会社で週20時間以上働く人（学生を除く）は、年収にかかわらず勤め先の社会保険に入ります。'),
        ('質問 いくら', '収入が給与だけなら、年収178万円まで自分の所得税はかかりません。家族の税金の扶養に入れるのは136万円まで、社会保険の扶養に入れるのは130万円まで（19〜22歳は150万円・60歳以上は180万円）です。'),
        ('質問 配特', '令和8年分は、配偶者の年収（給与だけ）が207万円以下なら受けられます。169万円までは控除額が38万円です。そこから年収が増えるほど減り、207万円を超えるとなくなります。'),
        ('質問 学生', '19〜22歳なら、年収150万円未満は親の社会保険の扶養に入ったままです。親の税金の控除（特定親族特別控除）も、令和8年分は子の年収159万円まで満額の63万円です。年収が150万円以上になると、社会保険の扶養から外れます。'),
        ('質問 106万円', '賃金の要件（月8万8千円以上）は2026年10月になくなりました。'),
        ('質問 住民税', '令和8年に働いた分の住民税は、令和9年6月から払います。'),
        ('質問 級地', 'この表の110万円・119万円は、東京23区などの1級地の目安です。'),
        ('関連 62万円', '給与・年金・事業の収入から、扶養の62万円に入るかが分かります。'),
        ('結論の注', '社会保険は19〜22歳が150万円・60歳以上が180万円です'),
        ('更新日', '更新日：2026年11月23日（令和8年度税制改正に対応）'),
    ]:
        chk('本文 ' + label, ''.join(w.split()) in dd, True)
    chk('本文の数字と原本', (mstr(hm8), mstr(hn8), mstr(tm8), TOKUTEI[0][1], HAITOKU[0][1], 88000 * 12 // M, 1040000 - 620000, 740000 - 690000, 620000 + 370000),
        ('169万円', '207万円', '159万円', 63, 38, 105, 420000, 50000, 990000))

    # ---- 出典の文字・id の重なり・目次 ----
    links = dict(await pg.eval_on_selector_all('.src a', "as=>as.map(a=>[a.getAttribute('href'),a.textContent])"))
    for href, w in [
        ('https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2026/20251226taikou.pdf', '財務省「令和8年度税制改正の大綱」'),
        ('https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf', '国税庁「令和8年度税制改正（所得税の基礎控除の引上げ等関係）Q&A」'),
        ('https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1195.htm', '国税庁 タックスアンサー No.1195'),
        ('https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1177.htm', 'No.1177'),
        ('https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm', '国税庁 タックスアンサー No.1410 給与所得控除'),
        ('https://www.nenkin.go.jp/oshirase/taisetu/jigyosho/2026/202610/100104.html', '日本年金機構「2026（令和8）年10月に社会保険の短時間労働者に係る賃金要件が撤廃されました」'),
        ('https://www.nenkin.go.jp/service/kounen/tekiyo/hihokensha1/20141202.html', '日本年金機構「従業員（健康保険・厚生年金保険の被保険者）が家族を被扶養者にするとき、被扶養者に異動があったときの手続き」'),
        ('https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html', '総務省「個人住民税」'),
    ]:
        chk('出典 ' + href[-24:], links.get(href), w)
    chk('出典の数', len(links), 8)
    ids_all = await pg.eval_on_selector_all('[id]', 'es=>es.map(e=>e.id)')
    chk('id の重なり', sorted(set(i for i in ids_all if ids_all.count(i) > 1)), [])
    chk('目次の行き先', await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>{var e=document.getElementById(a.getAttribute('href').slice(1));return !!e&&e.tagName==='H2'})"), [True] * 8)
    # JS が書き換える前の既定(年収130万円・配偶者)
    chk('元の既定', ('id="inc" inputmode="numeric" min="0" max="10000000" step="1000" value="1300000"' in raw, '<button type="button" class="on" data-v="0">配偶者</button>' in raw), (True, True))
    # 計算の箱に直に書いた既定の結果(JS が書き換える前の HTML)
    d = tool(1300000, 0)
    for k in ids:
        chk('元の結果 ' + k, ('id="%s">%s<' % (k, d[k])) in raw, True)
    chk('元の結果 色', '<div class="vd" id="vd">' in raw, d['j4'] == '外れる')
    # ---- まとめのパネル(税金の壁・社会保険の壁のタブ) ----
    chk('パネルの3つ', await pg.eval_on_selector_all('.kp-k li', "ls=>ls.map(l=>[l.querySelector('span').textContent,l.querySelector('b').textContent])"),
        [['自分に所得税がかかり始める', mstr(zei8)], ['家族の扶養に入れる上限', mstr(fy8)], ['社会保険の扶養から外れる', '130万円']])
    kp = await pg.eval_on_selector_all('.kp-p', "ps=>ps.map(p=>[...p.querySelectorAll('.kp-r')].map(r=>[...r.children].map(c=>c.textContent)))")
    chk('パネル 税金', kp[0], [['所得税（本人）', mstr(zei7), mstr(zei8)], ['住民税（所得割）', mstr(jm7), mstr(jm8)], ['配偶者控除', mstr(fy7), mstr(fy8)],
        ['配偶者特別控除が満額', mstr(hm7), mstr(hm8)], ['扶養控除', mstr(fy7), mstr(fy8)], ['19〜22歳の特定親族特別控除が満額', mstr(tm7), mstr(tm8)]])
    chk('パネル 社会保険', kp[1], [['106万円の壁', '106万円', 'なし撤廃'], ['家族の扶養（下の2つ以外）', '130万円', '130万円変わらず'],
        ['19〜22歳の扶養', '150万円', '150万円変わらず'], ['60歳以上・障害のある人の扶養', '180万円', '180万円変わらず']])
    chk('パネルの見出し', await pg.eval_on_selector_all('.kp-hd', "hs=>hs.map(h=>[...h.children].map(c=>c.textContent))"), [['年収の壁', '令和7年', '令和8・9年']] * 2)
    chk('パネルの注', '住民税は単身・1級地の目安で、左は令和8年度・右は令和9・10年度の住民税です。' in raw, True)
    return n, bad
run('nenshu-kabe', body)
