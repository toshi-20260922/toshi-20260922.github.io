# 説明・注釈の文の点検のために、ページの文を1文ずつ番号を付けて書き出す。
# 使い方:python3 tools/text_units.py <ページの住所>   例 python3 tools/text_units.py furusato
# 書き出すもの:本文(main の中。ページ下のツール一覧は除く)の文・表の注記・よくある質問・構造化データ(FAQPage)の文・題名と説明文。
# 印:[数] 数字や日付が入る文 / [切] 言い切りの文(要りません・できます・なりません 等) / [注] 注記(※・注・小さい字)
import asyncio, json, os, re, sys
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug = sys.argv[1].strip('/')
f = os.path.join(ROOT, 'site', slug, 'index.html') if slug else os.path.join(ROOT, 'site', 'index.html')
KIRI = re.compile(r'(要りません|不要です|必要です|できます|できません|なりません|なります|かかりません|かかります|ありません|対象です|対象外|されます|されません|までです|からです|以上|以下|未満|超える|を超え)')
JS = r'''() => {
 const main = (document.querySelector('main') || document.body).cloneNode(true);
 main.querySelectorAll('nav.tools,script,style').forEach(e => e.remove());
 const out = [];
 const walk = (el, tag) => {
   for (const c of el.children) {
     const t = c.tagName;
     if (['P','LI','TD','TH','H1','H2','H3','H4','DT','DD','FIGCAPTION','SUMMARY','SMALL','LABEL','BUTTON','A'].includes(t) && !c.querySelector('p,li,td,th,h2,h3,dt,dd')) {
       const s = c.innerText.replace(/\s+/g, ' ').trim();
       const cls = (c.className || '') + ' ' + (c.parentElement.className || '');
       if (s) out.push([t.toLowerCase(), /note|chu|small|cap|src/.test(cls) || t === 'SMALL' || /^[※注]/.test(s), s]);
     } else walk(c, t);
   }
 };
 walk(main);
 const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent);
 return {out, ld, title: document.title, desc: (document.querySelector('meta[name=description]') || {}).content || ''};
}'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 390, 'height': 800})
        await pg.goto('file://' + f)
        r = await pg.evaluate(JS)
        await b.close()
    n = 0
    def emit(kind, note, text):
        nonlocal n
        for sen in re.split(r'(?<=。)', text):
            sen = sen.strip()
            if not sen: continue
            n += 1
            m = ('[数]' if re.search(r'[0-9]', sen) else '') + ('[切]' if KIRI.search(sen) else '') + ('[注]' if note else '')
            print('%03d %s %s %s' % (n, kind, m, sen))
    emit('title', False, r['title']); emit('desc', False, r['desc'])
    for kind, note, text in r['out']: emit(kind, note, text)
    for raw in r['ld']:
        try: d = json.loads(raw)
        except Exception: continue
        for q in (d.get('mainEntity') or []) if isinstance(d, dict) else []:
            emit('ld-q', False, q.get('name', '')); emit('ld-a', False, (q.get('acceptedAnswer') or {}).get('text', ''))
    print('文の数 %d' % n)
asyncio.run(main())
