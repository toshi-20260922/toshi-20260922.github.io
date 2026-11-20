# 最低賃金のページ(全国と公開済みの都道府県の全部)の突き合わせ。毎日の全ツール点検の saitei の回が使う。
# 原本:厚生労働省「令和8年度 地域別最低賃金 全国一覧」https://www.mhlw.go.jp/content/11200000/001753406.pdf
#      厚生労働省「令和8年度地域別最低賃金額答申状況」https://www.mhlw.go.jp/content/11302000/001745621.pdf
#      特定最低賃金は各労働局の発表(北海道 002868951.pdf・愛知 002888802.pdf・大阪 saitei.html・埼玉・福岡・兵庫・宮城・千葉・茨城・広島・熊本の労働局のページ)
# 最後に原本を確かめた日:2026-11-20
# 決まり:ページの JS を見ずに、下の NAT(原本から読んだ47都道府県)と TOKU(決定した特定最低賃金)から自分で最低ラインを出す。
#   最低ライン = その日に有効な地域別最低賃金 と その日に有効な特定最低賃金 の高い方。
#   時給・月給のちょうどと1円下を、発効日の前後の日付(Date を差し替え)で判定させて比べる。月給と日給の早見表の全行も比べる。
# 新しい県を公開したら SLUG に足す。特定最低賃金が決定したら TOKU に足す(答申だけのものは入れない)。
import os, sys, asyncio, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import url, done, num
from playwright.async_api import async_playwright
NAT = [('北海道', 1131, 1075, 10, 1), ('青森', 1090, 1029, 10, 29), ('岩手', 1090, 1031, 12, 1), ('宮城', 1098, 1038, 10, 1), ('秋田', 1090, 1031, 10, 14), ('山形', 1092, 1032, 10, 30), ('福島', 1094, 1033, 10, 16), ('茨城', 1136, 1074, 10, 18), ('栃木', 1125, 1068, 10, 1), ('群馬', 1120, 1063, 10, 3), ('埼玉', 1196, 1141, 10, 1), ('千葉', 1195, 1140, 10, 1), ('東京', 1280, 1226, 10, 1), ('神奈川', 1279, 1225, 10, 1), ('新潟', 1108, 1050, 10, 1), ('富山', 1119, 1062, 10, 1), ('石川', 1113, 1054, 10, 3), ('福井', 1112, 1053, 10, 4), ('山梨', 1113, 1052, 11, 1), ('長野', 1117, 1061, 10, 2), ('岐阜', 1121, 1065, 10, 1), ('静岡', 1154, 1097, 10, 15), ('愛知', 1195, 1140, 10, 1), ('三重', 1143, 1087, 10, 1), ('滋賀', 1136, 1080, 10, 3), ('京都', 1180, 1122, 11, 16), ('大阪', 1231, 1177, 10, 1), ('兵庫', 1172, 1116, 10, 1), ('奈良', 1107, 1051, 10, 4), ('和歌山', 1101, 1045, 10, 3), ('鳥取', 1090, 1030, 10, 3), ('島根', 1092, 1033, 10, 10), ('岡山', 1104, 1047, 10, 2), ('広島', 1141, 1085, 10, 11), ('山口', 1101, 1043, 10, 8), ('徳島', 1103, 1046, 11, 1), ('香川', 1092, 1036, 10, 1), ('愛媛', 1093, 1033, 11, 1), ('高知', 1086, 1023, 10, 29), ('福岡', 1114, 1057, 10, 4), ('佐賀', 1095, 1030, 11, 15), ('長崎', 1087, 1031, 11, 2), ('熊本', 1092, 1034, 12, 1), ('大分', 1096, 1035, 11, 1), ('宮崎', 1085, 1023, 10, 24), ('鹿児島', 1090, 1026, 10, 25), ('沖縄', 1086, 1023, 12, 2)]
SLUG = {'osaka': '大阪', 'tokyo': '東京', 'kanagawa': '神奈川', 'aichi': '愛知', 'hokkaido': '北海道', 'saitama': '埼玉', 'fukuoka': '福岡', 'chiba': '千葉',
        'hyogo': '兵庫', 'kyoto': '京都', 'okinawa': '沖縄', 'kumamoto': '熊本', 'ibaraki': '茨城', 'hiroshima': '広島', 'kagoshima': '鹿児島', 'mie': '三重',
        'shizuoka': '静岡', 'miyagi': '宮城', 'niigata': '新潟', 'nagano': '長野'}
A = '2025-01-01'  # いまの額(発効済み)
# 県: [(業種の名前の一部, [(この日から, 額), ...])]
TOKU = {
 'hokkaido': [('鉄鋼業', [(A, 1165), ('2026-12-01', 1221)]), ('処理牛乳', [(A, 1113), ('2026-12-01', 1160)]), ('電子部品', [(A, 1116), ('2026-12-01', 1174)]), ('船舶', [(A, 1105), ('2026-12-01', 1162)])],
 'aichi': [('輸送用機械', [(A, 1146), ('2026-12-16', 1208)]), ('製鉄業', [(A, 1175), ('2027-01-01', 1230)])],
 'osaka': [('塗料', [(A, 1191), ('2026-12-01', 1245)]), ('鉄鋼業', [(A, 1185), ('2026-12-01', 1240)]), ('非鉄金属', [(A, 1180), ('2026-12-01', 1235)]), ('はん用', [(A, 1197), ('2026-12-01', 1258)]),
           ('電子部品', [(A, 1197), ('2026-12-01', 1258)]), ('自動車・同附属品', [(A, 1194), ('2026-12-01', 1256)]), ('自動車小売業', [(A, 993), ('2026-12-17', 1232)])],
 'saitama': [('非鉄金属', [(A, 1161), ('2026-12-01', 1216)]), ('光学機械', [(A, 1177), ('2026-12-01', 1232)]), ('電子部品', [(A, 1168), ('2026-12-01', 1223)]), ('輸送用機械', [(A, 1165), ('2026-12-01', 1224)]), ('自動車小売業', [(A, 1152), ('2026-12-01', 1207)])],
 'fukuoka': [('製鉄業', [(A, 1176), ('2026-12-10', 1238)]), ('電子部品', [(A, 1137), ('2026-12-10', 1195)]), ('輸送用機械', [(A, 1147), ('2026-12-10', 1205)]), ('自動車（新車）小売業', [(A, 1131), ('2026-12-10', 1185)])],
 'hyogo': [('塗料', [(A, 1158), ('2026-12-01', 1199)]), ('鉄鋼業', [(A, 1180), ('2026-12-01', 1231)]), ('はん用', [(A, 1150), ('2026-12-01', 1206)]), ('電子部品', [(A, 1117), ('2026-12-01', 1173)]),
           ('輸送用機械', [(A, 1188), ('2026-12-01', 1243)]), ('計量器', [(A, 1117), ('2026-12-01', 1173)])],
 'miyagi': [('鉄鋼業', [(A, 1125), ('2026-12-15', 1187)]), ('電子部品', [(A, 1077), ('2026-12-15', 1138)]), ('自動車小売業', [(A, 1101), ('2026-12-15', 1161)])],
 'chiba': [('鉄鋼業', [(A, 1210)])], 'ibaraki': [('鉄鋼業', [(A, 1166)])], 'hiroshima': [('製鉄業', [(A, 1179)])],
 'kumamoto': [('電子部品', [(A, 1063)]), ('自動車・同附属品', [(A, 1074)])],
}
DAYS = ['2026-11-15', '2026-11-20', '2026-11-30', '2026-12-01', '2026-12-02', '2026-12-09', '2026-12-10', '2026-12-14', '2026-12-15', '2026-12-16', '2026-12-17', '2026-12-31', '2027-01-01']
INIT = "(()=>{const T=new Date('%sT12:00:00+09:00').getTime();const D=Date;class X extends D{constructor(...a){super(...(a.length?a:[T]))}static now(){return T}};window.Date=X;})()"
ND = {n: (a, b, '2026-%02d-%02d' % (mo, da)) for n, a, b, mo, da in NAT}
def reg(name, day):
    a, b, eff = ND[name]
    return b if day < eff else a
def sp(hist, day):
    v = 0
    for d, amt in hist:
        if d <= day: v = amt
    return v
def cl(x):
    return math.ceil(x)
async def judge(pg, lim, tag):
    """時給と月給(年間休日120日・8時間)のちょうどと1円下。合わない件数を返す。"""
    n = bad = 0
    await pg.click('.seg button[data-k="0"]')
    for pay, want in ((lim, '満たしています'), (lim - 1, '下回っています')):
        await pg.fill('#pay', str(pay)); v = await pg.inner_text('#o-vd'); mm = num(await pg.inner_text('#o-m')); n += 2
        if v != want: bad += 1; print('NG 時給', tag, pay, v)
        if mm != lim: bad += 1; print('NG 比べる最低賃金', tag, mm, lim)
    await pg.click('.seg button[data-k="2"]')
    need = cl(F(lim) * F(245 * 8, 12))
    for pay, want in ((need, '満たしています'), (need - 1, '下回っています')):
        await pg.fill('#pay', str(pay)); v = await pg.inner_text('#o-vd'); n += 1
        if v != want: bad += 1; print('NG 月給', tag, pay, v)
    await pg.click('.seg button[data-k="0"]')
    return n, bad
async def rows(pg, hid):
    return await pg.evaluate("h=>[...document.querySelectorAll(':is(#'+h+' ~ .tw):not(#'+h+' ~ .tw ~ .tw) tbody tr')].map(r=>[...r.cells].map(c=>c.innerText.trim()))", hid)
async def main():
    n = bad = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for slug, name in SLUG.items():
            m, o, eff = ND[name]
            for day in DAYS:
                ctx = await b.new_context(); await ctx.add_init_script(INIT % day)
                await ctx.route(lambda u: not u.startswith('file:'), lambda r: r.abort())  # 外の計測の読み込みを止める(待ち時間を無くす)
                pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
                await pg.goto(url('saitei-chingin-' + slug))
                r = m if slug == 'osaka' else reg(name, day)  # 大阪のページは10月1日より前の日を扱わない(DAYS は全部10月1日より後)
                if await pg.query_selector('#ind'): await pg.select_option('#ind', '0')
                k, e = await judge(pg, r, '%s %s 県の額' % (slug, day)); n += k; bad += e
                opts = await pg.evaluate("()=>[...document.querySelectorAll('#ind option')].map(o=>o.text)")
                tk = TOKU.get(slug, [])
                n += 1
                if len(opts) != (len(tk) + 1 if tk else 0): bad += 1; print('NG 業種の数', slug, opts)
                for nm, hist in tk:
                    idx = [i for i, t in enumerate(opts) if i > 0 and t.startswith(nm)]
                    n += 1
                    if len(idx) != 1: bad += 1; print('NG 業種が選べない', slug, nm); continue
                    await pg.select_option('#ind', str(idx[0]))
                    k, e = await judge(pg, max(r, sp(hist, day)), '%s %s %s' % (slug, day, nm)); n += k; bad += e
                if day == '2026-11-20':
                    # 月給の早見表:時給×(365−年間休日)×8÷12 の円未満切り上げ。日給の早見表:時給×時間の円未満切り上げ
                    t = await rows(pg, 'list'); n += 1
                    if len(t) != 5: bad += 1; print('NG 月給の表の行数', slug, len(t))
                    for row in t:
                        hol = num(row[0]); a = cl(F(m) * F((365 - hol) * 8, 12)); c0 = cl(F(o) * F((365 - hol) * 8, 12)); n += 3
                        if [num(row[2]), num(row[3]), num(row[4])] != [a, c0, a - c0]: bad += 1; print('NG 月給の表', slug, row)
                    t = await rows(pg, 'day'); n += 1
                    if len(t) != 6: bad += 1; print('NG 日給の表の行数', slug, len(t))
                    for row in t:
                        h = F(row[0].replace('時間', '')); d = cl(F(m) * h); n += 1
                        if num(row[1]) != d: bad += 1; print('NG 日給の表', slug, row)
                    body = await pg.inner_text('body')
                    for s in ('%s円' % format(m, ','), '%s円' % format(o, ',')):
                        n += 1
                        if s not in body: bad += 1; print('NG 本文に無い', slug, s)
                for e in errs: bad += 1; print('画面のエラー', slug, e[:100])
                await ctx.close()
        # 全国のページ:47都道府県を発効日の前後で
        for day in ('2026-11-20', '2026-11-30', '2026-12-01', '2026-12-02'):
            ctx = await b.new_context(); await ctx.add_init_script(INIT % day)
            await ctx.route(lambda u: not u.startswith('file:'), lambda r: r.abort())  # 外の計測の読み込みを止める(待ち時間を無くす)
            pg = await ctx.new_page(); await pg.goto(url('saitei-chingin'))
            opts = await pg.evaluate("()=>[...document.querySelectorAll('#pref option')].map(o=>o.text)")
            n += 1
            if len(opts) != 47: bad += 1; print('NG 全国 県の数', len(opts))
            for i, (name, a, o, mo, da) in enumerate(NAT):
                n += 1
                if not opts[i].startswith(name): bad += 1; print('NG 全国 並び', opts[i], name); continue
                await pg.select_option('#pref', str(i))
                k, e = await judge(pg, reg(name, day), '全国 %s %s' % (day, name)); n += k; bad += e
            if day == '2026-11-20':
                t = await rows(pg, 'rank'); n += 1
                if len(t) != 47: bad += 1; print('NG 全国の表の行数', len(t))
                for row in t:
                    hit = [x for x in NAT if row[1].startswith(x[0])]; n += 5
                    if len(hit) != 1: bad += 1; print('NG 全国の表 県', row); continue
                    name, a, o, mo, da = hit[0]; rk = 1 + sum(1 for x in NAT if x[1] > a)
                    want = [rk, a, o, a - o, '%d/%d' % (mo, da), cl(F(a) * F(245 * 8, 12))]
                    got = [num(row[0]), num(row[2]), num(row[3]), num(row[4]), row[5], num(row[6])]
                    if got != want: bad += 1; print('NG 全国の表', row, want)
            await ctx.close()
        await b.close()
    done(n, bad)
asyncio.run(main())
