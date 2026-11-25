# 早見表の上の「下で選んだ…」をやめ、表の条件をその場で書く(表の上だけ読めば分かる形)
import re
def opt(i): return 'var e=document.getElementById("%s");return e.options[e.selectedIndex].text.replace(/（[^）]*）/,"");'%i
def num(i): return 'var v=String(document.getElementById("%s").value).replace(/[^0-9.]/g,"");return Number(v).toLocaleString("ja-JP");'%i
def seg(i): return 'var b=document.querySelector("#%s .on");return b?b.textContent:"";'%i
P={
 'hensai':('<p>下で入力した条件で、借りてからの1年ごとに表示しています。</p>',
   '"借りる額"+A()+"円・年利"+B()+"%・"+C()+"返済（据置"+E()+"）・"+D()+"の場合です。"',
   [num('amt'),'return document.getElementById("rate").value;',opt('yr'),seg('s-m'),opt('suem')]),
 'hoteifukurihi':('<p>下で選んだ都道府県で、1人だけを雇っている場合の1か月の額です。</p>',
   'A()+"で1人だけを雇っている場合の1か月の額です。"',[opt('pref')]),
 'soneki-bunkiten':('<p>下で入力した数字で、変動費率と固定費が変わらない場合の利益です。</p>',
   '"売上高"+A()+"円・変動費"+B()+"円・固定費"+C()+"円で、変動費率と固定費が変わらない場合の利益です。"',[num('sal'),num('vc'),num('fc')]),
 'yatou-hiyou':('<p>下で選んだ都道府県と年齢の条件で、賞与なしで計算しています。</p>',
   'A()+"・"+B()+"・賞与なしで計算しています。"',[opt('pref'),seg('s-age')]),
}
for d,(old,expr,fs) in P.items():
    p='site/%s/index.html'%d; s=open(p).read()
    s=re.sub(r'<script id="tcapj">.*?</script>','',s,flags=re.S)
    if old in s: s=s.replace(old,'<p class="cap" id="t-cap2"></p>')
    assert 'id="t-cap2"' in s,d
    fn=''.join('function %s(){try{%s}catch(x){return ""}}'%(n,f) for n,f in zip('ABCDE',fs))
    js=('<script id="tcapj">(function(){%sfunction u(){document.getElementById("t-cap2").textContent=%s;}'
        'u();document.addEventListener("input",function(){setTimeout(u,0)},true);document.addEventListener("change",function(){setTimeout(u,0)},true);'
        'document.addEventListener("click",function(){setTimeout(u,0)},true);})();</script>')%(fn,expr)
    s=s.replace('</body>',js+'</body>',1); open(p,'w').write(s); print(d)
