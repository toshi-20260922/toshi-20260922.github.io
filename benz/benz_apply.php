<?php
// 関所（gate.py pass）が出した荷物だけを WordPress に反映する。
// 引数：WordPressの場所 作業フォルダ 荷物のフォルダ
[$self, $wpdir, $work, $dir] = $argv;
define('WP_USE_THEMES', false);
require $wpdir . '/wp-load.php';
$done_file = "$work/applied.txt";
$done = file_exists($done_file) ? array_filter(explode("\n", file_get_contents($done_file))) : [];
$now = date('Y-m-d H:i:s');
foreach (glob("$dir/*.json") as $f) {
  $p = json_decode(file_get_contents($f), true);
  $tok = $p['通行証'] ?? '';
  if (!preg_match('/^[0-9a-f]{24}$/', $tok)) { echo "$now 通行証が無い荷物は送らない：" . basename($f) . "\n"; continue; }
  if (in_array($tok, $done, true)) continue;
  if (empty($p['meta_description'])) { echo "$now メタディスクリプションが無い荷物は送らない：$tok\n"; continue; }
  // 荷物の中身が関所の通行証と合っているか（本文・題名・メタから作り直して比べる）
  $check = substr(hash('sha256', ($p['body_sha256'] ?? '') . $p['content'] . $p['title'] . $p['meta_description']), 0, 24);
  if ($check !== $tok) { echo "$now 通行証と中身が合わない：$tok\n"; continue; }
  $post = ['post_title' => $p['title'], 'post_content' => $p['content'],
           'post_status' => in_array($p['status'] ?? 'draft', ['draft', 'publish'], true) ? $p['status'] : 'draft'];
  if (!empty($p['post_id'])) {
    $old = get_post((int)$p['post_id']);
    if (!$old || $old->post_type !== 'post') { echo "$now 更新先の投稿が無い：{$p['post_id']}\n"; continue; }
    // 上書きの前に今の本文を控える
    @mkdir("$work/backup", 0700, true);
    file_put_contents("$work/backup/{$p['post_id']}_" . date('Ymd_His') . ".html", $old->post_content);
    $post['ID'] = (int)$p['post_id'];
    $id = wp_update_post(wp_slash($post), true);
  } else {
    $post['post_name'] = $p['slug'] ?? '';
    $id = wp_insert_post(wp_slash($post), true);
  }
  if (is_wp_error($id)) { echo "$now 失敗：$tok " . $id->get_error_message() . "\n"; continue; }
  update_post_meta($id, 'ssp_meta_description', $p['meta_description']);
  if (!empty($p['featured_media'])) set_post_thumbnail($id, (int)$p['featured_media']);
  file_put_contents($done_file, "$tok\n", FILE_APPEND);
  echo "$now 反映：ID $id {$post['post_status']} 通行証 $tok\n";
}
