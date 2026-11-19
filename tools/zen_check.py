# 毎日の全ツール点検:tools/seikaku/ の突き合わせを全部流し、突き合わせがまだ無いページを数える。
# 使い方:リポジトリの直下で python3 tools/zen_check.py
# 最後の行が「全ツール点検 合わない 0 本 / 突き合わせの無いページ 0」なら全ページの計算が自分の計算と一致。
import glob, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'tools', 'seikaku')
PAGES = [p['path'].strip('/') for p in json.load(open(os.path.join(ROOT, 'tools', 'pages.json'), encoding='utf-8'))]
have = {os.path.basename(f)[:-3] for f in glob.glob(os.path.join(D, '*.py')) if not os.path.basename(f).startswith('_')}
def covered(slug):
    if slug in have: return slug
    if slug.startswith('saitei-chingin') and 'saitei' in have: return 'saitei'
    return None
ng = []
for name in sorted(have):
    r = subprocess.run([sys.executable, os.path.join(D, name + '.py')], capture_output=True, text=True, timeout=1200)
    last = (r.stdout.strip().splitlines() or ['出力なし'])[-1]
    print('%-28s %s' % (name, last))
    if r.returncode != 0:
        ng.append(name)
        for l in (r.stdout + r.stderr).strip().splitlines()[-15:]:
            print('   ', l)
nai = [s for s in PAGES if not covered(s)]
for s in nai:
    print('突き合わせなし', '/' + s + '/')
print('全ツール点検 合わない %d 本 / 突き合わせの無いページ %d' % (len(ng), len(nai)))
sys.exit(1 if ng else 0)
