#!/bin/sh
# taxtable.jp : GitHub の taxtable ブランチの site/ を public_html に反映する(消さない・上書き前に控えを取る)
T="$HOME/tt"
S="$HOME/taxtable.jp/public_html"
U="https://github.com/toshi-20260922/toshi-20260922.github.io/archive/refs/heads/taxtable.tar.gz"
[ -d "$S" ] || exit 1
mkdir -p "$T" || exit 1
if ! mkdir "$T/lock" 2>/dev/null; then
  find "$T/lock" -maxdepth 0 -mmin +30 -exec rmdir {} \; 2>/dev/null
  exit 0
fi
trap 'rmdir "$T/lock" 2>/dev/null' EXIT
now=$(date '+%Y-%m-%d %H:%M:%S')
stamp=$(date '+%Y%m%d_%H%M%S')
log(){ echo "$now $*" >> "$T/log.txt"; }
rm -rf "$T/new"; mkdir -p "$T/new"
curl -sL --max-time 90 "$U" -o "$T/new.tgz" && tar xzf "$T/new.tgz" -C "$T/new" --strip-components=1 2>/dev/null
if [ ! -f "$T/new/deploy.sh" ]; then
  log "fetch failed"
else
  ver=$(cat "$T/new/VERSION" 2>/dev/null)
  if [ -d "$T/new/site" ]; then
    cd "$T/new/site" || exit 1
    find . -type f | while IFS= read -r f; do
      f=${f#./}
      case "$f" in *..*|wp-*|*.php|.ht*|*/.ht*) continue;; esac
      if [ ! -f "$S/$f" ] || ! cmp -s "$f" "$S/$f"; then
        d=$(dirname "$f")
        if [ -f "$S/$f" ]; then mkdir -p "$T/backup/$stamp/$d"; cp -p "$S/$f" "$T/backup/$stamp/$f"; fi
        mkdir -p "$S/$d"
        if cp "$f" "$S/$f.tt_tmp" && mv "$S/$f.tt_tmp" "$S/$f"; then chmod 644 "$S/$f"; log "deployed $f (ver $ver)"; else log "FAILED $f"; fi
      fi
    done
  fi
  echo "$now ok ver=$ver" > "$T/last.txt"
fi
{ echo "last run: $now"; cat "$T/last.txt" 2>/dev/null; echo "--- log (last 40) ---"; tail -n 40 "$T/log.txt" 2>/dev/null; } > "$S/tt_status.txt"
