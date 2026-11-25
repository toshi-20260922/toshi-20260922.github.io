# benz ブランチ（ベンツ完全ガイドの記事の受け渡し）
- benz/payload/*.json：関所（gate.py pass）が出した通行証付きの記事のデータ
- エックスサーバーの Cron が benz_deploy.sh を10分おきに動かし、benz_apply.php が通行証を照らし合わせて WordPress に反映する
- 通行証の無いデータ・中身と通行証が合わないデータは反映しない
