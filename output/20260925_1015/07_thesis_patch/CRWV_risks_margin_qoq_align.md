# ThesisPatch — CRWV · risks_margin_qoq_align

- as_of 2026-09-25 · run 20260925_1015 · operation **amend** · requires_human_approval: true
- 카드 필드: `risks[1] ('마진 하락 추세(59%)...' 항목)` · basis_claims: c_20260919_CRWV_5, c_20260919_CRWV_11
- 출처 후보: output/20260925_1015/06_portfolio.json#thesis_patch_candidates[tpc_01]

## reason
[fact] tpc_01과 동일 근거 — 2026-09-20 사용자 확정 기준 = QoQ, 카드 axes[margin_trend] 확정 주석이 risks '마진 하락 추세(59%)' 문구를 정정 후보로 명기. [fact] Q1'26 56%→Q2'26 59%(c_20260919_CRWV_5, grade 1). [fact] 순이자비용 5분기 $267M→$640M(c_20260919_CRWV_5 조정표, 카드 key_metrics 2026-09-20 확정 주석에 기재). [fact] 회사 예시곡선: 다수 배치 동시 램프 시 aggregate contribution margin 단기 25%→5% 압축 후 mid 20%s 안정화 — 예시치이며 실적 아님(c_20260919_CRWV_11, grade 1). [inference:moderate] 확정 기준상 현재 마진은 개선 국면이므로 '하락 추세'라는 현재형 서술은 부정확하나, 램프 구간 마진 재압축과 이자부담 증가가 겹칠 위험은 여전히 유효하다 — 리스크를 삭제하지 않고 조건부로 재서술한다. [fact] 이전 원문은 주석 행으로 보존(P9).

## diff
```diff
-   - "마진 하락 추세(59%)와 이자비용의 동시 진행"
+   # 2026-09-25 ThesisPatch(amend, run 20260925_1015) — 정정 고지(P9), 이전 항목 원문 보존: - "마진 하락 추세(59%)와 이자비용의 동시 진행" / 정정 사유: '하락 추세'는 YoY 전제 서술로, 2026-09-20 사용자 확정 기준(QoQ)상 Q1'26 56%→Q2'26 59% 개선과 부호가 반대다. 리스크 자체(마진 압력과 이자부담의 동시 진행)는 유지하되 현재형 '하락'을 조건부 '재압축' 위험으로 정합. risks 5개 불변(전문 기준 계수, F20).
+   - "마진 재압축과 이자비용 증가의 동시 진행 — Adj. EBITDA 마진은 확정 기준(QoQ)으로 Q1'26 56%→Q2'26 59% +3%p 개선(YoY 참고치 Q2'25 62%→59%)이나, 회사 예시곡선상 다수 배치 동시 램프 시 aggregate contribution margin 단기 압축 가능(예시치, 실적 아님) · 순이자비용 5분기 $267M→$640M 증가"
```

## expected_after (F20)
- contains: ['마진 재압축과 이자비용 증가의 동시 진행 — Adj. EBITDA 마진은 확정 기준(QoQ)', '이전 항목 원문 보존: - "마진 하락 추세(59%)와 이자비용의 동시 진행"']
- not_contains: ['\n  - "마진 하락 추세(59%)와 이자비용의 동시 진행"']
- counts: [{'path': 'risks', 'n': 5}, {'path': 'key_metrics', 'n': 10}]

> [fact] 구절 '마진 하락 추세(59%)'는 axes[margin_trend] 확정 주석과 P9 보존 주석 행에 잔존하므로 not_contains에는 활성 목록 항목 형태(줄바꿈+'  - "')만 사용했다.

## 적용 순서
4건 모두 서로 다른 목록 항목을 건드리며 before 문자열이 겹치지 않는다 — 순서 무관(24개 순열 dry-run 통과).
