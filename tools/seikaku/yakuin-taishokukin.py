# /yakuin-taishokukin/ 役員退職金の手取り。
# 原本:国税庁 No.1420 退職金を受け取ったとき(退職所得控除・2分の1・勤続5年以下の役員等は2分の1にしない・令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/1420.htm
# 国税庁 No.2732 別紙 退職所得の源泉徴収税額の速算表(課税退職所得は1,000円未満切り捨て・税額は1円未満切り捨て・令和8年4月1日現在法令等)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2732_besshi.htm
#   https://www.nta.go.jp/publication/pamph/gensen/zeigakuhyo2026/data/18.pdf (令和8年分)
# 国税庁 役員等勤続年数(1年未満の端数は1年に切り上げ) https://www.nta.go.jp/publication/pamph/hotei/yakuin_taishoku.pdf
# 総務省 退職所得に対する住民税の特別徴収(市町村民税6%・道府県民税4%・それぞれ100円未満切り捨て)
#   https://www.soumu.go.jp/main_sosiki/jichi_zeisei/czaisei/65871.html
# 国税庁 法人税基本通達 9-2-27の3(功績倍率法=退職の直前の給与の額×業務に従事した期間×職責に応じた倍率)
#   https://www.nta.go.jp/law/tsutatsu/kihon/hojin/09/09_02_07.htm
# 照らすもの:window.__taishoku と __kojo・結果の箱・HTML に手で書いた表1と表3の全行・JS が作る表2(5つの倍率)・本文の例の数字・JS が書き換える前の文
# 国税庁 No.2737 特定役員退職手当等(役員等勤続年数が5年以下は2分の1にしない・4年11か月は5年) https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2737.htm
# 国税庁 No.2732(申告書がないときは20.42%・翌月10日・死亡退職・前年以前4年内と確定拠出年金の一時金は9年内) https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2732.htm
# 国税庁 No.5208(損金に入れる時期・内定した額の未払金) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5208.htm
# 2026-11-20:JS が作る表4(#tb3 勤続20・25・30・35年×8つの退職金)の全行と見出しの控除・よくある質問の数字・関連リンクの数字・id の重なりを足した
# 2026-11-21:計算の箱と表2・表4に直に書いた既定の結果(JS が動く前のファイルの中身)・箱の注の文・勤続年数の質問の文を足した
# 総務省 65871(市町村民税6%・道府県民税4%・退職所得の金額は1,000円未満切り捨て・税額はそれぞれ100円未満切り捨て)を開き直した
# 大阪市 退職所得の課税の特例・広島市 退職所得に対する住民税のあらまし(指定都市も市民税6%・道府県民税4%)
#   https://www.city.osaka.lg.jp/zaisei/page/0000370614.html https://www.city.hiroshima.lg.jp/soshiki/26/1962.html
# 国税庁 No.2732(前に受け取った退職手当等の計算の基礎となった期間は勤続期間から除く。退職給与規程などで今回の計算の基礎に含める期間は除かない)
# 厚生労働省 いわゆる退職金の前払いに係る社会保険料の取扱いについて(平成15年10月1日 保保発第1001002号・庁保険発第1001001号。
#   退職時に支払われる退職金は報酬にも賞与にも該当しない。在職中の前払いは該当する) https://www.mhlw.go.jp/web/t_doc?dataId=00tb1107&dataType=1&pageNo=1
# 国税庁 No.5203(相当な額の判定:業務に従事した期間・退職の事情・同業種同規模の法人の支給状況) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5203.htm
# 開けなかった原本(2026-11-21):e-Gov の法人税法施行令70条・地方税法50条の4・328条の3、国税庁 No.2260
# 最後に原本を確かめた日:2026-11-21
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from _lib import run
SOKUSAN = [(1950000, 5, 0), (3300000, 10, 97500), (6950000, 20, 427500), (9000000, 23, 636000),
           (18000000, 33, 1536000), (40000000, 40, 2796000), (None, 45, 4796000)]
def kojo(n):
    return max(800000, 400000 * n) if n <= 20 else 8000000 + 700000 * (n - 20)
def ref(g, n):
    k = max(0, g - kojo(n))
    base = (k if n <= 5 else k // 2) // 1000 * 1000
    for top, r, d in SOKUSAN:
        if top is None or base <= top:
            kijun = base * r // 100 - d          # 課税退職所得は1,000円単位なので割り切れる
            it = max(0, kijun) * 1021 // 1000    # 復興特別所得税を合わせて1円未満切り捨て
            break
    shi = base * 6 // 100 // 100 * 100
    ken = base * 4 // 100 // 100 * 100
    return {'it': it, 'ju': shi + ken, 'net': g - it - shi - ken}
async def body(pg):
    n = bad = 0
    gs = [0, 1, 800000, 800001, 4000000, 8000000, 8001000, 15000000, 15001999, 30000000, 50000000,
          90000000, 150000000, 400000000, 1234567890]
    # 速算表の境目の前後(課税退職所得がちょうど境目になる退職金)
    for top, _, _ in SOKUSAN[:-1]:
        for yrs in (3, 20, 30):
            g0 = top + kojo(yrs) if yrs <= 5 else top * 2 + kojo(yrs)
            gs += [g0 - 2000, g0 - 1, g0, g0 + 1, g0 + 1999, g0 + 2000]
    for yrs in (1, 2, 5, 6, 19, 20, 21, 30, 45, 60):
        for g in gs:
            got = await pg.evaluate('([g,n])=>window.__taishoku(g,n)', [g, yrs])
            exp = ref(g, yrs); n += 1
            if any(got[k] != exp[k] for k in exp):
                bad += 1; print('NG', g, yrs, got, exp)
    # 画面の既定(月100万・30年・倍率3.0)の表示
    g = 1000000 * 30 * 3; exp = ref(g, 30); n += 1
    shown = int(''.join(c for c in await pg.inner_text('#o-n') if c.isdigit()))
    if shown != exp['net']:
        bad += 1; print('NG 既定の手取りの表示', shown, exp['net'])

    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, got, want)
    def d(t):
        return int(''.join(c for c in t if c.isdigit()) or 0)
    def man(v):
        return '{:,}'.format(v // 10000)

    # 退職所得控除(No.1420:20年以下は40万円×年数で80万円が下限・20年超は800万円+70万円×(年数-20)) 1年から60年まで
    for y in range(1, 61):
        chk('控除 %d年' % y, await pg.evaluate('n=>window.__kojo(n)', y), kojo(y))

    # HTML に手で書いた表1(勤続30年・退職金ごとの税金と手取り)の全行
    # 2026-11-20:表1は列が7つになった(退職金・課税される退職所得・所得税・住民税・税金の合計・手取り・税金の割合)
    rows = await pg.eval_on_selector_all('#tb tr', """rs=>rs.map(r=>({s:r.getAttribute('data-s'),
        c:[...r.children].map(td=>td.textContent.trim())}))""")
    chk('表1の行の数', [r['s'] for r in rows], ['1000', '1500', '2000', '3000', '4000', '5000', '7000', '10000'])
    for r in rows:
        g = int(r['s']) * 10000; e = ref(g, 30)
        tax = g - e['net']
        wari = (Fraction(tax * 1000, g) + Fraction(1, 2)).__floor__()      # 0.1%の位に四捨五入
        kz = max(0, g - kojo(30)) // 2 // 1000 * 1000
        chk('表1 %s 全部の列' % r['s'], r['c'],
            ['{:,}'.format(int(r['s'])), '{:,}'.format(kz), '{:,}'.format(e['it']), '{:,}'.format(e['ju']),
             '{:,}'.format(tax), '{:,}'.format(e['net']), '%d.%d%%' % (wari // 10, wari % 10)])
    # HTML に手で書いた表3(勤続年数ごとの控除と3,000万円の手取り)の全行
    rows = await pg.eval_on_selector_all(':is(#kojo ~ .tw):not(#kojo ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    chk('表3の行の数', [r[0] for r in rows], ['%d年' % y for y in (5, 10, 15, 20, 25, 30, 35, 40)])
    for r in rows:
        y = d(r[0]); e = ref(30000000, y)
        chk('表3 %d年 控除' % y, r[1], man(kojo(y)) + '万円')
        chk('表3 %d年 手取り' % y, r[2], '{:,}'.format(e['net']) + ('2分の1にしない' if y <= 5 else ''))

    # JS が作る表4(勤続年数で手取りはどう変わるか)の全行と、見出しに手で書いた控除の額
    heads = await pg.eval_on_selector_all(':is(#nen ~ .tw):not(#nen ~ .tw ~ .tw) thead th', "hs=>hs.map(h=>h.innerText.replace(/\\s+/g,''))")
    NS4 = (20, 25, 30, 35)
    chk('表4の見出し', heads, ['退職金（万円）'] + ['勤続%d年控除%s万円' % (y, man(kojo(y))) for y in NS4])
    rows = await pg.eval_on_selector_all('#tb3 tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
    chk('表4の行の数', [r[0] for r in rows], ['{:,}'.format(x) for x in (1000, 1500, 2000, 3000, 4000, 5000, 7000, 10000)])
    for r in rows:
        g = d(r[0]) * 10000
        for i, y in enumerate(NS4):
            chk('表4 %s万円 %d年' % (r[0], y), r[1 + i], '{:,}'.format(ref(g, y)['net']))
    # 特定役員退職手当等(No.2737):5年以下は2分の1にしない。5年と6年の境目を同じ退職金で比べる
    for g in (3000000, 10000000, 30000000):
        k5 = max(0, g - kojo(5)) // 1000 * 1000; k6 = max(0, g - kojo(6)) // 2 // 1000 * 1000
        chk('5年は2分の1にしない %d' % g, (await pg.evaluate('g=>window.__taishoku(g,5)', g))['base'], k5)
        chk('6年は2分の1にする %d' % g, (await pg.evaluate('g=>window.__taishoku(g,6)', g))['base'], k6)
    # id の重なり(目次のリンクが別の部品へ飛ばないこと)と、目次の行き先が見出しであること
    ids = await pg.eval_on_selector_all('[id]', 'es=>es.map(e=>e.id)')
    chk('id の重なり', sorted(set(i for i in ids if ids.count(i) > 1)), [])
    chk('目次の行き先', await pg.eval_on_selector_all('nav.toc a', "as=>as.map(a=>{var e=document.getElementById(a.getAttribute('href').slice(1));return e&&e.tagName==='H2'&&e.innerText.replace(/\\s+/g,'')===a.textContent.replace(/\\s+/g,'')})"), [True] * 8)

    # 本文の例の数字(勤続30年・3,000万円)
    e = ref(30000000, 30); kazei = (30000000 - kojo(30)) // 2
    txt = await pg.inner_text('main')
    flat = ''.join(txt.split())
    for label, want in [
        ('冒頭の文', '勤続30年で3,000万円を受け取ると、税金は{:,}円で手取りは{:,}円です。'.format(30000000 - e['net'], e['net'])),
        ('表1の注の控除', '勤続30年の退職所得控除は%s万円です。退職金から%s万円を引いて' % (man(kojo(30)), man(kojo(30)))),
        ('例の課税の額', '3,000万円から%s万円を引いて2分の1にした%s万円に税金がかかります。' % (man(kojo(30)), man(kazei))),
        ('例の所得税', '所得税は、%s万円×23%%−636,000円に102.1%%を掛けた%s円です。' % (man(kazei), '{:,}'.format(e['it']))),
        ('例の住民税', '住民税は{:,}円です。'.format(e['ju'])),
        ('控除の注', '勤続20年までは1年につき40万円（80万円に満たないときは80万円）、20年を超えた分は1年につき70万円です。'),
        ('申告書がない場合', '退職金の20.42%を差し引きます'),
        ('計算のしかたの住民税', '住民税は、2の額の6%と4%の合計（それぞれ100円未満は切り捨て）'),
        ('よくある質問 3,000万円', '役員としての勤続年数が30年なら、税金は所得税{:,}円と住民税{:,}円の合計{:,}円です。手取りは{:,}円です。'.format(e['it'], e['ju'], e['it'] + e['ju'], e['net'])),
        ('よくある質問 20.42%', '出していないときは20.42%が差し引かれ、確定申告で精算します。'),
        ('よくある質問 50%', '報酬がおおむね50%以上減った。'),
        ('5年以下 4年11か月', '勤続4年11か月は5年と数えるので、2分の1にしません。5年1か月は6年と数えるので、2分の1にします。'),
        ('控除の注 9年', '確定拠出年金（iDeCoなど）の一時金は前の年以前9年で判定します（令和8年1月1日以後に受け取った一時金が対象。改正前は4年）。'),
        ('控除の注 4年', '前の年以前4年のうちに別の退職金を受け取っていて'),
        ('表1の注の住民税', '住民税は、市区町村民税6%と道府県民税4%です。'),
        ('源泉徴収の期限', '原則として翌月10日までに納めます'),
        ('関連 法人税800万円', '中小法人の法人税の税率は、所得800万円を境に変わります。'),
        ('関連 所得税の税率', '所得税の税率は、課税される所得の額で%d%%から%d%%まで変わります。' % (SOKUSAN[0][1], SOKUSAN[-1][1])),
        ('更新日', '更新日：2026年11月21日（令和8年4月1日現在の法令）'),
        ('箱の注 申告書', '「退職所得の受給に関する申告書」を会社に出している場合の税額です'),
        ('箱の注 ほかの退職金', 'ほかに受け取った退職金がない場合の計算です'),
        ('箱の注 従業員の期間', '従業員だった期間がない場合の計算です'),
        ('よくある質問 前に受け取った退職金', 'ただし従業員のときに退職金を受け取っていれば、その期間は原則として含めません。'),
        ('よくある質問 5年の数え方', '2分の1にしない決まりの5年は、役員だった期間だけで数えます。'),
        ('よくある質問 社会保険料', '健康保険料と厚生年金保険料もかかりません。'),
        ('計算のしかた 1,000円未満', '残りを2分の1にする（1,000円未満は切り捨て）'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('例の速算表の段', (6950000 < kazei <= 9000000, kazei * 23 // 100 - 636000), (True, e['it'] * 1000 // 1021 + (1 if (e['it'] * 1000) % 1021 else 0)))
    chk('20.42%=20%×102.1%', Fraction(20, 100) * Fraction(1021, 1000), Fraction(2042, 10000))

    # JS が書き換える前の元の文(ファイルの中身)と、既定の選び方
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'yakuin-taishokukin', 'index.html'), encoding='utf-8').read()
    chk('元の文 倍率の注', '功績倍率3.0で計算' in raw, True)
    chk('元の文 既定の倍率', '<option value="30" selected' in raw, True)
    chk('元の文 既定の月額と年数', ('id="mon" inputmode="numeric" min="0" max="10000000" step="10000" value="1000000"' in raw, 'step="1" value="30"' in raw), (True, True))
    chk('説明の文 8行の範囲', '役員退職金1,000万円から1億円まで' in raw, True)
    # 2026-11-21:計算の箱と表2・表4に直に書いた既定の結果(月100万円・30年・倍率3.0)。JS が動かなくても同じ数字が出ること
    g0 = 1000000 * 30 * 3; e0 = ref(g0, 30); c = '{:,}'.format
    for label, want in [
        ('退職金の額', '<b id="o-g2">%s<i>円</i></b><em id="o-g">報酬月額×30年×倍率3.0</em>' % c(g0)),
        ('手取り', '<b id="o-n">%s<i>円</i></b><em id="o-k">退職所得控除 %s万円</em>' % (c(e0['net']), man(kojo(30)))),
        ('税金の合計', '<b id="o-tz">%s<i>円</i></b><em id="o-h">2分の1にして計算</em>' % c(e0['it'] + e0['ju'])),
        ('内訳', '<li id="o-tzl">税金の内訳は、所得税%s円（復興特別所得税を含む）・住民税%s円です</li>' % (c(e0['it']), c(e0['ju']))),
        ('倍率の注', 'id="bainote">功績倍率3.0で計算しています。報酬の月額×勤続年数×功績倍率です。</p>'),
        ('表2', '<tbody id="tb2">' + ''.join('<tr><td class="c">%d万円</td>' % x + ''.join('<td>%s</td>' % c(x * y * 3) for y in (10, 15, 20, 25, 30, 35)) + '</tr>'
                                            for x in (30, 50, 70, 100, 150)) + '</tbody>'),
        ('表4', '<tbody id="tb3">' + ''.join('<tr><td>%s</td>' % c(a) + ''.join('<td>%s</td>' % c(ref(a * 10000, y)['net']) for y in (20, 25, 30, 35)) + '</tr>'
                                            for a in (1000, 1500, 2000, 3000, 4000, 5000, 7000, 10000)) + '</tbody>'),
    ]:
        chk('元の文 既定の結果 ' + label, want in raw, True)
    chk('元の文 0円のままの結果', '>0<i>円</i>' in raw, False)
    # 住民税の端数(総務省:市町村民税と道府県民税をそれぞれ100円未満切り捨て)。合計してから切り捨てる形と違いが出る額で比べる
    for g in (15002000, 15006000, 15014000, 15018000):
        b = (g - kojo(30)) // 2 // 1000 * 1000
        chk('住民税 それぞれ切り捨て %d' % g, (await pg.evaluate('g=>window.__taishoku(g,30)', g))['ju'], b * 6 // 100 // 100 * 100 + b * 4 // 100 // 100 * 100)

    # 功績倍率法の式(最終報酬月額×勤続年数×功績倍率)と結果の箱・表2・黄色の行
    BAI = [('10', Fraction(1)), ('15', Fraction(3, 2)), ('20', Fraction(2)), ('25', Fraction(5, 2)), ('30', Fraction(3))]
    chk('倍率の選択肢', await pg.eval_on_selector_all('#bai option', 'os=>os.map(o=>[o.value,o.textContent])'),
        [[v, '%d.%d' % (f.numerator * 10 // f.denominator // 10, f.numerator * 10 // f.denominator % 10)] for v, f in BAI])
    TB1 = [1000, 1500, 2000, 3000, 4000, 5000, 7000, 10000]
    for bv, bf in BAI:
        await pg.select_option('#bai', bv)
        bs = '%d.%d' % (bf.numerator * 10 // bf.denominator // 10, bf.numerator * 10 // bf.denominator % 10)
        t2 = await pg.eval_on_selector_all('#tb2 tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
        want = [['%d万円' % x] + ['{:,}'.format(int(x * y * bf)) for y in (10, 15, 20, 25, 30, 35)] for x in (30, 50, 70, 100, 150)]
        chk('表2 倍率' + bs, t2, want)
        chk('表2の注 倍率' + bs, await pg.inner_text('#bainote'), '功績倍率%sで計算しています。報酬の月額×勤続年数×功績倍率です。' % bs)
        for m, y in [(300000, 1), (300000, 5), (500000, 6), (800000, 10), (1000000, 20), (1000000, 30), (1500000, 35),
                     (2000000, 40), (3000000, 45), (10000000, 60), (0, 30), (650000, 21)]:
            await pg.fill('#mon', str(m)); await pg.fill('#yrs', str(y))
            gq = m * y * bf
            if gq.denominator != 1:
                continue
            g = int(gq); e = ref(g, y)
            chk('箱 退職金 %d %d %s' % (m, y, bs), d(await pg.inner_text('#o-g2')), g)
            chk('箱 手取り %d %d %s' % (m, y, bs), d(await pg.inner_text('#o-n')), e['net'])
            chk('箱 税金 %d %d %s' % (m, y, bs), d(await pg.inner_text('#o-tz')), e['it'] + e['ju'])
            chk('箱 内訳 %d %d %s' % (m, y, bs), await pg.inner_text('#o-tzl'),
                '税金の内訳は、所得税{:,}円（復興特別所得税を含む）・住民税{:,}円です'.format(e['it'], e['ju']))
            chk('箱 式 %d %d %s' % (m, y, bs), await pg.inner_text('#o-g'), '報酬月額×%d年×倍率%s' % (y, bs))
            chk('箱 控除 %d %d %s' % (m, y, bs), await pg.inner_text('#o-k'), '退職所得控除 %s万円' % man(kojo(y)))
            chk('箱 2分の1 %d %d %s' % (m, y, bs), await pg.inner_text('#o-h'), '2分の1にしない' if y <= 5 else '2分の1にして計算')
            near = min(TB1, key=lambda s: (abs(s * 10000 - g), TB1.index(s)))
            chk('黄色の行 %d %d %s' % (m, y, bs), await pg.eval_on_selector_all('#tb tr.hit', "rs=>rs.map(r=>r.getAttribute('data-s'))"), [str(near)])
    return n, bad
run('yakuin-taishokukin', body)
