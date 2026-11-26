# 点検が読む制度の数字。原本は tools/rates.json。
# 段階2: 最低賃金の地域別（build_saitei.py）と国保22自治体（regions.py）の生成もこのファイルを読む。公開ページはまだ読まない。値は移す前と同じ。
import json, os
from fractions import Fraction as F

_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'rates.json')
D = json.load(open(_PATH, encoding='utf-8'))

def _val(key):
    return D[key]['value']

KAIGO = _val('kaigo')                 # 万分率 1.62%
SIEN = _val('sien')                   # 万分率 0.23%
NENKIN = _val('nenkin')               # 万分率 18.30%
NENKIN_PER_1000 = D['nenkin']['per_1000']   # 183/1000。万分率と同じ値
KYOSHUTSU = _val('kyoshutsu')         # 万分率 0.36%
KOYO = 50                             # 一般の本人 5/1000 を万分率にしたもの
KOYO_PER_1000 = D['koyo']['rows'][0]['r8_worker'][0]
KOYO_JIGYO_PER_10000 = 85             # 一般の事業主 8.5/1000
ROSAI = _val('rosai_default')         # 千分率。既定1業種
FUKKO_NUM = D['fukko']['num']
FUKKO_DEN = D['fukko']['den']
NENKIN_KOKUMIN = _val('nenkin_kokumin')
NINI_CAP = _val('nini_cap')
NENKIN_MIN = D['tokyu']['nenkin_min']
NENKIN_MAX = D['tokyu']['nenkin_max']
KEIGEN_BASE = D['keigen']['base']
WARI5 = D['keigen']['wari5']
WARI2 = D['keigen']['wari2']
assert KOYO_PER_1000 * 10 == KOYO
assert KOYO_JIGYO_PER_10000 == 85

def kenpo_pref():
    """47都道府県の医療分。(名前, 万分率) を北海道から。"""
    return [(r['name'], r['rate']) for r in D['kenpo_pref']['rows']]

def kenpo(name):
    for n, r in kenpo_pref():
        if n == name:
            return r
    raise KeyError(name)

TOKYO = kenpo('東京都')

def kenpo_picked():
    """dokuritsu が添字で持っていた4県。添字は都道府県の並び(0始まり)。"""
    pref = kenpo_pref()
    return {i: pref[i][1] for i in (12, 26, 14, 40)}

def _tokyu():
    return [(r['std'], r['upper']) for r in D['tokyu']['rows']]

def tokyu_yen():
    """(標準報酬月額, 報酬月額がこの額未満)。最後の未満は None。"""
    return list(_tokyu())

def tokyu_sen():
    """千円単位の (標準報酬, 未満)。最後の未満は None。"""
    return [(a // 1000, None if b is None else b // 1000) for a, b in _tokyu()]

def tokyu_sen_finite(n=None):
    """千円単位。最後の等級を除いた49行、または先頭 n 行。"""
    rows = [(a, b) for a, b in tokyu_sen() if b is not None]
    return rows if n is None else rows[:n]

def tokyu_meisai():
    """給与明細の形。最後の未満は上限なし(10**9)。"""
    return [(a, 10 ** 9 if b is None else b) for a, b in tokyu_sen()]

def tokyu_lower_std_sen():
    """(報酬月額の下限 千円, 標準報酬月額 千円)。先頭の下限は 0。"""
    rows = _tokyu()
    out = [(0, rows[0][0] // 1000)]
    for i in range(1, len(rows)):
        out.append((rows[i - 1][1] // 1000, rows[i][0] // 1000))
    return out

def tokyu_std_lower_yen():
    """(標準報酬月額, 報酬月額の下限)。先頭の下限は 0。"""
    rows = _tokyu()
    out = [(rows[0][0], 0)]
    for i in range(1, len(rows)):
        out.append((rows[i][0], rows[i - 1][1]))
    return out

def tokyu_upper_std_sen():
    """(未満 千円または None, 標準報酬 千円)。"""
    return [(None if b is None else b // 1000, a // 1000) for a, b in _tokyu()]

def std_sen():
    return [a // 1000 for a, _ in _tokyu()]

def std_yen():
    return [a for a, _ in _tokyu()]

def upper_sen():
    """未満の境目49個(最後の等級の上限は無い)。"""
    return [b // 1000 for _, b in _tokyu() if b is not None]

def lower_sen_with_zero():
    """副業の下限。先頭 0 と、49個の未満。"""
    return [0] + upper_sen()

def shaho_gr():
    """社会保険の等級。(等級番号, 標準報酬, 以上, 未満, 東京の折半額×10)。最後の未満は 0。"""
    rate = TOKYO
    prev = 0
    out = []
    for i, (std, up) in enumerate(_tokyu(), 1):
        out.append((i, std, prev, 0 if up is None else up, std * rate // 2000))
        prev = 0 if up is None else up
    return out

def os50():
    """大阪の額表。(標準報酬, 以上, 未満, 介護なし折半×10, 介護あり折半×10, 厚生年金の折半)。"""
    rate = kenpo('大阪府')
    nmin = D['tokyu']['nenkin_min']
    nmax = D['tokyu']['nenkin_max']
    prev = 0
    out = []
    for std, up in _tokyu():
        nen = 0 if std < nmin or std > nmax else std * NENKIN // 20000
        out.append((std, prev, 0 if up is None else up, std * rate // 2000, std * (rate + KAIGO) // 2000, nen))
        prev = 0 if up is None else up
    return out

def osaka_samples(keys):
    """標準報酬月額を鍵にした大阪の折半額×10。(介護なし, 介護あり, 支援金)。"""
    rate = kenpo('大阪府')
    return {s: (s * rate // 2000, s * (rate + KAIGO) // 2000, s * SIEN // 2000) for s in keys}

def _brackets(rows, key_up='upper'):
    return [(r[key_up], r['rate'], r['deduct']) for r in rows]

def sokusan_ue():
    """課税所得がこの額以下。最後の上限は None。"""
    return _brackets(D['sokusan']['rows'])

def sokusan_ue_m1000():
    """1,000円単位に切ったあとの比較用。有限の上限を1,000円下げる。"""
    return [(None if u is None else u - 1000, r, d) for u, r, d in sokusan_ue()]

def sokusan_shita():
    """この額以上でその率。最初の下限は1,000円。"""
    rows = sokusan_ue()
    out = [(1000, rows[0][1], rows[0][2])]
    for i in range(1, len(rows)):
        out.append((rows[i - 1][0], rows[i][1], rows[i][2]))
    return out

KISO_SHOTOKU = [(r['upper'], r['amount']) for r in D['kiso_shotoku']['rows']]
KISO_JUMIN = [(r['upper'], r['amount']) for r in D['kiso_jumin']['rows']]

def kiso_shotoku(g):
    for top, k in KISO_SHOTOKU:
        if g <= top:
            return k
    return 0

def kiso_jumin(g):
    for top, k in KISO_JUMIN:
        if g <= top:
            return k
    return 0

def keigen(g, n):
    """国保の軽減。7・5・2・0。"""
    b = D['keigen']
    if g <= b['base']:
        return 7
    if g <= b['base'] + b['wari5'] * n:
        return 5
    if g <= b['base'] + b['wari2'] * n:
        return 2
    return 0

def _kyuyo(x, p):
    if x < p['zero_under']:
        return 0
    if x < p['flat_under']:
        return x - p['min']
    for under, amt in p.get('bands') or []:
        if x < under:
            return amt
    if x < p['mid_under']:
        a = x // p['step'] * p['step']
        if x < p['mid_split']:
            return a * p['low_rate_num'] // p['low_rate_den'] - p['low_add']
        return a * p['high_rate_num'] // p['high_rate_den'] - p['high_add']
    if x < p['top_under']:
        return x * p['top_rate_num'] // p['top_rate_den'] - p['top_add']
    return x - p['cap']

def kyuyo_r8(x):
    """令和8年分の給与所得。"""
    return _kyuyo(x, D['kyuyo_r8'])

def kyuyo_r7(x):
    """令和7年分の給与所得(前年所得用)。"""
    return _kyuyo(x, D['kyuyo_r7'])

def koyo_gen():
    """雇用保険。(番号, 名前, 令和8本人, 事業主, うち二事業, 令和7本人, 令和7合計)。単位は千分率の分数。"""
    out = []
    for r in D['koyo']['rows']:
        out.append((r['id'], r['name'], F(*r['r8_worker']), F(*r['r8_employer']), F(*r['r8_niji']),
                    F(*r['r7_worker']), F(*r['r7_total'])))
    return out

def saitei_nat():
    """(短い県名, 令和8年度, 令和7年度, 月, 日)。"""
    return [(r['short'], r['reiwa8'], r['reiwa7'], r['month'], r['day']) for r in D['saitei']['rows']]

def kokuho_reg():
    """regions.REG と同じ鍵。p は [所得割, 均等割, 平等割, 上限] が4本。"""
    out = []
    for r in D['kokuho']['rows']:
        p = [[x['shotoku'], x['kinto'], x['byodo'], x['cap']] for x in r['parts']]
        out.append(dict(n=r['name'], s=r['short'], p=p, r=r['r'], nag=r['nag'], url=r['url'], src=r['src']))
    return out

def kokuho_d(with_pref=True):
    """点検の D。(短い名前, 4本の(所得割,均等割,平等割), 端数単位, 名古屋の減額, 医療分の上限[, 都道府県])。"""
    out = []
    for r in D['kokuho']['rows']:
        parts = [(x['shotoku'], x['kinto'], x['byodo']) for x in r['parts']]
        row = [r['short'], parts, r['r'], r['nag'], r['parts'][0]['cap']]
        if with_pref:
            row.append(r['pref'])
        out.append(tuple(row))
    return out

def kokuho_caps():
    r = D['kokuho']['rows'][0]
    return [x['cap'] for x in r['parts']]

def kokuho23():
    """東京23区・40歳未満。医療・支援・子ども。(所得割, 均等割, 上限)。"""
    p = D['kokuho']['rows'][0]['parts']
    return [(p[0]['shotoku'], p[0]['kinto'], p[0]['cap']),
            (p[1]['shotoku'], p[1]['kinto'], p[1]['cap']),
            (p[3]['shotoku'], p[3]['kinto'], p[3]['cap'])]

def kokuho_care():
    p = D['kokuho']['rows'][0]['parts'][2]
    return (p['shotoku'], p['kinto'], p['cap'])
