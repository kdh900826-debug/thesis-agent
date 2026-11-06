# ThesisPatch — IREN / key_metrics[3]·risks[2] — MW당 매출 계약 단가 기준선에 11/5 체결분 추가(F3 기준 분리 유지) (편집 2/2: risks)

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_keymetrics3_risks2_rev_per_mw_b` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- risks (before)
-  - "MW당 매출 — [실적 기준] 가동 MW 미공시로 산출 불가. [계약 단가 기준] $20M+/MW(IT)로 공표. 두 기준 혼용 금지"
+++ risks (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: MW당 매출 — [실적 기준] 가동 MW 미공시로 산출 불가. [계약 단가 기준] $20M+/MW(IT)로 공표. 두 기준 혼용 금지
+  - "MW당 매출 — [실적 기준] 운영 용량 약 93MW 공시(10-Q)됐으나 MW 기준 미특정·가동 ARR 기준일 불명으로 산출 보류. [계약 단가 기준] 8/27 $20M+/MW(IT), 11/5 체결분 5년 ~$22M·단기 ~$40M/MW(IT). 두 기준 혼용 금지(F3)"
```

## 왜

[fact] 보도자료 각주 6·7에 분기 말 이후 체결 계약의 MW(IT)당 단가와 3·5년 신규 계약 평균 단가 상승률이 회사 추정치로 기재됐다(IREN-2611-C13). 모두 계약 단가·목표 기준이며 실현 MW당 매출이 아니다(F3). [inference] 운영 용량 약 93MW는 MW 기준이 특정되지 않아 실적 기준 산출에 쓰지 않는다(IREN-2611-I05·I06).

## 근거 Claim

IREN-2611-C08, IREN-2611-C13

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).