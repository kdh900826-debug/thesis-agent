# ThesisPatch — CRWV / key_metrics / annotate

- **Run**: 20260919_2209 · as_of 2026-09-19 (`thesis-refine` S7/C7, `refine thesis CRWV`)
- **patch_id**: `tp_20260919_2209_CRWV_key_metrics_coverage_basis` · **priority**: medium
- **대상 필드**: `key_metrics[7] — 이자 커버리지 항목` (expected_after.counts: key_metrics=10 — F20)
- **operation**: `annotate` — 기존 서술 삭제 없이 주석 병기만 한다(P9)
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인**: 대상 카드 **전문 75행** 열람 후 before 원문 일치·목록 항목 수(axes 7 · key_metrics 10) 확인 완료 (F20 — 부분 읽기 기반 '부재' 판정 없음)
- **동반 패치(동일 회차)**: `output/20260919_2209/07_thesis_patch/CRWV.md` — axes / margin_trend 측정 기준 병기(high)

## diff

```diff
--- state/thesis_cards/CRWV.yaml (before)
+++ state/thesis_cards/CRWV.yaml (after 제안)
-  - "이자 커버리지 — ⚠️계산기준 미확정. 분자(Adj. EBITDA / GAAP 영업이익 중 택1)·분모(순이자비용 / 총이자비용 중 택1)·기간(분기 연환산 / TTM 중 택1)을 확정해야 KC-CRWV-3 판정이 가능하다. 임계는 1.5x 이하 경고·1.0x 이하 발동(KC-CRWV-3). 카드상 '현 ~2.2x'는 직전 세션 확인분으로 1차 자료 재대조 미완 ⚠️갱신"
+  # 2026-09-19 ThesisPatch(annotate, run 20260919_2209) — 이전 항목 원문 보존(P9): - "이자 커버리지 — ⚠️계산기준 미확정. 분자(Adj. EBITDA / GAAP 영업이익 중 택1)·분모(순이자비용 / 총이자비용 중 택1)·기간(분기 연환산 / TTM 중 택1)을 확정해야 KC-CRWV-3 판정이 가능하다. 임계는 1.5x 이하 경고·1.0x 이하 발동(KC-CRWV-3). 카드상 '현 ~2.2x'는 직전 세션 확인분으로 1차 자료 재대조 미완 ⚠️갱신" / 산식 채택은 사람 결정이므로 에이전트는 두 산식의 1차 실측치만 병기한다. key_metrics 10개 불변(전문 기준 계수, F20).
+  - "이자 커버리지 — ⚠️계산기준 미확정. 분자(Adj. EBITDA / GAAP 영업이익 중 택1)·분모(순이자비용 / 총이자비용 중 택1)·기간(분기 연환산 / TTM 중 택1)을 확정해야 KC-CRWV-3 판정이 가능하다. 임계는 1.5x 이하 경고·1.0x 이하 발동(KC-CRWV-3). 카드상 '현 ~2.2x'는 직전 세션 확인분으로 1차 자료 재대조 미완 ⚠️갱신 [⚠️ 2026-09-19 산식 병기 주석(run 20260919_2209) — (1) 분자·분모 공백 해소: 2026-09-17 8-K Ex 99.2 34p가 분기별 Adj. EBITDA 조정표와 'Interest expense, net' 단일 라인을 1차 공시했다(c_20260919_CRWV_5, grade 1 fact). 따라서 분자 = Adj. EBITDA, 분모 = Interest expense, net이 유일하게 산출 가능한 조합이다 — 회사가 총이자비용·자본화이자·이자수익을 분리공시하지 않아 '총이자비용 기준' 변형은 이번 창 자료로 산출 불가능하다. (2) 기간 두 기준 실측 병기(c_20260919_CRWV_6, inference:strong — 회사 직접 공시 지표가 아닌 산술 결합 파생값): (가) 분기 연환산 기준 = Q2'26 1,510/640 = 약 2.36x(분자·분모를 같이 4배하므로 분기 원비율과 수치 동일). (나) TTM 기준(Q3'25~Q2'26) = 4,403/1,875 = 약 2.35x. 분기 추이는 Q2'25 2.82x → Q3'25 2.69x → Q4'25 2.31x → Q1'26 2.16x → Q2'26 2.36x이며, 카드상 '현 ~2.2x'는 Q1'26(2.16x) 시점에 가장 근접한 값이다(오기가 아니라 시점 차). (3) 이번 회차 KC-CRWV-3 판정에는 기간 채택이 영향을 주지 않았다 — (가)·(나) 어느 기준이든 경고 1.5x·발동 1.0x를 모두 상회해 03_signal/CRWV.json은 not_met/confirmed로 기록했다. 단 conclusion의 진입 검토 조건 '이자 커버리지 3x 이상'까지의 잔여 거리는 기준별로 달라지므로 채택 확정이 필요하다. (4) 참고: 신규 전환사채 $3.7B/2.875%(c_20260919_CRWV_1·c_20260919_CRWV_14)의 연 추가이자 약 $106M을 TTM 분모에 단순 가산하면 약 2.22x이나, 이는 조달금 운용 이자수익·DDTL 5.5 이자·Adj. EBITDA 증가분을 반영하지 않은 정태적 예시 계산이다. (5) TTM 대 분기연환산 중 어느 쪽을 KC-CRWV-3 공식 산식으로 채택할지는 KC 임계·지표정의 확정 영역이므로 에이전트는 채택하지 않고 병기만 한다 — 사람 결정 대기(P11, CLAUDE.md §9, U4). (6) 잔여 공백: 총이자비용·자본화이자·이자수익 분리 수치는 미공시로 Q3 2026 10-Q 대기(unconfirmed 이월). 본 주석은 기존 서술을 삭제하지 않고 병기만 한다(P9)]"
```

## 왜

[fact] state/thesis_cards/CRWV.yaml 전문 75행 확인 결과 key_metrics의 이자 커버리지 항목은 분자·분모·기간 3개 선택지가 모두 미확정 상태로 기재돼 있다. [fact] 2026-09-17 8-K Ex 99.2 34p가 분기별 Adj. EBITDA 조정표와 'Interest expense, net' 단일 라인(267·311·388·536·640 $M)을 1차 공시해 분자·분모 공백은 해소됐다(c_20260919_CRWV_5, grade 1, confirmed). 회사가 총이자비용·자본화이자·이자수익을 분리공시하지 않으므로 '총이자비용 기준' 변형은 이번 창 자료로 산출 불가능하다. [fact] 기간 축만 남았고 두 기준의 실측치가 모두 산출됐다 — 분기 연환산 2.36x(분자·분모 동시 4배로 분기 원비율과 동일), TTM 2.35x(c_20260919_CRWV_6, inference:strong). [fact] 03_signal/CRWV.json의 next_gate에 '이자 커버리지 3x(정의 잠정 확정, TTM/분기연환산 채택은 사람 확인 대기)'가 기록돼 이월됐고 unconfirmed_carried에도 U4로 적재돼 있다. [fact] 이번 회차 KC-CRWV-3은 두 기준 모두 경고 1.5x·발동 1.0x를 상회해 not_met/confirmed로 기록됐으므로, 기간 채택 차이가 이번 회차 KC 판정 결과를 바꾸지 않는다는 점도 함께 기록했다. [fact] 신규 전환사채 $3.7B/2.875%의 연 추가이자 약 $106M 정태 가산 시 TTM 약 2.22x라는 계산도 '정태적 예시'임을 명시해 병기했다(c_20260919_CRWV_1·c_20260919_CRWV_14). [fact] TTM과 분기연환산 중 어느 쪽을 KC-CRWV-3의 공식 산식으로 채택할지는 KC 임계·지표정의 확정 영역으로 사람 결정이다(P11, CLAUDE.md §9) — 따라서 채택 amend가 아니라 병기 annotate로 처리했다. [fact] 기존 항목 서술은 삭제하지 않고 주석 블록만 덧붙였으며 이전 원문은 YAML 주석으로 보존했다(P9). [fact] key_metrics는 전문 기준 10개이며 본 패치로 변하지 않는다(F20).

**역전 판정 주석**: [fact] conclusion의 진입 검토 조건('이자 커버리지 3x 이상')이나 KC-CRWV-3의 임계·판정을 변경하지 않는다. [fact] 산식 채택을 하지 않고 두 기준의 실측치를 병기할 뿐이므로 논거 전복에 해당하지 않는다. 등급·행동 판정은 하지 않는다(P2/P15).

**사람 결정 경계**: [fact] 본 패치는 두 기준(산식)의 1차 실측치를 병기할 뿐 어느 쪽도 채택하지 않는다 — 채택은 측정 정의·KC 임계 확정 영역으로 사람의 권한이다(CLAUDE.md §9, P11, P2/P15). 등급·행동·목표치는 제안하지 않았다.

## 근거 Claim

c_20260919_CRWV_1, c_20260919_CRWV_14, c_20260919_CRWV_5, c_20260919_CRWV_6

출처: `output/20260919_2209/02_company/CRWV.json#claims[c_20260919_CRWV_1,c_20260919_CRWV_5,c_20260919_CRWV_6,c_20260919_CRWV_14] · output/20260919_2209/03_signal/CRWV.json#next_gate · #kill_check.own_company_kc[KC-CRWV-3] · #unconfirmed_carried[U4]`

## 적용 후 자동 대조(expected_after.contains)

- `2026-09-19 산식 병기 주석(run 20260919_2209)`
- `(가) 분기 연환산 기준 = Q2'26 1,510/640 = 약 2.36x`
- `(나) TTM 기준(Q3'25~Q2'26) = 4,403/1,875 = 약 2.35x`
- `사람 결정 대기(P11, CLAUDE.md §9, U4)`

**F20 주석**: [fact] 카드 전문 75행 확인 후 before 원문 일치와 key_metrics 10개 계수를 확정했다(F20). [fact] 목록형 필드(key_metrics)의 항목 문자열을 수정하므로 expected_after.counts를 포함했다(항목 수 불변 10).

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 승인 큐 등재는 오케스트레이터가 수행하며 본 스킬은 `state/thesis_cards/CRWV.yaml`·`state/pending_approvals.json`을 수정하지 않았다.
