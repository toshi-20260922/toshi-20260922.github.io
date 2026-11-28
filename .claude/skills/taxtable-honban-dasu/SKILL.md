---
name: taxtable-honban-dasu
description: タックステーブル(taxtable.jp)で何かを直したら毎回使う。本番に出す道は「toshi-20260922.github.io の taxtable の枝に push → 10分おきに自動で本番」の1つだけ。新しい入れ物・鍵・自動の仕組みを作りたくなったときと、できないことに当たったときも手を動かす前に必ず使う。
---

# タックステーブルを本番に出す

## 本番に出す道は1つだけ

- GitHub の **toshi-20260922/toshi-20260922.github.io** の **taxtable の枝** の site/ に入れる
- エックスサーバーの Cron が10分おきにその枝を読み、違うファイルを本番(public_html)に上書きする(2026-11-16 に本人が設定)
- 本番に出たかは https://taxtable.jp/tt_status.txt の ver= の数字で見る
- 新しいリポジトリ・GitHub Actions・SSH の鍵・エックスサーバーのファイル管理は使わない。本人に鍵やログインを頼まない

## 作業の始め方(毎回この順)

1. add_repo で toshi-20260922/toshi-20260922.github.io を access=push でつなぐ
2. 既定の枝ではなく taxtable の枝を取る:`git fetch --depth=50 origin taxtable` → `git worktree add <作業場所> FETCH_HEAD`
3. 作業はこの作業場所の中だけでする。CLAUDE.md と VERSION を読む

## 出す手順(毎回すべて)

1. 直したファイルを site/ に入れる
2. `python3 tools/finish.py` → `python3 tools/gate.py`。最後の行が「問題 0 件」でなければ出さない
3. VERSION の数字を1つ上げる
4. push の直前に `git fetch --depth=50 origin taxtable` をして、ほかのチャット(Claude.ai の予約)が先に入れた分があれば重ねる
5. `git push origin HEAD:taxtable`
6. tt_status.txt に新しい ver= が出るまで見張る(10分ほど)
7. 直したページを本番から取り、手元のファイルと1文字も違わないかを比べる
8. 本番のページをスマホ幅とパソコン幅で開き、直した所を実際に操作して確かめる
9. Search Console のインデックス登録のリクエストは taxtable-koukai の手順でやる

## グルグル回らないための決まり

- 新しい仕組み(入れ物・鍵・自動化)を作りたくなったら、作る前に docs/ と CLAUDE.md を「公開」「Cron」「push」「本番」で検索する。今ある仕組みが見つかったら、それを使う
- できないこと(権限が無い・403 など)に当たったら、その手番で本人に1行で言う。黙って別の道を作り始めない
- 同じ失敗が2回続いたら、手を変えて試し続けない。止めて何が起きたかを本人に言う
- 「本番は変えていません」と書いて終わらない。直したものは、その日のうちに上の手順で本番に出す

## 起きたこと(2026-11-27〜28・繰り返さない)

- 資料(docs/taxtable_vps_daily.md の「公開のやり方が変わった」)を読まずに、新しいリポジトリ toshi-20260922/taxtable を作った
- 本番に出す道が無いと思い込み、直したものを「本番は変えていません」のまま何時間も置いた
- GitHub Actions と鍵の仕組みを作り、本人にエックスサーバーの鍵の作業を頼んだ。全部要らなかった
- 夜中のあいだ、関所の待ちと 403 のやり直しを繰り返した。taxtable の枝に push したら10分で本番に出た
