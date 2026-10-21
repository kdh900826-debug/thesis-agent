---
name: noise-triage
description: source-ingest 결과가 존재할 때 사용. config/noise_filter.yaml 기준으로 잡뉴스를 걸러내고 승격 여부를 판정한다. 애매하면 승격(보수적).
---

# noise-triage — 잡뉴스 필터 / 승격 판정 (P3)

## 판정 절차

1. **[CODE 성격]** `config/noise_filter.yaml`의 공통 + 해당 종목 noise 패턴 대조
2. **[LLM]** 패턴 일치 항목도 `promote_if` 조건(매출·가이던스·마진·현금흐름·고객명·수주·양산일정 변화, KC 트리거·접근, 규제 확정) 중 하나라도 포함하면 **승격**
3. **애매하면 승격한다** — 잘못된 승격의 비용(알림 1건) < 잘못된 폐기의 비용(thesis 훼손 미탐지) (v1 §9-2)

## 출력

각 RawItem에 `{promote: bool, reason: "일치한 패턴/조건 명시"}`. 폐기 항목은 **로그만 남기고 버린다** (Run 로그에 기록 — 감사 추적).

## 금지

- P3의 7개 변화 항목 중 하나도 건드리지 않는 정보를 승격하는 것 (사유 없는 승격)
- 노이즈 판정을 이유로 원문 기록 자체를 생략하는 것 (dedup_key와 제목은 로그에 남긴다)
