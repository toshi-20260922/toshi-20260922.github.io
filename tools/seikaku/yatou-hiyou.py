# /yatou-hiyou/ 人を雇う費用の計算(従業員1人の会社負担)。
# 原本:
#  全国健康保険協会「令和8年度都道府県単位保険料率」(47都道府県の健康保険料率・介護1.62%・子ども子育て支援金0.23%)
#    https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  全国健康保険協会「令和8年3月分(4月納付分)からの健康保険・厚生年金保険の保険料額表(東京都)」(厚生年金18.3%・拠出金0.36%・本人負担は50銭以下切り捨て50銭超切り上げ)
#    https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#  厚生労働省・こども家庭庁「子ども・子育て支援金に関するQ&A」問6(一般保険料率と支援金率を合算した率を掛けて折半した額で端数処理)
#    https://www.mhlw.go.jp/hourei/doc/tsuchi/T260216S0101.pdf
#  日本年金機構「従業員に賞与を支給したときの手続き」(標準賞与額の上限は健康保険が年度の累計573万円・厚生年金は1か月あたり150万円。同じ月に2回以上なら合算)
#    https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20141203.html
#  全国健康保険協会の保険料額表(標準報酬月額の等級1〜50の区切り。区切りは令和2年9月から変わっていない)
#    https://www.kyoukaikenpo.or.jp/~/media/Files/shared/hokenryouritu/r5/ippan/r50210gunma.pdf
#  日本年金機構「保険料額表(厚生年金保険と協会けんぽ管掌の健康保険)」(令和8年度の拠出金率1,000分の3.6・厚生年金の上限32等級65万円)
#    https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/20200825.html
#  日本年金機構「厚生年金保険の保険料」(1等級8万8千円〜32等級65万円・標準賞与額は1,000円未満切り捨て)
#    https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20150515-01.html
#  日本年金機構「健康保険・船員保険の標準報酬月額の上限改定及び累計標準賞与額の上限変更」(第50級139万円・年度の累計573万円)
#    https://www.nenkin.go.jp/service/kounen/kyokaikenpo/0208.html
#  厚生労働省 山形労働局「令和8年度の雇用保険料率について」(一般の事業 労働者5/1,000・事業主8.5/1,000)
#    https://jsite.mhlw.go.jp/yamagata-roudoukyoku/koyouhoken-20260316.html
#  厚生労働省「令和8年度の労災保険率等について」(卸売業・小売業、飲食店又は宿泊業 3/1,000・その他の各種事業 3/1,000)
#    https://jsite.mhlw.go.jp/gunma-roudoukyoku/content/contents/002595367.pdf
# 最後に原本を確かめた日:2026-11-20
# 端数(2026-11-20 に /hoteifukurihi/ と同じ方式へ直した):健康保険(介護・支援金を合算した率)と厚生年金は、
#  全額(1円未満切り捨て)−本人負担(折半額の50銭以下切り捨て・50銭超切り上げ)が会社の負担。拠出金は1円未満切り捨て。
#  雇用保険と労災保険は1円未満四捨五入。合計は内訳の足し算。賞与は月ごとに別の月に払う前提(厚生年金は1か月150万円まで)。
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

# 原本の等級表(標準報酬月額, 報酬月額の「未満」)。50等級は上限なし。
GRADE = [(58000,63000),(68000,73000),(78000,83000),(88000,93000),(98000,101000),(104000,107000),(110000,114000),
 (118000,122000),(126000,130000),(134000,138000),(142000,146000),(150000,155000),(160000,165000),(170000,175000),
 (180000,185000),(190000,195000),(200000,210000),(220000,230000),(240000,250000),(260000,270000),(280000,290000),
 (300000,310000),(320000,330000),(340000,350000),(360000,370000),(380000,395000),(410000,425000),(440000,455000),
 (470000,485000),(500000,515000),(530000,545000),(560000,575000),(590000,605000),(620000,635000),(650000,665000),
 (680000,695000),(710000,730000),(750000,770000),(790000,810000),(830000,855000),(880000,905000),(930000,955000),
 (980000,1005000),(1030000,1055000),(1090000,1115000),(1150000,1175000),(1210000,1235000),(1270000,1295000),
 (1330000,1355000),(1390000,None)]
# 原本の令和8年度の健康保険料率(万分率)。北海道から沖縄県の順。
KENPO = [('北海道',1028),('青森県',985),('岩手県',951),('宮城県',1010),('秋田県',1001),('山形県',975),('福島県',950),
 ('茨城県',952),('栃木県',982),('群馬県',968),('埼玉県',967),('千葉県',973),('東京都',985),('神奈川県',992),
 ('新潟県',921),('富山県',959),('石川県',970),('福井県',971),('山梨県',955),('長野県',963),('岐阜県',980),
 ('静岡県',961),('愛知県',993),('三重県',977),('滋賀県',988),('京都府',989),('大阪府',1013),('兵庫県',1012),
 ('奈良県',991),('和歌山県',1006),('鳥取県',986),('島根県',994),('岡山県',1005),('広島県',978),('山口県',1015),
 ('徳島県',1024),('香川県',1002),('愛媛県',998),('高知県',1005),('福岡県',1011),('佐賀県',1055),('長崎県',1006),
 ('熊本県',1008),('大分県',1008),('宮崎県',977),('鹿児島県',1013),('沖縄県',944)]
KAIGO, SIEN, NENKIN, KYOSHUTSU = F(162,10000), F(23,10000), F(183,1000), F(36,10000)
KOYO_J, ROSAI = F(85,10000), F(3,1000)

def rnd(x):                       # 1円未満四捨五入(正の数)
    return int((x * 2 + 1) // 2)
def hyojun(m):
    for s, top in GRADE:
        if top is None or m < top: return s
def half(x):                      # 50銭以下切り捨て・50銭超切り上げ
    q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q
def kaisha(base, rate):           # 全額(円未満切り捨て)−本人負担
    z = base * rate
    return z.numerator // z.denominator - half(z / 2)
def tsuki(m, old, ken):           # ken は万分率
    s = hyojun(m); p = min(max(s, 88000), 650000)
    r = {'ken': kaisha(s, F(ken,10000) + SIEN + (KAIGO if old else 0)), 'nen': kaisha(p, NENKIN),
         'kyo': int(p * KYOSHUTSU // 1), 'koy': rnd(m * KOYO_J), 'rou': rnd(m * ROSAI)}
    r['t'] = sum(r.values()); return r
def shoyo(b, n, old, ken):
    t = 0; cum = 0
    for _ in range(n):
        sb = b // 1000 * 1000
        hk = max(0, min(sb, 5730000 - cum)); cum += hk
        pn = min(sb, 1500000)
        t += kaisha(hk, F(ken,10000) + SIEN + (KAIGO if old else 0)) + kaisha(pn, NENKIN) + int(pn * KYOSHUTSU // 1) + rnd(b * KOYO_J) + rnd(b * ROSAI)
    return t

async def setv(pg, m, b, bn, old, pi):
    await pg.fill('#pay', str(m)); await pg.fill('#bon', str(b))
    await pg.select_option('#pref', str(pi))
    await pg.click('#s-bn button[data-v="%d"]' % bn); await pg.click('#s-age button[data-v="%d"]' % old)

async def body(pg):
    n = bad = 0
    def chk(label, got, exp):
        nonlocal n, bad
        n += 1
        if got != exp: bad += 1; print('NG', label, '画面', got, '原本からの計算', exp)
    # 1) 都道府県の選択肢(名前と率)を原本の47件と比べる
    opts = await pg.eval_on_selector_all('#pref option', 'os=>os.map(o=>o.textContent)')
    chk('県の数', len(opts), 47)
    for (name, r), o in zip(KENPO, opts):
        chk('選択肢 ' + name, o, '%s（%d.%02d%%）' % (name, r // 100, r % 100))
    # 2) 月の会社負担:全等級の境目の前後(1円下・ちょうど・1円上)と代表例を、全47県・年齢2通りで関数に通す
    ms = {0, 1, 50000, 57999, 58000, 100000, 180000, 200000, 220000, 250000, 280000, 300000, 350000, 400000,
          450000, 500000, 650000, 800000, 1000000, 1390000, 2000000, 123456, 333333, 298765}
    for s, top in GRADE:
        if top: ms |= {top - 1, top, top + 1}
    ms = sorted(ms)
    for pi, (name, ken) in enumerate(KENPO):
        await pg.select_option('#pref', str(pi))
        for old in (0, 1):
            got = await pg.evaluate('([ms,old])=>ms.map(m=>{var r=window.__yt.month(m,old);return [r.ken,r.nen,r.kyo,r.koy,r.rou,r.t]})', [ms, old])
            for m, g in zip(ms, got):
                e = tsuki(m, old, ken)
                chk('月 %s %d old%d' % (name, m, old), g, [e[k] for k in ('ken','nen','kyo','koy','rou','t')])
    # 3) 賞与:上限(1か月150万円・年度573万円)の前後と1,000円未満の端数
    bs = [0, 999, 1000, 300000, 500500, 600000, 1499999, 1500000, 1500999, 1501000, 2864999, 2865000, 2865001,
          2866000, 3000000, 5729999, 5730000, 5731000, 8000000]
    for pi in (0, 12, 14, 26, 40, 46):
        name, ken = KENPO[pi]
        await pg.select_option('#pref', str(pi))
        for old in (0, 1):
            for bn in (0, 1, 2):
                got = await pg.evaluate('([bs,bn,old])=>bs.map(b=>Math.round(window.__yt.bonus(b,bn,old)))', [bs, bn, old])
                for b, g in zip(bs, got):
                    chk('賞与 %s %d×%d old%d' % (name, b, bn, old), g, shoyo(b, bn, old, ken))
    # 4) 画面の箱(入力欄に入れて読む):県・年齢・賞与を変えて
    cases = [(300000, 0, 0, 0, 12), (180000, 0, 0, 0, 0), (250000, 500000, 2, 1, 26), (289999, 0, 0, 1, 14),
             (290000, 300000, 1, 0, 40), (650000, 2000000, 2, 1, 46), (1400000, 3000000, 2, 0, 22),
             (88000, 0, 0, 0, 39), (224500, 123456, 2, 1, 13), (500000, 1500000, 2, 1, 12)]
    for m, b, bn, old, pi in cases:
        await setv(pg, m, b, bn, old, pi)
        name, ken = KENPO[pi]; e = tsuki(m, old, ken); mt = e['t']
        tag = '%s 月給%d 賞与%d×%d old%d' % (name, m, b, bn, old)
        chk('保険料(月) ' + tag, num(await pg.inner_text('#o-a')), mt)
        chk('1か月の総額 ' + tag, num(await pg.inner_text('#o-b')), m + mt)
        chk('1年の総額 ' + tag, num(await pg.inner_text('#o-c')), mt * 12 + m * 12 + shoyo(b, bn, old, ken) + b * bn)
        pct = rnd(F(mt, m) * 1000)
        chk('月給の% ' + tag, await pg.inner_text('#e-a'), '月給の%s%%' % (str(pct // 10) if pct % 10 == 0 else '%d.%d' % (pct // 10, pct % 10)))
        o1 = [int(x.replace(',', '')) for x in re.findall(r'([\d,]+)円', await pg.inner_text('#o-1'))]
        o2 = [int(x.replace(',', '')) for x in re.findall(r'([\d,]+)円', (await pg.inner_text('#o-2')).split('（')[0])]
        chk('内訳1 ' + tag, o1, [e[k] for k in ('ken', 'nen', 'kyo')])
        chk('内訳1の言葉 ' + tag, (await pg.inner_text('#o-1')).startswith('健康保険（介護保険・子ども・子育て支援金を含む）' if old else '健康保険（子ども・子育て支援金を含む）'), True)
        chk('内訳2 ' + tag, o2, [e[k] for k in ('koy', 'rou')])
        chk('県の名前 ' + tag, (await pg.inner_text('#o-3')).startswith(name + 'の協会けんぽ'), True)
        # 早見表の全行(選んだ県と年齢・賞与なし)
        rows = await pg.eval_on_selector_all('#tb tr', 'rs=>rs.map(r=>Array.from(r.cells).map(c=>c.textContent))')
        chk('早見表の行数 ' + tag, len(rows), 10)
        for row, v in zip(rows, (18, 20, 22, 25, 28, 30, 35, 40, 45, 50)):
            M = v * 10000; x = tsuki(M, old, ken)['t']
            chk('早見表 %d万 %s' % (v, tag), [num(c) for c in row], [v, x, M + x, (M + x) * 12])
    # 5) 手で書いた数字(結論の帯・冒頭の文・料率の表・よく聞かれること)。東京都・40歳未満・月給30万円
    html = await pg.content()
    e = tsuki(300000, 0, 985); mt = e['t']
    chk('結論の帯', '月給30万円の人を1人雇うと、会社が払う保険料は月%s円で1年の総額は%s円です' % (format(mt, ','), format((300000 + mt) * 12, ',')) in html, True)
    chk('冒頭の文', '月給30万円なら、会社が払う保険料は月%s円で月給のおよそ%s%%です' % (format(mt, ','), '%.1f' % (rnd(F(mt, 300000) * 1000) / 10)) in html, True)
    def pc(fr):                    # 率を%の文字にする(末尾の0を落とす)
        s = '%.3f' % float(fr * 100)   # 表示だけ。値は分数で持つ
        return s.rstrip('0').rstrip('.') + '%'
    tbl = await pg.eval_on_selector_all('#rate + .tw tbody tr', 'rs=>rs.map(r=>[r.cells[1].textContent,r.cells[2].textContent])')
    exp = [[pc(F(985,10000)/2)]*2, [pc(KAIGO/2)]*2, [pc(SIEN/2)]*2, [pc(NENKIN/2)]*2, [pc(KYOSHUTSU), 'なし'],
           [pc(KOYO_J), pc(F(5,1000))], [pc(ROSAI), 'なし']]
    chk('料率の表の行数', len(tbl), 7)
    for g, x in zip(tbl, exp): chk('料率の表', g, x)
    shaho = F(985,10000)/2 + SIEN/2 + NENKIN/2 + KYOSHUTSU
    chk('およそ14.6%', '%d.%d' % divmod(rnd(shaho * 1000), 10), '14.6')
    chk('およそ15.7%', '%d.%d' % divmod(rnd((shaho + KOYO_J + ROSAI) * 1000), 10), '15.7')
    chk('介護0.81%の文', '介護保険の' + pc(KAIGO/2) + 'が加わります' in html, True)
    chk('賞与の上限の文', '健康保険は年度の合計573万円、厚生年金は1か月150万円が上限です。同じ月に2回以上払うときは、その月の合計で150万円までです。' in html and '1回150万円' not in html, True)
    return n, bad
run('yatou-hiyou', body)
