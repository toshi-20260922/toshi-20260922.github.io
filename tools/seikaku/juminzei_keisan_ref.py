# /juminzei-keisan/ の計算(ページを見ずに書いた式)。build_juminzei_keisan.py と tools/seikaku/juminzei-keisan.py が使う。
# 令和9年度の住民税(2026年の給与)。東京23区など標準税率(市区町村6%・都道府県4%)・均等割と森林環境税5,000円・1級地。
# 数字の出どころ(どれも前に原本で確かめたページと同じ):
#  給与所得控除(令和8年分・No.1410)… /juminzei/ /tedori/
#  住民税の基礎控除 43万・29万・15万・0円 … /juminzei/(11/20)
#  配偶者控除 33万・22万・11万(合計所得900万・950万・1,000万円以下)・扶養控除33万・特定扶養45万・人的控除差(基礎5万・配偶者5万/4万/2万・扶養5万・特定18万)… /furusato/(11/21 zen)
#  非課税:所得割 35万×(人数+1)+10万+32万(扶養ありのとき)・均等割 35万×(人数+1)+10万+21万(1級地)・単身は45万 … /juminzei/
#  附則3条の3 の所得割の減額 … /juminzei/(11/20)
#  所得金額調整控除(年収850万円超で23歳未満の扶養親族がいる)… /furusato/ /nenmatsu-chosei/
#  2026年の社会保険料(協会けんぽ東京都・各月の料率)… /juminzei/
#  給料から引く毎月の額:年額を12で割り100円未満切り捨て・端数は6月分・年額が均等割5,000円以下は6月分で全額 … /taishoku-jumin/
from fractions import Fraction as F

def kyuyo(x):
    if x < 741000: return 0
    if x < 2191000: return x - 740000
    if x < 2193000: return 1451000
    if x < 2196000: return 1453000
    if x < 2200000: return 1456000
    if x < 6600000:
        a = x // 4000 * 4000
        return a // 4000 * 2800 - 80000 if x < 3600000 else a // 4000 * 3200 - 440000
    if x < 8500000: return x * 9 // 10 - 1100000
    return x - 1950000

BOUND = [63,73,83,93,101,107,114,122,130,138,146,155,165,175,185,195,210,230,250,270,290,310,330,350,370,395,425,455,485,515,545,575,605,635,665,695,730,770,810,855,905,955,1005,1055,1115,1175,1235,1295,1355]
STD = [58,68,78,88,98,104,110,118,126,134,142,150,160,170,180,190,200,220,240,260,280,300,320,340,360,380,410,440,470,500,530,560,590,620,650,680,710,750,790,830,880,930,980,1030,1090,1150,1210,1270,1330,1390]
def std(m):
    for b, s in zip(BOUND, STD):
        if m < b * 1000: return s * 1000
    return 1390000
def r50(x):
    x = F(x); q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q

def shaho(a, old=0):
    """2026年の1年分の社会保険料(協会けんぽ東京都・賞与なし・本人負担)。"""
    m = a // 12; s = std(m); p = min(max(s, 88000), 650000); t = 0
    for k in range(1, 13):
        hr = 991 if k <= 2 else (985 if k == 3 else 1008)
        kai = (159 if k <= 2 else 162) if old else 0
        ko = 55 if k <= 3 else 50
        t += r50(F(s * (hr + kai), 20000)) + r50(F(p * 1830, 20000)) + r50(F(m * ko, 10000))
    return t

def jumin(a, sh, sp=0, n0=0, n1=0, n2=0, n3=0, ide=0, iry=0):
    """a 年収・sh 社会保険料・sp 配偶者控除の対象の配偶者(0/1)・n0 16歳未満の子・n1 16〜18歳・n2 19〜22歳・n3 23〜69歳・ide iDeCoなど・iry 医療費控除。"""
    g = kyuyo(a)
    if a > 8500000 and (n0 + n1 + n2) > 0:
        g -= -(-(min(a, 10000000) - 8500000) // 10)  # 1円未満切り上げ
        g = max(g, 0)
    N = sp + n0 + n1 + n2 + n3
    kin_lim = 350000 * (N + 1) + 100000 + (210000 if N else 0)
    sho_lim = 350000 * (N + 1) + 100000 + (320000 if N else 0)
    r = {'g': g, 'kin': 0, 'sho': 0, 'shi': 0, 'ken': 0, 'y': 0, 'tr': 0, 'kind': 0, 'ded': 0}
    if g <= kin_lim:
        return r  # 住民税はかからない
    r['kin'] = 5000; r['kind'] = 1
    kiso = 430000 if g <= 24000000 else 290000 if g <= 24500000 else 150000 if g <= 25000000 else 0
    spk = (330000 if g <= 9000000 else 220000 if g <= 9500000 else 110000 if g <= 10000000 else 0) if sp else 0
    spd = (50000 if g <= 9000000 else 40000 if g <= 9500000 else 20000 if g <= 10000000 else 0) if sp else 0
    ded = sh + ide + iry + kiso + spk + 330000 * (n1 + n3) + 450000 * n2
    tr = max(0, g - ded) // 1000 * 1000
    r['tr'] = tr; r['ded'] = ded - sh
    if g <= sho_lim:
        r['y'] = 5000; return r  # 均等割だけ
    diff = 50000 + spd + 50000 * (n1 + n3) + 180000 * n2
    if g > 25000000: adj = 0
    elif tr <= 2000000: adj = min(diff, tr)
    else: adj = max(diff - (tr - 2000000), 50000)
    s0 = max(0, tr * 6 // 100 - adj * 3 // 100); k0 = max(0, tr * 4 // 100 - adj * 2 // 100)
    cap = g - sho_lim; tot = s0 + k0
    if tot > cap:
        shi = s0 * cap // (tot * 100) * 100; ken = k0 * cap // (tot * 100) * 100
    else:
        shi = s0 // 100 * 100; ken = k0 // 100 * 100
    r.update(shi=shi, ken=ken, sho=shi + ken, y=shi + ken + 5000, kind=2 if shi + ken else 1)
    return r

def tsuki(y):
    """給料から引く額:(6月分, 7月から翌年5月の毎月)。"""
    if y <= 5000: return (y, 0)
    m = y // 12 // 100 * 100
    return (y - m * 11, m)
