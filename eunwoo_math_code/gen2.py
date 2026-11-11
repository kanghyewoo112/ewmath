"""6~10권(초1~초5)용 추가 생성 종류. 정답은 모두 코드로 계산한다."""
from lib import *
from math import gcd

S = 19


def _e(*parts, s=S):
    return eq(*[str(x) for x in parts], size=s)


def _t(s, size=15):
    return txt(s, size, True, INK, True)


def lcm(a, b):
    return a * b // gcd(a, b)


def _frac(n, d):
    return f'<span style="display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;line-height:1.05;margin:0 2px"><span style="border-bottom:2px solid #2B2A33;padding:0 3px">{n}</span><span>{d}</span></span>'


def _ft(parts, size=19):
    """parts: 문자열/분수 튜플(n,d)의 리스트를 한 줄로"""
    out = ''
    for x in parts:
        out += _frac(*x) if isinstance(x, tuple) else f'<span style="margin:0 4px">{x}</span>'
    return f'<div style="font-family:Jua;font-size:{size}px;display:flex;align-items:center;flex-wrap:wrap">{out}</div>'


def one2(k, R, i):
    # ---- 초1 ----
    if k == 'jump_minus':
        a = R.randint(11, 19); b = R.randint(2, 9)
        if a - b < 1: return None
        return _t(f'수직선에서 {a}에서 왼쪽으로 {b}칸 가면 □', 15), str(a - b), (a, b)
    if k == 'jump_plus':
        a = R.randint(3, 12); b = R.randint(3, 9)
        return _t(f'수직선에서 {a}에서 오른쪽으로 {b}칸 가면 □', 15), str(a + b), (a, b)
    if k == 'story_add':
        a = R.randint(5, 40); b = R.randint(3, 30); n = R.choice(['사과', '구슬', '스티커', '색종이'])
        return _t(f'{n} {a}개에 {b}개가 더 생겼어요. 모두 □개', 14), f'{a + b}개', (a, b, n)
    if k == 'story_sub':
        a = R.randint(12, 60); b = R.randint(3, a - 2); n = R.choice(['사탕', '풍선', '쿠키', '귤'])
        return _t(f'{n} {a}개 중 {b}개를 먹었어요. 남은 것 □개', 14), f'{a - b}개', (a, b, n)
    if k == 'story_diff':
        a = R.randint(10, 50); b = R.randint(5, a - 1)
        return _t(f'은우 {a}개, 친구 {b}개. 은우가 □개 더 많아요', 14), f'{a - b}개', (a, b)
    if k == 'cmp_sym':
        a = R.randint(10, 99); b = R.randint(10, 99)
        return _t(f'{a} ○ {b}  (>, <, = 중 하나)', 16), ('>' if a > b else '<' if a < b else '='), (a, b)
    if k == 'tri_sum':
        a = R.randint(3, 15); b = R.randint(3, 15); c = R.randint(2, 12)
        return _e(a, '+', b, '+', c, '=', '□'), str(a + b + c), (a, b, c)
    if k == 'tri_mix':
        a = R.randint(10, 20); b = R.randint(2, 9); c = R.randint(2, 9)
        if a - b + c < 1: return None
        return _e(a, '−', b, '+', c, '=', '□'), str(a - b + c), (a, b, c)
    if k == 'pat_num':
        s = R.choice([2, 3, 4, 5, 10]); st = R.randint(1, 20); seq = [st + s * j for j in range(5)]
        h_ = R.randint(1, 4); ans = seq[h_]; seq[h_] = ''
        return row(numstrip(seq, 32), 8, False), str(ans), (s, st, h_)
    if k == 'two_add_nc':
        a = R.randint(11, 70); b = R.randint(11, 28)
        if (a % 10) + (b % 10) >= 10 or a + b > 99: return None
        return _e(a, '+', b, '=', '□'), str(a + b), (a, b)
    if k == 'two_sub_nb':
        a = R.randint(31, 99); b = R.randint(11, a - 10)
        if (a % 10) < (b % 10): return None
        return _e(a, '−', b, '=', '□'), str(a - b), (a, b)
    # ---- 초2 ----
    if k == 'mul_eq':
        a = R.randint(2, 9); b = R.randint(2, 9); return _e(a, '×', b, '=', '□'), str(a * b), (a, b)
    if k == 'mul_eq_s':
        a = R.choice([2, 3, 4, 5]); b = R.randint(2, 9); return _e(a, '×', b, '=', '□'), str(a * b), (a, b)
    if k == 'mul_blank':
        a = R.randint(2, 9); b = R.randint(2, 9); return _e('□', '×', b, '=', a * b), str(a), (a, b)
    if k == 'group_mul':
        a = R.randint(2, 9); b = R.randint(2, 9)
        return _t(f'{a}씩 {b}묶음은 □  ( {a} × {b} )', 14), str(a * b), (a, b)
    if k == 'times_more':
        a = R.randint(2, 9); b = R.randint(2, 6); return _t(f'{a}의 {b}배는 □', 16), str(a * b), (a, b)
    if k == 'hundreds':
        a = R.randint(101, 999)
        if a % 10 == 0: return None
        return _t(f'{a} = □백 □십 □일', 16), f'{a // 100}백 {a // 10 % 10}십 {a % 10}일', (a,)
    if k == 'cmp3':
        a = R.randint(100, 999); b = R.randint(100, 999)
        if a == b: return None
        return _t(f'{a} 와 {b} 중 더 큰 수는?', 15), str(max(a, b)), (a, b)
    if k == 'add2_c':
        a = R.randint(15, 79); b = R.randint(15, 79)
        if (a % 10) + (b % 10) < 10 or a + b > 150: return None
        return _e(a, '+', b, '=', '□'), str(a + b), (a, b)
    if k == 'sub2_b':
        a = R.randint(32, 99); b = R.randint(15, a - 5)
        if (a % 10) >= (b % 10): return None
        return _e(a, '−', b, '=', '□'), str(a - b), (a, b)
    if k == 'len_m_cm':
        m = R.randint(1, 5); c = R.randint(5, 95)
        return _t(f'{m}m {c}cm = □cm', 16), str(m * 100 + c), (m, c)
    if k == 'time_min':
        h_ = R.randint(1, 10); m = R.choice([10, 15, 20, 30, 40]); d = R.choice([10, 20, 30])
        t = m + d; hh = h_ + t // 60; mm = t % 60
        return _t(f'{h_}시 {m}분에서 {d}분 뒤는 □시 □분', 14), f'{hh}시 {mm}분', (h_, m, d)
    if k == 'mul_story':
        a = R.randint(2, 6); b = R.randint(2, 9); n = R.choice(['접시', '봉지', '상자'])
        return _t(f'{n} {a}개에 {b}개씩 담으면 모두 □개', 14), f'{a * b}개', (a, b, n)
    # ---- 초3 ----
    if k == 'div_eq':
        a = R.randint(2, 9); b = R.randint(2, 9); return _e(a * b, '÷', a, '=', '□'), str(b), (a, b)
    if k == 'div_story':
        a = R.randint(2, 8); b = R.randint(2, 9); n = R.choice(['사탕', '구슬', '쿠키'])
        return _t(f'{n} {a * b}개를 {a}명에게 똑같이 나누면 한 명에 □개', 14), f'{b}개', (a, b, n)
    if k == 'div_rem':
        d = R.randint(3, 9); q = R.randint(3, 9); r = R.randint(1, d - 1)
        return _t(f'{d * q + r} ÷ {d} = □ … □', 16), f'{q} … {r}', (d, q, r)
    if k == 'mul_21':
        a = R.randint(12, 49); b = R.randint(2, 9); return _e(a, '×', b, '=', '□'), str(a * b), (a, b)
    if k == 'add3':
        a = R.randint(120, 640); b = R.randint(120, 340); return _e(a, '+', b, '=', '□'), str(a + b), (a, b)
    if k == 'sub3':
        a = R.randint(300, 900); b = R.randint(110, a - 100); return _e(a, '−', b, '=', '□'), str(a - b), (a, b)
    if k == 'frac_read':
        d = R.randint(2, 8); n = R.randint(1, d - 1)
        return _t(f'전체를 {d}로 똑같이 나눈 것 중 {n}만큼은 분수로 □/□', 14), f'{n}/{d}', (d, n)
    if k == 'frac_cmp':
        d = R.randint(3, 12); a = R.randint(1, d - 1); b = R.randint(1, d - 1)
        if a == b: return None
        return _ft([(a, d), '와', (b, d), ' 중 더 큰 것은?'], 17), f'{max(a, b)}/{d}', (d, a, b)
    if k == 'frac_of':
        d = R.choice([2, 3, 4, 5, 6]); n = R.randint(2, 6)
        return _t(f'{d * n}의 1/{d} 은 □', 16), str(n), (d, n)
    if k == 'dec_cmp':
        a = R.randint(1, 99) / 10; b = R.randint(1, 99) / 10
        if a == b: return None
        return _t(f'{a} 와 {b} 중 더 큰 수는?', 15), str(max(a, b)), (a, b)
    if k == 'dec_add1':
        a = R.randint(1, 49); b = R.randint(1, 49)
        return _t(f'{a / 10} + {b / 10} = □', 17), f'{(a + b) / 10:g}', (a, b)
    if k == 'len_unit':
        km = R.randint(1, 9); m = R.choice([100, 200, 300, 500, 750])
        return _t(f'{km}km {m}m = □m', 16), str(km * 1000 + m), (km, m)
    if k == 'sec_time':
        m = R.randint(1, 4); s = R.choice([20, 30, 40, 50]); d = R.choice([30, 40, 50, 70])
        t = m * 60 + s + d
        return _t(f'{m}분 {s}초 + {d}초 = □분 □초', 15), f'{t // 60}분 {t % 60}초', (m, s, d)
    # ---- 초4 ----
    if k == 'big_read':
        a = R.randint(1, 9) * 10000 + R.randint(1, 9) * 1000 + R.randint(0, 9) * 100
        return _t(f'{a:,} 에서 만의 자리 숫자는 □', 15), str(a // 10000), (a,)
    if k == 'mul_32':
        a = R.randint(120, 480); b = R.randint(11, 39); return _e(a, '×', b, '=', '□'), str(a * b), (a, b)
    if k == 'div_32':
        b = R.randint(12, 49); q = R.randint(3, 19); return _e(b * q, '÷', b, '=', '□'), str(q), (b, q)
    if k == 'angle_tri':
        a = R.randint(30, 80); b = R.randint(30, 80)
        if a + b > 150: return None
        return _t(f'삼각형의 두 각이 {a}°, {b}°. 나머지 한 각은 □°', 14), f'{180 - a - b}°', (a, b)
    if k == 'angle_add':
        a = R.randint(20, 90); b = R.randint(20, 90)
        return _t(f'{a}° + {b}° = □°', 17), f'{a + b}°', (a, b)
    if k == 'frac_add_same':
        d = R.randint(5, 12); a = R.randint(1, d - 2); b = R.randint(1, d - a - 1)
        return _ft([(a, d), '+', (b, d), '= □/□'], 17), f'{a + b}/{d}', (d, a, b)
    if k == 'frac_sub_same':
        d = R.randint(5, 12); a = R.randint(3, d - 1); b = R.randint(1, a - 1)
        return _ft([(a, d), '−', (b, d), '= □/□'], 17), f'{a - b}/{d}', (d, a, b)
    if k == 'frac_mixed':
        d = R.randint(2, 6); w = R.randint(1, 4); n = R.randint(1, d - 1)
        return _t(f'{w}과 {n}/{d}를 가분수로: □/{d}', 15), f'{w * d + n}/{d}', (d, w, n)
    if k == 'dec2_add':
        a = R.randint(101, 899); b = R.randint(101, 899)
        return _t(f'{a / 100:.2f} + {b / 100:.2f} = □', 16), f'{(a + b) / 100:g}', (a, b)
    if k == 'dec2_sub':
        a = R.randint(300, 999); b = R.randint(101, a - 50)
        return _t(f'{a / 100:.2f} − {b / 100:.2f} = □', 16), f'{(a - b) / 100:g}', (a, b)
    if k == 'corr':
        m = R.randint(2, 5); c = R.randint(0, 3); x = R.randint(2, 9)
        return _t(f'y = {m}×x + {c} 일 때 x = {x}이면 y = □', 15), str(m * x + c), (m, c, x)
    if k == 'perim':
        a = R.randint(3, 15); b = R.randint(2, 12)
        return _t(f'가로 {a}cm, 세로 {b}cm인 직사각형의 둘레는 □cm', 14), str(2 * (a + b)), (a, b)
    if k == 'order_ops':
        a = R.randint(2, 20); b = R.randint(2, 9); c = R.randint(2, 9)
        return _e(a, '+', b, '×', c, '=', '□'), str(a + b * c), (a, b, c)
    if k == 'order_ops2':
        a = R.randint(20, 60); b = R.randint(2, 6); c = R.randint(2, 9); d = R.randint(2, 9)
        if a - b * c < 1: return None
        return _e(a, '−', b, '×', c, '+', d, '=', '□'), str(a - b * c + d), (a, b, c, d)
    # ---- 초5 ----
    if k == 'divisors':
        n = R.choice([12, 16, 18, 20, 24, 28, 30, 36, 40, 42, 48])
        ds = [d for d in range(1, n + 1) if n % d == 0]
        return _t(f'{n}의 약수는 모두 몇 개?', 15), f'{len(ds)}개 ({", ".join(map(str, ds))})', (n,)
    if k == 'multiples':
        a = R.randint(3, 9); n = R.randint(4, 8)
        return _t(f'{a}의 배수 중 {n}번째로 작은 수는?', 15), str(a * n), (a, n)
    if k == 'gcd':
        g = R.choice([2, 3, 4, 5, 6, 7]); a = g * R.randint(2, 8); b = g * R.randint(2, 8)
        if a == b or gcd(a, b) != g: return None
        return _t(f'{a}와 {b}의 최대공약수는?', 15), str(g), (a, b)
    if k == 'lcm':
        a = R.randint(2, 9); b = R.randint(2, 9)
        if a == b: return None
        return _t(f'{a}와 {b}의 최소공배수는?', 15), str(lcm(a, b)), (a, b)
    if k == 'reduce':
        g = R.randint(2, 6); n = R.randint(1, 5); d = R.randint(n + 1, 8)
        if gcd(n, d) != 1: return None
        return _ft([(n * g, d * g), '를 약분하면 □/□'], 17), f'{n}/{d}', (g, n, d)
    if k == 'frac_add_diff':
        d1 = R.choice([2, 3, 4, 5, 6]); d2 = R.choice([2, 3, 4, 5, 6])
        if d1 == d2: return None
        a = R.randint(1, d1 - 1); b = R.randint(1, d2 - 1); L = lcm(d1, d2)
        n = a * (L // d1) + b * (L // d2); g = gcd(n, L)
        return _ft([(a, d1), '+', (b, d2), '= □/□ (약분)'], 17), f'{n // g}/{L // g}', (a, d1, b, d2)
    if k == 'frac_mul_int':
        d = R.randint(2, 8); n = R.randint(1, d - 1); m = R.randint(2, 9); g = gcd(n * m, d)
        a_n, a_d = n * m // g, d // g
        ans = f'{a_n // a_d}' if a_d == 1 else f'{a_n}/{a_d}'
        return _ft([(n, d), '×', m, '= □'], 17), ans, (n, d, m)
    if k == 'dec_mul':
        a = R.randint(11, 99); b = R.randint(2, 9)
        return _t(f'{a / 10} × {b} = □', 17), f'{a * b / 10:g}', (a, b)
    if k == 'avg':
        v = [R.randint(5, 20) for _ in range(3)]
        if sum(v) % 3: return None
        return _t(f'{v[0]}, {v[1]}, {v[2]}의 평균은?', 15), str(sum(v) // 3), tuple(v)
    if k == 'area_rect':
        a = R.randint(3, 15); b = R.randint(2, 12)
        return _t(f'가로 {a}cm, 세로 {b}cm인 직사각형의 넓이는 □cm²', 14), str(a * b), (a, b)
    if k == 'area_tri':
        a = R.choice([4, 6, 8, 10, 12]); b = R.randint(3, 9)
        return _t(f'밑변 {a}cm, 높이 {b}cm인 삼각형의 넓이는 □cm²', 14), f'{a * b // 2}' if (a * b) % 2 == 0 else f'{a * b / 2}', (a, b)
    if k == 'ratio':
        a = R.randint(2, 9); b = R.randint(2, 9)
        if a == b: return None
        return _t(f'사과 {a}개, 배 {b}개. 사과 수 : 배 수 = □ : □', 14), f'{a} : {b}', (a, b)
    if k == 'prop':
        a = R.randint(2, 6); b = R.randint(2, 6); m = R.randint(2, 6)
        return _t(f'{a} : {b} = □ : {b * m}', 16), str(a * m), (a, b, m)
    if k == 'vol':
        a = R.randint(2, 9); b = R.randint(2, 7); c = R.randint(2, 6)
        return _t(f'가로 {a}cm, 세로 {b}cm, 높이 {c}cm 직육면체의 부피는 □cm³', 14), str(a * b * c), (a, b, c)
    if k == 'speed':
        v = R.choice([30, 40, 50, 60, 80]); t = R.randint(2, 5)
        return _t(f'한 시간에 {v}km 가는 차가 {t}시간 가면 □km', 14), f'{v * t}km', (v, t)
    return NotImplemented
