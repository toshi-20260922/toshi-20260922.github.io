import re,sys,asyncio,subprocess,json
from playwright.async_api import async_playwright
SITE='/home/claude/toshi-20260922.github.io/site/'
CORP='''
function k1(x){return Math.floor(x/1000)*1000;}
function h1(x){return Math.floor(x/100)*100;}
function corp(I,st){var A=k1(Math.max(0,I)),m=12;
 var L=k1(8000000),hz=h1(Math.min(A,L)*0.15+Math.max(0,A-L)*0.232);
 var bo=st?h1(Math.max(0,k1(hz-5000000))*0.04):0;
 var ch=h1(k1(hz)*0.103);
 var t1=4000000,t2=8000000;
 var jg=h1(Math.min(A,t1)*0.035+Math.max(0,Math.min(A,t2)-t1)*0.053+Math.max(0,A-t2)*0.07);
 var tk=h1(jg*0.37);
 var kp=h1(k1(hz)*0.01),sp=h1(k1(hz)*0.06);
 return hz+ch+bo+jg+tk+kp+sp+70000;}
'''
GEN='''(st)=>{var H=window.__h,o={};
 var PR=[400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1800,2000,2500,3000],MS=[20,30,40,50,60,70,80,90,100,120];
 [0,1].forEach(function(old){o[old]={};PR.forEach(function(p){var a=p*10000,kt=a-H.kojin(a,old),row={kt:kt,c:[]};
  MS.forEach(function(mm){var m=mm*10000,y=H.yakuin(m,old),R=m*12,me=y.me*12,co=y.co*12,g=H.kyuyo8(R);
   var it=H.itaxT(g-me-H.kiso(g)),ju=H.jumin(g,me,430000).y,P=a-R-co,cp=P>0?corp(P,st):70000;
   row.c.push({d:kt-(me+co+it+ju+cp),P:P,n:P-cp});});
  var h=H.houjin(a,old);row.all={d:h.net-H.kojin(a,old),m:h.m};o[old][p]=row;});});
 return o;}'''
def cells(tr): return [re.sub(r'<[^>]+>','|',c).strip('|') for c in re.findall(r'<td[^>]*>(.*?)</td>',tr,flags=re.S)]
def num(t): return int(t.replace('−','-').replace('+','').replace(',',''))
async def gen(html,st):
    html=html.replace('link(inc,incr,render);seg("s-age"','window.__h={kojin:kojin,houjin:houjin,yakuin:yakuin,kyuyo8:kyuyo8,itaxT:itaxT,kiso:kiso,jumin:jumin};link(inc,incr,render);seg("s-age"')
    assert '__h' in html
    async with async_playwright() as p:
        br=await p.chromium.launch();pg=await br.new_page();await pg.set_content(html,wait_until='domcontentloaded')
        await pg.add_script_tag(content=CORP);v=await pg.evaluate(GEN,st);await br.close();return v
def tables(s):
    T=[]
    for m in re.finditer(r'<table class="x7tb x7t1[0-9]">(.*?)</table>',s,flags=re.S):
        T.append([cells(tr) for tr in re.findall(r'<tr>(.*?)</tr>',m.group(1).split('</thead>')[1],flags=re.S)])
    return T
if __name__=='__main__':
    s=subprocess.run(['git','-C',SITE,'show','aebb002:site/houjinnari/index.html'],capture_output=True,text=True,check=True).stdout
    T=tables(s);print([len(t) for t in T],[len(t[0]) for t in T])
    for st in (0,1):
        V=asyncio.run(gen(s,st));bad=0;n=0
        for old,t in ((0,T[0]),(1,T[1])):
            for row in t:
                p=str(num(row[0].replace('万円','')));r=V[str(old)][p];n+=1
                if num(row[1])!=round(r['kt']/10000): bad+=1;print('kt',old,p,row[1],r['kt'])
                for i,c in enumerate(r['c']):
                    n+=1
                    if num(row[2+i])!=round(c['d']/10000): bad+=1; print('cell',st,old,p,i,row[2+i],c['d']) if bad<12 else None
                a=row[12].split('|');n+=1
                if num(a[0])!=round(r['all']['d']/10000) or a[-1]!='月%d万'%round(r['all']['m']/10000): bad+=1;print('all',old,p,row[12],r['all'])
        for row in T[2]:
            p=str(num(row[0].replace('万円','')));r=V['0'][p]
            for i,c in enumerate(r['c']):
                n+=1
                if num(row[1+i])!=round(c['n']/10000): bad+=1; print('nokoru',st,p,i,row[1+i],c['n'],c['P']) if bad<12 else None
        print('防衛特別法人税',st,'照らした数',n,'合わない',bad)
