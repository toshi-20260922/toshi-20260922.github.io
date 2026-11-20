# /houjinzei/ 法人税の早見表(法人税・地方法人税・防衛特別法人税。12か月の事業年度だけ)。
# 原本:
#  国税庁 No.5759 法人税の税率(資本金1億円以下は年800万円以下15%・所得が年10億円超の事業年度は17%・800万円超23.2%。令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5759.htm
#  国税庁「別表一の記載の仕方」(17%の判定は「所得金額又は欠損金額1」の欄の金額が10億円を超えるかで見る。1年未満は10億円÷12×月数)
#   https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/hojin/shinkoku/itiran2025/pdf/01-02-ki.pdf
#  国税庁「令和7年度 法人税関係法令の改正の概要」中小企業者等の法人税率の特例(17%・適用期限2年延長)
#   https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2025/pdf/F.pdf
#  国税庁 法人税基本通達16-4-1(1年未満の事業年度は800万円÷12×月数。1,000円未満の端数の扱い)
#   https://www.nta.go.jp/law/tsutatsu/kihon/hojin/16/16_04.htm
#  国税庁「地方法人税の税率の改正のお知らせ」(10.3%・令和元年10月1日以後に開始する課税事業年度)
#   https://www.nta.go.jp/publication/pamph/hojin/chihou_hojin/01.htm
#  国税庁「令和7年度 法人税関係法令の改正の概要」防衛特別法人税(4%・基礎控除 年500万円・令和8年4月1日以後開始・税額が無くても申告)
#   https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2025/pdf/E.pdf
#  総務省「法人住民税」(均等割 都道府県2万円+市町村5万円=年7万円・赤字でもかかる) https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_08.html
#  中小企業庁「法人税率の軽減」(前3事業年度の所得の平均が15億円を超える法人は特例から除く・本則19%・10億円超は17%) https://www.chusho.meti.go.jp/zaimu/zeisei/tokurei/houjin_keigen.html
#  国税庁「法人税のあらまし」申告と納付(終了の日の翌日から2か月以内・中間申告は算式の額が10万円以下なら不要) https://www.nta.go.jp/publication/pamph/hojin/aramashi2023/pdf/01-04.pdf
#  国税庁「法人税のあらましと申告の手引(令和7年10月)」別表一の記載要領(地方法人税の「所得の金額に対する法人税額」は1,000円未満切り捨て・税額が100円未満なら記載しない)
#   https://www.nta.go.jp/publication/pamph/hojin/aramashi2025/pdf/02-02.pdf
#  国税庁「防衛特別法人税の創設」(令和8年6月改訂。基準法人税額−基礎控除額 年500万円・4%・税額0円でも申告書を出す)
#   https://www.nta.go.jp/publication/pamph/pdf/0025004-109_1.pdf
#  国税庁「令和8年度 法人税関係法令の改正の概要」(法人税率・地方法人税・防衛特別法人税の改正は載っていない)
#   https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2026/pdf/A.pdf
#  国税庁 法人税基本通達9-5-1・9-5-2(事業税は申告書を提出した日の属する事業年度の損金。直前の事業年度分は申告前でも損金にできる)
#   https://www.nta.go.jp/law/tsutatsu/kihon/hojin/09/09_05_01.htm
#  中小企業庁「法人税率の軽減」は、15%の期限を「令和9年3月31日までの間に開始する各事業年度」と書いている(ページには期限を書いていない)
# 原本で確かめられなかった所:防衛特別法人税の課税標準1,000円未満と税額100円未満の切り捨て(国税通則法118条・119条の一般の決まり)は
#  上の資料に書かれていない。租税特別措置法42条の3の2の条文そのものは開けていない。負担率の四捨五入はページの表示の決めで原本は無い。
#  法人事業税の所得割の3段階の標準税率(総務省の PDF)は 11-20 に開けなかった。
# 11-20:ページの式(小数の 0.15・0.232・0.103・0.04)を整数の計算と総当たりで比べた(所得0〜3億円を1,000円刻み・10億円の前後・乱数30万件。248万件で違い0)。
# 照らすもの:結果の箱(法人税・地方法人税+防衛特別法人税・合計・負担率)・結果の文2つ・JS が作る早見表(4つの条件×19行)・
#  JS が書き換える前の HTML の数字(結果の箱・早見表19行)・防衛特別法人税の表4行・本文とよく聞かれることの例の数字
# 最後に原本を確かめた日: 2026-11-20
import os, re, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, SITE

def fl(x, unit):
    return int(x // unit) * unit

def ref(y, cap, st):
    """y=所得(円) cap=0:資本金1億円以下 1:1億円超 st=令和8年4月1日以後に始まる事業年度か"""
    s = fl(y, 1000)                                  # 所得の1,000円未満切り捨て
    if cap == 0:
        low = min(s, 8000000)
        rate = 17 if y > 1000000000 else 15          # 判定は切り捨てる前の所得金額(別表一の1欄)
        hr = F(low * rate, 100) + F((s - low) * 232, 1000)
    else:
        hr = F(s * 232, 1000)
    h = fl(hr, 100)                                  # 法人税 100円未満切り捨て
    c = fl(F(fl(hr, 1000) * 103, 1000), 100)         # 地方法人税
    b = fl(F(fl(max(F(0), hr - 5000000), 1000) * 4, 100), 100) if st else 0
    return h, c, b, h + c + b

def pct(t, y):
    """負担率(%)を小数第1位に四捨五入した値の10倍(整数)"""
    return int((F(t * 1000, y) + F(1, 2)) // 1)

def pct_s(t, y, fixed):
    p = pct(t, y)
    if fixed or p % 10:
        return '%d.%d%%' % (p // 10, p % 10)
    return '%d%%' % (p // 10)

def num(t):
    return int(''.join(ch for ch in t if ch.isdigit()) or 0)

def yen(n):
    return '{:,}'.format(n)

def s1(y, cap):
    if cap == 1:
        return '資本金1億円を超えるので、所得の全部を23.2%で計算しています'
    if y > 1000000000:
        return '所得が10億円を超えるので800万円までは17%で計算しています'
    return '所得のうち800万円までは15%、超えた分は23.2%で計算しています'

def s2(y, cap, st):
    h, c, b, t = ref(y, cap, st)
    if not st:
        return '令和8年3月31日までに始まる事業年度なので、防衛特別法人税は含めていません'
    if b > 0:
        return '防衛特別法人税%s円を含みます。地方法人税は%s円です' % (yen(b), yen(c))
    if h > 5000000:
        return '計算した額が100円未満で切り捨てになるので、防衛特別法人税はかかりません'
    return '防衛特別法人税は、法人税が500万円以下なのでかかりません'

ROWS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 40, 50, 70, 100]

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1
            print('合わない', label, '画面', got, '原本', want)

    # 1 JS が書き換える前の HTML(ファイルをそのまま読む)
    src = open(os.path.join(SITE, 'houjinzei', 'index.html'), encoding='utf-8').read()
    h, c, b, t = ref(10000000, 0, True)
    chk('元の法人税', num(re.search(r'id="o-h">([^<]*)', src).group(1)), h)
    chk('元の地方法人税', num(re.search(r'id="o-c">([^<]*)', src).group(1)), c)
    chk('元の防衛特別法人税', num(re.search(r'id="o-b">([^<]*)', src).group(1)), b)
    chk('元の合計', num(re.search(r'id="o-all">([^<]*)', src).group(1)), t)
    chk('元の負担率', re.search(r'id="o-rt">([^<]*)', src).group(1), '所得の' + pct_s(t, 10000000, False))
    chk('元の文1', re.search(r'id="o-1">([^<]*)', src).group(1), s1(10000000, 0))
    chk('元の文2', re.search(r'id="o-2">([^<]*)', src).group(1), s2(10000000, 0, True))
    chk('元の早見表の条件', re.search(r'id="t-cap">([^<]*)', src).group(1), '資本金1億円以下・令和8年4月1日以後に始まる事業年度')
    gtb = re.search(r'<tbody id="gtb">(.*?)</tbody>', src, re.S).group(1)
    rows = re.findall(r'<tr[^>]*><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td></tr>', gtb)
    chk('元の早見表の行数', len(rows), len(ROWS))
    for m, r in zip(ROWS, rows):
        v = m * 1000000
        h, c, b, t = ref(v, 0, True)
        chk('元の早見表 %d' % v, (num(r[0]), num(r[1]), r[2], num(r[3])), (v, t, pct_s(t, v, True), h))
    # 防衛特別法人税の表(資本金1億円以下の例)
    sec = src[src.index('id="bouei"'):src.index('id="small"')]
    brow = re.findall(r'<tr><td class="l">([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td></tr>', sec)
    chk('防衛の表の行数', len(brow), 4)
    for r, v in zip(brow, (20000000, 30000000, 50000000, 100000000)):
        h, c, b, t = ref(v, 0, True)
        lab = '1億円' if v == 100000000 else '%s万円' % yen(v // 10000)
        chk('防衛の表 %d' % v, (r[0], num(r[1]), num(r[2])), (lab, h, b))
    # 本文の例の数字
    h, c, b, t = ref(8000000, 0, True)
    chk('所得800万円の例', '法人税が%d万円・地方法人税が%s円で、合わせて%s円です' % (h // 10000, yen(c), yen(t)) in src, True)
    # 防衛特別法人税がかかり始める所得(およそ2,438万円):法人税が500万円を超える最初の所得を自分で探す
    # (100円以上の税額が実際に出るのは所得24,393,000円から。本文は「およそ」なので法人税が500万円を超える所で照らす)
    y0 = next(y for y in range(24000000, 25000000, 1000) if ref(y, 0, True)[0] > 5000000)
    chk('かかり始める所得 およそ2,438万円', int(F(y0, 10000) + F(1, 2)), 2438)
    chk('かかり始める所得の文', '所得がおよそ2,438万円を超えるとかかり始めます' in src, True)
    chk('元の防衛特別法人税のカードの下の文字', re.search(r'id="o-bl">([^<]*)', src).group(1), '対象外')
    # 早見表の読み方の率(法人税の率×(1+10.3%)を小数第1位に四捨五入)と、よく聞かれることの「9ポイントほど」
    r1 = F(15 * 1103, 1000); r2 = F(232 * 1103, 10000)
    chk('読み方 約16.5%', '所得の約%s%%（法人税15%%に、その10.3%%の地方法人税を足した率）' % (F(int(r1 * 10 + F(1, 2)), 10).__float__()) in src, True)
    chk('読み方 約25.6%', '超えた所得の約%s%%（法人税23.2%%に、その10.3%%の地方法人税を足した率）' % (F(int(r2 * 10 + F(1, 2)), 10).__float__()) in src, True)
    chk('率の差 9ポイントほど', int(r2 - r1 + F(1, 2)), 9)
    chk('率の差の文', '税率が9ポイントほど高くなります' in src, True)
    # 均等割(総務省:資本金等の額1千万円以下 道府県2万円+市町村(従業者50人以下)5万円)
    chk('均等割 年7万円', '標準の税率で年%d万円です' % ((20000 + 50000) // 10000) in src, True)
    # 税率の表
    for w in ('<td>15%</td><td>23.2%</td>', '<td>23.2%</td><td>23.2%</td>', '法人税の額×10.3%', '（法人税の額−500万円）×4%'):
        chk('税率の表 ' + w, w in src, True)

    # 2 画面の結果
    async def setv(y, cap, st):
        await pg.evaluate('''([y,cap,st])=>{
          var b=document.querySelectorAll(".seg button")[cap]; if(!b.classList.contains("on")) b.click();
          var k=document.getElementById("bou"); if(k.checked!==st) k.click();
          var i=document.getElementById("inc"); i.value=String(y); i.dispatchEvent(new Event("input",{bubbles:true}));}''', [y, cap, st])
    async def read():
        return await pg.evaluate('''()=>{var g=function(id){return document.getElementById(id).textContent};
          return {h:g("o-h"),c:g("o-c"),b:g("o-b"),bl:g("o-bl"),a:g("o-all"),r:g("o-rt"),s1:g("o-1"),s2:g("o-2"),cap:g("t-cap"),
          rows:[].map.call(document.querySelectorAll("#gtb tr"),function(tr){return [].map.call(tr.children,function(td){return td.textContent})}),
          hit:[].map.call(document.querySelectorAll("#gtb tr"),function(tr){return tr.className==="hit"})}}''')
    ys = [0, 1, 999, 1000, 1001, 500000, 1000000, 3000000, 5555555, 10000000, 12345678, 20000000, 30000000,
          50000000, 100000000, 123456789, 300000000, 2000000000, 9999999999, 10000000000]
    for bd in (8000000, 1000000000):                 # 800万円と10億円の境目
        ys += [bd - 1000, bd - 1, bd, bd + 1, bd + 999, bd + 1000, bd + 1001]
    # 法人税がちょうど500万円になる所得のまわり(防衛特別法人税の始まり)
    ys += [24378000, 24379000, 24379310, 24379999, 24380000, 24381000, 24382000, 24383000, 24392000, 24393000, 24394000, 24400000]
    ys += [21551000, 21552000, 21553000, 21565000, 21566000]      # 資本金1億円超で法人税が500万円になるあたり
    for cap in (0, 1):
        for st in (True, False):
            for y in ys:
                await setv(y, cap, st)
                g = await read()
                h, c, b, t = ref(y, cap, st)
                lab = '所得%d 資本金%d 令和8年4月以後%s ' % (y, cap, st)
                chk(lab + '法人税', num(g['h']), h)
                chk(lab + '地方法人税', num(g['c']), c)
                chk(lab + '防衛特別法人税', num(g['b']), b)
                chk(lab + '合計', num(g['a']), t)
                chk(lab + '防衛特別法人税のカードの下の文字', g['bl'], '年額' if b > 0 else '対象外')
                chk(lab + '負担率', g['r'], '所得の' + (pct_s(t, y, False) if y > 0 else '0%'))
                chk(lab + '文1', g['s1'], s1(y, cap))
                chk(lab + '文2', g['s2'], s2(y, cap, st))
            # JS が作る早見表(条件ごとに全行)
            await setv(10000000, cap, st)
            g = await read()
            chk('早見表の条件 %d %s' % (cap, st), g['cap'],
                ('資本金1億円以下' if cap == 0 else '資本金1億円超') + '・' +
                ('令和8年4月1日以後に始まる事業年度' if st else '令和8年3月31日までに始まる事業年度'))
            chk('早見表の行数', len(g['rows']), len(ROWS))
            for m, r in zip(ROWS, g['rows']):
                v = m * 1000000
                h, c, b, t = ref(v, cap, st)
                chk('早見表 %d %s %d' % (cap, st, v), (num(r[0]), num(r[1]), r[2], num(r[3])), (v, t, pct_s(t, v, True), h))
            chk('色の付く行', g['hit'].index(True) if True in g['hit'] else -1, ROWS.index(10))
    # 3 防衛特別法人税の課税標準と負担率の丸めを細かい刻みで(資本金1億円以下・令和8年4月以後)
    for y in list(range(24370000, 24400000, 1000)) + list(range(7990000, 8012000, 1000)) + [10 ** k + d for k in range(4, 10) for d in (-1, 0, 1)]:
        await setv(y, 0, True)
        g = await read()
        h, c, b, t = ref(y, 0, True)
        chk('細かい刻み %d' % y, (num(g['h']), num(g['c']), num(g['b']), num(g['a']), g['r'], g['s2']),
            (h, c, b, t, '所得の' + (pct_s(t, y, False) if y > 0 else '0%'), s2(y, 0, True)))
    return n, bad

run('houjinzei', body)
