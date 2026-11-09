"""책 데이터(gen.py·문제표)에서 홈페이지 퀴즈 데이터(data/quiz.js)를 만든다.

사용:  python tools/build_quiz.py
환경변수 EW_CODE 로 책 코드 폴더를 바꿀 수 있다 (기본: eunwoo_math_code/eunwoo_math_code).

구조
  - 책의 주차(12주)마다 문제 풀(weeks[g])을 만든다. g = (권-1)*12 + (주-1)
  - 한 권은 30개 마을(하루에 하나)이고, 한 주를 2~3개 마을이 나눠 쓴다.
  - 문제마다 영역(t)과 난이도 단계(l: 1~5)를 붙인다. 퀴즈는 홈페이지에서 10문제로 구성한다.
      1~5번 복습(쉬운 단계, 앞선 주차 문제 포함), 6~10번 단계별로 어려워지는 문제
  영역: calc 연산 / think 사고력 / shape 도형·측정 / curr 교과 / ahead 선행 / deep 심화
"""
import json
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CODE = os.environ.get('EW_CODE') or os.path.join(ROOT, 'eunwoo_math_code', 'eunwoo_math_code')
sys.path.insert(0, CODE)
sys.path.insert(0, HERE)

import gen  # noqa: E402
import content, content2, content3, content4, content5  # noqa: E402
import probs, probs2  # noqa: E402  (probs2 에 X, probs3~5 가 X 를 채운다)
import probs3, probs4, probs5  # noqa: E402,F401
from book1_data import BOOK1  # noqa: E402

CONTENT = {1: content, 2: content2, 3: content3, 4: content4, 5: content5}
P, X = probs.P, probs2.X
NBOOKS = 5
VILLAGES = 30      # 한 권의 마을 수 (하루에 하나)
WEEKS = 12         # 한 권의 주차 수

BOOK_INFO = {
    1: ('1권', '1~100 수 세기와 덧셈·뺄셈'),
    2: ('2권', '두 자리 수 · 받아올림 · 시계와 도형'),
    3: ('3권', '세 수 · 몇십몇 계산 · 길이와 그래프'),
    4: ('4권', '수 구조 · 계산 전략 · 추리'),
    5: ('5권', '받아올림 · 곱셈 준비 · 시간'),
}
MEASURE = {'clock', 'clock_hour', 'min5', 'hour_later', 'length', 'len_cmp', 'len_add',
           'shape_facts', 'data_most', 'data_diff'}
MEASURE_RE = re.compile(r'(시계|바늘|\d\s?시|\d\s?분|시간|cm|길이|모양|세모|네모|동그라미|변이|꼭짓점|도형|표에서|그래프|자를)')
TITLE_MEASURE_RE = re.compile(r'(시계|시간|도형|자료|규칙|그래프|cm|어림|^자 |길이)')
EMO = ['🍎', '🐟', '⭐', '🌸', '🍓', '🐥']
CATS = ['calc', 'think', 'shape', 'curr', 'ahead', 'deep']
CUSTOM = ('count', 'pattern', 'shape_name', 'shape_count', 'shape_sides', 'clue', 'between',
          'two_step', 'compare_expr', 'digit_cards', 'blank_two')
PAIRS = [('될 수 없어요', '될 수 있어요'), ('될 수 있어요', '될 수 없어요'), ('같아요', '달라요'), ('달라요', '같아요'),
         ('있어요', '없어요'), ('없어요', '있어요'), ('맞아요', '틀려요'), ('틀려요', '맞아요'),
         ('아니요', '네'), ('네', '아니요'), ('예', '아니요')]
ICONS = ['🏡', '🌳', '🍯', '🦆', '🏰', '🧺', '🎈', '🍭', '🌈', '🚂', '🐻', '🦋']
SUFFIX = ['', ' ②', ' ③']

# 문제 종류별 기본 난이도 점수 (클수록 어려움)
BASE = {
    'plus_small': 1, 'minus_small': 1, 'make10': 1, 'count': 1, 'teen_ones': 1, 'plus_ten': 1, 'next': 1,
    'hund': 1.5, 'cmp': 1.2, 'tens_ones': 1.5, 'odd_even': 1.2, 'tenmore': 1.8, 'clock_hour': 1.3,
    'length': 1.5, 'shape_facts': 1, 'skip': 2.2, 'plus_to20': 2, 'minus_teen': 2.2, 'blank_plus': 2,
    'blank_minus': 2.3, 'blank2': 2.5, 'tens_plus': 1.8, 'tens_pm': 2, 'plus_nocarry': 2,
    'minus_noborrow': 2.2, 'plus_carry2': 3, 'minus_borrow2': 3.2, 'triple': 2.6, 'same_add': 2.3,
    'group': 2.3, 'share': 2.4, 'clock': 2, 'min5': 2.3, 'hour_later': 2.6, 'len_cmp': 2.2, 'len_add': 2.2,
    'data_most': 2, 'data_diff': 2.8, 'pattern': 1.8, 'shape_name': 1.2, 'shape_count': 1.4,
    'shape_sides': 1.3, 'clue': 4, 'between': 3.5, 'two_step': 4, 'compare_expr': 3, 'digit_cards': 4.5,
    'blank_two': 4,
}
ITEM_BASE = {'concept': 1.5, 'grade': 2, 'apply': 3, 'think': 3.5, 'olymp': 4.5}


# ---------------------------------------------------------------- 조사 (숫자 읽기의 받침에 맞춤)
def _jong(n):
    return n % 10 in (0, 1, 3, 6, 7, 8)


def eun(n):
    return f'{n}은' if _jong(n) else f'{n}는'


def gwa(n):
    return f'{n}과' if _jong(n) else f'{n}와'


# ---------------------------------------------------------------- 그림
def big(t):
    return f'<div class="big">{t}</div>'


def vis(t):
    return f'<div class="vis">{t}</div>'


def clock_svg(h, half, size=250):
    cx = cy = size / 2
    r = size / 2 - 6
    s = (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#2B2A33" stroke-width="5"/>')
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        x = cx + (r - size * 0.12) * math.cos(a)
        y = cy + (r - size * 0.12) * math.sin(a) + size * 0.035
        s += f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="{size * 0.1:.0f}" fill="#2B2A33">{n}</text>'
    ha = math.radians(((h % 12) + (0.5 if half else 0)) * 30 - 90)
    ma = math.radians((180 if half else 0) - 90)
    s += (f'<line x1="{cx}" y1="{cy}" x2="{cx + r * .5 * math.cos(ha):.1f}" y2="{cy + r * .5 * math.sin(ha):.1f}" '
          f'stroke="#2B2A33" stroke-width="8" stroke-linecap="round"/>'
          f'<line x1="{cx}" y1="{cy}" x2="{cx + r * .75 * math.cos(ma):.1f}" y2="{cy + r * .75 * math.sin(ma):.1f}" '
          f'stroke="#E5484D" stroke-width="5" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="6" fill="#2B2A33"/></svg>')
    return s


def ruler_svg(v):
    u = 36
    w = 10 * u + 40
    s = f'<svg width="{w}" height="104" viewBox="0 0 {w} 104"><rect x="20" y="10" width="{v * u}" height="30" rx="10" fill="#7FD8B5" stroke="#2B2A33" stroke-width="3"/>'
    s += f'<rect x="14" y="52" width="{10 * u + 12}" height="40" rx="6" fill="#FFE9AE" stroke="#2B2A33" stroke-width="3"/>'
    for i in range(11):
        x = 20 + i * u
        s += f'<line x1="{x}" y1="52" x2="{x}" y2="66" stroke="#2B2A33" stroke-width="3"/>'
        s += f'<text x="{x}" y="88" text-anchor="middle" font-size="16" fill="#2B2A33">{i}</text>'
    return s + '</svg>'


def table_html(names, vals):
    h = ''.join(f'<th>{n}</th>' for n in names)
    d = ''.join(f'<td>{v}</td>' for v in vals)
    return f'<table class="tb"><tr>{h}</tr><tr>{d}</tr></table>'


# ---------------------------------------------------------------- 보기 만들기
def variants(ans, R, first_only=False, minv=0, maxv=None):
    ms = list(re.finditer(r'\d+', ans))
    out = []
    if not ms:
        return out
    tries = 0
    while len(out) < 3 and tries < 80:
        tries += 1
        m = ms[0] if first_only else R.choice(ms)
        d = R.choice([-3, -2, -1, 1, 2, 3]) if tries < 40 else R.choice([-6, -5, -4, 4, 5, 6, 10, -10])
        nv = int(m.group()) + d
        if nv < minv or (maxv is not None and nv > maxv):
            continue
        s = ans[:m.start()] + str(nv) + ans[m.end():]
        if s != ans and s not in out:
            out.append(s)
    d = 1
    while len(out) < 3 and d < 40:
        m = ms[0]
        for nv in (int(m.group()) + d, int(m.group()) - d):
            s = ans[:m.start()] + str(nv) + ans[m.end():]
            if nv >= minv and (maxv is None or nv <= maxv) and s != ans and s not in out and len(out) < 3:
                out.append(s)
        d += 1
    return out


def pack(ask, v, ans, R, opts=None, **kw):
    if opts is None:
        clock = ('시' in ans and kw.get('clock'))
        opts = [ans] + variants(ans, R, first_only=bool(clock), minv=1 if clock else 0, maxv=12 if clock else None)
    opts = list(dict.fromkeys(opts))
    if len(opts) < 2:
        return None
    R.shuffle(opts)
    q = {'a': ask, 'v': v, 'c': opts, 'k': opts.index(ans)}
    if max(len(o) for o in opts) > 3:
        q['s'] = 1
    return q


def mag(text):
    nums = [int(x) for x in re.findall(r'\d+', text)]
    m = max(nums) if nums else 0
    return 0.8 if m >= 100 else 0.5 if m >= 50 else 0.25 if m >= 20 else 0


def score_gen(kind, q):
    txt = re.sub('<[^>]+>', ' ', q['a'] + ' ' + q['v'])
    return BASE.get(kind, 2) + mag(txt)


# ---------------------------------------------------------------- 종류별 문제 만들기
def from_gen(kind, R, seed_idx):
    for _ in range(40):
        it = gen._one(kind, R, seed_idx)
        if it is not None:
            return it
    return None


def render_gen(kind, R, seen):
    it = from_gen(kind, R, len(seen))
    if it is None:
        return None
    _, ans, key = it
    sig = (kind, key)
    if sig in seen:
        return None
    seen.add(sig)
    ask, v = '계산해 볼까요?', ''
    opts = None
    clock = False
    if kind in ('plus_small', 'plus_to20'):
        a, b = key
        v = big(f'{a} + {b} = ?')
    elif kind in ('plus_nocarry', 'plus_carry2'):
        t, u, b = key
        v = big(f'{t * 10 + u} + {b} = ?')
    elif kind in ('minus_small', 'minus_teen'):
        a, b = key
        v = big(f'{a} − {b} = ?')
    elif kind in ('minus_noborrow', 'minus_borrow2'):
        t, u, b = key
        v = big(f'{t * 10 + u} − {b} = ?')
    elif kind == 'plus_ten':
        v = big(f'10 + {key[0]} = ?')
    elif kind == 'tens_plus':
        t, b = key
        v = big(f'{t * 10} + {b} = ?')
    elif kind == 'tens_pm':
        a, b, f = key
        v = big(f'{a * 10} {"−" if f else "+"} {b * 10} = ?')
    elif kind == 'make10':
        ask, v = '□에 알맞은 수는?', big(f'{key[0]} + □ = 10')
    elif kind == 'blank_plus':
        ask, v = '□에 알맞은 수는?', big(f'{key[0]} + □ = {key[1]}')
    elif kind == 'blank_minus':
        ask, v = '□에 알맞은 수는?', big(f'{key[0]} − □ = {key[1]}')
    elif kind == 'blank2':
        ask, v = '□에 알맞은 수는?', big(f'{key[0]} + □ = {key[0] + int(ans)}')
    elif kind == 'triple':
        v = big(f'{key[0]} + {key[1]} + {key[2]} = ?')
    elif kind == 'same_add':
        v_, m = key
        v = big(' + '.join([str(v_)] * m) + ' = ?')
    elif kind == 'teen_ones':
        ask, v = '□에 알맞은 수는?', big(f'{key[0]} = 10과 □')
    elif kind == 'tens_ones':
        ask, v = f'{eun(key[0])} 십이 몇 개, 일이 몇 개일까요?', big(str(key[0]))
    elif kind == 'cmp':
        a, b = key
        ask, v = '더 큰 수는 무엇일까요?', big(f'{a} &nbsp; {b}')
        extra = [x for x in range(10, 100) if x not in (a, b, int(ans))]
        opts = [str(a), str(b)] + [str(x) for x in R.sample(extra, 2)]
    elif kind in ('next', 'hund'):
        a = key[0]
        ask, v = '빈칸에 알맞은 수는?', big(f'{a}, ?, {a + 2}')
    elif kind == 'tenmore':
        a, s = key
        ask = f'{a}보다 {abs(s)} {"큰" if s > 0 else "작은"} 수는 무엇일까요?'
    elif kind == 'skip':
        s, st = key
        seq = [st + s * j for j in range(5)]
        hole = seq.index(int(ans))
        ask = f'{s}씩 뛰어 세어요. 물음표에 알맞은 수는?'
        v = big(', '.join('?' if j == hole else str(x) for j, x in enumerate(seq)))
    elif kind == 'odd_even':
        ask, v = f'{eun(key[0])} 짝수일까요, 홀수일까요?', big(str(key[0]))
        opts = ['짝수', '홀수']
    elif kind == 'group':
        m, val = key
        ask = f'{val}개씩 {m}묶음이에요. 모두 몇 개일까요?'
        v = vis(''.join(f'<span class="grp">{"🍎" * val}</span>' for _ in range(m)))
    elif kind == 'share':
        g, each = key
        ask = f'콩 {g * each}개를 {g}접시에 똑같이 나누면 한 접시에 몇 개일까요?'
    elif kind in ('clock', 'clock_hour'):
        h, half = (key[0], key[1]) if kind == 'clock' else (key[0], False)
        ask, v, clock = '몇 시일까요?', vis(clock_svg(h, half)), True
    elif kind == 'min5':
        ask = f'긴 바늘이 {key[0]}을 가리켜요. 몇 분일까요?'
    elif kind == 'hour_later':
        ask, clock = f'{key[0]}시에서 {key[1]}시간 뒤는 몇 시일까요?', True
    elif kind == 'length':
        ask, v = '막대의 길이는 몇 cm일까요?', vis(ruler_svg(key[0]))
    elif kind == 'len_cmp':
        ask = f'{key[0]}cm 막대와 {key[1]}cm 막대가 있어요. 몇 cm 더 길까요?'
    elif kind == 'len_add':
        ask, v = '길이를 더해 보아요.', big(f'{key[0]}cm + {key[1]}cm = ?')
    elif kind == 'data_most':
        names = ['사과', '귤', '포도']
        ask, v = '가장 많은 것은 무엇일까요?', vis(table_html(names, key))
        opts = names[:]
    elif kind == 'data_diff':
        ask, v = '어느 쪽이 몇 개 더 많을까요? 차이는?', vis(table_html(['빨강', '파랑'], key))
    elif kind == 'shape_facts':
        (name, _), q = key
        ask = f'{name}의 {q}은 몇 개일까요?'
        v = vis({'세모': '🔺', '네모': '🟦', '동그라미': '🔵'}[name])
    else:
        return None
    return pack(ask, v, ans, R, opts, clock=clock)


def render_custom(kind, R, seen, b, top):
    SH = {'t': ('🔺', '세모', 3), 's': ('🟦', '네모', 4), 'c': ('🔵', '동그라미', 0)}
    top = max(top, 10)
    if kind == 'count':
        e, n = R.choice(EMO), R.randint(3, 9)
        sig = (kind, e, n)
        if sig in seen:
            return None
        seen.add(sig)
        return pack('모두 몇 개일까요?', vis(e * n), str(n), R)
    if kind == 'pattern':
        x, y, z, w = R.sample(EMO, 4)
        seqs = [[x, y, x, y, x], [x, x, y, x, x], [x, y, z, x, y]]
        i = R.randrange(3)
        seq, ans = seqs[i], [y, y, z][i]
        sig = (kind, tuple(seq), ans)
        if sig in seen:
            return None
        seen.add(sig)
        return pack('규칙을 찾아요. 물음표에 알맞은 것은?', vis(''.join(seq) + '❓'), ans, R, opts=[x, y, z, w])
    if kind == 'shape_name':
        k, t = R.choice([('변이 3개인 모양은?', 't'), ('꼭짓점이 4개인 모양은?', 's'), ('뾰족한 곳이 하나도 없는 모양은?', 'c')])
        seen.add((kind, t, len(seen)))
        opts = [f'{SH[x][0]} {SH[x][1]}' for x in SH]
        return pack(k, '', f'{SH[t][0]} {SH[t][1]}', R, opts=opts)
    if kind == 'shape_count':
        t, s = R.randint(1, 5), R.randint(1, 5)
        w = R.choice('ts')
        items = ['🔺'] * t + ['🟦'] * s
        R.shuffle(items)
        sig = (kind, tuple(items), w)
        if sig in seen:
            return None
        seen.add(sig)
        return pack(f'{SH[w][1]}는 모두 몇 개일까요?', vis(''.join(items)), str(t if w == 't' else s), R)
    if kind == 'shape_sides':
        w, side = R.choice('ts'), R.choice(['변', '꼭짓점'])
        sig = (kind, w, side)
        if sig in seen:
            return None
        seen.add(sig)
        return pack(f'{SH[w][1]}의 {side}은 몇 개일까요?', big(SH[w][0]), str(SH[w][2]), R)
    if kind == 'clue':
        lo = R.randint(2, max(3, top - 6))
        sig = (kind, lo)
        if sig in seen:
            return None
        seen.add(sig)
        v = f'<div class="ask" style="line-height:1.7">① {lo}보다 커요<br>② {lo + 3}보다 작아요<br>③ {eun(lo + 1)} 아니에요</div>'
        return pack('비밀 숫자를 찾아요!', v, str(lo + 2), R)
    if kind == 'between':
        a = R.randint(2, max(3, top - 9))
        c = a + R.randint(3, 6)
        sig = (kind, a, c)
        if sig in seen:
            return None
        seen.add(sig)
        return pack(f'{gwa(a)} {c} 사이에 있는 수는 모두 몇 개일까요?', big(f'{a} … {c}'), str(c - a - 1), R)
    if kind == 'two_step':  # a ± b ± c 두 번 계산
        a = R.randint(3, top - 2)
        o1, o2 = R.choice('+−'), R.choice('+−')
        b, c = R.randint(1, 9), R.randint(1, 9)
        r1 = a + b if o1 == '+' else a - b
        r2 = r1 + c if o2 == '+' else r1 - c
        if not (1 <= r1 <= top and 0 <= r2 <= top):
            return None
        sig = (kind, a, o1, b, o2, c)
        if sig in seen:
            return None
        seen.add(sig)
        return pack('앞에서부터 차례로 계산해요.', big(f'{a} {o1} {b} {o2} {c} = ?'), str(r2), R)
    if kind == 'compare_expr':
        a, b = R.randint(2, max(3, top // 2)), R.randint(2, max(3, top // 2))
        c, d = R.randint(2, max(3, top // 2)), R.randint(2, max(3, top // 2))
        l, r = a + b, c + d
        sig = (kind, a, b, c, d)
        if sig in seen or abs(l - r) > 6:
            return None
        seen.add(sig)
        ans = '>' if l > r else '<' if l < r else '='
        return pack('○ 안에 알맞은 기호는?', big(f'{a} + {b} ○ {c} + {d}'), ans, R, opts=['>', '<', '='])
    if kind == 'digit_cards':
        ds = R.sample(range(1, 10), 3)
        nums = sorted({x * 10 + y for x in ds for y in ds if x != y})
        if b <= 2:
            ask, ans = '카드 3장 중 2장으로 만든 두 자리 수 중 가장 큰 수는?', nums[-1]
        else:
            ask, ans = '카드 3장 중 2장으로 만든 두 자리 수 중 가장 큰 수와 가장 작은 수의 합은?', nums[-1] + nums[0]
        sig = (kind, tuple(sorted(ds)), b <= 2)
        if sig in seen:
            return None
        seen.add(sig)
        cards = ''.join(f'<span class="grp">{d}</span>' for d in ds)
        return pack(ask, vis(cards), str(ans), R)
    if kind == 'blank_two':
        b2, d2 = R.randint(1, 9), R.randint(1, 9)
        lo, hi = b2 + d2 + 1, min(max(top, 20), 40)
        if lo > hi:
            return None
        c2 = R.randint(lo, hi)
        sig = (kind, b2, c2, d2)
        if sig in seen:
            return None
        seen.add(sig)
        return pack('□에 알맞은 수는?', big(f'□ + {b2} = {c2} − {d2}'), str(c2 - d2 - b2), R)
    return None


def gen_pool(kinds, n, seed, b, top):
    """종류 목록에서 서로 다른 문제를 n개 만든다 (난이도 점수 '_s' 포함)."""
    out = []
    if not kinds:
        return out
    R = random.Random(seed)
    seen = set()
    guard = 0
    while len(out) < n and guard < n * 40:
        guard += 1
        k = kinds[len(out) % len(kinds)] if guard % 3 else R.choice(kinds)
        q = render_custom(k, R, seen, b, top) if k in CUSTOM else render_gen(k, R, seen)
        if q:
            q['_s'] = score_gen(k, q)
            out.append(q)
    return out


# ---------------------------------------------------------------- 글 문제 -> 퀴즈
def convert_item(q, a, R, field):
    s = a.strip()
    base = ITEM_BASE[field] + 0.5 * min(len(q), 80) / 80 + mag(q)
    for w, o in PAIRS:
        if s.startswith(w):
            opts = [w, o]
            R.shuffle(opts)
            return {'a': q, 'v': '', 'c': opts, 'k': opts.index(w), 's': 1, '_s': base - 0.3}
    t = re.sub(r'\s*\([^)]*\)\s*$', '', s)
    if re.fullmatch(r'[\d+\-−×÷\s]+=\s*\d+', t):
        t = t.split('=')[-1].strip()
    ok = (re.fullmatch(r'\d+\s?[가-힣a-zA-Z]{0,3}', t)
          or re.fullmatch(r'\d+시( \d+분)?', t)
          or re.fullmatch(r'\d+[가-힣a-zA-Z]{0,2}(,\s*\d+[가-힣a-zA-Z]{0,2}){1,3}', t))
    if ok:
        clock = '시' in t and '분' not in t
        r = pack(q, '', t, R, clock=clock)
        if r:
            r['_s'] = base
            return r
    return {'a': q, 'v': '', 'd': s, '_s': base + 0.5}  # 아빠와 함께 풀기 카드


# ---------------------------------------------------------------- 주차 데이터
def top_of(b, title, rng):
    nums = [int(x) for x in re.findall(r'(\d+)(?!\s*권)', rng) if int(x) >= 5]
    if nums:
        return max(nums)
    if TITLE_MEASURE_RE.search(title + ' ' + rng):
        return 30
    return 100


def week_data(b):
    out = []
    for wk in CONTENT[b].WEEKS:
        w = wk['n']
        if b == 1:
            src = BOOK1[w]
            c = src['c']
            items = {f: list(src[f]) for f in ('think', 'apply', 'grade', 'olymp')}
            items['concept'] = []
        else:
            src = P[b][w]
            c = src['c']
            items = {f: [src[f]] for f in ('think', 'apply', 'grade', 'olymp', 'concept')}
            for f, lst in X[b][w].items():
                items[f] += list(lst)
        out.append(dict(b=b, w=w, g=(b - 1) * WEEKS + (w - 1), title=wk['title'], rng=wk['rng'], c=c,
                        items=items, top=top_of(b, wk['title'], wk['rng'])))
    return out


def number_kinds(c):
    return [k for k in c if k not in MEASURE and k != 'skip']


def assign_levels(pool):
    """영역별로 난이도 점수 순위를 5단계(1~5)로 나눈다."""
    for cat in CATS:
        qs = sorted([q for q in pool if q['t'] == cat], key=lambda q: q['_s'])
        n = len(qs)
        for i, q in enumerate(qs):
            q['l'] = min(5, 1 + (i * 5) // max(n, 1))
    for q in pool:
        del q['_s']


def build_week(v, allv, review):
    b, w, g = v['b'], v['w'], v['g']
    R = random.Random(f'{b}-{w}')
    seed = f'{b}-{w}'
    top = v['top']
    nk = number_kinds(v['c'])
    mk = [k for k in v['c'] if k in MEASURE]
    sk = [k for k in v['c'] if k == 'skip']
    curr_k = nk[2] if len(nk) >= 3 else None
    calc_ks = [k for i, k in enumerate(nk) if not (len(nk) >= 3 and i == 2)] or review[:4]
    nxt = []
    for later in allv[g + 1:]:
        nxt = number_kinds(later['c'])
        if nxt:
            break
    if not nxt:
        nxt = ['plus_carry2', 'minus_borrow2', 'same_add']
    conv = {f: [(convert_item(q, a, R, f), f) for q, a in lst] for f, lst in v['items'].items()}

    def items_of(fields, measure):
        out = []
        for f in fields:
            for q, _ in conv[f]:
                if bool(MEASURE_RE.search(q['a'])) == measure:
                    out.append(q)
        return out

    pools = {c_: [] for c_ in CATS}
    hard = ['two_step', 'compare_expr', 'blank_two'] if not TITLE_MEASURE_RE.search(v['title']) else ['two_step']
    pools['calc'] = (gen_pool(calc_ks, 18, seed + 'calc', b, top)
                     + [q for q in items_of(['apply'], False) if 'd' not in q]
                     + gen_pool(hard, 8, seed + 'hardcalc', b, top))
    pools['curr'] = (gen_pool([curr_k] if curr_k else [], 12, seed + 'curr', b, top)
                     + items_of(['concept', 'grade'], False))
    if b == 1 and w <= 3:
        pools['curr'] += gen_pool(['count'], 8, seed + 'cnt', b, top)
    pools['ahead'] = gen_pool([k for k in nxt if k not in MEASURE][:3] or nxt, 18, seed + 'ahead', b, top)
    pools['shape'] = (gen_pool(mk, 14, seed + 'shape', b, top)
                      + items_of(['apply', 'grade', 'concept', 'think', 'olymp'], True))
    if b <= 3 or sum('d' not in q for q in pools['shape']) < 5:
        pools['shape'] += gen_pool(['shape_name', 'shape_count', 'shape_sides'], 10, seed + 'sh2', b, top)
    pools['think'] = items_of(['think'], False) + gen_pool(sk, 10, seed + 'skip', b, top)
    pools['think'] += gen_pool(['pattern'], 6, seed + 'pat', b, top)
    if sum('d' not in q for q in pools['think']) < 8:
        pools['think'] += gen_pool(['skip', 'digit_cards'], 8, seed + 'skp', b, top)
    pools['deep'] = items_of(['olymp'], False)
    pools['deep'] += gen_pool(['between', 'clue', 'digit_cards'], 10, seed + 'deep', b, top)
    flat = []
    for cat, lst in pools.items():
        uniq, seen = [], set()
        for q in lst:
            key = q['a'] + q.get('v', '')
            if key not in seen:
                seen.add(key)
                uniq.append(q)
        choice = [q for q in uniq if 'd' not in q]
        dad = [q for q in uniq if 'd' in q] if cat in ('think', 'deep', 'curr') else []
        if len(choice) < 6:  # 비는 영역은 같은 권의 계산 종류로 복습 문제를 채운다
            extra = gen_pool([k for k in review if k not in nk][:4] or review[:4], 8, seed + cat + 'rev', b, top)
            choice += [q for q in extra if q['a'] + q.get('v', '') not in seen]
        if not choice:
            raise SystemExit(f'문제 풀이 비었습니다: {b}권 {w}주 {cat}')
        for q in choice[:26] + dad[:4]:
            q['t'] = cat
            flat.append(q)
    assign_levels(flat)
    return flat


def build():
    allv = [v for b in range(1, NBOOKS + 1) for v in week_data(b)]
    weeks = [None] * len(allv)
    for b in range(1, NBOOKS + 1):
        vs = [v for v in allv if v['b'] == b]
        review = []
        for v in vs:
            review += [k for k in number_kinds(v['c']) if k not in review]
        for v in vs:
            weeks[v['g']] = {'q': build_week(v, allv, review)}
    books = []
    for b in range(1, NBOOKS + 1):
        vs = [v for v in allv if v['b'] == b]
        villages = []
        # 12주를 30개 마을에 나눠 담는다 (한 주에 2~3개 마을)
        owner = [k * WEEKS // VILLAGES for k in range(VILLAGES)]
        for k in range(VILLAGES):
            wi = owner[k]
            v = vs[wi]
            same = [x for x in range(VILLAGES) if owner[x] == wi]
            j, m = same.index(k), len(same)
            icon = ICONS[wi % 12]
            if '졸업' in v['title']:
                icon = '🎓'
            elif '시계' in v['title'] or '시간' in v['title']:
                icon = '⏰'
            elif '그래프' in v['title'] or '자료' in v['title']:
                icon = '📊'
            elif v['title'].startswith('자 '):
                icon = '📏'
            villages.append(dict(t=v['title'] + (SUFFIX[j] if m > 1 else ''), r=v['rng'], i=icon, g=v['g'], j=j, m=m))
        books.append(dict(n=b, title=BOOK_INFO[b][0], sub=BOOK_INFO[b][1], v=villages))
    return {'books': books, 'weeks': weeks}


def main():
    data = build()
    out = os.path.join(ROOT, 'data')
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, 'quiz.js')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('window.EW=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    total = sum(len(w['q']) for w in data['weeks'])
    print(f'{path}  ({os.path.getsize(path) // 1024}KB, 문제 {total}개, 주차 풀 {len(data["weeks"])}개, '
          f'마을 {sum(len(b["v"]) for b in data["books"])}개)')


if __name__ == '__main__':
    main()
