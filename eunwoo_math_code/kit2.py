from kit import *
from fam import F

NAMES = ['오늘의 이야기', '식으로 풀기', '놀이로 익히기', '방법 비교하기', '그림·표로 풀기', '오래 생각하기']
ASKS = ['{n}을(를) 어떻게 생각했어?', '왜 그렇게 풀었어?', '이기려면 어떻게 해야 할까?', '두 방법은 무엇이 같고 달라?', '그림으로 나타내면 어떻게 돼?', '다른 방법도 있을까?']


def wk(b, title, rng, kid, kinds, concept, think, apply, grade, olymp, say, play, skill, tip='', mats='연필, 공책, 색연필, 수 카드', lv=1, names=None, asks=None):
    noun = title
    nm = names or [f'{title} 이야기', f'{title} 풀기', f'{title} 놀이', f'{title} 비교', f'{title} 그림으로', '오래 생각하기']
    ak = asks or [a.format(n=noun) for a in ASKS]
    parent = (tip + ' ' if tip else '') + '풀이 시간보다 설명하는 말을 먼저 들어 주세요. 틀리면 정답 대신 "어디까지 맞았어?"라고 물어요.'
    checks = CK(skill, '문제 5개 중 4개 이상 맞힌다', '풀이를 말로 설명한다', '숫자나 모양이 바뀌어도 같은 방법을 쓴다')
    b.auto(title, rng, kid, parent, mats, checks, tuple(kinds), dict(concept=concept, think=think, apply=apply, grade=grade, olymp=olymp), nm, ak, play, say, lv=lv)


def months(titles, rngs, kids, focus, skip, ends):
    return {i + 1: dict(title=titles[i], rng=rngs[i], kid=kids[i], focus=focus[i], skip=skip[i], end=ends[i]) for i in range(3)}


def check(items3, titles, notes):
    out = {}
    for i in range(3):
        out[i + 1] = ([(a, vis(x)) for a, x in items3[i]], titles[i], notes[i])
    return out
