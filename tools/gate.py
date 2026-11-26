# 公開前の関所:全ページを数えて、最後の行が「問題 0 件」のときだけ site/gate_ok.txt を作る。
# 使い方:リポジトリの直下で python3 tools/finish.py のあと python3 tools/gate.py
import asyncio, glob, json, os, re
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
PAGES = json.load(open(os.path.join(ROOT, 'tools', 'pages.json'), encoding='utf-8'))
OK = os.path.join(SITE, 'gate_ok.txt')
if os.path.exists(OK):
    os.remove(OK)

files = sorted(glob.glob(os.path.join(SITE, '*', 'index.html'))) + [os.path.join(SITE, 'index.html')]
probs = []
HIKAKU = json.load(open(os.path.join(ROOT, 'tools', 'hikaku_bun.json'), encoding='utf-8'))
def bad(f, kind, detail):
    probs.append((f.replace(SITE + '/', ''), kind, detail))

# 1 HTMLだけで数えるもの
allp = {p['path'].strip('/') for p in PAGES}
for f in files:
    s = open(f, encoding='utf-8').read()
    me = os.path.basename(os.path.dirname(f)) if f.endswith('/index.html') and os.path.dirname(f) != SITE else ''
    # 普段の会話で言わない「算出」(2026/11/22 本人「算出とか言うかよ　計算ちゃうんか」)。国税庁の表・法令の名前だけ例外。
    _vis = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', '', s, flags=re.S)
    for _m in re.finditer(r'算出(?!率)', _vis):
        if _vis[_m.start():_m.start() + 6] == '算出所得税額':
            continue
        bad(f, '算出(計算と書く)', _vis[max(0, _m.start() - 15):_m.end() + 10].replace('\n', ' '))
    # 表の4桁以上の数字はカンマを入れる(2026/11/23 法人成りの表で「1113」を見つけた)
    for _m in re.finditer(r'<td[^>]*>([+−-]?\d{4,})(?:<small>|</td>)', s):
        bad(f, '表の数字にカンマが無い', _m.group(1))
    # 早見表の大見出しを1つの年齢に固定しない。年齢で変わる表は切り替えか、同じ見出しの下に並べる(2026/11/23 本人「40歳以上の人が見たら私が使える早見表がない」)
    for _m in re.finditer(r'<h2[^>]*>([^<]*早見表[^<]*（[^<]*歳[^<]*）)</h2>', s):
        bad(f, '早見表の見出しが1つの年齢に固定', _m.group(1))
    # 答えの列だけの表にしたページに「右に動かすと」の案内を残さない(2026-11-24)
    if me in json.load(open(os.path.join(ROOT, 'tools', 'kotae_retsu.json'), encoding='utf-8')) and re.search(r'右に動かす|横に動かす|横にスクロール', re.sub(r'<script.*?</script>', '', s, flags=re.S)):
        bad(f, '答えの列だけの表なのに横に動かす案内が残っている', '')
    # 文字の種類は tools/font.json の1か所で決める(2026/11/25 本人「フォントの種類もめっちゃくちゃにばらついてるのでなおしてな」)。
    # 使ってよいのは var(--tt-font)(本文)・var(--tt-fv)(題名の帯)・inherit と、firstview_keep の選択子(ファーストビューを今のまま残す所)だけ
    _font = json.load(open(os.path.join(ROOT, 'tools', 'font.json'), encoding='utf-8'))
    _css = '\n'.join(re.findall(r'<style\b[^>]*>(.*?)</style>', s, re.S))
    _vals = []
    for _r in re.finditer(r'([^{}]*)\{([^{}]*)\}', _css):
        if any(_x.strip() in _font['firstview_keep'] for _x in _r.group(1).split(',')):
            continue
        _vals += re.findall(r'font-family\s*:\s*([^;}]+)', _r.group(2))
    for _a in re.findall(r'\sstyle="([^"]*)"', s):
        _vals += re.findall(r'font-family\s*:\s*([^;]+)', _a)
    for _v in _vals:
        if _v.strip() not in ('inherit', 'var(--tt-font)', 'var(--tt-fv)'):
            bad(f, 'フォントを個別に決めている(tools/font.json にそろえる)', _v.strip()[:40])
    if '<style id="ttfont">' not in s or 'family=Noto+Sans+JP' not in s:
        bad(f, 'フォントの共通設定が無い', 'python3 tools/finish.py を流す')
    if '税理士事務所' in s:
        bad(f, '税理士事務所', '')
    canon = re.search(r'<link rel="canonical" href="([^"]+)">', s)
    want = 'https://taxtable.jp/' + (me + '/' if me else '')
    if not canon or canon.group(1) != want:
        bad(f, 'canonical', canon.group(1) if canon else 'なし')
    ogu = re.search(r'<meta property="og:url" content="([^"]+)">', s)
    if me and (not ogu or ogu.group(1) != want):
        bad(f, 'og:url', ogu.group(1) if ogu else 'なし')
    if me and not re.search(r'<meta property="og:title" content="[^"]+">', s):
        bad(f, 'og:title', 'なし')
    # 計測タグは finish.py の tt-track の1か所だけ。目印付きと自動操作では読み込まない(2026/11/25)
    _tn = len(re.findall(r'<script id="tt-track">', s))
    if _tn != 1:
        bad(f, '計測タグ', 'tt-track が %d 個' % _tn)
    else:
        _tb = re.search(r'<script id="tt-track">(.*?)</script>', s, re.S).group(1)
        if 'G-CW5VSP86R1' not in _tb or 'z9qg6yckbq' not in _tb:
            bad(f, '計測タグ', '測定IDが違う')
        if 'notrack' not in _tb or 'navigator.webdriver' not in _tb or 'tt_naibu' not in _tb:
            bad(f, '計測タグ', '除外の仕掛けが足りない')
    if re.search(r'<script\b[^>]*src="https://www\.googletagmanager\.com/gtag/js', s):
        bad(f, '計測タグ', 'gtag を常に読み込むタグが残っている')
    for _sm in re.finditer(r'<script\b[^>]*>.*?</script>', s, re.S):
        if 'id="tt-track"' in _sm.group(0):
            continue
        if 'G-CW5VSP86R1' in _sm.group(0) or 'clarity.ms/tag' in _sm.group(0) or 'tt_naibu' in _sm.group(0):
            bad(f, '計測タグ', 'tt-track の外に計測のスクリプトが残っている')
            break
    for h in re.findall(r'href="(/[^"#?]*)"', s):
        p = os.path.join(SITE, h.lstrip('/'))
        q = os.path.join(ROOT, 'live', h.lstrip('/'))
        if not (os.path.exists(p) or os.path.exists(os.path.join(p, 'index.html')) or os.path.exists(q)):
            bad(f, '行き先の無いリンク', h)
    if me and me != 'policy':
        m = re.search(r'<nav class="tools">(.*?)</nav>', s, re.S)
        have = {h.strip('/') for h in re.findall(r'href="(/[^"]+/)"', m.group(1))} if m else set()
        for p in allp - have - {me}:
            bad(f, '一覧の抜け', p)
    if me and 'id="calc"' in s:
        hy, ca = s.find('class="hy1"'), s.find('id="calc"')
        if hy < 0 or hy > ca:
            bad(f, '早見表が計算の箱より上に無い', 'tools/hayami_first.json に見出しの id を足して finish.py を流す')
    # 同業他社と比べるページ(決算分析・ベンチマーク)には、競合他社との比較の文が必須(2026/11/23 本人「これは必須なのよ絶対な」)。
    # tools/hikaku_bun.json の pages に載せたページと、id="bench" を持つページを数える。文は一字も変えない。
    if me and (me in HIKAKU['pages'] or 'id="bench"' in s):
        _pos = _vis.find(HIKAKU['bun'])
        if _pos < 0:
            bad(f, '競合他社との比較の文が無い', HIKAKU['bun'])
        elif 'id="calc"' in s and s.find(HIKAKU['bun']) < s.find('id="calc"'):
            bad(f, '競合他社との比較の文が結果より上にある', '計算の結果のすぐ下に置く')
    if me and me != 'policy' and me not in allp:
        bad(f, 'pages.json に無いページ', me)
    head = s.split('</head>', 1)[0]
    def link_ok(rel, href):
        for tag in re.findall(r'<link\b[^>]*>', head):
            rm = re.search(r'\brel="([^"]*)"', tag)
            hm = re.search(r'\bhref="([^"]*)"', tag)
            if rm and hm and rel in rm.group(1).split() and hm.group(1) == href:
                return True
        return False
    if not link_ok('icon', '/favicon.svg'):
        bad(f, 'favicon', 'rel="icon" なし')
    if not link_ok('apple-touch-icon', '/apple-touch-icon.png'):
        bad(f, 'apple-touch-icon', 'なし')

# トップページの一覧の名前(2026/11/22 本人「早見表の項目に計算ツールを置いてる」「ツール名として早見表にしないと異常」)
# 早見表の一覧に置く名前には「早見表」を入れる。計算ツールの一覧に置く名前に「早見表」を入れない。
_top = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
def _names(start, end, tag):
    i = _top.find(start)
    if i < 0:
        return []
    b = _top[i:_top.find(end, i)]
    if tag == 'a':
        return re.findall(r'<a href="/[^"#]+"[^>]*>([^<]*)</a>', b)
    return [re.sub(r'<br>', '', x) for x in re.findall(r'<a href="/[^"#]+"[^>]*>(?:(?!</a>).)*?<%s>(.*?)</%s>' % (tag, tag), b, re.S)]
_mi = re.search(r'id="list"', _top); _ti = re.search(r'id="tools"', _top)
for _where, _st, _en, _tag, _want in [
    ('メニューの早見表一覧', '<button type="button">早見表一覧</button>', '</div></div>', 'a', True),
    ('最初の画面の早見表メニュー', '<p>早見表メニュー</p>', '</div>', 'span', True),
    ('下の早見表一覧', _top[_mi.start():_mi.start() + 40] if _mi else '\0', 'id="tools"', 'b', True),
    ('メニューの計算ツール', '<button type="button">計算ツール</button>', '</div></div>', 'a', False),
    ('下の計算ツール一覧', _top[_ti.start():_ti.start() + 40] if _ti else '\0', '</section>', 'b', False)]:
    for _n in _names(_st, _en, _tag):
        if _want and '早見表' not in _n:
            bad(os.path.join(SITE, 'index.html'), '早見表の一覧に早見表でない名前', _where + ' ' + _n)
        if not _want and '早見表' in _n:
            bad(os.path.join(SITE, 'index.html'), '計算ツールの一覧に早見表の名前', _where + ' ' + _n)

# 同じページはトップページの中で同じ名前にする(2026/11/22)。早見表の名前と計算の名前はそれぞれ1つまで。
_all = {}
for _st, _en, _tag in [('<button type="button">早見表一覧</button>', '</div></div>', 'a'), ('<button type="button">計算ツール</button>', '</div></div>', 'a'),
                       ('<p>早見表メニュー</p>', '</div>', 'span'), ('class="pop"', '</ul>', 'span'),
                       (_top[_mi.start():_mi.start() + 40] if _mi else '\0', 'id="tools"', 'b'), (_top[_ti.start():_ti.start() + 40] if _ti else '\0', '</section>', 'b')]:
    _i = _top.find(_st)
    if _i < 0:
        continue
    _b = _top[_i:_top.find(_en, _i)]
    _pat = r'<a href="(/[^"#]+)"[^>]*>([^<]*)</a>' if _tag == 'a' else r'<a href="(/[^"#]+)"[^>]*>(?:(?!</a>).)*?<%s>(.*?)</%s>' % (_tag, _tag)
    for _h, _n in re.findall(_pat, _b, re.S):
        _all.setdefault(_h, set()).add(re.sub(r'<br>|\s', '', _n))
for _h, _ns in _all.items():
    for _grp in ([x for x in _ns if '早見表' in x], [x for x in _ns if '早見表' not in x]):
        if len(_grp) > 1:
            bad(os.path.join(SITE, 'index.html'), '同じページの名前が場所で違う', _h + ' ' + '／'.join(sorted(_grp)))

# 言い方の点検(tools/kotoba.py の NG に当たる所)。直しは python3 tools/kotoba.py --fix
import sys as _sys
_sys.path.insert(0, os.path.join(ROOT, 'tools'))
import kotoba as _kotoba
for _f, _c in _kotoba.find():
    bad(os.path.join(ROOT, _f), '言い方(kotoba.py)', _c)

# 全ページ共通の部品が全ページ同じか(2026/11/22 本人「やるべきことやってよ」。トップだけ違うロゴ・ファビコンの欠けを本人が見つけた)
# ヘッダー・画面下のボタン・フッター・監修・制作税理士の欄を、全ページで比べる。いちばん多い形と違うページを問題として数える。
# 運営方針(policy)のヘッダーと画面下のボタンには「開業相談」があり、ほかのページと違う(本人の判断待ち。2026/11/22 報告)。
_EXC = {'header': {'policy'}, 'fbar': {'policy'}}
def _common(name, pat, clean):
    _vals = {}
    for _f in files:
        _rel = os.path.relpath(os.path.dirname(_f), SITE)
        if _rel == '.' or _rel.startswith('saitei-chingin-') and name == 'auth' and False:
            continue
        _s = open(_f, encoding='utf-8').read()
        _m = re.search(pat, _s, re.S)
        _v = clean(_m.group(0)) if _m else '(無い)'
        _vals.setdefault(_v, []).append(_rel)
    if len(_vals) <= 1:
        return
    _main = max(_vals, key=lambda k: len(_vals[k]))
    for _v, _ps in _vals.items():
        if _v == _main:
            continue
        for _rel in _ps:
            if _rel in _EXC.get(name, set()):
                continue
            bad(os.path.join(SITE, _rel, 'index.html'), '共通の部品がほかのページと違う', name)
_cl = lambda x: re.sub(r'\s+', ' ', re.sub(r' data-cta="[^"]*"| style="[^"]*"', '', x))
_common('header', r'<header.*?</header>', _cl)
_common('fbar', r'<div class="fbar[^"]*">.*?</div>', _cl)
_common('footer', r'<footer.*?</footer>', _cl)
_common('auth', r'<p class="auth-h">.*?</p><p class="auth-n">.*?</p><p class="auth-r">.*?</p>', _cl)
_common('favicon', r'<link rel="icon"[^>]*>\s*<link rel="apple-touch-icon"[^>]*>', _cl)
# トップページのロゴもほかのページと同じか
_tl = re.search(r'<a class="logo" href="/">.*?</a>', _top, re.S)
_sl = re.search(r'<a class="logo" href="/">.*?</a>', open(files[1] if os.path.dirname(files[0]) == SITE else files[0], encoding='utf-8').read(), re.S)
_tl = re.search(r'<a class="(?:logo|nlg)" href="/">.*?</a>', _top, re.S)
_lk = lambda x: (re.findall(r'src="([^"]+)"', x), re.findall(r'<b>(.*?)</b>', x), re.findall(r'<small>(.*?)</small>', x))
if not _tl or not _sl or _lk(_tl.group(0)) != _lk(_sl.group(0)):
    bad(os.path.join(SITE, 'index.html'), '共通の部品がほかのページと違う', 'トップページのロゴ')

# 2 画面で数えるもの
JS = r'''() => {
 const main = document.querySelector('main') || document.body;
 const t = main.innerText;
 const out = {touten: [], zen: [], nan: /NaN|undefined/.test(t)};
 const t2 = t.replace(/「[^」]*」/g, '「」').replace(/法人税、住民税及び事業税/g, '');
 for (const line of t2.split(/[\n\t]/)) for (const sen of line.split('。')) {
   if ((sen.match(/、/g) || []).length >= 2) out.touten.push(sen.trim());
 }
 const z = t.match(/[Ａ-Ｚａ-ｚ０-９]+/g); if (z) out.zen = z.slice(0, 5);
 out.ov = document.documentElement.scrollWidth - window.innerWidth;
 // 表の中で2文字ずつ縦に折れる狭い列(2026/11/22 年収の壁の4列目。本人「見やすい？プロゴとくらべて」)
 // 文字1つずつの位置を取り、行の数を数える。1行あたり2文字以下で3行以上に折れるセルを数える。
 out.narrow = [];
 for (const c of document.querySelectorAll('main td, main th')) {
   if (!c.getBoundingClientRect().width) continue;
   const tops = new Set(); let n = 0;
   const w = document.createTreeWalker(c, NodeFilter.SHOW_TEXT);
   while (w.nextNode()) {
     const tn = w.currentNode;
     for (let k = 0; k < tn.length; k++) {
       if (/\s/.test(tn.data[k])) continue;
       const rg = document.createRange(); rg.setStart(tn, k); rg.setEnd(tn, k + 1);
       const rc = rg.getClientRects()[0]; if (!rc) continue;
       tops.add(rc.top); n++;
     }
   }
   const lh = parseFloat(getComputedStyle(c).fontSize) || 14;
   const ys = [...tops].sort((a, b) => a - b); let lines = 0, last = -1e9;
   for (const y of ys) { if (y - last > lh * 0.7) { lines++; last = y; } }
   if (n >= 4 && lines >= 3 && n / lines <= 2) out.narrow.push((c.innerText || '').replace(/\s/g, '').slice(0, 12) + ' ' + Math.round(c.getBoundingClientRect().width) + 'px');
 }
 return out;
}'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (360, 390, 414, 1280):
            for f in files:
                pg = await b.new_page(viewport={'width': w, 'height': 800})
                errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                await pg.goto('file://' + f)
                r = await pg.evaluate(JS)
                if errs: bad(f, '画面のエラー', '%d %s' % (w, errs[0][:80]))
                if r['ov'] > 0: bad(f, 'はみ出し', '%dpx 幅%d' % (r['ov'], w))
                if r['nan']: bad(f, 'NaN', str(w))
                if w == 390:
                    for x in r['touten']: bad(f, '「、」2つ以上', x)
                    for x in r['zen']: bad(f, '全角英数字', x)
                    for x in r['narrow'][:3]: bad(f, '表の列が狭くて縦に折れる', x)
                await pg.close()
        await b.close()
asyncio.run(main())

# 行の折れ方（tools/gyou.py）。給与明細の件数だけ問題に数える。ほかのページは件数の報告だけ。
import gyou
_gc, _gd = gyou.run()
for _rel, _ni in _gc.items():
    if not _ni:
        continue
    if _rel.split(os.sep)[0] == 'kyuyo-meisai':
        for _x in _gd[_rel]:
            bad(os.path.join(SITE, _rel), '改行', _x)
    else:
        print('報告\t%s\t改行 %d件' % (_rel, _ni))

seen = set()
for x in probs:
    if x in seen: continue
    seen.add(x)
    print('\t'.join(x))
n = len(seen)
# トップの立場のパネルごとのツールの本数(2026/11/23 本人「ジャンルのパネルもあるのにさ、全くツールなくない？」)。
# 3本に満たないパネルを「注意」として毎回出す(公開は止めない)。題材の候補を作るときに先に埋める。
_top = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
for _m in re.finditer(r'<div class="pnl[^"]*" id="(p\d+)" role="tabpanel">(.*?)<a class="go', _top, re.S):
    _k = len(re.findall(r'<li><a href="/', _m.group(2)))
    if _k < 3:
        print('注意\tindex.html\tトップの立場のパネル %s のツールが %d 本(3本に満たない)' % (_m.group(1), _k))
print('問題 %d 件' % n)
if n == 0:
    open(OK, 'w').write('ok\n')
