import re
S='/home/claude/toshi-20260922.github.io/site/'
t=open(S+'houjinzei-keisan/index.html').read()
T='損益分岐点の計算ツール｜売上高・変動費・固定費から損益分岐点売上高と安全余裕率を出す【計算式つき】'
D='売上高・変動費・固定費を入力すると、損益分岐点売上高・損益分岐点比率・安全余裕率・限界利益率を表示します。売上が増減したときの利益の表と、計算式・計算例・損益分岐点を下げる方法も載せています。'
head=t[:t.index('<body')]
head=head.replace('法人税の計算シミュレーション｜住民税・事業税まで合計いくら？所得を入力して計算【令和8年度】',T)
head=re.sub(r'(<meta name="description" content=")[^"]*',lambda m:m.group(1)+D,head)
head=re.sub(r'(<meta property="og:description" content=")[^"]*',lambda m:m.group(1)+D,head)
head=head.replace('https://taxtable.jp/houjinzei-keisan/','https://taxtable.jp/soneki-bunkiten/')
# 構造化データは型のページのものを外す
head=re.sub(r'<script type="application/ld\+json">.*?</script>\s*','',head,flags=re.S)
b=t[t.index('<body'):]
hdr=b[:b.index('<main class="wrap">')].replace('houjinzei_keisan_','soneki_')
nav=b[b.index('<nav class="tools">'):b.index('</nav>',b.index('<nav class="tools">'))+6]
nav=nav.replace('<div class="t">早見表・計算ツール一覧</div>','<div class="t">早見表・計算ツール一覧</div> <a href="/houjinzei-keisan/">法人税の計算シミュレーション（住民税・事業税まで）</a>',1) if '/houjinzei-keisan/' not in nav else nav
foot=b[b.index('</main>'):b.index('<script',b.index('</main>'))].replace('houjinzei_keisan_','soneki_')
auth=b[b.index('<div class="auth" id="auth">'):b.index('<div class="close">')]
MAIN='''<main class="wrap">
<div class="top">
 <div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="損益分岐点のグラフ"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><path d="M14 48V14M14 48h36" stroke="#0f3d31" stroke-width="2.5" stroke-linecap="round"/><path d="M14 36h36" stroke="#9fc4b6" stroke-width="2.5"/><path d="M14 48L48 16" stroke="#e3b465" stroke-width="3" stroke-linecap="round"/><path d="M14 36L48 26" stroke="#0f3d31" stroke-width="3" stroke-linecap="round"/><circle cx="35" cy="29" r="4" fill="#ffffff" stroke="#b5473a" stroke-width="2.5"/></svg></div>
 <p class="upd">更新日：2026年11月19日</p>
 <h1>'''+T+'''</h1>
</div>
<div class="sum" id="calc">
 <div class="h"><span>結論</span>売上高・変動費・固定費を入力すると、赤字にならない売上高を表示します</div>
 <div class="in">
  <div class="full">
   <label for="sal">売上高（1年または1か月）</label>
   <div class="row"><input type="text" id="sal" inputmode="numeric" value="50,000,000"><span>円</span></div>
  </div>
  <div>
   <label for="vc">変動費（仕入・材料費・外注費など）</label>
   <div class="row"><input type="text" id="vc" inputmode="numeric" value="30,000,000"><span>円</span></div>
  </div>
  <div>
   <label for="fc">固定費（人件費・家賃など）</label>
   <div class="row"><input type="text" id="fc" inputmode="numeric" value="17,000,000"><span>円</span></div>
  </div>
 </div>
 <div class="amt wide">
  <div><small>損益分岐点<br>売上高</small><b id="o-a">0<i>円</i></b><em>利益が0になる売上</em></div>
  <div><small>損益分岐点<br>比率</small><b id="o-b">0<i>%</i></b><em>低いほど赤字になりにくい</em></div>
  <div><small>安全余裕率</small><b id="o-c">0<i>%</i></b><em>売上が減っても黒字の幅</em></div>
 </div>
 <ul>
  <li id="o-1">限界利益0円・限界利益率0%・利益0円</li>
  <li id="o-2">売上高が0円減ると、利益が0になります</li>
  <li>売上高・変動費・固定費は、同じ期間（1年か1か月）の額を入れます</li>
 </ul>
</div>
<div class="rcta"><p>損益分岐点を出すには、毎月の帳簿で変動費と固定費が分かれている必要があります。記帳から決算・申告まで、まとめてお受けしています。</p><a href="https://oyama-toshiro.com/contact/" data-cta="soneki_result_marunage">経理丸投げの無料相談</a></div>
<div class="share">
 <a class="ln" href="https://social-plugins.line.me/lineit/share?url=https://taxtable.jp/soneki-bunkiten/">LINEで送る</a>
 <a class="x" href="https://x.com/intent/post?url=https://taxtable.jp/soneki-bunkiten/">Xでポストする</a>
</div>
<p>損益分岐点は、利益がちょうど0になる売上高です。売上高がこの額を上回れば黒字で、下回れば赤字です。<span class="mk">損益分岐点売上高は、固定費を限界利益率（1−変動費率）で割って出します。</span></p>
<nav class="toc"><div class="t">目次</div><ol>
 <li><a href="#shiki">損益分岐点の計算式</a></li>
 <li><a href="#rei">損益分岐点の計算例</a></li>
 <li><a href="#list">売上高が増減したときの利益</a></li>
 <li><a href="#wake">変動費と固定費の分け方</a></li>
 <li><a href="#sageru">損益分岐点を下げる3つの方法</a></li>
 <li><a href="#qa">損益分岐点でよく聞かれること</a></li>
</ol></nav>

<h2 id="shiki">損益分岐点の計算式</h2>
<div class="tw"><table>
 <thead><tr><th style="width:34%">出すもの</th><th>計算式</th></tr></thead>
 <tbody>
  <tr><td class="l">変動費率</td><td class="l">変動費 ÷ 売上高</td></tr>
  <tr><td class="l">限界利益</td><td class="l">売上高 − 変動費</td></tr>
  <tr><td class="l">限界利益率</td><td class="l">限界利益 ÷ 売上高<small>1 − 変動費率と同じ</small></td></tr>
  <tr><td class="l">損益分岐点売上高</td><td class="l">固定費 ÷（1 − 変動費率）</td></tr>
  <tr><td class="l">損益分岐点比率</td><td class="l">損益分岐点売上高 ÷ 売上高 × 100</td></tr>
  <tr><td class="l">安全余裕率</td><td class="l">（売上高 − 損益分岐点売上高）÷ 売上高 × 100<small>100 − 損益分岐点比率と同じ</small></td></tr>
 </tbody>
</table></div>
<p class="note" style="margin-top:8px">損益分岐点比率と安全余裕率は、足すと100%になります。</p>

<h2 id="rei">損益分岐点の計算例</h2>
<p>売上高5,000万円・変動費3,000万円・固定費1,700万円の会社で計算します。</p>
<ul class="x7ul">
 <li>変動費率：3,000万円 ÷ 5,000万円 ＝ 60%</li>
 <li>限界利益率：1 − 60% ＝ 40%</li>
 <li>損益分岐点売上高：1,700万円 ÷ 40% ＝ 4,250万円</li>
 <li>損益分岐点比率：4,250万円 ÷ 5,000万円 ＝ 85%</li>
 <li>安全余裕率：100% − 85% ＝ 15%</li>
</ul>
<p>この会社は、売上高が15%（750万円）減ると利益が0になります。いまの利益は、限界利益2,000万円から固定費1,700万円を引いた300万円です。</p>

<h2 id="list">売上高が増減したときの利益</h2>
<p>上で入力した数字で、変動費率と固定費が変わらない場合の利益です。</p>
<div class="tw"><table>
 <thead><tr><th>売上高の<br>増減</th><th>売上高<br>（円）</th><th>限界利益<br>（円）</th><th>利益<br>（円）</th></tr></thead>
 <tbody id="tb"></tbody>
</table></div>
<p class="note" style="margin-top:8px">利益がマイナスの行は赤字です。売上高が減っても固定費は減らないので、利益は売上高より大きな割合で減ります。</p>
<p class="ask">会社の利益にかかる税金はいくらか？<br>計算ツールで確かめてみてください。</p>
<a class="cbtn nx" href="/houjinzei-keisan/" data-cta="soneki_next_houjinzei">法人税の計算シミュレーション</a>

<h2 id="wake">変動費と固定費の分け方</h2>
<p>変動費は売上高に比例して増える費用で、固定費は売上高が0でもかかる費用です。</p>
<div class="tw"><table>
 <thead><tr><th style="width:26%">区分</th><th>主な費用</th></tr></thead>
 <tbody>
  <tr><td class="l">変動費</td><td class="l">商品の仕入・材料費・外注費・販売手数料・荷造運賃</td></tr>
  <tr><td class="l">固定費</td><td class="l">役員報酬・給料・社会保険料・家賃・減価償却費・リース料・支払利息</td></tr>
 </tbody>
</table></div>
<p>水道光熱費や残業代のように、両方の性質を持つ費用もあります。最初は勘定科目ごとにどちらかに決めて、毎月同じ分け方で計算します。</p>
<h3>会社を経営している方は、毎月の数字で損益分岐点を確かめてください</h3>
<p>損益分岐点は、決算書が出来てから年に1回見るだけでは遅くなります。毎月の試算表で売上高と比べると、赤字になる前に手を打てます。帳簿の付け方は、専門家に相談してください。</p>
<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="soneki_mid_marunage">経理丸投げの無料相談</a>

<h2 id="sageru">損益分岐点を下げる3つの方法</h2>
<ul class="x7ul">
 <li>固定費を減らす：家賃・リース料・保険料など、毎月決まって出ていく費用を見直します</li>
 <li>変動費率を下げる：仕入先・外注先と条件を見直し、売上高に対する原価の割合を下げます</li>
 <li>販売価格を上げる：同じ数量でも売上高が増えるので、変動費率が下がります</li>
</ul>
<p>変動費率と固定費が同じまま売上高を増やしても、損益分岐点売上高は変わりません。売上高を増やすと下がるのは損益分岐点比率です。</p>
<p class="ask">人を1人雇うと、固定費はいくら増えるか？<br>計算ツールで確かめてみてください。</p>
<a class="cbtn nx" href="/yatou-hiyou/" data-cta="soneki_next_yatou">従業員を1人雇う費用</a>

<h2 id="qa"><span class="nw">損益分岐点で</span><span class="nw">よく聞かれること</span></h2>
<h3>損益分岐点とは、何ですか？</h3>
<p>利益がちょうど0になる売上高です。売上高から変動費と固定費を引いた額が0になる点で、損益分岐点売上高とも呼びます。</p>
<h3>損益分岐点比率は、低いほうがよいのですか？</h3>
<p>低いほうが、売上高が減っても赤字になりにくい会社です。損益分岐点比率が100%を超えていると、いまの売上高では赤字です。</p>
<h3>借入金の返済は、固定費に入れますか？</h3>
<p>入れません。元金の返済は費用ではないので、損益分岐点の計算には入りません。支払利息は固定費に入れます。返済まで含めて必要な売上高を知りたいときは、固定費に年間の返済額を足して計算します。</p>
<h3>目標の利益を出すには、売上高がいくら必要ですか？</h3>
<p>固定費に目標の利益を足して、限界利益率で割ります。固定費1,700万円・限界利益率40%の会社が利益500万円を出す場合で計算します。2,200万円 ÷ 40% ＝ 5,500万円の売上高が必要です。</p>

<div class="src">出典・参考（2026年11月確認）<ul>
  <li><a href="https://j-net21.smrj.go.jp/qa/financial/Q0240.html">中小企業基盤整備機構 J-Net21「損益分岐点の計算方法と経営改善に向けた活用方法を教えてください。」</a></li>
  <li>表の金額は、上の計算式から計算しています</li>
</ul></div>

'''+auth+'''<div class="close"><p class="close-h"><span class="nw">毎月の数字を、</span><span class="nw">まとめて任せる</span></p><p>損益分岐点を毎月確かめるには、毎月の帳簿が要ります。会社を経営している方の、記帳から決算・申告までをまるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p><a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="soneki_close_marunage">経理丸投げの無料相談</a></div>

'''+nav+'\n'
JS='''<script>
(function(){
function f(n){return Math.round(n).toLocaleString("ja-JP");}
function num(el){return Math.max(0,parseInt(String(el.value).replace(/[^0-9]/g,""),10)||0);}
function fmt(el){el.value=num(el).toLocaleString("ja-JP");}
function sg(n){var a=Math.round(Math.abs(n));return (n<0&&a>0?"−":"")+a.toLocaleString("ja-JP");}
function t10(a,b){return Math.round(Math.abs(a)*1000/b)*(a<0?-1:1);}
function pt(t){return (t<0?"−":"")+(Math.abs(t)/10).toFixed(1);}
var sal=document.getElementById("sal"),vc=document.getElementById("vc"),fc=document.getElementById("fc");
function calc(S,V,F){var m=S-V,mr=S>0?m/S:0,ok=S>0&&m>0,bep=ok?F*S/m:0;return {m:m,mr:mr,ok:ok,bep:bep,br:ok?F*100/m:0,pf:m-F};}
function render(){var S=num(sal),V=num(vc),F=num(fc),r=calc(S,V,F),bt=r.ok?t10(F,r.m):0,gap=r.ok?f(Math.abs(S*r.pf/r.m)):"";
 document.getElementById("o-a").innerHTML=(r.ok?f(r.bep):"—")+"<i>円</i>";
 document.getElementById("o-b").innerHTML=(r.ok?pt(bt):"—")+"<i>%</i>";
 document.getElementById("o-c").innerHTML=(r.ok?pt(1000-bt):"—")+"<i>%</i>";
 document.getElementById("o-1").textContent="限界利益"+sg(r.m)+"円・限界利益率"+pt(S>0?t10(r.m,S):0)+"%・利益"+sg(r.pf)+"円";
 document.getElementById("o-2").textContent=!r.ok?"変動費が売上高以上なので、売上高を増やしても黒字になりません":(r.pf>=0?"売上高が"+gap+"円減ると、利益が0になります":"売上高があと"+gap+"円増えると、利益が0になります");
 var t="";[-30,-20,-10,0,10,20,30].forEach(function(d){var s=S*(100+d)/100,m=r.m*(100+d)/100,pf=(r.m*(100+d)-F*100)/100;
  t+="<tr"+(d===0?" class=\\"hit\\"":"")+"><td>"+(d>0?"+":(d<0?"−":""))+Math.abs(d)+"%</td><td>"+f(s)+"</td><td>"+sg(m)+"</td><td>"+sg(pf)+"</td></tr>";});
 document.getElementById("tb").innerHTML=t;}
[sal,vc,fc].forEach(function(e){e.addEventListener("input",render);e.addEventListener("blur",function(){fmt(e);});});
render();
window.__sb={calc:calc};
})();
</script>
</body>
</html>
'''
i=head.rindex('</style>');head=head[:i]+'.x7ul{margin:0 0 20px;padding:0 0 0 1.2em;line-height:1.9}.x7ul li{margin:0 0 6px}\n'+head[i:]
out=head+hdr+MAIN+foot+JS
open(S+'soneki-bunkiten/index.html','w').write(out);print(len(out),'x7ul' in head)
