import re,json,sys
sys.path.insert(0,'.')
from regions import *
SITE='/home/claude/toshi-20260922.github.io/site/'
PM={'東京23区':'東京都','目黒区':'東京都','中野区':'東京都','江戸川区':'東京都','札幌市':'北海道','仙台市':'宮城県','さいたま市':'埼玉県','千葉市':'千葉県','横浜市':'神奈川県','川崎市':'神奈川県','相模原市':'神奈川県','新潟市':'新潟県','浜松市':'静岡県','名古屋市':'愛知県','京都市':'京都府','大阪市・堺市':'大阪府','神戸市':'兵庫県','岡山市':'岡山県','広島市':'広島県','北九州市':'福岡県','福岡市':'福岡県','熊本市':'熊本県'}
PN=[p[0] for p in PREF]
def f(n): return format(n,',')
RGJS='var RG='+json.dumps([dict(n=r['n'],s=r['s'],p=r['p'],r=r['r'],g=r['nag'],f=PN.index(PM[r['s']])) for r in REG],ensure_ascii=False,separators=(',',':'))+';'
PFJS='var PF='+json.dumps(PREF,ensure_ascii=False,separators=(',',':'))+';'
OPT=''.join('<option value="%d">%s</option>'%(i,r['n']) for i,r in enumerate(REG))+'<option value="x">一覧にない市区町村（料率を入力する）</option>'
CUST='''<div class="full cust" id="cust" hidden>
   <label>住んでいる市区町村の料率（令和8年度）</label>
   <div class="cg">
    <span></span><span>所得割（%）</span><span>均等割（円）</span><span>平等割（円）</span>
    <span>医療分</span><input type="number" id="c00" inputmode="decimal" min="0" max="20" step="0.01" aria-label="医療分の所得割"><input type="number" id="c01" inputmode="numeric" min="0" max="200000" step="1" aria-label="医療分の均等割"><input type="number" id="c02" inputmode="numeric" min="0" max="200000" step="1" aria-label="医療分の平等割">
    <span>支援金分</span><input type="number" id="c10" inputmode="decimal" min="0" max="20" step="0.01" aria-label="支援金分の所得割"><input type="number" id="c11" inputmode="numeric" min="0" max="200000" step="1" aria-label="支援金分の均等割"><input type="number" id="c12" inputmode="numeric" min="0" max="200000" step="1" aria-label="支援金分の平等割">
    <span>介護分</span><input type="number" id="c20" inputmode="decimal" min="0" max="20" step="0.01" aria-label="介護分の所得割"><input type="number" id="c21" inputmode="numeric" min="0" max="200000" step="1" aria-label="介護分の均等割"><input type="number" id="c22" inputmode="numeric" min="0" max="200000" step="1" aria-label="介護分の平等割">
    <span>子ども分</span><input type="number" id="c30" inputmode="decimal" min="0" max="20" step="0.01" aria-label="子ども分の所得割"><input type="number" id="c31" inputmode="numeric" min="0" max="200000" step="1" aria-label="子ども分の均等割"><input type="number" id="c32" inputmode="numeric" min="0" max="200000" step="1" aria-label="子ども分の平等割">
   </div>
   <p class="cn">料率は市区町村のホームページか保険料の通知書に載っています。平等割がない区分は0のままにします。</p>
  </div>'''
CSS='''
/* 地域の欄 2026/11/16 */
.cust{background:#ffffff14;border-radius:8px;padding:12px}
.cust[hidden]{display:none}
.cg{display:grid;grid-template-columns:auto 1fr 1fr 1fr;gap:6px;align-items:center;font-size:12px;line-height:1.4;color:#dfeee8;margin:6px 0 0}
.in .cg input:is([type=number],.cmn){width:100%;min-width:0;font-size:15px;font-weight:700;padding:6px 4px;border-radius:6px}
.cn{font-size:12px;line-height:1.6;color:#dfeee8;margin:8px 0 0}
'''
# 共通の計算(ブラウザ)
JSK='''
function rd(n){return n===7?"7割":(n===5?"5割":(n===2?"2割":"なし"));}
function kokuho(R,g,meOld,fam,famOld){
 var n=1+fam,base=Math.max(0,g-430000);
 var red=g<=430000?7:(g<=430000+310000*n?5:(g<=430000+570000*n?2:0));
 var parts=[];R.p.forEach(function(c,i){
  var cnt=i===2?((meOld?1:0)+famOld):n,ib=i===2?(meOld?base:0):base;
  if(!cnt){parts.push(0);return;}
  var v=Math.floor(ib*c[0]/10000)+Math.floor(c[1]*cnt*(10-red)/10)+Math.floor(c[2]*(10-red)/10);
  if(R.g&&i===0&&red>0)v=Math.max(0,v-2000*cnt);
  v=Math.floor(v/R.r)*R.r;parts.push(Math.min(c[3],v));});
 return {t:parts.reduce(function(a,b){return a+b;},0),p:parts,red:red};
}
var reg=document.getElementById("reg"),cust=document.getElementById("cust"),CAP=[670000,260000,170000,30000],lastR=0;
function ci(i,j){return document.getElementById("c"+i+j);}
function fillCust(R){for(var i=0;i<4;i++){ci(i,0).value=(R.p[i][0]/100).toFixed(2);ci(i,1).value=R.p[i][1];ci(i,2).value=R.p[i][2];}}
function curR(){
 if(reg.value!=="x"){lastR=+reg.value;return RG[lastR];}
 var p=[];for(var i=0;i<4;i++){p.push([Math.round((parseFloat(ci(i,0).value)||0)*100),Math.max(0,parseInt(ci(i,1).value,10)||0),Math.max(0,parseInt(ci(i,2).value,10)||0),CAP[i]]);}
 return {n:"入力した料率",s:"入力した料率",p:p,r:1,g:0,f:-1};
}
'''
def patch(s,old,new,cnt=1):
    assert s.count(old)==cnt,(old[:60],s.count(old))
    return s.replace(old,new)
def nowrap_check(t):
    bad=[x for x in re.split(r'[。？]',re.sub(r'<[^>]+>','',t)) if x.count('、')>=2]
    return bad

# ===== /kokuho-keisan/ =====
import subprocess
def src(p): return subprocess.run(['git','-C',SITE,'show','a5c5a54:site/'+p],capture_output=True,text=True,check=True).stdout
def addcss(s):
    h=s.index('</head>');i=s.rindex('</style>',0,h);return s[:i]+CSS+s[i:]
s=src('kokuho-keisan/index.html')
T='国民健康保険料の計算【令和8年度】年収・所得からいくらになるか'
s=patch(s,'国民健康保険料の計算【大阪府・令和8年度】年収・所得からいくらになるか',T,2)
s=patch(s,'<meta name="description" content="大阪府の令和8年度の国民健康保険料を計算します。前の年の給与の年収か所得と、家族の人数を入力すると、1年間の保険料と内訳を表示します。大阪府内はどの市町村も同じ料率です。">','<meta name="description" content="令和8年度の国民健康保険料を計算します。住んでいる市区町村と前の年の年収・家族の人数を入力すると、1年間の保険料と内訳を表示します。政令指定都市19市と東京23区の料率を登録しています。ほかの市区町村も料率を入力すれば計算できます。">')
s=addcss(s)
s=patch(s,'更新日：2026年11月7日（大阪府の令和8年度の府内統一保険料率）','更新日：2026年11月16日（令和8年度の市区町村ごとの保険料率）')
s=patch(s,'<span>結論</span>前の年の収入を入力すると、1年間の国民健康保険料を表示します','<span>結論</span>市区町村と前の年の収入を入力すると、1年間の国民健康保険料を表示します')
s=patch(s,''' <div class="in">
  <div class="full">
   <label>前の年の収入の種類</label>''',''' <div class="in">
  <div class="full">
   <label for="reg">住んでいる市区町村</label>
   <select id="reg">'''+OPT+'''</select>
  </div>
  '''+CUST+'''
  <div class="full">
   <label>前の年の収入の種類</label>''')
s=patch(s,'<li>大阪府内はどの市町村も同じ保険料率です</li>','<li id="o-reg">東京23区の令和8年度の料率で計算しています</li>')
s=patch(s,'<span class="mk">大阪府の令和8年度は、所得割が合わせて12.84%（40〜64歳の人は15.44%）です。</span>上限は1年で95万円（40〜64歳の人は112万円）です。','<span class="mk">料率は市区町村ごとに違うので、住んでいる市区町村を選んで計算します。</span>上限は多くの市区町村で1年96万円（40〜64歳の人は113万円）です。')
s=patch(s,'国民健康保険料は、前の年の所得から43万円を引いた額にかかる所得割と、1人ごとの均等割、1世帯ごとの平等割の合計です。','国民健康保険料は前の年の所得から43万円を引いた額にかかる所得割と、1人ごとの均等割・1世帯ごとの平等割の合計です。')
s=patch(s,''' <li><a href="#rate">大阪府の保険料率（令和8年度）</a></li>''',''' <li><a href="#rate">選んだ市区町村の保険料率</a></li>
 <li><a href="#hikaku">市区町村ごとの保険料</a></li>''')
s=patch(s,'<p class="cap" id="t-cap">大阪府・令和8年度・家族なし</p>','<p class="cap" id="t-cap">東京23区・令和8年度・家族なし</p>')
# 料率の表(選んだ地域) + 地域ごとの比較
i=s.index('<h2 id="rate">');j=s.index('<h2 id="red">')
rows=''
for r in REG:
    a=kokuho(r,kyuyo7(4000000),0,0,0)[0];b=kokuho(r,kyuyo7(4000000),1,0,0)[0]
    rows+=' <tr><td class="l">%s</td><td>%s</td><td>%s</td></tr>\n'%(r['s'],f(a),f(b))
lo=min(REG,key=lambda r:kokuho(r,kyuyo7(4000000),0,0,0)[0]);hi=max(REG,key=lambda r:kokuho(r,kyuyo7(4000000),0,0,0)[0])
lov=kokuho(lo,kyuyo7(4000000),0,0,0)[0];hiv=kokuho(hi,kyuyo7(4000000),0,0,0)[0]
print('min',lo['s'],lov,'max',hi['s'],hiv)
NEW='''<h2 id="rate">選んだ市区町村の保険料率</h2>
<p class="cap" id="r-cap">東京23区・令和8年度</p>
<div class="tw"><table>
 <thead><tr><th>区分</th><th>所得割</th><th>均等割<br>（1人・円）</th><th>平等割<br>（1世帯・円）</th><th>上限<br>（円）</th></tr></thead>
 <tbody id="rtb"></tbody>
</table></div>
<p class="note" style="margin-top:8px">子ども・子育て支援金分は令和8年度から加わりました。均等割は18歳以上の人の額です。端数の切り捨て方は市区町村で違うので、通知書の額と数百円ずれることがあります。</p>
<h2 id="hikaku">市区町村ごとの保険料</h2>
<p>前の年の給与の年収が400万円で、1人で加入する場合の1年間の保険料です。</p>
<div class="tw"><table>
 <thead><tr><th>市区町村</th><th>40歳未満<br>（年・円）</th><th>40〜64歳<br>（年・円）</th></tr></thead>
 <tbody>
'''+rows+''' </tbody>
</table></div>
<p class="note" style="margin-top:8px">東京23区は、目黒区・中野区・江戸川区を除く20区の料率です。大阪府は府内のどの市町村も同じ料率です。静岡市は公式ページに料率の表が見当たらないので、一覧に含めていません。</p>
'''
s=s[:i]+NEW+s[j:]
s=patch(s,'''<h3>大阪市と堺市で保険料は違いますか？</h3>
<p>大阪府は府内統一の保険料率なので、同じ所得・同じ世帯なら、どの市町村でも保険料は同じです。</p>''','''<h3>市区町村で保険料はどのくらい違いますか？</h3>
<p>年収400万円・1人で加入・40歳未満の場合、この早見表の22の地域では年%s円（%s）から年%s円（%s）まで開きがあります。</p>
<h3>一覧にない市区町村に住んでいる場合は、どう計算しますか？</h3>
<p>市区町村の欄で「一覧にない市区町村（料率を入力する）」を選びます。市区町村のホームページにある所得割・均等割・平等割を入力すると計算できます。</p>'''%(f(lov),lo['s'],f(hiv),'大阪府内' if hi['s']=='大阪市・堺市' else hi['s']))
# 出典
i=s.index('<div class="src">');j=s.index('</div>',i)+6
seen=[];li=''
for r in REG:
    if r['url'] not in seen:
        seen.append(r['url']);li+='  <li><a href="%s">%s</a></li>\n'%(r['url'],r['src'])
SRC='''<div class="src">出典・参考（2026年11月確認）<ul>
'''+li+'''  <li><a href="https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/04hokenryounituite.html">横浜市「保険料について」（軽減の基準額）</a></li>
  <li>表の金額は、上の資料の料率から計算しています</li>
</ul></div>'''
s=s[:i]+SRC+s[j:]
# 計算
i=s.index('var C=[[950');j=s.index('var inc=document.getElementById("inc")',i)
s=s[:i]+RGJS+JSK+s[j:]
s=patch(s,'var RN={0.7:"7割",0.5:"5割",0.2:"2割",0:"なし"};','')
s=patch(s,'x=kokuho(g,old,fm,fo);','R=curR(),x=kokuho(R,g,old,fm,fo);')
s=patch(s,'document.getElementById("o-r").textContent=RN[x.red];','document.getElementById("o-r").textContent=rd(x.red);')
s=patch(s,'document.getElementById("t-cap").textContent="大阪府・令和8年度・"+(fm?"家族"+fm+"人":"家族なし");','''document.getElementById("t-cap").textContent=R.s+"・令和8年度・"+(fm?"家族"+fm+"人":"家族なし");
 document.getElementById("o-reg").textContent=(R.f<0?"入力した料率":R.s+"の令和8年度の料率")+"で計算しています";
 document.getElementById("r-cap").textContent=R.s+"・令和8年度";
 var LB=["医療分","後期高齢者支援金分","介護分（40〜64歳）","子ども・子育て支援金分"],rh="";
 R.p.forEach(function(c,i){rh+="<tr><td class=\\"l\\">"+LB[i]+"</td><td>"+(c[0]/100).toFixed(2)+"%</td><td>"+f(c[1])+"</td><td>"+f(c[2])+"</td><td>"+f(c[3])+"</td></tr>";});
 document.getElementById("rtb").innerHTML=rh;''')
s=patch(s,'f(kokuho(gg,0,fm,0).t)','f(kokuho(R,gg,0,fm,0).t)')
s=patch(s,'f(kokuho(gg,1,fm,fm).t)','f(kokuho(R,gg,1,fm,fm).t)')
s=patch(s,'link(inc,incr,render);','''reg.addEventListener("change",function(){var x=reg.value==="x";if(x)fillCust(RG[lastR]);cust.hidden=!x;render();});
cust.addEventListener("input",render);
link(inc,incr,render);''')
s=s.replace('Math.floor(A*0.7)-80000','A/4000*2800-80000').replace('Math.floor(A*0.8)-440000','A/4000*3200-440000').replace('Math.floor(x*0.9)-1100000','Math.floor(x*9/10)-1100000');open(SITE+'kokuho-keisan/index.html','w').write(s)
print('kokuho-keisan ok',len(s))

# ===== /kokuho/ =====
G=[[58,63],[68,73],[78,83],[88,93],[98,101],[104,107],[110,114],[118,122],[126,130],[134,138],[142,146],[150,155],[160,165],[170,175],[180,185],[190,195],[200,210],[220,230],[240,250],[260,270],[280,290],[300,310],[320,330]]
def std(m):
    for a,b in G:
        if m<b*1000:return a*1000
    return 320000
def r50(n,d):  # n/d を50銭以下切り捨て・超は切り上げ
    q,rm=divmod(n,d);return q+1 if rm*2>d else q
PR=dict(PREF)
def nini(a,old,rate):
    sm=std(a//12);return r50(sm*(rate+23+(162 if old else 0)),10000)*12
def kk(r,a,old,fam=0):
    return kokuho(r,kyuyo7(a),old,fam,fam if old else 0)[0]
# 公式の額表(東京・令和8年4月分〜)との照らし合わせ
assert r50(320000*(985+23),10000)==32256 and r50(320000*(985+23+162),10000)==37440 and r50(300000*(985+23),10000)==30240
s=src('kokuho/index.html')
s=patch(s,'国民健康保険と任意継続どっちが安い？【大阪府・令和8年度】退職前の年収で比べる早見表','国民健康保険と任意継続どっちが安い？【令和8年度】退職前の年収で比べる早見表',2)
s=patch(s,'<meta name="description" content="会社を辞めたあとの健康保険を、大阪府の令和8年度の国民健康保険料と、協会けんぽの任意継続で比べました。退職前の年収を入力すると、1年間の保険料とどちらが安いかを表示します。">','<meta name="description" content="会社を辞めたあとの健康保険を、令和8年度の国民健康保険料と協会けんぽの任意継続で比べます。住んでいる市区町村と退職前の年収を入力すると、1年間の保険料とどちらが安いかを表示します。政令指定都市19市・東京23区・47都道府県の料率に対応しています。">')
s=addcss(s)
s=patch(s,'更新日：2026年11月7日（大阪府の令和8年度の国民健康保険料率）','更新日：2026年11月16日（令和8年度の市区町村ごとの国民健康保険料率と協会けんぽの料率）')
s=patch(s,'<span>結論</span>退職前の年収を入力すると、どちらが安いかを表示します','<span>結論</span>市区町村と退職前の年収を入力すると、どちらが安いかを表示します')
POPT=''.join('<option value="%d"%s>%s（%.2f%%）</option>'%(i,' selected' if p[0]=='東京都' else '',p[0],p[1]/100) for i,p in enumerate(PREF))
s=patch(s,''' <div class="in">
  <div class="full">
   <label for="inc">退職前の年収（前の年の給与）</label>''',''' <div class="in">
  <div class="full">
   <label for="reg">住んでいる市区町村（国民健康保険）</label>
   <select id="reg">'''+OPT+'''</select>
  </div>
  '''+CUST+'''
  <div class="full">
   <label for="pref">住んでいる都道府県（協会けんぽの任意継続）</label>
   <select id="pref">'''+POPT+'''</select>
  </div>
  <div class="full">
   <label for="inc">退職前の年収（前の年の給与）</label>''')
s=patch(s,'<b id="o-k">0<i>円</i></b><em>大阪府</em>','<b id="o-k">0<i>円</i></b><em id="e-k">東京23区</em>')
s=patch(s,'<b id="o-n">0<i>円</i></b><em>協会けんぽ大阪</em>','<b id="o-n">0<i>円</i></b><em id="e-n">協会けんぽ東京都</em>')
# 任意継続のほうが安くなり始める年収(単身・自己都合)
def be(r,old):
    rate=PR[PM[r['s']]];last=None
    for a in range(12000000,990000,-10000):
        if nini(a,old,rate)<kk(r,a,old): last=a
        else: break
    return last
tk=REG[0];b0=be(tk,0)
print('東京23区 分かれ目',b0, kk(tk,b0,0),nini(b0,0,985),'1つ下',kk(tk,b0-10000,0),nini(b0-10000,0,985))
s=patch(s,'国民健康保険は前の年の所得で決まり、上限がずっと高くなります。<span class="mk">大阪府で単身の場合、退職前の年収がおよそ400万円を超えると、年収が上がるほど任意継続のほうが安くなります。</span>','国民健康保険は前の年の所得で決まり、上限がずっと高くなります。<span class="mk">どちらが安いかは、住んでいる市区町村と退職前の年収で変わります。</span>')
s=patch(s,'''  <li><a href="#rate">大阪府の国民健康保険料率（令和8年度）</a></li>''','''  <li><a href="#wakare">任意継続のほうが安くなる年収</a></li>
  <li><a href="#rate">選んだ市区町村の国民健康保険料率</a></li>''')
s=patch(s,'<p class="cap" id="t-cap">40歳未満・自己都合・家族なし</p>','<p class="cap" id="t-cap">東京23区・40歳未満・自己都合・家族なし</p>')
s=patch(s,'国民健康保険は大阪府の令和8年度の府内統一保険料率で、給与所得から43万円を引いた額に所得割をかけ、均等割・平等割を足しています。','国民健康保険は選んだ市区町村の令和8年度の料率で計算しています。給与所得から43万円を引いた額に所得割をかけ、均等割・平等割を足した額です。')
s=patch(s,'任意継続は、年収を12で割った月給の標準報酬月額（上限32万円）に、協会けんぽ大阪支部の令和8年度の料率をかけています。','任意継続は年収を12で割った月給の標準報酬月額（上限32万円）に、選んだ都道府県の協会けんぽの料率をかけています。')
i=s.index('<h2 id="rate">');j=s.index('<h2 id="nini">')
rows=''
for r in REG:
    b=be(r,0);b2=be(r,1)
    rows+=' <tr><td class="l">%s</td><td>%s</td><td>%s</td></tr>\n'%(r['s'],('%d万円から'%(b//10000)) if b else '—',('%d万円から'%(b2//10000)) if b2 else '—')
    print(r['s'],b,b2)
NEW='''<h2 id="wakare">任意継続のほうが安くなる年収</h2>
<p>1人で加入し、自己都合で辞めた場合です。退職前の年収が表の額以上なら、任意継続のほうが安くなります。</p>
<div class="tw"><table>
 <thead><tr><th>住んでいる市区町村</th><th>40歳未満</th><th>40〜64歳</th></tr></thead>
 <tbody>
'''+rows+''' </tbody>
</table></div>
<p class="note" style="margin-top:8px">任意継続は、その市区町村がある都道府県の協会けんぽの料率で計算しています。東京23区は、目黒区・中野区・江戸川区を除く20区の料率です。静岡市は公式ページに料率の表が見当たらないので、一覧に含めていません。</p>
<h2 id="rate">選んだ市区町村の国民健康保険料率</h2>
<p>令和8年度から、子ども・子育て支援金分が加わりました。</p>
<p class="cap" id="r-cap">東京23区・令和8年度</p>
<div class="tw">
<table>
 <thead><tr><th>区分</th><th>所得割</th><th>均等割<br>（1人・円）</th><th>平等割<br>（1世帯・円）</th><th>上限<br>（円）</th></tr></thead>
 <tbody id="rtb"></tbody>
</table>
</div>
<p class="note" style="margin-top:8px">上限は1年間の額です。均等割は18歳以上の人の額です。端数の切り捨て方は市区町村で違うので、通知書の額と数百円ずれることがあります。</p>

'''
s=s[:i]+NEW+s[j:]
s=patch(s,'協会けんぽ大阪支部の令和8年度の料率は、子ども・子育て支援金を含めて10.36%、40〜64歳は介護保険を含めて11.98%です。','協会けんぽの令和8年度の料率は都道府県ごとに9.21%（新潟県）から10.55%（佐賀県）です。これに子ども・子育て支援金の0.23%が加わり、40〜64歳は介護保険の1.62%も加わります。')
assert min(PREF,key=lambda p:p[1])[0]=='新潟県' and max(PREF,key=lambda p:p[1])[0]=='佐賀県'
k5=kk(tk,5000000,0);n5=nini(5000000,0,985)
print('東京23区 500万',k5,n5)
os_=REG[SHORT.index('大阪市・堺市')];print('大阪 500万',kk(os_,5000000,0),nini(5000000,0,1013),'(直す前のページ:国保およそ49万・任意継続およそ40万)')
def man(n): return '%d万%s円'%(n//10000,('%d千'%round(n%10000/1000)) if round(n%10000/1000) else '')
s=patch(s,'<p>大阪府・単身・40歳未満・自己都合なら、国民健康保険が年およそ49万円、任意継続が年およそ40万円で、任意継続のほうが年10万円近く安くなります。</p>','<p>東京23区・1人で加入・40歳未満・自己都合なら、国民健康保険が年%s円で任意継続が年%s円です。%sのほうが年%s円安くなります。市区町村で結果が変わるので、上の計算で確かめてください。</p>'%(f(k5),f(n5),'任意継続' if n5<k5 else '国民健康保険',f(abs(k5-n5))))
s=patch(s,'''<h3>大阪府以外に住んでいる場合も同じですか？</h3>
<p>国民健康保険の料率は都道府県や市区町村で違い、任意継続の料率も都道府県で違います。この早見表は大阪府に住み、協会けんぽ大阪支部の会社を辞めた場合です。</p>''','''<h3>住んでいる地域で結果は変わりますか？</h3>
<p>変わります。国民健康保険の料率は市区町村ごとに違い、協会けんぽの任意継続の料率は住んでいる都道府県で決まります。</p>
<h3>一覧にない市区町村に住んでいる場合は、どう比べますか？</h3>
<p>市区町村の欄で「一覧にない市区町村（料率を入力する）」を選びます。市区町村のホームページにある所得割・均等割・平等割を入力すると比べられます。</p>
<h3>健康保険組合の任意継続も同じ計算ですか？</h3>
<p>違います。この早見表の任意継続は協会けんぽの料率と上限です。健康保険組合は組合ごとに料率と上限が決まっているので、組合に確かめてください。</p>''')
i=s.index('<div class="src">');j=s.index('</div>',i)+6
SRC2='''<div class="src">出典・参考（2026年11月確認）
 <ul>
'''+li+'''  <li><a href="https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/04hokenryounituite.html">横浜市「保険料について」（軽減の基準額）</a></li>
  <li><a href="https://www.kyoukaikenpo.or.jp/news/r07_dec/1259.html">全国健康保険協会「令和8年度の任意継続被保険者の標準報酬月額の上限」</a></li>
  <li><a href="https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08">全国健康保険協会「令和8年度の都道府県単位保険料率」</a></li>
  <li><a href="https://www.kyoukaikenpo.or.jp/~/media/Files/shared/hokenryouritu/r8/ninkei/13tokyo.pdf">全国健康保険協会「任意継続被保険者の保険料額表（東京都・令和8年4月分から）」</a></li>
  <li>表の金額は、上の資料の料率から計算しています</li>
 </ul>
</div>'''
s=s[:i]+SRC2+s[j:]
# 計算
i=s.index(' var C=[[950');j=s.index(' function f(n)',i)
JS2=RGJS+PFJS+JSK+'''
 var pref=document.getElementById("pref");
 function kk(R,a,old,hi,fam){var g=kyuyo(a);if(hi)g=Math.floor(g*30/100);return kokuho(R,g,old,fam,old?fam:0).t;}
 function nini(a,old){var s=std(Math.floor(a/12));return {y:r50(s*(PF[+pref.value][1]+23+(old?162:0))/10000)*12,s:s};}
'''
s=s[:i]+JS2+s[j:]
s=patch(s,'var a=Math.max(0,parseInt(inc.value,10)||0),fm=+fam.value,k=kokuho(a,old,hi,fm),nn=nini(a,old),d=Math.abs(k-nn.y);','var a=Math.max(0,parseInt(inc.value,10)||0),fm=+fam.value,R=curR(),k=kk(R,a,old,hi,fm),nn=nini(a,old),d=Math.abs(k-nn.y);')
s=patch(s,'document.getElementById("t-cap").textContent=(old?"40〜64歳":"40歳未満")','''document.getElementById("e-k").textContent=R.s;document.getElementById("e-n").textContent="協会けんぽ"+PF[+pref.value][0];
  document.getElementById("r-cap").textContent=R.s+"・令和8年度";
  var LB=["医療分","後期高齢者支援金分","介護分（40〜64歳）","子ども・子育て支援金分"],rh="";
  R.p.forEach(function(c,i){rh+="<tr><td class=\\"l\\">"+LB[i]+"</td><td>"+(c[0]/100).toFixed(2)+"%</td><td>"+f(c[1])+"</td><td>"+f(c[2])+"</td><td>"+f(c[3])+"</td></tr>";});
  document.getElementById("rtb").innerHTML=rh;
  document.getElementById("t-cap").textContent=R.s+"・"+(old?"40〜64歳":"40歳未満")''')
s=patch(s,'var kk=kokuho(r*10000,old,hi,fm),ny=nini(r*10000,old).y;','var kv=kk(R,r*10000,old,hi,fm),ny=nini(r*10000,old).y;')
s=patch(s,'<td>"+f(kk)+"</td><td>"+f(ny)+"</td><td class=\\"c\\">"+(kk<ny?"国保":(kk>ny?"任意継続":"同じ"))','<td>"+f(kv)+"</td><td>"+f(ny)+"</td><td class=\\"c\\">"+(kv<ny?"国保":(kv>ny?"任意継続":"同じ"))')
s=patch(s,' fam.addEventListener("change",render);',''' fam.addEventListener("change",render);
 reg.addEventListener("change",function(){var x=reg.value==="x";if(x)fillCust(RG[lastR]);else pref.value=RG[+reg.value].f;cust.hidden=!x;render();});
 cust.addEventListener("input",render);pref.addEventListener("change",render);''')
s=s.replace('Math.floor(A*0.7)-80000','A/4000*2800-80000').replace('Math.floor(A*0.8)-440000','A/4000*3200-440000').replace('Math.floor(x*0.9)-1100000','Math.floor(x*9/10)-1100000');open(SITE+'kokuho/index.html','w').write(s)
print('kokuho ok',len(s))
