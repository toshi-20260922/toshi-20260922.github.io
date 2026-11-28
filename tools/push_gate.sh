#!/bin/bash
# 公開の関所。push の前に必ず通す。1つでも引っかかったら止める。
# Claude Code の hooks(.claude/settings.json)と git の pre-push の両方から呼ばれる。
cd "$(git rev-parse --show-toplevel)" || exit 2
python3 tools/finish.py >/dev/null 2>&1 || { echo "止めました: finish.py が失敗しました" >&2; exit 2; }
if [ -n "$(git status --porcelain -- site tools | grep -v "site/gate_ok.txt")" ]; then
  echo "止めました: finish.py が書き換えたファイル、またはコミットしていない変更があります。" >&2
  git status --short -- site tools | grep -v "site/gate_ok.txt" >&2
  exit 2
fi
OUT=$(python3 tools/gate.py 2>&1)
LAST=$(printf '%s\n' "$OUT" | tail -1)
if [ "$LAST" != "問題 0 件" ]; then
  echo "止めました: gate.py の結果が「問題 0 件」ではありません。" >&2
  printf '%s\n' "$OUT" | grep -v '^報告' | tail -40 >&2
  exit 2
fi
git checkout -q -- site/gate_ok.txt 2>/dev/null
echo "関所を通過: 問題 0 件" >&2
exit 0
