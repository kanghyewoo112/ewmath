import os, re, subprocess, sys
# 1) 기존 패치(mkn)로 build_gen.py 생성
exec(open('mkn.py', encoding='utf-8').read())
s = open('build_gen.py', encoding='utf-8').read()
# 출력 폴더 보장
s = s.replace("for _f in os.listdir(OUT):", "os.makedirs(OUT, exist_ok=True)\nfor _f in os.listdir(OUT):")
# 2) 공통 쪽 코드 삽입
common = open('common_src.py', encoding='utf-8').read()
s = s.replace("# ---------------------------------------------------------------- assemble", common + "\n\n# ---------------------------------------------------------------- assemble")
# 3) 앞쪽 구성: 표지 → 한눈에 → 주간표 → 공통 5쪽 → 도구함
front = ("files.append(('f1_glance.dc.html', '한눈에', 'front', glance(), '한눈에'))\n"
         "files.append(('f2_map.dc.html', '주간표', 'front', c_map(), '주간표'))\n"
         "files.append(('f3_long.dc.html', '6~13세 긴 지도', 'front', c_long(), '긴 지도'))\n"
         "files.append(('f4_eval.dc.html', '평가 방법', 'front', c_eval(), '평가 방법'))\n"
         "files.append(('f4b_academy.dc.html', '학원 조사표', 'front', c_academy(), '학원 조사표'))\n"
         "files.append(('f4c_sources.dc.html', '출처와 한계', 'front', c_sources(), '출처와 한계'))\n"
         "files.append(('f4d_research.dc.html', '연구 근거', 'front', c_research(), '연구 근거'))\n")
i = s.index("files.append(('f5_tools1")
s = s[:i] + front + s[i:]
# 4) 월말 점검: 5축 + A·B·C·D 판정
s = s.replace("['수와 수량', '가르기·계산', '도형·측정', '규칙·사고력', '말로 설명하기', '끈기와 태도']", "['개념 (왜 그런지)', '연산 (정확하게)', '전략 (방법 고르기)', '추론 (이유 말하기)', '태도 (다시 해 보기)']")
s = s.replace('h("영역별 판정", 18)', 'h("5축 판정", 18)')
s = re.sub(r"crit = \[.*?\]\n", "crit = ['A 계산: 6문제 중 5개 이상 (천천히)', 'B 개념: 그림·말로 왜 그런지 보여 준다', 'C 적용: 이야기 문제를 풀고 식으로 쓴다', 'D 전이: 숫자·상황이 바뀌어도 쓴다', '계산 때문에 사고가 막히지 않는다', '문제를 지나치게 싫어하지 않는다']\n", s, count=1, flags=re.S)
s = s.replace('h("다음 달로 가는 기준", 18)', 'h("다음 달로 가는 기준 (4문제 판정)", 18)')
# 5) 토요일 복습 줄 (3권부터)
s = s.replace("    return f'<div style=\"flex:none;border-top:2px dashed #BE185D;padding:5px 14px 4px;background:#FFF7FA\">", "    rev = '<div style=\"display:flex;align-items:center;gap:8px;height:24px;font-size:13px\"><b>토요일 복습</b><span>이번 주 3 + 지난주 1 + 지난달 1 = 5문제 이내, 방법을 고르는 연습</span></div>' if B.NO >= 3 else ''\n    return f'<div style=\"flex:none;border-top:2px dashed #BE185D;padding:5px 14px 4px;background:#FFF7FA\">", 1)
s = s.replace("{why}{nxt}{memo}</div>'", "{why}{rev}{nxt}{memo}</div>'")
a_ = s.index('def satcheck'); b_ = s.index('def week_pages')
seg = s[a_:b_].replace('height:22px', 'height:20px').replace('height:24px', 'height:21px').replace('height:18px', 'height:16px')
s = s[:a_] + seg + s[b_:]
# 6) 한눈에: 이전 권 결과 확인표 이름
open('build_gen.py', 'w', encoding='utf-8').write(s)
print('patched')
