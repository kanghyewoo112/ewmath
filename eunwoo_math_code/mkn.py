import re, sys
s = open('build2.py', encoding='utf-8').read()
s = s.replace("from content2 import WEEKS", "import importlib, os as _os\nB = importlib.import_module(_os.environ['BOOKMOD'])\nWEEKS = B.WEEKS")
s = s.replace("OUT = '/home/claude/gen/out2/project'", "OUT = f'/home/claude/gen/out{B.NO}/project'")
s = s.replace("BOOK = '은우의 수학 모험 2권'", "BOOK = f'은우의 수학 모험 {B.NO}권'")
s = s.replace('"숫자 " + w["rng"]', 'w["rng"]')
# MONTHS
a = s.index('MONTHS = {'); b = s.index('def month_cover')
s = s[:a] + 'MONTHS = B.MONTHS\n\n\n' + s[b:]
s = s.replace('숫자 {d[\'rng\']}', "{d['rng']}").replace('숫자 {w["rng"]}', '{w["rng"]}')
# check_page
a = s.index('def check_page(m):'); b = s.index("    cells = ''", a)
s = s[:a] + "def check_page(m):\n    d = MONTHS[m]\n    tasks, ttl, nxt = B.CHECK[m]\n" + s[b:]
# glance
a = s.index('def glance():'); b = s.index('def guide():')
glance = '''def glance():
    ws = lambda m: ''.join(f'<div style="display:flex;gap:8px;font-size:14px"><b style="width:44px;color:#6C4FD6">{w["n"]}주</b><span>{w["title"]} <span style="color:{MUTE}">({w["rng"]})</span></span></div>' for w in WEEKS if w['m'] == m)
    col = lambda m, c, t: f'<div style="flex:1;border:2px solid {c};border-radius:16px;background:#fff;padding:10px 12px;display:flex;flex-direction:column;gap:6px">{pill(f"{m}개월차 · {MONTHS[m]['rng']}", c, "#fff", 13)}{h(MONTHS[m]["title"], 18)}{ws(m)}<div style="font-size:13px;color:{MUTE};margin-top:2px">{t}</div></div>'
    gate = table([f'{B.PREV}권 점검 결과 (처음 한 번 표시)', '통과', '일부', '보완'], [[g, '☐', '☐', '☐'] for g in B.GATE], None, 13, 3)
    inner = f\'\'\'
<div style="height:54px;flex:none;display:flex;align-items:center;gap:12px">{bear(46)}{h(f"{B.NO}권 · 은우의 다음 12주 한눈에", 30)}</div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>① 시작 조건</b><br>" + B.CARDS[0], 13.5), "#E3EEFF", "#1C64C8", 10, "flex:1")}
{card(p("<b>② 지금 가장 먼저</b><br>" + B.CARDS[1], 13.5), "#EEE9FF", "#6C4FD6", 10, "flex:1")}
{card(p("<b>③ 지금 안 해도 되는 것</b><br>" + B.CARDS[2], 13.5), "#FFE3EE", "#BE185D", 10, "flex:1")}
</div>
<div style="flex:none">{h(f"{B.PREV}권 결과 확인표", 18)}<div style="margin-top:4px">{gate}</div></div>
<div style="flex:none">{h("④ 이번 3개월 · 12주 지도", 18)}</div>
<div style="display:flex;gap:10px;flex:none">{col(1, "#6C4FD6", B.ENDS[0])}{col(2, "#C2410C", B.ENDS[1])}{col(3, "#18794E", B.ENDS[2])}</div>
<div style="flex:none;display:flex;gap:10px">
{card(p("<b>⑤ 다음 단계로 가는 조건</b><br>이해 80%↑ · 정확도 90%↑ · 설명 · 새 유형 적용 · 막히지 않음 · 싫어하지 않음. 월말 점검표에 있어요.", 13.5), "#fff", "#7A798A", 10, "flex:1")}
{card(p("<b>⑥ 부모 체크포인트</b><br>토요일 10분. 몇 문제를 풀었는지보다 왜 틀렸는지(몰랐어요 · 헷갈렸어요 · 실수했어요)를 적어요.", 13.5), "#FFF0C2", "#8A5A00", 10, "flex:1")}
</div>
{card(p("<b>더 보기</b> " + B.MORE, 13), "#fff", "#7A798A", 8)}
<div style="flex:1"></div>{{FOOT}}
\'\'\'
    return doc(f'{B.NO}권 한눈에', inner)


'''
s = s[:a] + glance + s[b:]
# cover
s = s.replace('{pill("7세 사고력 수학 · 12주 코스", "#fff", "#6C4FD6", 18)}', '{pill(B.AGE, "#fff", "#6C4FD6", 18)}')
s = s.replace('2권 · 십과 일, 10 채우기, 시계와 도형</div>', '{B.SUB}</div>')
s = s.replace("return doc('은우의 수학 모험 2권', inner, '#BFE3FF'", "return doc(BOOK, inner, '#BFE3FF'")
# tools
a = s.index('def tools1():'); b = s.index('# ---------------------------------------------------------------- records')
tools = open('tools_src.py', encoding='utf-8').read()
s = s[:a] + tools + '\n\n' + open('extras_v2.py', encoding='utf-8').read() + '\n\n' + s[b:]
s = s.replace("tools1(), '도구함'", "TOOLFN[B.TOOLS[0]](1), '도구함'").replace("tools2(), '도구함'", "TOOLFN[B.TOOLS[1]](2), '도구함'")
# 앞부분 중복 설명 제거, 추가 문제 쪽 삽입
s = s.replace("files.append(('f1_glance.dc.html', '12주 한눈에', 'front', glance(), '한눈에'))\n", '')
s = s.replace("files.append(('f2_guide.dc.html', '사용법', 'front', guide(), '사용법'))\n", '')
old = "        a, b = week_pages(w)\n"
i0 = s.index(old); i1 = s.index("    files.append((f'm{m}_check")
loop = """        a, b = week_pages(w)
        n_ = w["n"]
        files.append((f'm{m}_w{n_}a.dc.html', f'{n_}주차 A', f'm{m}', doc(f'{n_}주차 A', a), f'{m}개월차'))
        for q, inner in enumerate(extra_pages(w, 0)):
            files.append((f'm{m}_w{n_}am{q+1}.dc.html', f'{n_}주차 A 더풀기{q+1}', f'm{m}', doc(f'{n_}주차 A 더풀기', inner, pad='26px 40px', gap=6), f'{m}개월차'))
        files.append((f'm{m}_w{n_}b.dc.html', f'{n_}주차 B', f'm{m}', doc(f'{n_}주차 B', b, pad='26px 40px', gap=5), f'{m}개월차'))
        for q, inner in enumerate(extra_pages(w, 1)):
            files.append((f'm{m}_w{n_}bm{q+1}.dc.html', f'{n_}주차 B 더풀기{q+1}', f'm{m}', doc(f'{n_}주차 B 더풀기', inner, pad='26px 40px', gap=6), f'{m}개월차'))
"""
s = s[:i0] + loop + s[i1:]
s = s.replace("    files.append((f'm{m}_check.dc.html', f'{m}개월차 점검', f'm{m}', check_page(m), f'{m}개월차'))\n", "    files.append((f'm{m}_check.dc.html', f'{m}개월차 점검', f'm{m}', check_page(m), f'{m}개월차'))\n    for q, ahtml in enumerate(answer_pages(m)):\n        files.append((f'm{m}_ans{q+1}.dc.html', f'{m}개월차 정답{q+1}', f'm{m}', ahtml, f'{m}개월차'))\n")
s = s.replace("files = []  # (filename", "for _f in os.listdir(OUT):\n    if _f.endswith('.dc.html'): os.remove(os.path.join(OUT, _f))\nfiles = []  # (filename")
# notes
s = s.replace('보완 노트 · 3권 준비', '보완 노트 · {B.NO + 1}권 준비').replace('④ 3권에서 더 하고 싶은 것', '④ {B.NO + 1}권에서 더 하고 싶은 것')
s = s.replace("title='은우의 수학 모험 2권',", "title=BOOK,")
open(f'build_gen.py', 'w', encoding='utf-8').write(s)
