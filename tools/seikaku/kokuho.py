# /kokuho/ 国民健康保険と任意継続の比較(令和8年度・22の地域×47都道府県)。
# 原本(2026-11-20 に開いて確かめたもの):
#   全国健康保険協会「令和8年度の協会けんぽの保険料率は3月分（4月納付分）から改定されます」(47都道府県の料率・介護1.62%・
#     子ども・子育て支援金率0.23%・任意継続は令和8年4月分から) https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/rate_prefectures/r08
#   全国健康保険協会「【健康保険】令和8年度の任意継続被保険者の標準報酬月額の上限について」(32万円。令和7年9月30日の平均318,100円)
#     https://www.kyoukaikenpo.or.jp/news/r07_dec/1259.html
#   全国健康保険協会「協会けんぽの子ども・子育て支援金率について」(任意継続被保険者は令和8年4月分から0.23%)
#     https://www.kyoukaikenpo.or.jp/about/business/insurance_rate/003/index.html
#   全国健康保険協会 任意継続被保険者の保険料額表(令和8年4月分から)東京支部・京都支部
#     (保険料=標準報酬月額×(健康保険料率+支援金率0.23%(+介護1.62%))を合わせて掛け、1円未満は切り捨て。
#      東京 126,000円→12,700円(12,700.8)・142,000円→14,313円(14,313.6)/京都 126,000円→12,751円(12,751.2)・58,000円→5,869円(5,869.6)。
#      等級は58,000円(63,000円未満)から320,000円(310,000円以上)までの23等級)
#     https://www.kyoukaikenpo.or.jp/~/media/Files/shared/hokenryouritu/r8/ninkei/13tokyo.pdf
#     https://www.kyoukaikenpo.or.jp/~/media/Files/shared/hokenryouritu/r8/ninkei/26kyoto.pdf
#   全国健康保険協会 よくあるご質問「保険料について」(退職時の標準報酬月額×住んでいる都道府県の料率・上限32万円・全額自己負担)
#     https://www.kyoukaikenpo.or.jp/faq/voluntary_continuation/005/index.html
#   東京都中央区「国民健康保険の保険料」(特別区 7.51%・47,600円・67万円/2.8%・17,600円・26万円/2.43%・17,800円・17万円/0.27%・1,873円・3万円。
#     所得割の基礎=総所得金額等−住民税の基礎控除(2,400万円以下43万円・2,450万円以下29万円・2,500万円以下15万円・超0円))
#     https://www.city.chuo.lg.jp/a0024/kurashi/hokennenkin/kokuho/kokuhonitsuite/noufu/hokenryo.html
#   東京都保健医療局「令和8年度 特別区国民健康保険料一覧表」(目黒区 介護2.35%/中野区 8.03%・47,100円・2.94%・17,400円・2.53%・17,700円/
#     江戸川区 7.83%・48,900円・2.84%・17,400円・2.45%・17,400円・子ども1,780円+90円) https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/tokubetuku202605-pdf
#   大阪府「令和8年度大阪府市町村標準保険料率等の算定結果について」(9.50%・34,990円・33,908円・66万円/3.06%・11,191円・10,845円・26万円/
#     2.60%・18,682円・17万円/0.28%・1,841円・3万円) https://www.pref.osaka.lg.jp/o100080/kokuho/iryouseido/hokenryouritsu/hokenryouritsu2.html
#   横浜市「令和８年度保険料の料率等について」(8.33%・40,870円/2.62%・13,380円/2.84%・16,200円/0.34%・1,770円・限度額67・26・17・3万円)
#     https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/r7hokennryouritu.html
#   横浜市「保険料について」(軽減の基準 7割43万円・5割43万円+31万円×被保険者数・2割43万円+57万円×被保険者数・+10万円×(給与所得者等の数−1))
#     https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/04hokenryounituite.html
#   厚生労働省「国民健康保険の保険料・保険税について」(非自発的失業者=特定受給資格者・特定理由離職者は前年の給与所得を30/100として算定)
#     https://www.mhlw.go.jp/stf/newpage_21517.html
# 上の原本で開いていない地域の国民健康保険の料率は、tools/seikaku/kokuho-keisan.py の頭に書いた原本(同じ日に別の係が開いたもの)と tools/regions.py の値。
# 給与所得は令和7年分の給与所得控除(65万円・190万円以下)と所得税法の別表第五(660万円未満は4,000円ごと)。
# 照らすもの:22の地域×年齢×辞めた理由×家族0〜3人×年収(等級の境目・軽減の境目・上限の前後)の結果の箱と結論の文・
#   早見表(JS)の全行と黄色の行・料率の表・任意継続のほうが安くなる年収の表(手で書いた22行×2)・協会けんぽの料率の表(手で書いた47行)・
#   都道府県の選択肢47・市区町村を選ぶと都道府県が切り替わること・47都道府県×23等級の任意継続・料率を入れる欄・よくある質問と本文の数字・
#   JS が書き換える前の文・tools/regions.py の PREF と REG
# 2026-11-21 に開き直した原本:協会けんぽの上の3ページ(上限32万円・47都道府県の料率・介護1.62%・支援金0.23%・任意継続は4月分から)と
#   よくあるご質問「保険料について」・「任意継続」(20日以内・2年間・資格喪失申出書)・任意継続の保険料額表(東京支部。全23等級の2列)。
#   国民健康保険は22の地域の全部(東京都保健医療局の一覧表・札幌・仙台・さいたま・千葉・横浜・川崎・相模原・新潟・浜松・名古屋・京都・大阪府・
#   神戸・岡山・広島・北九州・福岡・熊本)の所得割・均等割・平等割・限度額。軽減の基準(43万円・31万円・57万円)は浜松・新潟・熊本。
#   厚生労働省(非自発的失業者 30/100)。開けなかったもの:任意継続の保険料額表の新しい置き場所(assets/13tokyo2_r8.pdf・27osaka2_r8.pdf)・静岡市。
# 2026-11-21 の2回目の見直しで開いたもの:広島市「国民健康保険料の軽減」(令和8年度 5割31万円・2割57万円・+10万円×(給与所得者等の数−1))・
#   大阪府(医療66万円・支援26万円・介護17万円・子ども3万円)・中央区(基礎控除の段・限度額67・26・17・3万円)・
#   協会けんぽ 上限32万円のページと愛知支部の任意継続の額表(10.16%・11.78%。支援金は合算・1円未満切り捨てと一致)。
#   非自発的失業の30/100を7割・5割・2割の判定にも使う文は、厚生労働省の資料2つ・新宿区・江戸川区・川崎市・千葉市・秋田市・西宮市で確認できなかった。
# 最後に原本を確かめた日: 2026-11-21
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from fractions import Fraction as F
from _lib import run
import rates
TOKYO = rates.TOKYO

# 協会けんぽ 令和8年度の都道府県単位保険料率(%の100倍)。協会けんぽのページから書き写した
KP = rates.kenpo_pref()
SHIEN, KAIGO, NINI_CAP = rates.SIEN, rates.KAIGO, rates.NINI_CAP
# 標準報酬月額(健康保険 1〜23等級):(月額, 報酬月額がこの額未満)
TOKYU = rates.tokyu_sen_finite(22)

CAP = rates.kokuho_caps()
# (表示名, [医療, 支援, 介護, 子ども] の (所得割 %の100倍, 均等割, 平等割), 端数の単位, 名古屋の独自減額, 医療分の限度額, 都道府県)
D = rates.kokuho_d(True)
PIDX = {name: i for i, (name, _) in enumerate(KP)}

def fl(x):
    x = F(x)
    return x.numerator // x.denominator

def kyuyo(x):
    """令和7年分の給与所得(所得税法28条・別表第五)。"""
    return rates.kyuyo_r7(x)

def keigen(g, n):
    return rates.keigen(g, n)

def hoken(d, g, me40, fam, fam40):
    p, r, nag, cap0 = d[1], d[2], d[3], d[4]
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
    return sum(out)

def kokuho(d, a, old, hi, fam):
    """退職前の年収 a。会社都合など(非自発的失業者)は給与所得を100分の30にする。家族は収入なし・本人と同じ年代。"""
    g = kyuyo(a)
    if hi: g = fl(F(g * 30, 100))
    return hoken(d, g, old, fam, fam if old else 0)

def hyojun(m):
    for s, top in TOKYU:
        if m < top * 1000: return s * 1000
    return NINI_CAP

def nini(a, old, rate):
    """月給=年収÷12(円未満切り捨て)。保険料=標準報酬月額×料率の合計(1円未満切り捨て)×12か月。"""
    s = hyojun(a // 12)
    return fl(F(s * (rate + SHIEN + (KAIGO if old else 0)), 10000)) * 12, s

def c(v):
    return '{:,}'.format(v)

def pc(v):
    return '%d.%02d%%' % (v // 100, v % 100)

LB = ['医療分', '後期高齢者支援金分', '介護分（40〜64歳）', '子ども・子育て支援金分']
ROWS = [200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000]

JS_SET = """cs=>{
 const out=[];const reg=document.getElementById('reg'),pref=document.getElementById('pref'),inc=document.getElementById('inc'),fam=document.getElementById('fam');
 const tx=id=>document.getElementById(id).innerText.replace(/\\s+/g,'');
 for(const k of cs){
  if(reg.value!==String(k[0])){reg.value=String(k[0]);reg.dispatchEvent(new Event('change'));}
  if(pref.value!==String(k[1])){pref.value=String(k[1]);pref.dispatchEvent(new Event('change'));}
  document.querySelector('#s-age button[data-v="'+k[3]+'"]').click();
  document.querySelector('#s-hi button[data-v="'+k[4]+'"]').click();
  fam.value=String(k[5]);fam.dispatchEvent(new Event('change'));
  inc.value=String(k[2]);inc.dispatchEvent(new Event('input'));
  out.push([tx('o-k'),tx('o-n'),tx('o-vd'),tx('o-vds'),tx('o-note'),tx('e-k'),tx('e-n'),tx('t-cap'),
   k[6]?[...document.querySelectorAll('#ktb tr')].map(r=>[...r.children].map(td=>td.textContent)):null,
   [...document.querySelectorAll('#ktb tr.hit')].map(r=>r.children[0].textContent)]);
 }
 return out;}"""

async def body(pg):
    n = bad = 0
    def chk(label, got, want):
        nonlocal n, bad
        n += 1
        if got != want:
            bad += 1
            if bad < 40: print('NG', label, repr(got)[:300], repr(want)[:300])

    here = os.path.dirname(os.path.abspath(__file__))
    raw = open(os.path.join(here, '..', '..', 'site', 'kokuho', 'index.html'), encoding='utf-8').read()

    # 原本どうしの照らし合わせ(協会けんぽの任意継続の保険料額表)
    for s, w0, w1 in [(58000, 5846, 6786), (126000, 12700, 14742), (142000, 14313, 16614), (320000, 32256, 37440)]:
        chk('東京支部の額表 %d' % s, [fl(F(s * (TOKYO + SHIEN), 10000)), fl(F(s * (TOKYO + SHIEN + KAIGO), 10000))], [w0, w1])
    for s, w0, w1 in [(58000, 5869, 6809), (126000, 12751, 14792), (134000, 13560, 15731), (320000, 32384, 37568)]:
        chk('京都支部の額表 %d' % s, [fl(F(s * (989 + SHIEN), 10000)), fl(F(s * (989 + SHIEN + KAIGO), 10000))], [w0, w1])
    # 協会けんぽ 任意継続被保険者の保険料額表(東京支部・令和8年4月分から)の全23等級。2026-11-21 に表から書き写した(40歳未満 10.08%・40〜64歳 11.70%)
    TOKYO_HYO = [(58, 5846, 6786), (68, 6854, 7956), (78, 7862, 9126), (88, 8870, 10296), (98, 9878, 11466), (104, 10483, 12168),
                 (110, 11088, 12870), (118, 11894, 13806), (126, 12700, 14742), (134, 13507, 15678), (142, 14313, 16614), (150, 15120, 17550),
                 (160, 16128, 18720), (170, 17136, 19890), (180, 18144, 21060), (190, 19152, 22230), (200, 20160, 23400), (220, 22176, 25740),
                 (240, 24192, 28080), (260, 26208, 30420), (280, 28224, 32760), (300, 30240, 35100), (320, 32256, 37440)]
    chk('東京支部の額表の等級', [x[0] for x in TOKYO_HYO], [g[0] for g in TOKYU] + [NINI_CAP // 1000])
    for s, w0, w1 in TOKYO_HYO:
        chk('東京支部の額表(全等級) %d' % s, [fl(F(s * 1000 * (TOKYO + SHIEN), 10000)), fl(F(s * 1000 * (TOKYO + SHIEN + KAIGO), 10000))], [w0, w1])
    chk('都道府県の数', len(KP), 47)
    lo = min(KP, key=lambda x: x[1]); hi_ = max(KP, key=lambda x: x[1])

    # tools/regions.py(読むだけ)と原本から書いた値の照らし合わせ
    import regions
    chk('regions.py PREF', [tuple(x) for x in regions.PREF], KP)
    chk('regions.py REG の数', len(regions.REG), len(D))
    for r, d in zip(regions.REG, D):
        caps = [d[4]] + CAP[1:]
        chk('regions.py ' + d[0], [r['s'], [tuple(x) for x in r['p']], r['r'], r['nag']],
            [d[0], [q + (caps[j],) for j, q in enumerate(d[1])], d[2], d[3]])

    # 都道府県の選択肢(47)と、手で書いた協会けんぽの料率の表(47行)
    opts = await pg.eval_on_selector_all('#pref option', "os=>os.map(o=>[o.value,o.textContent])")
    chk('都道府県の選択肢', opts, [[str(i), '%s（%s）' % (nm, pc(r))] for i, (nm, r) in enumerate(KP)])
    rows = await pg.eval_on_selector_all(':is(#nini ~ .tw):not(#nini ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.innerText.trim()))")
    chk('協会けんぽの表の行の数', len(rows), 47)
    for r, (nm, rt) in zip(rows, KP):
        chk('協会けんぽの表 ' + nm, r, [nm, pc(rt), pc(rt + SHIEN), pc(rt + SHIEN + KAIGO)])

    # 47都道府県×23等級×年齢の任意継続(東京23区のまま都道府県だけ変える。月給が等級のまん中になる年収)
    cases = []
    grades = [(s * 1000, (top * 1000 - 1) * 12) for s, top in TOKYU] + [(NINI_CAP, 310000 * 12)]
    for pi in range(47):
        for s, a in grades:
            for old in (0, 1):
                cases.append((0, pi, a, old, 0, 0, 0))
    # 等級の境目の前後(月給がちょうど境目になる年収)。東京都と大阪府
    for pi in (PIDX['東京都'], PIDX['大阪府'], PIDX['佐賀県']):
        for s, top in TOKYU:
            for a in (top * 12000 - 1, top * 12000, top * 12000 + 11, top * 12000 + 12):
                cases.append((0, pi, a, 1, 0, 0, 0))
    # 22の地域×年齢×辞めた理由×家族。年収は給与所得控除・軽減・上限の境目の前後と代表例
    for i, d in enumerate(D):
        pi = PIDX[d[5]]
        for old in (0, 1):
            for hi in (0, 1):
                for fam in (0, 1, 2, 3):
                    nn = 1 + fam
                    As = {0, 650999, 651000, 1000000, 1080000, 1081000, 1899999, 1900000, 2000000, 2500000, 3000000, 3599999, 3600000,
                          3719999, 3720000, 4000000, 4567891, 5000000, 6599999, 6600000, 8499999, 8500000, 10000000, 12000000,
                          20000000, 25949999, 25950000, 26450001, 26950001, 30000000}
                    # 軽減の境目(給与所得がちょうど境目になる年収。190万円以下は年収−65万円)
                    for th in (430000, 430000 + 310000 * nn, 430000 + 570000 * nn):
                        for dg in (-1, 0, 1, 4000):
                            As.add(th + 650000 + dg)
                    for a in sorted(As):
                        cases.append((i, pi, a, old, hi, fam, 0))
                    # 早見表の全行(その条件の表を1回読む)
                    cases.append((i, pi, 5000000, old, hi, fam, 1))
    # 市区町村と違う都道府県を選んだとき
    for i, pi in [(0, PIDX['佐賀県']), (15, PIDX['新潟県']), (20, PIDX['沖縄県'])]:
        for a in (2400000, 3000000, 4000000, 7000000):
            cases.append((i, pi, a, 1, 0, 1, 1))

    for s0 in range(0, len(cases), 300):
        part = cases[s0:s0 + 300]
        res = await pg.evaluate(JS_SET, [list(k) for k in part])
        for k, got in zip(part, res):
            i, pi, a, old, hi, fam, tbl = k
            d = D[i]; rate = KP[pi][1]
            kv = kokuho(d, a, old, hi, fam); ny, s = nini(a, old, rate)
            lab = '%s %s 年収%d 年齢%d 理由%d 家族%d' % (d[0], KP[pi][0], a, old, hi, fam)
            chk('箱 国保 ' + lab, got[0], c(kv) + '円')
            chk('箱 任意継続 ' + lab, got[1], c(ny) + '円')
            df = abs(kv - ny)
            chk('結論 ' + lab, got[2], ('%sのほうが年%s円安いです' % ('国民健康保険' if kv < ny else '任意継続', c(df))) if df else 'どちらも同じ額です')
            chk('結論の下 ' + lab, got[3], '国民健康保険は年%s円・任意継続は年%s円です' % (c(kv), c(ny)))
            chk('標準報酬月額の文 ' + lab, got[4], '任意継続の保険料は、標準報酬月額%s円（月給を年収÷12とした場合）で計算しています' % c(s))
            chk('地域の名前 ' + lab, [got[5], got[6]], [d[0], '協会けんぽ' + KP[pi][0]])
            chk('表の題 ' + lab, got[7], '%s・%s・%s・%s' % (d[0], '40〜64歳' if old else '40歳未満', '会社都合など' if hi else '自己都合', '家族%d人' % fam if fam else '家族なし'))
            hit = [c(r) for r in ROWS if a >= r * 10000][-1:]
            chk('黄色の行 ' + lab, got[9], hit)
            if tbl:
                want = []
                for r in ROWS:
                    k2 = kokuho(d, r * 10000, old, hi, fam); n2 = nini(r * 10000, old, rate)[0]
                    want.append([c(r), c(k2), c(n2), '国保' if k2 < n2 else ('任意継続' if k2 > n2 else '同じ')])
                chk('早見表 ' + lab, got[8], want)

    # 黄色の行(入力した年収を超えない中でいちばん近い行)
    for a, want in [(1999999, []), (2000000, ['200']), (4490000, ['400']), (4500000, ['450']), (30000000, ['1,000'])]:
        res = await pg.evaluate(JS_SET, [[0, PIDX['東京都'], a, 0, 0, 0, 0]])
        chk('黄色の行 %d' % a, res[0][9], want)

    # 市区町村を選ぶと都道府県がその市区町村のある都道府県に切り替わる・料率の表
    for i, d in enumerate(D):
        await pg.select_option('#pref', str(PIDX['沖縄県'] if d[5] != '沖縄県' else 0))
        await pg.select_option('#reg', str(i))
        chk('都道府県の切り替え ' + d[0], await pg.input_value('#pref'), str(PIDX[d[5]]))
        rows = await pg.eval_on_selector_all('#rtb tr', "rs=>rs.map(r=>[...r.children].map(td=>td.textContent))")
        caps = [d[4]] + CAP[1:]
        chk('料率の表 ' + d[0], rows, [[LB[j], pc(q[0]), c(q[1]), c(q[2]), c(caps[j])] for j, q in enumerate(d[1])])
        chk('料率の表の題 ' + d[0], await pg.inner_text('#r-cap'), d[0] + '・令和8年度')
    opts = await pg.eval_on_selector_all('#reg option', "os=>os.map(o=>o.textContent)")
    for i, d in enumerate(D):
        chk('市区町村の選択肢 ' + d[0], opts[i].startswith(d[0]), True)

    # 任意継続のほうが安くなる年収(手で書いた22行。1人・自己都合・その市区町村の都道府県の料率)
    # 1万円きざみで、その年収から上(3,000万円まで)はずっと任意継続のほうが安くなるいちばん小さい年収
    def wakare(d, old):
        rate = KP[PIDX[d[5]]][1]
        x = None
        for m in range(3000, 99, -1):
            if nini(m * 10000, old, rate)[0] < kokuho(d, m * 10000, old, 0, 0): x = m
            else: break
        return x
    rows = await pg.eval_on_selector_all(':is(#wakare ~ .tw):not(#wakare ~ .tw ~ .tw) tbody tr', "rs=>rs.map(r=>[...r.children].map(td=>td.innerText.trim()))")
    chk('安くなる年収の表の行の数', len(rows), 22)
    for r, d in zip(rows, D):
        chk('安くなる年収 ' + d[0], r, [d[0], '%d万円から' % wakare(d, 0), '%d万円から' % wakare(d, 1)])
        # その年収より下で任意継続が安い所がないか(200万円以上)
        for old in (0, 1):
            w = wakare(d, old); rate = KP[PIDX[d[5]]][1]
            # 大阪市・堺市だけは、表の額より下でも任意継続のほうが安い年収がある(標準報酬月額の等級の段で入れ替わる)。注記の文と合わせる
            chk('安くなる年収より下 ' + d[0], bool([m for m in range(200, w) if nini(m * 10000, old, rate)[0] < kokuho(d, m * 10000, old, 0, 0)]), d[0] == '大阪市・堺市')
    chk('安くなる年収の注記', '大阪市・堺市は、年収が表の額より低くても任意継続のほうが安くなることがあります。' in raw, True)

    # 一覧にない市区町村(料率を入れる)。選んでいた地域の料率が入り、端数は1円・独自減額なし・上限は67万円で計算する
    await pg.select_option('#reg', '15')
    await pg.select_option('#reg', 'x')
    vals = [await pg.input_value('#c%d%d' % (j, k)) for j in range(4) for k in range(3)]
    chk('料率を入れる欄 大阪府の値', vals, [x for q in D[15][1] for x in ('%d.%02d' % (q[0] // 100, q[0] % 100), c(q[1]), c(q[2]))])
    chk('料率を入れても都道府県はそのまま', await pg.input_value('#pref'), str(PIDX['大阪府']))
    my = [(812, 31234, 12345), (255, 9876, 1111), (199, 12000, 0), (31, 1555, 99)]
    low = [(100, 30000, 0), (50, 10000, 0), (40, 10000, 0), (5, 1000, 0)]      # 上限に届かない低い料率(基礎控除の段を見る)
    for rates in (my, low):
        for j in range(4):
            await pg.fill('#c%d0' % j, '%d.%02d' % (rates[j][0] // 100, rates[j][0] % 100))
            await pg.fill('#c%d1' % j, str(rates[j][1]))
            await pg.fill('#c%d2' % j, str(rates[j][2]))
        dx = ('入力した料率', rates, 1, 0, 670000, '大阪府')
        for a, old, hi, fam in [(0, 0, 0, 0), (1390000, 1, 0, 1), (4000000, 1, 0, 2), (4000000, 0, 1, 0), (12000000, 1, 0, 3),
                                (25950000, 1, 0, 0), (25950001, 1, 0, 0), (26450001, 0, 0, 1), (26950001, 1, 0, 0), (30000000, 0, 0, 0)]:
            res = await pg.evaluate(JS_SET.replace("if(reg.value!==String(k[0]))", "if(false)"), [['x', PIDX['大阪府'], a, old, hi, fam, 0]])
            chk('入力した料率 %d %d %d %d' % (a, old, hi, fam), res[0][:2] + [res[0][5]],
                [c(kokuho(dx, a, old, hi, fam)) + '円', c(nini(a, old, 1013)[0]) + '円', '入力した料率'])
    await pg.select_option('#reg', '0')

    # 本文とよくある質問の数字
    k5 = kokuho(D[0], 5000000, 0, 0, 0); n5 = nini(5000000, 0, TOKYO)[0]
    flat = ''.join((await pg.inner_text('main')).split())
    for label, want in [
        ('QA 年収500万円', '東京23区・1人で加入・40歳未満・自己都合なら、国民健康保険が年%s円で任意継続が年%s円です。任意継続のほうが年%s円安くなります。' % (c(k5), c(n5), c(k5 - n5))),
        ('料率の幅', '協会けんぽの令和8年度の料率は都道府県ごとに%s（%s）から%s（%s）です。' % (pc(lo[1]), lo[0], pc(hi_[1]), hi_[0])),
        ('支援金と介護', 'これに子ども・子育て支援金の%sが加わり、40〜64歳は介護保険の%sも加わります。' % (pc(SHIEN), pc(KAIGO))),
        ('表の注記の率', '支援金込みは子ども・子育て支援金率%sを足した率です。40〜64歳はさらに介護保険料率%sを足します。' % (pc(SHIEN), pc(KAIGO))),
        ('上限 冒頭', '令和8年度は%d万円が上限です。' % (NINI_CAP // 10000)),
        ('上限 前提', '標準報酬月額の上限%d万円で計算しています' % (NINI_CAP // 10000)),
        ('上限 早見表の注記', '標準報酬月額（上限%d万円）' % (NINI_CAP // 10000)),
        ('上限 決まり方', '退職したときの額と%d万円の少ないほうです。月給が%d万円を超えていた人は、いくら高くても%d万円で計算されます。' % ((NINI_CAP // 10000,) * 3)),
        ('43万円', '給与所得から43万円を引いた額に所得割をかけ'),
        ('20日', '退職日の翌日から20日以内'),
        ('30%', '給与所得を30%として扱います。'),
        ('4月分', '任意継続の人は4月分の保険料から新しい料率になります。'),
        ('最長2年', '最長2年入り続けるしくみです。'),
    ]:
        chk('本文 ' + label, want in flat, True)
    desc = '政令指定都市19市・東京23区・47都道府県の料率に対応しています。'
    chk('description と og', raw.count(desc), 2)
    chk('政令指定都市の数(大阪市・堺市は2市)', len([d for d in D if d[0].endswith('市')]) + 1, 19)

    # JS が書き換える前の元の文(既定は東京23区・東京都・年収500万円・40歳未満・自己都合・家族なし)
    for label, want in [
        ('既定の年収', 'id="inc" inputmode="numeric" min="0" max="30000000" step="10000" value="5000000"'),
        ('既定の都道府県', '<option value="12" selected>東京都（9.85%）</option>'),
        ('表の題', '<p class="cap" id="t-cap">東京23区・40歳未満・自己都合・家族なし</p>'),
        ('料率の題', '<p class="cap" id="r-cap">東京23区・令和8年度</p>'),
        ('国保', '<b id="o-k">%s<i>円</i></b><em id="e-k">東京23区</em>' % c(k5)),
        ('任意継続', '<b id="o-n">%s<i>円</i></b><em id="e-n">協会けんぽ東京都</em>' % c(n5)),
        ('安いほう', '<b id="o-w" style="font-size:18px">任意継続</b><em id="o-d">年%s円安い</em>' % c(k5 - n5)),
        ('結論', '<b id="o-vd">任意継続のほうが年%s円安いです</b><span id="o-vds">国民健康保険は年%s円・任意継続は年%s円です</span>' % (c(k5 - n5), c(k5), c(n5))),
        ('標準報酬月額の文', '<li id="o-note">任意継続の保険料は、標準報酬月額320,000円（月給を年収÷12とした場合）で計算しています</li>'),
    ]:
        chk('元の文 ' + label, want in raw, True)
    # 出典のリンクの文字(2026-11-21 に着いたページの題名と合わせた)
    for t in ['東京都保健医療局「令和8年度 特別区国民健康保険料一覧表」', '札幌市「保険料の計算」', '仙台市「保険料はいくら（令和8年度）」', 'さいたま市「国民健康保険税の計算」',
              '千葉市「令和8年度国民健康保険料率の決定」', '横浜市「令和8年度保険料の料率等について」', '川崎市「令和8年度の国民健康保険料について」',
              '相模原市「令和8年度 国民健康保険税の税率等について」', '新潟市「令和8年度の国民健康保険料率と軽減判定所得について」', '浜松市「保険料について」',
              '名古屋市「令和8年度分の国民健康保険料」', '京都市「令和8年度の保険料の計算方法について」', '大阪府「令和8年度大阪府市町村標準保険料率等の算定結果について」',
              '神戸市「国民健康保険料の額」', '岡山市「令和8年度国民健康保険料率のお知らせ」', '広島市「国民健康保険料の計算方法」', '北九州市「国民健康保険料の計算方法」',
              '福岡市「国民健康保険料の計算方法」', '熊本市「国民健康保険 保険料について」']:
        chk('出典の文字 ' + t, raw.count('>' + t + '</a>'), 1)
    chk('更新日', '更新日：2026年11月23日（' in raw, True)
    chk('span の開きと閉じの数', raw.count('<span'), raw.count('</span>'))
    chk('id の重なり', len(set(__import__('re').findall(r'\sid="([^"]+)"', raw))), len(__import__('re').findall(r'\sid="([^"]+)"', raw)))
    return n, bad

run('kokuho', body)
