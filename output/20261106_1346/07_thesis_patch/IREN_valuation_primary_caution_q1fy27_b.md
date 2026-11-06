# ThesisPatch — IREN / valuation.primary·caution — 11/5 기준 EV/ARR 재산출, FY26 '인식 0' 문구 갱신 (편집 2/2: valuation)

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_valuation_primary_caution_q1fy27_b` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- valuation (before)
-    Microsoft·Horizon 계약은 ASC842 리스로 분류돼 FY26 손익계산서에 매출 인식액이 0이다 — 현 매출 배수에 thesis 핵심 계약이 반영돼 있지 않다.
+++ valuation (after 제안)
+    Microsoft·Horizon 계약은 ASC842 리스로 분류돼 FY26 손익계산서 인식액이 0이었고, FY27 Q1부터 AI Cloud Lease 매출 $65M이 인식되기 시작했다(Horizon 1 인수 이후, 단독 금액 미분리) — Horizon 2-4는 아직 미반영이므로 현 매출 배수에 thesis 핵심 계약은 일부만 반영돼 있다. [2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: 현 매출 배수에 thesis 핵심 계약이 반영돼 있지 않다]
```

## 왜

[fact] valuation-decompose 규칙(P10·F9)에 따라 L2가 재산출했다: 분모 A 3.02x~3.89x, 분모 B 12.08x~15.58x, 분모 기여 0·전액 분자 기여(02_company/IREN.json#valuation_snapshot). [fact] 가격은 11/5 정규장 종가 $18.03(grade 4, 실적 발표 전)이다 — 실적 반응은 미반영이다. [fact] caution의 'FY26 인식액 0' 서술은 FY27 Q1 리스 매출 $65M 인식으로 시점이 지났다(IREN-2611-C03·C04).

## 근거 Claim

IREN-2611-C03, IREN-2611-C04

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).