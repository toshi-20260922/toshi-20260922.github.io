# /kani-kazei/ 簡易課税の事業区分と納める消費税。
# 一次情報(最後に原本を確かめた日: 2026-11-21。No.6505 と No.6509 を本文で読んだ(5,000万円以下・初日の前日まで・みなし仕入率90〜40%・75%の特例・令和9年4月1日から令和11年3月31日の引下げと簡易課税の特例の記載あり)。ほかの原本は11-20のまま):
#   国税庁 No.6505 簡易課税制度(令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6505.htm
#     基準期間の課税売上高5,000万円以下・届出書は適用を受ける課税期間の初日の前日まで・2年間は不適用届出書を出せない・
#     1種類で75%以上の特例・3種類以上で2種類の合計が75%以上の特例・区分していない場合は一番低い率・
#     令和9年4月1日〜令和11年3月31日の飲食料品の税率引下げと簡易課税の特例・2割特例と3割特例のあとの届出の特例
#   国税庁 No.6509 簡易課税制度の事業区分(令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6509.htm
#     第1種90%・第2種80%・第3種70%・第4種60%・第5種50%・第6種40%。Q&A(固定資産の売却は第4種) .../6509_qa.htm
#   国税庁 D1-22 消費税簡易課税制度選択届出手続 https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/shohi/annai/1461_13.htm
#     提出時期(事業を開始した課税期間はその課税期間中)・調整対象固定資産と高額特定資産
#   国税庁 No.6371 端数計算 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6371.htm
#     課税標準額は1,000円未満切り捨て・消費税額は1円未満切り捨て・納める税額は100円未満切り捨て
#   国税庁 No.6303(国税7.8%・地方消費税は国税の22/78)・「消費税のあらまし」010.pdf・申告書（簡易課税用）の書き方 202411_02.pdf
#   国税庁 質疑応答事例 日本標準産業分類からみた事業区分 https://www.nta.go.jp/law/shitsugi/shohi/20/03.htm (とび工事・しゅんせつ工事・植木の剪定は第4種、造園工事は第3種)
#   国税庁 令和8年度税制改正特集 https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/index.htm
#     2割特例は令和8年9月30日の属する課税期間まで・3割特例は個人事業者の令和9年分と令和10年分
# ページの JS を見ずに書いた計算:控除できる額を、使える計算(原則・1業種75%・2業種75%)を全部並べて一番大きいものにする。
# 2026-11-20 に足したもの:事業区分の表(率・納める割合・目安)、売上ごとの表の全部のマス、75%の特例の例の表、
#   決算月ごとの届出の期限の表、計算の箱の国税・地方・差し引いた額・使った率と計算の名前、10億円・1兆円・10兆円の入力。
#   ページは1つの欄が50億円で頭打ちになっていたので、10兆円までに直した(それより上は頭打ち)。
import os, sys, random, re, calendar
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
RT = [90, 80, 70, 60, 50, 40]
SHU = ['第1種', '第2種', '第3種', '第4種', '第5種', '第6種']
def mine(s):
    """原本の手順。戻り値は 合計・売上の消費税・差し引く額・国税・地方・(一番多い計算の名前と率の一覧)"""
    S = sum(s); T = (S - S % 1000) * 78 // 1000
    nz = [i for i in range(6) if s[i]]
    opts = [(sum(s[i] * RT[i] for i in range(6)) * T // (100 * S), '原則の計算（業種ごとの割合）', F(sum(s[i] * RT[i] for i in range(6)), S))]
    if len(nz) > 1:
        for i in nz:
            if s[i] * 100 >= 75 * S: opts.append((T * RT[i] // 100, SHU[i] + 'が75%以上の特例', F(RT[i])))
    if len(nz) > 2:
        for x in nz:
            for y in nz:
                if RT[x] > RT[y] and (s[x] + s[y]) * 100 >= 75 * S:
                    w = s[x] * RT[x] + (S - s[x]) * RT[y]
                    opts.append((w * T // (100 * S), SHU[x] + 'と' + SHU[y] + 'で75%以上の特例', F(w, S)))
    d = max(o[0] for o in opts); k = (T - d) // 100 * 100; ch = (k * 22 // 78) // 100 * 100
    return k + ch, T, d, k, ch, [o for o in opts if o[0] == d]
def c(n): return '{:,}'.format(n)
def pct(fr):
    v = fr * 10; r = (v.numerator * 2 + v.denominator) // (2 * v.denominator)   # 小数1けたに四捨五入
    return ('%d' % (r // 10)) if r % 10 == 0 else ('%d.%d' % (r // 10, r % 10))
CASES = [[0,0,0,0,9000000,0], [8000000,2000000,0,0,0,0], [4500000,3500000,0,0,2000000,0], [0,7000000,3000000,0,0,0],
         [0,0,0,7500000,2500000,0], [0,0,0,7499999,2500001,0], [0,0,0,0,0,999], [0,0,0,0,0,1000], [0,0,0,0,0,50000000],
         [3000000,4500000,0,0,2500000,0], [3000000,4499999,0,0,2500001,0], [1,1,1,1,1,1],
         # 大きな金額(10億円・50億円の前後・1兆円・10兆円)
         [1000000000,0,0,0,0,0], [0,0,0,0,1000000000,0], [0,0,0,0,0,1000000000], [750000000,0,0,0,250000000,0], [749999999,0,0,0,250000001,0],
         [5000000000,0,0,0,0,0], [5000000001,0,0,0,0,0], [0,0,0,0,7000000000,0], [0,6000000000,0,0,0,3000000000],
         [1000000000000,0,0,0,0,0], [0,0,0,0,1000000000000,0], [0,0,0,0,0,1000000000000], [750000000000,0,0,0,250000000000,0],
         [749999999999,0,0,0,250000000001,0], [300000000000,450000000000,0,0,250000000000,0], [300000000000,449999999999,0,0,250000000001,0],
         [1000000000000]*6, [999999999999,1,0,0,0,0], [10000000000000,0,0,0,0,0], [10000000000000]*6, [9999999999999,1234567890123,1,999,0,10000000000000]]
random.seed(20261120)
for _ in range(400):
    CASES.append([random.choice([0, 0, random.choice([random.randint(1, 30000000), random.randint(1, 900000000)])]) for _ in range(6)])
for _ in range(100):
    CASES.append([random.choice([0, 0, random.choice([random.randint(1, 5000000000), random.randint(1, 10000000000000)])]) for _ in range(6)])
def tb(i): return ':is(#%s ~ .tw):not(#%s ~ .tw ~ .tw) tbody tr' % (i, i)
async def rows(pg, i):
    return await pg.evaluate("s=>[...document.querySelectorAll(s)].map(r=>[...r.cells].map(c=>c.innerText.replace(/\\s+/g,'')))", tb(i))
async def body(pg):
    n = bad = 0
    def ck(ok, *msg):
        nonlocal n, bad
        n += 1
        if not ok: bad += 1; print('NG', *msg)
    for s in CASES:
        if sum(s) == 0: continue
        for i in range(6): await pg.fill('#s%d' % i, str(s[i]))
        tot, T, d, k, ch, best = mine(s)
        o = await pg.evaluate("['o-t','o-k','o-te','o-how','o-r','o-re'].map(i=>document.getElementById(i).innerText)")
        ck(num(o[0]) == tot, s, '合計', o[0], tot)
        ck(num(o[1]) == T, s, '売上の消費税', o[1], T)
        ck(o[2] == '国税%s円・地方%s円' % (c(k), c(ch)), s, '内訳', o[2], k, ch)
        ck(o[3].startswith('売上の消費税%s円から%s円を差し引いています' % (c(T), c(d))), s, '差し引く額', o[3], T, d)
        ck(any(o[5] == b[1] and abs(F(o[4].replace('%', '')) - b[2]) <= F(1, 20) for b in best), s, '率と計算の名前', o[4], o[5], [(b[1], float(b[2])) for b in best])
    # 業種を選ぶと、表と同じ区分が出るか
    html = await pg.content()
    rei = dict(re.findall(r'<tr><td class="l">([^<]+)</td><td>(第\d種)</td>', html))
    ck(len(rei) == 39, '業種の例の行の数', len(rei))
    opts = await pg.evaluate("[...document.querySelectorAll('#ex option')].map(o=>[o.value,o.text])")
    for v, t in opts:
        await pg.select_option('#ex', v); vd = await pg.inner_text('#o-vd'); vs = await pg.inner_text('#o-vds')
        g = rei.get(t); r = RT[SHU.index(g)] if g else -1
        ck(g and vd == '%s（みなし仕入率%d%%）です' % (g, r) and vs.endswith('売上の消費税の%d%%を納めます' % (100 - r)), '区分', t, vd, vs, g)
    # 事業区分の表:率・納める割合・目安(本則課税と比べて、課税仕入れが売上の何%未満なら簡易課税が少ないか)
    kb = await rows(pg, 'kubun'); ck(len(kb) == 6, '事業区分の表の行の数', len(kb))
    for i, r in enumerate(kb[:6]):
        # 自分の計算:売上1,000万円(税抜)で、仕入れの割合を1%ずつ動かして簡易課税が少なくなる一番上の割合を出す
        S = 10000000; kani = mine([S if j == i else 0 for j in range(6)])[0]; top = None
        for p in range(0, 101):
            kk = (S * 78 // 1000 - S * p // 100 * 78 // 1000) // 100 * 100; hon = kk + kk * 22 // 78 // 100 * 100
            if kani < hon: top = p
        ck(r[0] == SHU[i] and r[1] == '%d%%' % RT[i] and r[2] == '%d%%' % (100 - RT[i]), '事業区分の表', r[:3])
        ck(top == RT[i] - 1 and r[3] == '課税仕入れが売上の%d%%未満' % RT[i], '目安の列', r[3], top)
    # 売上ごとの納める消費税の表(全部のマス)
    gk = await rows(pg, 'gaku'); ck(len(gk) == 6, '売上ごとの表の行の数', len(gk))
    for i, r in enumerate(gk[:6]):
        ck(r[0] == '%s（%d%%）' % (SHU[i], RT[i]), '売上ごとの表の見出し', r[0])
        for j, S in enumerate([5000000, 10000000, 30000000, 50000000]):
            want = mine([S if x == i else 0 for x in range(6)])[0]
            ck(num(r[j + 1]) == want, '売上ごとの表', SHU[i], S, r[j + 1], want)
    # 75%の特例の例の表(内訳の文字から売上を読み、計算の名前・率・納める額を出す)
    tk = await rows(pg, 'tokurei'); ck(len(tk) == 4, '特例の例の表の行の数', len(tk))
    for r in tk:
        s = [0] * 6
        for a, b in re.findall(r'第(\d)種(\d+)万円', r[0]): s[int(a) - 1] = int(b) * 10000
        ck(sum(s) == 10000000, '特例の例の合計', r[0], sum(s))
        tot, T, d, k, ch, best = mine(s)
        ck(any(b[1].startswith(r[1]) and pct(b[2]) + '%' == r[2] for b in best) and num(r[3]) == tot, '特例の例', r, tot, [(b[1], pct(b[2])) for b in best])
    # 届出の期限の表(法人。期の初日の前日=決算月の末日。うるう年でない年で見る)
    kg = await rows(pg, 'kigen'); ck(len(kg) == 12, '届出の期限の表の行の数', len(kg))
    for m, r in enumerate(kg[:12], 1):
        want = ['%d月' % m, '%d月1日' % (m % 12 + 1), '%d月%d日' % (m, calendar.monthrange(2027, m)[1])]
        ck(r == want, '届出の期限', r, want)
    ck('2月の期限はうるう年なら29日です' in html and calendar.monthrange(2028, 2)[1] == 29, 'うるう年の注記')
    # 本文の例(第5種900万円)を自分の計算から組み立てる
    tot, T, d, k, ch, best = mine([0, 0, 0, 0, 9000000, 0])
    want = '第5種で売上900万円なら、売上の消費税（国税）は%s円です。50%%の%s円を差し引いて国税%s円、地方消費税%s円で合計%s円です。' % (c(T), c(d), c(k), c(ch), c(tot))
    ck(want in html, '本文の例', want)
    # 計算のしかたの表の端数処理の言葉
    ks = await rows(pg, 'keisan')
    for i, w in enumerate(['1,000円未満を切り捨てる', '7.8%', '100円未満を切り捨てる', '22/78']):
        ck(len(ks) == 4 and w in ks[i][1], '計算のしかた', i + 1, w)
    ck('1円未満を切り捨てる' in ks[1][1] and '100円未満を切り捨てる' in ks[3][1], '計算のしかたの端数')
    # 計算の箱に直に書いた既定の結果(JS が動く前の HTML)を、既定の入力(税理士ほか・第5種900万円)の自分の計算と比べる(2026-11-21)
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'kani-kazei', 'index.html'), encoding='utf-8').read()
    tot, T, d, k, ch, best = mine([0, 0, 0, 0, 9000000, 0])
    for w in ('<b id="o-t">%s<i>円</i></b><em id="o-te">国税%s円・地方%s円</em>' % (c(tot), c(k), c(ch)),
              '<b id="o-r">%s<i>%%</i></b><em id="o-re">%s</em>' % (pct(best[0][2]), best[0][1]),
              '<b id="o-k">%s<i>円</i></b>' % c(T),
              '<li id="o-how">売上の消費税%s円から%s円を差し引いています。控除が一番多くなる計算を選んでいます</li>' % (c(T), c(d)),
              '<b id="o-vd">第5種（みなし仕入率50%）です</b><span id="o-vds">税理士・社労士・デザイン・経営コンサルタントは第5種です。専門サービス業は第5種です。売上の消費税の50%を納めます</span>',
              'value="26" selected', 'id="s4" inputmode="numeric" min="0" max="10000000000000" step="1" value="9000000"'):
        ck(w in raw, '既定の結果', w)
    # 飲食料品の税率引下げは法案の段階(2026-11-21 未成立)。成立したと言い切る文が無いこと
    ck('法案は' in raw and '成立した場合は' in raw and '消費税率が下がり、' not in raw, '飲食料品の税率引下げの文')
    # 条件の数字
    for w in ('基準期間の課税売上高が5,000万円以下', '基準期間の課税売上高が5,000万円を超える課税期間は使えません', '一度使い始めると2年間はやめられません',
              '使いたい課税期間が始まる日の前日まで', '令和9年4月1日から令和11年3月31日まで', '全部に70%を使います'):
        ck(w in html, '条件の文', w)
    return n, bad
run('kani-kazei', body)
