# /yakuin-taishokukin/ 役員退職金の手取り。
# 原本:国税庁 No.1420(退職所得控除・2分の1・勤続5年以下の役員等は2分の1にしない)・No.2732(退職所得の源泉徴収税額の速算表)・No.2737(住民税 市6%・県4%・各100円未満切り捨て)
# 最後に原本を確かめた日:2026-11-19
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run
SOKUSAN = [(1950000, 5, 0), (3300000, 10, 97500), (6950000, 20, 427500), (9000000, 23, 636000),
           (18000000, 33, 1536000), (40000000, 40, 2796000), (None, 45, 4796000)]
def kojo(n):
    return max(800000, 400000 * n) if n <= 20 else 8000000 + 700000 * (n - 20)
def ref(g, n):
    k = max(0, g - kojo(n))
    base = (k if n <= 5 else k // 2) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or base <= top:
            kijun = base * r // 100 - d          # 課税退職所得は1,000円単位なので割り切れる
            it = max(0, kijun) * 1021 // 1000    # 復興特別所得税を合わせて1円未満切り捨て
            break
    shi = base * 6 // 100 // 100 * 100
    ken = base * 4 // 100 // 100 * 100
    return {'it': it, 'ju': shi + ken, 'net': g - it - shi - ken}
async def body(pg):
    n = bad = 0
    gs = [0, 1, 800000, 800001, 4000000, 8000000, 8001000, 15000000, 15001999, 30000000, 50000000,
          90000000, 150000000, 400000000, 1234567890]
    # 速算表の境目の前後(課税退職所得がちょうど境目になる退職金)
    for top, _, _ in SOKUSAN[:-1]:
        for yrs in (3, 20, 30):
            g0 = top + kojo(yrs) if yrs <= 5 else top * 2 + kojo(yrs)
            gs += [g0 - 2000, g0 - 1, g0, g0 + 1, g0 + 1999, g0 + 2000]
    for yrs in (1, 2, 5, 6, 19, 20, 21, 30, 45, 60):
        for g in gs:
            got = await pg.evaluate('([g,n])=>window.__taishoku(g,n)', [g, yrs])
            exp = ref(g, yrs); n += 1
            if any(got[k] != exp[k] for k in exp):
                bad += 1; print('NG', g, yrs, got, exp)
    # 画面の既定(月100万・30年・倍率3.0)の表示
    g = 1000000 * 30 * 3; exp = ref(g, 30); n += 1
    shown = int(''.join(c for c in await pg.inner_text('#o-n') if c.isdigit()))
    if shown != exp['net']:
        bad += 1; print('NG 既定の手取りの表示', shown, exp['net'])
    return n, bad
run('yakuin-taishokukin', body)
