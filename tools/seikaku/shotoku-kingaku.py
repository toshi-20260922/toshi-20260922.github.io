# /shotoku-kingaku/ 所得金額の計算(収入から合計所得金額を出す)。
# 原本:国税庁 No.1410 給与所得控除(令和8年分・令和9年分は220万円まで74万円。69万1,000円以上220万円未満の給与所得の表。
#   660万円未満は所得税法別表第五・660万円以上850万円未満は収入×90%−110万円・850万円以上は収入−195万円。令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
# 国税庁「源泉所得税の改正のあらまし(令和8年4月)」(最低保障額65万円→74万円は令和8・9年分。令和10年分以後は69万円。
#   扶養親族等62万円以下=給与136万円以下・特定親族62万円超123万円以下=197万円以下・配偶者特別控除133万円以下=207万円以下・勤労学生89万円以下=163万円以下。
#   基礎控除:合計所得489万円以下=給与665万5,556円以下は104万円・655万円以下67万円・2,350万円以下62万円)
#   https://www.nta.go.jp/publication/pamph/gensen/2026kaisei.pdf
# 国税庁「令和8年分 年末調整のしかた」年末調整等のための給与所得控除後の給与等の金額の表(741,000円未満は0円・2,191,000円未満は収入−74万円・
#   2,191,000〜2,193,000円は1,451,000円・〜2,196,000円は1,453,000円・〜2,200,000円は1,456,000円・2,200,000円から4,000円きざみ・
#   3,596,000円→2,437,200円・3,600,000円→2,440,000円・6,596,000円→4,836,800円・660万円以上は1円未満切り捨て)
#   https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/114.pdf
# 国税庁 No.1411 所得金額調整控除(給与と年金:給与所得控除後の給与等の金額(10万円超は10万円)+公的年金等に係る雑所得の金額(同)−10万円。
#   年収850万円超で23歳未満の扶養親族などがいる場合の控除はページの計算に含めていない。措法41の3の11) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1411.htm
# 国税庁「暮らしの税情報(令和8年度版)高齢者と税(年金と税)」(公的年金等に係る雑所得の速算表・65歳以上は昭和37年1月1日以前生まれ)
#   https://www.nta.go.jp/publication/pamph/koho/kurashi/html/03_1.htm
# 国税庁 No.1600 公的年金等の課税関係(令和8年4月1日現在法令等。年金以外の合計所得金額1,000万円超・2,000万円超の表は図で載っている)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1600.htm
# 国税庁 No.1199 基礎控除(2,350万円超48万円・2,400万円超32万円・2,450万円超16万円・2,500万円超0円) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
# 国税庁 No.2072 青色申告特別控除(10万円・55万円・65万円。黒字の額が上限。令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2072.htm
# 東京都中央区「令和9年度から適用される個人住民税の主な改正」・浜松市「令和9年度税制改正について」(住民税も令和9年度から扶養親族・同一生計配偶者は62万円以下・基礎控除は改正なし)
#   https://www.city.chuo.lg.jp/a0009/kurashi/zeikin/juuminzei/r9kaisei.html https://www.city.hamamatsu.shizuoka.jp/shiminze/zei/siminze/zeiseikaisei_r9.html
# 照らすもの:window.__sk(給与・年金・事業・雑・一時)・結果の箱の文・給与の早見表の全行・年金の早見表の全行・合計所得金額で決まることの表の全行・
#   控除額の式の表の全行・本文とよくある質問の数字・出典の文字・id の重なり
# 2026-11-20 の直し(ページの誤り):住民税の扶養の所得要件「58万円以下のまま」→ 令和9年度分から62万円以下。「年収190万円以下…74万円」→220万円以下。
#   「年収660万円未満は4,000円きざみ」→220万円以上660万円未満。措法41条の3の3→41条の3の11。出典の文字(あらまし)と開けない出典(箕面市・税額表等)の差し替え。
# 最後に原本を確かめた日:2026-11-20
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run
MAN = 10000

def kyuyo(x):
    """別表第五の手順。660万円未満は表・660万円以上は式(1円未満切り捨て)。"""
    if x < 741000: return 0
    if x < 2191000: return x - 740000
    if x < 2193000: return 1451000
    if x < 2196000: return 1453000
    if x < 2200000: return 1456000
    if x < 6600000:
        a = x // 4000 * 4000                       # 表の行の「以上」の額
        if a < 3600000: return a - (a * 30 // 100 + 80000)         # 行の額−(行の額×30%+8万円)
        return a - (a * 20 // 100 + 440000)
    if x < 8500000: return x * 90 // 100 - 1100000
    return x - 1950000

def kojo_shiki(x):
    """No.1410 の控除額の表(式)。"""
    if x <= 2200000: return 740000
    if x <= 3600000: return x * 30 // 100 + 80000
    if x <= 6600000: return x * 20 // 100 + 440000
    if x <= 8500000: return x * 10 // 100 + 1100000
    return 1950000

def nenkin(y, old, other):
    if y <= 0: return 0
    add = 0 if other <= 1000 * MAN else (100000 if other <= 2000 * MAN else 200000)
    if old and y < 330 * MAN: v = y - 110 * MAN
    elif not old and y < 130 * MAN: v = y - 60 * MAN
    elif y < 410 * MAN: v = y * 75 // 100 - 275000
    elif y < 770 * MAN: v = y * 85 // 100 - 685000
    elif y < 1000 * MAN: v = y * 95 // 100 - 1455000
    else: v = y - 1955000
    return max(0, v + add)

def kiso(t):
    for top, v in [(489, 104), (655, 67), (2350, 62), (2400, 48), (2450, 32), (2500, 16)]:
        if t <= top * MAN: return v * MAN
    return 0

AO = [0, 100000, 550000, 650000]
def ref(q, y, old, js, je, ao, zi, ze, ii, ie):
    g = kyuyo(q)
    rieki = js - je
    jig = rieki - min(AO[ao], max(0, rieki))        # 青色申告特別控除は黒字の額まで
    zo = zi - ze
    ichi = max(0, ii - ie - 500000)                 # 一時所得(特別控除50万円のあと)
    other = g + jig + max(0, zo) + ichi // 2
    p = nenkin(y, old, other)
    adj = max(0, min(g, 100000) + min(p, 100000) - 100000) if (g > 0 and p > 0) else 0
    g2 = g - adj
    zat = max(0, p + zo)                            # 雑所得の赤字はほかの所得から引けない
    keijo = g2 + jig + zat
    tot = keijo + ichi // 2 if keijo >= 0 else max(0, ichi + keijo) // 2   # 赤字は一時所得(2分の1にする前)から引く
    return {'g': g2, 'adj': adj, 'p': p, 'jig': jig, 'zat': zat, 'ichi': ichi, 'tot': tot}

def yen(v): return '{:,}'.format(v)

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)
    async def sk(*a):
        return await pg.evaluate('a=>window.__sk.apply(null,a)', list(a))

    # 1 給与だけ:境目の前後と、4,000円きざみの行の端・2,000万円まで
    qs = set([0, 1, 690999, 691000, 740999, 741000, 741001, 1360000, 1630000, 1970000, 2070000, 6655556, 6655557,
              11950000, 11950001, 20000000, 20000001, 25450000, 100000000])
    for b in (2191000, 2193000, 2196000, 2200000, 2204000, 3596000, 3600000, 3604000, 6596000, 6600000, 8500000):
        qs.update([b - 1001, b - 1000, b - 1, b, b + 1, b + 3999, b + 4000])
    qs.update(range(0, 20000001, 37000)); qs.update(range(2180000, 2212000, 500)); qs.update(range(6590000, 6610000, 333))
    for q in sorted(qs):
        got = await sk(q, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        chk('給与 %d' % q, (got['g'], got['tot']), (kyuyo(q), kyuyo(q)))
    # 表の行の額では、表の額=行の額−式の控除額(No.1410 の式と別表第五が同じ額になること)
    for a in list(range(2200000, 6600000, 4000)) + [6600000, 7000000, 8500000, 9000000, 20000000]:
        chk('式と表 %d' % a, kyuyo(a), a - kojo_shiki(a))

    # 2 年金:65歳未満・65歳以上・ほかの所得3つの段
    ys = [0, 1, 600000, 600001, 1100000, 1100001, 1220000, 1220001, 1299999, 1300000, 1300001, 1720000, 1720001, 3299999, 3300000,
          4099999, 4100000, 4100001, 7699999, 7700000, 9999999, 10000000, 15000000]
    for old in (0, 1):
        for y in ys:
            for q in (0, 11950000, 11950001, 21950000, 21950001):
                got = await sk(q, y, old, 0, 0, 0, 0, 0, 0, 0)
                e = ref(q, y, old, 0, 0, 0, 0, 0, 0, 0)
                chk('年金 %d %d %d' % (y, old, q), got, e)
    # 3 組み合わせ(所得金額調整控除・事業の赤字・青色の上限・雑所得の赤字・一時所得)
    cases = []
    for q in (0, 800000, 840000, 841000, 1300000, 5000000, 9000000):
        for y, old in ((0, 0), (650000, 0), (700000, 0), (1150000, 1), (1200000, 1), (2500000, 1)):
            for js, je, ao in ((0, 0, 0), (3000000, 1000000, 3), (1000000, 600000, 2), (1000000, 950000, 1), (500000, 2000000, 3), (0, 9000000, 0)):
                for zi, ze in ((0, 0), (300000, 100000), (100000, 400000)):
                    for ii, ie in ((0, 0), (2000000, 1000000), (600000, 99999), (5000001, 0)):
                        cases.append((q, y, old, js, je, ao, zi, ze, ii, ie))
    for c in cases:
        chk('組み合わせ %s' % (c,), await sk(*c), ref(*c))

    # 4 結果の箱(入力欄に入れて文を読む)
    async def box(q=0, y=0, old=0, js=0, je=0, ao=0, zi=0, ze=0, ii=0, ie=0):
        for i, v in (('q', q), ('y', y), ('js', js), ('je', je), ('zi', zi), ('ze', ze), ('ii', ii), ('ie', ie)):
            await pg.fill('#' + i, str(v))
        await pg.select_option('#ao', str(ao))
        await pg.click('#s-old button[data-v="%d"]' % old)
        return ref(q, y, old, js, je, ao, zi, ze, ii, ie)
    chk('既定の入力', (await pg.input_value('#q')).replace(',', ''), '1300000')
    chk('既定の合計所得金額', await pg.inner_text('#o-t'), yen(kyuyo(1300000)) + '円')
    boxes = [dict(q=1360000), dict(q=1360001), dict(q=1361000), dict(q=1630000), dict(q=1631000), dict(q=1970000), dict(q=1971000),
             dict(q=2070000), dict(q=2071000), dict(q=6655556), dict(q=6655557), dict(q=8500000), dict(q=8500001), dict(q=11950000),
             dict(q=11950001), dict(q=25450000), dict(q=25450001), dict(q=25950000), dict(q=26450000), dict(q=26950000), dict(q=26950001),
             dict(y=1720000, old=1), dict(y=1720001, old=1), dict(y=1220000), dict(y=1220001), dict(q=1300000, y=1500000, old=1),
             dict(js=3000000, je=1000000, ao=3), dict(q=3000000, js=0, je=1000000), dict(ii=3000000, ie=1000000), dict(q=900000, zi=100000, ze=300000)]
    for b in boxes:
        e = await box(**b); t = e['tot']; lab = '箱 %s ' % (b,)
        chk(lab + '合計所得金額', await pg.inner_text('#o-t'), yen(t) + '円')
        chk(lab + '基礎控除', await pg.inner_text('#o-k'), yen(kiso(t)) + '円')
        ok = t <= 62 * MAN
        chk(lab + '結論', await pg.inner_text('#o-vd'), '扶養控除・配偶者控除の対象になります' if ok else '扶養控除・配偶者控除の対象になりません')
        chk(lab + '結論の注', await pg.inner_text('#o-vds'), '合計所得金額が62万円以下です（家族の所得税の扶養）' if ok else
            '合計所得金額が62万円を超えています。' + ('配偶者なら配偶者特別控除の対象です（133万円以下）' if t <= 133 * MAN else '配偶者特別控除の上限133万円も超えています'))
        br = '内訳：給与所得%s円' % yen(e['g'])
        if e['adj']: br += '（所得金額調整控除%s円を引いた額）' % yen(e['adj'])
        br += '・事業所得%s円・雑所得%s円' % (yen(e['jig']) if e['jig'] >= 0 else '-' + yen(-e['jig']), yen(e['zat']))
        if e['ichi']: br += '・一時所得%s円の半分' % yen(e['ichi'])
        chk(lab + '内訳', await pg.inner_text('#o-br'), br)
        sp = ('19〜22歳の子なら特定親族特別控除の対象です（62万円超123万円以下）' if 62 * MAN < t <= 123 * MAN else
              '学生なら勤労学生控除を受けられる額です（89万円以下・働いて得た所得以外が10万円以下）' if t <= 89 * MAN else '勤労学生控除の上限89万円を超えています')
        chk(lab + '学生', await pg.inner_text('#o-sp'), sp)
        chk(lab + '本人', await pg.inner_text('#o-kg'), '本人の合計所得金額が1,000万円を超えるので、配偶者控除・配偶者特別控除は受けられません' if t > 1000 * MAN
            else '本人の合計所得金額が1,000万円以下なので、配偶者控除・配偶者特別控除を受けられる側です')

    def sel(i): return ':is(#%s ~ .tw):not(#%s ~ .tw ~ .tw) tbody tr' % (i, i)
    async def rows(i):
        return await pg.eval_on_selector_all(sel(i), "rs=>rs.map(r=>[...r.children].map(td=>td.innerText.replace(/\\s+/g,'')))")
    def mstr(v):
        return '{:,}万円'.format(v // MAN)

    # 5 給与の早見表(HTML に手で書いた表)の全行
    K = [100, 110, 136, 150, 160, 163, 180, 190, 197, 200, 207, 250, 300, 400, 500, 665, 850, 1000, 1200, 1500, 2000]
    r = await rows('kyuyo')
    chk('給与の表の行', [x[0] for x in r], [mstr(k * MAN) for k in K])
    for x, k in zip(r, K):
        q = k * MAN
        chk('給与の表 %d万円' % k, x[1:], [yen(q - kyuyo(q)), yen(kyuyo(q))])
    # 6 年金の早見表の全行
    N = [60, 80, 100, 110, 130, 150, 180, 200, 250, 300, 330, 400, 500]
    r = await rows('nenkin')
    chk('年金の表の行', [x[0] for x in r], [mstr(k * MAN) for k in N])
    for x, k in zip(r, N):
        chk('年金の表 %d万円' % k, x[1:], [yen(nenkin(k * MAN, 0, 0)), yen(nenkin(k * MAN, 1, 0))])
    # 7 合計所得金額で決まることの表:合計所得金額の上限から、給与だけの年収の上限を自分で探す
    def nenshu_max(lim):
        lo, hi = 0, 40000000                     # kyuyo は年収が増えて減ることがないので、いちばん上の年収を1円ずつ確かめる
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if kyuyo(mid) <= lim: lo = mid
            else: hi = mid - 1
        return lo
    def ystr(v):
        return mstr(v) if v % MAN == 0 else '%d万%s円' % (v // MAN, yen(v % MAN))
    want = [['家族の扶養控除・配偶者控除の対象', '62万円以下', ystr(nenshu_max(62 * MAN)) + '以下'],
            ['特定親族特別控除の対象（19〜22歳）', '62万円超123万円以下', '%s超%s以下' % (ystr(nenshu_max(62 * MAN)), ystr(nenshu_max(123 * MAN)))],
            ['配偶者特別控除の対象', '62万円超133万円以下', '%s超%s以下' % (ystr(nenshu_max(62 * MAN)), ystr(nenshu_max(133 * MAN)))],
            ['勤労学生控除を受けられる', '89万円以下', ystr(nenshu_max(89 * MAN)) + '以下'],
            ['本人の基礎控除が%d万円' % (kiso(0) // MAN), '489万円以下', ystr(nenshu_max(489 * MAN)) + '以下'],
            ['配偶者控除・配偶者特別控除を受ける本人', '1,000万円以下', ystr(nenshu_max(1000 * MAN)) + '以下']]
    chk('決まることの表', await rows('kabe'), want)
    chk('年収の上限(あらましの括弧書き)', [nenshu_max(v * MAN) for v in (62, 123, 133, 89, 489, 1000)], [1360000, 1970000, 2070000, 1630000, 6655556, 11950000])
    # 8 控除額の式の表の全行(式の文字と、式で出した額が自分の計算と同じこと)
    want = [['220万円以下', '74万円'], ['220万円超360万円以下', '年収×30%＋8万円'], ['360万円超660万円以下', '年収×20%＋44万円'],
            ['660万円超850万円以下', '年収×10%＋110万円'], ['850万円超', '195万円（上限）']]
    chk('式の表', await rows('kojo'), want)
    chk('式の境目', [kojo_shiki(v) for v in (2200000, 3600000, 6600000, 8500000, 8500001)], [740000, 1160000, 1760000, 1950000, 1950000])
    chk('式の境目でつながる', (2200000 * 30 // 100 + 80000, 3600000 * 20 // 100 + 440000, 6600000 * 10 // 100 + 1100000, 8500000 * 10 // 100 + 1100000),
        (740000, 1160000, 1760000, 1950000))

    # 9 本文・よくある質問の数字
    def nen_max(lim, old):
        y = 0
        for c in range(0, 4000001):
            if nenkin(c, old, 0) <= lim: y = c
        return y
    flat = ''.join((await pg.inner_text('main')).split())
    for label, want in [
        ('冒頭', '令和8年分と令和9年分は、年収220万円以下の人の給与所得控除が74万円です。'),
        ('表の注', '年収219万1,000円から220万円未満は国税庁の表で決まった額です。年収220万円以上660万円未満は、年収を4,000円きざみに切り下げてから計算します。年収850万円を超えると給与所得控除は195万円で増えません。'),
        ('導入', '給与だけの人は年収%d万円で合計所得金額が%d万円になります。' % (136, kyuyo(1360000) // MAN)),
        ('導入2', '令和8年分から給与所得控除の最低額が74万円になり、扶養の所得要件も58万円から62万円に上がりました。'),
        ('年金の文', '65歳以上の人は、年金の収入が330万円未満なら110万円を引けます。65歳未満の人は、130万円未満なら60万円です。'),
        ('年金の注', '65歳以上は、令和8年12月31日に65歳以上の人（昭和%d年1月1日以前に生まれた人）です。' % (2026 + 1 - 65 - 1925)),
        ('年金の注2', '年金以外の合計所得金額が1,000万円を超える人は、雑所得が%d万円（2,000万円を超えると%d万円）多くなります。' % (
            (nenkin(3000000, 0, 10000001) - nenkin(3000000, 0, 0)) // MAN, (nenkin(3000000, 0, 20000001) - nenkin(3000000, 0, 0)) // MAN)),
        ('住民税の注', '住民税の扶養の所得要件も、令和9年度分から合計所得金額62万円以下です。'),
        ('箱の注', '判定は所得税の決まりです。住民税の扶養の所得要件も、令和9年度分から62万円以下です'),
        ('式の注', '年収69万1,000円から220万円未満は国税庁の表で給与所得の額が決まっています。'),
        ('調整控除', '所得金額調整控除として最大10万円が給与所得から引かれます。年収850万円を超える人に23歳未満の扶養親族がいる場合などの所得金額調整控除は、この計算に含めていません。'),
        ('青色', '青色申告特別控除（10万円・55万円・65万円）'),
        ('一時', '収入から払った額と特別控除の50万円を引き、その半分を合計所得金額に入れます。'),
        ('質問 136万円', '年収136万円の給与なら、所得は136万円から74万円を引いた%d万円です。' % (kyuyo(1360000) // MAN)),
        ('質問 197万円', '19歳から22歳の子は、年収%d万円まで特定親族特別控除の対象です。' % (nenshu_max(123 * MAN) // MAN)),
        ('質問 年金', '65歳以上で公的年金だけなら、年金の収入%d万円まで雑所得が62万円以下です。' % (nen_max(62 * MAN, 1) // MAN)),
        ('質問 年金65歳未満', '65歳未満は年金の収入%d万円までです。' % (nen_max(62 * MAN, 0) // MAN)),
        ('質問 事業', '売上300万円・経費100万円・青色65万円なら、所得は%d万円です。' % (ref(0, 0, 0, 3000000, 1000000, 3, 0, 0, 0, 0)['tot'] // MAN)),
        ('質問 両方', '両方がそれぞれ10万円を超えると、所得金額調整控除として給与所得から%d万円が引かれます。' % (ref(841000, 700001, 0, 0, 0, 0, 0, 0, 0, 0)['adj'] // MAN)),
        ('質問 850万円', '年収1,000万円なら給与所得は%d万円で、2,000万円なら%s万円です。' % (kyuyo(10000000) // MAN, yen(kyuyo(20000000) // MAN))),
        ('出典 あらまし', '国税庁「源泉所得税の改正のあらまし（令和8年4月）」'),
        ('出典 住民税', '東京都中央区「令和9年度から適用される個人住民税の主な改正」（住民税の扶養の所得要件は62万円以下・基礎控除は改正なし）'),
        ('出典 条文', '租税特別措置法第41条の3の11（所得金額調整控除）'),
        ('更新日', '更新日：2026年11月20日'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('古い文が残っていない', [w for w in ('58万円以下のまま', '年収190万円以下', '41条の3の3', '箕面市', '令和8年度税制改正による所得税の基礎控除の引上げ、') if w in flat], [])
    ids = await pg.eval_on_selector_all('[id]', 'es=>es.map(e=>e.id)')
    chk('id の重なり', sorted(set(i for i in ids if ids.count(i) > 1)), [])
    chk('目次の行き先', await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>{var e=document.getElementById(a.getAttribute('href').slice(1));return !!e&&e.tagName==='H2'&&e.innerText.replace(/\\s+/g,'')===a.textContent.replace(/\\s+/g,'')})"), [True] * 8)
    return n, bad
run('shotoku-kingaku', body)
