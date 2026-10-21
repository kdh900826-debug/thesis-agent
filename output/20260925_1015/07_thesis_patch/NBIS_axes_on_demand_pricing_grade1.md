# ThesisPatch — NBIS / axes / annotate (on_demand_pricing_power 근거등급 grade 3 → grade 1)

- **Run**: 20260925_1015 · 2026-09-25 (`refine thesis NBIS`, L4 후보 tpc_05)
- **대상 슬롯**: `axes[id=on_demand_pricing_power].label` 말미에 주석 추가 — 축 id·축 수 **변경 없음 (8 → 8)**
- **operation**: `annotate` · **승인 필요**: 예 (requires_human_approval: true, F17) · **핵심 논거 역전**: 아니오
- **사전 확인 (F20)**: 카드 **전문** 열람(105행) + yaml.safe_load 계수: axes = 8, key_metrics = 7. before 문자열 카드 내 출현 횟수 = 1
- **선행 결정 의존**: 부분 의존. L4 원문은 '무변화 축 delta 발행 규약' 결정이고, 오케스트레이터 지시는 axis-naming 결정으로 표기함. 본 패치는 축 id를 바꾸지 않으므로 어느 결정과도 충돌하지 않는다(inference:medium)

## diff

```diff
--- state/thesis_cards/NBIS.yaml (before, 26행 말미)
+++ state/thesis_cards/NBIS.yaml (after 제안)
-부호 활성화 조건 = 2026-10-01 이후 nebius.com/prices 신단가 1차 확인 또는 Q3 2026 실적자료의 단가·ARPU 언급"}
+부호 활성화 조건 = 2026-10-01 이후 nebius.com/prices 신단가 1차 확인 또는 Q3 2026 실적자료의 단가·ARPU 언급 [2026-09-25 근거등급 격상 주석(annotate, run 20260925_1015) — 위 서술은 P9에 따라 삭제하지 않고 보존한다. (1)[fact] 2026-09-25 조회 nebius.com/prices(grade 1, confirmed)에 2026-10-01 발효 인상 후 단가가 회사에 의해 직접 게시됨: HGX H100 $3.85→$4.50(+16.9%) / H200 $4.50→$5.40(+20.0%) / B200 $7.15→$8.50(+18.9%). 2026-09-19 조회 시점에는 동일 페이지에 인상 고지 문구가 없었다(c_20260919_NBIS_1). 이로써 위 '2차 인상 고지'의 근거는 이 3개 모델에 한해 grade 3→grade 1, confirmed=false→true로 격상된다(c_20260925_NBIS_1, c_20260925_NBIS_2). (2)[fact] HGX B300·GB300/GB200 NVL72는 현재·인상 후 단가 모두 'Contact sales'로 비공개 — 보도된 B300 수치와 CPU-only 25%·메모리 약 41% 인상률은 여전히 1차 교차검증 없음(grade 3 유지). (3)[fact] P7 — 본 건은 '가격 고지 확정' 단계(3단 중 1단)다. 발효일 2026-10-01은 as_of(2026-09-25) 기준 미도래이며 가격 고지 ≠ 계약 갱신·체결 ≠ 매출 인식. (4)[fact] P2 — 리스트 가격 게시는 확정 매출·마진·가이던스 수치가 아니므로 시그널 상향 근거로 부적격이다(03_signal 상향 게이트 not_met — revenue_recognized 미충족, holding_reinforcement로만 분류). (5)[inference:high — 근거등급 판단에 한정, 매출·마진 영향 크기 아님] 위 부호 활성화 조건 중 '신단가 1차 게시' 요소만 충족됐고 '2026-10-01 이후 발효 확인'과 'Q3 2026 실적자료의 단가·ARPU 언급'은 미충족이다. 축 id·정의는 변경하지 않는다. commitment discount의 $1B+ 계약 전가 여부는 미확인으로 contract_monetization 축과 부호 분리를 유지한다. 다음 관측점 = 2026-10-01 이후 nebius.com/prices 재조회(발효 확인), B300/GB300 단가 공개 여부, Q3 2026 실적자료의 단가·ARPU·commitment discount 언급]"}
```

## 왜

[fact] 카드 전문(state/thesis_cards/NBIS.yaml, 105행)을 열람하고 yaml.safe_load로 계수한 결과 axes는 8개다 — growth_arr, margin_transition, funding_access, leverage_burden, capacity_delivery, contract_monetization, on_demand_pricing_power, customer_concentration(F20 전문 기준 계수). [fact] 현재 on_demand_pricing_power 라벨은 2026-10-01 발효 2차 인상을 'grade 3·confirmed=false, 1차 공시 경로 부재'로 기록하고 있고, 카드 어디에도 인상 후 단가나 run 20260925_1015 기록이 없다 — 카드가 아직 grade 1을 반영하지 않았으므로 후보를 드롭하지 않는다. [fact] c_20260925_NBIS_1(grade 1, confirmed): 2026-09-25 nebius.com/prices에 H100 $3.85→$4.50(+16.9%), H200 $4.50→$5.40(+20.0%), B200 $7.15→$8.50(+18.9%)와 발효일 2026-10-01이 직접 게시됐고, B300/GB300 계열은 'Contact sales'로 비공개다. [fact] 게시된 '현재' 단가 3개는 카드 라벨의 2026-09-19 기준선(H100 $3.85 / H200 $4.50 / B200 $7.15)과 일치한다. [inference:high] c_20260925_NBIS_2 — 축 근거가 3개 모델에 한해 grade 3→1로 격상된다. 이 강도는 등급 판단 자체에 한정되며 매출·마진 영향 크기에 대한 것이 아니다. [fact] P7 — 발효일이 as_of 기준 미도래이고 본 건은 가격 고지 단계이므로 stage 표기를 '가격 고지 확정'으로 유지하며 매출 인식 주장을 넣지 않는다. [fact] P2 — 03_signal/NBIS.json 상향 게이트는 revenue_recognized 미충족으로 not_met(vacuous)이며 본 Delta는 holding_reinforcement로만 분류된다. 이 캐비엇을 주석에 명기했다. [fact] P9 — 기존 라벨 문언(grade 3 서술 포함)은 삭제하지 않고 그대로 두며, 라벨 끝에 날짜가 붙은 주석 블록을 덧붙이는 방식이다. 축 id·축 수(8)는 변경하지 않는다.

## 증거 한계 (주석 문안에 반영됨)

- **P4**: 격상은 **H100/H200/B200 3개 모델**에 한정된다. B300·GB300/GB200 NVL72는 'Contact sales'로 비공개이고, CPU-only 25%·메모리 약 41% 수치는 여전히 grade 3이다.
- **P7**: 단계는 **가격 고지 확정**이다. 발효일 2026-10-01은 as_of 기준 미도래이며 가격 고지 ≠ 계약 ≠ 매출 인식이다.
- **P2**: 리스트 가격은 확정 매출·마진 수치가 아니므로 상향 근거로 쓸 수 없다. 03_signal 상향 게이트는 not_met이며 holding_reinforcement로만 분류된다.
- **P9**: 기존 라벨 문언(grade 3 서술 포함)을 그대로 보존한다. `expected_after.contains`가 보존 여부를 검증한다.

## 후속 주의

[fact] L4 tpc_05의 card_field는 'axes.on_demand_pricing_power / key_metrics'였으나 key_metrics 부분은 생성하지 않았다 — on-demand 단가 항목을 새로 추가하면 목록 항목 수가 7→8로 바뀌는데, 발효(2026-10-01) 1차 확인 전이고 P2상 확정 매출 지표도 아니기 때문이다. 발효 확인 후 재검토한다. [fact] KC 신설·임계 변경 없음(P11, CLAUDE.md §9).

## 근거 Claim

c_20260925_NBIS_1, c_20260925_NBIS_2

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 대조 → 실패 시 원복).
