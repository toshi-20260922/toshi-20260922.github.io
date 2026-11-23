# /tsukin-teate/ 通勤手当の非課税限度額(電車・バス/車・自転車/両方。駐車場代と有料道路を足す)。
# 原本:
#  国税庁 No.2585 マイカー・自転車通勤者の通勤手当(令和8年4月1日現在法令等・12段・駐車場は月5,000円まで・
#   有料道路は合理的な料金を足して月15万円まで・片道2km未満は全額課税で駐車場も有料道路も対象外)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2585.htm
#  国税庁 No.2582 電車・バス通勤者の通勤手当(最も経済的かつ合理的な経路の定期代・月15万円・グリーン料金は含まない・
#   交通機関と交通用具の併用は合計で月15万円まで)  https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2582.htm
#  国税庁「通勤手当の非課税限度額の改正について」(令和8年度税制改正・令和8年4月1日以後に支払われるべき通勤手当・
#   片道65km以上の4段・駐車場等料金相当額 月5,000円まで・同日前の分の差額の追加支給は除く)
#   https://www.nta.go.jp/users/gensen/2026tsukin/index.htm  Q&A https://www.nta.go.jp/users/gensen/2026tsukin/pdf/01.pdf
#  国税庁「通勤手当の非課税限度額の改正について」(令和7年。令和7年11月20日施行・令和7年4月1日以後に支払われるべき分・
#   政令の公布は令和7年11月19日。10km以上の6段を引き上げ。2km以上10km未満の4,200円は変わらない。
#   改正前 7,100・12,900・18,700・24,400・28,000・31,600円(55km以上は一律))
#   https://www.nta.go.jp/users/gensen/2025tsukin/index.htm
#  財務省 令和8年度 政令改正要綱(所得税法施行令第20条の2。駐車場等の料金を負担することを常例とする者)
#   https://www.mof.go.jp/tax_policy/tax_reform/outline/fy2026/seirei/youkou/93_shotoku.pdf
#  日本年金機構 厚生年金保険の研修資料(報酬等の例に通勤手当)
#   https://www.nenkin.go.jp/service/riyoushabetsu/nenkiniin/kenshu/1.files/kounen2026_03.pdf
#  大阪労働局 労働保険の賃金(算入するもの:通勤手当・非課税部分も含む)
#   https://jsite.mhlw.go.jp/osaka-roudoukyoku/hourei_seido_tetsuzuki/roudou_hoken/hourei_seido/kosin/keizoku/kakunin.html
#  国税庁 令和7年11月の改正のページの文「改正前に、改正前の非課税限度額を超えた通勤手当を支払っていた場合には、
#   令和7年分の年末調整で対応が必要となることがあります」・Q&A https://www.nta.go.jp/users/gensen/2025tsukin/pdf/03.pdf
#   (公布 令和7年11月19日・施行 11月20日・退職者には支払金額を直した源泉徴収票を再交付)
#  国税庁 質疑応答事例「通勤手当、住居手当」(消費税。通勤に通常必要な範囲は所得税の限度額を超えても全額が課税仕入れ・
#   消費税法第2条第1項第12号・基本通達11-6-5)  https://www.nta.go.jp/law/shitsugi/shohi/16/04.htm
#  日本年金機構 年金Q&A「標準報酬月額の対象となる報酬に、通勤手当は含まれるのですか。」(通勤手当は報酬に含まれます)
#   https://www.nenkin.go.jp/section/faq/kounen/hyoujunhoushu/20140602-03.html
#  厚生労働省「最低賃金の対象となる賃金」(精皆勤手当、通勤手当及び家族手当は除く)
#   https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/chingin/newpage_43898.html
#   (newpage_43875 は「最低賃金制度の概要」で題名が違う。2026-11-20 に出典のリンクを直した)
# 片道の距離は「以上・未満」でそのまま比べる(端数を丸める定めは原本に無い)。金額は全部整数の円。
# 照らすもの:画面の箱(限度額・課税・1年分・判定の文・内訳の文)・距離の表・月2万円の表・本文と よく聞かれること の数字・元の文
# 最後に原本を確かめた日:2026-11-21(No.2585 の表の全12行・駐車場の上限5,000円・最高限度150,000円と No.2582 の15万円を本文で読んだ。どちらも令和8年4月1日現在法令等。2026tsukin・2025tsukin・消費税の質疑応答は11-20のまま)
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from _lib import run, SITE

DAN = [(0, None), (2, 4200), (10, 7300), (15, 13500), (25, 19700), (35, 25900), (45, 32300),
       (55, 38700), (65, 45700), (75, 52700), (85, 59600), (95, 66400)]
# 令和7年3月31日までに支払われるべき分の限度額(国税庁 2025tsukin の表の「改正前」。距離の下の境目, 円)
OLD2025 = [(0, None), (2, 4200), (10, 7100), (15, 12900), (25, 18700), (35, 24400), (45, 28000), (55, 31600)]
def old2025(lo):
    a = None
    for l, v in OLD2025:
        if lo >= l:
            a = v
    return a
JOGEN = 150000
CHUSHA = 5000

def gendo(km):          # km は Fraction。2km未満は None
    a = None
    for lo, v in DAN:
        if km >= lo:
            a = v
    return a

def ref(mode, pay, pas, km, park, toll):
    a = gendo(km)
    if a is None:
        car, pk = 0, 0
    else:
        pk = min(park, CHUSHA)
        car = a + pk + toll
    if mode == 0:
        lim = min(pas, JOGEN)
    elif mode == 1:
        lim = min(car, JOGEN)
    else:
        lim = min(pas + car, JOGEN)
    return lim, max(0, pay - lim), a, pk, car

def c(v):
    return '{:,}'.format(v)

def want_texts(mode, pay, pas, ks, park, toll):
    km = Fraction(ks)
    lim, t, a, pk, car = ref(mode, pay, pas, km, park, toll)
    if mode == 0:
        how = '定期代%s円%sまでが非課税です' % (c(pas), '（月15万円が上限）' if pas > JOGEN else '')
    elif mode == 1:
        if a is None:
            how = '片道2km未満なので全額が課税されます'
        else:
            how = '片道%skmの限度額%s円%s%sです' % (ks, c(a), ('＋駐車場代%s円' % c(pk)) if pk else '',
                                              ('＋有料道路%s円' % c(toll)) if toll else '')
    else:
        how = '定期代%s円＋車・自転車の分%s円%sです' % (c(pas), c(car), '（月15万円が上限）' if pas + car > JOGEN else '')
    if t > 0:
        vd, vds = '限度額を超えています', '毎月%s円が給与として課税されます。その月の給与に足して源泉徴収します' % c(t)
    else:
        vd, vds = '全額非課税です', '通勤手当%s円は限度額%s円以内なので所得税はかかりません' % (c(pay), c(lim))
    return [c(lim) + '円', c(t) + '円', ('1年で%s円' % c(t * 12)) if t > 0 else '1か月あたり', vd, vds, how]

READ = '''([m,pay,pas,km,park,toll])=>{
 document.querySelector('.seg button[data-k="'+m+'"]').click();
 const s=(i,v)=>{document.getElementById(i).value=String(v);};
 s('pay',pay);s('pas',pas);s('km',km);s('park',park);s('toll',toll);
 document.getElementById('pay').dispatchEvent(new Event('input'));
 return ['o-l','o-t','o-tn','o-vd','o-vds','o-how'].map(i=>document.getElementById(i).textContent);
}'''

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)

    # ---- 元の文と既定の値(電車・バス・手当20,000円・定期代18,000円) ----
    got = await pg.evaluate("()=>['o-l','o-t','o-tn','o-vd','o-vds','o-how'].map(i=>document.getElementById(i).textContent)")
    chk('既定の箱', got, want_texts(0, 20000, 18000, '12', 0, 0))

    # ---- 車・自転車:どの段も境目の0.1km下・ちょうど・0.1km上、限度の1円下・ちょうど・1円上 ----
    kms = ['0', '0.5', '1.9', '1.99', '2', '2.1', '5', '12', '120', '500']
    for lo, _ in DAN[2:]:
        kms += ['%d.9' % (lo - 1), str(lo), '%d.1' % lo]
    for ks in kms:
        a = gendo(Fraction(ks)) or 0
        for park in (0, 1, 4999, 5000, 5001, 20000):
            for toll in (0, 3000):
                lim = ref(1, 0, 0, Fraction(ks), park, toll)[0]
                for pay in sorted({0, 1, max(0, lim - 1), lim, lim + 1, 20000, 200000}):
                    got = await pg.evaluate(READ, [1, pay, 0, ks, park, toll])
                    chk('車 %skm 手当%d 駐車場%d 有料%d' % (ks, pay, park, toll), got, want_texts(1, pay, 0, ks, park, toll))
    # 有料道路で15万円の上限に届く所
    for ks, toll in (('30', 120000), ('30', 130300), ('30', 130301), ('95', 78600), ('95', 83600), ('1', 100000)):
        for pay in (149999, 150000, 150001, 300000):
            got = await pg.evaluate(READ, [1, pay, 0, ks, 5000, toll])
            chk('車 上限 %s %d %d' % (ks, toll, pay), got, want_texts(1, pay, 0, ks, 5000, toll))

    # ---- 電車・バス:定期代と15万円の境目 ----
    for pas in (0, 1, 18000, 149999, 150000, 150001, 400000):
        for pay in sorted({0, 1, max(0, pas - 1), pas, pas + 1, 149999, 150000, 150001, 1000000}):
            got = await pg.evaluate(READ, [0, pay, pas, '12', 0, 0])
            chk('電車 定期%d 手当%d' % (pas, pay), got, want_texts(0, pay, pas, '12', 0, 0))

    # ---- 両方:定期代+車の分で15万円 ----
    for pas, ks, park, toll in ((18000, '12', 0, 0), (18000, '1.9', 3000, 5000), (100000, '40', 5000, 0), (120000, '64.9', 0, 0),
                                (111300, '65', 0, 0), (111301, '55', 5000, 1000), (140000, '95', 6000, 2000), (0, '10', 0, 0)):
        lim = ref(2, 0, pas, Fraction(ks), park, toll)[0]
        for pay in sorted({0, max(0, lim - 1), lim, lim + 1, 200000}):
            got = await pg.evaluate(READ, [2, pay, pas, ks, park, toll])
            chk('両方 %d %s %d %d 手当%d' % (pas, ks, park, toll, pay), got, want_texts(2, pay, pas, ks, park, toll))

    # ---- 距離の表(全行) ----
    rows = await pg.evaluate("()=>[...document.querySelectorAll('#kyori ~ .tw')][0].querySelectorAll('tbody tr').length")
    cells = await pg.evaluate("()=>[...[...document.querySelectorAll('#kyori ~ .tw')][0].querySelectorAll('tbody tr')].map(r=>[...r.children].map(td=>td.textContent))")
    chk('距離の表の行の数', rows, len(DAN))
    for i, (lo, v) in enumerate(DAN):
        if i >= len(cells):
            break
        hi = DAN[i + 1][0] if i + 1 < len(DAN) else None
        name = '2km未満' if i == 0 else ('%dkm以上' % lo if hi is None else '%dkm以上%dkm未満' % (lo, hi))
        # 2026-11-20:4列目は2025年4月〜2026年3月の分の限度額(国税庁 2025tsukin。55km以上は一律38,700円・駐車場の加算なし)
        # 2026-11-20:5列目は2025年3月31日までに払うべき分(令和7年の改正の前の額。55km以上は一律31,600円)
        w = [name] + ['全額課税'] * 4 if v is None else [name, c(v), c(v + CHUSHA), c(min(v, 38700)), c(old2025(lo))]
        chk('距離の表 %d行目' % i, cells[i], w)

    # ---- 月2万円の表(車・駐車場代なし) ----
    cells = await pg.evaluate("()=>[...[...document.querySelectorAll('#rei ~ .tw')][0].querySelectorAll('tbody tr')].map(r=>[...r.children].map(td=>td.textContent))")
    kms2 = [5, 12, 20, 30, 40, 50, 60, 70]
    chk('月2万円の表の行の数', len(cells), len(kms2))
    for row, km in zip(cells, kms2):
        lim, t, _, _, _ = ref(1, 20000, 0, Fraction(km), 0, 0)
        chk('月2万円の表 %dkm' % km, row, ['%dkm' % km, c(lim), c(20000 - t), c(t), c(t * 12)])

    # ---- 本文・よく聞かれること・説明の文の数字 ----
    flat = ''.join((await pg.inner_text('main')).split())
    raw = open(os.path.join(SITE, 'tsukin-teate', 'index.html'), encoding='utf-8').read()
    # 月2万円が全額非課税になる最初の段
    first = next(lo for lo, v in DAN if v and v >= 20000)
    t12 = ref(1, 20000, 0, Fraction(12), 0, 0)[1]
    lo_a, hi_a = DAN[1][1], DAN[-1][1]
    for label, want in [
        ('結論', '電車・バスは月15万円まで、車・自転車は片道の距離で月%s円〜%s円まで非課税です' % (c(lo_a), c(hi_a))),
        ('冒頭 上限', '月15万円が上限です。'),
        ('冒頭 12km', '片道12kmなら月%s円までです。' % c(gendo(Fraction(12)))),
        ('冒頭 改正', '2026年4月1日以後に払うべき分から片道65km以上の区分が引き上げられ、駐車場代を月%s円まで足せるようになりました。' % c(CHUSHA)),
        ('表の列の題 新', '2026年4月からの限度額'),
        ('表の列の題 旧', '2026年3月までの分'),
        ('表の列の題 2025年3月まで', '2025年3月までの分'),
        ('表の説明', '通勤手当の1か月の限度額（右から2列目は2025年4月1日から2026年3月31日まで・一番右は2025年3月31日までに払うべき分）'),
        ('2025年の改正', '2025年11月19日に公布された政令で片道10km以上の区分が引き上げられ、2025年4月1日以後に払うべき分にさかのぼって使います。'),
        ('2025年の改正 一番右の列', '2025年3月31日までに払うべき分は早見表の一番右の列で判定します。'),
        ('よく聞かれること 2025年', '2025年4月1日以後に払うべき分は、2025年11月の改正後の限度額で判定します。それより前に払うべき分は改正前の限度額です。'),
        ('有料道路', '有料道路を使う人は、合理的な経路の料金を足して月15万円までです。'),
        ('電車 15万円', '月15万円を超えるときは15万円までです。'),
        ('グリーン料金', 'グリーン料金は含めません'),
        ('併用', '定期代と車の距離の限度額を足して月15万円までです'),
        ('月2万円 全額非課税', '片道%dkm以上なら月2万円は全額非課税です。' % first),
        ('月2万円 12km', '片道12kmでは毎月%s円・1年で%s円が給与として課税されます。' % (c(t12), c(t12 * 12))),
        ('改正 65km', '65km以上75km未満は%s円・95km以上は%s円に引き上げた' % (c(DAN[8][1]), c(DAN[11][1]))),
        ('改正 駐車場', '月%s円まで限度額に足せるようにした' % c(CHUSHA)),
        ('改正 令和8年度', '令和8年度の税制改正で'),
        ('改正 差額', '2026年3月31日までに払うべきだった分を、あとから差額として払うときは改正前の限度額で判定します。'),
        ('よく聞かれること 限度', '2km以上10km未満の月%s円から95km以上の月%s円までです。' % (c(lo_a), c(hi_a))),
        ('よく聞かれること 駐車場', '2026年4月1日以後に払うべき通勤手当からです。勤務先か駅などの近くの駐車場で、月%s円が上限です。' % c(CHUSHA)),
        ('よく聞かれること 社会保険', '標準報酬月額を決める報酬には全額を含めます。雇用保険料の計算でも賃金に入ります。'),
        ('社会保険', '健康保険・厚生年金の標準報酬月額を決めるときは、通勤手当も全額を報酬に入れます。'),
        ('更新日', '更新日：2026年11月21日（国税庁No.2582・No.2585令和8年4月1日現在法令等）'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('最低賃金の出典のリンク', 'chingin/newpage_43898.html">厚生労働省「最低賃金の対象となる賃金」' in raw, True)
    chk('最低賃金から除く3つの手当', '基本給と毎月払う手当から通勤手当・精皆勤手当・家族手当を除いた額で、最低賃金を満たしているかを確かめます。' in flat, True)
    chk('2025年分の年末調整', '改正前の限度額を超えて払っていた分は、2025年分の年末調整で直すことがあります。' in flat, True)
    chk('消費税', '通勤に通常必要な範囲なら全額が課税仕入れです。所得税の限度額を超えた分も含みます' in flat, True)
    chk('消費税の通達', '消費税法第2条第1項第12号・消費税法基本通達11-6-5' in flat, True)
    desc = '通勤手当の非課税限度額は、電車・バスの定期代なら月15万円まで、車・自転車なら片道の距離で月%s円〜%s円です。' % (c(lo_a), c(hi_a))
    chk('説明の文', len(re.findall(r'(?:name="description"|property="og:description") content="' + re.escape(desc), raw)), 2)
    chk('説明の文(description と og)が同じ', len(set(re.findall(r'(?:name="description"|property="og:description") content="([^"]*)"', raw))), 1)
    chk('元の文 既定の値', ('id="pay" inputmode="numeric" min="0" max="10000000" step="1" value="20000"' in raw,
                     'id="pas" inputmode="numeric" min="0" max="10000000" step="1" value="18000"' in raw), (True, True))
    html = re.sub(r'<script.*?</script>|<style.*?</style>', '', raw, flags=re.S)
    # 2026-11-21:計算の箱に直に書いた既定の結果(JS が動く前の HTML)も自分の計算と同じか(申し送りの形16・26)
    w = want_texts(0, 20000, 18000, '12', 0, 0)
    def inner(i):
        m = re.search(r'id="%s"[^>]*>(.*?)</(?:b|span|em|li)>' % i, html, flags=re.S)
        return re.sub(r'<[^>]+>', '', m.group(1)) if m else None
    chk('元の HTML の既定の結果', [inner(i) for i in ('o-l', 'o-t', 'o-tn', 'o-vd', 'o-vds', 'o-how')], w)
    chk('元の HTML の判定の箱の色', 'class="vd" id="vd"' in raw, w[3] == '限度額を超えています')
    chk('span の開きと閉じの数', html.count('<span'), html.count('</span>'))
    chk('2025年の改正で上がった段は10km以上の6つ', [lo for lo, v in OLD2025 if v and v != dict(DAN)[lo]], [10, 15, 25, 35, 45, 55])
    chk('列の数', len(cells) and 0 or len(await pg.evaluate("()=>[...document.querySelectorAll(':is(#kyori ~ .tw):not(#kyori ~ .tw ~ .tw) thead th')].map(x=>x.textContent)")), 5)
    chk('25km では月2万円は課税が残る', ref(1, 20000, 0, Fraction(25), 0, 0)[1], 300)
    return n, bad

run('tsukin-teate', body)
