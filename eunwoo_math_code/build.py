import os, json
from lib import *
from content import WEEKS

OUT = '/home/claude/gen/out/project'
os.makedirs(OUT, exist_ok=True)
MINS = {'월': 25, '화': 15, '수': 20, '목': 20, '금': 25, '토': 20}
BOOK = '은우의 수학 모험 1권'


def doc(title, inner, bg='#FFF9EC', pad='36px 40px', gap=8):
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Jua&amp;family=Noto+Sans+KR:wght@400;500;700&amp;display=swap" rel="stylesheet">
<style>body{{margin:0}}</style>
</helmet>
<div style="width:794px;height:1123px;box-sizing:border-box;position:relative;overflow:hidden;background:{bg};font-family:'Noto Sans KR',sans-serif;color:#2B2A33;padding:{pad};display:flex;flex-direction:column;gap:{gap}px">
{inner}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":794,"height":1123}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>'''


def h(t, size=26, color=INK):
    return f'<div style="font-family:\'Jua\',sans-serif;font-size:{size}px;color:{color};line-height:1.2">{t}</div>'


def p(t, size=15, color=INK, bold=False, extra=''):
    return f'<div style="font-size:{size}px;line-height:1.5;color:{color};font-weight:{700 if bold else 400};{extra}">{t}</div>'


def pill(t, bg, fg='#fff', size=14):
    return f'<span style="background:{bg};color:{fg};border-radius:999px;padding:3px 12px;font-size:{size}px;font-weight:700;white-space:nowrap">{t}</span>'


def footer(pno, label=''):
    return f'<div style="display:flex;align-items:center;justify-content:space-between;height:24px;flex:none;font-size:12px;color:{MUTE}"><span>{BOOK} · {label}</span><span style="display:flex;align-items:center;gap:6px">{bunny(20)}<b>{pno}</b></span></div>'


def card(inner, bg='#fff', border='#2B2A33', pad=12, extra=''):
    return f'<div style="background:{bg};border:2px solid {border};border-radius:16px;padding:{pad}px;box-sizing:border-box;{extra}">{inner}</div>'


# ---------------------------------------------------------------- week pages
def dayblock(d, h_):
    st, ti, nm = C[d['c']]
    mins = MINS[d['d']]
    head = f'<div style="display:flex;align-items:center;gap:10px;background:{st};color:#fff;padding:0 14px;height:36px;flex:none"><span style="width:26px;height:26px;border-radius:50%;background:#fff;color:{st};font-family:Jua;font-size:17px;display:flex;align-items:center;justify-content:center">{d["d"]}</span><span style="font-family:Jua;font-size:20px;line-height:1">{d["name"]}</span><span style="flex:1"></span><span style="font-size:13px;font-weight:700">{nm} · {mins}분</span></div>'
    warm = ''
    if d['warm']:
        warm = f'<div style="background:#FFE9DC;padding:0 14px;height:28px;flex:none;display:flex;align-items:center;gap:8px;font-size:13.5px"><b style="color:#C2410C">10분 수 놀이</b><span>{d["warm"]}</span></div>'
    body = f'<div style="flex:1;min-height:0;display:flex;gap:14px;padding:8px 14px;align-items:center;overflow:hidden"><div style="flex:0 0 205px;font-size:15.5px;line-height:1.45">{d["task"]}</div><div style="flex:1;min-width:0">{d["vis"]}</div></div>'
    ask = f'<div style="background:{ti};padding:5px 14px;min-height:30px;flex:none;display:flex;align-items:center;gap:8px;font-size:13.5px;line-height:1.35"><b style="color:{st};white-space:nowrap">부모 질문</b><span>{d["ask"]}</span></div>'
    return head, warm, body, ask, st, h_


def render_day(d, h_, extra_after=''):
    head, warm, body, ask, st, hh = dayblock(d, h_)
    return f'<div style="height:{hh}px;flex:none;box-sizing:border-box;border:2px solid {st};border-radius:16px;background:#fff;overflow:hidden;display:flex;flex-direction:column">{head}{warm}{body}{ask}{extra_after}</div>'


def week_header(w, side, hh=60):
    return f'<div style="height:{hh}px;flex:none;display:flex;align-items:center;gap:12px">{bunny(50)}<div style="display:flex;flex-direction:column;gap:2px"><div style="display:flex;align-items:center;gap:8px">{pill(str(w["n"]) + "주차", "#6C4FD6")}{pill("숫자 " + w["rng"], "#fff", "#2B2A33")}</div>{h(w["title"], 28)}</div><div style="flex:1"></div>{pill(side, "#FFF0C2", "#2B2A33")}</div>'


def satcheck(w):
    labels = ['이해', '수행', '설명', '전이']
    rows = ''
    for lab, phrase in zip(labels, w['checks']):
        rows += f'<div style="display:flex;align-items:center;gap:8px;height:22px;font-size:13px"><b style="width:34px;color:#BE185D">{lab}</b><span style="flex:1">{phrase}</span><span style="font-size:15px;font-weight:700;letter-spacing:6px;white-space:nowrap">◎ ○ △</span></div>'
    why = '<div style="display:flex;align-items:center;gap:12px;height:24px;font-size:13px"><b>틀린 이유</b><span>몰랐어요 ☐ ☐ ☐</span><span>헷갈렸어요 ☐ ☐ ☐</span><span>실수했어요 ☐ ☐ ☐</span></div>'
    nxt = '<div style="display:flex;align-items:center;gap:8px;height:24px;font-size:13px"><b>이번 주 결정</b><span>☐ 다음 주 진행</span><span>☐ 월·화는 복습</span><span>☐ 심화 더 하기</span></div>'
    memo = f'<div style="display:flex;align-items:flex-end;gap:8px;height:24px;font-size:13px"><b>다음 주 반영</b><div style="flex:1;border-bottom:1.5px solid #7A798A;height:18px"></div></div>'
    return f'<div style="flex:none;border-top:2px dashed #BE185D;padding:5px 14px 4px;background:#FFF7FA"><div style="font-size:13px;color:#BE185D;font-weight:700;margin-bottom:2px">토요일 점검 · 부모님이 표시해요 (◎ 잘함 ○ 보통 △ 더 필요)</div>{rows}{why}{nxt}{memo}</div>'


def week_pages(w):
    pa = [week_header(w, '월 · 화 · 수')]
    intro = f'<div style="height:62px;flex:none;display:flex;gap:10px"><div style="flex:1.1;background:#EEE9FF;border:2px solid #6C4FD6;border-radius:14px;padding:6px 12px;font-size:14px;line-height:1.4"><b style="color:#6C4FD6">이번 주 모험</b><br>{w["kid"]}</div><div style="flex:1;background:#fff;border:2px solid #7A798A;border-radius:14px;padding:6px 12px;font-size:13px;line-height:1.4"><b>부모님 준비물</b><br>{w["mats"]}</div></div>'
    pa.append(intro)
    for d in w['days'][:3]:
        pa.append(render_day(d, 283))
    pa.append(footer(f'{{PNO}}', f'{w["n"]}주차 A'))

    pb = [week_header(w, '목 · 금 · 토', 50)]
    tip = f'<div style="height:34px;flex:none;background:#fff;border:2px solid #7A798A;border-radius:12px;display:flex;align-items:center;gap:10px;padding:0 12px;font-size:13px"><b style="color:#BE185D">틀렸어요?</b><span>바로 알려 주지 말고 ① 문제 다시 읽기 → ② 그림이나 콩으로 보기 → ③ 힌트 하나 → ④ 스스로 해결. 정답 설명은 마지막!</span></div>'
    pb.append(f'<div style="min-height:28px;flex:none;background:#FFF0C2;border-radius:10px;display:flex;align-items:center;padding:3px 12px;font-size:12.5px;line-height:1.35"><b>부모 한마디</b>&nbsp;&nbsp;{w["parent"]}</div>')
    pb.append(render_day(w['days'][3], 250))
    pb.append(render_day(w['days'][4], 250))
    pb.append(render_day(w['days'][5], 428, satcheck(w)))
    pb.append(footer('{PNO}', f'{w["n"]}주차 B'))
    return '\n'.join(pa), '\n'.join(pb)


# ---------------------------------------------------------------- month covers & checks
MONTHS = {
    1: dict(title='숫자 마을 탐험대', rng='1~20', kid=['1부터 20까지 세요', '5와 10을 둘로 나눠요', '규칙과 모양을 찾아요'],
            focus='수량 감각, 5와 10의 구조, 말로 설명하기', skip='덧셈·뺄셈 식 쓰기, 시계, 문제집 진도 나가기', end='10 가르기·모으기를 콩 없이 말할 수 있어요.'),
    2: dict(title='열 묶음 숲 모험', rng='21~50', kid=['10개씩 묶어 큰 수를 세요', '10 만들기 짝을 척척 찾아요', '합치기와 줄어들기 이야기를 만들어요'],
            focus='10묶음과 낱개, 10 만들기 숙달, 덧셈·뺄셈의 의미', skip='받아올림·받아내림, 곱셈, 계산 속도 훈련', end='덧셈·뺄셈 이야기를 그림으로 풀고 말로 설명해요.'),
    3: dict(title='백 마을 졸업 여행', rng='51~100', kid=['100까지 수의 구조를 알아요', '2씩 5씩 뛰고 시계를 읽어요', '식을 이야기로 바꾸고 문제를 만들어요'],
            focus='100까지 수 구조, 10 이하 덧뺄셈 암산, 새로운 문제에 적용', skip='두 자리 수 덧셈, 곱셈구구 외우기, 초2 문제집', end='석 달 동안 배운 것을 처음 보는 문제에 써요.'),
}


def month_cover(m):
    d = MONTHS[m]
    ws = [w for w in WEEKS if w['m'] == m]
    stops = ''
    for w in ws:
        stops += f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:6px"><div style="width:74px;height:74px;border-radius:50%;border:3px dashed #7A798A;background:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;color:{MUTE};text-align:center">스티커<br>붙여요</div>{pill(str(w["n"]) + "주차", "#6C4FD6", "#fff", 13)}<div style="font-family:Jua;font-size:16px;text-align:center;line-height:1.2">{w["title"]}</div><div style="font-size:12px;color:{MUTE}">숫자 {w["rng"]}</div></div>'
    routine = table(['요일', '하는 일', '시간'], [
        ['월', '10분 수 놀이 + 사고력 놀이', '35분'], ['화', '10분 수 놀이 + 도형·측정', '25분'], ['수', '수학 놀이·게임', '20분'],
        ['목', '10분 수 놀이 + 교과 개념', '30분'], ['금', '10분 수 놀이 + 사고력 놀이', '35분'], ['토', '심화 놀이 + 부모 점검 10분', '30분'], ['일', '쉬어요 · 재미있었던 문제 다시 보기', '자유']], None, 14, 4)
    kids = ''.join(f'<div style="display:flex;align-items:center;gap:10px;font-size:18px;font-family:Jua">{icon("star", 26)}{k}</div>' for k in d['kid'])
    inner = f'''
<div style="display:flex;align-items:center;gap:16px;height:150px;flex:none;background:#DDF5E9;border:3px solid #18794E;border-radius:24px;padding:0 24px">{bunny(96)}<div style="flex:1"><div style="margin-bottom:4px">{pill(f"{m}개월차 · 숫자 {d['rng']}", "#18794E")}</div>{h(d["title"], 42)}</div>{bear(96)}</div>
{card(h("이번 달 나의 목표", 22, "#6C4FD6") + '<div style="display:flex;flex-direction:column;gap:8px;margin-top:8px">' + kids + '</div>', '#EEE9FF', '#6C4FD6')}
<div style="flex:none">{h("12주 모험 지도", 20)}</div>
<div style="display:flex;gap:10px;flex:none">{stops}</div>
<div style="display:flex;gap:12px;flex:none"><div style="flex:1.25">{h("이번 달 주간 루틴", 18)}<div style="margin-top:4px">{routine}</div></div><div style="flex:1;display:flex;flex-direction:column;gap:8px">{card(p("<b>이번 달 중심</b><br>" + d["focus"], 14), "#fff", "#18794E", 10)}{card(p("<b>지금 하지 않아도 되는 것</b><br>" + d["skip"], 14), "#fff", "#BE185D", 10)}{card(p("<b>이 달이 끝나면</b><br>" + d["end"], 14), "#FFF0C2", "#8A5A00", 10)}</div></div>
{card(p("<b>하루 최대 35분.</b> 아이가 싫어하는 신호(딴짓, 한숨, 거부)가 보이면 거기서 멈추고 놀이로 바꿔요. 시간이 아니라 재미가 기준이에요.", 14), "#E3EEFF", "#1C64C8", 10)}
'''
    return doc(f'{m}개월차 표지', inner + '<div style="flex:1"></div>{FOOT}', '#FFF9EC')


def check_page(m):
    d = MONTHS[m]
    if m == 1:
        tasks = [
            ('1. 세어 보기', V1(tenframes(17), txt('□개', 18, True, INK, True))),
            ('2. 더 큰 수에 ○', row(cards([14, 9], 40) + txt('과', 16, True) + cards([12, 18], 40), 8, False)),
            ('3. 가르기', row(bond(10, 4, '', .85) + bond(7, '', 3, .85), 8, False)),
            ('4. 규칙 찾기', pattern(['cr', 'cb', 'cy', 'cr', 'cb', '?'], 30)),
            ('5. 세모에 ○', row(shape('s', 'b', 36) + shape('t', 'r', 36) + shape('c', 'g', 36) + shape('t', 'y', 36), 10, False)),
            ('6. 말로 설명', p('10을 둘로 나누는 방법을 한 가지 말하고 그려요.', 14)),
        ]
        ttl = '1개월차 점검: 숫자 마을 탐험대'
        nxt = '10 가르기가 불안하면 2개월차 1주를 복습 주간으로 써요.'
    elif m == 2:
        tasks = [
            ('1. 묶어 세기', V1(tenframes(38, '#2F7DE1', 14), txt('10묶음 □개, 낱개 □개', 15, True, INK, True))),
            ('2. 합치기', plusrow(4, 3, 'flower', 20)),
            ('3. 줄어들기', minusrow(7, 3, 'fish', 20)),
            ('4. 10 만들기', row(bond(10, '', 6, .85) + bond(10, 7, '', .85), 8, False)),
            ('5. 반쪽 그리기', sym(150, 100)),
            ('6. 말로 설명', p('5마리 중 2마리가 갔어요. 어떻게 풀었는지 그리고 말해요.', 14)),
        ]
        ttl = '2개월차 점검: 열 묶음 숲 모험'
        nxt = '덧셈·뺄셈 이야기를 그림으로 풀지 못하면 3개월차 1주를 이야기 복습으로 시작해요.'
    else:
        tasks = [
            ('1. 백 판 빈칸', hundred(81, 100, blanks=(83, 87, 91, 96, 99), cell=24)),
            ('2. 10씩 뛰기', numstrip([30, 40, '', 60, '', ''], 34)),
            ('3. 식 풀기', V1(eq('4', '+', '5', '=', '□', size=20), eq('9', '−', '6', '=', '□', size=20))),
            ('4. 몇 시일까요?', row(clockq(4, 70) + clockq(9, 70), 8, False)),
            ('5. 그래프 읽기', V1(bars(9, 6), txt('몇 개 더 많을까? □개', 15, True, INK, True))),
            ('6. 새로운 문제', p('연못에 오리가 5마리, 3마리가 더 와서 2마리가 갔어요. 몇 마리? 그림이나 말로 풀어요.', 13.5)),
        ]
        ttl = '3개월차 종합 진단: 백 마을 졸업 여행'
        nxt = '석 달 점검 결과를 채팅에 알려 주면 2권을 아이 수준에 맞춰 설계해요.'
    cells = ''
    for t, v in tasks:
        cells += f'<div style="border:2px solid #2B2A33;border-radius:14px;background:#fff;padding:8px 10px;box-sizing:border-box;height:158px;overflow:hidden"><div style="font-family:Jua;font-size:16px;color:#6C4FD6;margin-bottom:6px">{t}</div>{v}</div>'
    tbl = table(['영역', 'A 충분함', 'B 발달 중', 'C 보완 필요'], [[a, '☐', '☐', '☐'] for a in ['수와 수량', '가르기·계산', '도형·측정', '규칙·사고력', '말로 설명하기', '끈기와 태도']], None, 13, 3)
    crit = ['이해: 개념을 80% 이상 안다', '수행: 기본 문제 정확도 90% 이상', '설명: 자기 풀이를 말한다', '전이: 새 유형에 적용한다', '계산 때문에 사고가 막히지 않는다', '문제를 지나치게 싫어하지 않는다']
    critx = ''.join(f'<div style="font-size:13.5px;display:flex;gap:6px"><span>☐</span><span>{c}</span></div>' for c in crit)
    inner = f'''
<div style="height:56px;flex:none;display:flex;align-items:center;gap:12px">{bear(48)}{h(ttl, 26)}</div>
{p("아이가 풀 때 부모님은 도와주지 않고 지켜봐요. 모르는 문제는 건너뛰어도 괜찮아요.", 13.5, MUTE)}
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;flex:none">{cells}</div>
<div style="display:flex;gap:12px;flex:none"><div style="flex:1.1">{h("영역별 판정", 18)}<div style="margin-top:4px">{tbl}</div></div><div style="flex:1">{h("다음 달로 가는 기준", 18)}<div style="display:flex;flex-direction:column;gap:5px;margin-top:6px">{critx}</div></div></div>
{card(p("<b>결정</b>&nbsp; ☐ 그대로 다음 달 진행&nbsp;&nbsp; ☐ 1주 복습 후 진행&nbsp;&nbsp; ☐ 보완 영역 먼저<br>" + nxt, 13.5), "#FFF0C2", "#8A5A00", 8)}
<div style="flex:1"></div>{{FOOT}}
'''
    return doc(ttl, inner)


def V1(*a):
    return '<div style="display:flex;flex-direction:column;gap:6px">' + ''.join(a) + '</div>'


# ---------------------------------------------------------------- front matter
def cover():
    tiles = ''.join(f'<div style="width:54px;height:54px;border-radius:14px;background:{["#E5484D","#F5B301","#2F9E44","#2F7DE1","#8E5BD6"][i%5]};color:#fff;font-family:Jua;font-size:30px;display:flex;align-items:center;justify-content:center">{i+1}</div>' for i in range(10))
    stars = ''.join(f'<div style="position:absolute;left:{x}px;top:{y}px">{icon("star", s)}</div>' for x, y, s in [(70, 90, 40), (650, 70, 34), (120, 400, 28), (620, 440, 44), (330, 60, 26)])
    inner = f'''
{stars}
<div style="flex:1"></div>
<div style="text-align:center">{pill("6세 사고력 수학 · 12주 코스", "#fff", "#6C4FD6", 18)}</div>
<div style="text-align:center;font-family:Jua;font-size:84px;line-height:1.05;color:#fff;text-shadow:0 4px 0 #6C4FD6">은우의<br>수학 모험</div>
<div style="text-align:center;font-family:Jua;font-size:30px;color:#2B2A33">1권 · 숫자 마을 탐험 (1~100)</div>
<div style="display:flex;justify-content:center;align-items:flex-end;gap:30px">{bunny(190)}{bear(190)}</div>
<div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap">{tiles}</div>
<div style="margin:10px auto 0;width:520px;background:#fff;border:3px solid #2B2A33;border-radius:18px;padding:12px 20px;font-size:18px;display:flex;justify-content:space-between"><span>이름: <b>은우</b></span><span>시작한 날: ____월 ____일</span></div>
<div style="flex:1"></div>
'''
    return doc('은우의 수학 모험 1권', inner, '#BFE3FF', '36px 40px')


def glance():
    ws = lambda m: ''.join(f'<div style="display:flex;gap:8px;font-size:14px"><b style="width:44px;color:#6C4FD6">{w["n"]}주</b><span>{w["title"]} <span style="color:{MUTE}">({w["rng"]})</span></span></div>' for w in WEEKS if w['m'] == m)
    col = lambda m, c, t: f'<div style="flex:1;border:2px solid {c};border-radius:16px;background:#fff;padding:10px 12px;display:flex;flex-direction:column;gap:6px">{pill(f"{m}개월차 · 숫자 {MONTHS[m]["rng"]}", c, "#fff", 13)}{h(MONTHS[m]["title"], 18)}{ws(m)}<div style="font-size:13px;color:{MUTE};margin-top:2px">{t}</div></div>'
    diag = table(['영역', '지금 모습 (처음 한 번 표시)', 'A', 'B', 'C'], [
        ['수', '1~20을 정확히 세요 / 20 넘는 수를 알아요', '☐', '☐', '☐'], ['5와 10', '5와 10을 둘로 나눠요', '☐', '☐', '☐'], ['계산', '간단한 합치기·줄어들기를 말해요', '☐', '☐', '☐'],
        ['도형', '기본 도형 이름, 합치기, 위치', '☐', '☐', '☐'], ['사고력', '규칙 찾기, 분류, 경우 찾기', '☐', '☐', '☐'], ['설명', '자기 방법을 말해요', '☐', '☐', '☐'], ['태도', '한 문제를 오래 생각해요 / 틀려도 다시 해요', '☐', '☐', '☐']], None, 13, 3)
    inner = f'''
<div style="height:54px;flex:none;display:flex;align-items:center;gap:12px">{bunny(46)}{h("은우의 첫 12주 한눈에", 30)}</div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>① 현재 수준</b><br>처음에는 아직 몰라요. 1주차 월요일 전에 아래 표를 10분만 보고 A 충분함, B 발달 중, C 보완 필요로 표시해요. 1주차에 다시 확인해요.", 13.5), "#E3EEFF", "#1C64C8", 10, "flex:1")}
{card(p("<b>② 지금 가장 먼저</b><br>콩 세기, 5와 10 가르기, 규칙 찾기. 이 셋이 앞으로 모든 수학의 뿌리예요.", 13.5), "#EEE9FF", "#6C4FD6", 10, "flex:1")}
{card(p("<b>③ 지금 안 해도 되는 것</b><br>받아올림, 곱셈, 속도 훈련, 문제집 여러 권. 급하지 않아요.", 13.5), "#FFE3EE", "#BE185D", 10, "flex:1")}
</div>
<div style="flex:none">{h("현재 수준 확인표", 18)}<div style="margin-top:4px">{diag}</div></div>
<div style="flex:none">{h("④ 이번 3개월 · 12주 지도", 18)}</div>
<div style="display:flex;gap:10px;flex:none">{col(1, "#6C4FD6", "끝: 10 가르기·모으기를 콩 없이 말해요")}{col(2, "#C2410C", "끝: 덧셈·뺄셈 이야기를 그림으로 풀어요")}{col(3, "#18794E", "끝: 처음 보는 문제에 지금까지 배운 것을 써요")}</div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>⑤ 다음 단계로 가는 조건</b><br>이해 80%↑ · 기본 정확도 90%↑ · 풀이 설명 · 새 유형 적용 · 계산 때문에 막히지 않음 · 문제를 지나치게 싫어하지 않음. 이 6가지가 월말 점검표에 있어요.", 13.5), "#fff", "#7A798A", 10, "flex:1")}
{card(p("<b>⑥ 부모 체크포인트</b><br>토요일 10분만 확인해요. 얼마나 많이 풀었는지보다 왜 틀렸는지(몰랐어요 · 헷갈렸어요 · 실수했어요)를 적어요.", 13.5), "#FFF0C2", "#8A5A00", 10, "flex:1")}
</div>
{card(p("<b>더 보기</b> 주간 시간표와 질문법은 <b>사용법</b> 쪽, 6개월·1년 목표와 선행/심화 결정은 <b>로드맵 2/2</b> 쪽, 오려 쓰는 카드와 백 판은 <b>도구함</b> 쪽에 있어요.", 13), "#fff", "#7A798A", 8)}
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('은우의 첫 12주 한눈에', inner)


def guide():
    routine = table(['요일', '영역', '시간', '이렇게 해요'], [
        ['월', '<b style="color:#C2410C">연산</b> 10 + <b style="color:#6C4FD6">사고력</b>', '35분', '구체물로 만져 보고 이야기해요'],
        ['화', '<b style="color:#C2410C">연산</b> 10 + <b style="color:#18794E">도형·측정</b>', '25분', '오리고 붙이고 비교해요'],
        ['수', '<b style="color:#8A5A00">수학 놀이</b>', '20분', '게임과 보드게임, 부담 없이'],
        ['목', '<b style="color:#C2410C">연산</b> 10 + <b style="color:#1C64C8">교과 개념</b>', '30분', '교과 개념을 그림으로 확인해요'],
        ['금', '<b style="color:#C2410C">연산</b> 10 + <b style="color:#6C4FD6">사고력</b>', '35분', '월요일을 이어서 응용해요'],
        ['토', '<b style="color:#BE185D">심화</b> + 점검', '30분', '어려운 문제를 오래 생각해요 + 부모 점검'],
        ['일', '쉬기', '자유', '재미있었던 문제를 다시 보거나 쉬어요']], None, 14, 4)
    legend = ''.join(f'<div style="display:flex;align-items:center;gap:6px;font-size:13px">{pill(C[k][2], C[k][0], "#fff", 12)}<span>{t}</span></div>' for k, t in [('think', '사고력·선행 코스'), ('calc', '연산 준비 코스'), ('curr', '교과·나이별 진도'), ('deep', '심화 코스'), ('shape', '도형·측정·규칙·자료'), ('play', '게임과 놀이')])
    steps = [('1', '준비물 상자', '콩 20개, 주사위 2개, 색종이, 종이컵 2개, 연필. 이것만 있으면 돼요.'), ('2', '월요일에 펼치기', '1주차 A면을 펼치고 "10분 수 놀이"부터 시작해요.'), ('3', '토요일 점검', '그 주 B면 아래 점검표에 표시하고 결정해요.')]
    stp = ''.join(f'<div style="flex:1;display:flex;gap:10px;align-items:flex-start;background:#fff;border:2px solid #2B2A33;border-radius:14px;padding:10px"><div style="flex:none;width:34px;height:34px;border-radius:50%;background:#6C4FD6;color:#fff;font-family:Jua;font-size:20px;display:flex;align-items:center;justify-content:center">{n}</div><div style="font-size:13.5px;line-height:1.4"><b>{a}</b><br>{b}</div></div>' for n, a, b in steps)
    wrong = ''.join(f'<div style="flex:1;border:2px solid {c};border-radius:14px;background:{t};padding:10px;font-size:13.5px;line-height:1.45"><b style="color:{c}">{a}</b><br>{b}</div>' for a, b, c, t in [
        ('몰랐어요', '개념이 부족해요. 콩과 그림으로 처음부터 다시 만져 봐요.', '#C2410C', '#FFE9DC'), ('헷갈렸어요', '개념은 알아요. 비슷한 문제를 다른 모양으로 한 번 더 풀어요.', '#1C64C8', '#E3EEFF'), ('실수했어요', '주의가 흐트러졌어요. 천천히 다시 읽고 확인하는 습관만 잡아요.', '#18794E', '#DDF5E9')])
    inner = f'''
<div style="height:54px;flex:none;display:flex;align-items:center;gap:12px">{bear(46)}{h("이 책 사용법 · 오늘 저녁에 시작해요", 28)}</div>
<div style="display:flex;gap:10px;flex:none">{stp}</div>
<div style="flex:none">{h("색깔은 이 책의 네 가지 코스예요", 18)}<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-top:6px">{legend}</div></div>
<div style="flex:none">{h("1주일 시간표", 18)}<div style="margin-top:4px">{routine}</div></div>
<div style="flex:none">{h("틀렸을 때 이유를 세 가지로 나눠요", 18)}<div style="display:flex;gap:10px;margin-top:6px">{wrong}</div></div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>질문은 이 세 가지만 기억해요</b><br>① 왜 그렇게 생각했어?<br>② 다른 방법도 있을까?<br>③ 하나를 바꾸면 어떻게 될까?<br><b>틀렸을 때</b> 다시 읽기 → 그림·콩 → 힌트 하나 → 스스로. 설명은 마지막!", 13.5), "#EEE9FF", "#6C4FD6", 10, "flex:1")}
{card(p("<b>이럴 땐 멈춰요</b><br>사흘 연속 싫어하면 활동을 줄이고 놀이만 해요. 선행 속도도 늦춰요. 아이가 수학을 좋아하는 것이 가장 큰 진도예요.", 14), "#FFE3EE", "#BE185D", 10, "flex:1")}
</div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('이 책 사용법', inner)


def stagecard(age, head, rows, books, color):
    lines = ''.join(f'<div style="display:flex;gap:8px;font-size:12.5px;line-height:1.38"><b style="flex:0 0 58px;color:{color}">{a}</b><span style="flex:1">{b}</span></div>' for a, b in rows)
    return f'<div style="flex:none;border:2px solid {color};border-radius:16px;background:#fff;padding:8px 12px;display:flex;gap:12px"><div style="flex:0 0 92px;display:flex;flex-direction:column;gap:6px;align-items:flex-start">{pill(age, color, "#fff", 16)}<div style="font-family:Jua;font-size:15px;line-height:1.25">{head}</div><div style="font-size:12px;color:{MUTE}">{books}</div></div><div style="flex:1;display:flex;flex-direction:column;gap:3px">{lines}</div></div>'


def map1():
    cards_ = [
        ('6세', '수의 구조와<br>말하기', [('수·연산', '1~100 세기, 10 가르기·모으기, 덧셈·뺄셈의 의미(그림), 10 이하 암산 시작'), ('사고력', '구체물 → 그림 → 말. 규칙·분류·경우 찾기'), ('도형·측정', '평면·입체 이름, 합치기, 대칭 맛보기, 길이·무게 비교, 정각 시계'), ('교과·선행', '초1 핵심 개념을 놀이로 경험. 문제집 진도가 목표 아님')], '1권 (지금)', '#6C4FD6'),
        ('7세', '초1 안정화', [('수·연산', '100까지 수 구조 확실히, 20 이하 덧셈·뺄셈(받아올림 의미 경험), 두 자리 수 읽기·쓰기'), ('사고력', '표·그림으로 조건 정리, 거꾸로 생각하기, 여러 풀이'), ('도형·측정', '도형 특징, 쌓기, 탱그램, 비표준 길이 재기, 30분 시계, 표·그래프'), ('교과·선행', '초1 핵심 개념 안정. 준비되면 초2 개념을 가볍게 경험')], '2~5권', '#C2410C'),
        ('8세 · 초1', '초1 완성 +<br>초2 기본', [('수·연산', '받아올림·받아내림의 원리 이해, 두 자리 덧뺄셈 의미, 묶어 세기(곱셈 준비)'), ('사고력', '문장제를 그림·식으로 설명, 방법 비교, 경우의 수 기초'), ('도형·측정', '도형 구성과 분해, 규칙 추론, 길이 단위(cm), 시계 5분 단위'), ('교과·선행', '초1 완성 + 초2 기본. 선행은 6개월 안팎이 기본 범위')], '6~9권', '#18794E'),
        ('9세 · 초2', '초2 안정화 +<br>초3 개념 경험', [('수·연산', '곱셈의 의미와 구구 이해(암기는 이해 뒤), 세 자리 수'), ('사고력', '서술형 풀이, 규칙 수열, 논리 추론'), ('도형·측정', '길이·시간 단위 정리, 도형의 성질, 자료 해석'), ('교과·선행', '현재 학년 심화 우선. 초3 개념은 준비도에 따라 맛보기')], '10~13권', '#1C64C8'),
        ('10세 · 초3', '초3 + 개념 심화', [('수·연산', '나눗셈의 의미, 분수 개념, 곱셈 응용'), ('사고력', '왜 그런지 설명하기, 풀이 비교, 문제 만들기'), ('도형·측정', '도형 둘레·넓이 감각, 시간·들이·무게 단위'), ('교과·선행', '초3 안정 + 심화. 선행은 개념 이해가 단단할 때만')], '14~17권', '#BE185D'),
    ]
    cs = ''.join(stagecard(a, hd, r, b, c) for a, hd, r, b, c in cards_)
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}{h("6~10세 수학 로드맵 (1/2) · 나이별 큰 그림", 26)}</div>
{p("나이는 대략의 위치이고, 실제 속도는 월말 점검표가 정해요. 약 3개월에 한 권씩, 17권 정도를 계획해요.", 13, MUTE)}
{cs}
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('6~10세 수학 로드맵 1', inner)


def map2():
    goal = table(['시점', '은우의 목표'], [
        ['3개월 (1권 끝)', '수: 1~100 구조, 10 가르기, 10 이하 덧뺄셈 의미 · 도형: 합치기, 대칭 맛보기 · 말: 한 문장으로 설명'],
        ['6개월 (2권 끝)', '수: 20 이하 덧뺄셈(받아올림 경험), 두 자리 수 · 도형: 쌓기, 탱그램, 30분 시계 · 말: 이유를 두 문장으로'],
        ['1년 (4권 끝)', '초1 핵심 개념(100까지의 수, 덧셈·뺄셈, 모양, 시각, 규칙) 안정 · 설명 2~3문장 · 조건이 되면 초2 개념 맛보기']], None, 13.5, 5)
    decide = table(['월말 점검 결과', '다음 3개월'], [
        ['6가지 기준을 모두 통과', '선행: 다음 학년 개념을 조금 맛보기. 사고력·도형은 그대로 병행'],
        ['3~5가지 통과', '심화: 지금 개념을 다른 모양으로 깊게 풀기, 문제 만들기'],
        ['2가지 이하', '보완: 부족한 영역을 한 달 먼저 채우기, 선행은 멈추기']], None, 13.5, 5)
    ten = ['수량 감각', '사고력', '연산', '교과', '도형·공간', '측정·규칙·자료', '수학 문해력', '심화 문제해결', '선행', '학습 습관']
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h("6~10세 수학 로드맵 (2/2) · 이동 기준과 목표", 26)}</div>
<div style="flex:none">{h("다음 단계로 넘어가는 조건 (6가지 모두 확인)", 18)}
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:6px">{"".join(card(p(f"<b>{a}</b><br>{b}", 13), "#fff", "#7A798A", 8) for a, b in [("이해", "왜 그런지 안다 (80% 이상)"), ("수행", "기본 문제 정확도 90% 이상"), ("설명", "자기 풀이를 말한다"), ("전이", "숫자와 모양이 바뀌어도 쓴다"), ("부담 없음", "계산 때문에 사고가 막히지 않는다"), ("즐거움", "문제를 지나치게 싫어하지 않는다")])}</div></div>
<div style="flex:none">{h("선행할까 심화할까?", 18)}<div style="margin-top:4px">{decide}</div></div>
<div style="flex:none">{h("은우의 3·6·12개월 목표", 18)}<div style="margin-top:4px">{goal}</div></div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>8개 트랙을 함께 관리해요</b><br>" + " · ".join(ten) + "<br>한 영역만 앞서가지 않아요. 연산이 빨라도 수량 감각이나 도형이 약하면 연산 진도만 올리지 않아요.", 13), "#EEE9FF", "#6C4FD6", 10, "flex:1.2")}
{card(p("<b>학원·교재는 도구예요</b><br>이 책이 집에서의 중심이에요. 사고력 학원을 다니면 월·금 사고력 활동은 복습으로 바꿔요. 특정 학원의 진도표는 공식 자료로 확인된 것만 쓰고, 이 책에는 그대로 옮기지 않았어요.", 13), "#FFF0C2", "#8A5A00", 10, "flex:1")}
</div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('6~10세 수학 로드맵 2', inner)



def tools1():
    frames = ''.join(f'<div style="border:2px dashed #7A798A;border-radius:12px;padding:8px;background:#fff">{tenframe(0, 10, "#E5484D", 40)}</div>' for _ in range(6))
    cs = ''.join(f'<div style="height:78px;border:2px dashed #7A798A;border-radius:10px;background:#fff;display:flex;align-items:center;justify-content:center;font-family:Jua;font-size:34px">{i}</div>' for i in range(1, 21))
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}{h("도구함 (1/2) · 텐프레임과 숫자 카드", 26)}</div>
{p("점선을 따라 오려서 써요. 콩이나 단추를 칸에 놓아요. 교구를 따로 사지 않아도 돼요.", 13, MUTE)}
<div style="flex:none">{h("텐프레임 6장", 18)}<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:6px;justify-items:center">{frames}</div></div>
<div style="flex:none">{h("숫자 카드 1~20", 18)}<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:6px">{cs}</div></div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('도구함 1', inner)


def tools2():
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h("도구함 (2/2) · 백 판과 10 가르기 표", 26)}</div>
{p("백 판은 벽에 붙여 두고 9~12주에 써요. 10 가르기 표는 4주차와 6주차에 써요.", 13, MUTE)}
<div style="flex:none;display:flex;justify-content:center">{hundred(1, 100, cell=62)}</div>
<div style="flex:none">{h("10 가르기 표", 18)}<div style="margin-top:6px">{table(["10", "10", "10", "10", "10", "10", "10", "10", "10"], [["1 · 9", "2 · 8", "3 · 7", "4 · 6", "5 · 5", "6 · 4", "7 · 3", "8 · 2", "9 · 1"]], None, 15, 6)}</div></div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('도구함 2', inner)

# ---------------------------------------------------------------- records
def log():
    rows = []
    for w in WEEKS:
        rows.append([f'<b>{w["n"]}</b> {w["title"]}', '', '', '', '', '', '', ''])
    th = ['주차', '이해', '수행', '설명', '전이', '몰', '헷', '실', '결정 · 다음 주 반영']
    head = ''.join(f'<th style="border:1.5px solid #2B2A33;background:#F1EFE6;padding:5px 4px;font-size:12.5px">{t}</th>' for t in th)
    body = ''
    for w in WEEKS:
        body += f'<tr style="height:50px"><td style="border:1.5px solid #2B2A33;padding:2px 6px;font-size:13px;background:#fff;width:150px"><b style="color:#6C4FD6">{w["n"]}주</b> {w["title"]}</td>' + ''.join('<td style="border:1.5px solid #2B2A33;background:#fff"></td>' for _ in range(7)) + '<td style="border:1.5px solid #2B2A33;background:#fff;width:200px"></td></tr>'
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}{h("토요일 점검 기록표 (12주)", 28)}</div>
{p("◎ 잘함 ○ 보통 △ 더 필요 · 몰 = 몰랐어요 개수, 헷 = 헷갈렸어요 개수, 실 = 실수했어요 개수. 결정은 진행 · 복습 · 심화 중에 적어요.", 13, MUTE)}
<table style="border-collapse:collapse;width:100%;flex:none"><tr>{head}</tr>{body}</table>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('토요일 점검 기록표', inner)


def notes():
    box_ = lambda t, hh=120: card(p(f"<b>{t}</b>", 14) + lines(3), "#fff", "#7A798A", 10, f"height:{hh}px;flex:none;overflow:hidden")
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h("보완 노트 · 다음 책 준비", 28)}</div>
{p("12주가 끝나면 아래를 적어요. 매주 토요일에도 짧게 적어 두면 다음 주를 아이에게 맞출 수 있어요.", 13.5, MUTE)}
{box_("① 은우가 가장 즐거워한 활동")}
{box_("② 어려워했거나 싫어한 활동")}
{box_("③ 더 채워야 하는 영역 (수 · 가르기 · 도형 · 규칙 · 설명 · 끈기)")}
{box_("④ 2권에서 더 하고 싶은 것 / 줄이고 싶은 것")}
{card(p("<b>매주 토요일, 채팅에 이것만 알려 주세요</b><br>① 점검표 결과 (◎ ○ △ 와 틀린 이유 개수)<br>② 은우가 한 말 한 마디 (좋았던 것, 어려웠던 것)<br>③ 집중이 얼마나 지속됐는지, 기분은 어땠는지<br>그 내용으로 다음 주 활동을 더하거나 바꾸고, 필요한 부분은 보완해 드려요.", 14), "#EEE9FF", "#6C4FD6", 12, "flex:none")}
<div style="flex:1"></div>{{FOOT}}
'''
    return doc('보완 노트', inner)


# ---------------------------------------------------------------- assemble
files = []  # (filename, title, page, html, label)
files.append(('Main.dc.html', '표지', 'front', cover(), '표지'))
files.append(('f1_glance.dc.html', '12주 한눈에', 'front', glance(), '한눈에'))
files.append(('f2_guide.dc.html', '사용법', 'front', guide(), '사용법'))
files.append(('f3_map1.dc.html', '로드맵 1', 'front', map1(), '로드맵'))
files.append(('f4_map2.dc.html', '로드맵 2', 'front', map2(), '로드맵'))
files.append(('f5_tools1.dc.html', '도구함 1', 'front', tools1(), '도구함'))
files.append(('f6_tools2.dc.html', '도구함 2', 'front', tools2(), '도구함'))
for m in (1, 2, 3):
    files.append((f'm{m}_cover.dc.html', f'{m}개월차 표지', f'm{m}', month_cover(m), f'{m}개월차'))
    for w in [x for x in WEEKS if x['m'] == m]:
        a, b = week_pages(w)
        files.append((f'm{m}_w{w["n"]}a.dc.html', f'{w["n"]}주차 A', f'm{m}', doc(f'{w["n"]}주차 A', a), f'{m}개월차'))
        files.append((f'm{m}_w{w["n"]}b.dc.html', f'{w["n"]}주차 B', f'm{m}', doc(f'{w["n"]}주차 B', b, pad='26px 40px', gap=5), f'{m}개월차'))
    files.append((f'm{m}_check.dc.html', f'{m}개월차 점검', f'm{m}', check_page(m), f'{m}개월차'))
files.append(('r1_log.dc.html', '점검 기록표', 'rec', log(), '기록'))
files.append(('r2_notes.dc.html', '보완 노트', 'rec', notes(), '기록'))

boards, order, counters = {}, [], {}
for i, (fn, title, page, html_, label) in enumerate(files):
    pno = i + 1
    foot = footer(pno, label) if '{FOOT}' in html_ else ''
    html_ = html_.replace('{FOOT}', foot).replace('{PNO}', str(pno))
    # week pages carry their own footer placeholders already replaced via {PNO}
    html_ = html_.replace('{{PNO}}', str(pno))
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(html_)
    k = counters.get(page, 0)
    counters[page] = k + 1
    boards[fn] = dict(x=(k % 5) * 874, y=(k // 5) * 1243, w=794, h=1123, title=f'{pno}. {title}', page=page)
    order.append(fn)

canvas = dict(v=3, createdOnFiles=dict(v=1, at='2026-11-09T09:00:00Z'), title='은우의 수학 모험 1권',
              launch=dict(view='canvas'),
              pages=[dict(id='front', name='시작하기 · 로드맵'), dict(id='m1', name='1개월차'), dict(id='m2', name='2개월차'), dict(id='m3', name='3개월차'), dict(id='rec', name='기록')],
              boards=boards, order=order, notes={}, designSystems=[])
json.dump(canvas, open(os.path.join(OUT, 'canvas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(files), 'files')
