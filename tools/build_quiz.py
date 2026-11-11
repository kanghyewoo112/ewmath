"""책 데이터(문제 생성기·문제 틀)에서 홈페이지 퀴즈 데이터(data/quiz.js)를 만든다.

사용:  python tools/build_quiz.py      (만든 뒤 python tools/verify_quiz.py 로 최종 확인)
환경변수 EW_CODE 로 책 코드 폴더를 바꿀 수 있다 (기본: eunwoo_math_code).

구조
  - 1~10권, 권마다 12주. 한 권은 30개 마을(하루에 하나)이고 한 주를 2~3개 마을이 나눠 쓴다.
  - 마을마다 문제 15개를 미리 정해 둔다. 모든 마을(300개)에서 같은 문제가 겹치지 않게 배정한다.
      1~5번  복습  (쉬운 단계, 현재 주차와 앞선 두 주차에서)
      6~10번 현재 내용 중간 단계
      11~15번 단계별로 어려워지는 문제
  - 영역: calc 연산 / think 사고력 / shape 도형·측정 / curr 교과 / ahead 선행 / deep 심화
"""
import importlib
import json
import os
import random
import re
import sys

import qlib as Q
from qlib import CATS, MEASURE, MEASURE_RE, TITLE_MEASURE_RE, CUSTOM, sigof, gen_pool, convert_item, convert_family

import kit  # noqa: E402  (v2 코드: 문제 틀을 가져오기 위해 _fill 을 가로챈다)
import fam  # noqa: E402

_caught = {}
_orig_fill = kit._fill


def _spy(NO, n, kinds, F, lv=1):
    _caught[(NO, n)] = (kinds, F, lv)
    return _orig_fill(NO, n, kinds, F, lv)


kit._fill = _spy

import content  # noqa: E402
import probs, probs2  # noqa: E402
from book1_data import BOOK1  # noqa: E402

MODS = {no: importlib.import_module(f'bk{no}') for no in range(2, 11)}
P, X = probs.P, probs2.X

NBOOKS, VILLAGES, WEEKS, QUIZ = 10, 30, 12, 15
FIELDS = ('concept', 'think', 'apply', 'grade', 'olymp')
BOOK_INFO = {
    1: ('1권', '1~100 수 세기와 덧셈·뺄셈'),
    2: ('2권', '백 판 · 10 만들기 · 몇십몇 계산'),
    3: ('3권', '10 넘는 덧셈·뺄셈 · 세 수 · 입체도형'),
    4: ('4권', '수 구조 · 덧셈뺄셈 이야기 · 시계'),
    5: ('5권', '100이 넘는 수 · 받아올림 · 길이'),
    6: ('6권', '수 표현 · 받아올림·내림 · 규칙'),
    7: ('7권', '세 자리 수 · 두 자리 계산 · 곱셈'),
    8: ('8권', '세 자리 계산 · 곱셈·나눗셈 · 분수'),
    9: ('9권', '큰 수 · 각도 · 분수와 소수'),
    10: ('10권', '약수와 배수 · 분수·소수 · 비와 비율'),
}
ICONS = ['🏡', '🌳', '🍯', '🦆', '🏰', '🧺', '🎈', '🍭', '🌈', '🚂', '🐻', '🦋']
SUFFIX = ['', ' ②', ' ③']

# 15문제의 자리: (영역, 난이도 단계, 복습 여부)
SLOTS = [
    ('calc', 1, True), ('curr', 1, True), ('shape', 1, True), ('calc', 2, True), ('think', 2, True),
    ('curr', 2, False), ('calc', 3, False), ('ahead', 3, False), ('shape', 3, False), ('think', 3, False),
    ('calc', 4, False), ('ahead', 4, False), ('shape', 4, False), ('deep', 4, False), ('deep', 5, False),
]


# ---------------------------------------------------------------- 주차 데이터
def top_of(title, rng):
    nums = [int(x) for x in re.findall(r'(\d+)(?!\s*권)', rng) if int(x) >= 5]
    if nums:
        return max(nums)
    return 30 if TITLE_MEASURE_RE.search(title + ' ' + rng) else 100


def number_kinds(c):
    return [k for k in c if k not in MEASURE and k != 'skip']


def week_list():
    out = []
    for wk in content.WEEKS:  # 1권
        src = BOOK1[wk['n']]
        items = {f: list(src[f]) for f in ('think', 'apply', 'grade', 'olymp')}
        items['concept'] = []
        out.append(dict(b=1, w=wk['n'], title=wk['title'], rng=wk['rng'], c=src['c'], items=items, F=None, lv=1))
    for no in range(2, 11):
        for wk in MODS[no].b.weeks:
            n = wk['n']
            items = {f: [P[no][n][f]] for f in FIELDS}
            for f, lst in X[no][n].items():
                items[f] += list(lst)
            kinds, F, lv = _caught.get((no, n), (None, None, 1))
            out.append(dict(b=no, w=n, title=wk['title'], rng=wk['rng'], c=tuple(P[no][n]['c']), items=items, F=F, lv=lv))
    for g, wk in enumerate(out):
        wk['g'] = g
        wk['top'] = top_of(wk['title'], wk['rng'])
    return out


# ---------------------------------------------------------------- 문제 풀 (필요하면 더 만들어 늘린다)
class Pool:
    def __init__(self, maker):
        self.maker, self.round, self.items, self.sigs, self.cuts = maker, 0, [], set(), None
        self.dead = 0
        self.extend()

    def extend(self):
        if self.dead >= 3:
            return 0
        added = 0
        batch = self.maker(self.round)
        self.round += 1
        fresh = []
        for q in batch:
            s = sigof(q)
            if s in self.sigs:
                continue
            self.sigs.add(s)
            fresh.append(q)
        if self.cuts is None and fresh:
            sc = sorted(q['_s'] for q in fresh)
            self.cuts = [sc[min(len(sc) - 1, len(sc) * i // 5)] for i in (1, 2, 3, 4)]
        for q in fresh:
            q['l'] = 1 + sum(q['_s'] >= c for c in self.cuts)
            self.items.append(q)
            added += 1
        self.dead = 0 if added else self.dead + 1
        return added


def build_pools(wk, allw, review, mreview):
    b, g, top = wk['b'], wk['g'], wk['top']
    seed = f'{b}-{wk["w"]}'
    c = wk['c']
    nk, mk, sk = number_kinds(c), [k for k in c if k in MEASURE], [k for k in c if k == 'skip']
    curr_k = nk[2] if len(nk) >= 3 else None
    calc_ks = [k for i, k in enumerate(nk) if not (len(nk) >= 3 and i == 2)] or review[:4]
    nxt = []
    for later in allw[g + 1:]:
        nxt = number_kinds(later['c'])
        if nxt:
            break
    if not nxt:
        nxt = ['plus_carry2', 'minus_borrow2', 'same_add']
    nxt = [k for k in nxt if k not in MEASURE][:3] or nxt
    F = wk['F']
    old = b <= 5

    def text_items(field, r):
        """글 문제: 문제 틀이 있으면 매번 새 숫자로 뽑고, 없으면 책에 적힌 문제를 처음 한 번만 쓴다."""
        R = random.Random(f'{seed}{field}{r}')
        if F and field in F:
            fams = F[field] if isinstance(F[field], list) else [F[field]]
            out = []
            for i, f in enumerate(fams):
                try:
                    inst = fam.draw(f, 16, g * 100003 + FIELDS.index(field) * 7919 + r * 104729 + i * 31, wk['lv'])
                except ValueError:
                    continue
                inst = list(dict.fromkeys(inst))
                out += convert_family(inst, field, R)
            return out
        return [x for x in (convert_item(q, a, R, field) for q, a in wk['items'][field]) if x] if r == 0 else []

    def split(lst, measure):
        return [q for q in lst if bool(MEASURE_RE.search(q['a'])) == measure]

    def only_choice(lst):
        return [q for q in lst if 'd' not in q]

    def calc(r):
        out = gen_pool(calc_ks, 16, f'{seed}calc{r}', b, top) + only_choice(split(text_items('apply', r), False))
        if old:
            hard = ['two_step', 'compare_expr', 'blank_two'] if not TITLE_MEASURE_RE.search(wk['title']) else ['two_step']
            out += gen_pool(hard, 6, f'{seed}hc{r}', b, top)
        return out

    def curr(r):
        out = gen_pool([curr_k] if curr_k else [], 10, f'{seed}curr{r}', b, top)
        out += split(text_items('concept', r) + text_items('grade', r), False)
        if b == 1 and wk['w'] <= 3:
            out += gen_pool(['count'], 8, f'{seed}cnt{r}', b, top)
        return out

    def ahead(r):
        return gen_pool(nxt, 16, f'{seed}ahead{r}', b, top)

    def shape(r):
        out = gen_pool(mk, 12, f'{seed}shape{r}', b, top)
        out += split(sum((text_items(f, r) for f in ('apply', 'grade', 'concept')), []), True)
        if b <= 3:
            out += gen_pool(['shape_name', 'shape_count', 'shape_sides'], 10, f'{seed}sh2{r}', b, top)
        if len([q for q in out if 'd' not in q]) < 10:  # 측정 내용이 없는 주차는 같은 권의 다른 주차 측정 문제로 채운다
            out += gen_pool(mreview or review[:4], 10, f'{seed}shm{r}', b, top)
        if r >= 2:  # 측정 문제가 바닥나면 마지막 수단으로 같은 권의 계산 문제를 쓴다
            out += gen_pool(review[:6], 10, f'{seed}shr{r}', b, top)
        return out

    def think(r):
        out = text_items('think', r) + gen_pool(sk, 10, f'{seed}skip{r}', b, top)
        if b <= 3:
            out += gen_pool(['pattern'], 6, f'{seed}pat{r}', b, top)
        if old:
            out += gen_pool(['skip', 'digit_cards'], 6, f'{seed}skp{r}', b, top)
        if not [q for q in out if 'd' not in q]:
            out += gen_pool(calc_ks, 8, f'{seed}threv{r}', b, top)
        return out

    def deep(r):
        out = text_items('olymp', r)
        if old:
            out += gen_pool(['between', 'clue', 'digit_cards'], 10, f'{seed}deep{r}', b, top)
        if not [q for q in out if 'd' not in q]:
            out += gen_pool(nxt + calc_ks, 10, f'{seed}dprev{r}', b, top)  # 다음에 배울 더 어려운 계산으로 채운다
        return out

    makers = dict(calc=calc, curr=curr, ahead=ahead, shape=shape, think=think, deep=deep)
    return {cat: Pool(m) for cat, m in makers.items()}


# ---------------------------------------------------------------- 배정
def pick_from(pool, slot, used, rng, dad_ok, level_mode):
    cat, want, rv = slot
    if level_mode == 'exact':
        ok = (lambda q: q['l'] <= want) if rv else (lambda q: q['l'] == want)
    elif level_mode == 'near':
        ok = (lambda q: q['l'] <= want + 1) if rv else (lambda q: abs(q['l'] - want) <= 1)
    else:
        ok = lambda q: True  # noqa: E731
    cands = [q for q in pool.items if sigof(q) not in used and ok(q) and ('d' not in q or dad_ok)]
    if not cands:
        return None
    ch = [q for q in cands if 'd' not in q]
    if ch and not (dad_ok and rng.random() < 0.2):
        return rng.choice(ch)
    return rng.choice(cands)


def take(pools, g, slot, used, rng, dad_ok, allw):
    cat, want, rv = slot
    if rv:
        r = rng.random()
        offs = [0, -1, -2] if r < 0.4 else [-1, 0, -2] if r < 0.7 else [-2, -1, 0]
    else:
        offs = [0]
    srcs = [g + o for o in offs if g + o >= 0]
    srcs += [g + o for o in (1, -1, 2, -2, 3, -3) if 0 <= g + o < len(allw) and allw[g + o]['b'] == allw[g]['b'] and g + o not in srcs]
    for mode in ('exact', 'near', 'any'):
        for sg in srcs:
            pool = pools[sg][cat]
            q = pick_from(pool, slot, used, rng, dad_ok, mode)
            tries = 0
            while q is None and tries < 4:  # 쓸 수 있는 문제가 없으면 풀을 늘려 본다
                tries += 1
                if not pool.extend():
                    continue
                q = pick_from(pool, slot, used, rng, dad_ok, mode)
            if q is not None:
                return q
    raise SystemExit(f'문제를 배정하지 못했습니다: week {g} slot {slot}')


def build():
    allw = week_list()
    nb = {b: [w for w in allw if w['b'] == b] for b in range(1, NBOOKS + 1)}
    review = {}
    for b, ws in nb.items():
        lst = []
        for w in ws:
            lst += [k for k in number_kinds(w['c']) if k not in lst]
        review[b] = lst
    mreview = {}
    for b, ws in nb.items():
        lst = []
        for w in ws:
            lst += [k for k in w['c'] if k in MEASURE and k not in lst]
        mreview[b] = lst
    pools = {w['g']: build_pools(w, allw, review[w['b']], mreview[w['b']]) for w in allw}
    used = set()
    books = []
    for b in range(1, NBOOKS + 1):
        ws = nb[b]
        owner = [k * WEEKS // VILLAGES for k in range(VILLAGES)]
        villages = []
        for k in range(VILLAGES):
            wi = owner[k]
            wk = ws[wi]
            same = [x for x in range(VILLAGES) if owner[x] == wi]
            j, m = same.index(k), len(same)
            rng = random.Random(f'v{b}-{k}')
            qs, dads = [], 0
            for slot in SLOTS:
                dad_ok = slot[0] in ('think', 'deep') and slot[1] >= 3 and dads < 2
                q = take(pools, wk['g'], slot, used, rng, dad_ok, allw)
                used.add(sigof(q))
                dads += 'd' in q
                item = {kk: vv for kk, vv in q.items() if not kk.startswith('_')}
                item['t'] = slot[0]
                qs.append(item)
            icon = ICONS[wi % 12]
            title = wk['title']
            if '졸업' in title or '종합' in title and wi == 11 and b == 1:
                icon = '🎓'
            elif '시계' in title or '시각' in title or '시간' in title:
                icon = '⏰'
            elif '그래프' in title or '자료' in title or '표' in title:
                icon = '📊'
            elif title.startswith('자 ') or '길이' in title or 'cm' in title:
                icon = '📏'
            elif '분수' in title:
                icon = '🍰'
            elif '곱셈' in title or '구구' in title:
                icon = '✖️'
            elif '나눗셈' in title:
                icon = '➗'
            elif '도형' in title or '입체' in title or '넓이' in title or '둘레' in title or '부피' in title:
                icon = '🔷'
            villages.append(dict(t=title + (SUFFIX[j] if m > 1 else ''), r=wk['rng'], i=icon, q=qs))
        books.append(dict(n=b, title=BOOK_INFO[b][0], sub=BOOK_INFO[b][1], v=villages))
    return {'books': books}


def main():
    data = build()
    out = os.path.join(Q.ROOT, 'data')
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, 'quiz.js')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('window.EW=' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    total = sum(len(v['q']) for b in data['books'] for v in b['v'])
    print(f'{path}  ({os.path.getsize(path) // 1024}KB, 책 {len(data["books"])}권, '
          f'마을 {sum(len(b["v"]) for b in data["books"])}개, 문제 {total}개)')


if __name__ == '__main__':
    main()
