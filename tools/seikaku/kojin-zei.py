# /kojin-zei/ 個人事業主の手取りの早見表。
# 原本:
# 国税庁 No.1199 基礎控除(令和8年分・令和9年分:合計所得489万円以下104万円・655万円以下67万円・2,350万円以下62万円・以後48万/32万/16万/0。令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#   https://www.nta.go.jp/users/gensen/nencho/index/kyuyosyotokusya.htm (令和8年分の基礎控除の表)
# 国税庁 No.2072 青色申告特別控除(55万円・65万円・10万円) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2072.htm
# 国税庁 No.2260 所得税の税率(速算表・課税される所得金額は1,000円未満切り捨て・復興特別所得税2.1%)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
# 東京都主税局 個人事業税(事業主控除290万円・税率3〜5%・青色申告特別控除は適用なし・8月と11月)
#   https://www.tax.metro.tokyo.lg.jp/kazei/work/kojin_ji
# 東京都主税局 個人住民税(都民税4%・区市町村民税6%・均等割1,000円+3,000円・森林環境税1,000円・調整控除・45万円以下は非課税)
#   https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju
# 中央区 基礎控除(住民税。2,400万円以下43万円・2,450万円以下29万円・2,500万円以下15万円・超は0円)
#   https://www.city.chuo.lg.jp/a0009/kurashi/zeikin/juuminzei/shotokukoujo/zintekikozyo.html
# 日本年金機構 国民年金保険料(令和8年度 月17,920円) https://www.nenkin.go.jp/service/kokunen/hokenryo/hokenryo.html
# 国民健康保険(令和8年度。料率は tools/regions.py。2026-11-19 に公式ページで確かめたのは次の3つ)
#   東京23区:世田谷区「保険料の計算方法」 https://www.city.setagaya.lg.jp/02060/297.html
#            世田谷区「保険料の軽減・減免について」(7割43万円・5割+31万円×人数・2割+57万円×人数) https://www.city.setagaya.lg.jp/02060/300.html
#   横浜市「令和8年度保険料の料率等について」 https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/r7hokennryouritu.html
#   大阪府「令和8年度大阪府市町村標準保険料率等の算定結果について」(医療分の上限は66万円) https://www.pref.osaka.lg.jp/o100080/kokuho/iryouseido/hokenryouritsu/hokenryouritsu2.html
# 照らすもの:画面の結果(22の市区町村×青色3通り×年齢2通り×利益)・JS の料率と regions.py・HTML に手で書いた表2つの全行・JS が作る表・本文の数字
# 税額の端数:所得税と復興特別所得税の合計は100円未満切り捨て(申告納税額)・住民税の所得割は区市町村分と都道府県分でそれぞれ100円未満切り捨て・個人事業税は課税標準1,000円未満と税額100円未満を切り捨て
# 2026-11-20 に確かめ直したもの:
#   国税庁 No.1199・「給与所得者(従業員)の方へ(令和8年分)」の基礎控除の表(489万円以下104万円・655万円以下67万円・2,350万円以下62万円・48万/32万/16万)
#   国税庁 No.2072(令和8年4月1日現在。55万円=複式簿記と期限内申告・65万円=さらに優良な電子帳簿か e-Tax・10万円=それ以外。令和9年分からの改正はこのページに無い)
#   国税庁「令和9年分から青色申告特別控除はどう変わる?」(令和9年分から。複式簿記と e-Tax で65万円・優良な電子帳簿も満たすと75万円) https://www.nta.go.jp/taxes/shiraberu/shinkoku/kojin_jigyo/0026004-012.pdf
#   国税庁 No.2260(速算表・1,000円未満切り捨て・復興特別所得税2.1%)
#   東京都主税局 個人事業税(事業主控除290万円・第1種5%・第2種4%・第3種5%と3%・青色申告特別控除は所得に加算・8月と11月・法定業種は70)
#   東京都主税局 個人住民税(調整控除・都民税4%と区市町村民税6%・均等割1,000円と3,000円・森林環境税1,000円・45万円以下は非課税・年4回)
#   浦添市「令和9年度からの個人住民税の主な改正点」(住民税の基礎控除43万円は変更なし) https://www.city.urasoe.lg.jp/doc/2026102300129
#   大阪市「所得控除額の計算」(住民税の基礎控除 43万円・29万円・15万円) https://www.city.osaka.lg.jp/zaisei/page/0000370588.html
#   日野市「令和8年度国民健康保険税の税制改正に伴う変更について」(上限 67万・26万・17万・3万円。軽減 43万円・+31万円×人数・+57万円×人数) https://www.city.hino.lg.jp/kurashi/kokuhonenkin/1023198/1023199/1030606.html
#   日本年金機構 国民年金保険料(令和8年度 月17,920円)
# 2026-11-20 に足した照らし合わせ:青色申告特別控除の表(55万円・10万円・白色の列。5行)・黄色の行(入力した利益を超えない中でいちばん近い行)
# 2026-11-21 に確かめ直したもの:国税庁「給与所得者(従業員)の方へ(令和8年分)」の基礎控除の表・No.1199(令和8年4月1日現在)・No.2072・No.2260・
#   「令和8年度税制改正(所得税の基礎控除の引上げ等関係)Q&A」(題名と令和8年5月)・東京都主税局 個人事業税と個人住民税・
#   東京都保健医療局「令和8年度 特別区国民健康保険料一覧表」・世田谷区「保険料の計算方法」・横浜市「保険料について」(令和8年度の軽減 43万円・+31万円・+57万円)・
#   仙台市「令和9年度(令和8年分)から適用される個人市県民税の税制改正等について」(住民税の基礎控除は改正なし・非課税の所得45万円以下は同じ)・日本年金機構 国民年金保険料
# 2026-11-21 に足した照らし合わせ:計算の箱に直に書いた既定の結果(JS が書き換える前の HTML。申し送りの形11・16)
# 最後に原本を確かめた日:2026-11-21
import os, sys, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fractions import Fraction
from _lib import run, PICK_JS, SITE
import regions
import rates

NEN = rates.NENKIN_KOKUMIN * 12
SOKUSAN = rates.sokusan_ue_m1000()
KISO = rates.KISO_SHOTOKU
JKISO = rates.KISO_JUMIN
CAPS = rates.kokuho_caps()

def step(tbl, g):
    for top, v in tbl:
        if g <= top:
            return v
    return 0

def shotokuzei(g, sh):
    t = max(0, g - sh - step(KISO, g)) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or t <= top:
            b = t * r // 100 - d
            break
    return max(0, b) * rates.FUKKO_NUM // rates.FUKKO_DEN // 100 * 100

def juminzei(g, sh):
    if g <= 450000:
        return 0
    t = max(0, g - sh - step(JKISO, g)) // 1000 * 1000
    if g > 25000000:
        sa = 0
    elif t <= 2000000:
        sa = min(50000, t)
    else:
        sa = 50000          # {5万円-(課税所得-200万円)}の5%は2,500円未満になるので2,500円
    shi = max(0, t * 6 // 100 - sa * 3 // 100) // 100 * 100
    ken = max(0, t * 4 // 100 - sa * 2 // 100) // 100 * 100
    return shi + ken + 5000

def jigyozei(a):
    return max(0, a - 2900000) // 1000 * 1000 * 5 // 100 // 100 * 100

def kokuho(R, g, old):
    """単身。R は regions.py の1件。"""
    base = max(0, g - rates.KEIGEN_BASE)
    kei = rates.keigen(g, 1)
    tot = 0
    for i, (ritsu, kinto, byodo, cap) in enumerate(R['p']):
        if i == 2 and not old:
            continue
        v = base * ritsu // 10000 + kinto * (10 - kei) // 10 + byodo * (10 - kei) // 10
        if R['nag'] and i == 0 and kei:
            v = max(0, v - 2000)
        tot += min(cap, v // R['r'] * R['r'])
    return tot

def ref(R, a, ao, old):
    g = max(0, a - min(ao, a))
    k = kokuho(R, g, old)
    sh = k + NEN
    it, ju, jg = shotokuzei(g, sh), juminzei(g, sh), jigyozei(a)
    return dict(k=k, sh=sh, it=it, ju=ju, jg=jg, tax=it + ju + jg, net=a - it - ju - jg - sh)

def half_up(fr):
    return (fr.numerator * 2 + fr.denominator) // (2 * fr.denominator)

def d(t):
    return int(''.join(c for c in t if c.isdigit()) or 0)

READ = '''([ri,ao,old,as])=>{''' + PICK_JS + '''(ri);
 document.querySelector('#s-ao button[data-v="'+ao+'"]').click();document.querySelector('#s-age button[data-v="'+old+'"]').click();
 var inc=document.getElementById("inc"),o=[];as.forEach(function(a){inc.value=a;inc.dispatchEvent(new Event("input"));
  o.push(["o-n","o-t","o-s","o-br","o-sh","o-nr"].map(function(i){return document.getElementById(i).textContent;}));});return o;}'''

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, '画面', got, '原本から', want)
    html = open(os.path.join(SITE, 'kojin-zei', 'index.html'), encoding='utf-8').read()
    # 1 JS の料率と regions.py
    RG = json.loads(re.search(r'var RG=(\[.*?\]);\n', html).group(1))
    chk('市区町村の数', len(RG), len(regions.REG))
    for a, b in zip(RG, regions.REG):
        chk('料率 ' + b['s'], (a['p'], a['r'], a['g']), (b['p'], b['r'], b['nag']))
    # 2026-11-19 に公式ページで確かめた3つ
    OFF = {'東京23区': [[751, 47600, 0, 670000], [280, 17600, 0, 260000], [243, 17800, 0, 170000], [27, 1873, 0, 30000]],
           '横浜市': [[833, 40870, 0, 670000], [262, 13380, 0, 260000], [284, 16200, 0, 170000], [34, 1770, 0, 30000]],
           '大阪市・堺市': [[950, 34990, 33908, 660000], [306, 11191, 10845, 260000], [260, 18682, 0, 170000], [28, 1841, 0, 30000]]}
    for a in RG:
        if a['s'] in OFF:
            chk('公式ページの料率 ' + a['s'], a['p'], OFF[a['s']])
    # 2 画面の結果
    GS = [430000, 740000, 1000000, 4890000, 6550000, 23500000, 24000000, 24500000, 25000000]
    for ri, R in enumerate(regions.REG):
        for ao in (650000, 100000, 0):
            for old in (0, 1):
                As = [0, 1, 99999, 2000000, 2899999, 2900000, 2900999, 2901000, 2999999, 3000000, 5000000, 5540000, 5550000,
                      7200000, 7210000, 8000000, 8890000, 8900000, 11490000, 11500000, 15000000, 20000000, 30000000, 50000000]
                for g in GS:
                    As += [g + ao - 1, g + ao, g + ao + 1, g + ao + 1000]
                As += list(range(1830000, 20000000, 371000))
                got = await pg.evaluate(READ, [ri, ao, old, As])
                for a, t in zip(As, got):
                    e = ref(R, a, ao, old); n += 1
                    br = [d(x) for x in re.findall(r'[0-9,]+円', t[3])]
                    sh = [d(x) for x in re.findall(r'[0-9,]+円', t[4])]
                    pct = half_up(Fraction(e['net'] * 100, a)) if a else 0
                    g2 = (-d(t[0]) if t[0].startswith('-') else d(t[0]), d(t[1]), d(t[2]), br, sh, t[5])
                    w2 = (e['net'], e['tax'], e['sh'], [e['it'], e['ju'], e['jg']], [e['k'], NEN], '利益の%d%%' % pct)
                    if g2 != w2:
                        bad += 1
                        if bad < 40: print('NG', R['s'], a, ao, old, g2, w2)
    # 3 はじめの形に戻して、JS が作る表(11行)
    await pg.evaluate(READ, [0, 650000, 0, [5000000]])
    TK = regions.REG[0]
    rows = await pg.evaluate('()=>[].map.call(document.querySelectorAll("#tb tr"),function(r){return [].map.call(r.cells,function(c){return c.textContent;});})')
    chk('JS の表の行数', len(rows), 11)
    for r in rows:
        e = ref(TK, d(r[0]) * 10000, 650000, 0)
        chk('JS の表 %s万円' % r[0], [d(x) for x in r[1:]], [e['tax'], e['sh'], e['net']])
    chk('表の見出し', await pg.inner_text('#t-cap'), '青色申告65万円・40歳未満・東京23区')
    text = await pg.inner_text('main')
    def has(label, s):
        chk(label + ' 「' + s + '」', s in text, True)
    f = lambda v: format(v, ',')
    # 4 手で書いた表2つ(各27行)
    tbs = await pg.evaluate('()=>[].map.call(document.querySelectorAll("table.x7t10"),function(t){return [].map.call(t.tBodies[0].rows,function(r){return [].map.call(r.cells,function(c){return c.textContent;});});})')
    chk('手で書いた表の数', len(tbs), 2)
    want_a = list(range(200, 1000, 50)) + list(range(1000, 2001, 100))
    for old, tb in enumerate(tbs):
        chk('表%d の利益の並び' % old, [d(r[0]) for r in tb], want_a)
        for r in tb:
            a = d(r[0]) * 10000; e = ref(TK, a, 650000, old)
            tot = e['tax'] + e['sh']
            p10 = half_up(Fraction(e['net'] * 1000, a))
            want = [e['it'], e['ju'], e['jg'], e['k'], NEN, tot, e['net'], half_up(Fraction(e['net'], 12)), '%d.%d%%' % (p10 // 10, p10 % 10)]
            chk('表%d %s' % (old, r[0]), [d(x) for x in r[1:9]] + [r[9]], want)
    chk('trNone の残り', html.count('trNone'), 0)
    # 4-0 計算の箱に直に書いた既定の結果(JS が動く前の HTML)。既定は東京23区・利益500万円・青色65万円・40歳未満
    e0 = ref(regions.REG[0], d(re.search(r'id="inc"[^>]*value="(\d+)"', html).group(1)), 650000, 0)
    def raw(i):
        return re.sub(r'<[^>]+>', '', re.search(r'id="%s">(.*?)</(?:b|em|li)>' % i, html).group(1))
    chk('既定の入力', re.search(r'id="inc"[^>]*value="(\d+)"', html).group(1), '5000000')
    chk('箱の既定 手取り', raw('o-n'), f(e0['net']) + '円')
    chk('箱の既定 手取り率', raw('o-nr'), '利益の%d%%' % half_up(Fraction(e0['net'] * 100, 5000000)))
    chk('箱の既定 税金', raw('o-t'), f(e0['tax']) + '円')
    chk('箱の既定 社会保険料', raw('o-s'), f(e0['sh']) + '円')
    chk('箱の既定 税金の内訳', raw('o-br'), '税金の内訳は、所得税%s円・住民税%s円・個人事業税%s円です' % (f(e0['it']), f(e0['ju']), f(e0['jg'])))
    chk('箱の既定 社会保険料の内訳', raw('o-sh'), '社会保険料は、国民健康保険%s円と国民年金%s円です' % (f(e0['k']), f(NEN)))
    chk('箱の既定 地域', raw('o-reg'), '国民健康保険は%sの令和8年度の料率で計算しています' % regions.REG[0]['s'])
    # 4-2 青色申告特別控除の表(手で書いた5行。65万円の手取りと、55万円・10万円・白色のときに減る額)
    ab = await pg.evaluate('()=>[].map.call(document.querySelectorAll(":is(#ao ~ .tw):not(#ao ~ .tw ~ .tw) tbody tr"),function(r){return [].map.call(r.cells,function(c){return c.textContent;});})')
    chk('青色の表の利益の並び', [d(r[0]) for r in ab], [300, 500, 700, 1000, 1500])
    for r in ab:
        a = d(r[0]) * 10000; n65 = ref(TK, a, 650000, 0)['net']
        want = [f(n65)] + ['−' + f(n65 - ref(TK, a, x, 0)['net']) for x in (550000, 100000, 0)]
        chk('青色の表 %s' % r[0], r[1:], want)
    # 4-3 黄色の行は、入力した利益を超えない中でいちばん近い行
    RW = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500]
    for a in (1990000, 2000000, 5990000, 6000000, 14990000, 15000000, 50000000):
        hit = await pg.evaluate('''(a)=>{var inc=document.getElementById("inc");inc.value=a;inc.dispatchEvent(new Event("input"));
          var t=[].map.call(document.querySelectorAll("#tb tr.hit"),function(r){return r.cells[0].textContent;});return t;}''', a)
        w = [x for x in RW if x * 10000 <= a]
        chk('黄色の行 %d' % a, [d(x) for x in hit], w[-1:])
    await pg.evaluate(READ, [0, 650000, 0, [5000000]])
    pass   # 黄色の文は2026-11-25に消した
    has('均等割と森林環境税', '均等割と森林環境税が合わせて5,000円')
    # 5 本文の数字(東京23区・青色65万円・40歳未満)
    R5 = lambda ao, old=0, a=5000000: ref(TK, a, ao, old)
    a5 = R5(650000)
    has('冒頭', '手取りは年%s円（月あたり%s円・手取り率%s%%）' % (f(a5['net']), f(half_up(Fraction(a5['net'], 12))), '%.1f' % (half_up(Fraction(a5['net'] * 1000, 5000000)) / 10)))
    has('冒頭', '引かれる%s円のうち国民健康保険と国民年金が%s円で、所得税・住民税・個人事業税の合計%s円より%s' % (
        f(a5['tax'] + a5['sh']), f(a5['sh']), f(a5['tax']), '多くなります' if a5['sh'] > a5['tax'] else '少なくなります'))
    man = range(2000000, 20000001, 10000)
    kit = max(a for a in man if (lambda x: x['k'] > x['it'])(ref(TK, a, 650000, 0)))
    has('読み方1', '利益%s万円までは、所得税より国民健康保険のほうが多い' % f(kit // 10000))
    ts = min(a for a in man if (lambda x: x['tax'] > x['sh'])(ref(TK, a, 650000, 0)))
    chk('税金が社会保険料を上回ったあとに戻らない', all((lambda x: x['tax'] > x['sh'])(ref(TK, a, 650000, 0)) for a in man if a >= ts), True)
    has('読み方1', '上回るのは、利益%s万円からです' % f(ts // 10000))
    x554, x555, x720, x721 = [ref(TK, a, 650000, 0) for a in (5540000, 5550000, 7200000, 7210000)]
    has('読み方2', '所得税が年%s円増えて手取りは年%s円減ります' % (f(x555['it'] - x554['it']), f(x554['net'] - x555['net'])))
    has('読み方2', '利益720万円から721万円では、手取りが年%s円減ります' % f(x720['net'] - x721['net']))
    cap = min(a for a in man if ref(TK, a, 650000, 0)['k'] >= 960000)
    capo = min(a for a in man if ref(TK, a, 650000, 1)['k'] >= 1130000)
    has('読み方3', '国民健康保険は利益%s万円で上限に届く' % f(cap // 10000))
    chk('40〜59歳も同じ利益で上限', capo, cap)
    has('問い', '利益%s万円あたりで上限に届きます' % f(cap // 10000))
    chk('上限の合計', (sum(CAPS) - CAPS[2], sum(CAPS)), (960000, 1130000))
    has('読み方3', '単身で年96万円（40〜59歳は介護分を含めて年113万円）が上限です')
    has('読み方4', '利益500万円で年%s円です' % f(a5['jg']))
    ds = [ref(TK, a, 650000, 0)['net'] - ref(TK, a, 100000, 0)['net'] for a in range(2000000, 20000001, 500000)]
    has('読み方5', '手取りが年%d万〜%d万円違う' % (half_up(Fraction(min(ds), 10000)), half_up(Fraction(max(ds), 10000))))
    b5, w5 = R5(100000), R5(0)
    has('読み方5', '65万円控除の手取りは年%s円です。10万円控除では年%s円・白色申告では年%s円です' % (f(a5['net']), f(b5['net']), f(w5['net'])))
    has('読み方5', '65万円控除と10万円控除の差は年%s円です' % f(R5(650000, 0, 8000000)['net'] - R5(100000, 0, 8000000)['net']))
    has('青色', '合わせて年およそ%d万円少なくなります' % half_up(Fraction(a5['net'] - w5['net'], 10000)))
    has('問い', '年%s円（月あたり%s円）です。所得税%s円・住民税%s円・個人事業税%s円・国民健康保険%s円・国民年金215,040円が引かれます' % (
        f(a5['net']), f(half_up(Fraction(a5['net'], 12))), f(a5['it']), f(a5['ju']), f(a5['jg']), f(a5['k'])))
    has('問い', '合計は年およそ%d万円です。社会保険料は年およそ%d万円です' % (half_up(Fraction(a5['tax'], 10000)), half_up(Fraction(a5['sh'], 10000))))
    has('前提', '国民年金は月17,920円（年%s円）' % f(NEN))
    return n, bad

run('kojin-zei', body)
