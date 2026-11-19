# 最低賃金のページ(全国と都道府県)を作る。2026/11/17 夜。
# 使い方:リポジトリの直下で python3 tools/build_saitei.py
# 金額:厚生労働省「令和8年度地域別最低賃金額答申状況」(001745621.pdf)
import math, os, re, json, datetime
# 作る日(日本時間)。発効日がこの日より後のページは「になります」と書く
_t = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
TODAY = (_t.year, _t.month, _t.day)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
OSAKA = open(os.path.join(SITE, 'saitei-chingin-osaka', 'index.html'), encoding='utf-8').read()

# 都道府県・令和8年度・令和7年度・発効日(答申の予定日)
RAW = """北海道 1131 1075 10/1
青森県 1090 1029 10/29
岩手県 1090 1031 12/1
宮城県 1098 1038 10/1
秋田県 1090 1031 10/14
山形県 1092 1032 10/30
福島県 1094 1033 10/16
茨城県 1136 1074 10/18
栃木県 1125 1068 10/1
群馬県 1120 1063 10/3
埼玉県 1196 1141 10/1
千葉県 1195 1140 10/1
東京都 1280 1226 10/1
神奈川県 1279 1225 10/1
新潟県 1108 1050 10/1
富山県 1119 1062 10/1
石川県 1113 1054 10/3
福井県 1112 1053 10/4
山梨県 1113 1052 11/1
長野県 1117 1061 10/2
岐阜県 1121 1065 10/1
静岡県 1154 1097 10/15
愛知県 1195 1140 10/1
三重県 1143 1087 10/1
滋賀県 1136 1080 10/3
京都府 1180 1122 11/16
大阪府 1231 1177 10/1
兵庫県 1172 1116 10/1
奈良県 1107 1051 10/4
和歌山県 1101 1045 10/3
鳥取県 1090 1030 10/3
島根県 1092 1033 10/10
岡山県 1104 1047 10/2
広島県 1141 1085 10/11
山口県 1101 1043 10/8
徳島県 1103 1046 11/1
香川県 1092 1036 10/1
愛媛県 1093 1033 11/1
高知県 1086 1023 10/29
福岡県 1114 1057 10/4
佐賀県 1095 1030 11/15
長崎県 1087 1031 11/2
熊本県 1092 1034 12/1
大分県 1096 1035 11/1
宮崎県 1085 1023 10/24
鹿児島県 1090 1026 10/25
沖縄県 1086 1023 12/2"""
P = []
for ln in RAW.split('\n'):
    n, a, b, d = ln.split()
    mo, da = d.split('/')
    P.append(dict(name=n, new=int(a), old=int(b), mo=int(mo), da=int(da)))
D = {p['name']: p for p in P}
assert len(P) == 47
# 答申の増え方の分布(厚労省の発表)と合うか
from collections import Counter
cnt = Counter(p['new'] - p['old'] for p in P)
assert cnt == Counter({65: 1, 64: 1, 63: 2, 62: 2, 61: 4, 60: 4, 59: 5, 58: 4, 57: 7, 56: 11, 55: 3, 54: 3}), cnt
assert max(p['new'] for p in P) == 1280 and min(p['new'] for p in P) == 1085

def rank(n):
    v = D[n]['new']
    return 1 + sum(1 for p in P if p['new'] > v)

def c(n):
    return '{:,}'.format(n)

def mon(m, hol, h=8):
    return math.ceil(m * (365 - hol) * h / 12 - 1e-9)

def hrs(hol, h=8):
    return (365 - hol) * h / 12

def f1(x):
    return '{:,.1f}'.format(math.floor(x * 10 + 1e-9) / 10)

def man(y):
    # 201064 → 20万1,064円
    a, b = divmod(y, 10000)
    return '%d万%s円' % (a, c(b)) if b else '%d万円' % a

def ds(p):
    return '2026年%d月%d日' % (p['mo'], p['da'])

# ---- 共通の部品(大阪のページから取る) ----
STYLE = OSAKA[OSAKA.index('<style>'):OSAKA.index('</head>')]
HEAD_END = '</head>'
AUTH = re.search(r'<div class="auth" id="auth">.*?</div>', OSAKA, re.S).group(0)
TOOLS_NAV = re.search(r'<nav class="tools">.*?</nav>', OSAKA, re.S).group(0)
FOOT = OSAKA[OSAKA.index('</main>\n<footer'):OSAKA.index('<div class="fbar one">')]
TAIL = OSAKA[OSAKA.index('<script id="fbzj">'):]
LOGO = re.search(r'<a class="logo" href="/">.*?</a>', OSAKA, re.S).group(0)
PIC = re.search(r'<div class="pic">.*?</div>', OSAKA, re.S).group(0)
PIC_YEN = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="人と円"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><circle cx="25" cy="24" r="8" fill="#0f3d31"/><path d="M11 50c1-10 7-15 14-15s13 5 14 15z" fill="#0f3d31"/><circle cx="46" cy="40" r="10" fill="#e3b465"/><text x="46" y="45" font-size="13" font-weight="700" text-anchor="middle" fill="#0f3d31" font-family="sans-serif">円</text></svg></div>'
STYLE = STYLE  # 同じ見た目

def page(slug, title, desc, upd, body, script, cta, pic=PIC_YEN):
    url = 'https://taxtable.jp/%s/' % slug
    return ('<!doctype html>\n<html lang="ja"><head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="color-scheme" content="light">\n'
            '<title>%s</title>\n<link rel="canonical" href="%s">\n<meta name="description" content="%s">\n%s</head>\n<body>\n'
            '<header class="hd"><div class="wrap">\n %s\n <nav><a href="/#list">早見表・計算ツール</a><a href="#auth">監修した税理士</a></nav>\n'
            ' <div class="hcta"><a class="y" href="https://oyama-toshiro.com/contact/" data-cta="%s_head_marunage">経理丸投げの無料相談 →</a></div>\n</div></header>\n\n'
            '<main class="wrap">\n<div class="top">\n %s\n <p class="upd">%s</p>\n <h1>%s</h1>\n</div>\n\n%s\n%s\n%s\n%s'
            '<div class="fbar one">\n <a class="k" href="https://oyama-toshiro.com/contact/" data-cta="%s_fbar_marunage"><small>全国オンライン対応</small><span>経理丸投げの無料相談 ›</span></a>\n</div>\n\n'
            '<script>\n%s\n</script>\n\n%s') % (title, url, desc, STYLE, LOGO, cta, pic, upd, title, body, AUTH, close_box(cta), TOOLS_NAV + '\n' + FOOT, cta, script, TAIL)

def close_box(cta):
    return ('<div class="close"><p class="close-h"><span class="nw">最低賃金が上がる年の、</span><span class="nw">帳簿と申告も</span></p>'
            '<p>最低賃金が上がると、給料の額も帳簿に付ける人件費も変わります。記帳から決算・申告まで、まるごとお受けしています。全国どこからでも対応します。初回のご相談は無料、オンラインでもお受けしています。</p>'
            '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="%s_close_marunage">経理丸投げの無料相談</a></div>') % cta

def share(slug):
    u = 'https://taxtable.jp/%s/' % slug
    return '<div class="share">\n <a class="ln" href="https://social-plugins.line.me/lineit/share?url=%s">LINEで送る</a>\n <a class="x" href="https://x.com/intent/post?url=%s">Xでポストする</a>\n</div>\n' % (u, u)

def rel(slug, items):
    li = ''.join('<li>%s<a href="/%s/" data-cta="rel_%s_%s">%s</a></li>' % (t, h, slug, h, l) for h, l, t in items)
    return '<style>.rl{list-style:none;padding:0;margin:0 0 24px}.rl li{padding:12px 0;border-bottom:1px solid #e6eaea;line-height:1.7}.rl a{display:block;font-weight:700;color:#00775a;margin-top:2px}</style><h2 id="rel">次に確かめること</h2><ul class="rl">%s</ul>\n' % li

def table(head, rows, hit=None):
    th = ''.join('<th>%s</th>' % h for h in head)
    tr = ''
    for i, r in enumerate(rows):
        cls = ' class="hit"' if hit is not None and i == hit else ''
        tr += '<tr%s>%s</tr>' % (cls, ''.join(r))
    return '<div class="tw">\n<table>\n <thead><tr>%s</tr></thead>\n <tbody>%s</tbody>\n</table>\n</div>\n' % (th, tr)

def td(x, cls=''):
    return '<td%s>%s</td>' % (' class="%s"' % cls if cls else '', x)

FUKUMU = '''<h2 id="fukumu">最低賃金に含める賃金・含めない賃金</h2>
<p>最低賃金と比べるのは、毎月決まって払う基本的な賃金だけです。給料の総額をそのまま比べると、実際より高く見えて判定を誤ります。</p>
<h3>含めるもの</h3>
<ul>
 <li>基本給</li>
 <li>職務手当・役職手当・資格手当など毎月決まって払う手当</li>
</ul>
<h3>含めないもの</h3>
<ul>
 <li>結婚手当など臨時に払う賃金</li>
 <li>賞与など1か月を超える期間ごとに払う賃金</li>
 <li>残業代・休日出勤の手当・深夜の割増分</li>
 <li>精皆勤手当・通勤手当・家族手当</li>
</ul>
'''

SRC_COMMON = '''  <li><a href="https://www.mhlw.go.jp/stf/newpage_75950.html">厚生労働省「全ての都道府県で地域別最低賃金の改定額が答申されました」</a>（令和8年9月3日）</li>
  <li><a href="https://www.mhlw.go.jp/content/11302000/001745621.pdf">厚生労働省「令和8年度地域別最低賃金額答申状況」</a></li>
  <li><a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/chingin/newpage_43899.html">厚生労働省「最低賃金額以上かどうかを確認する方法」</a></li>
  <li><a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/chingin/newpage_43875.html">厚生労働省「最低賃金の対象となる賃金」</a></li>
  <li><a href="https://elaws.e-gov.go.jp/document?lawid=334AC0000000137">e-Gov法令検索「最低賃金法」</a>（第4条・第6条・第7条・第40条）</li>
'''

# ---- 都道府県のページ ----
JS_PREF = r'''(function(){
 var BASE=%(base)d,OLD=%(old)d,PN="%(pn)s",DATE="%(date)s",EFF="%(eff)s",PRE=new Date()<new Date(EFF),NB=PRE?OLD:BASE;
 var IND=%(ind)s;
 var k=0,$=function(i){return document.getElementById(i)};
 function f(n){return Math.round(n).toLocaleString("ja-JP");}
 function f1(n){return (Math.floor(n*10+1e-9)/10).toLocaleString("ja-JP",{minimumFractionDigits:1,maximumFractionDigits:1});}
 function num(i){var v=parseFloat($(i).value);return isNaN(v)?0:v;}
 function render(){
  var pay=num("pay"),ex=num("ex"),base=Math.max(0,pay-ex),div=1,lbl=["時給","日給","月給"][k];
  $("pay-l").textContent=lbl;
  $("w-day").classList.toggle("hide",k!==1);$("w-mon").classList.toggle("hide",k!==2);
  if(k===1){div=Math.max(0.25,num("dh"));}
  if(k===2){div=Math.max(1,(365-Math.min(300,num("hol")))*Math.max(0.25,num("mh"))/12);}
  var h=base/div,ix=$("ind")?+$("ind").value:0,x=IND[ix],fut=x.length>3&&new Date()<new Date(x[3]),cur=ix===0?NB:(fut?x[4]:x[1]),M=Math.max(NB,cur),sp=ix>0&&cur>NB;
  var ok=h>=M-1e-9,gap=Math.max(0,M-h);
  $("o-h").innerHTML=f1(h)+"<i>円</i>";
  $("o-hn").textContent=k===0?"含めない手当を除く":k===1?"日給÷"+div+"時間":"月給÷"+f1(div)+"時間";
  $("o-m").innerHTML=f(M)+"<i>円</i>";
  $("o-mn").textContent=(sp?(fut?x[5]:x[2])+"から"+(fut?"・"+x[2]+"から"+f(x[1])+"円":""):(PRE?"改定前の額・"+DATE+"から"+f(BASE)+"円":DATE+"から"));
  var vd=$("vd");vd.className="vd"+(ok?" no":"");
  if(ok){$("o-vd").textContent="満たしています";$("o-vds").textContent=(h-M<0.05)?"時給に直すと"+f1(h)+"円で、最低賃金"+f(M)+"円と同じ額です":"時給に直すと"+f1(h)+"円で、最低賃金"+f(M)+"円より"+f1(h-M)+"円高い額です";}
  else{var per=k===0?"":(k===1?"1日あたり":"1か月あたり")+f(Math.ceil(gap*div-1e-9))+"円足りません。";
   $("o-vd").textContent="下回っています";$("o-vds").textContent="最低賃金"+f(M)+"円より時給あたり"+f1(gap)+"円足りません。"+per+"差額を払う必要があります";}
  $("o-old").textContent=PRE?DATE+"からの"+f(BASE)+"円と比べると"+(h>=BASE-1e-9?"満たしています":"下回っています（時給あたり"+f1(BASE-h)+"円）"):"改定前の"+f(OLD)+"円と比べると"+(h>=OLD-1e-9?"満たしています":"下回っています（時給あたり"+f1(OLD-h)+"円）");
 }
 ["pay","ex","dh","hol","mh"].forEach(function(i){$(i).addEventListener("input",render);});
 if($("ind"))$("ind").addEventListener("change",render);
 document.querySelectorAll(".seg button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".seg button").forEach(function(y){y.classList.remove("on");});b.classList.add("on");k=+b.dataset.k;
  if(k===0)$("pay").value=%(ex_h)d;if(k===1)$("pay").value=%(ex_d)d;if(k===2)$("pay").value=%(ex_m)d;render();});});
 render();
})();'''


def pref_page(cfg):
    n = cfg['name']; p = D[n]; m = p['new']; o = p['old']; up = m - o
    slug = 'saitei-chingin-' + cfg['slug']; cta = 'saitei_' + cfg['slug']
    word = cfg['word']; short = cfg['short']
    title = '【%s】2026年はいくら？時給%s円と月給の目安・計算【令和8年度】' % (word, c(m))
    m120 = mon(m, 120); m105 = mon(m, 105)
    desc = '%sの最低賃金は%sから時給%s円です。年間休日ごとの月給の目安・%sの特定最低賃金・近くの都道府県との比較を早見表にしました。時給・日給・月給を入れると最低賃金を下回っていないかが分かります。' % (n, ds(p), c(m), n)
    upd = '更新日：%s（厚生労働省・%s 令和8年度の%s最低賃金）' % (cfg.get('upd', '2026年11月17日'), cfg['kyoku'], n)
    ind = cfg.get('ind', [])
    IND = [[n + '最低賃金（下の業種以外）', m, ds(p)]] + ind
    sel = ''
    if ind:
        opts = ''.join('<option value="%d">%s</option>' % (i, x[0]) for i, x in enumerate(IND))
        sel = '  <div class="full">\n   <label for="ind">働いている事業場の業種</label>\n   <select id="ind">%s</select>\n  </div>\n' % opts
    ex_h = (m // 10) * 10 - 30
    calc = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span>%(n)sの最低賃金は%(ds)sから時給%(m)s円です</div>
 <div class="amt">
  <div><small>%(n)sの<br>最低賃金</small><b>%(m)s<i>円</i></b><em>%(ds)sから</em></div>
  <div><small>前の年度</small><b>%(o)s<i>円</i></b><em>改定の前日まで</em></div>
  <div><small>上がった額</small><b>%(up)d<i>円</i></b><em>時給あたり</em></div>
 </div>
 <div class="in">
  <div class="full">
   <label>給料の払い方</label>
   <div class="seg seg3"><button type="button" class="on" data-k="0">時給</button><button type="button" data-k="1">日給</button><button type="button" data-k="2">月給</button></div>
  </div>
  <div class="full">
   <label for="pay" id="pay-l">時給</label>
   <div class="row"><input type="number" id="pay" inputmode="numeric" min="0" max="10000000" step="1" value="%(exh)d"><span>円</span></div>
  </div>
  <div class="full">
   <label for="ex" id="ex-l">このうち最低賃金に含めない手当（通勤手当・家族手当・精皆勤手当・残業代など）</label>
   <div class="row"><input type="number" id="ex" inputmode="numeric" min="0" max="10000000" step="1" value="0"><span>円</span></div>
  </div>
  <div class="full hide" id="w-day">
   <label for="dh">1日の決まった労働時間</label>
   <div class="row"><input type="number" id="dh" inputmode="decimal" min="1" max="24" step="0.25" value="8"><span>時間</span></div>
  </div>
  <div class="full hide" id="w-mon">
   <label for="hol">年間の休日の日数（会社の年間カレンダー）</label>
   <div class="row"><input type="number" id="hol" inputmode="numeric" min="0" max="300" step="1" value="120"><span>日</span></div>
   <label for="mh">1日の決まった労働時間</label>
   <div class="row"><input type="number" id="mh" inputmode="decimal" min="1" max="24" step="0.25" value="8"><span>時間</span></div>
  </div>
%(sel)s </div>
 <div class="vd" id="vd"><b id="o-vd"></b><span id="o-vds"></span></div>
 <div class="amt jdg">
  <div><small>時給に直すと</small><b id="o-h"></b><em id="o-hn"></em></div>
  <div><small>比べる最低賃金</small><b id="o-m"></b><em id="o-mn"></em></div>
 </div>
 <ul>
  <li id="o-old"></li>
  <li>%(mid)s</li>
  <li>本社ではなく、その人が働いている%(n)s内の事業場で判定します</li>
 </ul>
</div>
''' % dict(n=n, ds=ds(p), m=c(m), o=c(o), up=up, exh=ex_h, sel=sel, mid=cfg['mid'])
    intro = '<p>%sの最低賃金は、%sから時給%s円%s。前の年度の%s円から%d円の引上げで、全国で%d番目に高い額です。<span class="mk">年間休日120日・1日8時間の月給なら、月%sが最低ラインです。</span>%s</p>\n' % (n, ds(p), c(m), 'になります' if (2026, p['mo'], p['da']) > TODAY else 'になりました', c(o), up, rank(n), man(m120), cfg['intro'])
    toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#list">月給にすると最低いくらか（年間休日ごと）</a></li>
  <li><a href="#day">時給・日給の早見表</a></li>
  <li><a href="#tokutei">%(n)sの特定最低賃金</a></li>
  <li><a href="#kinki">近くの都道府県と比べる</a></li>
  <li><a href="#fukumu">最低賃金に含める賃金・含めない賃金</a></li>
  <li><a href="#kanzan">日給・月給を時給に直すやり方</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">%(s)sの最低賃金でよく聞かれること</a></li>
 </ol>
</nav>
''' % dict(n=n, s=short)
    rows = []
    for hol in (125, 120, 115, 110, 105):
        a = mon(m, hol); b = mon(o, hol)
        rows.append([td('%d日' % hol), td('%.1f' % hrs(hol)), td(c(a)), td(c(b)), td(c(a - b))])
    sec1 = ('<h2 id="list">月給にすると最低いくらか（年間休日ごと）</h2>\n<p>月給の人は、月給を1か月の平均の労働時間で割って最低賃金と比べます。1日8時間で働く会社の年間休日ごとに、最低賃金を満たす月給を出しました。</p>\n'
            '<p class="cap">%s・1日8時間・含めない手当を除いた月給</p>\n' % n
            + table(['年間<br>休日', '1か月の<br>平均時間', '令和8年度<br>（円）', '令和7年度<br>（円）', '差<br>（円）'], rows)
            + '<p class="note" style="margin-top:8px">1か月の平均時間は（365日−年間休日）×8時間÷12で出しています。月給は円未満を切り上げた額です。基本給と毎月決まって払う手当の合計がこの額以上なら、最低賃金を満たしています。</p>\n')
    rows = []
    for h in (4, 5, 6, 7, 7.5, 8):
        d = math.ceil(m * h - 1e-9)
        rows.append([td(('%g' % h) + '時間'), td(c(d)), td(c(d * 20)), td(c(d * 240))])
    sec2 = ('<h2 id="day">時給・日給の早見表</h2>\n<p>パート・アルバイトの1日の時間ごとに、時給%s円で払うときの日給と月の額を出しました。月の額は1か月に20日働く場合です。</p>\n<p class="cap">%s・時給%s円</p>\n' % (c(m), n, c(m))
            + table(['1日の<br>時間', '日給<br>（円）', '月20日<br>（円）', '年間<br>（円）'], rows)
            + '<p class="note" style="margin-top:8px">日給は円未満を切り上げた額です。年間の額は月20日を12か月続けた場合です。</p>\n')
    sec3 = '<h2 id="tokutei">%sの特定最低賃金</h2>\n%s' % (n, cfg['tokutei'])
    rows = []; hit = None
    for i, nn in enumerate(cfg['near']):
        q = D[nn]
        if nn == n: hit = i
        rows.append([td(nn, 'l'), td(c(q['new'])), td(c(q['old'])), td('+%d' % (q['new'] - q['old'])), td('%d月%d日' % (q['mo'], q['da'])), td('%d位' % rank(nn))])
    rows.append([td('全国加重平均', 'l'), td('1,177'), td('1,121'), td('+56'), td('―'), td('―')])
    sec4 = ('<h2 id="kinki">近くの都道府県と比べる</h2>\n<p>%s</p>\n<p class="cap">令和8年度・時間額</p>\n' % cfg['near_lead']
            + table(['都道府県', '令和8<br>年度', '令和7<br>年度', '上がった<br>額', 'いつ<br>から', '全国<br>順位'], rows, hit)
            + '<p class="note" style="margin-top:8px">%s 全国の一覧は<a href="/saitei-chingin/">最低賃金の一覧</a>にまとめています。</p>\n' % cfg['near_note'])
    # 日給・月給の例
    dex = ex_h * 8
    dh = ex_h
    sm = cfg['ex_month']; h120 = sm / hrs(120); h125 = sm / hrs(125)
    def cmpx(hh):
        return ('%s円上回ります' % f1(hh - m)) if hh >= m else ('%s円下回ります' % f1(m - hh))
    t125 = ('年間休日125日なら時給%s円で、%s。' % (f1(h125), '満たしています' if h125 >= m else '最低賃金を%s円下回ります' % f1(m - h125)))
    sec5 = ('<h2 id="kanzan">日給・月給を時給に直すやり方</h2>\n<h3>日給</h3>\n<p>日給を1日の決まった労働時間で割ります。日給%s円で1日8時間なら時給%s円で、%sの最低賃金を%d円下回ります。</p>\n'
            '<h3>月給</h3>\n<p>月給を1か月の平均の労働時間で割ります。1か月の平均の労働時間は、1年間の決まった労働時間を12で割って出します。年間休日120日・1日8時間なら、1か月の平均は163.3時間です。</p>\n'
            '<h3>月給%sは大丈夫か</h3>\n<p>年間休日120日・1日8時間なら、月給%sは時給%s円です。%sの最低賃金%s円を%s。%s</p>\n') % (
        c(dex), c(dh), n, m - dh, man(sm), man(sm), f1(h120), n, c(m), cmpx(h120), t125)
    sec6 = rel(slug, cfg['rel'])
    qa = ('<h2 id="qa">%sの最低賃金でよく聞かれること</h2>\n' % short
          + '<h3>%sの最低賃金はいつから%s円ですか？</h3>\n<p>%sからです。その前日までに働いた分は、前の年度の%s円で判定します。</p>\n' % (short, c(m), ds(p), c(o))
          + '<h3>%sで月給はいくら以上ならいいですか？</h3>\n<p>年間休日120日・1日8時間なら、含めない手当を除いて月%s以上です。年間休日105日なら月%s以上です。</p>\n' % (short, man(m120), man(m105))
          + cfg['qa']
          + '<h3>試用期間なら最低賃金より低くてもいいですか？</h3>\n<p>%s長の許可を受けていなければ下げられません。許可を受けずに下げた分は、最低賃金との差額を払うことになります。</p>\n' % cfg['kyoku']
          + '<h3>最低賃金を下回っていたらどうなりますか？</h3>\n<p>最低賃金に届かない部分の決まりは無効になり、最低賃金と同じ額で決めたものとみなされます。差額を払う必要があり、%sの最低賃金を払わなかったときは50万円以下の罰金の決まりがあります。</p>\n' % n)
    src = '<div class="src">出典・参考（2026年11月確認）\n <ul>\n%s%s </ul>\n</div>\n' % (cfg['src'], SRC_COMMON)
    body = calc + '\n' + share(slug) + '\n' + intro + '\n' + toc + '\n' + sec1 + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + FUKUMU + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
    js = JS_PREF % dict(base=m, old=o, pn=n, date=ds(p), eff='2026-%02d-%02dT00:00:00+09:00' % (p['mo'], p['da']), ind=json.dumps(IND, ensure_ascii=False), ex_h=ex_h, ex_d=dex, ex_m=sm)
    html_ = page(slug, title, desc, upd, body, js, cta)
    os.makedirs(os.path.join(SITE, slug), exist_ok=True)
    open(os.path.join(SITE, slug, 'index.html'), 'w', encoding='utf-8').write(html_)
    return slug, title

REL_COMMON = [
    ('saitei-chingin', '最低賃金の一覧', '47都道府県の最低賃金を、高い順に並べて比べられます。'),
    ('yatou-hiyou', '人を雇う費用の計算', '人を1人雇うと、給料のほかに会社の負担がかかります。'),
    ('shakaihoken', '社会保険料の早見表', '給料から引かれる社会保険料は、標準報酬月額で決まります。'),
    ('koyohoken', '雇用保険料の早見表', '雇用保険料は、業種ごとに率が決まっています。'),
    ('hoteifukurihi', '法定福利費の計算', '会社が払う社会保険料は、法定福利費として経費になります。'),
    ('part-fuyou', 'パートの扶養の計算', 'パートの月収で、扶養に入れるかの目安が分かります。'),
    ('gakusei-kabe', '学生バイトの年収の壁', '学生のアルバイトは、年収で親の扶養と本人の税金が変わります。'),
    ('tedori', '年収の手取りの早見表', '年収から税金と社会保険料を引いた手取りを、年収ごとに見られます。'),
    ('tsukin-teate', '通勤手当の非課税限度額', '通勤手当は最低賃金に含めず、所得税は限度額まで非課税です。'),
]

def rel_for(own_extra):
    return own_extra + REL_COMMON

PREFS = [
 dict(name='東京都', slug='tokyo', short='東京', word='東京の最低賃金', kyoku='東京労働局',
      mid='東京都の特定最低賃金は東京都最低賃金より低いので、1,280円と比べます',
      intro='東京都の特定最低賃金はどれも東京都最低賃金より低いので、業種にかかわらず1,280円以上が最低ラインです。',
      tokutei='''<p>東京都には、鉄鋼業や機械器具の製造業などに4つの特定最低賃金があります。額は829円〜871円で、平成22年〜26年に決まったまま改定されていません。東京都最低賃金1,280円より低いので、実際は1,280円以上を払えば足ります。</p>
<p class="cap">東京都の特定最低賃金の業種（令和7年度の一覧）</p>
<ul>
 <li>鉄鋼業</li>
 <li>はん用機械器具・生産用機械器具製造業</li>
 <li>業務用機械器具・電気機械器具・情報通信機械器具製造業など</li>
 <li>自動車・同附属品製造業・船舶製造・修理業など</li>
</ul>

''' + \
          '<p class="note" style="margin-top:8px">令和8年度は、東京地方最低賃金審議会に特定最低賃金の改正と自動車小売業（新車）の新設の申出が出ています。決まって東京都最低賃金を上回る額になったときは、この欄を直します。</p>\n',
      near=['東京都', '神奈川県', '埼玉県', '千葉県', '山梨県', '大阪府', '愛知県'],
      near_lead='東京都と近くの県・大阪府・愛知県の令和8年度の最低賃金です。働く場所が都県をまたぐときは、事業場がある都道府県の額で判定します。',
      near_note='東京都は全国で一番高い額で、神奈川県との差は1円です。埼玉県・千葉県とは84円〜85円の差があります。',
      ex_month=210000,
      qa='<h3>本社が地方で東京の店で働く人はどちらの額ですか？</h3>\n<p>働いている東京の店の額で、時給1,280円です。派遣社員は、派遣先の事業場がある都道府県の額で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/tokyo-roudoukyoku/news_topics/houdou/20260930chinginka_00001.html">東京労働局「東京都最低賃金が10月1日から1,280円に」</a>（令和8年9月30日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/tokyo-roudoukyoku/content/contents/002025134.pdf">東京労働局「東京都の特定最低賃金 改正一覧表（平成21年度〜令和7年度）」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/tokyo-roudoukyoku/content/contents/002822599.pdf">東京地方最低賃金審議会「令和8年度 特定（産業別）最低賃金 改正等申出状況」</a></li>\n',
      rel=[('saitei-chingin-kanagawa', '神奈川県の最低賃金', '神奈川県は1,279円で、東京都との差は1円です。'),
           ('saitei-chingin-saitama', '埼玉県の最低賃金', '埼玉県は1,196円で、東京都との差は84円です。'),
           ('saitei-chingin-chiba', '千葉県の最低賃金', '千葉県は1,195円で、東京都との差は85円です。')]),
 dict(name='神奈川県', slug='kanagawa', short='神奈川', word='神奈川県の最低賃金', kyoku='神奈川労働局',
      mid='神奈川県の特定最低賃金は令和7年度に改定されず、神奈川県最低賃金の額になっています',
      intro='神奈川県の特定最低賃金7業種は令和7年度に改定されず、神奈川県最低賃金の額で判定します。',
      tokutei='''<p>神奈川県には、製造業と自動車小売業に7つの特定最低賃金があります。神奈川労働局の一覧では、7業種とも令和7年度は改定されなかったため神奈川県最低賃金の額になっています。いまは業種にかかわらず1,279円以上が最低ラインです。</p>
<p class="cap">神奈川県の特定最低賃金</p>
''' + table(['業種', '令和7年度', 'いまの<br>最低ライン'], [
          [td(x, 'l'), td('改定なし', 'c'), td('1,279円', 'c')] for x in ['塗料製造業', '鉄鋼業', '電線・ケーブル製造業', '一般機械器具製造業', '電気機械器具製造業', '輸送用機械器具製造業', '自動車小売業']]) +
          '<p class="note" style="margin-top:8px">神奈川労働局「特定（産業別）最低賃金」（令和7年11月26日更新）によります。令和8年度に神奈川県最低賃金を上回る額で改正されたときは、この表を直します。</p>\n',
      near=['東京都', '神奈川県', '埼玉県', '千葉県', '山梨県', '静岡県'],
      near_lead='神奈川県と近くの都県の令和8年度の最低賃金です。県境をまたいで通う人も、働く事業場がある都県の額で判定します。',
      near_note='神奈川県は東京都に次いで全国で2番目に高い額です。隣の静岡県とは125円・山梨県とは166円の差があります。',
      ex_month=210000,
      qa='<h3>東京の会社に雇われて神奈川の営業所で働く人はどちらの額ですか？</h3>\n<p>働いている神奈川の営業所の額で、時給1,279円です。東京都の1,280円とは1円違うので、本社の額で管理している会社は気を付けてください。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/kanagawa-roudoukyoku/home/houdou/20260827_00001.html">神奈川労働局「令和8年度「神奈川県最低賃金」を改正決定します」</a>（令和8年8月27日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kanagawa-roudoukyoku/hourei_seido_tetsuzuki/saiteichingin_chinginseido/_119684.html">神奈川労働局「神奈川県最低賃金の推移」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/kanagawa-roudoukyoku/hourei_seido_tetsuzuki/saiteichingin_chinginseido/_119730.html">神奈川労働局「特定（産業別）最低賃金」</a></li>\n',
      rel=[('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で全国で一番高い額です。')]),
 dict(name='北海道', slug='hokkaido', short='北海道', word='北海道の最低賃金', kyoku='北海道労働局',
      ind=[['鉄鋼業（鉄素形材製造業・その他の鉄鋼業を除く）', 1165, '2025年12月1日']],
      mid='鉄鋼業は北海道の特定最低賃金1,165円と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼業だけは、これより高い北海道の特定最低賃金1,165円がかかります。',
      tokutei='''<p>北海道には4つの特定最低賃金があります。鉄鋼業の1,165円だけが北海道の最低賃金1,131円より高く、ほかの3業種は2026年10月1日から北海道の最低賃金と同じ1,131円で判定します。</p>
<p class="cap">北海道の特定最低賃金・時間額</p>
''' + table(['業種', '時間額', 'いつから', '前の額'], [
          [td('鉄鋼業（鉄素形材製造業・その他の鉄鋼業を除く）', 'l'), td('1,165円'), td('2025年<br>12月1日', 'c'), td('1,100円')],
          [td('処理牛乳・乳飲料・乳製品・糖類製造業', 'l'), td('1,131円'), td('2026年<br>10月1日', 'c'), td('1,113円')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,131円'), td('2026年<br>10月1日', 'c'), td('1,116円')],
          [td('船舶製造・修理業・船体ブロック製造業', 'l'), td('1,131円'), td('2026年<br>10月1日', 'c'), td('1,105円')]]) +
          '<p class="note" style="margin-top:8px">1,131円の3業種は、北海道の最低賃金が特定最低賃金の額を上回ったため北海道の最低賃金で判定する業種です。業種に入るかどうかは、その事業場の主な事業で決まります。</p>\n',
      near=['北海道', '青森県', '岩手県', '秋田県', '宮城県', '東京都'],
      near_lead='北海道と東北の県・東京都の令和8年度の最低賃金です。北海道は東北6県のどこよりも高い額です。',
      near_note='北海道と東北6県で一番高い宮城県の差は33円です。岩手県は12月1日からの引上げです。',
      ex_month=180000,
      qa='<h3>札幌と地方で最低賃金は違いますか？</h3>\n<p>違いません。北海道の最低賃金は道内のどこでも時給1,131円です。鉄鋼業の事業場だけは特定最低賃金の1,165円です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/hokkaido-roudoukyoku/content/contents/002798678.pdf">北海道労働局「北海道最低賃金の改正決定」</a>（令和8年9月1日）</li>\n  <li><a href="https://www.city.sapporo.jp/keizai/koyo/rodo/chingin.html">札幌市「北海道の最低賃金」</a>（特定最低賃金・2026年9月7日更新）</li>\n',
      rel=[('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、北海道との差は149円です。')]),
 dict(name='愛知県', slug='aichi', short='愛知', word='愛知県の最低賃金', kyoku='愛知労働局',
      mid='愛知県の特定最低賃金（鉄鋼業・輸送用機械器具製造業）は、いまは愛知県最低賃金より低い額です',
      intro='鉄鋼業と輸送用機械器具製造業の特定最低賃金は、12月以降に愛知県最低賃金を上回る額への改正が審議されています。',
      tokutei='''<p>愛知県の特定最低賃金は、鉄鋼業と輸送用機械器具製造業の2つです。いまの額はどちらも愛知県最低賃金1,195円より低いので、1,195円以上が最低ラインです。令和8年度の改正は、愛知地方最低賃金審議会の専門部会で次の案が出ています。</p>
<p class="cap">愛知県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '改正の案', 'いつから<br>（案）'], [
          [td('製鉄業・製鋼・製鋼圧延業・鋼材製造業', 'l'), td('1,175円'), td('1,230円'), td('2027年<br>1月1日', 'c')],
          [td('輸送用機械器具製造業', 'l'), td('1,146円'), td('1,208円'), td('2026年<br>12月16日', 'c')]]) +
          '<p class="note" style="margin-top:8px">改正の案は専門部会の報告の案（令和8年10月）で、まだ決まった額ではありません。決まったときはこの表と計算を直します。自動車や部品の工場で働く人は、案のとおりに決まると12月16日から1,208円以上が最低ラインになります。</p>\n',
      near=['愛知県', '岐阜県', '三重県', '静岡県', '長野県', '東京都', '大阪府'],
      near_lead='愛知県と東海・長野の県・東京都・大阪府の令和8年度の最低賃金です。岐阜や三重から通う人も、愛知県内の事業場なら愛知県の額で判定します。',
      near_note='愛知県は千葉県と同じ額で全国で5番目に高い額です。岐阜県とは74円・三重県とは52円の差があります。',
      ex_month=195000,
      qa='<h3>自動車の部品工場は特定最低賃金ですか？</h3>\n<p>自動車や部品を作る事業場は、輸送用機械器具製造業の特定最低賃金の対象です。いまの額1,146円は愛知県最低賃金より低いので、1,195円以上を払えば足ります。改正の案どおりに決まると12月16日から1,208円になります。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/002762658.pdf">愛知労働局「愛知県最低賃金の改正について答申」</a>（令和8年8月5日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/002843463.pdf">愛知労働局「最低賃金の履行確保を主眼とする監督指導の結果」</a>（令和8年10月5日・愛知県最低賃金1,195円の発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/002849058.pdf">愛知地方最低賃金審議会「鉄鋼業最低賃金専門部会 資料」</a>（令和8年10月8日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/002849062.pdf">愛知地方最低賃金審議会「輸送用機械器具製造業最低賃金専門部会 報告（案）」</a>（令和8年10月7日）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、愛知県より36円高い額です。')]),
]

# ---- 2026/11/18 に足した5府県(埼玉・福岡・千葉・兵庫・京都) ----
# 特定最低賃金:ind の要素は [業種, 新しい額, 新しい額の発効日, ISO日付, いまの額, いまの額の発効日]。発効日の前はいまの額で判定する。
PREFS += [
 dict(name='埼玉県', slug='saitama', short='埼玉', word='埼玉県の最低賃金', kyoku='埼玉労働局', upd='2026年11月18日',
      ind=[['非鉄金属製造業', 1216, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1161, '2025年12月1日'],
           ['光学機械器具・レンズ・時計・同部分品製造業', 1232, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1177, '2025年12月1日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1223, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1168, '2025年12月1日'],
           ['輸送用機械器具製造業', 1224, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1165, '2025年12月1日'],
           ['自動車小売業', 1207, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1152, '2025年12月1日']],
      mid='製造業など5業種は12月1日から特定最低賃金に変わります。業種を選ぶと切り替わります',
      intro='製造業と自動車小売業の5業種は、12月1日から特定最低賃金の1,207円〜1,232円がかかります。',
      tokutei='''<p>埼玉県には6つの特定最低賃金があります。5業種は令和8年12月1日から改正され、どれも埼玉県最低賃金1,196円より高くなります。11月30日までは改正前の額が埼玉県最低賃金より低いので、1,196円以上が最低ラインです。</p>
<p class="cap">埼玉県の特定最低賃金・時間額</p>
''' + table(['業種', '12月1日<br>から', 'いまの額', '上がった<br>額'], [
          [td('非鉄金属製造業', 'l'), td('1,216円'), td('1,161円'), td('+55')],
          [td('光学機械器具・レンズ・時計・同部分品製造業', 'l'), td('1,232円'), td('1,177円'), td('+55')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,223円'), td('1,168円'), td('+55')],
          [td('輸送用機械器具製造業', 'l'), td('1,224円'), td('1,165円'), td('+59')],
          [td('自動車小売業', 'l'), td('1,207円'), td('1,152円'), td('+55')],
          [td('各種商品小売業', 'l'), td('849円'), td('849円'), td('―')]]) +
          '<p class="note" style="margin-top:8px">各種商品小売業の849円は平成28年12月1日から改正されていません。埼玉県最低賃金より低いので、この業種は1,196円で判定します。業種に入るかどうかは、その事業場の主な事業で決まります。</p>\n',
      near=['埼玉県', '東京都', '千葉県', '神奈川県', '群馬県', '栃木県', '茨城県'],
      near_lead='埼玉県と近くの都県の令和8年度の最低賃金です。埼玉から東京に通う人は、働く東京の事業場の額で判定します。',
      near_note='埼玉県は全国で4番目に高い額で、千葉県より1円高い額です。東京都とは84円の差があります。',
      ex_month=200000,
      qa='<h3>埼玉に住んで東京で働く人はどちらの額ですか？</h3>\n<p>働いている東京の事業場の額で、時給1,280円です。住んでいる県ではなく、働く事業場がある都道府県の額で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/saitama-roudoukyoku/hourei_seido_tetsuzuki/chingin_kanairoudou.html">埼玉労働局「最低賃金・家内労働」</a>（埼玉県最低賃金と特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/saitama-roudoukyoku/content/contents/002784855.pdf">埼玉労働局「埼玉県最低賃金の改正決定」</a>（令和8年8月21日）</li>\n  <li><a href="https://www.pref.saitama.lg.jp/a0809/rodo/912-2009-1204-137.html">埼玉県「埼玉県の最低賃金・最低工賃」</a>（令和7年度の特定最低賃金の額）</li>\n',
      rel=[('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、埼玉県との差は84円です。'),
           ('saitei-chingin-chiba', '千葉県の最低賃金', '千葉県は1,195円で、埼玉県より1円低い額です。')]),
 dict(name='福岡県', slug='fukuoka', short='福岡', word='福岡県の最低賃金', kyoku='福岡労働局', upd='2026年11月18日',
      ind=[['製鉄業・製鋼・製鋼圧延業・鋼材製造業', 1238, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1176, '2025年12月10日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1195, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1137, '2025年12月10日'],
           ['輸送用機械器具製造業', 1205, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1147, '2025年12月10日'],
           ['自動車（新車）小売業', 1185, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1131, '2025年12月10日']],
      mid='鉄鋼・電子部品・輸送用機械・新車小売の4業種は特定最低賃金と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼業など4業種は、いまの特定最低賃金も福岡県最低賃金より高い額です。12月10日からさらに上がります。',
      tokutei='''<p>福岡県には5つの特定最低賃金があります。鉄鋼業・電子部品など・輸送用機械器具・新車の小売業の4業種は、いまの額も福岡県最低賃金1,114円より高い額です。令和8年12月10日から改正されます。百貨店・総合スーパーは令和8年度の改正がなく、福岡県最低賃金に抜かれました。</p>
<p class="cap">福岡県の特定最低賃金・時間額</p>
''' + table(['業種', '12月10日<br>から', 'いまの額', '上がった<br>額'], [
          [td('製鉄業・製鋼・製鋼圧延業・鋼材製造業', 'l'), td('1,238円'), td('1,176円'), td('+62')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,195円'), td('1,137円'), td('+58')],
          [td('輸送用機械器具製造業', 'l'), td('1,205円'), td('1,147円'), td('+58')],
          [td('自動車（新車）小売業', 'l'), td('1,185円'), td('1,131円'), td('+54')],
          [td('百貨店・総合スーパーマーケット', 'l'), td('改正なし'), td('1,065円'), td('―')]]) +
          '<p class="note" style="margin-top:8px">百貨店・総合スーパーの1,065円（令和8年2月1日から）は福岡県最低賃金より低いので、10月4日からは1,114円で判定します。いまの額は12月9日まで使います。</p>\n',
      near=['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '山口県', '広島県'],
      near_lead='福岡県と九州・山口・広島の令和8年度の最低賃金です。九州で一番高いのは福岡県です。',
      near_note='福岡県は九州7県で一番高い額です。佐賀県とは19円・熊本県とは22円の差があり、熊本県は12月1日からの引上げです。',
      ex_month=185000,
      qa='<h3>福岡市と北九州市で最低賃金は違いますか？</h3>\n<p>違いません。福岡県の最低賃金は県内のどこでも時給1,114円です。鉄鋼業など4業種の事業場だけは、特定最低賃金がかかります。</p>\n'
         + '<h3>福岡県はなぜ10月4日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、福岡県は10月4日でした。10月3日までに働いた分は前の年度の1,057円で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/fukuoka-roudoukyoku/jirei_toukei/chingin_kanairoudou/toukei/saitei_chingin/chingin09_22.html">福岡労働局「福岡県の最低賃金」</a>（地域別最低賃金と特定最低賃金）</li>\n  <li><a href="https://www.pref.fukuoka.lg.jp/contents/2026saiteichngin.html">福岡県「福岡県最低賃金が改正されます」</a>（令和8年10月8日更新）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、福岡県より117円高い額です。'),
           ('saitei-chingin-kumamoto', '熊本県の最低賃金', '熊本県は12月1日から1,092円で、福岡県より22円低い額です。')]),
 dict(name='千葉県', slug='chiba', short='千葉', word='千葉県の最低賃金', kyoku='千葉労働局', upd='2026年11月18日',
      ind=[['鉄鋼業', 1210, '2025年12月25日']],
      mid='鉄鋼業は千葉県の特定最低賃金1,210円と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼業だけは、いまも千葉県最低賃金より高い特定最低賃金1,210円がかかります。',
      tokutei='''<p>千葉県には7つの特定最低賃金があります。いま千葉県最低賃金1,195円より高いのは鉄鋼業の1,210円だけです。鉄鋼業と電子部品などの2業種は、千葉地方最低賃金審議会が12月25日からの改正を答申しています。</p>
<p class="cap">千葉県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '答申の額', 'いつから<br>（予定）'], [
          [td('鉄鋼業', 'l'), td('1,210円'), td('1,265円'), td('2026年<br>12月25日', 'c')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,169円'), td('1,224円'), td('2026年<br>12月25日', 'c')],
          [td('調味料製造業（味そを除く）', 'l'), td('889円'), td('―'), td('―', 'c')],
          [td('はん用機械器具・生産用機械器具製造業', 'l'), td('922円'), td('―'), td('―', 'c')],
          [td('計量器・測定器・分析機器・理化学機械器具・医療用機械器具・光学機械器具・時計・眼鏡製造業', 'l'), td('887円'), td('―'), td('―', 'c')],
          [td('各種商品小売業', 'l'), td('848円'), td('―'), td('―', 'c')],
          [td('自動車（新車）小売業', 'l'), td('922円'), td('―'), td('―', 'c')]]) +
          '<p class="note" style="margin-top:8px">答申の額は千葉労働局長の決定と公示の前なので、計算には入れていません。決まったときはこの表と計算を直します。いまの額が1,195円より低い6業種は、千葉県最低賃金の1,195円で判定します。</p>\n',
      near=['千葉県', '東京都', '神奈川県', '埼玉県', '茨城県'],
      near_lead='千葉県と近くの都県の令和8年度の最低賃金です。千葉から東京に通う人は、働く東京の事業場の額で判定します。',
      near_note='千葉県は愛知県と同じ額で全国で5番目に高い額です。埼玉県とは1円・茨城県とは59円の差があります。',
      ex_month=200000,
      qa='<h3>千葉県の鉄鋼業の最低賃金はいくらですか？</h3>\n<p>いまは特定最低賃金の時給1,210円です。12月25日から1,265円にする答申が出ていて、決まるとその日から1,265円になります。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/content/contents/002801978.pdf">千葉労働局「千葉県最低賃金の改正決定」</a>（令和8年9月1日公示）</li>\n  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/content/contents/002786897.pdf">千葉労働局「千葉県の最低賃金の一覧」</a>（特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/content/contents/002862096.pdf">千葉地方最低賃金審議会「鉄鋼業最低賃金の改正決定に関する答申」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/hourei_seido_tetsuzuki/r08chibasaichin_boucyou_04_00002.html">千葉労働局「電子部品等の特定最低賃金の答申と異議の申出」</a>（令和8年10月7日）</li>\n',
      rel=[('saitei-chingin-saitama', '埼玉県の最低賃金', '埼玉県は1,196円で、千葉県より1円高い額です。'),
           ('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、千葉県との差は85円です。'),
           ('saitei-chingin-ibaraki', '茨城県の最低賃金', '茨城県は1,136円で、千葉県より59円低い額です。')]),
 dict(name='兵庫県', slug='hyogo', short='兵庫', word='兵庫県の最低賃金', kyoku='兵庫労働局', upd='2026年11月18日',
      ind=[['塗料製造業', 1199, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1158, '2025年12月1日'],
           ['鉄鋼業', 1231, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1180, '2025年12月1日'],
           ['はん用機械器具・生産用機械器具・業務用機械器具製造業', 1206, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1150, '2025年12月1日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1173, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1117, '2025年12月1日'],
           ['輸送用機械器具製造業', 1243, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1188, '2025年12月1日'],
           ['計量器・測定器・分析機器・試験機・測量機械器具製造業', 1173, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1117, '2025年12月1日']],
      mid='製造業の6業種は12月1日から特定最低賃金に変わります。業種を選ぶと切り替わります',
      intro='製造業の6業種は12月1日から特定最低賃金の1,173円〜1,243円がかかります。',
      tokutei='''<p>兵庫県の特定最低賃金のうち、製造業の6業種が令和8年12月1日から改正されます。11月30日までは、鉄鋼業の1,180円と輸送用機械器具製造業の1,188円が兵庫県最低賃金1,172円より高い額です。</p>
<p class="cap">兵庫県の特定最低賃金・時間額</p>
''' + table(['業種', '12月1日<br>から', 'いまの額', '上がった<br>額'], [
          [td('塗料製造業', 'l'), td('1,199円'), td('1,158円'), td('+41')],
          [td('鉄鋼業', 'l'), td('1,231円'), td('1,180円'), td('+51')],
          [td('はん用機械器具・生産用機械器具・業務用機械器具製造業', 'l'), td('1,206円'), td('1,150円'), td('+56')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,173円'), td('1,117円'), td('+56')],
          [td('輸送用機械器具製造業', 'l'), td('1,243円'), td('1,188円'), td('+55')],
          [td('計量器・測定器・分析機器・試験機・測量機械器具製造業', 'l'), td('1,173円'), td('1,117円'), td('+56')]]) +
          '<p class="note" style="margin-top:8px">繊維工業・各種商品小売業・自動車小売業の特定最低賃金は兵庫県最低賃金を上回らないので、10月1日から1,172円で判定します。電子部品などと計量器などの1,173円は、兵庫県最低賃金より1円高い額です。</p>\n',
      near=['兵庫県', '大阪府', '京都府', '岡山県', '鳥取県', '徳島県', '和歌山県'],
      near_lead='兵庫県と近くの府県の令和8年度の最低賃金です。兵庫から大阪に通う人は、働く大阪の事業場の額で判定します。',
      near_note='兵庫県は全国で8番目に高い額です。大阪府とは59円・京都府とは8円の差があり、岡山県より68円高い額です。',
      ex_month=195000,
      qa='<h3>神戸と姫路で最低賃金は違いますか？</h3>\n<p>違いません。兵庫県の最低賃金は県内のどこでも時給1,172円です。製造業の6業種の事業場だけは、12月1日から特定最低賃金がかかります。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/hyogo-roudoukyoku/content/contents/002875983.pdf">兵庫労働局「兵庫県の最低賃金」</a>（地域別最低賃金と特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hyogo-roudoukyoku/home/sintyaku_itiran/news_topics/houdou/2026.html">兵庫労働局「報道発表 2026年」</a>（9月1日 兵庫県最低賃金 時間額1,172円に改正決定）</li>\n  <li><a href="https://www.nishi.or.jp/smph/kurashi/rodo/rodogyosei/saiteichingin.html">西宮市「最低賃金」</a>（特定最低賃金の額・2026年11月9日更新）</li>\n  <li><a href="https://web.pref.hyogo.lg.jp/sr05/saiteitingin.html">兵庫県「最低賃金」</a>（令和7年度の特定最低賃金の額）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、兵庫県より59円高い額です。'),
           ('saitei-chingin-kyoto', '京都府の最低賃金', '京都府は11月16日から1,180円で、兵庫県より8円高い額です。')]),
 dict(name='京都府', slug='kyoto', short='京都', word='京都府の最低賃金', kyoku='京都労働局', upd='2026年11月18日',
      mid='京都府の特定最低賃金は、11月16日からどれも京都府最低賃金より低い額です',
      intro='京都府の特定最低賃金はどれも1,180円より低くなったので、業種にかかわらず1,180円以上が最低ラインです。',
      tokutei='''<p>京都府には6つの特定最低賃金があります。電気機械器具製造業の1,136円（令和8年1月24日から）が一番高い額ですが、11月16日からは京都府最低賃金1,180円より低くなりました。いまは業種にかかわらず1,180円以上が最低ラインです。</p>
<ul>
 <li>電気機械器具製造業：令和8年度は、これから改正の審議を行う予定です</li>
 <li>輸送用機械器具製造業・自動車（新車）小売業：改正の申出がありましたが、改正は決まりませんでした</li>
 <li>金属製品製造業・各種商品小売業・はん用機械器具など製造業：改正の申出がありませんでした</li>
</ul>
''' + '<p class="note" style="margin-top:8px">京都労働局の発表（令和8年9月18日）によります。電気機械器具製造業の改正が決まって1,180円を上回ったときは、この欄を直します。</p>\n',
      near=['京都府', '大阪府', '兵庫県', '滋賀県', '奈良県', '福井県', '三重県'],
      near_lead='京都府と近くの府県の令和8年度の最低賃金です。京都府は近畿で大阪府に次いで高い額です。',
      near_note='京都府は全国で7番目に高い額です。大阪府とは51円の差があり、兵庫県より8円・滋賀県より44円高い額です。',
      ex_month=195000,
      qa='<h3>京都府はなぜ11月16日からですか？</h3>\n<p>京都地方最低賃金審議会が、使用者側の意見を踏まえて発効日を11月16日に指定したためです。11月15日までに働いた分は、前の年度の1,122円で判定します。</p>\n'
         + '<h3>11月の給料はどちらの額で計算しますか？</h3>\n<p>11月15日までに働いた分は1,122円・11月16日からの分は1,180円で判定します。月の途中で締める会社は、日ごとに分けて確かめてください。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002816577.pdf">京都労働局「京都府最低賃金の改正決定」</a>（令和8年9月18日公示）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002814861.pdf">京都労働局「令和8年度 特定最低賃金の改正等について」</a>（令和8年9月18日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002505545.pdf">京都労働局「京都府の特定最低賃金」</a>（電気機械器具製造業 令和8年1月24日から）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002840599.pdf">京都地方最低賃金審議会 議事録</a>（発効日の審議）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、京都府より51円高い額です。'),
           ('saitei-chingin-hyogo', '兵庫県の最低賃金', '兵庫県は1,172円で、京都府より8円低い額です。')]),
 dict(name='沖縄県', slug='okinawa', short='沖縄', word='沖縄県の最低賃金', kyoku='沖縄労働局', upd='2026年11月19日',
      mid='沖縄県の最低賃金は12月2日から変わります。12月1日までは前の年度の1,023円です',
      intro='12月1日までに働いた分は前の年度の1,023円で判定します。沖縄県の特定最低賃金はどれも県の最低賃金より低い額です。',
      tokutei='''<p>沖縄県には4つの特定最低賃金があります。どれも沖縄県最低賃金より低いので、業種にかかわらず12月2日からは1,086円以上が最低ラインです。</p>
<p class="cap">沖縄県の特定最低賃金・時間額</p>
''' + table(['業種', '特定最低<br>賃金', '決まった日'], [
          [td('糖類製造業', 'l'), td('769円'), td('平成30年11月25日')],
          [td('新聞業', 'l'), td('879円'), td('令和4年11月17日')],
          [td('各種商品小売業', 'l'), td('770円'), td('平成30年11月23日')],
          [td('自動車（新車）小売業', 'l'), td('770円'), td('平成30年11月18日')]]) +
          '<p class="note" style="margin-top:8px">新聞業・糖類製造業・自動車（新車）小売業は令和8年度に改正の申出がありましたが、審議会は改正が必要との結論に至りませんでした（令和8年8月14日の審議会）。</p>\n',
      near=['沖縄県', '鹿児島県', '宮崎県', '熊本県', '長崎県', '福岡県', '東京都'],
      near_lead='沖縄県と九州の県の令和8年度の最低賃金です。沖縄県は発効日が12月2日で、全国で一番遅い日です。',
      near_note='沖縄県は高知県と同じ額で、宮崎県より1円高く鹿児島県より4円低い額です。九州で一番高い福岡県とは28円の差があります。',
      ex_month=180000,
      qa='<h3>沖縄県はなぜ12月2日からですか？</h3>\n<p>発効日は審議会で労使の意見が分かれ、採決で決まりました。使用者側は1,080円・令和9年1月2日からの案を出しましたが、1,086円・12月2日からの案が賛成8名・反対6名で答申されました（令和8年9月3日の審議会）。</p>\n'
         + '<h3>11月の給料はどちらの額で判定しますか？</h3>\n<p>11月に働いた分は、前の年度の1,023円で判定します。12月2日からの分は1,086円です。12月の途中で締める会社は、日ごとに分けて確かめてください。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002840324.pdf">沖縄労働局「令和8年度沖縄県最低賃金は時間額1,086円」</a>（令和8年10月5日・12月2日から発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002866931.pdf">沖縄地方最低賃金審議会 第4回 議事要旨</a>（令和8年9月3日・発効日の採決）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002776112.pdf">沖縄地方最低賃金審議会「令和8年度 審議計画」</a>（特定最低賃金の推移）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002816953.pdf">沖縄地方最低賃金審議会 第3回 議事要旨</a>（令和8年8月14日・特定最低賃金の必要性）</li>\n  <li><a href="https://www.pref.okinawa.jp/shigoto/koyorodo/1012030/1012038/1012041/1012040.html">沖縄県「沖縄県最低賃金」</a>（2026年10月23日更新）</li>\n',
      rel=[('saitei-chingin-kagoshima', '鹿児島県の最低賃金', '鹿児島県は1,090円で、沖縄県より4円高い額です。'),
           ('saitei-chingin-fukuoka', '福岡県の最低賃金', '福岡県は1,114円で、九州で一番高い額です。')]),
 dict(name='熊本県', slug='kumamoto', short='熊本', word='熊本県の最低賃金', kyoku='熊本労働局', upd='2026年11月19日',
      ind=[['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1063, '2026年1月1日'],
           ['自動車・同附属品製造業・船舶製造・修理業・舶用機関製造業', 1074, '2026年1月1日']],
      mid='熊本県の最低賃金は12月1日から変わります。11月30日までは前の年度の1,034円です',
      intro='11月30日までに働いた分は前の年度の1,034円で判定します。電子部品などと自動車などの製造業は、11月30日まで特定最低賃金の方が高い額です。',
      tokutei='''<p>熊本県には3つの特定最低賃金があります。電子部品などの1,063円と自動車などの1,074円は、11月30日までは熊本県最低賃金1,034円より高い額です。12月1日からは熊本県最低賃金1,092円の方が高くなります。</p>
<p class="cap">熊本県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '発効日'], [
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,063円'), td('令和8年1月1日')],
          [td('自動車・同附属品製造業・船舶製造・修理業・舶用機関製造業', 'l'), td('1,074円'), td('令和8年1月1日')],
          [td('百貨店・総合スーパー', 'l'), td('855円'), td('―')]]) +
          '<p class="note" style="margin-top:8px">令和8年度の特定最低賃金の改正は、熊本地方最低賃金審議会が10月30日に答申しています。改正後の額と発効日は、官報で公示されたあとにこの表へ反映します。百貨店・総合スーパーの855円は県の最低賃金より低いので、県の最低賃金で判定します。</p>\n',
      near=['熊本県', '福岡県', '佐賀県', '長崎県', '大分県', '宮崎県', '鹿児島県'],
      near_lead='熊本県と九州の県の令和8年度の最低賃金です。熊本県は12月1日からの引上げで、九州では沖縄県に次いで遅い発効日です。',
      near_note='熊本県は島根県と同じ額です。福岡県とは22円の差があり、鹿児島県より2円・宮崎県より7円高い額です。',
      ex_month=180000,
      qa='<h3>熊本県の新しい最低賃金はいつからですか？</h3>\n<p>令和8年12月1日からです。前の年度の1,034円は令和8年1月1日から使われていたので、11か月で58円上がります。</p>\n'
         + '<h3>半導体の工場で働く人の最低賃金はいくらですか？</h3>\n<p>電子部品・デバイスの製造業なら、11月30日までは特定最低賃金の1,063円です。12月1日からは熊本県最低賃金の1,092円の方が高いので、1,092円以上が必要です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/kumamoto-roudoukyoku/content/contents/002801916.pdf">熊本労働局「令和8年度熊本県最低賃金の改正答申について」</a>（令和8年9月1日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kumamoto-roudoukyoku/content/contents/002838706.pdf">熊本労働局「第13回熊本地方最低賃金審議会の審議結果について」</a>（令和8年9月28日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kumamoto-roudoukyoku/content/contents/002477426.pdf">熊本労働局「熊本県特定（産業別）最低賃金の改正について」</a>（令和7年12月1日官報公示・令和8年1月1日発効）</li>\n  <li><a href="https://www.pref.kumamoto.jp/soshiki/62/186613.html">熊本県「最低賃金」</a>（2026年11月9日更新）</li>\n',
      rel=[('saitei-chingin-fukuoka', '福岡県の最低賃金', '福岡県は1,114円で、熊本県より22円高い額です。'),
           ('saitei-chingin-kagoshima', '鹿児島県の最低賃金', '鹿児島県は1,090円で、熊本県より2円低い額です。')]),
 dict(name='茨城県', slug='ibaraki', short='茨城', word='茨城県の最低賃金', kyoku='茨城労働局', upd='2026年11月19日',
      ind=[['鉄鋼業', 1166, '2026年3月1日']],
      mid='鉄鋼業の事業場は特定最低賃金の1,166円と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼業だけは特定最低賃金の1,166円がかかります。',
      tokutei='''<p>茨城県には4つの特定最低賃金があります。10月18日からは鉄鋼業の1,166円だけが茨城県最低賃金1,136円より高い額です。ほかの3業種は1,136円で判定します。</p>
<p class="cap">茨城県の特定最低賃金・時間額</p>
''' + table(['業種', '特定最低<br>賃金', '発効日'], [
          [td('鉄鋼業', 'l'), td('1,166円'), td('令和8年3月1日')],
          [td('はん用・生産用・業務用機械器具製造業', 'l'), td('1,105円'), td('令和8年3月1日')],
          [td('計量器・医療用機械器具・光学機械器具・電子部品・電気機械器具・情報通信機械器具・時計製造業', 'l'), td('1,115円'), td('令和8年3月19日')],
          [td('各種商品小売業', 'l'), td('―'), td('―')]]) +
          '<p class="note" style="margin-top:8px">機械器具の2業種は特定最低賃金が1,136円より低いので、10月18日からは茨城県最低賃金で判定します。各種商品小売業は令和7年10月12日から茨城県最低賃金で判定しています。令和8年度の特定最低賃金の改正が決まったら、この欄を直します。</p>\n',
      near=['茨城県', '東京都', '千葉県', '埼玉県', '栃木県', '群馬県', '福島県'],
      near_lead='茨城県と近くの都県の令和8年度の最低賃金です。茨城から東京・千葉に通う人は、働く事業場の都県の額で判定します。',
      near_note='茨城県は全国で12番目に高い額です。千葉県とは59円・東京都とは144円の差があり、栃木県より11円・福島県より42円高い額です。',
      ex_month=185000,
      qa='<h3>茨城県はなぜ10月18日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、茨城県は10月18日でした。10月17日までに働いた分は前の年度の1,074円で判定します。</p>\n'
         + '<h3>つくばと水戸で最低賃金は違いますか？</h3>\n<p>違いません。茨城県の最低賃金は県内のどこでも時給1,136円です。鉄鋼業の事業場だけは特定最低賃金の1,166円がかかります。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/ibaraki-roudoukyoku/content/contents/saichin_press080918.pdf">茨城労働局「茨城県最低賃金は令和8年10月18日から時間額1,136円に」</a>（令和8年9月18日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/ibaraki-roudoukyoku/roudoukyoku/gyoumu_naiyou/kijunbu/chingin/chingin01.html">茨城労働局「茨城県の最低賃金」</a>（特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/ibaraki-roudoukyoku/content/contents/chingin_tokutei_R080113press11p.pdf">茨城労働局「令和7年度茨城県特定（産業別）最低賃金の改正答申について」</a>（令和8年1月13日）</li>\n  <li><a href="https://www.pref.ibaraki.jp/shokorodo/rosei/rodo/saitei/tokusai.html">茨城県「茨城県特定（産業別）最低賃金改正」</a>（2026年3月27日更新）</li>\n',
      rel=[('saitei-chingin-chiba', '千葉県の最低賃金', '千葉県は1,195円で、茨城県より59円高い額です。'),
           ('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、茨城県との差は144円です。')]),
 dict(name='広島県', slug='hiroshima', short='広島', word='広島県の最低賃金', kyoku='広島労働局', upd='2026年11月19日',
      ind=[['製鉄業・鋼材・銑鉄鋳物・可鍛鋳鉄製造業など（鉄鋼業）', 1179, '2025年12月31日']],
      mid='鉄鋼業の事業場は特定最低賃金の1,179円と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼業だけは特定最低賃金の1,179円がかかります。',
      tokutei='''<p>広島県には8つの特定最低賃金があります。10月11日からは鉄鋼業の1,179円だけが広島県最低賃金1,141円より高い額です。ほかの7業種は1,141円で判定します。</p>
<p class="cap">広島県の特定最低賃金・時間額</p>
''' + table(['業種', '特定最低<br>賃金', '10月11日から<br>判定する額'], [
          [td('製鉄業・鋼材・銑鉄鋳物・可鍛鋳鉄製造業など', 'l'), td('1,179円'), td('1,179円')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,110円'), td('1,141円')],
          [td('自動車・同附属品製造業', 'l'), td('1,105円'), td('1,141円')],
          [td('金属製品製造業・はん用など機械器具製造業・船舶製造業・自動車小売業・各種商品小売業', 'l'), td('県の額より低い'), td('1,141円')]]) +
          '<p class="note" style="margin-top:8px">鉄鋼業・電子部品など・自動車の3業種の額は令和7年12月31日からのものです。令和8年度は8業種の改正の必要性が審議会に諮問され、船舶製造業と自動車小売業は改正しないと答申されました（令和8年10月7日）。ほかの6業種の改正が決まったら、この欄を直します。</p>\n',
      near=['広島県', '岡山県', '山口県', '島根県', '鳥取県', '愛媛県', '大阪府'],
      near_lead='広島県と中国・四国の近くの県の令和8年度の最低賃金です。広島県は中国地方で一番高い額です。',
      near_note='広島県は全国で11番目に高い額です。岡山県より37円・山口県より40円・島根県より49円高く、大阪府とは90円の差があります。',
      ex_month=185000,
      qa='<h3>広島県はなぜ10月11日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、広島県は10月11日でした。10月10日までに働いた分は前の年度の1,085円で判定します。</p>\n'
         + '<h3>自動車の部品工場で働く人の最低賃金はいくらですか？</h3>\n<p>自動車・同附属品製造業の特定最低賃金は1,105円で、広島県最低賃金1,141円より低い額です。10月11日からは1,141円以上が必要です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002815206.pdf">広島労働局「広島県最低賃金の改正について 令和8年10月11日から1,141円へ」</a>（令和8年9月11日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002823834.pdf">広島労働局「広島県の最低賃金」</a>（リーフレット・令和8年9月）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002469689.pdf">広島労働局「広島県特定（産業別）最低賃金の改正について」</a>（令和7年11月28日・令和7年12月31日発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002882326.pdf">広島労働局「広島県特定最低賃金の改正決定の必要性の有無について」</a>（令和8年10月7日答申）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、広島県より90円高い額です。'),
           ('saitei-chingin-fukuoka', '福岡県の最低賃金', '福岡県は1,114円で、広島県より27円低い額です。')]),
 dict(name='鹿児島県', slug='kagoshima', short='鹿児島', word='鹿児島県の最低賃金', kyoku='鹿児島労働局', upd='2026年11月19日',
      mid='鹿児島県の特定最低賃金は、10月25日からどれも鹿児島県最低賃金より低い額です',
      intro='新車の販売店も、10月25日からは1,090円以上が最低ラインです。',
      tokutei='''<p>鹿児島県には3つの特定最低賃金があります。自動車（新車）小売業の1,048円（令和7年12月28日から）は、10月25日からの鹿児島県最低賃金1,090円より低い額です。令和8年度はどの業種も改正がないので、業種にかかわらず1,090円以上が最低ラインです。</p>
<ul>
 <li>自動車（新車）小売業：1,048円。令和8年度は改正の申出がありましたが、改正は決まりませんでした</li>
 <li>電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業：令和8年度は改正の申出がありましたが、改正は決まりませんでした</li>
 <li>百貨店・総合スーパー：令和8年度は改正の申出がありませんでした</li>
</ul>
''' + '<p class="note" style="margin-top:8px">鹿児島労働局「鹿児島県の最低賃金について」と令和8年8月28日の運営小委員会の議事要旨によります。</p>\n',
      near=['鹿児島県', '熊本県', '宮崎県', '福岡県', '大分県', '沖縄県'],
      near_lead='鹿児島県と九州・沖縄の令和8年度の最低賃金です。鹿児島県は64円の引上げで、九州では佐賀県の65円に次ぐ上げ幅です。',
      near_note='鹿児島県は鳥取県と同じ額です。熊本県より2円低く、宮崎県より5円・沖縄県より4円高い額です。',
      ex_month=180000,
      qa='<h3>鹿児島県はなぜ10月25日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、鹿児島県は10月25日でした。10月24日までに働いた分は前の年度の1,026円で判定します。</p>\n'
         + '<h3>新車の販売店の最低賃金はいくらですか？</h3>\n<p>自動車（新車）小売業の特定最低賃金は1,048円ですが、10月25日からは鹿児島県最低賃金1,090円の方が高い額です。令和8年度は特定最低賃金の改正がないので、1,090円以上が必要です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/hourei_seido_tetsuzuki/kane/saitin01.html">鹿児島労働局「鹿児島県の最低賃金について」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/content/contents/2026-0828-1_r08_a3.pdf">鹿児島地方最低賃金審議会 第3回 議事要旨</a>（令和8年8月26日・1,090円の答申）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/content/contents/2025-1128-5_20251128.pdf">鹿児島労働局「鹿児島県自動車（新車）小売業最低賃金の改正について」</a>（令和7年11月28日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/content/contents/2026-0831-8_r08-c1.pdf">鹿児島地方最低賃金審議会 運営小委員会 議事要旨</a>（令和8年8月28日）</li>\n',
      rel=[('saitei-chingin-kumamoto', '熊本県の最低賃金', '熊本県は12月1日から1,092円で、鹿児島県より2円高い額です。'),
           ('saitei-chingin-okinawa', '沖縄県の最低賃金', '沖縄県は12月2日から1,086円で、鹿児島県より4円低い額です。')]),
]

if __name__ == '__main__':
    out = []
    for cfg in PREFS:
        cfg['rel'] = rel_for(cfg['rel'])
        out.append(pref_page(cfg))
    for s, t in out:
        print(s, t)


# ---- 全国のページ /saitei-chingin/ ----
HAVE = {'大阪府': 'osaka', '東京都': 'tokyo', '神奈川県': 'kanagawa', '北海道': 'hokkaido', '愛知県': 'aichi',
        '埼玉県': 'saitama', '福岡県': 'fukuoka', '千葉県': 'chiba', '兵庫県': 'hyogo', '京都府': 'kyoto',
        '沖縄県': 'okinawa', '熊本県': 'kumamoto', '茨城県': 'ibaraki', '広島県': 'hiroshima', '鹿児島県': 'kagoshima'}

JS_ALL = r'''(function(){
 var PR=%(pr)s;
 var k=0,$=function(i){return document.getElementById(i)};
 function f(n){return Math.round(n).toLocaleString("ja-JP");}
 function f1(n){return (Math.floor(n*10+1e-9)/10).toLocaleString("ja-JP",{minimumFractionDigits:1,maximumFractionDigits:1});}
 function num(i){var v=parseFloat($(i).value);return isNaN(v)?0:v;}
 function render(){
  var pay=num("pay"),ex=num("ex"),base=Math.max(0,pay-ex),div=1,lbl=["時給","日給","月給"][k];
  $("pay-l").textContent=lbl;
  $("w-day").classList.toggle("hide",k!==1);$("w-mon").classList.toggle("hide",k!==2);
  if(k===1){div=Math.max(0.25,num("dh"));}
  if(k===2){div=Math.max(1,(365-Math.min(300,num("hol")))*Math.max(0.25,num("mh"))/12);}
  var x=PR[+$("pref").value],M=x[1],h=base/div,ok=h>=M-1e-9,gap=Math.max(0,M-h);
  var now=new Date(),eff=new Date(2026,x[3]-1,x[4]),pre=now<eff;
  $("o-h").innerHTML=f1(h)+"<i>円</i>";
  $("o-hn").textContent=k===0?"含めない手当を除く":k===1?"日給÷"+div+"時間":"月給÷"+f1(div)+"時間";
  $("o-m").innerHTML=f(M)+"<i>円</i>";
  $("o-mn").textContent=x[0]+"・2026年"+x[3]+"月"+x[4]+"日から";
  var vd=$("vd");vd.className="vd"+(ok?" no":"");
  if(ok){$("o-vd").textContent="満たしています";$("o-vds").textContent=(h-M<0.05)?"時給に直すと"+f1(h)+"円で、"+x[0]+"の最低賃金"+f(M)+"円と同じ額です":"時給に直すと"+f1(h)+"円で、"+x[0]+"の最低賃金"+f(M)+"円より"+f1(h-M)+"円高い額です";}
  else{var per=k===0?"":(k===1?"1日あたり":"1か月あたり")+f(Math.ceil(gap*div-1e-9))+"円足りません。";
   $("o-vd").textContent="下回っています";$("o-vds").textContent=x[0]+"の最低賃金"+f(M)+"円より時給あたり"+f1(gap)+"円足りません。"+per+"差額を払う必要があります";}
  $("o-old").textContent=pre?"まだ発効前です。2026年"+x[3]+"月"+x[4]+"日の前日までは改定前の"+f(x[2])+"円と比べます（"+(h>=x[2]-1e-9?"満たしています":"下回っています")+"）":"改定前の"+f(x[2])+"円から"+(M-x[2])+"円上がりました";
 }
 ["pay","ex","dh","hol","mh"].forEach(function(i){$(i).addEventListener("input",render);});
 $("pref").addEventListener("change",render);
 document.querySelectorAll(".seg button").forEach(function(b){b.addEventListener("click",function(){document.querySelectorAll(".seg button").forEach(function(y){y.classList.remove("on");});b.classList.add("on");k=+b.dataset.k;
  if(k===0)$("pay").value=1200;if(k===1)$("pay").value=9600;if(k===2)$("pay").value=200000;render();});});
 render();
})();'''


def all_page():
    slug = 'saitei-chingin'; cta = 'saitei_all'
    title = '【最低賃金の一覧】2026年はいくら？47都道府県のランキングと計算【令和8年度】'
    desc = '令和8年度の最低賃金は全国加重平均で時給1,177円です。47都道府県の最低賃金を高い順のランキング・発効日・年間休日120日の月給の目安の一覧にしました。都道府県と時給・日給・月給を入れると最低賃金を下回っていないかが分かります。'
    upd = '更新日：2026年11月18日（厚生労働省 令和8年度地域別最低賃金額答申状況）'
    pr = [[p['name'], p['new'], p['old'], p['mo'], p['da']] for p in P]
    opts = ''.join('<option value="%d"%s>%s（%s円）</option>' % (i, ' selected' if p['name'] == '東京都' else '', p['name'], c(p['new'])) for i, p in enumerate(P))
    calc = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span>令和8年度の最低賃金は全国加重平均で時給1,177円です</div>
 <div class="amt">
  <div><small>全国加重<br>平均</small><b>1,177<i>円</i></b><em>前の年度1,121円</em></div>
  <div><small>一番高い<br>東京都</small><b>1,280<i>円</i></b><em>10月1日から</em></div>
  <div><small>一番低い<br>宮崎県</small><b>1,085<i>円</i></b><em>10月24日から</em></div>
 </div>
 <div class="in">
  <div class="full">
   <label for="pref">働いている事業場の都道府県</label>
   <select id="pref">%s</select>
  </div>
  <div class="full">
   <label>給料の払い方</label>
   <div class="seg seg3"><button type="button" class="on" data-k="0">時給</button><button type="button" data-k="1">日給</button><button type="button" data-k="2">月給</button></div>
  </div>
  <div class="full">
   <label for="pay" id="pay-l">時給</label>
   <div class="row"><input type="number" id="pay" inputmode="numeric" min="0" max="10000000" step="1" value="1200"><span>円</span></div>
  </div>
  <div class="full">
   <label for="ex" id="ex-l">このうち最低賃金に含めない手当（通勤手当・家族手当・精皆勤手当・残業代など）</label>
   <div class="row"><input type="number" id="ex" inputmode="numeric" min="0" max="10000000" step="1" value="0"><span>円</span></div>
  </div>
  <div class="full hide" id="w-day">
   <label for="dh">1日の決まった労働時間</label>
   <div class="row"><input type="number" id="dh" inputmode="decimal" min="1" max="24" step="0.25" value="8"><span>時間</span></div>
  </div>
  <div class="full hide" id="w-mon">
   <label for="hol">年間の休日の日数（会社の年間カレンダー）</label>
   <div class="row"><input type="number" id="hol" inputmode="numeric" min="0" max="300" step="1" value="120"><span>日</span></div>
   <label for="mh">1日の決まった労働時間</label>
   <div class="row"><input type="number" id="mh" inputmode="decimal" min="1" max="24" step="0.25" value="8"><span>時間</span></div>
  </div>
 </div>
 <div class="vd" id="vd"><b id="o-vd"></b><span id="o-vds"></span></div>
 <div class="amt jdg">
  <div><small>時給に直すと</small><b id="o-h"></b><em id="o-hn"></em></div>
  <div><small>比べる最低賃金</small><b id="o-m"></b><em id="o-mn"></em></div>
 </div>
 <ul>
  <li id="o-old"></li>
  <li>本社ではなく、その人が働いている事業場の都道府県で判定します</li>
  <li>業種ごとの特定最低賃金がかかる人は、高い方の額と比べます</li>
 </ul>
</div>
''' % opts
    intro = '<p>令和8年度の最低賃金は、全国加重平均で時給1,177円です。前の年度の1,121円から56円の引上げです。<span class="mk">一番高い東京都は1,280円・一番低い宮崎県は1,085円で、差は195円です。</span>引上げの日は都道府県ごとに違い、10月1日から12月2日までに順に変わります。</p>\n'
    toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#rank">47都道府県の最低賃金の一覧（高い順）</a></li>
  <li><a href="#itsu">最低賃金はいつから上がるか（発効日の順）</a></li>
  <li><a href="#getsu">月給にすると最低いくらか</a></li>
  <li><a href="#fukumu">最低賃金に含める賃金・含めない賃金</a></li>
  <li><a href="#kanzan">日給・月給を時給に直すやり方</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">最低賃金でよく聞かれること</a></li>
 </ol>
</nav>
'''
    rows = []
    for p in sorted(P, key=lambda x: (-x['new'], P.index(x))):
        nm = p['name']
        cell = '<a href="/saitei-chingin-%s/">%s</a>' % (HAVE[nm], nm) if nm in HAVE else nm
        rows.append([td('%d' % rank(nm), 'c'), td(cell, 'l'), td(c(p['new'])), td(c(p['old'])), td('+%d' % (p['new'] - p['old'])), td('%d/%d' % (p['mo'], p['da']), 'c'), td(c(mon(p['new'], 120)))])
    sec1 = ('<h2 id="rank">47都道府県の最低賃金の一覧（高い順）</h2>\n<p>令和8年度の地域別最低賃金を高い順に並べました。月給は年間休日120日・1日8時間で最低賃金を満たす額です。都道府県の名前を押すと、その県の特定最低賃金や近くの県との比較を見られます。</p>\n<p class="cap">令和8年度・時間額（円）</p>\n'
            + table(['順位', '都道府県', '令和8<br>年度', '令和7<br>年度', '上げ<br>幅', '発効<br>日', '月給の<br>目安'], rows)
            + '<p class="note" style="margin-top:8px">発効日は厚生労働省の答申状況の予定日です。月給の目安は円未満を切り上げた額です。全国加重平均は1,177円（前の年度1,121円）です。</p>\n')
    # いつから
    by = {}
    for p in P:
        by.setdefault((p['mo'], p['da']), []).append(p['name'])
    rows = []
    for (mo, da) in sorted(by):
        rows.append([td('%d月%d日' % (mo, da), 'c'), td('・'.join(by[(mo, da)]), 'l'), td('%d' % len(by[(mo, da)]), 'c')])
    late = [p['name'] for p in P if (p['mo'], p['da']) > (11, 18)]
    sec2 = ('<h2 id="itsu">最低賃金はいつから上がるか（発効日の順）</h2>\n<p>最低賃金は、都道府県ごとに決まった発効日から新しい額になります。発効日の前日までに働いた分は、前の年度の額で判定します。2026年11月18日の時点で、%sはまだ発効前です。</p>\n' % '・'.join(late)
            + table(['発効日', '都道府県', '数'], rows)
            + '<p class="note" style="margin-top:8px">10月1日に変わったのは%d都道府県です。一番遅いのは沖縄県の12月2日です。</p>\n' % len(by[(10, 1)]))
    # 月給
    rows = []
    for nm in ['東京都', '神奈川県', '大阪府', '埼玉県', '愛知県', '北海道', '福岡県', '宮崎県']:
        m = D[nm]['new']
        rows.append([td(nm, 'l')] + [td(c(mon(m, h))) for h in (125, 120, 110, 105)])
    sec3 = ('<h2 id="getsu">月給にすると最低いくらか</h2>\n<p>月給の人は、月給を1か月の平均の労働時間で割って最低賃金と比べます。主な都道府県について、年間休日ごとに最低賃金を満たす月給を出しました。</p>\n<p class="cap">1日8時間・含めない手当を除いた月給（円）</p>\n'
            + table(['都道府県', '休日<br>125日', '休日<br>120日', '休日<br>110日', '休日<br>105日'], rows)
            + '<p class="note" style="margin-top:8px">1か月の平均時間は（365日−年間休日）×8時間÷12で出しています。ほかの都道府県は上の計算に月給と年間休日を入れると判定できます。</p>\n')
    sm = 200000
    sec5 = ('<h2 id="kanzan">日給・月給を時給に直すやり方</h2>\n<h3>日給</h3>\n<p>日給を1日の決まった労働時間で割ります。日給9,600円で1日8時間なら時給1,200円です。東京都・神奈川県・大阪府では下回り、それ以外の道府県では満たしています。</p>\n'
            '<h3>月給</h3>\n<p>月給を1か月の平均の労働時間で割ります。年間休日120日・1日8時間なら1か月の平均は163.3時間で、月給20万円は時給%s円です。</p>\n'
            '<h3>月給20万円で足りる都道府県</h3>\n<p>年間休日120日・1日8時間なら、月給20万円で最低賃金を満たすのは%d道府県です。東京都・神奈川県・大阪府の3都府県では下回ります。</p>\n') % (f1(sm / hrs(120)), sum(1 for p in P if sm / hrs(120) >= p['new']))
    rel_items = [('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で全国で一番高い額です。'),
                 ('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、特定最低賃金が12月から上がります。'),
                 ('saitei-chingin-kanagawa', '神奈川県の最低賃金', '神奈川県は1,279円で、東京都との差は1円です。'),
                 ('saitei-chingin-aichi', '愛知県の最低賃金', '愛知県は1,195円で、自動車の工場の特定最低賃金の改正が審議されています。'),
                 ('saitei-chingin-hokkaido', '北海道の最低賃金', '北海道は1,131円で、鉄鋼業だけ1,165円です。')] + REL_COMMON[1:7] + [REL_COMMON[8]]
    sec6 = rel(slug, rel_items)
    qa = ('<h2 id="qa">最低賃金でよく聞かれること</h2>\n'
          '<h3>2026年の最低賃金はいつから上がりますか？</h3>\n<p>都道府県ごとに違い、2026年10月1日から12月2日までに順に上がります。東京都・神奈川県・大阪府・愛知県などは10月1日からです。</p>\n'
          '<h3>最低賃金が一番高いのはどこですか？</h3>\n<p>東京都の時給1,280円です。2番目は神奈川県の1,279円・3番目は大阪府の1,231円です。</p>\n'
          '<h3>最低賃金が一番低いのはどこですか？</h3>\n<p>宮崎県の時給1,085円です。東京都との差は195円で、一番低い額は一番高い額の84.8%です。</p>\n'
          '<h3>正社員にも最低賃金はかかりますか？</h3>\n<p>かかります。正社員・パート・アルバイトなど働き方にかかわらず、働く人すべてにかかります。月給の人は時給に直して比べます。</p>\n'
          '<h3>最低賃金を下回っていたらどうなりますか？</h3>\n<p>最低賃金に届かない部分の決まりは無効になり、最低賃金と同じ額で決めたものとみなされます。差額を払う必要があり、地域別最低賃金を払わなかったときは50万円以下の罰金の決まりがあります。</p>\n')
    src = '<div class="src">出典・参考（2026年11月確認）\n <ul>\n%s </ul>\n</div>\n' % SRC_COMMON
    body = calc + '\n' + share(slug) + '\n' + intro + '\n' + toc + '\n' + sec1 + '\n' + sec2 + '\n' + sec3 + '\n' + FUKUMU + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
    js = JS_ALL % dict(pr=json.dumps(pr, ensure_ascii=False))
    os.makedirs(os.path.join(SITE, slug), exist_ok=True)
    open(os.path.join(SITE, slug, 'index.html'), 'w', encoding='utf-8').write(page(slug, title, desc, upd, body, js, cta))
    return slug, title

if __name__ == '__main__':
    print(all_page())
