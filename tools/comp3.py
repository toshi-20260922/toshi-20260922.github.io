import sys,subprocess
from PIL import Image,ImageDraw,ImageFont
T='/root/.claude/projects/-home-claude/1402f227-0341-5818-a430-e59d3713da02/tool-results/mcp-remote-devices-blob-'
FONT=[f for f in subprocess.check_output(['fc-list',':lang=ja','file']).decode().split('\n') if 'Sans' in f][0].split(':')[0]
F=ImageFont.truetype(FONT,30);G=ImageFont.truetype(FONT,22)
W=750
def norm(im):im=im.convert('RGB');return im.resize((W,int(im.height*W/im.width)))
def stack(fs):
    ims=[norm(Image.open(T+f+'.jpg')) for f in fs];h=sum(i.height for i in ims)+12*(len(ims)-1)
    c=Image.new('RGB',(W,h),'#888');y=0
    for i in ims:c.paste(i,(0,y));y+=i.height+12
    return c
def make(out,cols):
    # cols: [(名前,色,URL,画像 or None)]
    ims=[c[3] for c in cols];h=max([i.height for i in ims if i] or [600])+100
    c=Image.new('RGB',(W*3+40,h),'#ffffff');d=ImageDraw.Draw(c)
    for k,(n,col,u,im) in enumerate(cols):
        x=k*(W+20);d.text((x+10,8),n,font=F,fill=col);d.text((x+10,52),u,font=G,fill='#555555')
        if im:c.paste(im,(x,100))
        else:d.rectangle([x,100,x+W,700],fill='#f2f2f2');d.text((x+40,380),'同じ題材のページはありません',font=F,fill='#777777')
    c.save(out);print(out,c.size)
if __name__=='__main__':
    make('hk3_zoyozei.png',[('プロゴ','#b03030','progo-tax.com/zoyozei-hayami/',stack(['1794894120307-arm4ze','1794894130312-lpi5dg'])),
     ('経営サポートプラスアルファ','#1d3a8a','keiei-support-plus-a.com/zeirishi-hiyou/zouyozei-keisan-simulation/',stack(['1794896938819-e2kzd5','1794896953992-duc2jf'])),
     ('うち（taxtable.jp）','#00775a','taxtable.jp/zoyozei/',norm(Image.open('o_zoyozei.png')))])
