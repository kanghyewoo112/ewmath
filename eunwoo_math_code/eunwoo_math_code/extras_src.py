import probs as _probs
import gen as _gen

CATS = [  # (이름, 요일, 색 key, 분량)
    ('사고력 선행', '월', 'think', 15), ('응용력·사고력', '월', 'think', 15),
    ('개념 이해', '화', 'curr', 10), ('나이별 진도', '화', 'curr', 10),
    ('반복 학습', '수', 'play', 15),
    ('교과', '목', 'curr', 10), ('연산 준비', '목', 'calc', 10),
    ('정확도 향상', '금', 'shape', 15),
    ('심화·올림피아드', '토', 'deep', 20)]
HINT = {4: '천천히, 정확하게 풀어요', 5: '교과서에 나오는 유형이에요', 6: '수 모형이나 손가락으로 확인해요', 7: '풀고 나서 거꾸로 계산해 확인해요'}
HAND_KEYS = ['think', 'apply', 'concept', 'grade']
CIRC = '①②③④⑤⑥⑦⑧⑨'


def week_items(w):
    """9개 문제: dict(no, cat, day, col, mins, kind, q/ cells, ans)"""
    spec = _probs.P[B.NO][w['n']]
    base = (w['n'] - 1) * 9
    items = []
    seed0 = B.NO * 1000 + w['n'] * 10

    def hand(i, key):
        q, a = spec[key]
        items.append(dict(i=i, kind='hand', q=q, ans=a))

    def kset(i, kind, n, hint):
        its = _gen.kind_items(kind, n, seed0 + i)
        items.append(dict(i=i, kind='set', hint=hint, cells=[x[0] for x in its], ans=' · '.join(f'{CIRC[j]} {x[1]}' for j, x in enumerate(its))))
    hand(0, 'think'); hand(1, 'apply'); hand(2, 'concept'); hand(3, 'grade')
    kset(4, spec['c'][0], 8, '천천히, 정확하게 8문제를 풀어요')
    kset(5, spec['c'][2], 6, '교과서에 나오는 유형이에요')
    kset(6, spec['c'][1], 6, '수 모형이나 손가락으로 확인해요')
    kset(7, spec['c'][3], 6, '풀고 나서 거꾸로 계산해 확인해요')
    hand(8, 'olymp')
    for it in items:
        nm, day, col, mins = CATS[it['i']]
        it.update(no=base + it['i'] + 1, cat=nm, day=day, col=col, mins=mins)
    return items


def prob_box(it, hh):
    st, ti, _ = C[it['col']]
    head = f'<div style="display:flex;align-items:center;gap:8px;height:30px;flex:none;background:{st};padding:0 12px;color:#fff"><span style="min-width:34px;height:22px;border-radius:11px;background:#fff;color:{st};font-family:Jua;font-size:15px;display:flex;align-items:center;justify-content:center;padding:0 4px">{it["no"]}</span><span style="font-family:Jua;font-size:17px">{it["cat"]}</span><span style="flex:1"></span><span style="font-size:12px">{it["day"]}요일 · 약 {it["mins"]}분</span></div>'
    if it['kind'] == 'hand':
        body = f'<div style="flex:1;min-height:0;display:flex;gap:12px;padding:8px 12px;align-items:stretch"><div style="flex:1.25;font-size:15.5px;line-height:1.5;display:flex;align-items:center">{it["q"]}</div><div style="flex:1;border:2px dashed #7A798A;border-radius:10px;padding:3px 8px;font-size:11.5px;color:#7A798A;background:#FFFEFA">내 풀이 · 답: ________</div></div>'
    else:
        ncol = 2
        cells = ''.join(f'<div style="display:flex;align-items:center;gap:6px;min-width:0"><b style="font-size:15px;color:{st};flex:none">{CIRC[j]}</b>{c}</div>' for j, c in enumerate(it['cells']))
        body = f'<div style="flex:1;min-height:0;padding:6px 12px;display:flex;flex-direction:column;gap:4px;justify-content:center"><div style="font-size:12.5px;color:{st};font-weight:700">{it["hint"]}</div><div style="display:grid;grid-template-columns:repeat({ncol},minmax(0,1fr));gap:6px 14px;align-items:center">{cells}</div></div>'
    return f'<div style="height:{hh}px;flex:none;box-sizing:border-box;border:2px solid {st};border-radius:14px;background:#fff;overflow:hidden;display:flex;flex-direction:column">{head}{body}</div>'


def extra_pages(w):
    its = week_items(w)
    lo, hi = its[0]['no'], its[-1]['no']
    hd = lambda side: f'<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}<div style="display:flex;flex-direction:column;gap:2px"><div style="display:flex;align-items:center;gap:8px">{pill(str(w["n"]) + "주차 · 더 풀어 보기", "#6C4FD6")}{pill(side + " · " + str(lo) + "~" + str(hi) + "번", "#fff", "#2B2A33")}</div>{h(w["title"], 24)}</div></div>'
    note = '<div style="min-height:28px;flex:none;background:#FFF0C2;border-radius:10px;display:flex;align-items:center;padding:3px 12px;font-size:12.5px;line-height:1.35"><b>고르는 방법</b>&nbsp;&nbsp;그날 주제(A·B면)와 짝이 되는 문제예요. 아이 기분에 맞게 골라 풀고, 하루 35분을 넘기지 않아요. 정답은 월말 정답 쪽에 있어요.</div>'
    c1 = [hd('월·화·수'), note] + [prob_box(it, 140) for it in its[0:4]] + [prob_box(its[4], 330)] + ['{FOOT}']
    c2 = [hd('목·금·토')] + [prob_box(its[5], 254), prob_box(its[6], 254), prob_box(its[7], 254), prob_box(its[8], 190)] + ['<div style="flex:1"></div>{FOOT}']
    return '\n'.join(c1), '\n'.join(c2)


def answer_page(m):
    ws = [w for w in WEEKS if w['m'] == m]
    blocks = ''
    for w in ws:
        lines = ''
        for it in week_items(w):
            a = it['ans']
            lines += f'<div style="display:flex;gap:6px;font-size:11.5px;line-height:1.4;padding:1px 0"><b style="flex:0 0 28px;color:#6C4FD6">{it["no"]}</b><span style="flex:1">{a}</span></div>'
        blocks += f'<div style="border:1.5px solid #7A798A;border-radius:12px;background:#fff;padding:6px 10px;box-sizing:border-box"><div style="font-family:Jua;font-size:15px;margin-bottom:2px">{w["n"]}주 · {w["title"]}</div>{lines}</div>'
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h(f"{m}개월차 정답과 지도 (부모용)", 26)}</div>
{p("아이가 풀 때 정답을 먼저 보여 주지 않아요. 틀리면 ① 다시 읽기 → ② 그림·콩으로 보기 → ③ 힌트 하나 → ④ 스스로 해결. 풀이가 달라도 이유를 말하면 맞아요. 아래는 한 가지 예시 답이에요.", 12.5, MUTE)}
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;flex:none;align-items:start">{blocks}</div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc(f'{m}개월차 정답', inner)
