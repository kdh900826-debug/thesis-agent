---
name: fact-split
description: noise-triage 승격 항목에서 Claim을 생성할 때 사용. 확정 사실과 추론을 분리 태깅하고 추론 강도를 부여한다. 태그 없는 문장은 출력 불가.
---

# fact-split — 사실/추론 분리 (P1)

## Claim 스키마 (v1 §4)

```jsonc
{
  "id": "c_{YYYYMMDD}_{ticker}_{seq}",
  "ticker": "IREN",
  "claim_type": "fact",              // fact | inference — 필수
  "text": "...",
  "evidence_grade": 1,
  "source": {"type": "6-K", "url": "...", "filed_at": "..."},
  "inference_strength": null,        // inference일 때만: strong | medium | weak
  "quantitative": false,             // 매출/마진/현금흐름/가이던스 수치 포함 여부
  "scope": "company_specific",       // company_specific | sector | macro — P6/P13 필터 기준
  "confirmed": true
}
```

## 규칙

- 원문에 명시된 수치·사건 = `fact`. 함의·전망·해석 = `inference` + 강도(strong/medium/weak)
- `fact`는 `source.url` + `evidence_grade ∈ {1,2}` 필수. 3·4등급 단독이면 `confirmed: false`
- **scope 태깅에 특히 주의**: "네오클라우드 전반", "금리 인하 기대" 류는 company_specific이 아니다 — sector/macro로 태깅해야 arbiter 필터가 작동한다(F11·F13)
- 원문 불충분 시 인용 보류, `unconfirmed` 적재(P5). "확인되지 않음 → 없음" 서술 금지(F10)
