# /kakutei-shinkoku-keisan/ 確定申告シミュレーション(2026-11-21 新規)。
# 定数は前に原本で確かめたページの値を使う(この回は WebSearch だけで、本文は読めない):
#   給与所得(年末調整等のための給与所得控除後の給与等の金額の表・令和8年分)… seikaku/shotoku-kingaku.py と同じ
#   基礎控除(489万円以下104万・655万円以下67万・2,350万円以下62万・2,400万円以下48万・2,450万円以下32万・2,500万円以下16万)… No.1199・2026kaisei.pdf
#   速算表 No.2260・復興特別所得税(基準所得税額×2.1%・1円未満切捨て)
#   医療費控除 No.1120(10万円か総所得金額等の5%の少ない方・上限200万円)・寄附金控除 No.1150(総所得金額等の40%まで・2千円)
#   配偶者控除 No.1191(900万以下38万・950万以下26万・1,000万以下13万)・扶養控除 No.1180(一般38万・特定63万)
#   課税所得の1,000円未満切捨て・申告納税額の100円未満切捨て(国税通則法118条・119条)
# 照らすもの:window.__shinkoku の結果を、ページの式を見ずに書いた下の ref と比べる。境目(課税所得195万・330万・695万・900万、
#   合計所得489万・655万、医療費の5%と10万円が入れ替わる合計所得200万、寄附の40%、配偶者控除の900万・950万・1,000万、100円未満)。
#   既定の入力で JS を止めた画面の数字と、早見表・例の表の全行。
import os, sys, re, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
import rates

def gs(x):
    return rates.kyuyo_r8(x)

def kiso(t):
    return rates.kiso_shotoku(t)

def tax(k):
    br = [(1950000, 5), (3300000, 10), (6950000, 20), (9000000, 23), (18000000, 33), (40000000, 40), (10**15, 45)]
    t = 0; lo = 0
    for hi, r in br:          # 速算表ではなく、帯ごとに足す形で出す
        if k > lo:
            t += (min(k, hi) - lo) * r
        lo = hi
    return t // 100

def ref(q, wq, jo, wj, sha, ide, sei, iryo, kifu, hg, fu, tf, loan):
    tot = gs(q) + jo
    md = max(0, iryo - (100000 if tot >= 2000000 else tot * 5 // 100))
    md = min(md, 2000000)
    kd = max(0, min(kifu, tot * 40 // 100) - 2000)
    sp = 0
    if hg:
        sp = 380000 if tot <= 9000000 else (260000 if tot <= 9500000 else (130000 if tot <= 10000000 else 0))
    deduct = sha + ide + min(sei, 170000) + md + kd + sp + fu * 380000 + tf * 630000 + kiso(tot)
    kz = (tot - deduct) // 1000 * 1000 if tot > deduct else 0
    base = max(0, tax(kz) - loan)
    total = base * rates.FUKKO_NUM // rates.FUKKO_DEN
    d = total - wq - wj
    return dict(tz=total, kz=kz, pay=(d // 100 * 100) if d > 0 else 0, ref=-d if d < 0 else 0)

async def body(pg):
    n = bad = 0
    async def js(*a):
        return await pg.evaluate('a=>window.__shinkoku.apply(null,a)', list(a))
    def chk(lab, got, want):
        nonlocal n, bad
        n += 1
        for k in want:
            if got[k] != want[k]:
                bad += 1; print('合わない', lab, k, got[k], want[k]); return
    # 1 年収ごと(1万円きざみ 100〜3,000万円)・社会保険料15%
    for m in range(100, 3001, 7):
        q = m * 10000; sh = q * 15 // 100
        a = (q, 0, 0, 0, sh, 0, 0, 0, 0, 0, 0, 0, 0)
        chk(a, await js(*a), ref(*a))
    # 2 課税所得の境目の前後(給与以外の所得で合わせる)
    for kz in [1950000, 3300000, 6950000, 9000000, 18000000, 40000000]:
        for dlt in [-1000, -1, 0, 1, 999, 1000]:
            jo = kz + 1040000 + dlt
            a = (0, 0, jo, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            chk(('kz', kz, dlt), await js(*a), ref(*a))
    # 3 合計所得の境目(基礎控除・配偶者控除・医療費の5%)
    for t in [1999999, 2000000, 2000001, 4890000, 4890001, 6550000, 6550001, 9000000, 9000001, 9500000, 9500001, 10000000, 10000001, 23500000, 23500001, 25000000, 25000001]:
        for hg in [0, 1]:
            for iryo in [0, 99999, 100000, 150000, 2200000]:
                a = (0, 300000, t, 0, 0, 0, 0, iryo, 0, hg, 0, 0, 0)
                chk(('tot', t, hg, iryo), await js(*a), ref(*a))
    # 4 組み合わせ
    for q, jo, sha, sei, iryo, kifu, hg, fu, tf, loan, wq, wj in itertools.product(
            [0, 1360000, 3000000, 5000000, 8500000, 12000000], [0, 200000, 500000, 3000000], [0, 700000],
            [0, 200000], [0, 300000], [0, 60000, 3000000], [0, 1], [0, 2], [0, 1], [0, 150000], [0, 100000], [0, 306300]):
        a = (q, wq, jo, wj, sha, 0, sei, iryo, kifu, hg, fu, tf, loan)
        chk(a, await js(*a), ref(*a))
    # 5 JS を止める前(既定の文字)と動いた後の結果の箱
    h = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'kakutei-shinkoku-keisan', 'index.html'), encoding='utf-8').read()
    vals = {i: int(re.search(r'id="%s"[^>]*value="(\d+)"' % i, h).group(1)) for i in ['q', 'wq', 'jo', 'wj', 'sha', 'ide', 'sei', 'iryo', 'kifu', 'loan']}
    w = ref(vals['q'], vals['wq'], vals['jo'], vals['wj'], vals['sha'], vals['ide'], vals['sei'], vals['iryo'], vals['kifu'], 0, 0, 0, vals['loan'])
    raw = re.search(r'id="o-a">([^<]*)<', h).group(1)
    n += 1
    if num(raw) != w['ref']:
        bad += 1; print('合わない 既定の文字 o-a', raw, w['ref'])
    got = num(await pg.inner_text('#o-a'))
    n += 1
    if got != w['ref']:
        bad += 1; print('合わない 画面 o-a', got, w['ref'])
    # 箱に入れて動かす
    for q, jo, iryo, wq in [(4000000, 0, 400000, 57176), (5000000, 500000, 0, 90358), (0, 2000000, 0, 0)]:
        await pg.fill('#q', str(q)); await pg.fill('#jo', str(jo)); await pg.fill('#iryo', str(iryo)); await pg.fill('#wq', str(wq))
        await pg.fill('#sha', str(q * 15 // 100 if q else 400000)); await pg.fill('#wj', str(306300 if q == 0 else 0))
        r = ref(q, wq, jo, 306300 if q == 0 else 0, q * 15 // 100 if q else 400000, 0, 0, iryo, 0, 0, 0, 0, 0)
        g = num(await pg.inner_text('#o-a')); lab = await pg.inner_text('#o-al')
        want = r['ref'] or r['pay']
        n += 1
        if g != want or (r['pay'] and '納める' not in lab):
            bad += 1; print('合わない 箱', q, jo, iryo, g, lab, r)
    # 6 早見表と例の表(年末調整の額・戻る額)
    rows = re.findall(r'<tr><td>([\d,]+)万円</td><td>(\d+)%</td><td>([\d,]+)</td><td>([\d,]+)</td><td>([\d,]+)</td></tr>', h)
    n += 1
    if len(rows) != 7:
        bad += 1; print('早見表の行の数', len(rows))
    for m, rt, w0, r1, r2 in rows:
        q = int(m.replace(',', '')) * 10000; sh = q * 15 // 100
        nen = ref(q, 0, 0, 0, sh, 0, 0, 0, 0, 0, 0, 0, 0)['tz']
        a1 = ref(q, nen, 0, 0, sh, 0, 0, 300000, 0, 0, 0, 0, 0)['ref']
        a2 = ref(q, nen, 0, 0, sh, 0, 0, 0, 50000, 0, 0, 0, 0)['ref']
        n += 1
        if (num(w0), num(r1), num(r2)) != (nen, a1, a2):
            bad += 1; print('合わない 早見表', m, w0, r1, r2, nen, a1, a2)
    return n, bad

run('kakutei-shinkoku-keisan', body)
