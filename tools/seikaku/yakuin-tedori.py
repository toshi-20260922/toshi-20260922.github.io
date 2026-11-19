# /yakuin-tedori/ 役員報酬の手取りの早見表(月10万〜150万円の手取りと会社負担)。
# 原本:
#  全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分(4月納付分)から改定されます」(47都道府県の料率・介護1.62%・子ども・子育て支援金0.23%は令和8年4月分から)
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  全国健康保険協会「令和8年3月分(4月納付分)からの健康保険・厚生年金保険の保険料額表(東京都)」(全50等級の報酬月額の境目・厚生年金18.300%・
#   厚生年金は93,000円未満が1等級で635,000円以上が32等級・本人負担は50銭以下切り捨て50銭超切り上げ・納入告知書の額は合算額の円未満切り捨て・拠出金0.36%は事業主だけ)
#   https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#  日本年金機構「厚生年金保険料額表」・「保険料額表(令和2年9月分〜)(厚生年金保険と協会けんぽ管掌の健康保険)」(上限は32等級65万円・令和8年度の拠出金率1,000分の3.6)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/index.html
#   https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/20200825.html
#  日本年金機構「子ども・子育て拠出金率が改定されました」(令和2年4月から0.36%) https://www.nenkin.go.jp/oshirase/taisetu/2020/202005/20200514.html
#  日本年金機構 年金委員研修の資料(標準報酬月額の上限:令和9年9月68万円・令和10年9月71万円・令和11年9月75万円)
#   https://www.nenkin.go.jp/service/riyoushabetsu/cooperator/nenkiniin/7.files/shiryo1_2025.pdf
#  国税庁 No.1410 給与所得控除(令和8年分・令和9年分:220万円まで74万円・850万円超は195万円・(注2)220万円未満の表・(注3)660万円未満は別表第五・令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
#  国税庁「所得税のしくみ」(令和8年分の基礎控除:489万円以下104万円・655万円以下67万円・2,350万円以下62万円・48万円・32万円・16万円・2,500万円超0円)
#   https://www.nta.go.jp/publication/pamph/koho/kurashi/html/01_1.htm   (No.1199 基礎控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm)
#  国税庁 No.2260 所得税の税率(速算表・課税所得は1,000円未満切り捨て・復興特別所得税2.1%) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
#  国税庁 No.5211 役員に対する給与(定期同額給与・3月を経過する日まで・臨時改定事由・業績悪化改定事由) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5211.htm
#  大田区「住民税の計算の仕組み」(特別区民税6%・都民税4%・均等割3,000円+1,000円+森林環境税1,000円・令和9年度からの給与所得の表(4,000円刻み)・
#   調整控除(200万円超は2,500円)・課税所得1,000円未満切り捨て・税額100円未満切り捨て) https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/keisannosikumi.html
#  大田区「住民税が課税されない方」(単身は合計所得45万円以下) https://www.city.ota.tokyo.jp/seikatsu/zeikin/kazei/hikazei.html
#  江東区「税額控除の種類」(住民税の基礎控除:2,400万円以下43万円・2,450万円以下29万円・2,500万円以下15万円。調整控除は合計所得2,500万円以下の人が対象)
#   https://www.city.koto.lg.jp/060502/kurashi/zekin/kuminze/zeikoujo.html
#  杉並区「令和9年度からの改正」(住民税の給与所得控除の最低保障額は令和9年度・10年度74万円) https://www.city.suginami.tokyo.jp/s028/12563.html
#  山形労働局「令和8年度の雇用保険料率について」(一般の事業の労働者負担1,000分の5) https://jsite.mhlw.go.jp/yamagata-roudoukyoku/koyouhoken-20260316.html
#  開けなかった原本:東京都主税局「個人住民税」 https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju
# 会社の負担は、被保険者ごとの「全額(1円未満切り捨て)−本人負担」で出す(納入告知額は合算額の円未満切り捨て・事業主はそこから本人負担を引いた残り)。
# 照らすもの:結果の箱(入力欄に値を入れて読む)・JS が作る表2つ・HTML に手で書いた内訳の表2つの全行・本文とよくある質問の数字・JS が書き換える前の元の文
# 最後に原本を確かめた日:2026-11-19
import os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

PREF = [('北海道', 1028), ('青森県', 985), ('岩手県', 951), ('宮城県', 1010), ('秋田県', 1001), ('山形県', 975),
        ('福島県', 950), ('茨城県', 952), ('栃木県', 982), ('群馬県', 968), ('埼玉県', 967), ('千葉県', 973),
        ('東京都', 985), ('神奈川県', 992), ('新潟県', 921), ('富山県', 959), ('石川県', 970), ('福井県', 971),
        ('山梨県', 955), ('長野県', 963), ('岐阜県', 980), ('静岡県', 961), ('愛知県', 993), ('三重県', 977),
        ('滋賀県', 988), ('京都府', 989), ('大阪府', 1013), ('兵庫県', 1012), ('奈良県', 991), ('和歌山県', 1006),
        ('鳥取県', 986), ('島根県', 994), ('岡山県', 1005), ('広島県', 978), ('山口県', 1015), ('徳島県', 1024),
        ('香川県', 1002), ('愛媛県', 998), ('高知県', 1005), ('福岡県', 1011), ('佐賀県', 1055), ('長崎県', 1006),
        ('熊本県', 1008), ('大分県', 1008), ('宮崎県', 977), ('鹿児島県', 1013), ('沖縄県', 944)]
KAIGO, SIEN, NENKIN, KYOSHUTSU = 162, 23, 1830, 36      # 1万分の1の単位
# 協会けんぽの保険料額表の全50等級:(標準報酬月額, 報酬月額がこの額未満)。最後の等級は1,355,000円以上。
TOKYU = [(58000, 63000), (68000, 73000), (78000, 83000), (88000, 93000), (98000, 101000), (104000, 107000),
         (110000, 114000), (118000, 122000), (126000, 130000), (134000, 138000), (142000, 146000), (150000, 155000),
         (160000, 165000), (170000, 175000), (180000, 185000), (190000, 195000), (200000, 210000), (220000, 230000),
         (240000, 250000), (260000, 270000), (280000, 290000), (300000, 310000), (320000, 330000), (340000, 350000),
         (360000, 370000), (380000, 395000), (410000, 425000), (440000, 455000), (470000, 485000), (500000, 515000),
         (530000, 545000), (560000, 575000), (590000, 605000), (620000, 635000), (650000, 665000), (680000, 695000),
         (710000, 730000), (750000, 770000), (790000, 810000), (830000, 855000), (880000, 905000), (930000, 955000),
         (980000, 1005000), (1030000, 1055000), (1090000, 1115000), (1150000, 1175000), (1210000, 1235000),
         (1270000, 1295000), (1330000, 1355000), (1390000, None)]
SOKUSAN = [(1950000, 5, 0), (3300000, 10, 97500), (6950000, 20, 427500), (9000000, 23, 636000),
           (18000000, 33, 1536000), (40000000, 40, 2796000), (None, 45, 4796000)]

def half(x):
    """本人負担の端数:50銭以下切り捨て・50銭超切り上げ。"""
    q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q

def hyojun(m):
    for s, top in TOKYU:
        if top is None or m < top:
            return s

def shaho(mon, rate, old):
    """1か月分。(本人負担, 会社負担)。会社負担は制度ごとの全額(円未満切り捨て)から本人負担を引いた残りと拠出金。"""
    s = hyojun(mon); p = min(max(s, 88000), 650000)
    r = rate + SIEN + (KAIGO if old else 0)
    mk, mn = half(F(s * r, 20000)), half(F(p * NENKIN, 20000))
    return mk + mn, (s * r // 10000 - mk) + (p * NENKIN // 10000 - mn) + p * KYOSHUTSU // 10000

def kyuyo(x):
    """給与所得(令和8年分。住民税は令和9年度分で同じ表)。"""
    if x < 741000: return 0
    if x < 2191000: return x - 740000
    if x < 2193000: return 1451000
    if x < 2196000: return 1453000
    if x < 2200000: return 1456000
    if x < 6600000:
        a = x // 4000 * 4000
        return a * 7 // 10 - 80000 if x < 3600000 else a * 8 // 10 - 440000
    if x < 8500000: return x * 9 // 10 - 1100000
    return x - 1950000

def kiso_shotoku(g):
    for top, k in [(4890000, 1040000), (6550000, 670000), (23500000, 620000), (24000000, 480000), (24500000, 320000), (25000000, 160000)]:
        if g <= top: return k
    return 0

def kiso_jumin(g):
    for top, k in [(24000000, 430000), (24500000, 290000), (25000000, 150000)]:
        if g <= top: return k
    return 0

def ref(mon, rate, old):
    a = mon * 12
    me1, co1 = shaho(mon, rate, old); me, co = me1 * 12, co1 * 12
    g = kyuyo(a)
    # 所得税と復興特別所得税
    t = max(0, g - me - kiso_shotoku(g)) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or t <= top:
            base = t * r // 100 - d; break
    it = base * 1021 // 1000 // 100 * 100
    # 住民税(東京23区・単身)
    if g <= 450000:
        ju = 0
    else:
        tj = max(0, g - me - kiso_jumin(g)) // 1000 * 1000
        if g > 25000000: c6 = c4 = 0                       # 調整控除は合計所得2,500万円以下の人だけ
        else:
            adj = min(50000, tj) if tj <= 2000000 else 50000   # 200万円超は2,500円(=5万円×5%)
            c6, c4 = adj * 3 // 100, adj * 2 // 100
        ju = max(0, tj * 6 // 100 - c6) // 100 * 100 + max(0, tj * 4 // 100 - c4) // 100 * 100 + 5000
    net = a - me - it - ju
    return {'a': a, 's': me, 'i': it, 'j': ju, 't': net, 'c': a + co, 'ce': co}

def r_half_up(fr):
    return (fr + F(1, 2)).__floor__()
def per_month(net): return r_half_up(F(net, 12))
def ritsu(net, a):
    if not a: return '0.0'
    v = r_half_up(F(net * 1000, a)); return '%d.%d' % (v // 10, v % 10)
def f(v): return '{:,}'.format(v)
def d(t): return int(''.join(c for c in t if c.isdigit()) or 0)

JS = """cs=>{var inc=document.getElementById('inc'),pref=document.getElementById('pref'),bs=document.querySelectorAll('#s-age button');
return cs.map(c=>{if(+pref.value!==c[1]){pref.value=String(c[1]);pref.dispatchEvent(new Event('change',{bubbles:true}))}
 if(!bs[c[2]].classList.contains('on'))bs[c[2]].click();
 inc.value=String(c[0]);inc.dispatchEvent(new Event('input',{bubbles:true}));
 return ['o-m','o-y','o-c','o-r','o-br'].map(i=>document.getElementById(i).textContent)})}"""

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'yakuin-tedori', 'index.html'), encoding='utf-8').read()

    # 0 自分の計算を原本の保険料額表(東京)の値と比べる:50万円の折半額と109万円の折半額(健康保険+支援金)
    chk('原本 50万円 健保+支援金の折半', F(500000 * (985 + SIEN), 20000), F(24625) + F(575))
    chk('原本 50万円 介護ありの折半', F(500000 * (985 + SIEN + KAIGO), 20000), F(28675) + F(575))
    chk('原本 50万円 厚生年金の折半', F(500000 * NENKIN, 20000), F(45750))
    chk('原本 109万円 健保+支援金の折半', F(1090000 * (985 + SIEN), 20000), F(536825, 10) + F(12535, 10))
    chk('等級の数', len(TOKYU), 50)

    # 1 都道府県の選択肢(名前・料率・最初は東京都)
    opts = await pg.eval_on_selector_all('#pref option', 'os=>os.map(o=>[o.textContent,o.value,o.selected])')
    chk('都道府県の選択肢', [o[0] for o in opts], ['%s（%d.%02d%%）' % (nm, r // 100, r % 100) for nm, r in PREF])
    chk('選択肢の値', [o[1] for o in opts], [str(i) for i in range(47)])
    chk('最初に選ばれている県', [o[0][:3] for o in opts if o[2]], ['東京都'])

    # 2 結果の箱:入力欄に値を入れて読む
    mons = set()
    for _, top in TOKYU[:-1]:                               # 全50等級の境目(1円下・ちょうど・1円上)
        mons |= {top - 1, top, top + 1}
    mons |= {0, 1, 50000, 61749, 61750, 61751, 95000, 97500, 99167,          # 給与所得0・住民税の非課税の前後
             182583, 182584, 182749, 182750, 182999, 183000, 183333, 183334,  # 219.1万・219.3万・219.6万・220万円
             299999, 300000, 300001, 549999, 550000, 550001, 708333, 708334,  # 360万・660万・850万円
             554629, 554630,                                                  # 給与所得489万円(基礎控除104万円→67万円)
             2120833, 2120834, 2162500, 2162501, 2204166, 2204167, 2245833, 2245834,   # 給与所得2,350万・2,400万・2,450万・2,500万円
             2500000, 2999999, 3000000}
    mons |= set(range(100000, 1500001, 50000)) | set(range(60000, 3000000, 7919))
    # 速算表の境目になる月額を自分の計算で探して前後を足す(東京・40歳未満)
    def kazei(m):
        a = m * 12; g = kyuyo(a); return max(0, g - shaho(m, 985, 0)[0] * 12 - kiso_shotoku(g))
    for top, _, _ in SOKUSAN[:-1]:
        lo, hi = 0, 6000000
        while lo < hi:
            mid = (lo + hi) // 2
            if kazei(mid) > top + 999: hi = mid
            else: lo = mid + 1
        mons |= {lo - 2, lo - 1, lo, lo + 1}
    mons = sorted(m for m in mons if 0 <= m <= 3000000)
    cases = [(m, 12, o) for m in mons for o in (0, 1)]
    for i in (0, 14, 26, 40, 46, 2, 6):                     # 北海道・新潟・大阪・佐賀・沖縄・岩手・福島は境目と代表例
        cases += [(m, i, o) for m in mons[::3] for o in (0, 1)]
    for i in range(47):                                     # 全県:低い・中くらい・高い
        cases += [(m, i, o) for m in (100000, 110000, 300000, 500000, 650000, 1000000, 1500000, 2300000) for o in (0, 1)]
    got = await pg.evaluate(JS, cases)
    for (m, i, o), g in zip(cases, got):
        e = ref(m, PREF[i][1], o)
        want = [f(per_month(e['t'])) + '円', f(e['t']) + '円', f(e['c']) + '円', '手取り率 ' + ritsu(e['t'], e['a']) + '%',
                '年に引かれる額は、社会保険料%s円・所得税%s円・住民税%s円です' % (f(e['s']), f(e['i']), f(e['j']))]
        n += 1
        if g != want:
            bad += 1
            if bad <= 40: print('NG 箱', m, PREF[i][0], o, g, want)

    # 3 JS が作る早見表(選んだ県・年齢)と見出しの文
    ROWS = list(range(10, 101, 5)) + [110, 120, 130, 140, 150]
    for i, o, m in [(12, 0, 500000), (12, 1, 1234567), (26, 1, 90000), (0, 0, 1500000), (46, 1, 427000)]:
        await pg.evaluate(JS, [(m, i, o)])
        chk('表の上の文', await pg.inner_text('#t-cap'), '単身・協会けんぽ%s・%s' % (PREF[i][0], '40〜64歳' if o else '40歳未満'))
        trs = await pg.eval_on_selector_all('#ttb tr', 'ts=>ts.map(t=>[t.className,[].map.call(t.children,d=>d.textContent)])')
        chk('表1の行の数', len(trs), len(ROWS))
        hit = max([k for k, r in enumerate(ROWS) if m >= r * 10000], default=-1)
        chk('黄色の行', [k for k, t in enumerate(trs) if t[0] == 'hit'], [hit] if hit >= 0 else [])
        for r, (_, tds) in zip(ROWS, trs):
            e = ref(r * 10000, PREF[i][1], o)
            chk('表1 %d万円 %s' % (r, PREF[i][0]), tds, [str(r), f(per_month(e['t'])), ritsu(e['t'], e['a']) + '%', f(e['c'])])
    # 会社が払う総額の表(40歳未満・東京都)
    trs = await pg.eval_on_selector_all('#ctb tr', 'ts=>ts.map(t=>[].map.call(t.children,d=>d.textContent))')
    chk('表2の行', [t[0] for t in trs], ['30万円', '50万円', '80万円', '100万円'])
    for t in trs:
        e = ref(d(t[0]) * 10000, 985, 0)
        chk('表2 ' + t[0], t[1:], [f(e['a']), f(e['ce']), f(e['c'])])

    # 4 HTML に手で書いた内訳の表2つの全行(東京・40歳未満と40〜64歳)
    tbs = re.findall(r'<table class="x7tb">.*?</table>', raw, re.S)
    chk('内訳の表の数', len(tbs), 2)
    for o, tb in enumerate(tbs):
        rows = [re.findall(r'<td>(.*?)</td>', tr) for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', tb, re.S)[1:]]
        chk('内訳の表の行 %d' % o, [r[0] for r in rows], ['%d万円' % r for r in ROWS if r != 140])
        for r in rows:
            e = ref(d(r[0]) * 10000, 985, o)
            chk('内訳 %s %d' % (r[0], o), r[1:], [f(e['a']), f(e['s']), f(e['i']), f(e['j']), f(e['t']), f(per_month(e['t'])),
                                               ritsu(e['t'], e['a']) + '%', f(e['c'])])
        chk('色の行 %d' % o, re.findall(r'<tr class="x7hl"><td>(.*?)</td>', tb), ['50万円'])

    # 5 JS が書き換える前の元の文(ファイルの中身)と本文・よくある質問の数字
    e30, e50, e100 = ref(300000, 985, 0), ref(500000, 985, 0), ref(1000000, 985, 0)
    for label, want in [
        ('元の箱 月', '<b id="o-m">%s<i>円</i></b><em id="o-r">手取り率 %s%%</em>' % (f(per_month(e50['t'])), ritsu(e50['t'], e50['a']))),
        ('元の箱 年', '<b id="o-y">%s<i>円</i></b>' % f(e50['t'])),
        ('元の箱 会社', '<b id="o-c">%s<i>円</i></b>' % f(e50['c'])),
        ('元の文 引かれる額', '<li id="o-br">年に引かれる額は、社会保険料%s円・所得税%s円・住民税%s円です</li>' % (f(e50['s']), f(e50['i']), f(e50['j']))),
        ('元の欄', 'id="inc" inputmode="numeric" min="0" max="3000000" step="10000" value="500000"'),
        ('元の表の上の文', '<p class="cap" id="t-cap">単身・協会けんぽ東京都・40歳未満</p>'),
        ('冒頭の文', '報酬月額50万円なら手取りは月およそ%d万円で、会社は保険料を含めて年およそ%d万円を払います。' % (r_half_up(F(e50['t'], 120000)), r_half_up(F(e50['c'], 10000)))),
        ('質問 30万円', '月あたり%s円です。1年の報酬360万円から、社会保険料%s円・所得税%s円・住民税%s円が引かれます。' % (f(per_month(e30['t'])), f(e30['s']), f(e30['i']), f(e30['j']))),
        ('質問 50万円', '手取りは月およそ%d万円で年%s円です。手取り率は%s%%です。' % (r_half_up(F(e50['t'], 120000)), f(e50['t']), ritsu(e50['t'], e50['a']))),
        ('質問 100万円(元の文)', '<p id="q100">40歳未満・単身なら、手取りは月およそ%d万円で年%s円です。手取り率は%s%%です。</p>' % (r_half_up(F(e100['t'], 120000)), f(e100['t']), ritsu(e100['t'], e100['a']))),
        ('拠出金の率', '子ども・子育て拠出金（厚生年金の標準報酬月額の0.36%）'),
        ('厚生年金の頭打ち', '厚生年金の標準報酬月額は65万円が上限なので、報酬月額が635,000円以上になると'),
        ('上限の引き上げ', '上限は令和9年9月から68万円・令和10年9月から71万円・令和11年9月から75万円に上がります。'),
        ('給与所得控除の頭打ち', '年収850万円を超えると控除は195万円で増えなくなる'),
        ('雇用保険料の率', '給料の0.5%の雇用保険料'),
        ('注の料率', '厚生年金18.3%で計算した本人負担です。'),
    ]:
        chk('文 ' + label, want in raw, True)
    chk('質問 100万円(画面)', await pg.inner_text('#q100'), '40歳未満・単身なら、手取りは月およそ%d万円で年%s円です。手取り率は%s%%です。' % (r_half_up(F(e100['t'], 120000)), f(e100['t']), ritsu(e100['t'], e100['a'])))
    # 「50万円の社長は10%、100万円の社長は23%の部分まで」
    def dan(m):
        a = m * 12; g = kyuyo(a); t = max(0, g - shaho(m, 985, 0)[0] * 12 - kiso_shotoku(g)) // 1000 * 1000
        return next(r for top, r, _ in SOKUSAN if top is None or t <= top)
    chk('税率の段 50万円と100万円', (dan(500000), dan(1000000), '報酬月額50万円の社長は10%、100万円の社長は23%の部分まで' in raw), (10, 23, True))
    chk('厚生年金が頭打ちになる月額', (shaho(634999, 985, 0)[0] < shaho(635000, 985, 0)[0], hyojun(634999), hyojun(635000)), (True, 620000, 650000))
    chk('給与所得控除の上限', (8500000 - kyuyo(8500000), 20000000 - kyuyo(20000000), 8499000 - kyuyo(8499000) < 1950000), (1950000, 1950000, True))
    chk('余った閉じタグ', len(re.findall(r'<span\b', raw)), len(re.findall(r'</span>', raw)))
    return n, bad

run('yakuin-tedori', body)
