def _tool_blocks(k):
    rods = ''.join('<div style="width:30px;height:160px;border:2px dashed #7A798A;background:#EAF2FF;display:grid;grid-template-rows:repeat(10,1fr);flex:none">' + ''.join('<div style="border-bottom:1px solid #7A798A"></div>' for _ in range(10)) + '</div>' for _ in range(10))
    cubes = ''.join('<div style="width:30px;height:30px;border:2px dashed #7A798A;background:#FFF0C2;flex:none"></div>' for _ in range(20))
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}{h(f"도구함 ({k}/2) · 수 모형", 26)}</div>
{p("점선을 따라 오려요. 막대 하나는 10, 낱개 하나는 1이에요. 두 자리 수를 만들 때 써요.", 13, MUTE)}
<div style="flex:none">{h("10 막대 10개", 18)}<div style="display:flex;gap:10px;margin-top:6px">{rods}</div></div>
<div style="flex:none">{h("낱개 20개", 18)}<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:6px">{cubes}</div></div>
<div style="flex:none">{h("텐프레임 2장", 18)}<div style="display:flex;gap:16px;margin-top:6px">{tenframe(0, 10, "#E5484D", 44)}{tenframe(0, 10, "#E5484D", 44)}</div></div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc(f'도구함 {k}', inner)


def _tool_clock(k):
    import math
    face = svg(300, 300, ''.join(f'<text x="{150+118*math.cos(math.radians(i*30-90)):.1f}" y="{162+118*math.sin(math.radians(i*30-90)):.1f}" text-anchor="middle" font-size="26" font-weight="700" fill="#2B2A33">{i}</text>' for i in range(1, 13)) + ''.join(f'<line x1="{150+132*math.cos(math.radians(i*6-90)):.1f}" y1="{150+132*math.sin(math.radians(i*6-90)):.1f}" x2="{150+142*math.cos(math.radians(i*6-90)):.1f}" y2="{150+142*math.sin(math.radians(i*6-90)):.1f}" stroke="#2B2A33" stroke-width="2"/>' for i in range(60)) + '<circle cx="150" cy="150" r="142" fill="none" stroke="#2B2A33" stroke-width="4"/><circle cx="150" cy="150" r="6" fill="#2B2A33"/>', "0 0 300 300")
    hands = row('<div style="width:14px;height:90px;background:#2B2A33;border-radius:7px;flex:none"></div><div style="width:10px;height:130px;background:#C2410C;border-radius:5px;flex:none"></div>', 16, False, 'flex-end')
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h(f"도구함 ({k}/2) · 시계판", 26)}</div>
{p("시계판의 숫자를 따라 오리고, 짧은 바늘(검정)과 긴 바늘(주황)을 오려서 핀으로 가운데에 꽂아요. 눈금 하나는 1분, 숫자 하나는 5분이에요.", 13, MUTE)}
<div style="flex:none;display:flex;gap:24px;justify-content:center"><div style="width:300px;height:300px;flex:none">{face}</div>{hands}</div>
<div style="flex:none;display:flex;justify-content:center">{table(["시각", "짧은 바늘", "긴 바늘"], [["정각", "숫자 가리킴", "12"], ["30분", "두 숫자 사이", "6"], ["5분", "그 숫자 그대로", "1"]], None, 16, 6)}</div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc(f'도구함 {k}', inner)


def _tool_ruler(k):
    rl = lambda n: ruler(n, None, 37.8)
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}{h(f"도구함 ({k}/2) · 나만의 자", 26)}</div>
{p("점선을 따라 오려요. 0에 물건의 한쪽 끝을 맞추고 다른 쪽 끝의 눈금을 읽어요. 길이 활동(9~10주)에 써요.", 13, MUTE)}
<div style="flex:none">{h("10cm 자", 18)}<div style="margin-top:8px;border:2px dashed #7A798A;padding:10px;border-radius:12px;display:inline-block">{rl(10)}</div></div>
<div style="flex:none">{h("10cm 자 (한 개 더)", 18)}<div style="margin-top:8px;border:2px dashed #7A798A;padding:10px;border-radius:12px;display:inline-block">{rl(10)}</div></div>
<div style="flex:none">{h("재 볼 물건 막대", 18)}<div style="display:flex;flex-direction:column;gap:10px;margin-top:8px">{''.join(f'<div style="width:{n*37.8:.1f}px;height:28px;border:2px dashed #7A798A;background:{c};border-radius:6px;flex:none"></div>' for n, c in [(3, '#FFB3C7'), (5, '#BFE3FF'), (7, '#FFF0C2'), (9, '#DDF5E9')])}</div></div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc(f'도구함 {k}', inner)


def _tool_hundred(k):
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bear(44)}{h(f"도구함 ({k}/2) · 백 판과 10 가르기 표", 26)}</div>
{p("백 판은 벽에 붙여 두고 수 규칙을 찾을 때 써요. 10 가르기 표는 계산 전에 말로 확인해요.", 13, MUTE)}
<div style="flex:none;display:flex;justify-content:center">{hundred(1, 100, cell=62)}</div>
<div style="flex:none">{h("10 가르기 표", 18)}<div style="margin-top:6px">{table(["10", "10", "10", "10", "10", "10", "10", "10", "10"], [["1 · 9", "2 · 8", "3 · 7", "4 · 6", "5 · 5", "6 · 4", "7 · 3", "8 · 2", "9 · 1"]], None, 15, 6)}</div></div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc(f'도구함 {k}', inner)


def _tool_pattern(k):
    import math
    def poly(pts, col, w=70, h_=70):
        return svg(w, h_, f'<polygon points="{pts}" fill="{col}" stroke="#7A798A" stroke-width="2" stroke-dasharray="5 4"/>')
    tri = poly('35,6 66,64 4,64', '#FFB3C7')
    sq = poly('6,6 64,6 64,64 6,64', '#BFE3FF')
    rho = poly('20,6 66,6 50,64 4,64', '#FFF0C2')
    hexa = poly('20,6 50,6 66,35 50,64 20,64 4,35', '#DDF5E9')
    items = ''.join(f'<div style="flex:none">{x}</div>' for x in [tri] * 6 + [sq] * 6 + [rho] * 4 + [hexa] * 4)
    inner = f'''
<div style="height:50px;flex:none;display:flex;align-items:center;gap:12px">{bunny(44)}{h(f"도구함 ({k}/2) · 도형 조각", 26)}</div>
{p("점선을 따라 오려요. 세모 6개, 네모 6개, 마름모 4개, 육각형 4개로 새 모양을 만들고 도형 활동에 써요.", 13, MUTE)}
<div style="flex:none;display:flex;flex-wrap:wrap;gap:14px;justify-content:center;padding:10px;border:2px dashed #7A798A;border-radius:12px">{items}</div>
<div style="flex:none">{h("만들어 볼 모양", 18)}<div style="margin-top:6px">{table(["모양", "필요한 조각"], [["큰 세모", "세모 4개"], ["꽃", "육각형 1개 + 세모 6개"], ["기차", "네모 3개 + 세모 1개"]], None, 15, 6)}</div></div>
<div style="flex:1"></div>{{FOOT}}
'''
    return doc(f'도구함 {k}', inner)


TOOLFN = {'blocks': _tool_blocks, 'clock': _tool_clock, 'ruler': _tool_ruler, 'hundred': _tool_hundred, 'pattern': _tool_pattern}
