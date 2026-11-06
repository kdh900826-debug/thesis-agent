# ThesisPatch — IREN / catalysts[0] — FY27 Q1 10-Q 촉매 소진, 리스 매출 $65M 최초 인식 반영

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_catalysts0_q1fy27_lease_recognized` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- catalysts (before)
-  - "FY27 Q1 10-Q (2026년 11월 경) — ASC842 리스 매출 최초 인식 금액. 사전 정의 상향 게이트 ⑪(Horizon 1 인식 금액)의 유일한 관측점"
+++ catalysts (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: FY27 Q1 10-Q (2026년 11월 경) — ASC842 리스 매출 최초 인식 금액. 사전 정의 상향 게이트 ⑪(Horizon 1 인식 금액)의 유일한 관측점
+  - "[소진 2026-11-05] FY27 Q1 10-Q: AI Cloud Lease 매출(ASC842) $65M 최초 인식 = 고정 리스료 $49M + 가용성 조건부 $16M. Microsoft Agreement 포함으로만 서술돼 Horizon 1 단독분은 미분리 — 상향 게이트 ⑪은 금액 분리 미충족. 후속 관측점 = FY27 Q2 10-Q(2027-02 경): Horizon 1 단독 또는 계약별 리스 매출 분리 여부, Horizon 2-4 인수 후 리스 개시 금액"
```

## 왜

[fact] 카드 catalysts[0]이 관측점으로 지정한 FY27 Q1 10-Q가 2026-11-05 제출됐다. [fact] AI Cloud Lease 매출 $65M(고정 $49M + 조건부 $16M)이 처음 인식됐고(IREN-2611-C03), 10-Q는 Microsoft Agreement를 포함(including)한다고만 서술해 Horizon 1 단독 금액이 분리되지 않았다(IREN-2611-C04). [inference:medium] 최소 리스료 스케줄로 환산하면 $49M은 H1 약 1.6개월분과 규모가 맞으나 확정은 아니다(IREN-2611-I02).

## 근거 Claim

IREN-2611-C03, IREN-2611-C04, IREN-2611-I02

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).