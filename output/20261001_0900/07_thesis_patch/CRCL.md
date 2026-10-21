# ThesisPatch 인덱스 — CRCL (run 20261001_0900, as_of 2026-10-01)

- 패치 1건 (requires_human_approval: true, F17) — 카드 직접 쓰기 없음

- `CRCL_axes_ousd_launch_sign_activation` — axes / annotate — axes[competition_ousd_consortium] — OUSD 공식 출시·실측 유통량 최초 공시로 부호 활성화 조건 관측상 최초 충족(grade 4 확인 대상) 주석 · 의존: 없음

## approval_order

```json
"[fact] 1건 — 순서 의존 없음."
```

## dry_run

```json
"[fact] scratchpad 사본 적용 후 verify_after_apply PASS. 실카드 미수정."
```

## escalations

```json
[
 {
  "id": "esc_20261001_0900_crcl_governance_axis",
  "type": "axis_addition_requires_human_decision",
  "summary": "[fact] 2026-09-25 8-K(Item 5.02, c_20261001_CRCL_1, grade1·confirmed): 공동창업자 이사 P. Sean Neville 즉시 사임(이사회 8→7인), CFO Jeremy Fox-Geen 사임 통지(후임 선임 시까지 최대 2026-12-31 재직, 서치펌 탐색), 양건 모두 '운영·정책 이견 무관' 명시.",
  "why_not_auto_patched": "[fact] 04_sector stablecoin su_1001_14가 신규 축 management_governance_succession을 제안했으나 이는 축 추가(axes 8→9)다 — (1) 축 명명 표준화(esc_L4_2209_03) 선행 결정 의존, (2) 03_signal이 이 재료를 '카드 비정의 축 — 노이즈 경계'로 기록했고 경영진 교체는 P3 변화 범주(매출·가이던스·마진·현금흐름·고객명·수주·양산일정)에 직접 속하지 않아 노이즈/축 판정 자체가 사람 영역이다. 따라서 패치를 자동 제안하지 않고 에스컬레이션한다.",
  "draft_for_human": "[inference] 채택 시 초안 — 축 추가: {id: management_governance_succession, label: \"경영진 승계·거버넌스 — 2026-09-25 8-K: CFO Fox-Geen 사임 통지(후임 선임 시까지 최대 2026-12-31 재직), 이사 Neville 사임(이사회 8→7인), 이견 무관 명시(c_20261001_CRCL_1). 관측점: CFO 후임 선임 공시, Q3'26 10-Q 서명·실적콜 경영진 코멘트 연속성\"} — depends_on_human_decision: axis_naming_standardization. 대안: 축 추가 없이 risks에 '경영진 승계' 항목 추가(축 수 불변).",
  "depends_on_human_decision": "axis_naming_standardization",
  "basis_claims": [
   "c_20261001_CRCL_1",
   "c_20261001_CRCL_2"
  ]
 }
]
```

## excluded_candidates

```json
[
 {
  "candidate": "risks[0] OUSD 참여 기관 수(140+ → 200+) 갱신",
  "decision": "skipped_logged",
  "reason": "[fact] 200+ 수치는 c_3(grade4·confirmed=false) 단독 — axes 주석에 확인 대상으로만 기재하고 risks 원문 수치는 정정하지 않았다(P4)."
 },
 {
  "candidate": "key_metrics 'OUSD 실측 점유율 영향' 수치 기입",
  "decision": "skipped_logged",
  "reason": "[fact] 점유율 판정 분모(회사 정의 계열) 신규치가 없어 산출 불가 — axes 주석의 '약 0.6%'는 grade4 2차 집계 기반 inference로만 기재."
 },
 {
  "candidate": "Arc TVL $494M·밈코인 82% 반영(diversification)",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_CRCL_4 grade4·confirmed=false, 출처 신뢰도 미검증 — 근거 부족."
 },
 {
  "candidate": "earnings_checkpoints.date(Q3)",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_CRCL_9: 공식 IR 공지 없음, 애그리게이터 11/12 추정은 F1상 불가 — null 유지가 정답."
 }
]
```

## kc_context

```json
"[fact] 03_signal/CRCL.json proposed_signal 🔴 — 본 패치는 등급과 무관."
```
