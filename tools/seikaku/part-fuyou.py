# /part-fuyou/ パートの扶養の計算(月収ごとの早見表・扶養の判定の箱・年収の壁の一覧)。
# 原本:
#  国税庁 No.1199 基礎控除(令和8年分・9年分は合計所得489万円以下が104万円=62万円+加算42万円・令和8年4月1日現在法令等)
#    https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#  財務省「令和8年度税制改正の大綱」(加算は489万円以下42万円・489万円超655万円以下5万円・給与所得控除の最低保障額69万円+令和8・9年の特例5万円)
#    https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2026/08taikou_01.htm
#  国税庁「令和8年度税制改正(所得税の基礎控除の引上げ等関係)Q&A」令和8年5月
#    (給与の収入74万1,000円以上219万1,000円未満は収入−74万円・219万1,000円以上220万円未満は145万1,000円・145万3,000円・145万6,000円)
#    https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf
#  国税庁「令和8年分 年末調整のしかた」昨年と比べて変わった点(同一生計配偶者は62万円以下=給与136万円以下・配偶者特別控除は62万円超133万円以下=給与136万円超207万円以下)
#    https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/102.pdf
#  国税庁 No.1191 配偶者控除(令和8年分は62万円以下・本人900万円以下38万円・950万円以下26万円・1,000万円以下13万円・1,000万円超は不可)
#    https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1191.htm
#  国税庁 No.1195 配偶者特別控除(令和8年分以降:62万円超95万円以下38万円・以下5万円きざみで36・31・26・21・16・11・6万円・130万円超133万円以下3万円)
#    https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1195.htm
#  総務省「令和8年度地方税制改正(案)について」(住民税の給与所得控除の最低保障額は令和9年度分から74万円・単身者の非課税の線は110万円→119万円・基本額等45万円は変更なし)
#    https://www.soumu.go.jp/main_content/001047636.pdf
#  東京都主税局「個人住民税」(均等割は都民税1,000円+区市町村民税3,000円・森林環境税1,000円・扶養なしの非課税は45万円以下・調整控除は人的控除の差と課税所得の少ないほうの5%=区3%+都2%)
#    https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju
#  全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分(4月納付分)から改定されます」(東京都9.85%・介護1.62%・子ども・子育て支援金0.23%は令和8年4月分から)
#    https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  全国健康保険協会「令和8年3月分(4月納付分)からの健康保険・厚生年金保険の保険料額表」東京支部(等級の境目・厚生年金18.3%・88,000円が下限・本人負担は50銭以下切り捨て)
#    https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#  厚生労働省・こども家庭庁「子ども・子育て支援金に関するQ&A」問6(一般保険料率と支援金率を合算した率で折半してから端数処理。shakaihoken.py と同じ)
#  厚生労働省「令和8年度 雇用保険料率のご案内」(一般の事業の労働者負担5/1,000・令和8年4月1日から令和9年3月31日)
#    https://www.mhlw.go.jp/content/001692566.pdf
#  日本年金機構「2026(令和8)年10月に社会保険の短時間労働者に係る賃金要件が撤廃されました」(2026年10月1日・週20時間以上・51人以上・学生でない)
#    https://www.nenkin.go.jp/oshirase/taisetu/jigyosho/2026/202610/100104.html
#  日本年金機構「短時間労働者に対する健康保険・厚生年金保険の適用拡大のご案内」(令和9年10月36人以上・令和11年10月21人以上・令和14年10月11人以上)
#    https://www.nenkin.go.jp/oshirase/topics/2021/0219.html
#  厚生労働省「短時間労働者の社会保険の加入拡大のポイント」(令和17年10月から10人以下) https://www.mhlw.go.jp/content/12500000/001633788.pdf
#  日本年金機構「従業員(健康保険・厚生年金保険の被保険者)が家族を被扶養者にするとき、被扶養者に異動があったときの手続き」(年間収入130万円未満・今後の見込みの額)
#    https://www.nenkin.go.jp/service/kounen/tekiyo/hihokensha1/20141202.html
# 判定に使う金額:社会保険の扶養=月収×12が130万円未満/配偶者の控除=給与の年収−給与所得控除(合計所得)/住民税の非課税=合計所得45万円以下(1級地・扶養なし)
# ページの前提:手取り=月収−社会保険料−(年の所得税+住民税)を12で割って1円未満を切り捨てた額。賞与なし・12か月同じ月収。
# 照らすもの:早見表13行の全部の列・結論の3つの数字・判定の箱(境目の前後)・壁の一覧7行・線引きの表3行・社会保険料の表3行・配偶者の控除の表11行・本文とよくある質問の数字・JS の境目
# 2026-11-20 に見つけたページの誤り:手取りが戻る境目を m<126846 と手で入れていた(126,847〜126,861円は住民税の段で扶養内の上限より1〜15円少ない)。126862 に直した。
# 2026-11-21 に見つけたページの誤り:判定の箱に直に書いた既定の結果が空だった(既定の月収108,000円の結果を書いた)。「年収が190万円以下なら74万円を引きます」(令和8年分は219万1,000円未満まで収入−74万円)。壁の一覧の130万円の行(130万円ちょうどで外れる)。
# 2026-11-21 に開いた原本:国税庁 No.1191・1195・1199・1410(220万円まで74万円)・1800(178万円=74万円+104万円)・改正Q&A・年末調整のしかた 102.pdf/総務省 令和8年度地方税制改正(案)/
#  福岡市「令和9年度個人市県民税の税制改正」(非課税119万円・同一生計配偶者62万円) https://www.city.fukuoka.lg.jp/zaisei/shisanzei/life/R9_kaisei.html
#  東京都主税局「個人住民税」/協会けんぽ 令和8年度の料率/厚生労働省 雇用保険料率のご案内・「年収の壁」への対応 https://www.mhlw.go.jp/stf/taiou_001_00002.html
#  日本年金機構(賃金要件の撤廃・適用拡大のご案内・被扶養者の手続き)・「労働契約内容による年間収入での被扶養者の認定の取り扱いについて」(令和8年4月1日から。賃金は諸手当と賞与を含む)
#    https://www.nenkin.go.jp/oshirase/taisetu/jigyosho/2026/202605/0501.html
# 今日開いていない原本:財務省の大綱・協会けんぽ R8_13tokyo.pdf・厚生労働省 001633788.pdf・子ども・子育て支援金に関するQ&A
# 最後に原本を確かめた日:2026-11-21
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from _lib import run
import rates

# ---- 原本の手順から書いた計算 ----
KENPO_B = rates.upper_sen()[:22]
KENPO_S = rates.std_sen()[:23]
def hyojun(m):
    for b, s in zip(KENPO_B, KENPO_S):
        if m < b * 1000:
            return s * 1000
    return 320000
def r50(x):                                   # 50銭以下切り捨て・50銭超切り上げ
    fl = x.__floor__()
    return fl + (1 if x - fl > F(1, 2) else 0)
def shaho(m):
    s = hyojun(m)
    kenpo = r50(F(s) * (F(rates.TOKYO, 10000) + F(rates.SIEN, 10000)) / 2)
    nenkin = r50(F(max(s, rates.NENKIN_MIN)) * F(rates.NENKIN_PER_1000, 1000) / 2)
    koyo = r50(F(m) * F(rates.KOYO_PER_1000, 1000))
    return kenpo, nenkin, koyo
def kyuyo_shotoku(y):                         # 令和8年分(月収30万円未満=年360万円未満まで)
    if y < 741000: return 0
    if y < 2191000: return y - 740000
    if y < 2193000: return 1451000
    if y < 2196000: return 1453000
    if y < 2200000: return 1456000
    return y // 4000 * 1000 * 28 // 10 - 80000
def zei(y, sha_nen):
    sh = kyuyo_shotoku(y)
    kz = max(0, sh - sha_nen - rates.KISO_SHOTOKU[0][1]) // 1000 * 1000       # 基礎控除104万円(合計所得489万円以下)
    it = kz * 5 // 100 * rates.FUKKO_NUM // rates.FUKKO_DEN // 100 * 100           # 195万円以下は5%・復興特別所得税・100円未満切り捨て
    if sh <= 450000:                                         # 住民税の非課税(1級地・扶養なし)
        return it, 0
    kj = max(0, sh - sha_nen - rates.KISO_JUMIN[0][1]) // 1000 * 1000
    ch = min(50000, kj)                                      # 調整控除(基礎控除の差5万円と課税所得の少ないほう)
    shi = max(0, kj * 6 // 100 - ch * 3 // 100) // 100 * 100
    ken = max(0, kj * 4 // 100 - ch * 2 // 100) // 100 * 100
    return it, shi + ken + 4000 + 1000                       # 均等割4,000円+森林環境税1,000円
def net_fuyo(m):
    it, ju = zei(m * 12, 0)
    return m - (it + ju) // 12
def net_sha(m):
    k, n, ko = shaho(m)
    it, ju = zei(m * 12, (k + n + ko) * 12)
    return m - k - n - ko - (it + ju) // 12
KYUYO_KOJO = 740000
HAI_MAX, TOKU_FULL, TOKU_END = 620000, 950000, 1330000
TOKU = [(950000, 38), (1000000, 36), (1050000, 31), (1100000, 26), (1150000, 21), (1200000, 16), (1250000, 11), (1300000, 6), (1330000, 3)]
def haigu(y):                                 # 夫や妻の合計所得900万円以下の場合の控除額(万円)と名前
    sh = kyuyo_shotoku(y)
    if sh <= HAI_MAX: return 38, '配偶者控除'
    for top, a in TOKU:
        if sh <= top: return a, '配偶者特別控除'
    return 0, '控除なし'
FUYO_MAX = (1300000 - 1) // 12                # 月収×12が130万円未満になるいちばん高い月収
def c(v): return '{:,}'.format(v)
def man(v):
    assert v % 10000 == 0
    return '%d万円' % (v // 10000)

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'part-fuyou', 'index.html'), encoding='utf-8').read()
    flat = ''.join((await pg.inner_text('main')).split())
    def has(label, want):
        chk('本文 ' + label, ''.join(want.split()) in flat, True)

    # 境目(原本の数字から)
    y_hai = HAI_MAX + KYUYO_KOJO; y_full = TOKU_FULL + KYUYO_KOJO; y_end = TOKU_END + KYUYO_KOJO
    y_jumin = 450000 + KYUYO_KOJO; y_shotoku = 1040000 + KYUYO_KOJO
    chk('境目', (FUYO_MAX, y_jumin, y_hai, y_full, y_shotoku, y_end), (108333, 1190000, 1360000, 1690000, 1780000, 2070000))
    chk('所得税は178万円まで0円', (zei(y_shotoku, 0)[0], zei(y_shotoku + 2000, 0)[0] > 0), (0, True))
    chk('住民税は119万円まで0円・超えると5,000円+所得割', (zei(y_jumin, 0)[1], zei(y_jumin + 1, 0)[1] >= 5000), (0, True))
    target = net_fuyo(FUYO_MAX)
    lows = [m for m in range(FUYO_MAX + 1, 300000) if net_sha(m) < target]
    modoru = max(lows) + 1                    # これ以上なら扶養内の上限の手取りを下回らない月収
    chk('手取りが戻る月収', modoru, 126862)
    chk('手取りが戻る月収 およそ12万7千円・年およそ152万円', ((modoru + 500) // 1000, (modoru * 12 + 5000) // 10000), (127, 152))
    chk('JS の境目', 'm<%d)' % modoru in raw, True)

    # 早見表(月収ごと・HTML に手で書いた13行)の全部の列
    rows = await pg.eval_on_selector_all(':is(#list ~ .tw):not(#list ~ .tw ~ .tw) tbody tr', """rs=>rs.map(r=>[...r.children].map(td=>
        [...td.childNodes].map(x=>x.textContent.trim()).filter(x=>x)))""")
    MS = [80000, 90000, 100000, FUYO_MAX, 110000, 120000, 130000, 140000, y_full // 12, 150000, 160000, 170000, 180000]
    chk('早見表の行の数', len(rows), len(MS))
    for r, m in zip(rows, MS):
        y = m * 12
        if m % 10000 == 0:
            c1 = [man(m), '年' + man(y)]
        elif m == FUYO_MAX:
            c1 = [c(m) + '円', '年' + man(1300000), '扶養の上限']
        else:
            c1 = [c(m) + '円', '年' + man(y_full), '控除満額の上限']
        ok = m <= FUYO_MAX
        c2 = ['入れる' if ok else '外れる', '配偶者の控除', '%d万円' % haigu(y)[0]]
        c3 = ['扶養内のまま', c(net_fuyo(m)) + '円' if ok else '扶養から外れる', '社会保険に入る', c(net_sha(m)) + '円']
        chk('早見表 %d' % m, r, [c1, c2, c3])
    has('早見表の前提', '住民税は令和9年度（東京23区などの1級地・扶養親族なし）の目安です。')
    has('早見表の注 雇用保険', '雇用保険に入っている場合は、月収の0.5%がさらに引かれます。')
    has('早見表の注 地域の名前', '勤め先の健康保険（協会けんぽ東京支部・40歳未満）・厚生年金・雇用保険に入った場合です。')

    # 結論の3つの数字
    amt = await pg.eval_on_selector_all('.sum > .amt > div', "ds=>ds.map(d=>[d.querySelector('b').textContent,d.querySelector('em').textContent])")
    def man1(v):                              # 0.1万円の位に四捨五入
        t = (v + 500) // 1000
        return '%d.%d万円' % (t // 10, t % 10)
    chk('結論の3つ', amt, [[man1(FUYO_MAX), '月%s円' % c(FUYO_MAX)], [man1(modoru), '年約%d万円' % ((modoru * 12 + 5000) // 10000)],
                         [man1(y_full // 12), '月%s円' % c(y_full // 12)]])
    chk('結論の見出し', await pg.inner_text('.sum > .h'), '結論パートの月収で見ると、分かれ目はこの3つです')
    has('結論 地域の名前', '手取りは協会けんぽ東京支部・40歳未満で計算しています')
    has('結論 51人', '勤め先が従業員51人以上で週20時間以上働く人は、月収にかかわらず社会保険に入ります')
    d1 = target - net_sha(FUYO_MAX + 1); d2 = target - net_sha(110000)
    chk('超えた直後に減る額', ((d2 + 500) // 1000, (d1 + 500) // 1000), (14, 15))
    has('減る額の文', '月108,333円を少し超えて社会保険に入ると、手取りは扶養内より月1万4千〜1万5千円ほど減ります。')
    has('戻る月収の文', '手取りが元に戻るのは月収約12万7千円から。')
    chk('題名の下の説明', '社会保険に入ると、月収約12万7千円で扶養内の手取りに追いつきます。' in raw, True)

    # 判定の箱(自分の月収で確かめる)
    ms = [0, 1, 60000, 88000, 100000, 108000, FUYO_MAX - 1, FUYO_MAX, FUYO_MAX + 1, 110000, 120000, 126845, 126846, 126847,
          modoru - 1, modoru, modoru + 1, 127000, 130000, 150000, 200000, 250000, 1000000, 10000000]
    for top in [HAI_MAX] + [t for t, _ in TOKU]:
        mm = (top + KYUYO_KOJO) // 12
        ms += [mm - 1, mm, mm + 1]
    for m in ms:
        await pg.fill('#inc', str(m))
        y = m * 12; a, nm = haigu(y)
        got = [await pg.inner_text('#' + i) for i in ('j1', 'j2', 'j2e', 'j3', 'o-vd', 'o-vds')]
        if m <= FUYO_MAX:
            v = ['扶養内です', '社会保険の扶養に入れます。月%s円を超えると外れます' % c(FUYO_MAX)]
        elif m < modoru:
            v = ['扶養から外れて手取りが減ります', '社会保険料が引かれるので扶養内のときより手取りが少なくなります。手取りが戻るのは月収約12万7千円からです']
        else:
            v = ['社会保険の扶養から外れます', '手取りは扶養内の上限のときと同じか、それより多くなります']
        chk('箱 %d' % m, got, ['入れる' if m <= FUYO_MAX else '外れる', '%d万円' % a, nm, c(y) + '円'] + v)
        if FUYO_MAX < m < 300000:             # 文と自分の計算の向きが合うこと
            chk('箱の文と手取り %d' % m, net_sha(m) < target, m < modoru and net_sha(m) < target)
    chk('箱の上限の文字', await pg.eval_on_selector_all('.amt.jdg em', 'es=>es.map(e=>e.textContent)'),
        ['月%s円まで' % c(FUYO_MAX), '控除なし', '12か月同じ額の場合'])
    for v in (60000, 108000, 150000, 200000):     # つまみと入力欄がそろうこと
        await pg.evaluate("v=>{var e=document.getElementById('incr');e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}))}", v)
        chk('つまみ %d' % v, await pg.inner_text('#j3'), c(v * 12) + '円')
    await pg.fill('#inc', '108000')            # 箱に直に書いた既定の結果(JS が書き換える前の文)が、既定の月収の結果と同じこと
    dy = 108000 * 12; da, dnm = haigu(dy)
    chk('元の文 既定の結果 判定', '<div class="vd no" id="vd"><b id="o-vd">扶養内です</b><span id="o-vds">社会保険の扶養に入れます。月%s円を超えると外れます</span></div>' % c(FUYO_MAX) in raw, True)
    chk('元の文 既定の結果 3つ', ('<b id="j1">%s</b>' % ('入れる' if 108000 <= FUYO_MAX else '外れる') in raw,
        '<b id="j2">%d万円</b><em id="j2e">%s</em>' % (da, dnm) in raw, '<b id="j3">%s<i>円</i></b>' % c(dy) in raw), (True, True, True))
    chk('元の文と画面 既定', [await pg.inner_text('#' + i) for i in ('j1', 'j2', 'j2e', 'j3', 'o-vd')], ['入れる', '%d万円' % da, dnm, c(dy) + '円', '扶養内です'])
    chk('元の文と画面 既定の色', await pg.get_attribute('#vd', 'class'), 'vd no')
    chk('元の文 既定の月収', 'id="inc" inputmode="numeric" min="0" max="10000000" step="1000" value="108000"' in raw, True)

    # パートの年収の壁の一覧(7行)
    rows = await pg.eval_on_selector_all(':is(#kabe ~ .tw):not(#kabe ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent.trim()))")
    chk('壁の一覧', rows, [
        ['週20時間', '本人', '従業員51人以上の勤め先なら年収にかかわらず勤め先の社会保険に入ります'],
        [man(y_jumin), '本人', '本人に住民税がかかり始めます（令和9年度・1級地の目安）'],
        [man(1300000), '本人', '年収130万円以上になると配偶者の社会保険の扶養から外れ、自分で保険料を払います'],
        [man(y_hai), '配偶者', '配偶者控除が配偶者特別控除に変わります（額は%d万円のまま）' % haigu(y_hai + 1)[0]],
        [man(y_full), '配偶者', '配偶者特別控除が少しずつ減り始めます'],
        [man(y_shotoku), '本人', '本人に所得税がかかり始めます'],
        [man(y_end), '配偶者', '配偶者特別控除がなくなります']])
    chk('壁の一覧 低い順', [y_jumin, 1300000, y_hai, y_full, y_shotoku, y_end], sorted([y_jumin, 1300000, y_hai, y_full, y_shotoku, y_end]))
    chk('壁の前後の控除', [haigu(y_hai), haigu(y_hai + 1), haigu(y_full), haigu(y_full + 1), haigu(y_end), haigu(y_end + 1)],
        [(38, '配偶者控除'), (38, '配偶者特別控除'), (38, '配偶者特別控除'), (36, '配偶者特別控除'), (3, '配偶者特別控除'), (0, '控除なし')])
    has('壁の注', '税金の壁は令和8年分（住民税は令和9年度）の給与だけの年収です。配偶者の控除は、扶養する人の合計所得が900万円以下の場合の額です。')

    # どこで線を引くか(3行)
    rows = await pg.eval_on_selector_all(':is(#sen ~ .tw):not(#sen ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.innerText.replace(/\\s+/g,'')))")
    chk('線引きの表', rows, [
        ['社会保険の扶養に残る', '130万円未満（月%s円以下）' % c(FUYO_MAX), '保険料がかからず配偶者の控除も満額です', '週20時間以上で51人以上の勤め先なら、この額より下でも社会保険に入ります'],
        ['社会保険に入っても損をしない', '年%d万円あたりから' % ((modoru * 12 + 5000) // 10000), '将来の厚生年金が増えます', '130万円を少し超えるだけだと、保険料の分だけ扶養内より手取りが減ります'],
        ['配偶者の控除を満額で残す', '%s以下（月%s円以下）' % (man(y_full), c(y_full // 12)), '配偶者の控除が38万円のままです', '本人の住民税は%sを超えるとかかります' % man(y_jumin)]])
    has('線引きの注', '年152万円は、上の計算の結果に出る「社保に入って手取りが戻る」月収を年にした目安です（協会けんぽ東京支部・40歳未満）。')

    # 社会保険に入ると引かれる額(3行)
    rows = await pg.eval_on_selector_all(':is(#sha ~ .tw):not(#sha ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent.trim()))")
    chk('社会保険料の表', rows, [[man(m)] + [c(x) for x in shaho(m)] + [c(sum(shaho(m)))] for m in (100000, 130000, 150000)])
    has('社会保険料の前提', '協会けんぽ東京支部・40歳未満、令和8年4月分からの料率で計算しています。')
    has('社会保険料の注', '健康保険は子ども・子育て支援金（0.23%）を含みます。40歳から64歳の人は介護保険料（1.62%の半分）が加わります。厚生年金は、月収が9万3千円未満でも標準報酬月額8万8千円で計算します。')
    nen = F(110000) * F(5481, 1000000) * 12
    chk('年金が増える額', (hyojun(110000), (nen + F(1, 2)).__floor__()), (110000, 7235))
    has('年金が増える額の文', '65歳からの年金が年約7,235円増えます（標準報酬月額11万円×5.481/1000×12か月）。')

    # 週20時間で決まる人
    has('賃金要件の撤廃', '2026年10月から、社会保険に入るかどうかの月収の条件（月8万8千円）がなくなりました。勤め先の従業員が51人以上なら、次の条件を満たす人は月収にかかわらず勤め先の社会保険に入ります。')
    chk('3つの条件', await pg.eval_on_selector_all('dl.st dd', 'ds=>ds.map(d=>d.textContent)'), ['週の労働時間が20時間以上', '2か月を超えて働く見込みがある', '学生ではない'])
    has('50人以下', '従業員50人以下の勤め先は、順に対象が広がります。')

    # 配偶者の控除が満額の月収(11行)
    rows = await pg.eval_on_selector_all(':is(#hai ~ .tw):not(#hai ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.innerText.replace(/\\s+/g,'')))")
    want = [['%s以下' % man(y_hai), '〜%s円' % c(y_hai // 12), '配偶者控除38万円'],
            ['%s超%s以下' % (man(y_hai), man(y_full)), '〜%s円' % c(y_full // 12), '配偶者特別控除%d万円' % TOKU[0][1]]]
    for top, a in TOKU[1:]:
        want.append(['〜' + man(top + KYUYO_KOJO), c((top + KYUYO_KOJO) // 12) + '円', '%d万円' % a])
    want.append(['%s超' % man(y_end), c(y_end // 12) + '円超', '0円'])
    chk('配偶者の控除の表', rows, want)
    for top, a in TOKU:                       # 表の年収の上限の前後で控除額が変わること
        yy = top + KYUYO_KOJO
        chk('控除の段 %d' % yy, (haigu(yy)[0], haigu(yy + 1)[0] < a), (a, True))
    has('控除の表の前提', 'パートの年収で、夫や妻の所得税の控除額が変わります。夫や妻の合計所得が900万円以下の場合です。')
    has('控除の表の注', '令和8年分の金額です。給与所得控除の最低額は74万円です。パートの給与の年収から74万円を引いた額が合計所得になり、その額で控除額が決まります。')

    # 本人の税金・年末調整・よくある質問の数字
    has('所得税178万円', '令和8年分の所得税は、給与だけなら年収%sまでかかりません。給与所得控除の74万円と基礎控除の104万円を合わせた額です。' % man(y_shotoku))
    has('住民税119万円', '住民税は基礎控除が43万円なので、早くかかり始めます。東京23区などでは年収%sを超えると均等割4,000円と森林環境税1,000円の年5,000円がかかり、所得税より先に負担が出ます（令和9年度）。' % man(y_jumin))
    has('年末調整 74万円', '年収が219万円以下なら74万円を引きます。')
    chk('219万円以下は74万円', [y - kyuyo_shotoku(y) for y in (741000, 1900000, 2070000, 2190000, 2190999)], [KYUYO_KOJO] * 5)
    chk('219万1,000円を超えると収入−74万円でなくなる', 2192000 - kyuyo_shotoku(2192000) != KYUYO_KOJO, True)
    chk('130万円ちょうどは扶養から外れる', (FUYO_MAX * 12 < 1300000, (FUYO_MAX + 1) * 12 >= 1300000), (True, True))
    has('年末調整 136万円', 'パートの年収が%s以下：所得は%s以下で、配偶者控除の欄に書きます' % (man(y_hai), man(HAI_MAX)))
    has('年末調整 207万円', '%sを超えて%s以下：配偶者特別控除の欄に書きます' % (man(y_hai), man(y_end)))
    has('年末調整 900万円', '扶養する人の合計所得が900万円を超える：控除額が少なくなり、1,000万円を超えると受けられません')
    has('質問 103万円', '令和8年分では、本人に所得税がかかり始めるのは年収%sです。配偶者控除が受けられる上限も%sに上がり、103万円で変わることはなくなりました。' % (man(y_shotoku), man(y_hai)))
    has('質問 150万円', '以前の150万円は配偶者特別控除が満額で受けられる上限でした。令和7年分は%sで、令和8年分は%sに上がっています。' % (man(TOKU_FULL + 650000), man(y_full)))
    has('質問 900万円', '扶養する人の合計所得が900万円を超えると控除額が少なくなり、1,000万円を超えると配偶者控除も配偶者特別控除も受けられません。')
    has('質問 通勤手当', '月の給与が10万円でも通勤手当が1万円あれば、月11万円として見ます。')
    has('質問 国保', '国民健康保険には扶養という仕組みがないので、%s円の上限はありません。' % c(FUYO_MAX))
    has('質問 国保の控除', '夫の所得税の配偶者控除は、会社員のときと同じく年収%s・%sで決まります。' % (man(y_hai), man(y_full)))
    has('質問 社会保険と控除', '社会保険に入っても年%sまでは38万円のままです。' % man(y_full))
    has('関連 62万円', '給与・年金・事業の収入から、扶養の%sに入るかが分かります。' % man(HAI_MAX))
    has('更新日', '更新日：2026年11月21日（令和8年分に対応）')
    has('出典を確かめた月', '出典・参考（2026年11月確認）')

    # 出典のリンクの文字(着いたページの題名と合わせたもの)
    links = await pg.eval_on_selector_all('.src a', "as=>as.map(a=>[a.getAttribute('href'),a.textContent])")
    chk('出典のリンク', links, [
        ['https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1191.htm', '国税庁 タックスアンサー No.1191 配偶者控除'],
        ['https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1195.htm', 'No.1195 配偶者特別控除'],
        ['https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf', '国税庁「令和8年度税制改正（所得税の基礎控除の引上げ等関係）Q&A」'],
        ['https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08', '全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます」'],
        ['https://www.mhlw.go.jp/content/001692566.pdf', '厚生労働省「令和8年度 雇用保険料率のご案内」'],
        ['https://www.nenkin.go.jp/oshirase/taisetu/jigyosho/2026/202610/100104.html', '日本年金機構「2026（令和8）年10月に社会保険の短時間労働者に係る賃金要件が撤廃されました」'],
        ['https://www.nenkin.go.jp/service/kounen/tekiyo/hihokensha1/20141202.html', '日本年金機構「従業員（健康保険・厚生年金保険の被保険者）が家族を被扶養者にするとき、被扶養者に異動があったときの手続き」'],
        ['https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm', '国税庁 タックスアンサー No.1199 基礎控除'],
        ['https://www.soumu.go.jp/main_content/001047636.pdf', '総務省「令和8年度地方税制改正（案）について」'],
        ['https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju', '東京都主税局「個人住民税」']])

    # id の重なりと目次の行き先
    ids = await pg.eval_on_selector_all('[id]', 'es=>es.map(e=>e.id)')
    chk('id の重なり', sorted(set(i for i in ids if ids.count(i) > 1)), [])
    chk('目次の行き先', await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>{var e=document.getElementById(a.getAttribute('href').slice(1));return !!e&&e.tagName==='H2'&&e.innerText.replace(/\\s+/g,'')===a.textContent.replace(/\\s+/g,'')})"), [True] * 6)
    return n, bad
run('part-fuyou', body)
