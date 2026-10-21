# ThesisPatch — CRWV / earnings_checkpoints — earnings_checkpoints.items[2] 'Adj. EBITDA 마진 59%에서 추가 하락 여부' — YoY 전제 잔여 문구를 확정 기준(QoQ)으로 정합 / amend

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `CRWV_earnings_checkpoints_margin_qoq_align` · priority: medium
- **대상 필드**: `earnings_checkpoints` — earnings_checkpoints.items[2] 'Adj. EBITDA 마진 59%에서 추가 하락 여부' — YoY 전제 잔여 문구를 확정 기준(QoQ)으로 정합
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — CRWV 3건은 서로 다른 행(catalysts 53행 / axes 29행 / earnings_checkpoints 72행)을 치환하고 counts는 각자 필드만 검사한다. 권장: catalysts → axes → earnings_checkpoints
- **사전 확인(F20)**: `state/thesis_cards/CRWV.yaml` 전문 86행 열람, before 출현 1회 확인. 현재 계수 axes 7 / key_metrics 10 / catalysts 4 / risks 5 / kill_conditions_ref 4 / version_history 12 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "earnings_checkpoints.items", "n": 8}] · contains 2건 · not_contains 1건

## diff

```diff
--- state/thesis_cards/CRWV.yaml (before)
+++ state/thesis_cards/CRWV.yaml (after 제안)
-    - "Adj. EBITDA 마진 59%에서 추가 하락 여부"
+    # 2026-10-01 ThesisPatch(amend, run 20261001_0900) — 정정 고지(P9), 이전 항목 원문 보존: - "Adj. EBITDA 마진 59%에서 추가 하락 여부" / 정정 사유: '추가 하락'은 마진이 하락 중이라는 YoY 전제 서술로, 2026-09-20 사용자 확정 축 판정 기준(QoQ: Q1'26 56%→Q2'26 59% +3%p 개선)과 방향 전제가 반대다. 2026-09-25 key_metrics·risks 정정(동일 사유)에서 누락된 잔여 문구. 관측 대상(Q3 마진) 자체는 유지. items 8개 불변(전문 기준 계수, F20).
+    - "Adj. EBITDA 마진 — Q3'26 실측의 QoQ 방향(확정 기준: Q2'26 59% 대비 개선/압축) · YoY 참고치(Q3'25 61%) 병기"
```

## 왜

[fact] state/thesis_cards/CRWV.yaml 전문 86행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 7 / key_metrics 10 / catalysts 4 / risks 5 / kill_conditions_ref 4 / earnings_checkpoints.items 8 / version_history 12(F20). [fact] 오케스트레이터 직전 메모가 지목한 key_metrics '마진 59%로 하락 추세'·risks '마진 하락 추세(59%)'는 전문 확인 결과 이미 2026-09-25 승인 패치(ap_20260925_1055_thesis_patch_crwv_key_metrics_margin_qoq_align·crwv_risks_margin_qoq_align)로 QoQ 기준 정정이 적용돼 있다(카드 41~42행·58~59행) — 해당 2건은 재패치 대상이 아니다(메모가 stale). [fact] 같은 YoY 전제를 가진 잔여 문구가 earnings_checkpoints.items 3번째 '…59%에서 추가 하락 여부'(72행)에 남아 있다 — '추가 하락'은 하락이 진행 중이라는 전제이며 확정 기준(QoQ, 2026-09-20 사용자 결정, 카드 27행 기록)상 직전 관측은 +3%p 개선이다. 관측 항목은 유지하고 전제 문구만 중립화한다(P9 원문 주석 보존). [fact] YoY 참고치 Q3'25 61%는 카드 27행에 기록된 5분기 실측(c_20260919_CRWV_5)에서 가져왔다. [fact] 이번 run 04_sector/neocloud.json margin_trend도 '확정 기준(QoQ) Q1'26 56%→Q2'26 59% 유지'로 기록했다(supporting_claims 없음 — 신규 자료 0건).

**역전 판정 주석**: [fact] 관측 항목 문구 정합이며 thesis·conclusion·리스크 존재를 바꾸지 않는다.

## 근거 Claim

c_20260919_CRWV_5

[fact] c_20260919_CRWV_5: 2026-09-17 8-K Ex 99.2 5분기 Adj. EBITDA 조정표(grade1·confirmed). 이번 run 03_signal/04_sector에는 인용되지 않은 직전 run Claim이며 output/20260919_2209/03_signal/CRWV.json·04_sector/neocloud.json 인용을 확인했다. 이번 run에는 마진 신규 1차 자료가 없다 — 본 패치는 신규 사실이 아니라 사용자 확정 기준과의 문구 정합이다. 신규 run Claim 부재가 승인 판단에 영향을 줄 경우 reject 가능(사람 판단).

출처: `output/20261001_0900/03_signal/CRWV.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/neocloud.json#axis_view · output/20261001_0900/03_input/arbiter_CRWV.json(수치·문구 대조) · output/20260919_2209/03_signal/CRWV.json(c_20260919_CRWV_5 인용 확인)`

**F20 주석**: [fact] before는 72행 전체 원문이며 출현 1회 확인. 원문은 주석 행 안에 '- "…"' 형태로 보존되므로 not_contains는 앞 공백 4칸+'- "' 패턴(실제 목록 항목)으로 한정해 주석 문자열과 충돌하지 않게 했다. counts 8로 항목 수 불변(주석 행은 계수에 포함되지 않음)을 검증한다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
