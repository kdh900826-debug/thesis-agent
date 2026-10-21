---
name: thesis-refine
description: L4 실행 시 또는 refine thesis 명령 시 사용. 신규 1차 자료가 thesis 카드의 어느 항목을 부정확하게 만들었는지 판정하고 ThesisPatch를 제안한다. 자동 반영 절대 금지.
---

# thesis-refine — ThesisPatch 생성 (S7, C7)

## ThesisPatch 스키마 (설계서 §7)

```jsonc
{
  "ticker": "IREN",
  "card_field": "핵심 지표",              // 카드 9항목 중 하나 (yaml 키: thesis|key_metrics|catalysts|risks|kill_conditions_ref|noise_filter_ref|earnings_checkpoints|valuation|conclusion) 또는 axes
  "operation": "amend",                  // amend | decompose | add_kc | annotate
  "before": "...", "after": "...",
  "reason": "...",
  "basis_claims": ["c_..."],             // 필수 — 근거 없는 패치 금지
  "requires_human_approval": true,       // 항상 true (F17)
  "axis_decomposition": null             // P8 발동 시 하위 축 목록
}
```

## 규칙

- 기존 서술은 **삭제가 아닌 정정 표기**(P9) — before를 보존하고 after로 대체 제안
- `add_kc` 패치는 정량 임계 + 결과 쌍 필수(P11) — 없으면 패치 자체가 무효
- **thesis 핵심 논거를 뒤집는 패치 → 자동 제안 금지, 에스컬레이션**
- 근거 부족 → 패치 제외 + `unconfirmed` 적재(스킵+로그)
- 산출: `output/{run_id}/07_thesis_patch/{TICKER}.md` (diff 블록) + `state/pending_approvals.json`에 `type: thesis_patch` 건 등재
- 승인 후 적용은 이 스킬이 아니라 `version-publish`의 `approvals.py`가 수행(D10)
