# 住民税の計算 /juminzei-keisan/ を作る。2026/11/23。
# 式と数字は tools/seikaku/juminzei_keisan_ref.py(前に原本で確かめた /juminzei/ /furusato/ /taishoku-jumin/ と同じ定数)。
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seikaku'))
import build_saitei as B
from juminzei_keisan_ref import jumin, shaho, tsuki, kyuyo

c = B.c; td = B.td; table = B.table
slug = 'juminzei-keisan'; cta = 'juminzeikeisan'
title = '【住民税の計算】年収と家族でいくら？毎月引かれる額と早見表【令和9年度】'
desc = '2026年の年収から、令和9年度（2027年6月から）の住民税と毎月の給料から引かれる額を計算します。配偶者・子ども・iDeCo・医療費控除を入力でき、年収150万円から1,500万円までの早見表も載せています。'
upd = '更新日：2026年11月23日（令和9年度の住民税・2026年の年収）'

def J(a, **k):
    return jumin(a, shaho(a), **k)

# ---- 早見表(年額・家族別) ----
ROWS = [1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 6000000, 7000000, 8000000, 9000000, 10000000, 12000000, 15000000]
CASES = [('単身', {}), ('配偶者あり', {'sp': 1}), ('配偶者と高校生', {'sp': 1, 'n1': 1}), ('配偶者と大学生', {'sp': 1, 'n2': 1})]
rows = []
for a in ROWS:
    rows.append([td(c(a // 10000) + '万')] + [td(c(J(a, **k)['y'])) for _, k in CASES])
sec1 = ('<h2 id="hayami">年収と家族で見る住民税の早見表</h2>\n'
        '<p>2026年の年収で決まる、令和9年度の住民税の1年分です。単位は円です。</p>\n'
        '<p class="cap">東京23区など・給与だけ・協会けんぽ東京都・40歳未満・令和9年度</p>\n'
        + table(['年収', '単身', '配偶者<br>あり', '配偶者と<br>高校生', '配偶者と<br>大学生'], rows)
        + '<p class="note" style="margin-top:8px">配偶者は配偶者控除を受ける人です。高校生は16歳から18歳の扶養親族で、大学生は19歳から22歳の扶養親族（特定扶養親族）です。'
        '社会保険料は2026年の各月の料率で計算し、賞与はない場合です。</p>\n')

# ---- 早見表(毎月の額・単身) ----
MR = [2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000, 10000000]
rows = []
for a in MR:
    y = J(a)['y']; j6, jm = tsuki(y)
    rows.append([td(c(a // 10000) + '万'), td(c(y)), td(c(j6)), td(c(jm))])
sec1b = ('<h2 id="tsuki">毎月の給料から引かれる住民税の早見表</h2>\n'
         '<p>会社員の住民税は、2027年6月から2028年5月までの12回に分けて給料から引かれます。</p>\n'
         '<p class="cap">単身・東京23区など・令和9年度・単位は円</p>\n'
         + table(['年収', '1年分', '6月分', '7月から<br>翌年5月の毎月'], rows)
         + '<p class="note" style="margin-top:8px">毎月の額は1年分を12で割り、100円未満を切り捨てた額です。切り捨てた端数は6月分に入ります。</p>\n')

# ---- 計算の箱 ----
D_A = 5000000
d = J(D_A); d6, dm = tsuki(d['y']); dsh = shaho(D_A)
def opt(idn, n):
    return '<select id="%s">%s</select>' % (idn, ''.join('<option value="%d"%s>%d人</option>' % (i, ' selected' if i == 0 else '', i) for i in range(n + 1)))
calc_html = ('<div class="sum" id="calc">\n <div class="h"><span>結論</span>年収と家族を入力すると、令和9年度の住民税と毎月の額を表示します</div>\n <div class="in">\n'
  '  <div class="full">\n   <label for="inc">2026年の年収（給与の額面）</label>\n   <div class="row"><input type="number" id="inc" inputmode="numeric" min="0" max="30000000" step="10000" value="%d"><span>円</span></div>\n'
  '   <input type="range" id="incr" min="0" max="20000000" step="10000" value="%d" aria-label="年収">\n  </div>\n'
  '  <div class="full">\n   <label>社会保険料（1年分）</label>\n   <div class="seg" id="s-sh"><button type="button" class="on" data-v="0">年収から計算する</button><button type="button" data-v="1">自分で入力する</button></div>\n'
  '   <div class="row" id="shw" style="display:none"><input type="number" id="sh" inputmode="numeric" min="0" step="1000" value="%d"><span>円</span></div>\n'
  '   <label>年齢</label>\n   <div class="seg" id="s-age"><button type="button" class="on" data-v="0">40歳未満</button><button type="button" data-v="1">40〜64歳</button></div>\n  </div>\n'
  '  <div class="full">\n   <label>配偶者控除を受ける配偶者</label>\n   <div class="seg" id="s-sp"><button type="button" class="on" data-v="0">いない</button><button type="button" data-v="1">いる</button></div>\n  </div>\n'
  '  <div><label for="n0">16歳未満の子</label>%s</div>\n  <div><label for="n1">16〜18歳の扶養親族</label>%s</div>\n'
  '  <div><label for="n2">19〜22歳の扶養親族</label>%s</div>\n  <div><label for="n3">23〜69歳の扶養親族</label>%s</div>\n'
  '  <div><label for="ide">iDeCoなどの掛金（1年分）</label><div class="row"><input type="number" id="ide" inputmode="numeric" min="0" step="1000" value="0"><span>円</span></div></div>\n'
  '  <div><label for="iry">医療費控除の額</label><div class="row"><input type="number" id="iry" inputmode="numeric" min="0" step="1000" value="0"><span>円</span></div></div>\n </div>\n'
  ' <div class="vd" id="vd"><b id="o-vd">住民税は1年%s円です</b><span id="o-vds">給料から引かれるのは6月が%s円・7月から翌年5月が毎月%s円です</span></div>\n'
  ' <div class="amt">\n  <div><small>住民税<br>（1年分）</small><b id="o-y">%s<i>円</i></b><em id="o-ye">令和9年度</em></div>\n'
  '  <div><small>6月分</small><b id="o-6">%s<i>円</i></b><em>最初の月</em></div>\n'
  '  <div><small>7月から<br>翌年5月</small><b id="o-m">%s<i>円</i></b><em>毎月</em></div>\n </div>\n'
  ' <ul>\n  <li id="o-br">内訳は、所得割%s円（市区町村%s円・都道府県%s円）・均等割と森林環境税5,000円です</li>\n'
  '  <li id="o-ks">給与所得%s円から社会保険料%s円と基礎控除など%s円を引いた課税所得%s円に10%%を掛け、調整控除を引いています</li>\n'
  '  <li>東京23区などの標準の税率（市区町村6%%・都道府県4%%）で計算しています。給与のほかに所得がある人や生命保険料控除などがある人は、この額と違います</li>\n </ul>\n</div>\n') % (
    D_A, D_A, dsh, opt('n0', 5), opt('n1', 5), opt('n2', 5), opt('n3', 5),
    c(d['y']), c(d6), c(dm), c(d['y']), c(d6), c(dm),
    c(d['sho']), c(d['shi']), c(d['ken']),
    c(d['g']), c(dsh), c(d['ded']), c(d['tr']))

intro = ('<p>住民税は、前の年の所得にかかる税金です。2026年の年収で決まるのが令和9年度の住民税で、会社員は2027年6月から1年かけて給料から引かれます。'
         '<span class="mk">年収500万円で単身なら住民税は1年%s円で、7月からは毎月%s円です。</span>'
         '配偶者や扶養している家族がいると控除が増えて、住民税は下がります。</p>\n') % (c(d['y']), c(dm))

toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#hayami">年収と家族で見る住民税の早見表</a></li>
  <li><a href="#tsuki">毎月の給料から引かれる住民税の早見表</a></li>
  <li><a href="#shikata">住民税の計算のしかた</a></li>
  <li><a href="#kojo">所得税と額が違う控除</a></li>
  <li><a href="#hikazei">住民税がかからない人</a></li>
  <li><a href="#chui">この計算に含めていないもの</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">住民税の計算でよく聞かれること</a></li>
 </ol>
</nav>
'''

# 計算のしかたの例(年収500万円・単身)
ex = d; exsh = dsh; exk = 430000
sec2 = ('<h2 id="shikata">住民税の計算のしかた</h2>\n'
        '<p>住民税は所得に応じてかかる所得割と、所得にかかわらず決まった額の均等割の合計です。</p>\n'
        '<ol>\n <li>年収から給与所得控除を引いた額が給与所得です</li>\n'
        ' <li>給与所得から社会保険料・基礎控除・配偶者控除・扶養控除などを引いた額が課税所得です（1,000円未満は切り捨て）</li>\n'
        ' <li>課税所得に10%（市区町村6%・都道府県4%）を掛け、調整控除を引いた額が所得割です（100円未満は切り捨て）</li>\n'
        ' <li>所得割に、均等割と森林環境税の5,000円を足します</li>\n</ol>\n'
        '<p>年収500万円・単身の例です（協会けんぽ東京都・40歳未満）。</p>\n'
        + table(['項目', '金額（円）'], [
            [td('年収', 'l'), td(c(D_A))],
            [td('給与所得', 'l'), td(c(ex['g']))],
            [td('社会保険料', 'l'), td(c(exsh))],
            [td('基礎控除', 'l'), td(c(exk))],
            [td('課税所得', 'l'), td(c(ex['tr']))],
            [td('所得割（調整控除を引いたあと）', 'l'), td(c(ex['sho']))],
            [td('均等割と森林環境税', 'l'), td('5,000')],
            [td('住民税（1年分）', 'l'), td(c(ex['y']))]])
        + '<p class="note" style="margin-top:8px">調整控除は所得税と住民税の控除の差をもとにした控除で、合計所得金額が2,500万円以下の人が受けられます。</p>\n')

sec3 = ('<h2 id="kojo">所得税と額が違う控除</h2>\n'
        '<p>住民税の控除は、所得税より低い額の控除があります。所得税がかからない人でも住民税がかかることがあるのは、このためです。</p>\n'
        + table(['控除', '住民税', '所得税（令和8年分）'], [
            [td('基礎控除', 'l'), td('43万円'), td('最大104万円')],
            [td('配偶者控除', 'l'), td('33万円'), td('38万円')],
            [td('扶養控除（16〜18歳・23〜69歳）', 'l'), td('33万円'), td('38万円')],
            [td('特定扶養控除（19〜22歳）', 'l'), td('45万円'), td('63万円')]])
        + '<p class="note" style="margin-top:8px">配偶者控除は本人の合計所得金額が900万円以下の場合の額です。住民税の配偶者控除は900万円超で22万円・950万円超で11万円・1,000万円超で0円です。基礎控除は合計所得金額が2,400万円を超えると下がります。</p>\n'
        '<p>16歳未満の子は扶養控除がありません。ただし住民税がかからない人の判定では、人数に入ります。</p>\n')

sec4 = ('<h2 id="hikazei">住民税がかからない人</h2>\n'
        '<p>合計所得金額が次の額以下なら、住民税はかかりません（東京23区などの1級地の基準）。扶養の人数には、配偶者と16歳未満の子も入ります。</p>\n'
        + table(['扶養の人数', '合計所得金額', '給与だけの年収'], [
            [td('0人（単身）', 'l'), td('45万円'), td('119万円')],
            [td('1人', 'l'), td('101万円'), td('175万円')],
            [td('2人', 'l'), td('136万円'), td('210万円')],
            [td('3人', 'l'), td('171万円'), td('255万9,999円')]])
        + '<p>扶養している家族がいる人は、合計所得金額が「35万円×（扶養の人数＋1）＋10万円＋32万円」以下なら所得割がかかりません。この額を少し超えた人は、所得割が減らされます。</p>\n')

sec5 = ('<h2 id="chui">この計算に含めていないもの</h2>\n'
        '<ul>\n <li>給与のほかの所得（副業・年金・不動産など）</li>\n'
        ' <li>生命保険料控除・地震保険料控除・ふるさと納税などの寄附金控除・住宅ローン控除</li>\n'
        ' <li>70歳以上の扶養親族・障害者控除・ひとり親控除・寡婦控除・勤労学生控除</li>\n'
        ' <li>配偶者特別控除（配偶者の所得が配偶者控除の基準を超える場合）</li>\n'
        ' <li>標準の税率と違う税率の自治体（名古屋市など）・均等割を上乗せしている自治体（神奈川県など）</li>\n</ul>\n'
        '<p>配偶者や扶養親族に当たるかどうかの所得の基準は、この計算では判定していません。</p>\n')

rel_items = [
    ('juminzei', '住民税の早見表', '住民税がかからない年収と、年収ごとの住民税を早見表で確かめられます。'),
    ('taishoku-jumin', '退職後の住民税の計算', '会社を辞めた翌年の住民税と、一括で払う額が分かります。'),
    ('furusato', 'ふるさと納税の限度額の計算', '住民税の所得割から、ふるさと納税の上限額の目安が分かります。'),
    ('tedori', '年収の手取りの早見表', '住民税・所得税・社会保険料を引いた手取りを、年収ごとに確かめられます。'),
    ('shotokuzei', '所得税の計算', '年収ごとの所得税と税率が分かります。'),
    ('nenmatsu-chosei', '年末調整の還付金の計算', '年末調整で戻る所得税の目安が分かります。'),
    ('kakutei-shinkoku-keisan', '確定申告シミュレーション', '医療費控除などで所得税がいくら戻るかが分かります。'),
    ('fukugyo', '副業の税金の計算', '副業の所得が加わると、住民税と所得税がいくら増えるかが分かります。'),
    ('nenshu-kabe', '年収の壁の早見表', '扶養から外れる年収と、手取りが減る年収の壁が分かります。'),
    ('iryohi-kojo', '医療費控除の計算', '医療費控除の額と、所得税と住民税がいくら減るかが分かります。'),
    ('shakaihoken', '社会保険料の早見表', '月給ごとの健康保険料と厚生年金保険料が分かります。'),
]
sec6 = B.rel(slug, rel_items)

q3 = J(3000000); q3s = J(3000000, sp=1); q8 = J(8000000); q8f = J(8000000, sp=1, n2=1)
q36, q3m = tsuki(q3['y'])
qa = ('<h2 id="qa">住民税の計算でよく聞かれること</h2>\n'
      '<h3>年収300万円の住民税はいくらですか？</h3>\n<p>東京23区などで単身なら、令和9年度の住民税は1年%s円です。給料からは6月に%s円、7月から翌年5月まで毎月%s円が引かれます。配偶者控除を受ける配偶者がいると1年%s円です。</p>\n'
      '<h3>年収800万円の住民税はいくらですか？</h3>\n<p>単身なら1年%s円です。配偶者控除を受ける配偶者と大学生の子が1人いると、1年%s円です。</p>\n'
      '<h3>住民税はいつから払いますか？</h3>\n<p>2026年の年収で決まる令和9年度の住民税は、会社員なら2027年6月の給料から引かれます。会社員でない人は、市区町村から届く納税通知書で6月・8月・10月・翌年1月の4回に分けて払います。</p>\n'
      '<h3>6月の住民税だけ高いのはなぜですか？</h3>\n<p>1年分を12で割ったときの100円未満の端数を、6月分にまとめるからです。</p>\n'
      '<h3>16歳未満の子がいると住民税は下がりますか？</h3>\n<p>16歳未満の子には扶養控除がないので、所得割は下がりません。ただし住民税がかからない人の判定では人数に入るので、年収が低い人はかからなくなることがあります。</p>\n') % (
    c(q3['y']), c(q36), c(q3m), c(q3s['y']), c(q8['y']), c(q8f['y']))

src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.tax.metro.tokyo.lg.jp/kazei/kojin_ju">東京都主税局「個人住民税」</a></li>
  <li><a href="https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/czaisei_seido/150790_06.html">総務省「個人住民税」</a></li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm">国税庁 タックスアンサー No.1410 給与所得控除</a></li>
  <li><a href="https://www.nta.go.jp/users/gensen/2026kiso/pdf/0026005-024.pdf">国税庁「令和8年度税制改正（所得税の基礎控除の引上げ等関係）Q＆A」</a></li>
  <li><a href="https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08">全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます」</a></li>
  <li>表の金額は、上の資料の控除・税率・料率をもとに計算しています。</li>
 </ul>
</div>
'''

# ---- JS(juminzei_keisan_ref.py と同じ式) ----
JS = r'''(function(){
 function kyuyo(x){
  if(x<741000)return 0;
  if(x<2191000)return x-740000;
  if(x<2193000)return 1451000;
  if(x<2196000)return 1453000;
  if(x<2200000)return 1456000;
  if(x<6600000){var A=Math.floor(x/4000)*4000;return x<3600000?A/4000*2800-80000:A/4000*3200-440000;}
  if(x<8500000)return Math.floor(x*9/10)-1100000;
  return x-1950000;
 }
 var G=[[58,63],[68,73],[78,83],[88,93],[98,101],[104,107],[110,114],[118,122],[126,130],[134,138],[142,146],[150,155],[160,165],[170,175],[180,185],[190,195],[200,210],[220,230],[240,250],[260,270],[280,290],[300,310],[320,330],[340,350],[360,370],[380,395],[410,425],[440,455],[470,485],[500,515],[530,545],[560,575],[590,605],[620,635],[650,665],[680,695],[710,730],[750,770],[790,810],[830,855],[880,905],[930,955],[980,1005],[1030,1055],[1090,1115],[1150,1175],[1210,1235],[1270,1295],[1330,1355],[1390,1e9]];
 function std(m){for(var i=0;i<G.length;i++){if(m<G[i][1]*1000)return G[i][0]*1000;}return 1390000;}
 function hu(n,d){var q=Math.floor(n/d),r=n-q*d;return (r*2>d)?q+1:q;}
 function shaho(a,old){var m=Math.floor(a/12),s=std(m),p=Math.min(Math.max(s,88000),650000),t=0;
  for(var k=1;k<=12;k++){var hr=k<=2?991:(k===3?985:1008),kai=old?(k<=2?159:162):0,ko=k<=3?55:50;t+=hu(s*(hr+kai),20000)+hu(p*1830,20000)+hu(m*ko,10000);}return t;}
 function jumin(a,sh,o){
  var g=kyuyo(a);
  if(a>8500000&&(o.n0+o.n1+o.n2)>0)g=Math.max(0,g-Math.ceil((Math.min(a,10000000)-8500000)/10));
  var N=o.sp+o.n0+o.n1+o.n2+o.n3,kl=350000*(N+1)+100000+(N?210000:0),sl=350000*(N+1)+100000+(N?320000:0);
  var r={g:g,kin:0,sho:0,shi:0,ken:0,y:0,tr:0,kind:0,ded:0};
  if(g<=kl)return r;
  r.kin=5000;r.kind=1;
  var kiso=g<=24000000?430000:(g<=24500000?290000:(g<=25000000?150000:0));
  var spk=o.sp?(g<=9000000?330000:(g<=9500000?220000:(g<=10000000?110000:0))):0,spd=o.sp?(g<=9000000?50000:(g<=9500000?40000:(g<=10000000?20000:0))):0;
  var oth=o.ide+o.iry+kiso+spk+330000*(o.n1+o.n3)+450000*o.n2,tr=Math.floor(Math.max(0,g-sh-oth)/1000)*1000;
  r.tr=tr;r.ded=oth;
  if(g<=sl){r.y=5000;return r;}
  var diff=50000+spd+50000*(o.n1+o.n3)+180000*o.n2,adj=g>25000000?0:(tr<=2000000?Math.min(diff,tr):Math.max(diff-(tr-2000000),50000));
  var s0=Math.max(0,Math.floor(tr*6/100)-Math.floor(adj*3/100)),k0=Math.max(0,Math.floor(tr*4/100)-Math.floor(adj*2/100));
  var cap=g-sl,tot=s0+k0,shi,ken;
  if(tot>cap){shi=Math.floor(s0*cap/(tot*100))*100;ken=Math.floor(k0*cap/(tot*100))*100;}
  else{shi=Math.floor(s0/100)*100;ken=Math.floor(k0/100)*100;}
  r.shi=shi;r.ken=ken;r.sho=shi+ken;r.y=shi+ken+5000;r.kind=(shi+ken)?2:1;return r;
 }
 function tsuki(y){if(y<=5000)return [y,0];var m=Math.floor(Math.floor(y/12)/100)*100;return [y-m*11,m];}
 function f(n){return n.toLocaleString("ja-JP");}
 function v(id){return Math.max(0,parseInt(String(document.getElementById(id).value).replace(/[^0-9]/g,""),10)||0);}
 var inc=document.getElementById("inc"),incr=document.getElementById("incr"),own=0,old=0,sp=0;
 window.__jk=function(a,sh,o){return jumin(a,sh<0?shaho(a,o.old||0):sh,o);};window.__jsh=shaho;
 function render(){
  var a=Math.min(30000000,v("inc")),sh=own?v("sh"):shaho(a,old);
  var o={sp:sp,n0:+document.getElementById("n0").value,n1:+document.getElementById("n1").value,n2:+document.getElementById("n2").value,n3:+document.getElementById("n3").value,ide:v("ide"),iry:v("iry")};
  var r=jumin(a,sh,o),t=tsuki(r.y);
  document.getElementById("o-y").innerHTML=f(r.y)+"<i>円</i>";
  document.getElementById("o-6").innerHTML=f(t[0])+"<i>円</i>";
  document.getElementById("o-m").innerHTML=f(t[1])+"<i>円</i>";
  document.getElementById("vd").className=r.y?"vd":"vd no";
  document.getElementById("o-vd").textContent=r.y?"住民税は1年"+f(r.y)+"円です":"住民税はかかりません";
  document.getElementById("o-vds").textContent=r.y===0?"合計所得金額が住民税のかからない基準以下です":(r.y<=5000?"所得割はかからず、均等割と森林環境税の5,000円だけです。会社員は6月の給料でまとめて引かれます":"給料から引かれるのは6月が"+f(t[0])+"円・7月から翌年5月が毎月"+f(t[1])+"円です");
  document.getElementById("o-br").textContent=r.y===0?"所得割も均等割もかかりません":"内訳は、所得割"+f(r.sho)+"円（市区町村"+f(r.shi)+"円・都道府県"+f(r.ken)+"円）・均等割と森林環境税5,000円です";
  document.getElementById("o-ks").textContent=r.kind===0?"給与所得は"+f(r.g)+"円です":"給与所得"+f(r.g)+"円から社会保険料"+f(sh)+"円と基礎控除など"+f(r.ded)+"円を引いた課税所得"+f(r.tr)+"円に10%を掛け、調整控除を引いています";
 }
 inc.addEventListener("input",function(){incr.value=inc.value;render();});
 incr.addEventListener("input",function(){inc.value=incr.value;render();});
 ["sh","ide","iry"].forEach(function(id){document.getElementById(id).addEventListener("input",render);});
 ["n0","n1","n2","n3"].forEach(function(id){document.getElementById(id).addEventListener("change",render);});
 function seg(id,cb){var bs=document.querySelectorAll("#"+id+" button");bs.forEach(function(b){b.addEventListener("click",function(){bs.forEach(function(x){x.classList.remove("on");});b.classList.add("on");cb(+b.dataset.v);render();});});}
 seg("s-sh",function(x){own=x;document.getElementById("shw").style.display=x?"":"none";if(x)document.getElementById("sh").value=shaho(Math.min(30000000,v("inc")),old);});
 seg("s-age",function(x){old=x;});seg("s-sp",function(x){sp=x;});
 render();
})();'''

PIC = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="家と円"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><path d="M12 30 28 16l16 14v20H12z" fill="#0f3d31"/><rect x="23" y="36" width="10" height="14" fill="#eef6f2"/><circle cx="46" cy="42" r="10" fill="#e3b465"/><text x="46" y="47" font-size="13" font-weight="700" text-anchor="middle" fill="#0f3d31" font-family="sans-serif">円</text></svg></div>'

VD_CSS = '<style>.vd{background:#ffffff;color:#0f3d31;border-left:8px solid #00775a;border-radius:6px;padding:14px 16px;margin:0 0 12px}.vd.no{border-left-color:#6b7472}.vd b{display:block;font-size:24px;line-height:1.4;font-weight:700;color:#00775a}.vd span{display:block;font-size:14px;line-height:1.6;margin-top:4px}#calc select{width:100%}@media(max-width:519px){#calc .amt{grid-template-columns:1fr 1fr!important}#calc .amt>div:first-child{grid-column:1/-1}}</style>\n'

body = B.hy_wrap(sec1 + sec1b) + calc_html + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
h = B.page(slug, title, desc, upd, body, JS, cta, pic=PIC, auth=B.auth_box('総務省・東京都主税局と国税庁'))
h = h.replace('</head>', VD_CSS + '</head>', 1)
close_old = B.close_box(cta)
close_new = ('<div class="close"><p class="close-h"><span class="nw">給料から住民税を引く会社の、</span><span class="nw">給与計算と帳簿も</span></p>'
             '<p>住民税の特別徴収や年末調整から、記帳・決算・申告までをまるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="juminzeikeisan_close_marunage">経理丸投げの無料相談</a></div>')
assert close_old in h
h = h.replace(close_old, close_new)
os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(h)
print('ok', title)
for a in ROWS: print(a, [J(a, **k)['y'] for _, k in CASES])
