# /gakusei-kabe/ 学生バイトの年収の壁(19歳以上23歳未満・給与だけの場合)。
# 原本:
# 国税庁 No.1177 特定親族特別控除(令和8年4月1日現在法令等。合計所得62万円超123万円以下・段ごとの控除額・給与だけなら197万円以下)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1177.htm
# 国税庁 No.1180 扶養控除(令和8年分から合計所得62万円以下・一般38万円・特定扶養親族63万円・12月31日現在の年齢)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1180.htm
# 国税庁 No.1175 勤労学生控除(27万円・令和8年分から合計所得89万円以下・扶養控除等申告書か確定申告)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1175.htm
# 国税庁 No.1199 基礎控除・暮らしの税情報「所得税のしくみ」(令和8年分は合計所得489万円以下が104万円)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#   https://www.nta.go.jp/publication/pamph/koho/kurashi/html/01_1.htm
# 国税庁「源泉所得税の改正のあらまし(令和8年4月)」(給与所得控除の最低保障額74万円・令和8年分と9年分は
#   収入74万1,000円以上219万1,000円未満の給与所得=収入−74万円・所得要件を給与収入に直した額136万・159万…197万・163万円・
#   復興特別所得税は令和8年分まで2.1%)
#   https://www.nta.go.jp/publication/pamph/gensen/2026kaisei.pdf
# 国税庁「令和8年度税制改正(所得税の基礎控除の引上げ等関係)Q&A」 https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf
# 住民税(令和9年度):仙台市・千葉市「令和9年度から適用される個人市県民税の改正」(給与所得控除の最低保障額74万円・基礎控除の改正なし・
#   扶養62万円以下・勤労学生89万円以下・均等割も所得割もかからない人は合計所得45万円以下=給与119万円以下)
#   https://www.city.sendai.jp/shiminze-kikaku/kurashi/tetsuzuki/zekin/kojin/kaisei/r8.html
#   https://www.city.chiba.jp/zaiseikyoku/zeimu/kazeikanri/zeiseikaiseijuminzei2027.html
# 総務省 個人住民税(均等割4,000円=道府県民税1,000円+市町村民税3,000円・森林環境税1,000円・所得割10%=4%+6%・基礎控除43万円・特定扶養45万円・一般33万円)
#   https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html
# 江戸川区 住民税の所得控除(勤労学生控除26万円・特定親族特別控除の住民税の額:95万円以下45万円・その上は41・31・21・11・6・3万円)
#   https://www.city.edogawa.tokyo.jp/e013/kurashi/zeikin/juminzei/zei_gaiyo/shotokukojyo.html
# 調整控除(地方税法314条の6・37条。人的控除額の差=基礎控除5万円・勤労学生控除1万円。合計課税所得金額200万円以下は
#   差の合計と合計課税所得金額の小さい方の5%)は、この回は公的ページを開いて確かめられていない(法令の定めで書いた)。
# 日本年金機構「19歳以上23歳未満の方の被扶養者認定における年間収入要件が変わります」(150万円未満・認定日が属する年の12月31日の年齢・配偶者を除く)
#   https://www.nenkin.go.jp/oshirase/taisetu/2025/202508/0819.html
# 日本年金機構「国民年金の加入と保険料のご案内」(国内に住む20歳以上60歳未満は国民年金の被保険者。親の健康保険の扶養とは別)
#   https://www.nenkin.go.jp/tokusetsu/20kanyu.html
# 照らすもの:早見表(18行の全部の列)・計算の箱(控除額・控除の名前・社会保険・所得税・住民税・結論の文)・物差しの位置と壁の一覧・
#   月ごとの表(6行)・親の税金の表(4行)・内訳の表(11行)・本文と注とよくある質問の数字・説明文(description)・id の重なり・更新日
# 過去の誤り:均等割6,000円・勤労学生85万円と書いていた。2026-11-20 に直した所:所得税が「かかる」の境目(178万円超→実際に税額が出る178万2,000円以上)・
#   「国民年金に入る」の文・「197万円でゼロ」・150万円ちょうどの扱い・勤労学生控除で所得税が減るという文・出典の題名
# 最後に原本を確かめた日:2026-11-20
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from _lib import run

MAN = 10000
KYUYO_MIN = 74 * MAN            # 給与所得控除の最低保障額(令和8年分・9年分。住民税は令和9年度・10年度)
KISO_IT = 104 * MAN             # 所得税の基礎控除(合計所得489万円以下)
KISO_JU = 43 * MAN              # 住民税の基礎控除
FUYO_LIMIT = 62 * MAN           # 扶養親族の合計所得
KINRO_LIMIT = 89 * MAN          # 勤労学生の合計所得
KINRO_IT, KINRO_JU = 27 * MAN, 26 * MAN
HIKAZEI_JU = 45 * MAN           # 1級地の均等割の非課税の限度(35万円+10万円)。所得割の限度も扶養なしは45万円
KINTO, SHINRIN = 4000, 1000
SHAHO = 150 * MAN               # 19歳以上23歳未満は150万円未満
# No.1177 の表(合計所得の上限・所得税の控除額)。住民税は95万円以下が45万円で、その上は同じ額
TOKU = [(85, 63), (90, 61), (95, 51), (100, 41), (105, 31), (110, 21), (115, 11), (120, 6), (123, 3)]

def shotoku(x):
    """給与所得(令和8年分)。74万1,000円以上219万1,000円未満は収入−74万円。"""
    if x < 741000:
        return 0
    if x < 2191000:
        return x - KYUYO_MIN
    if x < 2193000: return 1451000
    if x < 2196000: return 1453000
    if x < 2200000: return 1456000
    assert x <= 3600000
    y = x // 4000 * 4000
    return y - (y * 30 // 100 + 80000)

def oya_it(x):
    s = shotoku(x)
    if s <= FUYO_LIMIT:
        return 63, '扶養控除'
    for top, v in TOKU:
        if s <= top * MAN:
            return v, '特定親族特別控除'
    return 0, '控除なし'

def oya_ju(x):
    s = shotoku(x)
    if s <= 95 * MAN:
        return 45
    return oya_it(x)[0]

def my_it(x):
    s = shotoku(x)
    k = KINRO_IT if s <= KINRO_LIMIT else 0
    kazei = max(0, s - KISO_IT - k) // 1000 * 1000
    assert kazei <= 1950000
    return kazei * 5 // 100 * 1021 // 1000 // 100 * 100     # 5%は1,000円単位に掛けるので割り切れる

def my_ju(x):
    s = shotoku(x)
    if s <= HIKAZEI_JU:
        return 0
    kin = s <= KINRO_LIMIT
    kazei = max(0, s - KISO_JU - (KINRO_JU if kin else 0)) // 1000 * 1000
    sa = min(50000 + (10000 if kin else 0), kazei)          # 合計課税所得200万円以下の調整控除
    assert kazei <= 2000000
    shi = max(0, kazei * 6 // 100 - sa * 3 // 100) // 100 * 100
    ken = max(0, kazei * 4 // 100 - sa * 2 // 100) // 100 * 100
    return shi + ken + KINTO + SHINRIN

def c(v):
    return '{:,}'.format(v)

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)

    # 壁の額を原本の定数から出す
    W_JU = HIKAZEI_JU + KYUYO_MIN          # 119万円
    W_FUYO = FUYO_LIMIT + KYUYO_MIN        # 136万円
    W_MAN = 85 * MAN + KYUYO_MIN           # 159万円
    W_KINRO = KINRO_LIMIT + KYUYO_MIN      # 163万円
    W_IT = KISO_IT + KYUYO_MIN             # 178万円
    W_END = 123 * MAN + KYUYO_MIN          # 197万円
    chk('壁の額', [W_JU, W_FUYO, SHAHO, W_MAN, W_KINRO, W_IT, W_END],
        [1190000, 1360000, 1500000, 1590000, 1630000, 1780000, 1970000])
    chk('壁の前後の税額', [my_ju(W_JU), my_ju(W_JU + 1), my_it(W_IT), my_it(W_IT + 1999), my_it(W_IT + 2000)], [0, 5000, 0, 0, 100])

    # 1 早見表(HTML に手で書いた18行)
    rows = await pg.eval_on_selector_all(':is(#list ~ .tw):not(#list ~ .tw ~ .tw) tbody tr', """rs=>rs.map(r=>{
        var t=r.children, w=t[0].cloneNode(true), sm=w.querySelector('small'), s=sm?sm.textContent:''; if(sm)sm.remove();
        return {x:w.textContent.trim(), sm:s, oya:t[1].textContent.trim(), sh:t[2].textContent.trim(), me:t[3].textContent.trim(), cls:t[2].className}})""")
    XS = [100, 110, 119, 120, 130, 136, 140, 150, 159, 160, 163, 170, 178, 180, 190, 197, 200, 210]
    chk('早見表の行', [r['x'] for r in rows], ['%d万円' % v for v in XS])
    LBL = {W_JU: 'ここまで住民税0', W_FUYO: 'ここまで扶養控除', SHAHO: '親の社会保険から外れる', W_MAN: 'ここまで満額',
           W_KINRO: '勤労学生控除の上限', W_IT: 'ここまで所得税0', W_END: 'ここまで親の控除あり'}
    for r, v in zip(rows, XS):
        x = v * MAN
        chk('早見表 %d 親の控除' % v, r['oya'], '所得税%d万円住民税%d万円' % (oya_it(x)[0], oya_ju(x)))
        chk('早見表 %d 社会保険' % v, (r['sh'], r['cls']), ('入れる', 'n') if x < SHAHO else ('外れる', 'n x'))
        chk('早見表 %d 自分の税金' % v, r['me'], '所得税%s円住民税%s円' % (c(my_it(x)), c(my_ju(x))))
        chk('早見表 %d 行の小さい字' % v, r['sm'], LBL.get(x, ''))
    # 小さい字が数字と食い違わないこと(ここまで=その年収ではまだ変わっていない)
    chk('小さい字と数字', [my_ju(W_JU), oya_it(W_FUYO)[1], oya_it(W_MAN)[0], oya_it(W_MAN + 1)[0], my_it(W_IT), oya_it(W_END)[0], oya_it(W_END + 1)[0],
                    shotoku(W_KINRO) <= KINRO_LIMIT, shotoku(W_KINRO + 1) <= KINRO_LIMIT],
        [0, '扶養控除', 63, 61, 0, 3, 0, True, False])

    # 2 計算の箱
    async def box(x):
        await pg.fill('#inc', str(x))
        return await pg.evaluate("""()=>({j1:document.getElementById('j1').textContent,j1e:document.getElementById('j1e').textContent,
            j2:document.getElementById('j2').textContent,j3:document.getElementById('j3').textContent,j4:document.getElementById('j4').textContent,
            vd:document.getElementById('vd').className,b:document.getElementById('o-vd').textContent,s:document.getElementById('o-vds').textContent})""")
    xs = [0, 500000, 740000, 1000000, 1234000, 2190000, 2500000, 3000000]
    for w in (W_JU, W_FUYO, SHAHO, W_MAN, W_KINRO, W_IT, W_END) + tuple(t * MAN + KYUYO_MIN for t, _ in TOKU):
        xs += [w - 1000, w - 1, w, w + 1, w + 1000]
    xs += [W_IT + 1999, W_IT + 2000, W_IT + 3000]
    for x in sorted(set(xs)):
        g = await box(x)
        a, nm = oya_it(x)
        chk('箱 %d 親の控除' % x, (g['j1'], g['j1e']), ('%d万円' % a, nm))
        chk('箱 %d 社会保険' % x, g['j2'], '入れる' if x < SHAHO else '外れる')
        chk('箱 %d 所得税' % x, g['j3'], 'かかる' if my_it(x) > 0 else 'かからない')
        if x < 2191000:
            chk('箱 %d 住民税' % x, g['j4'], 'かかる' if my_ju(x) > 0 else 'かからない')
        if x >= SHAHO:
            want = ('vd', '親の社会保険の扶養から外れます', '自分で国民健康保険などに入ります。' + ('親の控除は%d万円です' % a if a else '親の控除もなくなります'))
        elif nm == '扶養控除':
            want = ('vd no', '親の扶養のままでいられます', '親の扶養控除63万円も親の社会保険の扶養もそのままです')
        else:
            want = ('vd no', '親の控除も社会保険の扶養もそのままです', '扶養控除は特定親族特別控除に変わりますが、額は63万円で同じです')
            chk('箱 %d 150万円未満は63万円' % x, a, 63)
        chk('箱 %d 結論' % x, (g['vd'], g['b'], g['s']), want)
    chk('箱の小さい字', await pg.eval_on_selector_all('#calc .amt em', 'es=>es.map(e=>e.textContent)'),
        [await pg.inner_text('#j1e'), '%d万円未満まで' % (SHAHO // MAN), '%d万円まで0円' % (W_IT // MAN), '%d万円まで0円（目安）' % (W_JU // MAN)])
    # つまみと入力欄がそろうこと
    await pg.evaluate("()=>{var r=document.getElementById('incr');r.value='1600000';r.dispatchEvent(new Event('input',{bubbles:true}))}")
    chk('つまみ', (await pg.input_value('#inc'), await pg.inner_text('#j1')), ('1,600,000', '%d万円' % oya_it(1600000)[0]))
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'gakusei-kabe', 'index.html'), encoding='utf-8').read()
    chk('元の文 既定の年収', raw.count('value="1500000"'), 2)

    # 3 結論の3つの数字と去年(令和7年分:扶養58万円+65万円・基礎控除95万円+65万円)
    amt = await pg.eval_on_selector_all('.sum > .amt > div', "ds=>ds.map(d=>[d.querySelector('b').textContent,d.querySelector('em').textContent])")
    chk('結論の3つ', amt, [['%d万円' % (W_FUYO // MAN), '去年は%d万円' % (58 + 65)], ['%d万円' % (SHAHO // MAN), '変わらず'],
                       ['%d万円' % (W_IT // MAN), '去年は%d万円' % (95 + 65)]])

    # 4 物差し(100万〜220万円の線の上の位置)と壁の一覧
    WALLS = [W_JU, W_FUYO, SHAHO, W_MAN, W_IT, W_END]
    ms = await pg.eval_on_selector_all('.ruler .m', "ms=>ms.map(m=>[m.querySelector('b').textContent,m.style.left,m.className])")
    def pos(w):
        q = (Fraction(w - 100 * MAN, 120 * MAN) * 1000 + Fraction(1, 2)).__floor__()
        return ('%d.%d%%' % (q // 10, q % 10)).replace('.0%', '%')
    chk('物差し', ms, [[str(w // MAN), pos(w), 'm s' if w == SHAHO else ('m' if w in (W_JU, W_IT) else 'm d')] for w in WALLS])
    st = await pg.eval_on_selector_all('dl.st > div', "ds=>ds.map(d=>[d.querySelector('dt').textContent,d.querySelector('dd').textContent])")
    chk('壁の一覧', st, [
        ['119万円', '自分に住民税がかかり始める（令和9年度・1級地の目安）'],
        ['136万円', '親の控除が、扶養控除から特定親族特別控除に変わる（控除額63万円は同じ）'],
        ['150万円', '親の社会保険の扶養から外れる。自分で国民健康保険に入る'],
        ['159万円', '親の控除（特定親族特別控除）が減り始める'],
        ['178万円', '自分に所得税がかかり始める'],
        ['197万円', '親の控除（特定親族特別控除）がなくなる']])
    chk('壁の一覧の額', [s[0] for s in st], ['%d万円' % (w // MAN) for w in WALLS])

    # 5 月ごとの表(年収÷12 は1円未満切り捨て・時給1,200円の時間は1時間未満切り捨て)
    rows = await pg.eval_on_selector_all(':is(#tsuki ~ .tw):not(#tsuki ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    WHAT = ['自分に住民税がかかり始める', '親の控除が特定親族特別控除に変わる（額は同じ）', '親の社会保険の扶養から外れる（ちょうど150万円でも外れる）',
            '親の控除が減り始める', '自分に所得税がかかり始める', '親の控除がなくなる']
    chk('月の表', rows, [['%d万円' % (w // MAN), t, c(w // 12) + '円', '約%d時間' % (Fraction(w, 12 * 1200).__floor__())] for w, t in zip(WALLS, WHAT)])

    # 6 親の税金の表(控除63万円×税率×102.1%は1円未満切り捨て・住民税は45万円×10%)
    rows = await pg.eval_on_selector_all(':is(#oya ~ .tw):not(#oya ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    BAND = [(5, '課税所得195万円以下'), (10, '195万円超〜330万円'), (20, '330万円超〜695万円'), (23, '695万円超〜900万円')]
    want = []
    for r, lab in BAND:
        it = 63 * MAN * r * 1021 // 100000
        ju = 45 * MAN * 10 // 100
        want.append(['%d%%%s' % (r, lab), c(it) + '円', c(ju) + '円', '約%d万円' % ((Fraction(it + ju, MAN) + Fraction(1, 2)).__floor__())])
    chk('親の税金の表', rows, want)

    # 7 内訳の表(合計所得の段・給与の年収=合計所得+74万円・所得税の控除額)
    rows = await pg.eval_on_selector_all(':is(#why ~ .tw):not(#why ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    want = [['62万円以下', '%d万円以下' % (W_FUYO // MAN), '扶養控除63万円'],
            ['62万円超〜85万円以下', '%d万円超〜%d万円以下' % (W_FUYO // MAN, W_MAN // MAN), '特定親族特別控除63万円']]
    for (lo, _), (top, v) in zip(TOKU, TOKU[1:]):
        want.append(['%d万円超〜%d万円以下' % (lo, top), '〜%d万円' % (top + KYUYO_MIN // MAN), '%d万円' % v])
    want.append(['123万円超', '%d万円超' % (W_END // MAN), '0円'])
    chk('内訳の表', rows, want)
    for (top, v) in TOKU:      # 表の段と箱の計算が同じこと
        x = top * MAN + KYUYO_MIN
        chk('内訳の段 %d' % top, (oya_it(x)[0], oya_it(x + 1)[0] < v or top == 85), (v, True))

    # 8 本文・注・よくある質問・説明文の数字
    flat = ''.join((await pg.inner_text('main')).split())
    desc = await pg.get_attribute('meta[name=description]', 'content')
    chk('説明文が同じ', await pg.get_attribute('meta[property="og:description"]', 'content'), desc)
    chk('説明文の数字', '親の扶養控除は%d万円まで、特定親族特別控除は%d万円まで満額で%d万円を超えるとゼロ、親の社会保険の扶養は%d万円未満。'
        % (W_FUYO // MAN, W_MAN // MAN, W_END // MAN, SHAHO // MAN) in desc, True)
    title = await pg.title()
    chk('題名', (title, await pg.inner_text('h1')), ('【学生バイトの年収の壁】親の扶養はいくらまで？%d万・%d万・%d万円【2026年】' % (W_FUYO // MAN, SHAHO // MAN, W_IT // MAN),) * 2)
    for label, want in [
        ('早見表の前の文', '自分の税金は所得税が令和8年分で、住民税が令和9年度（東京23区などの1級地の目安）です。'),
        ('早見表の注 勤労学生', '勤労学生控除（所得税%d万円は合計所得%d万円以下＝給与%d万円以下・住民税%d万円も令和9年度から合計所得%d万円以下）を使って計算しています。'
         % (KINRO_IT // MAN, KINRO_LIMIT // MAN, W_KINRO // MAN, KINRO_JU // MAN, KINRO_LIMIT // MAN)),
        ('早見表の注 均等割', '住民税には均等割%s円と森林環境税%s円を含めています。' % (c(KINTO), c(SHINRIN))),
        ('結論 1', '親の控除は%d万円まで満額の63万円、そこから減って%d万円を超えるとなくなります' % (W_MAN // MAN, W_END // MAN)),
        ('結論 2', '%d万円は23歳になる年の前まで。23歳になる年からは130万円です' % (SHAHO // MAN)),
        ('導入', '%d万円を超えても親の控除はすぐには減りません。減り始めるのは%d万円を超えてから、なくなるのは%d万円を超えてからです。社会保険だけは%d万円で外れます。'
         % (W_FUYO // MAN, W_MAN // MAN, W_END // MAN, SHAHO // MAN)),
        ('月の表の注', '社会保険の%d万円は、これからの1年の見込みで判断します。' % (SHAHO // MAN)),
        ('136万円の崖 1', '%d万円を超えても親の控除が63万円のまま続くのは、12月31日の時点で19歳以上23歳未満の子だけです。' % (W_FUYO // MAN)),
        ('136万円の崖 2', '扶養控除38万円がなくなります'),
        ('136万円の崖 3', '住民税は扶養控除33万円の10%で、年3万3千円増えます。'),
        ('扶養内 税金', '19〜22歳なら%d万円までは控除が満額です。%d万円までは控除が少しずつ減ります' % (W_MAN // MAN, W_END // MAN)),
        ('扶養内 社会保険', '年収の見込みが%d万円以上になると外れます。外れると自分で国民健康保険に入ります' % (SHAHO // MAN)),
        ('親の税金の前の文', '学生の年収が%d万円を超えて親の控除（所得税63万円・住民税45万円）がなくなると、親の税金は次の分だけ増えます。親の所得税率で変わります。' % (W_END // MAN)),
        ('親の税金の注', '所得税の増加は控除63万円に税率と復興特別所得税（2.1%）をかけたもの、住民税の増加は控除45万円の10%です。'),
        ('内訳の前の文', '令和8年分から、給与所得控除の最低額が%d万円になりました。学生の給与から%d万円を引いた額が「合計所得金額」' % (KYUYO_MIN // MAN, KYUYO_MIN // MAN)),
        ('内訳の注 住民税', '住民税の特定親族特別控除は合計所得95万円以下が45万円で、それより上は所得税と同じ額です。'),
        ('内訳の注 去年', '令和7年分（去年）は給与所得控除が65万円だったので、同じ区分が%d万円・%d万円・%d万円でした。' % (58 + 65, 85 + 65, 123 + 65)),
        ('質問 103万円', '親の扶養控除の上限は令和7年分で%d万円、令和8年分で%d万円に上がっています。' % (58 + 65, W_FUYO // MAN)),
        ('質問 136万円', '扶養控除63万円が特定親族特別控除63万円に名前を変えるだけで、額は同じです。減り始めるのは%d万円を超えてからです。' % (W_MAN // MAN)),
        ('質問 150万円', '23歳になる年からは130万円に戻ります。配偶者の扶養に入っている人は年齢に関係なく130万円です。'),
        ('質問 月12万5千円', '月の給料が12万5千円以上の状態が続くと'),
        ('質問 4年生', '今年の1月から12月の給料が%d万円や%d万円を超えるかを見ます。' % (W_FUYO // MAN, W_MAN // MAN)),
        ('質問 源泉徴収', '年収%d万円以下なのに給料から所得税が引かれているのはなぜですか？' % (W_IT // MAN)),
        ('質問 勤労学生', '年収%d万円までの学生なら、申請すると自分の住民税が少なくなります。所得税は%d万円までかからないので変わりません。' % (W_KINRO // MAN, W_IT // MAN)),
        ('関連 扶養の62万円', '扶養の%d万円に入るかが分かります。' % (FUYO_LIMIT // MAN)),
        ('更新日', '更新日：2026年11月20日（令和8年分に対応）'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('月12万5千円', Fraction(SHAHO, 12), 125000)
    # 勤労学生控除で変わるのは住民税だけ(163万円までは控除がなくても所得税は0円)
    chk('勤労学生と所得税', max(0, shotoku(W_KINRO) - KISO_IT), 0)
    for bad_word in ('均等割6,000円', '合計所得85万円以下', '国民年金に入', '国民年金・国民健康保険', '197万円でゼロ', '197万円でなくなります'):
        chk('残っていない言葉 ' + bad_word, bad_word in flat or bad_word in desc, False)

    # 9 id の重なりと目次の行き先
    ids = await pg.eval_on_selector_all('[id]', 'es=>es.map(e=>e.id)')
    chk('id の重なり', sorted(set(i for i in ids if ids.count(i) > 1)), [])
    toc = await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>{var e=document.getElementById(a.getAttribute('href').slice(1));return !!e&&e.tagName==='H2'&&e.innerText.replace(/\\s+/g,'')===a.textContent.replace(/\\s+/g,'')})")
    chk('目次の行き先', toc, [True] * len(toc))
    return n, bad
run('gakusei-kabe', body)
