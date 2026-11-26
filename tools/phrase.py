# 画面の文を BudouX の文節で区切り、区切りの外で折れないようにする。
# finish.py と tools/build_kyuyo_meisai.py から使う。
# 使い方: リポジトリの直下で python3 -c "import sys; sys.path.insert(0,'tools'); import phrase; print(phrase.phrases('月31,667円です。'))"
import html, json, os, re
import budoux

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PARSER = budoux.load_default_japanese_parser()

# 行頭に来ると読みにくい助詞。後ろの語にくっつけず、前の語にくっつける。
PART_ONE = set('のをにはがとでもへやかねよぞわ')
PART_LONG = ('から', 'まで', 'より', 'って', 'では', 'には', 'とは', 'かは')
# 中黒で並ぶ列（2つ以上）は、語と語のあいだ（中黒の直後）で折ってよい。
# 中黒が1つの複合語（子ども・子育て、農林水産・清酒）は折らない。

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
# この中は、中の文だけを文節で包む。リンク（a）もその中だけで区切る。
# リンクの直後の助詞は、包む前にリンクの中へ移す。
BLOCK = {
    'address', 'article', 'aside', 'blockquote', 'div', 'dl', 'dt', 'dd', 'fieldset',
    'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'header', 'li', 'main', 'nav', 'ol', 'p', 'pre', 'section', 'table', 'thead',
    'tbody', 'tfoot', 'tr', 'td', 'th', 'ul', 'button', 'caption', 'a',
}
ATOMIC = {'select', 'svg', 'textarea', 'math'}


def phrases(text):
    """文を、折ってよい単位のリストにする。"""
    if text is None:
        return []
    parts = []
    for bit in text.split('\uE001'):
        parts.extend(_one(bit))
        parts.append('\uE001')
    if parts and parts[-1] == '\uE001':
        parts.pop()
    return [p for p in parts if p != '']


def breaks(text):
    """折ってよい位置（文字の終わり）。文節の端と、中黒が2つ以上ある列の中黒の直後。"""
    ends = set()
    i = 0
    for p in phrases(text):
        i += len(p)
        ends.add(i)
    ends.add(len(text))
    return ends


def wrap_text(text):
    """プレーンな文字列を span.ph で包む。JS が差し替える文でも同じ分け方。"""
    out = []
    for p in phrases(text):
        if p == '\uE001':
            out.append('<br>')
            continue
        if not p.strip():
            out.append(html.escape(p, quote=False))
            continue
        out.append('<span class="ph">' + html.escape(p, quote=False) + '</span>')
    return ''.join(out)


def _one(text):
    if text == '':
        return []
    parts = _PARSER.parse(text)
    parts = _glue(parts)
    parts = _glue_dots(parts)
    parts = _explode_lists(parts)
    parts = _split_spaces(parts)
    parts = _glue(parts)
    return parts


def _glue(parts):
    out = []
    for p in parts:
        if out and _stick(out[-1], p):
            out[-1] += p
        else:
            out.append(p)
    return out


def _glue_dots(parts):
    """BudouX が分けた中黒は、複合語（中黒1つ）だけ前へくっつける。列は分けたまま。"""
    out = []
    for p in parts:
        if out and (out[-1].endswith('・') or p.startswith('・')) and (out[-1] + p).count('・') <= 1:
            out[-1] += p
        else:
            out.append(p)
    return out


def _split_spaces(parts):
    """長い塊だけ、空白のところで分ける。数字と単位は同じ側に残す。"""
    out = []
    for p in parts:
        if len(p) <= 14 or ' ' not in p and '\u3000' not in p:
            out.append(p)
            continue
        buf = ''
        for ch in p:
            if ch in ' \u3000' and len(buf) >= 2:
                out.append(buf + ch)
                buf = ''
            else:
                buf += ch
        if buf:
            out.append(buf)
    return out


def _kanji(ch):
    return '\u4e00' <= ch <= '\u9fff'


def _latin_before(s):
    """助詞の直前が英字（「PDF」など。かぎ括弧は飛ばす）。"""
    j = len(s) - 1
    while j >= 0 and s[j] in '「『（(["\'':
        j -= 1
    saw = False
    while j >= 0 and ('A' <= s[j] <= 'Z' or 'a' <= s[j] <= 'z'):
        saw = True
        j -= 1
    return saw


def latin_kanji_cut(text, i):
    """位置 i が「英字＋助詞｜漢字」（「PDFに｜保存」）なら True。行末にしてはいけない境目。"""
    if not text or i <= 0 or i >= len(text) or not _kanji(text[i]):
        return False
    prev = text[:i]
    for p in sorted(PART_LONG, key=len, reverse=True):
        if prev.endswith(p) and _latin_before(prev[:-len(p)]):
            return True
    return prev[-1] in PART_ONE and _latin_before(prev[:-1])


def _stick(prev, nxt):
    if not prev or not nxt:
        return False
    if nxt[0] in PART_ONE or nxt.startswith(PART_LONG):
        return True
    # 「ます」「す」で行が始まらないように、前の語へくっつける。
    if nxt.startswith('ます') or nxt.startswith('す'):
        return True
    if (prev[-1].isdigit() or prev[-1] in ',，') and nxt[0] in '円％%人歳月日分万千倍':
        return True
    if all(c in '。、．，,.・）)」』】〉》' for c in nxt):
        return True
    # 「PDFに保存」のように、かぎ括弧の中の英字＋助詞＋漢字は境目で折らない。
    if '「' in prev and '」' in nxt and latin_kanji_cut(prev + nxt, len(prev)):
        return True
    return False


def _explode_lists(parts):
    """中黒が2つ以上なら、中黒の直後で分ける。1つの複合語はそのまま。"""
    out = []
    for p in parts:
        if p.count('・') < 2:
            out.append(p)
            continue
        buf = ''
        for ch in p:
            buf += ch
            if ch == '・':
                out.append(buf)
                buf = ''
        if buf:
            out.append(buf)
    return out


def _tag_end(s, i):
    quote = None
    j = i + 1
    while j < len(s):
        c = s[j]
        if quote:
            if c == quote:
                quote = None
        elif c in '"\'':
            quote = c
        elif c == '>':
            return j + 1
        j += 1
    return len(s)


def _tag_name(raw):
    m = re.match(r'</?\s*([A-Za-z0-9]+)', raw)
    return m.group(1).lower() if m else ''


def _class_list(raw):
    m = re.search(r'''class\s*=\s*["']([^"']*)["']''', raw)
    return m.group(1).split() if m else []


def _parse(s, i, end_tag):
    nodes = []
    while i < len(s):
        if s.startswith('<!--', i):
            j = s.find('-->', i)
            j = len(s) if j < 0 else j + 3
            nodes.append(('raw', s[i:j]))
            i = j
            continue
        if s[i] != '<':
            j = s.find('<', i)
            j = len(s) if j < 0 else j
            if j > i:
                nodes.append(('text', s[i:j]))
            i = j
            continue
        j = _tag_end(s, i)
        raw = s[i:j]
        name = _tag_name(raw)
        if raw.startswith('</'):
            if end_tag and name == end_tag:
                return nodes, j
            nodes.append(('raw', raw))
            i = j
            continue
        if name in ('script', 'style'):
            close = '</' + name
            k = s.lower().find(close, j)
            if k < 0:
                nodes.append(('raw', s[i:]))
                return nodes, len(s)
            k = s.find('>', k) + 1
            nodes.append(('raw', s[i:k]))
            i = k
            continue
        if name in VOID or raw.endswith('/>'):
            nodes.append(('void', raw, name))
            i = j
            continue
        if name in ATOMIC:
            inner, k = _parse(s, j, name)
            nodes.append(('atom', s[i:k], name))
            i = k
            continue
        children, k = _parse(s, j, name)
        nodes.append(('el', name, raw, children))
        i = k
    return nodes, i


def _pull_particles(nodes):
    """リンクの直後の助詞を、リンクの中へ移す。文の文字は変えない。"""
    for n in nodes:
        if n[0] == 'el':
            _pull_particles(n[3])
    i = 1
    while i < len(nodes):
        prev, cur = nodes[i - 1], nodes[i]
        if cur[0] == 'text' and prev[0] == 'el' and prev[1] in ('a', 'b', 'strong', 'em', 'i'):
            t = html.unescape(cur[1])
            k = _lead_part(t)
            if k:
                _append_text(prev[3], t[:k])
                rest = t[k:]
                if rest:
                    nodes[i] = ('text', html.escape(rest, quote=False))
                else:
                    nodes.pop(i)
                    continue
        i += 1


def _lead_part(t):
    if not t:
        return 0
    for p in PART_LONG:
        if t.startswith(p):
            return len(p)
    if t[0] in PART_ONE:
        return 1
    return 0


def _append_text(children, text):
    if children and children[-1][0] == 'text':
        children[-1] = ('text', children[-1][1] + html.escape(text, quote=False))
    else:
        children.append(('text', html.escape(text, quote=False)))


def _transparent(name, open_tag):
    if name != 'span':
        return False
    if re.fullmatch(r'<span\s*>', open_tag):
        return True
    c = set(_class_list(open_tag))
    return bool(c) and c <= {'ph', 'nw'} and 'id=' not in open_tag and 'style=' not in open_tag


def _flatten(nodes, acc):
    for n in nodes:
        if n[0] == 'text':
            acc.append(('t', html.unescape(n[1])))
        elif n[0] == 'void':
            if n[2] == 'br':
                acc.append(('br', n[1]))
            else:
                acc.append(('m', n[1]))
        elif n[0] == 'atom':
            if n[2] == 'select':
                acc.append(('a', n[1]))
            else:
                acc.append(('m', n[1]))
        elif n[0] == 'raw':
            acc.append(('m', n[1]))
        elif n[0] == 'el':
            if _transparent(n[1], n[2]):
                _flatten(n[3], acc)
            elif n[1] in BLOCK or 'upd' in _class_list(n[2]):
                acc.append(('block', n))
            else:
                acc.append(('m', n[2]))
                _flatten(n[3], acc)
                acc.append(('m', '</' + n[1] + '>'))


def _emit(acc):
    """文節ごとに span.ph で包む。タグをまたぐ span は作らない（タグの前でいったん閉じる）。"""
    text = []
    for a in acc:
        if a[0] == 't':
            text.append(a[1])
        elif a[0] == 'a':
            text.append('\uE000')
        elif a[0] == 'br':
            text.append('\uE001')
    s = ''.join(text)
    if not s.strip('\uE000\uE001 \t\r\n'):
        return ''.join(a[1] for a in acc)
    bset = breaks(s)
    out, buf, pos = [], [], 0

    def flush():
        nonlocal buf
        if not buf:
            return
        body = ''.join(buf)
        plain = re.sub(r'<[^>]+>', '', body).replace('\uE000', '')
        if plain.strip():
            out.append('<span class="ph">' + body + '</span>')
        else:
            out.append(body)
        buf = []

    for a in acc:
        if a[0] == 'm':
            flush()
            out.append(a[1])
            continue
        if a[0] == 'br':
            flush()
            out.append(a[1])
            pos += 1
            continue
        if a[0] == 'a':
            buf.append(a[1])
            pos += 1
            if pos in bset:
                flush()
            continue
        for ch in a[1]:
            buf.append(html.escape(ch, quote=False))
            pos += 1
            if pos in bset:
                flush()
    flush()
    return ''.join(out)


def _render(nodes):
    acc = []
    _flatten(nodes, acc)
    out = []
    buf = []
    for a in acc:
        if a[0] == 'block':
            if buf:
                out.append(_emit(buf))
                buf = []
            n = a[1]
            # 題名の帯の日付と、全ページで同じ監修の3行は包まない（関所が形を比べる）。
            if _class_list(n[2]) and set(_class_list(n[2])) & {'upd', 'auth-h', 'auth-n', 'auth-r'}:
                out.append(n[2] + _unwrap_inner(n[3]) + '</' + n[1] + '>')
            else:
                out.append(n[2] + _render(n[3]) + '</' + n[1] + '>')
        else:
            buf.append(a)
    if buf:
        out.append(_emit(buf))
    return ''.join(out)


def _unwrap_inner(nodes):
    """文節の span を外して、もとの文に戻す。"""
    parts = []
    for n in nodes:
        if n[0] == 'text':
            parts.append(n[1])
        elif n[0] in ('raw', 'void'):
            parts.append(n[1])
        elif n[0] == 'atom':
            parts.append(n[1])
        elif n[0] == 'el':
            inner = _unwrap_inner(n[3])
            if _transparent(n[1], n[2]):
                parts.append(inner)
            else:
                parts.append(n[2] + inner + '</' + n[1] + '>')
    return ''.join(parts)


def _raw_inner(nodes):
    parts = []
    for n in nodes:
        if n[0] == 'text':
            parts.append(n[1])
        elif n[0] in ('raw', 'void'):
            parts.append(n[1] if n[0] == 'raw' else n[1])
        elif n[0] == 'atom':
            parts.append(n[1])
        elif n[0] == 'el':
            parts.append(n[2] + _raw_inner(n[3]) + '</' + n[1] + '>')
    return ''.join(parts)


def apply_fragment(fragment):
    nodes, _ = _parse(fragment, 0, None)
    _pull_particles(nodes)
    return _render(nodes)


def _normalize_mrow(html):
    """「選んだ月」と月の選択と「の」が、助詞の前で分かれない並びにする。"""
    pat = re.compile(
        r'(<div class="mrow">\s*<label\b[^>]*>)(.*?)(</label>\s*)(<select\b[\s\S]*?</select>)(\s*(?:<span\b[^>]*>[\s\S]*?</span>|[^<]+))',
        re.S)

    def repl(m):
        return m.group(1) + m.group(2) + m.group(4) + m.group(5) + '</label>'

    return pat.sub(repl, html, count=1)


def apply_page(html):
    """<main> の中だけ文節で包む。題名の帯の日付（class=upd）と main の外は変えない。"""
    html = _normalize_mrow(html)
    m = re.search(r'<main\b[^>]*>', html)
    if not m:
        return html
    start = m.end()
    end = html.lower().rfind('</main>')
    if end < start:
        return html
    inner = apply_fragment(html[start:end])
    html = html[:start] + inner + html[end:]
    block = '<script id="tt-ph">\n' + js_runtime() + '\n</script>\n'
    if 'id="tt-ph"' in html:
        html = re.sub(r'<script id="tt-ph">[\s\S]*?</script>\n?', lambda _m: block, html, count=1)
    else:
        needle = '<script>\n(function(){\n var PF='
        if needle in html:
            html = html.replace(needle, block + needle, 1)
    return html


def js_runtime():
    """ページの JS が文を差し替えたあとも、同じ分け方で包む。"""
    model = json.dumps(_PARSER.model, ensure_ascii=False, separators=(',', ':'))
    return (
        '(function(){\n'
        'var M=' + model + ';\n'
        'var base=-0.5*Object.keys(M).reduce(function(s,k){return s+Object.keys(M[k]).reduce(function(a,w){return a+M[k][w]},0)},0);\n'
        'function bx(s){\n'
        ' if(!s)return [];\n'
        ' var c=[s[0]],i,sc,U=M;\n'
        ' var u1=U.UW1||{},u2=U.UW2||{},u3=U.UW3||{},u4=U.UW4||{},u5=U.UW5||{},u6=U.UW6||{};\n'
        ' var b1=U.BW1||{},b2=U.BW2||{},b3=U.BW3||{},t1=U.TW1||{},t2=U.TW2||{},t3=U.TW3||{},t4=U.TW4||{};\n'
        ' for(i=1;i<s.length;i++){sc=base;\n'
        '  if(i>2)sc+=u1[s[i-3]]||0; if(i>1)sc+=u2[s[i-2]]||0; sc+=u3[s[i-1]]||0; sc+=u4[s[i]]||0;\n'
        '  if(i+1<s.length)sc+=u5[s[i+1]]||0; if(i+2<s.length)sc+=u6[s[i+2]]||0;\n'
        '  if(i>1)sc+=b1[s.slice(i-2,i)]||0; sc+=b2[s.slice(i-1,i+1)]||0; if(i+1<s.length)sc+=b3[s.slice(i,i+2)]||0;\n'
        '  if(i>2)sc+=t1[s.slice(i-3,i)]||0; if(i>1)sc+=t2[s.slice(i-2,i+1)]||0;\n'
        '  if(i+1<s.length)sc+=t3[s.slice(i-1,i+2)]||0; if(i+2<s.length)sc+=t4[s.slice(i,i+3)]||0;\n'
        '  if(sc>0)c.push(s[i]); else c[c.length-1]+=s[i];}\n'
        ' return c;\n'
        '}\n'
        'var ONE="のをにはがとでもへやかねよぞわ", LONG=["から","まで","より","って","では","には","とは","かは"];\n'
        'function stick(p,n){\n'
        ' if(!p||!n)return false;\n'
        ' if(ONE.indexOf(n[0])>=0)return true;\n'
        ' for(var i=0;i<LONG.length;i++)if(n.indexOf(LONG[i])===0)return true;\n'
        ' if(n.indexOf("ます")===0||n.indexOf("す")===0)return true;\n'
        ' if((p[p.length-1]>="0"&&p[p.length-1]<="9"||p[p.length-1]===","||p[p.length-1]==="，")&&"円％%人歳月日分万千倍".indexOf(n[0])>=0)return true;\n'
        ' if(/^[。、．，,.・）)」』】〉》]+$/.test(n))return true;\n'
        ' if(p.indexOf("「")>=0&&n.indexOf("」")>=0&&latinKanji(p,n))return true;\n'
        ' return false;\n'
        '}\n'
        'function latinKanji(p,n){\n'
        ' if(!p||!n)return false;\n'
        ' var c=n.charCodeAt(0); if(!(c>=0x4e00&&c<=0x9fff))return false;\n'
        ' var cut=p.length;\n'
        ' if(ONE.indexOf(p[p.length-1])>=0)cut=p.length-1;\n'
        ' else{var hit=false; for(var i=0;i<LONG.length;i++){if(p.slice(-LONG[i].length)===LONG[i]){hit=true;cut=p.length-LONG[i].length;break;}} if(!hit)return false;}\n'
        ' var j=cut-1; while(j>=0&&"「『（([\\"\'".indexOf(p[j])>=0)j--;\n'
        ' var saw=false; while(j>=0&&((p[j]>="A"&&p[j]<="Z")||(p[j]>="a"&&p[j]<="z"))){saw=true;j--;}\n'
        ' return saw;\n'
        '}\n'
        'function glue(a){var o=[]; for(var i=0;i<a.length;i++){if(o.length&&stick(o[o.length-1],a[i]))o[o.length-1]+=a[i]; else o.push(a[i]);} return o;}\n'
        'function dots(a){var o=[],i,p; for(i=0;i<a.length;i++){p=a[i]; if(o.length&&(o[o.length-1].slice(-1)==="・"||p[0]==="・")&&(o[o.length-1]+p).split("・").length-1<=1)o[o.length-1]+=p; else o.push(p);} return o;}\n'
        'function explode(a){var o=[],i,p,b,j; for(i=0;i<a.length;i++){p=a[i]; if((p.split("・").length-1)<2){o.push(p); continue;} b=""; for(j=0;j<p.length;j++){b+=p[j]; if(p[j]==="・"){o.push(b); b="";}} if(b)o.push(b);} return o;}\n'
        'function spaces(a){var o=[],i,p,b,j,ch; for(i=0;i<a.length;i++){p=a[i]; if(p.length<=14||(p.indexOf(" ")<0&&p.indexOf("\\u3000")<0)){o.push(p); continue;} b=""; for(j=0;j<p.length;j++){ch=p[j]; if((ch===" "||ch==="\\u3000")&&b.length>=2){o.push(b+ch); b="";} else b+=ch;} if(b)o.push(b);} return o;}\n'
        'function parts(s){return glue(spaces(explode(dots(glue(bx(s))))));}\n'
        'function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;");}\n'
        'window.PH=function(s){return parts(String(s)).map(function(p){return p.trim()? \'<span class="ph">\'+esc(p)+"</span>" : esc(p);}).join("");};\n'
        '})();'
    )
