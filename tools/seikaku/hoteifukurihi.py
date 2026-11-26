# /hoteifukurihi/ 法定福利費の計算(社会保険料の会社負担・本人負担・年金事務所に納める額)。
# 原本:
#  全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分(4月納付分)から改定されます」(47都道府県の健康保険料率・介護1.62%・子ども・子育て支援金0.23%は令和8年4月分から)
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  全国健康保険協会「令和8年3月分(4月納付分)からの健康保険・厚生年金保険の保険料額表」東京・大阪(等級58,000〜1,390,000円・厚生年金88,000〜650,000円・全額の値)
#   https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf  https://www.kyoukaikenpo.or.jp/~/media/Files/shared/hokenryouritu/r8/ippan/27osaka.pdf
#   表の注(11-21 に東京・大阪の両方で読んだ):40〜64歳は健康保険料率と支援金率に介護保険料率を加える・納入告知書の額は被保険者ごとの保険料を合算して円未満切り捨て・
#   標準賞与額の上限は健康保険(介護・支援金)が年度(4月1日〜翌3月31日)の累計573万円、厚生年金と拠出金が1か月150万円
#  日本年金機構「従業員に賞与を支給したときの手続き」(標準賞与額は1,000円未満切り捨て・上限573万円と150万円)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/hoshu/20141203.html
#  日本年金機構「厚生年金保険料等の免除(産前産後休業・育児休業等期間)」(被保険者・事業主の両方の負担が免除)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/menjo/20140122-01.html
#  日本年金機構「保険料額表(令和2年9月分〜)」(令和8年度の拠出金率0.36%・令和8年度版の料額表へのリンク)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/20200825.html
#  日本年金機構「保険料の計算方法について」(納入告知額は制度ごとに合計して1円未満切り捨て・被保険者ごとに端数処理しない・本人負担は50銭以下切り捨て50銭超切り上げ・事業主負担は納入告知額から本人負担の合計を引く)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/nofu/20121026.html
#  日本年金機構「厚生年金保険料額表(令和8年度版)」(18.300%・子ども・子育て拠出金0.36% 令和8年4月1日〜適用)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/20200825.files/R08ryougaku.pdf
#  厚生労働省・こども家庭庁「子ども・子育て支援金に関するQ&A」令和8年2月12日 問6(本人負担は一般保険料率と支援金率を合算した率で折半してから端数処理)
#   https://www.mhlw.go.jp/hourei/doc/tsuchi/T260216S0101.pdf
# 最後に原本を確かめた日:2026-11-21(R08ryougaku.pdf だけは 11-21 に開けず 11-20 のまま)
# 申し送り(11-21):令和8年10月分から「保険料調整制度」を使う事業所向けの別の料額表(R8.10_13東京.pdf など)が出ている。ふつうの料額表(令和8年3月分〜)は変わっていない。
#  納入告知額で健康保険料と支援金を合算してから円未満を切り捨てるかは、Q&A にも年金機構のページにも書かれていない(料額表の注「被保険者ごとの保険料を合算」から合算で計算している)。
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num
import rates

# 協会けんぽ 令和8年度の健康保険料率(%を100倍した整数)。原本のページから写した。
PREF = rates.kenpo_pref()
KAIGO, SIEN, NENKIN, KYOSHUTSU = rates.KAIGO, rates.SIEN, rates.NENKIN, rates.KYOSHUTSU
# 健康保険の標準報酬月額 50等級(千円)。厚生年金は 88〜650 の32等級。
STD = rates.std_yen()
SH = [150000, 200000, 240000, 260000, 300000, 340000, 380000, 410000, 440000, 500000, 560000, 620000, 650000, 710000]

def half(x):
    """本人負担の端数:50銭以下切り捨て・50銭超切り上げ(x は Fraction)。"""
    q = x.numerator // x.denominator
    return q + 1 if x - q > F(1, 2) else q

def ref(pr, rows):
    """rows = [(標準報酬月額, 年齢区分 0:〜39 1:40〜64 2:65〜69 3:70〜74, 人数)]"""
    ken = nen = kyo = F(0); mk = mn = 0; n = 0
    for s, a, c in rows:
        if not c:
            continue
        n += c
        hr = pr + SIEN + (KAIGO if a == 1 else 0)          # 介護は40〜64歳だけ
        ken += F(s * hr * c, 10000)
        mk += half(F(s * hr, 20000)) * c
        if a != 3:                                          # 70歳からは厚生年金と拠出金がかからない
            p = min(max(s, rates.NENKIN_MIN), rates.NENKIN_MAX)
            nen += F(p * NENKIN * c, 10000)
            kyo += F(p * KYOSHUTSU * c, 10000)
            mn += half(F(p * NENKIN, 20000)) * c
    K, N, Y = ken.numerator // ken.denominator, nen.numerator // nen.denominator, kyo.numerator // kyo.denominator
    return {'K': K, 'N': N, 'Y': Y, 'total': K + N + Y, 'me': mk + mn, 'co': K + N + Y - mk - mn,
            'coK': K - mk, 'coN': N - mn, 'n': n}

# 原本の保険料額表の値(全額)。(料率, 標準報酬月額, 40歳未満の健康保険+支援金の全額×10, 40〜64歳の全額×10, 厚生年金の全額)
GENPON = [(rates.TOKYO, 58000, 57130 + 1334, 66526 + 1334, None), (rates.TOKYO, 1390000, 1369150 + 31970, 1594330 + 31970, None),
          (rates.TOKYO, 150000, 147750 + 3450, 172050 + 3450, 27450), (rates.TOKYO, 300000, 295500 + 6900, 344100 + 6900, 54900),
          (rates.TOKYO, 710000, 699350 + 16330, 814370 + 16330, None),
          (1013, 58000, 58754 + 1334, 68150 + 1334, None), (1013, 200000, 202600 + 4600, 235000 + 4600, 36600),
          (1013, 410000, 415330 + 9430, 481750 + 9430, 75030), (1013, 650000, 658450 + 14950, 763750 + 14950, 118950),
          (1013, 1390000, 1408070 + 31970, 1633250 + 31970, None)]

async def body(pg):
    n = bad = 0
    def ng(*a):
        nonlocal bad
        bad += 1; print('NG', *a)
    # 0 自分の計算を原本の保険料額表の値と比べる
    for pr, s, k0, k1, nk in GENPON:
        n += 1
        if F(s * (pr + SIEN), 1000) != k0 or F(s * (pr + SIEN + KAIGO), 1000) != k1 or (nk is not None and F(s * NENKIN, 10000) != nk):
            ng('原本の料額表と自分の計算', pr, s)
    # 0-2 JS が書き換える前の、HTML に直に書いた既定の結果(東京都・30万円・〜39歳・1人)
    import re
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'hoteifukurihi', 'index.html'), encoding='utf-8').read()
    e = ref(rates.TOKYO, [(300000, 0, 1)]); f = lambda v: '{:,}'.format(v)
    for s in ['<b id="o-a">%s<i>円</i></b>' % f(e['co']), '<b id="o-b">%s<i>円</i></b>' % f(e['me']), '<b id="o-c">%s<i>円</i></b>' % f(e['total']),
              '<li id="o-1">健康保険（介護保険・子ども・子育て支援金を含む）%s円（会社%s円・本人%s円）</li>' % (f(e['K']), f(e['coK']), f(e['K'] - e['coK'])),
              '<li id="o-2">厚生年金%s円（会社%s円・本人%s円）・子ども・子育て拠出金%s円（会社だけ）・対象1人</li>' % (f(e['N']), f(e['coN']), f(e['N'] - e['coN']), f(e['Y']))]:
        n += 1
        if s not in raw: ng('直に書いた既定の結果', s)
    # 0-3 JS に小数の定数や小数の割り算が残っていないか(整数で掛けてから割る)
    js = raw[raw.index('var STD='):raw.index('window.__hf')]
    n += 1
    if re.search(r'\d\.\d|/10000\b|/20000\b(?!;return)|1e-9', js.split('function calc')[1].split('var rows')[0]): ng('calc に小数の計算が残っている')
    # 0-4 文「会社負担と本人負担は、1人につき1円までずれる」:健康保険の差は人数以内・厚生年金は差なし(自分の計算で全県・全等級)
    mx = 0
    for r in sorted(set(r for _, r in PREF)):
        for a in range(3):
            for c in (1, 7, 30):
                for s in STD:
                    x = ref(r, [(s, a, c)]); n += 1
                    d = abs(x['coK'] - (x['K'] - x['coK'])); mx = max(mx, d)
                    if d > c or x['coN'] != x['N'] - x['coN']: ng('会社と本人の差が人数を超える', r, s, a, c, d)
    n += 1
    if mx < 2: ng('差が2円以上になる例が無い(文と合わない)', mx)
    # 1 都道府県の料率(選択肢の値と表示)
    opts = await pg.eval_on_selector_all('#pref option', 'os=>os.map(o=>[o.textContent,o.value,o.selected])')
    n += 1
    if len(opts) != 47: ng('都道府県の数', len(opts))
    for (name, r), o in zip(PREF, opts):
        n += 1
        if o[0] != '%s（%d.%02d%%）' % (name, r // 100, r % 100) or int(o[1]) != r:
            ng('料率', name, r, o)
    n += 1
    if [o[0][:3] for o in opts if o[2]] != ['東京都']: ng('最初に選ばれている県')
    # 2 計算:全県の料率×全等級×年齢4区分(1人)
    cases = []
    for r in sorted(set(r for _, r in PREF)):
        for s in STD:
            for a in range(4):
                cases.append((r, [(s, a, 1)]))
    # 人数分まとめて(端数が積み上がる組み合わせ)
    for r in (rates.TOKYO, 1013, 1028, 921, 1055, 944):
        cases += [(r, [(150000, 0, 3)]), (r, [(410000, 1, 7), (150000, 0, 5)]), (r, [(58000, 0, 30), (1390000, 1, 30)]),
                  (r, [(98000, 1, 13), (110000, 2, 9), (710000, 3, 4), (260000, 0, 11)]),
                  (r, [(s, a, c) for s, a, c in zip(STD, [0, 1, 2, 3] * 13, list(range(1, 31)) * 2)]),
                  (r, [(650000, 0, 1), (680000, 0, 1), (88000, 0, 1), (78000, 0, 1)]),
                  (r, [(300000, 0, 0)]), (r, [(118000, 1, 29), (126000, 0, 17), (134000, 1, 23)])]
    got = await pg.evaluate('cs=>cs.map(c=>window.__hf.calc(c[0],c[1].map(r=>({s:r[0],a:r[1],c:r[2]}))))', cases)
    for (r, rows), g in zip(cases, got):
        e = ref(r, rows); n += 1
        if any(g[k] != e[k] for k in e): ng('calc', r, rows, g, e)
    # 3 画面:県を選び、行に値を入れて結果の箱を読む
    async def setrows(idx, rows):
        await pg.click('#rst')
        await pg.eval_on_selector('#pref', '(el,i)=>{el.selectedIndex=i;el.dispatchEvent(new Event("change",{bubbles:true}))}', idx)
        for i in range(len(rows) - 1):
            await pg.click('#add')
        for i, (s, a, c) in enumerate(rows):
            for cls, v in (('rs', s), ('ra', a), ('rc', c)):
                await pg.eval_on_selector_all('#rows .rw', '(ws,x)=>{var el=ws[x[0]].querySelector("."+x[1]);el.value=String(x[2]);el.dispatchEvent(new Event("change",{bubbles:true}))}', [i, cls, v])
    for idx, rows in [(12, [(300000, 0, 1)]), (26, [(410000, 1, 7), (150000, 0, 5)]), (0, [(58000, 0, 30), (1390000, 1, 30)]),
                      (40, [(98000, 1, 13), (110000, 2, 9), (710000, 3, 4)]), (14, [(650000, 2, 2), (680000, 3, 1)]),
                      (46, [(150000, 0, 3)])]:
        await setrows(idx, rows)
        r = PREF[idx][1]; e = ref(r, rows); n += 1
        a, b, c = [num(await pg.inner_text(x)) for x in ('#o-a', '#o-b', '#o-c')]
        if (a, b, c) != (e['co'], e['me'], e['total']): ng('画面の3つの箱', PREF[idx][0], rows, (a, b, c), e)
        n += 1
        t1 = await pg.inner_text('#o-1'); t2 = await pg.inner_text('#o-2')
        f = lambda v: '{:,}'.format(v)
        e1 = '健康保険（介護保険・子ども・子育て支援金を含む）%s円（会社%s円・本人%s円）' % (f(e['K']), f(e['coK']), f(e['K'] - e['coK']))
        e2 = '厚生年金%s円（会社%s円・本人%s円）・子ども・子育て拠出金%s円（会社だけ）・対象%d人' % (f(e['N']), f(e['coN']), f(e['N'] - e['coN']), f(e['Y']), e['n'])
        if t1 != e1 or t2 != e2: ng('内訳の文', t1, e1, t2, e2)
        # 4 早見表(選んだ県で1人)の全行
        trs = await pg.eval_on_selector_all('#tb tr', 'ts=>ts.map(t=>[].map.call(t.children,d=>d.textContent))')
        n += 1
        if len(trs) != len(SH): ng('表の行の数', len(trs))
        for s, tr in zip(SH, trs):
            x, y = ref(r, [(s, 0, 1)]), ref(r, [(s, 1, 1)]); n += 1
            if [num(v) for v in tr] != [s, x['co'], x['me'], y['co'], y['me']]: ng('表', PREF[idx][0], tr)
    # 5 「はじめに戻す」で東京都・30万円・〜39歳・1人に戻るか
    await pg.click('#rst'); n += 1
    sel = await pg.eval_on_selector('#pref', 'el=>el.options[el.selectedIndex].textContent')
    if not sel.startswith('東京都'): ng('はじめに戻すで選ばれる県', sel)
    # 6 手で書いた数字(結論・仕訳・料率の表・等級の幅)
    e = ref(rates.TOKYO, [(300000, 0, 1)])
    txt = await pg.inner_text('body')
    f = lambda v: '{:,}'.format(v)
    for s in ['東京都・標準報酬月額30万円・40歳未満の人1人なら、会社負担の法定福利費は月%s円です' % f(e['co']), '預り金（社会保険料）%s' % f(e['me']),
              '普通預金 %s' % f(300000 - e['me']), '法定福利費 %s' % f(e['co']), '普通預金 %s' % f(e['total']),
              '東京都9.85%・大阪府10.13%', '1.62%', '0.23%', '18.3%', '0.36%',
              '（%s円から%s円）' % (f(STD[0]), f(STD[-1])), '（88,000円から650,000円）', '年度の合計573万円', '厚生年金は1か月150万円が上限です',
              '賞与の1,000円未満を切り捨てた標準賞与額', '賞与の保険料がない月は納付額と同じ額になります', '保険料が免除されている人は、人数に含めないでください',
              '1人につき1円までずれることがあります', '更新日：2026年11月21日']:
        n += 1
        if s not in txt.replace('\n', ''): ng('手で書いた数字', s)
    n += 1
    stds = await pg.eval_on_selector_all('#rows .rw:first-child .rs option', 'os=>os.map(o=>+o.value)')
    if stds != STD: ng('標準報酬月額の選択肢')
    return n, bad
run('hoteifukurihi', body)
