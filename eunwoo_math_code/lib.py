"""Components for the Eunwoo math book. All styling inline (Design canvas format)."""
INK = "#2B2A33"
MUTE = "#5C5B6B"
# key: (strong, tint, label)
C = {
    'think': ('#6C4FD6', '#EEE9FF', '사고력'),
    'calc':  ('#C2410C', '#FFE9DC', '연산'),
    'curr':  ('#1C64C8', '#E3EEFF', '교과'),
    'shape': ('#18794E', '#DDF5E9', '도형·측정'),
    'deep':  ('#BE185D', '#FFE3EE', '심화'),
    'play':  ('#8A5A00', '#FFF0C2', '수학 놀이'),
}
SHAPE_COL = {'r': '#E5484D', 'b': '#2F7DE1', 'y': '#F5B301', 'g': '#2F9E44', 'p': '#8E5BD6'}


def svg(w, h, inner, vb=None):
    vb = vb or f"0 0 {w} {h}"
    return f'<svg width="{w}" height="{h}" viewBox="{vb}" aria-hidden="true" style="flex:none">{inner}</svg>'


def icon(k, s=26):
    d = {
        'apple': '<circle cx="12" cy="14" r="8" fill="#E5484D"/><path d="M12 6c0-2 1-3 3-3 0 2-1 3-3 3z" fill="#2F9E44"/>',
        'star': '<polygon points="12,2 15,9 22,9.5 16.5,14 18.5,21.5 12,17.5 5.5,21.5 7.5,14 2,9.5 9,9" fill="#F5B301"/>',
        'flower': '<g fill="#E64980"><circle cx="12" cy="5.5" r="4"/><circle cx="18.5" cy="10.5" r="4"/><circle cx="16" cy="18" r="4"/><circle cx="8" cy="18" r="4"/><circle cx="5.5" cy="10.5" r="4"/></g><circle cx="12" cy="12.5" r="3.2" fill="#FFD43B"/>',
        'fish': '<ellipse cx="11" cy="12" rx="8" ry="5.5" fill="#2F9BE8"/><polygon points="17,12 23,6 23,18" fill="#2F9BE8"/><circle cx="7.5" cy="10.5" r="1.2" fill="#fff"/>',
        'heart': '<path d="M12 21C4 14 2 10 2 7.5 2 4.5 4.5 3 7 3c2 0 3.7 1 5 3 1.3-2 3-3 5-3 2.5 0 5 1.5 5 4.5C22 10 20 14 12 21z" fill="#F06595"/>',
    }[k]
    return svg(s, s, d, "0 0 24 24")


def bunny(s=60):
    return svg(s, s, '<ellipse cx="35" cy="24" rx="9" ry="20" fill="#fff" stroke="#2B2A33" stroke-width="3"/><ellipse cx="65" cy="24" rx="9" ry="20" fill="#fff" stroke="#2B2A33" stroke-width="3"/><ellipse cx="35" cy="26" rx="4" ry="12" fill="#FFB3C7"/><ellipse cx="65" cy="26" rx="4" ry="12" fill="#FFB3C7"/><circle cx="50" cy="62" r="32" fill="#fff" stroke="#2B2A33" stroke-width="3"/><circle cx="39" cy="58" r="3.5" fill="#2B2A33"/><circle cx="61" cy="58" r="3.5" fill="#2B2A33"/><ellipse cx="50" cy="66" rx="4" ry="3" fill="#F06595"/><path d="M44 72q6 6 12 0" fill="none" stroke="#2B2A33" stroke-width="2.5" stroke-linecap="round"/><circle cx="30" cy="68" r="5" fill="#FFB3C7" opacity=".7"/><circle cx="70" cy="68" r="5" fill="#FFB3C7" opacity=".7"/>', "0 0 100 100")


def bear(s=60):
    return svg(s, s, '<circle cx="24" cy="30" r="12" fill="#C98B5B" stroke="#2B2A33" stroke-width="3"/><circle cx="76" cy="30" r="12" fill="#C98B5B" stroke="#2B2A33" stroke-width="3"/><circle cx="50" cy="56" r="34" fill="#D9A06C" stroke="#2B2A33" stroke-width="3"/><ellipse cx="50" cy="68" rx="15" ry="11" fill="#F3D9B8"/><circle cx="39" cy="50" r="3.5" fill="#2B2A33"/><circle cx="61" cy="50" r="3.5" fill="#2B2A33"/><ellipse cx="50" cy="64" rx="5" ry="3.5" fill="#2B2A33"/><path d="M44 72q6 5 12 0" fill="none" stroke="#2B2A33" stroke-width="2.5" stroke-linecap="round"/>', "0 0 100 100")


def box(w=46, h=38, r=10):
    return f'<div style="width:{w}px;height:{h}px;border:2px dashed #7A798A;border-radius:{r}px;background:#fff;flex:none"></div>'


def row(inner, gap=6, wrap=True, align='center', extra=''):
    return f'<div style="display:flex;align-items:{align};gap:{gap}px;flex-wrap:{"wrap" if wrap else "nowrap"};{extra}">{inner}</div>'


def txt(t, size=16, bold=False, color=INK, jua=False, extra=''):
    ff = "font-family:'Jua','Noto Sans KR',sans-serif;" if jua else ''
    return f'<span style="font-size:{size}px;font-weight:{700 if bold else 400};color:{color};{ff}{extra}">{t}</span>'


def countrow(n, kind='apple', s=26, ans=True, label=''):
    items = ''.join(icon(kind, s) for _ in range(n))
    a = box() if ans else ''
    lab = txt(label, 15, True, MUTE) if label else ''
    return row(lab + row(items, 3, True, 'center', 'max-width:420px') + a, 10)


def tenframe(k, total=10, color='#E5484D', cell=26):
    cells = ''
    for i in range(total):
        fill = f'<circle cx="{cell/2}" cy="{cell/2}" r="{cell/2-4}" fill="{color}"/>' if i < k else ''
        cells += svg(cell, cell, f'<rect x="0.5" y="0.5" width="{cell-1}" height="{cell-1}" fill="#fff" stroke="#2B2A33" stroke-width="1.5"/>{fill}')
    return f'<div style="display:grid;grid-template-columns:repeat(5,{cell}px);gap:0;flex:none">{cells}</div>'


def tenframes(n, color='#E5484D', cell=26):
    out = ''
    left = n
    while left > 0:
        out += tenframe(min(10, left), 10, color, cell)
        left -= 10
    return row(out, 14)


def bond(whole, a='', b='', s=0.7):
    def c(cx, cy, v, strong=False):
        fill = '#FFF0C2' if strong else '#fff'
        t = f'<text x="{cx}" y="{cy+8}" text-anchor="middle" font-size="22" font-family="Jua, sans-serif" fill="#2B2A33">{v}</text>' if v != '' else ''
        stroke = '#2B2A33' if v != '' else '#7A798A'
        dash = '' if v != '' else ' stroke-dasharray="4 3"'
        return f'<circle cx="{cx}" cy="{cy}" r="22" fill="{fill}" stroke="{stroke}" stroke-width="2.5"{dash}/>{t}'
    inner = '<line x1="75" y1="46" x2="38" y2="78" stroke="#2B2A33" stroke-width="2.5"/><line x1="75" y1="46" x2="112" y2="78" stroke="#2B2A33" stroke-width="2.5"/>'
    inner += c(75, 26, whole, True) + c(38, 96, a) + c(112, 96, b)
    return svg(int(150 * s), int(122 * s), inner, "0 0 150 122")


def shape(kind, col, s=34):
    f = SHAPE_COL[col]
    d = {
        'c': f'<circle cx="20" cy="20" r="16" fill="{f}"/>',
        't': f'<polygon points="20,4 36,35 4,35" fill="{f}"/>',
        's': f'<rect x="5" y="5" width="30" height="30" rx="2" fill="{f}"/>',
        'h': f'<polygon points="20,3 25,15 38,15 28,23 32,36 20,28 8,36 12,23 2,15 15,15" fill="{f}"/>',
    }[kind]
    return svg(s, s, d, "0 0 40 40")


def qslot(s=34):
    return f'<div style="width:{s}px;height:{s}px;border:2px dashed #7A798A;border-radius:8px;background:#fff;flex:none;display:flex;align-items:center;justify-content:center;font-family:Jua;font-size:20px;color:#7A798A">?</div>'


def pattern(seq, s=34):
    out = ''
    for t in seq:
        out += qslot(s) if t == '?' else shape(t[0], t[1], s)
    return row(out, 8, False)


def numstrip(vals, w=40, hl=None):
    out = ''
    for v in vals:
        if v == '':
            out += f'<div style="width:{w}px;height:{w}px;border:2px dashed #7A798A;border-radius:10px;background:#fff;flex:none"></div>'
        else:
            bg = '#FFF0C2' if (hl and v in hl) else '#fff'
            out += f'<div style="width:{w}px;height:{w}px;border:2px solid #2B2A33;border-radius:10px;background:{bg};flex:none;display:flex;align-items:center;justify-content:center;font-family:Jua;font-size:20px">{v}</div>'
    return row(out, 5, True)


def compare(a, b, kind='fish', s=22):
    ga = row(''.join(icon(kind, s) for _ in range(a)), 2, True, 'center', 'width:150px')
    gb = row(''.join(icon(kind, s) for _ in range(b)), 2, True, 'center', 'width:150px')
    mid = '<div style="width:30px;height:30px;border:2px dashed #7A798A;border-radius:50%;background:#fff;flex:none"></div>'
    return row(ga + mid + gb, 12, False)


def plusrow(a, b, kind='flower', s=24, op='+'):
    ga = row(''.join(icon(kind, s) for _ in range(a)), 2, True, 'center', 'max-width:150px')
    gb = row(''.join(icon(kind, s) for _ in range(b)), 2, True, 'center', 'max-width:150px')
    return row(ga + txt(op, 26, True, '#C2410C', True) + gb + txt('=', 24, True, MUTE, True) + box(46, 30), 8, False)


def minusrow(a, b, kind='fish', s=24):
    out = ''
    for i in range(a):
        if i >= a - b:
            out += f'<div style="position:relative;width:{s}px;height:{s}px;flex:none"><div style="opacity:.35">{icon(kind, s)}</div><div style="position:absolute;left:0;top:{s//2-1}px;width:{s}px;height:3px;background:#E5484D;transform:rotate(-35deg)"></div></div>'
        else:
            out += icon(kind, s)
    return row(row(out, 3, True, 'center', 'max-width:300px') + txt('남은 것', 14, True, MUTE) + box(46, 30), 8, False)


def dice(n, s=40):
    pos = {1: [(.5, .5)], 2: [(.28, .28), (.72, .72)], 3: [(.25, .25), (.5, .5), (.75, .75)],
           4: [(.28, .28), (.72, .28), (.28, .72), (.72, .72)], 5: [(.28, .28), (.72, .28), (.5, .5), (.28, .72), (.72, .72)],
           6: [(.3, .25), (.7, .25), (.3, .5), (.7, .5), (.3, .75), (.7, .75)]}[n]
    dots = ''.join(f'<circle cx="{x*s}" cy="{y*s}" r="{s*.075+1.5}" fill="#2B2A33"/>' for x, y in pos)
    return svg(s, s, f'<rect x="1.5" y="1.5" width="{s-3}" height="{s-3}" rx="8" fill="#fff" stroke="#2B2A33" stroke-width="2.5"/>{dots}')


def drawbox(label, w=None, h=90):
    ww = f'width:{w}px;' if w else 'width:100%;'
    return f'<div style="{ww}height:{h}px;box-sizing:border-box;border:2px dashed #7A798A;border-radius:14px;background:#fff;padding:6px 10px;font-size:13px;color:{MUTE}">{label}</div>'


def hundred(start=1, end=100, blanks=(), shade=(), cell=26):
    out = ''
    for v in range(start, end + 1):
        if v in blanks:
            out += f'<div style="width:{cell}px;height:{cell-4}px;border:1.5px dashed #7A798A;background:#fff"></div>'
        else:
            bg = '#FFD9A8' if v in shade else '#fff'
            out += f'<div style="width:{cell}px;height:{cell-4}px;border:1.5px solid #2B2A33;background:{bg};font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center">{v}</div>'
    return f'<div style="display:grid;grid-template-columns:repeat(10,{cell}px);gap:0;flex:none">{out}</div>'


def clock(h, s=88):
    import math
    nums = ''
    for i in range(1, 13):
        a = math.radians(i * 30 - 90)
        nums += f'<text x="{50+36*math.cos(a):.1f}" y="{54+36*math.sin(a):.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#2B2A33">{i}</text>'
    a = math.radians((h % 12) * 30 - 90)
    hand = f'<line x1="50" y1="50" x2="{50+22*math.cos(a):.1f}" y2="{50+22*math.sin(a):.1f}" stroke="#2B2A33" stroke-width="4.5" stroke-linecap="round"/>'
    minute = '<line x1="50" y1="50" x2="50" y2="18" stroke="#C2410C" stroke-width="3" stroke-linecap="round"/>'
    return svg(s, s, f'<circle cx="50" cy="50" r="46" fill="#fff" stroke="#2B2A33" stroke-width="3"/>{nums}{hand}{minute}<circle cx="50" cy="50" r="3.5" fill="#2B2A33"/>', "0 0 100 100")


def clockq(h, s=88):
    return row(clock(h, s) + txt('□시', 20, True, '#2B2A33', True), 6, False)


def table(header, rows, widths=None, size=14, pad=6):
    th = ''.join(f'<th style="border:1.5px solid #2B2A33;background:#F1EFE6;padding:{pad}px 8px;font-size:{size}px;text-align:center">{h}</th>' for h in header)
    body = ''
    for r in rows:
        body += '<tr>' + ''.join(f'<td style="border:1.5px solid #2B2A33;padding:{pad}px 8px;font-size:{size}px;text-align:center;background:#fff">{c}</td>' for c in r) + '</tr>'
    return f'<table style="border-collapse:collapse;width:100%"><tr>{th}</tr>{body}</table>'


def balance(left_n=3, right_n=1):
    return svg(190, 90, '<polygon points="95,40 80,84 110,84" fill="#C98B5B" stroke="#2B2A33" stroke-width="2.5"/><line x1="20" y1="30" x2="170" y2="50" stroke="#2B2A33" stroke-width="4" stroke-linecap="round"/><rect x="8" y="14" width="46" height="14" rx="4" fill="#E3EEFF" stroke="#2B2A33" stroke-width="2"/><rect x="138" y="52" width="46" height="14" rx="4" fill="#E3EEFF" stroke="#2B2A33" stroke-width="2"/>' + icon('apple', 16).replace('<svg ', '<svg x="23" y="-2" ').replace('width="16" height="16"', 'width="16" height="16"') + icon('star', 16).replace('<svg ', '<svg x="153" y="36" '))


def solids():
    cube = svg(56, 56, '<polygon points="10,18 34,18 34,46 10,46" fill="#9EC5FF" stroke="#2B2A33" stroke-width="2.5"/><polygon points="10,18 20,8 44,8 34,18" fill="#C9DEFF" stroke="#2B2A33" stroke-width="2.5"/><polygon points="34,18 44,8 44,36 34,46" fill="#6FA3F0" stroke="#2B2A33" stroke-width="2.5"/>')
    ball = svg(56, 56, '<circle cx="28" cy="28" r="20" fill="#FFB3C7" stroke="#2B2A33" stroke-width="2.5"/><ellipse cx="21" cy="21" rx="6" ry="4" fill="#fff" opacity=".7"/>')
    can = svg(56, 56, '<rect x="12" y="14" width="32" height="30" fill="#A8E6C1" stroke="#2B2A33" stroke-width="2.5"/><ellipse cx="28" cy="44" rx="16" ry="6" fill="#A8E6C1" stroke="#2B2A33" stroke-width="2.5"/><ellipse cx="28" cy="14" rx="16" ry="6" fill="#D4F5E1" stroke="#2B2A33" stroke-width="2.5"/>')
    return row(cube + ball + can, 18, False)


def house():
    return svg(80, 70, '<rect x="14" y="32" width="52" height="34" fill="#F5B301" stroke="#2B2A33" stroke-width="2.5"/><polygon points="8,32 40,6 72,32" fill="#E5484D" stroke="#2B2A33" stroke-width="2.5"/><rect x="32" y="46" width="16" height="20" fill="#fff" stroke="#2B2A33" stroke-width="2"/>')


def twotri():
    return row(svg(60, 56, '<polygon points="6,50 6,6 50,50" fill="#9EC5FF" stroke="#2B2A33" stroke-width="2.5"/>') + txt('+', 24, True, MUTE, True) + svg(60, 56, '<polygon points="54,6 54,50 10,6" fill="#FFB3C7" stroke="#2B2A33" stroke-width="2.5"/>') + txt('=', 24, True, MUTE, True) + qslot(44), 8, False)


def sym(w=170, h=110):
    # left half of a heart-like arrow on dotted grid, dashed axis
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#9A99A8"/>' for x in range(10, w, 20) for y in range(10, h, 20))
    left = '<polyline points="90,95 50,55 50,35 70,20 90,35" fill="none" stroke="#2B2A33" stroke-width="3" stroke-linejoin="round"/>'
    axis = f'<line x1="90" y1="4" x2="90" y2="{h-4}" stroke="#C2410C" stroke-width="2.5" stroke-dasharray="6 4"/>'
    return svg(w, h, f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="#fff" stroke="#7A798A" stroke-width="1.5"/>{dots}{left}{axis}')


def bars(a, b, cell=22):
    def bar(n, col):
        return row(''.join(f'<div style="width:{cell}px;height:{cell}px;border:1.5px solid #2B2A33;background:{col};flex:none"></div>' for _ in range(n)), 0, False)
    return f'<div style="display:flex;flex-direction:column;gap:6px">{bar(a, "#9EC5FF")}{bar(b, "#FFB3C7")}</div>'


def graph(cols=4, rows=6, labels=None, cell=24):
    labels = labels or [icon('apple', 22), icon('star', 22), icon('flower', 22), icon('fish', 22)]
    g = ''
    for r in range(rows):
        g += ''.join(f'<div style="width:{cell}px;height:{cell}px;border:1.5px solid #7A798A;background:#fff"></div>' for _ in range(cols))
    grid = f'<div style="display:grid;grid-template-columns:repeat({cols},{cell+36}px);gap:0">' + ''.join(
        f'<div style="display:flex;flex-direction:column;align-items:center;gap:0">' + ''.join(f'<div style="width:{cell+30}px;height:{cell}px;border:1.5px solid #7A798A;background:#fff"></div>' for _ in range(rows)) + f'<div style="padding-top:3px">{labels[c]}</div></div>' for c in range(cols)) + '</div>'
    return grid


def calendar():
    heads = ''.join(f'<div style="font-size:13px;font-weight:700;text-align:center;color:{"#BE185D" if d=="일" else INK}">{d}</div>' for d in '일월화수목금토')
    cells = ''.join('<div style="height:24px;border:1.5px solid #7A798A;background:#fff"></div>' for _ in range(14))
    return f'<div style="display:grid;grid-template-columns:repeat(7,44px);gap:0;flex:none">{heads}{cells}</div>'


def board(n=10):
    out = ''
    for i in range(1, n + 1):
        out += f'<div style="width:34px;height:34px;border:2px solid #2B2A33;border-radius:50%;background:{"#FFF0C2" if i in (1, n) else "#fff"};display:flex;align-items:center;justify-content:center;font-family:Jua;font-size:16px;flex:none">{i}</div>'
        if i < n:
            out += '<div style="width:8px;height:3px;background:#7A798A;flex:none"></div>'
    return row(out, 0, False)


def cards(vals, w=40):
    out = ''.join(f'<div style="width:{w}px;height:{int(w*1.3)}px;border:2px solid #2B2A33;border-radius:8px;background:#fff;font-family:Jua;font-size:20px;display:flex;align-items:center;justify-content:center;flex:none">{v}</div>' for v in vals)
    return row(out, 6, True)


def eq(*parts, size=24):
    out = ''
    for p in parts:
        if p == '□':
            out += box(40, 30)
        else:
            out += txt(p, size, True, INK, True)
    return row(out, 8, False)


def lines(n=2, w='100%'):
    return ''.join(f'<div style="width:{w};height:1.5px;background:#7A798A;margin-top:22px"></div>' for _ in range(n))


def blocks(t, o):
    rods = ''.join('<div style="width:13px;height:66px;background:#9EC5FF;border:1.5px solid #2B2A33;display:grid;grid-template-rows:repeat(10,1fr);flex:none">' + ''.join('<div style="border-bottom:1px solid #2B2A33"></div>' for _ in range(10)) + '</div>' for _ in range(t))
    cubes = ''.join('<div style="width:13px;height:13px;background:#FFD43B;border:1.5px solid #2B2A33;flex:none"></div>' for _ in range(o))
    return row(row(rods, 4, False, 'flex-end') + row(cubes, 3, True, 'flex-end', 'max-width:70px'), 16, False, 'flex-end')


def clock2(h, half=False, s=88):
    import math
    nums = ''
    for i in range(1, 13):
        a = math.radians(i * 30 - 90)
        nums += f'<text x="{50+36*math.cos(a):.1f}" y="{54+36*math.sin(a):.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="#2B2A33">{i}</text>'
    a = math.radians((h % 12) * 30 + (15 if half else 0) - 90)
    hand = f'<line x1="50" y1="50" x2="{50+22*math.cos(a):.1f}" y2="{50+22*math.sin(a):.1f}" stroke="#2B2A33" stroke-width="4.5" stroke-linecap="round"/>'
    minute = '<line x1="50" y1="50" x2="50" y2="82" stroke="#C2410C" stroke-width="3" stroke-linecap="round"/>' if half else '<line x1="50" y1="50" x2="50" y2="18" stroke="#C2410C" stroke-width="3" stroke-linecap="round"/>'
    return svg(s, s, f'<circle cx="50" cy="50" r="46" fill="#fff" stroke="#2B2A33" stroke-width="3"/>{nums}{hand}{minute}<circle cx="50" cy="50" r="3.5" fill="#2B2A33"/>', "0 0 100 100")


def clockq2(h, half=False, s=80):
    return row(clock2(h, half, s) + txt('□시 □분' if half else '□시', 18, True, '#2B2A33', True), 6, False)


def stackview(hs, cell=24):
    cols = ''
    for n in hs:
        cols += '<div style="display:flex;flex-direction:column-reverse;gap:0">' + ''.join(f'<div style="width:{cell}px;height:{cell}px;background:#9EC5FF;border:2px solid #2B2A33;box-sizing:border-box"></div>' for _ in range(n)) + '</div>'
    return row(cols, 0, False, 'flex-end')


def tan4():
    return svg(84, 84, '<polygon points="4,4 80,4 42,42" fill="#FFB3C7" stroke="#2B2A33" stroke-width="2.5"/><polygon points="80,4 80,80 42,42" fill="#9EC5FF" stroke="#2B2A33" stroke-width="2.5"/><polygon points="80,80 4,80 42,42" fill="#A8E6C1" stroke="#2B2A33" stroke-width="2.5"/><polygon points="4,80 4,4 42,42" fill="#FFE08A" stroke="#2B2A33" stroke-width="2.5"/>')


def ruler(n=10, obj=None, unit=37.8):
    w = n * unit
    ticks = ''.join(f'<div style="position:absolute;left:{i*unit:.1f}px;top:0;width:1.5px;height:{20 if i % 5 == 0 else 13}px;background:#2B2A33"></div><div style="position:absolute;left:{i*unit-7:.1f}px;top:22px;font-size:11px;width:16px;text-align:center">{i}</div>' for i in range(n + 1))
    bar = f'<div style="width:{obj*unit:.1f}px;height:16px;background:#FFB3C7;border:2px solid #2B2A33;border-radius:4px;box-sizing:border-box;margin-bottom:6px"></div>' if obj else ''
    return f'<div style="display:flex;flex-direction:column;padding-left:8px">{bar}<div style="position:relative;width:{w:.1f}px;height:40px;background:#FFF0C2;border:1.5px solid #2B2A33;box-sizing:border-box">{ticks}</div></div>'


def groups(n, k, kind='apple', s=20):
    g = ''.join('<div style="border:2px solid #7A798A;border-radius:14px;padding:4px 6px;background:#fff;display:flex;gap:2px;flex:none">' + ''.join(icon(kind, s) for _ in range(k)) + '</div>' for _ in range(n))
    return row(g, 8, True, 'center', 'max-width:440px')


def p(t, size=15, color=INK, bold=False, extra=''):
    return f'<div style="font-size:{size}px;line-height:1.5;color:{color};font-weight:{700 if bold else 400};{extra}">{t}</div>'
