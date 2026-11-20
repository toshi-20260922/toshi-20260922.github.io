# /(トップページ site/index.html)全ページへの入口。計算ツールのページではないので、行き先のページと食い違っていないかを数える。
# 照らす相手(一次情報は行き先の各ページの突き合わせ tools/seikaku/<住所>.py が持つ。トップはそのページの画面の数字と比べる):
#  1 内部リンク:行き先の site/<住所>/index.html があるか。tools/pages.json の全ページがトップから1つ以上リンクされているか。
#    都道府県の最低賃金(/saitei-chingin-*/)はトップにパネルもリンクも置かない。「最低賃金の一覧」(/saitei-chingin/)が
#    実在する県のページへ全部リンクしていれば、そこから到達したと数える(2026-11-20 オーナー指示)。
#  2 名前:メニュー・立場別の一覧・カードの文字は、行き先の title と h1 の【】の中の言葉と同じか。
#    ヒーローのタイルやタブの短い名前は、「早見表」で終わるものは【】の言葉と「の」を除いて同じか。ほかは言葉が行き先の題名か見出しにあるか。
#  3 数字:タイル・よく聞かれること・カードの数字と、ヒーローの4つのタブ・国保と任意継続の比較の結果を、行き先のページを開いて同じ条件で読んだ結果と比べる。
#    ヒーローの「法人成りの分岐点 早見表」(役員報酬 月30万円)は、行き先が万円の整数なので、下の自分の計算(整数)で0.1万円まで出して比べる。
#    自分の計算の一次情報(法令・公的資料):
#     国税庁 No.2260 所得税の税率 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2260.htm
#     国税庁 No.1410 給与所得控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1410.htm
#     国税庁 No.1199 基礎控除 https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1199.htm
#     国税庁 No.5759 法人税の税率 https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5759.htm
#     東京都主税局「個人住民税」 https://www.tax.metro.tokyo.lg.jp/kazei/life/kojin_ju ・「個人事業税」 https://www.tax.metro.tokyo.lg.jp/kazei/work/kojin_ji
#     全国健康保険協会「令和8年3月分(4月納付分)からの健康保険・厚生年金保険の保険料額表(東京都)」 https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf
#     港区「国民健康保険料」(東京23区の令和8年度の料率) https://www.city.minato.tokyo.jp/shikaku/kurashi/hoken/kenkohoken/hokenryo.html
#     日本年金機構「国民年金保険料」(令和8年度 月17,920円) https://www.nenkin.go.jp/service/kokunen/hokenryo/hokenryo.html
#    この回(2026-11-20)は公的サイトを開き直していない。定数は同じ日に /houjinnari/ の係が確かめた tools/seikaku/houjinnari.py と同じ値で、
#    自分の計算が行き先の早見表(万円の整数)と全行で合うことをこの突き合わせの中で確かめている。
#  4 年・年度:今日(2026-11-20=令和8年)で正しいか。ページの数を書いていれば pages.json の数と合うか。
#  5 構造化データ(JSON-LD)・canonical・og。
# 最後に確かめた日: 2026-11-20
import os, re, sys, json, asyncio
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import SITE, ROOT, done
from playwright.async_api import async_playwright

TOP = os.path.join(SITE, 'index.html')
PAGES = json.load(open(os.path.join(ROOT, 'tools', 'pages.json'), encoding='utf-8'))
REIWA, SEIREKI, KYOU = 8, 2026, '2026年11月20日'

# ---- 自分の計算(整数。ヒーローの法人成りの表だけに使う) ----
STD = [58, 68, 78, 88, 98, 104, 110, 118, 126, 134, 142, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300,
       320, 340, 360, 380, 410, 440, 470, 500, 530, 560, 590, 620, 650, 680, 710, 750, 790, 830, 880, 930, 980,
       1030, 1090, 1150, 1210, 1270, 1330, 1390]
LIM = [63, 73, 83, 93, 101, 107, 114, 122, 130, 138, 146, 155, 165, 175, 185, 195, 210, 230, 250, 270, 290, 310,
       330, 350, 370, 395, 425, 455, 485, 515, 545, 575, 605, 635, 665, 695, 730, 770, 810, 855, 905, 955, 1005,
       1055, 1115, 1175, 1235, 1295, 1355]
SOKUSAN = [(1950000, 5, 0), (3300000, 10, 97500), (6950000, 20, 427500), (9000000, 23, 636000),
           (18000000, 33, 1536000), (40000000, 40, 2796000), (None, 45, 4796000)]
KOKUHO23 = [(751, 47600, 670000), (280, 17600, 260000), (27, 1873, 30000)]     # 40歳未満:医療・支援金・子ども分(所得割×1万分の1, 均等割, 上限)

def std(m):
    for s, t in zip(STD, LIM):
        if m < t * 1000: return s * 1000
    return 1390000
def half(x):
    q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q
def r_half_up(x): return (x + F(1, 2)).__floor__()
def kyuyo(x):
    if x < 741000: return 0
    if x < 2191000: return x - 740000
    if x < 2193000: return 1451000
    if x < 2196000: return 1453000
    if x < 2200000: return 1456000
    if x < 6600000:
        a = x // 4000 * 4000
        return a * 7 // 10 - 80000 if x < 3600000 else a * 8 // 10 - 440000
    if x < 8500000: return x * 9 // 10 - 1100000
    return x - 1950000
def kiso(g):
    for top, v in ((4890000, 1040000), (6550000, 670000), (23500000, 620000), (24000000, 480000), (24500000, 320000), (25000000, 160000)):
        if g <= top: return v
    return 0
def kiso_ju(g):
    for top, v in ((24000000, 430000), (24500000, 290000), (25000000, 150000)):
        if g <= top: return v
    return 0
def shotokuzei(t):
    t = max(0, t) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or t <= top:
            return (t * r // 100 - d) * 1021 // 1000 // 100 * 100
def jumin(g, sh):
    if g <= 450000: return 0
    t = max(0, g - sh - kiso_ju(g)) // 1000 * 1000
    adj = 0 if g > 25000000 else (min(50000, t) if t <= 2000000 else 50000)
    return max(0, t * 6 // 100 - adj * 3 // 100) // 100 * 100 + max(0, t * 4 // 100 - adj * 2 // 100) // 100 * 100 + 5000
def yakuin(m):
    """(本人負担, 会社負担)の月額。協会けんぽ東京都・40歳未満。会社負担=全額(円未満切り捨て)−本人負担+子ども・子育て拠出金(円未満切り捨て)。"""
    s = std(m); p = min(max(s, 88000), 650000)
    ken = half(F(s * (985 + 23), 20000)); nen = half(F(p * 1830, 20000))
    return ken + nen, s * (985 + 23) // 10000 + p * 1830 // 10000 - ken - nen + p * 36 // 10000
def kojin_futan(a):
    """個人事業のままの税金・社会保険料の合計(青色申告65万円・東京23区の国保・国民年金・個人事業税5%)。"""
    g = max(0, a - min(650000, a)); base = max(0, g - 430000)
    red = 7 if g <= 430000 else (5 if g <= 740000 else (2 if g <= 1000000 else 0))
    sh = sum(min(c, base * r // 10000 + k * (10 - red) // 10) for r, k, c in KOKUHO23) + 17920 * 12
    jg = max(0, a - 2900000) // 1000 * 1000 * 5 // 100 // 100 * 100
    return shotokuzei(g - sh - kiso(g)) + jumin(g, sh) + jg + sh
def jigyo(a):
    jg = (min(a, 4000000) * 35 + max(0, min(a, 8000000) - 4000000) * 53 + max(0, a - 8000000) * 70) // 1000 // 100 * 100
    return jg, jg * 37 // 100 // 100 * 100
def corp(p):
    """会社に残した利益にかかる法人税など(均等割7万円を含む)。前の年の分の法人事業税・特別法人事業税を引いた所得で出す。"""
    i = p
    for _ in range(30):
        i = p - sum(jigyo(max(0, i) // 1000 * 1000))
    a = max(0, i) // 1000 * 1000
    hz = (min(a, 8000000) * 150 + max(0, a - 8000000) * 232) // 1000 // 100 * 100
    kz = hz // 1000 * 1000
    return (hz + kz * 103 // 1000 // 100 * 100 + max(0, kz - 5000000) // 1000 * 1000 * 4 // 100 // 100 * 100 + sum(jigyo(a))
            + kz * 1 // 100 // 100 * 100 + kz * 6 // 100 // 100 * 100 + 70000)
def houjin_futan(a, m):
    """役員報酬を月 m 円にして残りを会社に残すときの税金・社会保険料の合計。"""
    me, co = yakuin(m); r = m * 12; g = kyuyo(r); p = a - r - co * 12
    return me * 12 + co * 12 + shotokuzei(g - me * 12 - kiso(g)) + jumin(g, me * 12) + (corp(p) if p > 0 else 70000)

def num(t):
    s = ''.join(ch for ch in t if ch.isdigit() or ch == '.')
    v = F(s or '0')
    return -v if ('−' in t or t.strip().startswith('-')) else v
def nums(t): return [int(x.replace(',', '')) for x in re.findall(r'\d[\d,]*', t)]
def man1(v):
    """0.1万円まで(四捨五入)の文字。"""
    x = r_half_up(F(abs(v), 1000)); s = '{:,}.{}'.format(x // 10, x % 10)
    return s
def strip(t): return re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', t))
def kakko(t):
    m = re.match(r'\s*【(.+?)】', t)
    return m.group(1) if m else ''
def nashi(t): return re.sub(r'[の\s　]', '', t)

SET_INC = """([pre, id, vals, outs])=>{var $=function(i){return document.getElementById(i)};
 pre.forEach(function(p){var e=$(p[0]);if(p[1]==='click'){var b=document.querySelector(p[0]);if(!b.classList.contains('on'))b.click();}
  else if(String(e.value)!==String(p[1])){e.value=String(p[1]);e.dispatchEvent(new Event('change',{bubbles:true}));}});
 var inc=$(id);return vals.map(function(v){inc.value=String(v);inc.dispatchEvent(new Event('input',{bubbles:true}));
  return outs.map(function(o){return $(o).textContent})})}"""
TOP_TAB = """([i, vals])=>{document.querySelector('.tabs button[data-t="'+i+'"]').click();var sl=document.getElementById('sl');
 return vals.map(function(v){sl.value=String(v);sl.dispatchEvent(new Event('input',{bubbles:true}));
  var hit=document.querySelector('#tb tr.hit');
  return {v:document.getElementById('sl-v').textContent,hit:hit?[].map.call(hit.children,function(c){return c.textContent}):null,
   rows:[].map.call(document.querySelectorAll('#tb tr'),function(r){return [].map.call(r.children,function(c){return c.textContent})}),
   card:document.getElementById('rc').innerText.replace(/\\s+/g,' '),nt:document.getElementById('nt').textContent,
   link:[document.getElementById('tlink').getAttribute('href'),document.getElementById('tlink').textContent]}})}"""

async def main():
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1
            if bad <= 60: print('NG', label, '| トップ:', got, '| 行き先・正:', want)
            elif os.environ.get('ALL'): print('NG', label)
    raw = open(TOP, encoding='utf-8').read()
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 390, 'height': 800})
        dp = await b.new_page(viewport={'width': 390, 'height': 800})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('file://' + TOP)
        async def go(slug):
            await dp.goto('file://' + os.path.join(SITE, slug, 'index.html'))
        MAIN = {}
        async def maintext(slug):
            if slug not in MAIN:
                await go(slug); MAIN[slug] = ''.join((await dp.inner_text('main')).split())
            return MAIN[slug]

        # ---- 1 内部リンク ----
        links = await pg.evaluate("""()=>[...document.querySelectorAll('a[href]')].map(a=>{var c=a.closest('.dd')?'menu':a.closest('ul.lk')?'lk':a.closest('ul.cards')?'card':
          a.closest('.ph')?'ph':a.closest('.pop')?'pop':a.classList.contains('lap')?'lap':a.id==='tlink'?'tlink':a.closest('.sim')?'sim':'other';
          var nm=c==='card'?a.querySelector('b').textContent:(c==='ph'||c==='pop')?a.querySelector('span').textContent:c==='lap'?a.getAttribute('aria-label'):a.textContent;
          return [a.getAttribute('href'),c,nm.replace(/\\s+/g,' ').trim(),a.textContent.replace(/\\s+/g,' ').trim()]})""")
        inner = [l for l in links if l[0].startswith('/')]
        for h, c, nm, _ in inner:
            f = os.path.join(SITE, h.strip('/').split('#')[0], 'index.html') if h.strip('/') else TOP
            chk('リンク先がある %s (%s)' % (h, c), os.path.exists(f), True)
        hs = set(l[0] for l in inner)
        chk('pages.json のページの数', len(PAGES), 59)
        # 都道府県の最低賃金はトップに直接置かず、「最低賃金の一覧」から開く。
        list_html = open(os.path.join(SITE, 'saitei-chingin', 'index.html'), encoding='utf-8').read()
        list_hrefs = set(re.findall(r'href="(/[^"#?]*/)"', list_html))
        existing_prefs = ['/' + name + '/' for name in sorted(os.listdir(SITE))
                          if name.startswith('saitei-chingin-') and os.path.isfile(os.path.join(SITE, name, 'index.html'))]
        for pth in existing_prefs:
            chk('最低賃金の一覧からリンク ' + pth, pth in list_hrefs, True)
        via_list = {p for p in existing_prefs if p in list_hrefs} if '/saitei-chingin/' in hs else set()
        for q in PAGES:
            path = q['path']
            chk('トップからリンクされている ' + path, path in hs or (path.startswith('/saitei-chingin-') and path in via_list), True)
        ids = set(re.findall(r'\bid="([^"]+)"', raw))
        for h, c, nm, _ in links:
            if h.startswith('#'):
                chk('ページ内リンクの行き先 ' + h, h[1:] in ids, True)
        for h, c, nm, _ in links:
            if h.startswith('http'):
                chk('外のリンク ' + h[:60], h in ('https://oyama-toshiro.com/contact/', 'https://oyama-toshiro.com/yuushi/',
                    'https://docs.google.com/forms/d/e/1FAIpQLSdCmggUpJpkXMiAnXkkmfbaIrG52Zuw7ZrqjgEnsfj6xTIzhQ/viewform'), True)
        # CTA の出口:「経理丸投げの無料相談」と書いたリンクは全部 contact へ
        for h, c, nm, tx in links:
            if '無料相談' in tx:
                chk('CTA の出口 ' + tx[:30], h, 'https://oyama-toshiro.com/contact/')

        # ---- 2 名前 ----
        TITLE = {}
        for q in PAGES:
            r = open(os.path.join(SITE, q['path'].strip('/'), 'index.html'), encoding='utf-8').read()
            t = re.search(r'<title>(.*?)</title>', r, re.S).group(1).strip()
            h1 = strip(re.search(r'<h1[^>]*>(.*?)</h1>', r, re.S).group(1))
            h2 = [strip(x) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', r, re.S)]
            TITLE[q['path']] = (t, h1, h2)
            chk('title と h1 の【】が同じ ' + q['path'], kakko(t), kakko(h1))
        for h, c, nm, _ in inner:
            if h not in TITLE: continue
            t, h1, h2 = TITLE[h]; k = kakko(t)
            if c in ('menu', 'lk', 'card'):
                chk('名前 %s (%s)' % (h, c), nm, k)
            else:
                s = re.sub(r'(を開く|を開く →| →)$', '', nm.replace(' →', '')).strip()
                s = re.sub(r'を開く$', '', s)
                if s.endswith('早見表') and k.endswith('早見表'):
                    chk('短い名前 %s (%s)' % (h, c), nashi(s), nashi(k))
                elif s.endswith('早見表'):
                    chk('短い名前 %s (%s)' % (h, c), any(nashi(s) == nashi(x)[:len(nashi(s))] for x in h2), True)
                else:
                    mt = await maintext(h.strip('/'))
                    words = [w for w in re.split(r'[のとを\s]|だけ|詳しく|計算する', s) if w]
                    chk('短い名前の言葉 %s (%s) %s' % (h, c, s), [w for w in words if w not in t and w not in mt], [])
        tabs = await pg.eval_on_selector_all('.tabs button', 'bs=>bs.map(b=>b.textContent)')
        chk('タブの名前', tabs, ['役員報酬の手取り', '法人成りの分岐点', '個人事業主の手取り', '年収の壁'])
        for nm_, path in zip(tabs, ['/yakuin-tedori/', '/houjinnari/', '/kojin-zei/', '/nenshu-kabe/']):
            t, h1, h2 = TITLE[path]
            chk('タブの名前が行き先の題名か見出しにある ' + nm_, any(nashi(nm_) in nashi(x) for x in [t] + h2), True)

        # ---- 3 数字 ----
        tile = {}
        for li in await pg.eval_on_selector_all('.pop li a', "as=>as.map(a=>[a.getAttribute('href'),a.querySelector('em').firstChild.textContent,a.querySelector('em b').textContent])"):
            tile[li[0]] = (li[1], li[2])
        nby = await pg.inner_text('p.nby')
        qa = await pg.eval_on_selector_all('.pnl', "ps=>ps.map(p=>[p.id].concat(['.q','.a','.n'].map(s=>(p.querySelector('.qa '+s)||{}).textContent||'')))")
        qa = {x[0]: x[1:] for x in qa}
        cards = {}
        for h, s in await pg.eval_on_selector_all('ul.cards a', "as=>as.map(a=>[a.getAttribute('href'),a.querySelector('span').textContent])"):
            cards[h] = s

        # 3-1 年収の壁
        await go('nenshu-kabe')
        wl = await dp.eval_on_selector_all('table.wl tbody tr:not(.g)', "rs=>rs.map(r=>[r.children[0].firstChild.textContent.trim(),r.children[2].firstChild.textContent.trim()])")
        W = dict(wl)
        chk('タイル 所得税の壁', tile['/nenshu-kabe/'], ('所得税の壁', W.get('所得税')))
        chk('壁の表の行の数', len(wl) >= 14, True)
        want_wall = [W.get('住民税（所得割）'), W.get('家族の扶養（下の2つ以外）'), W.get('配偶者控除'), W.get('配偶者特別控除が満額'), W.get('所得税'), W.get('配偶者特別控除がなくなる')]
        chk('扶養控除の壁は配偶者控除と同じ', W.get('扶養控除'), W.get('配偶者控除'))
        WA = [900000, 1190000, 1200000, 1290000, 1300000, 1360000, 1370000, 1690000, 1700000, 1780000, 1790000, 2070000, 2080000, 2200000]   # つまみは1万円きざみ
        r3 = (await pg.evaluate(TOP_TAB, [3, WA]))
        chk('タブ 年収の壁 の金額', [r[0] for r in r3[0]['rows']], want_wall)
        chk('タブ 年収の壁 の言葉', [r[1:3] for r in r3[0]['rows']], [['住民税がかかり始める', '本人の住民税'], ['社会保険の扶養から外れる', '親・配偶者の健康保険'],
            ['扶養控除・配偶者控除が使えなくなる', '親・配偶者の所得税'], ['配偶者特別控除が減り始める', '配偶者の所得税'], ['所得税がかかり始める', '本人の所得税'], ['配偶者特別控除がなくなる', '配偶者の所得税']])
        # 超えた・まだ:社会保険は130万円以上で外れる(行き先の箱の文)。ほかは「超えると」
        wv = [int(num(x) * 10000) for x in want_wall]
        for a, r in zip(WA, r3):
            want = ['超えた' if (a >= w if i == 1 else a > w) else 'まだ' for i, w in enumerate(wv)]
            chk('タブ 年収の壁 %d' % a, [x[3] for x in r['rows']], want)
            chk('タブ 年収の壁 札 %d' % a, '超えている壁 %dつ' % want.count('超えた') in r['card'], True)
        got = await dp.evaluate(SET_INC, [[['#s-who button[data-v="0"]', 'click']], 'inc', [1299999, 1300000], ['o-vd']])
        chk('行き先 130万円ちょうどで外れる', ['外れ' in got[0][0], '外れ' in got[1][0]], [False, True])
        chk('タブ 年収の壁 の注', r3[0]['nt'].startswith('令和%d年分以降（住民税は令和%d年度以降）の数字。住民税は単身・1級地の目安。社会保険は家族の扶養（%s）の場合。' % (REIWA, REIWA + 1, W.get('家族の扶養（下の2つ以外）'))), True)
        chk('行き先 住民税の壁は単身・1級地で令和9年度から', '単身・1級地の目安。令和7年の欄は令和8年度、令和8・9年の欄は令和9・10年度の住民税' in await maintext('nenshu-kabe'), True)
        chk('質問 扶養 答え', qa['p3'][1], '年収%s未満' % W.get('家族の扶養（下の2つ以外）'))
        chk('質問 扶養 注', qa['p3'][2], '19〜22歳は%s未満、60歳以上は%s未満' % (W.get('19〜22歳の扶養'), W.get('60歳以上・障害のある人の扶養')))
        chk('カード 年収の壁', cards['/nenshu-kabe/'], '住民税・所得税・扶養・社会保険の壁を、令和%d年と並べて一覧に' % (REIWA - 1))
        chk('行き先 表の頭', await dp.eval_on_selector_all('table.wl thead th', 'ts=>ts.map(t=>t.textContent)'), ['年収の壁', '令和7年', '令和8・9年', 'もとの制度'])

        # 3-2 社会保険料・雇用保険料・源泉徴収・住民税・年収の手取り
        await go('shakaihoken')
        got = await dp.evaluate(SET_INC, [[['pref', 12], ['.seg button[data-a="0"]', 'click']], 'pay', [300000], ['o-me']])
        chk('タイル 社会保険料', tile['/shakaihoken/'], ('月給30万円', '月' + got[0][0]))
        chk('質問 社会保険料', qa['p2'][1:], ['本人%s／月' % got[0][0], '協会けんぽ東京都・40歳未満・令和%d年度' % REIWA])
        await go('koyohoken')
        await dp.click('.seg button[data-t="0"]'); await dp.fill('#pay', '300000')
        chk('タイル 雇用保険料', tile['/koyohoken/'], ('月給30万円', '月' + await dp.inner_text('#o-me')))
        chk('カード 雇用保険料', cards['/koyohoken/'].startswith('令和%d年度の料率で' % REIWA) and '令和%d年度' % REIWA in TITLE['/koyohoken/'][0], True)
        await go('gensen-hoshu')
        await dp.select_option('#kind', '0'); await dp.select_option('#who', '0'); await dp.select_option('#payer', '0'); await dp.fill('#amt', '100000')
        chk('タイル 源泉徴収', tile['/gensen-hoshu/'], ('報酬10万円', await dp.inner_text('#o-t')))
        chk('カード 源泉徴収', ('10.21%' in cards['/gensen-hoshu/'], await dp.inner_text('#o-f')), (True, '支払う金額×10.21%'))
        await go('juminzei')
        got = await dp.evaluate(SET_INC, [[['#s-sh button[data-v="1"]', 'click'], ['#s-age button[data-v="0"]', 'click']], 'inc', [5000000], ['o-y']])
        seg = await dp.eval_on_selector_all('#s-sh button.on, #s-age button.on', 'bs=>bs.map(b=>b.textContent)')
        chk('行き先 住民税の条件', seg, ['入っている', '40歳未満'])
        chk('タイル 住民税', tile['/juminzei/'], ('年収500万円', '年%s万円' % man1(int(num(got[0][0])))))
        await go('tedori')
        got = await dp.evaluate(SET_INC, [[['pref', 12], ['#s-age button:nth-child(1)', 'click']], 'inc', [5000000], ['o-y', 'o-m']])
        ty, tm = int(num(got[0][0])), int(num(got[0][1]))
        chk('タイル 年収の手取り', tile['/tedori/'], ('年収500万円', '約%d万円' % r_half_up(F(ty, 10000))))
        chk('ヒーローの注', nby.startswith('表は令和%d年分・東京都・40歳未満・扶養なしの目安です（年収500万円の手取りは月あたり約%s万円）。' % (REIWA, man1(tm))), True)
        chk('カード 年収の手取り', (cards['/tedori/'].startswith('年収100万円から2,000万円までの手取り'), '年収100万〜2,000万円' in TITLE['/tedori/'][0]), (True, True))

        # 3-3 副業
        mt = await maintext('fukugyo')
        chk('タイル 副業', (tile['/fukugyo/'], '副業が給料以外で、所得が20万円を超える要る' in mt), (('所得20万円超は', '申告が要る'), True))

        # 3-4 役員報酬の手取り(タイルとタブの全部の目盛り)
        ms = list(range(100000, 1500001, 10000))
        await go('yakuin-tedori')
        dst = await dp.evaluate(SET_INC, [[['pref', 12], ['#s-age button:nth-child(1)', 'click']], 'inc', ms, ['o-m', 'o-y', 'o-c', 'o-r', 'o-br']])
        topv = await pg.evaluate(TOP_TAB, [0, ms])
        chk('タブ 役員報酬 リンク', topv[0]['link'], ['/yakuin-tedori/', '役員報酬の手取り早見表を開く →'])
        for m, d_, t_ in zip(ms, dst, topv):
            om, oy, oc = int(num(d_[0])), int(num(d_[1])), int(num(d_[2])); br = nums(d_[4])
            rate = d_[3].replace('手取り率', '').strip()
            if m % 50000 == 0:
                chk('タブ 役員報酬 行 %d' % m, t_['hit'], ['%s万円' % '{:,}'.format(m // 10000), '{:,}'.format(br[0]), '{:,}'.format(br[1]), '{:,}'.format(br[2]), '{:,}'.format(om), rate])
            chk('タブ 役員報酬 札 %d' % m, [x in t_['card'] for x in ('手取り（月あたり） {:,}円'.format(om), '手取り率 %s（年間報酬 %s円の内訳）' % (rate, '{:,}'.format(m * 12)),
                '社会保険料（本人） {:,}円 所得税 {:,}円 住民税 {:,}円 手取り {:,}円'.format(br[0], br[1], br[2], oy), '会社負担込みの総コスト（年） {:,}円'.format(oc))], [True] * 4)
        i50 = ms.index(500000)
        chk('タイル 役員報酬', tile['/yakuin-tedori/'], ('月50万円の手取り', '月%d万円' % r_half_up(F(int(num(dst[i50][0])), 10000))))
        chk('タブ 役員報酬 の注', topv[0]['nt'].startswith('40歳未満・令和%d年分・協会けんぽ東京都。単身・賞与なし。役員は雇用保険に入らないので雇用保険料は含めていません。住民税は前の年も同じ報酬だった場合。' % REIWA), True)
        chk('タブ 役員報酬 はじめの値', (await pg.evaluate("()=>{document.querySelector('.tabs button[data-t=\"0\"]').click();return 1}"), raw.count('v:500000,step:50000')), (1, 1))

        # 3-5 個人事業主の手取り(タブの全部の目盛り)と「よく聞かれること」
        ps = list(range(2000000, 20000001, 100000))
        await go('kojin-zei')
        dst = await dp.evaluate(SET_INC, [[['reg', 0], ['#s-ao button:nth-child(1)', 'click'], ['#s-age button[data-v="0"]', 'click']], 'inc', ps, ['o-n', 'o-br', 'o-sh', 'o-nr']])
        chk('行き先 個人事業の条件', await dp.eval_on_selector_all('#s-ao button.on, #s-age button.on', 'bs=>bs.map(b=>b.textContent)'), ['65万円', '40歳未満'])
        topv = await pg.evaluate(TOP_TAB, [2, ps])
        chk('タブ 個人事業 リンク', topv[0]['link'], ['/kojin-zei/', '個人事業主の手取り早見表を開く →'])
        KO = {}
        for a, d_, t_ in zip(ps, dst, topv):
            te = int(num(d_[0])); it, ju, jg = nums(d_[1]); ko, nen = nums(d_[2]); KO[a] = te
            r1 = r_half_up(F(te * 1000, a)); rate = '%d.%d%%' % (r1 // 10, r1 % 10)
            tm_ = r_half_up(F(te, 12))
            if a % 500000 == 0:
                chk('タブ 個人事業 行 %d' % a, t_['hit'], ['%s万円' % '{:,}'.format(a // 10000), '{:,}'.format(it + ju), '{:,}'.format(jg), '{:,}'.format(ko + nen), '{:,}'.format(tm_), rate])
            chk('タブ 個人事業 札 %d' % a, [x in t_['card'] for x in ('手取り（月あたり） {:,}円'.format(tm_), '手取り率 %s（1年の手取り %s円）' % (rate, '{:,}'.format(te)),
                '所得税 {:,}円 住民税 {:,}円 個人事業税 {:,}円 国保・年金 {:,}円 手取り {:,}円'.format(it, ju, jg, ko + nen, te), '税金・保険料の合計（年） {:,}円'.format(a - te))], [True] * 4)
            chk('自分の計算 個人事業 %d' % a, kojin_futan(a), a - te)
        chk('タブ 個人事業 の注', topv[0]['nt'].startswith('40歳未満・単身・所得税は令和%d年分、住民税は令和%d年度。青色申告65万円控除・東京23区の国保（令和%d年度）・国民年金。個人事業税は税率5%%の業種。' % (REIWA, REIWA + 1, REIWA)), True)
        chk('質問 個人事業 問い', qa['p4'][0], 'よく聞かれること：個人事業の利益が500万円なら、税金と社会保険料の合計は？')
        chk('質問 個人事業 答え', qa['p4'][1], '年%s万円' % man1(5000000 - KO[5000000]))
        chk('質問 個人事業 注', qa['p4'][2], '40歳未満・単身・東京23区・令和%d年分。法人成りの分岐点 早見表の「個人事業のまま」の額' % REIWA)
        chk('カード 個人事業', (cards['/kojin-zei/'].startswith('利益200万〜2,000万円の'), '利益200万〜2,000万円' in TITLE['/kojin-zei/'][0]), (True, True))

        # 3-6 法人成り(タブ:全額を役員報酬にした比較。ヒーローの表:役員報酬 月30万円)
        ps = list(range(3000000, 20000001, 100000))
        await go('houjinnari')
        dst = await dp.evaluate(SET_INC, [[['reg', 0], ['pref', 12], ['#s-age button:nth-child(1)', 'click']], 'inc', ps, ['o-k', 'o-h', 'o-d', 'o-1']])
        topv = await pg.evaluate(TOP_TAB, [1, ps])
        chk('タブ 法人成り リンク', topv[0]['link'], ['/houjinnari/', '法人成りの分岐点 早見表を開く →'])
        for a, d_, t_ in zip(ps, dst, topv):
            k, h = int(num(d_[0])), int(num(d_[1])); df = h - k; m = nums(d_[3])[0]
            chk('行き先 法人成りの差 %d' % a, int(num(d_[2])), df)
            if a % 1000000 == 0:
                chk('タブ 法人成り 行 %d' % a, t_['hit'], ['%s万円' % '{:,}'.format(a // 10000), '{:,}'.format(k), '{:,}'.format(h), ('+' if df >= 0 else '−') + '{:,}'.format(abs(df))])
            chk('タブ 法人成り 札 %d' % a, [x in t_['card'] for x in (('法人にしたほうが多い額（年）' if df >= 0 else '個人事業のほうが多い額（年）') + ' {:,}円'.format(abs(df)),
                '手取りは個人事業で {:,}円、法人にすると {:,}円'.format(k, h), '法人の役員報酬（月） {:,}円'.format(m))], [True] * 3)
        chk('タブ 法人成り の注', topv[0]['nt'].startswith('40歳未満・単身・令和%d年分。個人事業は青色申告65万円控除・東京23区の国保。法人は利益を全部役員報酬にし、協会けんぽ東京都・均等割7万円。' % REIWA), True)
        # 行き先の早見表(40歳未満)の「個人事業のまま」「報酬月30万」の列
        hy = await dp.eval_on_selector_all(':is(#bunki ~ .tw):not(#bunki ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(c=>c.textContent))")
        hd = await dp.eval_on_selector_all(':is(#bunki ~ .tw):not(#bunki ~ .tw ~ .tw) thead th', "ts=>ts.map(t=>t.textContent)")
        chk('行き先 早見表の列', hd[:3], ['事業の利益（年）', '個人事業のまま', '報酬月20万'])
        c30 = hd.index('報酬月30万')
        HY = {int(num(r[0])): (int(num(r[1])), int(num(r[c30]))) for r in hy}
        for pm, (ko_, df_) in HY.items():                     # 自分の計算が行き先の表の全行と合うか
            a = pm * 10000
            chk('自分の計算 個人事業のまま %d' % pm, r_half_up(F(kojin_futan(a), 10000)), ko_)
            d30 = kojin_futan(a) - houjin_futan(a, 300000)
            chk('自分の計算 報酬月30万 %d' % pm, (1 if d30 >= 0 else -1) * r_half_up(F(abs(d30), 10000)), df_)
        lap = await pg.eval_on_selector_all('a.lap tbody tr', "rs=>rs.map(r=>[r.className].concat([...r.children].map(c=>c.textContent)))")
        chk('ヒーローの表 題', await pg.eval_on_selector('a.lap .pt', "e=>[e.querySelector('b').textContent,e.querySelector('span').textContent]"),
            ['法人成りの分岐点 早見表', '役員報酬が月30万円のとき。税金・社会保険料の合計の目安'])
        chk('ヒーローの表 頭', await pg.eval_on_selector_all('a.lap thead th', 'ts=>ts.map(t=>t.textContent)'), ['事業の利益', '個人事業のまま', '法人', '差（年額）'])
        want = []
        first = None
        for pm in (500, 600, 800, 1000):
            a = pm * 10000; ko_ = kojin_futan(a); ho_ = houjin_futan(a, 300000); d30 = ko_ - ho_
            if first is None and d30 > 0: first = pm
            want.append(['hl' if pm == first else '', '{:,}万円'.format(pm), man1(ko_) + '万円', man1(ho_) + '万円', ('+' if d30 >= 0 else '−') + man1(d30) + '万円'])
            chk('ヒーローの表 %d は行き先の表にある' % pm, pm in HY, True)
        chk('ヒーローの表', lap, want)
        # 月30万円の分岐点:行き先の「3. 役員報酬を月30万円にする場合」の文(10万円きざみ)
        mt = await maintext('houjinnari')
        m_ = re.search(r'3\.役員報酬を月30万円にする場合利益([\d,]+)万円から、法人のほうが軽くなります', mt)
        chk('行き先 月30万円の分岐点の文', bool(m_), True)
        last = 0
        for a in range(3000000, 30000001, 100000):
            if kojin_futan(a) - houjin_futan(a, 300000) <= 0: last = a
        chk('自分の計算 月30万円の分岐点', '{:,}'.format((last + 100000) // 10000), m_.group(1) if m_ else '')
        chk('質問 法人成り 問い', qa['p1'][0], 'よく聞かれること：役員報酬を月30万円にするなら、法人成りは利益いくらから？')
        chk('質問 法人成り 答え', qa['p1'][1], '利益%s万円から' % (m_.group(1) if m_ else ''))
        chk('質問 法人成り 注', qa['p1'][2], '40歳未満・単身・東京23区・令和%d年分。税金と社会保険料の合計で比べた場合' % REIWA)
        chk('行き先 前提の見出し', '試算の前提（令和%d年分・東京23区・単身）' % REIWA in TITLE['/houjinnari/'][2], True)

        # 3-7 国保と任意継続の比較(大阪府)
        cs = [(a, o, f) for a in (0, 980000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 6000000, 7000000, 8000000, 10000000, 12000000, 15000000)
              for o in (0, 1) for f in (0, 1, 2, 3)]
        cs += [(a, o, 0) for a in range(1000000, 9000001, 130000) for o in (0, 1)]
        await go('kokuho')
        dst = await dp.evaluate("""cs=>{var $=function(i){return document.getElementById(i)};
          $('reg').value='15';$('reg').dispatchEvent(new Event('change'));$('pref').value='26';$('pref').dispatchEvent(new Event('change'));
          document.querySelector('#s-hi button[data-v="0"]').click();
          var o=cs.map(function(c){document.querySelector('#s-age button[data-v="'+c[1]+'"]').click();$('fam').value=String(c[2]);$('fam').dispatchEvent(new Event('change'));
            $('inc').value=String(c[0]);$('inc').dispatchEvent(new Event('input'));return [$('o-k').textContent,$('o-n').textContent]});
          return {o:o,reg:$('reg').options[$('reg').selectedIndex].textContent,pref:$('pref').options[$('pref').selectedIndex].textContent,
            hi:document.querySelector('#s-hi button.on').textContent,fam:[...$('fam').options].map(function(x){return x.textContent})}}""", cs)
        chk('行き先 国保の条件', [dst['reg'][:3], dst['pref'][:3], dst['hi']], ['大阪市', '大阪府', '自己都合'])
        chk('行き先 家族の選択肢の数', len(dst['fam']) >= 4, True)
        topv = await pg.evaluate("""cs=>{var $=function(i){return document.getElementById(i)};
          return cs.map(function(c){document.querySelector('#kold button[data-v="'+c[1]+'"]').click();$('kf').value=String(c[2]);$('kf').dispatchEvent(new Event('change'));
            $('ka').value=String(c[0]);$('ka').dispatchEvent(new Event('input'));return ['ko-k','ko-n','ko-w','ko-d'].map(function(i){return $(i).textContent})})}""", cs)
        for c, d_, t_ in zip(cs, dst['o'], topv):
            k, nn = int(num(d_[0])), int(num(d_[1]))
            w = '国民健康保険のほうが安い' if k < nn else ('任意継続のほうが安い' if k > nn else '同じ額')
            chk('国保と任意継続 %s' % (c,), t_, ['{:,}円'.format(k), '{:,}円'.format(nn), w, '' if k == nn else '年{:,}円'.format(abs(k - nn))])
        chk('国保と任意継続 の注', await pg.inner_text('.sim .sc p.nt'), '大阪府・令和%d年度・自己都合の退職・家族は収入なしの場合。任意継続は月給を年収÷12とした標準報酬月額で出しています' % REIWA)
        chk('国保と任意継続 はじめの値', await pg.eval_on_selector('#ka', 'e=>e.getAttribute("value")'), '4000000')
        chk('国保と任意継続 の文', '大阪府の国民健康保険と会社の健康保険の任意継続のどちらが安いかを表示します。' in await pg.inner_text('.sim'), True)
        chk('行き先 題名に令和8年度', '令和%d年度' % REIWA in TITLE['/kokuho/'][0], True)

        # 3-8 贈与税・最低賃金・ほかのカードの数字
        mt = await maintext('zoyozei')
        chk('質問 贈与税', (qa['p5'][1], qa['p5'][2], '110万円' in mt, 'No.4402' in mt or '4402' in open(os.path.join(SITE, 'zoyozei', 'index.html'), encoding='utf-8').read()),
            ('年110万円を超えると', '1年間にもらった合計が110万円以下なら、申告も要りません（国税庁 No.4402）', True, True))
        chk('質問 税務調査', qa['p6'][1:], ['原則、事前に通知がある', '日時・場所・対象の税目などが、あらかじめ電話で伝えられます（国税通則法74条の9）'])
        for h, s in cards.items():
            if h.startswith('/saitei-chingin-'):
                m_ = re.search(r'時給([\d,]+)円', s); t_ = re.search(r'時給([\d,]+)円', TITLE[h][0])
                mt = await maintext(h.strip('/'))
                chk('カード 最低賃金 ' + h, (m_.group(1) if m_ else None, True), (t_.group(1) if t_ else '', ('時給%s円' % (m_.group(1) if m_ else '')) in mt or ('%s円' % (m_.group(1) if m_ else '')) in mt))
                chk('カード 最低賃金 計算の言葉 ' + h, s.endswith('時給・日給・月給で判定'), True)
        # カードの文の中の言葉が行き先のページにあるか(数字・日付・業種の数)
        for h, words in {
            '/saitei-chingin/': ['47都道府県', '発効日'], '/gakusei-kabe/': ['136万円', '150万円', '159万円', '197万円'],
            '/part-fuyou/': ['月8万〜18万円'], '/furusato/': ['2,000円'], '/genbutsu-kyuyo/': ['令和8年4月'], '/kakutei-shinkoku/': ['令和8年分', '口座振替', '決算月'],
            '/hoteifukurihi/': ['47都道府県'], '/chukosha-taiyonensu/': ['2年'], '/niwari-tokurei/': ['3割特例', '簡易課税', '届出'], '/shotoku-kingaku/': ['62万円', '合計所得金額'],
            '/tsukin-teate/': ['駐車場'], '/yatou-hiyou/': ['月給'], '/nenmatsu-chosei/': ['12月'], '/juminzei/': ['0円'],
        }.items():
            mt = await maintext(h.strip('/')); mt += ''.join(TITLE[h][0].split())
            chk('カードの言葉が文にある ' + h, [w for w in words if w not in cards[h]], [])
            chk('カードの言葉が行き先にある ' + h, [w for w in words if w not in mt], [])

        # ---- 4 年・年度・日付・ページの数 ----
        vis = await pg.evaluate("()=>document.body.innerText")
        for i in range(4):
            vis += (await pg.evaluate(TOP_TAB, [i, [1000000]]))[0]['nt']
        ys = sorted(set(re.findall(r'令和\d+年度?分?|20\d\d年(?:\d+月\d+日)?', vis)))
        OK = {'令和%d年' % (REIWA - 1), '令和%d年分' % REIWA, '令和%d年度' % REIWA, '令和%d年度' % (REIWA + 1), '令和%d年' % REIWA, KYOU}
        chk('年・年度の文字', [y for y in ys if y not in OK], [])
        chk('早見表一覧の年度', '令和%d年度の数字に更新済み' % REIWA in vis, True)
        chk('最終更新の日', re.findall(r'最終更新：(\d+年\d+月\d+日)', vis), [KYOU])
        chk('ページの数を書いた文', re.findall(r'\d+\s*(?:の|個の|本の|種類の)(?:ツール|早見表|ページ)', vis), [])
        chk('カードの数', len(cards), len(set(cards)))

        # ---- 5 構造化データ・canonical・og ----
        chk('canonical', re.findall(r'<link rel="canonical" href="([^"]+)">', raw), ['https://taxtable.jp/'])
        chk('og:url', [u for u in re.findall(r'<meta property="og:url" content="([^"]*)">', raw) if u != 'https://taxtable.jp/'], [])
        for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
            d_ = json.loads(s)
            for x in (d_ if isinstance(d_, list) else [d_]):
                if x.get('url'): chk('JSON-LD の url', x['url'], 'https://taxtable.jp/')
                if x.get('name'): chk('JSON-LD の name が画面にある', x['name'] in vis or x['name'] in raw, True)
        chk('title', re.search(r'<title>(.*?)</title>', raw).group(1), '税金と社会保険の早見表｜タックステーブル')
        chk('余った閉じタグ', len(re.findall(r'<span\b', raw)), len(re.findall(r'</span>', raw)))
        await b.close()
    for e in errs:
        print('画面のエラー', e[:120]); bad += 1
    return n, bad

n, bad = asyncio.run(main())
done(n, bad)
