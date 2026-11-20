# /genbutsu-kyuyo/ 非課税の限度額の早見表(現物給与。計算は通勤手当と食事の2つ・あとは表の全部の数字を原本の値と比べる)。
# 原本(どれも令和8年4月1日現在法令等):
#  国税庁「通勤手当の非課税限度額の改正について」(令和8年4月1日以後に支払われるべき通勤手当・片道65km以上の4つの段・駐車場は月5,000円まで)
#   https://www.nta.go.jp/users/gensen/2026tsukin/index.htm
#  国税庁「食事の現物支給に係る所得税の非課税限度額の引上げについて」(月3,500円→7,500円・夜食代 300円以下→650円以下・令和8年4月1日以後に支給する食事)
#   https://www.nta.go.jp/users/gensen/2026shokuji/index.htm
#  国税庁 No.2582 電車・バス通勤者の通勤手当(月15万円・グリーン料金は含まれない・両方使う人は足して月15万円まで)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2582.htm
#  国税庁 No.2585 マイカー・自転車通勤者の通勤手当(距離の12段・駐車場は月5,000円まで・片道2km未満は対象外)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2585.htm
#  国税庁 No.2594 食事を支給したとき(半分以上を負担・差額が月7,500円以下・消費税を除いた金額の10円未満の端数は切り捨てて判定・
#   夜食代は1食650円以下・例:13,000円と6,000円は7,000円が課税)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2594.htm
#  国税庁 No.2597 使用人に社宅や寮などを貸したとき(0.2%・12円÷3.3・0.22%・50%以上)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2597.htm
#  国税庁 No.2600 役員に社宅などを貸したとき(132平方メートル・99平方メートル・12%・10%・6%・12分の1・家賃の50%と多いほう)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2600.htm
#  国税庁 No.2591 創業記念品や永年勤続表彰記念品の支給をしたとき(1万円以下・おおむね5年以上・おおむね10年以上)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2591.htm
#  国税庁 No.2603 従業員レクリエーション旅行や研修旅行(4泊5日以内・50%以上)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2603.htm
#  国税庁 No.2606 金銭を貸し付けたとき(令和8年中の貸付けは年1.3%・差額が年5,000円以下)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2606.htm
#  国税庁 No.2601 職務に必要な技術などを習得する費用を支出したとき  https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2601.htm
#  国税庁 No.2508 給与所得となるもの  https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2508.htm
#  日本年金機構「厚生年金保険の保険料」(通勤手当と現物も報酬に含める)  https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20150515-01.html
#  国税庁「食事を支給したときの非課税限度額の判定」(消費税を除いた合計の10円未満の端数を切り捨てて月7,500円と比べる)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2594-1.htm
#  国税庁「通勤手当の非課税限度額の改正について」(令和7年4月1日以後の分。55km以上は31,600円→38,700円。令和8年3月までの列のもと)
#   https://www.nta.go.jp/users/gensen/2025tsukin/index.htm
#  国税庁 質疑応答事例「アルバイトに支給する通勤手当の非課税限度額」(日割額ではなく月額で判定)  https://www.nta.go.jp/law/shitsugi/gensen/03/21.htm
#  国税庁 質疑応答事例「通勤手当、住居手当」(通勤に通常必要な範囲は全額が課税仕入れ)  https://www.nta.go.jp/law/shitsugi/shohi/16/04.htm
#  日本年金機構「全国現物給与価額一覧表」(令和8年4月から。食事は都道府県ごとに違う額・住宅は令和8年10月から1平方メートル当たり。
#   このページは都道府県ごとの額を載せていない。1つの県の額を地域名なしで載せていないことを下で見る)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20150511.html
# 2026-11-20 に確かめたこと:食事の月額は令和8年4月1日以後に支給する食事から3,500円→7,500円・夜食代は300円→650円。
#  通勤手当は令和7年4月(10km以上の引上げ)と令和8年4月(65km以上の4段と駐車場5,000円)の2回改正。どれもページと同じ。
# 照らすもの:window.__tsukin と __shokuji・結果の箱・黄色の行・HTML に手で書いた表の全行・本文の数字・JS が書き換える前の元の文
# 2026-11-21 に確かめたこと:上の国税庁のページ(2026tsukin・2026shokuji・No.2582・2585・2594・2597・2600・2591・2603・2606・2601・2508)は
#  どれも令和8年4月1日現在法令等のままで数字は同じ。源泉徴収票の「支払金額」は非課税の通勤手当を除いた額(2025tsukin の Q&A の Q15)。
#  従業員から受け取る食事代は課税の売上げ(No.6471)・社宅の使用料は非課税(質疑応答事例「社宅に係る仕入税額控除」)。
#  計算の箱に直に書いた既定の結果(非課税の限度 0円・「非課税の限度」・「判定」)を既定の入力の結果に直し、下で元の HTML と比べる形にした。
# 最後に原本を確かめた日: 2026-11-21
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from _lib import run, SITE

# No.2585 の表(片道の距離の下の端・令和8年4月からの額・令和8年3月までの額)。None は全額課税。
DAN = [(0, None, None), (2, 4200, 4200), (10, 7300, 7300), (15, 13500, 13500), (25, 19700, 19700), (35, 25900, 25900),
       (45, 32300, 32300), (55, 38700, 38700), (65, 45700, 38700), (75, 52700, 38700), (85, 59600, 38700), (95, 66400, 38700)]
JOGEN = 150000      # No.2582 月15万円
CHUSHA = 5000       # 駐車場は月5,000円まで
SHOKU = 7500        # No.2594 月7,500円
def dan(km):        # km は Fraction
    k = 0
    for i, (lo, _, _) in enumerate(DAN):
        if km >= lo:
            k = i
    return k
def ref_tsukin(mode, km, pay, park):
    if mode == 0:
        lim = JOGEN
    else:
        a = DAN[dan(km)][1]
        lim = 0 if a is None else a + min(park, CHUSHA)
    hi = min(pay, lim)
    return [lim, hi, pay - hi]
def ref_shokuji(price, futan):
    co = max(0, price - futan)
    ok = futan * 2 >= price and co // 10 * 10 <= SHOKU      # 10円未満の端数は切り捨てて判定
    return 0 if ok else co
def c(v):
    return '{:,}'.format(v)

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)
    def d(t):
        return int(''.join(ch for ch in t if ch.isdigit()) or 0)

    # ---- 通勤手当の関数(境目のちょうど・0.1km下・0.1km上と、低い・中くらい・高い手当) ----
    kms = ['0', '0.5', '1.9', '2', '2.1', '5', '300', '500']
    for lo, _, _ in DAN[2:]:
        kms += ['%d.9' % (lo - 1), str(lo), '%d.1' % lo]
    for ks in kms:
        kf = Fraction(ks)
        lim0 = DAN[dan(kf)][1] or 0
        pays = sorted({0, 1, 3000, 15000, 80000, 149999, 150000, 150001, 1000000, max(0, lim0 - 1), lim0, lim0 + 1,
                       lim0 + 4999, lim0 + 5000, lim0 + 5001})
        for park in (0, 1, 3000, 4999, 5000, 5001, 20000):
            for pay in pays:
                got = await pg.evaluate('([k,p,q])=>window.__tsukin(1,k,p,q)', [float(ks), pay, park])
                chk('マイカー %skm 手当%d 駐車場%d' % (ks, pay, park), got, ref_tsukin(1, kf, pay, park))
    for pay in (0, 1, 15000, 149999, 150000, 150001, 300000, 1000000):
        got = await pg.evaluate('p=>window.__tsukin(0,12,p,0)', pay)
        chk('電車・バス 手当%d' % pay, got, ref_tsukin(0, Fraction(12), pay, 0))

    # ---- 食事の関数(半分の境目・7,500円の境目・10円未満の端数) ----
    cases = [(0, 0), (13000, 6000), (13000, 6499), (13000, 6500), (13000, 6501), (15000, 7500), (15000, 7499), (15001, 7501),
             (15002, 7501), (15010, 7501), (15018, 7509), (15019, 7509), (15020, 7510), (15020, 7509), (16000, 8500), (16000, 8491),
             (16000, 8490), (16000, 8489), (20000, 12500), (20000, 12499), (20000, 12490), (20000, 12489), (3000, 1500), (3000, 1499),
             (7000, 3500), (7000, 0), (5000, 9000), (100000, 50000), (100000, 92500), (100000, 92491), (1000000, 992500), (1, 0), (1, 1), (2, 1)]
    for price, futan in cases:
        chk('食事 %d %d' % (price, futan), await pg.evaluate('([a,b])=>window.__shokuji(a,b)', [price, futan]), ref_shokuji(price, futan))
    chk('No.2594 の例', ref_shokuji(13000, 6000), 7000)

    # ---- 画面の箱(入力欄に値を入れて読む) ----
    chk('既定の箱 電車・バス', [d(await pg.inner_text('#o-lim')), d(await pg.inner_text('#o-t')), await pg.inner_text('#o-tj')],
        [JOGEN, 0, '通勤手当は全額非課税です'])
    chk('既定の箱 食事', [d(await pg.inner_text('#o-s')), await pg.inner_text('#o-sj'), await pg.inner_text('#o-m')],
        [0, '食事の補助は非課税です', '会社の負担は6,500円。2つの条件を満たしています'])
    for pay in (15000, 150000, 150001, 200000):
        await pg.fill('#pay', str(pay)); r = ref_tsukin(0, Fraction(0), pay, 0)
        chk('箱 電車 %d' % pay, [d(await pg.inner_text('#o-lim')), d(await pg.inner_text('#o-t')), await pg.inner_text('#o-tj'), await pg.inner_text('#o-l')],
            [r[0], r[2], ('通勤手当のうち月%s円は課税されます' % c(r[2])) if r[2] else '通勤手当は全額非課税です', '電車・バスは合理的な経路の運賃で月150,000円まで非課税です'])
        chk('電車は黄色の行なし %d' % pay, await pg.eval_on_selector_all('#tb tr.hit', 'rs=>rs.length'), 0)
    await pg.click('#s-mode button[data-v="1"]')
    for ks, pay, park in [('12', 15000, 0), ('1.9', 5000, 3000), ('2', 4200, 0), ('2', 4201, 0), ('9.9', 10000, 5000), ('10', 7300, 6000),
                          ('14.9', 12301, 5000), ('64.9', 50000, 0), ('65', 50000, 0), ('74.9', 45701, 0), ('75', 60000, 4000), ('85', 59600, 0),
                          ('94.9', 70000, 5000), ('95', 71400, 9999), ('95', 71401, 9999), ('120', 100000, 0)]:
        kf = Fraction(ks)
        await pg.fill('#km', ks); await pg.fill('#pay', str(pay)); await pg.fill('#park', str(park))
        r = ref_tsukin(1, kf, pay, park)
        if kf < 2:
            l = '片道2km未満のマイカー・自転車通勤は全額課税です'
        else:
            l = '片道%skmの非課税の限度は月%s円です' % (ks, c(r[0])) + ('（駐車場を含む）' if park > 0 else '')
        chk('箱 マイカー %s %d %d' % (ks, pay, park),
            [d(await pg.inner_text('#o-lim')), d(await pg.inner_text('#o-t')), await pg.inner_text('#o-tj'), await pg.inner_text('#o-l')],
            [r[0], r[2], ('通勤手当のうち月%s円は課税されます' % c(r[2])) if r[2] else '通勤手当は全額非課税です', l])
        chk('黄色の行 %s' % ks, await pg.eval_on_selector_all('#tb tr.hit', "rs=>rs.map(r=>r.getAttribute('data-k'))"), [str(dan(kf))])
    for price, futan in [(13000, 6500), (13000, 6000), (15000, 7500), (15018, 7509), (15020, 7510), (16000, 8490), (16000, 8489), (20000, 12000), (0, 0)]:
        await pg.fill('#price', str(price)); await pg.fill('#futan', str(futan))
        s = ref_shokuji(price, futan); co = max(0, price - futan)
        if s == 0:
            want = [0, '食事の補助は非課税です', '会社の負担は%s円。2つの条件を満たしています' % c(co)]
        else:
            want = [s, '食事の補助は月%s円が課税されます' % c(s), '本人の負担が半分に届いていません' if futan * 2 < price else '会社の負担が月7,500円を超えています']
        chk('箱 食事 %d %d' % (price, futan), [d(await pg.inner_text('#o-s')), await pg.inner_text('#o-sj'), await pg.inner_text('#o-m')], want)

    # ---- HTML に手で書いた表(距離の表の全行) ----
    rows = await pg.eval_on_selector_all('#tb tr', "rs=>rs.map(r=>[r.getAttribute('data-k')].concat([...r.children].map(td=>td.textContent)))")
    chk('距離の表の行の数', len(rows), len(DAN))
    for i, (lo, new, old) in enumerate(DAN):
        if i >= len(rows):
            break
        hi = DAN[i + 1][0] if i + 1 < len(DAN) else None
        name = '2km未満' if i == 0 else ('%dkm以上' % lo if hi is None else '%dkm以上%dkm未満' % (lo, hi))
        if new is None:
            wn = wo = '全額課税'
        else:
            wn = c(new) + '円' + ('%s円上がった' % c(new - old) if new != old else ''); wo = c(old) + '円'
        chk('距離の表 %d行目' % i, rows[i], [str(i), name, wn, wo])

    # ---- 本文と表の数字(原本の値から作った文が画面にあるか) ----
    flat = ''.join((await pg.inner_text('main')).split())
    lo_a, hi_a = DAN[1][1], DAN[-1][1]
    for label, want in [
        ('一覧 電車・バス', '最も経済的で合理的な経路の定期券などの額。月15万円まで'),
        ('一覧 マイカー', '片道の距離に応じて月%s円から%s円。片道2km未満は全額課税' % (c(lo_a), c(hi_a))),
        ('一覧 駐車場', '片道2km以上の人は、駐車場の料金を月%s円まで上乗せ' % c(CHUSHA)),
        ('一覧 食事', '本人が半分以上を負担し、会社の負担が月%s円以下（消費税を除く）' % c(SHOKU)),
        ('一覧 夜食', '夜食を出せないときに現金で渡す場合、1食650円以下（消費税を除く）'),
        ('一覧 従業員の社宅', '本人から、賃貸料相当額の50%以上の家賃を受け取る'),
        ('一覧 役員の社宅', '役員の社宅本人から、賃貸料相当額の家賃を受け取る'),
        ('一覧 記念品', '処分見込価額が1万円以下（消費税を除く）など'),
        ('一覧 旅行', '4泊5日以内、参加が全体の50%以上など'),
        ('一覧 貸付金', '決まった利率で計算した利息との差額が、年5,000円以下など'),
        ('冒頭の改正', '令和8年4月から食事の限度が月3,500円から7,500円に上がり、マイカー通勤の限度も変わりました。'),
        ('通勤 上限', '上限は月15万円です。'),
        ('通勤 グリーン料金', 'グリーン料金は含まれません。'),
        ('通勤 表の注', '令和8年4月1日以後に支払われるべき通勤手当から、片道65km以上の限度額が上がりました。'),
        ('通勤 駐車場', '令和8年4月からは通勤に使う駐車場の料金も、月5,000円まで限度額に足せます。対象は片道2km以上の人で、勤務先や通勤に使う駅などの周辺にある駐車場です。'),
        ('通勤 両方', '合計の上限は月15万円です。'),
        ('食事 条件1', '本人が、食事の価額の半分以上を負担している'),
        ('食事 条件2', '食事の価額から本人の負担を引いた額が、月7,500円以下（消費税を除く）'),
        ('食事 例', '月13,000円の食事で本人の負担が6,000円なら半分に届かないので、差額の%s円が課税されます。' % c(ref_shokuji(13000, 6000))),
        ('食事 改正', '限度額は令和8年4月1日以後に支給する食事から、月3,500円が7,500円に上がりました。深夜勤務の夜食代も、1食300円以下が650円以下に上がっています。'),
        ('社宅 小規模の式', '建物の固定資産税の課税標準額×0.2%12円×建物の総床面積（平方メートル）÷3.3敷地の固定資産税の課税標準額×0.22%'),
        ('社宅 小規模でない式', '次の2つの合計の12分の1建物の固定資産税の課税標準額×12%（法定耐用年数が30年を超える建物は10%）敷地の固定資産税の課税標準額×6%'),
        ('社宅 借りている', '会社が払う家賃の50%と上の行の額の、多いほう'),
        ('社宅 小規模の広さ', '法定耐用年数が30年以下の建物なら床面積132平方メートル以下です。30年を超える建物なら99平方メートル以下です。'),
        ('社宅 50%', '従業員は賃貸料相当額の50%以上を受け取っていれば、差額は課税されません。'),
        ('記念品', '処分見込価額が1万円以下（消費税を除く）。定期的に配るものは、おおむね5年以上の間隔'),
        ('永年勤続', '勤続おおむね10年以上の人が対象。2回目からは、前の表彰からおおむね5年以上の間隔。'),
        ('旅行', '旅行の期間が4泊5日以内。参加が全体の50%以上。'),
        ('貸付金', '令和8年中の貸付けは年1.3%で計算した利息との差額が課税。差額が年5,000円以下なら課税されません'),
        ('よく聞かれること 通勤', '電車やバスは月15万円までです。'),
        ('よく聞かれること 夜食', '1食650円以下を渡す場合は別です。'),
        ('箱の注', '令和8年4月1日以後に支払う通勤手当と、同じ日以後に支給する食事の限度額で計算しています'),
    ]:
        chk('本文 ' + label, want in flat, True)
    # ---- HTML に手で書いた表の全行(一覧・食事の条件・記念品など・消費税。原本の値から作った文と1行ずつ比べる) ----
    async def tbl(hid):
        return await pg.eval_on_selector_all(':is(#%s ~ .tw):not(#%s ~ .tw ~ .tw) tbody tr' % (hid, hid),
                                             "rs=>rs.map(r=>[...r.children].map(td=>td.textContent.replace(/\\s+/g,'')))")
    NIGHT_NEW, NIGHT_OLD, SHOKU_OLD = 650, 300, 3500      # 2026shokuji の改正前と改正後
    KINEN, KASHI_SA, KASHI_RITSU = 10000, 5000, '1.3'     # No.2591・No.2606
    want_m = [
        ['通勤手当電車・バス', '最も経済的で合理的な経路の定期券などの額。月%d万円まで' % (JOGEN // 10000), '限度を超えた部分が給与', '―'],
        ['通勤手当マイカー・自転車', '片道の距離に応じて月%s円から%s円。片道2km未満は全額課税' % (c(lo_a), c(hi_a)), '限度を超えた部分が給与', '令和8年4月から片道65km以上の限度が上がった'],
        ['通勤用の駐車場', '片道2km以上の人は、駐車場の料金を月%s円まで上乗せ' % c(CHUSHA), '上乗せは月%s円まで' % c(CHUSHA), '令和8年4月から上乗せができた'],
        ['食事', '本人が半分以上を負担し、会社の負担が月%s円以下（消費税を除く）' % c(SHOKU), '会社の負担の全額が給与', '令和8年4月から月%s円が%s円に上がった' % (c(SHOKU_OLD), c(SHOKU))],
        ['深夜勤務の夜食代', '夜食を出せないときに現金で渡す場合、1食%d円以下（消費税を除く）' % NIGHT_NEW, '渡した額の全額が給与', '令和8年4月から1食%d円が%d円に上がった' % (NIGHT_OLD, NIGHT_NEW)],
        ['従業員の社宅・寮', '本人から、賃貸料相当額の50%以上の家賃を受け取る', '賃貸料相当額と受け取った家賃の差額が給与', '―'],
        ['役員の社宅', '本人から、賃貸料相当額の家賃を受け取る', '賃貸料相当額と受け取った家賃の差額が給与', '―'],
        ['創業記念などの品', '処分見込価額が%d万円以下（消費税を除く）など' % (KINEN // 10000), '品物の価額が給与', '―'],
        ['従業員の旅行', '4泊5日以内、参加が全体の50%以上など', '会社の負担が給与', '―'],
        ['貸付金の利息', '決まった利率で計算した利息との差額が、年%s円以下など' % c(KASHI_SA), '決まった利率の利息との差額が給与', '―'],
    ]
    want_s = [['1', '本人が、食事の価額の半分以上を負担している'], ['2', '食事の価額から本人の負担を引いた額が、月%s円以下（消費税を除く）' % c(SHOKU)]]
    want_o = [
        ['創業記念などの品', '記念品としてふさわしい物で、処分見込価額が%d万円以下（消費税を除く）。定期的に配るものは、おおむね5年以上の間隔' % (KINEN // 10000)],
        ['永年勤続の記念品・旅行', '勤続おおむね10年以上の人が対象。2回目からは、前の表彰からおおむね5年以上の間隔。金額が社会一般からみて相当'],
        ['従業員の旅行', '旅行の期間が4泊5日以内。参加が全体の50%以上。内容をまとめて見て判定されます'],
        ['仕事に必要な研修・資格', '職務に直接必要な技術や知識を習得させる費用で、適正なもの'],
        ['貸付金の利息', '令和8年中の貸付けは年%s%%で計算した利息との差額が課税。差額が年%s円以下なら課税されません' % (KASHI_RITSU, c(KASHI_SA))],
    ]
    want_z = [['通勤手当', '通勤に通常必要な額は、会社の課税仕入れになる'], ['社宅の家賃', '従業員や役員から受け取る家賃は、住宅の貸付けなので非課税の売上げになる'],
              ['食事代', '従業員や役員から受け取る食事代は、課税の売上げになる']]
    for hid, want in (('matome', want_m), ('shokuji', want_s), ('other', want_o)):
        got = await tbl(hid)
        chk('表 %s の行の数' % hid, len(got), len(want))
        for i, w in enumerate(want):
            chk('表 %s %d行目' % (hid, i + 1), got[i] if i < len(got) else None, w)
    got = await pg.eval_on_selector_all('#shaho ~ h3 + p + .tw tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent.replace(/\\s+/g,'')))")
    chk('表 消費税の行の数', len(got), len(want_z))
    for i, w in enumerate(want_z):
        chk('表 消費税 %d行目' % (i + 1), got[i] if i < len(got) else None, w)
    # 社宅:会社が借りた部屋で「同じ式」になるのは従業員と役員の小規模な住宅だけ(No.2597・No.2600)
    chk('本文 社宅 借りた部屋', '従業員や役員（小規模な住宅）に会社が借りた部屋を貸す場合も、同じ式で計算します。' in flat, True)
    chk('本文 社宅 借りた部屋(古い文が残っていない)', '。会社が借りた部屋を貸す場合も' in flat, False)
    # 現物給与の価額(日本年金機構)は都道府県ごとに違う。県名なしの1地域の額(食事の月額・住宅の1畳や1平方メートル当たり)を載せていないこと
    chk('現物給与の価額を1地域で固定していない', bool(re.search(r'1畳|畳1畳|1平方メートル(当|あ)たり|1人1[かヶケ]?月(当|あ)たり', flat)), False)
    chk('パートの通勤手当は月を単位', '短い期間だけ雇う人も、月を単位にして限度額を計算します。' in flat, True)
    chk('更新日', '更新日：2026年11月21日' in flat, True)
    for i, (lo, new, old) in enumerate(DAN[8:], 8):      # 上がった額の小さい字
        chk('上がった額 %d行目' % i, new - old, [7000, 14000, 20900, 27700][i - 8])

    # ---- JS が書き換える前の元の文・既定の値・余った閉じタグ ----
    raw = open(os.path.join(SITE, 'genbutsu-kyuyo', 'index.html'), encoding='utf-8').read()
    chk('元の文 既定の値', ('id="pay" inputmode="numeric" min="0" max="1000000" step="100" value="15000"' in raw,
                     'step="0.1" value="12"' in raw, 'id="price" inputmode="numeric" min="0" max="1000000" step="100" value="13000"' in raw,
                     'id="futan" inputmode="numeric" min="0" max="1000000" step="100" value="6500"' in raw), (True, True, True, True))
    chk('元の文 箱', ('<b id="o-tj">通勤手当は全額非課税です</b>' in raw, '<b id="o-sj">食事の補助は非課税です</b>' in raw), (True, True))
    # 計算の箱に直に書いた既定の結果(JS が動く前の HTML)を、既定の入力(電車・バス 15,000円/食事 13,000円・本人 6,500円)の自分の計算と比べる
    r0 = ref_tsukin(0, Fraction(12), 15000, 0)
    def raw_of(i):
        m = re.search(r'id="%s">(.*?)</(?:b|span)>' % i, raw, flags=re.S)
        return re.sub(r'<[^>]+>', '', m.group(1)) if m else None
    chk('元の文 非課税の限度', raw_of('o-lim'), c(r0[0]) + '円')
    chk('元の文 課税される額', raw_of('o-t'), c(r0[2]) + '円')
    chk('元の文 通勤の説明', raw_of('o-l'), '電車・バスは合理的な経路の運賃で月%s円まで非課税です' % c(JOGEN))
    chk('元の文 食事の課税される額', raw_of('o-s'), c(ref_shokuji(13000, 6500)) + '円')
    chk('元の文 食事の説明', raw_of('o-m'), '会社の負担は%s円。2つの条件を満たしています' % c(13000 - 6500))
    chk('元の文 既定の食事は非課税', ref_shokuji(13000, 6500), 0)
    chk('元の文 既定の通勤手当は非課税', ref_tsukin(0, Fraction(12), 15000, 0)[2], 0)
    html = re.sub(r'<script.*?</script>|<style.*?</style>', '', raw, flags=re.S)
    chk('span の開きと閉じの数', html.count('<span'), html.count('</span>'))
    chk('説明の文(description と og)が同じ', len(set(re.findall(r'(?:name="description"|property="og:description") content="([^"]*)"', raw))), 1)
    return n, bad
run('genbutsu-kyuyo', body)
