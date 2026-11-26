# 給与明細の差引支給額 /kyuyo-meisai/ を作る。2026-11-26。
# 使い方: リポジトリの直下で python3 tools/build_kyuyo_meisai.py
# 数字: 協会けんぽ令和8年度・厚生年金18.3%・雇用保険令和8年度・国税庁の月額表の電算機計算（令和8年分）
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

GR = [(58,63),(68,73),(78,83),(88,93),(98,101),(104,107),(110,114),(118,122),(126,130),(134,138),(142,146),(150,155),(160,165),(170,175),(180,185),(190,195),(200,210),(220,230),(240,250),(260,270),(280,290),(300,310),(320,330),(340,350),(360,370),(380,395),(410,425),(440,455),(470,485),(500,515),(530,545),(560,575),(590,605),(620,635),(650,665),(680,695),(710,730),(750,770),(790,810),(830,855),(880,905),(930,955),(980,1005),(1030,1055),(1090,1115),(1150,1175),(1210,1235),(1270,1295),(1330,1355),(1390,10**9)]
PF = [("北海道",1028),("青森県",985),("岩手県",951),("宮城県",1010),("秋田県",1001),("山形県",975),("福島県",950),("茨城県",952),("栃木県",982),("群馬県",968),("埼玉県",967),("千葉県",973),("東京都",985),("神奈川県",992),("新潟県",921),("富山県",959),("石川県",970),("福井県",971),("山梨県",955),("長野県",963),("岐阜県",980),("静岡県",961),("愛知県",993),("三重県",977),("滋賀県",988),("京都府",989),("大阪府",1013),("兵庫県",1012),("奈良県",991),("和歌山県",1006),("鳥取県",986),("島根県",994),("岡山県",1005),("広島県",978),("山口県",1015),("徳島県",1024),("香川県",1002),("愛媛県",998),("高知県",1005),("福岡県",1011),("佐賀県",1055),("長崎県",1006),("熊本県",1008),("大分県",1008),("宮崎県",977),("鹿児島県",1013),("沖縄県",944)]
EI = [("一般の事業", 50), ("農林水産・清酒製造の事業", 60), ("建設の事業", 60)]
U = 120000
TAX = [(162500,5105,0),(275000,10210,8296),(579166,20420,36374),(750000,23483,54113),(1500000,33693,130688),(3333333,40840,237893),(0,45945,408061)]

def r50d(n, d):
    q, r = divmod(int(n), int(d))
    return q + (1 if r * 2 > d else 0)

def std(m):
    for s, hi in GR:
        if m < hi * 1000:
            return s * 1000
    return 1390000

def parts(pay, tsukin, rate, old, ei):
    """本人負担。健康保険・厚生年金・雇用保険。rate は協会けんぽの料率（10000分率・支援金の前）。"""
    base = max(0, pay) + max(0, tsukin)
    s = std(base)
    p = min(max(s, 88000), 650000)
    ken = r50d(s * (rate + 23 + (162 if old else 0)), 20000)
    nen = r50d(p * 1830, 20000)
    koy = r50d(base * ei, 10000)
    return s, ken, nen, koy

def cl(n, d):
    r = n % d
    return (n - r) // d + (1 if r else 0)

def tax(monthly_after, hg):
    """月額表の電算機計算。monthly_after は社会保険料を引いた月の課税支給額。戻りは月の所得税。"""
    a = max(0, monthly_after) * 12 * 10000
    if a <= 158333 * U:
        ky = 54167
    elif a <= 299999 * U:
        ky = cl(a * 3 + 66670 * U, 10 * U)
    elif a <= 549999 * U:
        ky = cl(a * 2 + 366670 * U, 10 * U)
    elif a <= 708330 * U:
        ky = cl(a + 916670 * U, 10 * U)
    else:
        ky = 162500
    if a <= 2120833 * U:
        ki = 48334
    elif a <= 2162499 * U:
        ki = 40000
    elif a <= 2204166 * U:
        ki = 26667
    elif a <= 2245833 * U:
        ki = 13334
    else:
        ki = 0
    b = max(a - (ky + ki + 31667 * hg) * U, 0)
    r = TAX[6]
    for i in range(6):
        if b <= TAX[i][0] * U:
            r = TAX[i]
            break
    dn = U * 100000
    n = b * r[1] - r[2] * dn
    if n < 0:
        n = 0
    return ((2 * n + 10 * dn) // (20 * dn)) * 10

def slip(pay, tsukin=0, rate=985, old=0, hg=0, ju=0, ei=50):
    s, ken, nen, koy = parts(pay, tsukin, rate, old, ei)
    sha = ken + nen + koy
    zei = tax(max(0, pay) - sha, hg)
    net = pay + tsukin - sha - zei - ju
    return dict(std=s, ken=ken, nen=nen, koy=koy, sha=sha, zei=zei, net=net)

def c(n):
    return '{:,}'.format(n)

def check_commas(html):
    text = re.sub(r'<script\b.*?</script>', '', html, flags=re.S)
    text = re.sub(r'<style\b.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<[^>]+>', '\n', text)
    bad = []
    for line in text.split('\n'):
        line = re.sub(r'「[^」]*」', '「」', line)
        for sen in line.split('。'):
            if sen.count('、') >= 2:
                bad.append(sen.strip())
    return bad

JS = r'''(function(){
 var GR=[[58,63],[68,73],[78,83],[88,93],[98,101],[104,107],[110,114],[118,122],[126,130],[134,138],[142,146],[150,155],[160,165],[170,175],[180,185],[190,195],[200,210],[220,230],[240,250],[260,270],[280,290],[300,310],[320,330],[340,350],[360,370],[380,395],[410,425],[440,455],[470,485],[500,515],[530,545],[560,575],[590,605],[620,635],[650,665],[680,695],[710,730],[750,770],[790,810],[830,855],[880,905],[930,955],[980,1005],[1030,1055],[1090,1115],[1150,1175],[1210,1235],[1270,1295],[1330,1355],[1390,1e9]];
 var PF=__PF__, EI=[[50],[60],[60]];
 var U=120000, TAX=[[162500,5105,0],[275000,10210,8296],[579166,20420,36374],[750000,23483,54113],[1500000,33693,130688],[3333333,40840,237893],[0,45945,408061]];
 function $(i){return document.getElementById(i)}
 function f(n){return Math.round(n).toLocaleString("ja-JP")}
 function r50d(n,d){var q=Math.floor(n/d),r=n%d;return r*2>d?q+1:q}
 function std(m){for(var i=0;i<GR.length;i++){if(m<GR[i][1]*1000)return GR[i][0]*1000}return 1390000}
 function cl(n,d){var r=n%d;return (n-r)/d+(r>0?1:0)}
 function tax(m,hg){var a=Math.max(0,m)*12*10000,ky;
  if(a<=158333*U)ky=54167;else if(a<=299999*U)ky=cl(a*3+66670*U,10*U);else if(a<=549999*U)ky=cl(a*2+366670*U,10*U);else if(a<=708330*U)ky=cl(a+916670*U,10*U);else ky=162500;
  var ki=a<=2120833*U?48334:a<=2162499*U?40000:a<=2204166*U?26667:a<=2245833*U?13334:0;
  var b=Math.max(a-(ky+ki+31667*hg)*U,0),r=TAX[6];
  for(var i=0;i<6;i++){if(b<=TAX[i][0]*U){r=TAX[i];break}}
  var dn=BigInt(U)*100000n,n=BigInt(b)*BigInt(r[1])-BigInt(r[2])*dn;
  if(n<0n)n=0n;
  return Number((2n*n+10n*dn)/(20n*dn))*10}
 function num(i){var v=parseInt($(i).value,10);return v>0?v:0}
 function go(pay,tsukin,rate,old,hg,ju,ei){
  var base=pay+tsukin,s=std(base),p=Math.min(Math.max(s,88000),650000);
  var ken=r50d(s*(rate+23+(old?162:0)),20000),nen=r50d(p*1830,20000),koy=r50d(base*ei,10000);
  var sha=ken+nen+koy,zei=tax(pay-sha,hg),net=pay+tsukin-sha-zei-ju;
  return {std:s,ken:ken,nen:nen,koy:koy,sha:sha,zei:zei,net:net}}
 window.__kyuyo=go;
 var old=0,hg=0,ei=0;
 function render(){
  var pay=Math.min(num("pay"),2000000),tsu=Math.min(num("tsukin"),500000),ju=Math.min(num("ju"),500000);
  var rate=PF[+$("pref").value][1],g=go(pay,tsu,rate,old,hg,ju,EI[ei][0]);
  $("o-net").innerHTML=f(g.net)+"<i>円</i>";
  $("o-lead").textContent="月給"+f(pay)+"円の差引支給額は"+f(g.net)+"円です";
  $("o-ken").textContent=f(g.ken)+"円";
  $("o-nen").textContent=f(g.nen)+"円";
  $("o-ei").textContent=f(g.koy)+"円";
  $("o-zei").textContent=f(g.zei)+"円";
  $("o-ju").textContent=f(ju)+"円";
  $("o-std").textContent="標準報酬月額 "+f(g.std)+"円";
  $("o-sha").textContent="社会保険料の合計 "+f(g.sha)+"円";
 }
 ["pay","tsukin","ju"].forEach(function(i){$(i).addEventListener("input",render)});
 $("pref").addEventListener("change",render);
 $("fuyo").addEventListener("change",function(){hg=+$("fuyo").value;render()});
 function seg(id,set){$(id).addEventListener("click",function(ev){var b=ev.target.closest("button");if(!b)return;set(+b.getAttribute("data-v"));var bs=$(id).querySelectorAll("button");for(var i=0;i<bs.length;i++)bs[i].className=bs[i]===b?"on":"";render()})}
 seg("s-old",function(v){old=v});
 seg("s-ei",function(v){ei=v});
 render();
})();'''

def hayami_rows(old):
    rows = []
    for pay in (200000, 250000, 300000, 350000, 400000, 500000):
        g = slip(pay, rate=985, old=old)
        hit = ' class="hit"' if pay == 300000 else ''
        rows.append('<tr%s><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><b>%s</b></td></tr>' % (
            hit, c(pay), c(g['std']), c(g['sha']), c(g['zei']), c(g['net'])))
    return '\n'.join(rows)

def table(rows, tid):
    return ('<div class="tw">\n<table id="%s">\n <thead><tr><th>月給<br>（円）</th><th>標準報酬<br>月額</th><th>社会保険料<br>（円）</th><th>所得税<br>（円）</th><th>差引支給額<br>（円）</th></tr></thead>\n <tbody>\n%s\n </tbody>\n</table>\n</div>\n' % (tid, rows))

def build():
    import build_saitei as b
    g = slip(300000)
    g40 = slip(300000, old=1)
    kaigo = g40['ken'] - g['ken']
    opts = ''.join('<option value="%d"%s>%s</option>' % (i, ' selected' if n == '東京都' else '', n) for i, (n, _) in enumerate(PF))
    hay = ('<h2 id="list">月給ごとの差引支給額</h2>\n'
           '<p>月給20万円から50万円まで、差引支給額を並べました。東京都の協会けんぽ・扶養0人・通勤手当なし・住民税なし・一般の事業です。40歳未満と40〜64歳を分けています。</p>\n'
           '<h3>40歳未満</h3>\n<p class="cap">介護保険料なし</p>\n' + table(hayami_rows(0), 'tb0') +
           '<h3>40〜64歳（介護保険料あり）</h3>\n<p class="cap">健康保険に介護保険料を含む</p>\n' + table(hayami_rows(1), 'tb1') +
           '<p class="note" style="margin-top:8px">社会保険料は標準報酬月額に料率をかけ、50銭以下は切り捨て・50銭を超えると切り上げています。所得税は社会保険料を引いた月給に、令和8年の給与で使う月額表の電算機計算をかけた額です。</p>\n')
    calc = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span><span id="o-lead">月給の差引支給額</span></div>
 <div class="amt">
  <div><small>差引支給額</small><b id="o-net">―</b><em id="o-std">標準報酬月額</em></div>
  <div><small>社会保険料</small><b id="o-sha">―</b><em>健康保険・厚生年金・雇用保険</em></div>
  <div><small>所得税</small><b id="o-zei">―</b><em>今月の天引き</em></div>
 </div>
 <div class="in">
  <div class="full">
   <label for="pay">月給（課税される支給。通勤手当を除く）</label>
   <div class="row"><input type="number" id="pay" inputmode="numeric" min="0" max="2000000" step="1000" value="300000"><span>円</span></div>
  </div>
  <div class="full">
   <label for="tsukin">通勤手当（所得税では非課税でも社会保険の報酬に入ります）</label>
   <div class="row"><input type="number" id="tsukin" inputmode="numeric" min="0" max="500000" step="1000" value="0"><span>円</span></div>
  </div>
  <div class="full">
   <label for="pref">勤め先の都道府県（協会けんぽ）</label>
   <select id="pref">%s</select>
  </div>
  <div class="full">
   <label>年齢</label>
   <div class="seg" id="s-old"><button type="button" class="on" data-v="0">40歳未満</button><button type="button" data-v="1">40〜64歳</button></div>
  </div>
  <div class="full">
   <label for="fuyo">扶養親族の数（甲欄）</label>
   <select id="fuyo"><option value="0" selected>0人</option><option value="1">1人</option><option value="2">2人</option><option value="3">3人</option><option value="4">4人</option><option value="5">5人</option><option value="6">6人</option><option value="7">7人</option></select>
  </div>
  <div class="full">
   <label for="ju">住民税（市区町村の通知額。今月天引きする額）</label>
   <div class="row"><input type="number" id="ju" inputmode="numeric" min="0" max="500000" step="100" value="0"><span>円</span></div>
  </div>
  <div class="full">
   <label>雇用保険の業種</label>
   <div class="seg seg3" id="s-ei"><button type="button" class="on" data-v="0">一般</button><button type="button" data-v="1">農林水産・清酒</button><button type="button" data-v="2">建設</button></div>
  </div>
 </div>
 <ul>
  <li>健康保険料 <b id="o-ken">―</b></li>
  <li>厚生年金 <b id="o-nen">―</b></li>
  <li>雇用保険 <b id="o-ei">―</b></li>
  <li>住民税 <b id="o-ju">―</b></li>
  <li>甲欄（主たる給与）です。乙欄・賞与・残業代は含めていません</li>
 </ul>
</div>
''' % opts
    intro = ('<p>給与明細の差引支給額は、総支給額から社会保険料・所得税・住民税を引いた額です。このページは月給の人の甲欄で計算します。</p>\n'
             '<p>東京都・40歳未満・扶養0人・通勤手当なし・住民税なし・月給30万円なら、差引支給額は%s円です。社会保険料は%s円で所得税は%s円です。</p>\n' % (c(g['net']), c(g['sha']), c(g['zei'])))
    toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#list">月給ごとの差引支給額</a></li>
  <li><a href="#shaho">社会保険料の出し方</a></li>
  <li><a href="#zei">所得税の出し方</a></li>
  <li><a href="#jumin">住民税は通知額を入力する</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">給与明細でよく聞かれること</a></li>
 </ol>
</nav>
'''
    sec_shaho = ('<h2 id="shaho">社会保険料の出し方</h2>\n'
                 '<p>健康保険と厚生年金は、月給と通勤手当を足した額を標準報酬月額に当てはめます。子ども・子育て支援金0.23%は健康保険料率に含めてから、本人と会社で半分ずつにします。</p>\n'
                 '<p>40〜64歳は介護保険料1.62%も健康保険料に含みます。厚生年金は18.3%の半分で、標準報酬月額は8万8千円以上65万円以下に揃えます。</p>\n'
                 '<p>雇用保険は標準報酬月額ではなく、月給と通勤手当を足した実額にかけます。一般の事業の本人負担は1000分の5です。農林水産・清酒製造と建設は1000分の6です。</p>\n'
                 '<p>会社負担は給与明細の差引支給額には出ません。端数は50銭以下を切り捨て、50銭を超えると切り上げます。</p>\n')
    sec_zei = ('<h2 id="zei">所得税の出し方</h2>\n'
               '<p>令和8年分の所得税は、12月の年末調整で新しい基礎控除に精算します。それまでの給与から天引きする税額は、改正前の月額表です。</p>\n'
               '<p>このページの所得税は、その月額表の電算機計算です。社会保険料を引いた月給から給与所得控除と基礎控除と扶養の額を引き、税率をかけます。扶養親族1人の額は月31,667円です。税額は10円単位です。</p>\n'
               '<p>通勤手当は限度額まで所得税の対象に入れず、社会保険料の計算にだけ入れます。残業代と賞与は入れていません。</p>\n')
    sec_ju = ('<h2 id="jumin">住民税は通知額を入力する</h2>\n'
              '<p>住民税は前年の所得で市区町村が決めた額を、6月から翌年5月まで天引きします。今月の月給だけでは計算できないので、通知書の額を入力します。</p>\n'
              '<p>入力が0円のときは住民税を引かずに出します。早見表も住民税なしの額です。</p>\n')
    rels = [
        ('tedori', '年収の手取りの早見表', '年収から税金と社会保険料を引いた1年の手取りを見られます。'),
        ('shakaihoken', '社会保険料の早見表', '標準報酬月額ごとの社会保険料を見られます。'),
        ('koyohoken', '雇用保険料の早見表', '雇用保険料は業種ごとの率で、賞与にもかかります。'),
        ('nenmatsu-chosei', '年末調整の還付', '12月の年末調整で、毎月天引きした税額との差を精算します。'),
        ('tsukin-teate', '通勤手当の非課税限度額', '通勤手当は所得税の限度額まで非課税です。'),
        ('nenshu-kabe', '年収の壁', '扶養に入る年収の壁は、月給を12倍した額の目安で見ます。'),
    ]
    sec_rel = b.rel('kyuyo-meisai', rels)
    qa = ('<h2 id="qa">給与明細でよく聞かれること</h2>\n'
          '<h3>月給30万円の差引支給額はいくらですか？</h3>\n'
          '<p>東京都・40歳未満・扶養0人・通勤手当なし・住民税なしなら、%s円です。社会保険料%s円と所得税%s円を引いた額です。</p>\n' % (c(g['net']), c(g['sha']), c(g['zei']))
          + '<h3>通勤手当は社会保険に入りますか？</h3>\n'
          '<p>所得税では限度額まで非課税でも、社会保険の報酬には入ります。このページは通勤手当を標準報酬月額と雇用保険に含め、所得税の対象には含めていません。</p>\n'
          + '<h3>40歳になると差引支給額はいくら減りますか？</h3>\n'
          '<p>40〜64歳は介護保険料が加わります。東京都で月給30万円・扶養0人なら、介護保険料の本人負担は%s円です。</p>\n' % c(kaigo)
          + '<h3>住民税を0円のままにしてよいですか？</h3>\n'
          '<p>通知が無い月や入社した年の6月より前は、天引きが0円のことがあります。通知額がある月は、その額を入力してください。</p>\n')
    src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/denshi_01.pdf">国税庁「令和8年分 月額表の甲欄を適用する給与等に対する税額の電算機計算の特例について」</a></li>
  <li><a href="https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08">全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます」</a></li>
  <li><a href="https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogaku.html">日本年金機構「厚生年金保険料額表」</a>（18.3%）</li>
  <li><a href="https://www.mhlw.go.jp/content/001692566.pdf">厚生労働省「令和8年度 雇用保険料率のご案内」</a></li>
 </ul>
</div>
'''
    body = b.hy_wrap(hay) + calc + '\n' + b.share('kyuyo-meisai') + '\n' + intro + '\n' + toc + '\n' + sec_shaho + '\n' + sec_zei + '\n' + sec_ju + '\n' + sec_rel + '\n' + qa + '\n' + src
    title = '【給与明細】月給の差引支給額はいくら？社会保険料と所得税の計算【令和8年】'
    desc = '月給から健康保険料・厚生年金・雇用保険・所得税・住民税を引いた差引支給額を計算します。東京都ほか協会けんぽの令和8年度の料率と、令和8年の給与で使う月額表で出します。'
    upd = '更新日：2026年11月26日（国税庁・全国健康保険協会・日本年金機構・厚生労働省）'
    js = JS.replace('__PF__', json.dumps(PF, ensure_ascii=False))
    html = b.page('kyuyo-meisai', title, desc, upd, body, js, 'kyuyo', auth=b.auth_box('国税庁・全国健康保険協会（協会けんぽ）・日本年金機構・厚生労働省'))
    close = ('<div class="close"><p class="close-h"><span class="nw">給与明細の数字も、</span><span class="nw">帳簿と申告も</span></p>'
             '<p>毎月の給料から引く税金と社会保険料は、年末調整と決算の数字につながります。記帳から決算・申告まで、まるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="kyuyo_close_marunage">経理丸投げの無料相談</a></div>')
    html = re.sub(r'<div class="close">.*?</div>', close, html, count=1, flags=re.S)
    bad = check_commas(html)
    if bad:
        raise SystemExit('読点が2つ: ' + ' / '.join(bad[:8]))
    path = os.path.join(ROOT, 'site', 'kyuyo-meisai', 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)
    wire()
    print('kyuyo-meisai', g['net'], g['sha'], g['zei'])

def wire():
    pj = os.path.join(ROOT, 'tools', 'pages.json')
    raw = open(pj, encoding='utf-8').read()
    if '/kyuyo-meisai/' not in raw:
        raw = raw.rstrip()
        if not raw.endswith(']'):
            raise SystemExit('pages.json')
        raw = raw[:-1].rstrip() + ',\n {\n  "path": "/kyuyo-meisai/",\n  "label": "給与明細の差引支給額",\n  "kw": "給与明細 手取り 差引支給額 月給 社会保険料 所得税"\n }\n]\n'
        open(pj, 'w', encoding='utf-8').write(raw)
    hj = os.path.join(ROOT, 'tools', 'hayami_first.json')
    h = json.load(open(hj, encoding='utf-8'))
    if 'kyuyo-meisai' not in h:
        h['kyuyo-meisai'] = 'list'
        json.dump(h, open(hj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        open(hj, 'a', encoding='utf-8').write('\n')
    sm = os.path.join(ROOT, 'site', 'sitemap.xml')
    sx = open(sm, encoding='utf-8').read()
    if '/kyuyo-meisai/' not in sx:
        line = '<url><loc>https://taxtable.jp/kyuyo-meisai/</loc><lastmod>2026-11-26</lastmod></url>\n'
        sx = sx.replace('</urlset>', line + '</urlset>')
        open(sm, 'w', encoding='utf-8').write(sx)
    note = '月給から社会保険料と所得税を引いた差引支給額を計算します。'
    label = '給与明細の差引支給額'
    for slug in ('tedori', 'shakaihoken', 'koyohoken', 'nenmatsu-chosei'):
        fp = os.path.join(ROOT, 'site', slug, 'index.html')
        s = open(fp, encoding='utf-8').read()
        if '/kyuyo-meisai/' in s:
            continue
        li = '<li>%s<a href="/kyuyo-meisai/" data-cta="rel_%s_kyuyo-meisai">%s</a></li>' % (note, slug, label)
        s2, n = re.subn(r'(<ul class="rl">.*?)(</ul>)', lambda m: m.group(1) + li + m.group(2), s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('関連リンクを足せない ' + slug)
        open(fp, 'w', encoding='utf-8').write(s2)

if __name__ == '__main__':
    if '--check' in sys.argv:
        g = slip(300000)
        print(g)
        print('40', slip(300000, old=1))
        print('fuyo1', slip(300000, hg=1)['zei'])
        print('tsu', slip(300000, tsukin=20000))
        print('osaka', slip(300000, rate=1013)['sha'])
        print('ei60', slip(300000, ei=60)['koy'])
        print('ju', slip(300000, ju=12000)['net'])
    else:
        build()
