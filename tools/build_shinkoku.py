# 確定申告シミュレーション /kakutei-shinkoku-keisan/ を作る。2026/11/21。
# 数字は前に原本で確かめたページと同じ式を使う:
#  給与所得・基礎控除(令和8年分) … /shotoku-kingaku/ /nenmatsu-chosei/(国税庁 2026kaisei.pdf)
#  速算表・復興特別所得税(基準所得税額×2.1%) … /shotokuzei/ /nenmatsu-chosei/
#  配偶者控除38・26・13万円・扶養控除38万円・特定扶養63万円・生命保険料と地震保険料の上限 … /nenmatsu-chosei/ /gakusei-kabe/
#  医療費控除(10万円か総所得金額等の5%・上限200万円) … /iryohi-kojo/
#  寄附金控除(総所得金額等の40%まで・2,000円を引く) … 国税庁 No.1150
#  申告納税額の100円未満切捨て … 国税通則法119条
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_saitei as B

c = B.c; td = B.td; table = B.table

def kyuyo(x):
    if x < 741000: return 0
    if x < 2191000: return x - 740000
    if x < 2193000: return 1451000
    if x < 2196000: return 1453000
    if x < 2200000: return 1456000
    if x < 6600000:
        a = x // 4000 * 4000
        return a * 7 // 10 - 80000 if x < 3600000 else a * 8 // 10 - 440000
    if x < 8500000: return x * 9 // 10 - 1100000
    return x - 1950000

def kiso(t):
    for lim, v in [(4890000, 1040000), (6550000, 670000), (23500000, 620000), (24000000, 480000), (24500000, 320000), (25000000, 160000)]:
        if t <= lim: return v
    return 0

def haigu(t):
    return 380000 if t <= 9000000 else 260000 if t <= 9500000 else 130000 if t <= 10000000 else 0

ZT = [(1950000, 5, 0), (3300000, 10, 97500), (6950000, 20, 427500), (9000000, 23, 636000), (18000000, 33, 1536000), (40000000, 40, 2796000)]
def zei(k):
    for lim, r, d in ZT:
        if k <= lim: return k * r // 100 - d
    return k * 45 // 100 - 4796000

def rate(k):
    for lim, r, d in ZT:
        if k <= lim: return r
    return 45

def calc(q, wq, jo, wj, sha, ide, sei, iryo, kifu, hg, fu, tf, loan):
    g = kyuyo(q)
    tot = g + jo
    ki = kiso(tot)
    hk = haigu(tot) if hg else 0
    iryd = min(2000000, max(0, iryo - min(100000, tot * 5 // 100)))
    kfd = max(0, min(kifu, tot * 40 // 100) - 2000)
    koj = sha + ide + min(sei, 170000) + iryd + kfd + hk + 380000 * fu + 630000 * tf + ki
    kz = max(0, tot - koj) // 1000 * 1000
    san = zei(kz)
    kij = max(0, san - loan)
    fk = kij * 21 // 1000
    tz = kij + fk
    d = tz - wq - wj
    pay = d // 100 * 100 if d > 0 else 0
    ref = -d if d < 0 else 0
    return dict(g=g, tot=tot, ki=ki, hk=hk, iryd=iryd, kfd=kfd, koj=koj, kz=kz, san=san, kij=kij, fk=fk, tz=tz, pay=pay, ref=ref, rt=rate(kz))

def nencho(q, sha):
    # 年末調整で引かれた1年分(配偶者・扶養なし・社会保険料と基礎控除だけ)
    return calc(q, 0, 0, 0, sha, 0, 0, 0, 0, 0, 0, 0, 0)['tz']

slug = 'kakutei-shinkoku-keisan'; cta = 'shinkoku'
title = '【確定申告シミュレーション】所得税はいくら戻る？いくら納める？【令和8年分】'
desc = '給与と源泉徴収税額・副業や事業の所得・医療費・ふるさと納税・社会保険料を入力すると、令和8年分の確定申告で戻る所得税と納める所得税が分かります。医療費30万円とふるさと納税で年収ごとにいくら戻るかの早見表付きです。'
upd = '更新日：2026年11月21日（国税庁 令和8年分の給与所得控除・基礎控除・税率）'

# ---- 早見表 ----
NEN = [300, 400, 500, 600, 700, 800, 1000]
def sha15(q):
    return q * 15 // 100
rows = []
for m in NEN:
    q = m * 10000; sh = sha15(q); w = nencho(q, sh)
    r0 = calc(q, w, 0, 0, sh, 0, 0, 0, 0, 0, 0, 0, 0)
    r1 = calc(q, w, 0, 0, sh, 0, 0, 300000, 0, 0, 0, 0, 0)
    r2 = calc(q, w, 0, 0, sh, 0, 0, 0, 50000, 0, 0, 0, 0)
    assert r0['ref'] == 0 and r0['pay'] == 0
    rows.append([td('%s万円' % c(m)), td('%d%%' % r0['rt']), td(c(w)), td(c(r1['ref'])), td(c(r2['ref']))])
HY_ROWS = rows
sec1 = ('<h2 id="hayami">確定申告で戻る所得税の早見表</h2>\n'
        '<p>会社員が医療費控除やふるさと納税で確定申告をすると、年末調整で引かれた所得税の一部が戻ります。戻る額は、控除の額に本人の所得税率と1.021を掛けた額がおおよその目安です。</p>\n'
        '<p class="cap">令和8年分・独身の会社員（年末調整済み）が申告した場合</p>\n'
        + table(['年収', '所得税率', '年末調整で<br>引かれた所得税<br>（円）', '医療費30万円<br>で戻る額<br>（円）', 'ふるさと納税<br>5万円で戻る額<br>（円）'], rows)
        + '<p class="note" style="margin-top:8px">社会保険料は年収の15%として計算しています。医療費は保険金などで補塡される額を引いた後の額です。ふるさと納税は所得税から戻る額だけで、住民税から引かれる額は含めていません。ワンストップ特例を使うと所得税からは戻らず、その分も住民税から引かれます。</p>\n')

# ---- 計算の箱 ----
D = dict(q=5000000, wq=0, jo=0, wj=0, sha=750000, ide=0, sei=0, iryo=300000, kifu=0, hg=0, fu=0, tf=0, loan=0)
D['wq'] = nencho(D['q'], D['sha'])
R = calc(**D)

def inp(i, lab, v, mx=10000000000):
    return ('   <label for="%s">%s</label>\n   <div class="row"><input type="number" id="%s" inputmode="numeric" min="0" max="%d" step="1" value="%d"><span>円</span></div>\n' % (i, lab, i, mx, v))

calc_html = ('<div class="sum" id="calc">\n <div class="h"><span>結論</span>1年分の所得税と引かれた源泉徴収税額の差が、戻る額か納める額です</div>\n <div class="in">\n'
  '  <div class="full">\n' + inp('q', '給与の収入（源泉徴収票の「支払金額」）', D['q']) + inp('wq', '給与から引かれた所得税（源泉徴収票の「源泉徴収税額」）', D['wq']) + '  </div>\n'
  '  <div class="full">\n' + inp('jo', '給与以外の所得（副業・事業の売上から経費を引いた額）', D['jo']) + inp('wj', '報酬から引かれた所得税（支払調書の源泉徴収税額）', D['wj']) + '  </div>\n'
  '  <div class="full">\n' + inp('sha', '社会保険料（給与から引かれた額と国民年金・国民健康保険の合計）', D['sha']) + inp('ide', 'iDeCo・小規模企業共済の掛金（1年の合計）', D['ide']) + inp('sei', '生命保険料・地震保険料の控除額（合計で最大17万円）', D['sei'], 170000) + '  </div>\n'
  '  <div class="full">\n' + inp('iryo', '1年に払った医療費（保険金などで補塡される額を引いた額）', D['iryo']) + inp('kifu', 'ふるさと納税などの寄附額（ワンストップ特例を使わない分）', D['kifu']) + inp('loan', '住宅ローン控除の額（税額から引く額）', D['loan']) + '  </div>\n'
  '  <div class="full">\n   <label>配偶者控除（配偶者の合計所得金額が62万円以下）</label>\n   <div class="seg" id="s-hg"><button type="button" class="on" data-v="0">なし</button><button type="button" data-v="1">あり</button></div>\n'
  '   <label for="fu">扶養している16歳以上の家族（19〜22歳を除く）</label>\n   <select id="fu"><option value="0">0人</option><option value="1">1人</option><option value="2">2人</option><option value="3">3人</option></select>\n'
  '   <label for="tf">扶養している19〜22歳の子（特定扶養親族）</label>\n   <select id="tf"><option value="0">0人</option><option value="1">1人</option><option value="2">2人</option></select>\n  </div>\n'
  ' </div>\n'
  ' <div class="vd" id="vd"><b id="o-vd">確定申告で%s円が戻ります</b><span id="o-vds">1年分の所得税%s円に対して、源泉徴収で%s円が引かれています</span></div>\n'
  ' <div class="amt jdg">\n  <div><small id="o-al">戻る所得税</small><b id="o-a">%s<i>円</i></b><em>復興特別所得税を含む</em></div>\n  <div><small>1年分の所得税</small><b id="o-t">%s<i>円</i></b><em>税率%d%%</em></div>\n </div>\n'
  ' <ul>\n  <li id="o-br">合計所得金額%s円・所得控除の合計%s円・課税所得%s円</li>\n  <li id="o-ko">医療費控除%s円・寄附金控除%s円・基礎控除%s円</li>\n  <li id="o-nd">給与以外の所得が20万円以下なので、医療費控除などを受けないなら確定申告はしなくてもかまいません</li>\n'
  '  <li>住民税は含めていません。申告した内容は市区町村に送られ、翌年度の住民税にも反映されます</li>\n </ul>\n</div>\n') % (
    c(R['ref']), c(R['tz']), c(D['wq']), c(R['ref']), c(R['tz']), R['rt'], c(R['tot']), c(R['koj']), c(R['kz']), c(R['iryd']), c(R['kfd']), c(R['ki']))

intro = ('<p>確定申告では、所得から所得控除を引いた課税所得に税率を掛けて1年分の所得税を出します。その額をすでに引かれた源泉徴収税額と比べます。<span class="mk">引かれた額の方が多ければ差額が戻り、少なければ差額を納めます。</span>令和8年分は基礎控除が最大104万円になり、給与所得控除の最低額は74万円です。</p>\n')

toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#hayami">確定申告で戻る所得税の早見表</a></li>
  <li><a href="#nagare">戻る額と納める額の計算の流れ</a></li>
  <li><a href="#rei">戻る人と納める人の例</a></li>
  <li><a href="#kojo">確定申告で受けられる主な控除</a></li>
  <li><a href="#hasu">端数の決まり</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">確定申告の計算でよく聞かれること</a></li>
 </ol>
</nav>
'''

sec2 = ('<h2 id="nagare">戻る額と納める額の計算の流れ</h2>\n'
        '<ol>\n <li>給与の収入から給与所得控除を引いて給与所得を出します。副業や事業の所得を足すと合計所得金額です</li>\n'
        ' <li>社会保険料・医療費控除・寄附金控除・配偶者控除・扶養控除・基礎控除などの所得控除を引きます。1,000円未満は切り捨てて課税所得にします</li>\n'
        ' <li>課税所得に税率を掛けて控除額を引くと所得税です。住宅ローン控除はこの所得税から引きます</li>\n'
        ' <li>残った所得税に2.1%の復興特別所得税を足すと、1年分の所得税です</li>\n'
        ' <li>給与や報酬から引かれた源泉徴収税額との差が、戻る額か納める額です</li>\n</ol>\n'
        '<p class="cap">令和8年分・所得税の速算表</p>\n'
        + table(['課税所得', '税率', '控除額'], [
            [td('195万円以下'), td('5%'), td('0円')],
            [td('195万円超330万円以下'), td('10%'), td('97,500円')],
            [td('330万円超695万円以下'), td('20%'), td('427,500円')],
            [td('695万円超900万円以下'), td('23%'), td('636,000円')],
            [td('900万円超1,800万円以下'), td('33%'), td('1,536,000円')],
            [td('1,800万円超4,000万円以下'), td('40%'), td('2,796,000円')],
            [td('4,000万円超'), td('45%'), td('4,796,000円')]])
        + '<p class="note" style="margin-top:8px">195万円ちょうどの人は5%です。基礎控除は合計所得金額489万円以下なら104万円で、655万円以下は67万円・2,350万円以下は62万円です。</p>\n')

# 例
EX = [
    ('会社員・医療費40万円', dict(q=4000000, jo=0, wj=0, sha=600000, ide=0, sei=0, iryo=400000, kifu=0, hg=0, fu=0, tf=0, loan=0)),
    ('会社員・ふるさと納税10万円', dict(q=7000000, jo=0, wj=0, sha=1050000, ide=0, sei=0, iryo=0, kifu=100000, hg=0, fu=0, tf=0, loan=0)),
    ('会社員・副業の所得50万円', dict(q=5000000, jo=500000, wj=0, sha=750000, ide=0, sei=0, iryo=0, kifu=0, hg=0, fu=0, tf=0, loan=0)),
    ('フリーランス・報酬300万円', dict(q=0, jo=2000000, wj=306300, sha=400000, ide=0, sei=0, iryo=0, kifu=0, hg=0, fu=0, tf=0, loan=0)),
]
rows = []
EXR = []
for lab, a in EX:
    w = nencho(a['q'], a['sha']) if a['q'] else 0
    r = calc(q=a['q'], wq=w, **{k: v for k, v in a.items() if k != 'q'})
    EXR.append((lab, a, w, r))
    res = ('戻る %s円' % c(r['ref'])) if r['ref'] else ('納める %s円' % c(r['pay']))
    rows.append([td(lab, 'l'), td(c(r['tz'])), td(c(w + a['wj'])), td(res)])
sec3 = ('<h2 id="rei">戻る人と納める人の例</h2>\n<p>よくある4つの例を、この計算で出しました。独身で配偶者や扶養の家族がいない場合です。</p>\n'
        '<p class="cap">令和8年分・独身の場合</p>\n'
        + table(['例', '1年分の<br>所得税（円）', '引かれた<br>所得税（円）', '確定申告'], rows)
        + '<p class="note" style="margin-top:8px">会社員の社会保険料は年収の15%として計算しています。会社員の「引かれた所得税」は年末調整で決まった額です。フリーランスの例は、1回100万円以下の報酬の合計が300万円で10.21%の306,300円が引かれた場合です。経費を引いた所得は200万円で、社会保険料（国民年金と国民健康保険）は40万円としています。</p>\n')

sec4 = ('<h2 id="kojo">確定申告で受けられる主な控除</h2>\n'
        '<ul>\n <li>医療費控除：1年の医療費から10万円（総所得金額等が200万円未満の人はその5%）を引いた額です。上限は200万円です</li>\n'
        ' <li>寄附金控除：ふるさと納税などの寄附額から2,000円を引いた額です。総所得金額等の40%が上限です</li>\n'
        ' <li>住宅ローン控除の1年目：2年目からは年末調整で受けられます</li>\n'
        ' <li>雑損控除：災害や盗難で住宅や家財に損害を受けた場合です</li>\n</ul>\n'
        '<p>国民年金・国民健康保険の保険料や、iDeCoの掛金を年末調整で出していない人も確定申告で控除できます。配偶者特別控除・老人扶養親族・障害者控除・寡婦控除などは、この計算に含めていません。</p>\n')

sec5 = ('<h2 id="hasu">端数の決まり</h2>\n'
        '<ul>\n <li>課税所得は1,000円未満を切り捨てます</li>\n'
        ' <li>復興特別所得税は住宅ローン控除などを引いた後の所得税（基準所得税額）の2.1%で、1円未満を切り捨てます</li>\n'
        ' <li>納める額は100円未満を切り捨てます。戻る額は1円単位です</li>\n</ul>\n')

rel_items = [
    ('iryohi-kojo', '医療費控除の計算', '医療費控除で戻る所得税と住民税を、年収と医療費から出せます。'),
    ('furusato', 'ふるさと納税の限度額の計算', '自己負担2,000円で済む寄附の上限を、年収と家族から出せます。'),
    ('fukugyo', '副業の税金の計算', '副業の所得が20万円を超えたら確定申告が要るかを判定できます。'),
    ('nenmatsu-chosei', '年末調整の還付金の計算', '会社員の年末調整で戻る所得税の目安が分かります。'),
    ('shotoku-kingaku', '所得金額の計算', '給与・年金・事業の収入から合計所得金額を出せます。'),
    ('shotokuzei', '所得税の計算', '年収ごとの所得税と税率を早見表で確かめられます。'),
    ('kojin-zei', '個人事業主の手取りの早見表', '事業の利益から税金と国民健康保険を引いた手取りが分かります。'),
    ('gensen-hoshu', '源泉徴収の早見表', '報酬から引かれる10.21%の源泉徴収税額を確かめられます。'),
    ('kakutei-shinkoku', '確定申告の期限の早見表', '令和8年分の確定申告は、令和9年2月16日から3月15日です。'),
    ('juminzei', '住民税の早見表', '確定申告の内容は、翌年度の住民税にも反映されます。'),
    ('taishokukin', '退職金の税金の計算', '退職所得の受給に関する申告書を出していない人は、確定申告で精算します。'),
]
sec6 = B.rel(slug, rel_items)

qa = ('<h2 id="qa">確定申告の計算でよく聞かれること</h2>\n'
      '<h3>会社員でも確定申告で税金は戻りますか？</h3>\n<p>医療費控除やふるさと納税（ワンストップ特例を使わない分）・住宅ローン控除の1年目は、年末調整では受けられません。確定申告をすると、引かれた所得税の一部が戻ります。年収500万円で医療費30万円なら%s円が戻ります。</p>\n'
      '<h3>戻る額はどのくらいが目安ですか？</h3>\n<p>控除が増えた額に本人の所得税率を掛け、1.021倍した額が目安です。税率10%%の人が医療費控除20万円を受けると、約2万円が戻ります。</p>\n'
      '<h3>副業の所得があると納める額はいくらですか？</h3>\n<p>副業の所得に本人の税率を掛けた額がおおよその目安です。年収500万円の会社員で副業の所得が50万円なら、%s円を納めます。</p>\n'
      '<h3>フリーランスの源泉徴収された報酬は戻りますか？</h3>\n<p>報酬から引かれた10.21%%は所得税の前払いです。経費や控除を引いた1年分の所得税より多く引かれていれば、差額が戻ります。</p>\n'
      '<h3>確定申告はいつまでですか？</h3>\n<p>令和8年分は令和9年2月16日から3月15日までです。税金が戻るだけの還付申告は、翌年1月1日から5年間出せます。</p>\n') % (c(R['ref']), c(EXR[2][3]['pay']))

src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/publication/pamph/gensen/2026kaisei.pdf">国税庁「令和8年度税制改正による所得税の基礎控除の引上げ、給与所得控除の最低保障額の引上げ等について」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm">国税庁 タックスアンサー No.2260 所得税の税率</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1120.htm">国税庁 タックスアンサー No.1120 医療費を支払ったとき（医療費控除）</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1150.htm">国税庁 タックスアンサー No.1150 一定の寄附金を支払ったとき（寄附金控除）</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1191.htm">国税庁 タックスアンサー No.1191 配偶者控除</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1180.htm">国税庁 タックスアンサー No.1180 扶養控除</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1900.htm">国税庁 タックスアンサー No.1900 給与所得者で確定申告が必要な人</a></li>
  <li>所得税法第73条・第78条・第83条・第84条・第89条／復興財源確保法第13条／国税通則法第119条</li>
 </ul>
</div>
'''

JS = r'''(function(){
 var $=function(i){return document.getElementById(i)},hg=0;
 function f(n){return Math.round(n).toLocaleString("ja-JP");}
 function num(i){var v=parseInt(String($(i).value).replace(/[^0-9]/g,""),10);return isNaN(v)?0:v;}
 function fl(a,b){return (a-a%b)/b;}
 function kyuyo(x){if(x<741000)return 0;if(x<2191000)return x-740000;if(x<2193000)return 1451000;if(x<2196000)return 1453000;if(x<2200000)return 1456000;
  if(x<6600000){var a=fl(x,4000)*4000;return x<3600000?fl(a*7,10)-80000:fl(a*8,10)-440000;}
  if(x<8500000)return fl(x*9,10)-1100000;return x-1950000;}
 function kiso(t){var T=[[4890000,1040000],[6550000,670000],[23500000,620000],[24000000,480000],[24500000,320000],[25000000,160000]];for(var i=0;i<T.length;i++){if(t<=T[i][0])return T[i][1];}return 0;}
 function haigu(t){return t<=9000000?380000:t<=9500000?260000:t<=10000000?130000:0;}
 var ZT=[[1950000,5,0],[3300000,10,97500],[6950000,20,427500],[9000000,23,636000],[18000000,33,1536000],[40000000,40,2796000]];
 function zei(k){for(var i=0;i<ZT.length;i++){if(k<=ZT[i][0])return fl(k*ZT[i][1],100)-ZT[i][2];}return fl(k*45,100)-4796000;}
 function rate(k){for(var i=0;i<ZT.length;i++){if(k<=ZT[i][0])return ZT[i][1];}return 45;}
 function calc(q,wq,jo,wj,sha,ide,sei,iryo,kifu,h,fu,tf,loan){
  var g=kyuyo(q),tot=g+jo,ki=kiso(tot),hk=h?haigu(tot):0;
  var iryd=Math.min(2000000,Math.max(0,iryo-Math.min(100000,fl(tot*5,100)))),kfd=Math.max(0,Math.min(kifu,fl(tot*40,100))-2000);
  var koj=sha+ide+Math.min(sei,170000)+iryd+kfd+hk+380000*fu+630000*tf+ki,kz=fl(Math.max(0,tot-koj),1000)*1000;
  var san=zei(kz),kij=Math.max(0,san-loan),fk=fl(kij*21,1000),tz=kij+fk,d=tz-wq-wj;
  return {g:g,tot:tot,ki:ki,hk:hk,iryd:iryd,kfd:kfd,koj:koj,kz:kz,san:san,kij:kij,fk:fk,tz:tz,pay:d>0?fl(d,100)*100:0,ref:d<0?-d:0,rt:rate(kz)};}
 window.__shinkoku=calc;
 function render(){
  var wq=num("wq"),wj=num("wj"),jo=num("jo"),q=num("q");
  var r=calc(q,wq,jo,wj,num("sha"),num("ide"),num("sei"),num("iryo"),num("kifu"),hg,+$("fu").value,+$("tf").value,num("loan"));
  var vd=$("vd");
  if(r.ref>0){$("o-vd").textContent="確定申告で"+f(r.ref)+"円が戻ります";$("o-al").textContent="戻る所得税";$("o-a").innerHTML=f(r.ref)+"<i>円</i>";vd.className="vd";}
  else if(r.pay>0){$("o-vd").textContent="確定申告で"+f(r.pay)+"円を納めます";$("o-al").textContent="納める所得税";$("o-a").innerHTML=f(r.pay)+"<i>円</i>";vd.className="vd no";}
  else{$("o-vd").textContent="戻る額も納める額もありません";$("o-al").textContent="戻る所得税";$("o-a").innerHTML="0<i>円</i>";vd.className="vd";}
  $("o-vds").textContent="1年分の所得税"+f(r.tz)+"円に対して、源泉徴収で"+f(wq+wj)+"円が引かれています";
  $("o-t").innerHTML=f(r.tz)+"<i>円</i>";$("o-t").nextElementSibling.textContent="税率"+r.rt+"%";
  $("o-br").textContent="合計所得金額"+f(r.tot)+"円・所得控除の合計"+f(r.koj)+"円・課税所得"+f(r.kz)+"円";
  $("o-ko").textContent="医療費控除"+f(r.iryd)+"円・寄附金控除"+f(r.kfd)+"円・基礎控除"+f(r.ki)+"円"+(r.hk?"・配偶者控除"+f(r.hk)+"円":"");
  var nd;
  if(q>20000000)nd="給与の収入が2,000万円を超えるので、確定申告が必要です";
  else if(q>0&&jo>200000)nd="給与以外の所得が20万円を超えるので、確定申告が必要です";
  else if(q>0)nd="給与以外の所得が20万円以下なので、医療費控除などを受けないなら確定申告はしなくてもかまいません";
  else nd=r.pay>0?"納める所得税があるので、確定申告が必要です":"引かれすぎた源泉徴収税額は、確定申告をすると戻ります";
  $("o-nd").textContent=nd;
 }
 ["q","wq","jo","wj","sha","ide","sei","iryo","kifu","loan"].forEach(function(i){$(i).addEventListener("input",render);});
 ["fu","tf"].forEach(function(i){$(i).addEventListener("change",render);});
 document.querySelectorAll("#s-hg button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll("#s-hg button").forEach(function(x){x.classList.remove("on");});b.classList.add("on");hg=+b.dataset.v;render();});});
 render();
})();'''

PIC = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="申告書と戻る矢印"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><rect x="14" y="12" width="26" height="36" rx="2" fill="#0f3d31"/><path d="M19 22h16M19 29h16M19 36h10" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/><circle cx="44" cy="44" r="10" fill="#e3b465"/><path d="M49 44h-9m3-4-4 4 4 4" fill="none" stroke="#0f3d31" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'

body = B.hy_wrap(sec1) + calc_html + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
h = B.page(slug, title, desc, upd, body, JS, cta, pic=PIC, auth=B.auth_box('国税庁'))
close_old = B.close_box(cta)
close_new = ('<div class="close"><p class="close-h"><span class="nw">確定申告の計算と提出を、</span><span class="nw">まるごと任せる</span></p>'
             '<p>副業や事業の所得がある人の確定申告は、記帳から申告までまるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="shinkoku_close_marunage">経理丸投げの無料相談</a></div>')
assert close_old in h
h = h.replace(close_old, close_new)
os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(h)

# 自分の計算の点検
assert kyuyo(5000000) == 3560000 and kyuyo(4000000) == 2760000 and kyuyo(7000000) == 5200000
assert zei(1950000) == 97500 and zei(1951000) == 97600 and zei(3300000) == 232500 and zei(6950000) == 962500
# 年収500万・社保75万:合計所得356万・控除179万・課税177万・5%で88,500・復興1,858 → 90,358
r = calc(5000000, 0, 0, 0, 750000, 0, 0, 0, 0, 0, 0, 0, 0)
assert r['kz'] == 1770000 and r['san'] == 88500 and r['tz'] == 88500 + 1858, r
# 医療費30万:控除20万 → 課税157万・78,500+1,648=80,148 → 戻る10,210
r = calc(5000000, 90358, 0, 0, 750000, 0, 0, 300000, 0, 0, 0, 0, 0)
assert r['iryd'] == 200000 and r['tz'] == 80148 and r['ref'] == 10210, r
# 100円未満の切り捨て
r = calc(5000000, 0, 500000, 0, 750000, 0, 0, 0, 0, 0, 0, 0, 0)
assert r['pay'] == r['tz'] // 100 * 100
print('ok', title)
for x in HY_ROWS: print(x)
for lab, a, w, r in EXR: print(lab, w, r['tz'], r['ref'], r['pay'])
