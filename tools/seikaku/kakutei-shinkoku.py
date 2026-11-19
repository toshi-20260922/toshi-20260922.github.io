# /kakutei-shinkoku/ 確定申告の期限の早見表(計算の少ないページ。表の全部の数字と日付を原本の値と比べる)。
# 原本:
#  国税庁「主な国税の納期限(法定納期限)及び振替日」(令和8年分:所得税 納期限 令和9年3月15日(月)・振替日 4月23日(金)/
#   消費税 納期限 3月31日(水)・振替日 4月30日(金)/予定納税 第1期 令和8年7月31日(金)・第2期 11月30日(月))
#   https://www.nta.go.jp/taxes/nozei/nofu/24200042/noufu_kigen.htm
#  国税庁 広報「所得税及び復興特別所得税の確定申告は…」(令和8年分:受付 令和9年2月16日(火)から3月15日(月)・還付申告は2月15日(月)以前でも出せる・
#   振替依頼書は3月15日(月)まで)  https://www.nta.go.jp/publication/pamph/koho/campaign/r9/Feb/01.htm
#  国税庁 広報「消費税・地方消費税(個人事業者)の確定申告と納税は正しくお早めに」(令和8年分:期限 令和9年3月31日(水)・振替日 4月30日(金))
#   https://www.nta.go.jp/publication/pamph/koho/campaign/r9/Feb/02.htm
#  国税庁 No.2020 確定申告(翌年2月16日から3月15日)  https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2020.htm
#  国税庁 No.4429 贈与税の申告と納税(翌年2月1日から3月15日)  https://www.nta.go.jp/taxes/shiraberu/taxanswer/zoyo/4429.htm
#  国税庁 No.2030 還付申告(翌年1月1日から5年間)  https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2030.htm
#  国税庁 No.2040 予定納税(予定納税基準額15万円以上・第1期 7月1日から7月31日・第2期 11月1日から11月30日)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2040.htm
#  国税庁 No.1900 給与所得者で確定申告が必要な人(2,000万円・20万円)  https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm
#  国税庁 No.2024 確定申告を忘れたとき(無申告加算税 5%/10%・15%・25%/15%・20%・30%。50万円・300万円の境目。1か月以内・過去5年の条件)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2024.htm
#  国税庁 No.9205 延滞税について・「延滞税の割合」(令和8年1月1日から12月31日:年2.8%・2か月を過ぎた日以後 年9.1%)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/osirase/9205.htm  https://www.nta.go.jp/taxes/nozei/entaizei/keisan/entai_wariai.htm
#  国税庁 No.2072 青色申告特別控除(65万円・55万円は期限内の申告が要件・それ以外は10万円)  https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2072.htm
#  国税庁 C1-1 法人税の申告(事業年度終了の日の翌日から2か月以内・土日祝日等は翌日)・C1-17 申告期限の延長の特例の申請(1か月)
#   https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/hojin/shinkoku/01.htm  https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/hojin/annai/1554_12.htm
#  国税通則法基本通達 第10条関係(日曜・祝日・一般の休日(1月2日と3日)・土曜・12月29日から31日は翌日)
#   https://www.nta.go.jp/law/tsutatsu/kihon/tsusoku/01/03/10.htm
#  祝日は国民の祝日に関する法律。春分の日と秋分の日は国立天文台の暦要項(2027年まで公表。2028年からは計算による見込みの日)。
# 最後に原本を確かめた日:2026-11-19
import os, sys, re, datetime, calendar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, SITE
D = datetime.date
W = '月火水木金土日'

# ---- 暦(ページの JS を見ずに書いたもの) ----
SHUNBUN = {2024: 20, 2025: 20, 2026: 20, 2027: 21, 2028: 20, 2029: 20, 2030: 20, 2031: 21, 2032: 20, 2033: 20, 2034: 20, 2035: 21, 2036: 20}
SHUBUN = {2024: 22, 2025: 23, 2026: 23, 2027: 23, 2028: 22, 2029: 23, 2030: 23, 2031: 23, 2032: 22, 2033: 23, 2034: 23, 2035: 23, 2036: 22}
def nth_mon(y, m, n):
    d = D(y, m, 1)
    return d + datetime.timedelta((7 - d.weekday()) % 7 + 7 * (n - 1))
def named(y):
    s = {D(y, 1, 1), D(y, 2, 11), D(y, 2, 23), D(y, 4, 29), D(y, 5, 3), D(y, 5, 4), D(y, 5, 5), D(y, 8, 11), D(y, 11, 3), D(y, 11, 23),
         nth_mon(y, 1, 2), nth_mon(y, 7, 3), nth_mon(y, 9, 3), nth_mon(y, 10, 2), D(y, 3, SHUNBUN[y]), D(y, 9, SHUBUN[y])}
    return s
_H = {}
def holidays(y):
    if y not in _H:
        s = named(y); out = set(s)
        for h in sorted(s):                       # 振替休日:日曜の祝日のあとの、祝日でない最初の日
            if h.weekday() == 6:
                n = h + datetime.timedelta(1)
                while n in s: n += datetime.timedelta(1)
                out.add(n)
        for h in sorted(s):                       # 国民の休日:祝日にはさまれた日
            mid = h + datetime.timedelta(1)
            if mid not in s and mid + datetime.timedelta(1) in s and mid.weekday() != 6: out.add(mid)
        _H[y] = out
    return _H[y]
def closed(d):
    return d.weekday() >= 5 or (d.month == 12 and d.day >= 29) or (d.month == 1 and d.day <= 3) or d in holidays(d.year)
def shift(d):
    while closed(d): d += datetime.timedelta(1)
    return d
def eom(y, m):
    y += (m - 1) // 12; m = (m - 1) % 12 + 1
    return D(y, m, calendar.monthrange(y, m)[1])
def md(d): return '%d月%d日（%s）' % (d.month, d.day, W[d.weekday()])
def ymd(d): return '%d年%s' % (d.year, md(d))
def big(d): return '%d月%d日' % (d.month, d.day)
def sub(d): return '%d年・%s曜' % (d.year, W[d.weekday()])

# ---- 原本の値(令和8年分) ----
SHO_S, SHO_E, SHO_F = D(2027, 2, 16), D(2027, 3, 15), D(2027, 4, 23)   # 所得税 受付の始め・期限・振替日
KAN_MAE = D(2027, 2, 15)                                              # 還付申告はこの日以前でも出せる
SZ_E, SZ_F = D(2027, 3, 31), D(2027, 4, 30)                           # 個人の消費税 期限・振替日
ZO_S, ZO_E = D(2027, 2, 1), D(2027, 3, 15)                            # 贈与税
KAN_S = D(2027, 1, 1); KAN_E = D(KAN_S.year + 5, 1, 1) - datetime.timedelta(1)   # 還付申告 翌年1月1日から5年間
LIST = [  # 「令和8年分の申告と納付の期限の一覧」の行ごとの文(空白と改行を取って比べる)
    '所得税復興特別所得税を含む|%sから%sまで納付の期限：%s口座振替の日：%s' % (ymd(SHO_S), md(SHO_E), md(SHO_E), md(SHO_F)),
    '所得税の還付申告|2027年1月1日から5年間%s以前でも出せる' % md(KAN_MAE),
    '消費税個人事業主|%sまで納付の期限：%s口座振替の日：%s' % (ymd(SZ_E), md(SZ_E), md(SZ_F)),
    '贈与税|%sから%sまで納付の期限：%s' % (ymd(ZO_S), md(ZO_E), md(ZO_E)),
    '所得税の予定納税|第1期：7月1日から7月31日第2期：11月1日から11月30日前年分の税額をもとに計算した額が15万円以上の人',
    '法人税・法人の消費税|事業年度が終わった日の翌日から2か月以内納付の期限も同じ日',
]
WHO = [['1', '2,000'], ['1', '20'], ['20']]                                # 「確定申告をしなければならない人」の右の列の数字
LATE = [(['1'], ['5']), ([], ['5']), ([], ['10', '50', '300', '15', '300', '25']), ([], ['15', '50', '300', '20', '300', '30']),
        ([], ['2.8', '2', '9.1', '2026', '1', '1', '12', '31'])]      # 「期限に遅れたときにかかる税金」の左と右の列の数字
SENT = [  # 表の外の文に出る数字と日付(原本の値から組み立てた文がページにそのままあるか)
    '令和8年分の所得税の確定申告は、%sから%sまでです' % (ymd(SHO_S), md(SHO_E)),
    '令和8年（2026年）分は%sから%sまでに出し、同じ3月15日までに納めます。' % (ymd(SHO_S), md(SHO_E)),
    '還付を受けるだけの申告は、%s以前でも出せます。' % md(KAN_MAE),
    '所得税は%sまで、消費税は%sまでに申し込みます。' % (md(SHO_E), md(SZ_E)),
    '税金が戻ってくる還付申告は、%s以前でも出せます。' % md(KAN_MAE),
    '還付申告は、その年の翌年1月1日から5年間出せます。',
    '令和8年分なら、%d年1月1日から%d年%d月%d日までです。' % (KAN_S.year, KAN_E.year, KAN_E.month, KAN_E.day),
    '令和8年分は3月15日が%s曜日なので、%sが期限です。' % (W[SHO_E.weekday()], md(SHO_E)),
    '令和8年分の所得税は%s、個人事業主の消費税は%sに引き落とされます。' % (ymd(SHO_F), md(SZ_F)),
    '申し込みの期限は、所得税が%sで消費税が%sです。' % (md(SHO_E), md(SZ_E)),
    '令和8年分の確定申告の期間は%sから%sまで。' % (ymd(SHO_S), md(SHO_E)),
    '個人事業主の青色申告特別控除の65万円と55万円は、期限内に申告した場合だけ受けられます。',
    '3月15日を過ぎると、控除は最高10万円になります。',
    '法人税と法人の消費税は、事業年度が終わった日の翌日から2か月以内に申告して納めます。',
    '税務署に申請すると申告の期限を1か月延ばせます。',
    '所得の合計が所得控除の合計を超えて税金が出るときに確定申告をします。',
]
def nums(t): return re.findall(r'\d[\d,.]*', t)
def flat(t): return re.sub(r'\s+', '', t)

def ref_calc(kind, today):
    if kind == 'sho': a, b, c, l1 = SHO_E, SHO_E, SHO_F, '受付は%sからです' % ymd(SHO_S)
    if kind == 'kan': a, b, c, l1 = KAN_E, None, None, '令和8年分の還付申告は、%sから5年間出せます' % ymd(KAN_S)
    if kind == 'sz': a, b, c, l1 = SZ_E, SZ_E, SZ_F, '申告と納付の期限は%sです' % ymd(SZ_E)
    if kind == 'zo': a, b, c, l1 = ZO_E, ZO_E, None, '受付は%sからです' % ymd(ZO_S)
    n = (a - today).days
    l2 = '今日から期限まで、あと%d日です' % n if n >= 0 else '期限を過ぎています。下の「期限に遅れたときにかかる税金」を見てください'
    return {'la': '出せる期限' if kind == 'kan' else '申告の期限', 'oa': big(a), 'ea': sub(a),
            'ob': big(b) if b else '—', 'eb': sub(b) if b else '', 'oc': big(c) if c else '—', 'ec': sub(c) if c else '', 'l1': l1, 'l2': l2}
def ref_houjin(k, today):
    """決算月 k の法人で、今日からあとに最初に来る期限。期限は事業年度の最後の日の2か月後の月末(休みなら次の平日)。"""
    y = today.year - 2
    while True:
        e = eom(y, k); dl = shift(eom(y, k + 2))
        if dl >= today: return e, dl
        y += 1
def ref_table(today):
    rows = []
    for i in range(12):
        y, m = today.year + (today.month - 1 + i) // 12, (today.month - 1 + i) % 12 + 1
        rows.append('%d月|%s|%s' % (m, ymd(eom(y, m)), ymd(shift(eom(y, m + 2)))))
    return rows

async def body(pg):
    n = bad = 0
    def chk(label, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp:
            bad += 1; print('NG', label, '\n  画面', got, '\n  原本', exp)
    # 1 原本の期限そのものが暦で休みに当たらないこと(当たれば翌日にずれるので原本の値と食い違う)
    for lab, d in (('所得税の期限', SHO_E), ('所得税の振替日', SHO_F), ('消費税の期限', SZ_E), ('消費税の振替日', SZ_F), ('贈与税の期限', ZO_E),
                   ('受付の始め', SHO_S), ('贈与税の始め', ZO_S)):
        chk(lab + 'が平日', shift(d), d)
    chk('2月15日は2月16日の前の日', KAN_MAE + datetime.timedelta(1), SHO_S)
    # 2 HTML に手で書いた曜日の全部(このページの「M月D日（曜）」は全部2027年の日付)
    src = open(os.path.join(SITE, 'kakutei-shinkoku', 'index.html'), encoding='utf-8').read()
    static = re.sub(r'<script.*?</script>', '', src, flags=re.S)
    static = static.replace('更新日：2026年11月19日', '')
    for m in re.finditer(r'(?:(\d{4})年)?(\d{1,2})月(\d{1,2})日（(.)）', static):
        d = D(2027, int(m.group(2)), int(m.group(3)))
        chk('曜日 ' + m.group(0), (m.group(1) or '2027', m.group(4)), ('2027', W[d.weekday()]))
    # 3 一覧の表・しなければならない人の表・遅れたときの表
    tb = await pg.evaluate("""()=>[...document.querySelectorAll('main table')].map(t=>[...t.tBodies[0].rows].map(r=>[...r.cells].map(c=>c.innerText)))""")
    chk('一覧の表の行の数', len(tb[0]), len(LIST))
    for row, exp in zip(tb[0], LIST):
        chk('一覧 ' + flat(row[0]), flat(row[0]) + '|' + flat(row[1]), exp)
    chk('しなければならない人の表の行の数', len(tb[2]), len(WHO))
    for row, exp in zip(tb[2], WHO):
        chk('人 ' + row[0], nums(row[1]), exp)
    chk('遅れたときの表の行の数', len(tb[3]), len(LATE))
    for row, (e0, e1) in zip(tb[3], LATE):
        chk('遅れ(左) ' + row[0][:12], nums(row[0]), e0)
        chk('遅れ(右) ' + row[0][:12], nums(row[1]), e1)
    # 4 表の外の文
    text = flat(re.sub(r'<[^>]+>', '', static)) + flat(static)   # 後ろは meta の説明文を見るため
    for s in SENT:
        chk('文 ' + s[:18], flat(s) in text, True)
    # 5 計算の箱と法人の表(今日の日付を変えて見る。年末年始・期限の当日と翌日・うるう年を含む)
    days = [D(2026, 11, 19), D(2026, 12, 31), D(2027, 1, 1), D(2027, 1, 4), D(2027, 1, 5), D(2027, 2, 1), D(2027, 2, 2), D(2027, 3, 15),
            D(2027, 3, 16), D(2027, 3, 31), D(2027, 4, 1), D(2027, 5, 31), D(2027, 8, 2), D(2027, 8, 3), D(2027, 12, 30), D(2028, 2, 29),
            D(2028, 5, 1), D(2029, 12, 31), D(2031, 12, 31), D(2032, 1, 1)]
    for t in days:
        await pg.clock.set_fixed_time(datetime.datetime(t.year, t.month, t.day, 12, 0))
        await pg.reload()
        for kind in ('sho', 'kan', 'sz', 'zo'):
            await pg.select_option('#kind', kind)
            got = await pg.evaluate("""()=>{var g=i=>document.getElementById(i).textContent;return {la:g('l-a'),oa:g('o-a'),ea:g('e-a'),ob:g('o-b'),eb:g('e-b'),oc:g('o-c'),ec:g('e-c'),l1:g('o-1'),l2:g('o-2')}}""")
            chk('箱 %s %s' % (t, kind), got, ref_calc(kind, t))
        await pg.select_option('#kind', 'ho')
        for k in range(1, 13):
            await pg.select_option('#ki', str(k))
            got = await pg.evaluate("""()=>{var g=i=>document.getElementById(i).textContent;return [g('o-a'),g('e-a'),g('o-b'),g('e-b'),g('o-c'),g('l-c'),g('o-1'),g('o-2')]}""")
            e, dl = ref_houjin(k, t)
            chk('箱 %s 法人%d月' % (t, k), got, [big(dl), sub(dl), big(dl), sub(dl), '%d日' % (dl - t).days, '残り', ymd(e) + 'に終わる事業年度の期限です',
                                              '申告の期限を1か月延ばす申請をしていても、納付の期限は' + ymd(dl) + 'のままです'])
        rows = await pg.evaluate("""()=>[...document.querySelectorAll('#tb tr')].map(r=>[...r.cells].map(c=>c.innerText.replace(/\\s+/g,'')).join('|'))""")
        chk('法人の表の行の数 %s' % t, len(rows), 12)
        for g, x in zip(rows, ref_table(t)):
            chk('法人の表 %s %s' % (t, x[:3]), g, x)
    # 6 月末の日を次の平日にずらす動き(2025年から2035年の全部の月末)
    for y in range(2025, 2036):
        for m in range(1, 13):
            d = eom(y, m)
            got = await pg.evaluate('([y,m,d])=>{var r=window.__tt.shift(new Date(y,m-1,d));return [r.getFullYear(),r.getMonth()+1,r.getDate()]}', [d.year, d.month, d.day])
            x = shift(d)
            chk('ずらす %s' % d, got, [x.year, x.month, x.day])
    return n, bad
run('kakutei-shinkoku', body)
