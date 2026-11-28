# 国保のページの「住んでいる市区町村」の欄を「都道府県→市区町村」の2段にする。
# 使い方: python3 tools/muni_page.py site/kokuho-keisan/index.html
# - var RG=[...] に tools/rates.json の地域で足りないものを後ろに足す(n,s,p,r,g,f の形)
# - <select id="reg"> の欄を、都道府県の欄(#pref-m)と市区町村の欄(#reg)に替える。#reg の値は今までどおり RG の番号か x
# - 都道府県を選ぶと #reg の中身を作り直す script#munij を置く
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from regions import REG, PREF
from muni import MUNI, PREF47

def rg_entry(r):
    pn = [p for p, _ in PREF]
    return dict(n=r['n'], s=r['s'], p=r['p'], r=r['r'], g=r['nag'], f=pn.index(r_pref(r)))

def r_pref(r):
    for p, n, s in MUNI:
        if s == r['s']:
            return p
    raise SystemExit('都道府県が分からない地域: ' + r['s'])

def main(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'var RG=(\[.*?\]);', s)
    rg = json.loads(m.group(1))
    have = [x['s'] for x in rg]
    for r in REG:
        if r['s'] not in have:
            rg.append(rg_entry(r))
    assert [x['s'] for x in rg] == [r['s'] for r in REG], '並びが regions.py と違う'
    s = s[:m.start()] + 'var RG=' + json.dumps(rg, ensure_ascii=False, separators=(',', ':')) + ';' + s[m.end():]
    idx = {x['s']: i for i, x in enumerate(rg)}
    mu = {}
    for p, n, sh in MUNI:
        mu.setdefault(p, []).append([n, idx[sh]])
    X = '一覧にない市区町村（料率を入力する）'
    pref_opt = ''.join('<option%s>%s</option>' % (' selected' if p == '東京都' else '', p) for p in PREF47)
    tk = ''.join('<option value="%d">%s</option>' % (i, n) for n, i in mu['東京都']) + '<option value="x">%s</option>' % X
    old = re.search(r'<div class="full">\s*<label for="reg">([^<]*)</label>\s*<select id="reg">.*?</select>\s*</div>', s, re.S)
    if old:
        new = ('<div>\n   <label for="pref-m">都道府県</label>\n   <select id="pref-m">%s</select>\n  </div>\n'
               '  <div>\n   <label for="reg">%s</label>\n   <select id="reg">%s</select>\n  </div>') % (pref_opt, old.group(1), tk)
        s = s[:old.start()] + new + s[old.end():]
    else:
        # 2回目からは中身だけ入れ替える
        s = re.sub(r'(<select id="pref-m">).*?(</select>)', lambda k: k.group(1) + pref_opt + k.group(2), s, count=1, flags=re.S)
        s = re.sub(r'(<select id="reg">).*?(</select>)', lambda k: k.group(1) + tk + k.group(2), s, count=1, flags=re.S)
    js = ('<script id="munij">(function(){var MU=%s,X=%s,pf=document.getElementById("pref-m"),rg=document.getElementById("reg");'
          'function fill(){var a=MU[pf.value]||[],h="";for(var i=0;i<a.length;i++)h+=\'<option value="\'+a[i][1]+\'">\'+a[i][0]+"</option>";'
          'h+=\'<option value="x">\'+X+"</option>";rg.innerHTML=h;rg.selectedIndex=0;rg.dispatchEvent(new Event("change"));}'
          'var MSG="料率を入力すると計算します。料率は市区町村のホームページか保険料の通知書に載っています。";'
          'function blank(){var c=document.querySelectorAll("#cust input"),e=1;for(var i=0;i<c.length;i++)if(c[i].value!=="")e=0;'
          'var on=rg.value==="x"&&e,calc=document.getElementById("calc"),ks=calc.children,vd=document.getElementById("vd");'
          'for(var i=0;i<ks.length;i++){var k=ks[i];if(k.classList.contains("amt")||k.classList.contains("ch")||k.tagName==="UL")k.style.display=on?"none":"";}'
          'var m=document.getElementById("munimsg");if(!m){m=document.createElement("p");m.id="munimsg";m.style.cssText="margin:12px 0 0;font-weight:700";'
          'm.textContent=MSG;(vd||document.getElementById("cust")).insertAdjacentElement(vd?"beforebegin":"afterend",m);}'
          'm.style.display=on?"":"none";if(vd)vd.style.display=on?"none":"";}'
          'pf.addEventListener("change",function(){fill();if(!MU[pf.value]){var c=document.querySelectorAll("#cust input");for(var i=0;i<c.length;i++)c[i].value="";'
          'document.getElementById("cust").dispatchEvent(new Event("input"));var kp=document.getElementById("pref");if(kp&&kp.options[pf.selectedIndex]&&kp.options[pf.selectedIndex].value===String(pf.selectedIndex)){kp.value=String(pf.selectedIndex);kp.dispatchEvent(new Event("change"));}}blank();});'
          'document.getElementById("cust").addEventListener("input",blank);rg.addEventListener("change",blank);})();</script>') % (json.dumps(mu, ensure_ascii=False, separators=(',', ':')), json.dumps(X, ensure_ascii=False))
    s = re.sub(r'<script id="munij">.*?</script>', '', s, flags=re.S)
    s = s.replace('</body>', js + '\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print(path, '地域', len(rg), '市区町村', len(MUNI))

if __name__ == '__main__':
    for p in sys.argv[1:]:
        main(p)
