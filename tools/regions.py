# 令和8年度の国民健康保険料率(各自治体の公式ページ 2026/11/16 確認)
# p = [医療, 支援, 介護, 子ども] 各 [所得割(%x100), 均等割(18歳以上1人), 平等割(1世帯), 上限]
def R(name, med, shi, kai, kod, cap0=670000, r=1, nag=0, url='', src=''):
    caps=[cap0,260000,170000,30000]
    return dict(n=name,p=[list(x)+[caps[i]] for i,x in enumerate([med,shi,kai,kod])],r=r,nag=nag,url=url,src=src)
TK='https://www.hokeniryo.metro.tokyo.lg.jp/documents/d/hokeniryo/tokubetuku202605-pdf'
TKS='東京都保健医療局「特別区の国民健康保険料一覧表（令和8年度）」'
REG=[
 R('東京23区（目黒区・中野区・江戸川区を除く20区）',(751,47600,0),(280,17600,0),(243,17800,0),(27,1873,0),url=TK,src=TKS),
 R('目黒区',(751,47600,0),(280,17600,0),(235,17800,0),(27,1873,0),url=TK,src=TKS),
 R('中野区',(803,47100,0),(294,17400,0),(253,17700,0),(27,1873,0),url=TK,src=TKS),
 R('江戸川区',(783,48900,0),(284,17400,0),(245,17400,0),(27,1870,0),url=TK,src=TKS),
 R('札幌市',(861,20550,32540),(256,6330,10010),(233,6020,7550),(29,1100,1000),r=10,url='https://www.city.sapporo.jp/hoken-iryo/kokuho/fuka.html',src='札幌市「国民健康保険料の決め方」'),
 R('仙台市',(796,27850,26700),(300,10410,9980),(244,9440,7070),(27,1010,900),url='https://www.city.sendai.jp/kenko-hoken/kurashi/tetsuzuki/kokumin/kenkohoken/hokenryo.html',src='仙台市「国民健康保険料」'),
 R('さいたま市',(764,43300,0),(273,14900,0),(237,16100,0),(26,1700,0),r=100,url='https://www.city.saitama.lg.jp/001/153/002/004/p010020.html',src='さいたま市「国民健康保険税の税率」'),
 R('千葉市',(721,23280,26640),(285,8880,10320),(257,16560,0),(31,1800,0),url='https://www.city.chiba.jp/hokenfukushi/iryoeisei/hoken/hokenryou-ketteishimashita.html',src='千葉市「令和8年度国民健康保険料率の決定」'),
 R('横浜市',(833,40870,0),(262,13380,0),(284,16200,0),(34,1770,0),url='https://www.city.yokohama.lg.jp/kurashi/koseki-zei-hoken/kokuho/hokenryo/r7hokennryouritu.html',src='横浜市「令和8年度保険料の料率等について」'),
 R('川崎市',(826,43261,0),(289,15306,0),(267,15828,0),(32,1742,0),url='https://www.city.kawasaki.jp/350/page/0000187752.html',src='川崎市「令和8年度の国民健康保険料について」'),
 R('相模原市',(675,29000,18000),(278,11500,7000),(232,12000,6000),(28,1360,800),url='https://www.city.sagamihara.kanagawa.jp/kurashi/1026448/kokuho/1007820/1007822.html',src='相模原市「令和8年度 国民健康保険税の税率等について」'),
 R('新潟市',(740,14700,19200),(310,7200,9000),(250,14100,0),(27,1600,0),r=100,url='https://www.city.niigata.lg.jp/kurashi/hoken/kokuho/hokenryo/henko.html',src='新潟市「令和8年度の国民健康保険料率と軽減判定所得について」'),
 R('浜松市',(720,25000,22000),(235,11000,8000),(190,14500,0),(33,2000,0),url='https://www.city.hamamatsu.shizuoka.jp/kokuho/kokuho_nenkin/kokuho/hokenryou.html',src='浜松市「国民健康保険料」'),
 R('名古屋市',(883,50591,0),(258,15784,0),(234,16120,0),(26,1863,0),r=10,nag=1,url='https://www.city.nagoya.jp/kurashi/hoken/1011736/1011793/1011794/1011799.html',src='名古屋市「令和8年度分の国民健康保険料」'),
 R('京都市',(794,30080,17930),(266,10360,6180),(251,11090,5370),(28,1170,660),url='https://www.city.kyoto.lg.jp/hokenfukushi/page/0000351039.html',src='京都市「令和8年度の保険料の計算方法について」'),
 R('大阪市・堺市（大阪府内は全市町村で同じ）',(950,34990,33908),(306,11191,10845),(260,18682,0),(28,1841,0),cap0=660000,url='https://www.pref.osaka.lg.jp/o100080/kokuho/iryouseido/hokenryouritsu/hokenryouritsu2.html',src='大阪府「令和8年度の府内統一保険料率」'),
 R('神戸市',(738,33700,21800),(297,13510,8740),(278,13970,6880),(26,1330,830),url='https://www.city.kobe.lg.jp/a52670/kurashi/support/insurance/gaku.html',src='神戸市「国民健康保険料の計算方法」'),
 R('岡山市',(815,28320,20880),(295,10320,6960),(260,10920,5280),(29,1200,720),url='https://www.city.okayama.jp/kurashi/0000011518.html',src='岡山市「令和8年度国民健康保険料率」'),
 R('広島市',(818,31228,30403),(264,10342,10069),(252,10443,7860),(27,1128,1044),url='https://www.city.hiroshima.lg.jp/living/hoken-nenkin/1021143/1025566/1003464.html',src='広島市「国民健康保険料の計算方法」'),
 R('北九州市',(831,23200,26400),(340,9720,11060),(290,9550,8220),(28,930,1000),url='https://www.city.kitakyushu.lg.jp/contents/924_10079.html',src='北九州市「国民健康保険料の計算方法」'),
 R('福岡市',(558,19807,18664),(314,10441,9838),(261,10160,7751),(28,1039,911),url='https://www.city.fukuoka.lg.jp/hofuku/kokuho/hp/seido/06-02.html',src='福岡市「国民健康保険料の計算方法」'),
 R('熊本市',(634,28400,18100),(298,13300,8500),(294,20300,0),(25,1700,0),url='https://www.city.kumamoto.jp/kiji003426/index.html',src='熊本市「令和8年度 熊本市国民健康保険料率」'),
]
SHORT=['東京23区','目黒区','中野区','江戸川区','札幌市','仙台市','さいたま市','千葉市','横浜市','川崎市','相模原市','新潟市','浜松市','名古屋市','京都市','大阪市・堺市','神戸市','岡山市','広島市','北九州市','福岡市','熊本市']
for r,s in zip(REG,SHORT): r['s']=s
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
        v=ib*c[0]//10000+c[1]*cnt*(10-red)//10+c[2]*(10-red)//10
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
