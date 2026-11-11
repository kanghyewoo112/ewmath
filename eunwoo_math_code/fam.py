"""문제 가족(family) 문법: 문장 틀 + 변수 범위 + 정답식. 정답은 파이썬이 계산한다.
F(q, spec, ans, ok='True')
  q    : '{a}개 중 {b}개…' 형식 문장
  spec : 'a:10-30,b:2-9,n:사과|구슬' (숫자 범위 또는 | 로 나눈 낱말 목록)
  ans  : 정답을 만드는 파이썬 식 (f-string 가능)
  ok   : 변수 조건 식
"""
import random
from math import gcd


def lcm(a, b):
    return a * b // gcd(a, b)


def F(q, spec, ans, ok='True'):
    return dict(q=q, spec=spec, ans=ans, ok=ok)


def _parse(spec):
    out = {}
    for part in spec.split(','):
        if ':' not in part and '=' in part:
            k, v = part.split('=', 1)
            out[k.strip()] = ('d', v, 0)
            continue
        k, v = part.split(':', 1)
        k = k.strip()
        if '|' in v or not v.replace('-', '').replace('.', '').isdigit() or v.count('-') != 1:
            out[k] = ('c', v.split('|'), 0)
        else:
            a, b = v.split('-')
            out[k] = ('r', int(a), int(b))
    return out


def draw(fam, n, seed, lv=1):
    R = random.Random(seed)
    P = _parse(fam['spec'])
    out, seen, guard = [], set(), 0
    while len(out) < n and guard < 600:
        guard += 1
        p = {}
        for k, (t, a, b) in P.items():
            if t == 'd':
                continue
            if t == 'r':
                hi = b + int((b - a) * 0.6 * (lv - 1))
                p[k] = R.randint(a, max(a, hi))
            else:
                p[k] = R.choice(a)
        env = dict(gcd=gcd, lcm=lcm, **p)
        try:
            for k, (t, a, b) in P.items():
                if t == 'd':
                    p[k] = env[k] = eval(a, env)
            if not eval(fam['ok'], env):
                continue
            q = fam['q'].format(**p)
            a_ = str(eval(fam['ans'], env))
        except Exception:
            continue
        if q in seen:
            continue
        seen.add(q)
        out.append((q, a_))
    if not out:
        raise ValueError('no items: ' + fam['q'])
    i = 0
    while len(out) < n:
        out.append(out[i % len(out)])
        i += 1
    return out


def hand(fams, n, seed, lv=1):
    """가족 목록에서 번갈아 n개"""
    if isinstance(fams, dict):
        fams = [fams]
    per = [draw(f, (n + len(fams) - 1) // len(fams) + 1, seed + 17 * i, lv) for i, f in enumerate(fams)]
    out, seen, j = [], set(), 0
    while len(out) < n and j < 40:
        for lst in per:
            if j < len(lst) and lst[j][0] not in seen:
                seen.add(lst[j][0])
                out.append(lst[j])
                if len(out) == n:
                    break
        j += 1
    k = 0
    while len(out) < n:
        out.append(out[k % len(out)])
        k += 1
    return out
