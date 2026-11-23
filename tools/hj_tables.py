# 法人成りのページ(/houjinnari/)の早見表を、今のページの計算(JS)からそのまま作り直す。
# 2026-11-23 本人「ぜんぶなおせー」:
#  1 マスの数字が何か表の上に書く  2 「個人事業のまま」の列を外し、左の列の小さい字にする
#  3 「社長の手取りで比べる」切り替え(会社に残るお金を数えない)  4 行ごとにいちばん得な役員報酬に枠
#  5 表のすぐ下に前提  6 60〜64歳の表(国民年金なし)。65歳以上は年金で変わるので表にしない
# 使い方: python3 tools/hj_tables.py   (何度流しても同じ結果になる)
import re, asyncio, sys
from playwright.async_api import async_playwright
sys.path.insert(0, 'tools')
import hj
P = 'site/houjinnari/index.html'
PRS = [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1800, 2000, 2500, 3000]
MS = [20, 30, 40, 50, 60, 70, 80, 90, 100, 120]
AGES = ['40歳未満', '40〜59歳', '60〜64歳']

def once(s, a, b):
    assert s.count(a) == 1, (a[:80], s.count(a)); return s.replace(a, b)
def man(x): return (x + 5000) // 10000          # 万円・四捨五入(負の数も同じ向き)
def sg(v): return ('+{:,}'.format(v)) if v > 0 else ('−{:,}'.format(-v) if v < 0 else '0')
def un(v): return ('−{:,}'.format(-v)) if v < 0 else '{:,}'.format(v)

s = open(P, encoding='utf-8').read()

# 計算: 60〜64歳は個人事業の国民年金をかけない(介護保険はかかる)
if 'sh=k+(old>1?0:NEN);' not in s:
    s = once(s, 'k=kokuho(curR(),g,old,0,0).t,sh=k+NEN;', 'k=kokuho(curR(),g,old,0,0).t,sh=k+(old>1?0:NEN);')
B3 = '<button type="button" data-v="2">60〜64歳</button>'
for sid in ('s-age', 'bka'):
    i = s.index('id="%s"' % sid); j = s.index('</div>', i)
    if 'data-v="2"' not in s[i:j]: s = s[:j] + B3 + s[j:]
    s = s.replace('<div class="bka" id="bka">', '<div class="bka bka3" id="bka">')
i = s.index('id="s-age"'); s = s[:i] + s[i:].replace('class="seg"', 'class="seg"', 1)

GEN = '''()=>{''' + hj.CORP + '''var H=window.__h,o={};
 var PR=%s,MS=%s;
 [0,1,2].forEach(function(old){o[old]={};PR.forEach(function(p){var a=p*10000,K=H.kojin(a,old),row={K:K,kt:a-K,c:[]};
  MS.forEach(function(mm){var m=mm*10000,y=H.yakuin(m,old),R=m*12,me=y.me*12,co=y.co*12,g=H.kyuyo8(R);
   var it=H.itaxT(g-me-H.kiso(g)),ju=H.jumin(g,me,430000).y,Pf=a-R-co,cp=Pf>0?corp(Pf,1):70000;
   row.c.push({d:(a-K)-(me+co+it+ju+cp),t:R-me-it-ju-K,P:Pf,n:Pf-cp});});
  var h=H.houjin(a,old);row.all={d:h.net-K,m:h.m};o[old][p]=row;});});
 return o;}''' % (PRS, MS)
async def calc(html):
    html = html.replace('link(inc,incr,render);seg("s-age"', 'window.__h={kojin:kojin,houjin:houjin,yakuin:yakuin,kyuyo8:kyuyo8,itaxT:itaxT,kiso:kiso,jumin:jumin};link(inc,incr,render);seg("s-age"', 1)
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page()
        await pg.set_content(html, wait_until='domcontentloaded'); v = await pg.evaluate(GEN); await br.close(); return v
V = asyncio.run(calc(s))

HEAD = '<thead><tr><th>事業の利益<br>（年）</th>' + ''.join('<th>報酬<br>月%d万</th>' % m for m in MS)
def table(old, mode):
    h = '<div class="tw"><table class="x7tb x7t13">' + HEAD + '<th>全額を<br>報酬</th></tr></thead><tbody>'
    for p in PRS:
        r = V[str(old)][str(p)]
        vals = [(man(c['d'] if mode == 'f' else c['t']), c['P']) for c in r['c']]
        av = man(r['all']['d'])
        ok = [v for v, P_ in vals if P_ >= 0] + [av]
        best = max(ok) if max(ok) > 0 else None
        lab = ('個人事業の負担%s万' % '{:,}'.format(man(r['kt']))) if mode == 'f' else ('個人事業の手取り%s万' % '{:,}'.format(man(r['K'])))
        h += '<tr><td>{:,}万円<small>{}</small></td>'.format(p, lab)
        marked = False
        for v, P_ in vals:
            cl = 'x7g' if P_ < 0 else ('x7p' if v > 0 else '')
            if not marked and P_ >= 0 and v == best: cl += ' x7b'; marked = True
            h += '<td class="%s">%s</td>' % (cl.strip(), '赤字' if (mode == 't' and P_ < 0) else sg(v))
        cl = 'x7p' if av > 0 else ''
        if not marked and av == best: cl += ' x7b'
        h += '<td class="%s">%s<small>月%d万</small></td></tr>' % (cl.strip(), sg(av), man(r['all']['m']))
    return h + '</tbody></table></div>'
def ntable(old):
    h = '<div class="tw"><table class="x7tb x7t13">' + HEAD + '</tr></thead><tbody>'
    for p in PRS:
        r = V[str(old)][str(p)]
        h += '<tr><td>{:,}万円</td>'.format(p) + ''.join('<td class="%s">%s</td>' % ('x7g' if c['P'] < 0 else '', un(man(c['n']))) for c in r['c']) + '</tr>'
    return h + '</tbody></table></div>'

LG = {'f': ('法人のほうが税金と社会保険料の合計が軽い', '個人事業のままのほうが軽い'),
      't': ('法人のほうが社長の手取りが多い', '個人事業のままのほうが手取りが多い')}
CAP = {'f': '法人にすると、税金と社会保険料の合計が年いくら軽くなるか（単位は万円）',
       't': '法人にすると、社長の手取りが年いくら増えるか（単位は万円）'}
def block(mode):
    h = '<div data-c="%s"%s><p class="bkcap">%s</p>' % (mode, '' if mode == 'f' else ' hidden', CAP[mode])
    if mode == 't': h += '<p class="bktn">会社に残るお金は数えずに、役員報酬から受け取る手取りと個人事業の手取りを比べています。会社にお金を残しても、社長の手取りは増えません。</p>'
    h += ('<p class="x7lg bklg"><span><i style="background:#dff0d0"></i>プラス：%s</span><span><i style="background:#fff"></i>マイナス：%s</span><span><i style="background:#eceeed"></i>会社が赤字になる組み合わせ</span><span><i class="x7bi"></i>枠：法人にするならいちばん得な役員報酬</span></p>' % LG[mode])
    for old in (0, 1, 2):
        h += '<div data-a="%d"%s>' % (old, '' if old == 0 else ' hidden') + table(old, mode) + '</div>'
    return h + '</div>'

NEWB = ('<h2 id="bunki">法人成りの分岐点 早見表</h2>'
        '<p>事業の利益と役員報酬の組み合わせごとに、法人にした場合と個人事業のままの場合を比べました。左の列の小さい字は、個人事業のままの負担か手取りです。「全額を報酬」の列は利益を役員報酬で払い切る場合で、小さい字はそのときの報酬の月額です。</p>'
        '<div class="bka bkc" id="bkc"><button type="button" class="on" data-v="f">負担の合計で比べる</button><button type="button" data-v="t">手取りで比べる</button></div>'
        '<div class="bka bka3" id="bkt">' + ''.join('<button type="button"%s data-v="%d">%s</button>' % (' class="on"' if i == 0 else '', i, a) for i, a in enumerate(AGES)) + '</div>'
        + block('f') + block('t') +
        '<p class="bktn">単身・東京23区の国民健康保険・協会けんぽ東京都・令和8年分で計算しています。ほかの地域は下の入力欄で選べます。</p>'
        '<p class="bktn">60〜64歳は、個人事業の国民年金の保険料をかけずに計算しています。65歳以上は受け取る年金の額で税金と国民健康保険料が変わるので、この表では扱っていません。</p>')
i = s.index('<h2 id="bunki">'); j = s.index('<div class="bkw" id="bkw">', i)
pre = s[s.rfind('<span id="bunki40"></span>', 0, i + 1):i] if '<span id="bunki40"></span>' in s[i - 40:i] else ''
s = s[:i] + NEWB + '\n' + s[j:]

i = s.index('<h2 id="nokoru">'); j = s.index('<p class="note">グレーは役員報酬と会社負担の社会保険料が利益を上回り', i)
s = s[:i] + ('<h2 id="nokoru">会社に残るお金（法人税などを払ったあと）</h2><p>利益から役員報酬・会社負担の社会保険料・法人税などを引いて、会社に残る金額です。単位は万円です。上の早見表で選んだ年齢で表示しています。</p>'
             + ''.join('<div data-a="%d"%s>' % (o, '' if o == 0 else ' hidden') + ntable(o) + '</div>' for o in (0, 1, 2))) + s[j:]
s = s.replace('<li><a href="#nokoru">会社に残るお金（40歳未満・法人税などを払ったあと）</a></li>', '<li><a href="#nokoru">会社に残るお金（法人税などを払ったあと）</a></li>')

CSS = ('.bka.bka3{grid-template-columns:1fr 1fr 1fr}.bklg span{display:block;margin:2px 0}.bklg i{margin-left:0!important}.bkc button{font-size:13px}.bkcap{font-size:15px;font-weight:700;color:#004d3c;margin:4px 0 6px}'
       '.x7tb td.x7b{outline:2.5px solid #004d3c;outline-offset:-3px}.x7lg i.x7bi{background:#fff;border:2.5px solid #004d3c}'
       '#bkt{max-width:none}.x7t13 td:first-child small{font-size:10px}')
if '.bka.bka3{' not in s: s = s.replace('</style>', CSS + '</style>', 1)

JS = '''<script id="bkjs">(function(){var st={c:'f',a:'0'};function on(id,v){[].forEach.call(document.querySelectorAll('#'+id+' button'),function(b){b.classList.toggle('on',b.dataset.v==v);});}
function show(){[].forEach.call(document.querySelectorAll('[data-c]'),function(e){e.hidden=e.dataset.c!=st.c;});[].forEach.call(document.querySelectorAll('[data-a]'),function(e){e.hidden=e.dataset.a!=st.a;});on('bkc',st.c);on('bkt',st.a);}
document.getElementById('bkc').addEventListener('click',function(e){var b=e.target.closest('button');if(b){st.c=b.dataset.v;show();}});
document.getElementById('bkt').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;st.a=b.dataset.v;show();var x=document.querySelector('#bka button[data-v="'+st.a+'"]');if(x&&!x.classList.contains('on'))x.click();});
var k=document.getElementById('bka');if(k)k.addEventListener('click',function(e){var b=e.target.closest('button');if(b){st.a=b.dataset.v;show();}});})();</script>'''
s = re.sub(r"<script>\(function\(\)\{var t=document.getElementById\('bkt'\).*?</script>", '', s, flags=re.S)
s = re.sub(r'<script id="bkjs">.*?</script>', '', s, flags=re.S)
s = s.replace('</body>', JS + '</body>', 1)

s = s.replace('<li>40歳以上の表は59歳までです。国民年金の保険料は60歳になると払わなくなるので、60歳から64歳は個人事業のままの負担が表より軽くなります</li>',
              '<li>60〜64歳の表は、個人事業の国民年金の保険料をかけずに計算しています。65歳以上は受け取る年金の額で税金と国民健康保険料が変わるので、表にしていません</li>')
q = '法人のほうが軽くなり始める利益は、役員報酬が月30万円なら570万円で月50万円なら740万円です。'
if q in s and '早見表の「60〜64歳」' not in s:
    s = once(s, q, q + '60〜64歳は国民年金の保険料がかからないので、早見表の「60〜64歳」で確かめられます。')
open(P, 'w', encoding='utf-8').write(s)
th = {}
for old in (0, 1, 2):
    th[old] = [p for p in PRS if man(V[str(old)][str(p)]['all']['d']) > 0][:1]
print('全額を報酬で法人の手取りが多くなる最初の行', th)
