import probs as _probs
import probs2 as _p2
import probs3, probs4, probs5
import gen as _gen
from playwright.sync_api import sync_playwright as _spw

# (이름, 색 key, 종류, 월화수 요일, 목금토 요일, 분)
CATS = [
    ('사고력 선행', 'think', 'think', '월', '금', 10), ('응용력·사고력', 'think', 'apply', '월', '금', 10),
    ('개념 이해', 'curr', 'concept', '화', '목', 8), ('나이별 진도', 'curr', 'grade', '화', '목', 6),
    ('반복 학습', 'play', 0, '수', '금', 8), ('교과', 'curr', 2, '화', '목', 8),
    ('연산 준비', 'calc', 1, '수', '금', 8), ('정확도 향상', 'shape', 3, '수', '토', 8),
    ('심화·올림피아드', 'deep', 'olymp', '수', '토', 15)]
CIRC = '①②③④⑤⑥⑦⑧⑨⑩'
PER = {6: 2, 7: 3, 8: 3, 9: 4, 10: 4}.get(B.NO, 2)  # 영역당 문제 수 (반쪽 기준)
NCELL = {6: 8, 7: 8, 8: 10, 9: 10, 10: 10}.get(B.NO, 6)
TALL = {'clock', 'clock_hour', 'length', 'group', 'data_most', 'data_diff'} | ({'skip', 'pat_num', 'reduce', 'frac_add_diff', 'frac_mul_int'} if B.NO >= 6 else set())


def _pool(kinds, need, seed):
    out, seen = [], set()
    for kd in dict.fromkeys(kinds):
        for html, ans in _gen.kind_items(kd, need, seed + len(out)):
            if html in seen:
                continue
            seen.add(html)
            out.append((html, ans))
            if len(out) >= need:
                return out
    i = 0
    while len(out) < need:
        out.append(out[i % len(out)])
        i += 1
    return out


def all_items(w):
    """{half: [cat 0..8][2 problems]} ; 한 문제 = dict(no, kind, q|cells, ans)"""
    n = w['n']
    spec = _probs.P[B.NO][n]
    x = _p2.X[B.NO][n]
    base = (n - 1) * 18 * PER
    res = {0: [], 1: []}
    for i, (nm, col, kk, dA, dB, mins) in enumerate(CATS):
        if isinstance(kk, str):
            key = {'think': 'think', 'apply': 'apply', 'concept': 'concept', 'grade': 'grade', 'olymp': 'olymp'}[kk]
            lst = [spec[key]] + list(x[key])
            while len(lst) < 2 * PER:
                lst = lst + lst
            for half in (0, 1):
                ps = []
                for j in range(PER):
                    q, a = lst[half * PER + j]
                    ps.append(dict(kind='hand', q=q, ans=a))
                res[half].append(ps)
        else:
            cs = spec['c']
            kinds = [cs[kk]] + [c for c in cs if c != cs[kk]]
            ncell = (4 if cs[kk] in TALL else NCELL)
            if B.NO >= 6 and cs[kk] not in TALL:
                import re as _re
                _smp = [len(_re.sub('<[^>]+>', '', h_)) for h_, a_ in _gen.kind_items(cs[kk], 6, 5)]
                _m = sum(_smp) / max(1, len(_smp))
                ncell = min(ncell, 4 if _m > 20 else 5 if _m > 11 else ncell)
            pool = _pool(kinds, ncell * PER * 2, B.NO * 1000 + n * 20 + i)
            for half in (0, 1):
                ps = []
                for j in range(PER):
                    sl = pool[half * PER * ncell + j * ncell: half * PER * ncell + (j + 1) * ncell]
                    ps.append(dict(kind='set', cells=[s[0] for s in sl], ans='  '.join(f'{CIRC[t]} {s[1]}' for t, s in enumerate(sl))))
                res[half].append(ps)
    for half in (0, 1):
        for i in range(9):
            for j in range(PER):
                res[half][i][j]['no'] = base + half * 9 * PER + PER * i + j + 1
    return res


def cat_block(w, half, i, ps):
    nm, col, kk, dA, dB, mins = CATS[i]
    st, ti, _ = C[col]
    day = dA if half == 0 else dB
    head = f'<div style="display:flex;align-items:center;gap:8px;height:30px;flex:none;background:{st};padding:0 12px;color:#fff"><span style="font-family:Jua;font-size:17px">{nm}</span><span style="flex:1"></span><span style="font-size:12px">{day}요일 추천 · 약 {mins}분</span></div>'
    pill_ = lambda no: f'<span style="flex:none;min-width:32px;height:22px;border-radius:11px;background:{st};color:#fff;font-family:Jua;font-size:14px;display:flex;align-items:center;justify-content:center;padding:0 4px;box-sizing:border-box">{no}</span>'
    if ps[0]['kind'] == 'hand':
        rows = ''
        for pr in ps:
            rows += f'<div style="display:flex;gap:10px;align-items:stretch;padding:7px 12px;border-top:1px solid {ti}">{pill_(pr["no"])}<div style="flex:1.7;font-size:14px;line-height:1.5;padding-top:1px">{pr["q"]}</div><div style="flex:1;min-height:50px;border:2px dashed #9A99A8;border-radius:10px;padding:3px 8px;font-size:11.5px;color:#7A798A;background:#FFFEFA">내 풀이 · 답</div></div>'
        body = rows
    else:
        cols = ''
        for pr in ps:
            cells = ''.join(f'<div style="display:flex;align-items:center;gap:6px;min-width:0;padding:2px 0"><b style="font-size:14px;color:{st};flex:none">{CIRC[t]}</b>{c}</div>' for t, c in enumerate(pr['cells']))
            cols += f'<div style="flex:1;min-width:0;padding:6px 12px;display:flex;flex-direction:column;gap:1px"><div style="display:flex;align-items:center;gap:8px;margin-bottom:2px">{pill_(pr["no"])}<span style="font-size:12px;color:{st};font-weight:700">{len(pr['cells'])}문제</span></div>{cells}</div>'
        body = f'<div style="display:flex;border-top:1px solid {ti}">{cols}</div>'
    return f'<div style="flex:none;box-sizing:border-box;border:2px solid {st};border-radius:14px;background:#fff;overflow:hidden">{head}{body}</div>'


def _measure(blocks):
    html = '<!doctype html><meta charset="utf-8"><body style="margin:0;font-family:\'Noto Sans KR\',sans-serif;color:#2B2A33"><div style="width:714px">' + ''.join(f'<div class="m">{b}</div>' for b in blocks) + '</div>'
    with _spw() as pw:
        br = pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        pg = br.new_page(viewport={'width': 794, 'height': 1123})
        pg.set_content(html)
        pg.wait_for_timeout(600)
        hs = pg.evaluate("()=>[...document.querySelectorAll('.m')].map(e=>e.getBoundingClientRect().height)")
        br.close()
    return hs


_CACHE = {}
SIDE = {0: '월 · 화 · 수', 1: '목 · 금 · 토'}


def _build_all():
    jobs = []  # (w, half, i, html)
    for w in WEEKS:
        its = all_items(w)
        for half in (0, 1):
            for i in range(9):
                jobs.append((w['n'], half, i, cat_block(w, half, i, its[half][i])))
    hs = _measure([j[3] for j in jobs])
    by = {}
    for (n, half, i, html), hh in zip(jobs, hs):
        by.setdefault((n, half), []).append((html, hh))
    CAP = 1071 - 24 - 6 - 8  # 내용 가능 높이(푸터 제외)
    for w in WEEKS:
        its = all_items(w)
        for half in (0, 1):
            pages, cur, used = [], [], 0
            first = True
            hdr_h = 50 + 6
            note_h = 34 + 6
            for html, hh in by[(w['n'], half)]:
                lim = CAP - hdr_h - (note_h if not pages else 0)
                if used + hh + 12 > lim and cur:
                    pages.append((cur, used))
                    cur, used = [], 0
                    lim = CAP - hdr_h
                cur.append(html)
                used += hh + 12
            pages.append((cur, used))
            lo = its[half][0][0]['no']
            hi = its[half][8][PER - 1]['no']
            out = []
            for k, (blks, used) in enumerate(pages):
                tot = len(pages)
                hdr = f'<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}<div style="display:flex;flex-direction:column;gap:2px"><div style="display:flex;align-items:center;gap:8px">{pill(str(w["n"]) + "주차 · 더 풀어 보기", "#6C4FD6")}{pill(SIDE[half] + " · " + str(lo) + "~" + str(hi) + "번", "#fff", "#2B2A33")}{pill(str(k + 1) + "/" + str(tot) + "쪽", "#FFF0C2", "#2B2A33", 12)}</div>{h(w["title"], 22)}</div></div>'
                parts = [hdr]
                if k == 0:
                    parts.append('<div style="height:34px;flex:none;background:#FFF0C2;border-radius:10px;display:flex;align-items:center;padding:0 12px;font-size:12.5px;line-height:1.35"><b>고르는 방법</b>&nbsp;&nbsp;앞쪽 설명 쪽의 주제와 짝이에요. 영역별로 골라 풀고 하루 35분을 넘기지 않아요. 정답은 월말 정답 쪽에 있어요.</div>')
                parts += blks
                lim = CAP - hdr_h - (note_h if k == 0 else 0)
                if k == len(pages) - 1 and lim - used >= 130:
                    parts.append(f'<div style="flex:1;min-height:0;border:2px dashed #9A99A8;border-radius:14px;background:#FFFEFA;padding:8px 14px;font-size:13px;color:#7A798A"><b style="color:#6C4FD6">★ 내가 만드는 문제</b> · 오늘 배운 것으로 엄마·아빠에게 낼 문제를 그림과 식으로 만들어 보세요.</div>')
                else:
                    parts.append('<div style="flex:1"></div>')
                parts.append('{FOOT}')
                out.append('\n'.join(parts))
            _CACHE[(w['n'], half)] = out


def extra_pages(w, half):
    if not _CACHE:
        _build_all()
    return _CACHE[(w['n'], half)]


def answer_pages(m):
    ws = [w for w in WEEKS if w['m'] == m]
    pages = []
    step = 2 if PER == 2 else 1
    for k in range(0, len(ws), step):
        cols = ''
        for w in ws[k:k + step]:
            its = all_items(w)
            lines = ''
            for half in (0, 1):
                lines += f'<div style="font-size:11.5px;font-weight:700;color:#BE185D;margin:4px 0 1px;break-after:avoid">{SIDE[half]}</div>'
                for i in range(9):
                    for pr in its[half][i]:
                        lines += f'<div style="display:flex;gap:6px;font-size:10.8px;line-height:1.38;padding:1px 0;border-bottom:1px dotted #E4E2EC;break-inside:avoid"><b style="flex:0 0 30px;color:#6C4FD6">{pr["no"]}</b><span style="flex:1">{pr["ans"]}</span></div>'
            body = lines if PER == 2 else f'<div style="column-count:2;column-gap:14px">{lines}</div>'
            cols += f'<div style="flex:1;min-width:0;border:1.5px solid #7A798A;border-radius:12px;background:#fff;padding:6px 10px;box-sizing:border-box;align-self:flex-start"><div style="font-family:Jua;font-size:15px;margin-bottom:2px">{w["n"]}주 · {w["title"]}</div>{body}</div>'
        intro = p("아이가 풀 때 정답을 먼저 보여 주지 않아요. 틀리면 ① 다시 읽기 → ② 그림·콩으로 보기 → ③ 힌트 하나 → ④ 스스로 해결. 풀이가 달라도 이유를 말하면 맞아요. 아래는 한 가지 예시 답이에요.", 12.5, MUTE) if k == 0 else ''
        tot = (len(ws) + step - 1) // step
        inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h(f"{m}개월차 정답과 지도 (부모용) {k // step + 1}/{tot}", 24)}</div>
{intro}
<div style="display:flex;gap:10px;flex:none;align-items:flex-start">{cols}</div>
<div style="flex:1"></div>{{FOOT}}
'''
        pages.append(doc(f'{m}개월차 정답 {k // step + 1}', inner, pad='26px 40px', gap=6))
    return pages
