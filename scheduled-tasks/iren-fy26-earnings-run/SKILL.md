---
name: iren-fy26-earnings-run
description: IREN FY26 실적(8/27 17:00 ET 발표) S2E 대응 — thesis-agent에서 run earnings IREN 1회 실행
---

작업 디렉토리(세션 cwd): C:\Users\user\Desktop\클로드\투자 가설 검증 — 시스템 루트는 그 하위 thesis-agent\.

이 프로젝트는 투자 Thesis 검증 에이전트 시스템이다. thesis-agent/CLAUDE.md(오케스트레이터 지침)를 먼저 읽고 그 규약을 전부 따르라. 오늘 실행할 명령은 **`run earnings IREN`** (S2E 실적 대응 모드) — IREN이 2026-08-27 17:00 ET(한국시간 8/28 06:00)에 발표한 FY26 실적(회계연도 2026-06-30 종료)을 처리한다.

**명령 실행 형식 (권한 자동 승인을 위해 반드시 준수):** 모든 Bash 명령은 `cd` 접두사나 `&&` 복합 없이, 프로젝트 루트(cwd) 기준 상대경로로 실행하라 — 예: `PYTHONIOENCODING=utf-8 python thesis-agent/.claude/skills/state-audit/scripts/state_audit.py`. 프로젝트 설정(.claude/settings.json)의 allow 규칙이 `python *` / `PYTHONIOENCODING=utf-8 python *` 접두사만 자동 승인한다. 스크립트 출력 경로 인자도 `thesis-agent/output/...` 형태 상대경로로 준다(스크립트 내부 ROOT 상대 경로는 자동 처리됨).

절차 요약 (CLAUDE.md·설계서 v2 §5 S2E 준수):
1. state-audit 스크립트(thesis-agent/.claude/skills/state-audit/scripts/state_audit.py)로 시작해 RunPlan 기록. Python 실행 시 PYTHONIOENCODING=utf-8 필수.
2. 사전 준비 브리핑을 읽어라: thesis-agent/output/20260816_0000/earnings_prep_IREN_20260827.md — 체크포인트 13항목별 기준선·판정 함의·D-day 실행 순서가 정리돼 있다.
3. L2(company-iren 정의 준수, thesis-agent/.claude/agents/company-iren.md)로 1차 자료 수집: EDGAR 8-K/exhibit·IR 자료 우선(thesis-agent/.claude/skills/source-ingest/scripts/edgar_fulltext.py --ticker IREN --forms 8-K 10-Q 10-K), 애그리게이터 헤드라인 수치 금지(F1). 콜 발언은 grade 2.
4. 카드(thesis-agent/state/thesis_cards/IREN.yaml)의 earnings_checkpoints 13항목 전건을 확인/미확인/상충으로 분류한 대조표 작성. 미공개는 unconfirmed(P5). beat/miss 서술 시 컨센서스 소스 명시(F8). 완전희석 주수는 단일값 금지·range(F9). 밸류 변동은 분자/분모 분해(P10).
5. thesis-agent/.claude/scripts/filter_arbiter_input.py로 필터본 생성 후 signal-arbiter 판정(상향은 3중 게이트 — Horizon 1 매출 인식 금액·시점이 유일한 revenue_recognized 후보). 등급 확정은 사람 — 후보까지만.
6. validate_output.py 자기 검증(company·signal 계층) 통과 필수.
7. 완료 후 사용자에게 보고: 체크포인트 대조 결과(13항목 분류), 시그널 후보 판정과 게이트 체크, KC-10·가격 라인($30/$28) 상태, ThesisPatch 후보(있다면 승인 큐 등재 — 목록형 필드 패치는 expected_after.counts 필수, F20), correlation_matrix의 IREN CRYPTO +M 재평가 제안(매출 믹스 확인 후 — 2026-08-15 사용자 예약 사항).

제약: 매수·매도 지시·목표가·목표 비중 단일값 생성 금지(P15). thesis 카드 자동 수정 금지 — ThesisPatch는 승인 큐 등재까지만(F17). 모든 문장 fact/inference 태깅(P1). 권한 프롬프트가 떠서 진행이 막히면 해당 단계를 건너뛰지 말고 어떤 명령이 막혔는지 보고에 명시하라.