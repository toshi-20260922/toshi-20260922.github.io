# 文の置き換え:tsv(ページ<TAB>元の文<TAB>新しい文)を読んで、HTMLの中の元の文を新しい文に置き換える。
# 元の文の途中にタグ(<span class="nw"> など)があっても見つける。末尾の折り返し止め(nw)は新しい文の最後の5文字に付け直す。
import sys, re, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
miss = 0; done = 0
for line in open(sys.argv[1], encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip() or line.startswith('#'):
        continue
    page, old, new = line.split('\t')
    f = os.path.join(SITE, page)
    s = open(f, encoding='utf-8').read()
    pat = '(?:<[^>]+>)*'.join(re.escape(c) for c in old)
    ms = list(re.finditer(pat, s))
    if not ms:
        print('見つからない', page, old[:40]); miss += 1; continue
    for m in reversed(ms):
        raw = m.group(0)
        rep = new
        if 'class="nw"' in raw and len(new) > 8 and '<' not in new:
            rep = new[:-5] + '<span class="nw">' + new[-5:] + '</span>'
        # 元にあった閉じタグ/開きタグの数がずれないよう、nw 以外のタグを含む場合は残す
        other = [t for t in re.findall(r'<[^>]+>', raw) if 'nw' not in t and t != '</span>']
        if other:
            print('タグを含むので手で直す', page, old[:40]); miss += 1; break
        s = s[:m.start()] + rep + s[m.end():]
        done += 1
    open(f, 'w', encoding='utf-8').write(s)
print('置き換え', done, '見つからない・手で直す', miss)
