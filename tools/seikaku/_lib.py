# 毎日の全ツール点検で使う共通の部品。
# 1ページにつき1つ tools/seikaku/<ページの住所>.py を置く(最低賃金の県ページは saitei.py の1つで全県を見る)。
# 決まり:ページの JS を見ずに書いた自分の計算(Python・整数か分数)と、画面の結果を同じ入力で比べる。
# 最後に done(照らした件数, 合わない件数) を呼ぶ。合わない件数が1以上なら終了コード1。
# ---- 申し送り(2026-11-19 15時の回。次の回は先に読む) ----
# ・リポジトリの直下の CLAUDE.md を毎回先に読む(説明文の誤りは Claude が直す。読みやすさは Grok Bot があとから書き直すので上書きして戻さない)。
# ・ページを作るスクリプト(tools/build2.py の kojin()・houjin()、tools/hj.py、tools/build_soneki.py)は古い版から作り直す形で、流すと今の直しが消える。流さずに HTML を直に直す。
# ・この日に見つかった誤りの形。まだ見ていないページで同じ形を必ず探す:
#   1 住民税の基礎控除を43万円で固定(合計所得2,400万円超は29万・15万・0円。2,500万円超は調整控除なし)。furusato・yakuin-tedori・houjinnari・kojin-zei で直した。同じ jumin() がほかのページにもある見込み
#   2 標準報酬月額の上の6等級の境目を隣の等級のまん中で出す(正しくは1,055,000・1,115,000・1,175,000・1,235,000・1,295,000・1,355,000円)。iryohi-kojo・nenmatsu-chosei で直した
#   3 小数の率や定数を掛けてから四捨五入・切り捨て(0.5円の所で1円ずれる)。整数で掛けて割る
#   4 子ども・子育て拠出金の四捨五入(原本は円未満切り捨て)と、会社負担=本人負担(原本は全額−本人負担)。houjinnari は未修正
#   5 所得金額調整控除(年収850万円超)・所得割の非課税の判定(35万円×人数+10万円+32万円)の抜け
#   6 出典のリンクの文字と着いたページの題名の違い(国税庁の令和8年度改正Q&A・協会けんぽ・大阪府。tools/regions.py の src にも同じ文字がある)
#   7 余った </span>・<trNone>・「はじめに戻す」で同じ値の別の選択肢が選ばれる・「近い行が黄色」の文と動きの違い
# ・1ページずつ係(Agent)に分けて8ページを同時に見ると1回で3巡(24ページ)進む。係には git と finish.py・gate.py を触らせない。
# ・この回は https://taxtable.jp/tt_status.txt を開けなかった(curl は403・WebFetch は許可待ちで時間切れ)。ver=33〜35 が本番に出たかは次の回が確かめる。
import os, sys, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.join(ROOT, 'site')

def url(slug):
    return 'file://' + os.path.join(SITE, slug, 'index.html')

def num(t):
    s = ''.join(ch for ch in t if ch.isdigit())
    v = int(s or 0)
    return -v if ('−' in t or t.strip().startswith('-')) else v

def done(n, bad):
    print('照らした %d 合わない %d' % (n, bad))
    sys.exit(1 if bad else 0)

def run(slug, body, width=390):
    """body(pg) は (照らした件数, 合わない件数) を返す async 関数。"""
    async def main():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page(viewport={'width': width, 'height': 800})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(url(slug))
            n, bad = await body(pg)
            await b.close()
            for e in errs:
                print('画面のエラー', e[:120]); bad += 1
            return n, bad
    n, bad = asyncio.run(main())
    done(n, bad)
