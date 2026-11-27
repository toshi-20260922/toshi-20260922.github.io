# /houjinnari/ 法人成りの計算(個人事業と法人の手取りの比較・分岐点の早見表)。
# 原本:
#  国税庁 No.2260 所得税の税率(速算表・課税所得は1,000円未満切り捨て・復興特別所得税2.1%・令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
#  国税庁 No.1199 基礎控除(令和8年分・9年分。2,350万円超は48万・32万・16万・0円) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#  国税庁「令和8年分 年末調整のしかた」基礎控除等(489万円以下104万円・655万円以下67万円) https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/106.pdf
#  国税庁「令和8年度税制改正による基礎控除の引上げ等」(本則62万円・加算42万円と5万円・給与所得控除の最低74万円・69万1,000円から220万円未満の表)
#   https://www.nta.go.jp/publication/pamph/gensen/2026kaisei.pdf  https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf
#  国税庁 No.2072 青色申告特別控除(65万円・令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2072.htm
#  東京都主税局「個人事業税」(事業主控除 年290万円・第1種5%・第2種4%・第3種5%(一部3%)・青色申告特別控除は適用なし) https://www.tax.metro.tokyo.lg.jp/kazei/work/kojin_ji
#  東京都主税局「個人住民税」(都民税4%・区市町村民税6%・均等割と森林環境税で5,000円・調整控除・2,500万円超は調整控除なし・45万円以下は非課税・
#   給与所得控除74万円は令和9年度分から) https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju
#  総務省「個人住民税」 https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html
#  日本年金機構「国民年金保険料」(令和8年度 月17,920円) https://www.nenkin.go.jp/service/kokunen/hokenryo/hokenryo.html
#  全国健康保険協会「令和8年度の都道府県単位保険料率」(47都道府県・介護1.62%・子ども・子育て支援金0.23%)
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  全国健康保険協会「令和8年3月分からの保険料額表(東京)」(等級の範囲・厚生年金18.3%・88,000円から650,000円・拠出金0.36%) https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#  厚生労働省・こども家庭庁「子ども・子育て支援金に関するQ&A」(一般保険料率と支援金率を合算して折半してから端数処理) https://www.mhlw.go.jp/hourei/doc/tsuchi/T260216S0101.pdf
#  日本年金機構「保険料の計算方法について」(本人負担は50銭以下切り捨て・50銭超切り上げ) https://www.nenkin.go.jp/service/kounen/hokenryo/nofu/20121026.html
#  国税庁 No.5759 法人税の税率(年800万円以下15%・超える部分23.2%・令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5759.htm
#  国税庁「地方法人税の税率の改正のお知らせ」(10.3%) https://www.nta.go.jp/publication/pamph/hojin/chihou_hojin/01.htm
#  国税庁「令和7年度 法人税関係法令の改正の概要」防衛特別法人税(4%・基礎控除 年500万円・令和8年4月1日以後開始) https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2025/pdf/E.pdf
#  総務省「法人住民税」(法人税割1.0%と6.0%・均等割2万円と5万円) https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_08.html
#  総務省「法人事業税」(3.5%・5.3%・7.0%) https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_09.html
#  東京都主税局「特別法人事業税」(基準法人所得割額の37%) https://www.tax.metro.tokyo.lg.jp/kazei/work/tokubetsu_houjin
#  国民健康保険(令和8年度・この日に公式ページで確かめた3つ):
#   東京23区(港区「国民健康保険料」7.51%・47,600円/2.80%・17,600円/2.43%・17,800円/0.27%・1,873円・上限67万26万17万3万・軽減の基準43万円+31万円・57万円×人数)
#    https://www.city.minato.tokyo.jp/shikaku/kurashi/hoken/kenkohoken/hokenryo.html
#   大阪府「令和8年度大阪府市町村標準保険料率等の算定結果について」 https://www.pref.osaka.lg.jp/o100080/kokuho/iryouseido/hokenryouritsu/hokenryouritsu2.html
#   横浜市「令和8年度保険料の料率等について」 https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/r7hokennryouritu.html
#   ほかの19の市区町村は tools/regions.py(2026/11/16 に公式ページで確かめた値)と同じかだけを見る。
# 照らすもの:結果の箱(個人事業・法人・差・役員報酬の月額・社会保険料・分岐点の文)・JS が作る10行の表・HTML に手で書いた早見表3枚の全マス・本文の分岐点の数字
#  国税庁 No.5300 損金の額に算入される租税公課等の範囲と損金算入時期(都道府県民税と市町村民税の本税は損金にならない・事業税は申告書を出した事業年度の損金)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5300.htm
#  法人税基本通達9-5-1・9-5-2(事業税と特別法人事業税の損金算入の時期) https://www.nta.go.jp/law/tsutatsu/kihon/hojin/09/09_05_01.htm
# 決め(2026-11-20 に直した):
#  ・会社負担の健康保険と厚生年金は 全額(円未満切り捨て)−本人負担。子ども・子育て拠出金は円未満切り捨て(/yakuin-tedori/ と同じ)。
#  ・早見表3枚の会社の所得は、毎年同じ利益が続く姿として前の年の分の法人事業税・特別法人事業税を引いてから出す。
#  ・法人住民税の均等割7万円は損金にならないので所得から引かない(税額には足す)。
#  東京都主税局「法人事業税・特別法人事業税」(不均一課税。年の所得2,500万円以下・資本金1億円以下は標準税率3.5%・5.3%・7.0%、超える会社は超過税率3.75%・5.665%・7.48%。
#   特別法人事業税は標準税率で出した所得割額の37%。法人都民税の法人税割は23区で7.0%) https://www.tax.metro.tokyo.lg.jp/kazei/work/houjinji
#  ・早見表は「地方税は標準税率」の前提のまま。東京都の超過税率がかかるのは利益3,000万円・報酬月20万円のマスだけで、前提の欄の注記(7万円から11万円)を自分の計算と照らす(2026-11-21)。
#  ・23区の法人税割を7.0%まとめて100円未満切り捨てにしても、画面に出る早見表のマスは1つも変わらない(2026-11-21 に確かめた)。
# 最後に原本を確かめた日:2026-11-21(今日開けたのは No.2260・No.1199・暮らしの税情報・令和8年度改正のあらましとQ&A・No.5759・防衛特別法人税・協会けんぽ・日本年金機構 国民年金・
#  東京都主税局 個人事業税と法人事業税・港区・横浜市・大阪府。No.5300・No.2072・総務省・ほかの19市区町村は今日は開いていない)
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fractions import Fraction as F
from _lib import run
import regions
import rates

# ---- 原本から書いた定数 ----
SOKUSAN = rates.sokusan_ue()
NENKIN_KOKUMIN = rates.NENKIN_KOKUMIN * 12
PREF = rates.kenpo_pref()
KAIGO, SIEN = rates.KAIGO, rates.SIEN
# 標準報酬月額(千円)と、その等級の上の境目(千円・未満)
STD = rates.std_sen()
TOP = rates.upper_sen()
# 国保:この日に公式ページで確かめた3つ [所得割(%×100), 均等割, 平等割, 上限]
KOKUHO_OK = {
    0: [[751, 47600, 0, 670000], [280, 17600, 0, 260000], [243, 17800, 0, 170000], [27, 1873, 0, 30000]],
    8: [[833, 40870, 0, 670000], [262, 13380, 0, 260000], [284, 16200, 0, 170000], [34, 1770, 0, 30000]],
    15: [[950, 34990, 33908, 660000], [306, 11191, 10845, 260000], [260, 18682, 0, 170000], [28, 1841, 0, 30000]],
}

def std(m):
    for s, t in zip(STD, TOP):
        if m < t * 1000: return s * 1000
    return 1390000
def half(x):
    q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q
def rnd(x):
    return (x + F(1, 2)).__floor__()
def yakuin(m, old, rate):
    s = std(m); p = min(max(s, rates.NENKIN_MIN), rates.NENKIN_MAX)
    ken = half(F(s * (rate + SIEN + (KAIGO if old else 0)), 20000)); nen = half(F(p * rates.NENKIN, 20000))
    zen = s * (rate + SIEN + (KAIGO if old else 0)) // 10000 + p * rates.NENKIN // 10000   # 全額は円未満切り捨て
    return ken + nen, zen - ken - nen + p * rates.KYOSHUTSU // 10000                           # 会社負担=全額−本人負担+拠出金(円未満切り捨て)
def kyuyo(x):
    return rates.kyuyo_r8(x)
def kiso(g):
    return rates.kiso_shotoku(g)
def kiso_ju(g):
    return rates.kiso_jumin(g)
def shotokuzei(t):
    t = max(0, t) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or t <= top:
            return (t * r // 100 - d) * rates.FUKKO_NUM // rates.FUKKO_DEN // 100 * 100
def jumin(g, sh):
    if g <= 450000: return 0
    t = max(0, g - sh - kiso_ju(g)) // 1000 * 1000
    adj = 0 if g > 25000000 else (min(50000, t) if t <= 2000000 else 50000)
    a = max(0, t * 6 // 100 - adj * 3 // 100) // 100 * 100
    b = max(0, t * 4 // 100 - adj * 2 // 100) // 100 * 100
    return a + b + 5000
def kokuho(R, g, old):
    base = max(0, g - rates.KEIGEN_BASE)
    red = rates.keigen(g, 1)
    tot = 0
    for i, c in enumerate(R['p']):
        if i == 2 and not old: continue
        v = base * c[0] // 10000 + c[1] * (10 - red) // 10 + c[2] * (10 - red) // 10
        if R.get('nag') and i == 0 and red > 0: v = max(0, v - 2000)
        tot += min(c[3], v // R['r'] * R['r'])
    return tot
def kojin(a, old, R):
    g = max(0, a - min(650000, a)); sh = kokuho(R, g, old) + (0 if old == 2 else NENKIN_KOKUMIN)   # 60〜64歳は国民年金なし
    it = shotokuzei(g - sh - kiso(g)); ju = jumin(g, sh)
    jg = max(0, a - 2900000) // 1000 * 1000 * 5 // 100 // 100 * 100
    return a - it - ju - jg - sh
def houjin(a, old, rate):
    avail = a - 70000; lo, hi, m = 0, max(0, avail // 12), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if (mid + yakuin(mid, old, rate)[1]) * 12 <= avail: m = mid; lo = mid + 1
        else: hi = mid - 1
    me, co = yakuin(m, old, rate); r = m * 12; sh = me * 12; g = kyuyo(r)
    return {'net': r - sh - shotokuzei(g - sh - kiso(g)) - jumin(g, sh), 'm': m, 'sh': (me + co) * 12}
def jigyo(a):
    """法人事業税と特別法人事業税(a は1,000円未満を切り捨てた所得)"""
    jg = (min(a, 4000000) * 35 + max(0, min(a, 8000000) - 4000000) * 53 + max(0, a - 8000000) * 70) // 1000 // 100 * 100
    return jg, jg * 37 // 100 // 100 * 100
def shotoku(p):
    """会社の所得。毎年同じ利益が続く姿として、前の年の分の法人事業税・特別法人事業税を引く(30回くり返して落ち着いた額)。
    法人住民税(均等割を含む)は損金にならないので引かない(国税庁 No.5300)。"""
    i = p
    for _ in range(30):
        i = p - sum(jigyo(max(0, i) // 1000 * 1000))
    return i
def corp(p):
    a = max(0, shotoku(p)) // 1000 * 1000
    hz = (min(a, 8000000) * 150 + max(0, a - 8000000) * 232) // 1000 // 100 * 100
    kz = hz // 1000 * 1000
    chiho = kz * 103 // 1000 // 100 * 100
    boei = max(0, kz - 5000000) // 1000 * 1000 * 4 // 100 // 100 * 100
    jg, tk = jigyo(a)
    return hz + chiho + boei + jg + tk + kz * 1 // 100 // 100 * 100 + kz * 6 // 100 // 100 * 100 + 70000
def cell(a, m, old, R, rate):
    """早見表の1マス:(個人事業のままの負担−法人の負担, 会社の利益, 会社に残る額)"""
    me, co = yakuin(m, old, rate); r = m * 12; g = kyuyo(r)
    it = shotokuzei(g - me * 12 - kiso(g)); ju = jumin(g, me * 12)
    p = a - r - co * 12; cp = corp(p) if p > 0 else 70000
    return (a - kojin(a, old, R)) - (me * 12 + co * 12 + it + ju + cp), p, p - cp
def cross(old, R, rate):
    last = 0
    for a in range(3000000, 30000001, 100000):
        if houjin(a, old, rate)['net'] <= kojin(a, old, R): last = a
    return last
def man(v):
    return rnd(F(v, 10000))
def d(t):
    s = ''.join(ch for ch in t if ch.isdigit()); v = int(s or 0)
    return -v if ('−' in t or '-' in t) else v

SET = """async ([reg, pref, old, a, cust]) => {
  const $ = id => document.getElementById(id), ev = (e, t) => e.dispatchEvent(new Event(t, {bubbles: true}));
  $('reg').value = String(reg); ev($('reg'), 'change');
  if (cust) { cust.forEach((row, i) => row.forEach((v, j) => { $('c' + i + j).value = v; })); ev($('c00'), 'input'); }
  $('pref').value = String(pref); ev($('pref'), 'change');
  document.querySelectorAll('#s-age button')[old].click();
  $('inc').value = String(a); ev($('inc'), 'input');
  const t = id => $(id).textContent;
  return {k: t('o-k'), h: t('o-h'), d: t('o-d'), w: t('o-w'), win: t('o-win'), wd: t('o-wd'), o1: t('o-1'), o2: t('o-2'), reg: t('o-reg'),
          tb: [...document.querySelectorAll('#tb tr')].map(r => [...r.children].map(c => c.textContent))};
}"""

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1
            if bad <= 60 or os.environ.get('ALL'): print('NG', label, got, want)

    # 1 ページの中の料率の表が原本(3つ)と regions.py(ほか)と同じか
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'houjinnari', 'index.html'), encoding='utf-8').read()
    import json
    i = raw.index('var RG=') + 7; j = raw.index('];var PF=', i) + 1
    RG = json.loads(raw[i:j]); k = raw.index(';', j + 8); PF = json.loads(raw[j + 8:k])
    chk('市区町村の数', len(RG), len(regions.REG))
    for idx, r in enumerate(RG):
        if idx in KOKUHO_OK: chk('国保の料率(原本) ' + r['s'], r['p'], KOKUHO_OK[idx])
        chk('国保の料率(regions.py) ' + r['s'], (r['p'], r['r'], r['g']), (regions.REG[idx]['p'], regions.REG[idx]['r'], regions.REG[idx]['nag']))
        chk('市区町村の都道府県 ' + r['s'], PREF[r['f']][0][:2] in {'東京': ['東京'], '札幌': ['北海'], '仙台': ['宮城'], 'さい': ['埼玉'], '千葉': ['千葉'],
            '横浜': ['神奈'], '川崎': ['神奈'], '相模': ['神奈'], '新潟': ['新潟'], '浜松': ['静岡'], '名古': ['愛知'], '京都': ['京都'], '大阪': ['大阪'],
            '神戸': ['兵庫'], '岡山': ['岡山'], '広島': ['広島'], '北九': ['福岡'], '福岡': ['福岡'], '熊本': ['熊本'],
            '目黒': ['東京'], '中野': ['東京'], '江戸': ['東京']}[r['s'][:2]], True)
    chk('協会けんぽの料率 47', [tuple(x) for x in PF], PREF)
    chk('都道府県の選択肢', await pg.eval_on_selector_all('#pref option', 'os=>os.map(o=>o.textContent)'),
        ['%s（%d.%02d%%）' % (nm, v // 100, v % 100) for nm, v in PREF])
    RR = [dict(p=r['p'], r=r['r'], nag=r['g'], s=r['s'], f=r['f']) for r in RG]

    # 2 結果の箱(市区町村22×年齢2×利益)
    PROF = [0, 1, 300000, 650000, 1080000, 1390000, 1650000, 2000000, 2899999, 2900000, 2901000, 3000000, 4000000, 5000000,
            5555555, 6000000, 7000000, 8000000, 9000000, 10000000, 12000000, 15000000, 20000000, 23999999, 24650000, 24650001,
            25150000, 25650000, 25650001, 30000000, 40000000, 50000000]
    async def one(ri, pi, old, a, cust=None, R=None):
        got = await pg.evaluate(SET, [ri, pi, old, a, cust])
        R = R or RR[ri]; rate = PREF[pi][1]
        kk = kojin(a, old, R); h = houjin(a, old, rate); df = h['net'] - kk
        tag = '%s %s %s %d' % (R.get('s', '入れた料率'), PREF[pi][0], ('40歳未満', '40〜59歳', '60〜64歳')[old], a)
        chk('個人事業 ' + tag, d(got['k']), kk)
        chk('法人 ' + tag, d(got['h']), h['net'])
        chk('差 ' + tag, got['d'], ('+' if df >= 0 else '−') + '{:,}円'.format(abs(df)))
        chk('どちらが多い ' + tag, (got['w'], got['win']), ('法人のほうが多い', '法人のほうが多く残ります') if df >= 0 else ('個人事業のほうが多い', '個人事業のままのほうが多く残ります'))
        chk('報酬の月額 ' + tag, got['o1'], '法人は役員報酬を月{:,}円とし、会社に残る利益をゼロにしています'.format(h['m']))
        chk('社会保険料 ' + tag, got['o2'], '法人の社会保険料は、本人負担と会社負担を合わせて年{:,}円です'.format(h['sh']))
        return got
    for ri in range(len(RR)):
        for old in (0, 1, 2):
            for a in PROF:
                await one(ri, RR[ri]['f'], old, a)
    # 都道府県47(東京23区の国保のまま)
    for pi in range(47):
        for old in (0, 1):
            for a in (4000000, 8000000, 13000000):
                await one(0, pi, old, a)
    # 3 帯の境目:役員報酬の月額が標準報酬の境目の前後になる利益(東京)と、給与所得・速算表の境目
    for t in (63, 93, 101, 195, 210, 635, 665, 695, 1005, 1055, 1115, 1175, 1235, 1295, 1355):
        for old in (0, 1):
            m = t * 1000
            for mm in (m - 1, m, m + 1):
                a = (mm + yakuin(mm, old, rates.TOKYO)[1]) * 12 + 70000
                for aa in (a - 1, a, a + 1):
                    await one(0, 12, old, aa)
    for r in (740999, 741000, 2190999, 2191000, 2192999, 2193000, 2195999, 2196000, 2199999, 2200000, 3599999, 3600000, 6599999, 6600000, 8499999, 8500000):
        m = r // 12
        for mm in (m, m + 1):
            a = (mm + yakuin(mm, 0, rates.TOKYO)[1]) * 12 + 70000
            await one(0, 12, 0, a); await one(0, 12, 0, a + 11)
    # 4 料率を自分で入れる欄(大阪府の料率を手で入れて、一覧の大阪と同じになるか)
    cu = [['%d.%02d' % (c[0] // 100, c[0] % 100), str(c[1]), str(c[2])] for c in RR[15]['p']]
    Rc = dict(p=[c[:3] + [cap] for c, cap in zip(RR[15]['p'], (670000, 260000, 170000, 30000))], r=1, nag=0)
    for old in (0, 1):
        for a in (1500000, 5000000, 9000000, 30000000):
            await one('x', 26, old, a, cu, Rc)
    await pg.evaluate("()=>{var r=document.getElementById('reg');r.value='0';r.dispatchEvent(new Event('change',{bubbles:true}));}")

    # 5 分岐点の文と10行の表(JS が作る)
    for ri, pi in ((0, 12), (15, 26), (8, 13), (13, 22), (20, 39)):
        for old in (0, 1):
            got = await pg.evaluate(SET, [ri, pi, old, 8000000, None])
            cx = cross(old, RR[ri], PREF[pi][1])
            kk = kojin(8000000, old, RR[ri]); h = houjin(8000000, old, PREF[pi][1]); df = h['net'] - kk
            cxs = '{:,}万円'.format((cx + 100000) // 10000) if 0 < cx < 30000000 else '3,000万円超'
            if cx == 0: cxs = '300万円'
            chk('分岐点の文 %s %d' % (RR[ri]['s'], old), got['wd'], '年{:,}円多く残ります。この条件で法人のほうが多く残るのは、利益が{}からです'.format(abs(df), cxs))
            chk('地域の文 %s' % RR[ri]['s'], got['reg'], '単身・%sの国民健康保険・協会けんぽ%sで計算しています' % (RR[ri]['s'], PREF[pi][0]))
            rows = []
            for r in (400, 500, 600, 700, 800, 900, 1000, 1200, 1500, 2000):
                A = r * 10000; k2 = kojin(A, old, RR[ri]); h2 = houjin(A, old, PREF[pi][1])['net']; dd = h2 - k2
                rows.append(['{:,}'.format(r), '{:,}'.format(k2), '{:,}'.format(h2), ('+' if dd >= 0 else '−') + '{:,}'.format(abs(dd))])
            for gr, wr in zip(got['tb'], rows): chk('10行の表 %s %d %s' % (RR[ri]['s'], old, wr[0]), gr, wr)
            chk('10行の表の行の数', len(got['tb']), 10)
    await pg.evaluate(SET, [0, 12, 0, 8000000, None])

    # 6 HTML に書いた早見表の全マス(比べ方2つ×年齢3つ=6枚)と会社に残るお金(年齢3つ)。東京23区・協会けんぽ東京都
    PRS = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2500, 3000]
    MS = [20, 30, 40, 50, 60, 70, 80, 90, 100, 120]
    tabs = await pg.eval_on_selector_all('table.x7tb', """ts=>ts.map(t=>({c:(t.closest('[data-c]')||{dataset:{c:'n'}}).dataset.c,a:(t.closest('[data-a]')||{dataset:{a:'-'}}).dataset.a,
        h:[...t.querySelectorAll('thead th')].map(x=>x.textContent),
        r:[...t.querySelectorAll('tbody tr')].map(r=>[...r.children].map(c=>({t:c.textContent,c:c.className})))}))""")
    chk('早見表の並び', [(t['c'], t['a']) for t in tabs], [(c, str(o)) for c in 'ft' for o in (0, 1, 2)] + [('n', str(o)) for o in (0, 1, 2)])
    def sg(v):
        return ('+{:,}'.format(v)) if v > 0 else ('−{:,}'.format(-v) if v < 0 else '0')
    for T in tabs[:6]:
        mode, old = T['c'], int(T['a']); nm = '%s%d' % (mode, old)
        chk('表%s の見出し' % nm, T['h'], ['事業の利益（年）'] + ['報酬月%d万' % m for m in MS] + ['全額を報酬'])
        chk('表%s の行の数' % nm, len(T['r']), len(PRS))
        for row, p in zip(T['r'], PRS):
            a = p * 10000; kk = kojin(a, old, RR[0])
            lab = ('個人事業の負担{:,}万' if mode == 'f' else '個人事業の手取り{:,}万').format(man(a - kk) if mode == 'f' else man(kk))
            chk('表%s %d 左の列' % (nm, p), row[0]['t'], '{:,}万円'.format(p) + lab)
            vals = []
            for mm in MS:
                dv, P, nk = cell(a, mm * 10000, old, RR[0], rates.TOKYO)
                vals.append((man(dv if mode == 'f' else dv - nk), P))
            h = houjin(a, old, rates.TOKYO); av = man(h['net'] - kk)
            ok = [v for v, P in vals if P >= 0] + [av]; best = max(ok) if max(ok) > 0 else None; marked = False
            for ci, (v, P) in enumerate(vals):
                cl = 'x7g' if P < 0 else ('x7p' if v > 0 else '')
                if not marked and P >= 0 and v == best: cl += ' x7b'; marked = True
                chk('表%s %d 報酬月%d万' % (nm, p, MS[ci]), row[1 + ci]['t'], '赤字' if (mode == 't' and P < 0) else sg(v))
                chk('表%s %d 報酬月%d万 の色と枠' % (nm, p, MS[ci]), row[1 + ci]['c'], cl.strip())
            cl = 'x7p' if av > 0 else ''
            if not marked and av == best: cl += ' x7b'
            chk('表%s %d 全額を報酬' % (nm, p), row[11]['t'], sg(av) + '月%d万' % man(h['m']))
            chk('表%s %d 全額を報酬 の色と枠' % (nm, p), row[11]['c'], cl.strip())
    for T in tabs[6:]:
        old = int(T['a'])
        chk('残るお金%d の見出し' % old, T['h'], ['事業の利益（年）'] + ['報酬月%d万' % m for m in MS])
        for row, p in zip(T['r'], PRS):
            for ci, mm in enumerate(MS):
                _, P, nk = cell(p * 10000, mm * 10000, old, RR[0], rates.TOKYO); v = man(nk)
                chk('残るお金%d %d 報酬月%d万' % (old, p, mm), row[1 + ci]['t'], ('−{:,}'.format(-v)) if v < 0 else '{:,}'.format(v))
                chk('残るお金%d %d 報酬月%d万 の色' % (old, p, mm), row[1 + ci]['c'], 'x7g' if P < 0 else '')
    # 切り替え:比べ方と年齢を選ぶと、その表だけが見える。年齢はつまみとそろう
    for c, a in (('t', 2), ('f', 1), ('t', 0), ('f', 0)):
        await pg.click('#bkc button[data-v="%s"]' % c); await pg.click('#bkt button[data-v="%d"]' % a)
        vis = await pg.eval_on_selector_all('table.x7tb', "ts=>ts.map(t=>t.offsetParent!==null)")
        want = [cc == c and o == a for cc in 'ft' for o in (0, 1, 2)] + [o == a for o in (0, 1, 2)]
        chk('見える表 %s%d' % (c, a), vis, want)
        chk('つまみの年齢 %s%d' % (c, a), await pg.eval_on_selector('#bka .on', 'e=>e.dataset.v'), str(a))

    # 6-2 つまみ:手取りで比べるとき、法人のほうが社長の手取りが多くなる利益の幅(会社が赤字でない範囲)
    def win(m, old):
        ok = [a for a in range(3000000, 30000001, 100000) if (lambda c: c[1] >= 0 and c[0] - c[2] > 0)(cell(a, m, old, RR[0], rates.TOKYO))]
        if ok: chk('幅がつながっている %d %d' % (m, old), ok, list(range(ok[0], ok[-1] + 1, 100000)))
        return (ok[0], ok[-1]) if ok else None
    await pg.click('#bkc button[data-v="t"]')
    for old in (0, 1, 2):
        await pg.click('#bka button[data-v="%d"]' % old)
        for m in range(100000, 1200001, 50000):
            await pg.evaluate("m=>{var b=document.getElementById('bkm');b.value=String(m);b.dispatchEvent(new Event('input',{bubbles:true}));}", m)
            got = await pg.evaluate("()=>['bko-v','bko-s','bko-k'].map(i=>{var e=document.getElementById(i);return e.hidden?null:e.textContent;})")
            w = win(m, old)
            want = (['利益{:,}万〜{:,}万円'.format(w[0] // 10000, w[1] // 10000), 'のときだけ法人のほうが社長の手取りが多くなります', '利益がこれより多いと増えた分は会社に残るので、個人事業のほうが手取りが多くなります'] if w
                    else ['個人事業のほうが手取りが多い', '法人のほうが社長の手取りが多くなる利益はありません', None])
            chk('つまみ 手取り %d %d' % (old, m), got, want)
    await pg.click('#bkc button[data-v="f"]'); await pg.click('#bka button[data-v="0"]')
    await pg.evaluate("()=>{var b=document.getElementById('bkm');b.value='300000';b.dispatchEvent(new Event('input',{bubbles:true}));}")
    chk('つまみ 負担の合計に戻す', await pg.evaluate("()=>document.getElementById('bko-v').textContent+'|'+document.getElementById('bko-s').textContent"), '利益590万円から|法人のほうが税金と社会保険料の合計が軽くなります')

    # 7 本文の分岐点の数字(10万円刻みで、それより上はずっと法人のほうが軽くなる利益)
    def th(m, old):
        last = 0
        for a in range(3000000, 30000001, 100000):
            if cell(a, m, old, RR[0], rates.TOKYO)[0] <= 0: last = a
        return (last + 100000) // 10000
    al = [(cross(o, RR[0], rates.TOKYO) + 100000) // 10000 for o in (0, 1)]
    t3 = [th(300000, o) for o in (0, 1)]; t5 = [th(500000, o) for o in (0, 1)]
    flat = ''.join((await pg.inner_text('main')).split())
    for label, want in [
        ('読み方1', '利益{:,}万円から、法人のほうが軽くなります（40〜59歳は{:,}万円から）。それより下では'.format(*al)),
        ('読み方2', '利益%d万円から、法人のほうが軽くなります（40〜59歳は%d万円から）。' % tuple(t5)),
        ('読み方3', '利益%d万円から、法人のほうが軽くなります（40〜59歳は%d万円から）。会社に残したお金は' % tuple(t3)),
        ('質問1 手取り', '社長の手取りで比べると、利益を全額役員報酬で払う形で利益{:,}万円から法人のほうが多くなります（40〜59歳は{:,}万円から）。'.format(*al)),
        ('質問1', '役員報酬が月30万円なら利益%d万円から法人のほうが軽くなります。月50万円なら%d万円からです。' % (t3[0], t5[0])),
        ('質問3', '役員報酬が月30万円なら%d万円で月50万円なら%d万円です。' % (t3[1], t5[1])),
        ('国民年金の月額', '国民年金（月{:,}円）'.format(NENKIN_KOKUMIN // 12)),
        ('事業主控除', '事業主控除290万円を超える所得に3〜5%（この計算は5%）'),
        ('住民税の標準税率', '住民税はどの地域も標準税率（所得割10%、均等割と森林環境税で年5,000円）です。'),
        
        ('均等割', '法人住民税の均等割は年7万円'),
        ('前提 事業税', '前の年の分の法人事業税・特別法人事業税を会社の経費に含めています'),
        ('前提 均等割', '法人住民税の均等割は、法人税の計算で経費にならないので所得から引いていません'),
        ('前提の国保', '国民健康保険（東京23区（目黒区・中野区・江戸川区を除く20区）の令和8年度）'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('均等割 2万円+5万円', 20000 + 50000, 70000)
    # 東京都の超過税率(年の所得2,500万円超)がかかるマスと、前提の欄の注記の金額
    def jigyo_tokyo(a):
        st = (min(a, 4000000) * 35 + max(0, min(a, 8000000) - 4000000) * 53 + max(0, a - 8000000) * 70) // 1000 // 100 * 100
        jg = st if a <= 25000000 else (min(a, 4000000) * 3750 + max(0, min(a, 8000000) - 4000000) * 5665 + max(0, a - 8000000) * 7480) // 100000 // 100 * 100
        return jg, st * 37 // 100 // 100 * 100
    g = globals(); j0 = g['jigyo']; diff = {}
    for old in (0, 1):
        for p in PRS:
            for mm in MS:
                g['jigyo'] = j0; v0 = man(cell(p * 10000, mm * 10000, old, RR[0], rates.TOKYO)[0])
                g['jigyo'] = jigyo_tokyo; v1 = man(cell(p * 10000, mm * 10000, old, RR[0], rates.TOKYO)[0])
                if v0 != v1: diff[(old, p, mm)] = v0 - v1
    g['jigyo'] = j0
    chk('超過税率で変わるマス', diff, {(0, 3000, 20): 7, (1, 3000, 20): 11})
    chk('本文 超過税率の注記', '東京都は年の所得が2,500万円を超える会社の法人事業税に超過税率（年800万円を超える所得に7.48%など）をかけます。その場合は利益3,000万円・報酬月20万円の組み合わせで、法人の負担が表より7万円から11万円ほど重くなります' in flat, True)
    chk('更新日', '更新日：2026年11月21日' in flat, True)
    # 書き換える前の元の文と既定の選び方
    # 書き換える前の元の文(HTML に直に書いた既定の結果)が、既定の条件(東京23区・東京都・40歳未満・利益800万円)の自分の計算と同じか
    k0 = kojin(8000000, 0, RR[0]); h0 = houjin(8000000, 0, rates.TOKYO); d0 = h0['net'] - k0; c0 = (cross(0, RR[0], rates.TOKYO) + 100000) // 10000
    sgn = '+' if d0 >= 0 else '−'
    for label, want in [
        ('勝ち', '<b id="o-win">%s</b>' % ('法人のほうが多く残ります' if d0 >= 0 else '個人事業のままのほうが多く残ります')),
        ('分岐点', '<span id="o-wd">年{:,}円多く残ります。この条件で法人のほうが多く残るのは、利益が{:,}万円からです</span>'.format(abs(d0), c0)),
        ('個人事業', '<b id="o-k">{:,}<i>円</i></b>'.format(k0)),
        ('法人', '<b id="o-h">{:,}<i>円</i></b>'.format(h0['net'])),
        ('差', '>%s{:,}<i>円</i></b><em id="o-w">%s</em>'.format(abs(d0)) % (sgn, '法人のほうが多い' if d0 >= 0 else '個人事業のほうが多い')),
        ('報酬', '<li id="o-1">法人は役員報酬を月{:,}円とし、会社に残る利益をゼロにしています</li>'.format(h0['m'])),
        ('社会保険料', '<li id="o-2">法人の社会保険料は、本人負担と会社負担を合わせて年{:,}円です</li>'.format(h0['sh'])),
        ('箱の色', '<div class="vd%s" id="vd">' % (' no' if d0 >= 0 else '')),
        ('既定の利益', 'id="inc" inputmode="numeric" min="0" max="50000000" step="10000" value="8000000"'),
    ]:
        chk('元の文 ' + label, want in raw, True)
    # 黄色の行:入力した利益を超えない中でいちばん近い行(400万円より下は無し)
    for a, want in ((3990000, []), (4000000, ['400']), (5990000, ['500']), (8000000, ['800']), (11990000, ['1,000']), (19990000, ['1,500']), (50000000, ['2,000'])):
        await pg.evaluate(SET, [0, 12, 0, a, None])
        chk('黄色の行 %d' % a, await pg.eval_on_selector_all('#tb tr.hit', 'rs=>rs.map(r=>r.children[0].textContent)'), [w + '万円' for w in want])
    await pg.evaluate(SET, [0, 12, 0, 8000000, None])
    chk('元の文 地域', '<li id="o-reg">単身・東京23区の国民健康保険・協会けんぽ東京都で計算しています</li>' in raw, True)
    chk('既定の都道府県', '<option value="12" selected>東京都（9.85%）</option>' in raw, True)
    chk('既定の市区町村', await pg.evaluate("()=>document.getElementById('reg').options[0].textContent"), '東京23区（下の3区を除く20区）')
    return n, bad

run('houjinnari', body)
