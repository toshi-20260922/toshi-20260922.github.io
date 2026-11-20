# /soneki-bunkiten/ 損益分岐点の計算。
# 原本:
#  中小企業基盤整備機構 J-Net21「損益分岐点の計算方法と経営改善に向けた活用方法を教えてください。」
#   https://j-net21.smrj.go.jp/qa/financial/Q0240.html
#   (変動費率=変動費÷売上高・限界利益=売上高−変動費・損益分岐点売上高=固定費÷(1−変動費率)・安全余裕率=(売上高−損益分岐点売上高)÷売上高×100)
#  J-Net21「損益分岐点を使った目標売上高」 https://j-net21.smrj.go.jp/startup/manual/list5/5-2-9.html
#   (損益分岐点売上高=固定費÷限界利益率・必要売上高=(固定費+目標利益)÷(1−変動費率))
#  中小企業庁 2026年版 小規模企業白書 第2部第1章 第2-1-16図の注
#   https://www.chusho.meti.go.jp/pamflet/hakusyo/2026/PDF/shokibo/04sHakusho_part2_chap1_web.pdf (ファイル名は Hakusho。Hakusyo では開けない)
#   (注3 損益分岐点売上高=固定費÷(1−変動費÷売上高)・注4 損益分岐点比率(%)=損益分岐点売上高÷売上高×(数字)。
#    2026-11-21 に開いた。取り出した文字は半角の数字が全部欠けていて「×」のあとの数字は読めない。「(%)」と「×」があるところまでは読めた)
#  日本政策金融公庫「ベテラン中小企業診断士が、分かりやすく解説～アフターコロナを見据えた「収益改善策」を考える～」(2022年9月)
#   https://www.jfc.go.jp/n/service/pdf/shindanshi_20220921.pdf
#   (変動費=原材料費・仕入原価・外注費・水道光熱費・アルバイト人件費など/固定費=賃借料・減価償却費・役員と従業員の人件費・支払利息など/損益分岐点=固定費÷(1−(変動費÷売上高)))
#  日本政策金融公庫「第6回 赤字にならない売上はいくら？」 https://www.jfc.go.jp/n/finance/sougyou/column/202303/index.html (2026-11-21 は開けなかった)
# 端数処理は原本に決まりが無い。画面は円を四捨五入・%を小数第1位で四捨五入しているので、分数で出した値を同じ桁で四捨五入して比べる。
# 安全余裕率は「100 − 画面の損益分岐点比率」と同じになること(ページの注記「足すと100%」)も確かめる。
# 2026-11-21:画面の四捨五入を整数の計算(BigInt)に直したので、売上高が億円より上で円がちょうど .5 になる組を足した(直す前は1円ずれた)。
#  表の下の注(#o-3)が入力ごとに合う文か・売上高0円の限界利益率が「—%」か・計算の箱に直に書いた既定の結果・目次の順も照らす。
# 最後に原本を確かめた日:2026-11-21(J-Net21 Q0240・J-Net21 5-2-9・小規模企業白書・日本政策金融公庫の2022年9月の資料)
import os, sys, re, random
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

def rnd(x):
    """四捨五入(0.5は0から遠いほうへ)。x は Fraction。"""
    a = abs(x)
    v = (a.numerator * 2 + a.denominator) // (2 * a.denominator)
    return -v if x < 0 else v
def yen(v):
    return ('−' if v < 0 else '') + format(abs(v), ',')
def pct(t10):
    """10倍した整数を 12.3 の形に。"""
    return ('−' if t10 < 0 else '') + '%d.%d' % (abs(t10) // 10, abs(t10) % 10)

def ref(S, V, F):
    m = S - V
    ok = S > 0 and m > 0
    o = {'m': m, 'pf': m - F, 'ok': ok}
    o['mr10'] = rnd(Fr(m * 1000, S)) if S > 0 else None   # 売上高が0円なら限界利益率(限界利益÷売上高)は決まらない
    if ok:
        bep = Fr(F * S, m)                 # 固定費 ÷ (1 − 変動費 ÷ 売上高)
        o['bep'] = rnd(bep)
        o['br10'] = rnd(bep / S * 1000)    # 損益分岐点売上高 ÷ 売上高 × 100
        o['an_exact'] = (S - bep) / S * 100  # (売上高 − 損益分岐点売上高) ÷ 売上高 × 100
        o['gap'] = rnd(abs(S - bep))
    rows = []
    for d in (-30, -20, -10, 0, 10, 20, 30):
        s = Fr(S * (100 + d), 100)
        mm = Fr(m * (100 + d), 100)        # 変動費率が同じなら限界利益も同じ割合で動く
        rows.append((rnd(s), rnd(mm), rnd(mm - F)))
    o['rows'] = rows
    return o

CASES = [
    (50000000, 30000000, 17000000),      # 画面の既定・ページの計算例(4,250万円・85%・15%)
    (1000000, 800000, 300000),           # J-Net21 Q0240 の例を月の売上100万円に当てたもの(分岐点150万円)
    (1000000, 500000, 200000),           # J-Net21 5-2-9 の例(分岐点40万円)
    (3000000, 900000, 1500000),          # 低い
    (120000000, 78000000, 36000000),     # 中くらい
    (9800000000, 6370000000, 2900000000),# 高い
    (50000000, 30000000, 20000000),      # 利益ちょうど0
    (50000000, 30000000, 19999999),      # 利益 +1円
    (50000000, 30000000, 20000001),      # 利益 −1円
    (50000000, 49999999, 17000000),      # 変動費が売上高の1円下
    (50000000, 50000000, 17000000),      # 変動費が売上高ちょうど
    (50000000, 50000001, 17000000),      # 変動費が売上高の1円上
    (50000000, 80000000, 17000000),      # 限界利益がマイナス
    (0, 0, 0), (0, 0, 17000000), (0, 1000, 17000000), (0, 30000000, 17000000), (1, 1, 0), (1, 0, 0),
    (50000000, 30000000, 0), (50000000, 0, 17000000), (50000000, 0, 0),
    (40000000, 0, 34100000),             # 比率がちょうど85.25%(四捨五入の境目)
    (40000000, 0, 48100000),             # 比率がちょうど120.25%
    (40000000, 0, 40020000),             # 比率100.05%
    (40000000, 0, 40010000),             # 比率100.025%(安全余裕率が0に丸まる)
    (40000000, 0, 39990000),             # 比率99.975%
    (3, 1, 1), (7, 3, 5), (1, 0, 1), (999, 333, 777), (1234567, 765433, 345678),
    (33333333, 11111111, 22222222), (900000000000, 630000000000, 250000000000),
    (2000, 1999, 1), (2000, 1, 3000), (50000050, 30000030, 17000017),
]
random.seed(20261119)
for _ in range(300):
    S = random.choice([random.randint(1, 10**4), random.randint(10**5, 10**8), random.randint(10**8, 10**11)])
    V = random.randint(0, S + S // 10)
    F = random.randint(0, S)
    CASES.append((S, V, F))
# 四捨五入の境目(比率が x.x5% ちょうど・円が .5 ちょうど)をねらった組
for k in range(1, 60):
    m = 2000 * k
    CASES.append((m + 1000, 1000, (2 * k * 7 + 1)))          # 比率 = F*100/m が .x5 になりやすい
    CASES.append((2 * k + 1, 2 * k - 1, k))                   # 分岐点 = F*S/2 が .5 になる(S が奇数で F が奇数のとき)

# 2026-11-21:金額が大きく、円がちょうど .5 になる組(小数の計算では1円ずれた)
CASES += [(186257622, 62085874, 293678863), (3261157910, 1956694746, 4304012711), (13554552669, 9681823335, 45199786733),
          (2627325819, 875775273, 4630706461), (4993478650, 2996087190, 3141433361), (20245179162, 6748393054, 9347033819)]
random.seed(20261121)
for _ in range(120):
    k = random.choice([10**7, 10**8, 10**9, 10**10])
    h = random.randint(1, k); F = random.randint(1, 5 * k) | 1
    S = h * random.choice([3, 5, 7]); CASES.append((S, S - 2 * h, F))      # 限界利益 2h・売上高 h×奇数 → 分岐点が .5
    CASES.append((S + random.randint(0, k), S - 2 * h, F))
# 注の文が変わる境目
CASES += [(50000000, 30000000, 0), (50000000, 50000000, 0), (50000000, 60000000, 0), (50000000, 30000000, 20000000),
          (50000000, 30000000, 25000000), (0, 0, 0), (0, 500, 100)]

NOTE0 = '利益がマイナスの行は赤字です。'
def note(S, V, F):
    """表の下の注。売上高が d% 動くと 限界利益は m×(100+d)/100・利益は そこから F を引いた額(自分で式から出した動き)。"""
    m = S - V
    if S == 0: return NOTE0
    if m < 0: return NOTE0 + '変動費が売上高を上回っているので、売上高が増えるほど赤字は大きくなります。'
    if m == 0: return NOTE0 + '変動費が売上高と同じなので、売上高が増減しても利益は変わりません。'
    if F == 0: return NOTE0 + '固定費が0円なので、利益は売上高と同じ割合で増減します。'
    if m - F > 0: return NOTE0 + '売上高が減っても固定費は減らないので、利益は売上高より大きな割合で減ります。'
    if m - F == 0: return NOTE0 + '売上高が減っても固定費は減らないので、売上高が減ると赤字になります。'
    return NOTE0 + '売上高が減っても固定費は減らないので、売上高が減ると赤字は大きくなります。'
def note_ok(S, V, F, rows):
    """注の文が、表の数字(自分の計算)の動きと合っているか。rows は (売上高, 限界利益, 利益) の7行(−30%〜+30%)。"""
    m = S - V; pf = [Fr(m * (100 + d), 100) - F for d in (-30, -20, -10, 0, 10, 20, 30)]
    if S == 0: return True
    if m < 0: return all(pf[i] > pf[i + 1] for i in range(6)) and pf[6] < 0          # 売上高が増えるほど赤字が大きい
    if m == 0: return len(set(pf)) == 1                                              # 利益は変わらない
    if F == 0: return all(pf[i] * 100 == pf[3] * (100 + d) for i, d in enumerate((-30, -20, -10, 0, 10, 20, 30)))  # 同じ割合
    if m - F > 0: return all((pf[3] - pf[i]) / pf[3] > Fr(-d, 100) for i, d in ((0, -30), (1, -20), (2, -10)))     # 売上高より大きな割合で減る
    if m - F == 0: return all(pf[i] < 0 for i in range(3))                           # 減ると赤字
    return pf[0] < pf[1] < pf[2] < pf[3] < 0                                         # 減ると赤字が大きくなる

HTML_REI = [  # ページに手で書いた計算例(万円)と、よくある質問の例
    ('変動費率 60%', lambda: Fr(3000, 5000) * 100 == 60),
    ('限界利益率 40%', lambda: (1 - Fr(3000, 5000)) * 100 == 40),
    ('損益分岐点売上高 4,250万円', lambda: Fr(1700) / (1 - Fr(3000, 5000)) == 4250),
    ('損益分岐点比率 85%', lambda: Fr(4250, 5000) * 100 == 85),
    ('安全余裕率 15%', lambda: Fr(5000 - 4250, 5000) * 100 == 15),
    ('15%は750万円', lambda: 5000 - 4250 == 750 and Fr(5000 * 15, 100) == 750),
    ('限界利益2,000万円・利益300万円', lambda: 5000 - 3000 == 2000 and 2000 - 1700 == 300),
    ('目標利益500万円で5,500万円', lambda: 1700 + 500 == 2200 and Fr(2200) / Fr(40, 100) == 5500),
]

async def body(pg):
    n = bad = 0
    html = await pg.content()
    for name, fn in HTML_REI:
        n += 1
        if not fn():
            bad += 1; print('NG 計算例', name)
    for s in ['3,000万円 ÷ 5,000万円 ＝ 60%', '1 − 60% ＝ 40%', '1,700万円 ÷ 40% ＝ 4,250万円', '4,250万円 ÷ 5,000万円 ＝ 85%',
              '100% − 85% ＝ 15%', '15%（750万円）', '限界利益2,000万円から固定費1,700万円を引いた300万円', '2,200万円 ÷ 40% ＝ 5,500万円']:
        n += 1
        if s not in html:
            bad += 1; print('NG ページに文が無い', s)
    # 計算の箱に直に書いた既定の結果(JS が書き換える前の文)と更新前の注。ファイルの文字を直に読む
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'soneki-bunkiten', 'index.html'), encoding='utf-8').read()
    S0, V0, F0 = [int(re.search(r'id="%s"[^>]*value="([0-9,]+)"' % i, raw).group(1).replace(',', '')) for i in ('sal', 'vc', 'fc')]
    e0 = ref(S0, V0, F0)
    for s in ['<b id="o-a">%s<i>円</i></b>' % format(e0['bep'], ','), '<b id="o-b">%s<i>%%</i></b>' % pct(e0['br10']),
              '<b id="o-c">%s<i>%%</i></b>' % pct(1000 - e0['br10']),
              '<li id="o-1">限界利益%s円・限界利益率%s%%・利益%s円</li>' % (yen(e0['m']), pct(e0['mr10']), yen(e0['pf'])),
              '<li id="o-2">売上高が%s円減ると、利益が0になります</li>' % format(e0['gap'], ','),
              ' id="o-3">%s</p>' % note(S0, V0, F0)]:
        n += 1
        if s not in raw:
            bad += 1; print('NG 直に書いた既定の結果', s)
    # 目次の順が画面の見出し(h2)の順と同じで、行き先が同じ文字の見出しであること・id の重なりが無いこと
    toc = await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>a.getAttribute('href').slice(1))")
    h2 = await pg.eval_on_selector_all('main h2[id]', "hs=>hs.map(h=>h.id)")
    n += 1
    if toc != h2:
        bad += 1; print('NG 目次の順', toc, h2)
    same = await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>{var e=document.getElementById(a.getAttribute('href').slice(1));return !!e&&e.innerText.replace(/\\s+/g,'')===a.textContent.replace(/\\s+/g,'')})")
    n += 1
    if not all(same):
        bad += 1; print('NG 目次の文字と見出し', same)
    ids = await pg.eval_on_selector_all('[id]', 'es=>es.map(e=>e.id)'); n += 1
    if len(ids) != len(set(ids)):
        bad += 1; print('NG id の重なり', sorted(set(i for i in ids if ids.count(i) > 1)))
    for S, V, F in CASES:
        for i, v in (('sal', S), ('vc', V), ('fc', F)):
            await pg.fill('#' + i, str(v))
        g = await pg.evaluate('''()=>({a:document.getElementById("o-a").textContent,b:document.getElementById("o-b").textContent,
          c:document.getElementById("o-c").textContent,nt:document.getElementById("o-3").textContent,l1:document.getElementById("o-1").textContent,l2:document.getElementById("o-2").textContent,
          rows:[...document.querySelectorAll("#tb tr")].map(r=>[...r.cells].map(c=>c.textContent))})''')
        e = ref(S, V, F)
        exp = {}
        if e['ok']:
            an10 = 1000 - e['br10']
            exp['a'] = format(e['bep'], ',') + '円'
            exp['b'] = pct(e['br10']) + '%'
            exp['c'] = pct(an10) + '%'
            exp['l2'] = ('売上高が%s円減ると、利益が0になります' % format(e['gap'], ',')) if e['pf'] >= 0 else \
                        ('売上高があと%s円増えると、利益が0になります' % format(e['gap'], ','))
            n += 1  # 画面の安全余裕率が、原本の式の値から0.05ポイントより離れていないこと
            if abs(Fr(an10, 10) - e['an_exact']) > Fr(1, 20):
                bad += 1; print('NG 安全余裕率が原本の式と離れている', S, V, F, pct(an10), float(e['an_exact']))
        else:
            exp['a'] = '—円'; exp['b'] = '—%'; exp['c'] = '—%'
            # 売上高が0円のときは変動費率(変動費÷売上高)が決まらないので、別の文になる
            exp['l2'] = '売上高が0円なので、損益分岐点売上高を計算できません' if S == 0 else '変動費が売上高以上なので、売上高を増やしても黒字になりません'
        exp['l1'] = '限界利益%s円・限界利益率%s%%・利益%s円' % (yen(e['m']), '—' if e['mr10'] is None else pct(e['mr10']), yen(e['pf']))
        exp['nt'] = note(S, V, F)
        n += 1
        if not note_ok(S, V, F, e['rows']):
            bad += 1; print('NG 注の文が表の動きと合わない', (S, V, F))
        exp['rows'] = [[('+' if d > 0 else ('−' if d < 0 else '')) + '%d%%' % abs(d), format(r[0], ','), yen(r[1]), yen(r[2])]
                       for d, r in zip((-30, -20, -10, 0, 10, 20, 30), e['rows'])]
        for k in ('a', 'b', 'c', 'l1', 'l2', 'nt', 'rows'):
            n += 1
            if g[k] != exp[k]:
                bad += 1; print('NG', (S, V, F), k, '画面', g[k], '自分の計算', exp[k])
        # window に出ている関数も同じ値か
        w = await pg.evaluate('([S,V,F])=>window.__sb.calc(S,V,F)', [S, V, F]); n += 1
        if w['m'] != e['m'] or w['pf'] != e['pf'] or bool(w['ok']) != e['ok']:
            bad += 1; print('NG __sb.calc', (S, V, F), w)
    return n, bad
run('soneki-bunkiten', body)
