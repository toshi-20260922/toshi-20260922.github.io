# 行の折れ方の検査。文字の位置から実際の行を取り、次を数える。
#   行の頭が助詞（の・を・に・は・が・と・で・も・へ・や など）や「す」「ます」
#   行の終わりが、tools/phrase.py の区切り以外。英字＋助詞＋漢字（「PDFに｜保存」）は BudouX が分けても区切りにしない
#   横にはみ出す
#   本文（main のうち題名の帯の日付以外）が 14px 未満
# 題名の帯の日付（.upd）とフッター・ヘッダーは見ない。
# 使い方: リポジトリの直下で
#   python3 tools/gyou.py                 # 全ページ。給与明細に1件でもあれば終了コード 1
#   python3 tools/gyou.py kyuyo-meisai    # そのページだけ
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phrase
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
WIDTHS = (375, 390, 1280)

JS = r'''() => {
  const root = document.querySelector("main") || document.body;
  const BLOCK = "p,li,h1,h2,h3,h4,h5,h6,td,th,button,a,figcaption,dt,dd,caption,div";
  const skipEl = (el) => !!el.closest(".upd, svg, select, option, script, style");
  const fonts = [];
  const seenFont = new Set();
  const segs = [];
  function addSeg(nodes) {
    const items = [];
    let text = "";
    for (const tn of nodes) {
      const el = tn.parentElement;
      if (!el) continue;
      const fs = parseFloat(getComputedStyle(el).fontSize) || 16;
      if (fs < 14 && !seenFont.has(el)) {
        seenFont.add(el);
        fonts.push({fs: Math.round(fs * 10) / 10, sample: (el.innerText || "").replace(/\s+/g, " ").trim().slice(0, 24)});
      }
      const raw = tn.data || "";
      for (let i = 0; i < raw.length; i++) {
        const ch = raw[i];
        if (ch === "\n" || ch === "\t" || ch === "\r") continue;
        const rg = document.createRange();
        rg.setStart(tn, i); rg.setEnd(tn, i + 1);
        const b = rg.getClientRects()[0];
        if (!b || b.width < 0.5) continue;
        items.push({ch, x: b.left, y: b.top, h: b.height, fs, i: text.length});
        text += ch;
      }
    }
    if (items.length) segs.push({text, items});
  }
  function segments(el) {
    const out = [];
    let buf = [];
    function flush() { if (buf.length) { out.push(buf); buf = []; } }
    function walk(node) {
      if (node.nodeType === 3) {
        if (node.parentElement && !skipEl(node.parentElement)) buf.push(node);
        return;
      }
      if (node.nodeType !== 1 || skipEl(node)) return;
      if (node !== el && node.matches(BLOCK)) { flush(); return; }
      if (node !== el) {
        const d = getComputedStyle(node).display;
        if (d === "block" || d === "flex" || d === "grid" || d === "list-item") {
          flush();
          for (const seg of segments(node)) out.push(seg);
          return;
        }
      }
      for (const c of node.childNodes) walk(c);
    }
    walk(el);
    flush();
    return out;
  }
  const els = [root, ...root.querySelectorAll(BLOCK)];
  for (const el of els) {
    if (skipEl(el)) continue;
    for (const nodes of segments(el)) addSeg(nodes);
  }
  const lines = [];
  function sameRow(r, it) {
    const a0 = r.y, a1 = r.y + r.h, b0 = it.y, b1 = it.y + it.h;
    const overlap = Math.min(a1, b1) - Math.max(a0, b0);
    return overlap > Math.min(r.h, it.h) * 0.45;
  }
  for (const rec of segs) {
    const rows = [];
    for (const it of rec.items) {
      let row = null;
      for (const r of rows) if (sameRow(r, it)) { row = r; break; }
      if (!row) { row = {y: it.y, h: it.h, items: []}; rows.push(row); }
      else {
        row.y = Math.min(row.y, it.y);
        row.h = Math.max(row.y + row.h, it.y + it.h) - row.y;
      }
      row.items.push(it);
    }
    for (const row of rows) {
      row.items.sort((a, b) => a.x - b.x);
      let s = 0;
      while (s < row.items.length && /\s/.test(row.items[s].ch)) s++;
      if (s >= row.items.length) continue;
      const first = row.items[s];
      const last = row.items[row.items.length - 1];
      lines.push({
        text: rec.text,
        head: rec.text.slice(first.i, first.i + 2),
        start: first.i,
        end: last.i + 1,
        sample: row.items.slice(s).map(x => x.ch).join("").trim().slice(0, 28)
      });
    }
  }
  return {
    ov: document.documentElement.scrollWidth - window.innerWidth,
    fonts,
    lines
  };
}'''


def _bad_head(head, start):
    if start <= 0 or not head:
        return False
    if head.startswith('ます') or head.startswith('す'):
        return True
    if head[0] in phrase.PART_ONE:
        return True
    return any(head.startswith(p) for p in phrase.PART_LONG)


def check_page(pg, width):
    data = pg.evaluate(JS)
    issues = []
    if data['ov'] > 1:
        issues.append('はみ出し %dpx 幅%d' % (data['ov'], width))
    for f in data['fonts']:
        issues.append('本文 %gpx「%s」幅%d' % (f['fs'], f['sample'], width))
    seen = set()
    for ln in data['lines']:
        text = ln['text']
        ok = phrase.breaks(text)
        if _bad_head(ln['head'], ln['start']):
            key = ('頭', ln['sample'], width)
            if key not in seen:
                seen.add(key)
                issues.append('行の頭「%s」幅%d' % (ln['sample'], width))
        # BudouX が「PDFに｜保存」のように英字＋助詞と漢字のあいだで分けても、そこは行末にしない。
        cut = phrase.latin_kanji_cut(text, ln['end'])
        if cut or (ln['end'] not in ok and ln['end'] != len(text)):
            key = ('末', ln['sample'], width)
            if key not in seen:
                seen.add(key)
                label = '行の終わり（英字＋助詞＋漢字）' if cut else '行の終わり'
                issues.append('%s「%s」幅%d' % (label, ln['sample'], width))
    return issues


def pages(names):
    out = []
    if names:
        for n in names:
            f = os.path.join(SITE, n, 'index.html') if n != 'index' else os.path.join(SITE, 'index.html')
            if os.path.isfile(f):
                out.append(f)
        return out
    out.append(os.path.join(SITE, 'index.html'))
    for d in sorted(os.listdir(SITE)):
        f = os.path.join(SITE, d, 'index.html')
        if os.path.isfile(f):
            out.append(f)
    return out


def run(names=None):
    files = pages(names)
    counts = {}
    detail = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in files:
            rel = os.path.relpath(f, SITE)
            got = []
            for w in WIDTHS:
                pg = b.new_page(viewport={'width': w, 'height': 800})
                pg.goto('file://' + f, wait_until='load')
                got.extend(check_page(pg, w))
                pg.close()
            # 同じ文が幅で重なるので、文面でまとめる
            uniq = []
            seen = set()
            for x in got:
                if x not in seen:
                    seen.add(x)
                    uniq.append(x)
            counts[rel] = len(uniq)
            detail[rel] = uniq
        b.close()
    return counts, detail


def main():
    names = sys.argv[1:]
    counts, detail = run(names)
    kyuyo = 0
    for rel, n in counts.items():
        if n == 0:
            continue
        name = rel.split(os.sep)[0]
        if name == 'kyuyo-meisai':
            kyuyo = n
            print('給与明細 %d件' % n)
            for x in detail[rel]:
                print('  ' + x)
        else:
            print('%s %d件' % (rel, n))
    zeros = sum(1 for n in counts.values() if n == 0)
    print('見たページ %d  0件 %d  給与明細 %d件' % (len(counts), zeros, counts.get(os.path.join('kyuyo-meisai', 'index.html'), kyuyo)))
    if names == ['kyuyo-meisai'] or not names:
        if counts.get(os.path.join('kyuyo-meisai', 'index.html'), 0):
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
