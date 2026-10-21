# ThesisPatch — HOOD / key_metrics / amend (예측시장 기준선 등재)

- **Run**: 20260905_0839 · 2026-09-05T08:55 (소급 확인 특별 태스크)
- **대상 필드**: `key_metrics` (expected_after.counts: key_metrics=7 — F20, 카드 전문 열람 후 before 일치 확인 ✅)
- **operation**: `amend` / **핵심 논거 역전**: ❌ 아니오

## diff

```diff
--- state/thesis_cards/HOOD.yaml (before)
+++ state/thesis_cards/HOOD.yaml (after 제안)
@@ -1 +1,2 @@
-  - "예측시장 매출·거래량"
+  - "예측시장(이벤트 계약) 매출·거래량 — Q2'26 $156M·YoY 10배+(8-K Ex-99.1 grade 1), 분기 계약 13.6B건.
+    거래매출 $776M 구성: 옵션 $342M > 이벤트 $156M > 주식 $129M > 크립토 $100M(-38%) — 비중 ~20.1%는
+    파생 계산(inference). 다음 관측점 Q3: 월드컵 계절성 여부·QoQ 방향"
```

## 왜

[fact] 정량 기준선 부재 항목에 Q2'26 확정치 등재 — 이후 실적 대조(earnings_checkpoints '예측시장 기여도')의 비교 기준 확보. 항목 수 7개 불변, 이전 값 주석 보존(P9).

## 근거 Claim

c_retro_HOOD_001, c_retro_HOOD_002, c_retro_HOOD_004

> 적용은 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
