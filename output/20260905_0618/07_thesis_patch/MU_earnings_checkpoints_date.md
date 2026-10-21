# ThesisPatch — MU / earnings_checkpoints / amend

- **Run**: 20260905_0618 · 2026-09-05T06:18 (L4 병행 `thesis-refine`)
- **대상 필드**: `earnings_checkpoints` (expected_after.counts: earnings_checkpoints.items=7 — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: 대상 카드 전문 열람 후 before 문자열의 카드 원문 일치 확인 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음)

## diff

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
@@ -1 +1,2 @@
-  date: "2026-09-22"
+  # 2026-09-05 ThesisPatch(amend, run 20260905_0618) — 이전: date: "2026-09-22"(가정일). 회사 공식 확정일 2026-09-30으로 정정(c_20260905_MU_02, grade 1). items 7개는 전건 미확인 상태로 불변 이월.
+  date: "2026-09-30"
```

## 왜

[fact] 회사 공식 보도자료(2026-08-26, grade 1)가 FY26 Q4 실적일을 2026-09-30으로 확정했다(c_20260905_MU_02). [fact] earnings_checkpoints.date는 체크포인트 대조 실행 시점을 지정하는 필드이므로 가정일을 유지하면 대조 자체가 잘못된 날짜에 트리거된다. [fact] items는 전문 기준 7개(SCA 가이던스 / $50B CapEx 계획 / CXMT·YMTC 대응 / LTA 비중 및 방향 / 선수금·계약부채 잔액 / 비트그로스 vs ASP 분해 / HBM 마진 vs 범용 마진 직접 확인)이며 이번 구간에 확인된 항목이 없어(c_20260905_MU_12·13) 전건 불변 이월한다 — 개수 변경 없음(F20). [fact] 이전 값은 주석으로 보존(P9).

**역전 판정 주석**: [fact] 체크포인트 실행 일자의 사실 정정이며 항목 내용·판정은 변경하지 않는다.

**후속 주의**: [fact] 정정 승인 시 run earnings MU의 트리거 일자가 2026-09-30이 된다. [fact] 9/30 실적은 미검증 가설 'HBM이 장기계약 대가로 마진이 더 낮다'(key_metrics ⚠️ 항목)의 유일한 직접 확인 지점이다.

## 근거 Claim

c_20260905_MU_02, c_20260905_MU_12, c_20260905_MU_13

출처: `output/20260905_0618/02_company/MU.json#earnings_checkpoint_status · #claims[c_20260905_MU_02]`

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
