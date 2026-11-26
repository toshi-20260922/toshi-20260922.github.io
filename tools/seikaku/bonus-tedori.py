# /bonus-tedori/ ボーナス手取り計算(賞与から社会保険料と所得税を引いた手取り)。
# 原本:
#  国税庁 タックスアンサー No.2523 賞与に対する源泉徴収(率の表の使い方・前月の給与が無いとき・10倍を超えるとき。6か月を超える期間は12)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2523.htm
#  国税庁「賞与に対する源泉徴収税額の算出率の表(令和8年分)」甲欄(下の R8。/shoyo-shotokuzei/ の点検と同じ原本)
#   https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/15-16.pdf
#  国税庁「給与所得の源泉徴収税額表(令和8年分)月額表」甲欄の全行(PDF から写した tools/getsugaku_r8.json。740,000円以上は表の式)
#   https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/01-07.pdf
#  日本年金機構「従業員に賞与を支給したときの手続き」(標準賞与額=1,000円未満切り捨て・健康保険は年度の累計573万円・厚生年金は1か月150万円・折半)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20141203.html
#  協会けんぽ令和8年度の都道府県の料率・介護1.62%・子ども・子育て支援金0.23%(tools/rates.json)、厚生年金18.3%、雇用保険の本人 5/1000(農林水産・清酒製造と建設 6/1000)
# 確かめ方:ページの JS を見ずに分数で計算し、画面(入力欄・結果・早見表・本文の数字)と比べる。国税庁 No.2523 の例(16,100円・1,510円・1,300円・87,540円・7,800円・7,954円)も見る。
import os, sys, json, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
import rates

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = json.load(open(os.path.join(ROOT, 'tools', 'getsugaku_r8.json'), encoding='utf-8'))
ROWS = G['rows']
PTS = {int(k): v for k, v in G['pts'].items()}
KAKO = [(740000, F(2042, 10000)), (790000, F(23483, 100000)), (960000, F(33693, 100000)), (1710000, F(4084, 10000)),
        (2130000, F(4084, 10000)), (2170000, F(4084, 10000)), (2210000, F(4084, 10000)), (2250000, F(4084, 10000)), (3500000, F(45945, 100000))]
RATE = [0, 2042, 4084, 6126, 8168, 10210, 12252, 14294, 16336, 18378, 20420, 22462, 24504, 26546, 28588, 30630,
        32672, 35735, 38798, 41861, 45945]
R8 = [
 [82, 94, 260, 309, 342, 372, 402, 433, 520, 605, 684, 715, 752, 795, 854, 922, 1318, 1521, 2621, 3495],
 [107, 250, 289, 346, 373, 401, 430, 463, 520, 621, 705, 739, 778, 821, 882, 952, 1342, 1526, 2645, 3527],
 [143, 276, 321, 377, 400, 426, 457, 492, 525, 636, 728, 764, 804, 848, 910, 983, 1367, 1526, 2669, 3559],
 [181, 300, 354, 405, 424, 452, 484, 517, 550, 651, 751, 788, 830, 876, 938, 1013, 1391, 1538, 2693, 3590],
 [218, 300, 387, 431, 452, 477, 509, 540, 577, 666, 774, 813, 856, 903, 966, 1044, 1416, 1555, 2716, 3622],
 [251, 304, 412, 457, 479, 503, 531, 564, 604, 681, 798, 838, 881, 930, 994, 1074, 1440, 1555, 2740, 3654],
 [284, 343, 438, 483, 505, 527, 553, 589, 630, 697, 821, 862, 907, 957, 1022, 1104, 1464, 1555, 2764, 3685],
 [317, 383, 463, 508, 529, 552, 578, 614, 657, 708, 845, 887, 933, 985, 1051, 1135, 1489, 1583, 2788, 3717]]
GRADE = rates.tokyu_upper_std_sen()

def half(x):
    x = F(x); q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q

def std(m):
    for top, s in GRADE:
        if top is None or m < top * 1000:
            return s * 1000

def getsu(x, hg):
    if x < 105000:
        return 0
    for r in ROWS:
        if r[0] <= x < r[1]:
            return r[2 + hg]
    base, rt = None, None
    for lo, r in KAKO:
        if x >= lo:
            base, rt = lo, r
    v = PTS[base][hg] + (x - base) * rt
    return v.numerator // v.denominator

def ken_rate(pref_rate, old):
    return F(pref_rate + rates.SIEN + (rates.KAIGO if old == 1 else 0), 10000)

def si_month(m, pr, old, ei):
    if m == 0:
        return 0
    h = std(m); p = min(max(h, rates.NENKIN_MIN), rates.NENKIN_MAX)
    return half(h * ken_rate(pr, old) / 2) + half(p * F(rates.NENKIN, 10000) / 2) + half(m * F(ei, 1000))

def ref(b, m, hg=0, pr=None, old=0, ei=5, kik=6, sk=None):
    pr = rates.TOKYO if pr is None else pr
    s = b // 1000 * 1000
    ken = half(min(s, 5730000) * ken_rate(pr, old) / 2)
    nen = half(min(s, 1500000) * F(rates.NENKIN, 10000) / 2)
    koy = half(b * F(ei, 1000))
    sb = ken + nen + koy
    k = si_month(m, pr, old, ei) if sk is None else min(sk, m)
    a = m - k; B = b - sb
    if m == 0 or a <= 0:        # 算出率の表（令和8年分）備考4・告示115号別表第三の備考：前月中の給与等の金額が社会保険料等以下は「ない場合」と同じ第3項第1号イ(2)。No.2523：前月の給与が無いとき・前月の給与が社会保険料以下のときは同じ計算
        z = getsu(B // kik, hg) * kik; mode = 1; i = None
    elif B > a * 10:
        a0 = max(a, 0)
        z = (getsu(a0 + B // kik, hg) - getsu(a0, hg)) * kik; mode = 2; i = None
    else:
        i = 20
        for j, top in enumerate(R8[min(hg, 7)]):
            if a < top * 1000:
                i = j; break
        z = B * RATE[i] // 100000; mode = 0
    z = max(z, 0)
    return dict(ken=ken, nen=nen, koy=koy, sb=sb, k=k, a=a, i=i, mode=mode, zei=z, te=b - sb - z)

def pct(i):
    return '%d.%03d%%' % (RATE[i] // 1000, RATE[i] % 1000)

def c(n):
    return '{:,}'.format(n)

async def body(pg):
    n = bad = 0
    def chk(label, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp:
            bad += 1
            print('合わない', label, '画面', got, '計算', exp)
    # 国税庁 No.2523 の例
    chk('No.2523 月額表 444,541円 1人', getsu(444541, 1), 16100)
    chk('No.2523 月額表 166,531円 1人', getsu(166531, 1), 1510)
    chk('No.2523 月額表 128,216円 0人', getsu(128216, 0), 1300)
    chk('No.2523 10倍超の例', (getsu(166531 + 1668062 // 6, 1) - getsu(166531, 1)) * 6, 87540)
    chk('No.2523 前月なしの例', getsu(769300 // 6, 0) * 6, 7800)
    chk('No.2523 率の表の例 285,454円 3人', 389558 * RATE[[j for j, t in enumerate(R8[3]) if 285454 < t * 1000][0]] // 100000, 7954)
    # ページの月額表の関数を、表の全行の下限と上限の1円前・式の区間で比べる
    pts = []
    for r in ROWS:
        pts += [r[0], r[1] - 1]
    pts += [740000, 740001, 765432, 789999, 790000, 800001, 959999, 960000, 1234567, 1710000, 2000001, 2130000, 2169999,
            2170000, 2209999, 2210000, 2249999, 2250000, 3000000, 3499999, 3500000, 4000000, 104999]
    got = await pg.evaluate('(a)=>a.map(x=>[0,1,2,3,4,5,6,7].map(h=>window.__getsu(x,h)))', pts)
    for x, row in zip(pts, got):
        for h in range(8):
            chk('月額表 %d %d人' % (x, h), row[h], getsu(x, h))
    async def ui(b, m, hg=0, pref='東京都', old=0, eiv='50', kik=6, sk=''):
        await pg.fill('#bon', str(b)); await pg.fill('#mae', str(m)); await pg.fill('#skin', str(sk))
        await pg.select_option('#fu', str(hg)); await pg.select_option('#pref', label=pref)
        await pg.click('#s-old button[data-v="%d"]' % old)
        sel = {'50': '#s-ei button:nth-child(1)', '60a': '#s-ei button:nth-child(2)', '60b': '#s-ei button:nth-child(3)'}[eiv]
        await pg.click(sel)
        await pg.click('#s-kik button[data-v="%d"]' % kik)
        return await pg.evaluate('()=>["o-te","o-sb","o-z","o-b","o-te2","o-zd","o-kenl","o-p","o-ken","o-nen","o-koy","o-q"].map(i=>document.getElementById(i).textContent)')
    cases = []
    for b in (0, 1000, 99999, 100000, 300000, 500000, 523456, 1000000, 1500000, 1500999, 1501000, 2000000, 3000000, 5730000, 6000000, 12000000):
        for m in (0, 80000, 150000, 300000, 450000, 800000, 1500000):
            cases.append((b, m, 0, '東京都', 0, '50', 6, ''))
    for pref in ('北海道', '大阪府', '佐賀県', '沖縄県', '新潟県'):
        for old in (0, 1, 2):
            for hg in (0, 2, 7):
                cases.append((800000, 350000, hg, pref, old, '50', 6, ''))
    for eiv in ('60a', '60b'):
        cases.append((700000, 320000, 1, '東京都', 1, eiv, 6, ''))
    for kik in (6, 12):
        for m in (0, 100000):
            cases.append((2400000, m, 1, '愛知県', 0, '50', kik, ''))
    for b in (300000, 1000000):                      # 前月の給与が社会保険料以下(手入力)・65歳以上
        cases.append((b, 50000, 0, '東京都', 0, '50', 6, '60000'))
        cases.append((b, 50000, 0, '東京都', 2, '50', 6, '50000'))
    for sk in ('0', '40000', '60000', '999999'):
        cases.append((600000, 300000, 0, '東京都', 0, '50', 6, sk))
    for (b, m, hg, pref, old, eiv, kik, sk) in cases:
        pr = rates.kenpo(pref); ei = 5 if eiv == '50' else 6
        x = ref(b, m, hg, pr, old, ei, kik, None if sk == '' else int(sk))
        t = await ui(b, m, hg, pref, old, eiv, kik, sk)
        tag = '%d %d %d %s %d %s %d %s' % (b, m, hg, pref, old, eiv, kik, sk)
        chk('手取り ' + tag, num(t[0]), x['te'])
        chk('社会保険料 ' + tag, num(t[1]), -x['sb'])
        chk('所得税 ' + tag, num(t[2]), -x['zei'])
        chk('手取り(下) ' + tag, num(t[4]), x['te'])
        chk('内訳 ' + tag, [t[6], num(t[8]), num(t[9]), num(t[10]), num(t[3]), re.sub(r'\s+', ' ', t[11])], ['健康保険・介護保険' if old == 1 else '健康保険', x['ken'], x['nen'], x['koy'], b, '賞与 %s円 の手取り' % c(b)])
        chk('内訳の足し算 ' + tag, num(t[8]) + num(t[9]) + num(t[10]), x['sb'])
        if x['mode'] == 0:
            my = '%s万円' % c(m // 10000) if m % 10000 == 0 else '%s円' % c(m)
            chk('率の文 ' + tag, t[5], '前月の給与%sから社会保険料%s円を引くと%s円なので、率は%sです' % (my, c(x['k']), c(x['a']), pct(x['i'])))
        else:
            want = ('前月の給与が無いので' if m == 0 else '前月の給与が社会保険料以下なので') if x['mode'] == 1 else '10倍を超えるので'
            chk('月額表の文 ' + tag, (want in t[5], '10倍を超える' in t[5] and x['a'] <= 0), (True, False))
        if b > 0:
            v = x['te'] * 1000 // b
            chk('割合 ' + tag, t[7], '賞与の%d.%d%%が手元に残ります' % (v // 10, v % 10))
    # 10倍の境目(社会保険料を引いた賞与が前月の10倍ちょうどと1円上)
    for m in (200000, 300000):
        a = m - si_month(m, rates.TOKYO, 0, 5)
        for b in range(a * 10, a * 12):
            r = ref(b, m)
            if b - r['sb'] in (a * 10, a * 10 + 1):
                t = await ui(b, m)
                chk('10倍の境目 %d %d' % (b, m), (num(t[0]), '10倍' in t[5]), (r['te'], r['mode'] == 2))
    BR = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1200000, 1500000, 2000000, 3000000]
    # 最初に開いたときの早見表(HTML に書いた数字)
    html = open(os.path.join(ROOT, 'site', 'bonus-tedori', 'index.html'), encoding='utf-8').read()
    tb0 = re.search(r'<table id="tb">.*?<tbody>(.*?)</tbody>', html, re.S).group(1)
    cells = [re.sub(r'<[^>]+>', '', x) for x in re.findall(r'<td[^>]*>(.*?)</td>', tb0, re.S)]
    for k, b in enumerate(BR):
        x = ref(b, 300000)
        chk('HTMLの早見表 %d' % b, [num(cells[k * 4 + 1]), num(cells[k * 4 + 2]), num(cells[k * 4 + 3])], [x['sb'], x['zei'], x['te']])
    # 早見表(前月の給与5つ×年齢2つ)
    for mv in (200000, 300000, 400000, 500000, 600000):
        for old in (0, 1, 2):
            await pg.click('#h-mae button[data-v="%d"]' % mv); await pg.click('#h-age button[data-v="%d"]' % old)
            rows = await pg.evaluate('()=>[...document.querySelectorAll("#tb tbody tr")].map(r=>[...r.cells].map(c=>c.textContent))')
            chk('早見表の行数 %d %d' % (mv, old), len(rows), len(BR))
            for b, r in zip(BR, rows):
                x = ref(b, mv, old=old)
                chk('早見表 %d %d %d' % (mv, old, b), [r[0], num(r[1]), num(r[2]), '※' in r[2], num(r[3])],
                    ['%s万円' % c(b // 10000), x['sb'], x['zei'], x['mode'] != 0, x['te']])
            cap = await pg.evaluate('()=>document.getElementById("tb-cap").textContent')
            chk('早見表の説明 %d %d' % (mv, old), cap, '前月の給与%s万円・%s・扶養親族0人・東京都' % (mv // 10000, ['40歳未満', '40〜64歳', '65歳以上'][old]))
    # 前月の給与ごとの率の表
    M2 = [150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 600000, 700000, 800000, 1000000]
    rows = await pg.evaluate('()=>[...document.querySelectorAll("#rt tbody tr")].map(r=>[...r.cells].map(c=>c.textContent))')
    chk('率の表の行数', len(rows), len(M2))
    for m, r in zip(M2, rows):
        x0 = ref(500000, m, 0); x1 = ref(500000, m, 1)
        chk('率の表 %d' % m, [r[0], r[1], num(r[2]), num(r[3])], ['%s万円' % c(m // 10000), pct(x0['i']), x0['te'], x1['te']])
    # 本文とよくある質問の数字
    txt = re.sub(r'\s+', '', await pg.evaluate('()=>document.querySelector("main").textContent'))
    g = ref(500000, 300000); g40 = ref(500000, 300000, old=1); g60 = ref(600000, 300000); g45 = ref(600000, 450000); gz = ref(500000, 0)
    for s in ['ボーナス50万円の手取りは%s円です。社会保険料%s円と所得税%s円が引かれます。' % (c(g['te']), c(g['sb']), c(g['zei'])),
              '東京都で賞与50万円なら、40歳未満より%s円多く引かれます。' % c(g40['sb'] - g['sb']),
              '前月の給与30万円なら所得税は%s円で手取りは%s円です。' % (c(g60['zei']), c(g60['te'])),
              '所得税は%s円に増えて、手取りは%s円になります。' % (c(g45['zei']), c(g45['te'])),
              '賞与50万円なら、所得税は%s円で手取りは%s円です。' % (c(gz['zei']), c(gz['te'])),
              '前月の給与30万円・40歳未満・扶養親族0人・東京都なら%s円です。社会保険料%s円と所得税%s円を引いた額です。' % (c(g['te']), c(g['sb']), c(g['zei'])),
              '前月の給与30万円なら約%d割（%d%%）です。' % (round(F(g['te'] * 10, 500000)), round(F(g['te'] * 100, 500000))),
              '東京都で賞与50万円・前月の給与30万円なら、%s円減って%s円になります。' % (c(g['te'] - g40['te']), c(g40['te'])),
              '同じ月に2回出たときは2回の合計で見ます。',
              '65歳以上の介護保険料は賞与からは引かれず、年金などから納めます。',
              '70歳以上の人は厚生年金に入らないので、厚生年金保険料は引かれません。',
              '70歳以上の人は厚生年金保険料が引かれないので、手取りはこの計算より多くなります',
              '扶養控除等申告書を出していない人は算出率の表の乙欄の率を使い、所得税は甲欄と同じかそれより多くなります。',
              'このページは甲欄で計算していて、乙欄の計算はしていません。',
              '「前月中の給与等の金額がない場合や前月中の給与等の金額が前月中の社会保険料等の金額以下である場合」を同じ扱いとし',
              '前月に給与が無いとき（前月の給与が社会保険料以下のときも同じ）：']:
        chk('本文 ' + s[:24], s in txt, True)
    chk('足して見ます が残っていない', '足して見ます' in txt, False)
    cta = await pg.evaluate('()=>[...document.querySelectorAll("main [data-cta],header [data-cta],.fbar [data-cta],.close [data-cta]")].map(a=>a.getAttribute("data-cta"))')
    chk('data-cta は bonus-tedori_ で始まる', [x for x in cta if not x.startswith('bonus-tedori_')], [])
    chk('id の重なり', await pg.evaluate('()=>{var c={};document.querySelectorAll("[id]").forEach(e=>c[e.id]=(c[e.id]||0)+1);return Object.keys(c).filter(k=>c[k]>1)}'), [])
    return n, bad
run('bonus-tedori', body)
