# /iryohi-kojo/ 医療費控除の計算(戻る所得税と翌年度に減る住民税)。
# 原本:
#  国税庁 No.1120 医療費を支払ったとき(医療費控除) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1120.htm
#   (支払った医療費 − 保険金などで補てんされる金額) − 10万円(総所得金額等が200万円未満の人は5%)。最高200万円
#  国税庁 No.1410 給与所得控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
#   令和8年分・9年分:220万円まで74万円。660万円未満は別表第五(4,000円刻みの切り捨て。220万円未満は注2の表)
#  国税庁 No.1199 基礎控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#   令和8年分:489万円以下104万円・655万円以下67万円・2,350万円以下62万円・48万円・32万円・16万円・0円
#  国税庁 No.2260 所得税の税率 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
#   課税される所得金額は1,000円未満切り捨て。復興特別所得税は基準所得税額の2.1%
#  国税庁 令和8年分 年末調整のしかた https://www.nta.go.jp/users/gensen/nencho/index/shikata.htm
#   年調年税額=年調所得税額×102.1%(100円未満切り捨て)
#  全国健康保険協会 令和8年3月分からの保険料額表(東京都) https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#   健康保険9.85%・子ども・子育て支援金0.23%・厚生年金18.3%(88,000円から650,000円)・等級の境目
#  厚生労働省 令和8年度 雇用保険料率のご案内 https://www.mhlw.go.jp/content/001692566.pdf  労働者負担 5/1,000
#  住民税(令和9年度)は、医療費控除を引く前と引いた後の所得割の差で照らす(2026-11-20 から。前は「控除額の10%」で、
#   住民税の課税所得より控除額が大きいときに多く出ていた。例 年収300万円・医療費210万円で200,000円→110,600円)。
#   練馬区「調整控除」 https://www.city.nerima.tokyo.jp/kurashi/zei/jyuminzei/zeigakukojo/choseikojo.html
#    200万円以下:人的控除額の差(基礎控除は5万円)と合計課税所得金額の少ないほうの5%(区3%・都2%)
#    200万円超:{差 −(合計課税所得金額 − 200万円)}の5%。2,500円未満は2,500円。合計所得金額2,500万円超は調整控除なし
#   大田区「住民税の計算のしくみ」 https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/keisannosikumi.html
#    課税標準は1,000円未満切り捨て・区6%と都4%・100円未満切り捨て・基礎控除43万円
#   神戸市「令和9年度から適用される個人住民税の改正」 https://www.city.kobe.lg.jp/a83576/kurashi/tax/shikenminze/r9kaisei.html
#    給与所得控除の最低保障額は69万円(令和9・10年度は74万円)。基礎控除の改正は載っていない
#   住民税の基礎控除:合計所得2,400万円以下43万円・2,450万円以下29万円・2,500万円以下15万円・2,500万円超0円
#  国税庁 質疑応答事例「人間ドックの費用」 https://www.nta.go.jp/law/shitsugi/shotoku/05/09.htm
#   健康診断は原則対象外。重大な疾病が発見され、引き続きその疾病の治療を行った場合は対象(No.1122 は「原則として含まれません」)
#  国税庁 No.1129 セルフメディケーション税制:12,000円を差し引いた金額(最高88,000円)。通常の医療費控除と併せて受けられない
#  国税庁 No.2030 還付申告:その年の翌年1月1日から5年間
#  財務省 令和8年度税制改正の大綱(1/9):基礎控除62万円+特例(令和8・9年分 489万円以下42万円・489万円超655万円以下5万円)
#  総務省 事務連絡(令和8年1月21日) https://www.soumu.go.jp/main_content/001053325.pdf
#   個人住民税の給与所得控除の最低保障額69万円(令和9・10年度分はさらに5万円)。基礎控除の額と調整控除は載っていない
# 最後に原本を確かめた日:2026-11-21(No.1120・No.1122・No.1129・No.1199・No.1410・No.2260・No.2030・年末調整のしかた・
#   人間ドックの費用・財務省の大綱・協会けんぽ東京の3月分と10月分の保険料額表・厚生労働省の雇用保険料率・総務省の事務連絡。
#   練馬区・大田区・神戸市のページは 2026-11-20 に開いたまま)
# 2026-11-21:計算の箱に直に書いた既定の結果(0円のままだった)を足した。JS が動く前の HTML をファイルから読んで比べる。
# 社会保険料は、ページの注記の前提(毎月同じ額・賞与なし・令和8年度の料率を12か月)で1年分を分数で出し、1円未満を四捨五入する。
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run
import rates

# 保険料額表の等級(標準報酬月額, 報酬月額の下の境目)。協会けんぽの表のとおり手で写したもの。
GRADE = rates.tokyu_std_lower_yen()

def hyojun(m):
    h = GRADE[0][0]
    for g, lo in GRADE:
        if m >= lo:
            h = g
    return h

def shaho_nen(s):
    m = F(s, 12)
    h = hyojun(m)
    k = min(max(h, rates.NENKIN_MIN), rates.NENKIN_MAX)
    nen = 12 * (F(h * (rates.TOKYO + rates.SIEN), 20000) + F(k * rates.NENKIN_PER_1000, 2000)) + F(s * rates.KOYO_PER_1000, 1000)
    return int(nen + F(1, 2))                     # 1円未満四捨五入

def kyuyo_shotoku(s):
    return rates.kyuyo_r8(s)

def kiso(x):
    return rates.kiso_shotoku(x)

SOKUSAN = rates.sokusan_ue_m1000()

def zei(k):
    k = max(k, 0) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or k <= top:
            return k * r // 100 - d               # 1,000円単位なので割り切れる

def jkiso(x):
    return rates.kiso_jumin(x)

def shotokuwari(sh, x):
    """住民税の所得割(市6%+県4%。調整控除を引いて、それぞれ100円未満切り捨て)。"""
    x = max(x, 0) // 1000 * 1000
    if sh > 25000000:
        c = 0
    elif x <= 2000000:
        c = min(50000, x) * 5 // 100
    else:
        c = max(max(50000 - (x - 2000000), 0) * 5 // 100, 2500)
    shi = max(F(x * 6, 100) - F(c * 3, 5), 0)
    ken = max(F(x * 4, 100) - F(c * 2, 5), 0)
    return int(shi) // 100 * 100 + int(ken) // 100 * 100

def ref(s, med, hot):
    sh = kyuyo_shotoku(s)
    sa = shaho_nen(s)
    ashi = 100000 if sh >= 2000000 else sh * 5 // 100
    kj = min(max(med - hot - ashi, 0), 2000000)
    nencho = zei(sh - sa - kiso(sh)) * rates.FUKKO_NUM // rates.FUKKO_DEN // 100 * 100      # 年末調整で決まった額
    t = zei(sh - sa - kiso(sh) - kj)
    shinkoku = t * rates.FUKKO_NUM // rates.FUKKO_DEN                  # 確定申告:基準所得税額+復興特別所得税
    st = max(nencho - shinkoku, 0) if kj > 0 else 0
    jb = sh - sa - jkiso(sh)
    jm = max(shotokuwari(sh, jb) - shotokuwari(sh, jb - kj), 0) if kj > 0 else 0
    return {'kojo': kj, 'shotoku': st, 'jumin': jm, 'total': st + jm}

def digits(t):
    return int(''.join(c for c in t if c.isdigit()) or 0)

async def body(pg):
    n = bad = 0
    # 1) 関数を呼んで比べる。年収は画面で入れられる300万円から2,000万円。
    incomes = [3000000, 3000001, 3003999, 3004000, 3599999, 3600000, 3600001, 4000000, 4500000, 5000000,
               5000100, 5000300, 5555555, 6000000, 6599999, 6600000, 6600001, 7000000, 7777777, 8000000,
               8499999, 8500000, 8500001, 9000000, 10000000, 12000000, 15000000, 18000000, 20000000]
    # 等級の境目(月額がちょうど・1円下・1円上になる年収)。上のほうの等級を全部入れる。
    for g, lo in GRADE:
        if 250000 <= lo <= 1660000:
            incomes += [lo * 12 - 12, lo * 12, lo * 12 + 12]
    # 基礎控除の境目(給与所得が489万円・655万円をまたぐ年収)と、所得税の税率の境目をまたぐ年収
    for target in (4890000, 6550000):
        for s in range(6000000, 9000000, 4000):
            if kyuyo_shotoku(s) <= target < kyuyo_shotoku(s + 4000):
                incomes += [s - 1, s, s + 3999, s + 4000, s + 4001]
    for top, _, _ in SOKUSAN[:-2]:
        lo_s, hi_s = 3000000, 20000000
        while hi_s - lo_s > 1:                    # 課税所得がちょうど境目になる年収を二分で探す
            mid = (lo_s + hi_s) // 2
            if kyuyo_shotoku(mid) - shaho_nen(mid) - kiso(kyuyo_shotoku(mid)) > top + 1000:
                hi_s = mid
            else:
                lo_s = mid
        incomes += [lo_s - 5000, lo_s - 1, lo_s, hi_s, hi_s + 5000]
    incomes = sorted(set(s for s in incomes if 3000000 <= s <= 20000000))
    meds = [0, 99999, 100000, 100001, 100999, 101000, 150000, 200000, 300000, 500000, 1000000, 1234567,
            2099999, 2100000, 2100001, 3000000, 10000000]
    cases = [(s, m, 0) for s in incomes for m in meds]
    cases += [(s, 500000, h) for s in (3000000, 5000000, 7000000, 12000000) for h in (1, 100000, 399999, 400000, 400001, 500000, 600000)]
    # 給与所得が200万円をまたぐ年収(画面では入れられないが、関数の5%の枝を確かめる)
    for s in (1000000, 2000000, 2190999, 2200000, 2971999, 2972000, 2999999):
        cases += [(s, m, 0) for m in (50000, 74999, 75000, 75001, 99999, 100000, 100001, 150000, 300000)]
    # 住民税の課税所得より医療費控除が大きくなる所(年収が低く医療費が多い)と、その境目の前後
    for s in (3000000, 3200000, 3500000, 4000000, 4300000, 4500000, 5000000):
        jb = (kyuyo_shotoku(s) - shaho_nen(s) - 430000) // 1000 * 1000
        for kj in (jb - 60000, jb - 50000, jb - 49000, jb - 1000, jb, jb + 1000, jb + 100000, 1999999, 2000000):
            if 0 < kj <= 2000000:
                cases.append((s, kj + 100000, 0))
        cases += [(s, m, 0) for m in (100001, 100500, 101001, 123456, 1500000, 1800000, 2100000, 2500000)]
    # 住民税の課税所得が200万円から205万円をまたぐ所(調整控除は2,500円のまま)
    for s in range(4300000, 4500000, 20000):
        cases += [(s, m, 0) for m in (110000, 150000, 160000, 200000)]
    # 合計所得2,400万円超(画面では入れられない。基礎控除の段と調整控除なしの枝)
    for s in (25900000, 25950000, 25950001, 26450000, 26450001, 26950000, 26950001, 30000000):
        cases += [(s, m, 0) for m in (300000, 1000000, 2100000)]
    for s, m, h in cases:
        got = await pg.evaluate('([s,m,h])=>window.__iryo(s,m,h)', [s, m, h])
        exp = ref(s, m, h); n += 1
        if any(got[k] != exp[k] for k in exp):
            bad += 1; print('NG 関数', s, m, h, got, exp)
    # 2) 入力欄に入れて結果の箱を読む
    for s, m, h in [(5000000, 300000, 0), (3000000, 150000, 0), (7000000, 500000, 120000), (15000000, 1000000, 0),
                    (20000000, 10000000, 0), (5000000, 100000, 0), (9000000, 2500000, 300000),
                    (3000000, 2100000, 0), (3000000, 10000000, 0), (4000000, 1800000, 0)]:
        for i, v in (('#inc', s), ('#med', m), ('#hot', h)):
            await pg.fill(i, str(v))
        exp = ref(s, m, h)
        for box, key in (('#o-k', 'total'), ('#o-t', 'shotoku'), ('#o-z', 'jumin')):
            n += 1
            shown = digits(await pg.inner_text(box))
            if shown != exp[key]:
                bad += 1; print('NG 画面', s, m, h, box, shown, exp[key])
        n += 1
        e = await pg.inner_text('#o-e')
        want = ('医療費控除の額は%s円' % format(exp['kojo'], ',')) if exp['kojo'] > 0 else '10万円を超えた分が対象です'
        if e != want:
            bad += 1; print('NG 画面の控除額の文', s, m, h, e, want)
    # 3) 手で書いた早見表の全行(合計と住民税)
    html = await pg.content()
    tb = re.search(r'<tbody id="tb">(.*?)</tbody>', html, re.S).group(1)
    cols = [150000, 200000, 300000, 500000, 1000000]
    rows = re.findall(r'<tr data-s="(\d+)"[^>]*>(.*?)</tr>', tb, re.S)
    if len(rows) != 10:
        bad += 1; print('NG 早見表の行の数', len(rows))
    for ds, tr in rows:
        cells = re.findall(r'<b>([\d,]+)</b><br><small>([\d,]+)</small>', tr)
        first = digits(re.search(r'<td>([\d,]+)(?:万円)?</td>', tr).group(1))
        n += 1
        if first != int(ds) or len(cells) != 5:
            bad += 1; print('NG 早見表の行', ds, first, len(cells))
        for (tot, jm), m in zip(cells, cols):
            exp = ref(int(ds) * 10000, m, 0); n += 2
            if digits(tot) != exp['total']:
                bad += 1; print('NG 早見表 合計', ds, m, tot, exp['total'])
            if digits(jm) != exp['jumin']:
                bad += 1; print('NG 早見表 住民税', ds, m, jm, exp['jumin'])
    # 4) 本文に手で書いた例の数字
    text = await pg.inner_text('main')
    for s, m, where in ((5000000, 300000, '合わせて%s円が目安です'), (5000000, 300000, '年収500万円は%s円'),
                        (7000000, 300000, '年収700万円は%s円')):
        n += 1
        w = where % format(ref(s, m, 0)['total'], ',')
        if w not in text:
            bad += 1; print('NG 本文の例', w)
    # よく聞かれること:給与所得150万円なら5%は7万5,000円/令和8年分の還付申告は令和13年12月31日まで
    n += 1
    if 1500000 * 5 // 100 != 75000 or '7万5,000円を超えた分' not in text:
        bad += 1; print('NG 5%の例')
    n += 1
    if '令和%d年12月31日までです' % (8 + 5) not in text:
        bad += 1; print('NG 還付申告の期限の例')
    # 5) JS が書き換える前の HTML に直に書いた既定の結果(年収500万円・医療費30万円・戻った額0円)
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            'site', 'iryohi-kojo', 'index.html'), encoding='utf-8').read()
    dv = [int(re.search(r'id="%s"[^>]*value="(\d+)"' % i, raw).group(1)) for i in ('inc', 'med', 'hot')]
    exp = ref(*dv)
    for box, key in (('o-k', 'total'), ('o-t', 'shotoku'), ('o-z', 'jumin')):
        n += 1
        m = re.search(r'<b id="%s">([\d,]+)<i>円</i></b>' % box, raw)
        if not m or digits(m.group(1)) != exp[key]:
            bad += 1; print('NG 既定の結果', box, m and m.group(1), exp[key])
    n += 1
    if '<em id="o-e">医療費控除の額は%s円</em>' % format(exp['kojo'], ',') not in raw:
        bad += 1; print('NG 既定の控除額の文', exp['kojo'])
    # 6) 前提の文と、健康診断の例外の文
    for w in ('協会けんぽ東京支部の令和8年度の料率（40歳未満）を12か月分', '協会けんぽ東京・40歳未満',
              '重大な疾病が見つかり', '上限200万円', '総所得金額等が200万円未満の人は、<br>その5%'):
        n += 1
        if w not in raw:
            bad += 1; print('NG 前提の文', w)
    return n, bad

run('iryohi-kojo', body)
