# 借用書テンプレート（金額を入力すると文面と印紙税を表示する）。
# 原本:国税庁 No.7140 印紙税額の一覧表（第1号文書・令和8年4月1日現在法令等）
#       国税庁 No.7101 消費貸借に関する契約書
# 使い方:リポジトリの直下で python3 tools/build_shakuyo.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_saitei as B

# (この金額以下, 税額)。1円以上で、どれにも入らなければ50億円超の60万円。0円以下は金額の記載なし。
BANDS = [
    (9999, 0, '1万円未満'),
    (100000, 200, '1万円以上10万円以下'),
    (500000, 400, '10万円超50万円以下'),
    (1000000, 1000, '50万円超100万円以下'),
    (5000000, 2000, '100万円超500万円以下'),
    (10000000, 10000, '500万円超1,000万円以下'),
    (50000000, 20000, '1,000万円超5,000万円以下'),
    (100000000, 60000, '5,000万円超1億円以下'),
    (500000000, 100000, '1億円超5億円以下'),
    (1000000000, 200000, '5億円超10億円以下'),
    (5000000000, 400000, '10億円超50億円以下'),
]


def stamp(yen):
    if yen is None or yen <= 0:
        return 200, '金額の記載がないもの'
    for top, tax, name in BANDS:
        if yen <= top:
            return tax, name
    return 600000, '50億円超'


def interest(amount, rate, days):
    """年利は百分率。日数は貸した日の翌日から返す日まで。1年は365日。1円未満切り捨て。"""
    bp = int(round(float(rate) * 100))
    if amount <= 0 or bp <= 0 or days <= 0:
        return 0
    return amount * bp * days // 3650000


def yen(n):
    return '{:,}'.format(n)


def close_box(cta):
    return ('<div class="close"><p class="close-h"><span class="nw">借用書を書いたあとの、</span><span class="nw">帳簿と申告も</span></p>'
            '<p>お金の貸し借りは、帳簿の借入金と利息に残ります。記帳から決算・申告まで、まるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
            '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="%s_close_marunage">経理丸投げの無料相談</a></div>') % cta


JS = r'''(function(){
 var BANDS=[[9999,0,"1万円未満"],[100000,200,"1万円以上10万円以下"],[500000,400,"10万円超50万円以下"],[1000000,1000,"50万円超100万円以下"],[5000000,2000,"100万円超500万円以下"],[10000000,10000,"500万円超1,000万円以下"],[50000000,20000,"1,000万円超5,000万円以下"],[100000000,60000,"5,000万円超1億円以下"],[500000000,100000,"1億円超5億円以下"],[1000000000,200000,"5億円超10億円以下"],[5000000000,400000,"10億円超50億円以下"]];
 var $=function(i){return document.getElementById(i)};
 function f(n){return Math.round(n).toLocaleString("ja-JP");}
 function num(i){var v=parseFloat($(i).value);return isNaN(v)?0:v;}
 function esc(s){return String(s||"").replace(/[<>&]/g,"").replace(/\s+/g," ").trim().slice(0,40);}
 function stamp(yen){
  if(!(yen>0)) return [200,"金額の記載がないもの"];
  for(var i=0;i<BANDS.length;i++) if(yen<=BANDS[i][0]) return [BANDS[i][1],BANDS[i][2]];
  return [600000,"50億円超"];
 }
 function days(a,b){
  if(!a||!b) return 0;
  var A=new Date(a+"T00:00:00+09:00"),B=new Date(b+"T00:00:00+09:00");
  var d=Math.round((B-A)/86400000);
  return d>0?d:0;
 }
 function interest(amount,rate,d){
  var bp=Math.round(rate*100);
  if(!(amount>0)||bp<=0||!(d>0)) return 0;
  return Number((BigInt(Math.round(amount))*BigInt(bp)*BigInt(d))/3650000n);
 }
 function ymd(s){
  if(!s) return "";
  var p=s.split("-");
  return (+p[0])+"年"+(+p[1])+"月"+(+p[2])+"日";
 }
 function render(){
  var amount=Math.round(num("amt")),rate=num("rate"),d=days($("d1").value,$("d2").value);
  var st=stamp(amount),tax=st[0],band=st[1],intr=interest(amount,rate,d);
  var lender=esc($("lender").value)||"貸した人",borrower=esc($("borrower").value)||"借りた人",guar=esc($("guar").value);
  var lump=$("how").value==="1";
  $("o-tax").innerHTML=(tax?f(tax):"0")+"<i>円</i>";
  $("o-band").textContent=tax?band:(amount>0?"非課税":band);
  $("o-int").innerHTML=f(intr)+"<i>円</i>";
  $("o-intn").textContent=rate<=0?"無利息":"年"+rate+"%・"+d+"日";
  var vd=$("vd");
  if(amount>0&&tax===0){vd.className="vd no";$("o-vd").textContent="印紙税はかかりません";$("o-vds").textContent="1万円未満の借用書は非課税です";}
  else if(tax===0){vd.className="vd no";$("o-vd").textContent="金額を書いてください";$("o-vds").textContent="金額の記載がない借用書は200円です";}
  else{$("vd").className="vd";$("o-vd").textContent="印紙税は"+f(tax)+"円です";$("o-vds").textContent=band+"の区分です。紙1通ごとに貼ります";}
  var lines=[];
  lines.push("借用書");
  lines.push("");
  lines.push(lender+"から金"+(amount>0?f(amount):"（金額）")+"円を借り受けました。たしかに受け取りました。");
  lines.push("");
  lines.push("1. 借りた日は"+($("d1").value?ymd($("d1").value):"（日付）")+"です。");
  lines.push("2. 返す日は"+($("d2").value?ymd($("d2").value):"（日付）")+"です。");
  if(rate<=0) lines.push("3. 利息は付けません。");
  else lines.push("3. 利息は年"+rate+"%です。合計は"+f(intr)+"円です。");
  if(lump) lines.push("4. 元金は返す日に一括で返します。");
  else{
   var months=Math.max(1,Math.round(d/30));
   var per=amount>0?Math.floor(amount/months):0;
   lines.push("4. 元金は毎月に分けて返します。1か月の元金の目安は"+f(per)+"円です。");
  }
  if(guar) lines.push("5. "+guar+"は借りた人と連帯して保証します。");
  lines.push("");
  lines.push(($("d1").value?ymd($("d1").value):"（日付）"));
  lines.push("借りた人　"+borrower);
  $("o-doc").textContent=lines.join("\n");
 }
 ["amt","rate","d1","d2","lender","borrower","guar","how"].forEach(function(i){$(i).addEventListener("input",render);$(i).addEventListener("change",render);});
 render();
})();'''


def main():
    B.close_box = close_box
    slug = 'shakuyo'
    title = '【借用書テンプレート】金額を入力すると文面と印紙税を表示する'
    desc = '借用書の文面と印紙税を、借りる金額から計算します。1万円未満は非課税で、100万円ちょうどは1,000円、300万円は2,000円です。紙1通ごとにかかり、データを送るだけで紙を作らないときはかかりません。'
    upd = '更新日：2026年11月27日（国税庁 No.7140 令和8年4月1日現在法令等）'
    rows = []
    for top, tax, name in BANDS:
        rows.append([B.td(name, 'l'), B.td('非課税' if tax == 0 else yen(tax) + '円')])
    rows.append([B.td('50億円超', 'l'), B.td('600,000円')])
    rows.append([B.td('金額の記載がないもの', 'l'), B.td('200円')])
    sec1 = ('<h2 id="list">借用書の印紙税はいくらか（金額の区分）</h2>\n'
            '<p>紙の借用書は、契約金額で印紙税が決まります。下の表は国税庁の印紙税額の一覧表（No.7140）の第1号文書です。</p>\n'
            '<p class="cap">消費貸借に関する契約書・1通あたり</p>\n'
            + B.table(['契約金額', '印紙税'], rows)
            + '<p class="note" style="margin-top:8px">不動産の売買契約にある軽減は、借用書にはありません。金額を書かない借用書は200円です。2通作るときは2通分です。</p>\n')
    calc = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span>300万円の借用書の印紙税は2,000円です</div>
 <div class="amt">
  <div><small>印紙税<br>1通</small><b id="o-tax">2,000<i>円</i></b><em id="o-band">100万円超500万円以下</em></div>
  <div><small>利息の<br>合計</small><b id="o-int">0<i>円</i></b><em id="o-intn">無利息</em></div>
 </div>
 <div class="in">
  <div class="full">
   <label for="amt">借りる金額</label>
   <div class="row"><input type="number" id="amt" inputmode="numeric" min="0" max="100000000000" step="1" value="3000000"><span>円</span></div>
  </div>
  <div>
   <label for="lender">貸した人</label>
   <input type="text" id="lender" maxlength="40" value="貸主株式会社">
  </div>
  <div>
   <label for="borrower">借りた人</label>
   <input type="text" id="borrower" maxlength="40" value="借主 一郎">
  </div>
  <div>
   <label for="d1">借りた日</label>
   <input type="date" id="d1" value="2026-04-01">
  </div>
  <div>
   <label for="d2">返す日</label>
   <input type="date" id="d2" value="2027-03-31">
  </div>
  <div>
   <label for="rate">年利（0なら無利息）</label>
   <div class="row"><input type="number" id="rate" inputmode="decimal" min="0" max="100" step="0.01" value="0"><span>%</span></div>
  </div>
  <div>
   <label for="how">返し方</label>
   <select id="how"><option value="1" selected>返す日に一括で返す</option><option value="2">毎月に分けて返す</option></select>
  </div>
  <div class="full">
   <label for="guar">連帯保証人（空なら書きません）</label>
   <input type="text" id="guar" maxlength="40" value="">
  </div>
 </div>
 <div class="vd" id="vd"><b id="o-vd">印紙税は2,000円です</b><span id="o-vds">100万円超500万円以下の区分です。紙1通ごとに貼ります</span></div>
 <div id="o-doc" style="white-space:pre-wrap;background:#f4f7f6;border:1px solid #d5e2dc;border-radius:8px;padding:14px 16px;line-height:1.9;margin-top:12px">借用書

貸主株式会社から金3,000,000円を借り受けました。たしかに受け取りました。

1. 借りた日は2026年4月1日です。
2. 返す日は2027年3月31日です。
3. 利息は付けません。
4. 元金は返す日に一括で返します。

2026年4月1日
借りた人　借主 一郎</div>
 <ul>
  <li>日数は借りた日の翌日から返す日までです。1年は365日として1円未満を切り捨てます</li>
  <li>この文面は記入例です。契約の条件は当事者で決めてください</li>
 </ul>
</div>
'''
    intro = ('<p>借用書は、お金を借りたことを紙に残す文書です。契約金額によって貼る印紙税が決まります。'
             '<span class="mk">300万円なら1通2,000円で、100万円ちょうどなら1,000円です。</span>'
             'データを送るだけで紙を作らないときは、印紙税はかかりません。</p>\n')
    toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#list">借用書の印紙税はいくらか</a></li>
  <li><a href="#kiri">区分の境目</a></li>
  <li><a href="#kami">紙と電子契約の違い</a></li>
  <li><a href="#risoku">利息の計算のしかた</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">借用書でよく聞かれること</a></li>
 </ol>
</nav>
'''
    sec2 = ('<h2 id="kiri">区分の境目</h2>\n'
            '<p>税額が上がるのは、記載された金額が区分を超えたときです。ちょうど境目の金額は、低い方の税額です。</p>\n'
            + B.table(['契約金額', '印紙税'], [
                [B.td('9,999円', 'l'), B.td('非課税')],
                [B.td('10,000円', 'l'), B.td('200円')],
                [B.td('100,000円', 'l'), B.td('200円')],
                [B.td('100,001円', 'l'), B.td('400円')],
                [B.td('1,000,000円', 'l'), B.td('1,000円')],
                [B.td('1,000,001円', 'l'), B.td('2,000円')],
                [B.td('10,000,000円', 'l'), B.td('10,000円')],
                [B.td('10,000,001円', 'l'), B.td('20,000円')],
                [B.td('50,000,000円', 'l'), B.td('20,000円')],
                [B.td('50,000,001円', 'l'), B.td('60,000円')],
            ])
            + '<p class="note" style="margin-top:8px">100万円ちょうどは1,000円です。1円でも超えると2,000円です。5,000万円ちょうどは20,000円で、1円超えると60,000円です。</p>\n')
    sec3 = ('<h2 id="kami">紙と電子契約の違い</h2>\n'
            '<p>印紙税は、紙の文書を作ったときにかかります。借用書を2通作ると、それぞれに印紙税がかかります。</p>\n'
            '<p>データを送るだけで紙を作らない電子契約は、課税される文書を作っていません。あとから紙に印刷して相手に渡すと、その紙にかかります。</p>\n')
    sec4 = ('<h2 id="risoku">利息の計算のしかた</h2>\n'
            '<p>利息は元金に年利と日数を掛けて365で割り、1円未満を切り捨てます。日数は借りた日の翌日から返す日までです。</p>\n'
            '<p>300万円を年1.5%で365日借りると、利息は45,000円です。年利0%なら利息は0円で、文面には利息を付けないと書きます。</p>\n'
            '<p>毎月の元金と利息の内訳は<a href="/hensai/">借入の返済の計算</a>で見られます。元金の返済は経費にならず、事業のための利息は経費になります。</p>\n')
    rel = B.rel(slug, [
        ('hensai', '借入の返済の計算', '毎月の返済額は、借入の返済の計算で見られます。'),
        ('soneki-bunkiten', '損益分岐点の計算', 'いくら売れば赤字にならないかは、損益分岐点で分かります。'),
        ('houjinnari', '法人成りの計算', '個人事業から会社にするかは、所得で損得が分かれます。'),
        ('houjinzei', '法人税の早見表', '会社の利益にかかる法人税は、所得800万円を境に税率が変わります。'),
        ('kojin-zei', '個人事業主の手取りの早見表', '個人事業主の手取りは、国保と国民年金を引いて考えます。'),
        ('shotokuzei', '所得税の計算', '受け取った利息の税金は、所得税の計算で見られます。'),
        ('kakutei-shinkoku', '確定申告の期限の早見表', '申告の期限は、所得税と法人税で違います。'),
        ('yakuin-tedori', '役員報酬の手取りの早見表', '役員報酬の手取りは、社会保険料を引いた額で考えます。'),
        ('hoteifukurihi', '法定福利費の計算', '会社が払う社会保険料は、法定福利費として経費になります。'),
        ('furusato', 'ふるさと納税の限度額の計算', 'ふるさと納税の上限は、所得で決まります。'),
    ])
    qa = ('<h2 id="qa">借用書でよく聞かれること</h2>\n'
          '<h3>100万円の借用書の印紙税はいくらですか？</h3>\n<p>1,000円です。50万円を超え100万円以下の区分です。</p>\n'
          '<h3>300万円ではいくらですか？</h3>\n<p>2,000円です。100万円を超え500万円以下の区分です。</p>\n'
          '<h3>電子契約でも印紙税はかかりますか？</h3>\n<p>紙の借用書を作ったときにかかります。データを送るだけで紙を作らないときはかかりません。</p>\n'
          '<h3>1万円未満は非課税ですか？</h3>\n<p>金額を書いた借用書で1万円未満は非課税です。金額を書かない借用書は200円です。</p>\n'
          '<h3>利息は経費になりますか？</h3>\n<p>事業のための借入なら利息は経費になります。元金の返済は経費になりません。</p>\n'
          '<h3>連帯保証人は必要ですか？</h3>\n<p>法律で必須ではありません。保証人を書くと、その人も紙の契約の当事者になります。</p>\n')
    src = ('<div class="src">出典・参考（2026年11月確認）\n <ul>\n'
           '  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7140.htm">国税庁 No.7140「印紙税額の一覧表（その1）」</a>（令和8年4月1日現在法令等・第1号文書）</li>\n'
           '  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/inshi/7101.htm">国税庁 No.7101「不動産の譲渡・土地の賃貸借・消費貸借・運送等に関する契約書」</a></li>\n'
           ' </ul>\n</div>\n')
    body = (B.hy_wrap(sec1) + calc + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n'
            + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + rel + '\n' + qa + '\n' + src)
    html = B.page(slug, title, desc, upd, body, JS, 'shakuyo', auth=B.auth_box('国税庁'))
    os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
    open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(html)
    # 初期表示の検算
    assert stamp(3000000) == (2000, '100万円超500万円以下')
    assert stamp(1000000) == (1000, '50万円超100万円以下')
    assert stamp(1000001) == (2000, '100万円超500万円以下')
    assert stamp(9999) == (0, '1万円未満')
    assert stamp(10000) == (200, '1万円以上10万円以下')
    assert stamp(0) == (200, '金額の記載がないもの')
    assert stamp(5000000001) == (600000, '50億円超')
    assert stamp(5000000000) == (400000, '10億円超50億円以下')
    assert interest(3000000, 1.5, 365) == 45000
    assert interest(3000000, 0, 365) == 0
    print('wrote', slug)


if __name__ == '__main__':
    main()
