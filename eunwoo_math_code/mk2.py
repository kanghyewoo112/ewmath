import re
b = open('build.py', encoding='utf-8').read()
b = b.replace("from content import WEEKS", "from content2 import WEEKS")
b = b.replace("OUT = '/home/claude/gen/out/project'", "OUT = '/home/claude/gen/out2/project'")
b = b.replace("BOOK = '은우의 수학 모험 1권'", "BOOK = '은우의 수학 모험 2권'")

months = '''MONTHS = {
    1: dict(title='십과 일 탐험대', rng='두 자리 수', kid=['두 자리 수를 십과 일로 읽어요', '10과 몇으로 수를 만들어요', '두 자리 수의 크기를 비교해요'],
            focus='1권 복습, 두 자리 수 구조, 크기 비교', skip='받아올림 계산 속도, 세 자리 수, 문제집 진도 나가기', end='두 자리 수를 막대와 낱개로 설명할 수 있어요.'),
    2: dict(title='10 채우기 모험', rng='20까지 계산', kid=['9에 하나를 옮겨 10을 만들어요', '8과 7도 10을 만들어 더해요', '십몇에서 몇을 빼요'],
            focus='10 만들어 더하기(받아올림의 원리), 십몇 빼기 몇, 이야기 문제', skip='두 자리 수 덧셈, 받아내림 속도 훈련, 곱셈', end='20 이하 덧셈·뺄셈을 그림으로 풀고 말로 설명해요.'),
    3: dict(title='시계와 도형 졸업 여행', rng='시계·도형·규칙', kid=['30분 시계를 읽어요', '도형 조각으로 새 모양을 만들어요', '규칙을 만들고 조건을 정리해요'],
            focus='30분 시계, 도형 조각과 쌓기, 규칙 만들기와 자료', skip='분 단위 시계, 곱셈구구, 초2 문제집', end='6개월 동안 배운 것을 처음 보는 문제에 써요.'),
}


'''
b = re.sub(r"MONTHS = \{.*?\n\}\n\n\n", lambda m: months, b, count=1, flags=re.S)

check = '''def check_page(m):
    d = MONTHS[m]
    if m == 1:
        tasks = [
            ('1. 십과 일', V1(blocks(3, 6), txt('□ 십 □ 일 → □', 16, True, INK, True))),
            ('2. 10과 몇', V1(tenframes(15, '#E5484D', 16), txt('10과 □ → □', 16, True, INK, True))),
            ('3. 더 큰 수에 ○', row(cards([37, 73], 40) + txt('과', 16, True) + cards([58, 52], 40), 8, False)),
            ('4. 앞수·뒷수', numstrip([39, '', 41, '', 43], 34)),
            ('5. 순서 놓기', V1(cards([42, 17, 65], 36), numstrip(['', '', ''], 34))),
            ('6. 말로 설명', p('46이 64보다 작은 이유를 말하고 그려요.', 14)),
        ]
        ttl = '1개월차 점검: 십과 일 탐험대'
        nxt = '두 자리 수 구조가 불안하면 2개월차 1주를 수 모형 복습으로 써요.'
    elif m == 2:
        tasks = [
            ('1. 10 만들기', row(tenframe(9, 10, '#E5484D', 18) + txt('+', 18, True, INK, True) + tenframe(4, 10, '#E5484D', 18), 8, False)),
            ('2. 9 + 몇', V1(eq('9', '+', '5', '=', '□', size=20), eq('8', '+', '6', '=', '□', size=20))),
            ('3. 10에서 빼기', V1(eq('10', '−', '4', '=', '□', size=20), eq('14', '−', '4', '=', '□', size=20))),
            ('4. 이야기 풀이', p('사과 7개에 5개가 더 왔어요. 모두 몇 개? 그림이나 말로 풀어요.', 13.5)),
            ('5. 표 읽기', V1(table(['사과', '딸기', '귤'], [['6', '3', '4']], None, 14, 4), txt('가장 많은 것에 ○', 14, True, MUTE))),
            ('6. 말로 설명', p('왜 9 + 4가 10 + 3과 같을까? 그림을 그려 설명해요.', 13.5)),
        ]
        ttl = '2개월차 점검: 10 채우기 모험'
        nxt = '10 만들기를 설명하지 못하면 3개월차 1주를 텐프레임 복습으로 시작해요.'
    else:
        tasks = [
            ('1. 몇 시일까요?', row(clockq2(4, False, 62) + clockq2(9, True, 62), 6, False)),
            ('2. 변과 꼭짓점', table(['모양', '변', '꼭짓점'], [['세모', '□', '□'], ['네모', '□', '□']], None, 13, 3)),
            ('3. 쌓기 블록', V1(stackview([2, 3, 1], 20), txt('모두 □개', 14, True, INK, True))),
            ('4. 규칙 찾기', V1(numstrip([4, 8, 12, '', 20, ''], 30), txt('몇씩 커져요? □', 14, True, INK, True))),
            ('5. 새로운 문제', p('사탕 9개에 6개가 더 생겼고 4개를 먹었어요. 몇 개? 그림이나 말로 풀어요.', 13)),
            ('6. 말로 설명', p('6개월 동안 가장 재미있었던 것을 한 문장으로 말해요.', 14)),
        ]
        ttl = '3개월차 종합 진단: 시계와 도형 졸업 여행'
        nxt = '점검 결과를 채팅에 알려 주면 3권을 아이 수준에 맞춰 설계해요.'
'''
b = re.sub(r"def check_page\(m\):\n    d = MONTHS\[m\]\n.*?(    cells = '')", lambda m_: check + m_.group(1), b, count=1, flags=re.S)

glance = '''def glance():
    ws = lambda m: ''.join(f'<div style="display:flex;gap:8px;font-size:14px"><b style="width:44px;color:#6C4FD6">{w["n"]}주</b><span>{w["title"]} <span style="color:{MUTE}">({w["rng"]})</span></span></div>' for w in WEEKS if w['m'] == m)
    col = lambda m, c, t: f'<div style="flex:1;border:2px solid {c};border-radius:16px;background:#fff;padding:10px 12px;display:flex;flex-direction:column;gap:6px">{pill(f"{m}개월차 · {MONTHS[m]["rng"]}", c, "#fff", 13)}{h(MONTHS[m]["title"], 18)}{ws(m)}<div style="font-size:13px;color:{MUTE};margin-top:2px">{t}</div></div>'
    gate = table(['1권 점검 결과 (처음 한 번 표시)', '통과', '일부', '보완'], [
        ['10 가르기·모으기를 정확히 안다', '☐', '☐', '☐'], ['1~100의 수 구조를 안다', '☐', '☐', '☐'], ['덧셈·뺄셈의 의미를 그림으로 설명한다', '☐', '☐', '☐'],
        ['정각 시계와 규칙 띠를 한다', '☐', '☐', '☐'], ['자기 풀이를 한두 문장으로 말한다', '☐', '☐', '☐'], ['문제를 싫어하지 않고 해 본다', '☐', '☐', '☐']], None, 13, 3)
    inner = f\'\'\'
<div style="height:54px;flex:none;display:flex;align-items:center;gap:12px">{bear(46)}{h("2권 · 은우의 다음 12주 한눈에", 30)}</div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>① 시작 조건</b><br>1권 점검에서 6가지 기준이 대부분 통과면 바로 시작해요. 보완이 많으면 1주차를 두 번 반복해요.", 13.5), "#E3EEFF", "#1C64C8", 10, "flex:1")}
{card(p("<b>② 지금 가장 먼저</b><br>두 자리 수 구조(십과 일)와 10 만들기. 받아올림 계산의 뿌리예요.", 13.5), "#EEE9FF", "#6C4FD6", 10, "flex:1")}
{card(p("<b>③ 지금 안 해도 되는 것</b><br>세 자리 수, 곱셈, 속도 훈련, 문제집 여러 권. 급하지 않아요.", 13.5), "#FFE3EE", "#BE185D", 10, "flex:1")}
</div>
<div style="flex:none">{h("1권 결과 확인표", 18)}<div style="margin-top:4px">{gate}</div></div>
<div style="flex:none">{h("④ 이번 3개월 · 12주 지도", 18)}</div>
<div style="display:flex;gap:10px;flex:none">{col(1, "#6C4FD6", "끝: 두 자리 수를 막대와 낱개로 설명해요")}{col(2, "#C2410C", "끝: 20 이하 덧뺄셈을 그림으로 풀어요")}{col(3, "#18794E", "끝: 6개월 배운 것을 새 문제에 써요")}</div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>⑤ 다음 단계로 가는 조건</b><br>1권과 같아요. 이해 80%↑ · 정확도 90%↑ · 설명 · 새 유형 적용 · 막히지 않음 · 싫어하지 않음. 월말 점검표에 있어요.", 13.5), "#fff", "#7A798A", 10, "flex:1")}
{card(p("<b>⑥ 부모 체크포인트</b><br>토요일 10분. 몇 문제를 풀었는지보다 왜 틀렸는지(몰랐어요 · 헷갈렸어요 · 실수했어요)를 적어요.", 13.5), "#FFF0C2", "#8A5A00", 10, "flex:1")}
</div>
{card(p("<b>더 보기</b> 6~10세 로드맵과 주간 시간표는 <b>1권</b>에 있어요. 2권 도구함에는 수 모형과 시계판이 있어요.", 13), "#fff", "#7A798A", 8)}
<div style="flex:1"></div>{{FOOT}}
\'\'\'
    return doc('2권 한눈에', inner)


'''
b = re.sub(r"def glance\(\):.*?(def guide\(\):)", lambda m_: glance + m_.group(1), b, count=1, flags=re.S)

tools = '''def tools1():
    rods = ''.join('<div style="width:30px;height:160px;border:2px dashed #7A798A;background:#EAF2FF;display:grid;grid-template-rows:repeat(10,1fr);flex:none">' + ''.join('<div style="border-bottom:1px solid #7A798A"></div>' for _ in range(10)) + '</div>' for _ in range(10))
    cubes = ''.join('<div style="width:30px;height:30px;border:2px dashed #7A798A;background:#FFF0C2;flex:none"></div>' for _ in range(20))
    inner = f\'\'\'
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}{h("도구함 (1/2) · 수 모형", 26)}</div>
{p("점선을 따라 오려요. 막대 하나는 10, 낱개 하나는 1이에요. 두 자리 수를 만들 때 써요.", 13, MUTE)}
<div style="flex:none">{h("10 막대 10개", 18)}<div style="display:flex;gap:10px;margin-top:6px">{rods}</div></div>
<div style="flex:none">{h("낱개 20개", 18)}<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:6px">{cubes}</div></div>
<div style="flex:none">{h("텐프레임 2장", 18)}<div style="display:flex;gap:16px;margin-top:6px">{tenframe(0, 10, "#E5484D", 44)}{tenframe(0, 10, "#E5484D", 44)}</div></div>
<div style="flex:1"></div>{{FOOT}}
\'\'\'
    return doc('도구함 1', inner)


def tools2():
    face = lambda: svg(300, 300, ''.join(f'<text x="{150+118*__import__("math").cos(__import__("math").radians(i*30-90)):.1f}" y="{162+118*__import__("math").sin(__import__("math").radians(i*30-90)):.1f}" text-anchor="middle" font-size="26" font-weight="700" fill="#2B2A33">{i}</text>' for i in range(1, 13)) + '<circle cx="150" cy="150" r="142" fill="#fff" stroke="#2B2A33" stroke-width="4"/><circle cx="150" cy="150" r="6" fill="#2B2A33"/>', "0 0 300 300")
    hands = row('<div style="width:14px;height:90px;background:#2B2A33;border-radius:7px;flex:none"></div><div style="width:10px;height:130px;background:#C2410C;border-radius:5px;flex:none"></div>', 16, False, 'flex-end')
    inner = f\'\'\'
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h("도구함 (2/2) · 시계판", 26)}</div>
{p("시계판의 숫자를 따라 오리고, 짧은 바늘(검정)과 긴 바늘(주황)을 오려서 핀으로 가운데에 꽂아요. 9~12주에 써요.", 13, MUTE)}
<div style="flex:none;display:flex;gap:24px;justify-content:center"><div style="width:300px;height:300px;flex:none">{face()}</div>{hands}</div>
<div style="flex:none;display:flex;justify-content:center">{table(["몇 시", "짧은 바늘", "긴 바늘"], [["정각", "숫자 가리킴", "12"], ["30분", "두 숫자 사이", "6"]], None, 16, 6)}</div>
<div style="flex:1"></div>{{FOOT}}
\'\'\'
    return doc('도구함 2', inner)


'''
b = re.sub(r"def tools1\(\):.*?(# -{20,} records)", lambda m_: tools + m_.group(1), b, count=1, flags=re.S)

b = b.replace("files.append(('f3_map1.dc.html', '로드맵 1', 'front', map1(), '로드맵'))\n", "").replace("files.append(('f4_map2.dc.html', '로드맵 2', 'front', map2(), '로드맵'))\n", "")
b = b.replace("1권 · 숫자 마을 탐험 (1~100)", "2권 · 십과 일, 10 채우기, 시계와 도형").replace("은우의 수학 모험 1권", "은우의 수학 모험 2권").replace("6세 사고력 수학 · 12주 코스", "7세 사고력 수학 · 12주 코스").replace("다음 책 준비", "3권 준비").replace("2권에서 더 하고 싶은 것", "3권에서 더 하고 싶은 것").replace("다음 책(2권)", "다음 책(3권)")
b = b.replace("title='은우의 수학 모험 2권'", "title='은우의 수학 모험 2권'")
open('build2.py', 'w', encoding='utf-8').write(b)
