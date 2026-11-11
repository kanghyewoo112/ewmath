"""새 지도(2~10권)용 제작 틀: 기존 주차 재배치(remap) + 새 주차(newweek) + 쪽 시각 요소 약식(vis)"""
import copy, re, importlib
from lib import *
from content import D, V
import probs as _P
import probs2 as _P2
import probs3, probs4, probs5  # noqa  (옛 X 등록)
import fam

T_ = lambda t, s=16: txt(t, s, True, INK, True)
V1 = lambda *a: '<div style="display:flex;flex-direction:column;gap:6px">' + ''.join(a) + '</div>'
CK = lambda a, b, c, d: [a, b, c, d]

# ---- 옛 자료 스냅샷 (책 번호가 바뀌어도 원본을 잃지 않도록)
OLDW = {}
for _b, _m in ((2, 'content2'), (3, 'content3'), (4, 'content4'), (5, 'content5')):
    OLDW[_b] = {w['n']: w for w in copy.deepcopy(importlib.import_module(_m).WEEKS)}
OLDP = copy.deepcopy(_P.P)
OLDX = copy.deepcopy(_P2.X)


def _eq(s):
    s = s.replace('-', '−').replace('*', '×').replace('/', '÷')
    t = re.findall(r'\d+|□|[+−×÷=()]', s)
    if '=' not in t:
        t += ['=', '□']
    return eq(*t, size=22)


def vis(items):
    out = []
    for it in items:
        k, _, v = it.partition(':')
        if k == 'eq':
            out.append(_eq(v))
        elif k == 'say':
            out.append(T_(v))
        elif k == 'draw':
            out.append(drawbox(v, None, 80))
        elif k == 'blocks':
            a, b = v.split(',')
            out.append(blocks(int(a), int(b)))
        elif k == 'strip':
            out.append(numstrip([(int(x) if x else '') for x in v.split(',')], 32))
        elif k == 'dice':
            out.append(row(''.join(dice(int(x)) for x in v.split(',')), 12, False))
        elif k == 'clock':
            out.append(row(''.join(clockq2(int(x.split(',')[0]), x.split(',')[1] == '1', 62) for x in v.split(';')), 10, False))
        elif k == 'frame':
            out.append(tenframes(int(v), '#E5484D', 18))
        elif k == 'groups':
            n, kk, kind = v.split(',')
            out.append(groups(int(n), int(kk), kind, 18))
        elif k == 'ruler':
            n, o = v.split(',')
            out.append(ruler(int(n), int(o)))
        elif k == 'cards':
            out.append(cards([int(x) for x in v.split(',')], 40))
        elif k == 'pattern':
            out.append(pattern(v.split(','), 30))
        elif k == 'stack':
            out.append(stackview([int(x) for x in v.split(',')], 22))
        elif k == 'bars':
            a, b = v.split(',')
            out.append(bars(int(a), int(b)))
        elif k == 'p':
            out.append(p(v, 13.5))
        else:
            raise ValueError(it)
    return V(*out)


DAYS = ['월', '화', '수', '목', '금', '토']


def _wk(n, title, rng, kid, parent, mats, checks, days, say=None):
    ds = []
    for dn, dd in zip(DAYS, days):
        cat, name, mins, task, vi, ask = dd[:6]
        warm = dd[6] if len(dd) > 6 else None
        ds.append(D(dn, cat, name, mins, task, vis(vi), ask, warm))
    return dict(n=n, m=(n - 1) // 4 + 1, title=title, rng=rng, kid=kid, parent=parent, mats=mats, checks=checks, days=ds, say=say or '')


def _fill(NO, n, kinds, F, lv=1):
    """가족 문법 F(dict: concept,think,apply,grade,olymp)로 P/X 항목을 만든다(정답은 계산)."""
    seed = NO * 1000 + n * 31
    per = {6: 2, 7: 3, 8: 3, 9: 4, 10: 4}.get(NO, 2)
    got = {k: fam.hand(F[k], 2 * per, seed + i * 7, lv) for i, k in enumerate(['concept', 'think', 'apply', 'grade', 'olymp'])}
    _P.P.setdefault(NO, {})[n] = _P.W(tuple(kinds), *[got[k][0] for k in ['concept', 'think', 'apply', 'grade', 'olymp']])
    _P2.X.setdefault(NO, {})[n] = _P2.T(*[got[k][1:] for k in ['think', 'apply', 'concept', 'grade', 'olymp']])


class Book:
    def __init__(self, NO):
        self.NO = NO
        self.weeks = []
        _P.P[NO] = {}
        _P2.X[NO] = {}

    def old(self, ob, ow, title=None, rng=None, kid=None, parent=None, say=None):
        n = len(self.weeks) + 1
        w = copy.deepcopy(OLDW[ob][ow])
        w['n'] = n
        w['m'] = (n - 1) // 4 + 1
        if title:
            w['title'] = title
        if rng:
            w['rng'] = rng
        if kid:
            w['kid'] = kid
        if parent:
            w['parent'] = parent
        w['say'] = say or ''
        self.weeks.append(w)
        _P.P[self.NO][n] = copy.deepcopy(OLDP[ob][ow])
        _P2.X[self.NO][n] = copy.deepcopy(OLDX[ob][ow])

    def new(self, title, rng, kid, parent, mats, checks, days, kinds, F, say=None, lv=1):
        n = len(self.weeks) + 1
        self.weeks.append(_wk(n, title, rng, kid, parent, mats, checks, days, say))
        _fill(self.NO, n, kinds, F, lv)

    def swap_day(self, wi, di, ob, ow, si, letter):
        """주차 wi(1부터)의 di번째 날을 옛 책 ob의 ow주 si번째 날 카드로 바꾼다"""
        d = copy.deepcopy(OLDW[ob][ow]['days'][si])
        d['d'] = letter
        self.weeks[wi - 1]['days'][di] = d


import gen as _gen


def _items(kind, n, seed):
    return [h for h, a in _gen.kind_items(kind, n, seed)]


def auto_days(NO, n, names, asks, kinds, F, play, warm='연산 10분: 암산 말하기', lv=1):
    """주차 6일 카드를 가족·생성기에서 자동으로 만든다. names/asks: 6개씩, play=(과제 문장,)"""
    seed = NO * 7000 + n * 13
    q = lambda key, i=0: fam.draw(F[key], 3, seed + i, lv)[0][0]
    c1 = _items(kinds[0], 3, seed + 1)
    c2 = _items(kinds[1], 3, seed + 2)
    ds = []
    ds.append(D('월', 'think', names[0], 25, '오늘의 이야기를 읽고 그림이나 식으로 먼저 생각해요.', V(p(q('concept'), 13.5), drawbox('내 생각', None, 70)), asks[0], warm))
    ds.append(D('화', 'curr', names[1], 20, '식을 풀고 어떻게 풀었는지 말해요.', V(*c1), asks[1], warm))
    ds.append(D('수', 'play', names[2], 20, play, V(p(play, 13.5)), asks[2]))
    ds.append(D('목', 'curr', names[3], 20, '식을 풀고 방법을 비교해요.', V(*c2), asks[3], warm))
    ds.append(D('금', 'think', names[4], 25, '문제를 읽고 그림·표·식 중 하나를 골라 풀어요.', V(p(q('think', 5), 13.5), drawbox('풀이', None, 70)), asks[4]))
    ds.append(D('토', 'deep', names[5], 20, '한 문제를 오래 생각해요. 힌트는 하나만 받아요.', V(p(q('olymp', 9), 13.5), drawbox('풀이', None, 80)), asks[5]))
    return ds


def _tobook_auto(self, title, rng, kid, parent, mats, checks, kinds, F, names, asks, play, say, lv=1):
    n = len(self.weeks) + 1
    self.weeks.append(dict(n=n, m=(n - 1) // 4 + 1, title=title, rng=rng, kid=kid, parent=parent, mats=mats, checks=checks,
                           days=auto_days(self.NO, n, names, asks, kinds, F, play, lv=lv), say=say))
    _fill(self.NO, n, kinds, F, lv)


Book.auto = _tobook_auto
