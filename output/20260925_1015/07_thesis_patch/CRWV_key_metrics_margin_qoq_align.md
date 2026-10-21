# ThesisPatch — CRWV · key_metrics_margin_qoq_align

- as_of 2026-09-25 · run 20260925_1015 · operation **amend** · requires_human_approval: true
- 카드 필드: `key_metrics[4] ('Adj. EBITDA 마진 ...' 항목)` · basis_claims: c_20260919_CRWV_5
- 출처 후보: output/20260925_1015/06_portfolio.json#thesis_patch_candidates[tpc_01]

## reason
[fact] 2026-09-20 사용자가 margin_trend 축 판정 기준을 시퀀셜(QoQ)로 확정했다(ap_20260920_0804_thesis_patch_crwv_margin_basis_adopted, approved; 카드 axes[margin_trend] '✅ 2026-09-20 기준 확정' 주석). [fact] 같은 주석이 'key_metrics 마진 59%로 하락 추세 문구는 YoY 전제이므로 정정 후보 상정'을 후속 과제로 명기했다. [fact] 5분기 Adj. EBITDA 마진 실측 Q2'25 62%→Q3'25 61%→Q4'25 57%→Q1'26 56%→Q2'26 59%(c_20260919_CRWV_5, grade 1). [inference:strong] 확정 기준(QoQ)으로 읽으면 현 항목의 '하락 추세'는 Q1'26→Q2'26 +3%p 개선과 부호가 반대이므로, 수치는 유지하고 방향 서술만 확정 기준으로 정합한다. [fact] 이전 원문은 주석 행으로 보존(P9). [fact] 이번 창 신규 마진 Claim 0건 — 근거는 직전 회차 Claim과 승인된 사람 결정이다. [fact] '⚠️갱신' 표지 제거 여부는 본 패치 범위 밖(유지).

## diff
```diff
-   - "Adj. EBITDA 마진 59%로 하락 추세 ⚠️갱신"
+   # 2026-09-25 ThesisPatch(amend, run 20260925_1015) — 정정 고지(P9), 이전 항목 원문 보존: - "Adj. EBITDA 마진 59%로 하락 추세 ⚠️갱신" / 정정 사유: '하락 추세'는 YoY(Q2'25 62%→Q2'26 59%) 전제 서술로, 2026-09-20 사용자 확정 축 판정 기준(QoQ)과 방향 부호가 반대다. 59% 수치 자체는 정확 — 수치 오류가 아니라 판정 기준 불일치 정정. key_metrics 10개 불변(전문 기준 계수, F20).
+   - "Adj. EBITDA 마진 Q2'26 59% — 확정 기준(QoQ, 2026-09-20 사용자 결정): Q1'26 56%→Q2'26 59% = +3%p 개선 / YoY 참고치: Q2'25 62%→Q2'26 59% = -3%p ⚠️갱신"
```

## expected_after (F20)
- contains: ["Adj. EBITDA 마진 Q2'26 59% — 확정 기준(QoQ, 2026-09-20 사용자 결정)", '이전 항목 원문 보존: - "Adj. EBITDA 마진 59%로 하락 추세 ⚠️갱신"']
- not_contains: ['\n  - "Adj. EBITDA 마진 59%로 하락 추세 ⚠️갱신"']
- counts: [{'path': 'key_metrics', 'n': 10}, {'path': 'risks', 'n': 5}, {'path': 'axes', 'n': 7}]

> [fact] not_contains는 줄바꿈+2칸 들여쓰기+'- "'로 시작하는 활성 목록 항목 형태만 겨냥한다. 같은 구절이 axes[margin_trend] 확정 주석과 본 패치의 P9 보존 주석 행(': - "' 형태)에 남아 있으므로 구절 단독 문자열은 not_contains에 쓰지 않았다.

## 적용 순서
4건 모두 서로 다른 목록 항목을 건드리며 before 문자열이 겹치지 않는다 — 순서 무관(24개 순열 dry-run 통과).
