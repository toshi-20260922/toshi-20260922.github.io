# 令和8年度の国民健康保険料率。23地域の値は tools/rates.json の kokuho。
# p = [医療, 支援, 介護, 子ども] 各 [所得割(%x100), 均等割(18歳以上1人), 平等割(1世帯), 上限]
# 協会けんぽの都道府県の率（PREF）はここには残す。静岡市は足していない。
import json, os
def _kokuho_reg():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rates.json')
    rows = json.load(open(path, encoding='utf-8'))['kokuho']['rows']
    out = []
    for r in rows:
        p = [[x['shotoku'], x['kinto'], x['byodo'], x['cap']] for x in r['parts']]
        d = dict(n=r['name'], p=p, r=r['r'], nag=r['nag'], url=r['url'], src=r['src'])
        d['s'] = r['short']
        out.append(d)
    return out
REG = _kokuho_reg()
SHORT = [r['s'] for r in REG]
assert len(REG) == 23 and SHORT == ['東京23区','目黒区','中野区','江戸川区','札幌市','仙台市','さいたま市','千葉市','横浜市','川崎市','相模原市','新潟市','浜松市','名古屋市','京都市','大阪市・堺市','神戸市','岡山市','広島市','北九州市','福岡市','熊本市','奈良県']
PREF=[('北海道',1028),('青森県',985),('岩手県',951),('宮城県',1010),('秋田県',1001),('山形県',975),('福島県',950),('茨城県',952),('栃木県',982),('群馬県',968),('埼玉県',967),('千葉県',973),('東京都',985),('神奈川県',992),('新潟県',921),('富山県',959),('石川県',970),('福井県',971),('山梨県',955),('長野県',963),('岐阜県',980),('静岡県',961),('愛知県',993),('三重県',977),('滋賀県',988),('京都府',989),('大阪府',1013),('兵庫県',1012),('奈良県',991),('和歌山県',1006),('鳥取県',986),('島根県',994),('岡山県',1005),('広島県',978),('山口県',1015),('徳島県',1024),('香川県',1002),('愛媛県',998),('高知県',1005),('福岡県',1011),('佐賀県',1055),('長崎県',1006),('熊本県',1008),('大分県',1008),('宮崎県',977),('鹿児島県',1013),('沖縄県',944)]
def kyuyo7(x):
    if x<651000:return 0
    if x<1900000:return x-650000
    if x<6600000:
        A=x//4000*4000
        return A*7//10-80000 if x<3600000 else A*8//10-440000
    if x<8500000:return x*9//10-1100000
    return x-1950000
def kokuho(R,g,meOld,fam,famOld):
    n=1+fam;base=max(0,g-430000)
    red=7 if g<=430000 else (5 if g<=430000+310000*n else (2 if g<=430000+570000*n else 0))
    parts=[]
    for i,c in enumerate(R['p']):
        cnt=((1 if meOld else 0)+famOld) if i==2 else n
        ib=(base if meOld else 0) if i==2 else base
        if cnt==0: parts.append(0);continue
        v=ib*c[0]//10000+cnt*(c[1]*(10-red)//10)+c[2]*(10-red)//10
        if R['nag'] and i==0 and red>0: v=max(0,v-2000*cnt)
        v=v//R['r']*R['r']
        parts.append(min(c[3],v))
    return sum(parts),parts,red
if __name__=='__main__':
    import json
    # 公式の計算例との照らし合わせ
    ng=[r for r in REG if r['s']=='名古屋市'][0]
    print('名古屋 20歳単身 所得0 →',kokuho(ng,0,0,0,0),'公式 18,450')
    ni=[r for r in REG if r['s']=='新潟市'][0]
    t,p,_=kokuho(ni,2370000,1,1,0)
    print('新潟 44歳+38歳 所得237万 →',p,'公式 医療206,800(3人) 支援90,700(3人) 介護62,600')
    kw=[r for r in REG if r['s']=='川崎市'][0]
    print('川崎 均等割 医療3人',3*43261,'支援',3*15306,'子ども2人',2*1742,'公式 129,783 / 45,918 / 3,330+154')
    for r in REG:
        t,p,_=kokuho(r,kyuyo7(4000000),0,0,0);t2,_,_=kokuho(r,kyuyo7(4000000),1,0,0)
        print(r['s'],t,t2)
