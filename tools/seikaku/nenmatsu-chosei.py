# /nenmatsu-chosei/ 年末調整の還付金の計算。
# 原本:
#  国税庁「令和8年分 年末調整のしかた」 https://www.nta.go.jp/users/gensen/nencho/index/shikata.htm
#   昨年と比べて変わった点 https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/102.pdf
#   基礎控除等 https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/106.pdf
#   給与と徴収税額の集計(年調年税額=年調所得税額×102.1%・100円未満切り捨て) https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/109.pdf
#   年末調整等のための給与所得控除後の給与等の金額の表 https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/114.pdf
#   算出所得税額の速算表 https://www.nta.go.jp/publication/pamph/gensen/nencho2026/pdf/115.pdf
#  国税庁「令和8年度税制改正(所得税の基礎控除の引上げ等関係)Q&A」 https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf
#  財務省「令和8年度税制改正の大綱」 https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2026/08taikou_01.htm
#  国税庁「令和8年分 月額表の甲欄を適用する給与等に対する税額の電算機計算の特例について」 https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/denshi_01.pdf
#  国税庁「賞与に対する源泉徴収税額の算出率の表(令和8年分)」 https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/15-16.pdf
#  協会けんぽ「令和8年3月分からの健康保険・厚生年金保険の保険料額表(東京)」 https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#  厚生労働省「令和8年度 雇用保険料率のご案内」 https://www.mhlw.go.jp/content/001692566.pdf
#  国税庁 No.1900 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm
#  国税庁 No.1410 給与所得控除(令和8年分・令和9年分は収入220万円まで74万円) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
#  国税庁 No.1199 基礎控除(令和8年分・令和9年分と令和10年分以後の表) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#  国税庁「令和8年分 給与所得の源泉徴収票等の法定調書の作成と提出の手引」(交付と提出の期限は令和9年2月1日) https://www.nta.go.jp/publication/pamph/hotei/tebiki2026/PDF/02.pdf
# 最後に原本を確かめた日:2026-11-21(102・106・107・109・114・115の各PDF・年末調整のしかたのページ・改正Q&A・大綱・電算機計算の特例・
#  賞与の算出率の表・協会けんぽ東京・雇用保険料率・No.1900・No.1410・No.1199・法定調書の手引を開いた)
# 2026-11-21 2回目の見直し:114.pdf(2,191,000〜2,200,000円の3行と6,600,000円以上の式)・115.pdf(速算表・基礎控除・配偶者控除と配偶者特別控除・
#  特定親族特別控除の表)・109.pdf(102.1%・100円未満切り捨て)・102.pdf・電算機計算の特例(第1〜4表)・協会けんぽ令和8年度の料率をもう一度開いて合っていた。
#  102.pdf で子育て世帯の生命保険料控除の上限6万円は令和8・9年分と確かめた。No.1410・No.1199 は許可待ちで開けなかった(同じ数字を 102・114・115 で確かめた)。
# 2026-11-21:ページの JS を整数(一部 BigInt)で掛けて割る形に直した。下の「7」で画面から入れられる年収(1万円きざみ)を全部照らす。
# ページの前提(注記に書いてある):毎月同じ額の給与・令和8年度の料率を12か月に当てはめる・毎月の社会保険料は1円未満を丸めない・
# 賞与は夏と冬の2回同じ額で保険料は50銭以下切り捨て(健康保険と支援金は合わせて丸める)。
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, SITE

# 協会けんぽの等級表(報酬月額の下の境目, 標準報酬月額)
GRADE = [(0, 58), (63, 68), (73, 78), (83, 88), (93, 98), (101, 104), (107, 110), (114, 118), (122, 126), (130, 134),
         (138, 142), (146, 150), (155, 160), (165, 170), (175, 180), (185, 190), (195, 200), (210, 220), (230, 240),
         (250, 260), (270, 280), (290, 300), (310, 320), (330, 340), (350, 360), (370, 380), (395, 410), (425, 440),
         (455, 470), (485, 500), (515, 530), (545, 560), (575, 590), (605, 620), (635, 650), (665, 680), (695, 710),
         (730, 750), (770, 790), (810, 830), (855, 880), (905, 930), (955, 980), (1005, 1030), (1055, 1090),
         (1115, 1150), (1175, 1210), (1235, 1270), (1295, 1330), (1355, 1390)]
def hyojun(m):
    h = 58
    for lo, std in GRADE:
        if m >= lo * 1000: h = std
    return h * 1000
def kenpo_rate(kaigo):                       # 健康保険9.85%+支援金0.23%(+介護1.62%)
    return F(985 + 23 + (162 if kaigo else 0), 10000)
def r50(x):                                  # 50銭以下切り捨て・50銭超切り上げ
    f = x.numerator // x.denominator
    return f + 1 if x - f > F(1, 2) else f
def half_up(x):
    return (2 * x.numerator + x.denominator) // (2 * x.denominator)
def shaho_month(m, kaigo):
    h = hyojun(m); k = min(max(h, 88000), 650000)
    return [h * kenpo_rate(kaigo) / 2, k * F(183, 1000) / 2, m * F(5, 1000)]
# 電算機計算の特例(令和8年分)
def gensen_month(a, n):
    if a <= 158333: ky = F(54167)
    elif a <= 299999: ky = a * F(30, 100) + 6667
    elif a <= 549999: ky = a * F(20, 100) + 36667
    elif a <= 708330: ky = a * F(10, 100) + 91667
    else: ky = F(162500)
    ky = -((-ky.numerator) // ky.denominator)             # 1円未満切り上げ
    if a <= 2120833: ki = 48334
    elif a <= 2162499: ki = 40000
    elif a <= 2204166: ki = 26667
    elif a <= 2245833: ki = 13334
    else: ki = 0
    b = max(a - ky - ki - 31667 * n, F(0))
    T = [(162500, 5105, 0), (275000, 10210, 8296), (579166, 20420, 36374), (750000, 23483, 54113),
         (1500000, 33693, 130688), (3333333, 40840, 237893), (None, 45945, 408061)]
    for top, r, d in T:
        if top is None or b <= top:
            t = max(b * F(r, 100000) - d, F(0)); break
    return half_up(t / 10) * 10                           # 10円未満四捨五入
# 賞与の算出率の表(令和8年分・甲欄。千円未満の境目)
SHOYO = {0: [82, 94, 260, 309, 342, 372, 402, 433, 520, 605, 684, 715, 752, 795, 854, 922, 1318, 1521, 2621, 3495],
         1: [107, 250, 289, 346, 373, 401, 430, 463, 520, 621, 705, 739, 778, 821, 882, 952, 1342, 1526, 2645, 3527]}
RITSU = [0, 2042, 4084, 6126, 8168, 10210, 12252, 14294, 16336, 18378, 20420, 22462, 24504, 26546, 28588, 30630,
         32672, 35735, 38798, 41861, 45945]
# 年末調整等のための給与所得控除後の給与等の金額の表(令和8年分)
def kyuyo_shotoku(s):
    if s < 741000: return 0
    if s < 2191000: return s - 740000
    if s < 2193000: return 1451000
    if s < 2196000: return 1453000
    if s < 2200000: return 1456000
    if s < 3600000: return s // 4000 * 4000 * 7 // 10 - 80000
    if s < 6600000: return s // 4000 * 4000 * 8 // 10 - 440000
    if s < 8500000: return s * 9 // 10 - 1100000
    return s - 1950000
def kiso(x):
    for top, v in ((4890000, 1040000), (6550000, 670000), (23500000, 620000), (24000000, 480000),
                   (24500000, 320000), (25000000, 160000)):
        if x <= top: return v
    return 0
def haigusha(x):
    return 380000 if x <= 9000000 else 260000 if x <= 9500000 else 130000 if x <= 10000000 else 0
SOKUSAN = [(1950000, 5, 0), (3300000, 10, 97500), (6950000, 20, 427500), (9000000, 23, 636000),
           (18000000, 33, 1536000), (40000000, 40, 2796000), (None, 45, 4796000)]
def ref(S, B, hg, kg, ideco=0, seiho=0, loan=0):
    if B >= S or S <= 0: return {'ng': 1}
    m = F(S - B, 12); sh = kyuyo_shotoku(S)
    n = hg if sh <= 9000000 else 0                        # 源泉控除対象配偶者は本人の合計所得900万円以下
    sm = shaho_month(m, kg)
    t = gensen_month(m - sum(sm), n) * 12
    sa = half_up(sum(sm) * 12)
    if B > 0:
        b = B // 2
        a = m - (r50(sm[0]) + r50(sm[1]) + r50(sm[2]))
        idx = 20
        for j, c in enumerate(SHOYO[n]):
            if a < c * 1000: idx = j; break
        room = 5730000
        for _ in range(2):
            s = b // 1000 * 1000; kb = min(s, room); room -= kb
            x = r50(kb * kenpo_rate(kg) / 2) + r50(min(s, 1500000) * F(183, 1000) / 2) + r50(b * F(5, 1000))
            if b - x > a * 10: return {'ng': 2}
            t += (b - x) * RITSU[idx] // 100000
            sa += x
    ki = kiso(sh)
    ko = sa + ki + (haigusha(sh) if hg else 0) + ideco + seiho
    base = max(sh - ko, 0) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or base <= top:
            san = base * r // 100 - d; break
    z = max(san - loan, 0) * 1021 // 1000 // 100 * 100
    return {'ng': 0, 't': t, 'z': z, 'k': t - z, 'ki': ki, 'sh': sh, 'sa': sa}

def digits(t):
    return int(''.join(c for c in t if c.isdigit()) or 0)

async def body(pg):
    n = bad = 0
    def chk(label, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp:
            bad += 1; print('NG', label, '画面', got, '原本から', exp)
    # 1 関数どうし
    Ss = list(range(1500000, 20000001, 100000))
    Ss += [1, 740999, 741000, 741001, 1000000, 2190999, 2191000, 2192999, 2193000, 2195999, 2196000, 2199999, 2200000,
           2200001, 3599999, 3600000, 3600001, 6599999, 6600000, 6600001, 6655555, 6655556, 6655557, 8499999, 8500000,
           8500001, 10949999, 10950000, 10950001, 11450000, 11450001, 11950000, 11950001, 19999999, 20000000]
    for lo, _ in GRADE[1:]:                                # 等級の境目の前後(月給がちょうど・1円下・1円上)
        Ss += [lo * 1000 * 12 - 12, lo * 1000 * 12, lo * 1000 * 12 + 12]
    for a in (158333, 299999, 549999, 708330):             # 月の給与所得控除の帯の近く
        Ss += [a * 12 * 100 // 85 // 10000 * 10000 + d for d in (-10000, 0, 10000, 20000)]
    Ss = sorted(set(s for s in Ss if s <= 20000000))
    for S in Ss:
        for hg in (0, 1):
            for kg in (0, 1):
                got = await pg.evaluate('([S,h,k])=>window.__nencho(S,0,h,k,0,0,0)', [S, hg, kg])
                exp = ref(S, 0, hg, kg)
                chk('賞与なし S=%d 配偶者%d 介護%d' % (S, hg, kg), {k: got.get(k) for k in exp}, exp)
    for S in list(range(2000000, 20000001, 500000)) + [3990000, 4010000, 6660000, 12660000]:
        for B in (10000, 300000, 1000000, S // 5 // 10000 * 10000, S // 3 // 10000 * 10000, 6000000, S - 10000, S):
            for hg, kg in ((0, 0), (1, 1)):
                got = await pg.evaluate('([S,B,h,k])=>window.__nencho(S,B,h,k,0,0,0)', [S, B, hg, kg])
                exp = ref(S, B, hg, kg)
                chk('賞与あり S=%d B=%d 配偶者%d' % (S, B, hg), {k: got.get(k) for k in exp}, exp)
    for S in (3000000, 5000000, 6000000, 6660000, 9000000, 15000000):
        for ide, sei, loan in ((276000, 0, 0), (0, 170000, 0), (0, 0, 500000), (816000, 120000, 135000), (144000, 50000, 2000)):
            got = await pg.evaluate('([S,i,s,l])=>window.__nencho(S,0,1,0,i,s,l)', [S, ide, sei, loan])
            exp = ref(S, 0, 1, 0, ide, sei, loan)
            chk('控除あり S=%d' % S, {k: got.get(k) for k in exp}, exp)
    # 2 HTML に手で書いた早見表の全行
    html = open(os.path.join(SITE, 'nenmatsu-chosei', 'index.html'), encoding='utf-8').read()
    # 2026-11-24:早見表を「年収・戻る額(単身)・戻る額(配偶者控除あり)」の3列にし、天引きと調整後の所得税は内訳の表(tb2)へ分けた
    rows = re.findall(r'<tr data-s="(\d+)">(.*?)</tr>', html)
    chk('早見表の行の数', len(rows), 22)
    chk('早見表の列の題', re.search(r'<thead><tr>(.*?)</tr></thead>\s*<tbody id="tb">', html, re.S).group(1),
        '<th>年収</th><th>戻る額<br>単身</th><th>戻る額<br>配偶者控除あり</th>')
    rows2 = re.findall(r'<tr>(<td>[\d,]+万円</td>.*?)</tr>', html[html.index('id="tb2"'):html.index('</tbody>', html.index('id="tb2"'))])
    chk('内訳の表の行の数', len(rows2), 22)
    for (s, tds), t2 in zip(rows, rows2):
        c = [digits(x) for x in re.findall(r'<td>(.*?)</td>', tds)]
        c2 = [digits(x) for x in re.findall(r'<td>(.*?)</td>', t2)]
        S = int(s) * 10000; a = ref(S, 0, 0, 0); h = ref(S, 0, 1, 0)
        chk('早見表 %s万円' % s, c, [int(s), a['k'], h['k']])
        chk('早見表 %s万円 年収の字' % s, re.findall(r'<td>(.*?)</td>', tds)[0], '{:,}万円'.format(int(s)))
        chk('内訳 %s万円' % s, c2, [int(s), a['t'], a['z'], kiso(kyuyo_shotoku(S)) // 10000])
    # 3 文の中の金額
    r6 = ref(6000000, 0, 0, 0)
    chk('冒頭の600万円', '年収600万円・単身の場合、戻る額の目安は%s円です' % format(r6['k'], ',') in html, True)
    chk('QAの600万円', '目安は%s円です。毎月の天引きの1年分が%s円で年末調整で決まる所得税が%s円' % (
        format(r6['k'], ','), format(r6['t'], ','), format(r6['z'], ',')) in html, True)
    chk('400万円と700万円', '年収400万円・単身なら戻る額は%s円、年収700万円・単身なら%s円です' % (
        format(ref(4000000, 0, 0, 0)['k'], ','), format(ref(7000000, 0, 0, 0)['k'], ',')) in html, True)
    # 4 表と注記の定数(原本の値)
    # 合計所得489万円・655万円・2,350万円にあたる給与の年収
    top489 = max(s for s in range(6650000, 6660000) if kyuyo_shotoku(s) <= 4890000)
    chk('489万円にあたる年収', top489, 6655556)
    chk('655万円にあたる年収', max(s for s in range(8490000, 8510000) if kyuyo_shotoku(s) <= 6550000), 8500000)
    chk('2,350万円にあたる年収', 23500000 + 1950000, 25450000)
    for label, frag in [
        ('基礎控除489万円以下', '489万円以下</td><td class="l">104万円</td><td class="l">68万〜95万円</td>'),
        ('基礎控除655万円以下', '655万円以下</td><td class="l">67万円</td><td class="l">63万円</td>'),
        ('基礎控除2,350万円以下', '2,350万円以下</td><td class="l">62万円</td><td class="l">58万円</td>'),
        ('給与所得控除の最低額', '最低額</td><td class="l">74万円</td><td class="l">65万円</td>'),
        ('扶養の所得', '<td class="l">62万円以下<br>給与だけなら<br>136万円以下</td><td class="l">58万円以下<br>給与だけなら<br>123万円以下</td>'),
        ('生命保険料控除', '<td class="l">上限6万円</td><td class="l">上限4万円</td>'),
        ('差の表1', '<td class="l">665万5,556円まで</td><td>104万円</td><td>46万円</td>'),
        ('差の表2', '<td class="l">665万5,556円超〜850万円</td><td>67万円</td><td>9万円</td>'),
        ('差の表3', '<td class="l">850万円超〜2,545万円</td><td>62万円</td><td>4万円</td>'),
        ('扶養親族', '<span class="nw">136万円以下</span></td><td class="l"><span class="nw">123万円以下</span>'),
        ('特定親族', '<span class="nw">136万円超</span><br><span class="nw">197万円以下</span></td><td class="l"><span class="nw">123万円超</span><br><span class="nw">188万円以下</span>'),
        ('配偶者特別控除', '<span class="nw">136万円超</span><br><span class="nw">207万円以下</span></td><td class="l"><span class="nw">123万円超</span><br><span class="nw">201万5,999円以下</span>'),
        ('勤労学生', '<span class="nw">163万円以下</span></td><td class="l"><span class="nw">150万円以下</span>'),
        ('料率', '健康保険9.85%・子ども子育て支援金0.23%・厚生年金18.3%を会社と半分ずつ・40歳未満）と雇用保険0.5%'),
        ('配偶者控除の額', '控除額は38万円です。本人の合計所得が900万円を超えると26万円・950万円を超えると13万円に下がり、1,000万円を超えると受けられません。'),
        ('施行日', '改正は令和8年12月1日に始まり'),
        ('令和9年分の税額表', '令和9年1月1日以後に支払われる給与からは、改正後の「令和9年分 源泉徴収税額表」が使われます。'),
        ('2,000万円', '給与の収入が2,000万円を超える方は、年末調整の対象になりません。'),
        ('月の基礎控除58万円', '毎月の天引きは基礎控除58万円で計算されます。'),
    ]:
        chk(label, frag in html, True)
    # 収入の上限は所得の上限から出す(給与所得控除の最低74万円。207万円は表で所得133万円になる上の端)
    chk('62万+74万', 620000 + 740000, 1360000)
    chk('123万+74万', 1230000 + 740000, 1970000)
    chk('89万+74万', 890000 + 740000, 1630000)
    chk('配偶者特別控除の上の端', kyuyo_shotoku(2070000) <= 1330000 < kyuyo_shotoku(2070001), True)
    chk('月の基礎控除', 48334 * 12 // 10000, 58)
    # 6 2026-11-20 に足した分:並び替えのあとの文と、合計所得900万円の境目
    chk('早見表は上にある', html.index('id="list"') < html.index('id="calc"'), True)
    chk('計算の箱の文は「上の早見表」', '<li>上の早見表は、選んだ年齢と賞与で計算した額です。控除の申告は入れていません</li>' in html and '下の早見表' not in html, True)
    chk('900万円の注記', '合計所得が900万円を超える年収1,200万円以上の行は、毎月の天引きを配偶者なしで計算しています。' in html, True)
    over = [int(s) for s, _ in rows if kyuyo_shotoku(int(s) * 10000) > 9000000]
    chk('合計所得900万円超の行', over, [1200, 1500, 2000])
    chk('合計所得900万円にあたる年収', 9000000 + 1950000, 10950000)
    # 去年(改正前)の基礎控除は58万円に37万・30万・10万・5万円を足した額。今年は62万円に42万・5万円(年末調整のしかた 昨年と比べて変わった点 注2)
    chk('去年の基礎控除', [58 + x for x in (37, 30, 10, 5, 0)], [95, 88, 68, 63, 58])
    chk('今年の基礎控除', [62 + x for x in (42, 5, 0)], [104, 67, 62])
    # 生命保険料控除12万円+地震保険料控除5万円(年末調整のしかた 保険料控除)
    chk('保険の控除の上限', 120000 + 50000, 170000)
    chk('保険の控除の文', '申告書に書く控除額です（最大17万円）' in html and 'id="sei" inputmode="decimal" min="0" max="17"' in html, True)
    chk('更新日', '更新日：2026年11月21日（' in html, True)
    # 7 2026-11-21 に足した分
    # 画面から入れられる年収(1万円きざみ・1万〜2,000万円)を賞与なしで全部
    allS = [x * 10000 for x in range(1, 2001)]
    for hg in (0, 1):
        for kg in (0, 1):
            got = await pg.evaluate('([L,h,k])=>L.map(S=>window.__nencho(S,0,h,k,0,0,0))', [allS, hg, kg])
            for S, g in zip(allS, got):
                exp = ref(S, 0, hg, kg)
                chk('全部の年収 S=%d 配偶者%d 介護%d' % (S, hg, kg), {k: g.get(k) for k in exp}, exp)
    # 賞与あり(年収10万円きざみ・賞与は年収の1割〜5割と端の額)
    for S in range(1500000, 20000001, 100000):
        for B in (S // 10 // 10000 * 10000, S // 4 // 10000 * 10000, S // 2 // 10000 * 10000, 10000, 11470000, 3010000):
            for hg, kg in ((0, 0), (1, 0), (0, 1), (1, 1)):
                got = await pg.evaluate('([S,B,h,k])=>window.__nencho(S,B,h,k,0,0,0)', [S, B, hg, kg])
                exp = ref(S, B, hg, kg)
                chk('賞与あり2 S=%d B=%d 配偶者%d 介護%d' % (S, B, hg, kg), {k: got.get(k) for k in exp}, exp)
    # 計算の箱に直に書いた既定の結果(JS が動く前の字。年収500万円・単身・40歳未満)
    e5 = ref(5000000, 0, 0, 0)
    chk('直に書いた既定の結果', all(x in html for x in (
        '<b id="o-k">%s<i>円</i></b>' % format(e5['k'], ','), '<b id="o-t">%s<i>円</i></b>' % format(e5['t'], ','),
        '<b id="o-z">%s<i>円</i></b><em id="o-b">基礎控除%d万円</em>' % (format(e5['z'], ','), e5['ki'] // 10000))), True)
    # 給与所得控除74万円は収入220万円まで(No.1410。改正Q&A Q3-1 は収入200万円の給与所得を126万円と書く。去年は200万円×30%+8万円=68万円)
    chk('収入200万円の給与所得', kyuyo_shotoku(2000000), 1260000)
    chk('収入220万円の給与所得', kyuyo_shotoku(2200000), 2200000 - 740000)
    chk('収入220万4,000円の控除は74万円より多い', 2204000 - kyuyo_shotoku(2204000) > 740000, True)
    chk('表の行 360万円・659万6,000円', [kyuyo_shotoku(3600000), kyuyo_shotoku(6596000)], [2440000, 4836800])
    chk('220万円の文', '年収220万円未満の方は、給与所得控除が74万円に上がる分も年末調整で反映されます。' in html and '年収190万円以下' not in html, True)
    # 令和8年分の源泉徴収票の交付・給与支払報告書の提出の期限は令和9年2月1日(1月31日が日曜日)
    import datetime
    chk('2027年1月31日は日曜日', datetime.date(2027, 1, 31).weekday(), 6)
    chk('期限の行', '<td class="l">2027年2月1日まで</td>' in html and '令和8年分は1月31日が日曜日のため、期限は2月1日になる' in html and '翌年1月31日まで' not in html, True)
    # JS に小数の率が残っていないか(整数で掛けて割る形)
    js = html[html.index(' var H=[58,'):html.index(' window.__nencho=calc;')]
    chk('JS に小数の定数なし', re.findall(r'(?<![\d])0?\.\d+', js), [])
    # 5 画面の操作
    async def show():
        return [digits(await pg.inner_text('#o-' + k)) for k in 'tzk'], await pg.inner_text('#o-e'), await pg.inner_text('#o-b')
    e = ref(5000000, 0, 0, 0)
    v, msg, kb = await show()
    chk('既定の500万円', v, [e['t'], e['z'], e['k']]); chk('既定の基礎控除の字', kb, '基礎控除104万円')
    hit = await pg.evaluate('document.querySelector("#tb tr.hit").getAttribute("data-s")'); chk('黄色の行', hit, '500')
    # 早見表の切り替えと行のタップ(2026-11-24 本人「黄色くならないし」「えらべないし」)
    async def tbl():
        return await pg.evaluate("()=>[...document.querySelectorAll('#tb tr')].map(r=>[r.getAttribute('data-s'),...[...r.cells].map(c=>c.textContent)])")
    for ag in (0, 1):
        for bn in (0, 1):
            await pg.click('#nca button[data-v="%d"]' % ag); await pg.click('#ncb button[data-v="%d"]' % bn)
            got = await tbl()
            for r in got:
                S = int(r[0]) * 10000; B = S // 4 if bn else 0
                chk('切り替え 年齢%d 賞与%d %s万円' % (ag, bn, r[0]), [(-1 if r[2].startswith('−') else 1) * digits(r[2]), (-1 if r[3].startswith('−') else 1) * digits(r[3])], [ref(S, B, 0, ag)['k'], ref(S, B, 1, ag)['k']])
            chk('切り替えと計算の箱の年齢 %d' % ag, await pg.evaluate("document.querySelector('#s-a .on').getAttribute('data-v')"), str(ag))
    await pg.click('#tb tr[data-s="300"]')
    chk('行をタップすると年収が入る', await pg.input_value('#inc'), '300')
    chk('行をタップすると黄色', await pg.evaluate('document.querySelector("#tb tr.hit").getAttribute("data-s")'), '300')
    await pg.fill('#bon', '150'); await pg.dispatch_event('#bon', 'input')
    chk('賞与を入れても黄色', await pg.evaluate('(document.querySelector("#tb tr.hit")||{}).getAttribute ? document.querySelector("#tb tr.hit").getAttribute("data-s") : null'), '300')
    chk('賞与を入れると賞与ありの表', await pg.evaluate("document.querySelector('#ncb .on').getAttribute('data-v')"), '1')
    await pg.fill('#bon', '0'); await pg.dispatch_event('#bon', 'input'); await pg.click('#nca button[data-v="0"]')
    await pg.fill('#inc', '700'); await pg.click('#s-h button[data-v="1"]'); await pg.click('#s-a button[data-v="1"]')
    e = ref(7000000, 0, 1, 1); v, msg, kb = await show()
    chk('700万円・配偶者・40〜64歳', v, [e['t'], e['z'], e['k']]); chk('基礎控除の字67万円', kb, '基礎控除67万円')
    await pg.fill('#bon', '150'); await pg.evaluate('document.querySelector("details.more").open=true')
    await pg.fill('#ide', '27.6'); await pg.fill('#sei', '20'); await pg.fill('#loan', '13.5')
    e = ref(7000000, 1500000, 1, 1, 276000, 170000, 135000); v, msg, kb = await show()
    chk('賞与と控除を入れた表示', v, [e['t'], e['z'], abs(e['k'])])
    chk('不足の字', msg, '12月の給与で精算' if e['k'] >= 0 else '戻らず、この額が不足します')
    await pg.fill('#inc', '2001'); v, msg, kb = await show(); chk('2,000万円超の字', msg.startswith('年収2,000万円を超える人は年末調整の対象外'), True)
    await pg.fill('#inc', '300'); await pg.fill('#bon', '300'); v, msg, kb = await show(); chk('賞与が年収以上', msg, '賞与は、年収より小さい額を入力してください')
    return n, bad
run('nenmatsu-chosei', body)
