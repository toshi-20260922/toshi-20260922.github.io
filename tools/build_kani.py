# 簡易課税の事業区分と納める消費税の計算 /kani-kazei/ を作る。2026/11/20。
# 原本:国税庁 No.6509「簡易課税制度の事業区分」・No.6509 Q&A・No.6505「簡易課税制度」・No.6371「端数計算」・No.6303「税率」、
#      質疑応答事例「簡易課税制度の事業区分」20/01〜20/16(業種の例)、「消費税のあらまし」010.pdf(75%の特例の例)、
#      「消費税及び地方消費税の申告書（簡易課税用）の書き方」202411_02.pdf(特例の計算と百円未満切捨ての例)
import os, sys, json
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_saitei as B

RATE = [90, 80, 70, 60, 50, 40]
SHU = ['第1種', '第2種', '第3種', '第4種', '第5種', '第6種']
NAME = ['卸売業', '小売業など', '製造業・建設業など', '飲食店業など', 'サービス業など', '不動産業']

def calc(s):
    """s = 第1種〜第6種の税抜の課税売上高。標準税率10%だけ。控除が一番多い方法で計算する。"""
    S = sum(s)
    if S <= 0:
        return dict(T=0, D=0, koku=0, chiho=0, total=0, how='', rate=F(0))
    K = S // 1000 * 1000                    # 課税標準額は1,000円未満切捨て
    T = K * 78 // 1000                      # 消費税額(7.8%・1円未満切捨て)
    cands = []
    w = sum(F(s[i]) * RATE[i] for i in range(6)) / (S * 100)
    cands.append((T * w, '原則の計算（業種ごとの割合）', w))
    kinds = [i for i in range(6) if s[i] > 0]
    for i in kinds:
        if 4 * s[i] >= 3 * S and len(kinds) >= 2:
            r = F(RATE[i], 100); cands.append((T * r, '%sが75%%以上の特例' % SHU[i], r))
    if len(kinds) >= 3:
        for a in kinds:
            for b in kinds:
                if a < b and 4 * (s[a] + s[b]) >= 3 * S:
                    r = (F(s[a]) * RATE[a] + F(S - s[a]) * RATE[b]) / (S * 100)
                    cands.append((T * r, '%sと%sで75%%以上の特例' % (SHU[a], SHU[b]), r))
    best = max(cands, key=lambda x: x[0])
    D = int(best[0])                        # 1円未満切捨て
    koku = (T - D) // 100 * 100             # 納める国税は100円未満切捨て
    chiho = koku * 22 // 78 // 100 * 100    # 地方消費税は国税の78分の22・100円未満切捨て
    return dict(T=T, D=D, koku=koku, chiho=chiho, total=koku + chiho, how=best[1], rate=best[2])

# 国税庁の例で確かめる
r = calc([0, 0, 0, 0, 9000000, 0]); assert (r['T'], r['koku'], r['chiho'], r['total']) == (702000, 351000, 99000, 450000), r
assert 1799601 * 80 // 100 == 1439680            # 申告書の書き方:特例(1種類で75%以上)の控除対象仕入税額
assert 320200 * 22 // 78 // 100 * 100 == 90300   # 同:譲渡割額 90,312円→90,300円
r = calc([8000000, 2000000, 0, 0, 0, 0]); assert r['rate'] == F(90, 100), r          # あらまし:第1種80・第2種20は全体に90%
r = calc([4500000, 3500000, 0, 0, 2000000, 0]); assert r['rate'] == F(45 * 90 + 55 * 80, 10000), r  # 第1種45・第2種35・第5種20
r = calc([0, 7000000, 3000000, 0, 0, 0]); assert r['rate'] == F(77, 100), r          # 第2種70・第3種30は原則で77%

# 業種の例:(グループ, 業種, 第何種(0〜5), ひとこと)
EX = [
 ('仕入れた商品をそのまま売る', '卸売業（事業者に売る）', 0, '仕入れた商品の形を変えずに、ほかの事業者に売ります'),
 ('仕入れた商品をそのまま売る', '小売業（消費者に売る）', 1, '仕入れた商品の形を変えずに、消費者に売ります'),
 ('仕入れた商品をそのまま売る', 'ネットショップ（消費者に売る）', 1, '事業者に売った分は第1種です'),
 ('仕入れた商品をそのまま売る', '精肉店・鮮魚店（切る・刻むだけ）', 1, '焼く・揚げるなど加熱して売ると第3種です'),
 ('仕入れた商品をそのまま売る', '美容室・理容店の化粧品やシャンプーの販売', 1, 'カットやパーマなどの施術は第5種です'),
 ('仕入れた商品をそのまま売る', '農業・漁業（飲食料品を売る）', 1, '令和元年10月から第2種です'),
 ('作る・工事をする', '建設業（工事の請負）', 2, '工事を丸ごと下請に出しても第3種です'),
 ('作る・工事をする', '造園工事の請負', 2, '植木の剪定だけなら第4種です'),
 ('作る・工事をする', '製造業（製造問屋を含む）', 2, '材料の支給を受けて加工するだけなら第4種です'),
 ('作る・工事をする', 'パン・菓子・惣菜・弁当の製造小売', 2, '店内で食べさせる部分は第4種です'),
 ('作る・工事をする', '出版業（印刷を外に出しても）', 2, '新聞などの紙上広告の収入は第5種です'),
 ('作る・工事をする', '農業・林業（飲食料品以外を売る）', 2, '花や木材など、食べ物でないものを売る場合です'),
 ('作る・工事をする', '宅配ピザ・仕出し専門店（食べる席がない）', 2, '飲食店の出前は第4種です'),
 ('作る・工事をする', '中古車に板金・塗装・部品交換をして売る', 2, '手を加えずに売ると第1種か第2種です'),
 ('作る・工事をする', '自分で建てた建物を売る', 2, 'ほかの人が建てた建物をそのまま売ると第1種か第2種です'),
 ('飲食店・加工賃など', '飲食店（食堂・すし店・喫茶店など）', 3, '持ち帰りの商品を仕入れて売る部分は第2種です'),
 ('飲食店・加工賃など', '飲食店の出前・仕出し', 3, '食べる席のない宅配専門店は第3種です'),
 ('飲食店・加工賃など', '建設の手間仕事（材料の支給を受けて行う作業）', 3, '道具を持っていくかどうかにかかわらず第4種です'),
 ('飲食店・加工賃など', 'とび工事・しゅんせつ工事', 3, '国税庁の質疑応答事例で第4種とされています'),
 ('飲食店・加工賃など', '庭師の植木の剪定', 3, '造園工事の請負は第3種です'),
 ('飲食店・加工賃など', '支給された材料の賃加工（精米・縫製など）', 3, '材料を自分で仕入れて作ると第3種です'),
 ('飲食店・加工賃など', '代理商・仲立業', 3, '不動産の仲介は第6種です'),
 ('飲食店・加工賃など', '事業で使っていた車・機械などの売却', 3, '本業が何でも第4種です'),
 ('サービス業など', '運送業・倉庫業', 4, '運輸業は第5種です'),
 ('サービス業など', 'ソフトウェア開発・情報処理サービス', 4, '設計を外注していても第5種です'),
 ('サービス業など', '広告業', 4, ''),
 ('サービス業など', '税理士・社労士・デザイン・経営コンサルタント', 4, '専門サービス業は第5種です'),
 ('サービス業など', '旅館・ホテル', 4, '館内の売店や自動販売機の売上は第2種です'),
 ('サービス業など', '美容室・理容店・クリーニング店の施術', 4, '化粧品などを売った分は第2種です'),
 ('サービス業など', '自動車の修理（部品代を含む）', 4, '部品代を分けて請求しても第5種です'),
 ('サービス業など', '機械の修理・畳の表替え', 4, ''),
 ('サービス業など', '学習塾などの教育', 4, ''),
 ('サービス業など', 'レンタル・リース（物品賃貸業）', 4, '売買とされるリースは第1種か第2種です'),
 ('サービス業など', '保険代理店の手数料', 4, ''),
 ('サービス業など', '警備業・ビルの清掃などの建物サービス', 4, ''),
 ('サービス業など', '職業紹介・労働者派遣', 4, ''),
 ('不動産業', '不動産の仲介', 5, ''),
 ('不動産業', '事務所・店舗の貸付けと不動産の管理', 5, '住宅の貸付けは非課税なので売上に入れません'),
 ('不動産業', '駐車場の貸付け', 5, ''),
]

c = B.c; td = B.td; table = B.table
slug = 'kani-kazei'; cta = 'kani'
title = '【簡易課税の事業区分】第何種？業種の一覧とみなし仕入率・納める消費税の計算【2026年】'
desc = '簡易課税の事業区分は第1種から第6種まであり、みなし仕入率は90%から40%です。業種を選ぶと第何種かが分かり、業種ごとの売上を入力すると75%の特例も含めて納める消費税を計算します。'
upd = '更新日：2026年11月20日（国税庁 No.6505・No.6509 令和8年4月1日現在法令等）'

opts = ''; grp = None
for i, (g, nm, k, note) in enumerate(EX):
    if g != grp:
        if grp is not None:
            opts += '</optgroup>'
        opts += '<optgroup label="%s">' % g; grp = g
    opts += '<option value="%d"%s>%s</option>' % (i, ' selected' if nm.startswith('税理士') else '', nm)
opts += '</optgroup>'
inputs = ''.join('''  <div class="full">
   <label for="s%d">%s（%s・%d%%）の売上（税抜）</label>
   <div class="row"><input type="number" id="s%d" inputmode="numeric" min="0" max="5000000000" step="1" value="%d"><span>円</span></div>
  </div>
''' % (i, SHU[i], NAME[i], RATE[i], i, 9000000 if i == 4 else 0) for i in range(6))

calc_html = '''<div class="sum" id="calc">
 <div class="h"><span>結論</span>業種を選ぶと、簡易課税の第何種かとみなし仕入率を表示します</div>
 <div class="in">
  <div class="full">
   <label for="ex">業種</label>
   <select id="ex">%(opts)s</select>
  </div>
 </div>
 <div class="vd no" id="vd"><b id="o-vd"></b><span id="o-vds"></span></div>
 <div class="in">
%(inputs)s </div>
 <div class="amt">
  <div><small>納める消費税<br>（国税と地方の合計）</small><b id="o-t"></b><em id="o-te"></em></div>
  <div><small>使った<br>みなし仕入率</small><b id="o-r"></b><em id="o-re"></em></div>
  <div><small>売上の<br>消費税（国税）</small><b id="o-k"></b><em>税抜の売上×7.8%%</em></div>
 </div>
 <ul>
  <li id="o-how"></li>
  <li>税率10%%の売上だけで計算しています。基準期間の課税売上高が5,000万円以下で、届出を出している場合に使えます</li>
 </ul>
</div>
''' % {'opts': opts, 'inputs': inputs}

intro = ('<p>簡易課税は、売上の消費税に業種ごとの「みなし仕入率」をかけた額を仕入れの消費税とみなす計算です。'
         '<span class="mk">卸売業は第1種で90%・小売業は第2種で80%・製造業や建設業は第3種で70%・飲食店は第4種で60%・サービス業は第5種で50%・不動産業は第6種で40%です。</span>'
         '業種は取引ごとに分けて判定します。2つ以上の業種があるときは、1つの業種の売上が75%以上なら全体にその率を使える特例があります。</p>\n')

toc = '''<nav class="toc">
 <div class="t">目次</div>
 <ol>
  <li><a href="#kubun">第1種から第6種までの事業区分</a></li>
  <li><a href="#rei">業種ごとの事業区分の例</a></li>
  <li><a href="#gaku">売上ごとの納める消費税</a></li>
  <li><a href="#tokurei">2つ以上の業種があるとき（75%の特例）</a></li>
  <li><a href="#keisan">納める消費税の計算のしかた</a></li>
  <li><a href="#rel">次に確かめること</a></li>
  <li><a href="#qa">簡易課税の事業区分でよく聞かれること</a></li>
 </ol>
</nav>
'''

DEF = ['他の人から買った商品を、形を変えずにほかの事業者に売る事業',
       '他の人から買った商品を形を変えずに売る事業で第1種以外のもの・農業・林業・漁業のうち飲食料品を売る事業',
       '農業・林業・漁業（飲食料品以外）・鉱業・建設業・製造業（製造小売業を含む）・電気業・ガス業・熱供給業・水道業。加工賃をもらう仕事は除く',
       '第1種・第2種・第3種・第5種・第6種のどれにも当たらない事業。飲食店業・加工賃をもらう仕事・事業で使っていた固定資産の売却など',
       '運輸通信業・金融業・保険業・サービス業（飲食店業を除く）',
       '不動産業']
rows = [[td(SHU[i]), td('%d%%' % RATE[i]), td('%d%%' % (100 - RATE[i])), td(DEF[i], 'l')] for i in range(6)]
sec1 = ('<h2 id="kubun">第1種から第6種までの事業区分</h2>\n<p>納める割合は、売上の消費税のうち実際に納める割合です。みなし仕入率が高い業種ほど納める消費税が少なくなります。</p>\n'
        + table(['区分', 'みなし<br>仕入率', '納める<br>割合', '当たる事業'], rows)
        + '<p class="note" style="margin-top:8px">第3種と第5種は、おおむね日本標準産業分類の大分類で判定します。日本標準産業分類で運輸通信業・金融業・保険業・サービス業に当たる事業は、加工賃をもらう仕事でも第5種です（国税庁 No.6509）。</p>\n')

rr = [[td(nm, 'l'), td(SHU[k]), td(note or '―', 'l')] for g, nm, k, note in EX]
sec2 = ('<h2 id="rei">業種ごとの事業区分の例</h2>\n<p>国税庁の質疑応答事例とタックスアンサーに載っている例です。同じ店でも取引ごとに区分が変わることがあります。</p>\n'
        + table(['業種・取引', '区分', 'ひとこと'], rr)
        + '<p class="note" style="margin-top:8px">商品に自分の商標を付けるだけ・いくつかの商品を詰め合わせるだけなら、形を変えていないので第1種か第2種です（国税庁 質疑応答事例）。</p>\n')

gg = []
for i in range(6):
    row = [td('%s<br>（%d%%）' % (SHU[i], RATE[i]))]
    for amt in (5000000, 10000000, 30000000, 50000000):
        s = [0] * 6; s[i] = amt; row.append(td(c(calc(s)['total'])))
    gg.append(row)
sec3 = ('<h2 id="gaku">売上ごとの納める消費税</h2>\n<p>1つの業種で税率10%の売上だけのときの、国税と地方消費税の合計です。</p>\n'
        + table(['区分', '売上<br>500万円', '1,000万円', '3,000万円', '5,000万円'], gg)
        + '<p class="note" style="margin-top:8px">売上は税抜の課税売上高です。簡易課税を使えるのは、2年前（法人は2期前）の課税売上高が5,000万円以下の課税期間です。</p>\n')

def ex_row(lbl, s):
    r = calc(s)
    return [td(lbl, 'l'), td(r['how'].replace('（業種ごとの割合）', ''), 'l'), td('%s%%' % ('%.1f' % float(r['rate'] * 100)).rstrip('0').rstrip('.')), td(c(r['total']))]
tk = [ex_row('第1種800万円・第2種200万円', [8000000, 2000000, 0, 0, 0, 0]),
      ex_row('第1種450万円・第2種350万円・第5種200万円', [4500000, 3500000, 0, 0, 2000000, 0]),
      ex_row('第2種700万円・第3種300万円', [0, 7000000, 3000000, 0, 0, 0]),
      ex_row('第4種800万円・第5種200万円', [0, 0, 0, 8000000, 2000000, 0])]
sec4 = ('<h2 id="tokurei">2つ以上の業種があるとき（75%の特例）</h2>\n<p>原則は、業種ごとの売上の割合でみなし仕入率を平均します。次の特例に当たるときは、控除が多くなる方を選べます。</p>\n'
        '<ul>\n <li>1つの業種の売上が全体の75%以上なら、その業種のみなし仕入率を全体に使えます</li>\n <li>3つ以上の業種があり2つの業種の売上の合計が75%以上なら、率が高い方の業種の売上にその率を使えます。残りの売上には低い方の率を使います</li>\n</ul>\n'
        '<p class="cap">計算の例（合計1,000万円）</p>\n'
        + table(['売上の内訳', '使う計算', 'みなし<br>仕入率', '納める<br>消費税'], tk)
        + '<p class="note" style="margin-top:8px">売上を業種ごとに分けていないときは、分けていない部分に一番低いみなし仕入率を使います。帳簿・請求書の控え・レジの記録などで業種ごとに分けておきます（国税庁 No.6505・質疑応答事例）。</p>\n')

sec5 = ('<h2 id="keisan">納める消費税の計算のしかた</h2>\n'
        + table(['順番', '計算'], [
            [td('1'), td('税抜の売上の1,000円未満を切り捨てる（課税標準額）', 'l')],
            [td('2'), td('課税標準額×7.8%で売上の消費税（国税）を出し、1円未満を切り捨てる', 'l')],
            [td('3'), td('売上の消費税×みなし仕入率を差し引き、100円未満を切り捨てる（納める国税）', 'l')],
            [td('4'), td('納める国税×22/78で地方消費税を出し、100円未満を切り捨てる', 'l')]])
        + '<p>第5種で売上900万円なら、売上の消費税（国税）は702,000円です。50%の351,000円を差し引いて国税351,000円、地方消費税99,000円で合計450,000円です。</p>\n'
        '<p class="note" style="margin-top:8px">令和9年4月1日から令和11年3月31日までは飲食料品の譲渡の消費税率が下がり、その間は簡易課税の計算にも特例があります（国税庁 No.6505）。このページの計算は税率10%の売上だけです。</p>\n')

rel_items = [
    ('niwari-tokurei', '消費税の計算', '2割特例が終わったあと、簡易課税・本則課税・3割特例のどれが得かを比べられます。'),
    ('kakutei-shinkoku', '確定申告の期限の早見表', '消費税の申告と納付の期限を確かめられます。'),
    ('houjinnari', '法人成りの計算', '会社にすると、消費税の免税や簡易課税の判定がやり直しになります。'),
    ('kojin-zei', '個人事業主の手取りの早見表', '消費税を払ったあと、所得税と住民税でいくら残るかが分かります。'),
    ('houjinzei-keisan', '法人税の計算', '会社の利益から、法人税・住民税・事業税の合計を出せます。'),
    ('fukugyo', '副業の税金の計算', '副業の売上が1,000万円を超えると、2年後から消費税がかかります。'),
    ('gensen-hoshu', '源泉徴収の早見表', 'デザイン料や原稿料を払うときは、源泉徴収が要るかを確かめます。'),
    ('taiyonensu', '法定耐用年数の一覧', '事業で使った車や機械を売ると、簡易課税では第4種です。'),
    ('soneki-bunkiten', '損益分岐点の計算', 'いくら売れば赤字にならないかを確かめられます。'),
    ('shotoku-kingaku', '所得金額の計算', '事業の所得から、合計所得金額と扶養に入るかが分かります。'),
    ('hensai', '借入の返済の計算', '開業資金を借りたら、毎月の返済額を先に確かめます。'),
]
sec6 = B.rel(slug, rel_items)

qa = ('<h2 id="qa">簡易課税の事業区分でよく聞かれること</h2>\n'
      '<h3>フリーランスのデザイナーやエンジニアは第何種ですか？</h3>\n<p>第5種です。デザイン業や情報サービス業はサービス業に当たり、みなし仕入率は50%です。</p>\n'
      '<h3>一人親方の建設業は第3種ですか、第4種ですか？</h3>\n<p>材料を自分で仕入れて工事を請け負うなら第3種です。材料の支給を受けて作業だけをするなら、道具を持っていくかどうかにかかわらず第4種です。</p>\n'
      '<h3>事業で使っていた車を売ったら第何種ですか？</h3>\n<p>第4種です。本業が何であっても、事業で使っていた固定資産の売却は第4種です。</p>\n'
      '<h3>簡易課税の届出はいつまでに出しますか？</h3>\n<p>使いたい課税期間が始まる日の前日までです。一度使い始めると、2年間はやめる届出を出せません。</p>\n'
      '<h3>業種ごとに売上を分けないとどうなりますか？</h3>\n<p>分けていない売上には、その中で一番低いみなし仕入率を使います。第2種と第3種を分けていなければ、全部に70%を使います。</p>\n')

src = '''<div class="src">出典・参考（2026年11月確認）
 <ul>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6509.htm">国税庁 No.6509「簡易課税制度の事業区分」</a>（令和8年4月1日現在法令等）</li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6509_qa.htm">国税庁「簡易課税制度の事業区分 Q&amp;A」</a>（固定資産の売却・加工くず）</li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6505.htm">国税庁 No.6505「簡易課税制度」</a>（適用の条件・75%の特例・区分していない場合）</li>
  <li><a href="https://www.nta.go.jp/law/shitsugi/shohi/20/02.htm">国税庁 質疑応答事例「事業区分の判定のフローチャート」</a>と同じ章の業種別の事例（20/01〜20/16）</li>
  <li><a href="https://www.nta.go.jp/publication/pamph/shohi/aramashi/pdf/010.pdf">国税庁「消費税のあらまし」簡易課税制度</a>（75%の特例の計算例）</li>
  <li><a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6371.htm">国税庁 No.6371「端数計算」</a>・<a href="https://www.nta.go.jp/taxes/shiraberu/taxanswer/shohi/6303.htm">No.6303「消費税および地方消費税の税率」</a></li>
  <li><a href="https://www.nta.go.jp/publication/pamph/shohi/kaisei/yoshiki/pdf/202411_02.pdf">国税庁「消費税及び地方消費税の申告書（簡易課税用）の書き方」</a>（地方消費税の百円未満切捨ての例）</li>
 </ul>
</div>
'''

JS = r'''(function(){
 var R=[90,80,70,60,50,40],SHU=["第1種","第2種","第3種","第4種","第5種","第6種"],EX=%(EX)s;
 var $=function(i){return document.getElementById(i)};
 function f(n){return n.toLocaleString("ja-JP");}
 function num(i){var v=parseInt($(i).value,10);if(isNaN(v)||v<0)v=0;return Math.min(v,5000000000);}
 function md(a,b,c){return Number(BigInt(Math.round(a))*BigInt(Math.round(b))/BigInt(Math.round(c)));}
 function calc(s){var S=0,i,a,b;for(i=0;i<6;i++)S+=s[i];if(S<=0)return null;
  var K=Math.floor(S/1000)*1000,T=md(K,78,1000),c=[],kinds=[];
  var w=0;for(i=0;i<6;i++){w+=s[i]*R[i];if(s[i]>0)kinds.push(i);}
  c.push([md(T,w,S*100),"原則の計算（業種ごとの割合）",w/S]);
  if(kinds.length>=2)kinds.forEach(function(i){if(4*s[i]>=3*S)c.push([md(T,R[i],100),SHU[i]+"が75%%以上の特例",R[i]]);});
  if(kinds.length>=3)kinds.forEach(function(a){kinds.forEach(function(b){if(a<b&&4*(s[a]+s[b])>=3*S){var x=s[a]*R[a]+(S-s[a])*R[b];c.push([md(T,x,S*100),SHU[a]+"と"+SHU[b]+"で75%%以上の特例",x/S]);}});});
  var best=c[0];c.forEach(function(x){if(x[0]>best[0])best=x;});
  var koku=Math.floor((T-best[0])/100)*100,chiho=Math.floor(md(koku,22,78)/100)*100;
  return {T:T,D:best[0],koku:koku,chiho:chiho,total:koku+chiho,how:best[1],rate:best[2]};}
 function render(){
  var e=EX[+$("ex").value];
  $("o-vd").textContent=SHU[e[2]]+"（みなし仕入率"+R[e[2]]+"%%）です";
  $("o-vds").textContent=e[1]+"は"+SHU[e[2]]+"です。"+(e[3]?e[3]+"。":"")+"売上の消費税の"+(100-R[e[2]])+"%%を納めます";
  var s=[],i;for(i=0;i<6;i++)s.push(num("s"+i));
  var r=calc(s);
  if(!r){$("o-t").innerHTML="0<i>円</i>";$("o-te").textContent="売上を入力してください";$("o-r").innerHTML="―";$("o-re").textContent="";$("o-k").innerHTML="0<i>円</i>";$("o-how").textContent="業種ごとの税抜の売上を入力すると計算します";return;}
  $("o-t").innerHTML=f(r.total)+"<i>円</i>";$("o-te").textContent="国税"+f(r.koku)+"円・地方"+f(r.chiho)+"円";
  $("o-r").innerHTML=(Math.round(r.rate*10)/10)+"<i>%%</i>";$("o-re").textContent=r.how;
  $("o-k").innerHTML=f(r.T)+"<i>円</i>";
  $("o-how").textContent="売上の消費税"+f(r.T)+"円から"+f(r.D)+"円を差し引いています。控除が一番多くなる計算を選んでいます";}
 $("ex").addEventListener("change",render);
 for(var i=0;i<6;i++)$("s"+i).addEventListener("input",render);
 window.__kani=calc;
 render();
})();''' % {'EX': json.dumps([[g, nm, k, note] for g, nm, k, note in EX], ensure_ascii=False)}

PIC = '<div class="pic"><svg viewBox="0 0 64 64" width="56" height="56" role="img" aria-label="6つの区分の箱"><circle cx="32" cy="32" r="31" fill="#eef6f2"/><rect x="12" y="16" width="12" height="12" rx="2" fill="#0f3d31"/><rect x="26" y="16" width="12" height="12" rx="2" fill="#00775a"/><rect x="40" y="16" width="12" height="12" rx="2" fill="#00775a"/><rect x="12" y="32" width="12" height="12" rx="2" fill="#00775a"/><rect x="26" y="32" width="12" height="12" rx="2" fill="#00775a"/><rect x="40" y="32" width="12" height="12" rx="2" fill="#e08a2c"/></svg></div>'

body = calc_html + '\n' + B.share(slug) + '\n' + intro + '\n' + toc + '\n' + sec1 + '\n' + sec2 + '\n' + sec3 + '\n' + sec4 + '\n' + sec5 + '\n' + sec6 + '\n' + qa + '\n' + src
h = B.page(slug, title, desc, upd, body, JS, cta, pic=PIC, auth=B.auth_box('国税庁'))
close_old = B.close_box(cta)
close_new = ('<div class="close"><p class="close-h"><span class="nw">簡易課税にするか、</span><span class="nw">迷ったら</span></p>'
             '<p>簡易課税にするか本則課税にするかで、帳簿のつけ方と申告書が変わります。記帳から決算・申告まで、まるごとお受けしています。全国どこからでも対応します。初回のご相談は無料です。</p>'
             '<a class="cbtn" href="https://oyama-toshiro.com/contact/" data-cta="kani_close_marunage">経理丸投げの無料相談</a></div>')
assert close_old in h
h = h.replace(close_old, close_new)
os.makedirs(os.path.join(B.SITE, slug), exist_ok=True)
open(os.path.join(B.SITE, slug, 'index.html'), 'w', encoding='utf-8').write(h)
print('ok', title)
