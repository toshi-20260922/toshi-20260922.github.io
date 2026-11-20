# /gensen-hoshu/ 源泉徴収の早見表(報酬の源泉徴収は要る?要らない?職種の一覧と計算)。
# 原本(どれも令和8年4月1日現在法令等):
# 国税庁 No.2792 源泉徴収が必要な報酬・料金等とは(範囲・消費税・名目・交通費の直接払い)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2792.htm
# 国税庁 No.2795 原稿料や講演料等を支払ったとき(100万円以下 A×10.21%・100万円超 (A−100万円)×20.42%+102,100円・1円未満切り捨て・
#   150万円の例 204,200円・懸賞の賞金 1回5万円以下・翌月10日・納期の特例の対象外)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2795.htm
# 国税庁 No.2798 弁護士や税理士等に支払う報酬・料金(同じ式・登録免許税などの実費・納期の特例 7月10日と翌年1月20日)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2798.htm
# 国税庁 No.2801 司法書士等に支払う報酬・料金((1回の支払い−1万円)×10.21%・5万円の例 4,084円・納期の特例)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2801.htm
# 国税庁 No.2804 外交員等に支払う報酬・料金((その月の額−12万円)×10.21%・給与があれば12万円から給与を引いた残り)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2804.htm
# 国税庁 No.2807 ホステス等に支払う報酬・料金((1回の支払い−5,000円×計算期間の全日数)×10.21%)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2807.htm
# 国税庁 No.2813 広告宣伝のために支払う賞金等((賞金−50万円)×10.21%・物品は評価・金品と選べない旅行は含めない)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2813.htm
# 国税庁 No.2505 源泉所得税及び復興特別所得税の納付期限と納期の特例(翌月10日・常時10人未満・申請して承認・7月10日と翌年1月20日・
#   対象は給与と退職手当と税理士や弁護士や司法書士などの報酬)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2505.htm
# 国税庁 No.2507 復興特別所得税の源泉徴収(合計税率=所得税率×102.1%・1円未満切り捨て・令和9年分からの名前と合計税率は変わらないこと)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/gensen/2507.htm
# 国税庁 No.6929 消費税等と源泉所得税および復興特別所得税(原則は消費税込み・請求書等で区分されていれば報酬の額だけでよい)
#   https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6929.htm
# 国税庁 所得税基本通達 204-1から204-5・204-6から204-10・204-11から204-18
#   https://www.nta.go.jp/law/tsutatsu/kihon/shotoku/36/01.htm  .../36/02.htm  .../36/03.htm
# 国税庁「令和8年版 源泉徴収のあらまし」第5 報酬・料金等の源泉徴収事務(控除額5万円・給与を払っていない個人・類似するが該当しないものの欄・納期の特例の範囲)
#   https://www.nta.go.jp/publication/pamph/gensen/aramashi2026/pdf/07.pdf
# 開けなかった原本:e-Gov法令検索の所得税法204条・205条と所得税法施行令320条・322条(本文が取れない。上のあらましが引く条文番号で確かめた)
# 照らすもの:window.__gensen・結果の箱(要る要らない・額・式・期限)・HTML に手で書いた早見表の全行・種類ごとの式の表・納期の特例の表・本文の例の数字
# 国税庁「防衛特別所得税及び復興特別所得税に関するQ&A(源泉徴収関係)」令和8年5月(令和9年1月から防衛特別所得税1%・復興特別所得税1.1%・合計税率は所得税率×102.1%のまま・
#   端数は合計額で1円未満切り捨て・講演料222,222円の例 22,688円)
#   https://www.nta.go.jp/publication/pamph/pdf/0026005-024_03.pdf
# 国税庁 法令解釈通達「インボイス制度開始後の報酬・料金等に対する源泉徴収」(区分されていれば報酬の額だけ・適格請求書でなくてもよい)
#   https://www.nta.go.jp/law/tsutatsu/kobetsu/shotoku/gensen/111209/01.htm
# 国税庁 質疑応答事例「手話通訳の報酬」(翻訳・通訳のどちらにも当たらず対象外。関係通達 204-6)
#   https://www.nta.go.jp/law/shitsugi/gensen/05/04.htm
# 11/20:金額の欄が10億円で頭打ちになり、20億円と入力しても10億円の結果を出していた(ページの誤り)。上限を1兆円に上げた(1兆円でも整数の計算は正確)。
#   よく聞かれることの「納期の特例を使えるのは、給与と…だけ」に退職金が抜けていた(No.2505 は給与や退職金と一定の報酬)。ページを直した。
#   原本の計算例(ホステス75万円・31日 60,749円、講演料222,222円 22,688円、外交員20万円 8,168円、司法書士5万円 4,084円)と手取り契約の割り戻しを足した。
# 11/20 に開けなかった原本:No.2507・No.6929(許可待ちで時間切れ。同じ中身を上のQ&Aとインボイスの通達と No.2795 で確かめた)・e-Gov の所得税法と施行令
# 11/21:計算の箱に直に書いた既定の結果が「0円」「計算式」「納期の特例」のままだった(申し送りの形16)。既定(個人・給与を払っている側・原稿料など・10万円)の
#   結果 10,210円・89,790円・「支払う金額×10.21%」・「種類によります」に直した。204条1項3号の支払う機関の名前が古かった(社会保険診療報酬支払基金は
#   令和8年10月1日に医療情報基盤・診療報酬審査支払機構に変わった。No.2792 と通達204-19 は新しい名前)。ページを直した。
#   今日開けた原本:No.2792・2795・2798・2801・2804・2807・2813・2505・2507・6929・通達204-6〜10(36/02.htm)・204-19(36/04.htm)・令和8年版あらまし第5。
#   開けなかった原本:e-Gov の所得税法と施行令(今日は開いていない)
# 最後に原本を確かめた日: 2026-11-21
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from _lib import run

R1 = Fraction(1021, 10000)   # 10% × 102.1%
R2 = Fraction(2042, 10000)   # 20% × 102.1%
KOJO = {1: 10000, 2: 120000, 4: 500000, 5: 50000}   # 司法書士等・外交員等・広告宣伝の賞金・プロボクサー

def ref(k, a, d=30):
    """原本の手順。k=0 は原稿料や弁護士など(100万円超は20.42%)。それ以外は控除してから10.21%。1円未満切り捨て。"""
    if k == 0:
        if a <= 1000000:
            return (a * R1).__floor__()
        return ((a - 1000000) * R2 + 102100).__floor__()
    ded = 5000 * d if k == 3 else KOJO[k]
    return (max(0, a - ded) * R1).__floor__()

def c(n):
    return '{:,}'.format(n)

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1; print('NG', label, repr(got), repr(want))

    chk('10.21%=10%×102.1%', Fraction(10, 100) * Fraction(1021, 1000), R1)
    chk('20.42%=20%×102.1%', Fraction(20, 100) * Fraction(1021, 1000), R2)
    chk('102,100円=100万円×10.21%', 1000000 * R1, 102100)

    # 原本に載っている計算例で、自分の計算そのものを確かめる
    chk('原本の例 150万円', ref(0, 1500000), 204200)
    chk('原本の例 講演料222,222円', ref(0, 222222), 22688)
    chk('原本の例 司法書士5万円', ref(1, 50000), 4084)
    chk('原本の例 外交員20万円', ref(2, 200000), 8168)
    chk('原本の例 ホステス75万円・31日', ref(3, 750000, 31), 60749)
    # 手取りで約束した報酬(No.2813 の ÷0.8979 と同じ割り戻し):報酬=手取り÷(1−10.21%) の1円未満切り捨て
    g = (100000 / (1 - R1)).__floor__()
    chk('手取り10万円の報酬', (g, ref(0, g), g - ref(0, g)), (111370, 11370, 100000))

    # 1 window.__gensen を広く(低い・中くらい・高い・境目の前後・端数の出る額)
    amts = [0, 1, 9, 10, 97, 98, 979, 980, 9999, 10000, 10001, 12345, 33333, 49999, 50000, 50001, 55555, 99999, 100000,
            119999, 120000, 120001, 123456, 150000, 200000, 499999, 500000, 500001, 777777, 999990, 999999, 1000000,
            1000001, 1000004, 1000005, 1000009, 1000010, 1234567, 1500000, 2000000, 3000000, 9999999, 123456789, 1000000000]
    for k in (0, 1, 2, 4, 5):
        extra = [KOJO[k] + x for x in (-1, 0, 1, 9, 10, 97, 98)] if k else []
        for a in amts + extra:
            chk('__gensen %d %d' % (k, a), await pg.evaluate('([k,a])=>window.__gensen(k,a,30)', [k, a]), ref(k, a))
    for d in (1, 2, 15, 28, 30, 31, 366):
        for a in amts + [5000 * d - 1, 5000 * d, 5000 * d + 1, 5000 * d + 9, 5000 * d + 10, 5000 * d + 98]:
            chk('__gensen 3 %d %d日' % (a, d), await pg.evaluate('([a,d])=>window.__gensen(3,a,d)', [a, d]), ref(3, a, d))

    # 2 結果の箱(入力欄に値を入れて読む)
    async def box():
        return await pg.evaluate("""()=>({t:document.getElementById('o-t').textContent,n:document.getElementById('o-n').textContent,
          need:document.getElementById('o-need').textContent,why:document.getElementById('o-why').textContent,
          f:document.getElementById('o-f').textContent,e:document.getElementById('o-e').textContent,d:document.getElementById('o-d').textContent,
          l:document.getElementById('l-amt').textContent,days:document.getElementById('daysbox').style.display,
          hit:[...document.querySelectorAll('#tb tr.hit')].map(r=>r.children[0].textContent)})""")
    TB = [10000, 30000, 50000, 100000, 200000, 300000, 500000, 1000000, 1500000, 2000000, 3000000]
    # 既定(個人・給与を払っている側・原稿料など・10万円)
    b = await box()
    chk('既定の箱', (b['t'], b['n'], b['need'], b['d']), ('10,210円', '89,790円', '源泉徴収が必要です', '翌月10日'))
    ui = [0, 1, 10000, 50000, 99999, 100000, 120000, 120001, 200000, 500000, 500001, 999999, 1000000, 1000001, 1000005, 1500000, 3000000, 1000000000]
    for k in (0, 1, 2, 3, 4, 5, 9):
        await pg.select_option('#kind', str(k))
        for who, payer in ((0, 0), (1, 0), (0, 1), (1, 1)):
            await pg.select_option('#who', str(who)); await pg.select_option('#payer', str(payer))
            for a in (ui if (who, payer) == (0, 0) else [100000, 1500000]):
                for d in ((1, 30, 31) if k == 3 else (30,)):
                    if k == 3:
                        await pg.fill('#days', str(d))
                    await pg.fill('#amt', str(a))
                    b = await box(); lab = '箱 種類%d 相手%d 払う側%d %d円 %d日' % (k, who, payer, a, d)
                    # 原本:204条の報酬で、相手が個人で、払う側が給与を払っている(ホステス等は払う側を問わない)ときだけ要る
                    need = k != 9 and who == 0 and (payer == 0 or k == 3)
                    t = ref(k, a, d) if need else 0
                    chk(lab + ' 要否', b['need'], '源泉徴収が必要です' if need else '源泉徴収は不要です')
                    chk(lab + ' 額', b['t'], c(t) + '円')
                    chk(lab + ' 払う額', b['n'], c(a - t) + '円')
                    chk(lab + ' 期限', b['d'], '翌月10日' if need else 'なし')
                    chk(lab + ' 日数の欄', b['days'], '' if k == 3 else 'none')
                    chk(lab + ' 金額の欄の名前', b['l'], 'その月に支払う金額' if k == 2 else ('賞金の額' if k == 4 else '1回に支払う金額'))
                    if need:
                        if k == 0:
                            f = '支払う金額×10.21%' if a <= 1000000 else '100万円を超える部分×20.42%＋102,100円'
                        elif k == 3:
                            f = '（支払う金額−5,000円×%d日）×10.21%%' % d
                        else:
                            f = '（支払う金額−%s円）×10.21%%' % c(KOJO[k])
                        chk(lab + ' 式', b['f'], f)
                        # 納期の特例:No.2505・あらまし(弁護士や司法書士などの報酬だけ。原稿料・外交員・ホステス・賞金・ボクサーは対象外)
                        e = {0: '種類によります', 1: '納期の特例を使えます', 2: '納期の特例は使えません', 3: '納期の特例は使えません',
                             4: '支払った月の翌月', 5: '支払った月の翌月'}[k]
                        chk(lab + ' 特例', b['e'], e)
                        chk(lab + ' 理由', b['why'], '所得税法204条に並んでいる報酬です。支払った月の翌月10日までに納めます')
                    else:
                        why = '所得税法204条に無い仕事' if k == 9 else ('法人への支払い' if who == 1 else '給与を払っていない個人の支払い')
                        chk(lab + ' 理由', b['why'], why + 'なので、源泉徴収はしません')
                        chk(lab + ' 式', (b['f'], b['e']), ('源泉徴収しないので0円', '納める税金はありません'))
                    near = min(TB, key=lambda s: (abs(s - a), TB.index(s)))
                    chk(lab + ' 黄色の行', b['hit'], [c(near)] if k == 0 else [])
    await pg.select_option('#kind', '0'); await pg.select_option('#who', '0'); await pg.select_option('#payer', '0')
    # 入力の上限で結果だけ頭打ちになっていないか(10億円を超える額)
    for a in (1000000001, 2000000000, 50000000000, 999999999999, 1000000000000):
        await pg.fill('#amt', str(a)); b = await box()
        chk('箱 大きい額 %d' % a, (b['t'], b['n']), (c(ref(0, a)) + '円', c(a - ref(0, a)) + '円'))
    await pg.fill('#amt', '100000')

    # 3 HTML に手で書いた早見表の全行(No.2795 の式)
    rows = await pg.eval_on_selector_all('#tb tr', "rs=>rs.map(r=>[r.getAttribute('data-s')].concat([...r.children].map(td=>td.textContent)))")
    chk('早見表の行', [int(r[0]) * 10000 for r in rows], TB)
    for r in rows:
        a = int(r[0]) * 10000; t = ref(0, a)
        chk('早見表 %d' % a, r[1:], [c(a), c(t), c(a - t)])

    # 4 種類ごとの式の表・納期の特例の表・消費税と交通費の表
    def flat(t):
        return ''.join(t.split())
    rate = [[flat(x) for x in r] for r in await pg.eval_on_selector_all(':is(#rate ~ .tw):not(#rate ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.innerText))")]
    chk('式の表', rate, [
        ['原稿料・講演料・デザイン料弁護士・税理士などの報酬出演料・契約金', '支払う金額×10.21%100万円を超える部分は20.42%'],
        ['司法書士・土地家屋調査士・海事代理士の報酬', '（1回の支払い−1万円）×10.21%'],
        ['外交員・集金人・検針人の報酬', '（その月の支払い−12万円）×10.21%'],
        ['ホステス・コンパニオンの報酬', '（1回の支払い−5,000円×計算期間の日数）×10.21%'],
        ['広告宣伝のための賞金', '（賞金−50万円）×10.21%'],
        ['プロボクサーの報酬', '（1回の支払い−5万円）×10.21%']])
    pay = [[flat(x) for x in r] for r in await pg.eval_on_selector_all(':is(#pay ~ .tw):not(#pay ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.innerText))")]
    chk('納期の特例の表', pay, [
        ['弁護士・税理士・司法書士などの報酬', '使えます（7月10日と翌年1月20日）'],
        ['原稿料・講演料', '使えません（翌月10日）'],
        ['外交員・集金人・検針人の報酬', '使えません（翌月10日）'],
        ['ホステス・コンパニオンの報酬', '使えません（翌月10日）']])

    # 5 本文の例と注の数字
    txt = flat(await pg.inner_text('main'))
    for label, want in [
        ('冒頭の率', '税率は10.21%で、1回の支払いが100万円を超える部分は20.42%です。'),
        ('冒頭の例', '10万円の原稿料なら、%s円を差し引いて%s円を払います。' % (c(ref(0, 100000)), c(100000 - ref(0, 100000)))),
        ('早見表の注', '100万円までは支払う金額×10.21%です。100万円を超えると、超えた部分×20.42%に102,100円を足します。1円未満は切り捨てます。'),
        ('令和9年の注', '令和9年1月からは、源泉徴収する税の名前が「所得税・防衛特別所得税・復興特別所得税」に変わります。合計の率は同じなので、10.21%と20.42%の計算は変わりません（国税庁No.2507）。'),
        ('司法書士の例', '司法書士に5万円を払うなら、1万円を引いた4万円に10.21%%を掛けて%s円です。' % c(ref(1, 50000))),
        ('外交員の例', '外交員に月20万円を払うなら、12万円を引いた8万円に10.21%%を掛けて%s円です。' % c(ref(2, 200000))),
        ('外交員の給与', '外交員に同じ月の給与も払うときは、12万円から給与の額を引いた残りを報酬から引きます。'),
        ('150万円の例', '150万円の原稿料なら、100万円を超える50万円に20.42%%を掛けて102,100円を足した%s円です。' % c(ref(0, 1500000))),
        ('納める期限', '差し引いた所得税は、支払った月の翌月10日までに納めます。'),
        ('納期の特例の条件', '給与を払う人数が常に10人未満の事業者は、税務署の承認を受けると半年分をまとめて納める「納期の特例」を使えます。'),
        ('手取りの例', '手取り10万円なら報酬は111,370円（1円未満は切り捨て）で、源泉徴収する額は11,370円です。'),
        ('納期の特例の範囲', '納期の特例を使えるのは、給与・退職金と弁護士・税理士・司法書士など一部の資格の人への報酬だけです。'),
        ('更新日', '更新日：2026年11月21日'),
        ('3号の機関の名前', '医療情報基盤・診療報酬審査支払機構（2026年9月までの社会保険診療報酬支払基金）が払う診療報酬'),
        ('懸賞の賞金', '懸賞応募作品の入選者への賞金（1回おおむね5万円以下）'),
        ('一覧 司法書士', '1回の支払いから1万円を引いて計算'),
        ('一覧 ボクサー', '1回の支払いから5万円を引いて計算'),
        ('一覧 外交員', 'その月の支払いから12万円を引いて計算'),
        ('一覧 ホステス', '5,000円×計算期間の日数を引いて計算'),
        ('一覧 賞金', '50万円を引いて計算'),
        ('消費税', '原則は、消費税を含めた金額に税率を掛けます。請求書などで報酬と消費税がはっきり分かれていれば、報酬の額だけに掛けてかまいません'),
        ('法令の日付', '令和8年4月1日現在の法令'),
    ]:
        chk('本文 ' + label, want in txt, True)

    # 6 一覧の要る・要らない(通達204-6・204-10・204-11・204-17・あらましの「類似するが該当しないもの」の欄)
    han = await pg.eval_on_selector_all('#hb tr:not(.grp)', "rs=>rs.map(r=>[r.children[0].childNodes[0].textContent,r.children[1].textContent])")
    hd = dict((a, b) for a, b in han)
    chk('一覧の行の数', len(han), 51)
    for name in ['手話通訳の報酬', '製本の料金', '試験問題の出題料・答案の採点料', '懸賞応募作品の選稿料・審査料', '字や絵の看板書き料',
                 '懸賞応募作品の入選者への賞金（1回おおむね5万円以下）', '行政書士の報酬', '登記・申請のための登録免許税や手数料の実費',
                 '自分で開いた公演の入場料など、不特定多数から受けるもの', '旅行など、金品と選べない形の賞', '上の報酬を法人に払う場合',
                 '給与を払っていない個人が、上の報酬を払う場合', '交通費・宿泊費を、交通機関やホテルに直接払った分']:
        chk('一覧 不要 ' + name, hd.get(name), '不要')
    for name in ['デザインと施工をまとめて請け負った代金', '損害保険の鑑定人（火災・自動車など）の報酬', '雇用契約などで、給与に当たるもの']:
        chk('一覧 場合による ' + name, hd.get(name), '場合による')
    chk('一覧 残りは要', sorted(set(v for k, v in han)), ['不要', '場合による', '要'])
    chk('一覧 要の数', sum(1 for k, v in han if v == '要'), len(han) - 13 - 3)

    # 7 ファイルの中身:JS が書き換える前の値・余った閉じタグ
    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'gensen-hoshu', 'index.html'), encoding='utf-8').read()
    chk('元の値 金額', 'id="amt" inputmode="numeric" min="0" max="1000000000000" step="1000" value="100000"' in raw, True)
    # 計算の箱に直に書いた既定の結果(JS が動く前の文)。既定は個人・給与を払っている側・原稿料など・10万円
    d0 = ref(0, 100000)
    chk('元の結果 額', '<b id="o-t">%s<i>円</i></b><em id="o-f">支払う金額×10.21%%</em>' % c(d0) in raw, True)
    chk('元の結果 払う額', '<b id="o-n">%s<i>円</i></b>' % c(100000 - d0) in raw, True)
    chk('元の結果 期限', '<b id="o-d" style="font-size:16px;line-height:1.6">翌月10日</b><em id="o-e">種類によります</em>' in raw, True)
    chk('元の結果 要否', '<b id="o-need">源泉徴収が必要です</b><span id="o-why">所得税法204条に並んでいる報酬です。支払った月の翌月10日までに納めます</span>' in raw, True)
    chk('元の値 日数', 'id="days" inputmode="numeric" min="1" max="366" step="1" value="30"' in raw, True)
    bodyhtml = re.sub(r'<script.*?</script>|<style.*?</style>', '', raw, flags=re.S)
    chk('span の開きと閉じの数', len(re.findall(r'<span\b', bodyhtml)), len(re.findall(r'</span>', bodyhtml)))
    return n, bad
run('gensen-hoshu', body)
