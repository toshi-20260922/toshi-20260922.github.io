# /hensai/ 借入の返済の計算(元金均等・元利均等・据置・借りる年月・1年ごとの表・毎月の返済予定表)。
# 原本:
# 日本政策金融公庫「金利情報 小規模事業者/個人事業主の方【国民生活事業】」(令和8年11月2日現在。無担保・税務申告を2期終えていない方の基準利率 3.75〜5.15%)
#   https://www.jfc.go.jp/n/rate/index.html
# 日本政策金融公庫「新規開業・スタートアップ支援資金」(設備資金20年以内・運転資金10年以内・どちらも「うち据置期間5年以内」)
#   https://www.jfc.go.jp/n/finance/search/01_sinkikaigyou_m.html
# 日本政策金融公庫「小規模事業者/個人事業主の方【国民生活事業】」(ご返済は原則として月賦払い。元金均等返済・元利均等返済・ステップ(段階)返済など)
#   https://www.jfc.go.jp/n/finance/flow/goriyou.html
# 日本政策金融公庫「返済シミュレーション(事業資金用)」(試算は目安。借入日・金額・返済期間・金利等の条件で実際の返済額と異なる場合がある)
#   https://www.jfc.go.jp/n/finance/simulation.html
# 国税庁 No.2606 金銭を貸し付けたとき(令和8年4月1日現在法令等。令和8年中の貸付け1.3%・令和4〜7年0.9%・令和3年1.0%。
#   借り入れて貸したときはその借入金の利率。差額が1年で5,000円以下は課税しない)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2606.htm
# 国税庁 No.2210 必要経費の知識(業務のための借入金の利息は必要経費になる)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2210.htm
# 国税庁 確定申告書等作成コーナー「借入金利子」(借入金の返済額のうち元本に相当する部分の金額は必要経費にならない)
#   https://www.keisan.nta.go.jp/r7yokuaru_sp/socat3/socat33/scid095.html
# 確認できなかったこと:公庫(国民生活事業)の利息が日割りかどうか・円未満の端数の扱い。公庫のページに書かれていない。
#   このページの端数は「利息=残っている元金×年利÷12の1円未満切り捨て」「元金均等の毎回の元金=借りる額÷回数の1円未満切り捨て」
#   「元利均等の毎回の返済額=式の額を1円の位に四捨五入」「最後の回で残りを全部返す」という、ページが自分で決めて画面に書いている決まり。
# 照らすもの:自分で書いた式(分数)と、結果の箱の3つの数字・箱の4行の文・1年ごとの表の全行・毎月の返済予定表の全行・返す月の年月。
#   借りる額10通り×年利9通り×期間6通り×据置5通り×返し方2通り。HTML に手で書いた表(役員への貸付の利率)・箱に直に書いた既定の数字・よくある質問の数字・本文の数字。
# 2026-11-20 に見つけたページの誤り:年利を小数のまま掛けて切り捨てていた(500万円×3.75%÷12=15,625円が15,624円と出た)。整数で掛けて割る形に直した。
#   見出し「据置期間とは」と据置の入力欄の id がどちらも sue で、目次から入力欄へ飛んでいた。入力欄を suem にした。箱に直に書いた既定の結果が0円だった。
# 2026-11-21:1年ごとの表(#tb)が HTML では空で、JS が動くまで早見表に行が無かった。既定の条件の7行を HTML に直に書いた(突き合わせは下の「元の文 tb」)。
#   この日は係が原本を開けなかった(web-fetch を呼べない)。公庫の基準利率の日付(令和8年11月2日現在)と No.2606 は 11-20 に確かめた値のまま。
# 最後に原本を確かめた日:2026-11-21(公庫「金利情報」だけ本文で読んだ。令和8年11月2日現在・無担保の基準利率3.95〜5.35%と3.75〜5.15%・有担保2.95〜4.95%。ほかの原本は11-20のまま)
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from _lib import run

_pw = {}
def ganri(P, i, N):
    """元利均等の毎回の返済額(分数)。P×i×(1+i)^N ÷ ((1+i)^N − 1)。金利0なら P÷N。"""
    if i == 0:
        return Fraction(P, N)
    key = (i, N)
    if key not in _pw:
        _pw[key] = (1 + i) ** N
    q = _pw[key]
    return P * i * q / (q - 1)

def ref(P, rate, Y, S, m):
    """rate は年利(%)の文字。Y 年・据置 S か月・m=0 元金均等 / 1 元利均等。返すのは月ごとの (元金, 利息, 残り)。"""
    i = Fraction(rate) / 100 / 12
    T = Y * 12; N = T - S
    kin = P // N                                             # 元金均等:毎回の元金(1円未満切り捨て)
    A = (ganri(P, i, N) + Fraction(1, 2)).__floor__()        # 元利均等:毎回の返済額(1円の位に四捨五入)
    bal = P; mon = []
    for k in range(1, T + 1):
        it = (bal * i).__floor__()                           # 利息:残っている元金×年利÷12(1円未満切り捨て)
        if k <= S:
            pr = 0
        elif k == T:
            pr = bal                                         # 最後の回で残りを全部返す
        else:
            pr = min(kin if m == 0 else A - it, bal)          # 元金は残りを超えない(ごく小さい額で四捨五入の分が積もったとき)
        bal -= pr
        mon.append((pr, it, bal))
    return {'mon': mon, 'N': N, 'kin': kin, 'sue': (P * i).__floor__(),
            'first': mon[S][0] + mon[S][1], 'tot': sum(x[1] for x in mon)}

def c(v):
    return '{:,}'.format(v)

SET = """([P,r,Y,S,m,y0,m0])=>{
  function put(id,v){document.getElementById(id).value=String(v);}
  put('amt',P);put('rate',r);put('yr',Y);put('suem',S);put('ky',y0);put('km',m0);
  document.querySelector('#s-m button[data-v="'+m+'"]').click();   // ボタンを押すと1回だけ計算し直す(手で入力する道筋は下で別に見る)
  function t(id){return document.getElementById(id).textContent}
  function rows(id){return [...document.querySelectorAll('#'+id+' tr')].map(function(tr){return [...tr.children].map(function(td){return td.textContent})})}
  return {a:t('o-a'),ae:t('o-ae'),b:t('o-b'),c:t('o-c'),l1:t('o-1'),l2:t('o-2'),l3:t('o-3'),tb:rows('tb'),tbm:rows('tbm'),
          on:[...document.querySelectorAll('#s-m button.on')].map(function(b){return b.textContent})};
}"""

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1
            if bad <= 60:
                print('NG', label, str(got)[:160], '|', str(want)[:160])

    def want_of(P, rate, Y, S, m, y0, m0):
        e = ref(P, rate, Y, S, m); mon = e['mon']
        tbm = []
        for k, (pr, it, bal) in enumerate(mon, 1):
            idx = y0 * 12 + (m0 - 1) + k                     # 返済は借りた月の翌月から
            tbm.append([str(k), '%d年%d月' % (idx // 12, idx % 12 + 1), c(pr + it), c(pr), c(it), c(bal)])
        tb = []
        for y in range(Y):
            seg = mon[y * 12:(y + 1) * 12]
            tb.append([str(y + 1), c(sum(x[0] for x in seg)), c(sum(x[1] for x in seg)), c(seg[-1][2])])
        last = y0 * 12 + (m0 - 1) + Y * 12
        return e, {
            'a': c(e['first']) + '円', 'ae': '据置のあと' if S else '1回目',
            'b': c(e['tot']) + '円', 'c': c(P + e['tot']) + '円',
            'l1': '据置の%dか月は、毎月%s円の利息だけを払います' % (S, c(e['sue'])) if S else '据置はなく、1か月目から元金を返します',
            'l2': ('元金と利息を合わせて、毎月ほぼ同じ額を%d回で返します' % e['N']) if m else ('元金は毎月%s円ずつ、%d回で返します' % (c(e['kin']), e['N'])),
            'l3': '最後の返済は%d年%d月です' % (last // 12, last % 12 + 1),
            'tb': tb, 'tbm': tbm, 'on': ['元利均等' if m else '元金均等']}

    PS = [0, 1, 999, 1000000, 3000000, 5000000, 7770000, 12345678, 30000000, 100000000]
    RS = ['0', '0.05', '0.5', '1.3', '2.05', '3.75', '5.15', '9.95', '15']
    YS = [3, 5, 7, 10, 15, 20]
    SS = [0, 3, 6, 12, 24]
    j = 0
    for P in PS:
        for rate in RS:
            for Y in YS:
                for S in SS:
                    for m in (0, 1):
                        j += 1
                        y0 = 2025 + j % 4; m0 = j % 12 + 1
                        e, want = want_of(P, rate, Y, S, m, y0, m0)
                        got = await pg.evaluate(SET, [P, rate, Y, S, m, y0, m0])
                        tag = '%d %s%% %d年 据置%d %s' % (P, rate, Y, S, '元利' if m else '元金')
                        for k in ('a', 'ae', 'b', 'c', 'l1', 'l2', 'l3', 'on'):
                            chk(tag + ' ' + k, got[k], want[k])
                        chk(tag + ' 1年ごとの表', got['tb'], want['tb'])
                        chk(tag + ' 毎月の表', got['tbm'], want['tbm'])
                        # 式そのものの確かめ(ページと関わりなく成り立つはずのこと)
                        mon = e['mon']
                        chk(tag + ' 元金の合計=借りた額', (sum(x[0] for x in mon), mon[-1][2]), (P, 0))
                        chk(tag + ' 元金が負でない', min(x[0] for x in mon) >= 0, True)
                        if m == 1 and e['N'] > 1 and P >= 1000000:      # 1,000円に満たないような額は四捨五入の分で先に返し終わるので除く
                            # 元利均等:最後の回を除いて毎回の返済額が同じ
                            pays = [x[0] + x[1] for x in mon[S:-1]]
                            chk(tag + ' 毎回が同じ額', len(set(pays)), 1)
                            # 最後の回の調整は、毎回の丸め(四捨五入0.5円+利息の切り捨て1円)に利息が付いて積もった分まで
                            i_ = Fraction(rate) / 1200
                            lim = Fraction(3, 2) * (((1 + i_) ** e['N'] - 1) / i_ if i_ else e['N'])
                            chk(tag + ' 最後の回の調整の幅', abs(mon[-1][0] + mon[-1][1] - pays[0]) <= lim, True)
                        if m == 0 and e['N'] > 1:
                            chk(tag + ' 最後の回の元金の調整', 0 <= mon[-1][0] - e['kin'] < e['N'], True)

    # 小数の誤差が出やすい所:残り×年利÷12 がちょうど整数になる組み合わせ(切り捨てで1円減らないこと)
    for P, rate in [(5000000, '3.75'), (8000000, '3.75'), (2400000, '5.15'), (24000000, '2.05'), (12000000, '1.3'),
                    (6000000, '0.9'), (2400000, '4.35'), (9600000, '2.35'), (4800000, '5.35'), (2400000, '3.95')]:
        i = Fraction(rate) / 1200
        chk('割り切れる組み合わせ %d %s' % (P, rate), (P * i).denominator, 1)
        got = await pg.evaluate(SET, [P, rate, 7, 6, 0, 2026, 12])
        chk('据置の利息 %d %s' % (P, rate), got['l1'], '据置の6か月は、毎月%s円の利息だけを払います' % c(int(P * i)))

    # 画面を人が触る道筋(入力欄に打つ・選ぶ・ボタンを押す・つまみを動かす)
    await pg.reload()
    D = (5000000, '3.75', 7, 6, 0, 2026, 12)
    e0, w0 = want_of(*D)
    for k, sel in (('a', '#o-a'), ('b', '#o-b'), ('c', '#o-c'), ('l1', '#o-1'), ('l2', '#o-2'), ('l3', '#o-3'), ('ae', '#o-ae')):
        chk('既定の画面 ' + k, (await pg.text_content(sel)), w0[k])
    chk('既定の画面 1年ごとの表', await pg.eval_on_selector_all('#tb tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))"), w0['tb'])
    chk('既定の画面 毎月の表', await pg.eval_on_selector_all('#tbm tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))"), w0['tbm'])
    for P, rate, Y, S, m, y0, m0 in [(3000000, '2.35', 5, 0, 1, 2025, 1), (10000000, '5.15', 10, 12, 0, 2027, 6),
                                     (72000000, '4.95', 20, 24, 1, 2028, 11), (1500000, '3.75', 3, 3, 1, 2026, 12)]:
        await pg.fill('#amt', str(P)); await pg.fill('#rate', rate)
        await pg.select_option('#yr', str(Y)); await pg.select_option('#suem', str(S))
        await pg.select_option('#ky', str(y0)); await pg.select_option('#km', str(m0))
        await pg.click('#s-m button[data-v="%d"]' % m)
        e, want = want_of(P, rate, Y, S, m, y0, m0)
        tag = '手で入力 %d %s' % (P, rate)
        chk(tag + ' 入力欄の表示', await pg.evaluate("()=>Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').get.call(document.getElementById('amt'))"), c(P))
        for k, sel in (('a', '#o-a'), ('b', '#o-b'), ('c', '#o-c'), ('l1', '#o-1'), ('l2', '#o-2'), ('l3', '#o-3')):
            chk(tag + ' ' + k, (await pg.text_content(sel)), want[k])
        chk(tag + ' 1年ごとの表', await pg.eval_on_selector_all('#tb tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))"), want['tb'])
        chk(tag + ' 毎月の表', await pg.eval_on_selector_all('#tbm tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))"), want['tbm'])
    # つまみ(100万〜3,000万円)
    await pg.evaluate("()=>{var e=document.getElementById('amtr');e.value='20000000';e.dispatchEvent(new Event('input',{bubbles:true}));}")
    e, want = want_of(20000000, '3.75', 3, 3, 1, 2026, 12)
    chk('つまみ 利息の合計', await pg.text_content('#o-b'), want['b'])
    chk('つまみ 入力欄', await pg.evaluate("()=>document.getElementById('amt').value"), '20000000')

    # 表の見出し・選択肢・id の重なり・目次
    await pg.reload()
    chk('1年ごとの表の見出し', await pg.eval_on_selector_all(':is(#list ~ .tw):not(#list ~ .tw ~ .tw) thead th', "hs=>hs.map(h=>h.innerText.replace(/\\s+/g,''))"),
        ['年目', '返した元金（円）', '払った利息（円）', '年の終わりの残り（円）'])
    chk('毎月の表の見出し', await pg.eval_on_selector_all(':is(#tsuki ~ .tw):not(#tsuki ~ .tw ~ .tw) thead th', "hs=>hs.map(h=>h.innerText.replace(/\\s+/g,''))"),
        ['回', '返す月', '返済額（円）', 'うち元金（円）', 'うち利息（円）', '返したあとの残り（円）'])
    chk('期間の選択肢', await pg.eval_on_selector_all('#yr option', 'os=>os.map(o=>[o.value,o.textContent])'), [[str(y), '%d年' % y] for y in YS])
    chk('据置の選択肢', await pg.eval_on_selector_all('#suem option', 'os=>os.map(o=>[o.value,o.textContent])'),
        [['0', 'なし'], ['3', '3か月'], ['6', '6か月'], ['12', '1年'], ['24', '2年']])
    chk('据置は期間より短い', max(SS) < min(YS) * 12, True)
    chk('公庫の期間と据置の上限(設備20年・据置5年)の中', (max(YS) <= 20, max(SS) <= 60), (True, True))
    chk('借りる月の選択肢', await pg.eval_on_selector_all('#km option', 'os=>os.map(o=>[o.value,o.textContent])'), [[str(x), '%d月' % x] for x in range(1, 13)])
    ids = await pg.eval_on_selector_all('[id]', 'es=>es.map(e=>e.id)')
    chk('id の重なり', sorted(set(i for i in ids if ids.count(i) > 1)), [])
    chk('目次の行き先', await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>{var e=document.getElementById(a.getAttribute('href').slice(1));return !!e&&e.tagName==='H2'&&e.innerText.replace(/\\s+/g,'')===a.textContent.replace(/\\s+/g,'')})"), [True] * 8)

    # HTML に手で書いた表:会社が自分のお金を貸す場合の利率(国税庁 No.2606)
    NTA2606 = [('2026年（令和8年）', Fraction(13, 10)), ('2022年〜2025年（令和4年〜令和7年）', Fraction(9, 10)), ('2021年（令和3年）', Fraction(1))]
    rows = await pg.eval_on_selector_all(':is(#yakuin ~ .tw):not(#yakuin ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    chk('No.2606 の表', rows, [[a, '%d.%d%%' % (f * 10 // 10, f * 10 % 10)] for a, f in NTA2606])
    for a, _ in NTA2606:                                      # 西暦と令和の年の対応
        ys = [int(x) for x in re.findall(r'(\d{4})年', a)]; rs = [int(x) for x in re.findall(r'令和(\d+)年', a)]
        chk('西暦と令和 ' + a, [y - 2018 for y in ys], rs)

    # 本文・よくある質問・箱に直に書いた既定の数字(ファイルの中身)
    flat = ''.join((await pg.inner_text('main')).split())
    def oku(v, unit):                                         # およその書き方(千円・万円の位に四捨五入)
        return (Fraction(v, unit) + Fraction(1, 2)).__floor__()
    s = oku(e0['sue'], 1000)
    for label, want in [
        ('よくある質問 500万円', '年3.75%%・据置6か月・元金均等なら、据置の間は毎月およそ%d万%d千円の利息だけです。そのあと最初の月の返済はおよそ%d万円です。利息の合計はおよそ%d万円です。'
            % (s // 10, s % 10, oku(e0['first'], 10000), oku(e0['tot'], 10000))),
        ('基準利率', '日本政策金融公庫の基準利率は令和8年11月2日現在で、無担保で申告が2期未満の場合に年3.75%から5.15%です。'),
        ('期間', '日本政策金融公庫の新規開業・スタートアップ支援資金は、設備資金が20年以内・運転資金が10年以内です。どちらも据置期間はこの中の5年以内です。'),
        ('5,000円', '1年の差額が5,000円以下なら課税されないなどの例外があります。'),
        ('利息の切り捨て', '利息は、残っている元金に年利の12分の1をかけて1円未満を切り捨てています'),
        ('回数の注', '返済の回数は、返す期間の月数から据置の月数を引いた回数です。'),
        ('返し方の種類', '元金均等返済・元利均等返済・ステップ（段階）返済などがあります。'),
        ('更新日', '更新日：2026年11月21日（日本政策金融公庫の令和8年11月2日現在の基準利率）'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('年利の既定は基準利率の下の端', await pg.evaluate("()=>document.getElementById('rate').getAttribute('value')"), '3.75')
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'hensai', 'index.html'), encoding='utf-8').read()
    for label, want in [
        ('o-a', '<b id="o-a">%s<i>円</i></b><em id="o-ae">据置のあと</em>' % c(e0['first'])),
        ('o-b', '<b id="o-b">%s<i>円</i></b>' % c(e0['tot'])),
        ('o-c', '<b id="o-c">%s<i>円</i></b>' % c(5000000 + e0['tot'])),
        ('o-1', '<li id="o-1">%s</li>' % w0['l1']),
        ('o-2', '<li id="o-2">%s</li>' % w0['l2']),
        ('o-3', '<li id="o-3">%s</li>' % w0['l3']),
        ('tb', '<tbody id="tb">' + ''.join('<tr><td class="c">%d</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (k + 1, c(sum(x[0] for x in e0['mon'][k*12:k*12+12])), c(sum(x[1] for x in e0['mon'][k*12:k*12+12])), c(e0['mon'][k*12+11][2])) for k in range(7)) + '</tbody>'),
        ('既定の借りる額', 'id="amt" inputmode="numeric" min="0" max="100000000" step="100000" value="5000000"'),
        ('既定の期間', '<option value="7" selected'),
        ('既定の据置', '<option value="6" selected'),
        ('既定の返し方', '<button type="button" class="on" data-v="0">元金均等</button>'),
        ('既定の借りる年', '<option value="2026" selected'),
        ('既定の借りる月', '<option value="12" selected'),
    ]:
        chk('元の文 ' + label, want in raw, True)
    return n, bad
run('hensai', body)
