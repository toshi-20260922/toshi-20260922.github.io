# /tedori-gyakusan/ 手取りから年収を逆算(2026-11-22 新規)。
# 自分の計算:tools/seikaku/tedori.py の ref(ページを見ずに書いた手取りの式。11-21 に原本と照らした)を使い、
#   月給を100円きざみで上げて、目標の手取りに初めて届く月給を出す。
# 照らすもの:window.__gyaku の結果(月給・1年の手取り・社会保険料・所得税・住民税)を、47都道府県×2つの年齢×目標の手取りで。
#   届いた月給の100円下では届かないこと(一番低い額か)。早見表2つの全行・計算の箱に直に書いた既定の文字・箱を動かした結果・本文とよくある質問の数字。
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num, SITE
import rates

src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tedori.py'), encoding='utf-8').read()
src = src[:src.index('def r_half_up')].replace('from _lib import run', '')
T = {'__file__': os.path.abspath(__file__)}
exec(compile(src, 'tedori_ref', 'exec'), T)
ref = T['ref']; PREF = T['PREF']

def te(m, r, o): return ref(m * 12, r, o)

def want_m(t, r, o):
    m = 0
    while te(m, r, o)['t'] // 12 < t: m += 100
    return m

def want_y(t, r, o):
    m = 0
    while te(m, r, o)['t'] < t: m += 100
    return m

def f(v): return '{:,}'.format(v)

def pct1(net, a):
    v = (net * 1000 * 2 + a) // (2 * a)
    return '%d.%d' % (v // 10, v % 10)

async def body(pg):
    n = bad = 0
    def chk(lab, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('合わない', lab, got, want)
    async def js(t, k, pi, o):
        return await pg.evaluate('a=>window.__gyaku(a[0],a[1],a[2],a[3])', [t, k, pi, o])
    # 1 47都道府県×年齢×月の手取り
    MT = [0, 1, 50000, 123456, 150000, 200000, 250000, 300000, 412345, 500000, 800000, 1500000]
    cache = {}
    for pi, (p, r) in enumerate(PREF):
        for o in (0, 1):
            ts = MT if p in ('東京都', '大阪府', '佐賀県', '新潟県') else [150000, 300000, 500000]
            for t in ts:
                g = await js(t, 0, pi, o); m = want_m(t, r, o); e = te(m, r, o)
                chk(('月', p, o, t), (g['m'], g['t'], g['s'], g['i'], g['j']), (m, e['t'], e['s'], e['i'], e['j']))
                if m >= 100:
                    chk(('月 100円下で届かない', p, o, t), te(m - 100, r, o)['t'] // 12 < t, True)
            for t in ([1000000, 3000000, 5000000, 12345678, 30000000] if p == '東京都' else [3000000]):
                g = await js(t, 1, pi, o); m = want_y(t, r, o); e = te(m, r, o)
                chk(('年', p, o, t), (g['m'], g['t']), (m, e['t']))
    # 2 早見表
    h = open(os.path.join(SITE, 'tedori-gyakusan', 'index.html'), encoding='utf-8').read()
    rows = re.findall(r'<tr><td>([\d,]+)</td><td>([\d,]+)</td><td>([\d,]+)</td><td>([\d,]+)</td><td>([\d.]+)%</td></tr>', h)
    chk('月の早見表の行数', len(rows), 12)
    for tr in rows:
        t = num(tr[0]); m = want_m(t, rates.TOKYO, 0); e = te(m, rates.TOKYO, 0)
        chk(('月の表', t), tuple(tr[1:]), (f(m), f(m * 12), f(m - e['t'] // 12), pct1(e['t'], m * 12)))
    rows = re.findall(r'<tr><td>([\d,]+)万円</td><td>([\d,]+)</td><td>([\d,]+)</td><td>([\d,]+)</td></tr>', h)
    chk('年の早見表の行数', len(rows), 10)
    for tr in rows:
        t = num(tr[0]) * 10000; m = want_y(t, rates.TOKYO, 0); e = te(m, rates.TOKYO, 0)
        chk(('年の表', t), tuple(tr[1:]), (f(m * 12), f(m), f(m * 12 - e['t'])))
    # 3 既定の文字(JS が動く前)と画面
    m30 = want_m(300000, rates.TOKYO, 0); e = te(m30, rates.TOKYO, 0)
    for s in ['<b id="o-vd">必要な月給は%s円です</b>' % f(m30), '<b id="o-m">%s<i>円</i></b>' % f(m30),
              '<b id="o-y">%s<i>円</i></b>' % f(m30 * 12), '<b id="o-d">%s<i>円</i></b>' % f(m30 - e['t'] // 12),
              '手取り率%s%%' % pct1(e['t'], m30 * 12),
              '社会保険料%s円・所得税%s円・住民税%s円' % (f(e['s'] // 12), f(e['i'] // 12), f(e['j'] // 12)),
              'この月給の手取りは月%s円です' % f(e['t'] // 12),
              '手取り月30万円には額面でおよそ%s万円' % f((m30 + 5000) // 10000)]:
        chk(('既定の文字', s), s in h, True)
    await pg.goto('file://' + os.path.join(SITE, 'tedori-gyakusan', 'index.html'))
    chk('画面 o-m', num(await pg.inner_text('#o-m')), m30)
    # 4 箱を動かす(大阪・40〜64歳・月25万円 → 1年の手取り400万円)
    await pg.select_option('#pref', '26')
    await pg.click('#s-age button[data-a="1"]')
    await pg.fill('#tg', '250000')
    m = want_m(250000, 1013, 1)
    chk('箱 大阪 40〜64歳 25万', num(await pg.inner_text('#o-m')), m)
    await pg.click('#s-kind button[data-v="1"]')
    await pg.fill('#tg', '4000000')
    m = want_y(4000000, 1013, 1)
    chk('箱 1年の手取り400万', (num(await pg.inner_text('#o-m')), num(await pg.inner_text('#o-y'))), (m, m * 12))
    # 5 本文・よくある質問
    for t in (200000, 250000, 300000):
        m = want_m(t, rates.TOKYO, 0)
        chk(('質問の月給', t), ('月給%s円' % f(m)) in h, True)
    for t in (3000000, 5000000):
        m = want_y(t, rates.TOKYO, 0)
        chk(('質問の年収', t), ('年収%s円' % f(m * 12)) in h, True)
    for t in (200000, 400000):
        m = want_m(t, rates.TOKYO, 0); e = te(m, rates.TOKYO, 0)
        chk(('およそ8割', t), 75 <= e['t'] * 100 // (m * 12) <= 84, True)
    return n, bad

run('tedori-gyakusan', body)
