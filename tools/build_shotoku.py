# 所得金額の計算 /shotoku-kingaku/ を作る。2026/11/18。
# 原本:国税庁「令和8年度税制改正による所得税の基礎控除の引上げ、給与所得控除の最低保障額の引上げ等について」(2026kaisei.pdf)
#       国税庁「令和8年分所得税の税額表等」(公的年金等に係る雑所得の速算表)・租税特別措置法41条の3の3(所得金額調整控除)
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_saitei as B

c = B.c; td = B.td; table = B.table

def kyuyo(x):
    # 令和8・9年分の給与所得(特例適用後)
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

def nenkin(y, old, other):
    # 公的年金等に係る雑所得。old=1 は65歳以上(昭和37年1月1日以前生まれ)。other は年金以外の合計所得金額
    k = 0 if other <= 10000000 else (100000 if other <= 20000000 else 200000)
    if old and y < 3300000:
        v = y - 1100000 + k
    elif y < 1300000:
        v = y - 600000 + k
    elif y < 4100000:
        v = y * 75 // 100 - 275000 + k
    elif y < 7700000:
        v = y * 85 // 100 - 685000 + k
    elif y < 10000000:
        v = y * 95 // 100 - 1455000 + k
    else:
        v = y - 1955000 + k
    return max(0, v)

AOIRO = [0, 100000, 550000, 650000]

def calc(q, y, old, js, je, ao, zi, ze, ii, ie):
    g = kyuyo(q)
    prof = js - je
    blue = min(AOIRO[ao], max(0, prof))
    jig = prof - blue
    zo = zi - ze
    ichi = max(0, ii - ie - 500000)
    other = g + jig + max(0, zo) + ichi // 2
    p = nenkin(y, old, other) if y > 0 else 0
    adj = max(0, min(g, 100000) + min(p, 100000) - 100000) if g > 0 and p > 0 else 0
    g2 = g - adj
    zat = max(0, p + zo)
    base = g2 + jig + zat
    if base >= 0:
        tot = base + ichi // 2
    else:
        tot = max(0, ichi + base) // 2
    return dict(g=g2, adj=adj, p=p, jig=jig, zat=zat, ichi=ichi, tot=tot)

def kiso(t):
    for lim, v in [(4890000, 1040000), (6550000, 670000), (23500000, 620000), (24000000, 480000), (24500000, 320000), (25000000, 160000)]:
        if t <= lim: return v
    return 0

slug = 'shotoku-kingaku'; cta = 'shotoku'
title = '【所得金額の計算】収入から合計所得金額を出す｜給与・年金・事業【令和8年分】'
desc = '給与・年金・事業・副業の収入を入力すると、令和8年分の所得金額と合計所得金額が分かります。扶養の62万円・配偶者特別控除の133万円・勤労学生の89万円に入るかと、本人の基礎控除の額も出ます。給与所得と年金の雑所得の早見表付きです。'
upd = '更新日：2026年11月18日（国税庁 令和8年分の給与所得控除・基礎控除・所得要件）'

calc_html = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span>収入から経費や控除を引いた額が所得で、その合計が合計所得金額です</div>
 <div class="in">
  <div class="full">
   <label for="q">給与の収入（1年・税金や保険料が引かれる前）</label>
   <div class="row"><input type="number" id="q" inputmode="numeric" min="0" max="1000000000" step="1" value="1300000"><span>円</span></div>
  </div>
  <div class="full">
   <label for="y">公的年金の収入（1年・国民年金・厚生年金など）</label>
   <div class="row"><input type="number" id="y" inputmode="numeric" min="0" max="1000000000" step="1" value="0"><span>円</span></div>
   <label>令和8年12月31日の年齢</label>
   <div class="seg" id="s-old"><button type="button" class="on" data-v="0">65歳未満</button><button type="button" data-v="1">65歳以上</button></div>
  </div>
  <div class="full">
   <label for="js">事業の売上（個人事業・1年）</label>
   <div class="row"><input type="number" id="js" inputmode="numeric" min="0" max="10000000000" step="1" value="0"><span>円</span></div>
   <label for="je">事業の経費</label>
   <div class="row"><input type="number" id="je" inputmode="numeric" min="0" max="10000000000" step="1" value="0"><span>円</span></div>
   <label for="ao">青色申告特別控除</label>
   <select id="ao"><option value="0">白色申告（なし）</option><option value="1">10万円</option><option value="2">55万円</option><option value="3">65万円（電子申告など）</option></select>
  </div>
  <div class="full">
   <label for="zi">副業などの収入（雑所得・年金以外）</label>
   <div class="row"><input type="number" id="zi" inputmode="numeric" min="0" max="10000000000" step="1" value="0"><span>円</span></div>
   <label for="ze">副業などの経費</label>
   <div class="row"><input type="number" id="ze" inputmode="numeric" min="0" max="10000000000" step="1" value="0"><span>円</span></div>
  </div>
  <div class="full">
   <label for="ii">一時所得の収入（生命保険の満期金・懸賞の賞金など）</label>
   <div class="row"><input type="number" id="ii" inputmode="numeric" min="0" max="10000000000" step="1" value="0"><span>円</span></div>
   <label for="ie">一時所得を得るために払った額（払った保険料など）</label>
   <div class="row"><input type="number" id="ie" inputmode="numeric" min="0" max="10000000000" step="1" value="0"><span>円</span></div>
  </div>
 </div>
 <div class="vd" id="vd"><b id="o-vd"></b><span id="o-vds"></span></div>
 <div class="amt jdg">
  <div><small>合計所得金額</small><b id="o-t"></b><em>令和8年分</em></div>
  <div><small>本人の基礎控除</small><b id="o-k"></b><em>所得税</em></div>
 </div>
 <ul>
  <li id="o-br"></li>
  <li id="o-sp"></li>
  <li id="o-kg"></li>
  <li>判定は所得税の決まりです。住民税の扶養の所得要件は58万円以下のままで、所得税とは違います</li>
 </ul>
</div>
'''

intro = '<p>所得金額は、収入から経費や給与所得控除・公的年金等控除を引いた額です。<span class="mk">給与だけの人は年収136万円で合計所得金額が62万円になります。ここまでなら、家族の扶養控除や配偶者控除の対象です。</span>令和8年分から給与所得控除の最低額が74万円になり、扶養の所得要件も58万円から62万円に上がりました。</p>\n'

toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#kyuyo">給与の収入と給与所得の早見表</a></li>
  <li><a href="#nenkin">公的年金の収入と雑所得の早見表</a></li>
  <li><a href="#kabe">合計所得金額で決まること（令和8年分）</a></li>
  <li><a href="#keisan">所得の種類ごとの計算のしかた</a></li>
  <li><a href="#chui">合計所得金額に入るもの・入らないもの</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">所得金額でよく聞かれること</a></li>
 </ol>
</nav>
'''

rows = []
for m in [100, 110, 136, 150, 160, 163, 180, 190, 197, 200, 207, 250, 300, 400, 500, 665, 850, 1000]:
    q = m * 10000; g = kyuyo(q)
    rows.append([td('%s万円' % c(m)), td(c(q - g)), td(c(g))])
sec1 = ('<h2 id="kyuyo">給与の収入と給与所得の早見表</h2>\n<p>給与の所得は、年収から給与所得控除を引いた額です。令和8年分と令和9年分は、年収190万円以下の人の給与所得控除が74万円です。</p>\n<p class="cap">令和8年分・給与所得控除と給与所得</p>\n'
        + table(['年収', '給与所得控除<br>（円）', '給与所得<br>（円）'], rows)
        + '<p class="note" style="margin-top:8px">年収219万1,000円から220万円未満は国税庁の表で決まった額です。年収660万円未満は、年収を4,000円きざみに切り下げてから計算します。年収850万円を超えると給与所得控除は195万円で増えません。</p>\n')

rows = []
for m in [60, 80, 100, 110, 130, 150, 180, 200, 250, 300, 330, 400, 500]:
    y = m * 10000
    rows.append([td('%s万円' % c(m)), td(c(nenkin(y, 0, 0))), td(c(nenkin(y, 1, 0)))])
sec2 = ('<h2 id="nenkin">公的年金の収入と雑所得の早見表</h2>\n<p>公的年金の所得は、年金の収入から公的年金等控除を引いた雑所得です。65歳以上の人は、年金の収入が330万円未満なら110万円を引けます。65歳未満の人は、130万円未満なら60万円です。</p>\n<p class="cap">令和8年分・年金以外の合計所得金額が1,000万円以下の場合</p>\n'
        + table(['年金の収入', '65歳未満<br>（円）', '65歳以上<br>（円）'], rows)
        + '<p class="note" style="margin-top:8px">65歳以上は、令和8年12月31日に65歳以上の人（昭和37年1月1日以前に生まれた人）です。年金以外の合計所得金額が1,000万円を超える人は、雑所得が10万円（2,000万円を超えると20万円）多くなります。</p>\n')

kabe_rows = [
    ['家族の扶養控除・配偶者控除の対象', '62万円以下', '136万円以下'],
    ['特定親族特別控除の対象（19〜22歳）', '62万円超123万円以下', '136万円超197万円以下'],
    ['配偶者特別控除の対象', '62万円超133万円以下', '136万円超207万円以下'],
    ['勤労学生控除を受けられる', '89万円以下', '163万円以下'],
    ['本人の基礎控除が104万円', '489万円以下', '665万5,556円以下'],
    ['配偶者控除・配偶者特別控除を受ける本人', '1,000万円以下', '1,195万円以下'],
]
sec3 = ('<h2 id="kabe">合計所得金額で決まること（令和8年分）</h2>\n<p>扶養や控除に入れるかどうかは、年収ではなく合計所得金額で決まります。給与だけの人の年収の目安も並べました。</p>\n<p class="cap">令和8年分の所得税</p>\n'
        + table(['決まること', '合計所得金額', '給与だけなら<br>年収'], [[td(a, 'l'), td(b), td(cc)] for a, b, cc in kabe_rows])
        + '<p class="note" style="margin-top:8px">勤労学生控除は、給与など働いて得た所得以外の所得が10万円以下という条件もあります。住民税の扶養の所得要件は合計所得金額58万円以下で、所得税の62万円とは違います。社会保険の扶養は所得ではなく収入（年130万円未満など）で決まります。</p>\n')

sec4 = ('<h2 id="keisan">所得の種類ごとの計算のしかた</h2>\n'
        '<h3>給与所得</h3>\n<p>年収から給与所得控除を引きます。給与と公的年金の両方がある人は、所得金額調整控除として最大10万円が給与所得から引かれます。</p>\n'
        '<h3>事業所得</h3>\n<p>売上から経費を引き、青色申告の人は青色申告特別控除（10万円・55万円・65万円）を引きます。赤字のときは、給与所得などから差し引けます。</p>\n'
        '<h3>雑所得</h3>\n<p>公的年金は公的年金等控除を引いた額です。副業の収入などは、収入から経費を引きます。雑所得の赤字は、ほかの種類の所得から引けません。</p>\n'
        '<h3>一時所得</h3>\n<p>収入から払った額と特別控除の50万円を引き、その半分を合計所得金額に入れます。生命保険の満期金なら、払った保険料の合計を引けます。</p>\n')

sec5 = ('<h2 id="chui">合計所得金額に入るもの・入らないもの</h2>\n'
        '<ul>\n <li>入る：給与・事業・不動産・公的年金や副業の雑所得・一時所得の半分など</li>\n'
        ' <li>申告すれば入る：株の売却益や配当など、確定申告で申告すると決めた分</li>\n'
        ' <li>入らない：遺族年金・障害年金・失業給付・通勤手当（限度額まで）などの非課税の収入</li>\n</ul>\n'
        '<p>不動産の赤字のうち土地を買うための借入金の利子は、ほかの所得から引けません。前の年までの赤字を繰り越して引く分は、合計所得金額を出したあとに引きます。</p>\n')

rel_items = [
    ('nenshu-kabe', '年収の壁の早見表', '136万円・160万円・178万円などの壁を、年収ごとに確かめられます。'),
    ('part-fuyou', 'パートの扶養の計算', 'パートの月収で、税金と社会保険の扶養に入れるかの目安が分かります。'),
    ('gakusei-kabe', '学生バイトの年収の壁', '学生のアルバイトは、年収で親の扶養と本人の税金が変わります。'),
    ('shotokuzei', '所得税の計算', '合計所得金額から所得控除を引いた課税所得に、税率をかけます。'),
    ('juminzei', '住民税の早見表', '住民税は所得の額で決まり、扶養の基準も所得税と違います。'),
    ('tedori', '年収の手取りの早見表', '年収から税金と社会保険料を引いた手取りを、年収ごとに見られます。'),
    ('fukugyo', '副業の税金の計算', '会社員の副業の所得が20万円を超えたら、確定申告が要ります。'),
    ('kojin-zei', '個人事業主の手取りの早見表', '事業所得から国保・国民年金・税金を引いた手取りを見られます。'),
    ('furusato', 'ふるさと納税の限度額の計算', '所得の額と家族で、寄附の上限の目安が決まります。'),
    ('nenmatsu-chosei', '年末調整の還付金の計算', '会社員は年末調整で、1年分の給与所得から税金を計算し直します。'),
    ('kakutei-shinkoku', '確定申告の期限の早見表', '年金と事業の所得がある人は、確定申告の期限を確かめておきましょう。'),
    ('iryohi-kojo', '医療費控除の計算', '総所得金額が200万円未満の人は、所得の5%を超えた医療費から控除できます。'),
]
sec6 = B.rel(slug, rel_items)

qa = ('<h2 id="qa">所得金額でよく聞かれること</h2>\n'
      '<h3>所得と収入の違いは何ですか？</h3>\n<p>収入は受け取った金額そのものです。所得は、収入から経費や給与所得控除などを引いた額です。年収136万円の給与なら、所得は136万円から74万円を引いた62万円です。</p>\n'
      '<h3>扶養に入れるのは年収いくらまでですか？</h3>\n<p>所得税の扶養控除・配偶者控除は、合計所得金額62万円以下です。給与だけなら年収136万円以下です。19歳から22歳の子は、年収197万円まで特定親族特別控除の対象です。</p>\n'
      '<h3>年金をもらっている親は扶養に入れますか？</h3>\n<p>65歳以上で公的年金だけなら、年金の収入172万円まで雑所得が62万円以下です。この範囲なら扶養に入れます。65歳未満は年金の収入122万円までです。</p>\n'
      '<h3>個人事業主の所得はどう出しますか？</h3>\n<p>売上から経費を引き、青色申告なら青色申告特別控除を引いた額です。売上300万円・経費100万円・青色65万円なら、所得は135万円です。</p>\n'
      '<h3>給与と年金の両方があるときは？</h3>\n<p>給与所得と年金の雑所得を足します。両方がそれぞれ10万円を超えると、所得金額調整控除として給与所得から10万円が引かれます。</p>\n')

src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/publication/pamph/gensen/2026kaisei.pdf">国税庁「令和8年度税制改正による所得税の基礎控除の引上げ、給与所得控除の最低保障額の引上げ等について」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/tetsuzuki/shinsei/annai/shinkoku/pdf/r08/zeigakuhyo.pdf">国税庁「令和8年分所得税の税額表等」</a>（公的年金等に係る雑所得の速算表）</li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm">国税庁 タックスアンサー No.1410 給与所得控除</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1600.htm">国税庁 タックスアンサー No.1600 公的年金等の課税関係</a></li>
  <li><a href="https://www.city.minoh.lg.jp/zeimu/zeiseikaisei/r09zeiseikaisei.html">箕面市「令和9年度からの個人住民税の主な改正点」</a>（住民税の基礎控除は改正なし）</li>
  <li>所得税法第22条・第27条・第28条・第34条・第35条・第69条／租税特別措置法第41条の3の3（所得金額調整控除）</li>
 </ul>
</div>
'''

JS = r'''(function(){
 var $=function(i){return document.getElementById(i)},old=0,AO=[0,100000,550000,650000];
 function f(n){return Math.round(n).toLocaleString("ja-JP");}
 function num(i){var v=parseInt(String($(i).value).replace(/[^0-9]/g,""),10);return isNaN(v)?0:v;}
 function kyuyo(x){if(x<741000)return 0;if(x<2191000)return x-740000;if(x<2193000)return 1451000;if(x<2196000)return 1453000;if(x<2200000)return 1456000;
  if(x<6600000){var a=Math.floor(x/4000)*4000;return x<3600000?Math.floor(a*7/10)-80000:Math.floor(a*8/10)-440000;}
  if(x<8500000)return Math.floor(x*9/10)-1100000;return x-1950000;}
 function nenkin(y,o,other){var k=other<=10000000?0:(other<=20000000?100000:200000),v;
  if(o&&y<3300000)v=y-1100000+k;else if(y<1300000)v=y-600000+k;else if(y<4100000)v=Math.floor(y*75/100)-275000+k;
  else if(y<7700000)v=Math.floor(y*85/100)-685000+k;else if(y<10000000)v=Math.floor(y*95/100)-1455000+k;else v=y-1955000+k;return Math.max(0,v);}
 function kiso(t){var T=[[4890000,1040000],[6550000,670000],[23500000,620000],[24000000,480000],[24500000,320000],[25000000,160000]];for(var i=0;i<T.length;i++){if(t<=T[i][0])return T[i][1];}return 0;}
 function calc(q,y,o,js,je,ao,zi,ze,ii,ie){var g=kyuyo(q),prof=js-je,blue=Math.min(AO[ao],Math.max(0,prof)),jig=prof-blue,zo=zi-ze,ichi=Math.max(0,ii-ie-500000);
  var other=g+jig+Math.max(0,zo)+Math.floor(ichi/2),p=y>0?nenkin(y,o,other):0,adj=(g>0&&p>0)?Math.max(0,Math.min(g,100000)+Math.min(p,100000)-100000):0;
  var g2=g-adj,zat=Math.max(0,p+zo),base=g2+jig+zat,tot=base>=0?base+Math.floor(ichi/2):Math.floor(Math.max(0,ichi+base)/2);
  return {g:g2,adj:adj,p:p,jig:jig,zat:zat,ichi:ichi,tot:tot};}
 window.__sk=calc;
 function render(){
  var r=calc(num("q"),num("y"),old,num("js"),num("je"),+$("ao").value,num("zi"),num("ze"),num("ii"),num("ie")),t=r.tot;
  $("o-t").innerHTML=f(t)+"<i>円</i>";$("o-k").innerHTML=f(kiso(t))+"<i>円</i>";
  var ok=t<=620000,vd=$("vd");vd.className="vd"+(ok?" no":"");
  $("o-vd").textContent=ok?"扶養控除・配偶者控除の対象になります":"扶養控除・配偶者控除の対象になりません";
  $("o-vds").textContent=ok?"合計所得金額が62万円以下です（家族の所得税の扶養）":"合計所得金額が62万円を超えています。"+(t<=1330000?"配偶者なら配偶者特別控除の対象です（133万円以下）":"配偶者特別控除の上限133万円も超えています");
  var br="内訳：給与所得"+f(r.g)+"円";if(r.adj)br+="（所得金額調整控除"+f(r.adj)+"円を引いた額）";
  br+="・事業所得"+f(r.jig)+"円・雑所得"+f(r.zat)+"円";if(r.ichi)br+="・一時所得"+f(r.ichi)+"円の半分";$("o-br").textContent=br;
  $("o-sp").textContent=(t>620000&&t<=1230000)?"19〜22歳の子なら特定親族特別控除の対象です（62万円超123万円以下）":(t<=890000?"学生なら勤労学生控除を受けられる額です（89万円以下・働いて得た所得以外が10万円以下）":"勤労学生控除の上限89万円を超えています");
  $("o-kg").textContent=t>10000000?"本人の合計所得金額が1,000万円を超えるので、配偶者控除・配偶者特別控除は受けられません":"本人の合計所得金額が1,000万円以下なので、配偶者控除・配偶者特別控除を受けられる側です";
 }
 ["q","y","js","je","zi","ze","ii","ie"].forEach(function(i){$(i).addEventListener("input",render);});$("ao").addEventListener("change",render);
 document.querySelectorAll("#s-old button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll("#s-old button").forEach(function(x){x.classList.remove("on");});b.classList.add("on");old=+b.dataset.v;render();});});
 render();
})();'''

PIC = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="収入から所得へ"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><rect x="12" y="16" width="16" height="32" rx="2" fill="#0f3d31"/><rect x="36" y="28" width="16" height="20" rx="2" fill="#00775a"/><path d="M29 24h6l-3-4m3 4-3 4" fill="none" stroke="#e08a2c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text x="44" y="42" font-size="11" font-weight="700" text-anchor="middle" fill="#ffffff" font-family="sans-serif">所</text></svg></div>'

body = B.hy_wrap(sec1) + calc_html + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
h = B.page(slug, title, desc, upd, body, JS, cta, pic=PIC, auth=B.auth_box('国税庁'))
close_old = B.close_box(cta)
close_new = ('<div class="close"><p class="close-h"><span class="nw">所得の計算と確定申告を、</span><span class="nw">まるごと任せる</span></p>'
             '<p>事業と年金と給与の所得をまとめて申告する人は、記帳から確定申告までまるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="shotoku_close_marunage">経理丸投げの無料相談</a></div>')
assert close_old in h
h = h.replace(close_old, close_new)
os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(h)

# 自分の計算の点検(国税庁の数字と突き合わせ)
assert kyuyo(1360000) == 620000 and kyuyo(1970000) == 1230000 and kyuyo(2070000) == 1330000 and kyuyo(1630000) == 890000
assert kyuyo(6655556) == 4890000 or kyuyo(6655556) <= 4890000
assert kyuyo(11950000) == 10000000
assert nenkin(1720000, 1, 0) == 620000 and nenkin(1220000, 0, 0) == 620000
assert nenkin(3300000, 1, 0) == 2200000 and nenkin(3299999, 1, 0) == 2199999
assert calc(3000000 * 0, 0, 0, 3000000, 1000000, 3, 0, 0, 0, 0)['tot'] == 1350000
r = calc(1500000, 1500000, 1, 0, 0, 0, 0, 0, 0, 0)
assert r['adj'] == 100000 and r['tot'] == 760000 - 100000 + 400000
assert calc(0, 0, 0, 0, 0, 0, 0, 0, 1500000, 400000)['tot'] == 300000
assert calc(2000000, 0, 0, 1000000, 2000000, 0, 0, 0, 0, 0)['tot'] == 260000
print('ok', title)
