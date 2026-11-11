import random
from lib import *

S = 19


def _e(a, op, b, r='□'):
    return eq(str(a), op, str(b), '=', str(r), size=S)


def _t(s, size=15):
    return txt(s, size, True, INK, True)


def kind_items(kind, n, seed):
    """returns list of (html, answer) for n items of the kind"""
    R = random.Random(seed)
    out = []
    seen = set()
    guard = 0
    while len(out) < n and guard < 400:
        guard += 1
        it = _one(kind, R, len(out))
        if it is None or it[2] in seen:
            continue
        seen.add(it[2])
        out.append((it[0], it[1]))
    return out


def _one(k, R, i):
    from gen2 import one2
    _r = one2(k, R, i)
    if _r is not NotImplemented:
        return _r
    # each branch returns (html, answer, key)
    if k == 'make10':
        a = R.randint(1, 9); return _e(a, '+', '□', 10), str(10 - a), (a,)
    if k == 'plus_small':
        a = R.randint(1, 8); b = R.randint(1, 10 - a); return _e(a, '+', b), str(a + b), (a, b)
    if k == 'minus_small':
        a = R.randint(3, 10); b = R.randint(1, a - 1); return _e(a, '−', b), str(a - b), (a, b)
    if k == 'cmp':
        a = R.randint(10, 99); b = R.randint(10, 99)
        if a == b: return None
        return row(cards([a, b], 34) + _t('더 큰 수는?', 14), 10, False), str(max(a, b)), (a, b)
    if k == 'next':
        a = R.randint(10, 97); return numstrip([a, '', a + 2], 34), str(a + 1), (a,)
    if k == 'plus_ten':
        b = R.randint(1, 9); return _e(10, '+', b), str(10 + b), (b,)
    if k == 'plus_to20':
        a = R.randint(2, 9); b = R.randint(2, 9)
        if a + b < 11: return None
        return _e(a, '+', b), str(a + b), (a, b)
    if k == 'minus_teen':
        a = R.randint(11, 18); b = R.randint(2, 9)
        if a - b < 1 or (a % 10) >= b: return None
        return _e(a, '−', b), str(a - b), (a, b)
    if k == 'tens_ones':
        a = R.randint(11, 99); return _t(f'{a} = □십 □일', 16), f'{a // 10}십 {a % 10}일', (a,)
    if k == 'teen_ones':
        a = R.randint(11, 19); return _t(f'{a} = 10과 □', 17), str(a - 10), (a,)
    if k == 'tens_plus':
        t = R.randint(2, 9); b = R.randint(1, 9); return _e(t * 10, '+', b), str(t * 10 + b), (t, b)
    if k == 'plus_nocarry':
        t = R.randint(1, 8); u = R.randint(0, 7); b = R.randint(1, 9 - u) if u < 9 else 0
        if b < 1: return None
        return _e(t * 10 + u, '+', b), str(t * 10 + u + b), (t, u, b)
    if k == 'minus_noborrow':
        t = R.randint(1, 9); u = R.randint(2, 9); b = R.randint(1, u)
        return _e(t * 10 + u, '−', b), str(t * 10 + u - b), (t, u, b)
    if k == 'tens_pm':
        a = R.randint(1, 9); b = R.randint(1, 9)
        if R.random() < .5:
            if a + b > 10: return None
            return _e(a * 10, '+', b * 10), str((a + b) * 10), (a, b, 0)
        if b >= a: return None
        return _e(a * 10, '−', b * 10), str((a - b) * 10), (a, b, 1)
    if k == 'blank_plus':
        c = R.randint(11, 20); a = R.randint(2, 9); b = c - a
        if b < 2 or b > 9: return None
        return _e(a, '+', '□', c), str(b), (a, c)
    if k == 'blank_minus':
        c = R.randint(11, 18); d = R.randint(3, 9); b = c - d
        if b < 2 or b > 9: return None
        return _e(c, '−', '□', d), str(b), (c, d)
    if k == 'triple':
        a = R.randint(1, 9); b = R.randint(1, 9); c = R.randint(1, 9)
        if a + b + c > 20: return None
        return eq(str(a), '+', str(b), '+', str(c), '=', '□', size=S), str(a + b + c), (a, b, c)
    if k == 'same_add':
        v = R.randint(2, 9); m = R.randint(2, 4)
        if v * m > 30: return None
        return eq(*(' + '.join([str(v)] * m), '=', '□'), size=S), str(v * m), (v, m)
    if k == 'plus_carry2':
        t = R.randint(1, 8); u = R.randint(3, 9); b = R.randint(10 - u, 9)
        if u + b < 10: return None
        return _e(t * 10 + u, '+', b), str(t * 10 + u + b), (t, u, b)
    if k == 'minus_borrow2':
        t = R.randint(2, 9); u = R.randint(0, 6); b = R.randint(u + 1, 9)
        return _e(t * 10 + u, '−', b), str(t * 10 + u - b), (t, u, b)
    if k == 'skip':
        s = R.choice([2, 5, 10]); st = s * R.randint(1, 5)
        seq = [st + s * j for j in range(5)]; hole = R.randint(1, 4)
        ans = seq[hole]; seq[hole] = ''
        return row(numstrip(seq, 32) + _t(f'{s}씩', 14), 8, False), str(ans), (s, st)
    if k == 'length':
        v = R.randint(2, 9); return row(ruler(10, v, 26) + _t('□cm', 15), 6, False), f'{v}cm', (v,)
    if k == 'clock':
        h_ = R.randint(1, 12); half = R.random() < .5
        return row(clockq2(h_, half, 56) + _t('몇 시? □', 14), 10, False), f'{h_}시' + (' 30분' if half else ''), (h_, half)
    if k == 'clock_hour':
        h_ = R.randint(1, 12); return row(clockq2(h_, False, 56) + _t('□시', 15), 10, False), f'{h_}시', (h_,)
    if k == 'min5':
        v = R.randint(1, 11); return _t(f'긴 바늘이 {v}을 가리켜요. 몇 분일까요?', 14), f'{v * 5}분', (v,)
    if k == 'hour_later':
        h_ = R.randint(1, 9); d = R.randint(1, 3); return _t(f'{h_}시에서 {d}시간 뒤는 몇 시?', 14), f'{h_ + d}시', (h_, d)
    if k == 'group':
        m = R.randint(2, 4); v = R.choice([2, 3, 4, 5])
        return row(groups(m, v, 'apple', 14) + _t(f'{v}개씩 {m}묶음 → □개', 14), 8, False), str(m * v), (m, v)
    if k == 'share':
        g = R.choice([2, 3, 4]); each = R.randint(2, 5)
        return _t(f'콩 {g * each}개를 {g}접시에 똑같이. 한 접시에 □개', 14), str(each), (g, each)
    if k == 'hund':
        a = R.randint(98, 118); return numstrip([a, '', a + 2], 34), str(a + 1), (a,)
    if k == 'data_most':
        v = [R.randint(2, 9) for _ in range(3)]
        if len(set(v)) < 3: return None
        nm = ['사과', '귤', '포도']
        return table(nm, [[str(x) for x in v]], None, 13, 3) + _t('가장 많은 것은?', 13), nm[v.index(max(v))], tuple(v)
    if k == 'data_diff':
        v = [R.randint(2, 9) for _ in range(2)]
        if v[0] == v[1]: return None
        nm = ['빨강', '파랑']
        return table(nm, [[str(x) for x in v]], None, 13, 3) + _t('몇 개 더 많을까?', 13), str(abs(v[0] - v[1])), tuple(v)
    if k == 'shape_facts':
        s = R.choice([('세모', 3), ('네모', 4), ('동그라미', 0)])
        q = R.choice(['변', '꼭짓점'])
        return _t(f'{s[0]}의 {q}은 몇 개?', 15), f'{s[1]}개', (s, q)
    if k == 'len_cmp':
        a = R.randint(3, 9); b = R.randint(2, 8)
        if a == b: return None
        return _t(f'{a}cm 막대와 {b}cm 막대. 몇 cm 더 길까?', 14), f'{abs(a - b)}cm', (a, b)
    if k == 'len_add':
        a = R.randint(2, 6); b = R.randint(2, 6)
        return _t(f'{a}cm + {b}cm = □cm', 16), f'{a + b}cm', (a, b)
    if k == 'odd_even':
        a = R.randint(10, 60); return _t(f'{a}은 짝수? 홀수?', 15), '짝수' if a % 2 == 0 else '홀수', (a,)
    if k == 'tenmore':
        a = R.randint(11, 79); s = R.choice([10, -10])
        return _t(f'{a}보다 {abs(s)} {"큰" if s > 0 else "작은"} 수는?', 15), str(a + s), (a, s)
    if k == 'blank2':
        a = R.randint(10, 60); b = R.randint(2, 9)
        if (a % 10) + b > 9: return None
        return eq(str(a), '+', '□', '=', str(a + b), size=S), str(b), (a, b)
    raise ValueError(k)
