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
def bad(f, kind, detail):
    probs.append((f.replace(SITE + '/', ''), kind, detail))

# 1 HTMLだけで数えるもの
allp = {p['path'].strip('/') for p in PAGES}
for f in files:
    s = open(f, encoding='utf-8').read()
    me = os.path.basename(os.path.dirname(f)) if f.endswith('/index.html') and os.path.dirname(f) != SITE else ''
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
                await pg.close()
        await b.close()
asyncio.run(main())

seen = set()
for x in probs:
    if x in seen: continue
    seen.add(x)
    print('\t'.join(x))
n = len(seen)
print('問題 %d 件' % n)
if n == 0:
    open(OK, 'w').write('ok\n')
