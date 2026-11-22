# 手取りから年収を逆算 /tedori-gyakusan/ を作る。2026/11/22。
# 数字と式は /tedori/ と同じ(2026/11/21 の全ツール点検で原本と照らした式)。
#  協会けんぽ 令和8年度の47都道府県の料率・介護1.62%・子ども・子育て支援金0.23%・厚生年金18.3%(上限65万円)・等級50・本人負担は50銭以下切り捨て
#  雇用保険 令和8年度 一般の事業の労働者負担1,000分の5
#  国税庁 No.1410(令和8年分の給与所得控除)・令和8年分の基礎控除・No.2260 速算表・復興特別所得税2.1%・100円未満切り捨て
#  住民税 令和9年度(所得割10%・均等割と森林環境税5,000円・基礎控除43万円の段・調整控除・東京23区の単身は合計所得45万円以下が非課税)
# 逆算:月給(額面)を100円きざみで上げていき、1年の手取り÷12(1円未満切り捨て)が目標以上になる一番低い月給。賞与なし。
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_saitei as B

c = B.c; td = B.td; table = B.table
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# /tedori/ の突き合わせ(ページを見ずに書いた式)をそのまま使う
src_t = open(os.path.join(ROOT, 'tools', 'seikaku', 'tedori.py'), encoding='utf-8').read()
src_t = src_t[:src_t.index('def r_half_up')].replace('from _lib import run', '')
T = {'__file__': os.path.join(ROOT, 'tools', 'seikaku', 'tedori.py')}
exec(compile(src_t, 'tedori_ref', 'exec'), T)
ref = T['ref']; PREF = T['PREF']
TOKYO = 985

def tedori(m, rate=TOKYO, old=0):
    return ref(m * 12, rate, old)

def gyaku_m(target, rate=TOKYO, old=0):
    """月の手取りが target 円以上になる一番低い月給(100円きざみ)。"""
    m = (target + 99) // 100 * 100
    while tedori(m, rate, old)['t'] // 12 < target:
        m += 100
    return m

def gyaku_y(target, rate=TOKYO, old=0):
    """1年の手取りが target 円以上になる一番低い月給(100円きざみ)。"""
    m = (target // 12 + 99) // 100 * 100
    while tedori(m, rate, old)['t'] < target:
        m += 100
    return m

def pct1(net, a):
    v = (net * 1000 * 2 + a) // (2 * a)
    return '%d.%d' % (v // 10, v % 10)

slug = 'tedori-gyakusan'; cta = 'gyakusan'
title = '【手取り年収の逆算】手取り月20万・30万に必要な額面は？月給と年収の早見表【2026年】'
desc = '月の手取りや1年の手取りから、必要な額面の月給と年収を逆算します。手取り15万円から50万円までの早見表と、都道府県・年齢を選べる計算付きです。2026年（令和8年分）の税金と令和8年度の社会保険料で計算しています。'
upd = '更新日：2026年11月22日（令和8年分の税制・令和8年度の保険料率）'

# ---- 早見表(月の手取り) ----
MT = [150000, 180000, 200000, 220000, 250000, 280000, 300000, 330000, 350000, 400000, 450000, 500000]
rows = []; MR = {}
for t in MT:
    m = gyaku_m(t); e = tedori(m); MR[t] = (m, e)
    rows.append([td(c(t)), td(c(m)), td(c(m * 12)), td(c(m - e['t'] // 12)), td(pct1(e['t'], m * 12) + '%')])
hy_m = rows
sec1 = ('<h2 id="hayami">月の手取りから見る額面の早見表</h2>\n'
        '<p>月の手取りがこの額になる、一番低い額面の月給です。年収は月給の12か月分で、賞与はない場合です。</p>\n'
        '<p class="cap">単身・協会けんぽ東京都・40歳未満・2026年</p>\n'
        + table(['月の手取り<br>（円）', '必要な月給<br>（額面・円）', '年収<br>（円）', '引かれる額<br>（月・円）', '手取り率'], hy_m)
        + '<p class="note" style="margin-top:8px">月の手取りは、1年の手取りを12で割った額です（1円未満は切り捨て）。月給は100円単位です。住民税は前の年も同じ年収だった場合の額です。</p>\n')

# ---- 早見表(1年の手取り) ----
YT = [2000000, 2500000, 3000000, 3500000, 4000000, 5000000, 6000000, 7000000, 8000000, 10000000]
rows = []; YR = {}
for t in YT:
    m = gyaku_y(t); e = tedori(m); YR[t] = (m, e)
    rows.append([td(c(t // 10000) + '万円'), td(c(m * 12)), td(c(m)), td(c(m * 12 - e['t']))])
hy_y = rows
sec1b = ('<h2 id="nen">1年の手取りから見る年収の早見表</h2>\n'
         '<p class="cap">単身・協会けんぽ東京都・40歳未満・賞与なし・2026年</p>\n'
         + table(['1年の手取り', '必要な年収<br>（円）', '月給<br>（円）', '引かれる額<br>（年・円）'], hy_y))

# ---- 計算の箱 ----
D_T = 300000
dm, de = MR[D_T]
opts = ''.join('<option value="%d"%s>%s（%s%%）</option>' % (i, ' selected' if p == '東京都' else '', p, '%d.%02d' % (r // 100, r % 100)) for i, (p, r) in enumerate(PREF))
calc_html = ('<div class="sum" id="calc">\n <div class="h"><span>結論</span>ほしい手取りを入力すると、必要な額面の月給と年収を表示します</div>\n <div class="in">\n'
  '  <div class="full">\n   <label>入力する手取り</label>\n   <div class="seg" id="s-kind"><button type="button" class="on" data-v="0">月の手取り</button><button type="button" data-v="1">1年の手取り</button></div>\n'
  '   <label for="tg" id="tg-l">ほしい月の手取り</label>\n   <div class="row"><input type="number" id="tg" inputmode="numeric" min="0" max="36000000" step="1000" value="%d"><span>円</span></div>\n  </div>\n'
  '  <div class="full">\n   <label>年齢</label>\n   <div class="seg" id="s-age"><button type="button" class="on" data-a="0">40歳未満</button><button type="button" data-a="1">40〜64歳</button></div>\n'
  '   <label for="pref">勤め先の都道府県（協会けんぽ）</label>\n   <select id="pref">%s</select>\n  </div>\n </div>\n'
  ' <div class="vd" id="vd"><b id="o-vd">必要な月給は%s円です</b><span id="o-vds">年収にすると%s円です（賞与なし）</span></div>\n'
  ' <div class="amt">\n  <div><small>必要な月給<br>（額面）</small><b id="o-m">%s<i>円</i></b><em>100円単位</em></div>\n'
  '  <div><small>年収<br>（12か月分）</small><b id="o-y">%s<i>円</i></b><em id="o-yr">手取り率%s%%</em></div>\n'
  '  <div><small>引かれる額<br>（1か月）</small><b id="o-d">%s<i>円</i></b><em>税金と保険料</em></div>\n </div>\n'
  ' <ul>\n  <li id="o-br">1か月の内訳は、社会保険料%s円・所得税%s円・住民税%s円です（1年分を12で割った額）</li>\n'
  '  <li id="o-tt">この月給の手取りは月%s円です</li>\n'
  '  <li>単身・給与だけ・賞与なしで、住民税は東京23区の基準で前の年も同じ年収だった場合の額です</li>\n </ul>\n</div>\n') % (
    D_T, opts, c(dm), c(dm * 12), c(dm), c(dm * 12), pct1(de['t'], dm * 12), c(dm - de['t'] // 12),
    c(de['s'] // 12), c(de['i'] // 12), c(de['j'] // 12), c(de['t'] // 12))

intro = ('<p>手取りは、額面の給料から社会保険料・所得税・住民税を引いた額です。<span class="mk">手取り月30万円には額面でおよそ%s万円の月給が要ります。</span>引かれる額は年収が上がるほど割合が増えるので、手取りを1.25倍するような決まった掛け算では出せません。このページは額面を少しずつ上げて手取りを計算し、ほしい手取りに届く一番低い額面を出しています。</p>\n') % c((dm + 5000) // 10000)

toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#hayami">月の手取りから見る額面の早見表</a></li>
  <li><a href="#nen">1年の手取りから見る年収の早見表</a></li>
  <li><a href="#shikata">逆算のしかた</a></li>
  <li><a href="#utiwake">手取り30万円の内訳</a></li>
  <li><a href="#chui">手取りが表と変わる人</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">手取りの逆算でよく聞かれること</a></li>
 </ol>
</nav>
'''

sec2 = ('<h2 id="shikata">逆算のしかた</h2>\n'
        '<ol>\n <li>額面の月給から、健康保険料・厚生年金保険料・雇用保険料を引きます。健康保険と厚生年金は標準報酬月額の等級で決まります</li>\n'
        ' <li>年収から給与所得控除・社会保険料・基礎控除を引いた課税所得に、所得税の税率を掛けます</li>\n'
        ' <li>住民税は課税所得のおよそ10%に、均等割と森林環境税の5,000円を足した額です</li>\n'
        ' <li>額面から1から3を引いた額が手取りです。額面を100円ずつ上げて、ほしい手取りに届く一番低い額面を探します</li>\n</ol>\n'
        '<p>社会保険料は等級で段になっているので、等級が上がる境目のすぐ上では額面が増えても手取りが少し減ることがあります。表の月給はほしい手取りに初めて届く額です。</p>\n')

e30 = de
sec3 = ('<h2 id="utiwake">手取り30万円の内訳</h2>\n'
        '<p>手取り月30万円に届く月給%s円の人の1か月です（単身・協会けんぽ東京都・40歳未満）。</p>\n' % c(dm)
        + table(['項目', '1か月（円）'], [
            [td('額面の月給', 'l'), td(c(dm))],
            [td('健康保険料', 'l'), td(c(e30['k'] // 12))],
            [td('厚生年金保険料', 'l'), td(c(e30['n'] // 12))],
            [td('雇用保険料', 'l'), td(c(e30['e'] // 12))],
            [td('所得税', 'l'), td(c(e30['i'] // 12))],
            [td('住民税', 'l'), td(c(e30['j'] // 12))],
            [td('手取り', 'l'), td(c(e30['t'] // 12))]])
        + '<p class="note" style="margin-top:8px">所得税と住民税は1年分を12で割った額です（1円未満は切り捨て）。給与明細の所得税は毎月の源泉徴収税額表で引かれ、年末調整で1年分に合わせます。</p>\n')

sec4 = ('<h2 id="chui">手取りが表と変わる人</h2>\n'
        '<ul>\n <li>40歳から64歳の人：介護保険料がかかるので、同じ手取りに必要な額面が上がります</li>\n'
        ' <li>東京都以外の協会けんぽの人：健康保険の料率が違います。上の計算で都道府県を選べます</li>\n'
        ' <li>社会人1年目の人：前の年に所得が無ければ住民税がかからないので、手取りは表より多くなります</li>\n'
        ' <li>賞与がある人：年収が同じでも月給が下がるので、社会保険料と月の手取りが変わります</li>\n'
        ' <li>扶養している家族がいる人：扶養控除や配偶者控除で税金が下がり、必要な額面が下がります</li>\n'
        ' <li>通勤手当がある人：非課税の限度額までは税金がかかりませんが、社会保険料の計算には入ります</li>\n</ul>\n')

rel_items = [
    ('tedori', '年収の手取りの早見表', '年収100万円から2,000万円までの手取りと引かれる額を、早見表で確かめられます。'),
    ('shakaihoken', '社会保険料の早見表', '月給ごとの健康保険料と厚生年金保険料を、都道府県別に確かめられます。'),
    ('koyohoken', '雇用保険料の早見表', '令和8年度の雇用保険料率と、月給ごとの本人負担が分かります。'),
    ('shotokuzei', '所得税の計算', '年収ごとの所得税と税率を早見表で確かめられます。'),
    ('juminzei', '住民税の早見表', '年収ごとの住民税と、住民税がかからない年収が分かります。'),
    ('shoyo-shotokuzei', '賞与の所得税の計算', '賞与から引かれる所得税と社会保険料を計算できます。'),
    ('nenshu-kabe', '年収の壁の早見表', '扶養から外れる年収と、手取りが減る年収の壁が分かります。'),
    ('yakuin-tedori', '役員報酬の手取りの早見表', '社長の役員報酬から手取りを確かめられます。'),
    ('fukugyo', '副業の税金の計算', '本業の手取りに副業の所得が加わると、税金がいくら増えるかが分かります。'),
    ('kakutei-shinkoku-keisan', '確定申告シミュレーション', '医療費控除やふるさと納税で、所得税がいくら戻るかが分かります。'),
    ('tsukin-teate', '通勤手当の非課税限度額', '通勤距離ごとの非課税の限度額が分かります。'),
]
sec6 = B.rel(slug, rel_items)

m20 = MR[200000][0]; m25 = MR[250000][0]; m30 = MR[300000][0]
y300 = YR[3000000][0] * 12; y500 = YR[5000000][0] * 12
qa = ('<h2 id="qa">手取りの逆算でよく聞かれること</h2>\n'
      '<h3>手取り20万円の額面はいくらですか？</h3>\n<p>単身・協会けんぽ東京都・40歳未満なら、額面の月給%s円で手取りが20万円に届きます。年収にすると%s円です。</p>\n'
      '<h3>手取り30万円の額面と年収はいくらですか？</h3>\n<p>同じ条件で、額面の月給%s円・年収%s円です。手取り25万円なら月給%s円です。</p>\n'
      '<h3>手取り年収300万円・500万円に必要な年収はいくらですか？</h3>\n<p>賞与なしの場合は手取り300万円に年収%s円が要ります。手取り500万円なら年収%s円です。</p>\n'
      '<h3>手取りは額面の何割ですか？</h3>\n<p>月給20万円から40万円の人は、額面のおよそ8割が手取りです。年収が上がると所得税の税率が上がるので、手取りの割合は下がります。</p>\n'
      '<h3>社会人1年目でも同じですか？</h3>\n<p>住民税は前の年の所得にかかります。前の年に所得が無かった1年目の人は住民税がかからないので、同じ額面でも手取りは表より多くなります。</p>\n') % (
    c(m20), c(m20 * 12), c(m30), c(m30 * 12), c(m25), c(y300), c(y500))

src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf">国税庁「令和8年度税制改正（所得税の基礎控除の引上げ等関係）Q＆A」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm">国税庁 タックスアンサー No.1410 給与所得控除</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm">国税庁 タックスアンサー No.2260 所得税の税率</a></li>
  <li><a href="https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08">全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます」</a></li>
  <li><a href="https://www.mhlw.go.jp/content/001692566.pdf">厚生労働省「令和8年度 雇用保険料率のご案内」</a></li>
  <li><a href="https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html">総務省「個人住民税」</a></li>
  <li>表の金額は、上の資料の控除・税率・料率をもとに計算しています。</li>
 </ul>
</div>
'''

# JS:/tedori/ の関数をそのまま写す
th = open(os.path.join(B.SITE, 'tedori', 'index.html'), encoding='utf-8').read()
def grab(name_start, name_end):
    i = th.index(name_start); j = th.index(name_end, i)
    return th[i:j]
pf = re.search(r'var PF=\[\[.*?\]\];', th).group(0)
core = grab('function kyuyo(x){', 'function f(n){')
assert 'function all(a,old)' in core and 'PF[+pref.value]' in core
JS = (r'''(function(){
 ''' + pf + r'''
 var pref=document.getElementById("pref"),old=0,kind=0;
 ''' + core + r'''
 function f(n){return n.toLocaleString("ja-JP");}
 function gm(t){var m=Math.ceil(t/100)*100;while(Math.floor(all(m*12,old).t/12)<t)m+=100;return m;}
 function gy(t){var m=Math.ceil(Math.floor(t/12)/100)*100;while(all(m*12,old).t<t)m+=100;return m;}
 window.__gyaku=function(t,k,pi,o){pref.value=String(pi);old=o;var m=k?gy(t):gm(t),x=all(m*12,o);return {m:m,t:x.t,s:x.s,i:x.i,j:x.j};};
 var tg=document.getElementById("tg");
 function render(){
  var t=Math.min(36000000,Math.max(0,parseInt(String(tg.value).replace(/[^0-9]/g,""),10)||0));
  var m=kind?gy(t):gm(t),a=m*12,x=all(a,old),mt=Math.floor(x.t/12);
  document.getElementById("o-vd").textContent="必要な月給は"+f(m)+"円です";
  document.getElementById("o-vds").textContent="年収にすると"+f(a)+"円です（賞与なし）";
  document.getElementById("o-m").innerHTML=f(m)+"<i>円</i>";
  document.getElementById("o-y").innerHTML=f(a)+"<i>円</i>";
  document.getElementById("o-yr").textContent="手取り率"+(a?(Math.round(x.t/a*1000)/10).toFixed(1):"0.0")+"%";
  document.getElementById("o-d").innerHTML=f(m-mt)+"<i>円</i>";
  document.getElementById("o-br").textContent="1か月の内訳は、社会保険料"+f(Math.floor(x.s/12))+"円・所得税"+f(Math.floor(x.i/12))+"円・住民税"+f(Math.floor(x.j/12))+"円です（1年分を12で割った額）";
  document.getElementById("o-tt").textContent=kind?"この年収の手取りは1年"+f(x.t)+"円です":"この月給の手取りは月"+f(mt)+"円です";
 }
 tg.addEventListener("input",render);
 pref.addEventListener("change",render);
 document.querySelectorAll("#s-age button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll("#s-age button").forEach(function(x){x.classList.remove("on");});b.classList.add("on");old=+b.dataset.a;render();});});
 document.querySelectorAll("#s-kind button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll("#s-kind button").forEach(function(x){x.classList.remove("on");});b.classList.add("on");kind=+b.dataset.v;document.getElementById("tg-l").textContent=kind?"ほしい1年の手取り":"ほしい月の手取り";tg.value=kind?"3600000":"300000";render();});});
 render();
})();''')

PIC = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="手取りから額面へ戻る矢印"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><rect x="12" y="34" width="16" height="16" rx="2" fill="#0f3d31"/><rect x="36" y="16" width="16" height="34" rx="2" fill="#0f3d31"/><path d="M18 28c2-10 10-14 18-12" fill="none" stroke="#e3b465" stroke-width="3.5" stroke-linecap="round"/><path d="M32 12l5 4-5 5" fill="none" stroke="#e3b465" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'

VD_CSS = '<style>.vd{background:#ffffff;color:#0f3d31;border-left:8px solid #00775a;border-radius:6px;padding:14px 16px;margin:0 0 12px}.vd b{display:block;font-size:24px;line-height:1.4;font-weight:700;color:#00775a}.vd span{display:block;font-size:14px;line-height:1.6;margin-top:4px}@media(max-width:519px){#calc .amt{grid-template-columns:1fr 1fr!important}#calc .amt>div:first-child{grid-column:1/-1}}</style>\n'

body = B.hy_wrap(sec1 + sec1b) + calc_html + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + sec6 + '\n' + qa + '\n' + src
h = B.page(slug, title, desc, upd, body, JS, cta, pic=PIC, auth=B.auth_box('国税庁と協会けんぽ'))
h = h.replace('</head>', VD_CSS + '</head>', 1)
close_old = B.close_box(cta)
close_new = ('<div class="close"><p class="close-h"><span class="nw">人を雇う会社の、</span><span class="nw">給与計算と帳簿も</span></p>'
             '<p>給料の額面と手取りの計算から、記帳・決算・申告までをまるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="gyakusan_close_marunage">経理丸投げの無料相談</a></div>')
assert close_old in h
h = h.replace(close_old, close_new)
os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(h)

print('ok', title)
for t in MT: print('月', t, MR[t][0], MR[t][1]['t'] // 12)
for t in YT: print('年', t, YR[t][0] * 12, YR[t][1]['t'])
