# /yakuin-shataku/ 役員社宅の家賃の計算。
# 原本:国税庁 No.2600「役員に社宅などを貸したとき」 https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2600.htm
#      (令和8年4月1日現在法令等。小規模=耐用年数30年以下132㎡以下・30年超99㎡以下。
#       小規模:家屋×0.2%+12円×床面積÷3.3+敷地×0.22%。小規模でない自社所有:(家屋×12%(30年超は10%)+敷地×6%)÷12。
#       借上げ:家賃の50%と自社所有の算式の多いほう。240㎡超は豪華社宅の判定)
#      所得税基本通達36-40・36-41 https://www.nta.go.jp/law/tsutatsu/kihon/shotoku/05/04.htm
#      国税庁 No.2597「使用人に社宅や寮などを貸したとき」 https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2597.htm
#      国税庁「主な減価償却資産の耐用年数表」 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/pdf/2100_01.pdf
# 端数:原本に端数処理の定めは無い。ページは「各項目の1円未満を四捨五入」と断っているので、その断りどおりかを見る。
# 最後に原本を確かめた日:2026-11-19
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

def r(x):                      # 1円未満を四捨五入(0.5は切り上げ)
    return int((F(x) * 2 + 1) // 2)

def ref(k, m2, ie, tochi, own, rent):
    """k=1:耐用年数30年超 0:30年以下。m2 は文字列(小数可)。own=1:会社の持ち物。"""
    m = F(m2)
    lim = 99 if k == 1 else 132
    if m <= lim:
        p1 = r(F(ie) * 2 / 1000); p2 = r(12 * m / F('3.3')); p3 = r(F(tochi) * 22 / 10000)
        return {'kind': 's', 'v': p1 + p2 + p3, 'p1': p1, 'p2': p2, 'p3': p3, 'big': m > 240}
    y = r((F(ie) * (10 if k == 1 else 12) / 100 + F(tochi) * 6 / 100) / 12)
    if own == 1:
        return {'kind': 'o', 'v': y, 'y': y, 'big': m > 240}
    half = r(F(rent) / 2)
    return {'kind': 'r', 'v': max(y, half), 'y': y, 'half': half, 'big': m > 240}

async def body(pg):
    n = bad = 0
    # 1) 関数どうし。床面積は境目(99・132・240)の前後と小数。金額は低い・中・高いと四捨五入の境目。
    m2s = ['0', '1', '25.5', '33', '68.8875', '70', '98.99', '99', '99.01', '120', '131.99', '132', '132.01',
           '200', '240', '240.01', '300', '0.1375', '13.6125', '41.1125', '0.4125', '3.9875', '5.9125', '7.2875', '11.1375']
    ies = [0, 1, 249, 250, 251, 60, 3000000, 6000000, 6000250, 12345678, 50000000, 300000000, 999999999]
    tos = [0, 1, 2272, 2273, 2500, 3000000, 9876543, 40000000, 500000000]
    rents = [0, 1, 99999, 200000, 200001, 1500000]
    for k in (0, 1):
        for m2 in m2s:
            for ie in ies:
                for to in tos:
                    for own in (0, 1):
                        for rent in (rents if own == 0 else [0]):
                            exp = ref(k, m2, ie, to, own, rent)
                            got = await pg.evaluate('([k,m,i,t,o,r])=>window.__sh.calc(k,m,i,t,o,r)',
                                                    [k, float(m2), ie, to, own, rent])
                            n += 1
                            if any(got.get(key) != val for key, val in exp.items()):
                                bad += 1
                                if bad <= 30: print('NG', k, m2, ie, to, own, rent, got, exp)
    # 小規模でない算式の0.5の境目((家屋×率+敷地×6)÷1200 がちょうど .5)と、その1円前後
    for k, rate in ((1, 10), (0, 12)):
        for q in (0, 7, 12345, 400000):
            for to in (0, 100, 5555500):
                rest = 1200 * q + 600 - to * 6
                if rest < 0 or rest % rate: continue
                for ie in (rest // rate - 1, rest // rate, rest // rate + 1):
                    if ie < 0: continue
                    for own in (0, 1):
                        exp = ref(k, '150', ie, to, own, 0)
                        got = await pg.evaluate('([k,m,i,t,o,r])=>window.__sh.calc(k,m,i,t,o,r)', [k, 150, ie, to, own, 0])
                        n += 1
                        if got['v'] != exp['v'] or got['y'] != exp['y']:
                            bad += 1; print('NG 境目', k, ie, to, own, got, exp)
    # 小数の定数(0.10・0.06)を掛けてから丸めると1円ずれた組(2026-11-19 に見つけてページを整数の式に直した)
    for k, ie, to in ((1, 14892204, 379426760), (1, 1131384, 349261060), (1, 23133909, 479863985), (1, 5551527, 185511155)):
        for own in (0, 1):
            exp = ref(k, '150', ie, to, own, 0)
            got = await pg.evaluate('([k,m,i,t,o,r])=>window.__sh.calc(k,m,i,t,o,r)', [k, 150, ie, to, own, 0])
            n += 1
            if got['v'] != exp['v']: bad += 1; print('NG 小数の丸め', k, ie, to, own, got, exp)
    # 借上げ:家賃の50%と算式がちょうど同じ・1円上下
    for ie, to in ((20000000, 15000000), (8000000, 4000000)):
        y = ref(1, '150', ie, to, 1, 0)['v']
        for rent in (2 * y - 2, 2 * y - 1, 2 * y, 2 * y + 1, 2 * y + 2):
            exp = ref(1, '150', ie, to, 0, rent)
            got = await pg.evaluate('([k,m,i,t,o,r])=>window.__sh.calc(k,m,i,t,o,r)', [1, 150, ie, to, 0, rent])
            n += 1
            if got['v'] != exp['v'] or got['half'] != exp['half']:
                bad += 1; print('NG 50%の境目', rent, got, exp)

    # 2) 画面。入力欄に値を入れて結果の箱と文を読む。
    async def screen(k, m2, ie, to, own, rent, get):
        await pg.click('#kozo button[data-v="%d"]' % k)
        await pg.click('#own button[data-v="%d"]' % own)
        await pg.fill('#m2', m2); await pg.fill('#ie', str(ie)); await pg.fill('#tochi', str(to))
        if own == 0: await pg.fill('#rent', str(rent))
        await pg.fill('#get', str(get))
        return {'a': num(await pg.inner_text('#o-a')), 'ae': num((await pg.inner_text('#o-ae')).replace('1年で', '')),
                'b': num(await pg.inner_text('#o-b')), 'c': await pg.inner_text('#o-c'),
                'msg': await pg.inner_text('#o-msg'), 'li': await pg.inner_text('#o-1'),
                'rentbox': await pg.is_visible('#rentbox')}
    cases = [(1, '70', 6000000, 3000000, 0, 200000, 18855), (1, '70', 6000000, 3000000, 0, 200000, 0),
             (1, '70', 6000000, 3000000, 0, 200000, 10000), (1, '99', 8000000, 4000000, 0, 150000, 30000),
             (1, '99.01', 8000000, 4000000, 0, 150000, 30000), (1, '99.01', 8000000, 4000000, 1, 0, 30000),
             (0, '132', 5000000, 6000000, 1, 0, 0), (0, '132.01', 5000000, 6000000, 1, 0, 50000),
             (0, '132.01', 5000000, 6000000, 0, 300000, 150000), (1, '150', 20000000, 15000000, 0, 480000, 200000),
             (1, '240', 30000000, 30000000, 0, 600000, 400000), (1, '240.01', 30000000, 30000000, 0, 600000, 400000),
             (0, '250', 40000000, 50000000, 1, 0, 700000), (1, '25', 1000000, 500000, 0, 60000, 5000)]
    for k, m2, ie, to, own, rent, get in cases:
        s = await screen(k, m2, ie, to, own, rent, get)
        e = ref(k, m2, ie, to, own, rent)
        lim = 99 if k == 1 else 132
        chk = [('賃貸料相当額', s['a'], e['v']), ('1年で', s['ae'], e['v'] * 12),
               ('給与になる額', s['b'], max(e['v'] - get, 0)),
               ('家賃の欄が出る', s['rentbox'], own == 0),
               ('文:小規模', ('小規模な住宅の算式' in s['msg']), e['kind'] == 's'),
               ('文:境目の㎡', ('%d㎡' % lim) in s['msg'], True),
               ('文:豪華社宅', '豪華社宅' in s['msg'], F(m2) > 240)]
        if own == 0: chk.append(('会社が持つ家賃', num(s['c']), max(rent - get, 0)))
        else: chk.append(('会社が持つ家賃は—', s['c'].strip(), '—'))
        if e['kind'] == 's':
            chk.append(('内訳', [int(x.replace(',', '')) for x in re.findall(r'([\d,]+)円', s['li'])], [e['p1'], e['p2'], e['p3']]))
        else:
            chk.append(('算式の文の率', ('×%d%%' % (10 if k == 1 else 12)) in s['li'], True))
            chk.append(('算式の文の額', num(s['li'].split('＝')[1]), e['y']))
        if e['kind'] == 'r':
            got2 = [int(x.replace(',', '')) for x in re.findall(r'（([\d,]+)円）', s['msg'])]
            chk.append(('文:50%と算式の額', got2, [e['half'], e['y']]))
        for name, g, x in chk:
            n += 1
            if g != x: bad += 1; print('NG 画面', (k, m2, ie, to, own, rent, get), name, g, x)

    # 3) 手で書いた早見表(床面積70㎡・小規模)の全部の数字
    rows = await pg.evaluate('''()=>[...document.querySelectorAll("table.t5 tbody tr")].map(tr=>[...tr.children].map(td=>td.textContent))''')
    head = await pg.evaluate('''()=>[...document.querySelectorAll("table.t5 thead th")].map(th=>th.textContent)''')
    tos2 = [int(re.search(r'(\d+)万円', h).group(1)) * 10000 for h in head[1:]]
    n += 1
    if tos2 != [2000000, 3000000, 4000000, 6000000] or len(rows) != 6: bad += 1; print('NG 早見表の形', head, len(rows))
    for row in rows:
        ie = int(row[0].replace(',', '').replace('万円', '')) * 10000
        for to, cell in zip(tos2, row[1:]):
            n += 1
            e = ref(1, '70', ie, to, 0, 0)['v']
            if num(cell) != e: bad += 1; print('NG 早見表', ie, to, cell, e)
    # 4) 本文に手で書いた数字
    html = await pg.content()
    e0 = ref(1, '70', 6000000, 3000000, 0, 0)
    for name, ok in [
        ('結論の18,855円', '家屋の課税標準額600万円・敷地300万円）なら、役員から月%s円以上' % format(e0['v'], ',') in re.sub(r'<[^>]+>', '', html)),
        ('床面積の部分255円', '（12円×70㎡÷3.3㎡）は%d円です' % e0['p2'] in html),
        ('小規模 132㎡', '132㎡<br>以下' in html), ('小規模 99㎡', '99㎡<br>以下' in html),
        ('率 0.2%', '①家屋の課税標準額×0.2%' in html), ('率 0.22%', '③敷地の課税標準額×0.22%' in html),
        ('12円÷3.3㎡', '②12円×床面積（㎡）÷3.3㎡' in html),
        ('率 12%と10%', '①家屋の課税標準額×12%（耐用年数30年超の建物は10%）' in html), ('率 6%', '②敷地の課税標準額×6%' in html),
        ('12分の1', '次の2つの合計の12分の1' in html), ('借上げ50%', '会社が払う家賃の50%と' in html),
        ('豪華社宅240㎡', '床面積が240㎡を超えるもののうち' in html),
        ('耐用年数 木造22年', '木造（22年）' in html), ('木骨モルタル20年', '木骨モルタル（20年）' in html),
        ('鉄骨27年・19年', '肉厚4mm以下の鉄骨' in html and '（27年・19年）' in html),
        ('鉄筋コンクリート47年', '鉄筋コンクリート（47年）' in html), ('れんが・ブロック38年', 'れんが・ブロック（38年）' in html),
        ('鉄骨34年', '肉厚4mm超の鉄骨（34年）' in html),
        ('従業員50%', '従業員から賃貸料相当額の50%以上を受け取っていれば' in html),
        ('令和8年4月1日現在', '令和8年4月1日現在' in html),
        ('既定の受取額18,855', 'id="get" class="w" type="text" inputmode="numeric" value="%s"' % format(e0['v'], ',') in html),
    ]:
        n += 1
        if not ok: bad += 1; print('NG 本文', name)
    return n, bad
run('yakuin-shataku', body)
