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
HYCSS = '.hy1{margin:20px 0 4px}.hy1 h2{margin-top:0}.lead2{margin:14px 0 0;font-weight:700}'
LEAD = '<p class="lead2">自分の数字で計算したい人は、下に入力してください。</p>\n'
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
    for x, y in (('上で入力した', '下で入力した'), ('上で選んだ', '下で選んだ'), ('上の計算', '下の計算'), ('上の入力', '下の入力')):
        sec = re.sub('(?<!以)' + x, y, sec)
    s = s[:k] + '<section class="hy1">\n' + sec + LEAD + '</section>\n\n' + s[k:]
    if HYCSS not in s:
        s = s.replace('</style>', HYCSS + '</style>', 1)
    return s

changed = 0
for f in sorted(glob.glob(os.path.join(SITE, '*', 'index.html'))):
    me = os.path.basename(os.path.dirname(f))
    s = open(f, encoding='utf-8').read()
    o = s
    s = hayami_first(me, s)
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
    if s != o:
        open(f, 'w', encoding='utf-8').write(s)
        changed += 1

print('finish.py: 書き換えたページ', changed)
