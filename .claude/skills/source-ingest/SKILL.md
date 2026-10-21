---
name: source-ingest
description: L2 종목 에이전트가 리서치를 개시할 때 사용. EDGAR full-text 검색으로 1차 공시를 수집하고, 웹검색 결과와 병합해 evidence_grade를 자동 부여하고 중복을 제거한다.
---

# source-ingest — 1차 자료 수집·등급 부여 (D15 하이브리드)

## 수집 경로

1. **공시 [CODE]:** `python .claude/skills/source-ingest/scripts/edgar_fulltext.py --ticker <T> --forms <coverage.yaml의 edgar_forms> --since <기간>`
   - 서식은 coverage.yaml의 `edgar_forms`를 따르되, 발행사 지위는 바뀔 수 있다 — `--since` 조회가 0건이면 서식 가정부터 재검증(submissions API의 최근 form 분포 확인). 예: IREN은 2025-07 외국 발행사→국내 신고인 전환(20-F/6-K → 8-K/10-Q/10-K)
   - `--forms` 필터는 정확 일치 — 두 단어 서식은 따옴표 필요(`"SCHEDULE 13G"`), 와일드카드(`424B*`) 불가
2. **뉴스·규제 [LLM 웹검색]:** 날짜 한정 + 지표 지정 쿼리 (예: `"CRCL" "August 18 2026" USDC circulation reserve income`). 규제(SEC 보도자료·의회 법안·PUCT)는 기관 도메인 우선

## 등급 부여 규칙 (P4)

- `config/sources.yaml` 도메인 매핑으로 `evidence_grade` 자동 부여. 미등재 도메인 = 4
- 웹검색 항목은 **1차 자료 URL 역추적 의무** — 역추적 성공 시 1차 URL로 대체, 실패 시 `confirmed: false`
- grade 2(경영진 직접 발언)는 스크립트가 부여하지 않는다 — 직접 인용 확인 후 에이전트가 수동 부여
- 애그리게이터 캘린더의 자동 추정 라벨은 grade와 무관하게 판정 근거 불가 (F1)

## 출력

`RawItem[]` — `{id, ticker, title, url, domain, evidence_grade, published_at, retrieved_at, dedup_key}`. 동일 사실 중복 병합(최고 등급 소스로 대표). 1차 자료 미확보 항목은 `unconfirmed` 후보로 표기(P5).
