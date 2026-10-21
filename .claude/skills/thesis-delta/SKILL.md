---
name: thesis-delta
description: Claim 생성 완료 후 사용. 해당 종목 thesis card의 axes에 대해 강화/훼손/중립을 매핑하고 리스크 이관을 표기한다. 카드에 없는 축이면 신규 축 제안으로 전환한다.
---

# thesis-delta — thesis 축 매핑 (P7·P8)

## Delta 스키마 (v1 §4)

```jsonc
{
  "axis": "execution_delivery",      // 반드시 state/thesis_cards/{T}.yaml의 axes.id 중 하나
  "direction": "strengthen",          // strengthen | weaken | neutral | break
  "prior_state": "...", "new_state": "...",
  "risk_transfer_to": ["..."],        // 리스크 이관 명시 — 총량 보존 확인 (소멸 아님)
  "supporting_claims": ["c_..."]
}
```

## 규칙

- **P7 3단 분리:** 계약 존재 / 계약 이행 / 매출 인식을 별도 이벤트로 기록. 앞 단계 통과가 뒤 단계를 함의하지 않는다. `stage` 필드로 표기
- **리스크 이관:** 리스크가 사라진 게 아니라 옮겨간 경우 `risk_transfer_to`에 이관처 명시 (예: IREN H1 인도 완료 → 리스크는 H2-4로 이관)
- **축 매핑 실패:** 카드 axes에 없는 축이 필요하면 Delta를 만들지 말고 **신규 축 제안**으로 전환 → 에스컬레이션(P8). 임의로 기존 축에 우겨넣지 않는다
- **축 분해(P8):** 새 1차 자료가 기존 축 판정을 뒤집으면 하위 축 분해를 제안 (thesis-refine으로 전달)
