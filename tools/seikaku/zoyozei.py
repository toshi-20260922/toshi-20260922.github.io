# /zoyozei/ 贈与税の計算(暦年課税)。もらった額ごとの税額の早見表。
# 原本:国税庁 タックスアンサー
#   No.4408 贈与税の計算と税率(暦年課税) https://www.nta.go.jp/taxes/shiraberu/taxanswer/zoyo/4408.htm
#     (基礎控除110万円・一般税率と特例税率の速算表・計算例 500万円で一般53万円と特例48万5,000円)
#   No.4402 贈与税がかかる場合 https://www.nta.go.jp/taxes/shiraberu/taxanswer/zoyo/4402.htm
#     (110万円以下は申告不要・申告と納税は翌年2月1日から3月15日・延納は10万円超)
#   No.4429 贈与税の申告と納税 https://www.nta.go.jp/taxes/shiraberu/taxanswer/zoyo/4429.htm
#   No.4161 贈与財産の加算と税額控除(暦年課税) https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4161.htm
#     (加算対象期間の表・令和9年1月2日以後は3年より前の分から合計100万円を引く)
#   No.4103 相続時精算課税の選択 https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4103.htm
#     (60歳以上・18歳以上・基礎控除110万円は令和6年1月1日以後・特別控除2,500万円・20%・届出は翌年2月1日から3月15日)
#   No.4452 夫婦の間で居住用の不動産を贈与したときの配偶者控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/zoyo/4452.htm
#   No.4155 相続税の税率 https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4155.htm
#   端数:課税価格は1,000円未満切り捨て・税額は100円未満切り捨て(国税通則法118条・119条)
# 最後に原本を確かめた日:2026-11-20(どのページも「令和8年4月1日現在法令等」。No.4402 のQ&A(4402_qa.htm)で「毎年100万円ずつ10年間」も確かめた)
import os, sys, re
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
KISO = 1100000
MAN = 10000
# (基礎控除後の課税価格の上限, 税率%, 控除額) No.4408 の速算表
TOKUREI = [(200, 10, 0), (400, 15, 10), (600, 20, 30), (1000, 30, 90), (1500, 40, 190),
           (3000, 45, 265), (4500, 50, 415), (None, 55, 640)]
IPPAN = [(200, 10, 0), (300, 15, 10), (400, 20, 25), (600, 30, 65), (1000, 40, 125),
         (1500, 45, 175), (3000, 50, 250), (None, 55, 400)]
def base(g):
    return max(0, g - KISO) // 1000 * 1000
def ref(g, T):
    k = base(g)
    for top, r, d in T:
        if top is None or k <= top * MAN:
            return max(0, k * r // 100 - d * MAN) // 100 * 100   # k は1,000円単位なので割り切れる
def pct1(t, g):
    """もらった額に対する割合。小数1位に四捨五入した文字。"""
    v = Fraction(t * 1000, g)            # 0.1%単位
    n = int(v + Fraction(1, 2))
    return '%d.%d%%' % (n // 10, n % 10)
def maxgift(x, T):
    """贈与税の割合が x% 以下に収まるいちばん大きい贈与額(万円)。1万円きざみで全部の額を調べる(万円未満は切り捨て)。"""
    best = 0
    for m in range(1, 20001):
        g = m * MAN
        if ref(g, T) * 100 <= x * g:
            best = m
    # 1万円上では x% を超えることも確かめる
    assert ref((best + 1) * MAN, T) * 100 > x * (best + 1) * MAN
    return best
async def body(pg):
    n = bad = 0
    def ck(label, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp:
            bad += 1; print('NG', label, '画面', got, '原本', exp)
    # 1 計算の関数(境目の前後と代表例)
    gs = [0, 1, 500000, 1099999, 1100000, 1100001, 1100999, 1101000, 1101001, 1500000, 2345678, 5000000,
          7777777, 12000000, 25000000, 50000000, 99999999, 300000000, 1000000000]
    for T in (TOKUREI, IPPAN):
        for top, _, _ in T[:-1]:
            g0 = KISO + top * MAN
            gs += [g0 - 1000, g0 - 1, g0, g0 + 1, g0 + 999, g0 + 1000, g0 + 1001]
    for kind, T in ((0, TOKUREI), (1, IPPAN)):
        for g in sorted(set(gs)):
            got = await pg.evaluate('([g,k])=>window.__zoyo(g,k)', [g, kind])
            ck('関数 %d %s' % (g, '一般' if kind else '特例'), got, ref(g, T))
    # 2 入力欄に入れて結果の箱を読む
    btn = await pg.query_selector_all('#s-kind button')
    for kind, T in ((0, TOKUREI), (1, IPPAN)):
        await btn[kind].click()
        for g in (0, 1000000, 1100000, 1100001, 1101000, 3100000, 3100001, 4100000, 4101000, 5000000,
                  5100000, 7100000, 11100000, 16100000, 31100000, 31101000, 46100000, 46101000, 123456789):
            await pg.fill('#amt', str(g))
            t = ref(g, T)
            ck('箱 税額 %d %d' % (g, kind), num(await pg.inner_text('#o-t')), t)
            ck('箱 手元 %d %d' % (g, kind), num(await pg.inner_text('#o-n')), g - t)
            ck('箱 残り %d %d' % (g, kind), num(await pg.inner_text('#o-b')), base(g))
            ck('箱 税率の名前 %d %d' % (g, kind), await pg.inner_text('#o-k'), '一般税率' if kind else '特例税率')
            if g > 0:
                ck('箱 割合 %d %d' % (g, kind), await pg.inner_text('#o-r'), 'もらった額の' + pct1(t, g))
            ck('箱 申告 %d %d' % (g, kind), await pg.inner_text('#o-vd'),
               '贈与税の申告が必要です' if g > KISO else '贈与税の申告は不要です')   # No.4402 110万円以下は申告不要
            if g > KISO:
                s = await pg.inner_text('#o-vds')
                m = re.search(r'贈与税は([0-9,]+)円', s)
                ck('箱 説明の税額 %d %d' % (g, kind), num(m.group(1)) if m else None, t)
                ck('箱 説明の期限 %d %d' % (g, kind), '翌年2月1日から3月15日まで' in s, True)
    # 3 早見表の全行(手で書いた数字)
    rows = await pg.evaluate('''()=>[...document.querySelectorAll("#tb tr")].map(r=>[r.getAttribute("data-s"),...[...r.children].map(c=>[...c.childNodes].map(x=>x.textContent))])''')
    ck('早見表の行数', len(rows), 16)
    for ds, c0, c1, c2 in rows:
        g = int(ds) * MAN
        ck('早見表 行の額 %s' % ds, num(c0[0]), int(ds))
        for nm, c, T in (('特例', c1, TOKUREI), ('一般', c2, IPPAN)):
            t = ref(g, T)
            ck('早見表 %s万 %s 税額' % (ds, nm), num(c[0]), t)
            ck('早見表 %s万 %s 割合' % (ds, nm), c[1], pct1(t, g))
    # 黄色の行(入れた額にいちばん近い行)
    await pg.fill('#amt', '5000000')
    ck('黄色の行', await pg.evaluate('()=>[...document.querySelectorAll("#tb tr.hit")].map(r=>r.getAttribute("data-s")).join()'), '500')
    # 文は「入力した額に近い行が黄色」。入力を超えない行ではなく、差がいちばん小さい行が1つだけ黄色になる
    HY = [110, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500, 2000, 3000, 5000]
    ck('黄色の文', '下で入力した額に近い行が黄色になります。' in await pg.inner_text('.hy1'), True)
    for g in (0, 1290000, 1310000, 4490000, 4510000, 17400000, 17600000, 40100000, 999999999):
        await pg.fill('#amt', str(g))
        exp = min(HY, key=lambda m: abs(m * MAN - g))
        ck('黄色の行 %d' % g, await pg.evaluate('()=>[...document.querySelectorAll("#tb tr.hit")].map(r=>r.getAttribute("data-s")).join()'), str(exp))
    # id の重なりが無い・相手のいない閉じタグが無い・全画面のボタンは6行以上の表だけに付く
    ids = await pg.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)')
    ck('id の重なり', len(ids), len(set(ids)))
    src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'zoyozei', 'index.html'), encoding='utf-8').read()
    ck('span の開きと閉じ', len(re.findall(r'<span[ >]', src)), src.count('</span>'))
    ck('全画面のボタンの数', await pg.evaluate('()=>document.querySelectorAll("main button.fsb").length'),
       await pg.evaluate('()=>[...document.querySelectorAll("main .tw")].filter(w=>w.querySelectorAll("tr").length>=6).length'))
    ck('早見表の全画面のボタン', await pg.evaluate('()=>document.querySelectorAll(":is(#list ~ .tw):not(#list ~ .tw ~ .tw) tbody tr").length'), 16)
    # 4 速算表(手で書いた表)を原本の値と比べる
    tabs = await pg.evaluate('''()=>[...document.querySelectorAll("main table")].map(t=>[...t.querySelectorAll("tbody tr")].map(r=>[...r.children].map(c=>c.innerText.replace(/\\s+/g,""))))''')
    def sokusan(T):
        out = []
        for i, (top, r, d) in enumerate(T):
            lab = ('%s万円以下' % format(top, ',')) if top else ('%s万円超' % format(T[i - 1][0], ','))
            out.append([lab, '%d%%' % r, ('%s万円' % format(d, ',')) if d else 'なし'])
        return out
    for nm, i, T in (('特例', 1, TOKUREI), ('一般', 2, IPPAN)):
        exp = sokusan(T)
        ck('速算表 %s 行数' % nm, len(tabs[i]), 8)
        for a, b in zip(tabs[i], exp):
            for x, y in zip(a, b):
                ck('速算表 %s %s' % (nm, b[0]), x, y)
    # 5 割合で見る贈与額の表
    xs = [5, 10, 15, 20, 30, 40]
    ck('割合の表 行数', len(tabs[3]), len(xs))
    for row, x in zip(tabs[3], xs):
        ck('割合の表 %d%% 見出し' % x, row[0], '%d%%' % x)
        ck('割合の表 %d%% 特例' % x, row[1], '%s万円' % format(maxgift(x, TOKUREI), ','))
        ck('割合の表 %d%% 一般' % x, row[2], '%s万円' % format(maxgift(x, IPPAN), ','))
    # 6 文章の中の数字(原本の値)
    txt = await pg.evaluate('()=>document.querySelector("main").innerText.replace(/\\s+/g,"")')
    k = base(5000000)
    facts = [
        '500万円をもらった場合、110万円を引いた残りは%d万円です。' % (k // MAN),
        '390万円×15%%−10万円で%d万%s円です。' % (ref(5000000, TOKUREI) // MAN, format(ref(5000000, TOKUREI) % MAN, ',')),   # No.4408 計算例 485,000円
        '390万円×20%%−25万円で%d万円です。' % (ref(5000000, IPPAN) // MAN),                                                   # No.4408 計算例 530,000円
        'もらった額が400万円までは、2つの税率の表で税額が同じです。',
        'もらった額が110万円までなら贈与税はかからず、申告も要りません。',                      # No.4402
        '贈与税の申告は、翌年の2月1日から3月15日までです。',                                    # No.4402・No.4429
        '期間は、もらった年の翌年2月1日から3月15日までです。',
        '令和8年12月31日まで亡くなる前3年以内',                                                 # No.4161
        '令和9年1月1日から令和12年12月31日まで令和6年1月1日から亡くなった日まで',
        '令和13年1月1日から亡くなる前7年以内',
        '亡くなった日が令和9年1月2日以後の場合は、亡くなる前3年より前の分のうち合計100万円までは足し戻しません。',
        '相続時精算課税は60歳以上の父母や祖父母から、18歳以上の子や孫への贈与で選べる制度です。',   # No.4103
        '年齢は、贈与をした年の1月1日で見ます。',
        '毎年の基礎控除110万円（令和6年1月1日以後の贈与）',
        '特別控除通算2,500万円まで',
        '超えた分の税率一律20%',
        '最初の贈与を受けた翌年の2月1日から3月15日までに、届出書を税務署に出します',
        '婚姻期間20年以上で贈与税の申告をすると、110万円のほかに最高2,000万円まで引けます',     # No.4452
        '最高2,000万円の配偶者控除があります。',
        '贈与税額が10万円を超えて期限までに金銭で納めることが難しい場合は',                      # No.4402・No.4429
        '相続税の税率は、法定相続分に応じた取得金額ごとに10%から55%です。',                      # No.4155
        '（令和8年4月1日現在の法令）',
        '贈与税ではなく所得税がかかります',                                                       # No.4402・No.4405 法人からの贈与
        '生活費や教育費の名目でも、預金にしたり株式や不動産を買うお金にしたりした分には贈与税がかかります。',   # No.4405
        '毎年そのつど贈与の契約を結んで各年の合計が110万円以下なら、かかりません。',              # No.4402 Q&A
        '約束した年にまとめて受け取る権利をもらったものとして、贈与税がかかります。',             # No.4402 Q&A(定期金に関する権利)
        '同じ配偶者からは一生に一度だけ使えます。',                                               # No.4452
        '申告の期限までに税務署に申請して、許可を受けます。',                                     # No.4402 延納
        '110万円以下で贈与税がかからなかった年の分も、足し戻します。',                            # No.4161
        '一度選ぶとその贈与者からの贈与は、暦年課税に戻せません。',                               # No.4103
        '夫の父からの贈与にも、一般税率の表を使います。',                                         # No.4408
    ]
    for f in facts:
        ck('文 ' + f[:24], f in txt, True)
    # 400万円までは2つの表で同じ・400万円を1,000円超えると違う
    ck('400万円まで同じ', all(ref(g, TOKUREI) == ref(g, IPPAN) for g in range(0, 4000001, 1000)), True)
    # 2つの表が分かれるのは基礎控除後300万円超(もらった額410万円超)から。早見表の次の行(500万円)では違う
    ck('500万円では違う', ref(5000000, TOKUREI) != ref(5000000, IPPAN), True)
    return n, bad
run('zoyozei', body)
