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
STYLE = re.sub(r'<link rel="icon" href="/favicon\.svg" type="image/svg\+xml">', '', STYLE)
STYLE = re.sub(r'<link rel="apple-touch-icon" href="/apple-touch-icon\.png">', '', STYLE)
STYLE = STYLE.rstrip()
HEAD_END = '</head>'
AUTH = re.search(r'<div class="auth" id="auth">.*?</div>', OSAKA, re.S).group(0)
TOOLS_NAV = re.search(r'<nav class="tools">.*?</nav>', OSAKA, re.S).group(0)

def hy_wrap(sec):
    # 早見表を計算の箱の前に置く
    return ('<section class="hy1">\n' + sec.rstrip()
            + '\n<p class="lead2">自分の数字で計算したい人は、下に入力してください。</p>\n</section>\n\n')

def auth_box(src):
    # 監修枠。src はそのページの出典の機関名（「、」は使わない）
    return ('<div class="auth" id="auth"><p class="auth-h">監修・制作税理士</p><p class="auth-n">大山 俊郎</p>'
            '<p class="auth-r">近畿税理士会所属（登録番号127208）</p>'
            '<p>このページの数字は2026年11月に私が確かめました。もとにしているのは、%sの数字です。</p>'
            '<p><a href="/#auth">詳しいプロフィール</a></p></div>') % src
FOOT = OSAKA[OSAKA.index('</main>\n<footer'):OSAKA.index('<div class="fbar one">')]
TAIL = OSAKA[OSAKA.index('<script id="fbzj">'):]
LOGO = re.search(r'<a class="logo" href="/">.*?</a>', OSAKA, re.S).group(0)
PIC = re.search(r'<div class="pic">.*?</div>', OSAKA, re.S).group(0)
PIC_YEN = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="人と円"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><circle cx="25" cy="24" r="8" fill="#0f3d31"/><path d="M11 50c1-10 7-15 14-15s13 5 14 15z" fill="#0f3d31"/><circle cx="46" cy="40" r="10" fill="#e3b465"/><text x="46" y="45" font-size="13" font-weight="700" text-anchor="middle" fill="#0f3d31" font-family="sans-serif">円</text></svg></div>'
STYLE = STYLE  # 同じ見た目

def page(slug, title, desc, upd, body, script, cta, pic=PIC_YEN, auth=None):
    if auth is None:
        auth = AUTH
    url = 'https://taxtable.jp/%s/' % slug
    return ('<!doctype html>\n<html lang="ja"><head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="color-scheme" content="light">\n'
            '<title>%s</title>\n<link rel="canonical" href="%s">\n<meta name="description" content="%s">\n%s\n<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png"></head>\n<body>\n'
            '<header class="hd"><div class="wrap">\n %s\n <nav><a href="/#list">早見表・計算ツール</a><a href="#auth">監修・制作税理士</a></nav>\n'
            ' <div class="hcta"><a class="y" href="https://oyama-toshiro.com/contact/" data-cta="%s_head_marunage">経理丸投げの無料相談 →</a></div>\n</div></header>\n\n'
            '<main class="wrap">\n<div class="top">\n %s\n <p class="upd">%s</p>\n <h1>%s</h1>\n</div>\n\n%s\n%s\n%s\n%s'
            '<div class="fbar one">\n <a class="k" href="https://oyama-toshiro.com/contact/" data-cta="%s_fbar_marunage"><small>全国オンライン対応</small><span>経理丸投げの無料相談 ›</span></a>\n</div>\n\n'
            '<script>\n%s\n</script>\n\n%s') % (title, url, desc, STYLE, LOGO, cta, pic, upd, title, body, auth, close_box(cta), TOOLS_NAV + '\n' + FOOT, cta, script, TAIL)

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
  <li><a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/chingin/newpage_43898.html">厚生労働省「最低賃金の対象となる賃金」</a></li>
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
    desc = '%sの最低賃金は%sから時給%s円です。年間休日ごとの月給の目安・%sの特定最低賃金・近くの都道府県との比較を早見表にしました。時給・日給・月給を入力すると最低賃金を下回っていないかが分かります。' % (n, ds(p), c(m), n)
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
  <div><small>%(agaru)s</small><b>%(up)d<i>円</i></b><em>時給あたり</em></div>
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
''' % dict(n=n, ds=ds(p), m=c(m), o=c(o), up=up, exh=ex_h, sel=sel, mid=cfg['mid'], agaru='上がる額' if (2026, p['mo'], p['da']) > TODAY else '上がった額')
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
    sec1 = ('<h2 id="list">月給にすると最低いくらか（年間休日ごと）</h2>\n<p>月給の人は、月給を1か月の平均の労働時間で割って最低賃金と比べます。1日8時間で働く会社の年間休日ごとに、最低賃金を満たす月給を計算しました。</p>\n'
            '<p class="cap">%s・1日8時間・含めない手当を除いた月給</p>\n' % n
            + table(['年間<br>休日', '1か月の<br>平均時間', '令和8年度<br>（円）', '令和7年度<br>（円）', '差<br>（円）'], rows)
            + '<p class="note" style="margin-top:8px">1か月の平均時間は（365日−年間休日）×8時間÷12で出しています。月給は円未満を切り上げた額です。基本給と毎月決まって払う手当の合計がこの額以上なら、最低賃金を満たしています。</p>\n')
    rows = []
    for h in (4, 5, 6, 7, 7.5, 8):
        d = math.ceil(m * h - 1e-9)
        rows.append([td(('%g' % h) + '時間'), td(c(d)), td(c(d * 20)), td(c(d * 240))])
    sec2 = ('<h2 id="day">時給・日給の早見表</h2>\n<p>パート・アルバイトの1日の時間ごとに、時給%s円で払うときの日給と月の額を計算しました。月の額は1か月に20日働く場合です。</p>\n<p class="cap">%s・時給%s円</p>\n' % (c(m), n, c(m))
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
    sec5 = ('<h2 id="kanzan">日給・月給を時給に直すやり方</h2>\n<h3>日給</h3>\n<p>日給を1日の決まった労働時間で割ります。日給%s円で1日8時間なら時給%s円で、%sの最低賃金%sを%d円下回ります。</p>\n'
            '<h3>月給</h3>\n<p>月給を1か月の平均の労働時間で割ります。1か月の平均の労働時間は、1年間の決まった労働時間を12で割って出します。年間休日120日・1日8時間なら、1か月の平均は163.3時間です。</p>\n'
            '<h3>月給%sは大丈夫か</h3>\n<p>年間休日120日・1日8時間なら、月給%sは時給%s円です。%sの最低賃金%s円を%s。%s</p>\n') % (
        c(dex), c(dh), (('%d月%d日からの' % (p['mo'], p['da'])) if (2026, p['mo'], p['da']) > TODAY else '') + n, (c(m) + '円') if (2026, p['mo'], p['da']) > TODAY else '', m - dh, man(sm), man(sm), f1(h120), n, c(m), cmpx(h120), t125)
    sec6 = rel(slug, cfg['rel'])
    qa = ('<h2 id="qa">%sの最低賃金でよく聞かれること</h2>\n' % short
          + '<h3>%sの最低賃金はいつから%s円ですか？</h3>\n<p>%sからです。その前日までに働いた分は、前の年度の%s円で判定します。</p>\n' % (short, c(m), ds(p), c(o))
          + '<h3>%sで月給はいくら以上ならいいですか？</h3>\n<p>年間休日120日・1日8時間なら、含めない手当を除いて月%s以上です。年間休日105日なら月%s以上です。</p>\n' % (short, man(m120), man(m105))
          + cfg['qa']
          + '<h3>試用期間なら最低賃金より低くてもいいですか？</h3>\n<p>%s長の許可を受けていなければ下げられません。許可を受けずに下げた分は、最低賃金との差額を払うことになります。</p>\n' % cfg['kyoku']
          + '<h3>最低賃金を下回っていたらどうなりますか？</h3>\n<p>最低賃金に届かない部分の決まりは無効になり、最低賃金と同じ額で決めたものとみなされます。差額を払う必要があり、%sの最低賃金を払わなかったときは50万円以下の罰金の決まりがあります。</p>\n' % n)
    src = '<div class="src">出典・参考（2026年11月確認）\n <ul>\n%s%s </ul>\n</div>\n' % (cfg['src'], SRC_COMMON)
    body = hy_wrap(sec1) + calc + '\n' + share(slug) + '\n' + intro + '\n' + toc + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + FUKUMU + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
    js = JS_PREF % dict(base=m, old=o, pn=n, date=ds(p), eff='2026-%02d-%02dT00:00:00+09:00' % (p['mo'], p['da']), ind=json.dumps(IND, ensure_ascii=False), ex_h=ex_h, ex_d=dex, ex_m=sm)
    html_ = page(slug, title, desc, upd, body, js, cta, auth=auth_box(cfg['kyoku'] + 'と厚生労働省'))
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
 dict(name='東京都', slug='tokyo', short='東京', word='東京の最低賃金', kyoku='東京労働局', upd='2026年11月20日',
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
          '<p class="note" style="margin-top:8px">令和8年度は、東京地方最低賃金審議会に特定最低賃金の改正3件と新設2件の申出が出ています。新設の申出は電気機械器具製造業などと自動車小売業（新車）です。決まって東京都最低賃金を上回る額になったときは、この欄を直します。</p>\n',
      near=['東京都', '神奈川県', '埼玉県', '千葉県', '山梨県', '大阪府', '愛知県'],
      near_lead='東京都と近くの県・大阪府・愛知県の令和8年度の最低賃金です。働く場所が都県をまたぐときは、事業場がある都道府県の額で判定します。',
      near_note='東京都は全国で一番高い額で、神奈川県との差は1円です。埼玉県・千葉県とは84円〜85円の差があります。',
      ex_month=210000,
      qa='<h3>本社が地方で東京の店で働く人はどちらの額ですか？</h3>\n<p>働いている東京の店の額で、時給1,280円です。派遣社員は、派遣先の事業場がある都道府県の額で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/tokyo-roudoukyoku/news_topics/houdou/20260930chinginka_00001.html">東京労働局「東京都最低賃金が10月1日から1,280円に」</a>（令和8年9月30日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/tokyo-roudoukyoku/content/contents/002025134.pdf">東京労働局「東京都の特定最低賃金 改正一覧表（平成21年度〜令和7年度）」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/tokyo-roudoukyoku/content/contents/002822599.pdf">東京地方最低賃金審議会「令和8年度 特定（産業別）最低賃金 改正等申出状況」</a></li>\n',
      rel=[('saitei-chingin-kanagawa', '神奈川県の最低賃金', '神奈川県は1,279円で、東京都との差は1円です。'),
           ('saitei-chingin-saitama', '埼玉県の最低賃金', '埼玉県は1,196円で、東京都との差は84円です。'),
           ('saitei-chingin-chiba', '千葉県の最低賃金', '千葉県は1,195円で、東京都との差は85円です。')]),
 dict(name='神奈川県', slug='kanagawa', short='神奈川', word='神奈川県の最低賃金', kyoku='神奈川労働局', upd='2026年11月20日',
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
      src='  <li><a href="https://jsite.mhlw.go.jp/kanagawa-roudoukyoku/home/houdou/20260827_00001.html">神奈川労働局「令和8年度「神奈川県最低賃金」を改正決定します」</a>（令和8年8月27日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kanagawa-roudoukyoku/hourei_seido_tetsuzuki/saiteichingin_chinginseido/_119684.html">神奈川労働局「神奈川県の最低賃金金額改正一覧」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/kanagawa-roudoukyoku/hourei_seido_tetsuzuki/saiteichingin_chinginseido/_119730.html">神奈川労働局「特定（産業別）最低賃金」</a></li>\n',
      rel=[('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で全国で一番高い額です。'),
           ('saitei-chingin-shizuoka', '静岡県の最低賃金', '静岡県は1,154円で、神奈川県との差は125円です。')]),
 dict(name='北海道', slug='hokkaido', short='北海道', word='北海道の最低賃金', kyoku='北海道労働局', upd='2026年11月20日',
      ind=[['鉄鋼業（鉄素形材製造業・その他の鉄鋼業を除く）', 1221, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1165, '2025年12月1日'],
           ['処理牛乳・乳飲料・乳製品・糖類製造業', 1160, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1113, ''],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1174, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1116, ''],
           ['船舶製造・修理業・船体ブロック製造業', 1162, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1105, '']],
      mid='鉄鋼業はいまも特定最低賃金1,165円と比べます。4業種とも12月1日から新しい特定最低賃金に変わります。業種を選ぶと切り替わります',
      intro='鉄鋼業はこれより高い特定最低賃金1,165円がかかり、12月1日からは4業種に特定最低賃金の1,160円〜1,221円がかかります。',
      tokutei='''<p>北海道には4つの特定最低賃金があります。4業種とも令和8年12月1日から改定され、どれも北海道の最低賃金1,131円より高くなります。11月30日までは鉄鋼業が1,165円で、ほかの3業種は1,131円で判定します。</p>
<p class="cap">北海道の特定最低賃金・時間額</p>
''' + table(['業種', '11月30日まで', '12月1日から'], [
          [td('鉄鋼業（鉄素形材製造業・その他の鉄鋼業を除く）', 'l'), td('1,165円'), td('1,221円')],
          [td('処理牛乳・乳飲料・乳製品・糖類製造業', 'l'), td('1,131円<br>（北海道の額）'), td('1,160円')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,131円<br>（北海道の額）'), td('1,174円')],
          [td('船舶製造・修理業・船体ブロック製造業', 'l'), td('1,131円<br>（北海道の額）'), td('1,162円')]]) +
          '<p class="note" style="margin-top:8px">12月1日からの額は、北海道労働局「北海道特定最低賃金の改定（引上げ）について」（令和8年10月28日）によります。鉄鋼業を除く3業種のいまの特定最低賃金（1,113円・1,116円・1,105円）は北海道の最低賃金より低いので、11月30日までは1,131円以上が必要です。業種に入るかどうかは、その事業場の主な事業で決まります。</p>\n',
      near=['北海道', '青森県', '岩手県', '秋田県', '宮城県', '東京都'],
      near_lead='北海道と東北の県・東京都の令和8年度の最低賃金です。北海道は東北6県のどこよりも高い額です。',
      near_note='北海道と東北6県で一番高い宮城県の差は33円です。岩手県は12月1日からの引上げです。',
      ex_month=180000,
      qa='<h3>札幌と地方で最低賃金は違いますか？</h3>\n<p>違いません。北海道の最低賃金は道内のどこでも時給1,131円です。鉄鋼業の事業場は特定最低賃金の1,165円で、12月1日からは4業種に1,160円〜1,221円の特定最低賃金がかかります。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/hokkaido-roudoukyoku/content/contents/002798678.pdf">北海道労働局「北海道最低賃金を時間額1,131円に引上げます」</a>（令和8年9月1日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hokkaido-roudoukyoku/content/contents/002868951.pdf">北海道労働局「北海道特定最低賃金の改定（引上げ）について」</a>（令和8年10月28日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hokkaido-roudoukyoku/minimum_wage.html">北海道労働局「最低賃金について」</a></li>\n',
      rel=[('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、北海道との差は149円です。'),
           ('saitei-chingin-miyagi', '宮城県の最低賃金', '宮城県は1,098円で、北海道より33円低い額です。')]),
 dict(name='愛知県', slug='aichi', short='愛知', word='愛知県の最低賃金', kyoku='愛知労働局', upd='2026年11月20日',
      ind=[['輸送用機械器具製造業', 1208, '2026年12月16日', '2026-12-16T00:00:00+09:00', 1146, ''],
           ['製鉄業・製鋼・製鋼圧延業・鋼材製造業', 1230, '2027年1月1日', '2027-01-01T00:00:00+09:00', 1175, '']],
      mid='輸送用機械器具製造業は12月16日から1,208円に変わり、鉄鋼業は2027年1月1日から1,230円に変わります。業種を選ぶと切り替わります',
      intro='輸送用機械器具製造業は2026年12月16日から1,208円、鉄鋼業は2027年1月1日から1,230円の特定最低賃金に変わります。',
      tokutei='''<p>愛知県には9つの特定最低賃金があり、令和8年度に額が改正されたのは鉄鋼業と輸送用機械器具製造業の2つです。いまの額はどちらも愛知県最低賃金1,195円より低いので、発効日の前日までは1,195円以上が最低ラインです。令和8年度の改正は令和8年11月13日に官報で公示され、次の額に決まりました。</p>
<p class="cap">愛知県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '新しい額', 'いつから'], [
          [td('製鉄業・製鋼・製鋼圧延業・鋼材製造業', 'l'), td('1,175円'), td('1,230円'), td('2027年<br>1月1日', 'c')],
          [td('輸送用機械器具製造業', 'l'), td('1,146円'), td('1,208円'), td('2026年<br>12月16日', 'c')]]) +
          '<p class="note" style="margin-top:8px">愛知労働局「愛知県の特定最低賃金（2業種）を引上げます」（令和8年11月13日）によります。発効日の前日までは愛知県最低賃金1,195円で判定します。額が改正されなかったほかの7業種も1,195円で判定します。自動車や部品の工場で働く人は、2026年12月16日から1,208円以上が最低ラインになります。</p>\n',
      near=['愛知県', '岐阜県', '三重県', '静岡県', '長野県', '東京都', '大阪府'],
      near_lead='愛知県と東海・長野の県・東京都・大阪府の令和8年度の最低賃金です。岐阜や三重から通う人も、愛知県内の事業場なら愛知県の額で判定します。',
      near_note='愛知県は千葉県と同じ額で全国で5番目に高い額です。岐阜県とは74円・三重県とは52円の差があります。',
      ex_month=195000,
      qa='<h3>自動車の部品工場は特定最低賃金ですか？</h3>\n<p>自動車や部品を作る事業場は、輸送用機械器具製造業の特定最低賃金の対象です。いまの額1,146円は愛知県最低賃金より低いので、1,195円以上を払えば足ります。2026年12月16日からは1,208円になります。18歳未満や65歳以上の人など特定最低賃金から除かれる人は、1,195円で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/002762658.pdf">愛知労働局「愛知県最低賃金の改正について答申」</a>（令和8年8月5日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/002843463.pdf">愛知労働局「最低賃金の履行確保を主眼とする監督指導の結果」</a>（令和8年10月5日・愛知県最低賃金1,195円の発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/002888802.pdf">愛知労働局「愛知県の特定最低賃金（2業種）を引上げます」</a>（令和8年11月13日）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、愛知県より36円高い額です。'),
           ('saitei-chingin-mie', '三重県の最低賃金', '三重県は1,143円で、愛知県より52円低い額です。'),
           ('saitei-chingin-shizuoka', '静岡県の最低賃金', '静岡県は1,154円で、愛知県より41円低い額です。')]),
]

# ---- 2026/11/18 に足した5府県(埼玉・福岡・千葉・兵庫・京都) ----
# 特定最低賃金:ind の要素は [業種, 新しい額, 新しい額の発効日, ISO日付, いまの額, いまの額の発効日]。発効日の前はいまの額で判定する。
PREFS += [
 dict(name='埼玉県', slug='saitama', short='埼玉', word='埼玉県の最低賃金', kyoku='埼玉労働局', upd='2026年11月20日',
      ind=[['非鉄金属製造業', 1216, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1161, '2025年12月1日'],
           ['光学機械器具・レンズ・時計・同部分品製造業', 1232, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1177, '2025年12月1日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1223, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1168, '2025年12月1日'],
           ['輸送用機械器具製造業', 1224, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1165, '2025年12月1日'],
           ['自動車小売業', 1207, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1152, '2025年12月1日']],
      mid='製造業など5業種は12月1日から特定最低賃金に変わります。業種を選ぶと切り替わります',
      intro='製造業と自動車小売業の5業種は、12月1日から特定最低賃金の1,207円〜1,232円がかかります。',
      tokutei='''<p>埼玉県には6つの特定最低賃金があります。5業種は令和8年12月1日から改正され、どれも埼玉県最低賃金1,196円より高くなります。11月30日までは改正前の額が埼玉県最低賃金より低いので、1,196円以上が最低ラインです。</p>
<p class="cap">埼玉県の特定最低賃金・時間額</p>
''' + table(['業種', '12月1日<br>から', 'いまの額', '上がる<br>額'], [
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
      src='  <li><a href="https://jsite.mhlw.go.jp/saitama-roudoukyoku/hourei_seido_tetsuzuki/chingin_kanairoudou.html">埼玉労働局「賃金・家内労働関係」</a>（埼玉県最低賃金と特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/saitama-roudoukyoku/content/contents/002784855.pdf">埼玉労働局「埼玉県最低賃金の改正決定」</a>（令和8年8月21日）</li>\n  <li><a href="https://www.pref.saitama.lg.jp/a0809/rodo/912-2009-1204-137.html">埼玉県「埼玉県の最低賃金・最低工賃」</a>（令和7年度の特定最低賃金の額）</li>\n',
      rel=[('saitei-chingin-gunma', '群馬県の最低賃金', '群馬県は1,120円で、埼玉県より76円低い額です。'),
           ('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、埼玉県との差は84円です。'),
           ('saitei-chingin-chiba', '千葉県の最低賃金', '千葉県は1,195円で、埼玉県より1円低い額です。')]),
 dict(name='福岡県', slug='fukuoka', short='福岡', word='福岡県の最低賃金', kyoku='福岡労働局', upd='2026年11月20日',
      ind=[['製鉄業・製鋼・製鋼圧延業・鋼材製造業', 1238, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1176, '2025年12月10日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1195, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1137, '2025年12月10日'],
           ['輸送用機械器具製造業', 1205, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1147, '2025年12月10日'],
           ['自動車（新車）小売業', 1185, '2026年12月10日', '2026-12-10T00:00:00+09:00', 1131, '2025年12月10日']],
      mid='鉄鋼・電子部品・輸送用機械・新車小売の4業種は特定最低賃金と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼業など4業種は、いまの特定最低賃金も福岡県最低賃金より高い額です。12月10日からさらに上がります。',
      tokutei='''<p>福岡県には5つの特定最低賃金があります。鉄鋼業・電子部品など・輸送用機械器具・新車の小売業の4業種は、いまの額も福岡県最低賃金1,114円より高い額です。令和8年12月10日から改正されます。百貨店・総合スーパーは令和8年度の改正がなく、福岡県最低賃金に抜かれました。</p>
<p class="cap">福岡県の特定最低賃金・時間額</p>
''' + table(['業種', '12月10日<br>から', 'いまの額', '上がる<br>額'], [
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
      rel=[('saitei-chingin-yamaguchi', '山口県の最低賃金', '山口県は1,101円で、福岡県より13円低い額です。'),
           ('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、福岡県より117円高い額です。'),
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
          '<p class="note" style="margin-top:8px">答申の額は千葉労働局長の決定と公示の前なので、計算には含めていません。決まったときはこの早見表と試算ツールを更新します。いまの額が1,195円より低い6業種は、千葉県最低賃金の1,195円で判定します。</p>\n',
      near=['千葉県', '東京都', '神奈川県', '埼玉県', '茨城県'],
      near_lead='千葉県と近くの都県の令和8年度の最低賃金です。千葉から東京に通う人は、働く東京の事業場の額で判定します。',
      near_note='千葉県は愛知県と同じ額で全国で5番目に高い額です。埼玉県とは1円・茨城県とは59円の差があります。',
      ex_month=200000,
      qa='<h3>千葉県の鉄鋼業の最低賃金はいくらですか？</h3>\n<p>いまは特定最低賃金の時給1,210円です。12月25日から1,265円にする答申が出ていて、決まるとその日から1,265円になります。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/content/contents/002801978.pdf">千葉労働局「千葉県最低賃金の改正決定」</a>（令和8年9月1日公示）</li>\n  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/content/contents/002786897.pdf">千葉労働局「千葉県の最低賃金の一覧」</a>（特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/content/contents/002862096.pdf">千葉地方最低賃金審議会「鉄鋼業最低賃金の改正決定に関する答申」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/chiba-roudoukyoku/hourei_seido_tetsuzuki/r08chibasaichin_boucyou_04_00002.html">千葉労働局「電子部品等の特定最低賃金の答申と異議の申出」</a>（令和8年10月7日）</li>\n',
      rel=[('saitei-chingin-saitama', '埼玉県の最低賃金', '埼玉県は1,196円で、千葉県より1円高い額です。'),
           ('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、千葉県との差は85円です。'),
           ('saitei-chingin-ibaraki', '茨城県の最低賃金', '茨城県は1,136円で、千葉県より59円低い額です。')]),
 dict(name='兵庫県', slug='hyogo', short='兵庫', word='兵庫県の最低賃金', kyoku='兵庫労働局', upd='2026年11月20日',
      ind=[['塗料製造業', 1199, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1158, '2025年12月1日'],
           ['鉄鋼業', 1231, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1180, '2025年12月1日'],
           ['はん用機械器具・生産用機械器具・業務用機械器具製造業', 1206, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1150, '2025年12月1日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1173, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1117, '2025年12月1日'],
           ['輸送用機械器具製造業', 1243, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1188, '2025年12月1日'],
           ['計量器・測定器・分析機器・試験機・測量機械器具製造業', 1173, '2026年12月1日', '2026-12-01T00:00:00+09:00', 1117, '2025年12月1日']],
      mid='製造業の6業種は12月1日に特定最低賃金が上がります。業種を選ぶと切り替わります',
      intro='製造業の6業種は12月1日から特定最低賃金が1,173円〜1,243円に上がります。',
      tokutei='''<p>兵庫県の特定最低賃金のうち、製造業の6業種が令和8年12月1日から改正されます。11月30日までは、鉄鋼業の1,180円と輸送用機械器具製造業の1,188円が兵庫県最低賃金1,172円より高い額です。</p>
<p class="cap">兵庫県の特定最低賃金・時間額</p>
''' + table(['業種', '12月1日<br>から', 'いまの額', '上がる<br>額'], [
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
      qa='<h3>神戸と姫路で最低賃金は違いますか？</h3>\n<p>違いません。兵庫県の最低賃金は県内のどこでも時給1,172円です。製造業の6業種の事業場だけは特定最低賃金がかかり、12月1日から1,173円〜1,243円です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/hyogo-roudoukyoku/content/contents/002875983.pdf">兵庫労働局「兵庫県の最低賃金」</a>（地域別最低賃金と特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hyogo-roudoukyoku/home/sintyaku_itiran/news_topics/houdou/2026.html">兵庫労働局「報道発表 2026年」</a>（9月1日 兵庫県最低賃金 時間額1,172円に改正決定）</li>\n  <li><a href="https://www.nishi.or.jp/smph/kurashi/rodo/rodogyosei/saiteichingin.html">西宮市「最低賃金」</a>（特定最低賃金の額・2026年11月9日更新）</li>\n  <li><a href="https://web.pref.hyogo.lg.jp/sr05/saiteitingin.html">兵庫県「最低賃金」</a>（令和7年度の特定最低賃金の額）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、兵庫県より59円高い額です。'),
           ('saitei-chingin-kyoto', '京都府の最低賃金', '京都府は11月16日から1,180円で、兵庫県より8円高い額です。'),
           ('saitei-chingin-okayama', '岡山県の最低賃金', '岡山県は1,104円で、兵庫県より68円低い額です。')]),
 dict(name='京都府', slug='kyoto', short='京都', word='京都府の最低賃金', kyoku='京都労働局', upd='2026年11月20日',
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
      qa='<h3>京都府はなぜ11月16日からですか？</h3>\n<p>京都地方最低賃金審議会が、公益委員の案をもとに発効日を11月16日とする答申を出したためです。11月15日までに働いた分は、前の年度の1,122円で判定します。</p>\n'
         + '<h3>11月の給料はどちらの額で計算しますか？</h3>\n<p>11月15日までに働いた分は1,122円・11月16日からの分は1,180円で判定します。月の途中で締める会社は、日ごとに分けて確かめてください。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002816577.pdf">京都労働局「京都府最低賃金の改正決定」</a>（令和8年9月18日公示）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002814861.pdf">京都労働局「令和8年度 特定最低賃金の改正等について」</a>（令和8年9月18日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002505545.pdf">京都労働局「京都府の特定最低賃金」</a>（電気機械器具製造業 令和8年1月24日から）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kyoto-roudoukyoku/content/contents/002840599.pdf">京都地方最低賃金審議会 議事録</a>（発効日の審議）</li>\n',
      rel=[('saitei-chingin-shiga', '滋賀県の最低賃金', '滋賀県は1,136円で、京都府より44円低い額です。'),
           ('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、京都府より51円高い額です。'),
           ('saitei-chingin-hyogo', '兵庫県の最低賃金', '兵庫県は1,172円で、京都府より8円低い額です。')]),
 dict(name='沖縄県', slug='okinawa', short='沖縄', word='沖縄県の最低賃金', kyoku='沖縄労働局', upd='2026年11月20日',
      mid='沖縄県の最低賃金は12月2日から変わります。12月1日までは前の年度の1,023円です',
      intro='12月1日までに働いた分は前の年度の1,023円で判定します。沖縄県の特定最低賃金はどれも県の最低賃金より低い額です。',
      tokutei='''<p>沖縄県には4つの特定最低賃金があります。どれも沖縄県最低賃金より低いので、業種にかかわらず12月2日からは1,086円以上が最低ラインです。</p>
<p class="cap">沖縄県の特定最低賃金・時間額</p>
''' + table(['業種', '特定最低<br>賃金', '発効日'], [
          [td('糖類製造業', 'l'), td('769円'), td('平成30年11月25日')],
          [td('新聞業', 'l'), td('879円'), td('令和4年11月17日')],
          [td('各種商品小売業', 'l'), td('770円'), td('平成30年11月23日')],
          [td('自動車（新車）小売業', 'l'), td('770円'), td('平成30年11月18日')]]) +
          '<p class="note" style="margin-top:8px">新聞業・糖類製造業・自動車（新車）小売業は令和8年度に改正の申出がありましたが、審議会は改正が必要との結論に至りませんでした（令和8年8月14日の審議会）。</p>\n',
      near=['沖縄県', '鹿児島県', '宮崎県', '熊本県', '長崎県', '福岡県', '東京都'],
      near_lead='沖縄県と九州の県の令和8年度の最低賃金です。沖縄県は発効日が12月2日で、全国で一番遅い日です。',
      near_note='沖縄県は高知県と同じ額で、宮崎県より1円高く鹿児島県より4円低い額です。九州で一番高い福岡県とは28円の差があります。',
      ex_month=180000,
      qa='<h3>沖縄県はなぜ12月2日からですか？</h3>\n<p>発効日は審議会で労使の意見が分かれ、採決で決まりました。使用者側は1,080円・令和9年1月2日からの案を出しましたが、採決で1,086円・12月2日からの案が賛成8名で答申されました（令和8年9月3日の審議会）。</p>\n'
         + '<h3>11月の給料はどちらの額で判定しますか？</h3>\n<p>11月に働いた分は、前の年度の1,023円で判定します。12月2日からの分は1,086円です。12月の途中で締める会社は、日ごとに分けて確かめてください。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002840324.pdf">沖縄労働局「令和8年度沖縄県最低賃金は時間額1,086円」</a>（令和8年10月5日・12月2日から発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002866931.pdf">沖縄地方最低賃金審議会 第4回 議事要旨</a>（令和8年9月3日・発効日の採決）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002776112.pdf">沖縄地方最低賃金審議会「令和8年度 審議計画」</a>（特定最低賃金の推移）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okinawa-roudoukyoku/content/contents/002816953.pdf">沖縄地方最低賃金審議会 第3回 議事要旨</a>（令和8年8月14日・特定最低賃金の必要性）</li>\n  <li><a href="https://www.pref.okinawa.jp/shigoto/koyorodo/1012030/1012038/1012041/1012040.html">沖縄県「沖縄県最低賃金」</a>（2026年10月23日更新）</li>\n',
      rel=[('saitei-chingin-kagoshima', '鹿児島県の最低賃金', '鹿児島県は1,090円で、沖縄県より4円高い額です。'),
           ('saitei-chingin-fukuoka', '福岡県の最低賃金', '福岡県は1,114円で、九州で一番高い額です。')]),
 dict(name='熊本県', slug='kumamoto', short='熊本', word='熊本県の最低賃金', kyoku='熊本労働局', upd='2026年11月21日',
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
      near_note='熊本県の12月1日からの額は山形県・島根県・香川県と同じです。福岡県とは22円の差があり、鹿児島県より2円・宮崎県より7円高い額です。',
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
      rel=[('saitei-chingin-tochigi', '栃木県の最低賃金', '栃木県は1,125円で、茨城県より11円低い額です。'),
           ('saitei-chingin-chiba', '千葉県の最低賃金', '千葉県は1,195円で、茨城県より59円高い額です。'),
           ('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で、茨城県との差は144円です。')]),
 dict(name='広島県', slug='hiroshima', short='広島', word='広島県の最低賃金', kyoku='広島労働局', upd='2026年11月20日',
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
          '<p class="note" style="margin-top:8px">鉄鋼業・電子部品など・自動車の3業種の額は令和7年12月31日からのものです。令和8年度は8業種の改正の必要性が審議会に諮問され、船舶製造業と自動車小売業は改正の必要性があるとの結論に至らなかったと答申されました（令和8年10月7日）。ほかの6業種の改正が決まったら、この欄を直します。</p>\n',
      near=['広島県', '岡山県', '山口県', '島根県', '鳥取県', '愛媛県', '大阪府'],
      near_lead='広島県と中国・四国の近くの県の令和8年度の最低賃金です。広島県は中国地方で一番高い額です。',
      near_note='広島県は全国で11番目に高い額です。岡山県より37円・山口県より40円・島根県より49円高く、大阪府とは90円の差があります。',
      ex_month=185000,
      qa='<h3>広島県はなぜ10月11日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、広島県は10月11日でした。10月10日までに働いた分は前の年度の1,085円で判定します。</p>\n'
         + '<h3>自動車の部品工場で働く人の最低賃金はいくらですか？</h3>\n<p>自動車・同附属品製造業の特定最低賃金は1,105円で、広島県最低賃金1,141円より低い額です。10月11日からは1,141円以上が必要です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002815206.pdf">広島労働局「広島県最低賃金の改正について 令和8年10月11日から1,141円へ」</a>（令和8年9月11日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002823834.pdf">広島労働局「広島県の最低賃金」</a>（リーフレット・令和8年9月）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002469689.pdf">広島労働局「広島県特定（産業別）最低賃金の改正について」</a>（令和7年11月28日・令和7年12月31日発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/hiroshima-roudoukyoku/content/contents/002882326.pdf">広島労働局「広島県特定最低賃金の改正決定の必要性の有無について」</a>（令和8年10月7日答申）</li>\n',
      rel=[('saitei-chingin-yamaguchi', '山口県の最低賃金', '山口県は1,101円で、広島県より40円低い額です。'),
           ('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、広島県より90円高い額です。'),
           ('saitei-chingin-fukuoka', '福岡県の最低賃金', '福岡県は1,114円で、広島県より27円低い額です。'),
           ('saitei-chingin-okayama', '岡山県の最低賃金', '岡山県は1,104円で、広島県より37円低い額です。')]),
 dict(name='鹿児島県', slug='kagoshima', short='鹿児島', word='鹿児島県の最低賃金', kyoku='鹿児島労働局', upd='2026年11月21日',
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
      near_note='鹿児島県は青森県・秋田県・鳥取県と同じ額です。岩手県も12月1日から同じ1,090円になります。熊本県の12月1日からの額より2円低く、宮崎県より5円・沖縄県より4円高い額です。',
      ex_month=180000,
      qa='<h3>鹿児島県はなぜ10月25日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、鹿児島県は10月25日でした。10月24日までに働いた分は前の年度の1,026円で判定します。</p>\n'
         + '<h3>新車の販売店の最低賃金はいくらですか？</h3>\n<p>自動車（新車）小売業の特定最低賃金は1,048円ですが、10月25日からは鹿児島県最低賃金1,090円の方が高い額です。令和8年度は特定最低賃金の改正がないので、1,090円以上が必要です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/hourei_seido_tetsuzuki/kane/saitin01.html">鹿児島労働局「鹿児島県の最低賃金について」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/content/contents/2026-0828-1_r08_a3.pdf">鹿児島地方最低賃金審議会 第3回 議事要旨</a>（令和8年8月26日・1,090円の答申）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/content/contents/2025-1128-5_20251128.pdf">鹿児島労働局「鹿児島県自動車（新車）小売業最低賃金の改正について」</a>（令和7年11月28日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/kagoshima-roudoukyoku/content/contents/2026-0831-8_r08-c1.pdf">鹿児島地方最低賃金審議会 運営小委員会 議事要旨</a>（令和8年8月28日）</li>\n',
      rel=[('saitei-chingin-kumamoto', '熊本県の最低賃金', '熊本県は12月1日から1,092円で、鹿児島県より2円高い額です。'),
           ('saitei-chingin-okinawa', '沖縄県の最低賃金', '沖縄県は12月2日から1,086円で、鹿児島県より4円低い額です。')]),
 dict(name='三重県', slug='mie', short='三重', word='三重県の最低賃金', kyoku='三重労働局', upd='2026年11月20日',
      mid='三重県の特定最低賃金は、どれもいまの三重県最低賃金より低い額です',
      intro='三重県の7つの特定最低賃金は、どれも1,143円より低い額です。',
      tokutei='''<p>三重県には7つの特定最低賃金があります。いまはどの業種も三重県最低賃金1,143円より低いので、業種にかかわらず1,143円以上が最低ラインです。</p>
<p class="cap">三重県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '令和8年度'], [
          [td('輸送用機械器具等製造業（自動車・同附属品・船舶・建設機械など）', 'l'), td('1,111円'), td('1,167円を答申')],
          [td('電線・ケーブル製造業', 'l'), td('1,097円'), td('1,153円を答申')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,031円'), td('改正しない')],
          [td('一般機械器具製造業', 'l'), td('762円'), td('改正しない')],
          [td('ガラス・同製品製造業', 'l'), td('923円'), td('―')],
          [td('洋食器・刃物・手道具・金物類製造業', 'l'), td('843円'), td('―')],
          [td('銑鉄鋳物・可鍛鋳鉄・鋳鉄管製造業', 'l'), td('739円'), td('―')]]) +
          '<p class="note" style="margin-top:8px">輸送用機械器具等と電線・ケーブルの2業種は、三重地方最低賃金審議会が令和8年10月21日に答申しました。発効は12月21日の予定です。異議の申出と官報の公示を経て決まるので、この計算にはまだ含めていません。決まったらこの欄と計算を直します。</p>\n',
      near=['三重県', '愛知県', '岐阜県', '静岡県', '滋賀県', '京都府', '奈良県', '和歌山県'],
      near_lead='三重県と東海・近畿の近くの府県の令和8年度の最低賃金です。三重から名古屋に通う人は、愛知県内の事業場なら愛知県の額で判定します。',
      near_note='三重県は全国で10番目に高い額です。愛知県とは52円・静岡県とは11円の差があり、岐阜県より22円・滋賀県より7円・奈良県より36円高い額です。',
      ex_month=185000,
      qa='<h3>三重県の最低賃金はいつから1,143円ですか？</h3>\n<p>令和8年10月1日からです。前の年度の1,087円は令和7年11月21日からだったので、10か月あまりで56円上がりました。</p>\n'
         + '<h3>自動車の部品工場で働く人の最低賃金はいくらですか？</h3>\n<p>輸送用機械器具等製造業の特定最低賃金はいま1,111円で、三重県最低賃金1,143円より低い額です。いまは1,143円以上が必要です。12月21日からの1,167円は答申の額で、決まったらこのページに入れます。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/mie-roudoukyoku/content/contents/002796736.pdf">三重労働局「三重県最低賃金が改正されます」</a>（令和8年9月1日・10月1日から1,143円）</li>\n  <li><a href="https://jsite.mhlw.go.jp/mie-roudoukyoku/content/contents/002796152.pdf">三重労働局「三重県内の最低賃金」</a>（リーフレット・令和8年10月1日発効版）</li>\n  <li><a href="https://jsite.mhlw.go.jp/mie-roudoukyoku/content/contents/002861359.pdf">三重労働局「2業種の三重県特定最低賃金改正を答申」</a>（令和8年10月21日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/mie-roudoukyoku/content/contents/002788911.pdf">令和8年度 第4回三重地方最低賃金審議会 議事要旨</a>（令和8年8月21日）</li>\n',
      rel=[('saitei-chingin-aichi', '愛知県の最低賃金', '愛知県は1,195円で、三重県より52円高い額です。'),
           ('saitei-chingin-gifu', '岐阜県の最低賃金', '岐阜県は1,121円で、三重県より22円低い額です。'),
           ('saitei-chingin-shizuoka', '静岡県の最低賃金', '静岡県は1,154円で、三重県より11円高い額です。')]),
 dict(name='静岡県', slug='shizuoka', short='静岡', word='静岡県の最低賃金', kyoku='静岡労働局', upd='2026年11月20日',
      mid='静岡県の特定最低賃金は、いまはどれも静岡県最低賃金より低い額です',
      intro='特定最低賃金の業種で働く人も、いまは1,154円以上が最低ラインです。',
      tokutei='''<p>静岡県の特定最低賃金は、10月15日からはどれも静岡県最低賃金1,154円より低い額です。特定最低賃金が改正されるまでは、業種にかかわらず1,154円以上が必要です。</p>
<p class="cap">静岡県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '令和8年度'], [
          [td('はん用・生産用・業務用・輸送用機械器具製造業', 'l'), td('1,133円'), td('1,184円を答申')],
          [td('鉄鋼・非鉄金属製造業', 'l'), td('1,117円'), td('1,160円を答申')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,042円'), td('改正の申出なし')]]) +
          '<p class="note" style="margin-top:8px">機械器具の4業種は、静岡地方最低賃金審議会の専門部会が10月30日に1,184円で答申しました。発効日と決定は確認できていないので、この計算にはまだ含めていません。鉄鋼・非鉄金属製造業は、静岡地方最低賃金審議会が11月12日に1,160円で答申しました。発効日は令和9年1月21日の予定で、決定はまだなので計算には含めていません。決まったらこの欄と計算を直します。</p>\n',
      near=['静岡県', '神奈川県', '東京都', '山梨県', '長野県', '愛知県', '岐阜県', '三重県'],
      near_lead='静岡県と近くの都県の令和8年度の最低賃金です。静岡県は東は神奈川県・西は愛知県に挟まれています。',
      near_note='静岡県は全国で9番目に高い額です。愛知県とは41円・神奈川県とは125円の差があり、三重県より11円・長野県より37円・山梨県より41円高い額です。',
      ex_month=190000,
      qa='<h3>静岡県はなぜ10月15日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、静岡県は10月15日でした。10月14日までに働いた分は前の年度の1,097円で判定します。</p>\n'
         + '<h3>浜松の自動車の部品工場で働く人の最低賃金はいくらですか？</h3>\n<p>輸送用機械器具製造業などの特定最低賃金はいま1,133円で、静岡県最低賃金1,154円より低い額です。いまは1,154円以上が必要です。静岡県の最低賃金は浜松市でも静岡市でも同じ額です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/shizuoka-roudoukyoku/roudoukyoku/roudou/chingin/newpage_00059.html">静岡労働局「令和8年度「静岡県最低賃金」の改正を決定しました」</a>（令和8年9月4日・10月15日から1,154円）</li>\n  <li><a href="https://jsite.mhlw.go.jp/shizuoka-roudoukyoku/content/contents/251106press_tokuchinkaisei.pdf">静岡労働局「静岡県特定最低賃金の改正を決定しました」</a>（令和7年11月6日・令和7年12月21日から）</li>\n  <li><a href="https://jsite.mhlw.go.jp/shizuoka-roudoukyoku/content/contents/R8_toku_hanyou_toushin.pdf">静岡地方最低賃金審議会「静岡県はん用機械器具、生産用機械器具、業務用機械器具、輸送用機械器具製造業最低賃金の改正決定について」</a>（答申）</li>\n  <li><a href="https://jsite.mhlw.go.jp/shizuoka-roudoukyoku/roudoukyoku/roudou/chingin/newpage_00052.html">静岡労働局「静岡地方最低賃金審議会」</a></li>\n',
      rel=[('saitei-chingin-aichi', '愛知県の最低賃金', '愛知県は1,195円で、静岡県より41円高い額です。'),
           ('saitei-chingin-kanagawa', '神奈川県の最低賃金', '神奈川県は1,279円で、静岡県との差は125円です。')]),
 dict(name='宮城県', slug='miyagi', short='宮城', word='宮城県の最低賃金', kyoku='宮城労働局', upd='2026年11月21日',
      ind=[['鉄鋼業', 1187, '2026年12月15日', '2026-12-15T00:00:00+09:00', 1125, '2025年12月15日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1138, '2026年12月15日', '2026-12-15T00:00:00+09:00', 1077, '2025年12月15日'],
           ['自動車小売業', 1161, '2026年12月15日', '2026-12-15T00:00:00+09:00', 1101, '2025年12月15日']],
      mid='鉄鋼業と自動車小売業はいまも特定最低賃金で判定します。3業種とも12月15日から新しい額に変わります。業種を選ぶと切り替わります',
      intro='鉄鋼業など3業種の特定最低賃金は、12月15日から1,138円〜1,187円に上がります。',
      tokutei='''<p>宮城県には3つの特定最低賃金があります。3業種とも令和8年12月15日から改正され、どれも宮城県最低賃金1,098円より高くなります。12月14日までは鉄鋼業の1,125円と自動車小売業の1,101円が1,098円より高い額です。電子部品などの製造業は12月14日まで1,098円で判定します。</p>
<p class="cap">宮城県の特定最低賃金・時間額</p>
''' + table(['業種', '12月14日まで', '12月15日から'], [
          [td('鉄鋼業', 'l'), td('1,125円'), td('1,187円')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,098円<br>（県の額）'), td('1,138円')],
          [td('自動車小売業', 'l'), td('1,101円'), td('1,161円')]]) +
          '<p class="note" style="margin-top:8px">12月15日からの額は、宮城労働局「宮城県特定最低賃金の改正が決定しました」によります。電子部品などの製造業の特定最低賃金1,077円（令和7年12月15日から）は県の額より低いので、12月14日までは1,098円以上が必要です。</p>\n',
      near=['宮城県', '岩手県', '秋田県', '山形県', '福島県', '青森県', '北海道', '東京都'],
      near_lead='宮城県と東北・北海道・東京都の令和8年度の最低賃金です。宮城県は東北6県で一番高い額です。',
      near_note='宮城県は全国で30番目の額です。福島県より4円・山形県より6円・青森県と秋田県より8円高く、北海道とは33円の差があります。岩手県は12月1日から1,090円になり、宮城県との差は8円です。',
      ex_month=180000,
      qa='<h3>宮城県の最低賃金はいつから1,098円ですか？</h3>\n<p>令和8年10月1日からです。前の年度の1,038円から60円上がりました。仙台市でもほかの市町村でも同じ額です。</p>\n'
         + '<h3>車の販売店で働く人の最低賃金はいくらですか？</h3>\n<p>自動車小売業の特定最低賃金は12月14日まで1,101円で、12月15日からは1,161円です。どちらも宮城県最低賃金1,098円より高いので、特定最低賃金で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/miyagi-roudoukyoku/content/contents/002764301.pdf">宮城労働局「令和8年度宮城県最低賃金の改正答申について」</a>（令和8年8月5日答申・10月1日発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/miyagi-roudoukyoku/content/contents/002811446.pdf">宮城労働局「確認OK？最低賃金」</a>（令和8年10月1日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/miyagi-roudoukyoku/content/contents/002871763.pdf">宮城労働局「宮城県特定最低賃金の改正が決定しました」</a>（令和8年12月15日から）</li>\n  <li><a href="https://jsite.mhlw.go.jp/miyagi-roudoukyoku/content/contents/002446962.pdf">宮城労働局「宮城県特定最低賃金の改正が決定しました」</a>（令和7年12月15日から）</li>\n  <li><a href="https://www.pref.miyagi.jp/soshiki/koyou/saichin.html">宮城県「宮城県最低賃金」</a></li>\n',
      rel=[('saitei-chingin-hokkaido', '北海道の最低賃金', '北海道は1,131円で、宮城県より33円高い額です。'),
           ('saitei-chingin-niigata', '新潟県の最低賃金', '新潟県は1,108円で、宮城県より10円高い額です。')]),
 dict(name='新潟県', slug='niigata', short='新潟', word='新潟県の最低賃金', kyoku='新潟労働局', upd='2026年11月20日',
      mid='新潟県の特定最低賃金は、10月1日からどれも新潟県最低賃金より低い額です',
      intro='新潟県の3つの特定最低賃金は令和8年度に改正がなく、どの業種も1,108円以上が最低ラインです。',
      tokutei='''<p>新潟県には3つの特定最低賃金があります。令和8年度はどの業種も改正がなく、10月1日からは3業種とも新潟県最低賃金1,108円より低い額です。業種にかかわらず1,108円以上が必要です。</p>
<p class="cap">新潟県の特定最低賃金・時間額</p>
''' + table(['業種', '特定最低<br>賃金', '10月1日から<br>判定する額'], [
          [td('自動車（新車）・自動車部分品・附属品小売業', 'l'), td('1,053円'), td('1,108円')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,005円'), td('1,108円')],
          [td('各種商品小売業', 'l'), td('932円'), td('1,108円')]]) +
          '<p class="note" style="margin-top:8px">自動車小売業の1,053円は令和7年12月14日からの額です。新潟労働局「新潟県最低賃金関係」に、令和8年度の特定最低賃金額は「改定されませんでしたので」新潟県最低賃金額の1,108円が適用されると書かれています。</p>\n',
      near=['新潟県', '山形県', '福島県', '群馬県', '長野県', '富山県', '東京都'],
      near_lead='新潟県と隣の県・東京都の令和8年度の最低賃金です。',
      near_note='新潟県は全国で24番目の額です。長野県とは9円・富山県とは11円・群馬県とは12円の差があり、福島県より14円・山形県より16円高い額です。',
      ex_month=180000,
      qa='<h3>新潟県の最低賃金はいつから1,108円ですか？</h3>\n<p>令和8年10月1日からです。前の年度の1,050円から58円上がりました。答申のあとに異議の申出があり、8月21日の審議会で改めて審議して決まりました。</p>\n'
         + '<h3>新車の販売店で働く人の最低賃金はいくらですか？</h3>\n<p>自動車（新車）小売業の特定最低賃金は1,053円ですが、10月1日からは新潟県最低賃金1,108円の方が高い額です。令和8年度は特定最低賃金の改正がないので、1,108円以上が必要です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/niigata-roudoukyoku/content/contents/R080828_2_pressrelease_check.pdf">新潟労働局「新潟県最低賃金を時間額1,108円に改正 令和8年10月1日から適用となります」</a>（令和8年8月28日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/niigata-roudoukyoku/hourei_seido_tetsuzuki/tingin_kanairoudou/chingin.html">新潟労働局「新潟県最低賃金関係」</a>（特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/niigata-roudoukyoku/content/contents/R071113_2_Z1.pdf">新潟労働局「新潟県特定最低賃金の改正について」</a>（令和7年11月14日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/niigata-roudoukyoku/hourei_seido_tetsuzuki/tingin_kanairoudou/r2saichin_giziroku.html">新潟地方最低賃金審議会 議事録</a></li>\n',
      rel=[('saitei-chingin-nagano', '長野県の最低賃金', '長野県は1,117円で、新潟県より9円高い額です。'),
           ('saitei-chingin-miyagi', '宮城県の最低賃金', '宮城県は1,098円で、新潟県より10円低い額です。')]),
 dict(name='長野県', slug='nagano', short='長野', word='長野県の最低賃金', kyoku='長野労働局', upd='2026年11月20日',
      mid='長野県の特定最低賃金は、いまはどれも長野県最低賃金より低い額です',
      intro='長野県の最低賃金が1,100円台になるのは初めてです。',
      tokutei='''<p>長野県には4つの特定最低賃金があります。10月2日からはどれも長野県最低賃金1,117円より低いので、業種にかかわらず1,117円以上が最低ラインです。</p>
<p class="cap">長野県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '令和8年度'], [
          [td('はん用・生産用・業務用機械器具・自動車・同附属品・船舶製造・修理業・舶用機関製造業', 'l'), td('1,105円'), td('1,161円を答申')],
          [td('計量器・医療用機械器具・光学機械器具・電子部品・電気機械器具・情報通信機械器具・時計・眼鏡製造業', 'l'), td('1,095円'), td('1,151円を答申')],
          [td('各種商品小売業', 'l'), td('950円'), td('改正しない')],
          [td('印刷・製版業', 'l'), td('850円'), td('―')]]) +
          '<p class="note" style="margin-top:8px">機械器具の2業種は、長野地方最低賃金審議会が10月20日と10月26日に答申しました。発効は12月25日の予定です。異議の申出と官報の公示を経て決まるので、この計算にはまだ含めていません。決まったらこの欄と計算を直します。</p>\n',
      near=['長野県', '新潟県', '群馬県', '埼玉県', '山梨県', '静岡県', '愛知県', '岐阜県', '富山県'],
      near_lead='長野県と隣の8県の令和8年度の最低賃金です。長野県は8つの県と接しています。',
      near_note='長野県は全国で19番目の額です。富山県とは2円・群馬県とは3円・岐阜県とは4円の差で、新潟県より9円・山梨県より4円高い額です。',
      ex_month=180000,
      qa='<h3>長野県はなぜ10月2日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、長野県は10月2日でした。10月1日までに働いた分は前の年度の1,061円で判定します。</p>\n'
         + '<h3>精密機械や電子部品の工場で働く人の最低賃金はいくらですか？</h3>\n<p>計量器・電子部品などの製造業の特定最低賃金はいま1,095円で、長野県最低賃金1,117円より低い額です。いまは1,117円以上が必要です。12月25日からの1,151円は答申の額で、決まったらこのページに入れます。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/nagano-roudoukyoku/content/contents/houdou8-32.pdf">長野労働局「長野県最低賃金が改正されます ～10月2日から時間額1,117円に～」</a>（令和8年9月2日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/nagano-roudoukyoku/content/contents/002765894.pdf">長野労働局「長野県最低賃金『時間額1117円』を答申」</a>（令和8年8月6日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/nagano-roudoukyoku/content/contents/houdou8-38.pdf">長野労働局「長野県はん用機械器具等製造業最低賃金『時間額1,161円』を答申」</a>（令和8年10月21日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/nagano-roudoukyoku/content/contents/houdou8-39.pdf">長野労働局「長野県計量器等製造業最低賃金『時間額1,151円』を答申」</a>（令和8年10月27日）</li>\n  <li><a href="https://saiteichingin.mhlw.go.jp/check/?p=19">厚生労働省「最低賃金早見表」長野県</a>（特定最低賃金のいまの額）</li>\n',
      rel=[('saitei-chingin-gunma', '群馬県の最低賃金', '群馬県は1,120円で、長野県より3円高い額です。'),
           ('saitei-chingin-niigata', '新潟県の最低賃金', '新潟県は1,108円で、長野県より9円低い額です。'),
           ('saitei-chingin-aichi', '愛知県の最低賃金', '愛知県は1,195円で、長野県との差は78円です。'),
           ('saitei-chingin-gifu', '岐阜県の最低賃金', '岐阜県は1,121円で、長野県より4円高い額です。')]),
 dict(name='岐阜県', slug='gifu', short='岐阜', word='岐阜県の最低賃金', kyoku='岐阜労働局', upd='2026年11月21日',
      mid='岐阜県の特定最低賃金は、いまはどれも岐阜県最低賃金より低い額です',
      intro='自動車と航空機の部品工場で働く人も、12月20日までは1,121円以上が最低ラインです。',
      tokutei='''<p>岐阜県には3つの特定最低賃金があります。いまはどの業種も岐阜県最低賃金1,121円より低いので、業種にかかわらず1,121円以上が最低ラインです。</p>
<p class="cap">岐阜県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '令和8年度'], [
          [td('自動車・同附属品製造業', 'l'), td('1,117円'), td('1,168円を答申')],
          [td('航空機・同附属品製造業', 'l'), td('1,049円'), td('1,125円を答申')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('965円'), td('確認できません')]]) +
          '<p class="note" style="margin-top:8px">自動車と航空機の2業種は、岐阜地方最低賃金審議会が令和8年10月21日の第499回審議会で答申しました。岐阜労働局のページには、令和8年12月21日に改正されると書かれています。改正決定の公示はまだ確かめていないので、この計算には含めていません。確かめたらこの欄と計算を直します。</p>\n',
      near=['岐阜県', '愛知県', '三重県', '滋賀県', '福井県', '石川県', '富山県', '長野県'],
      near_lead='岐阜県と隣の7県の令和8年度の最低賃金です。岐阜から名古屋に通う人は、愛知県内の事業場なら愛知県の額で判定します。',
      near_note='岐阜県は全国で16番目の額です。愛知県とは74円の差があり、三重県より22円・滋賀県より15円低い額です。富山県より2円・長野県より4円・石川県より8円・福井県より9円高い額です。',
      ex_month=180000,
      qa='<h3>岐阜県の最低賃金はいつから1,121円ですか？</h3>\n<p>令和8年10月1日からです。前の年度の1,065円は令和7年10月18日からだったので、1年たたずに56円上がりました。</p>\n'
         + '<h3>自動車の部品工場で働く人の最低賃金はいくらですか？</h3>\n<p>自動車・同附属品製造業の特定最低賃金はいま1,117円で、岐阜県最低賃金1,121円より4円低い額です。いまは1,121円以上が必要です。12月21日からの1,168円は答申の額で、決定を確かめたらこのページに入れます。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/gifu-roudoukyoku/roudoukyoku/gyoumu_naiyou/roudou_kijyun/chingin/sangyoubetu_itiran/sangyoubetu_itiran_00005.html">岐阜労働局「岐阜県の最低賃金」</a>（令和8年10月1日から1,121円・特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/gifu-roudoukyoku/content/contents/002779518.pdf">岐阜地方最低賃金審議会「令和8年度岐阜県最低賃金の改正決定に関する公益代表委員見解」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/gifu-roudoukyoku/content/contents/saichinshingikai_gijiroku_.html">岐阜労働局「岐阜地方最低賃金審議会 議事録」</a>（第499回・令和8年10月21日）</li>\n  <li><a href="https://www.pref.gifu.lg.jp/page/329757.html">岐阜県「最低賃金について知りたい。」</a></li>\n',
      rel=[('saitei-chingin-shiga', '滋賀県の最低賃金', '滋賀県は1,136円で、岐阜県より15円高い額です。'),
           ('saitei-chingin-aichi', '愛知県の最低賃金', '愛知県は1,195円で、岐阜県より74円高い額です。'),
           ('saitei-chingin-mie', '三重県の最低賃金', '三重県は1,143円で、岐阜県より22円高い額です。'),
           ('saitei-chingin-nagano', '長野県の最低賃金', '長野県は1,117円で、岐阜県より4円低い額です。')]),
 dict(name='岡山県', slug='okayama', short='岡山', word='岡山県の最低賃金', kyoku='岡山労働局', upd='2026年11月21日',
      ind=[['鉄鋼業', 1166, '2025年12月27日'],
           ['船舶製造・修理業・舶用機関製造業', 1159, '2026年1月1日']],
      mid='鉄鋼業と船舶製造・修理業は特定最低賃金と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼業と造船の事業場は、岡山県最低賃金より高い特定最低賃金がかかります。',
      tokutei='''<p>岡山県には7つの特定最低賃金があります。10月2日からは鉄鋼業の1,166円と船舶製造・修理業の1,159円が岡山県最低賃金1,104円より高い額です。ほかの5業種は1,104円で判定します。</p>
<p class="cap">岡山県の特定最低賃金・時間額</p>
''' + table(['業種', '特定最低<br>賃金', '10月2日から<br>判定する額'], [
          [td('鉄鋼業', 'l'), td('1,166円'), td('1,166円')],
          [td('船舶製造・修理業・舶用機関製造業', 'l'), td('1,159円'), td('1,159円')],
          [td('生産用機械器具製造業など（空気圧縮機・冷凍機・玉軸受・農業用機械・半導体製造装置・事務用機械器具など）', 'l'), td('1,103円'), td('1,104円')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,090円'), td('1,104円')],
          [td('自動車・同附属品製造業', 'l'), td('1,083円'), td('1,104円')],
          [td('耐火物製造業', 'l'), td('1,074円'), td('1,104円')],
          [td('各種商品小売業', 'l'), td('933円'), td('1,104円')]]) +
          '<p class="note" style="margin-top:8px">特定最低賃金の額は、岡山労働局「岡山県の最低賃金」の表によります（令和7年度に改正された額です）。令和8年度の改正は、労働局の表がまだ更新されていないので確認できません。改正が決まったらこの欄と計算を直します。生産用機械器具製造業などの1,103円は、岡山県最低賃金より1円低い額です。</p>\n',
      near=['岡山県', '兵庫県', '鳥取県', '広島県', '島根県', '香川県', '徳島県', '大阪府'],
      near_lead='岡山県と中国・四国・近畿の近くの府県の令和8年度の最低賃金です。県外の事業場で働く人は、その事業場がある都道府県の額で判定します。',
      near_note='岡山県は全国で26番目の額です。広島県とは37円・兵庫県とは68円の差があり、徳島県より1円・鳥取県より14円・香川県と島根県より12円高い額です。',
      ex_month=180000,
      qa='<h3>岡山県の最低賃金はいつから1,104円ですか？</h3>\n<p>令和8年10月2日からです。前の年度の1,047円は令和7年12月1日からだったので、10か月ほどで57円上がりました。</p>\n'
         + '<h3>倉敷の製鉄所や造船所で働く人の最低賃金はいくらですか？</h3>\n<p>鉄鋼業の特定最低賃金は1,166円で、船舶製造・修理業は1,159円です。どちらも岡山県最低賃金1,104円より高いので、特定最低賃金で判定します。下請けでも、事業場の業種が鉄鋼業や造船業なら同じです。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/okayama-roudoukyoku/hourei_seido_tetsuzuki/chinginkankei/saitin/saitin02.html">岡山労働局「岡山県の最低賃金」</a>（岡山県最低賃金と特定最低賃金の表）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okayama-roudoukyoku/newpage_502shimonn_00010.html">岡山労働局「岡山県最低賃金の答申」</a>（令和8年8月6日・1,104円）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okayama-roudoukyoku/content/contents/002355913.pdf">岡山労働局「岡山県最低賃金 1,104円を答申！」</a>（令和8年8月6日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/okayama-roudoukyoku/news_topics/2026houdou.html">岡山労働局「報道発表資料 2026年」</a>（9月2日 改正決定）</li>\n',
      rel=[('saitei-chingin-hiroshima', '広島県の最低賃金', '広島県は1,141円で、岡山県より37円高い額です。'),
           ('saitei-chingin-hyogo', '兵庫県の最低賃金', '兵庫県は1,172円で、岡山県より68円高い額です。')]), dict(name='栃木県', slug='tochigi', short='栃木', word='栃木県の最低賃金', kyoku='栃木労働局', upd='2026年11月22日',
      ind=[['塗料製造業', 1159, '2025年12月31日']],
      mid='塗料製造業は特定最低賃金1,159円と比べます。業種を選ぶと切り替わります',
      intro='塗料製造業の事業場は、栃木県最低賃金より高い特定最低賃金がかかります。',
      tokutei='''<p>栃木県には6つの特定最低賃金があります。10月1日からは塗料製造業の1,159円だけが栃木県最低賃金1,125円より高い額です。ほかの業種は1,125円で判定します。</p>
<p class="cap">栃木県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '令和8年度'], [
          [td('塗料製造業', 'l'), td('1,159円'), td('1,208円を答申')],
          [td('はん用機械器具・生産用機械器具・業務用機械器具製造業', 'l'), td('1,070円'), td('1,133円を答申')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,105円'), td('1,161円を答申')],
          [td('自動車・同附属品製造業', 'l'), td('1,114円'), td('1,167円を答申')],
          [td('計量器・測定器・分析機器・試験機・測量機械器具製造業など（医療用機械器具・光学機械器具・時計など）', 'l'), td('1,104円'), td('1,160円を答申')],
          [td('各種商品小売業', 'l'), td('確認できません'), td('改正なし')]]) +
          '<p class="note" style="margin-top:8px">いまの額は令和7年12月31日からの額です。令和8年度の額は栃木地方最低賃金審議会が令和8年10月30日に答申した額で、令和8年12月31日に発効する予定です。改正決定の公示はまだ確かめていないので、この計算には含めていません。各種商品小売業のいまの額は、労働局の資料では確認できません。</p>\n',
      near=['栃木県', '茨城県', '群馬県', '埼玉県', '福島県', '東京都', '千葉県'],
      near_lead='栃木県と隣の県・首都圏の令和8年度の最低賃金です。県外の事業場で働く人は、その事業場がある都道府県の額で判定します。',
      near_note='栃木県は全国で15番目の額です。茨城県より11円低く、群馬県より5円・福島県より31円高い額です。埼玉県とは71円の差があります。',
      ex_month=180000,
      qa='<h3>栃木県の最低賃金はいつから1,125円ですか？</h3>\n<p>令和8年10月1日からです。前の年度の1,068円も令和7年10月1日からだったので、1年で57円上がりました。</p>\n'
         + '<h3>塗料の工場で働く人の最低賃金はいくらですか？</h3>\n<p>塗料製造業の特定最低賃金は1,159円です。栃木県最低賃金1,125円より高いので、1,159円で判定します。12月31日からの1,208円は答申の額で、決定を確かめたらこのページに入れます。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/tochigi-roudoukyoku/newpage_01762.html">栃木労働局「令和8年10月1日から栃木県最低賃金が1,125円に改定されました！」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/tochigi-roudoukyoku/content/contents/002798058.pdf">栃木労働局「栃木県最低賃金を10月1日から1,125円に改正します」</a>（令和8年9月1日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/tochigi-roudoukyoku/content/contents/002877186.pdf">栃木労働局「令和8年度 栃木県特定最低賃金の改定を答申」</a>（令和8年10月30日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/tochigi-roudoukyoku/content/contents/002798064.pdf">栃木労働局「栃木県最低賃金」（掲示用）</a>（塗料製造業の特定最低賃金）</li>\n',
      rel=[('saitei-chingin-ibaraki', '茨城県の最低賃金', '茨城県は1,136円で、栃木県より11円高い額です。'),
           ('saitei-chingin-gunma', '群馬県の最低賃金', '群馬県は1,120円で、栃木県より5円低い額です。'),
           ('saitei-chingin-saitama', '埼玉県の最低賃金', '埼玉県は1,196円で、栃木県より71円高い額です。')]),
 dict(name='群馬県', slug='gunma', short='群馬', word='群馬県の最低賃金', kyoku='群馬労働局', upd='2026年11月22日',
      ind=[['製鋼・製鋼圧延業・鉄素形材製造業', 1131, '2026年1月1日']],
      mid='製鋼・鉄素形材製造業は特定最低賃金1,131円と比べます。業種を選ぶと切り替わります',
      intro='製鋼と鉄素形材の事業場は、群馬県最低賃金より高い特定最低賃金がかかります。',
      tokutei='''<p>群馬県には4つの特定最低賃金があります。10月3日からは製鋼・鉄素形材製造業の1,131円が群馬県最低賃金1,120円より高い額です。ほかの3業種は1,120円で、群馬県最低賃金と同じ額です。</p>
<p class="cap">群馬県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '令和8年度'], [
          [td('製鋼・製鋼圧延業・鉄素形材製造業', 'l'), td('1,131円'), td('1,186円を答申')],
          [td('ポンプ・圧縮機器・一般産業用機械・金属加工機械・事務用機械器具などの製造業', 'l'), td('1,120円'), td('1,175円を答申')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,120円'), td('1,175円を答申')],
          [td('輸送用機械器具製造業', 'l'), td('1,120円'), td('1,175円を答申')]]) +
          '<p class="note" style="margin-top:8px">いまの額は令和8年1月1日からの額です。令和8年度の額は群馬地方最低賃金審議会が10月27日と28日に答申した額です。群馬労働局の資料には、11月30日ごろに決定して12月30日ごろに発効する見込みと書かれています。改正決定の公示はまだ確かめていないので、この計算には含めていません。</p>\n',
      near=['群馬県', '栃木県', '埼玉県', '長野県', '新潟県', '茨城県', '東京都'],
      near_lead='群馬県と隣の県・首都圏の令和8年度の最低賃金です。県外の事業場で働く人は、その事業場がある都道府県の額で判定します。',
      near_note='群馬県は全国で17番目の額です。栃木県より5円・茨城県より16円低く、長野県より3円・新潟県より12円高い額です。埼玉県とは76円の差があります。',
      ex_month=180000,
      qa='<h3>群馬県の最低賃金はいつから1,120円ですか？</h3>\n<p>令和8年10月3日からです。前の年度の1,063円は令和8年3月1日からだったので、7か月ほどで57円上がりました。</p>\n'
         + '<h3>自動車の工場で働く人の最低賃金はいくらですか？</h3>\n<p>輸送用機械器具製造業の特定最低賃金は1,120円で、群馬県最低賃金と同じ額です。12月30日ごろからの1,175円は答申の額で、決定を確かめたらこのページに入れます。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/gunma-roudoukyoku/content/contents/002801040.pdf">群馬労働局「群馬県最低賃金を改正します ～10月3日から時間額1,120円に～」</a>（令和8年9月3日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/gunma-roudoukyoku/content/contents/002872651.pdf">群馬労働局「令和8年度群馬県特定最低賃金の改正を答申」</a>（令和8年10月29日）</li>\n  <li><a href="https://www.pref.gunma.jp/06/g2210045.html">群馬県「群馬県最低賃金が改正されました」</a>（特定最低賃金のいまの額）</li>\n',
      rel=[('saitei-chingin-tochigi', '栃木県の最低賃金', '栃木県は1,125円で、群馬県より5円高い額です。'),
           ('saitei-chingin-saitama', '埼玉県の最低賃金', '埼玉県は1,196円で、群馬県より76円高い額です。'),
           ('saitei-chingin-nagano', '長野県の最低賃金', '長野県は1,117円で、群馬県より3円低い額です。')]),
 dict(name='滋賀県', slug='shiga', short='滋賀', word='滋賀県の最低賃金', kyoku='滋賀労働局', upd='2026年11月22日',
      mid='滋賀県の特定最低賃金は、10月3日からはどれも滋賀県最低賃金より低い額です',
      intro='滋賀県の4つの特定最低賃金は滋賀県最低賃金1,136円より低いので、業種にかかわらず1,136円以上が最低ラインです。',
      tokutei='''<p>滋賀県には4つの特定最低賃金があります。どれも令和7年12月28日に改正された額で、10月3日からは滋賀県最低賃金1,136円より低くなりました。業種にかかわらず1,136円以上が最低ラインです。</p>
<p class="cap">滋賀県の特定最低賃金・時間額</p>
''' + table(['業種', '特定最低<br>賃金', '10月3日から<br>判定する額'], [
          [td('ガラス・セメント・衛生陶器・炭素・黒鉛製品・炭素繊維製造業', 'l'), td('1,099円'), td('1,136円')],
          [td('はん用機械器具・生産用機械器具・業務用機械器具製造業', 'l'), td('1,114円'), td('1,136円')],
          [td('計量器・光学機械器具・電子部品・電気機械器具・情報通信機械器具製造業', 'l'), td('1,105円'), td('1,136円')],
          [td('自動車・同附属品製造業', 'l'), td('1,115円'), td('1,136円')]]) +
          '<p class="note" style="margin-top:8px">特定最低賃金の額は、滋賀労働局の令和7年11月28日の発表によります。令和8年度の改正は、読んだ労働局の資料では確認できません。改正が決まったらこの欄を直します。</p>\n',
      near=['滋賀県', '京都府', '岐阜県', '三重県', '福井県', '大阪府', '奈良県'],
      near_lead='滋賀県と隣の府県の令和8年度の最低賃金です。京都や大阪の事業場に通う人は、その事業場がある府の額で判定します。',
      near_note='滋賀県は茨城県と並んで全国で12番目の額です。京都府より44円・三重県より7円低く、岐阜県より15円・福井県より24円・奈良県より29円高い額です。',
      ex_month=180000,
      qa='<h3>滋賀県の最低賃金はいつから1,136円ですか？</h3>\n<p>令和8年10月3日からです。前の年度の1,080円は令和7年10月5日からだったので、1年で56円上がりました。</p>\n'
         + '<h3>自動車部品や電子部品の工場で働く人の最低賃金はいくらですか？</h3>\n<p>特定最低賃金は1,115円と1,105円ですが、どちらも滋賀県最低賃金1,136円より低い額です。10月3日からは1,136円以上が必要です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/shiga-roudoukyoku/content/contents/002803443.pdf">滋賀労働局「滋賀県最低賃金の改正決定について」</a>（令和8年9月3日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/shiga-roudoukyoku/news_topics/newpage_071128_0001_00001.html">滋賀労働局「滋賀県特定（産業別）最低賃金の改正決定について」</a>（令和7年11月28日）</li>\n  <li><a href="https://jsite.mhlw.go.jp/shiga-roudoukyoku/content/contents/002473432.pdf">滋賀労働局「滋賀県特定（産業別）最低賃金の改正決定について」報道発表資料</a>（4業種の額）</li>\n',
      rel=[('saitei-chingin-kyoto', '京都府の最低賃金', '京都府は1,180円で、滋賀県より44円高い額です。'),
           ('saitei-chingin-gifu', '岐阜県の最低賃金', '岐阜県は1,121円で、滋賀県より15円低い額です。'),
           ('saitei-chingin-mie', '三重県の最低賃金', '三重県は1,143円で、滋賀県より7円高い額です。')]),
 dict(name='山口県', slug='yamaguchi', short='山口', word='山口県の最低賃金', kyoku='山口労働局', upd='2026年11月22日',
      ind=[['鉄鋼業・非鉄金属製錬・精製業・非鉄金属・同合金圧延業・非鉄金属素形材製造業', 1180, '2025年12月15日'],
           ['輸送用機械器具製造業', 1141, '2025年12月15日']],
      mid='鉄鋼・非鉄金属と輸送用機械器具製造業は特定最低賃金と比べます。業種を選ぶと切り替わります',
      intro='鉄鋼・非鉄金属と輸送用機械器具の事業場は、山口県最低賃金より高い特定最低賃金がかかります。',
      tokutei='''<p>山口県には4つの特定最低賃金があります。鉄鋼業・非鉄金属の1,180円と輸送用機械器具製造業の1,141円は、山口県最低賃金1,101円より高い額です。電子部品などと百貨店・総合スーパーの2業種は1,101円で判定します。</p>
<p class="cap">山口県の特定最低賃金・時間額</p>
''' + table(['業種', 'いまの額', '令和8年度'], [
          [td('鉄鋼業・非鉄金属製錬・精製業・非鉄金属・同合金圧延業・非鉄金属素形材製造業', 'l'), td('1,180円'), td('12月15日から1,238円')],
          [td('輸送用機械器具製造業', 'l'), td('1,141円'), td('12月15日から1,205円')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,032円'), td('改正なし')],
          [td('百貨店・総合スーパーマーケット', 'l'), td('1,000円'), td('改正なし')]]) +
          '<p class="note" style="margin-top:8px">いまの額のうち鉄鋼業などと輸送用機械器具製造業は令和7年12月15日から、ほかの2業種は令和6年12月15日からの額です。山口労働局のページには、2業種が令和8年12月15日から1,238円と1,205円になると書かれています。改正決定の公示はまだ確かめていないので、この計算には含めていません。</p>\n',
      near=['山口県', '広島県', '島根県', '福岡県', '岡山県', '大分県'],
      near_lead='山口県と中国・九州の近くの県の令和8年度の最低賃金です。県外の事業場で働く人は、その事業場がある都道府県の額で判定します。',
      near_note='山口県は和歌山県と並んで全国で28番目の額です。広島県より40円・福岡県より13円・岡山県より3円低く、島根県より9円・大分県より5円高い額です。',
      ex_month=180000,
      qa='<h3>山口県の最低賃金はいつから1,101円ですか？</h3>\n<p>令和8年10月8日からです。前の年度の1,043円から58円上がりました。</p>\n'
         + '<h3>製鉄所や造船所で働く人の最低賃金はいくらですか？</h3>\n<p>鉄鋼業などの特定最低賃金は1,180円で、造船や自動車の輸送用機械器具製造業は1,141円です。どちらも山口県最低賃金1,101円より高いので、特定最低賃金で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/yamaguchi-roudoukyoku/hourei_seido_tetsuzuki/chingin.html">山口労働局「賃金関係」</a>（山口県最低賃金と特定最低賃金）</li>\n  <li><a href="https://jsite.mhlw.go.jp/yamaguchi-roudoukyoku/content/contents/002883845.pdf">山口労働局「山口県の最低賃金（地域別最低賃金・特定最低賃金）」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/yamaguchi-roudoukyoku/content/contents/002810392.pdf">山口労働局「山口県の最低賃金」リーフレット</a>（令和8年9月）</li>\n',
      rel=[('saitei-chingin-hiroshima', '広島県の最低賃金', '広島県は1,141円で、山口県より40円高い額です。'),
           ('saitei-chingin-fukuoka', '福岡県の最低賃金', '福岡県は1,114円で、山口県より13円高い額です。'),
           ('saitei-chingin-okayama', '岡山県の最低賃金', '岡山県は1,104円で、山口県より3円高い額です。')]),
 dict(name='福島県', slug='fukushima', short='福島', word='福島の最低賃金', kyoku='福島労働局', upd='2026年11月26日',
      ind=[['自動車小売業（二輪を除く）', 1098, '2026年1月8日']],
      mid='自動車小売業（二輪を除く）は1,098円と比べます。ほかの業種は1,094円です',
      intro='自動車小売業（二輪を除く）だけは1,098円がかかります。',
      tokutei='''<p>福島県の特定最低賃金で、福島県最低賃金1,094円より高いのは自動車小売業（二輪を除く）の1,098円です。令和8年1月8日からこの額です。</p>
<p>非鉄金属製造業・輸送用機械器具製造業・計量器などの製造業・電子部品などの製造業は、地域別最低賃金を適用します。令和8年10月16日からは1,094円です。</p>
<p class="cap">福島県の特定最低賃金・時間額</p>
''' + table(['業種', '時間額', 'いつから'], [
          [td('自動車小売業（二輪を除く）', 'l'), td('1,098円'), td('2026年1月8日')],
          [td('非鉄金属製造業', 'l'), td('地域別を適用'), td('2026年10月16日から1,094円')],
          [td('輸送用機械器具製造業', 'l'), td('地域別を適用'), td('2026年10月16日から1,094円')],
          [td('計量器・測定器・時計・眼鏡などの製造業', 'l'), td('地域別を適用'), td('2026年10月16日から1,094円')],
          [td('電子部品・電気機械器具・情報通信機械器具製造業', 'l'), td('地域別を適用'), td('2026年10月16日から1,094円')]]) +
          '<p class="note" style="margin-top:8px">自動車小売業以外は令和7年度の改正がなく、令和8年10月16日からは福島県最低賃金1,094円です。新しい改正額は発表があり次第この表を直します。18歳未満や65歳以上の人などは特定最低賃金から除かれ、地域別で判定します。</p>\n',
      near=['福島県', '宮城県', '山形県', '茨城県', '栃木県', '新潟県'],
      near_lead='福島県と隣の県の令和8年度の最低賃金です。県外の事業場で働く人は、その事業場がある県の額で判定します。',
      near_note='福島県は全国で33番目の額です。宮城県より4円・新潟県より14円・栃木県より31円・茨城県より42円低く、山形県より2円高い額です。',
      ex_month=180000,
      qa='<h3>福島県の自動車販売の最低賃金はいくらですか？</h3>\n<p>二輪を除く自動車小売業は時給1,098円です。令和8年1月8日からで、福島県最低賃金より4円高い額です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/fukushima-roudoukyoku/jirei_toukei/chingin_kanairoudou.html">福島労働局「賃金・家内労働」</a>（福島県最低賃金と自動車小売業の発効日）</li>\n  <li><a href="https://www.pref.fukushima.lg.jp/sec/32011c/saiteichingin.html">福島県「最低賃金が令和8年10月16日から変わります」</a>（2026年10月6日更新）</li>\n  <li><a href="https://saiteichingin.mhlw.go.jp/check/?p=6">厚生労働省「最低賃金の比較チェック」福島県</a>（自動車小売業 1,098円・2026年1月8日）</li>\n',
      rel=[('saitei-chingin-miyagi', '宮城県の最低賃金', '宮城県は1,098円で、福島県より4円高い額です。'),
           ('saitei-chingin-niigata', '新潟県の最低賃金', '新潟県は1,108円で、福島県より14円高い額です。'),
           ('saitei-chingin-tochigi', '栃木県の最低賃金', '栃木県は1,125円で、福島県より31円高い額です。')]),
 dict(name='岩手県', slug='iwate', short='岩手', word='岩手の最低賃金', kyoku='岩手労働局', upd='2026年11月26日',
      ind=[['鉄鋼業・金属線製品・その他の金属製品製造業', 1072, '2026年1月15日'],
           ['光学機械器具・レンズ・時計製造業', 1052, '2026年2月1日'],
           ['電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 1039, '2026年1月15日'],
           ['自動車小売業', 1068, '2026年1月15日']],
      mid='12月1日より前は特定最低賃金のほうが高い業種を選べます。12月1日からは1,090円がすべての業種を上回ります',
      intro='12月1日からは岩手県最低賃金1,090円が、特定最低賃金のどの業種よりも高い額になります。',
      tokutei='''<p>岩手県の特定最低賃金は、どれも12月1日からの地域別最低賃金1,090円より低い額です。2026年11月30日までに働いた分は、改定前の1,031円より高い業種だけ特定最低賃金で判定します。</p>
<p class="cap">岩手県の特定最低賃金・時間額</p>
''' + table(['業種', '時間額', 'いつから'], [
          [td('鉄鋼業・金属線製品・その他の金属製品製造業', 'l'), td('1,072円'), td('2026年1月15日')],
          [td('光学機械器具・レンズ・時計製造業', 'l'), td('1,052円'), td('2026年2月1日')],
          [td('電子部品・デバイス・電子回路・電気機械器具・情報通信機械器具製造業', 'l'), td('1,039円'), td('2026年1月15日')],
          [td('自動車小売業', 'l'), td('1,068円'), td('2026年1月15日')],
          [td('百貨店・総合スーパー', 'l'), td('1,031円'), td('地域別を適用')],
          [td('各種商品小売業', 'l'), td('1,031円'), td('地域別を適用')]]) +
          '<p class="note" style="margin-top:8px">12月1日からは岩手県最低賃金1,090円が6業種のすべてを上回ります。次の改正までは1,090円です。岩手労働局は次の改正の対象を鉄鋼業・光学機械器具・自動車小売業としています。</p>\n',
      near=['岩手県', '青森県', '秋田県', '宮城県', '山形県', '福島県'],
      near_lead='岩手県は12月1日からの引上げです。隣の県の令和8年度の最低賃金です。',
      near_note='岩手県は青森県・秋田県・鳥取県・鹿児島県と同じ1,090円です。宮城県より8円・山形県より2円低い額です。',
      ex_month=180000,
      qa='<h3>岩手県はなぜ12月1日からですか？</h3>\n<p>発効日は都道府県ごとに決まり、岩手県は12月1日です。11月30日までに働いた分は前の年度の1,031円で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/iwate-roudoukyoku/roudoukyoku/gyoumu_naiyou/kijunbu/chingin.html">岩手労働局「賃金」</a>（12月1日から1,090円・特定最低賃金の額）</li>\n  <li><a href="https://jsite.mhlw.go.jp/iwate-roudoukyoku/content/contents/002555523.pdf">岩手労働局「岩手県特定（産業別）最低賃金が改正されました」</a>（令和8年2月）</li>\n',
      rel=[('saitei-chingin-miyagi', '宮城県の最低賃金', '宮城県は1,098円で、岩手県の12月1日からの額より8円高い額です。'),
           ('saitei-chingin-hokkaido', '北海道の最低賃金', '北海道は1,131円で、岩手県の12月1日からの額より41円高い額です。')]),
 dict(name='奈良県', slug='nara', short='奈良', word='奈良の最低賃金', kyoku='奈良労働局', upd='2026年11月26日',
      mid='3業種の特定最低賃金は奈良県最低賃金と同じ1,107円です',
      intro='特定最低賃金の3業種も同じ1,107円です。',
      tokutei='''<p>奈良県の特定最低賃金は3業種あり、どれも令和8年10月4日から1,107円です。奈良県最低賃金と同じ額なので、業種を分けずに1,107円で判定します。</p>
<p class="cap">奈良県の特定最低賃金・時間額</p>
''' + table(['業種', '時間額', 'いつから'], [
          [td('はん用・生産用・業務用機械器具製造業', 'l'), td('1,107円'), td('2026年10月4日')],
          [td('電子部品・電気機械器具製造業', 'l'), td('1,107円'), td('2026年10月4日')],
          [td('自動車小売業', 'l'), td('1,107円'), td('2026年10月4日')]]) +
          '<p class="note" style="margin-top:8px">3業種とも奈良県最低賃金と同じ額です。18歳未満や65歳以上の人などは特定最低賃金から除かれ、同じ1,107円の地域別で判定します。</p>\n',
      near=['奈良県', '大阪府', '京都府', '和歌山県', '三重県', '滋賀県'],
      near_lead='奈良県と隣の府県の令和8年度の最低賃金です。大阪や京都の事業場に通う人は、その事業場がある府の額で判定します。',
      near_note='奈良県は全国で25番目の額です。大阪府より124円・京都府より73円・三重県より36円低く、和歌山県より6円高い額です。',
      ex_month=180000,
      qa='<h3>奈良県の工場の特定最低賃金は地域別と違いますか？</h3>\n<p>はん用機械・電子部品・自動車小売の3業種は、令和8年10月4日から1,107円です。奈良県最低賃金と同じ額です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/nara-roudoukyoku/content/contents/002806416.pdf">奈良労働局「奈良県最低賃金 時間額1,107円」</a></li>\n  <li><a href="https://jsite.mhlw.go.jp/nara-roudoukyoku/newpage_01185.html">奈良労働局「令和8年度 奈良県最低賃金の改正が正式に決定しました」</a>（令和8年10月4日から）</li>\n',
      rel=[('saitei-chingin-osaka', '大阪府の最低賃金', '大阪府は1,231円で、奈良県より124円高い額です。'),
           ('saitei-chingin-kyoto', '京都府の最低賃金', '京都府は1,180円で、奈良県より73円高い額です。'),
           ('saitei-chingin-mie', '三重県の最低賃金', '三重県は1,143円で、奈良県より36円高い額です。')]),
 dict(name='長崎県', slug='nagasaki', short='長崎', word='長崎の最低賃金', kyoku='長崎労働局', upd='2026年11月26日',
      mid='特定最低賃金は審議中なので、長崎県最低賃金1,087円で判定します',
      intro='特定最低賃金3業種の令和8年度の改正は審議中です。決まった額ではないので、計算は1,087円でしています。',
      tokutei='''<p>はん用・生産用機械と電子部品・電気機械・情報通信機械と船舶製造・修理・舶用機関の3業種は、令和7年度は改正がありませんでした。令和8年度は長崎労働局の専門部会で審議中です。審議中の案はこの計算に入れていません。</p>
<p>長崎労働局は、改正されない場合は令和8年11月2日以降も地域別の1,087円を適用するとしています。必要性を審議する審議会は2026年11月30日です。</p>
<p class="cap">長崎県の特定最低賃金</p>
''' + table(['業種', '令和8年度', 'いまの判定'], [
          [td('はん用・生産用機械器具製造業', 'l'), td('審議中'), td('1,087円')],
          [td('電子部品・電気機械器具・情報通信機械器具製造業', 'l'), td('審議中'), td('1,087円')],
          [td('船舶製造・修理・舶用機関製造業', 'l'), td('審議中'), td('1,087円')]]) +
          '<p class="note" style="margin-top:8px">審議中の額は計算に入れていません。決まったらこの表と計算を直します。</p>\n',
      near=['長崎県', '佐賀県', '福岡県', '熊本県', '大分県', '鹿児島県'],
      near_lead='長崎県と九州の県の令和8年度の最低賃金です。熊本県は12月1日から1,092円です。',
      near_note='長崎県は全国で44番目の額です。福岡県より27円・佐賀県より8円・大分県より9円・熊本県より5円・鹿児島県より3円低い額です。',
      ex_month=180000,
      qa='<h3>長崎県の造船の最低賃金はいくらですか？</h3>\n<p>船舶製造・修理と舶用機関の特定最低賃金は、令和8年度はまだ審議中です。決まるまでは長崎県最低賃金の1,087円で判定します。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/nagasaki-roudoukyoku/hourei_seido_tetsuzuki/saitei_tingin/hourei_seido/saitin-new.html">長崎労働局「長崎県の最低賃金は？」</a>（地域別1,087円・特定は審議中）</li>\n  <li><a href="https://jsite.mhlw.go.jp/nagasaki-roudoukyoku/content/contents/press-26092902.pdf">長崎労働局「長崎県最低賃金を時間額1,087円に引上げ」</a>（令和8年9月29日公示・11月2日発効）</li>\n  <li><a href="https://jsite.mhlw.go.jp/nagasaki-roudoukyoku/content/contents/bocho-kaisai-26112003.pdf">長崎労働局「令和8年度第5回長崎地方最低賃金審議会の開催について」</a>（2026年11月30日・特定最低賃金の必要性）</li>\n',
      rel=[('saitei-chingin-fukuoka', '福岡県の最低賃金', '福岡県は1,114円で、長崎県より27円高い額です。'),
           ('saitei-chingin-kumamoto', '熊本県の最低賃金', '熊本県は12月1日から1,092円で、長崎県より5円高い額です。'),
           ('saitei-chingin-kagoshima', '鹿児島県の最低賃金', '鹿児島県は1,090円で、長崎県より3円高い額です。')]),
 dict(name='宮崎県', slug='miyazaki', short='宮崎', word='宮崎の最低賃金', kyoku='宮崎労働局', upd='2026年11月26日',
      mid='特定最低賃金4業種は本年度の改正がなく、宮崎県最低賃金1,085円を適用します',
      intro='宮崎県は全国で一番低い額です。特定最低賃金は本年度の改正がありません。',
      tokutei='''<p>部分肉・冷凍肉・乳製品と電子部品・電気機械・情報通信機械と各種商品小売業と自動車（新車）小売業は、本年度は改正がありません。宮崎労働局は、これらの業種に宮崎県最低賃金1,085円を適用するとしています。</p>
<p class="cap">宮崎県の特定最低賃金・時間額</p>
''' + table(['業種', '時間額', 'いつから'], [
          [td('部分肉・冷凍肉・乳製品製造業', 'l'), td('1,085円'), td('2026年10月24日')],
          [td('電子部品・電気機械器具・情報通信機械器具製造業', 'l'), td('1,085円'), td('2026年10月24日')],
          [td('各種商品小売業', 'l'), td('1,085円'), td('2026年10月24日')],
          [td('自動車（新車）小売業', 'l'), td('1,085円'), td('2026年10月24日')]]) +
          '<p class="note" style="margin-top:8px">4業種とも改正の必要ありとは結論が出ず、宮崎県最低賃金を適用します。計算の業種選択は分けていません。</p>\n',
      near=['宮崎県', '鹿児島県', '大分県', '熊本県', '沖縄県', '長崎県'],
      near_lead='宮崎県と九州・沖縄の令和8年度の最低賃金です。沖縄県は12月2日から1,086円です。',
      near_note='宮崎県は全国で一番低い額です。鹿児島県より5円・大分県より11円・熊本県より7円・沖縄県より1円・長崎県より2円低い額です。',
      ex_month=180000,
      qa='<h3>宮崎県は全国で一番低いですか？</h3>\n<p>令和8年度の地域別最低賃金では、宮崎県の1,085円が一番低い額です。隣の沖縄県は12月2日から1,086円です。</p>\n',
      src='  <li><a href="https://jsite.mhlw.go.jp/miyazaki-roudoukyoku/jirei_toukei/chingin_kanairoudou/tingin.html">宮崎労働局「宮崎県の最低賃金」</a>（1,085円・特定は本年度の改定なし）</li>\n  <li><a href="https://www.pref.miyazaki.lg.jp/rodoseisaku/shigoto/rodo/20170104103944.html">宮崎県「宮崎県最低賃金が改正されます」</a>（2026年10月9日更新）</li>\n',
      rel=[('saitei-chingin-kagoshima', '鹿児島県の最低賃金', '鹿児島県は1,090円で、宮崎県より5円高い額です。'),
           ('saitei-chingin-okinawa', '沖縄県の最低賃金', '沖縄県は12月2日から1,086円で、宮崎県より1円高い額です。'),
           ('saitei-chingin-kumamoto', '熊本県の最低賃金', '熊本県は12月1日から1,092円で、宮崎県より7円高い額です。')]),
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
        '沖縄県': 'okinawa', '熊本県': 'kumamoto', '茨城県': 'ibaraki', '広島県': 'hiroshima', '鹿児島県': 'kagoshima',
        '三重県': 'mie', '静岡県': 'shizuoka', '宮城県': 'miyagi', '新潟県': 'niigata', '長野県': 'nagano', '岐阜県': 'gifu', '岡山県': 'okayama', '栃木県': 'tochigi', '群馬県': 'gunma', '滋賀県': 'shiga', '山口県': 'yamaguchi',
        '福島県': 'fukushima', '岩手県': 'iwate', '奈良県': 'nara', '長崎県': 'nagasaki', '宮崎県': 'miyazaki'}

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
  var x=PR[+$("pref").value],now=new Date(),eff=new Date("2026-"+("0"+x[3]).slice(-2)+"-"+("0"+x[4]).slice(-2)+"T00:00:00+09:00"),pre=now<eff;
  var M=pre?x[2]:x[1],h=base/div,ok=h>=M-1e-9,gap=Math.max(0,M-h);
  $("o-h").innerHTML=f1(h)+"<i>円</i>";
  $("o-hn").textContent=k===0?"含めない手当を除く":k===1?"日給÷"+div+"時間":"月給÷"+f1(div)+"時間";
  $("o-m").innerHTML=f(M)+"<i>円</i>";
  $("o-mn").textContent=pre?x[0]+"・改定前の額・2026年"+x[3]+"月"+x[4]+"日から"+f(x[1])+"円":x[0]+"・2026年"+x[3]+"月"+x[4]+"日から";
  var vd=$("vd");vd.className="vd"+(ok?" no":"");
  if(ok){$("o-vd").textContent="満たしています";$("o-vds").textContent=(h-M<0.05)?"時給に直すと"+f1(h)+"円で、"+x[0]+"の最低賃金"+f(M)+"円と同じ額です":"時給に直すと"+f1(h)+"円で、"+x[0]+"の最低賃金"+f(M)+"円より"+f1(h-M)+"円高い額です";}
  else{var per=k===0?"":(k===1?"1日あたり":"1か月あたり")+f(Math.ceil(gap*div-1e-9))+"円足りません。";
   $("o-vd").textContent="下回っています";$("o-vds").textContent=x[0]+"の最低賃金"+f(M)+"円より時給あたり"+f1(gap)+"円足りません。"+per+"差額を払う必要があります";}
  $("o-old").textContent=pre?"まだ発効前です。2026年"+x[3]+"月"+x[4]+"日からの"+f(x[1])+"円と比べると"+(h>=x[1]-1e-9?"満たしています":"下回っています（時給あたり"+f1(x[1]-h)+"円）"):"改定前の"+f(x[2])+"円から"+(M-x[2])+"円上がりました";
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
    desc = '令和8年度の最低賃金は全国加重平均で時給1,177円です。47都道府県の最低賃金を高い順のランキング・発効日・年間休日120日の月給の目安の一覧にしました。都道府県と時給・日給・月給を入力すると最低賃金を下回っていないかが分かります。'
    upd = '更新日：2026年11月20日（厚生労働省 令和8年度地域別最低賃金全国一覧）'
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
  <li><a href="#futan">最低賃金で人を雇うときの会社の負担</a></li>
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
    sec1 = ('<h2 id="rank">47都道府県の最低賃金の一覧（高い順）</h2>\n<p>令和8年度の地域別最低賃金を高い順に並べました。月給は年間休日120日・1日8時間で最低賃金を満たす額です。都道府県の名前を選ぶと、その県の特定最低賃金や近くの県との比較を見られます。</p>\n<p class="cap">令和8年度・時間額（円）</p>\n'
            + table(['順位', '都道府県', '令和8<br>年度', '令和7<br>年度', '上げ<br>幅', '発効<br>日', '月給の<br>目安'], rows)
            + '<p class="note" style="margin-top:8px">発効日は厚生労働省「令和8年度地域別最低賃金全国一覧」の日付です。月給の目安は円未満を切り上げた額です。全国加重平均は1,177円（前の年度1,121円）です。</p>\n')
    # いつから
    by = {}
    for p in P:
        by.setdefault((p['mo'], p['da']), []).append(p['name'])
    rows = []
    for (mo, da) in sorted(by):
        rows.append([td('%d月%d日' % (mo, da), 'c'), td('・'.join(by[(mo, da)]), 'l'), td('%d' % len(by[(mo, da)]), 'c')])
    late = [p['name'] for p in P if (2026, p['mo'], p['da']) > TODAY]
    sec2 = ('<h2 id="itsu">最低賃金はいつから上がるか（発効日の順）</h2>\n<p>最低賃金は、都道府県ごとに決まった発効日から新しい額になります。発効日の前日までに働いた分は、前の年度の額で判定します。%s</p>\n' % (('%d年%d月%d日の時点で、%sはまだ発効前です。' % (TODAY + ('・'.join(late),))) if late else '')
            + table(['発効日', '都道府県', '数'], rows)
            + '<p class="note" style="margin-top:8px">10月1日に変わったのは%d都道府県です。一番遅いのは沖縄県の12月2日です。</p>\n' % len(by[(10, 1)]))
    # 月給
    rows = []
    for nm in ['東京都', '神奈川県', '大阪府', '埼玉県', '愛知県', '北海道', '福岡県', '宮崎県']:
        m = D[nm]['new']
        rows.append([td(nm, 'l')] + [td(c(mon(m, h))) for h in (125, 120, 110, 105)])
    sec3 = ('<h2 id="getsu">月給にすると最低いくらか</h2>\n<p>月給の人は、月給を1か月の平均の労働時間で割って最低賃金と比べます。主な都道府県について、年間休日ごとに最低賃金を満たす月給を計算しました。</p>\n<p class="cap">1日8時間・含めない手当を除いた月給（円）</p>\n'
            + table(['都道府県', '休日<br>125日', '休日<br>120日', '休日<br>110日', '休日<br>105日'], rows)
            + '<p class="note" style="margin-top:8px">1か月の平均時間は（365日−年間休日）×8時間÷12で出しています。ほかの都道府県は上の計算に月給と年間休日を入力すると判定できます。</p>\n')
    sm = 200000
    sec5 = ('<h2 id="kanzan">日給・月給を時給に直すやり方</h2>\n<h3>日給</h3>\n<p>日給を1日の決まった労働時間で割ります。日給9,600円で1日8時間なら時給1,200円です。東京都・神奈川県・大阪府では下回り、それ以外の道府県では満たしています。</p>\n'
            '<h3>月給</h3>\n<p>月給を1か月の平均の労働時間で割ります。年間休日120日・1日8時間なら1か月の平均は163.3時間で、月給20万円は時給%s円です。</p>\n'
            '<h3>月給20万円で足りる都道府県</h3>\n<p>年間休日120日・1日8時間なら、月給20万円で最低賃金を満たすのは%d道府県です。東京都・神奈川県・大阪府の3都府県では下回ります。</p>\n') % (f1(sm / hrs(120)), sum(1 for p in P if sm / hrs(120) >= p['new']))
    rel_items = [('saitei-chingin-tokyo', '東京の最低賃金', '東京都は1,280円で全国で一番高い額です。'),
                 ('saitei-chingin-osaka', '大阪の最低賃金', '大阪府は1,231円で、特定最低賃金が12月から上がります。'),
                 ('saitei-chingin-kanagawa', '神奈川県の最低賃金', '神奈川県は1,279円で、東京都との差は1円です。'),
                 ('saitei-chingin-aichi', '愛知県の最低賃金', '愛知県は1,195円で、輸送用機械器具製造業の特定最低賃金が12月16日から1,208円に上がります。'),
                 ('saitei-chingin-hokkaido', '北海道の最低賃金', '北海道は1,131円で、鉄鋼業など4業種に特定最低賃金があります。')] + REL_COMMON[1:7] + [REL_COMMON[8]]
    sec6 = rel(slug, rel_items)
    qa = ('<h2 id="qa">最低賃金でよく聞かれること</h2>\n'
          '<h3>2026年の最低賃金はいつから上がりますか？</h3>\n<p>都道府県ごとに違い、2026年10月1日から12月2日までに順に上がります。東京都・神奈川県・大阪府・愛知県などは10月1日からです。</p>\n'
          '<h3>最低賃金が一番高いのはどこですか？</h3>\n<p>東京都の時給1,280円です。2番目は神奈川県の1,279円・3番目は大阪府の1,231円です。</p>\n'
          '<h3>最低賃金が一番低いのはどこですか？</h3>\n<p>宮崎県の時給1,085円です。東京都との差は195円で、一番低い額は一番高い額の84.8%です。</p>\n'
          '<h3>正社員にも最低賃金はかかりますか？</h3>\n<p>かかります。正社員・パート・アルバイトなど働き方にかかわらず、働く人すべてにかかります。月給の人は時給に直して比べます。</p>\n'
          '<h3>最低賃金を下回っていたらどうなりますか？</h3>\n<p>最低賃金に届かない部分の決まりは無効になり、最低賃金と同じ額で決めたものとみなされます。差額を払う必要があり、地域別最低賃金を払わなかったときは50万円以下の罰金の決まりがあります。</p>\n'
          '<h3>通勤手当は最低賃金に含めますか？</h3>\n<p>含めません。基本給と毎月決まって払う手当だけで最低賃金を満たしているかを確かめます。通勤手当は社会保険料の計算では報酬に含めます。</p>\n<h3>最低賃金が上がると会社の負担はどれだけ増えますか？</h3>\n<p>上がった時給の分だけでなく保険料の会社の分も増えます。社会保険に入る人なら標準報酬月額が上がると保険料も上がります。</p>\n')
    FUTAN = '<h2 id="futan">最低賃金で人を雇うときの会社の負担</h2>\n<p>最低賃金は働く人に払う時給の下限です。会社は時給のほかに保険料なども負担します。</p>\n<ul>\n <li>社会保険に入る人は健康保険・厚生年金の保険料の半分を会社が払います</li>\n <li>雇用保険に入る人は雇用保険料の会社の分を払います</li>\n <li>労災保険料は全額を会社が払います</li>\n <li>通勤手当は最低賃金の計算に含めませんが、社会保険料と雇用保険料の計算には含めます</li>\n</ul>\n<p>時給と働く時間から会社の負担の合計を計算するときは<a href="/yatou-hiyou/">人を雇う費用の計算</a>を使ってください。</p>\n'
    src = '<div class="src">出典・参考（2026年11月確認）\n <ul>\n%s </ul>\n</div>\n' % ('  <li><a href="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/roudoukijun/minimumichiran/index.html">厚生労働省「地域別最低賃金の全国一覧」</a>（令和8年度）</li>\n' + SRC_COMMON)
    body = hy_wrap(sec1) + calc + '\n' + share(slug) + '\n' + intro + '\n' + toc + '\n' + sec2 + '\n' + sec3 + '\n' + FUKUMU + '\n' + sec5 + '\n' + FUTAN + '\n' + sec6 + '\n' + qa + '\n' + src
    js = JS_ALL % dict(pr=json.dumps(pr, ensure_ascii=False))
    os.makedirs(os.path.join(SITE, slug), exist_ok=True)
    open(os.path.join(SITE, slug, 'index.html'), 'w', encoding='utf-8').write(page(slug, title, desc, upd, body, js, cta, auth=auth_box('厚生労働省')))
    return slug, title

if __name__ == '__main__':
    print(all_page())
