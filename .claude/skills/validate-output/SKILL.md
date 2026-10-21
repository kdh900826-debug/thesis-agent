---
name: validate-output
description: 모든 계층 산출물의 발행 직전에 자동 실행. P1~P17 게이트를 규칙 기반으로 검증하고 위반 시 거부한다. 실패 시 재생성 최대 2회 후 에스컬레이션.
---

# validate-output — 발행 전 게이트 (VALIDATE_V2)

## 실행

```bash
python .claude/skills/validate-output/scripts/validate_output.py <산출물.json> --layer <layer>
# layer: macro | company | signal | sector | correlation | portfolio | thesis_patch | publish
```

## 검사 항목 (설계서 §2-3)

| layer | 검사 |
|---|---|
| 공통 | 모든 산출 필드 `as_of` 존재. `reused_from` 존재 시 `staleness_days` 표기(P16) |
| company | 전 Claim에 `claim_type`·`scope`·`evidence_grade`·`source.url` (P1·P4) |
| signal | 입력 Claim 중 `scope != company_specific` == 0 (P6·P13, F13). 상향 시 게이트 3종(quantitative·company_specific·revenue_recognized) |
| macro | 전망·시나리오 서술 검출 시 거부 (D3, F14) |
| sector | 개별 ticker 등급 변경 필드 부재 — `signal_mutation` null (P13) |
| correlation | 수치형 상관계수 표기 0건, `coefficient_used: false` (P14, F15) |
| portfolio | 매수/매도 동사·목표 비중 단일값·시점 지시 0건 (P15, F18) |
| thesis_patch | `basis_claims` 존재, `requires_human_approval: true`, add_kc 시 임계 쌍 (P11, F17) |
| publish | 승인 큐의 해당 건 `status == approved` (D6, F19). 파일명 충돌 없음 (P9) |

## 실패 처리

REJECT + 위반 목록 출력 → 재생성 최대 2회 → 에스컬레이션. **LLM 자기 검증(서사 문장·해석 타당성)은 각 에이전트가 발행 전 자체 수행하고, 이 스크립트는 결정론 규칙만 담당한다(D12).**
