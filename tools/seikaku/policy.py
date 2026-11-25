# /policy/ 運営方針(計算の無いページ。ページに書いてあるサイトの説明を、今の site/ の作りと照らす)。
# 照らす相手(このページは公的な数字を載せていないので、照らす相手はサイト自身):
#  site/ の全ページ(index.html)・tools/pages.json(一覧の名前)・live/(アイコンとロゴの置き場)・CLAUDE.md(言葉の決まり)
#  ページが名前を挙げる一次情報の出どころと、ほかのページの出典で使っている住所:
#   国税庁 https://www.nta.go.jp/ ・財務省 https://www.mof.go.jp/ ・総務省 https://www.soumu.go.jp/
#   全国健康保険協会(協会けんぽ) https://www.kyoukaikenpo.or.jp/ ・日本年金機構 https://www.nenkin.go.jp/ ・大阪府 https://www.pref.osaka.lg.jp/
# 見ないもの:運営者の名前・資格・登録番号・所在地・「12年」が正しいかどうか(確かめる手段が無い。トップページと同じ文字かだけを見る)。
#  外のリンク(oyama-toshiro.com・Google フォーム)が開くかどうかはここでは見ない(形だけを見る)。
# 最後に照らした日: 2026-11-21
import os, sys, re, glob, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import done, SITE, ROOT

TODAY = datetime.date.today()
n = bad = 0
def ck(ok, what):
    global n, bad
    n += 1
    if not ok:
        bad += 1; print('合わない', what)
def memo(what):
    print('残り', what)

def rd(p):
    return open(p, encoding='utf-8').read()
def text(h):
    h = re.sub(r'<(script|style)\b.*?</\1>', '', h, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h))

P = rd(os.path.join(SITE, 'policy', 'index.html'))
TOP = rd(os.path.join(SITE, 'index.html'))
pages = {os.path.basename(os.path.dirname(p)): rd(p) for p in glob.glob(os.path.join(SITE, '*', 'index.html'))}
tools = {k: v for k, v in pages.items() if k != 'policy'}
body = P[P.index('<main'):P.index('</main>')]
main_txt = text(body[:body.index('<nav class="tools">')])

# ---- 1 リンクの行き先 ----
def exists(path):
    path = path.split('#')[0].split('?')[0]
    if path.endswith('/'):
        return os.path.isfile(os.path.join(SITE, path.strip('/'), 'index.html'))
    # 画像とアイコンは site/ か、公開用の置き場 live/ にある
    return any(os.path.isfile(os.path.join(ROOT, d, path.lstrip('/'))) for d in ('site', 'live'))
OUT = {'oyama-toshiro.com', 'docs.google.com', 'www.googletagmanager.com', 'www.clarity.ms', 'taxtable.jp', 'fonts.googleapis.com', 'fonts.gstatic.com'}
for u in re.findall(r'(?:href|src)="([^"]+)"', P):
    if u.startswith('#'):
        ck(('id="%s"' % u[1:]) in P, 'ページ内の行き先が無い ' + u)
    elif u.startswith('/'):
        ok = exists(u)
        if ok and '#' in u:
            tgt = TOP if u.split('#')[0] == '/' else pages.get(u.split('#')[0].strip('/'), '')
            ok = ('id="%s"' % u.split('#')[1]) in tgt
        ck(ok, '内部リンクの行き先が無い ' + u)
    else:
        m = re.match(r'https://([^/]+)(?:/|$)', u)
        ck(bool(m) and m.group(1) in OUT, '外のリンクの形・行き先が決めた先でない ' + u)
# 一覧:全部のツールのページが載っているか・名前が pages.json と同じか
lst = dict(re.findall(r'<a href="(/[a-z0-9-]+/)">([^<]+)</a>', body[body.index('<nav class="tools">'):]))
for s in sorted(tools):
    ck('/%s/' % s in lst, '一覧に無いページ /%s/' % s)
for d in json.load(open(os.path.join(ROOT, 'tools', 'pages.json'), encoding='utf-8')):
    ck(lst.get(d['path']) == d['label'], '一覧の名前が pages.json と違う %s %s' % (d['path'], lst.get(d['path'])))
# 訂正フォームの住所が本文・フッター・ほかのページで同じか
forms = set(re.findall(r'https://docs\.google\.com/forms/[^"]+', P))
ck(len(forms) == 1, '訂正フォームの住所が1つでない')
for s, h in sorted(tools.items()):
    ck(set(re.findall(r'https://docs\.google\.com/forms/[^"]+', h)) <= forms, '訂正フォームの住所が違う /%s/' % s)

# ---- 2 一次情報の出どころの名前と住所 ----
SRC = {'国税庁': 'www.nta.go.jp', '財務省': 'www.mof.go.jp', '総務省': 'www.soumu.go.jp', '協会けんぽ': 'www.kyoukaikenpo.or.jp',
       '全国健康保険協会': 'www.kyoukaikenpo.or.jp', '日本年金機構': 'www.nenkin.go.jp', '大阪府': 'www.pref.osaka.lg.jp'}
srcs = {s: ''.join(re.findall(r'<div class="src".*?</div>', h, flags=re.S)) for s, h in tools.items()}
m = re.search(r'数字は、(.+?)などの公的機関', main_txt)
ck(bool(m), '「数字の出典」の文が見つからない')
named = re.split(r'[・（）]', m.group(1)) if m else []
named = [x for x in named if x]
m2 = re.search(r'数字は、(.+?)などの一次情報をもとに', text(P[P.index('id="auth"'):]))
named += [x for x in re.split(r'[・（）]', m2.group(1)) if x] if m2 else []
for nm in named:
    ck(nm in SRC, '照らす住所を決めていない出どころ ' + nm)
    if nm in SRC:
        ck(any(nm in text(v) for v in srcs.values()), 'ほかのページの出典に名前が無い ' + nm)
        ck(any(('https://%s/' % SRC[nm]) in v for v in srcs.values()), 'ほかのページの出典に住所が無い ' + SRC[nm])
# トップページの「出典：」と同じ顔ぶれか
mt = re.search(r'出典：(.+?)。', text(TOP))
ck(bool(mt) and m and set(re.split(r'[・（）]', mt.group(1))) - {''} == set(re.split(r'[・（）]', m.group(1))) - {''}, 'トップの出典の顔ぶれと違う')

# ---- 3 サイトの説明と今の作り ----
# 「各ページの最後に、参照した一次情報と確認日を記載」
ck('各ページの最後に、参照した一次情報（法令・公的資料）と確認日を記載しています' in main_txt, '出典と確認日の文が変わった')
for s in sorted(tools):
    ck(bool(srcs[s]) and re.search(r'確認|確かめ', text(srcs[s])) and re.search(r'20\d\d年\d+月', text(srcs[s])), '出典か確認日が無い /%s/' % s)
# 「各ページの一番上に更新日と対象の年度」
ck('各ページの一番上に更新日と対象の年度を書いています' in main_txt, '更新日と年度の文が変わった')
NO_NENDO = {'soneki-bunkiten'}   # 年度で変わる数字を持たないページ(損益分岐点)
for s, h in sorted(tools.items()):
    mu = re.search(r'<p class="upd">(.*?)</p>', h, flags=re.S)
    upd = text(mu.group(1)) if mu else ''
    ck('更新日：' in upd, '更新日が無い /%s/' % s)
    if s in NO_NENDO:
        if not re.search(r'令和|年度|年分', upd):
            memo('更新日の行に対象の年度が無い(年度で変わる数字を持たないページ) /%s/' % s)
        continue
    i = h.find('</h1>')
    head = upd + text(h[h.find('<h1'):i + 2500]) + ''.join(re.findall(r'<title>[^<]*', h))
    ck(bool(re.search(r'令和\d+年|20\d\d年', re.sub(r'(公開日|更新日)：\d+年\d+月\d+日', '', head))), '対象の年・年度が上のほうに無い /%s/' % s)
    if not re.search(r'令和|年度|年分', upd):
        memo('更新日の行に対象の年度が無い(題名か表の見出しにはある) /%s/' % s)
# 相談の案内:経理丸投げは各ページ・創業融資の相談はトップとこのページ
ck('各ページに、経理と申告をまとめて任せるサービスの案内を載せています' in main_txt, '相談の案内の文が変わった')
ck('創業融資の相談の案内は、トップページとこのページに載せています' in main_txt, '創業融資の案内の文が変わった')
for s, h in sorted(pages.items()):
    ck('https://oyama-toshiro.com/contact/' in h, '経理丸投げの案内が無い /%s/' % s)
ck('https://oyama-toshiro.com/contact/' in TOP, '経理丸投げの案内が無い トップ')
yu = {s for s, h in pages.items() if 'oyama-toshiro.com/yuushi/' in h} | ({'TOP'} if 'oyama-toshiro.com/yuushi/' in TOP else set())
ck(yu == {'TOP', 'policy'}, '創業融資の相談の案内があるページが文と違う %s' % sorted(yu))
# アクセス解析:site/ のページが読み込む外の仕組みが、説明に書いてあるか
KNOWN = {'www.googletagmanager.com': 'Googleアナリティクス', 'www.clarity.ms': 'Microsoft Clarity'}
NOT_ANALYTICS = {'fonts.googleapis.com', 'fonts.gstatic.com'}   # 文字の形の読み込み(解析ではない)
hosts = {}
for s, h in list(pages.items()) + [('TOP', TOP)]:
    js = ''.join(re.findall(r'<script\b.*?</script>', h, flags=re.S)) + ''.join(re.findall(r'<link\b[^>]*>', h))
    for hs in re.findall(r'https://([a-zA-Z0-9.-]+)', js):
        if hs != 'taxtable.jp':
            hosts.setdefault(hs, set()).add(s)
for hs, where in sorted(hosts.items()):
    if hs in NOT_ANALYTICS:
        memo('%s を読み込むページがある(%s)。アクセス解析の説明には書いていない' % (hs, '・'.join(sorted(where))))
        continue
    ck(hs in KNOWN and KNOWN[hs] in main_txt.replace('Google アナリティクス', 'Googleアナリティクス'), '説明に無い外の仕組みを読み込んでいる %s (%d ページ)' % (hs, len(where)))
for hs, nm in KNOWN.items():
    ck((nm in main_txt) == (hs in hosts), '説明にあるのに読み込んでいない ' + nm)
# 入力した数字を外へ送る作りが無いか(送信フォーム・通信の命令)
for s, h in sorted(pages.items()) + [('TOP', TOP)]:
    ck(not re.search(r'fetch\(|XMLHttpRequest|sendBeacon|<form\b|<iframe\b|WebSocket', h), '入力を外へ送れる作りがある /%s/' % s)

# ---- 4 年・日付 ----
mu = re.search(r'<p class="upd">更新日：(\d+)年(\d+)月(\d+)日</p>', P)
ck(bool(mu), '更新日が読めない')
if mu:
    d = datetime.date(*map(int, mu.groups()))
    ck(datetime.date(2026, 11, 7) <= d <= TODAY, '更新日が今日より先か、前の更新日より前 %s' % d)
for y in re.findall(r'(20\d\d)年', text(P)):
    ck(int(y) <= TODAY.year, '先の年が書いてある %s年' % y)
for dm in re.findall(r'"dateModified"\s*:\s*"([^"]+)"', P):
    ck(mu and dm[:10] == d.isoformat(), 'dateModified が更新日と違う ' + dm)

# ---- 5 言葉の決まり(CLAUDE.md) ----
vis = text(P) + ' ' + ' '.join(re.findall(r'content="([^"]*)"', P))
for w in ['作っている人', '作った税理士', '原本', '比べ方', '税理士事務所', '入れると出る', '入れていません', '通帳が増える', '生成AI', 'AIで', 'mkv', 'ver=']:
    ck(w not in vis, '使わない言葉がある ' + w)
ck(not re.search(r'(?<!早見)表と計算', vis), '使わない言葉がある 表と計算')
ck(not re.search(r'\bmk\d|\bv\d+\.\d+', vis), '版の文字がある')
for w in ['監修・制作税理士', '運営者プロフィール', '一次情報（法令・公的資料）', '早見表と試算ツール']:
    ck(w in vis, '決まった言葉が無い ' + w)
# 本文の1文に「、」は1つまで
for sen in re.split(r'(?<=。)', main_txt):
    ck(sen.count('、') <= 1, '「、」が2つ以上 ' + sen.strip()[:40])
# 本人の情報はトップページと同じ文字か(正しいかどうかは見ない)
for pat in [r'登録番号\d+', r'運営：[^<]+', r'近畿税理士会所属']:
    a = re.search(pat, P); b = re.search(pat, TOP)
    ck(bool(a and b) and a.group(0) == b.group(0), 'トップページと文字が違う ' + pat)

done(n, bad)
