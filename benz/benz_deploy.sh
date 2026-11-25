#!/bin/sh
# benz-handbook.com : GitHub の benz ブランチの payload/*.json（関所の通行証付き）を WordPress に反映する
# エックスサーバーの Cron で10分おきに動かす。WordPress へのログインもパソコンも要らない。
T="$HOME/benz_deploy"
WP="$HOME/benz-handbook.com/public_html"
U="https://github.com/toshi-20260922/toshi-20260922.github.io/archive/refs/heads/benz.tar.gz"
[ -f "$WP/wp-load.php" ] || exit 1
mkdir -p "$T" || exit 1
if ! mkdir "$T/lock" 2>/dev/null; then
  find "$T/lock" -maxdepth 0 -mmin +30 -exec rmdir {} \; 2>/dev/null
  exit 0
fi
trap 'rmdir "$T/lock" 2>/dev/null' EXIT
rm -rf "$T/new"; mkdir -p "$T/new"
curl -sL --max-time 90 "$U" -o "$T/new.tgz" && tar xzf "$T/new.tgz" -C "$T/new" --strip-components=1 2>/dev/null
if [ -d "$T/new/benz/payload" ]; then
  /usr/bin/php8.2 "$T/new/benz/benz_apply.php" "$WP" "$T" "$T/new/benz/payload" >> "$T/log.txt" 2>&1 || php "$T/new/benz/benz_apply.php" "$WP" "$T" "$T/new/benz/payload" >> "$T/log.txt" 2>&1
else
  echo "$(date '+%Y-%m-%d %H:%M:%S') fetch failed or no payload" >> "$T/log.txt"
fi
{ echo "last run: $(date '+%Y-%m-%d %H:%M:%S')"; tail -n 40 "$T/log.txt"; } > "$WP/benz_status.txt"
