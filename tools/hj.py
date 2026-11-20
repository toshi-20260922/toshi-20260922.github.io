import re,sys,asyncio,subprocess,json
from playwright.async_api import async_playwright
SITE='/home/claude/toshi-20260922.github.io/site/'
# 2026-11-20:会社の所得は、毎年同じ利益が続く姿として前の年の分の法人事業税・特別法人事業税を引いてから出す。
# 法人住民税の均等割は損金にならないので引かない(国税庁 No.5300)。tools/seikaku/houjinnari.py とは別に書いた計算で、表の全マスを照らす。
CORP='''
function k1(x){return Math.floor(x/1000)*1000;}
function h1(x){return Math.floor(x/100)*100;}
function jz(A){var jg=h1((Math.min(A,4000000)*35+Math.max(0,Math.min(A,8000000)-4000000)*53+Math.max(0,A-8000000)*70)/1000);return jg+h1(jg*37/100);}
function corp(P,st){var I=P;for(var n=0;n<30;n++)I=P-jz(k1(Math.max(0,I)));
 var A=k1(Math.max(0,I)),hz=h1((Math.min(A,8000000)*150+Math.max(0,A-8000000)*232)/1000),kz=k1(hz);
 var bo=st?h1(k1(Math.max(0,kz-5000000))*4/100):0;
 return hz+h1(kz*103/1000)+bo+jz(A)+h1(kz/100)+h1(kz*6/100)+70000;}
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
    s=open(SITE+'houjinnari/index.html',encoding='utf-8').read()
    T=tables(s);print([len(t) for t in T],[len(t[0]) for t in T])
    for st in (0,1):
        V=asyncio.run(gen(s,st));bad=0;n=0
        for old,t in ((0,T[0]),(1,T[1])):
            for row in t:
                p=str(num(row[0].replace('万円','')));r=V[str(old)][p];n+=1
                if num(row[1])!=int((r['kt']+5000)//10000): bad+=1;print('kt',old,p,row[1],r['kt'])
                for i,c in enumerate(r['c']):
                    n+=1
                    if num(row[2+i])!=int((c['d']+5000)//10000): bad+=1; print('cell',st,old,p,i,row[2+i],c['d']) if bad<12 else None
                a=row[12].split('|');n+=1
                if num(a[0])!=int((r['all']['d']+5000)//10000) or a[-1]!='月%d万'%int((r['all']['m']+5000)//10000): bad+=1;print('all',old,p,row[12],r['all'])
        for row in T[2]:
            p=str(num(row[0].replace('万円','')));r=V['0'][p]
            for i,c in enumerate(r['c']):
                n+=1
                if num(row[1+i])!=int((c['n']+5000)//10000): bad+=1; print('nokoru',st,p,i,row[1+i],c['n'],c['P']) if bad<12 else None
        print('防衛特別法人税',st,'照らした数',n,'合わない',bad)
