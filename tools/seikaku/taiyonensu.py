# /taiyonensu/ 法定耐用年数の一覧と減価償却の計算。
# 原本:
#  国税庁「主な減価償却資産の耐用年数表」(建物・建物附属設備・車両運搬具・器具備品の年数) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/pdf/2100_01.pdf
#  国税庁 No.5461「ソフトウエアの取得価額と耐用年数」(複写して販売するための原本と研究開発用は3年・その他は5年。耐令別表第三・第六。令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5461.htm
#  国税庁 No.2106「定額法と定率法による減価償却(平成19年4月1日以後に取得する場合)」(令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2106.htm
#   定額法=取得価額×償却率/定率法=期首の未償却残高×償却率。調整前償却額が償却保証額(取得価額×保証率)に満たない年から 改定取得価額×改定償却率
#   年の中途は ÷12×使った月数/有形の資産は1円を残す・無形固定資産は取得価額の全額
#   例:100万円・10年の定率法は 7年目から65,536円・10年目65,535円(下の ref_sched で同じになるかも見る)
#  国税庁 No.5410「減価償却資産の償却限度額の計算方法(平成19年4月1日以後取得分)」(調整前償却額が償却保証額に満たない場合) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5410.htm
#  定額法の償却率(耐用年数省令 別表第八):国税庁「青色申告の決算の手引き(現金主義用)」の減価償却資産の償却率等表 https://www.nta.go.jp/taxes/shiraberu/shinkoku/tebiki/2023/pdf/041.pdf
#   同じ率:国税庁 資料編 https://www.nta.go.jp/law/joho-zeikaishaku/shotoku/shinkoku/070412/pdf/3.pdf
#  定率法の償却率・改定償却率・保証率(別表第十・平成24年4月1日以後取得):国税庁「法人の減価償却制度の改正に関するQ&A」参考資料 https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2011/pdf/1112kaisei_faq.pdf
#  国税庁 No.5404「中古資産の耐用年数」(簡便法・1年未満切り捨て・2年未満は2年。耐令3・耐通1-5-1・1-5-4。令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5404.htm
#  国税庁 No.2100「減価償却のあらまし」(10万円未満・一括償却資産20万円未満・特例は令和8年4月1日以後の取得から40万円未満・令和11年3月31日まで・年300万円。令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2100.htm
#  国税庁 No.5408「中小企業者等の少額減価償却資産の取得価額の損金算入の特例」(40万円未満・従業員400人以下・令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5408.htm
#  国税庁「令和8年度 法人税関係法令の改正の概要」主な中小企業税制の見直し https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2026/pdf/G.pdf
#  中小企業庁「少額減価償却資産の特例」 https://www.chusho.meti.go.jp/zaimu/zeisei/tokurei/syougaku_shisan.html
#  国税庁 確定申告書等作成コーナー「減価償却費の端数処理」(個人の減価償却費の小数点以下の端数は切り上げ) https://www.keisan.nta.go.jp/r5yokuaru/aoiroshinkoku/hitsuyokeihi/genkashokyakuhi/hasushori.html
# 最後に原本を確かめた日: 2026-11-20
#  2026-11-21:作成コーナー「減価償却費の端数処理」だけ本文で読んだ(「減価償却費の計算で小数点以下の端数が生じた場合、切上げ処理」。償却方法を分ける記載は無い)。ほかの原本は 11-20 のまま。
#  作成コーナーの端数処理は、同じ 11-21 の3時の回が開いて確かめた(kiroku/zen/2026-11-21/chukosha-taiyonensu.txt)。
# 端数:年ごとの償却費の1円未満は、法人は切り捨て(償却限度額を超えない向き)・個人事業主は切り上げ(作成コーナーと同じ。2026-11-21 にページを切り捨てから直した。/chukosha-taiyonensu/ と同じ扱い)。
#  償却保証額との比べは丸める前の額で比べる(「満たない」)。
# 2026-11-20:ページは償却保証額との比べを切り捨てたあとの額でしていた(取得価額1,000円・耐用年数22年以上などで年の割り振りが変わる)。整数どうしの比べ bv*b*100<cost*hs に直した。tools/build_taiyo.py にも同じ直しが要る。
# 照らすもの:window.__taiyo(2年〜50年の全部の率)・結果の箱・毎年の表・判定の文(10万・20万・40万円の境目)・
#  HTML に手で書いた表(耐用年数33行・償却率18行・50万円の例5行・少額4行・中古車7行)・入力欄の選択肢・本文の数字
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

# 別表第八 定額法の償却率(千分率) 2年〜50年
GAKU = dict(zip(range(2, 51), [500, 334, 250, 200, 167, 143, 125, 112, 100, 91, 84, 77, 72, 67, 63, 59, 56, 53, 50,
                               48, 46, 44, 42, 40, 39, 38, 36, 35, 34, 33, 32, 31, 30, 29, 28, 28, 27, 26, 25,
                               25, 24, 24, 23, 23, 22, 22, 21, 21, 20]))
# 別表第十 定率法(平成24年4月1日以後取得) 償却率・改定償却率(千分率)・保証率(十万分率)
TEI = {2: (1000, None, None), 3: (667, 1000, 11089), 4: (500, 1000, 12499), 5: (400, 500, 10800), 6: (333, 334, 9911),
       7: (286, 334, 8680), 8: (250, 334, 7909), 9: (222, 250, 7126), 10: (200, 250, 6552), 11: (182, 200, 5992),
       12: (167, 200, 5566), 13: (154, 167, 5180), 14: (143, 167, 4854), 15: (133, 143, 4565), 16: (125, 143, 4294),
       17: (118, 125, 4038), 18: (111, 112, 3884), 19: (105, 112, 3693), 20: (100, 112, 3486), 21: (95, 100, 3335),
       22: (91, 100, 3182), 23: (87, 91, 3052), 24: (83, 84, 2969), 25: (80, 84, 2841), 26: (77, 84, 2716),
       27: (74, 77, 2624), 28: (71, 72, 2568), 29: (69, 72, 2463), 30: (67, 72, 2366), 31: (65, 67, 2286),
       32: (63, 67, 2216), 33: (61, 63, 2161), 34: (59, 63, 2097), 35: (57, 59, 2051), 36: (56, 59, 1974),
       37: (54, 56, 1950), 38: (53, 56, 1882), 39: (51, 53, 1860), 40: (50, 53, 1791), 41: (49, 50, 1741),
       42: (48, 50, 1694), 43: (47, 48, 1664), 44: (45, 46, 1664), 45: (44, 46, 1634), 46: (43, 44, 1601),
       47: (43, 44, 1532), 48: (42, 44, 1499), 49: (41, 42, 1475), 50: (40, 42, 1440)}
assert len(GAKU) == 49 and len(TEI) == 49

# 国税庁「主な減価償却資産の耐用年数表」と No.5461 から。(種類, ページの行の名前, 年数, 定額法だけか)
ASSETS = [
    ('建物', '鉄筋コンクリート造の事務所', 50), ('建物', '鉄筋コンクリート造の住宅', 47), ('建物', '鉄筋コンクリート造の店舗', 39),
    ('建物', '金属造（骨格材4mm超）の事務所', 38), ('建物', '金属造（骨格材4mm超）の店舗・住宅', 34),
    ('建物', '金属造（3mm超4mm以下）の店舗・住宅', 27), ('建物', '金属造（3mm以下）の店舗・住宅', 19),
    ('建物', '木造の事務所', 24), ('建物', '木造の店舗・住宅', 22), ('建物', '木造の飲食店', 20), ('建物', '木骨モルタル造の店舗・住宅', 20),
    ('建物附属設備', '電気設備（照明など）', 15), ('建物附属設備', '給排水・衛生設備・ガス設備', 15), ('建物附属設備', '店用簡易装備', 3),
    ('車両', '普通自動車（一般用）', 6), ('車両', '軽自動車（総排気量0.66L以下）', 4), ('車両', 'バイク（二輪・三輪）', 3),
    ('車両', '貨物自動車（ダンプ以外）', 5), ('車両', '自転車', 2),
    ('器具備品', 'パソコン（サーバー用を除く）', 4), ('器具備品', 'サーバー', 5), ('器具備品', 'コピー機・レジ', 5),
    ('器具備品', '事務机・いす・キャビネット（金属製）', 15), ('器具備品', '事務机・いす・キャビネット（金属製以外）', 8),
    ('器具備品', '応接セット（接客業用）', 5), ('器具備品', '冷蔵庫・洗濯機などの家電', 6), ('器具備品', 'エアコン（冷房用・暖房用機器）', 6),
    ('器具備品', 'テレビ・音響機器', 5), ('器具備品', 'カメラ', 5), ('器具備品', '看板・ネオンサイン', 3), ('器具備品', '時計', 10),
    ('ソフトウェア', 'ソフトウェア（自社で使うもの）', 5), ('ソフトウェア', 'ソフトウェア（販売用の原本・研究開発用）', 3)]
ONLY = ('建物', '建物附属設備', 'ソフトウェア')   # 定額法だけ(建物は平成10年4月1日以後・附属設備は平成28年4月1日以後・無形固定資産)

def ref_sched(cost, n, tr, months, soft, up=0):
    """cost=取得価額 n=耐用年数 tr=1 定率法 months=1年目に使った月数 soft=無形固定資産(0円まで) up=1 個人事業主(1円未満切り上げ)"""
    out, book, rev, low = [], cost, None, (0 if soft else 1)
    while book > low and len(out) < 80:
        mo = months if not out else 12
        if tr:
            r, kai, ho = TEI[n]
            if rev is None and ho is not None and F(book * r, 1000) < F(cost * ho, 100000):
                rev = book                       # 調整前償却額が償却保証額に満たない最初の年の期首の残り
            ann = F(book * r, 1000) if rev is None else F(rev * kai, 1000)
        else:
            ann = F(cost * GAKU[n], 1000)
        x = ann * mo / 12
        a = -int(-x // 1) if up else int(x)      # 1円未満:個人事業主は切り上げ・法人は切り捨て
        a = min(a, book - low)                   # 1円(無形は0円)を残す
        book -= a
        out.append(a)
    return out

def ref_chuko(L, y):
    """簡便法。L=法定耐用年数 y=過ぎた年数(1年単位)。"""
    if y <= 0:
        return L
    v = F(L, 5) if y >= L else (L - y) + F(y, 5)
    return max(int(v), 2)

def r3(v):
    return '%d.%03d' % (v // 1000, v % 1000)

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)
    def rows(i):
        return pg.evaluate('''i=>[...document.querySelectorAll(":is(#"+i+" ~ .tw):not(#"+i+" ~ .tw ~ .tw) tbody tr")]
            .map(r=>[...r.querySelectorAll("td")].map(d=>d.innerText.replace(/\\s+/g,"")))''', i)

    # 0 原本の例(No.2106:100万円・10年)。自分の計算が原本の例と同じか
    s = ref_sched(1000000, 10, 1, 12, 0)
    chk('No.2106 の例 定率法', (s[0], s[6], s[7], s[8], s[9], len(s)), (200000, 65536, 65536, 65536, 65535, 10))
    s = ref_sched(1000000, 10, 0, 12, 0)
    chk('No.2106 の例 定額法', (s[0], s[8], s[9], len(s)), (100000, 100000, 99999, 10))

    # 0-2 個人事業主の切り上げの例:1,234,567円×0.500=617,283.5円→617,284円。50万円・6年の定率法2年目 333,500円×0.333=111,055.5円→111,056円。法人は切り捨て
    chk('個人の切り上げ 定額法', ref_sched(1234567, 2, 0, 12, 0, 1), [617284, 617282])
    chk('個人の切り上げ 定率法', ref_sched(500000, 6, 1, 12, 0, 1)[:2], [166500, 111056])
    chk('法人の切り捨て 定率法', ref_sched(500000, 6, 1, 12, 0, 0)[:2], [166500, 111055])
    # 1 関数:2年〜50年の全部の率・定額法と定率法・月数・無形
    costs = [0, 1, 2, 3, 1000, 99999, 100000, 199999, 200000, 333333, 399999, 400000, 500000, 1000000, 1234567,
             2999999, 3000001, 7777777, 12345678, 98765432, 123456789, 3999999999, 10000000000]
    for yrs in range(2, 51):
        for cost in costs:
            for tr in (0, 1):
                for months in (12, 9, 1) if yrs not in (2, 3, 4, 5, 6, 10, 22, 50) else range(1, 13):
                    for soft, up in ((0, 0), (1, 0), (0, 1), (1, 1)):
                        got = await pg.evaluate('([c,y,t,m,s,u])=>window.__taiyo(c,y,t,m,s,u)', [cost, yrs, tr, months, soft, up])
                        exp = ref_sched(cost, yrs, tr, months, soft, up); n += 1
                        if got != exp:
                            bad += 1; print('NG sched', cost, yrs, tr, months, soft, up, got[:12], exp[:12])
                        if cost < 1000 and not up:
                            continue             # 1円〜3円は毎年の額が切り捨てで0円になり償却が進まない(関数の一致だけを見る)
                        n += 1
                        if sum(exp) != max(0, cost - (0 if soft else 1)):
                            bad += 1; print('NG 合計が取得価額−備忘価額でない', cost, yrs, tr, months, soft, up)
    # 償却保証額との比べが切り捨ての前後で変わる所を探して照らす(整数どうしの比べ)
    for yrs in range(3, 51):
        r, kai, ho = TEI[yrs]
        hit = 0
        for cost in range(100001, 100001 + 4000):
            book = cost
            for _ in range(yrs + 2):
                pre, gar = F(book * r, 1000), F(cost * ho, 100000)
                if pre < gar:
                    if int(pre) == int(gar):
                        hit += 1
                        got = await pg.evaluate('([c,y])=>window.__taiyo(c,y,1,12,0)', [cost, yrs]); n += 1
                        if got != ref_sched(cost, yrs, 1, 12, 0):
                            bad += 1; print('NG 保証額の境目', cost, yrs, got, ref_sched(cost, yrs, 1, 12, 0))
                    break
                book -= int(pre)
            if hit >= 3:
                break

    # 2 画面:入力して結果の箱と毎年の表を読む
    async def screen(idx, cost, who, hoho, mon, yrs=None):
        await pg.click('#s-who button[data-v="%d"]' % who)
        btn = pg.locator('#s-hoho button[data-v="%d"]' % hoho)
        await pg.select_option('#as', str(idx))
        if yrs is not None:
            await pg.fill('#yrs', str(yrs))
        if not await btn.is_disabled():
            await btn.click()
        await pg.fill('#cost', str(cost))
        await pg.select_option('#mon', str(mon))
        tb = await pg.evaluate('()=>[...document.querySelectorAll("#tb tr")].map(r=>[...r.querySelectorAll("td")].map(d=>d.innerText))')
        return {k: await pg.inner_text('#' + k) for k in ('o-n', 'o-ne', 'o-1', 'o-1e', 'o-2', 'o-how', 'o-vd', 'o-vds')}, tb
    cases = []
    for idx in range(len(ASSETS)):
        cases.append((idx, 500000, 0, 0, 4, None))
        cases.append((idx, 1234567, 1, 1, 1, None))
        cases.append((idx, 3000000, 0, 1, 10, None))
        cases.append((idx, 1234567, 0, 0, 2, None))
        cases.append((idx, 7777777, 0, 1, 5, None))
    for cost in (0, 1, 99999, 100000, 199999, 200000, 399999, 400000, 400001, 10000000000):
        for who, hoho in ((0, 0), (1, 1), (1, 0)):
            cases.append((19, cost, who, hoho, 12, None))
            cases.append((14, cost, who, hoho, 1, None))
    for yrs in (2, 3, 7, 10, 13, 22, 37, 44, 50):
        for mon in (1, 6, 12):
            cases.append((-1, 800000, 1, 1, mon, yrs))
            cases.append((-1, 800000, 0, 0, mon, yrs))
    for c in cases:
        idx, cost, who, hoho, mon, yrs = c
        o, tb = await screen(*c)
        hasu = await pg.inner_text('#o-hasu')
        if idx >= 0:
            kind, name, L = ASSETS[idx]
            only, soft = kind in ONLY, kind == 'ソフトウェア'
        else:
            name, L, only, soft = '耐用年数%d年の資産' % yrs, yrs, False, False
        tr = 0 if only else hoho
        months = 13 - mon
        s = ref_sched(cost, L, tr, months, soft, 0 if who else 1)
        rate = TEI[L][0] if tr else GAKU[L]
        if cost < 100000:
            vd, vds = '全額をその年の経費にできます', '10万円未満なので少額減価償却資産です'
        elif cost < 200000:
            vd, vds = '3年で3分の1ずつも選べます', '10万円以上20万円未満なので一括償却資産にできます'
        elif cost < 400000:
            vd, vds = '青色申告なら全額経費にもできます', '40万円未満の特例（令和8年4月1日以後の取得・年300万円まで）'
        else:
            vd, vds = '耐用年数で減価償却します', '%d年で経費にします' % L
        book, want_tb = cost, []
        for k, a in enumerate(s):
            book -= a
            want_tb.append(['%d年目' % (k + 1), '{:,}'.format(a), '{:,}'.format(book)])
        how = '定額法だけで' if only else ('定率法で' if tr else '定額法で')
        n += 1
        ok = (num(o['o-n']) == L and o['o-ne'] == ('定率法 ' if tr else '定額法 ') + r3(rate)
              and num(o['o-1']) == (s[0] if s else 0) and o['o-1e'] == '%dか月分' % months
              and num(o['o-2']) == (s[1] if len(s) > 1 else 0) and tb == want_tb
              and o['o-vd'] == vd and vds in o['o-vds'] and (name + 'を' + how + '計算しています') in o['o-how']
              and hasu == ('1円未満は切り捨てています。' if who else '1円未満は切り上げています（国税庁の確定申告書等作成コーナーと同じ）。')
              and (('年の途中から使ったので%d年に分かれます' % len(s)) in o['o-vds']) == (cost >= 400000 and len(s) > L))
        if not ok:
            bad += 1; print('NG 画面', c, o, tb[:3], s[:3])

    # 3 HTML に手で書いた表
    # 3-1 耐用年数の一覧:全行を原本の年数と比べる
    t = await rows('list')
    chk('耐用年数の表の行数', len(t), len(ASSETS))
    for row, (kind, name, L) in zip(t, ASSETS):
        chk('耐用年数 ' + name, row, [kind, name.replace(' ', ''), '%d年' % L])
    # 入力欄の選択肢も同じ並び・同じ年数
    opts = await pg.evaluate('()=>[...document.querySelectorAll("#as option")].map(o=>[o.value,o.textContent,o.parentElement.label||""])')
    chk('選択肢の数', len(opts), len(ASSETS) + 1)
    for (val, txt, grp), (i, (kind, name, L)) in zip(opts, enumerate(ASSETS)):
        chk('選択肢 ' + name, (val, txt, grp), (str(i), '%s（%d年）' % (name, L), kind))
    # 3-2 償却率の表:全行
    t = await rows('rate')
    chk('償却率の表の年数', [num(r[0]) for r in t], [2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 22, 24, 30, 34, 38, 39, 47, 50])
    for row in t:
        y = num(row[0]); r, kai, ho = TEI[y]
        want = ['%d年' % y, r3(GAKU[y]), r3(r), r3(kai) if kai else '―', ('0.%05d' % ho) if ho else '―']
        chk('償却率 %d年' % y, row, want)
    # 3-3 50万円の例
    t = await rows('rei')
    chk('50万円の例の年数', [num(r[0]) for r in t], [4, 5, 6, 8, 10])
    for row in t:
        y = num(row[0]); g = ref_sched(500000, y, 0, 12, 0); z = ref_sched(500000, y, 1, 12, 0)
        chk('50万円の例 %d年' % y, [num(x) for x in row[1:]], [g[0], z[0], z[1], z[0] + z[1]])
    # 3-4 少額の表(No.2100・No.5408)
    t = await rows('shogaku')
    chk('少額の表の行数', len(t), 4)
    flat = [''.join(r) for r in t]
    chk('少額 10万円未満', '10万円未満' in flat[0] and '少額減価償却資産' in flat[0], True)
    chk('少額 20万円未満', '10万円以上20万円未満' in flat[1] and '3年で3分の1ずつ' in flat[1] and '一括償却資産' in flat[1], True)
    chk('少額 40万円未満', '10万円以上40万円未満' in flat[2] and '年300万円まで' in flat[2] and '青色申告' in flat[2]
        and '令和8年3月31日までの取得は30万円未満' in flat[2], True)
    # 3-5 中古車の表(簡便法)
    t = await rows('chuko')
    chk('中古車の表の行の名前', [r[0] for r in t], ['新車', '1年落ち', '2年落ち', '3年落ち', '4年落ち', '5年落ち', '6年落ち以上'])
    for y, row in enumerate(t):
        ys = range(6, 40) if y == 6 else (y,)
        for col, L in ((1, 6), (2, 4), (3, 5)):
            n += 1
            if any(ref_chuko(L, yy) != num(row[col]) for yy in ys):
                bad += 1; print('NG 中古車', row, L, [ref_chuko(L, yy) for yy in ys][:3])
    head = await pg.evaluate('()=>[...document.querySelectorAll(":is(#chuko ~ .tw):not(#chuko ~ .tw ~ .tw) thead th")].map(d=>d.innerText.replace(/\\s+/g,""))')
    chk('中古車の表の見出し', head[1:], ['普通自動車（法定6年）', '軽自動車（法定4年）', '貨物自動車（法定5年）'])

    # 4 本文の数字
    txt = re.sub(r'\s+', '', await pg.inner_text('main'))
    L = {nm: y for _, nm, y in ASSETS}
    for label, s_, cond in (
        ('パソコン・普通自動車・木造の店舗', 'パソコンは4年・普通自動車は6年・木造の店舗は22年です',
         (L['パソコン（サーバー用を除く）'], L['普通自動車（一般用）'], L['木造の店舗・住宅']) == (4, 6, 22)),
        ('飲食店の年数', '30%を超えると34年です。超えないものは41年で、木造の飲食店は20年です', L['木造の飲食店'] == 20),
        ('サーバー用は5年', '4年です。サーバー用は5年です', L['サーバー'] == 5),
        ('軽自動車は4年', '新車の普通自動車は6年・軽自動車は4年です', L['軽自動車（総排気量0.66L以下）'] == 4),
        ('4年落ちの普通自動車', '4年落ちの普通自動車なら2年です', ref_chuko(6, 4) == 2),
        ('4月から9か月', '4月から使えば9か月分です', 13 - 4 == 9),
        ('10月から3か月', '10月に使い始めたら3か月分です', 13 - 10 == 3),
        ('簡便法の式', '法定耐用年数－過ぎた年数＋過ぎた年数×20%', True),
        ('全部が過ぎた式', '「法定耐用年数×20%」', True),
        ('端数', '1年未満の端数は切り捨て、2年に満たないときは2年にします', True),
        ('特例の期間', '令和8年4月1日から令和11年3月31日までに取得した資産が対象です', True),
        ('従業員400人', '従業員400人以下', True),
        ('定額法だけの取得日', '平成10年4月1日以後に取得した建物と平成28年4月1日以後に取得した建物附属設備・構築物は、定額法だけです', True),
        ('200%定率法', '平成24年4月1日以後に取得した資産の率（200%定率法）', True),
        ('法令の時点', '令和8年4月1日現在法令等', True)):
        chk('文 ' + label, (s_ in txt) and cond, True)
    # 計算の箱に直に書いた既定(パソコン・50万円・個人・定額法・4月)
    await pg.reload()
    o1 = num(await pg.inner_text('#o-1')); o2 = num(await pg.inner_text('#o-2'))
    s = ref_sched(500000, 4, 0, 9, 0, 1)
    chk('既定の結果', (o1, o2, num(await pg.inner_text('#o-n'))), (s[0], s[1], 4))
    # JS が書き換える前の HTML に直に書いた既定の結果(誤りの形16)
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'taiyonensu', 'index.html'), encoding='utf-8').read()
    book, trs = 500000, ''
    for k, a in enumerate(s):
        book -= a
        trs += '<tr><td>%d年目</td><td>%s</td><td>%s</td></tr>' % (k + 1, '{:,}'.format(a), '{:,}'.format(book))
    for want in ('<div class="vd no" id="vd"><b id="o-vd">耐用年数で減価償却します</b><span id="o-vds">4年で経費にします。年の途中から使ったので%d年に分かれます</span></div>' % len(s),
                 '<b id="o-n">4<i>年</i></b><em id="o-ne">定額法 %s</em>' % r3(GAKU[4]),
                 '<b id="o-1">{:,}<i>円</i></b><em id="o-1e">9か月分</em>'.format(s[0]),
                 '<b id="o-2">{:,}<i>円</i></b>'.format(s[1]),
                 '<li id="o-how">パソコン（サーバー用を除く）を定額法で計算しています。個人事業主は届け出なければ定額法です</li>',
                 '<span id="o-hasu">1円未満は切り上げています（国税庁の確定申告書等作成コーナーと同じ）。</span>',
                 '<tbody id="tb">' + trs + '</tbody>'):
        chk('既定の結果(HTML) ' + want[:30], want in raw, True)
    chk('文 50万円の表の端数の注記', '表は1円未満を切り捨てた額です。個人事業主は切り上げるので、6年の定率法2年目は{:,}円です'.format(ref_sched(500000, 6, 1, 12, 0, 1)[1]) in txt, True)
    chk('更新日', '更新日：2026年11月21日' in txt, True)

    # 5 並びと id
    ids = await pg.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)')
    chk('id の重なり', sorted(i for i in set(ids) if ids.count(i) > 1), [])
    pos = await pg.evaluate('()=>[document.querySelector("#list").getBoundingClientRect().top,document.querySelector("#calc").getBoundingClientRect().top]')
    chk('早見表が計算の箱より上', pos[0] < pos[1], True)
    return n, bad
run('taiyonensu', body)
