# 法定耐用年数の一覧と減価償却の計算 /taiyonensu/ を作る。2026/11/19。
# 原本:国税庁 No.2106(定額法と定率法)・No.2100(減価償却のあらまし・少額の特例40万円未満)・No.5409・No.5461、
#      国税庁「減価償却資産の償却率等表」(確定申告の手引き 041.pdf・耐用年数省令 別表第八・第十)、「主な減価償却資産の耐用年数表」(2100_01.pdf)
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_saitei as B

# 耐用年数: (定額法の償却率, 定率法の償却率, 改定償却率, 保証率) 1000分の・10万分の
RT = """2 500 1000 0 0
3 334 667 1000 11089
4 250 500 1000 12499
5 200 400 500 10800
6 167 333 334 9911
7 143 286 334 8680
8 125 250 334 7909
9 112 222 250 7126
10 100 200 250 6552
11 91 182 200 5992
12 84 167 200 5566
13 77 154 167 5180
14 72 143 167 4854
15 67 133 143 4565
16 63 125 143 4294
17 59 118 125 4038
18 56 111 112 3884
19 53 105 112 3693
20 50 100 112 3486
21 48 95 100 3335
22 46 91 100 3182
23 44 87 91 3052
24 42 83 84 2969
25 40 80 84 2841
26 39 77 84 2716
27 38 74 77 2624
28 36 71 72 2568
29 35 69 72 2463
30 34 67 72 2366
31 33 65 67 2286
32 32 63 67 2216
33 31 61 63 2161
34 30 59 63 2097
35 29 57 59 2051
36 28 56 59 1974
37 28 54 56 1950
38 27 53 56 1882
39 26 51 53 1860
40 25 50 53 1791
41 25 49 50 1741
42 24 48 50 1694
43 24 47 48 1664
44 23 45 46 1664
45 23 44 46 1634
46 22 43 44 1601
47 22 43 44 1532
48 21 42 44 1499
49 21 41 42 1475
50 20 40 42 1440"""
R = {}
for ln in RT.split('\n'):
    n, a, b, c_, d = map(int, ln.split())
    R[n] = (a, b, c_, d)
# 定額法の償却率はおおむね1÷耐用年数、定率法はその2倍(200%定率法)。読み取りの誤りを機械で探す
for n, (a, b, c_, d) in R.items():
    assert abs(a / 1000 - 1 / n) < 0.0015, n
    assert abs(b / 1000 - 2 / n) < 0.0015 or n == 2, n

# 資産: (グループ, 名前, 耐用年数, 定額法だけか)
A = [
 ('建物', '鉄筋コンクリート造の事務所', 50, 1), ('建物', '鉄筋コンクリート造の住宅', 47, 1), ('建物', '鉄筋コンクリート造の店舗', 39, 1),
 ('建物', '金属造（骨格材4mm超）の事務所', 38, 1), ('建物', '金属造（骨格材4mm超）の店舗・住宅', 34, 1),
 ('建物', '金属造（3mm超4mm以下）の店舗・住宅', 27, 1), ('建物', '金属造（3mm以下）の店舗・住宅', 19, 1),
 ('建物', '木造の事務所', 24, 1), ('建物', '木造の店舗・住宅', 22, 1), ('建物', '木造の飲食店', 20, 1), ('建物', '木骨モルタル造の店舗・住宅', 20, 1),
 ('建物附属設備', '電気設備（照明など）', 15, 1), ('建物附属設備', '給排水・衛生設備・ガス設備', 15, 1), ('建物附属設備', '店用簡易装備', 3, 1),
 ('車両', '普通自動車（一般用）', 6, 0), ('車両', '軽自動車（総排気量0.66L以下）', 4, 0), ('車両', 'バイク（二輪・三輪）', 3, 0),
 ('車両', '貨物自動車（ダンプ以外）', 5, 0), ('車両', '自転車', 2, 0),
 ('器具備品', 'パソコン（サーバー用を除く）', 4, 0), ('器具備品', 'サーバー', 5, 0), ('器具備品', 'コピー機・レジ', 5, 0),
 ('器具備品', '事務机・いす・キャビネット（金属製）', 15, 0), ('器具備品', '事務机・いす・キャビネット（金属製以外）', 8, 0),
 ('器具備品', '応接セット（接客業用）', 5, 0), ('器具備品', '冷蔵庫・洗濯機などの家電', 6, 0), ('器具備品', 'エアコン（冷房用・暖房用機器）', 6, 0),
 ('器具備品', 'テレビ・音響機器', 5, 0), ('器具備品', 'カメラ', 5, 0), ('器具備品', '看板・ネオンサイン', 3, 0), ('器具備品', '時計', 10, 0),
 ('ソフトウェア', 'ソフトウェア（自社で使うもの）', 5, 1), ('ソフトウェア', 'ソフトウェア（販売用の原本・研究開発用）', 3, 1),
]

def sched(cost, n, teiritsu, months=12):
    """1年ごとの償却費(1円未満切捨て)。最後は1円を残す。ソフトウェアは0円まで(nokori=0)。"""
    a, b, kr, hs = R[n]
    out = []; bv = cost; hosho = cost * hs // 100000; kaitei = None; y = 0
    while bv > 1 and y < 80:
        m = months if y == 0 else 12
        if not teiritsu:
            d = cost * a * m // 12000
        else:
            if kaitei is None:
                pre = bv * b // 1000
                if y > 0 and pre < hosho:
                    kaitei = bv
            if kaitei is None:
                d = bv * b * m // 12000
            else:
                d = kaitei * kr * m // 12000
        d = min(d, bv - 1)
        out.append(d); bv -= d; y += 1
    return out

# 国税庁 No.2106 の計算例(100万円・10年)
s = sched(1000000, 10, False)
assert s == [100000] * 9 + [99999], s
s = sched(1000000, 10, True)
assert s[:7] == [200000, 160000, 128000, 102400, 81920, 65536, 65536] and s[7:] == [65536, 65536, 65535], s
# No.5410 の例(耐用年数8年の保証率 0.07909)
assert R[8] == (125, 250, 334, 7909)

c = B.c; td = B.td; table = B.table
slug = 'taiyonensu'; cta = 'taiyo'
title = '【法定耐用年数の一覧】減価償却の計算と毎年の償却費【2026年】'
desc = 'パソコンは4年・普通自動車は6年・木造の店舗は22年など、よく使う資産の法定耐用年数を一覧にしました。取得価額と使い始めた月を入力すると、定額法・定率法で毎年の減価償却費と残りの額が分かります。10万円・20万円・40万円未満の扱いも出します。'
upd = '更新日：2026年11月19日（国税庁 No.2100・No.2106 令和8年4月1日現在法令等）'

opts = ''
grp = None
for i, (g, nm, n, only) in enumerate(A):
    if g != grp:
        if grp is not None:
            opts += '</optgroup>'
        opts += '<optgroup label="%s">' % g
        grp = g
    opts += '<option value="%d"%s>%s（%d年）</option>' % (i, ' selected' if nm.startswith('パソコン') else '', nm, n)
opts += '</optgroup><option value="-1">耐用年数を自分で入れる</option>'
mopts = ''.join('<option value="%d"%s>%d月</option>' % (m, ' selected' if m == 4 else '', m) for m in range(1, 13))

calc = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span>資産を選ぶと、法定耐用年数と1年目の減価償却費を表示します</div>
 <div class="in">
  <div class="full">
   <label for="as">資産の種類</label>
   <select id="as">%(opts)s</select>
  </div>
  <div class="full hide" id="w-n">
   <label for="yrs">耐用年数</label>
   <div class="row"><input type="number" id="yrs" inputmode="numeric" min="2" max="50" step="1" value="10"><span>年</span></div>
  </div>
  <div class="full">
   <label for="cost">取得価額（買った金額。消費税は経理の方式に合わせる）</label>
   <div class="row"><input type="number" id="cost" inputmode="numeric" min="0" max="10000000000" step="1" value="500000"><span>円</span></div>
  </div>
  <div class="full">
   <label>事業をしている人</label>
   <div class="seg" id="s-who"><button type="button" class="on" data-v="0">個人事業主</button><button type="button" data-v="1">法人</button></div>
  </div>
  <div class="full">
   <label>償却方法</label>
   <div class="seg" id="s-hoho"><button type="button" class="on" data-v="0">定額法</button><button type="button" data-v="1">定率法</button></div>
  </div>
  <div class="full">
   <label for="mon">使い始めた月（法人は事業年度の何か月目か）</label>
   <select id="mon">%(mopts)s</select>
  </div>
 </div>
 <div class="vd" id="vd"><b id="o-vd"></b><span id="o-vds"></span></div>
 <div class="amt">
  <div><small>法定耐用年数</small><b id="o-n"></b><em id="o-ne"></em></div>
  <div><small>1年目の<br>減価償却費</small><b id="o-1"></b><em id="o-1e"></em></div>
  <div><small>2年目の<br>減価償却費</small><b id="o-2"></b><em>1年分</em></div>
 </div>
 <ul>
  <li id="o-how"></li>
  <li>1円未満は切り捨てています。最後の年は1円を残します（ソフトウェアは0円まで）</li>
 </ul>
 <p class="cap" style="margin-top:12px">毎年の減価償却費</p>
 <div class="tw"><table><thead><tr><th>年</th><th>減価償却費<br>（円）</th><th>年末の残り<br>（円）</th></tr></thead><tbody id="tb"></tbody></table></div>
</div>
''' % {'opts': opts, 'mopts': mopts}

intro = '<p>法定耐用年数は、資産の種類ごとに国が決めた「何年で経費にするか」の年数です。<span class="mk">パソコンは4年・普通自動車は6年・木造の店舗は22年です。</span>買った金額を耐用年数で分けて毎年の経費にするのが減価償却で、個人事業主は届け出なければ定額法で計算します。</p>\n'

toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#list">よく使う資産の法定耐用年数</a></li>
  <li><a href="#rate">耐用年数ごとの償却率</a></li>
  <li><a href="#rei">50万円の資産なら毎年いくら経費になるか</a></li>
  <li><a href="#shogaku">10万円・20万円・40万円未満の扱い</a></li>
  <li><a href="#hoho">定額法と定率法の決まり</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">耐用年数でよく聞かれること</a></li>
 </ol>
</nav>
'''

rows = []
for g, nm, n, only in A:
    rows.append([td(g, 'l'), td(nm, 'l'), td('%d年' % n)])
sec1 = ('<h2 id="list">よく使う資産の法定耐用年数</h2>\n<p>新品で買った資産の耐用年数です。建物・建物附属設備・ソフトウェアは定額法だけで計算します。中古の資産は、残りの年数を見積もって短くできます。</p>\n'
        + table(['種類', '資産', '耐用<br>年数'], rows)
        + '<p class="note" style="margin-top:8px">国税庁「主な減価償却資産の耐用年数表」と耐用年数省令の別表第一・第三によります。鉄筋コンクリート造の飲食店は、木造の内装部分が延べ面積の30%を超えると34年です。超えないものは41年で、木造の飲食店は20年です。中古車の年数は<a href="/chukosha-taiyonensu/">中古車の耐用年数の計算</a>で確かめられます。</p>\n')

rr = []
for n in (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 22, 24, 30, 34, 38, 39, 47, 50):
    a, b, kr, hs = R[n]
    rr.append([td('%d年' % n), td('%.3f' % (a / 1000)), td('%.3f' % (b / 1000)), td('―' if not kr else '%.3f' % (kr / 1000)), td('―' if not hs else '%.5f' % (hs / 100000))])
sec2 = ('<h2 id="rate">耐用年数ごとの償却率</h2>\n<p>定額法は「取得価額×定額法の償却率」が毎年の償却費です。定率法は「年初の残り×定率法の償却率」で、その額が償却保証額（取得価額×保証率）を下回った年から「改定取得価額×改定償却率」に切り替えます。</p>\n'
        + table(['耐用<br>年数', '定額法', '定率法', '改定<br>償却率', '保証率'], rr)
        + '<p class="note" style="margin-top:8px">定率法は平成24年4月1日以後に取得した資産の率（200%定率法）です。上の計算では2年から50年までの全部の率を使っています。</p>\n')

ex = []
for n in (4, 5, 6, 8, 10):
    s1 = sched(500000, n, False); s2 = sched(500000, n, True)
    ex.append([td('%d年' % n), td(c(s1[0])), td(c(s2[0])), td(c(s2[1])), td(c(sum(s2[:2])))])
sec3 = ('<h2 id="rei">50万円の資産なら毎年いくら経費になるか</h2>\n<p>1月から1年間使った場合です。定率法は1年目の経費が大きく、年がたつほど少なくなります。</p>\n'
        + table(['耐用<br>年数', '定額法<br>毎年（円）', '定率法<br>1年目（円）', '定率法<br>2年目（円）', '定率法<br>2年の合計'], ex)
        + '<p class="note" style="margin-top:8px">年の途中から使ったときは、1年目の償却費を使った月数で月割りします。4月から使えば9か月分です。</p>\n')

sec4 = ('<h2 id="shogaku">10万円・20万円・40万円未満の扱い</h2>\n<p>取得価額が小さい資産は、耐用年数で分けずに経費にできる決まりがあります。</p>\n'
        + table(['取得価額', '扱い'], [
            [td('10万円未満', 'l'), td('使い始めた年に全額を経費にする（少額減価償却資産）', 'l')],
            [td('10万円以上<br>20万円未満', 'l'), td('3年で3分の1ずつ経費にすることも選べる（一括償却資産）', 'l')],
            [td('10万円以上<br>40万円未満', 'l'), td('青色申告の中小企業者等は、年300万円まで全額を経費にできる（令和8年3月31日までの取得は30万円未満）', 'l')],
            [td('上のどれにも<br>当たらない', 'l'), td('耐用年数で減価償却する', 'l')]])
        + '<p class="note" style="margin-top:8px">40万円未満の特例は、令和8年4月1日から令和11年3月31日までに取得した資産が対象です（国税庁 No.2100）。法人は従業員400人以下などの条件があります（中小企業庁）。</p>\n')

sec5 = ('<h2 id="hoho">定額法と定率法の決まり</h2>\n<h3>届け出ないときの方法</h3>\n<p>個人事業主は、届け出なければ定額法です。法人は届け出なければ、機械・車両・器具備品などは定率法です。</p>\n'
        '<h3>定額法だけの資産</h3>\n<p>平成10年4月1日以後に取得した建物と平成28年4月1日以後に取得した建物附属設備・構築物は、定額法だけです。ソフトウェアも定額法で、最後は0円まで償却します。</p>\n'
        '<h3>届け出の期限</h3>\n<p>個人事業主は、業務を始めた年の翌年3月15日までに税務署へ届け出ます。法人は、設立した事業年度の確定申告書の提出期限までです。</p>\n')

rel_items = [
    ('chukosha-taiyonensu', '中古車の耐用年数の計算', '中古で買った車は、新車の6年より短い年数で減価償却できます。'),
    ('kojin-zei', '個人事業主の手取りの早見表', '減価償却費も経費なので、所得と税金が下がります。'),
    ('houjinzei-keisan', '法人税の計算', '会社の利益から、法人税・住民税・事業税の合計を出せます。'),
    ('houjinzei', '法人税の早見表', '中小法人の法人税の税率は、所得800万円を境に変わります。'),
    ('niwari-tokurei', '消費税の計算', '設備を買った年の消費税も、2割特例と簡易課税で比べられます。'),
    ('soneki-bunkiten', '損益分岐点の計算', '減価償却費は、売上にかかわらず出ていく固定費です。'),
    ('hensai', '借入の返済の計算', '設備を借入で買うなら、毎月の返済額を先に確かめます。'),
    ('kakutei-shinkoku', '確定申告の期限の早見表', '減価償却の届け出と申告の期限を確かめられます。'),
    ('houjinnari', '法人成りの計算', '個人事業から会社にするかは、所得がいくらかで損得が分かれます。'),
    ('shotoku-kingaku', '所得金額の計算', '事業の所得から、合計所得金額と扶養に入るかが分かります。'),
    ('yakuin-shataku', '役員社宅の家賃の計算', '会社で建物を持つときは、社宅の家賃も決まりで計算します。'),
    ('kani-kazei', '簡易課税の事業区分', '事業で使った車や機械を売ると、簡易課税では第4種です。'),
]
sec6 = B.rel(slug, rel_items)

qa = ('<h2 id="qa">耐用年数でよく聞かれること</h2>\n'
      '<h3>パソコンの耐用年数は何年ですか？</h3>\n<p>4年です。サーバー用は5年です。10万円未満なら耐用年数で分けずに、使い始めた年に全額を経費にします。</p>\n'
      '<h3>車の耐用年数は何年ですか？</h3>\n<p>新車の普通自動車は6年・軽自動車は4年です。中古車は残りの年数を見積もって短くでき、4年落ちの普通自動車なら2年です。</p>\n'
      '<h3>定額法と定率法はどちらが得ですか？</h3>\n<p>経費になる合計の額は同じです。定率法は早い年に多く経費になるので、利益が多い年に買った資産は定率法のほうが税金を先に減らせます。</p>\n'
      '<h3>年の途中で買ったら、1年目はいくらですか？</h3>\n<p>1年分の償却費を12で割り、使い始めた月から12月までの月数を掛けます。10月に使い始めたら3か月分です。買っただけで使っていない月は数えません。</p>\n'
      '<h3>耐用年数が過ぎたら、資産はどうなりますか？</h3>\n<p>帳簿には1円が残り、捨てたり売ったりするまで資産として載ります。そのまま使い続けても、減価償却費はもう出ません。</p>\n')

src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2106.htm">国税庁 No.2106「定額法と定率法による減価償却」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2100.htm">国税庁 No.2100「減価償却のあらまし」</a>（少額の特例・40万円未満）</li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5409.htm">国税庁 No.5409「減価償却資産の償却方法の選定」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5461.htm">国税庁 No.5461「ソフトウエアの取得価額と耐用年数」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/pdf/2100_01.pdf">国税庁「主な減価償却資産の耐用年数表」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/shinkoku/tebiki/2023/pdf/041.pdf">国税庁「減価償却資産の償却率等表」</a>（耐用年数省令 別表第八・第十）</li>
  <li><a href="https://www.chusho.meti.go.jp/zaimu/zeisei/tokurei/syougaku_shisan.html">中小企業庁「中小企業者等の少額減価償却資産の取得価額の損金算入の特例」</a></li>
 </ul>
</div>
'''

JS = r'''(function(){
 var R=%(R)s,A=%(A)s;
 var who=0,hoho=0,$=function(i){return document.getElementById(i)};
 function f(n){return n.toLocaleString("ja-JP");}
 function num(i,lo,hi){var v=parseInt($(i).value,10);if(isNaN(v))v=lo;return Math.min(Math.max(v,lo),hi);}
 function sched(cost,n,tr,months,soft){var r=R[n],a=r[0],b=r[1],kr=r[2],hs=r[3],out=[],bv=cost,low=soft?0:1,hosho=Math.floor(cost*hs/100000),kai=-1,y=0;
  while(bv>low&&y<80){var m=y===0?months:12,d;
   if(!tr){d=Math.floor(cost*a*m/12000);}
   else{if(kai<0){var pre=Math.floor(bv*b/1000);if(y>0&&pre<hosho)kai=bv;}
    d=kai<0?Math.floor(bv*b*m/12000):Math.floor(kai*kr*m/12000);}
   d=Math.min(d,bv-low);out.push(d);bv-=d;y++;}
  return out;}
 function render(){
  var i=+$("as").value,only=0,soft=0,n,nm;
  if(i<0){$("w-n").classList.remove("hide");n=num("yrs",2,50);nm="耐用年数"+n+"年の資産";}
  else{$("w-n").classList.add("hide");n=A[i][2];only=A[i][3];soft=A[i][0]==="ソフトウェア";nm=A[i][1];}
  var cost=num("cost",0,10000000000),mon=+$("mon").value,months=13-mon,tr=only?0:hoho;
  var s=sched(cost,n,tr,months,soft),r=R[n];
  var bs=$("s-hoho").querySelectorAll("button");bs[1].disabled=!!only;bs[0].className=tr?"":"on";bs[1].className=tr?"on":"";
  $("o-n").innerHTML=n+"<i>年</i>";$("o-ne").textContent=(tr?"定率法 ":"定額法 ")+((tr?r[1]:r[0])/1000).toFixed(3);
  $("o-1").innerHTML=f(s[0]||0)+"<i>円</i>";$("o-1e").textContent=months+"か月分";
  $("o-2").innerHTML=f(s[1]||0)+"<i>円</i>";
  $("o-how").textContent=nm+"を"+(only?"定額法だけで":(tr?"定率法で":"定額法で"))+"計算しています。"+(only?"この資産は定率法を選べません":(who?"法人は届け出なければ定率法です":"個人事業主は届け出なければ定額法です"));
  var vd=$("vd"),t,sp;
  if(cost<100000){t="全額をその年の経費にできます";sp="10万円未満なので少額減価償却資産です。減価償却はしません";}
  else if(cost<200000){t="3年で3分の1ずつも選べます";sp="10万円以上20万円未満なので一括償却資産にできます。青色申告の中小企業者等は全額を経費にもできます";}
  else if(cost<400000){t="青色申告なら全額経費にもできます";sp="40万円未満の特例（令和8年4月1日以後の取得・年300万円まで）が使えなければ、下の表で減価償却します";}
  else{t="耐用年数で減価償却します";sp=n+"年で経費にします。"+(s.length>n?"年の途中から使ったので"+s.length+"年に分かれます":"")}
  vd.className="vd no";$("o-vd").textContent=t;$("o-vds").textContent=sp;
  var h="",bv=cost;for(var k=0;k<s.length;k++){bv-=s[k];h+="<tr><td>"+(k+1)+"年目</td><td>"+f(s[k])+"</td><td>"+f(bv)+"</td></tr>";}
  $("tb").innerHTML=h;}
 ["as","yrs","cost","mon"].forEach(function(i){$(i).addEventListener("input",render);$(i).addEventListener("change",render);});
 function seg(id,cb){$(id).querySelectorAll("button").forEach(function(b){b.addEventListener("click",function(){if(b.disabled)return;cb(+b.dataset.v);render();});});}
 seg("s-who",function(v){who=v;hoho=v;$("s-who").querySelectorAll("button").forEach(function(x){x.className=+x.dataset.v===v?"on":"";});});
 seg("s-hoho",function(v){hoho=v;});
 window.__taiyo=sched;
 render();
})();''' % {'R': json.dumps({str(k): v for k, v in R.items()}), 'A': json.dumps([[g, nm, n, o] for g, nm, n, o in A], ensure_ascii=False)}

PIC = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="年ごとに減る棒グラフ"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><rect x="13" y="18" width="8" height="30" rx="1.5" fill="#0f3d31"/><rect x="24" y="26" width="8" height="22" rx="1.5" fill="#00775a"/><rect x="35" y="33" width="8" height="15" rx="1.5" fill="#00775a"/><rect x="46" y="39" width="8" height="9" rx="1.5" fill="#e08a2c"/></svg></div>'

body = calc + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n' + sec1 + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
h = B.page(slug, title, desc, upd, body, JS, cta, pic=PIC, auth=B.auth_box('国税庁'))
close_old = B.close_box(cta)
close_new = ('<div class="close"><p class="close-h"><span class="nw">設備を買った年の、</span><span class="nw">帳簿と申告も</span></p>'
             '<p>減価償却は、買った年だけでなく耐用年数のあいだ毎年の決算に出てきます。記帳から決算・申告まで、まるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="taiyo_close_marunage">経理丸投げの無料相談</a></div>')
assert close_old in h
h = h.replace(close_old, close_new)
os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(h)
print('ok', title)
