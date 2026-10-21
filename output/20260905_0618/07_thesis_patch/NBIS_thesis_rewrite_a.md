# ThesisPatch — NBIS / thesis / amend (재작성, 에스컬레이션 선택지 A)

- **Run**: 20260905_0618 · 2026-09-05T08:30 (에스컬레이션 esc_20260905_0618_nbis_thesis_rewrite에 대한 사용자 결정 집행)
- **대상 필드**: `thesis` (블록 스칼라 — counts 해당 없음, F20 전문 열람 후 before 일치 확인 ✅)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true) / **핵심 논거 역전**: ✅ 예 — 단, 에이전트 판단이 아닌 사용자의 선택지 A 결정 집행

## diff

```diff
--- state/thesis_cards/NBIS.yaml (before)
+++ state/thesis_cards/NBIS.yaml (after 제안)
@@ -1,2 +1,9 @@
-  순현금 재무구조 + 최고 성장률 + 고객 선불금 기반 저희석 확장. Full-stack + 소프트웨어
-  (Token Factory, Echo) 보유로 MW당 수익화에서 bare-metal 대비 우위. NVIDIA·Meta 엔도스먼트.
+  대규모 자본시장 접근성 + 최고 성장률 + 고객 선불금 기반 확장 — 단 재무구조는 이자부 부채 > 현금으로
+  전환(6/30/26 확정)됐고, 확장의 조달 형태는 부채성·조건부 잠재 희석이 병존한다. Full-stack + 소프트웨어
+  (Token Factory, Echo) 보유로 MW당 수익화에서 bare-metal 대비 우위. NVIDIA·Meta 엔도스먼트.
+  [✍ 2026-09-05 재작성 — 사용자 결정: 선택지 A. 이전 문장(P9 보존): "순현금 재무구조 + 최고 성장률 +
+  고객 선불금 기반 저희석 확장." 근거: "순현금" 불성립(Debt $8,545.7M > 현금 $8,042.1M) ·
+  "저희석" 미성립(ATM 12.7M주 + $800M 교환 ~15.8M주 + 전환사채 원금 ~$15.0B 조건부 희석, 즉시 희석 아님 P7) ·
+  조달 접근성은 8/24 $5.75B 클로징으로 실증. '사람 결정 대기'는 본 재작성으로 해소]
```

## 왜

[fact] 2026-09-05 사용자가 에스컬레이션 선택지 A(재작성)를 채택했다. [fact] "순현금"·"저희석" 두 서술 모두 grade 1 확정 사실과 어긋나며(6/30 부채>현금, 대규모 조달 실행 완료), 반대 방향 사실(funding_access 강화)도 문장·주석에 함께 보존한다. [fact] 이전 문장은 원문 인용으로 보존(P9).

## 근거 Claim

c_20260905_NBIS_01, c_20260905_NBIS_02, c_20260905_NBIS_03, c_20260820_NBIS_01, c_20260820_NBIS_02

출처: `output/20260905_0618/07_thesis_patch/NBIS_escalation_thesis_rewrite.md`

> 적용은 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
