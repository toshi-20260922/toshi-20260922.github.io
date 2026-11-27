# 仕上げ:全ページの「早見表・計算ツール一覧」を tools/pages.json から作り直し、og タグをそろえる。
# 使い方:リポジトリの直下で python3 tools/finish.py
import json, re, glob, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
PAGES = json.load(open(os.path.join(ROOT, 'tools', 'pages.json'), encoding='utf-8'))

def nav_for(me):
    lines = ['<nav class="tools"><div class="t">早見表・計算ツール一覧</div>']
    for p in PAGES:
        if p['path'].strip('/') == me:
            continue
        lines.append(' <a href="%s">%s</a>' % (p['path'], p['label']))
    lines.append(' <a href="/">トップへ</a>')
    lines.append('</nav>')
    return '\n'.join(lines)


# 早見表を上に・入力欄を下に(2026/11/20 本人「早見表が上にあって、より詳しく知りたい人が下の入力欄に入力する。この流れであるべき」)
# 計算の箱(id="calc")のあるページは、tools/hayami_first.json に書いた見出しの欄を計算の箱の前へ動かす。何度流しても同じ結果になる。
HF = json.load(open(os.path.join(ROOT, 'tools', 'hayami_first.json'), encoding='utf-8'))
HYCSS = '.hy1{margin:20px 0 4px}.hy1 h2{margin-top:0}.lead2{margin:14px 0 0}.hyi{margin:0 0 16px}'
LEAD_NUM = '<p class="lead2">自分の数字で計算したい人は、下に入力してください。</p>\n'
LEAD_COND = '<p class="lead2">自分の条件で計算したい人は、下に入力してください。</p>\n'
def lead_for(s, k):
    # 数字の入力が無い（選択肢だけ）ページは「条件」と書く
    chunk = s[k:k + 8000]
    cut = re.search(r'\n<h2|\n<nav class="toc"', chunk)
    if cut:
        chunk = chunk[:cut.start()]
    return LEAD_NUM if re.search(r'<input\b', chunk) else LEAD_COND
def hayami_first(me, s):
    if 'id="calc"' not in s or 'class="hy1"' in s or me not in HF:
        return s
    a = s.find('<h2 id="%s"' % HF[me])
    mk = re.search(r'<div class="[a-z]+" id="calc">', s)
    k = mk.start() if mk else -1
    if a < 0 or k < 0 or a < k:
        return s
    b = s.find('<h2', a + 5)
    sec = s[a:b].rstrip() + '\n'
    s = s[:a] + s[b:]
    for x, y in (('上で入力した', '下で入力した'), ('上で選んだ', '下で選んだ'), ('上の計算', '下の計算'), ('上の入力', '下の入力'), ('上で計算した', '下で計算した')):
        sec = re.sub('(?<!以)' + x, y, sec)
    # 題名の直後に置く。計算の箱が結論の箱の中にあるページは、箱の前（題名の直下）に出す
    top = s.find('<div class="top">')
    h1 = s.find('</h1>', top) if top >= 0 else -1
    tm = re.search(r'</h1>\s*</div>', s[h1:]) if h1 >= 0 else None
    top_end = h1 + tm.end() if tm else k
    ins = k if s[top_end:k].strip() == '' else top_end
    block = '<section class="hy1">\n' + sec + lead_for(s, k) + '</section>\n\n'
    if ins == top_end:
        block = '\n' + block
    s = s[:ins] + block + s[ins:]
    if HYCSS not in s:
        s = s.replace('</style>', HYCSS + '</style>', 1)
    return s

# 冒頭の文(目次のすぐ前の段落)を早見表の見出しの前へ動かす(2026/11/25 プロゴと同じく、例を書いた文→早見表の順)。
# 早見表の黄色の行は冒頭の文の例の行なので、読む順に例の文が先に来るようにする。何度流しても同じ結果になる。
def intro_first(me, s):
    if 'class="hy1"' not in s or 'class="hyi"' in s:
        return s
    m = re.search(r'<p>((?:(?!</p>).)*)</p>\s*(?=<nav class="toc">)', s, re.S)
    a = s.find('<section class="hy1">')
    if not m or a < 0 or m.start() < a:
        return s
    p = '<p class="hyi">' + m.group(1) + '</p>\n'
    s = s[:m.start()] + s[m.end():]
    a = s.find('<section class="hy1">') + len('<section class="hy1">\n')
    return s[:a] + p + s[a:]

# 早見表のすぐ下の一行をプロゴと同じ「▶ 〜場合は、下の計算ツールで自分の条件のまま計算できます。」の形にする(2026/11/25)。
# 言葉は tools/ya_bun.json。「下の計算ツール」は計算の箱(id="calc")へのリンク。
YA = json.load(open(os.path.join(ROOT, 'tools', 'ya_bun.json'), encoding='utf-8'))
def yabun(me, s):
    s = s.replace('.lead2{margin:14px 0 0;font-weight:700}', '.lead2{margin:14px 0 0}.hyi{margin:0 0 16px}')
    if 'id="calc"' not in s or 'class="lead2"' not in s:
        return s
    L = '<a href="#calc">下の計算ツール</a>'
    t = '<p class="lead2">▶ %s</p>' % YA.get(me, '自分の数字で確かめたい人は、{L}で計算できます。').replace('{L}', L)
    return re.sub(r'<p class="lead2">.*?</p>', t, s, count=1, flags=re.S)

# 公開日(2026/11/20 プロゴと同じく公開日と更新日を並べる)。tools/published.json に無い新しいページは今日の日付を入れる。
# 2026/11/13 にまとめて取り込んだページは公開日が記録に無いので null のまま出さない(作らない)。
import datetime
PUBF = os.path.join(ROOT, 'tools', 'published.json')
PUB = json.load(open(PUBF, encoding='utf-8'))
def jd(d):
    y, m, dd = d.split('-'); return '%s年%d月%d日' % (y, int(m), int(dd))
def pubdate(me, s):
    if me not in PUB:
        PUB[me] = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
    d = PUB.get(me)
    if not d or '<p class="upd">公開日' in s:
        return s
    return s.replace('<p class="upd">更新日', '<p class="upd">公開日：%s　更新日' % jd(d), 1)

# 表の全画面表示。6行以上の表に付ける。2026-11-24 本人「拡大表示するという表現もめちゃくちゃ」「全体が表示されないし拡大すらされない」
# → ボタンの名前を「表全体を見る」にし、表を画面の幅に縮めて全体を一度に出す。
FSX = ('<style id="fsxc">.fsb{display:inline-block;margin:8px 0 6px;padding:6px 12px;border:1px solid #0f3d31;border-radius:6px;background:#ffffff;color:#0f3d31;font-weight:700;font-size:13px;cursor:pointer}'
       '.fso{position:fixed;top:0;left:0;right:0;bottom:0;z-index:9999;background:#ffffff;overflow:auto;padding:0 12px 24px}'
       '.fso .fsh{position:sticky;top:0;left:0;background:#ffffff;padding:10px 0;display:flex;justify-content:flex-end}.fso table{min-width:0;margin:0}.fsz{overflow:hidden}</style>'
       '<script id="fsx">(function(){var ws=document.querySelectorAll("main .tw");for(var i=0;i<ws.length;i++){(function(w){if(w.querySelectorAll("tr").length<6)return;'
       'var b=document.createElement("button");b.type="button";b.className="fsb";b.textContent="表全体を見る";'
       'b.addEventListener("click",function(){var o=document.createElement("div");o.className="fso";var h=document.createElement("div");h.className="fsh";'
       'var c=document.createElement("button");c.type="button";c.className="fsb";c.textContent="閉じる";h.appendChild(c);o.appendChild(h);'
       'var t=w.querySelector("table").cloneNode(true);t.removeAttribute("id");[].forEach.call(t.querySelectorAll("[id]"),function(e){e.removeAttribute("id")});var bx=document.createElement("div");bx.className="fsz";bx.appendChild(t);o.appendChild(bx);document.body.appendChild(o);document.body.style.overflow="hidden";t.style.width="max-content";var W=o.clientWidth-24,tw=t.offsetWidth,k=Math.min(1,W/tw);t.style.transformOrigin="0 0";t.style.transform="scale("+k+")";bx.style.height=Math.ceil(t.offsetHeight*k)+"px";bx.style.width=Math.floor(tw*k)+"px";'
       'c.addEventListener("click",function(){document.body.removeChild(o);document.body.style.overflow="";});});w.parentNode.insertBefore(b,w);})(ws[i]);}})();</script>')

# 答えの列だけの表(tools/kotae_retsu.json)。元の表はそのまま残し「ほかの列も見る」の中に入れる。答えの表は元の表から写すので数字は必ず同じ。
KR = json.load(open(os.path.join(ROOT, 'tools', 'kotae_retsu.json'), encoding='utf-8'))
KRC = '<style id="krc">.ucw{overflow-x:auto;margin:0 0 8px}.ucw table{width:100%}.ucn tr.hit td{background:#fff59d}.ucn tr.x7hl td{background:#eaf5d8;font-weight:700}.ucb{display:block;margin:4px 0 14px;padding:0;border:0;background:none;font-family:inherit;font-weight:700;color:#00775a;font-size:14px;cursor:pointer;text-decoration:underline}</style>'
def kotae(me, s):
    s = re.sub(r'<style id="krc">.*?</style><script id="krj">.*?</script>\n?', '', s, flags=re.S)
    if me not in KR:
        return s
    js = ('<script id="krj">(function(){var C=%s;var w=document.querySelector("main .tw");if(!w)return;var t=w.querySelector("table");if(!t)return;'
          'var ths=t.querySelectorAll("thead th"),hid=[];for(var i=0;i<ths.length;i++)if(C.indexOf(i)<0)hid.push(ths[i].textContent.replace(/\\s+/g,""));'
          'var u=document.createElement("div");u.className="ucw";var nt=document.createElement("table");nt.className="ucn";u.appendChild(nt);'
          'var fb=w.previousElementSibling&&w.previousElementSibling.className==="fsb"?w.previousElementSibling:null;w.parentNode.insertBefore(u,fb||w);'
          'var bt=document.createElement("button");bt.type="button";bt.className="ucb";var lb="ほかの列も見る（"+hid.slice(0,3).join("・")+(hid.length>3?"など":"")+"）";bt.textContent=lb;w.parentNode.insertBefore(bt,w);w.hidden=true;'
          'bt.addEventListener("click",function(){w.hidden=!w.hidden;bt.textContent=w.hidden?lb:"ほかの列を閉じる";});'
          'function cp(r){var x=document.createElement("tr");x.className=r.className;for(var k=0;k<C.length;k++){var c=r.children[C[k]];if(c){var y=c.cloneNode(true);y.removeAttribute("id");[].forEach.call(y.querySelectorAll("[id]"),function(e){e.removeAttribute("id")});x.appendChild(y);}}return x;}'
          'function build(){nt.innerHTML="";var th=document.createElement("thead");var hr=t.querySelector("thead tr");if(hr)th.appendChild(cp(hr));nt.appendChild(th);var tb=document.createElement("tbody");'
          '[].forEach.call(t.querySelectorAll("tbody tr"),function(r){var x=cp(r);x.addEventListener("click",function(){r.click();});tb.appendChild(x);});nt.appendChild(tb);}'
          'build();new MutationObserver(build).observe(t,{subtree:true,childList:true,attributes:true,attributeFilter:["class"],characterData:true});})();</script>') % json.dumps(KR[me])
    return s.replace('</body>', KRC + js + '\n</body>', 1)


# 表の1列目の「年収（万円）」の書き方をやめ、見出しは「年収」、マスは「950万円」と書く(2026-11-24 本人「年収は万円もおかしいし」)。
# 表を JS で作り直すページもあるので、表の中身が変わるたびに書き直す。
MANEN = ('<script id="manen">(function(){function fix(t){var th=t.querySelector("thead th");if(!th)return;var h=th.innerHTML;'
         'if(!/(<br>)?（?万円）?$/.test(h.trim())&&th.getAttribute("data-mn")!=="1")return;'
         'if(th.getAttribute("data-mn")!=="1"){th.innerHTML=h.trim().replace(/(<br>)?（?万円）?$/,"");th.setAttribute("data-mn","1");}'
         '[].forEach.call(t.querySelectorAll("tbody tr"),function(r){var c=r.cells[0];if(!c)return;var s=c.textContent.trim();if(/^[0-9,]+$/.test(s))c.textContent=s+"万円";});}'
         'var ts=document.querySelectorAll("main table");for(var i=0;i<ts.length;i++)(function(t){fix(t);var b=t.querySelector("tbody");if(b)new MutationObserver(function(){fix(t)}).observe(b,{childList:true,subtree:true});})(ts[i]);})();</script>')
def manen(me, s):
    s = re.sub(r'<script id="manen">.*?</script>\n?', '', s, flags=re.S)
    if '<main' not in s or not re.search(r'<th>[^<]*(<br>)?（?万円）?</th>', s):
        return s
    return s.replace('</body>', MANEN + '\n</body>', 1)


# 早見表の黄色の行(2026-11-25)。黄色は下の計算ツールに入力した値に当たる行に付く(各ページのJSが tr.hit を付ける)。
# 黄色の意味は表の上の一文(tools/kiiro_bun.json)で書く。
# 2026-11-25 本人「黄色の線を見る人はひとりもいないはず」。読む人は計算ツールで金額を見て終わるので、早見表の行に色を付けない(プロゴの早見表も同じ)。
HIT = '<style id="hitc">main table tr.hit td{background:transparent!important}</style><script id="hitj"></script>'
KB = json.load(open(os.path.join(ROOT, 'tools', 'kiiro_bun.json'), encoding='utf-8'))
def kiiro(me, s):
    s = re.sub(r'<p class="kiiro">.*?</p>\n?', '', s)
    if True:
        return s
    a = s.find('<section class="hy1">'); b = s.find('</section>', a)
    i = s.find('<div class="tw">', a)
    if i < 0 or i > b:
        return s
    return s[:i] + '<p class="kiiro">%s</p>\n' % KB[me] + s[i:]
def hitlb(me, s):
    s = re.sub(r'<style id="hitc">.*?</style><script id="hitj">.*?</script>\n?', '', s, flags=re.S)
    if 'tr.hit' not in s:
        return s
    return s.replace('</body>', HIT + '\n</body>', 1)

def fsx(me, s):
    if FSX in s or '<main' not in s:
        return s
    s = re.sub(r'<style id="fsxc">.*?</style><script id="fsx">.*?</script>\n?', '', s, flags=re.S)
    if '<main' not in s:
        return s
    return s.replace('</body>', FSX + '\n</body>', 1)


# 表の列が2文字ずつ縦に折れないようにする(2026/11/22 本人「見やすい？プロゴとくらべて」「やるべきことやってよ」)。
# 表のセルに最低の幅(4文字ぶん)を付け、8文字以下の短いセル(金額・日付・順位・見出し)は折り返さない。表が広くなったら .tw の中で横に動かせる。
TDW = ('<style id="tdwc">main .tw{overflow-x:auto;-webkit-overflow-scrolling:touch}main .tw th,main .tw td{min-width:4em}main .tw .tdn{white-space:nowrap}</style>'
       '<script id="tdw">(function(){function f(){var c=document.querySelectorAll("main .tw th,main .tw td");for(var i=0;i<c.length;i++){'
       'var t=(c[i].textContent||"").replace(/\\s/g,"");if(t.length&&t.length<=8)c[i].classList.add("tdn");else c[i].classList.remove("tdn");}}'
       'f();var m=document.querySelector("main");if(m&&window.MutationObserver){var b=0;new MutationObserver(function(){if(b)return;b=1;setTimeout(function(){b=0;f();},0);}).observe(m,{childList:true,subtree:true,characterData:true});}})();</script>')
def tdw(me, s):
    if 'id="tdw"' in s or '<main' not in s:
        return s
    return s.replace('</body>', TDW + '\n</body>', 1)

# ファビコン(2026/11/20)。head に rel="icon" か rel="apple-touch-icon" が無いページは </head> の直前に足す。何度流しても同じ結果になる。
ICON = '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
APPLE = '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
def has_link(chunk, rel):
    for tag in re.findall(r'<link\b[^>]*>', chunk):
        m = re.search(r'\brel="([^"]*)"', tag)
        if m and rel in m.group(1).split():
            return True
    return False
def icons(s):
    h = s.find('</head>')
    if h < 0:
        return s
    head = s[:h]
    add = ''
    if not has_link(head, 'icon'):
        add += ICON
    if not has_link(head, 'apple-touch-icon'):
        add += APPLE
    if not add:
        return s
    return head + add + s[h:]


# 計測(GA4・Clarity)を、本人のブラウザと自動の確認からは外す(2026/11/25 本人「自分が触ったらクリックに数えられるようになってない？」)。
# ?notrack=1 または従来の ?naibu=1 で目印を付け、付いている間と navigator.webdriver のときはタグ自体を読み込まない。
# ?notrack=0 または ?naibu=0 で目印を消す。決めるのはここ1か所だけ。
GA_ID = 'G-CW5VSP86R1'
CLARITY_ID = 'z9qg6yckbq'
TRACK = (
    '<script id="tt-track">(function(){var s=false;try{var q=location.search;'
    'if(/[?&](?:notrack|naibu)=1(?:&|$)/.test(q))localStorage.setItem("tt_naibu","1");'
    'if(/[?&](?:notrack|naibu)=0(?:&|$)/.test(q))localStorage.removeItem("tt_naibu");'
    's=localStorage.getItem("tt_naibu")==="1";}catch(e){}'
    'try{if(navigator.webdriver)s=true;}catch(e){}'
    'if(s)return;'
    'var g=document.createElement("script");g.async=1;g.src="https://www.googletagmanager.com/gtag/js?id=%s";'
    'document.head.appendChild(g);window.dataLayer=window.dataLayer||[];'
    'function gtag(){dataLayer.push(arguments);}window.gtag=gtag;gtag("js",new Date());gtag("config","%s");'
    '(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};'
    't=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;'
    'y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","%s");'
    '})();</script>'
) % (GA_ID, GA_ID, CLARITY_ID)
def track(s):
    # 古い計測タグとこの仕掛けを外してから入れ直す(何度流しても同じ結果)
    s = re.sub(r'<script id="tt-track">.*?</script>\n?', '', s, flags=re.S)
    s = re.sub(r'<script\b[^>]*src="https://www\.googletagmanager\.com/gtag/js\?id=G-CW5VSP86R1"[^>]*(?:></script>|\s*/>)\n?', '', s, flags=re.I)
    def _drop_old(m):
        b = m.group(0)
        if 'G-CW5VSP86R1' in b or 'clarity.ms/tag' in b or 'tt_naibu' in b:
            return ''
        return b
    s = re.sub(r'<script\b[^>]*>.*?</script>\n?', _drop_old, s, flags=re.S)
    h = s.find('</head>')
    if h < 0:
        return s
    return s[:h] + TRACK + '\n' + s[h:]

# 文字の種類(フォント)をそろえる(2026/11/25 本人「フォントの種類もめっちゃくちゃにばらついてるのでなおしてな」)。
# 決めるのは tools/font.json の1か所だけ。本文・表・ボタン・入力欄は body の字、ファーストビューは今の字のまま(firstview・firstview_keep)。
# 全ページでトップページと同じ Noto Sans JP を読み込む。ページに新しく font-family を書かない(tools/gate.py が数える)。
FONT = json.load(open(os.path.join(ROOT, 'tools', 'font.json'), encoding='utf-8'))
FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800;900&amp;display=swap">')
# 入力欄・ボタンの文字は何も書かないとブラウザの標準(Arial など)になるので、ここで本文の字に合わせる。ファーストビュー(firstview_pin)は今の字のまま
_PIN = ','.join(p + x for p in FONT['firstview_pin'] for x in ('', ' button', ' input', ' select', ' textarea'))
FONT_CSS = ('<style id="ttfont">:root{--tt-font:%s;--tt-fv:%s}'
            'body,button,input,select,textarea{font-family:var(--tt-font)}%s{font-family:var(--tt-fv)}</style>') % (FONT['body'], FONT['firstview'], _PIN)
def font_keep(sel):
    return any(x.strip() in FONT['firstview_keep'] for x in sel.split(','))
def fontu(s):
    # 古い読み込みと古い設定を外す(何度流しても同じ結果になる)
    s = re.sub(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*>', '', s)
    s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">', '', s)
    s = re.sub(r'<style id="ttfont">.*?</style>\n?', '', s, flags=re.S)
    def fix_rule(m):
        if font_keep(m.group(1)):
            return m.group(0)
        return m.group(1) + '{' + re.sub(r'font-family\s*:\s*(?!inherit\b|var\(--tt-)[^;}]+', 'font-family:var(--tt-font)', m.group(2)) + '}'
    def fix_css(m):
        return re.sub(r'([^{}]*)\{([^{}]*)\}', fix_rule, m.group(0))
    def fix_attr(m):
        return re.sub(r'font-family\s*:\s*(?!inherit\b|var\(--tt-)[^;"]+', 'font-family:var(--tt-font)', m.group(0))
    s = re.sub(r'<style\b[^>]*>.*?</style>', fix_css, s, flags=re.S)
    s = re.sub(r'\sstyle="[^"]*"', fix_attr, s)
    i = s.find('<style')
    h = s.find('</head>')
    at = i if 0 <= i < h else h
    return s[:at] + FONT_LINK + FONT_CSS + '\n' + s[at:]

changed = 0
for f in sorted(glob.glob(os.path.join(SITE, '*', 'index.html'))):
    me = os.path.basename(os.path.dirname(f))
    s = open(f, encoding='utf-8').read()
    o = s
    s = hayami_first(me, s)
    s = yabun(me, s)
    s = intro_first(me, s)
    s = kiiro(me, s)
    s = pubdate(me, s)
    s = fsx(me, s)
    s = manen(me, s)
    s = kotae(me, s)
    s = hitlb(me, s)
    s = tdw(me, s)
    s = icons(s)
    s = track(s)
    s = fontu(s)
    if '<nav class="tools">' in s:
        s = re.sub(r'<nav class="tools">.*?</nav>', lambda m: nav_for(me), s, count=1, flags=re.S)
    canon = re.search(r'<link rel="canonical" href="([^"]+)">', s)
    title = re.search(r'<title>(.*?)</title>', s, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)">', s)
    if canon and title:
        s = re.sub(r'\n?<meta property="og:[a-z_]+" content="[^"]*">', '', s)
        og = ['<meta property="og:type" content="article">',
              '<meta property="og:url" content="%s">' % canon.group(1),
              '<meta property="og:title" content="%s">' % title.group(1).strip(),
              '<meta property="og:site_name" content="タックステーブル">']
        if desc:
            og.append('<meta property="og:description" content="%s">' % desc.group(1))
        s = s.replace(canon.group(0), canon.group(0) + '\n' + '\n'.join(og), 1)
    # 給与明細だけ、画面の文を文節で包む。ほかのページは変えない。何度流しても同じ結果になる。
    if me == 'kyuyo-meisai':
        import phrase
        s = phrase.apply_page(s)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
        changed += 1

# トップページは上の作り直しの対象外なので、計測タグだけそろえる
_tf = os.path.join(SITE, 'index.html')
_ts = open(_tf, encoding='utf-8').read()
if track(_ts) != _ts:
    open(_tf, 'w', encoding='utf-8').write(track(_ts))
    changed += 1
# トップページのフォントもそろえる(tools/font.json)
_ts = open(_tf, encoding='utf-8').read()
if fontu(_ts) != _ts:
    open(_tf, 'w', encoding='utf-8').write(fontu(_ts))
    changed += 1

json.dump(PUB, open(PUBF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('finish.py: 書き換えたページ', changed)
