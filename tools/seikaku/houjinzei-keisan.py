# /houjinzei-keisan/ 法人税の計算(法人税・地方法人税・防衛特別法人税・法人事業税・特別法人事業税・法人住民税の合計)。
# 原本:
#  国税庁 No.5759 法人税の税率(年800万円以下15%・所得が年10億円超の事業年度は17%・超える部分23.2%) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5759.htm
#  法人税基本通達16-4-1(800万円の月割は1,000円未満切り捨て。切り捨てる端数が所得の切り捨て額より多いときは切り上げ) https://www.nta.go.jp/law/tsutatsu/kihon/hojin/16/16_04.htm
#  国税庁「地方法人税の税率の改正のお知らせ」(10.3%) https://www.nta.go.jp/publication/pamph/hojin/chihou_hojin/01.htm
#  国税庁「令和7年度 法人税関係法令の改正の概要」防衛特別法人税(4%・基礎控除 年500万円×月数÷12・令和8年4月1日以後開始) https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2025/pdf/E.pdf
#  総務省「法人事業税」(所得割 3.5%・5.3%・7.0%) https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_09.html
#  総務省「法人住民税」(法人税割 1.0%・6.0%、均等割の表) https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_08.html
#  東京都主税局「特別法人事業税」(基準法人所得割額の37%) https://www.tax.metro.tokyo.lg.jp/kazei/work/tokubetsu_houjin
#  埼玉県「第6号様式 記載の手引」(所得割の3つの欄の分け方・欄ごとに課税標準1,000円未満と税額100円未満を切り捨て・均等割の月割) https://www.pref.saitama.lg.jp/documents/195692/r8_kisai-no-tebiki.pdf
#  財務省「令和7年度 税制改正の解説」租税特別措置法等(法人税関係)(17%の「年10億円」は12か月未満の年度で 10億円÷12×月数=措法42の3の2③・15%と17%の特例は令和9年3月31日までに開始する事業年度・17%は令和7年4月1日以後開始) https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2025/explanation/PDF/p0425-0554.pdf
#  財務省「令和8年度 税制改正の解説」同(税率・年800万円・年10億円・適用期限に変更なし) https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2026/explanation/PDF/p0504-0716.pdf
#  国税庁 No.5762 欠損金の繰越控除(10年。平成30年4月1日前に開始した事業年度の分は9年) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5762.htm
#  地方法人税・防衛特別法人税の課税標準1,000円未満と税額100円未満の切り捨ては国税通則法の一般の決まりによる(上の資料には書かれていない)。
# 最後に原本を確かめた日:2026-11-20
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run
def fl(x, unit):
    return int(x // unit) * unit
KINTO = {(0, 0): (20000, 50000), (0, 1): (20000, 120000), (1, 0): (50000, 130000), (1, 1): (50000, 150000)}
def ref(I, K, m, st, cap, emp, om):
    sho = max(0, I - min(K, I))                 # 繰越欠損金を引いた所得
    A = fl(sho, 1000)
    # 法人税
    lim = F(8000000 * m, 12)
    L = fl(lim, 1000)
    if lim - L > sho - A:
        L += 1000
    low = min(A, L)
    rate = 17 if F(sho) > F(1000000000 * m, 12) else 15
    hr = F(low * rate, 100) + F((A - low) * 232, 1000)
    hz = fl(hr, 100)
    kijun = fl(hr, 1000)                        # 法人税額(1,000円未満切り捨て)
    ch = fl(F(kijun * 103, 1000), 100)
    bo = fl(F(fl(max(F(0), hr - F(5000000 * m, 12)), 1000) * 4, 100), 100) if st else 0
    # 法人事業税(第6号様式の3つの欄)
    c1 = min(F(sho), F(4000000 * m, 12))
    c2 = min(F(sho), F(8000000 * m, 12)) - c1
    c3 = F(sho) - c1 - c2
    jg = sum(fl(F(fl(c, 1000) * r, 1000), 100) for c, r in ((c1, 35), (c2, 53), (c3, 70)))
    tk = fl(F(jg * 37, 100), 100)
    kp = fl(F(kijun * 10, 1000), 100)
    sp = fl(F(kijun * 60, 1000), 100)
    kk = KINTO[(cap, emp)]
    kq = fl(F(kk[0] * om, 12), 100)
    sq = fl(F(kk[1] * om, 12), 100)
    return {'hz': hz, 'ch': ch, 'bo': bo, 'jg': jg, 'tk': tk, 'kp': kp, 'kq': kq, 'sp': sp, 'sq': sq,
            'kuni': hz + ch + bo, 'ken': jg + tk + kp + kq, 'shi': sp + sq,
            't': hz + ch + bo + jg + tk + kp + kq + sp + sq}
def num(t):
    return int(''.join(c for c in t if c.isdigit()) or 0)
async def body(pg):
    n = bad = 0
    base = [0, 1, 999, 1000, 1001, 500000, 1000000, 2000000, 3000000, 5000000, 6000000, 10000000, 15000000,
            20000000, 25000000, 30000000, 50000000, 123456789, 300000000, 2000000000]
    for b in (4000000, 8000000, 24379000, 1000000000):       # 帯の境目(400万・800万・防衛特別法人税の始まり・10億)
        base += [b - 1000, b - 1, b, b + 1, b + 999, b + 1000, b + 1001]
    base += [24378000, 24379310, 24380000, 24381000, 24382000, 24383000, 24400000, 24500000]
    cases = []
    for I in base:
        for st in (1, 0):
            cases.append((I, 0, 12, st, 0, 0, 12))
    for m in range(1, 12):                                    # 12か月未満:月割した境目の前後
        pts = [0, 1000000, 5000000, 10000000, 30000000, 2000000000]
        for b in (4000000, 8000000, 1000000000):
            q = b * m // 12
            pts += [q - 1000, q - 1, q, q + 1, q + 334, q + 667, q + 999, q + 1000, q + 1500]
        z = (1200000 * m // 12 + (5000000 * m // 12 - 1200000 * m // 12) * 1000 // 232) + 8000000 * m // 12
        pts += [z - 3000, z, z + 3000, z + 20000, z + 100000]
        for I in pts:
            if I < 0: continue
            cases.append((I, 0, m, 1, 0, 0, m))
            cases.append((I, 0, m, 0, 1, 1, max(1, m - 1)))
    for cap in (0, 1):                                        # 均等割の全部の組み合わせと月割
        for emp in (0, 1):
            for om in range(1, 13):
                cases.append((0, 0, 12, 1, cap, emp, om))
                cases.append((7654321, 0, 12, 1, cap, emp, om))
    for I, K in ((5000000, 2000000), (5000000, 5000000), (5000000, 9000000), (30000000, 5620690),
                 (30000000, 5621000), (1000500000, 499), (1000500000, 500), (1000500000, 501), (9000999, 1000500)):
        for m in (12, 7):
            cases.append((I, K, m, 1, 0, 0, m))
    for c in cases:
        got = await pg.evaluate('(a)=>window.__hk.calc.apply(null,a)', list(c))
        exp = ref(*c); n += 1
        if any(got[k] != exp[k] for k in exp):
            bad += 1; print('NG', c, {k: (got[k], exp[k]) for k in exp if got[k] != exp[k]})
    # 画面の既定(所得500万円・12か月)の表示と、結論の文の数字
    exp = ref(5000000, 0, 12, 1, 0, 0, 12)
    for sel, v in (('#o-a', exp['t']), ('#o-c', 5000000 - exp['t'])):
        n += 1
        if num(await pg.inner_text(sel)) != v:
            bad += 1; print('NG 既定の表示', sel, await pg.inner_text(sel), v)
    pct = F(exp['t'] * 1000, 5000000)
    pct = F(int(pct + F(1, 2)), 10)
    n += 1
    if (await pg.inner_text('#o-b')).replace('%', '').strip() != str(float(pct)):
        bad += 1; print('NG 既定の負担率', await pg.inner_text('#o-b'), float(pct))
    head = await pg.inner_text('#calc .h'); n += 1
    if '合計%s円' % format(exp['t'], ',') not in head or '%s%%' % float(pct) not in head:
        bad += 1; print('NG 結論の文', head)
    o1 = await pg.inner_text('#o-1'); n += 1
    if o1 != '国（税務署）%s円・都道府県%s円・市区町村%s円' % tuple(format(exp[k], ',') for k in ('kuni', 'ken', 'shi')):
        bad += 1; print('NG 内訳の文', o1)
    # 内訳の表(9行と合計)
    tu = await pg.eval_on_selector_all('#tu tr', 'rs=>rs.map(r=>r.cells[2].innerText)')
    want = [exp[k] for k in ('hz', 'ch', 'bo', 'jg', 'tk', 'kp', 'kq', 'sp', 'sq', 't')]
    n += 1
    if [num(x) for x in tu] != want:
        bad += 1; print('NG 内訳の表', tu, want)
    # 所得ごとの表の全行
    rows = await pg.eval_on_selector_all('#tb tr', 'rs=>rs.map(r=>Array.from(r.cells).map(c=>c.innerText))')
    ROWS = [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 2500, 3000]
    n += 1
    if len(rows) != len(ROWS):
        bad += 1; print('NG 表の行数', len(rows))
    rates = {}
    for r, v in zip(rows, ROWS):
        X = v * 10000; e = ref(X, 0, 12, 1, 0, 0, 12)
        p10 = int(F(e['t'] * 1000, X) + F(1, 2)); rates[v] = p10
        want = [v, e['t'], '%d.%d%%' % (p10 // 10, p10 % 10), X - e['t']]
        n += 1
        if [num(r[0]), num(r[1]), r[2], num(r[3])] != want:
            bad += 1; print('NG 表', r, want)
    # 文の数字:「300万円から800万円なら24%から25%」「およそ2,438万円を超えると防衛特別法人税」「均等割7万・14万・18万・20万」「7か月の4,666,000円と4,667,000円」
    n += 1
    lo = min(F(ref(X, 0, 12, 1, 0, 0, 12)['t'], X) for X in range(3000000, 8000001, 10000))
    hi = max(F(ref(X, 0, 12, 1, 0, 0, 12)['t'], X) for X in range(3000000, 8000001, 10000))
    if not (F(24, 100) <= lo and hi < F(25, 100)):
        bad += 1; print('NG 24%から25%', float(lo), float(hi))
    n += 1
    if not (ref(24379000, 0, 12, 1, 0, 0, 12)['bo'] == 0 and ref(24400000, 0, 12, 1, 0, 0, 12)['bo'] > 0):
        bad += 1; print('NG 2,438万円')
    n += 1
    if [sum(KINTO[k]) for k in ((0, 0), (0, 1), (1, 0), (1, 1))] != [70000, 140000, 180000, 200000]:
        bad += 1; print('NG 均等割の文')
    for I, Lw in ((5000000, 4667000), (5000667, 4666000), (5000666, 4667000)):
        got = await pg.evaluate('(a)=>window.__hk.calc.apply(null,a).L', [I, 0, 7, 1, 0, 0, 7]); n += 1
        if got != Lw:
            bad += 1; print('NG 7か月の15%の上限', I, got, Lw)
    # 画面の操作:7か月・所得1,000万円を入れて合計を読む
    await pg.fill('#inc', '10000000'); await pg.dispatch_event('#inc', 'input')
    await pg.select_option('#mo', '7')
    e = ref(10000000, 0, 7, 1, 0, 0, 7); n += 1
    if num(await pg.inner_text('#o-a')) != e['t']:
        bad += 1; print('NG 7か月の表示', await pg.inner_text('#o-a'), e['t'])
    # 10億円を超えるときの説明の文
    await pg.select_option('#mo', '12')
    await pg.fill('#inc', '1000001000'); await pg.dispatch_event('#inc', 'input'); n += 1
    if '17%' not in await pg.inner_text('#o-2'):
        bad += 1; print('NG 17%の文', await pg.inner_text('#o-2'))
    # 早見表が上・計算の箱が下の並び(2026-11-20):id の重なりなし・早見表が箱より上・黄色の行は入力した所得を超えない中でいちばん近い行
    ids = await pg.evaluate("Array.from(document.querySelectorAll('[id]')).map(e=>e.id)"); n += 1
    if len(ids) != len(set(ids)):
        bad += 1; print('NG id の重なり', [i for i in set(ids) if ids.count(i) > 1])
    n += 1
    if not await pg.evaluate("!!(document.getElementById('list').compareDocumentPosition(document.getElementById('calc'))&4)"):
        bad += 1; print('NG 早見表が箱より下')
    for I in (0, 999999, 1000000, 5000000, 7999999, 8000000, 29999999, 30000000, 99999999):
        await pg.fill('#inc', str(I)); await pg.dispatch_event('#inc', 'input')
        hit = await pg.eval_on_selector_all('#tb tr.hit', 'rs=>rs.map(r=>r.cells[0].innerText)')
        le = [v for v in ROWS if v * 10000 <= I]
        want = [format(le[-1], ',')] if le else []
        n += 1
        if hit != want:
            bad += 1; print('NG 黄色の行', I, hit, want)
    n += 1
    if '入力した所得を超えない中でいちばん近い行が黄色になります。' not in await pg.content():
        bad += 1; print('NG 黄色の行の文')
    return n, bad
run('houjinzei-keisan', body)
