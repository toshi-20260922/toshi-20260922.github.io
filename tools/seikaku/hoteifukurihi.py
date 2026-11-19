# /hoteifukurihi/ 法定福利費の計算(社会保険料の会社負担・本人負担・年金事務所に納める額)。
# 原本:
#  全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分(4月納付分)から改定されます」(47都道府県の健康保険料率・介護1.62%・子ども・子育て支援金0.23%は令和8年4月分から)
#   https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#  全国健康保険協会「令和8年3月分(4月納付分)からの健康保険・厚生年金保険の保険料額表」東京・大阪(等級58,000〜1,390,000円・厚生年金88,000〜650,000円・全額の値)
#   https://www.kyoukaikenpo.or.jp/assets/R8_13tokyo.pdf  https://www.kyoukaikenpo.or.jp/assets/R8_27osaka.pdf
#  日本年金機構「保険料の計算方法について」(納入告知額は制度ごとに合計して1円未満切り捨て・被保険者ごとに端数処理しない・本人負担は50銭以下切り捨て50銭超切り上げ・事業主負担は納入告知額から本人負担の合計を引く)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/nofu/20121026.html
#  日本年金機構「厚生年金保険料額表(令和8年度版)」(18.300%・子ども・子育て拠出金0.36% 令和8年4月1日〜適用)
#   https://www.nenkin.go.jp/service/kounen/hokenryo/ryogaku/ryogakuhyo/20200825.files/R08ryougaku.pdf
#  厚生労働省・こども家庭庁「子ども・子育て支援金に関するQ&A」令和8年2月12日 問6(本人負担は一般保険料率と支援金率を合算した率で折半してから端数処理)
#   https://www.mhlw.go.jp/hourei/doc/tsuchi/T260216S0101.pdf
# 最後に原本を確かめた日:2026-11-19
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

# 協会けんぽ 令和8年度の健康保険料率(%を100倍した整数)。原本のページから写した。
PREF = [('北海道', 1028), ('青森県', 985), ('岩手県', 951), ('宮城県', 1010), ('秋田県', 1001), ('山形県', 975),
        ('福島県', 950), ('茨城県', 952), ('栃木県', 982), ('群馬県', 968), ('埼玉県', 967), ('千葉県', 973),
        ('東京都', 985), ('神奈川県', 992), ('新潟県', 921), ('富山県', 959), ('石川県', 970), ('福井県', 971),
        ('山梨県', 955), ('長野県', 963), ('岐阜県', 980), ('静岡県', 961), ('愛知県', 993), ('三重県', 977),
        ('滋賀県', 988), ('京都府', 989), ('大阪府', 1013), ('兵庫県', 1012), ('奈良県', 991), ('和歌山県', 1006),
        ('鳥取県', 986), ('島根県', 994), ('岡山県', 1005), ('広島県', 978), ('山口県', 1015), ('徳島県', 1024),
        ('香川県', 1002), ('愛媛県', 998), ('高知県', 1005), ('福岡県', 1011), ('佐賀県', 1055), ('長崎県', 1006),
        ('熊本県', 1008), ('大分県', 1008), ('宮崎県', 977), ('鹿児島県', 1013), ('沖縄県', 944)]
KAIGO, SIEN, NENKIN, KYOSHUTSU = 162, 23, 1830, 36          # 1万分の1の単位
# 健康保険の標準報酬月額 50等級(千円)。厚生年金は 88〜650 の32等級。
STD = [58, 68, 78, 88, 98, 104, 110, 118, 126, 134, 142, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300,
       320, 340, 360, 380, 410, 440, 470, 500, 530, 560, 590, 620, 650, 680, 710, 750, 790, 830, 880, 930, 980,
       1030, 1090, 1150, 1210, 1270, 1330, 1390]
STD = [x * 1000 for x in STD]
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
            p = min(max(s, 88000), 650000)
            nen += F(p * NENKIN * c, 10000)
            kyo += F(p * KYOSHUTSU * c, 10000)
            mn += half(F(p * NENKIN, 20000)) * c
    K, N, Y = ken.numerator // ken.denominator, nen.numerator // nen.denominator, kyo.numerator // kyo.denominator
    return {'K': K, 'N': N, 'Y': Y, 'total': K + N + Y, 'me': mk + mn, 'co': K + N + Y - mk - mn,
            'coK': K - mk, 'coN': N - mn, 'n': n}

# 原本の保険料額表の値(全額)。(料率, 標準報酬月額, 40歳未満の健康保険+支援金の全額×10, 40〜64歳の全額×10, 厚生年金の全額)
GENPON = [(985, 150000, 147750 + 3450, 172050 + 3450, 27450), (985, 300000, 295500 + 6900, 344100 + 6900, 54900),
          (985, 710000, 699350 + 16330, 814370 + 16330, None),
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
    for r in (985, 1013, 1028, 921, 1055, 944):
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
    e = ref(985, [(300000, 0, 1)])
    txt = await pg.inner_text('body')
    f = lambda v: '{:,}'.format(v)
    for s in ['会社負担の法定福利費は月%s円です' % f(e['co']), '預り金（社会保険料）%s' % f(e['me']),
              '普通預金 %s' % f(300000 - e['me']), '法定福利費 %s' % f(e['co']), '普通預金 %s' % f(e['total']),
              '東京都9.85%・大阪府10.13%', '1.62%', '0.23%', '18.3%', '0.36%',
              '（%s円から%s円）' % (f(STD[0]), f(STD[-1])), '（88,000円から650,000円）', '年度の合計573万円', '150万円']:
        n += 1
        if s not in txt.replace('\n', ''): ng('手で書いた数字', s)
    n += 1
    stds = await pg.eval_on_selector_all('#rows .rw:first-child .rs option', 'os=>os.map(o=>+o.value)')
    if stds != STD: ng('標準報酬月額の選択肢')
    return n, bad
run('hoteifukurihi', body)
