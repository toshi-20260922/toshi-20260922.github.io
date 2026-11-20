# /chukosha-taiyonensu/ 中古車の耐用年数の計算。
# 原本:
#  国税庁 No.5404「中古資産の耐用年数」(令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/hojin/5404.htm
#   簡便法:全部経過=法定耐用年数×20%/一部経過=(法定耐用年数−経過年数)+経過年数×20%/1年未満切り捨て/2年未満は2年(耐用年数省令3条)
#  国税庁 No.2106「定額法と定率法による減価償却」(令和8年4月1日現在法令等) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/2106.htm
#   定額法=取得価額×償却率/定率法=期首未償却残高×償却率。調整前償却額<償却保証額(取得価額×保証率)の年から 改定取得価額×改定償却率/年の中途は ÷12×月数/1円を残す
#  国税庁「法人の減価償却制度の改正に関するQ&A」(平成24年2月)参考資料 200%定率法の償却率・改定償却率・保証率 https://www.nta.go.jp/publication/pamph/hojin/kaisei_gaiyo2011/pdf/1112kaisei_faq.pdf
#  国税庁 資料編(定額法の償却率・耐用年数省令別表第八) https://www.nta.go.jp/law/joho-zeikaishaku/shotoku/shinkoku/070412/pdf/3.pdf
#  国税庁「主な減価償却資産の耐用年数表」(車両・運搬具:その他6年・貨物その他5年・小型車とダンプ式4年・二輪三輪3年) https://www.nta.go.jp/taxes/shiraberu/taxanswer/shotoku/pdf/2100_01.pdf
#  国税庁「法人の減価償却制度の改正に関するQ&A」(平成19年4月) https://www.nta.go.jp/law/joho-zeikaishaku/hojin/h19/genkaqa.pdf
#   事業年度の中途で事業の用に供したとき=年の額÷事業年度の月数×事業の用に供した日から期末までの月数(令59①一)。月数は暦に従い1月に満たない端数は1月
#   届出をしないときは法定償却方法(令53)。残存簿価1円まで(令61②③)
#  国税庁 No.2100「減価償却のあらまし」(令和8年4月1日現在法令等):個人の法定の償却方法は定額法
#  国税庁 青色申告決算書の書き方(令和7年分):月の中途で取得した月は1か月として数える・届け出ていない方は定額法
#  国税庁 確定申告書等作成コーナー「減価償却費の端数処理」:個人の減価償却費の小数点以下の端数は切り上げ
#   https://www.keisan.nta.go.jp/r5yokuaru/aoiroshinkoku/hitsuyokeihi/genkashokyakuhi/hasushori.html
# 最後に原本を確かめた日:2026-11-21(e-Gov の条文そのものは開けていない。条文番号は国税庁の上の資料で確かめた)
# 端数:期ごとの償却費の1円未満は、法人は切り捨て(償却限度額を超えない向き。条文に定めなし)、個人事業主は切り上げ(作成コーナーと同じ。2026-11-21 にページを切り捨てから直した)。
import os, sys, re
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run, num

# 定率法(平成24年4月1日以後取得):償却率・改定償却率・保証率
TEI = {2: (F(1), None, None), 3: (F(667, 1000), F(1), F(11089, 100000)), 4: (F(500, 1000), F(1), F(12499, 100000)),
       5: (F(400, 1000), F(500, 1000), F(10800, 100000)), 6: (F(333, 1000), F(334, 1000), F(9911, 100000))}
GAKU = {2: F(500, 1000), 3: F(334, 1000), 4: F(250, 1000), 5: F(200, 1000), 6: F(167, 1000)}

def ref_life(L, m):
    """L=法定耐用年数(年) m=経過月数。月で計算して最後に1年未満を切り捨てる。"""
    if m <= 0:
        return L
    Lm = L * 12
    mon = F(Lm, 5) if m >= Lm else (Lm - m) + F(m, 5)
    return max(int(mon // 12), 2)

def ref_sched(cost, n, corp, mon1):
    out, book, rev = [], cost, None
    for i in range(n + 2):
        if book <= 1:
            break
        mo = mon1 if i == 0 else 12
        if corp:
            r, kai, ho = TEI[n]
            ann = book * r
            if rev is not None:
                ann = rev * kai
            elif ho is not None and ann < cost * ho:
                rev = book
                ann = rev * kai
        else:
            ann = cost * GAKU[n]
        x = ann * mo / 12
        a = int(x) if corp else -int(-x // 1)   # 1円未満:法人は切り捨て・個人事業主は切り上げ
        if a > book - 1:
            a = book - 1                # 1円を残す
        book -= a
        out.append(a)
    return out

async def body(pg):
    n = bad = 0
    # 0 個人事業主の1円未満は切り上げ(作成コーナー):1,234,567円×0.500=617,283.5円→617,284円。法人は切り捨て:1,000,001円×0.333=333,000.333→333,000円
    n += 2
    if ref_sched(1234567, 2, 0, 12) != [617284, 617282]:
        bad += 1; print('NG 個人の切り上げの例', ref_sched(1234567, 2, 0, 12))
    if ref_sched(1000001, 6, 1, 12)[0] != 333000:
        bad += 1; print('NG 法人の切り捨ての例', ref_sched(1000001, 6, 1, 12))
    # 0-2 計算の箱に直に書いた既定の結果(JS が書き換える前の HTML)が、既定の入力の結果と同じか
    raw = open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'site', 'chukosha-taiyonensu', 'index.html'), encoding='utf-8').read()
    d_m = (2026 * 12 + 12) - (2022 * 12 + 9); d_y = ref_life(6, d_m); d_mon = (3 - 12) % 12 + 1; d_s = ref_sched(3000000, d_y, 1, d_mon)
    for want in ('<p class="res-msg" id="o-msg">経過%dか月（%d年%dか月落ち）です。今期に使う月数は%dか月です。</p>' % (d_m, d_m // 12, d_m % 12, d_mon),
                 '<b id="o-a">%d<i>年</i></b><em id="o-ae">法定6年</em>' % d_y,
                 '<b id="o-b">{:,}<i>円</i></b><em id="o-be">{}か月分</em>'.format(d_s[0], d_mon),
                 '<b id="o-c">{:,}<i>円</i></b><em id="o-ce">12か月分</em>'.format(d_s[1]),
                 '<li id="o-1">定率法・償却率1.000で計算しました。期ごとの額：' + '→'.join('{:,}円'.format(x) for x in d_s) + '</li>'):
        n += 1
        if want not in raw:
            bad += 1; print('NG 既定の結果(HTML)', want)
    # 1 耐用年数:関数を全部の月で
    for L in (3, 4, 5, 6):
        for m in range(0, 400):
            got = await pg.evaluate('([L,m])=>window.__ck.life(L,m)', [L, m]); n += 1
            if got != ref_life(L, m):
                bad += 1; print('NG life', L, m, got, ref_life(L, m))
    # 2 期ごとの償却費:関数
    costs = [1000, 99999, 100001, 333333, 1000000, 1234567, 2999999, 3000000, 3000001, 4567891,
             7777777, 9999999, 12345678, 50000000, 123456789]
    for cost in costs:
        for yrs in (2, 3, 4, 5, 6):
            for corp in (1, 0):
                for mon1 in range(1, 13):
                    got = await pg.evaluate('([c,y,k,m])=>window.__ck.sched(c,y,k,m)', [cost, yrs, corp, mon1])
                    exp = ref_sched(cost, yrs, corp, mon1); n += 1
                    if got != exp:
                        bad += 1; print('NG sched', cost, yrs, corp, mon1, got, exp)
                    # 期ごとの額を足すと取得価額−1円(全部の期が出ているか)
                    n += 1
                    if sum(exp) != cost - 1:
                        bad += 1; print('NG 合計が取得価額−1円でない', cost, yrs, corp, mon1, exp)
    # 3 画面:入力欄に入れて結果の箱を読む
    async def screen(corp, fy, kind, ry, rm, uy, um, price):
        await pg.click('#kei button[data-v="%d"]' % (0 if corp else 1))
        if corp:
            await pg.select_option('#fy', str(fy))
        for i, v in (('kind', kind), ('ry', ry), ('rm', rm), ('uy', uy), ('um', um)):
            await pg.select_option('#' + i, str(v))
        await pg.fill('#price', str(price))
        return (num(await pg.inner_text('#o-a')), num(await pg.inner_text('#o-b')), num(await pg.inner_text('#o-c')),
                await pg.inner_text('#o-msg'), await pg.inner_text('#o-1'), await pg.inner_text('#o-be'), await pg.inner_text('#o-ce'))
    cases = []
    for kind in (6, 5, 4, 3):
        for (ry, rm, uy, um) in ((2026, 12, 2026, 12), (2026, 11, 2026, 12), (2025, 9, 2026, 12), (2025, 8, 2026, 12),
                                 (2024, 6, 2026, 12), (2024, 5, 2026, 12), (2023, 3, 2026, 12), (2023, 2, 2026, 12),
                                 (2022, 9, 2026, 12), (2005, 1, 2028, 12), (2021, 4, 2025, 1)):
            for corp, fy in ((1, 3), (1, 12), (1, 11), (0, 12)):
                cases.append((corp, fy, kind, ry, rm, uy, um, 3000000))
    cases += [(0, 12, k, ry, 1, 2026, um, pr) for k in (6, 4) for ry in (2022, 2025, 2026) for um in (1, 6, 12) for pr in (1234567, 999999, 1000001)]
    cases += [(1, 3, 6, 2022, 9, 2026, 4, 3000000), (1, 12, 4, 2020, 1, 2027, 1, 1234567),
              (1, 3, 6, 2022, 9, 2026, 12, 1234567), (0, 12, 6, 2025, 9, 2026, 1, 9999999), (1, 6, 5, 2025, 1, 2026, 7, 4567891)]
    for c in cases:
        corp, fy, kind, ry, rm, uy, um, price = c
        a, b, cc, msg, li, be, ce = await screen(*c)
        m = (uy * 12 + um) - (ry * 12 + rm)
        yrs = ref_life(kind, m)
        mon1 = ((fy if corp else 12) - um) % 12 + 1
        s = ref_sched(price, yrs, corp, mon1)
        rate = (TEI[yrs][0] if corp else GAKU[yrs])
        exp_rate = '%d.%03d' % (rate * 1000 // 1000, rate * 1000 % 1000)
        n += 1
        ok = (a == yrs and b == s[0] and cc == (s[1] if len(s) > 1 else 0) and ce == ('12か月分' if len(s) > 1 else '') and ('今期に使う月数は%dか月' % mon1) in msg
              and be == '%dか月分' % mon1 and ('償却率' + exp_rate) in li and ('定率法' if corp else '定額法') in li
              and li.endswith('→'.join('{:,}円'.format(x) for x in s))
              and (('経過%dか月（%d年%dか月落ち）' % (m, m // 12, m % 12)) in msg if m else '新車' in msg))
        if not ok:
            bad += 1; print('NG 画面', c, (a, b, cc, msg, li), yrs, s)
    # 使い始めが初度登録より前
    await pg.select_option('#ry', '2026'); await pg.select_option('#rm', '12')
    await pg.select_option('#uy', '2024'); await pg.select_option('#um', '1')
    n += 1
    if '初度登録より前' not in await pg.inner_text('#o-msg'):
        bad += 1; print('NG 前後が逆のときの文')
    # 4 HTML に手で書いた表
    tabs = await pg.evaluate('()=>[...document.querySelectorAll("main table")].map(t=>[...t.querySelectorAll("tbody tr")].map(r=>[...r.querySelectorAll("td")].map(d=>d.innerText.replace(/\\s+/g,""))))')
    # 何年落ちの表:行ごとの月の幅の全部の月で同じ年数か・幅の外へ1か月出ると変わるか
    rng = [(0, 0), (1, 15), (16, 30), (31, 45), (46, 399)]
    labels = ['経過0か月', '経過1〜15か月', '経過16〜30か月', '経過31〜45か月', '経過46か月以上']
    for row, (lo, hi), lab in zip(tabs[0], rng, labels):
        n += 1
        if lab not in row[0]:
            bad += 1; print('NG 表1の行の名前', row[0], lab)
        for col, L in enumerate((6, 5, 4, 3), 1):
            shown = num(row[col]); n += 1
            if any(ref_life(L, m) != shown for m in range(lo, hi + 1)):
                bad += 1; print('NG 表1', row[0], L, shown, [ref_life(L, m) for m in (lo, hi)])
    # 行の名前の「何年何か月」と経過月数が同じか
    for lab, lo, hi in (('1か月〜1年3か月', 1, 15), ('1年4か月〜2年6か月', 16, 30), ('2年7か月〜3年9か月', 31, 45), ('3年10か月以上', 46, None)):
        n += 1
        if not any(lab in r[0] for r in tabs[0]):
            bad += 1; print('NG 表1の年月の名前', lab)
    # 境目:普通乗用車45→3年・46→2年、軽15→3年・16→2年(結論の文)
    for L, m, y in ((6, 45, 3), (6, 46, 2), (4, 15, 3), (4, 16, 2), (5, 30, 3), (5, 31, 2), (3, 0, 3), (3, 1, 2), (6, 15, 5), (6, 16, 4), (6, 30, 4), (6, 31, 3)):
        n += 1
        if ref_life(L, m) != y:
            bad += 1; print('NG 境目', L, m, y)
    ketsu = await pg.inner_text('#calc .h'); n += 1
    if not ('3年10か月落ち（経過46か月）' in ketsu and '1年4か月落ち（経過16か月）' in ketsu and '2年' in ketsu):
        bad += 1; print('NG 結論の文', ketsu)
    # 簡便法の例の文:(72−46)+46×20%=35.2か月=2年11か月→2年
    txt = await pg.inner_text('main'); flat = re.sub(r'\s+', '', txt)
    v = (72 - 46) + F(46, 5); n += 1
    if not (v == F(352, 10) and int(v // 12) == 2 and int(v) % 12 == 11 and '（72か月−46か月）＋46か月×20%＝35.2か月で2年11か月' in flat):
        bad += 1; print('NG 簡便法の例の文')
    # 1年目の減価償却費の表(300万円・耐用年数2年)
    for row, mo in zip(tabs[2], (12, 9, 6, 3, 1)):
        n += 2
        if num(row[0]) != mo:
            bad += 1; print('NG 表3の月数', row)
        if num(row[1]) != ref_sched(3000000, 2, 1, mo)[0]:
            bad += 1; print('NG 表3 法人', row, ref_sched(3000000, 2, 1, mo)[0])
        if num(row[2]) != ref_sched(3000000, 2, 0, mo)[0]:
            bad += 1; print('NG 表3 個人', row, ref_sched(3000000, 2, 0, mo)[0])
    # 法人と個人の違いの表・よく聞かれることの償却率
    n += 1
    if not (tabs[3][1][1] == '1.000' and tabs[3][1][2] == '0.500'):
        bad += 1; print('NG 表4の償却率', tabs[3][1])
    def s3(fr):
        return '%d.%03d' % (fr * 1000 // 1000, fr * 1000 % 1000)
    teis = '・'.join('%d年%s' % (y, s3(TEI[y][0])) for y in (2, 3, 4, 5, 6))
    gaks = '・'.join('%d年%s' % (y, s3(GAKU[y])) for y in (2, 3, 4, 5, 6))
    n += 2
    if ('定率法は、' + teis + 'です') not in flat:
        bad += 1; print('NG 定率法の償却率の文', teis)
    if ('定額法は、' + gaks + 'です') not in flat:
        bad += 1; print('NG 定額法の償却率の文', gaks)
    # 入力欄の法定耐用年数の選択肢
    opts = await pg.evaluate('()=>[...document.querySelectorAll("#kind option")].map(o=>[o.value,o.textContent])')
    want = {'6': '普通乗用車', '5': '貨物自動車（ダンプ式を除く）', '4': '軽自動車・ダンプ式の貨物自動車', '3': '二輪・三輪'}
    for val, t in opts:
        n += 1
        if want.get(val, '?') not in t or ('（%s年）' % val) not in t:
            bad += 1; print('NG 車の種類', val, t)
    # 5 早見表が上・計算の箱が下の並び(2026-11-20):id の重なりなし・早見表が箱より上・黄色の行は1つで全部2年の行
    ids = await pg.evaluate('()=>[...document.querySelectorAll("[id]")].map(e=>e.id)')
    n += 1
    if len(ids) != len(set(ids)):
        bad += 1; print('NG id の重なり', sorted(i for i in set(ids) if ids.count(i) > 1))
    pos = await pg.evaluate('()=>[document.querySelector("#list").getBoundingClientRect().top,document.querySelector("#calc").getBoundingClientRect().top]')
    n += 1
    if not pos[0] < pos[1]:
        bad += 1; print('NG 早見表が計算の箱より下', pos)
    hit = await pg.evaluate('()=>[...document.querySelectorAll("main tr.hit")].map(r=>[...r.querySelectorAll("td")].map(d=>d.innerText.replace(/\\s+/g,"")))')
    n += 1
    if not (len(hit) == 1 and '経過46か月以上' in hit[0][0] and hit[0][1:] == ['2年'] * 4):
        bad += 1; print('NG 黄色の行', hit)
    return n, bad
run('chukosha-taiyonensu', body)
