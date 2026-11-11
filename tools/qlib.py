"""퀴즈 문제 만들기 부품: 책의 문제 생성기(gen.py)와 문제 틀(fam.py)에서 보기 있는 터치 문제를 만든다.

문제 하나의 모양 (data/quiz.js 에 그대로 저장)
  a 질문 글, v 그림/수식(HTML), c 보기 목록, k 정답 번호, s 작은 글씨, w 보기를 2열로,
  d 아빠와 함께 확인하는 카드의 정답 글(이 경우 c, k 없음), t 영역, l 난이도 단계(1~5)
"""
import hashlib
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CODE = os.environ.get('EW_CODE') or os.path.join(ROOT, 'eunwoo_math_code')
sys.path.insert(0, CODE)
sys.path.insert(0, HERE)

import gen  # noqa: E402

# 도형·측정 영역으로 보내는 문제 종류
MEASURE = {'clock', 'clock_hour', 'min5', 'hour_later', 'length', 'len_cmp', 'len_add', 'shape_facts',
           'data_most', 'data_diff', 'angle_add', 'angle_tri', 'perim', 'area_rect', 'area_tri', 'vol',
           'len_m_cm', 'len_unit', 'time_min', 'sec_time'}
MEASURE_RE = re.compile(r'(시계|바늘|\d\s?시|\d\s?분|시간|cm|길이|모양|세모|네모|동그라미|변이|꼭짓점|도형|표에서|그래프|자를'
                        r'|각도|°|넓이|둘레|부피|직사각형|삼각형|정사각형|직육면체|km|\bm\b)')
TITLE_MEASURE_RE = re.compile(r'(시계|시간|도형|자료|규칙|그래프|cm|어림|^자 |길이|각도|넓이|둘레|부피|표)')
EMO = ['🍎', '🐟', '⭐', '🌸', '🍓', '🐥']
CATS = ['calc', 'think', 'shape', 'curr', 'ahead', 'deep']
CUSTOM = ('count', 'pattern', 'shape_name', 'shape_count', 'shape_sides', 'clue', 'between',
          'two_step', 'compare_expr', 'digit_cards', 'blank_two')
PAIRS = [('될 수 없어요', '될 수 있어요'), ('될 수 있어요', '될 수 없어요'), ('같아요', '달라요'), ('달라요', '같아요'),
         ('있어요', '없어요'), ('없어요', '있어요'), ('맞아요', '틀려요'), ('틀려요', '맞아요'),
         ('아니요', '네'), ('네', '아니요'), ('예', '아니요')]

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
    # v2 에서 추가된 종류
    'jump_plus': 1.2, 'jump_minus': 1.5, 'story_add': 1.8, 'story_sub': 2.0, 'story_diff': 2.2, 'cmp_sym': 1.4,
    'tri_sum': 2.2, 'tri_mix': 2.6, 'add2_c': 2.6, 'sub2_b': 2.8, 'two_add_nc': 2.0, 'two_sub_nb': 2.1,
    'hundreds': 1.8, 'cmp3': 1.5, 'pat_num': 2.6, 'group_mul': 2.2, 'mul_story': 2.4, 'times_more': 2.4,
    'mul_eq': 2.4, 'mul_eq_s': 2.2, 'mul_blank': 2.8, 'add3': 3.0, 'sub3': 3.2, 'mul_21': 3.2, 'div_eq': 2.8,
    'div_story': 2.8, 'div_rem': 3.4, 'frac_read': 2.6, 'frac_of': 3.0, 'frac_cmp': 3.0, 'len_unit': 2.6,
    'len_m_cm': 2.4, 'time_min': 2.6, 'sec_time': 3.0, 'perim': 2.8, 'big_read': 2.6, 'mul_32': 3.8,
    'div_32': 3.8, 'angle_add': 2.4, 'angle_tri': 3.0, 'frac_add_same': 3.0, 'frac_sub_same': 3.0,
    'frac_mixed': 3.4, 'dec_cmp': 2.8, 'dec_add1': 3.0, 'dec2_add': 3.4, 'dec2_sub': 3.6, 'corr': 3.6,
    'area_rect': 3.0, 'order_ops': 3.4, 'divisors': 3.2, 'multiples': 3.0, 'gcd': 3.6, 'lcm': 3.6,
    'reduce': 3.6, 'frac_add_diff': 4.0, 'frac_mul_int': 3.6, 'dec_mul': 3.8, 'avg': 3.4, 'area_tri': 3.4,
    'vol': 3.6, 'ratio': 3.4, 'prop': 3.6, 'speed': 3.4,
}
ITEM_BASE = {'concept': 1.5, 'grade': 2, 'apply': 3, 'think': 3.5, 'olymp': 4.5}
# 답이 하나로 정해지지 않는 열린 문제의 표현
OPEN_Q = re.compile(r'(만드세요|만들어 ?보세요|내가 만든|만들고 답|예를 들어|여러 가지로 말|말해 보세요|설명하세요|설명해 보세요)')


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
    while len(out) < 3 and d < 60:
        m = ms[0]
        for nv in (int(m.group()) + d, int(m.group()) - d):
            s = ans[:m.start()] + str(nv) + ans[m.end():]
            if nv >= minv and (maxv is None or nv <= maxv) and s != ans and s not in out and len(out) < 3:
                out.append(s)
        d += 1
    return out


def flags(q, opts):
    m = max(len(o) for o in opts)
    if m > 3:
        q['s'] = 1
    if m > 9:
        q['w'] = 1
    return q


def pack(ask, v, ans, R, opts=None, **kw):
    if opts is None:
        clock = ('시' in ans and kw.get('clock'))
        opts = [ans] + variants(ans, R, first_only=bool(clock), minv=1 if clock else 0, maxv=12 if clock else None)
    opts = list(dict.fromkeys(opts))
    if len(opts) < 2:
        return None
    R.shuffle(opts)
    return flags({'a': ask, 'v': v, 'c': opts, 'k': opts.index(ans)}, opts)


def mag(text):
    nums = [int(x) for x in re.findall(r'\d+', text)]
    m = max(nums) if nums else 0
    return 0.8 if m >= 100 else 0.5 if m >= 50 else 0.25 if m >= 20 else 0


def score_gen(kind, q):
    txt = re.sub('<[^>]+>', ' ', q['a'] + ' ' + q['v'])
    return BASE.get(kind, 2.5) + mag(txt)


def sigof(q):
    """같은 문제인지 가리는 지문: 질문 + 그림(원본 HTML). 정답이 달라도 질문이 같으면 같은 문제로 본다."""
    return hashlib.md5((q['a'] + '|' + q.get('v', '')).encode('utf-8')).hexdigest()


# ---------------------------------------------------------------- 종류별 문제 만들기
def from_gen(kind, R, seed_idx):
    for _ in range(40):
        it = gen._one(kind, R, seed_idx)
        if it is not None and it is not NotImplemented:
            return it
    return None


def render_gen(kind, R, seen):
    it = from_gen(kind, R, len(seen))
    if it is None:
        return None
    html, ans, key = it
    sig = (kind, repr(key))
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
        # v2 에서 추가된 종류: 생성기가 만든 수식·글 그림을 그대로 크게 보여 준다
        ask, v = '풀어 볼까요?', f'<div class="gz">{html}</div>'
        clock = kind in ('time_min', 'sec_time')
        if kind == 'cmp_sym':
            ask, opts = '○ 안에 알맞은 기호는?', ['>', '<', '=']
        elif kind == 'cmp3':
            a, b = key[0], key[1]
            ask = '더 큰 수는 무엇일까요?'
            extra = sorted({int(ans) + d for d in (-11, -7, 7, 11, 13) if int(ans) + d > 0})
            opts = [str(a), str(b)] + [str(x) for x in R.sample(extra, 2)]
        elif kind == 'dec_cmp':
            a, b = key[0], key[1]
            ask = '더 큰 수는 무엇일까요?'
            extra = [x for x in (round(float(ans) + d, 1) for d in (-1.1, -0.3, 0.2, 0.6, 1.3)) if x > 0 and str(x) not in (str(a), str(b))]
            opts = [str(a), str(b)] + [str(x) for x in R.sample(extra, 2)]
        elif kind == 'frac_cmp':
            d, n1, n2 = key[0], key[1], key[2]
            ask = '더 큰 분수는 무엇일까요?'
            extra = [f'{n}/{d}' for n in range(1, d + 2) if n not in (n1, n2)]
            opts = [f'{n1}/{d}', f'{n2}/{d}'] + R.sample(extra, min(2, len(extra)))
    ans_c = re.sub(r'\s*\([^)]*\)\s*$', '', ans)  # 정답 뒤의 설명 괄호는 뺀다
    return pack(ask, v, ans_c, R, opts, clock=clock)


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
        sig = (kind, t)
        if sig in seen:
            return None
        seen.add(sig)
        opts = [f'{SH[x][0]} {SH[x][1]}' for x in SH]
        return pack(k, '', f'{SH[t][0]} {SH[t][1]}', R, opts=opts)
    if kind == 'shape_count':
        t, s = R.randint(1, 6), R.randint(1, 6)
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
        b2, c = R.randint(1, 9), R.randint(1, 9)
        r1 = a + b2 if o1 == '+' else a - b2
        r2 = r1 + c if o2 == '+' else r1 - c
        if not (1 <= r1 <= top and 0 <= r2 <= top):
            return None
        sig = (kind, a, o1, b2, o2, c)
        if sig in seen:
            return None
        seen.add(sig)
        return pack('앞에서부터 차례로 계산해요.', big(f'{a} {o1} {b2} {o2} {c} = ?'), str(r2), R)
    if kind == 'compare_expr':
        a, b2 = R.randint(2, max(3, top // 2)), R.randint(2, max(3, top // 2))
        c, d = R.randint(2, max(3, top // 2)), R.randint(2, max(3, top // 2))
        l, r = a + b2, c + d
        sig = (kind, a, b2, c, d)
        if sig in seen or abs(l - r) > 6:
            return None
        seen.add(sig)
        ans = '>' if l > r else '<' if l < r else '='
        return pack('○ 안에 알맞은 기호는?', big(f'{a} + {b2} ○ {c} + {d}'), ans, R, opts=['>', '<', '='])
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
def _clean(a):
    return re.sub(r'\s*\([^)]*\)\s*$', '', a.strip())


def convert_item(q, a, R, field):
    """(문제, 정답 글) 하나를 보기 문제로 바꾼다. 숫자·짝 고르기 형태가 아니면 아빠 확인 카드로 둔다."""
    s = a.strip()
    base = ITEM_BASE[field] + 0.5 * min(len(q), 80) / 80 + mag(q)
    if OPEN_Q.search(q) or re.match(r'^예\s*[:)]', s):  # 정답이 하나로 정해지지 않는 열린 문제는 아빠 확인 카드로
        return {'a': q, 'v': '', 'd': s, '_s': base + 0.5, 'open': 1}
    for w, o in PAIRS:
        if re.match('^' + re.escape(w) + r'(?![가-힣:])', s):  # '예: …' 같은 설명형 답은 제외
            opts = [w, o]
            R.shuffle(opts)
            return {'a': q, 'v': '', 'c': opts, 'k': opts.index(w), 's': 1, '_s': base - 0.3}
    t = _clean(s)
    if re.fullmatch(r'[\d+\-−×÷\s]+=\s*\d+', t):
        t = t.split('=')[-1].strip()
    ok = (re.fullmatch(r'\d+\s?[가-힣a-zA-Z]{0,3}', t)
          or re.fullmatch(r'\d+시( \d+분)?', t)
          or re.fullmatch(r'\d+[가-힣a-zA-Z]{0,2}(,\s*\d+[가-힣a-zA-Z]{0,2}){1,3}', t))
    if ok:
        num = re.match(r'\d+(\.\d+)?', t)
        if num and re.search(r'(?<![\d.])' + re.escape(num.group()) + r'(?![\d.])', q):
            return None  # 정답이 문제에 이미 나온 수와 같으면(열린 문제) 보기 문제로 쓰지 않는다
        clock = '시' in t and '분' not in t
        r = pack(q, '', t, R, clock=clock)
        if r:
            r['_s'] = base
            return r
    return {'a': q, 'v': '', 'd': s, '_s': base + 0.5}  # 아빠와 함께 풀기 카드


def convert_family(insts, field, R):
    """같은 문제 틀에서 뽑은 (문제, 정답) 목록을 퀴즈 문제 목록으로 바꾼다.
    숫자형이 아닌 정답은 같은 틀의 다른 문제 정답을 오답 보기로 쓴다."""
    out = []
    answers = list(dict.fromkeys(_clean(a) for _, a in insts))
    for q, a in insts:
        item = convert_item(q, a, R, field)
        if item is None:
            continue
        if 'd' in item and not item.get('open'):
            clean = _clean(a)
            others = [x for x in answers if x != clean]
            if clean and len(clean) <= 40 and len(others) >= 3 and '아이 말' not in a:
                opts = [clean] + R.sample(others, 3)
                R.shuffle(opts)
                item = flags({'a': q, 'v': '', 'c': opts, 'k': opts.index(clean), '_s': item['_s'] - 0.4}, opts)
        out.append(item)
    return out
