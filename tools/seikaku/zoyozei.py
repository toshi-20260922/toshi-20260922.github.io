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
#   No.4508 直系尊属から住宅取得等資金の贈与を受けた場合の非課税 https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4508.htm
#     (令和6年1月1日から令和8年12月31日までの贈与・省エネ等住宅1,000万円・それ以外500万円)
#   相続税法28条1項(令和6年1月1日施行の条文。新日本法規の法令ページで読んだ):申告書を出すのは
#     「第21条の5、第21条の7及び第21条の8の規定による贈与税額がある場合」。税額が0円なら暦年課税の申告は要らない。
#     110万円を1〜999円超える額は、残りを1,000円未満切り捨てで0円にしても、切り捨てずに10%を掛けて100円未満を切り捨てても税額0円。
#     ページは 11-21 に「税額があるときだけ申告が必要」に直した(それまでは110万円を1円でも超えると「申告が必要です」と「贈与税は0円です」が並んだ)。
#   端数:課税価格は1,000円未満切り捨て・税額は100円未満切り捨て(国税通則法118条・119条。条文そのものは 11-21 も開けていない。
#     No.4408 の計算例と国税庁の通則法基本通達119条関係のページまで)
# 最後に原本を確かめた日:2026-11-21(No.4408・No.4402・No.4429・No.4103・No.4161・No.4155・No.4508・相続税法28条。どのタックスアンサーも「令和8年4月1日現在法令等」)
#   No.4452・No.4405 は 11-21 は開けなかった(11-20 に確かめたまま)。No.4402 のQ&A(4402_qa.htm)は 11-20 に確かめた
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
        for g in (0, 1000000, 1100000, 1100001, 1100500, 1100999, 1101000, 1101999, 3100000, 3100001, 4100000, 4101000, 5000000,
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
               '贈与税の申告が必要です' if t > 0 else '贈与税の申告は不要です')   # 相続税法28条 贈与税額がある場合だけ・No.4402 110万円以下は申告不要
            s = await pg.inner_text('#o-vds')
            ck('箱 申告の色 %d %d' % (g, kind), await pg.get_attribute('#vd', 'class'), 'vd' if t > 0 else 'vd no')
            if t == 0:
                ck('箱 説明(税額なし) %d %d' % (g, kind), s, '110万円を引いた残りが1,000円未満なので、贈与税はかかりません' if g > KISO
                   else 'もらった額が110万円以下なので、贈与税はかかりません')
                ck('箱 0円と申告が並ばない %d %d' % (g, kind), '申告して納めます' in s, False)
            else:
                ck('箱 説明の頭 %d %d' % (g, kind), s.startswith('もらった額が110万円を超えています。'), True)
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
    ck('黄色の文が無い', '黄色' in await pg.inner_text('.hy1'), False)
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
        'もらった額が410万円までは、2つの税率の表で税額が同じです。',
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
        '省エネ等住宅で1,000万円まで・それ以外の住宅で500万円まで非課税です。',                   # No.4508
        '令和8年12月31日までにもらったお金が対象です（国税庁No.4508）。',                         # No.4508
        '「父母・祖父母から」は、もらった年の1月1日に18歳以上の子や孫が受ける場合です',           # No.4408
        '一般税率の表は、兄弟の間・夫婦の間・親から18歳未満の子への贈与などに使います。',         # No.4408
        '贈与の額（令和6年以後の分は毎年110万円を引いた残り）を相続財産に足して、相続税を計算します',   # No.4103
        '足し戻した財産にかかっていた贈与税は、相続税から引きます。',                             # No.4161
        '更新日：2026年11月21日（令和8年4月1日現在の法令）',
    ]
    for f in facts:
        ck('文 ' + f[:24], f in txt, True)
    # 410万円(110万円を引いた残り300万円)までは2つの表で同じ・1,000円超えると違う
    ck('410万円まで同じ', all(ref(g, TOKUREI) == ref(g, IPPAN) for g in range(0, 4100001, 1000)), True)
    ck('410万1,000円では違う', ref(4101000, TOKUREI) != ref(4101000, IPPAN), True)
    # 税額が出るいちばん低い額は110万1,000円(税額100円)。110万999円までは0円
    ck('110万999円は0円', (ref(1100999, TOKUREI), ref(1100999, IPPAN)), (0, 0))
    ck('110万1,000円は100円', (ref(1101000, TOKUREI), ref(1101000, IPPAN)), (100, 100))
    # 計算の箱に直に書いた既定の結果(JS が書き換える前の HTML)。既定は500万円・父母祖父母から
    g0 = int(re.search(r'id="amt"[^>]*value="(\d+)"', src).group(1)); t0 = ref(g0, TOKUREI)
    ck('既定 入力とつまみが同じ', re.search(r'id="amtr"[^>]*value="(\d+)"', src).group(1), str(g0))
    ck('既定 選ばれている税率', re.search(r'<button type="button" class="on" data-v="(\d)"', src).group(1), '0')
    def raw(i):
        return re.sub(r'<[^>]+>', '', re.search(r'id="%s"[^>]*>(.*?)</(?:b|em|span)>' % i, src).group(1))
    ck('既定 税額', raw('o-t'), format(t0, ',') + '円')
    ck('既定 手元', raw('o-n'), format(g0 - t0, ',') + '円')
    ck('既定 残り', raw('o-b'), format(base(g0), ',') + '円')
    ck('既定 割合', raw('o-r'), 'もらった額の' + pct1(t0, g0))
    ck('既定 税率の名前', raw('o-k'), '特例税率')
    ck('既定 申告', raw('o-vd'), '贈与税の申告が必要です')
    ck('既定 説明', raw('o-vds'), 'もらった額が110万円を超えています。贈与税は%s円です。翌年2月1日から3月15日までに申告して納めます' % format(t0, ','))
    # 開いた直後の画面も同じ(JS が書いたあと)
    await pg.reload()
    ck('開いた直後 税額', num(await pg.inner_text('#o-t')), t0)
    ck('開いた直後 説明', await pg.inner_text('#o-vds'), raw('o-vds'))
    # 2つの表が分かれるのは基礎控除後300万円超(もらった額410万円超)から。早見表の次の行(500万円)では違う
    ck('500万円では違う', ref(5000000, TOKUREI) != ref(5000000, IPPAN), True)
    return n, bad
run('zoyozei', body)
