"""data/quiz.js 최종 확인: 같은 문제가 한 번도 겹치지 않는지, 문제 모양이 올바른지 검사한다.

사용:  python tools/verify_quiz.py        (문제가 있으면 목록을 보여 주고 종료 코드 1)
"""
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'data', 'quiz.js')
NBOOKS, VILLAGES, QUIZ = 10, 30, 15
BAD = re.compile(r'NaN|undefined|None|\{|\}')


def load():
    s = open(PATH, encoding='utf-8').read()
    return json.loads(s[len('window.EW='):].rstrip().rstrip(';'))


def plain(q):
    t = re.sub(r'<[^>]+>', ' ', q['a'] + ' ' + q.get('v', ''))
    return re.sub(r'\s+', ' ', t).strip()


def main():
    d = load()
    errs = []
    books = d['books']
    if len(books) != NBOOKS:
        errs.append(f'책 수 {len(books)} (기대 {NBOOKS})')
    raw_seen = {}      # 질문+그림 원문 -> 위치
    plain_seen = {}    # 글자만 -> 위치 (그림이 글자가 아닌 문제는 제외)
    n_q = n_dad = 0
    slot_level = collections.defaultdict(list)
    slot_cat = collections.defaultdict(collections.Counter)
    per_book_dad = collections.Counter()
    for b in books:
        if len(b['v']) != VILLAGES:
            errs.append(f'{b["n"]}권 마을 수 {len(b["v"])} (기대 {VILLAGES})')
        for vi, v in enumerate(b['v']):
            where = f'{b["n"]}권 {vi + 1}일차'
            if len(v['q']) != QUIZ:
                errs.append(f'{where}: 문제 수 {len(v["q"])} (기대 {QUIZ})')
            for qi, q in enumerate(v['q']):
                n_q += 1
                loc = f'{where} {qi + 1}번'
                slot_level[qi].append(q.get('l', 0))
                slot_cat[qi][q.get('t')] += 1
                if not q.get('a') or BAD.search(q['a'] + q.get('v', '')):
                    errs.append(f'{loc}: 이상한 글자 {q.get("a", "")[:30]}')
                if 'd' in q:
                    n_dad += 1
                    per_book_dad[b['n']] += 1
                    if not q['d'].strip():
                        errs.append(f'{loc}: 빈 정답')
                else:
                    c, k = q.get('c'), q.get('k')
                    if not isinstance(c, list) or len(c) < 2:
                        errs.append(f'{loc}: 보기가 부족')
                    elif not (isinstance(k, int) and 0 <= k < len(c)):
                        errs.append(f'{loc}: 정답 번호 오류')
                    else:
                        if len(set(c)) != len(c):
                            errs.append(f'{loc}: 보기가 겹침 {c}')
                        if any(not str(x).strip() or BAD.search(str(x)) for x in c):
                            errs.append(f'{loc}: 이상한 보기 {c}')
                key = q['a'] + '|' + q.get('v', '')
                if key in raw_seen:
                    errs.append(f'같은 문제: {loc} = {raw_seen[key]}  [{plain(q)[:40]}]')
                else:
                    raw_seen[key] = loc
                if '<svg' not in q.get('v', ''):
                    p = plain(q)
                    if p in plain_seen and plain_seen[p] != loc and key not in raw_seen:
                        errs.append(f'글자가 같은 문제: {loc} = {plain_seen[p]}')
                    plain_seen.setdefault(p, loc)
    print(f'확인한 문제 {n_q}개 (아빠 확인 카드 {n_dad}개 = {n_dad * 100 / n_q:.1f}%), 서로 다른 문제 {len(raw_seen)}개')
    print('책별 아빠 확인 카드:', dict(sorted(per_book_dad.items())))
    print('번호별 평균 난이도:', [round(sum(slot_level[i]) / len(slot_level[i]), 2) for i in range(QUIZ)])
    print('번호별 영역:', [slot_cat[i].most_common(1)[0][0] for i in range(QUIZ)])
    if errs:
        print(f'\n문제 {len(errs)}건:')
        for e in errs[:60]:
            print(' -', e)
        sys.exit(1)
    print('\n최종 확인 통과: 300개 마을 × 15문제 = 4,500문제에 같은 문제가 없습니다.')


if __name__ == '__main__':
    main()
