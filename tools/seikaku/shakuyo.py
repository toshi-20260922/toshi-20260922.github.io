# /shakuyo/ 借用書の印紙税と文面。
# 原本:国税庁 No.7140（令和8年4月1日現在法令等）第1号文書の消費貸借に関する契約書
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7140.htm
#   5億円超10億円以下は20万円、10億円超50億円以下は40万円、50億円超は60万円（令和8年4月1日現在の表）
# 国税庁 No.7101 https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7101.htm
# 利息は元金×年利×日数÷365の1円未満切り捨て。日数は借りた日の翌日から返す日まで（日付の差）。
# ページの JS を見ずに下の式で計算し、画面の印紙税・利息・文面の金額と突き合わせる。
# 最後に原本を確かめた日: 2026-11-27
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

BANDS = [
    (9999, 0), (100000, 200), (500000, 400), (1000000, 1000), (5000000, 2000),
    (10000000, 10000), (50000000, 20000), (100000000, 60000), (500000000, 100000),
    (1000000000, 200000), (5000000000, 400000),
]


def stamp(yen):
    if yen <= 0:
        return 200
    for top, tax in BANDS:
        if yen <= top:
            return tax
    return 600000


def interest(amount, rate, days):
    bp = int(round(float(rate) * 100))
    if amount <= 0 or bp <= 0 or days <= 0:
        return 0
    return amount * bp * days // 3650000


async def body(pg):
    n = bad = 0

    def ng(*a):
        nonlocal bad
        bad += 1
        print('NG', *a)

    cases = [0, 1, 9999, 10000, 100000, 100001, 500000, 500001, 1000000, 1000001,
             3000000, 5000000, 5000001, 10000000, 10000001, 50000000, 50000001,
             100000000, 100000001, 500000000, 500000001, 1000000000, 1000000001,
             5000000000, 5000000001]
    for yen in cases:
        await pg.fill('#amt', str(yen))
        got = num(await pg.inner_text('#o-tax'))
        n += 1
        if got != stamp(yen):
            ng('印紙', yen, got, stamp(yen))
    # 利息。300万円・年1.5%・2026-04-01から2027-04-01は365日で45,000円
    await pg.fill('#amt', '3000000')
    await pg.fill('#rate', '1.5')
    await pg.fill('#d1', '2026-04-01')
    await pg.fill('#d2', '2027-04-01')
    got = num(await pg.inner_text('#o-int'))
    n += 1
    if got != 45000:
        ng('利息365日', got)
    doc = await pg.inner_text('#o-doc')
    n += 1
    if '45,000' not in doc:
        ng('文面の利息', doc[:80])
    # 無利息・日数が逆なら利息0
    await pg.fill('#rate', '0')
    await pg.fill('#d2', '2026-04-01')
    got = num(await pg.inner_text('#o-int'))
    n += 1
    if got != 0:
        ng('無利息', got)
    # 境目の文面。100万円ちょうどは1,000円
    await pg.fill('#amt', '1000000')
    await pg.fill('#rate', '0')
    got = num(await pg.inner_text('#o-tax'))
    vd = await pg.inner_text('#o-vd')
    n += 2
    if got != 1000:
        ng('100万', got)
    if '1,000' not in vd:
        ng('結論の枠', vd)
    # 1万円未満は非課税
    await pg.fill('#amt', '9999')
    vd = await pg.inner_text('#o-vd')
    n += 1
    if vd != '印紙税はかかりません':
        ng('非課税の枠', vd)
    # HTMLに直に書いた初期値（JSの前のファイル）は、300万円で2,000円
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            'site', 'shakuyo', 'index.html'), encoding='utf-8').read()
    n += 1
    if '印紙税は2,000円です' not in raw or '>2,000<i>円</i>' not in raw:
        ng('初期表示')
    return n, bad


if __name__ == '__main__':
    run('shakuyo', body)
