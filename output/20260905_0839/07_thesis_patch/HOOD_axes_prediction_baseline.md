# ThesisPatch — HOOD / axes / annotate (prediction_market 기준선 병기)

- **Run**: 20260905_0839 · 2026-09-05T08:55 (소급 확인 특별 태스크)
- **대상 필드**: `axes` (expected_after.counts: axes=5 — F20, 카드 전문 열람 후 before 일치 확인 ✅)
- **operation**: `annotate` / **핵심 논거 역전**: ❌ 아니오

## diff

```diff
--- state/thesis_cards/HOOD.yaml (before)
+++ state/thesis_cards/HOOD.yaml (after 제안)
@@ -1 +1,2 @@
-  - {id: prediction_market, label: "예측시장 — 매출 기여 vs 규제 리스크"}
+  - {id: prediction_market, label: "예측시장 — 매출 기여 vs 규제 리스크. 기준선(Q2'26, 8-K Ex-99.1 grade 1):
+    이벤트 계약 매출 $156M·YoY 10배+, 분기 계약 13.6B건 — 크립토·주식 매출 추월(비중 ~20.1% 파생 계산, inference).
+    ⚠️Q3 계절성 확인 전 지속성 미검증 · KC-HOOD-3 규제 리스크 상존"}
```

## 왜

[fact] 축 최초의 grade 1 매출 실측(8-K Ex-99.1) — 축 성격이 '매출 기여 미지수'에서 '실증된 매출 축(지속성 미검증)'으로 전환. 방향 판정·등급 근거 아님(P2). 이전 라벨 주석 보존(P9).

## 근거 Claim

c_retro_HOOD_001, c_retro_HOOD_002, c_retro_HOOD_003, c_retro_HOOD_004

> 적용은 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
