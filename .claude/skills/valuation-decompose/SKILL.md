---
name: valuation-decompose
description: 밸류에이션 관련 Claim 발생 시 또는 run earnings 실행 시 사용. 멀티플 변동을 분자/분모 기여로 분해하고, 분모 미확정 시 range를 산출한다.
---

# valuation-decompose — 분자/분모 분해 (P10, F6·F9)

## ValuationSnapshot 스키마 (v1 §4)

```jsonc
{
  "ticker": "IREN", "metric": "EV/ARR",
  "value": 5.7, "prior_value": 4.8,
  "numerator_delta": "+19% (주가 $37.93→$45.12)",
  "denominator_delta": "0% (ARR 목표 $4.0B 불변)",
  "interpretation": "멀티플 확장은 전적으로 분자 기여. 실적 개선 아님",
  "denominator_uncertainty": "완전희석 주수 495M vs 508M 미확정"
}
```

## 규칙

- 모든 밸류에이션 변동 서술에 `numerator_delta` + `denominator_delta` 필수 — 없으면 validate-output이 거부(F6)
- **분모 미확정(주수 충돌 등) 시 단일값 산출 금지 — range로 출력(F9)**
- 종목별 주의사항은 thesis card의 `valuation.caution`을 따른다 (예: CRWV는 순부채 필수 반영, MU는 저 P/E ≠ 밸류, COIN은 거래/구독 매출 멀티플 분리)
- 비교 시 기준 유형(목표치 vs 실적치) 필수 명기(F3)
