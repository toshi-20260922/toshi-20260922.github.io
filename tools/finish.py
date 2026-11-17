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

changed = 0
for f in sorted(glob.glob(os.path.join(SITE, '*', 'index.html'))):
    me = os.path.basename(os.path.dirname(f))
    s = open(f, encoding='utf-8').read()
    o = s
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
