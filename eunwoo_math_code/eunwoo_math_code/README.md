# 은우 수학 모험 생성 코드
- gen.py: 문제 생성기(kind_items), 정답은 코드로 계산
- probs.py / probs2~5.py: 직접 쓴 문제표 (P, X[2..5])
- content2b.py, content3~5.py: 권별 주차·월 내용
- build2.py + mkn.py: 권별 빌드 스크립트 생성(BOOKMOD=<모듈>), 출력 out{N}/project
- extras_v2.py: 더 풀어 보기 9파트 구성과 쪽 나누기
- pdfn.py N: PDF 변환 및 쪽 넘침 점검
필요: Python 3, playwright(chromium)
