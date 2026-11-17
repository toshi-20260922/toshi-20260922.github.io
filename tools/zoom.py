import subprocess
from PIL import Image,ImageDraw,ImageFont
T='/root/.claude/projects/-home-claude/1402f227-0341-5818-a430-e59d3713da02/tool-results/mcp-remote-devices-blob-'
FS=[f.split(':')[0] for f in subprocess.check_output(['fc-list',':lang=ja','file']).decode().split('\n') if 'NotoSansCJK' in f]
B=ImageFont.truetype([f for f in FS if 'Bold' in f][0],30);R=ImageFont.truetype([f for f in FS if 'Regular' in f or 'DemiLight' in f or 'Medium' in f][0],25)
H=ImageFont.truetype([f for f in FS if 'Bold' in f][0],40)
COL={'プロゴ':'#b03030','経営サポートプラスアルファ':'#1d3a8a','うち':'#00775a'}
def img(src):return Image.open(T+src+'.jpg' if not src.endswith('.png') else src).convert('RGB')
def wrap(d,text,font,w):
    out=[]
    for para in text.split('\n'):
        line=''
        for ch in para:
            if d.textlength(line+ch,font=font)>w:out.append(line);line=ch
            else:line+=ch
        out.append(line)
    return out
def sheet(out,title,items):
    CW,TW=620,820;rows=[]
    tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
    for n,(who,src,box,head,lines) in enumerate(items,1):
        c=img(src).crop(box);c=c.resize((CW,int(c.height*CW/c.width)))
        if c.height>760:c=c.resize((int(c.width*760/c.height),760))
        txt=[]
        for lab,body in lines:txt.append((lab,wrap(tmp,body,R,TW-30)))
        th=60+sum(40+len(b)*36+14 for _,b in txt)
        rows.append((n,who,c,head,txt,max(c.height+60,th)+30))
    Ht=90+sum(r[5] for r in rows);W=CW+TW+80
    im=Image.new('RGB',(W,Ht),'#ffffff');d=ImageDraw.Draw(im);d.text((24,22),title,font=H,fill='#222222');y=90
    for n,who,c,head,txt,h in rows:
        d.line([(0,y),(W,y)],fill='#dddddd',width=2)
        d.ellipse([20,y+14,64,y+58],fill=COL[who]);d.text((34 if n<10 else 26,y+16),str(n),font=B,fill='#ffffff')
        d.text((76,y+18),who,font=B,fill=COL[who])
        im.paste(c,(24,y+64));d.rectangle([22,y+62,24+c.width+1,y+64+c.height+1],outline=COL[who],width=4)
        x=CW+56;ty=y+18;d.text((x,ty),head,font=B,fill='#222222');ty+=52
        for lab,body in txt:
            d.text((x,ty),lab,font=B,fill={'意味':'#555555','使いやすい理由':'#8a5a00','うちは':'#00775a'}.get(lab,'#333333'));ty+=40
            for l in body:d.text((x+10,ty),l,font=R,fill='#2d3a3a');ty+=36
            ty+=14
        y+=h
    im.save(out);print(out,im.size)
