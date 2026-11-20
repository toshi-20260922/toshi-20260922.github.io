# /niwari-tokurei/ 消費税の計算(2割特例のあとの簡易課税・本則課税・3割特例の比較と届出の期限)。
# 原本:
#  国税庁「インボイス制度 令和8年度税制改正特集」(2割特例は令和8年9月30日の属する課税期間まで・3割特例は個人事業者の令和9年分と令和10年分・
#   免税事業者等からの仕入れは令和8年10月1日から2年間70%・簡易課税の届出は適用を受ける課税期間の申告期限まで。延長法人は延長後の期限)
#   https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/index.htm
#  国税庁「3割特例の創設」(課税標準額に対する消費税額からその7割を控除・確定申告書に付記)
#   https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice-review/pdf/0026002-095.pdf
#  国税庁 インボイスQ&A 問115-2(3割特例を使えない課税期間)・問117・問117-3(届出の期限。土日祝日と12月29日から31日は翌日)
#   https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/pdf/qa/117-3.pdf
#  国税庁 No.6505「簡易課税制度」・No.6509「簡易課税制度の事業区分」(みなし仕入率90・80・70・60・50・40%。基準期間の課税売上高5,000万円以下)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6505.htm  https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6509.htm
#  国税庁「消費税及び地方消費税の申告書(一般用)の書き方」(課税標準額は1,000円未満切り捨て・計算の途中の1円未満はその都度切り捨て・
#   差引税額は100円未満切り捨て・譲渡割額は×22/78で100円未満切り捨て)
#   https://www.nta.go.jp/publication/pamph/shohi/kaisei/yoshiki/pdf/202411_01.pdf
#  国税庁「2割特例 特設ページ」(令和5年10月1日から令和8年9月30日までの日の属する課税期間。3月決算法人は令和9年3月期まで)
#   https://www.nta.go.jp/taxes/shiraberu/zeimokubetsu/shohi/keigenzeiritsu/invoice_2tokurei.htm
#  2026-11-20:特集の頁からの3割特例のリーフレットは 0026004-099-01-1.pdf。0026002-095.pdf はこの日開けなかった。
#  2026-11-21:0026002-095.pdf は開けた。題名は「インボイス制度に関する令和8年度税制改正について」(「3割特例の創設」は中の見出し)。
#   届出の期限の例:個人は令和11年分の申告期限(令和12年4月1日)・12月決算法人は令和9年12月期の申告期限(令和10年2月29日)。
#   この特例は前の期に2割特例か3割特例を使った事業者だけ(No.6505・2割特例の概要)。
#  国税庁「2割特例(インボイス発行事業者となる小規模事業者に対する負担軽減措置)の概要」(事前の届出は不要・確定申告書に付記・特別控除税額は80%)
#   https://www.nta.go.jp/publication/pamph/shohi/kaisei/202304/01.htm
#  国税庁 No.6303「消費税および地方消費税の税率」(7.8%と2.2%。地方消費税は消費税額の78分の22)
#  2026-11-20:飲食料品の税率を令和9年4月1日から2年間1%にする案(国税庁 令和8年9月の案内は法案の成立が前提)。成立は未確認。ページは10%だけで計算。
#  2026-11-21:第222回国会 閣法第1号。令和8年11月6日に衆議院で可決・11月11日に参議院で委員会付託・参議院の議決と公布は空欄(参議院の議案情報)。まだ成立していない。
# 最後に原本を確かめた日:2026-11-21
import os, sys, re, datetime, calendar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

def h100(x):
    return x // 100 * 100
def tot(k):
    """国税の納付額(100円未満切り捨て)に地方消費税(国税×22/78・100円未満切り捨て)を足す。"""
    kk = h100(max(k, 0))
    return kk + h100(kk * 22 // 78)
def ref(uri, shi, men, rate):
    base = uri // 1000 * 1000
    ut = base * 78 // 1000                      # 課税標準額は1,000円単位なので割り切れる
    m = min(men, shi)
    ko = (shi - m) * 78 // 1000 + (m * 78 // 1000) * 70 // 100   # その都度1円未満切り捨て
    return {'ut': ut, 'ko': ko,
            'kan': tot(ut - ut * rate // 100),
            'hon': tot(ut - ko),
            'san': tot(ut - ut * 70 // 100),
            'ni': tot(ut - ut * 80 // 100)}

# 届出の期限(国税通則法第10条第2項・同施行令第2条第2項)
HOL = {datetime.date(2027, 1, 1), datetime.date(2028, 1, 1), datetime.date(2028, 4, 29), datetime.date(2028, 5, 3),
       datetime.date(2028, 5, 4), datetime.date(2028, 5, 5), datetime.date(2030, 1, 1)}
YOBI = '月火水木金土日'
def zurasu(d):
    moved = False
    while d.weekday() >= 5 or d in HOL or (d.month == 12 and d.day >= 29) or (d.month == 1 and d.day <= 3):
        d += datetime.timedelta(days=1); moved = True
    return d, moved
def matsu(y, m):
    return datetime.date(y, m, calendar.monthrange(y, m)[1])
def plus(y, m, k):
    m += k
    return (y + (m - 1) // 12, (m - 1) % 12 + 1)
def jp(d):
    return '%d年%d月%d日（%s）' % (d.year, d.month, d.day, YOBI[d.weekday()])
def houjin(mo):
    """決算月 mo の法人。2026年9月30日を含む事業年度が2割特例の最後の期。"""
    y = 2026 if mo >= 9 else 2027
    ny = y + 1                                   # 次の期の末
    d1, z1 = zurasu(matsu(*plus(ny, mo, 2)))     # 次の期の確定申告期限(期末の翌日から2か月)
    d2, z2 = zurasu(matsu(*plus(ny, mo, 3)))     # 申告期限の延長(1か月)がある法人
    return ['%d年%d月期' % (y, mo), '%d年%d月期' % (ny, mo), jp(d1), jp(d2)], (z1, z2)

MINASHI = {'90': '第1種', '80': '第2種', '70': '第3種', '60': '第4種', '50': '第5種', '40': '第6種'}

async def body(pg):
    n = bad = 0
    def chk(label, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp:
            bad += 1; print('NG', label, '画面', got, '原本', exp)
    # 1 計算(window.__nw.calc を同じ入力で呼ぶ)
    uris = [0, 999, 1000, 1001, 1282, 1283, 3000000, 4274000, 5000000, 5555000, 9000000, 9000999, 9999999,
            10000000, 10001000, 12345678, 30000000, 49999000, 50000000, 987654321]
    # 3割特例・2割特例・簡易課税で1円未満と100円未満の端数が境目に来る売上
    for b in range(1000, 400000, 1000):
        ut = b * 78 // 1000
        if (ut * 3) % 10 and -(-ut * 3 // 10) % 100 == 0 and len(uris) < 60:
            uris.append(b)
    shis = [(0, 0), (3000000, 300000), (3000000, 0), (3000000, 3000000), (1234567, 765433), (2999999, 1),
            (7777777, 3333333), (100000000, 0), (5000000, 9000000)]
    for uri in uris:
        for shi, men in shis:
            for rate in (90, 80, 70, 60, 50, 40):
                got = await pg.evaluate('([a,b,c,d])=>window.__nw.calc(a,b,c,d)', [uri, shi, men, rate])
                exp = ref(uri, shi, men, rate)
                n += 1
                if any(got[k] != exp[k] for k in exp):
                    bad += 1; print('NG 計算', uri, shi, men, rate, {k: got[k] for k in exp}, exp)
    # 2 画面の既定(法人・3月決算・第5種・売上900万・仕入れ300万・うち30万)
    exp = ref(9000000, 3000000, 300000, 50)
    chk('既定 簡易課税', num(await pg.inner_text('#o-a')), exp['kan'])
    chk('既定 本則課税', num(await pg.inner_text('#o-b')), exp['hon'])
    chk('既定 3割特例(法人は出さない)', (await pg.inner_text('#o-c')).strip(), '—')
    li = await pg.inner_text('#o-1')
    chk('既定 内訳の文の数字', [int(x.replace(',', '')) for x in re.findall(r'[\d,]+(?=円)', li)], [exp['ut'], exp['ko'], exp['ni']])
    chk('既定 判定', await pg.inner_text('#o-vd'), 'いちばん少ないのは簡易課税です')
    chk('既定 差額', num(re.search(r'より([\d,]+)円', await pg.inner_text('#o-vds')).group(1)), exp['hon'] - exp['kan'])
    # JS が書き換える前の元の文(HTML に直に書いた既定の結果)が画面と同じか
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'niwari-tokurei', 'index.html'), encoding='utf-8').read()
    def moto(i):
        m = re.search(r'id="%s"[^>]*>(.*?)</(?:b|p|li|span|em)>' % i, raw, re.S)
        return re.sub(r'<[^>]+>', '', m.group(1)) if m else None
    for i in ('o-msg', 'o-vd', 'o-vds', 'o-a', 'o-b', 'o-c', 'o-ce', 'o-1'):
        chk('元の文 ' + i, moto(i), (await pg.inner_text('#' + i)).strip())
    chk('元の文 簡易課税の額', num(moto('o-a')), exp['kan'])
    chk('元の文 本則課税の額', num(moto('o-b')), exp['hon'])
    chk('元の文 判定の箱の色', 'class="vd no" id="vd"' in raw, True)
    # 届出の期限の特例は前の期に2割特例を使った事業者だけ。出典の文字は着いた先の題名
    chk('条件 2割特例を使った法人', 'この期限は最後の期に2割特例を使った法人の場合です。' in raw, True)
    chk('出典の文字', '0026002-095.pdf">国税庁「インボイス制度に関する令和8年度税制改正について」' in raw, True)
    # 国税庁の例示:12月決算法人は令和10年2月29日・個人の令和11年分は令和12年4月1日
    chk('例示 12月決算', houjin(12)[0][2], '2028年2月29日（火）')
    chk('例示 個人 令和11年分', zurasu(datetime.date(2030, 3, 31))[0], datetime.date(2030, 4, 1))
    # 入力欄に値を入れて結果の箱を読む
    for uri, shi, men, gy in [(4274000, 1000000, 0, '70'), (12345678, 7777777, 3333333, '90'), (9999999, 2999999, 1, '40')]:
        await pg.fill('#uri', str(uri)); await pg.fill('#shi', str(shi)); await pg.fill('#men', str(men))
        await pg.select_option('#gy', gy)
        e = ref(uri, shi, men, int(gy))
        chk('入力 簡易 %d' % uri, num(await pg.inner_text('#o-a')), e['kan'])
        chk('入力 本則 %d' % uri, num(await pg.inner_text('#o-b')), e['hon'])
    # 個人事業者
    await pg.click('#kei button[data-v="1"]')
    chk('個人 3割特例', num(await pg.inner_text('#o-c')), e['san'])
    chk('個人 3割特例の年分', (await pg.inner_text('#o-ce')).strip(), '2027・2028年分')
    d27, _ = zurasu(datetime.date(2028, 3, 31)); d29, _ = zurasu(datetime.date(2030, 3, 31))
    msg = await pg.inner_text('#o-msg')
    chk('個人 届出の期限の文', '2027年分から簡易課税にする届出は%d年%d月%d日まで' % (d27.year, d27.month, d27.day) in msg and '2026年分が最後' in msg, True)
    await pg.click('#kei button[data-v="0"]')
    # 3 決算月ごとの表(HTML の表・JS の TBL・結果の文)
    rows = await pg.eval_on_selector_all(':is(#list ~ .tw):not(#list ~ .tw ~ .tw) tbody tr', 'rs=>rs.map(r=>Array.from(r.cells).map(c=>c.innerText.replace(/\\s+/g,"")))')
    tbl = await pg.evaluate('window.__nw.TBL')
    chk('表の行数', len(rows), 12)
    for mo in range(1, 13):
        e, (z1, z2) = houjin(mo)
        r = rows[mo - 1]
        chk('表 %d月 決算月' % mo, r[0], '%d月' % mo)
        chk('表 %d月 最後の期' % mo, r[1], e[0])
        chk('表 %d月 届出の期限' % mo, r[2], e[2] + ('※' if z1 else ''))
        chk('表 %d月 延長がある法人' % mo, r[3], e[3] + ('※' if z2 else ''))
        chk('TBL %d月' % mo, tbl[str(mo)], e)
        await pg.select_option('#fy', str(mo))
        chk('結果の文 %d月' % mo, await pg.inner_text('#o-msg'),
            '2割特例の最後の期は%sです。次の%sを簡易課税にする届出は%sまで（申告期限の延長がある法人は%sまで）です。' % tuple(e))
    # 4 個人事業者の表
    k = await pg.eval_on_selector_all(':is(#kojin ~ .tw):not(#kojin ~ .tw ~ .tw) tbody tr', 'rs=>rs.map(r=>Array.from(r.cells).map(c=>c.innerText.replace(/\\s+/g,"")))')
    chk('個人の表 2026年分', k[0][:2], ['2026年分', '2割特例（最後）・簡易課税・本則課税'])
    chk('個人の表 2027・2028年分', k[1], ['2027年分2028年分', '3割特例・簡易課税・本則課税', '%d年%d月%d日2026年分に2割特例を使った人' % (d27.year, d27.month, d27.day)])
    chk('個人の表 2029年分から', k[2], ['2029年分から', '簡易課税・本則課税', '%d年%d月%d日2028年分に3割特例を使った人' % (d29.year, d29.month, d29.day)])
    # 5 事業区分の表(No.6505・No.6509)と選ぶ欄
    g = await pg.eval_on_selector_all(':is(#gyoshu ~ .tw):not(#gyoshu ~ .tw ~ .tw) tbody tr', 'rs=>rs.map(r=>Array.from(r.cells).map(c=>c.innerText.replace(/\\s+/g,"")))')
    for i, rate in enumerate((90, 80, 70, 60, 50, 40)):
        r = g[i]
        chk('事業区分 %d' % (i + 1), (r[0][:3], r[1], r[2]), ('第%d種' % (i + 1), '%d%%' % rate, '%d%%' % (100 - rate)))
        chk('3割特例と比べると %d' % (i + 1), r[3], '簡易課税が少ない' if 100 - rate < 30 else '同じ' if 100 - rate == 30 else '3割特例が少ない')
    opts = await pg.eval_on_selector_all('#gy option', 'os=>os.map(o=>[o.value,o.textContent])')
    for v, t in opts:
        chk('選ぶ欄 ' + v, (t[:3], '（%s%%）' % v in t), (MINASHI[v], True))
    # 6 計算の例の文と結論の文
    html = await pg.content()
    e = ref(9000000, 3000000, 300000, 50)
    kk = h100(e['ut'] - e['ut'] * 50 // 100)
    for label, s in [('例 売上の消費税', '売上の消費税（国税）は%s円です' % format(e['ut'], ',')),
                     ('例 簡易課税', '国税%s円、地方消費税%s円で合計%s円です' % (format(kk, ','), format(e['kan'] - kk, ','), format(e['kan'], ','))),
                     ('例 本則課税', '差し引けるのは%s円と%s円です。納める合計は%s円です' % (format(2700000 * 78 // 1000, ','), format(300000 * 78 // 1000 * 70 // 100, ','), format(e['hon'], ','))),
                     ('結論 3月決算', '3月決算の会社なら%sが最後で、次の期を簡易課税にする届出は<b class="nw">%sまで</b>です' % (houjin(3)[0][0], houjin(3)[0][2][:-3]))]:
        chk(label, s in html, True)
    return n, bad
run('niwari-tokurei', body)
