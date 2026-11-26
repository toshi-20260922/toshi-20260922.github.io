# /kokuho-keisan/ 国民健康保険料の計算(令和8年度・22の地域)。
# 原本(2026-11-20 に開いて確かめたもの):
#   東京都中央区「国民健康保険料の計算方法」(特別区の料率 基礎7.51%・47,600円・67万円/支援2.8%・17,600円・26万円/介護2.43%・17,800円・17万円/
#     子ども0.27%・1,873円(18歳以上・73円の上乗せ込み)・3万円。所得割の基礎は総所得金額等−住民税の基礎控除43万円(2,400万円超は29万・15万・0円))
#     https://www.city.chuo.lg.jp/a0024/kurashi/hokennenkin/kokuho/kokuhonitsuite/noufu/hokenryo.html
#   世田谷区「保険料の軽減」(7割 43万円+10万円×(給与所得者等の数−1)・5割 +31万円×被保険者数・2割 +57万円×被保険者数)
#     https://www.city.setagaya.lg.jp/02060/300.html
#   名古屋市「令和8年度の軽減の基準」(同じ式。前年度は5割30.5万円・2割56万円) https://www.city.nagoya.jp/kurashi/hoken/1011736/1011793/1011807/1011809.html
#   名古屋市「令和8年度分の国民健康保険料」(8.83%・50,591円/2.58%・15,784円/2.34%・16,120円/0.26%・1,771円+92円・限度額67・26・17・3万円。
#     所得基準の減額がある世帯は1人2,000円を均等割から引く) https://www.city.nagoya.jp/kurashi/hoken/1011736/1011793/1011794/1011799.html
#   名古屋市「令和8年度名古屋市国民健康保険料計算例」(区分ごとに10円未満切り捨て。軽減の減額は1人ごとに出して人数を掛ける:例5 2割・2人 医療の減額20,238円=10,119円×2)
#     https://www.city.nagoya.jp/_res/projects/default_project/_page_/001/011/799/r8_keisanrei.pdf
#   大阪府「令和8年度の府内統一保険料率」(9.50%・34,990円・33,908円・66万円/3.06%・11,191円・10,845円・26万円/2.60%・18,682円・17万円/0.28%・1,841円・3万円)
#     https://www.pref.osaka.lg.jp/o100080/kokuho/iryouseido/hokenryouritsu/hokenryouritsu2.html
#   横浜市「令和8年度保険料の料率等について」(8.33%・40,870/2.62%・13,380/2.84%・16,200/0.34%・1,770(1,690+80))
#     https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/r7hokennryouritu.html
#   札幌市北区「国民健康保険料の計算」(8.61%・20,550・32,540/2.56%・6,330・10,010/2.33%・6,020・7,550/0.29%・1,100・1,000)
#     https://www.city.sapporo.jp/kitaku/tetsuzuki/hoken_nenkin/kokuho_keisan.html
#   福岡市「国民健康保険料の計算方法」(5.58%・19,807・18,664/3.14%・10,441・9,838/2.61%・10,160・7,751/0.28%・1,039・911)
#     https://www.city.fukuoka.lg.jp/hofuku/kokuho/hp/seido/06-02.html
#   さいたま市「国民健康保険税の税率」(7.64%・43,300/2.73%・14,900/2.37%・16,100/0.26%・1,700。100円未満は区分ごとに切り捨て)
#     https://www.city.saitama.lg.jp/001/153/002/004/p010020.html
#   相模原市「令和8年度 国民健康保険税の税率等について」(6.75%・29,000・18,000/2.78%・11,500・7,000/2.32%・12,000・6,000/0.28%・1,300+60・800)
#     https://www.city.sagamihara.kanagawa.jp/kurashi/1026448/kokuho/1007820/1007822.html
#   相模原市「国民健康保険税の税額計算」(計算例は区分ごとに100円未満切り捨て) https://www.city.sagamihara.kanagawa.jp/kurashi/1026448/kokuho/1026464/noufu/1007892.html
#   神戸市「国民健康保険料の額」(7.38%・33,700・21,800/2.97%・13,510・8,740/2.78%・13,970・6,880/0.26%・1,330・830)
#     https://www.city.kobe.lg.jp/a52670/kurashi/support/insurance/gaku.html
#   京都市「令和8年度の保険料の計算方法について」(7.94%・30,080・17,930/2.66%・10,360・6,180/2.51%・11,090・5,370/0.28%・1,170(1,110+60)・660)
#     https://www.city.kyoto.lg.jp/hokenfukushi/page/0000351039.html
# 上の原本で確かめていない地域(仙台・千葉・川崎・新潟・浜松・岡山・広島・北九州・熊本・目黒・中野・江戸川)の料率は tools/regions.py(2026/11/16 確認)の値。
# 給与所得は令和7年分の給与所得控除(65万円・190万円以下)と所得税法の別表第五(660万円未満は4,000円ごと)。
# 照らすもの:22の地域×家族0〜3人×年齢×軽減の境目・限度額の境目の前後の結果の箱(年額・月額・軽減・内訳)・年収別の表の全行・料率の表・
#   市区町村ごとの保険料の表(手で書いた22行)・よくある質問の数字・冒頭の上限・軽減の表・料率を入れる欄・JS が書き換える前の文
#   11-20 16時の回で開き直したもの: 東京都保健医療局「特別区の国民健康保険料一覧表（令和8年度）」(20区共通 7.51%・47,600/2.80%・17,600/2.43%・17,800/0.27%・1,800+73。
#     目黒 介護2.35%。中野 8.03%・47,100/2.94%・17,400/2.53%・17,700。江戸川 7.83%・48,900/2.84%・17,400/2.45%・17,400/子ども1,780+90)
#     https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/tokubetuku202605-pdf
#   大阪府(題名は「令和8年度大阪府市町村標準保険料率等の算定結果について」。医療分の限度額66万円)・横浜市・名古屋市(基礎控除は2,400万円超で29万・15万・0円と明記)・神戸市・
#   広島市「国民健康保険料の計算方法」(8.18%・31,228・30,403/2.64%・10,342・10,069/2.52%・10,443・7,860/0.27%・1,072+56・1,044) https://www.city.hiroshima.lg.jp/living/hoken-nenkin/1021143/1025566/1003464.html
#   横浜市「保険料に関する制度改正について」(限度額 医療66→67万円・子ども3万円新設。軽減 5割30.5→31万円・2割56→57万円) https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/04seidokaisei.html
#   横浜市「保険料について」(給与所得者等=給与の収入金額が55万円を超える方など) https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/04hokenryounituite.html
#   川崎市「国保のしおり(令和8年度)」で子ども分の均等割 1,742円(1,665+77)だけ確かめた。川崎市のほかの料率は開けず未確認。
# 申し送り(11-20 16時): 年収別の表に 1,200・1,500・2,000万円の行が足されていた(突き合わせの古さ。額は合っていた)。
#   ページの誤りは2つ直した: 基礎控除を43万円で固定(一覧にない市区町村で低い料率を入れ所得2,400万円超のとき差が出る)・出典の神戸市の題名。
#   残り: 名古屋市の子ども分は 1,771円と18歳以上の92円を別々に軽減する(計算例)。ページと regions.py は 1,863円をまとめて軽減するので、2割軽減のとき1人1円多く、
#   10円未満切り捨てのあとで10円ずれる場合がある(川崎市の5割も同じ形の見込み。川崎市の端数処理は未確認)。regions.py の形を変えないと直せない。
# 11-21 4時の回で開き直したもの(料率は tools/regions.py と全部同じ):
#   熊本市「国民健康保険　保険料について」(6.34%・28,400・18,100/2.98%・13,300・8,500/2.94%・20,300/0.25%・1,600+18歳以上100。限度額67・26・17・3万円) https://www.city.kumamoto.jp/kiji003426/index.html
#   北九州市「国民健康保険料の計算方法」(8.31%・23,200・26,400/3.40%・9,720・11,060/2.90%・9,550・8,220/0.28%・880+50・1,000) https://www.city.kitakyushu.lg.jp/contents/924_10079.html
#   福岡市「国民健康保険料の計算方法」(5.58%・19,807・18,664/3.14%・10,441・9,838/2.61%・10,160・7,751/0.28%・1,039(72円込み)・911)
#   岡山市「令和8年度国民健康保険料率のお知らせ」(8.15%・28,320・20,880/2.95%・10,320・6,960/2.60%・10,920・5,280/0.29%・1,200(60円込み)・720) https://www.city.okayama.jp/kurashi/0000011518.html
#   浜松市「保険料について」(7.20%・25,000・22,000/2.35%・11,000・8,000/1.90%・14,500/0.33%・1,800+200) https://www.city.hamamatsu.shizuoka.jp/kokuho/kokuho_nenkin/kokuho/hokenryou.html
#   新潟市「令和8年度の国民健康保険料率と軽減判定所得について」(7.4%・14,700・19,200/3.1%・7,200・9,000/2.5%・14,100/0.27%・1,600)
#   千葉市「令和8年度国民健康保険料率の決定」(7.21%・23,280・26,640/2.85%・8,880・10,320/2.57%・16,560/0.31%・1,800(120円込み))
#   仙台市「保険料はいくら（令和8年度）」(7.96%・27,850・26,700/3.00%・10,410・9,980/2.44%・9,440・7,070/0.27%・940+70・900)
#   川崎市「令和8年度の国民健康保険料について」(8.26%・43,261/2.89%・15,306/2.67%・15,828/0.32%・1,665+77)
#   厚生労働省 保発0115第9号(令和8年1月15日。基礎賦課額の限度額1万円引き上げ・子ども分3万円・軽減 5割31万円・2割57万円・令和8年4月1日施行)
#     https://www.mhlw.go.jp/hourei/doc/tsuchi/T260121S0030.pdf
#   厚生労働省 第220回医療保険部会(令和8年11月11日)の資料: 令和8年度は67・26・17・3万円(計113万円)。令和9年度は基礎69万円・支援27万円にする案(未決定)
#     https://www.mhlw.go.jp/content/12401000/001768124.pdf
# 申し送り(11-21): 計算の箱に直に書いた既定の結果(o-y・o-m・o-br)が「0円」のままだった(形11・16)。313,587円・26,132円・内訳に直し、下で照らす。
#   出典の文字を着いたページの題名に合わせた(仙台・浜松・岡山・熊本)。tools/regions.py の src は古い文字のまま。
#   給与所得者等の給与収入の基準: 名古屋・横浜・川崎・岡山・仙台・新潟は「55万円超」、熊本市は「65万円超」と書く。政令の条文は開けていない(ページは55万円のまま)。
# 最後に原本を確かめた日:2026-11-21
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from _lib import run
import rates

CAP = rates.kokuho_caps()
# (表示名, [医療, 支援, 介護, 子ども] の (所得割 %の100倍, 均等割, 平等割), 端数の単位, 名古屋の独自減額, 医療分の限度額)
D = rates.kokuho_d(False)

def fl(x):
    x = F(x)
    return x.numerator // x.denominator

def kyuyo(x):
    """令和7年分の給与所得(所得税法28条・別表第五)。"""
    return rates.kyuyo_r7(x)

def keigen(g, n):
    """世帯の総所得金額等 g・被保険者数 n(給与所得者等は1人)。"""
    return rates.keigen(g, n)

def hoken(d, g, me40, fam, fam40):
    name, p, r, nag, cap0 = d
    n = 1 + fam
    kiso = rates.kiso_jumin(g)
    base = max(0, g - kiso)
    red = keigen(g, n)
    caps = [cap0] + CAP[1:]
    out = []
    for i, (rate, kin, byo) in enumerate(p):
        cnt = (me40 + fam40) if i == 2 else n
        if cnt == 0:
            out.append(0); continue
        b = (base if me40 else 0) if i == 2 else base
        v = fl(F(b * rate, 10000))
        v += cnt * fl(F(kin * (10 - red), 10))        # 軽減は1人ごと
        v += fl(F(byo * (10 - red), 10))
        if nag and i == 0 and red:
            v = max(0, v - 2000 * cnt)
        v = v // r * r
        out.append(min(caps[i], v))
    return sum(out), out, red

def c(v):
    return '{:,}'.format(v)

RD = {7: '7割', 5: '5割', 2: '2割', 0: 'なし'}
LB = ['医療分', '後期高齢者支援金分', '介護分（40〜64歳）', '子ども・子育て支援金分']

JS_SET = """cs=>{
 const out=[];const reg=document.getElementById('reg'),inc=document.getElementById('inc'),fam=document.getElementById('fam'),famo=document.getElementById('famo');
 for(const k of cs){
  if(reg.value!==String(k[0])){reg.value=String(k[0]);reg.dispatchEvent(new Event('change'));}
  document.querySelector('#s-k button[data-v="'+k[1]+'"]').click();
  document.querySelector('#s-age button[data-v="'+k[3]+'"]').click();
  fam.value=String(k[4]);fam.dispatchEvent(new Event('change'));
  famo.value=String(k[5]);famo.dispatchEvent(new Event('change'));
  inc.value=String(k[2]);inc.dispatchEvent(new Event('input'));
  out.push([document.getElementById('o-y').innerText,document.getElementById('o-m').innerText,document.getElementById('o-r').innerText,document.getElementById('o-br').innerText,document.getElementById('o-vd').innerText,document.getElementById('o-vds').innerText]);
 }
 return out;}"""

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1
            if bad < 40: print('NG', label, repr(got), repr(want))

    raw = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'site', 'kokuho-keisan', 'index.html'), encoding='utf-8').read()

    # 原本どうしの照らし合わせ(名古屋の計算例・相模原の計算例の考え方)
    ng = D[13]
    chk('名古屋 計算例1 20歳単身 給与所得20万円', hoken(ng, 200000, 0, 0, 0)[0], 18450)
    chk('名古屋 計算例3 51歳単身 給与所得244万円', hoken(ng, 2440000, 1, 0, 0)[0], 365940)
    chk('名古屋 計算例3 内訳', hoken(ng, 2440000, 1, 0, 0)[1], [228070, 67640, 63150, 7080])
    chk('名古屋 計算例10 38歳単身 基礎控除後57万円(2割)', hoken(ng, 1000000, 0, 0, 0)[1], [88800, 27330, 0, 2970])
    chk('横浜市 令和8年度の軽減の基準(5割31万円・2割57万円) 2人', [keigen(430000 + 620000, 2), keigen(430000 + 620001, 2), keigen(430000 + 1140000, 2), keigen(430000 + 1140001, 2)], [5, 2, 2, 0])
    chk('大阪府 医療分の限度額', D[15][4], 660000)
    chk('上限の合計 40歳未満', sum(CAP) - CAP[2], 960000)
    chk('上限の合計 40〜64歳', sum(CAP), 1130000)

    # 料率の表(JS)と見出し
    for i, d in enumerate(D):
        await pg.select_option('#reg', str(i))
        rows = await pg.eval_on_selector_all('#rtb tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
        caps = [d[4]] + CAP[1:]
        want = [[LB[j], '%d.%02d%%' % (q[0] // 100, q[0] % 100), c(q[1]), c(q[2]), c(caps[j])] for j, q in enumerate(d[1])]
        chk('料率の表 ' + d[0], rows, want)
        chk('料率の表の題 ' + d[0], await pg.inner_text('#r-cap'), d[0] + '・令和8年度')
        chk('計算の地域の文 ' + d[0], await pg.inner_text('#o-reg'), d[0] + 'の令和8年度の料率で計算しています')

    # 結果の箱。所得(事業など)は軽減の境目と限度額の境目の前後、給与は控除の境目の前後
    cases = []
    for i, d in enumerate(D):
        for fam in range(4):
            nn = 1 + fam
            gs = {0, 1, 200000, 429999, 430000, 430001, 430000 + 310000 * nn - 1, 430000 + 310000 * nn, 430000 + 310000 * nn + 1,
                  430000 + 570000 * nn - 1, 430000 + 570000 * nn, 430000 + 570000 * nn + 1, 2000000, 4567891, 9000000, 24000000, 24000001, 24500001, 25000001, 30000000}
            for famo in sorted({0, 1 if fam else 0, fam}):
                for age in (0, 1):
                    # 限度額のちょうど前後(所得割+均等割+平等割が限度額に届く所得)
                    for j in range(4):
                        cnt = (age + famo) if j == 2 else nn
                        if cnt == 0 or (j == 2 and not age): continue
                        rate, kin, byo = d[1][j]
                        cap = ([d[4]] + CAP[1:])[j]
                        need = cap - (kin * cnt + byo)
                        b0 = -(-need * 10000 // rate)            # 所得割がこの額に届く基礎の所得
                        for dg in (-d[2] * 10000 // rate - 2, -1, 0, 1):
                            gs.add(max(0, b0 + 430000 + dg))
                    for g in sorted(gs):
                        cases.append((i, 1, g, age, fam, famo))
                    for a in (0, 650999, 651000, 1000000, 1899999, 1900000, 1903999, 1904000, 3599999, 3600000, 4000000, 6599999, 6600000, 8499999, 8500000, 12000000):
                        cases.append((i, 0, a, age, fam, famo))
    for s in range(0, len(cases), 400):
        part = cases[s:s + 400]
        res = await pg.evaluate(JS_SET, [list(k) for k in part])
        for k, got in zip(part, res):
            i, kind, a, age, fam, famo = k
            g = a if kind else kyuyo(a)
            t, ps, red = hoken(D[i], g, age, fam, famo)
            lab = '%s %s%d 年齢%d 家族%d(40〜64歳%d)' % (D[i][0], '所得' if kind else '年収', a, age, fam, famo)
            chk('箱 年額 ' + lab, got[0], c(t) + '円')
            chk('箱 月額 ' + lab, got[1], c(t // 12) + '円')
            chk('箱 軽減 ' + lab, got[2], RD[red])
            chk('箱 結論 ' + lab, got[4], '1年の国民健康保険料は%s円です' % c(t))
            chk('箱 結論の地域 ' + lab, got[5], D[i][0] + 'の令和8年度の料率で計算した額です')
            chk('箱 内訳 ' + lab, got[3], '内訳は、医療分%s円・後期高齢者支援金分%s円・介護分%s円・子ども・子育て支援金分%s円です' % tuple(c(x) for x in ps))

    # 年収別の表(JS)の全行。家族0〜3人
    # 11-20 にページの表へ 1,200・1,500・2,000万円の行が足された(上限に届く行)。行の並びはページの今の形に合わせ、額は自分の計算で出す
    ROWS = [100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200, 1500, 2000]
    chk('年収別の表の見出し', await pg.eval_on_selector_all(':is(#list ~ .tw):not(#list ~ .tw ~ .tw) thead th', "ts=>ts.map(t=>t.innerText.replace(/\\s+/g,''))"),
        ['前の年の年収', '40歳未満（年・円）', '40〜64歳（年・円）'])
    for i, d in enumerate(D):
        await pg.select_option('#reg', str(i))
        await pg.click('#s-k button[data-v="0"]')
        for fam in range(4):
            await pg.select_option('#fam', str(fam))
            rows = await pg.eval_on_selector_all('#tb tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
            want = [[c(r) + '万円', c(hoken(d, kyuyo(r * 10000), 0, fam, 0)[0]), c(hoken(d, kyuyo(r * 10000), 1, fam, fam)[0])] for r in ROWS]
            chk('年収別の表 %s 家族%d' % (d[0], fam), rows, want)
            # 「年収が高い行は上限の額で止まります」: 2,000万円の行は4つの区分とも限度額
            capsum = d[4] + sum(CAP[1:])
            chk('年収別の表 2,000万円は上限 %s 家族%d' % (d[0], fam), want[-1][1:], [c(capsum - CAP[2]), c(capsum)])
            for r in (1200, 1500, 2000):      # 足された行は区分ごとの内訳も限度額と比べる
                ps = hoken(d, kyuyo(r * 10000), 1, fam, fam)[1]
                chk('足された行の内訳は限度額以下 %s %d 家族%d' % (d[0], r, fam), all(x <= y for x, y in zip(ps, [d[4]] + CAP[1:])), True)
            chk('年収別の表の題 %s 家族%d' % (d[0], fam), await pg.inner_text('#t-cap'), d[0] + '・令和8年度・' + ('家族%d人' % fam if fam else '家族なし'))
    await pg.select_option('#fam', '0')

    # 黄色の行(入れた年収を超えない中でいちばん近い行)
    await pg.select_option('#reg', '0')
    for a, want in [(4000000, ['400']), (4490000, ['400']), (4500000, ['450']), (999999, []), (1000000, ['100']), (30000000, ['2,000']), (11999999, ['1,000']), (12000000, ['1,200']), (19999999, ['1,500']), (20000000, ['2,000'])]:
        await pg.fill('#inc', str(a))
        chk('黄色の行 %d' % a, await pg.eval_on_selector_all('#tb tr.hit', "rs=>rs.map(r=>r.children[0].textContent)"), [w + '万円' for w in want])
    chk('高い行の注記', '年収が高い行は上限の額で止まります。' in raw, True)
    chk('黄色の行の文', '入力した年収を超えない中でいちばん近い行が黄色になります。' in raw, True)

    # 一覧にない市区町村(料率を入れる)。選んでいた地域の料率が入り、端数は1円・独自減額なしで計算する
    await pg.select_option('#reg', '15')
    await pg.select_option('#reg', 'x')
    vals = [await pg.input_value('#c%d%d' % (j, k)) for j in range(4) for k in range(3)]
    chk('料率を入れる欄 大阪府の値', vals, [x for q in D[15][1] for x in ('%d.%02d' % (q[0] // 100, q[0] % 100), c(q[1]), c(q[2]))])
    my = [(812, 31234, 12345), (255, 9876, 1111), (199, 12000, 0), (31, 1555, 99)]
    for j in range(4):
        await pg.fill('#c%d0' % j, '%d.%02d' % (my[j][0] // 100, my[j][0] % 100))
        await pg.fill('#c%d1' % j, str(my[j][1]))
        await pg.fill('#c%d2' % j, str(my[j][2]))
    dx = ('入れた料率', my, 1, 0, 670000)
    for kind, a, age, fam, famo in [(1, 0, 0, 0, 0), (1, 740000, 1, 1, 1), (1, 740001, 0, 0, 0), (0, 4000000, 1, 2, 1), (0, 12000000, 1, 3, 3), (1, 1340000, 0, 1, 0),
                                      # 基礎控除は合計所得2,400万円超で29万・15万・0円(低い料率だと限度額に届かず差が出る。11-20 にページを直した)
                                      (1, 24000000, 1, 0, 0), (1, 24000001, 1, 0, 0), (1, 24500000, 1, 1, 1), (1, 24500001, 0, 0, 0), (1, 25000000, 1, 0, 0), (1, 25000001, 1, 2, 1), (1, 30000000, 0, 0, 0)]:
        res = await pg.evaluate(JS_SET.replace("if(reg.value!==String(k[0]))", "if(false)"), [['x', kind, a, age, fam, famo]])
        g = a if kind else kyuyo(a)
        t, ps, red = hoken(dx, g, age, fam, famo)
        chk('入れた料率 %d %d' % (kind, a), res[0][:3], [c(t) + '円', c(t // 12) + '円', RD[red]])
        chk('入れた料率 内訳 %d %d' % (kind, a), res[0][3], '内訳は、医療分%s円・後期高齢者支援金分%s円・介護分%s円・子ども・子育て支援金分%s円です' % tuple(c(x) for x in ps))
        chk('入れた料率 結論 %d %d' % (kind, a), res[0][4:], ['1年の国民健康保険料は%s円です' % c(t), '入力した料率で計算した額です'])
    chk('入れた料率の文', await pg.inner_text('#o-reg'), '入力した料率で計算しています')
    # 低い料率(限度額に届かない)で、基礎控除が 43万・29万・15万・0円と変わる所を見る
    lo_my = [(200, 10000, 0), (50, 3000, 0), (30, 3000, 0), (10, 500, 0)]
    for j in range(4):
        await pg.fill('#c%d0' % j, '%d.%02d' % (lo_my[j][0] // 100, lo_my[j][0] % 100))
        await pg.fill('#c%d1' % j, str(lo_my[j][1]))
        await pg.fill('#c%d2' % j, str(lo_my[j][2]))
    dlo = ('入れた料率', lo_my, 1, 0, 670000)
    chk('低い料率は限度額に届かない(基礎控除の差が見える)', hoken(dlo, 24000001, 1, 0, 0)[1][0] - hoken(dlo, 24000000, 1, 0, 0)[1][0], 2800)
    for a, age, fam, famo in [(24000000, 1, 0, 0), (24000001, 1, 0, 0), (24500000, 1, 1, 1), (24500001, 0, 0, 0), (25000000, 1, 0, 0), (25000001, 1, 2, 1), (30000000, 0, 0, 0)]:
        res = await pg.evaluate(JS_SET.replace("if(reg.value!==String(k[0]))", "if(false)"), [['x', 1, a, age, fam, famo]])
        t, ps, red = hoken(dlo, a, age, fam, famo)
        chk('低い料率 基礎控除の段階 所得%d' % a, res[0][:4], [c(t) + '円', c(t // 12) + '円', RD[red], '内訳は、医療分%s円・後期高齢者支援金分%s円・介護分%s円・子ども・子育て支援金分%s円です' % tuple(c(x) for x in ps)])

    # 市区町村ごとの保険料の表(手で書いた22行。給与400万円・1人)
    rows = await pg.eval_on_selector_all('#hikaku ~ .tw', "ws=>[...ws[0].querySelectorAll('tbody tr')].map(r=>[...r.children].map(td=>td.innerText))")
    g4 = kyuyo(4000000)
    want = [[d[0], c(hoken(d, g4, 0, 0, 0)[0]), c(hoken(d, g4, 1, 0, 0)[0])] for d in D]
    chk('比べる表の行の数', len(rows), 22)
    for r, w in zip(rows, want):
        chk('比べる表 ' + w[0], r, w)
    lo = min(D, key=lambda d: hoken(d, g4, 0, 0, 0)[0]); hi = max(D, key=lambda d: hoken(d, g4, 0, 0, 0)[0])
    flat = ''.join((await pg.inner_text('main')).split())
    for label, want in [
        ('QA 最も安い・高い', 'この早見表の22の地域では年%s円（%s）から年%s円（大阪府内）まで開きがあります。' % (c(hoken(lo, g4, 0, 0, 0)[0]), lo[0], c(hoken(hi, g4, 0, 0, 0)[0]))),
        ('冒頭 43万円', '前の年の所得から43万円を引いた額にかかる所得割'),
        ('冒頭 上限', '上限は多くの市区町村で1年%d万円（40〜64歳の人は%d万円）です。' % ((sum(CAP) - CAP[2]) // 10000, sum(CAP) // 10000)),
        ('軽減 7割', '7割43万円以下'),
        ('軽減 5割', '5割43万円＋31万円×加入者の数以下'),
        ('軽減 2割', '2割43万円＋57万円×加入者の数以下'),
        ('軽減 10万円', '1人増えるごとに基準に10万円ずつ足されます。'),
        ('軽減 55万円', '給与の収入が55万円を超える人'),
        ('会社都合 30%', '給与所得を30%として計算する'),
        ('QA 所得の年', '令和8年度（2026年4月から2027年3月）の保険料は、2025年の所得で計算します。'),
    ]:
        chk('本文 ' + label, want in flat, True)
    chk('最も高いのは大阪府', hi[0], '大阪市・堺市')
    desc = '政令指定都市19市と東京23区の料率を登録しています。'
    chk('description と og', raw.count(desc), 2)
    chk('政令指定都市の数(静岡市を除く20市のうち)', len([d for d in D if d[0].endswith('市') or d[0] == '大阪市・堺市']) + 1, 19)   # 大阪市・堺市は2市

    # JS が書き換える前の元の文(既定は東京23区・給与400万円・40歳未満・家族なし)
    for label, want in [
        ('既定の年収', 'id="inc" inputmode="numeric" min="0" max="30000000" step="10000" value="4000000"'),
        ('表の題', '<p class="cap" id="t-cap">東京23区・令和8年度・家族なし</p>'),
        ('料率の題', '<p class="cap" id="r-cap">東京23区・令和8年度</p>'),
        ('地域の文', '<li id="o-reg">東京23区の令和8年度の料率で計算しています</li>'),
    ]:
        chk('元の文 ' + label, want in raw, True)
    chk('元の文 結論(東京23区・給与400万円・40歳未満・1人)', '<b id="o-vd">1年の国民健康保険料は%s円です</b><span id="o-vds">東京23区の令和8年度の料率で計算した額です</span>' % c(hoken(D[0], kyuyo(4000000), 0, 0, 0)[0]) in raw, True)
    # 計算の箱に直に書いた既定の結果(JS が動く前の HTML。東京23区・給与400万円・40歳未満・1人)
    t0, p0, _ = hoken(D[0], kyuyo(4000000), 0, 0, 0)
    chk('元の文 年額', '<b id="o-y">%s<i>円</i></b>' % c(t0) in raw, True)
    chk('元の文 月額', '<b id="o-m">%s<i>円</i></b>' % c(t0 // 12) in raw, True)
    chk('元の文 軽減', '<b id="o-r" style="font-size:18px">なし</b>' in raw, True)
    chk('元の文 内訳', '<li id="o-br">内訳は、医療分%s円・後期高齢者支援金分%s円・介護分%s円・子ども・子育て支援金分%s円です</li>' % tuple(c(x) for x in p0) in raw, True)
    for nm in ['仙台市「保険料はいくら（令和8年度）」', '浜松市「保険料について」', '岡山市「令和8年度国民健康保険料率のお知らせ」', '熊本市「国民健康保険　保険料について」']:
        chk('出典の題名 ' + nm, raw.count(nm), 1)
    chk('出典 神戸市の題名', '神戸市「国民健康保険料の額」' in raw, True)
    chk('出典 大阪府の題名', '大阪府「令和8年度大阪府市町村標準保険料率等の算定結果について」' in raw, True)
    chk('軽減の文は「以下」(表と同じ条件)', '世帯の所得が基準以下だと、均等割と平等割が7割・5割・2割下がります。' in raw, True)
    chk('span の開きと閉じの数', raw.count('<span'), raw.count('</span>'))
    return n, bad

run('kokuho-keisan', body)
