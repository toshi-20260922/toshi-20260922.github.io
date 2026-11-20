import re,json,sys,asyncio,subprocess
sys.path.insert(0,'.')
from regions import *
exec(open('build_pm.py').read())
from playwright.async_api import async_playwright
SITE='/home/claude/toshi-20260922.github.io/site/'
b=open('build.py').read()
ns={}
exec(b[b.index('PN=['):b.index('def patch')],dict(globals()),ns)   # RGJS, PFJS, OPT, CUST, CSS, JSK
RGJS,PFJS,OPT,CUST,CSS,JSK=[ns[k] for k in ('RGJS','PFJS','OPT','CUST','CSS','JSK')]
def src(p): return subprocess.run(['git','-C',SITE,'show','aebb002:site/'+p],capture_output=True,text=True,check=True).stdout
def addcss(s):
    h=s.index('</head>');i=s.rindex('</style>',0,h);return s[:i]+CSS+s[i:]
def patch(s,old,new,cnt=1):
    assert s.count(old)==cnt,(old[:70],s.count(old));return s.replace(old,new)
def f(n): return format(int(n),',')
LI=''
seen=[]
for r in REG:
    if r['url'] not in seen: seen.append(r['url']);LI+='  <li><a href="%s">%s</a></li>\n'%(r['url'],r['src'])
LI+='  <li><a href="https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/04hokenryounituite.html">横浜市「保険料について」（軽減の基準額）</a></li>\n'
TKN='東京23区（目黒区・中野区・江戸川区を除く20区）'

async def run(html,expr):
    async with async_playwright() as p:
        br=await p.chromium.launch();pg=await br.new_page()
        await pg.set_content(html,wait_until='domcontentloaded');v=await pg.evaluate(expr);await br.close();return v

def kojin():
    s=src('kojin-zei/index.html')
    s=addcss(s)
    s=patch(s,''' <div class="in">
  <div class="full">
   <label for="inc">1年の利益（売上から経費を引いた額）</label>''',''' <div class="in">
  <div class="full">
   <label for="reg">住んでいる市区町村（国民健康保険）</label>
   <select id="reg">'''+OPT+'''</select>
  </div>
  '''+CUST+'''
  <div class="full">
   <label for="inc">1年の利益（売上から経費を引いた額）</label>''')
    i=s.index('var C=[[950');j=s.index('var inc=document.getElementById("inc")',i)
    s=s[:i]+RGJS+JSK+s[j:]
    s=patch(s,'k=kokuho(g,old,0,0).t,sh=k+NEN;','k=kokuho(curR(),g,old,0,0).t,sh=k+NEN;')
    s=patch(s,"gser('k'+ao+old,","gser('k'+ao+old+JSON.stringify(curR().p),")
    s=patch(s,'+"・大阪府";','+"・"+curR().s;\n document.getElementById("o-reg").textContent="国民健康保険は"+(curR().f<0?"入力した料率":curR().s+"の令和8年度の料率")+"で計算しています";')
    s=patch(s,'link(inc,incr,render);seg("s-ao"','reg.addEventListener("change",function(){var x=reg.value==="x";if(x)fillCust(RG[lastR]);cust.hidden=!x;render();});cust.addEventListener("input",render);\nlink(inc,incr,render);seg("s-ao"')
    s=patch(s,'<li>単身・事業の所得だけ・大阪府で、前の年も同じ所得だった場合です</li>','<li>単身・事業の所得だけで、前の年も同じ所得だった場合です</li>\n  <li id="o-reg">国民健康保険は東京23区の令和8年度の料率で計算しています</li>')
    # 数字を計算の中身から取り直す
    tmp=s.replace('link(inc,incr,render);seg("s-ao"','window.__c=calc;link(inc,incr,render);seg("s-ao"')
    V=asyncio.run(run(tmp,'''()=>{var c=window.__c,o={rows:{},p:{}};
     [0,1].forEach(function(old){o.rows[old]={};for(var a=2000000;a<=20000000;a+=500000)o.rows[old][a]=c(a,650000,old);});
     var p=o.p;p.a500=c(5000000,650000,0);p.b500=c(5000000,100000,0);p.w500=c(5000000,0,0);p.a800=c(8000000,650000,0);p.b800=c(8000000,100000,0);
     var a;p.kit=0;for(a=2000000;a<=20000000;a+=10000){var x=c(a,650000,0);if(x.k>x.it)p.kit=a;}
     p.kitmono=1;var seenLess=0;for(a=2000000;a<=20000000;a+=10000){var x=c(a,650000,0);if(x.k<=x.it)seenLess=1;else if(seenLess)p.kitmono=0;}
     p.taxsh=0;for(a=2000000;a<=20000000;a+=10000){var x=c(a,650000,0);if(x.tax>x.sh){p.taxsh=a;break;}}
     p.taxshmono=1;for(a=p.taxsh;a<=20000000;a+=10000){var x=c(a,650000,0);if(x.tax<=x.sh)p.taxshmono=0;}
     p.s554=c(5540000,650000,0);p.s555=c(5550000,650000,0);p.s720=c(7200000,650000,0);p.s721=c(7210000,650000,0);
     p.cap=0;for(a=2000000;a<=20000000;a+=10000){if(c(a,650000,0).k>=960000){p.cap=a;break;}}
     p.capo=0;for(a=2000000;a<=20000000;a+=10000){if(c(a,650000,1).k>=1130000){p.capo=a;break;}}
     p.dmin=1e9;p.dmax=0;for(a=2000000;a<=20000000;a+=500000){var d=c(a,650000,0).net-c(a,100000,0).net;if(d<p.dmin)p.dmin=d;if(d>p.dmax)p.dmax=d;}
     return o;}'''))
    P=V['p'];a5=P['a500']
    print('500万',a5,'k>it まで',P['kit'],P['kitmono'],'tax>sh から',P['taxsh'],P['taxshmono'],'上限',P['cap'],P['capo'],'65と10の差',P['dmin'],P['dmax'])
    assert P['kitmono'] and P['taxshmono'] and P['cap'] and P['capo']
    # 表
    def rows(old):
        def one(m):
            a=int(m.group(2).replace(',',''))*10000;x=V['rows'][str(old)][str(a)]
            tot=x['tax']+x['sh'];net=x['net']
            assert net==a-tot
            return '<tr%s><td>%s万円</td><td>%s</td><td>%s</td><td>%s</td><td class="x7kk">%s</td><td>215,040</td><td>%s</td><td>%s</td><td>%s</td><td>%.1f%%</td></tr>'%(m.group(1) or '',m.group(2),f(x['it']),f(x['ju']),f(x['jg']),f(x['k']),f(tot),f(net),f(round(net/12)),net/a*100)
        return one
    parts=s.split('<table class="x7tb x7t10">');assert len(parts)==3
    for n in (1,2):
        j=parts[n].index('</tbody>');body=parts[n][:j]
        body2,c=re.subn(r'<tr( class="x7hl")?><td>([0-9,]+)万円</td>.*?</tr>',rows(n-1),body,flags=re.S);assert c==27,c
        parts[n]=body2+parts[n][j:]
    s='<table class="x7tb x7t10">'.join(parts)
    def man(a): return f(a//10000)
    def oku(n): return '%d万'%round(n/10000)
    tot5=a5['tax']+a5['sh']
    s=patch(s,'利益（売上から経費を引いた額）が500万円なら、個人事業主の手取りは年3,615,257円（月あたり301,271円・手取り率72.3%）です。引かれる1,384,743円のうち、国民健康保険と国民年金が811,143円で、所得税・住民税・個人事業税の合計573,600円より多くなります。',
     '利益（売上から経費を引いた額）が500万円なら、個人事業主の手取りは年%s円（月あたり%s円・手取り率%.1f%%）です。引かれる%s円のうち国民健康保険と国民年金が%s円で、所得税・住民税・個人事業税の合計%s円より%s。'%(f(a5['net']),f(round(a5['net']/12)),a5['net']/50000,f(tot5),f(a5['sh']),f(a5['tax']),'多くなります' if a5['sh']>a5['tax'] else '少なくなります'))
    s=patch(s,'試算の前提（令和8年分・大阪府・単身）','試算の前提（令和8年分・東京23区・単身）')
    s=patch(s,'<li>国民健康保険は大阪府の令和8年度・単身。国民年金は月17,920円（年215,040円）</li>','<li>国民健康保険は'+TKN+'の令和8年度・単身。国民年金は月17,920円（年215,040円）</li>')
    s=patch(s,'国民健康保険は地域で料率が違います。この表は大阪府の料率です。','国民健康保険は市区町村で料率が違います。この表は'+TKN+'の料率です。ほかの市区町村は上の計算で選べます。')
    s=patch(s,'<h3>1. 利益920万円までは、所得税より国民健康保険のほうが多い</h3>','<h3>1. 利益%s万円までは、所得税より国民健康保険のほうが多い</h3>'%man(P['kit']))
    s=patch(s,'上回るのは、利益631万円からです。','上回るのは、利益%s万円からです。'%man(P['taxsh']))
    d1=P['s555']['it']-P['s554']['it'];d2=P['s554']['net']-P['s555']['net'];d3=P['s720']['net']-P['s721']['net']
    print('段差',d1,d2,d3);assert d1>0 and d2>0 and d3>0
    s=patch(s,'利益554万円から555万円になると所得税が年43,600円増え、手取りは年36,284円減ります。利益720万円から721万円では、手取りが年4,784円減ります。','利益554万円から555万円になると所得税が年%s円増え、手取りは年%s円減ります。利益720万円から721万円では、手取りが年%s円減ります。'%(f(d1),f(d2),f(d3)))
    s=patch(s,'<h3>3. 国民健康保険は利益1,114万円で上限に届く</h3><p>大阪府の令和8年度は、単身で年95万円（40〜59歳は介護分を含めて年112万円）が上限です。','<h3>3. 国民健康保険は利益%s万円で上限に届く</h3><p>東京23区の令和8年度は、単身で年96万円（40〜59歳は介護分を含めて年113万円）が上限です。'%man(P['cap']))
    lo,hi=round(P['dmin']/10000),round(P['dmax']/10000)
    s=patch(s,'<h3>5. 青色申告の65万円と10万円で、手取りが年18万〜21万円違う</h3>','<h3>5. 青色申告の65万円と10万円で、手取りが年%d万〜%d万円違う</h3>'%(lo,hi))
    s=patch(s,'利益500万円なら、65万円控除の手取りは年3,615,257円、10万円控除では年3,404,937円、白色申告では年3,365,497円です。利益800万円では、65万円控除と10万円控除の差は年180,170円です。','利益500万円なら、65万円控除の手取りは年%s円、10万円控除では年%s円、白色申告では年%s円です。利益800万円では、65万円控除と10万円控除の差は年%s円です。'%(f(a5['net']),f(P['b500']['net']),f(P['w500']['net']),f(P['a800']['net']-P['b800']['net'])))
    s=patch(s,'<p class="cap" id="t-cap">青色申告65万円・40歳未満・大阪府</p>','<p class="cap" id="t-cap">青色申告65万円・40歳未満・東京23区</p>')
    s=patch(s,'国民健康保険料は大阪府の令和8年度の料率、国民年金は','国民健康保険料は選んだ市区町村の令和8年度の料率、国民年金は')
    s=patch(s,'税金と国民健康保険料が合わせて年およそ25万円少なくなります。','税金と国民健康保険料が合わせて年およそ%d万円少なくなります。'%round((a5['net']-P['w500']['net'])/10000))
    s=patch(s,'<li>大阪府以外に住んでいる場合：国民健康保険の料率が違います</li>','<li>東京23区以外に住んでいる場合：国民健康保険の料率が違います。上の計算で市区町村を選べます</li>')
    s=patch(s,'40歳未満・単身・青色申告65万円・大阪府の場合、年3,615,257円（月あたり301,271円）です。所得税155,400円、住民税313,200円、個人事業税105,000円、国民健康保険596,103円、国民年金215,040円が引かれます。','40歳未満・単身・青色申告65万円・東京23区の場合、年%s円（月あたり%s円）です。所得税%s円、住民税%s円、個人事業税%s円、国民健康保険%s円、国民年金215,040円が引かれます。'%(f(a5['net']),f(round(a5['net']/12)),f(a5['it']),f(a5['ju']),f(a5['jg']),f(a5['k'])))
    s=patch(s,'大阪府の令和8年度は、単身で年95万円です。40〜59歳は介護分が加わり、年112万円です。利益1,114万円あたりで上限に届きます。','東京23区の令和8年度は、単身で年96万円です。40〜59歳は介護分が加わり、年113万円です。利益%s万円あたりで上限に届きます。上限は多くの市区町村で同じ額です。'%man(P['cap']))
    s=patch(s,'所得税・住民税・個人事業税の合計は年およそ57万円です。社会保険料は年およそ81万円です（国民健康保険は大阪府）。','所得税・住民税・個人事業税の合計は年およそ%d万円です。社会保険料は年およそ%d万円です（国民健康保険は東京23区）。'%(round(a5['tax']/10000),round(a5['sh']/10000)))
    s=patch(s,'''  <li><a href="https://www.pref.osaka.lg.jp/o100080/kokuho/iryouseido/hokenryouritsu/hokenryouritsu2.html">大阪府「令和8年度の府内統一保険料率」</a></li>
  <li><a href="https://www.city.neyagawa.osaka.jp/material/files/group/50/R8touitsuhokennryounitsuite.pdf">寝屋川市「令和8年度の統一保険料について」（軽減の基準額）</a></li>
''',LI)
    s=patch(s,'更新日：2026年11月10日（令和8年度税制改正に対応）','更新日：2026年11月16日（令和8年度税制改正に対応）')
    open(SITE+'kojin-zei/index.html','w').write(s);print('kojin-zei ok',len(s))
    return V
if __name__=='__main__' and 'kojin' in sys.argv: kojin()

def houjin():
    import hj
    s=src('houjinnari/index.html')
    s=addcss(s)
    POPT=''.join('<option value="%d"%s>%s（%.2f%%）</option>'%(i,' selected' if p[0]=='東京都' else '',p[0],p[1]/100) for i,p in enumerate(PREF))
    s=patch(s,''' <div class="in">
  <div class="full">
   <label for="inc">1年の利益（売上から経費を引いた額）</label>''',''' <div class="in">
  <div class="full">
   <label for="reg">住んでいる市区町村（個人事業の国民健康保険）</label>
   <select id="reg">'''+OPT+'''</select>
  </div>
  '''+CUST+'''
  <div class="full">
   <label for="pref">会社がある都道府県（法人の協会けんぽ）</label>
   <select id="pref">'''+POPT+'''</select>
  </div>
  <div class="full">
   <label for="inc">1年の利益（売上から経費を引いた額）</label>''')
    i=s.index('var C=[[950');j=s.index('function kiso(g)',i)
    s=s[:i]+RGJS+PFJS+JSK+'var pref=document.getElementById("pref");\n'+s[j:]
    s=patch(s,'k=kokuho(g,old,0,0).t,sh=k+NEN;','k=kokuho(curR(),g,old,0,0).t,sh=k+NEN;')
    s=patch(s,'var ken=r50(s*(1013+23+(old?162:0))/20000)','var ken=r50(s*(PF[+pref.value][1]+23+(old?162:0))/20000)')
    s=patch(s,"gser('d'+old,","gser('d'+old+pref.value+JSON.stringify(curR().p),")
    s=patch(s,'link(inc,incr,render);seg("s-age"','reg.addEventListener("change",function(){var x=reg.value==="x";if(x)fillCust(RG[lastR]);else pref.value=RG[+reg.value].f;cust.hidden=!x;render();});cust.addEventListener("input",render);pref.addEventListener("change",render);\nlink(inc,incr,render);seg("s-age"')
    s=patch(s,'<li>単身・大阪府（国民健康保険・協会けんぽ大阪支部）・法人住民税の均等割は年7万円で計算しています</li>','<li id="o-reg">単身・東京23区の国民健康保険・協会けんぽ東京都で計算しています</li>\n  <li>法人住民税の均等割は年7万円で計算しています</li>')
    s=patch(s,' var hit=-1;ROWS.forEach(function(r,i){if(a>=r*10000)hit=i;});\n var t="";',' document.getElementById("o-reg").textContent="単身・"+(curR().f<0?"入力した料率":curR().s)+"の国民健康保険・協会けんぽ"+PF[+pref.value][0]+"で計算しています";\n var hit=-1;ROWS.forEach(function(r,i){if(a>=r*10000)hit=i;});\n var t="";')
    V=asyncio.run(hj.gen(s,1))
    # 分かれ目
    TH=asyncio.run(run(s.replace('link(inc,incr,render);seg("s-age"','window.__h={kojin:kojin,houjin:houjin,yakuin:yakuin,kyuyo8:kyuyo8,itaxT:itaxT,kiso:kiso,jumin:jumin,cross:cross};link(inc,incr,render);seg("s-age"'),'''()=>{'''+hj.CORP+'''var H=window.__h,o={};
      function d(a,m,old){var y=H.yakuin(m,old),R=m*12,me=y.me*12,co=y.co*12,g=H.kyuyo8(R),it=H.itaxT(g-me-H.kiso(g)),ju=H.jumin(g,me,430000).y,P=a-R-co,cp=P>0?corp(P,1):70000;return (a-H.kojin(a,old))-(me+co+it+ju+cp);}
      [0,1].forEach(function(old){o[old]={all:H.cross(old)+100000};[300000,500000].forEach(function(m){var last=0;for(var a=3000000;a<=30000000;a+=100000){if(d(a,m,old)<=0)last=a;}o[old][m]=last+100000;});
       o[old].k500=5000000-H.kojin(5000000,old);});return o;}'''))
    print('分かれ目',TH)
    def sg(n):
        v=round(n/10000);return ('+%d'%v) if v>0 else ('−%d'%-v if v<0 else '0')
    T=list(re.finditer(r'(<table class="x7tb x7t1[0-9]">.*?</thead>)(.*?)(</table>)',s,flags=re.S));assert len(T)==3
    out=[];PRS=[400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800,2000,2500,3000]
    for ti,old in ((0,'0'),(1,'1')):
        h=''
        for p in PRS:
            r=V[old][str(p)];h+='<tr><td>%s万円</td><td class="x7k">%d</td>'%(f(p),round(r['kt']/10000))
            for c in r['c']:
                cls='x7g' if c['P']<0 else ('x7p' if round(c['d']/10000)>0 else '')
                h+='<td class="%s">%s</td>'%(cls,sg(c['d']))
            a=r['all'];h+='<td class="%s">%s<small>月%d万</small></td></tr>'%('x7p' if round(a['d']/10000)>0 else '',sg(a['d']),round(a['m']/10000))
        out.append(h)
    h=''
    for p in PRS:
        r=V['0'][str(p)];h+='<tr><td>%s万円</td>'%f(p)
        for c in r['c']:
            v=round(c['n']/10000);h+='<td class="%s">%s</td>'%('x7g' if c['P']<0 else '',('−%d'%-v) if v<0 else str(v))
        h+='</tr>'
    out.append(h)
    # 元の表の書き方(tbodyの有無)を保つ
    new=s;off=0
    for m,h in zip(T,out):
        body=m.group(2);pre=body[:body.index('<tr>')];post=body[body.rindex('</tr>')+5:]
        a,b=m.start(2)+off,m.end(2)+off;new=new[:a]+pre+h+post+new[b:];off+=len(pre+h+post)-len(body)
    s=new
    t0,t1=TH['0'],TH['1']
    def mn(v): return f(v//10000)
    s=patch(s,'利益1,250万円から、法人のほうが軽くなります（40〜59歳は1,260万円から）。','利益%s万円から、法人のほうが軽くなります（40〜59歳は%s万円から）。'%(mn(t0['all']),mn(t1['all'])))
    s=patch(s,'利益720万円から、法人のほうが軽くなります（40〜59歳は700万円から）。','利益%s万円から、法人のほうが軽くなります（40〜59歳は%s万円から）。'%(mn(t0['500000']),mn(t1['500000'])))
    s=patch(s,'利益560万円から、法人のほうが軽くなります（40〜59歳は550万円から）。','利益%s万円から、法人のほうが軽くなります（40〜59歳は%s万円から）。'%(mn(t0['300000']),mn(t1['300000'])))
    s=patch(s,'40歳未満・単身・大阪府の場合、役員報酬を月30万円にするなら利益560万円から、月50万円なら720万円から、法人のほうが税金と社会保険料の合計が軽くなります。','40歳未満・単身・東京23区の場合です。役員報酬を月30万円にするなら利益%s万円から、月50万円なら%s万円から法人のほうが税金と社会保険料の合計が軽くなります。'%(mn(t0['300000']),mn(t0['500000'])))
    s=patch(s,'法人のほうが軽くなり始める利益は、役員報酬が月30万円なら550万円、月50万円なら700万円です。','法人のほうが軽くなり始める利益は、役員報酬が月30万円なら%s万円、月50万円なら%s万円です。'%(mn(t1['300000']),mn(t1['500000'])))
    s=patch(s,'試算の前提（令和8年分・大阪府・単身）','試算の前提（令和8年分・東京23区・単身）')
    s=patch(s,'国民健康保険（大阪府の令和8年度）・国民年金</li>','国民健康保険（'+TKN+'の令和8年度）・国民年金</li>')
    s=patch(s,'協会けんぽ大阪支部の令和8年度の料率・厚生年金・子ども・子育て拠出金）、役員報酬にかかる所得税・住民税、会社に残した利益にかかる法人税・地方法人税・法人住民税・法人事業税・特別法人事業税','協会けんぽ東京都の令和8年度の料率・厚生年金・子ども・子育て拠出金）、役員報酬にかかる所得税・住民税、会社に残した利益にかかる法人税・地方法人税・防衛特別法人税・法人住民税・法人事業税・特別法人事業税')
    s=patch(s,'個人事業は所得税・住民税・個人事業税（5%）・国民健康保険（大阪府の令和8年度）・国民年金で計算しています。','個人事業は所得税・住民税・個人事業税（5%）・国民健康保険（選んだ市区町村の令和8年度）・国民年金で計算しています。')
    s=patch(s,'法人の社会保険料は協会けんぽ大阪支部の令和8年度の料率です。','法人の社会保険料は選んだ都道府県の協会けんぽの令和8年度の料率です。')
    s=patch(s,'利益を入れると、その場で比べる計算もできます。大阪府・令和8年分。">','市区町村と都道府県を選んで比べる計算もできます。早見表は東京23区・令和8年分です。">')
    s=patch(s,'''  <li><a href="https://www.pref.osaka.lg.jp/o100080/kokuho/iryouseido/hokenryouritsu/hokenryouritsu2.html">大阪府「令和8年度の府内統一保険料率」</a></li>
  <li><a href="https://www.city.neyagawa.osaka.jp/material/files/group/50/R8touitsuhokennryounitsuite.pdf">寝屋川市「令和8年度の統一保険料について」（軽減の基準額）</a></li>
''',LI.replace('  <li>','  <li>'))
    s=patch(s,'更新日：2026年11月10日（令和8年度税制改正に対応）','更新日：2026年11月16日（令和8年度税制改正に対応）')
    open(SITE+'houjinnari/index.html','w').write(s);print('houjinnari ok',len(s))
    # トップページの2枚
    t=open(SITE+'index.html').read()
    k5=TH['0']['k500']
    t=patch(t,'<p class="a">利益<b>560</b>万円から</p><p class="n">40歳未満・単身・大阪府・令和8年分。','<p class="a">利益<b>%s</b>万円から</p><p class="n">40歳未満・単身・東京23区・令和8年分。'%mn(t0['300000'])) if '利益<b>560</b>万円から' in t else t
    t=patch(t,'<p class="a">年<b>138.5</b>万円</p><p class="n">40歳未満・単身・大阪府・令和8年分。','<p class="a">年<b>%.1f</b>万円</p><p class="n">40歳未満・単身・東京23区・令和8年分。'%(k5/10000)) if '年<b>138.5</b>万円' in t else t
    open(SITE+'index.html','w').write(t);print('top ok',k5)
if __name__=='__main__' and 'houjin' in sys.argv: houjin()
