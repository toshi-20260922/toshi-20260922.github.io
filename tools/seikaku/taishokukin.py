# /taishokukin/ 退職金の税金の計算(手取り・税金の合計・退職所得控除・早見表)。
# 原本:
#  国税庁 No.1420 退職金を受け取ったとき(退職所得) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1420.htm
#   (退職所得控除 40万円×年数・80万円の下限・20年超は800万円+70万円×(年数-20)・2分の1・申告書を出さないと20.42%)
#  国税庁 No.2732 退職手当等に対する源泉徴収 https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2732.htm
#   (課税退職所得金額の式:一般・特定役員・短期の300万円超は 150万円+{収入-(300万円+控除)}・1,000円未満切り捨て)
#  国税庁 別紙 退職所得の源泉徴収税額の速算表 https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2732_besshi.htm
#   (税額=(A×B-C)×102.1%・1円未満切り捨て)
#  総務省 平成25年1月1日以降の退職所得に対する住民税の特別徴収について https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/65871.html
#   (市町村民税6%・道府県民税4%・それぞれ100円未満切り捨て)
#  国税庁 No.4117 相続税の課税対象になる死亡退職金 https://www.nta.go.jp/taxes/shiraberu/taxanswer/sozoku/4117.htm
#   (死亡後3年以内に支給が確定したものが相続税の対象)
# 最後に原本を確かめた日:2026-11-20
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

# 別紙の速算表(課税退職所得金額の上限・率%・控除額)
SOKUSAN = [(1950000, 5, 0), (3300000, 10, 97500), (6950000, 20, 427500), (9000000, 23, 636000),
           (18000000, 33, 1536000), (40000000, 40, 2796000), (None, 45, 4796000)]

def kojo(n):
    if n <= 20:
        return max(800000, 400000 * n)
    return 8000000 + 700000 * (n - 20)

def kazei(g, n, yakuin):
    """No.2732 の式。2倍した値で持って最後に割り、1,000円未満を切り捨てる。"""
    k = kojo(n)
    r = g - k
    if r <= 0:
        return 0
    if n <= 5 and yakuin:            # 特定役員退職手当等
        x2 = 2 * r
    elif n <= 5 and r > 3000000:     # 短期退職手当等で300万円超
        x2 = 2 * (1500000 + (g - (3000000 + k)))
    else:                            # 一般、または短期で300万円以下
        x2 = r
    return x2 // 2 // 1000 * 1000

def ref(g, n, yakuin):
    a = kazei(g, n, yakuin)
    for top, rate, c in SOKUSAN:
        if top is None or a <= top:
            base = a * rate // 100 - c       # a は1,000円単位なので割り切れる
            break
    it = max(0, base) * 1021 // 1000         # ×102.1% のあと1円未満切り捨て
    shi = a * 6 // 100 // 100 * 100
    ken = a * 4 // 100 // 100 * 100
    return {'k': kojo(n), 'inc': a, 'it': it, 'ju': shi + ken, 'tax': it + shi + ken, 'net': g - it - shi - ken}

READ = '''([g,n])=>{var a=document.getElementById("amt"),y=document.getElementById("yrs");
a.value=String(g);a.dispatchEvent(new Event("input",{bubbles:true}));
y.value=String(n);y.dispatchEvent(new Event("input",{bubbles:true}));
var t=function(i){return document.getElementById(i).textContent};
return {n:t("o-n"),t:t("o-t"),k:t("o-k"),br:t("o-br"),sh:t("o-sh"),vd:t("o-vd"),vds:t("o-vds"),nr:t("o-nr"),
rows:[].map.call(document.querySelectorAll("#tb tr"),function(r){return [].map.call(r.cells,function(c){return c.textContent})})}}'''

async def body(pg):
    n = bad = 0
    def ng(*a):
        nonlocal bad
        bad += 1
        print('NG', *a)

    base_gs = [0, 1, 799999, 800000, 800001, 1000000, 4000000, 5000000, 8000000, 8001000, 15000000, 15000001,
               15001999, 15002000, 20000000, 30000000, 50000000, 90000000, 150000000, 300000000]
    years = (1, 2, 3, 5, 6, 10, 19, 20, 21, 30, 38, 45, 60)
    for yak in (0, 1):
        await pg.click('#s-y button[data-v="%d"]' % yak)
        for yrs in years:
            gs = list(base_gs)
            k = kojo(yrs)
            # 退職所得控除ちょうどの前後
            gs += [k - 1, k, k + 1, k + 1999, k + 2000]
            # 速算表の境目の前後(課税退職所得がちょうど境目になる退職金)
            for top, _, _ in SOKUSAN[:-1]:
                if yrs <= 5 and yak:
                    g0 = top + k
                elif yrs <= 5 and top > 1500000:
                    g0 = top + 1500000 + k
                else:
                    g0 = top * 2 + k
                gs += [g0 - 2000, g0 - 1, g0, g0 + 1, g0 + 999, g0 + 1000, g0 + 1999, g0 + 2000]
            if yrs <= 5:   # 短期退職手当等の300万円の前後
                g0 = k + 3000000
                gs += [g0 - 2000, g0 - 1, g0, g0 + 1, g0 + 999, g0 + 1000, g0 + 2000]
            for g in gs:
                got = await pg.evaluate(READ, [g, yrs])
                e = ref(g, yrs, yak); n += 1
                m = re.search(r'所得税([\d,]+)円・住民税([\d,]+)円', got['br'])
                shown = {'net': num(got['n']), 'tax': num(got['t']), 'k': num(got['k']),
                         'it': num(m.group(1)), 'ju': num(m.group(2)), 'inc': num(got['sh'])}
                if any(shown[x] != e[x] for x in shown):
                    ng(g, yrs, yak, shown, e); continue
                # 結論の箱
                if e['tax']:
                    m2 = re.search(r'所得税([\d,]+)円・住民税([\d,]+)円', got['vds'])
                    if num(got['vd']) != e['net'] or not m2 or num(m2.group(1)) != e['it'] or num(m2.group(2)) != e['ju']:
                        ng('結論の箱', g, yrs, yak, got['vd'], got['vds'])
                else:
                    if 'かかりません' not in got['vd'] or num(re.search(r'控除の([\d,]+)円', got['vds']).group(1)) != e['k']:
                        ng('結論の箱(0円)', g, yrs, yak, got['vd'], got['vds'])
                # 手取りの割合(小数1位・四捨五入)
                pct = (2000 * e['net'] + g) // (2 * g) if g else 0
                want = '退職金の%s%%' % (str(pct // 10) if pct % 10 == 0 else '%d.%d' % (pct // 10, pct % 10))
                if got['nr'] != want:
                    ng('割合', g, yrs, yak, got['nr'], want)

    # 早見表の全行(従業員・勤続20年・30年・38年)。役員を選んでいても従業員の額のままか確かめる
    for yak in (1, 0):
        await pg.click('#s-y button[data-v="%d"]' % yak)
        got = await pg.evaluate(READ, [20000000, 30])
        man = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
        if len(got['rows']) != len(man):
            ng('早見表の行数', len(got['rows']))
        for row, m in zip(got['rows'], man):
            n += 1
            want = [m] + [ref(m * 10000, y, 0)['net'] for y in (20, 30, 38)]
            if [num(c) for c in row] != want:
                ng('早見表', row, want)

    # 手で書いた文の数字
    html = await pg.content()
    txt = await pg.inner_text('main')
    n += 1   # 勤続30年の退職所得控除
    if kojo(30) != 15000000 or '勤続30年なら、1,500万円までの退職金には税金がかかりません' not in txt:
        ng('勤続30年・1,500万円の文')
    n += 1   # よく聞かれること:2,000万円・勤続30年
    e = ref(20000000, 30, 0)
    qa = await pg.inner_text('#qa1')
    if 'およそ%s万円' % format(e['net'] // 10000, ',') not in qa or 'およそ%d万円' % ((e['tax'] + 5000) // 10000) not in qa:
        ng('よく聞かれることの額', qa, e)
    n += 1   # 退職所得控除の表
    if '40万円×勤続年数（80万円に満たないときは80万円）' not in txt or '800万円＋70万円×（勤続年数−20年）' not in txt:
        ng('退職所得控除の表の文')
    n += 1   # 申告書を出さないとき
    if '20.42%' not in txt:
        ng('20.42%の文')
    n += 1   # 短期退職手当等の300万円
    if '300万円を超える部分は2分の1にしません' not in txt:
        ng('300万円の文')
    n += 1   # 重複期間(No.2732:前年以前9年内・令和8年1月1日以後・改正前4年内)
    if '前年以前9年内' not in txt or '令和8年1月1日以後' not in txt or '改正前は4年内' not in txt:
        ng('9年内の文')
    # ---- 2026-11-20 に足された部品 ----
    # 退職所得控除を勤続年数ごとに並べた表(手で書いた全行)
    rows = await pg.evaluate("""()=>{var t=[].filter.call(document.querySelectorAll('main table'),function(t){return t.tHead&&t.tHead.textContent.indexOf('税金がかからない額')>=0});
    return t.length==1?[].map.call(t[0].tBodies[0].rows,function(r){return [].map.call(r.cells,function(c){return c.textContent})}):null}""")
    ys = [5, 10, 15, 20, 25, 30, 35, 40]
    if not rows or len(rows) != len(ys):
        ng('控除の表の行数', rows)
    else:
        for row, y in zip(rows, ys):
            n += 1
            want = ['%d年' % y, '%s万円' % format(kojo(y) // 10000, ',')]
            if row != want or kojo(y) % 10000:
                ng('控除の表', row, want)
    # 勤続30年の税金の内訳の表(全行・全列)と黄色の行(入力を超えない中でいちばん近い行)
    man = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000]
    T2 = """([g])=>{var a=document.getElementById("amt");a.value=String(g);a.dispatchEvent(new Event("input",{bubbles:true}));
    var f=function(id){var rs=document.querySelectorAll("#"+id+" tr");return {rows:[].map.call(rs,function(r){return [].map.call(r.cells,function(c){return c.textContent})}),hit:[].map.call(rs,function(r,i){return r.classList.contains("hit")?i:-1}).filter(function(i){return i>=0})}};
    return {a:f("tb"),b:f("tb2")}}"""
    for yak in (1, 0):
        await pg.click('#s-y button[data-v="%d"]' % yak)
        for g in (0, 4999999, 5000000, 9999999, 10000000, 19999999, 20000000, 24000000, 29999999, 30000000,
                  39999999, 40000000, 49999999, 50000000, 300000000):
            got = await pg.evaluate(T2, [g])
            hit = [i for i, m in enumerate(man) if g >= m * 10000][-1:]
            n += 1
            if got['a']['hit'] != hit or got['b']['hit'] != hit:
                ng('黄色の行', g, got['a']['hit'], got['b']['hit'], hit)
            if len(got['b']['rows']) != len(man):
                ng('内訳の表の行数', len(got['b']['rows'])); continue
            for row, m in zip(got['b']['rows'], man):
                n += 1
                G = m * 10000
                e = ref(G, 30, 0)
                p10 = (2000 * e['tax'] + G) // (2 * G)       # 税金÷退職金(%・小数1位・四捨五入)
                want = [format(m, ','), format(e['inc'], ','), format(e['it'], ','), format(e['ju'], ','),
                        format(e['net'], ','), '%d.%d%%' % (p10 // 10, p10 % 10)]
                if row != want:
                    ng('内訳の表', row, want)
    n += 1   # 黄色の行の文
    if '入力した退職金を超えない中でいちばん近い行が黄色になります' not in txt:
        ng('黄色の行の文')
    n += 1   # 内訳の表の前の文(控除の1,500万円)
    if kojo(30) != 15000000 or '控除の1,500万円を引いて2分の1にした額' not in txt:
        ng('内訳の表の前の文')
    n += 1   # 勤続年数の数え方(20年3か月は切り上げて21年・20年超は1年ごとに70万円)
    if kojo(21) - kojo(20) != 700000 or kojo(22) - kojo(21) != 700000 or \
       '勤続20年3か月なら21年として控除を計算します' not in txt or '1年ごとに控除が70万円増える' not in txt:
        ng('勤続年数の数え方の文')
    n += 1   # 役員の勤続5年以下(特定役員退職手当等)
    if '役員として勤続5年以下で受け取る退職金は、2分の1にしません' not in txt:
        ng('役員5年以下の文')
    n += 1   # 関連リンクの文:所得税の税率は5%から45%
    if (SOKUSAN[0][1], SOKUSAN[-1][1]) != (5, 45) or '5%から45%まで' not in txt:
        ng('5%から45%の文')
    n += 1   # 住民税の内訳の文
    if '市区町村民税6%と道府県民税4%の合計' not in txt:
        ng('6%と4%の文')
    n += 1   # 亡くなった人の退職金(No.4117:死亡後3年以内に支給が確定)
    if '亡くなってから3年以内に支給が確定' not in txt:
        ng('死亡退職金の3年の文')
    n += 1   # 確定申告(No.1420:原則として不要)
    if 'そのため原則として確定申告はいりません' not in txt:
        ng('確定申告の文')
    return n, bad

run('taishokukin', body)
