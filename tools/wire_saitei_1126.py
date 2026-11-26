# 2026-11-26 に足す5県だけを書き、一覧と隣の県からリンクする。全都道府県のページは作り直さない。
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_saitei as b

NEW = ['fukushima', 'iwate', 'nara', 'nagasaki', 'miyazaki']
LABEL = {
    'fukushima': ('福島県の最低賃金', '最低賃金 福島県 ふくしま いわき 郡山 時給'),
    'iwate': ('岩手県の最低賃金', '最低賃金 岩手県 いわて 盛岡 時給'),
    'nara': ('奈良県の最低賃金', '最低賃金 奈良県 なら 時給'),
    'nagasaki': ('長崎県の最低賃金', '最低賃金 長崎県 ながさき 佐世保 時給'),
    'miyazaki': ('宮崎県の最低賃金', '最低賃金 宮崎県 みやざき 時給'),
}

def build_pages():
    common = {a[0] for a in b.REL_COMMON}
    for cfg in b.PREFS:
        if cfg['slug'] not in NEW:
            continue
        own = [x for x in cfg['rel'] if x[0] not in common]
        cfg['rel'] = b.rel_for(own)
        print(b.pref_page(cfg))

def pages_json():
    pj = os.path.join(ROOT, 'tools', 'pages.json')
    raw = open(pj, encoding='utf-8').read()
    add = []
    for slug in NEW:
        path = '/saitei-chingin-%s/' % slug
        if path in raw:
            continue
        label, kw = LABEL[slug]
        add.append(' {\n  "path": "%s",\n  "label": "%s",\n  "kw": "%s"\n }' % (path, label, kw))
    if not add:
        return
    raw = raw.rstrip()
    if not raw.endswith(']'):
        raise SystemExit('pages.json')
    raw = raw[:-1].rstrip() + ',\n' + ',\n'.join(add) + '\n]\n'
    open(pj, 'w', encoding='utf-8').write(raw)

def hayami():
    hj = os.path.join(ROOT, 'tools', 'hayami_first.json')
    h = json.load(open(hj, encoding='utf-8'))
    for slug in NEW:
        h['saitei-chingin-' + slug] = 'list'
    json.dump(h, open(hj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(hj, 'a', encoding='utf-8').write('\n')

def sitemap():
    sm = os.path.join(ROOT, 'site', 'sitemap.xml')
    sx = open(sm, encoding='utf-8').read()
    lines = []
    for slug in NEW:
        loc = 'https://taxtable.jp/saitei-chingin-%s/' % slug
        if loc in sx:
            continue
        lines.append('<url><loc>%s</loc><lastmod>2026-11-26</lastmod></url>' % loc)
    if lines:
        sx = sx.replace('</urlset>', '\n'.join(lines) + '\n</urlset>')
        open(sm, 'w', encoding='utf-8').write(sx)

def national():
    fp = os.path.join(ROOT, 'site', 'saitei-chingin', 'index.html')
    s = open(fp, encoding='utf-8').read()
    names = {'福島県': 'fukushima', '岩手県': 'iwate', '奈良県': 'nara', '長崎県': 'nagasaki', '宮崎県': 'miyazaki'}
    for name, slug in names.items():
        old = '<td class="l">%s</td>' % name
        new = '<td class="l"><a href="/saitei-chingin-%s/">%s</a></td>' % (slug, name)
        s = s.replace(old, new)
    s = s.replace('<br>宮崎県</small>', '<br><a href="/saitei-chingin-miyazaki/">宮崎県</a></small>')
    s = s.replace('2026年11月22日の時点で、岩手県・熊本県・沖縄県はまだ発効前です。',
                  '2026年11月26日の時点で、岩手県・熊本県・沖縄県はまだ発効前です。')
    open(fp, 'w', encoding='utf-8').write(s)

def neighbor(slug, text, label, href):
    fp = os.path.join(ROOT, 'site', slug, 'index.html')
    s = open(fp, encoding='utf-8').read()
    if href in s:
        return
    li = '<li>%s<a href="%s" data-cta="rel_%s_%s">%s</a></li>' % (text, href, slug, href.strip('/'), label)
    import re
    s2, n = re.subn(r'(<ul class="rl">.*?)(</ul>)', lambda m: m.group(1) + li + m.group(2), s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('関連リンクを足せない ' + slug)
    open(fp, 'w', encoding='utf-8').write(s2)

def main():
    build_pages()
    pages_json()
    hayami()
    sitemap()
    national()
    neighbor('saitei-chingin-miyagi', '福島県は1,094円で、宮城県より4円低い額です。', '福島県の最低賃金', '/saitei-chingin-fukushima/')
    neighbor('saitei-chingin-miyagi', '岩手県は12月1日から1,090円で、宮城県より8円低い額です。', '岩手県の最低賃金', '/saitei-chingin-iwate/')
    neighbor('saitei-chingin-osaka', '奈良県は1,107円で、大阪府より124円低い額です。', '奈良県の最低賃金', '/saitei-chingin-nara/')
    neighbor('saitei-chingin-kagoshima', '宮崎県は1,085円で、鹿児島県より5円低い額です。', '宮崎県の最低賃金', '/saitei-chingin-miyazaki/')
    neighbor('saitei-chingin-fukuoka', '長崎県は1,087円で、福岡県より27円低い額です。', '長崎県の最低賃金', '/saitei-chingin-nagasaki/')
    print('wire ok')

if __name__ == '__main__':
    main()
