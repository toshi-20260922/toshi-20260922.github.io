# 通勤手当の非課税限度額のページ /tsukin-teate/ を作る。2026/11/17 夜。
# 原本:国税庁 No.2582・No.2585(令和8年4月1日現在法令等)・「通勤手当の非課税限度額の改正」(2026tsukin)
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_saitei as B

BANDS = [(2, 0), (10, 4200), (15, 7300), (25, 13500), (35, 19700), (45, 25900), (55, 32300), (65, 38700), (75, 45700), (85, 52700), (95, 59600), (10**9, 66400)]

def band(d):
    if d < 2:
        return 0
    for lim, amt in BANDS:
        if d < lim:
            return amt
    return 66400

def limit(mode, pas, d, park, toll):
    # mode 0:交通機関だけ 1:車・自転車だけ 2:両方
    if mode == 0:
        return min(pas, 150000)
    b = band(d)
    pk = min(park, 5000) if d >= 2 else 0
    car = b + pk + toll if d >= 2 else 0
    if mode == 1:
        return min(car, 150000)
    return min(pas + car, 150000)

c = B.c; td = B.td; table = B.table
slug = 'tsukin-teate'; cta = 'tsukin'
title = '【通勤手当の非課税限度額】2026年はいくら？距離別の早見表と課税になる額の計算【令和8年4月改正】'
desc = '通勤手当の非課税限度額は、電車・バスの定期代なら月15万円まで、車・自転車なら片道の距離で月4,200円〜66,400円です。2026年4月から片道65km以上の区分と駐車場代の加算が足されました。手当の額と距離を入れると、非課税の額と課税になる額が分かります。'
upd = '更新日：2026年11月17日（国税庁 No.2582・No.2585 令和8年4月1日現在法令等）'

rows = []
labels = ['2km未満', '2km以上10km未満', '10km以上15km未満', '15km以上25km未満', '25km以上35km未満', '35km以上45km未満', '45km以上55km未満', '55km以上65km未満', '65km以上75km未満', '75km以上85km未満', '85km以上95km未満', '95km以上']
for i, (lb, (lim, amt)) in enumerate(zip(labels, BANDS)):
    new = i >= 8
    rows.append([td(lb, 'l'), td('全額課税' if amt == 0 else c(amt)), td('全額課税' if amt == 0 else c(amt + 5000)), td('2026年4月から' if new else '', 'c')])
tbl = table(['片道の通勤距離', '月の限度額<br>（円）', '駐車場代を<br>足した上限<br>（円）', '区分'], rows)

# 例:車通勤で毎月2万円の手当
ex = []
for d in (5, 12, 20, 30, 40, 50, 60, 70):
    L = limit(1, 0, d, 0, 0)
    t = max(0, 20000 - L)
    ex.append([td('%dkm' % d), td(c(L)), td(c(min(20000, L))), td(c(t)), td(c(t * 12))])
extbl = table(['片道の<br>距離', '限度額<br>（円）', '非課税<br>（円）', '課税<br>（円）', '1年で<br>課税（円）'], ex)

calc = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span>電車・バスは月15万円まで、車・自転車は片道の距離で月4,200円〜66,400円まで非課税です</div>
 <div class="in">
  <div class="full">
   <label>通勤の方法</label>
   <div class="seg seg3"><button type="button" class="on" data-k="0">電車・バス</button><button type="button" data-k="1">車・自転車</button><button type="button" data-k="2">両方</button></div>
  </div>
  <div class="full">
   <label for="pay">会社が払う通勤手当（1か月）</label>
   <div class="row"><input type="number" id="pay" inputmode="numeric" min="0" max="10000000" step="1" value="20000"><span>円</span></div>
  </div>
  <div class="full" id="w-pas">
   <label for="pas">一番安く合理的な経路の定期代（1か月）</label>
   <div class="row"><input type="number" id="pas" inputmode="numeric" min="0" max="10000000" step="1" value="18000"><span>円</span></div>
  </div>
  <div class="full hide" id="w-car">
   <label for="km">車・自転車で通う片道の距離</label>
   <div class="row"><input type="number" id="km" inputmode="decimal" min="0" max="500" step="0.1" value="12"><span>km</span></div>
   <label for="park">駐車場代（勤務先か駅の近く・本人が払う分・1か月）</label>
   <div class="row"><input type="number" id="park" inputmode="numeric" min="0" max="1000000" step="1" value="0"><span>円</span></div>
   <label for="toll">有料道路の料金（合理的な経路・1か月）</label>
   <div class="row"><input type="number" id="toll" inputmode="numeric" min="0" max="10000000" step="1" value="0"><span>円</span></div>
  </div>
 </div>
 <div class="vd" id="vd"><b id="o-vd"></b><span id="o-vds"></span></div>
 <div class="amt jdg">
  <div><small>非課税の限度額</small><b id="o-l"></b><em>1か月あたり</em></div>
  <div><small>課税になる額</small><b id="o-t"></b><em id="o-tn"></em></div>
 </div>
 <ul>
  <li id="o-how"></li>
  <li>非課税の判定は所得税の決まりです。社会保険料の計算では、通勤手当も全額が報酬に入ります</li>
 </ul>
</div>
'''

intro = '<p>通勤手当は、1か月の限度額までは所得税がかかりません。電車・バスの人は一番安く合理的な経路の定期代で、月15万円が上限です。<span class="mk">車・自転車の人は片道の距離で決まり、片道12kmなら月7,300円までです。</span>2026年4月1日以後に払う分から片道65km以上の区分が引き上げられ、駐車場代を月5,000円まで足せるようになりました。</p>\n'

toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#kyori">車・自転車の距離別の限度額</a></li>
  <li><a href="#densha">電車・バスの限度額（月15万円）</a></li>
  <li><a href="#rei">月2万円の手当なら課税はいくらか</a></li>
  <li><a href="#kaisei">2026年4月の改正で変わったこと</a></li>
  <li><a href="#chui">間違えやすいところ</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">通勤手当でよく聞かれること</a></li>
 </ol>
</nav>
'''

sec1 = ('<h2 id="kyori">車・自転車の距離別の限度額</h2>\n<p>マイカー・自転車・バイクで通う人は、片道の通勤距離で1か月の限度額が決まります。片道2km未満の人は全額が課税されます。</p>\n<p class="cap">2026年4月1日以後に払う通勤手当・1か月</p>\n'
        + tbl
        + '<p class="note" style="margin-top:8px">駐車場代を足せるのは、勤務先か通勤に使う駅などの近くの駐車場で本人が料金を払うのが通例の場合です。有料道路を使う人は、合理的な経路の料金を足して月15万円までです。</p>\n')
sec2 = ('<h2 id="densha">電車・バスの限度額（月15万円）</h2>\n<p>電車・バスで通う人は、一番安く合理的な経路と方法で通うときの定期代が非課税です。月15万円を超えるときは15万円までです。</p>\n'
        '<ul>\n <li>新幹線や特急を使っても、グリーン料金は含めません</li>\n <li>電車と車を両方使う人は、定期代と車の距離の限度額を足して月15万円までです</li>\n <li>6か月定期を払う会社は、1か月あたりの額で判定します</li>\n</ul>\n')
sec3 = ('<h2 id="rei">月2万円の手当なら課税はいくらか</h2>\n<p>車通勤の人に毎月2万円の通勤手当を払う場合です。限度額を超える分は給与として課税され、その月の給与に足して源泉徴収します。</p>\n<p class="cap">車・自転車・駐車場代なし・手当月20,000円</p>\n'
        + extbl
        + '<p class="note" style="margin-top:8px">片道25km以上なら月2万円は全額非課税です。片道12kmでは毎月12,700円・1年で152,400円が給与として課税されます。</p>\n')
sec4 = ('<h2 id="kaisei">2026年4月の改正で変わったこと</h2>\n<p>令和8年度の税制改正で、車・自転車で通う人の限度額が変わりました。2026年4月1日以後に払うべき通勤手当から使います。</p>\n'
        '<ul>\n <li>片道65km以上の区分を足し、65km以上75km未満は45,700円・95km以上は66,400円に引き上げた</li>\n <li>勤務先や駅の近くの駐車場代を、月5,000円まで限度額に足せるようにした</li>\n</ul>\n'
        '<p>2026年3月31日までに払うべきだった分を、あとから差額として払うときは改正前の限度額で判定します。</p>\n')
sec5 = ('<h2 id="chui">間違えやすいところ</h2>\n<h3>パート・アルバイトも同じ限度額</h3>\n<p>短い時間で働く人も、1か月あたりの限度額で判定します。出勤した日数が少なくても限度額は減りません。</p>\n'
        '<h3>最低賃金には含めない</h3>\n<p>通勤手当は、最低賃金と比べる賃金に含めません。基本給と毎月決まって払う手当だけで最低賃金を満たしているかを確かめます。</p>\n'
        '<h3>社会保険料は全額が対象</h3>\n<p>非課税になるのは所得税と住民税です。健康保険・厚生年金の標準報酬月額を決めるときは、通勤手当も全額を報酬に入れます。</p>\n')

rel_items = [
    ('genbutsu-kyuyo', '非課税の限度額の早見表', '食事代・社宅など、通勤手当のほかの非課税の限度もまとめています。'),
    ('gensen-hoshu', '源泉徴収の早見表', '限度額を超えた分は給与に足して源泉徴収します。'),
    ('nenmatsu-chosei', '年末調整の還付金の計算', '課税になった通勤手当も、年末調整で1年分の給与に入ります。'),
    ('shakaihoken', '社会保険料の早見表', '通勤手当は全額が標準報酬月額の報酬に入ります。'),
    ('yatou-hiyou', '人を雇う費用の計算', '人を1人雇うと、給料のほかに会社の負担がかかります。'),
    ('hoteifukurihi', '法定福利費の計算', '会社が払う社会保険料は、法定福利費として経費になります。'),
    ('saitei-chingin', '最低賃金の一覧', '通勤手当を除いた給料で、最低賃金を満たしているかを確かめます。'),
    ('tedori', '年収の手取りの早見表', '年収から税金と社会保険料を引いた手取りを、年収ごとに見られます。'),
    ('part-fuyou', 'パートの扶養の計算', '社会保険の扶養の判定では、通勤手当も年収に入ります。'),
    ('koyohoken', '雇用保険料の早見表', '雇用保険料も通勤手当を含めた賃金で計算します。'),
    ('yakuin-shataku', '役員社宅の家賃の計算', '社宅の家賃も、決まった額を払えば給与として課税されません。'),
]
sec6 = B.rel(slug, rel_items)

qa = ('<h2 id="qa">通勤手当でよく聞かれること</h2>\n'
      '<h3>通勤手当はいくらまで非課税ですか？</h3>\n<p>電車・バスは一番安く合理的な経路の定期代で月15万円までです。車・自転車は片道の距離で決まり、2km以上10km未満の月4,200円から95km以上の月66,400円までです。</p>\n'
      '<h3>片道2km未満の自転車通勤の手当は課税ですか？</h3>\n<p>はい。車・自転車で片道2km未満の人に払う通勤手当は、全額が給与として課税されます。</p>\n'
      '<h3>ガソリン代を実費で払うと非課税ですか？</h3>\n<p>実費でも距離の限度額までが非課税です。限度額を超えた分は給与として課税されます。</p>\n'
      '<h3>駐車場代の加算はいつからですか？</h3>\n<p>2026年4月1日以後に払うべき通勤手当からです。勤務先か駅などの近くの駐車場で、月5,000円が上限です。</p>\n'
      '<h3>非課税の通勤手当は社会保険料にかかりますか？</h3>\n<p>かかります。所得税が非課税でも、標準報酬月額を決める報酬には全額を入れます。雇用保険料の計算でも賃金に入ります。</p>\n')

src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2585.htm">国税庁 No.2585「マイカー・自転車通勤者の通勤手当」</a>（令和8年4月1日現在法令等）</li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2582.htm">国税庁 No.2582「電車・バス通勤者の通勤手当」</a>（令和8年4月1日現在法令等）</li>
  <li><a href="https://www.nta.go.jp/users/gensen/2026tsukin/index.htm">国税庁「通勤手当の非課税限度額の改正について」</a></li>
  <li><a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/chingin/newpage_43875.html">厚生労働省「最低賃金の対象となる賃金」</a></li>
  <li>所得税法第9条第1項第5号・所得税法施行令第20条の2</li>
 </ul>
</div>
'''

JS = r'''(function(){
 var BANDS=%s;
 var k=0,$=function(i){return document.getElementById(i)};
 function f(n){return Math.round(n).toLocaleString("ja-JP");}
 function num(i){var v=parseFloat($(i).value);return isNaN(v)?0:v;}
 function band(d){if(d<2)return 0;for(var i=0;i<BANDS.length;i++){if(d<BANDS[i][0])return BANDS[i][1];}return 66400;}
 function render(){
  $("w-pas").classList.toggle("hide",k===1);$("w-car").classList.toggle("hide",k===0);
  var pay=num("pay"),pas=num("pas"),d=num("km"),park=num("park"),toll=num("toll"),L,how;
  var b=band(d),pk=d>=2?Math.min(park,5000):0,car=d>=2?b+pk+toll:0;
  if(k===0){L=Math.min(pas,150000);how="定期代"+f(pas)+"円"+(pas>150000?"（月15万円が上限）":"")+"までが非課税です";}
  else if(k===1){L=Math.min(car,150000);how=d<2?"片道2km未満なので全額が課税されます":"片道"+d+"kmの限度額"+f(b)+"円"+(pk?"＋駐車場代"+f(pk)+"円":"")+(toll&&d>=2?"＋有料道路"+f(toll)+"円":"")+"です";}
  else{L=Math.min(pas+car,150000);how="定期代"+f(pas)+"円＋車・自転車の分"+f(car)+"円"+(pas+car>150000?"（月15万円が上限）":"")+"です";}
  var t=Math.max(0,pay-L);
  $("o-l").innerHTML=f(L)+"<i>円</i>";
  $("o-t").innerHTML=f(t)+"<i>円</i>";
  $("o-tn").textContent=t>0?"1年で"+f(t*12)+"円":"1か月あたり";
  var vd=$("vd");vd.className="vd"+(t>0?"":" no");
  if(t>0){$("o-vd").textContent="限度額を超えています";$("o-vds").textContent="毎月"+f(t)+"円が給与として課税されます。その月の給与に足して源泉徴収します";}
  else{$("o-vd").textContent="全額非課税です";$("o-vds").textContent="通勤手当"+f(pay)+"円は限度額"+f(L)+"円以内なので所得税はかかりません";}
  $("o-how").textContent=how;
 }
 ["pay","pas","km","park","toll"].forEach(function(i){$(i).addEventListener("input",render);});
 document.querySelectorAll(".seg button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".seg button").forEach(function(y){y.classList.remove("on");});b.classList.add("on");k=+b.dataset.k;render();});});
 render();
})();''' % json.dumps([[lim if lim < 10**9 else 99999, amt] for lim, amt in BANDS])

PIC = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="電車と車"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><rect x="10" y="14" width="22" height="26" rx="5" fill="#0f3d31"/><rect x="14" y="19" width="14" height="8" rx="1.5" fill="#d8efe6"/><circle cx="15.5" cy="34" r="2" fill="#e3b465"/><circle cx="26.5" cy="34" r="2" fill="#e3b465"/><path d="M34 40h20l-3-8H37z" fill="#e08a2c"/><rect x="32" y="40" width="24" height="7" rx="2" fill="#e08a2c"/><circle cx="38" cy="49" r="3" fill="#0f3d31"/><circle cx="50" cy="49" r="3" fill="#0f3d31"/></svg></div>'

body = calc + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n' + sec1 + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
h = B.page(slug, title, desc, upd, body, JS, cta, pic=PIC)
close_old = B.close_box(cta)
close_new = ('<div class="close"><p class="close-h"><span class="nw">通勤手当を含めた給与計算と、</span><span class="nw">帳簿と申告も</span></p>'
             '<p>通勤手当の非課税と課税の分け方は、毎月の源泉徴収と年末調整に響きます。記帳から決算・申告まで、まるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="tsukin_close_marunage">経理丸投げの無料相談</a></div>')
assert close_old in h
h = h.replace(close_old, close_new)
os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(h)

# 自分の計算の点検(ページを見ずに)
assert band(1.9) == 0 and band(2) == 4200 and band(9.9) == 4200 and band(10) == 7300 and band(64.9) == 38700 and band(65) == 45700 and band(95) == 66400 and band(200) == 66400
assert limit(1, 0, 12, 8000, 0) == 12300
assert limit(0, 200000, 0, 0, 0) == 150000
assert limit(2, 140000, 30, 5000, 0) == 150000
assert limit(1, 0, 1.5, 5000, 3000) == 0
print('ok', title)
