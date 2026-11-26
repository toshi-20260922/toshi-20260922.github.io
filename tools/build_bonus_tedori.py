# ボーナス手取り計算 /bonus-tedori/ を作る。2026-11-26 夜。
# 使い方: リポジトリの直下で python3 tools/build_bonus_tedori.py
# 数字: 国税庁「賞与に対する源泉徴収税額の算出率の表（令和8年分）」・「給与所得の源泉徴収税額表（令和8年分）月額表」(tools/getsugaku_r8.json に全行)
#       No.2523（前月の給与が無いとき・10倍を超えるときの計算）・協会けんぽ令和8年度の料率・厚生年金18.3%・雇用保険令和8年度
#       日本年金機構「従業員に賞与を支給したときの手続き」（標準賞与額は1,000円未満切り捨て・健康保険は年度の累計573万円・厚生年金は1か月150万円）
# 結果の形: 明るい地に手取りを1つ大きく出し、その下に 賞与→社会保険料→所得税→手取り の順で内訳を並べる（2026-11-26 T O様の指摘で、白い帯と暗いマスの形は使わない）。
import datetime
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from build_kyuyo_meisai import GR, PF, std, r50d

GT = json.load(open(os.path.join(ROOT, 'tools', 'getsugaku_r8.json'), encoding='utf-8'))
ROWS = GT['rows']                          # [以上, 未満, 0人..7人]
PTS = {int(k): v for k, v in GT['pts'].items()}
SEG = [(740000, 20420), (790000, 23483), (960000, 33693), (1710000, 40840), (2130000, 40840), (2170000, 40840), (2210000, 40840), (2250000, 40840), (3500000, 45945)]
# 算出率の表（令和8年分）甲欄。扶養親族等0〜7人の「未満」の額（千円）と率（%の1000倍）
RATE = [0, 2042, 4084, 6126, 8168, 10210, 12252, 14294, 16336, 18378, 20420, 22462, 24504, 26546, 28588, 30630, 32672, 35735, 38798, 41861, 45945]
UP = [
 [82, 94, 260, 309, 342, 372, 402, 433, 520, 605, 684, 715, 752, 795, 854, 922, 1318, 1521, 2621, 3495],
 [107, 250, 289, 346, 373, 401, 430, 463, 520, 621, 705, 739, 778, 821, 882, 952, 1342, 1526, 2645, 3527],
 [143, 276, 321, 377, 400, 426, 457, 492, 525, 636, 728, 764, 804, 848, 910, 983, 1367, 1526, 2669, 3559],
 [181, 300, 354, 405, 424, 452, 484, 517, 550, 651, 751, 788, 830, 876, 938, 1013, 1391, 1538, 2693, 3590],
 [218, 300, 387, 431, 452, 477, 509, 540, 577, 666, 774, 813, 856, 903, 966, 1044, 1416, 1555, 2716, 3622],
 [251, 304, 412, 457, 479, 503, 531, 564, 604, 681, 798, 838, 881, 930, 994, 1074, 1440, 1555, 2740, 3654],
 [284, 343, 438, 483, 505, 527, 553, 589, 630, 697, 821, 862, 907, 957, 1022, 1104, 1464, 1555, 2764, 3685],
 [317, 383, 463, 508, 529, 552, 578, 614, 657, 708, 845, 887, 933, 985, 1051, 1135, 1489, 1583, 2788, 3717]]
TOKYO = 985

def getsu(x, hg):
    """月額表の甲欄の税額。x は社会保険料を引いたその月の給与。"""
    if x < 105000:
        return 0
    if x < 740000:
        for r in ROWS:
            if r[0] <= x < r[1]:
                return r[2 + hg]
    k = 740000
    for lo, rt in SEG:
        if x >= lo:
            k, r = lo, rt
    return PTS[k][hg] + (x - k) * r // 100000

def shaho_m(m, rate, old, ei):
    if m <= 0:
        return 0
    s = std(m)
    p = min(max(s, 88000), 650000)
    return r50d(s * (rate + 23 + (162 if old == 1 else 0)), 20000) + r50d(p * 1830, 20000) + r50d(m * ei, 10000)

def bonus(b, m, hg=0, rate=TOKYO, old=0, ei=50, kik=6, sk=None):
    sh = b // 1000 * 1000
    ken = r50d(min(sh, 5730000) * (rate + 23 + (162 if old == 1 else 0)), 20000)
    nen = r50d(min(sh, 1500000) * 1830, 20000)
    koy = r50d(b * ei, 10000)
    sb = ken + nen + koy
    k = shaho_m(m, rate, old, ei) if sk is None else min(sk, m)
    a = m - k
    B = b - sb
    if m <= 0 or a <= 0:
        mode, i = 1, -1
        zei = getsu(B // kik, hg) * kik
    elif B > a * 10:
        mode, i = 2, -1
        a0 = max(a, 0)
        zei = (getsu(a0 + B // kik, hg) - getsu(a0, hg)) * kik
    else:
        mode = 0
        c = UP[min(hg, 7)]
        i = 20
        for j, top in enumerate(c):
            if a < top * 1000:
                i = j
                break
        zei = B * RATE[i] // 100000
    zei = max(0, zei)
    return dict(sh=sh, ken=ken, nen=nen, koy=koy, sb=sb, k=k, a=a, i=i, mode=mode, zei=zei, te=b - sb - zei)

def c(n):
    return '{:,}'.format(n)

def pct(i):
    return '%d.%03d%%' % (RATE[i] // 1000, RATE[i] % 1000)

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

BONUS_ROWS = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1200000, 1500000, 2000000, 3000000]
MAE = [200000, 300000, 400000, 500000, 600000]
MAE2 = [150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 600000, 700000, 800000, 1000000]

def man(v):
    return '%s万円' % c(v // 10000)

def hayami_rows(m, old):
    out = []
    for b in BONUS_ROWS:
        g = bonus(b, m, old=old)
        mk = '※' if g['mode'] else ''
        out.append('<tr><td class="l">%s</td><td>%s</td><td>%s%s</td><td><b>%s</b></td></tr>' % (man(b), c(g['sb']), mk, c(g['zei']), c(g['te'])))
    return ''.join(out)

def ritsu_rows():
    out = []
    for m in MAE2:
        g0 = bonus(500000, m, hg=0)
        g1 = bonus(500000, m, hg=1)
        out.append('<tr><td class="l">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (man(m), pct(g0['i']), c(g0['te']), c(g1['te'])))
    return ''.join(out)

CSS = '''<style id="bonus-css">
/* 文の区切りで改行（給与明細の差引支給額と同じ。Chrome・Edge）。対応していない端末はふつうの改行のまま */
main p,.lead2,main li,.hint,.note,main h1,main h2,main h3,main td,main th,main button,main a,main label,main caption{word-break:auto-phrase}
.ph{white-space:nowrap}
.nw{white-space:nowrap}
/* 14px未満の字をなくす（給与明細の差引支給額と同じ） */
.src{font-size:14px}.share a{font-size:14px}.fsb{font-size:14px!important}.auth-h,.auth-r{font-size:14px}table th{font-size:14px}table td small{font-size:14px}
.bt-ctl{display:grid;gap:10px;margin:0 0 12px}
.bt-ctl p{margin:0 0 4px;font-size:14px;font-weight:700}
.bseg{display:flex;flex-wrap:wrap;gap:6px}
.bseg button{font-family:inherit;font-size:15px;font-weight:700;color:#004d3c;background:#ffffff;border:1.5px solid #9cc9b9;border-radius:8px;padding:8px 12px;cursor:pointer}
.bseg button.on{color:#ffffff;background:#00775a;border-color:#00775a}
.bcalc{background:#ffffff;border:2px solid #cfe3d8;border-radius:10px;padding:20px 16px;margin:8px 0 20px}
.bcalc h2{margin-top:0}
.bin{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0 0 18px}
.bin .bf{grid-column:1/3}
.bin label,.bin .lb{display:block;font-size:15px;font-weight:700;margin:0 0 4px;color:#1f2a2a}
.bin .brow{display:flex;align-items:center;gap:8px}
.bin .brow .u{color:#1f2a2a}
#rt{word-break:keep-all;overflow-wrap:anywhere}
.bin input{font-family:inherit;font-size:20px;font-weight:700;color:#1f2a2a;background:#ffffff;border:1px solid #9cc9b9;border-radius:8px;padding:8px 10px;width:100%;max-width:260px}
.bin select{font-family:inherit;font-size:16px;color:#1f2a2a;background:#ffffff;border:1px solid #9cc9b9;border-radius:8px;padding:8px 10px;width:100%}
.bin small{display:block;font-size:14px;color:#5b6666;margin-top:4px}
.bres{background:#ffffff;border:1px solid #cfe3d8;border-radius:10px;padding:18px 16px 16px;color:#1f2a2a}
.bres .bq{display:inline-block;margin:0 0 10px;padding:4px 12px;border-radius:6px;background:#eef6f2;color:#0f3d31;font-size:16px;font-weight:700;line-height:1.6}
.bres .ba{margin:0;line-height:1.2}
.bres .ba b{font-size:44px;font-weight:700;color:#00775a;font-variant-numeric:tabular-nums}
.bres .ba i{font-style:normal;font-size:20px;font-weight:700;color:#00775a;margin-left:2px}
.bres .bp{margin:4px 0 16px;padding:0 0 16px;border-bottom:1px solid #d6e5df;font-size:16px;font-weight:700;color:#0f3d31}
.bres .bh{margin:0 0 4px;font-size:16px;font-weight:700;color:#0f3d31;line-height:1.6}
#calc .bt{width:100%;max-width:560px;border-collapse:collapse;margin:0}
#calc .bt th,#calc .bt td{background:none;border:0;border-bottom:1px solid #e3ece8;padding:9px 0;height:auto;font-size:16px;line-height:1.5;color:#1f2a2a;white-space:nowrap}
#calc .bt th{text-align:left;font-weight:700}
#calc .bt td{text-align:right;font-weight:500;font-variant-numeric:tabular-nums}
#calc .bt tr.sub th,#calc .bt tr.sub td{font-size:15px;font-weight:500;color:#4a5656;padding:5px 0;border-bottom:1px dashed #e3ece8}
#calc .bt tr.sub th{padding-left:1em;white-space:normal}
#calc .bt tr.tt th,#calc .bt tr.tt td{background:#eef6f2;color:#00775a;font-size:18px;font-weight:700;border-bottom:0;padding:10px 8px}
#calc .bt tr.tt th{border-radius:6px 0 0 6px}
#calc .bt tr.tt td{border-radius:0 6px 6px 0}
.bres ul{margin:12px 0 0;padding:0 0 0 1.2em;font-size:14px;color:#4a5656;line-height:1.7}
.bres li{margin:0 0 4px;word-break:auto-phrase}
.bres li::marker{color:#00775a}
@media(max-width:359px){.bres{padding:14px 10px 12px}.bres .ba b{font-size:36px}#calc .bt th,#calc .bt td{font-size:15px}}
</style>'''

JS = r'''(function(){
 var PF=__PF__,GR=__GR__,ROWS=__ROWS__,PTS=__PTS__,SEG=__SEG__,RATE=__RATE__,UP=__UP__;
 function $(i){return document.getElementById(i)}
 function T(i,s){var e=$(i);if(window.PH)e.innerHTML=PH(s);else e.textContent=s}
 function f(n){return Math.round(n).toLocaleString("ja-JP")}
 function r50d(n,d){var q=Math.floor(n/d),r=n-q*d;return r*2>d?q+1:q}
 function std(m){for(var i=0;i<GR.length;i++){if(m<GR[i][1]*1000)return GR[i][0]*1000}return 1390000}
 function getsu(x,hg){if(x<105000)return 0;
  if(x<740000){var lo=0,hi=ROWS.length-1;while(lo<hi){var md=(lo+hi+1)>>1;if(ROWS[md][0]<=x)lo=md;else hi=md-1}return ROWS[lo][2+hg]}
  var k=740000,r=0;for(var i=0;i<SEG.length;i++){if(x>=SEG[i][0]){k=SEG[i][0];r=SEG[i][1]}}
  return PTS[k][hg]+Math.floor((x-k)*r/100000)}
 function shahoM(m,rate,old,ei){if(m<=0)return 0;var s=std(m),p=Math.min(Math.max(s,88000),650000);
  return r50d(s*(rate+23+(old===1?162:0)),20000)+r50d(p*1830,20000)+r50d(m*ei,10000)}
 function bonus(b,m,hg,rate,old,ei,kik,sk){var sh=Math.floor(b/1000)*1000;
  var ken=r50d(Math.min(sh,5730000)*(rate+23+(old===1?162:0)),20000),nen=r50d(Math.min(sh,1500000)*1830,20000),koy=r50d(b*ei,10000),sb=ken+nen+koy;
  var k=sk>=0?Math.min(sk,m):shahoM(m,rate,old,ei),a=m-k,B=b-sb,mode=0,i=-1,zei;
  if(m<=0||a<=0){mode=1;zei=getsu(Math.floor(B/kik),hg)*kik}
  else if(B>a*10){mode=2;var a0=Math.max(a,0);zei=(getsu(a0+Math.floor(B/kik),hg)-getsu(a0,hg))*kik}
  else{var cc=UP[Math.min(hg,7)];i=20;for(var j=0;j<cc.length;j++){if(a<cc[j]*1000){i=j;break}}zei=Math.floor(B*RATE[i]/100000)}
  zei=Math.max(0,zei);return {sh:sh,ken:ken,nen:nen,koy:koy,sb:sb,k:k,a:a,i:i,mode:mode,zei:zei,te:b-sb-zei}}
 window.__bonus=bonus;window.__getsu=getsu;
 function pct(i){var v=RATE[i];return Math.floor(v/1000)+"."+("00"+(v%1000)).slice(-3)+"%"}
 function man(v){return f(v/10000)+"万円"}
 function yen(v){return v%10000===0&&v>0?man(v):f(v)+"円"}
 var BR=__BR__,hm=300000,ho=0;
 function hayami(){var t=$("tb").tBodies[0],h="";
  for(var i=0;i<BR.length;i++){var g=bonus(BR[i],hm,0,985,ho,50,6,-1);
   h+='<tr><td class="l">'+man(BR[i])+'</td><td>'+f(g.sb)+'</td><td>'+(g.mode?"※":"")+f(g.zei)+'</td><td><b>'+f(g.te)+'</b></td></tr>'}
  t.innerHTML=h;T("tb-cap","前月の給与"+man(hm)+"・"+["40歳未満","40〜64歳","65歳以上"][ho]+"・扶養親族0人・東京都")}
 function bseg(id,set,after){$(id).addEventListener("click",function(ev){var b=ev.target.closest("button");if(!b)return;set(+b.getAttribute("data-v"));var bs=$(id).querySelectorAll("button");for(var i=0;i<bs.length;i++)bs[i].className=bs[i]===b?"on":"";after()})}
 bseg("h-mae",function(v){hm=v},hayami);bseg("h-age",function(v){ho=v},hayami);
 var old=0,ei=50,kik=6;
 function num(i,hi){var v=parseInt($(i).value,10);return v>0?Math.min(v,hi):0}
 function render(){var b=num("bon",50000000),m=num("mae",10000000),hg=+$("fu").value,rate=PF[+$("pref").value][1];
  var skv=$("skin").value.trim(),sk=skv===""?-1:num("skin",10000000);
  var g=bonus(b,m,hg,rate,old,ei,kik,sk);
  T("o-q","賞与 "+f(b)+"円 の手取り");
  $("o-te").textContent=f(g.te);
  T("o-p",b>0?"賞与の"+(Math.floor(g.te*1000/b)/10).toFixed(1)+"%が手元に残ります":"賞与の額を入力してください");
  $("o-b").textContent=f(b)+"円";
  $("o-sb").textContent=(g.sb>0?"−":"")+f(g.sb)+"円";
  T("o-kenl",old===1?"健康保険・介護保険":"健康保険");$("o-ken").textContent=f(g.ken)+"円";$("o-nen").textContent=f(g.nen)+"円";$("o-koy").textContent=f(g.koy)+"円";
  $("o-z").textContent=(g.zei>0?"−":"")+f(g.zei)+"円";
  var zd;
  if(g.mode===1)zd=(m>0?"前月の給与が社会保険料以下なので":"前月の給与が無いので")+"、月額表で計算しました（社会保険料を引いた賞与の"+kik+"分の1の税額を"+kik+"倍）";
  else if(g.mode===2)zd="社会保険料を引いた賞与が前月の給与の10倍を超えるので、月額表で計算しました";
  else zd="前月の給与"+yen(m)+"から社会保険料"+f(g.k)+"円を引くと"+f(g.a)+"円なので、率は"+pct(g.i)+"です";
  T("o-zd",zd);
  $("o-te2").textContent=f(g.te)+"円"}
 ["bon","mae","skin"].forEach(function(i){$(i).addEventListener("input",render)});
 ["fu","pref"].forEach(function(i){$(i).addEventListener("change",render)});
 bseg("s-old",function(v){old=v},render);bseg("s-ei",function(v){ei=v},render);bseg("s-kik",function(v){kik=v},render);
 render();
})();'''

def build():
    import build_saitei as B
    import phrase
    g = bonus(500000, 300000)
    g40 = bonus(500000, 300000, old=1)
    g60 = bonus(600000, 300000)
    g45 = bonus(600000, 450000)
    gz = bonus(500000, 0)
    hayami_btn = ''.join('<button type="button"%s data-v="%d">%s</button>' % (' class="on"' if m == 300000 else '', m, man(m)) for m in MAE)
    hay = ('<h2 id="list">ボーナスの額ごとの手取り</h2>\n'
           '<p>賞与10万円から300万円まで、引かれる社会保険料と所得税と手取りを並べました。所得税の率は前月の給与で変わるので、前月の給与と年齢を選んでください。</p>\n'
           '<div class="bt-ctl"><div><p>前月の給与（額面）</p><div class="bseg" id="h-mae">%s</div></div>'
           '<div><p>年齢</p><div class="bseg" id="h-age"><button type="button" class="on" data-v="0">40歳未満</button><button type="button" data-v="1">40〜64歳</button><button type="button" data-v="2">65歳以上</button></div></div></div>\n'
           '<p class="cap" id="tb-cap">前月の給与30万円・40歳未満・扶養親族0人・東京都</p>\n'
           '<div class="tw">\n<table id="tb">\n <thead><tr><th>賞与の額</th><th>社会保険料<br>（円）</th><th>所得税<br>（円）</th><th>手取り<br>（円）</th></tr></thead>\n <tbody>%s</tbody>\n</table>\n</div>\n'
           '<p class="note" style="margin-top:8px">東京都の協会けんぽ・一般の事業で計算しています。所得税に※が付いた行は、社会保険料を引いた賞与が前月の給与の10倍を超えるので月額表で計算した額です。</p>\n'
           % (hayami_btn, hayami_rows(300000, 0)))
    opts = ''.join('<option value="%d"%s>%s</option>' % (i, ' selected' if n == '東京都' else '', n) for i, (n, _) in enumerate(PF))
    fu = ''.join('<option value="%d"%s>%d人</option>' % (i, ' selected' if i == 0 else '', i) for i in range(8))
    calc = '''<section class="bcalc" id="calc">
<h2 id="keisan">自分のボーナスの手取りを計算する</h2>
<div class="bin">
 <div class="bf"><label for="bon">賞与の額（額面）</label><div class="brow"><input type="number" id="bon" inputmode="numeric" min="0" step="1000" value="500000"><span class="u">円</span></div></div>
 <div class="bf"><label for="mae">前月の給与（額面・通勤手当を除く）</label><div class="brow"><input type="number" id="mae" inputmode="numeric" min="0" step="1000" value="300000"><span class="u">円</span></div><small>前月に給与が無いときは0を入力します</small></div>
 <div><label for="fu">扶養親族等の数</label><select id="fu">%s</select></div>
 <div><label for="pref">勤め先の都道府県</label><select id="pref">%s</select></div>
 <div class="bf"><span class="lb">年齢</span><div class="bseg" id="s-old"><button type="button" class="on" data-v="0">40歳未満</button><button type="button" data-v="1">40〜64歳</button><button type="button" data-v="2">65歳以上</button></div><small>70歳以上の人は厚生年金保険料が引かれないので、手取りはこの計算より多くなります</small></div>
 <div class="bf"><span class="lb">雇用保険の業種</span><div class="bseg" id="s-ei"><button type="button" class="on" data-v="50">一般</button><button type="button" data-v="60">農林水産・清酒製造</button><button type="button" data-v="60">建設</button></div></div>
 <div class="bf"><label for="skin">前月の給与から引いた社会保険料</label><div class="brow"><input type="number" id="skin" inputmode="numeric" min="0" step="1" value="" placeholder="空欄なら自動"><span class="u">円</span></div><small>給与明細の額を入れると所得税の率がより正確になります</small></div>
 <div class="bf"><span class="lb">賞与の計算の期間</span><div class="bseg" id="s-kik"><button type="button" class="on" data-v="6">6か月以下</button><button type="button" data-v="12">6か月を超える</button></div><small>前月の給与が無いときなどに使います</small></div>
</div>
<div class="bres" aria-live="polite">
 <p class="bq" id="o-q">賞与 500,000円 の手取り</p>
 <p class="ba"><b id="o-te">%s</b><i>円</i></p>
 <p class="bp" id="o-p">賞与の%s%%が手元に残ります</p>
 <p class="bh">賞与から引かれる額と手取り</p>
 <table class="bt">
  <tbody>
   <tr><th>賞与の額</th><td id="o-b">500,000円</td></tr>
   <tr><th>社会保険料</th><td id="o-sb">−%s円</td></tr>
   <tr class="sub"><th id="o-kenl">健康保険</th><td id="o-ken">%s円</td></tr>
   <tr class="sub"><th>厚生年金</th><td id="o-nen">%s円</td></tr>
   <tr class="sub"><th>雇用保険</th><td id="o-koy">%s円</td></tr>
   <tr><th>所得税</th><td id="o-z">−%s円</td></tr>
   <tr class="tt"><th>手取り</th><td id="o-te2">%s円</td></tr>
  </tbody>
 </table>
 <ul>
  <li>所得税：<span id="o-zd">前月の給与30万円から社会保険料%s円を引くと%s円なので、率は%sです</span></li>
  <li>住民税はボーナスから引かれません。財形や社内の積立がある人は、明細の振込額がこれより少なくなります。</li>
 </ul>
</div>
</section>
''' % (fu, opts, c(g['te']), '%.1f' % (g['te'] * 1000 // 500000 / 10), c(g['sb']), c(g['ken']), c(g['nen']), c(g['koy']), c(g['zei']), c(g['te']), c(g['k']), c(g['a']), pct(g['i']))
    intro = ('<p>ボーナスの手取りは、賞与の額から社会保険料と所得税を引いた額です。住民税は引かれません。所得税の率は賞与の額ではなく、前月の給与と扶養親族等の数で決まります。</p>\n'
             '<p>前月の給与30万円・40歳未満・扶養親族0人・東京都なら、ボーナス50万円の手取りは%s円です。社会保険料%s円と所得税%s円が引かれます。</p>\n' % (c(g['te']), c(g['sb']), c(g['zei'])))
    toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#list">ボーナスの額ごとの手取り</a></li>
  <li><a href="#keisan">自分のボーナスの手取りを計算する</a></li>
  <li><a href="#ritsu">前月の給与ごとの所得税の率</a></li>
  <li><a href="#shaho">ボーナスから引かれる社会保険料</a></li>
  <li><a href="#zei">ボーナスから引かれる所得税</a></li>
  <li><a href="#tokubetsu">前月の給与が無いときと10倍を超えるとき</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">ボーナスの手取りでよく聞かれること</a></li>
 </ol>
</nav>
'''
    sec_ritsu = ('<h2 id="ritsu">前月の給与ごとの所得税の率</h2>\n'
                 '<p>ボーナス50万円で前月の給与だけを変えると、所得税の率と手取りは次のとおりです。40歳未満・東京都で計算しています。</p>\n'
                 '<div class="tw">\n<table id="rt">\n <thead><tr><th>前月の給与</th><th>所得税の率<br>（扶養0人）</th><th>扶養0人の<br>手取り（円）</th><th>扶養1人の<br>手取り（円）</th></tr></thead>\n <tbody>%s</tbody>\n</table>\n</div>\n'
                 '<p class="note" style="margin-top:8px">率は国税庁の「賞与に対する源泉徴収税額の算出率の表」（令和8年分）の甲欄です。前月の給与から社会保険料を引いた額で行を選びます。</p>\n' % ritsu_rows())
    sec_shaho = ('<h2 id="shaho">ボーナスから引かれる社会保険料</h2>\n'
                 '<p>健康保険と厚生年金は、賞与の1,000円未満を切り捨てた標準賞与額に料率をかけます。本人の負担はその半分です。子ども・子育て支援金0.23%%も健康保険料と一緒に引かれます。</p>\n'
                 '<p>40〜64歳は介護保険料1.62%%も加わります。東京都で賞与50万円なら、40歳未満より%s円多く引かれます。65歳以上の介護保険料は賞与からは引かれず、年金などから納めます。</p>\n'
                 '<p>70歳以上の人は厚生年金に入らないので、厚生年金保険料は引かれません。このページは70歳未満として計算しています。</p>\n'
                 '<p>標準賞与額には上限があります。健康保険は4月から翌年3月までの累計で573万円です。厚生年金は1か月150万円で、同じ月に2回出たときは2回の合計で見ます。このページは1回分の賞与で計算しています。</p>\n'
                 '<p>雇用保険料は賞与の額そのものにかけます。一般の事業の本人負担は1,000分の5で、農林水産・清酒製造と建設は1,000分の6です。毎月の保険料は<a href="/shakaihoken/">社会保険料の早見表</a>と<a href="/koyohoken/">雇用保険料の早見表</a>で見られます。</p>\n' % c(g40['sb'] - g['sb']))
    sec_zei = ('<h2 id="zei">ボーナスから引かれる所得税</h2>\n'
               '<p>所得税は、前月の給与から社会保険料を引いた額と扶養親族等の数で率を決めます。その率を、賞与から社会保険料を引いた額にかけます。1円未満は切り捨てです。</p>\n'
               '<p>同じ賞与60万円でも、前月の給与30万円なら所得税は%s円で手取りは%s円です。前月の給与が45万円だと所得税は%s円に増えて、手取りは%s円になります。</p>\n'
               '<p>扶養控除等申告書を出していない人は算出率の表の乙欄の率を使い、所得税は甲欄と同じかそれより多くなります。このページは甲欄で計算していて、乙欄の計算はしていません。</p>\n'
               '<p>ここで引かれる所得税は仮の額です。1年分の税額は12月の<a href="/nenmatsu-chosei/">年末調整</a>で精算されます。率の表を細かく見たい人は<a href="/shoyo-shotokuzei/">賞与の所得税の計算</a>をご覧ください。</p>\n'
               % (c(g60['zei']), c(g60['te']), c(g45['zei']), c(g45['te'])))
    sec_toku = ('<h2 id="tokubetsu">前月の給与が無いときと10倍を超えるとき</h2>\n'
                '<p>次の2つのときは率の表を使わず、毎月の給与と同じ月額表で計算します。国税庁のタックスアンサー No.2523 の決まりです。</p>\n'
                '<ul>\n <li>前月に給与が無いとき（前月の給与が社会保険料以下のときも同じ）：社会保険料を引いた賞与を6で割り、その額の月額表の税額を6倍します</li>\n'
                ' <li>社会保険料を引いた賞与が前月の給与（社会保険料を引いた額）の10倍を超えるとき：賞与を6で割った額に前月の給与を足して月額表で税額を調べ、前月の給与だけの税額を引いてから6倍します</li>\n</ul>\n'
                '<p>前月の給与が社会保険料以下のときの扱いは、国税庁の<a href="https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/15-16.pdf">「賞与に対する源泉徴収税額の算出率の表（令和8年分）」</a>の備考4によります。備考4は「前月中の給与等の金額がない場合や前月中の給与等の金額が前月中の社会保険料等の金額以下である場合」を同じ扱いとし、月額表で計算するとしています。</p>\n'
                '<p>賞与の計算の期間が6か月を超えるときは、6のかわりに12を使います。前月の給与が無い場合に賞与50万円なら、所得税は%s円で手取りは%s円です。</p>\n' % (c(gz['zei']), c(gz['te'])))
    rels = [
        ('shoyo-shotokuzei', '賞与の所得税の計算', '前月の給与ごとの率の表を、扶養の人数ごとに全部見られます。'),
        ('kyuyo-meisai', '給与明細の差引支給額', '毎月の給与から引かれる社会保険料と所得税を計算します。'),
        ('tedori', '年収の手取りの早見表', 'ボーナスを含めた1年の手取りを年収ごとに見られます。'),
        ('tedori-gyakusan', '手取り年収の逆算', '手取りから必要な年収を逆に計算します。'),
        ('nenmatsu-chosei', '年末調整の還付', 'ボーナスで引かれた所得税は、12月の年末調整で精算します。'),
        ('juminzei', '住民税の早見表', 'ボーナスを含めた年収で、翌年の住民税が決まります。'),
        ('nenshu-kabe', '年収の壁', '扶養の壁はボーナスを含めた年収で判定します。'),
    ]
    sec_rel = B.rel('bonus-tedori', rels)
    qa = ('<h2 id="qa">ボーナスの手取りでよく聞かれること</h2>\n'
          '<h3>ボーナス50万円の手取りはいくらですか？</h3>\n'
          '<p>前月の給与30万円・40歳未満・扶養親族0人・東京都なら%s円です。社会保険料%s円と所得税%s円を引いた額です。</p>\n' % (c(g['te']), c(g['sb']), c(g['zei']))
          + '<h3>ボーナスから住民税は引かれますか？</h3>\n'
          '<p>引かれません。住民税は前の年の所得で決まり、毎月の給与から引かれます。ボーナスは翌年の住民税の計算に入ります。</p>\n'
          '<h3>ボーナスの手取りは額面の何割ですか？</h3>\n'
          '<p>40歳未満・扶養親族0人・東京都で前月の給与30万円なら約%d割（%d%%）です。前月の給与が高いほど所得税の率が上がるので、手取りの割合は下がります。</p>\n' % (round(g['te'] * 10 / 500000), round(g['te'] * 100 / 500000))
          + '<h3>40歳になると手取りはいくら減りますか？</h3>\n'
          '<p>介護保険料が加わります。東京都で賞与50万円・前月の給与30万円なら、%s円減って%s円になります。</p>\n' % (c(g['te'] - g40['te']), c(g40['te']))
          + '<h3>ボーナスで引かれすぎた所得税は戻りますか？</h3>\n'
          '<p>ボーナスの所得税は仮の額なので、12月の年末調整で1年分の税額と精算されます。引かれすぎた分は戻ります。</p>\n')
    src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2523.htm">国税庁 タックスアンサー No.2523 賞与に対する源泉徴収</a></li>
  <li><a href="https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/15-16.pdf">国税庁「賞与に対する源泉徴収税額の算出率の表（令和8年分）」</a></li>
  <li><a href="https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/01-07.pdf">国税庁「給与所得の源泉徴収税額表（令和8年分）月額表」</a></li>
  <li><a href="https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20141203.html">日本年金機構「従業員に賞与を支給したときの手続き」</a>（標準賞与額と上限）</li>
  <li><a href="https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08">全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます」</a></li>
  <li><a href="https://www.mhlw.go.jp/content/001692566.pdf">厚生労働省「令和8年度 雇用保険料率のご案内」</a></li>
 </ul>
</div>
'''
    body = CSS + '\n' + hy_wrap(B, hay) + calc + '\n' + B.share('bonus-tedori') + '\n' + intro + '\n' + toc + '\n' + sec_ritsu + '\n' + sec_shaho + '\n' + sec_zei + '\n' + sec_toku + '\n' + sec_rel + '\n' + qa + '\n' + src
    title = '【ボーナス手取り計算】賞与の手取りはいくら？額面ごとの早見表【2026年】'
    desc = 'ボーナスの額面から社会保険料と所得税を引いた手取りを計算します。賞与10万円から300万円までの早見表と、前月の給与・扶養・都道府県を入れる計算があります。令和8年分の国税庁の表と協会けんぽの料率で出します。'
    _d = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    upd = '更新日：%d年%d月%d日（国税庁・全国健康保険協会・日本年金機構・厚生労働省）' % (_d.year, _d.month, _d.day)
    upd_nw = '更新日：<span class="nw">%d年%d月%d日</span>（<span class="nw">国税庁</span>・<span class="nw">全国健康保険協会</span>・<span class="nw">日本年金機構</span>・<span class="nw">厚生労働省</span>）' % (_d.year, _d.month, _d.day)
    js = (JS.replace('__GR__', json.dumps([list(x) for x in GR])).replace('__PF__', json.dumps(PF, ensure_ascii=False))
          .replace('__ROWS__', json.dumps(ROWS, separators=(',', ':'))).replace('__PTS__', json.dumps({str(k): v for k, v in PTS.items()}, separators=(',', ':')))
          .replace('__SEG__', json.dumps(SEG)).replace('__RATE__', json.dumps(RATE)).replace('__UP__', json.dumps(UP)).replace('__BR__', json.dumps(BONUS_ROWS)))
    # 率の表は、4:26版（型の phrase.py）と同じく文節の包みを外して <wbr> にする（このページの表だけ・本番のほかのページは変えない）
    js += '\n(function(){var t=document.getElementById("rt");if(!t)return;var sp=t.querySelectorAll("span.ph"),i,f;for(i=0;i<sp.length;i++){f=document.createDocumentFragment();while(sp[i].firstChild)f.appendChild(sp[i].firstChild);if(sp[i].nextSibling)f.appendChild(document.createElement("wbr"));sp[i].replaceWith(f);}})();\n'
    html = B.page('bonus-tedori', title, desc, upd, body, js, 'bonus-tedori', auth=B.auth_box('国税庁・全国健康保険協会（協会けんぽ）・日本年金機構・厚生労働省'))
    close = ('<div class="close"><p class="close-h"><span class="nw">賞与の計算も、</span><span class="nw">帳簿と申告も</span></p>'
             '<p>賞与から引く社会保険料と所得税は、毎月の給与計算と年末調整につながります。記帳から決算・申告まで、まるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="bonus-tedori_close_marunage">経理丸投げの無料相談</a></div>')
    html = re.sub(r'<div class="close">.*?</div>', close, html, count=1, flags=re.S)
    # このページの data-cta は「bonus-tedori_」で始める（2026-11-27 見張り）
    html = html.replace('data-cta="rel_bonus-tedori_', 'data-cta="bonus-tedori_rel_')
    bad = check_commas(html)
    if bad:
        raise SystemExit('読点が2つ: ' + ' / '.join(bad[:8]))
    path = os.path.join(ROOT, 'site', 'bonus-tedori', 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    html = phrase.apply_page(html)
    # 題名の帯の日付と出典の名前が途中で折れないようにする（帯は文節の包みの外なので、包んだあとに入れる）
    if html.count('<p class="upd">' + upd) != 1:
        raise SystemExit('更新日の帯が見つからない')
    html = html.replace('<p class="upd">' + upd, '<p class="upd">' + upd_nw, 1)
    open(path, 'w', encoding='utf-8').write(html)
    wire()
    print('bonus-tedori', g)

# 本番（5e91574）の build_saitei.hy_wrap は古い入力の案内（自分の数字で…）を入れる。このページは、本番の給与明細の差引支給額と
# 4:26 版（型の build_saitei.py）と同じ「ご自分の金額で計算する場合は、下の欄に入力してください。」にする（2026-11-27）
# 本番（5e91574）の phrase.py は <span>円</span> を span.ph で包み直すので、入力欄の「円」は class="u" の span にして
# 親の指定（.bin .brow .u）が文節の包みに当たらないようにした。率の表は本番の包み方だと列の幅の分け方が変わり、幅390で
# 「手取り」「（円）」の2行に分かれるので、4:26版と同じく表の中だけ包みを外して <wbr> にし、keep-all にした（4:26版と同じ高さ）。2026-11-27 8:20 JST
def hy_wrap(B, sec):
    s = B.hy_wrap(sec)
    old = '<p class="lead2">自分の数字で計算したい人は、下に入力してください。</p>'
    new = '<p class="lead2">ご自分の金額で計算する場合は、下の欄に入力してください。</p>'
    if old in s:
        s = s.replace(old, new)
    if new not in s:
        raise SystemExit('入力の案内が見つからない')
    return s

def wire():
    pj = os.path.join(ROOT, 'tools', 'pages.json')
    raw = open(pj, encoding='utf-8').read()
    if '/bonus-tedori/' not in raw:
        raw = raw.rstrip()
        if not raw.endswith(']'):
            raise SystemExit('pages.json')
        raw = raw[:-1].rstrip() + ',\n {\n  "path": "/bonus-tedori/",\n  "label": "ボーナス手取り計算",\n  "kw": "ボーナス 賞与 手取り 計算 社会保険料 所得税"\n }\n]\n'
        open(pj, 'w', encoding='utf-8').write(raw)
    hj = os.path.join(ROOT, 'tools', 'hayami_first.json')
    h = json.load(open(hj, encoding='utf-8'))
    if 'bonus-tedori' not in h:
        h['bonus-tedori'] = 'list'
        json.dump(h, open(hj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        open(hj, 'a', encoding='utf-8').write('\n')
    sm = os.path.join(ROOT, 'site', 'sitemap.xml')
    sx = open(sm, encoding='utf-8').read()
    if '/bonus-tedori/' not in sx:
        line = '<url><loc>https://taxtable.jp/bonus-tedori/</loc><lastmod>%s</lastmod></url>\n' % (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
        sx = sx.replace('</urlset>', line + '</urlset>')
        open(sm, 'w', encoding='utf-8').write(sx)
    note = 'ボーナスから<span class="nw">社会保険料と</span><span class="nw">所得税を</span><span class="nw">引いた手取りを</span><span class="nw">計算します。</span>'
    label = 'ボーナス手取り計算'
    for slug in ('shoyo-shotokuzei', 'kyuyo-meisai', 'tedori', 'koyohoken'):
        fp = os.path.join(ROOT, 'site', slug, 'index.html')
        s = open(fp, encoding='utf-8').read()
        if '/bonus-tedori/' in s.split('<nav class="tools">')[0]:
            continue
        li = '<li>%s<a href="/bonus-tedori/" data-cta="rel_%s_bonus-tedori">%s</a></li>' % (note, slug, label)
        s2, n = re.subn(r'(<ul class="rl">.*?)(</ul>)', lambda m: m.group(1) + li + m.group(2), s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit('関連リンクを足せない ' + slug)
        open(fp, 'w', encoding='utf-8').write(s2)

if __name__ == '__main__':
    if '--check' in sys.argv:
        print(getsu(444541, 1), getsu(166531, 1), getsu(128216, 0))   # 国税庁 No.2523 の例: 16,100・1,510・1,300
        print(bonus(500000, 300000))
        print(bonus(600000, 300000)['te'], bonus(600000, 450000)['te'])
    else:
        build()
