# ThesisPatch — IREN / key_metrics[3]·risks[2] — MW당 매출 계약 단가 기준선에 11/5 체결분 추가(F3 기준 분리 유지) (편집 1/2: key_metrics)

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_keymetrics3_risks2_rev_per_mw_a` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- key_metrics (before)
-  - "MW당 매출 — [계약 단가 기준] 최근 3년 계약 MW(IT)당 $20M 초과, 협의 중 ~$25M (8/27 공시). [실적 기준] 가동 MW 미공시로 산출 불가. 두 기준은 비교 불가하며 섹터 실적치 $10.5-12M과 직접 대조 금지(F3)"
+++ key_metrics (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: MW당 매출 — [계약 단가 기준] 최근 3년 계약 MW(IT)당 $20M 초과, 협의 중 ~$25M (8/27 공시). [실적 기준] 가동 MW 미공시로 산출 불가. 두 기준은 비교 불가하며 섹터 실적치 $10.5-12M과 직접 대조 금지(F3)
+  - "MW당 매출 — [계약 단가 기준, 회사 추정] 8/27: 최근 3년 계약 MW(IT)당 $20M 초과, 협의 중 ~$25M. 11/5(분기 말 이후 체결분): 5년 계약 ~$22M/MW(IT)·고객이 GPU capex 90% 선납, 단기 계약 ~$40M/MW(IT), Prince George H100 다년 재계약 종전 단가의 2배. 3·5년 신규 계약 평균 단가 +11%/+12%(ARR 가중, 내부 전력소비 가정 — 각주 6). 선납·기간 구조가 달라 8/27 수치와 같은 조건 비교 불가. [실적 기준] 운영 용량 약 93MW 공시됐으나 MW 기준(IT/gross) 미특정·가동 ARR 기준일 불명으로 산출 보류. 두 기준은 비교 불가하며 섹터 실적치 $10.5-12M과 직접 대조 금지(F3)"
```

## 왜

[fact] 보도자료 각주 6·7에 분기 말 이후 체결 계약의 MW(IT)당 단가와 3·5년 신규 계약 평균 단가 상승률이 회사 추정치로 기재됐다(IREN-2611-C13). 모두 계약 단가·목표 기준이며 실현 MW당 매출이 아니다(F3). [inference] 운영 용량 약 93MW는 MW 기준이 특정되지 않아 실적 기준 산출에 쓰지 않는다(IREN-2611-I05·I06).

## 근거 Claim

IREN-2611-C08, IREN-2611-C13, IREN-2611-I05, IREN-2611-I06

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).