# ThesisPatch 인덱스 — NBIS (run 20261001_0900, as_of 2026-10-01)

- 패치 2건 (requires_human_approval: true, F17) — 카드 직접 쓰기 없음

- `NBIS_axes_on_demand_effective_b300` — axes / annotate — axes[on_demand_pricing_power] — 2026-10-01 발효일 관측 주석: B300 단가 grade1 확정(+21.0%), CPU-only 품목별 인상률 1차 확인, 메모리 대조 불가, 과금 전환 미검증 · 의존: 없음
- `NBIS_axes_capacity_delivery_aib_50mw` — axes / annotate — axes[capacity_delivery] — AIB Data Centers 50MW·12년 바인딩 임차 계약 관측 주석(P7 1단) · 의존: 없음

## approval_order

```json
"[fact] 두 패치는 서로 다른 축 행을 치환하고 axes 8 불변 검사만 한다 — 순서 무관(드라이런 정순·역순 모두 PASS)."
```

## dry_run

```json
"[fact] scratchpad 사본에 approvals.py 동일 절차 적용 후 verify_after_apply — 단독·정순·역순 모두 PASS. 병합 미리보기: NBIS_dryrun_merged_preview.yaml. 실카드 미수정."
```

## excluded_candidates

```json
[
 {
  "candidate": "earnings_checkpoints.date(Q3 2026 실적일) 확정",
  "decision": "skipped_logged",
  "reason": "[fact] 회사 IR 공식 공지 미확보, 애그리게이터 추정(11/10 등)은 F1상 근거 불가 — date: null 유지."
 },
 {
  "candidate": "contract_monetization 축 — AIB 계약 MW당 가치 반영",
  "decision": "skipped_logged",
  "reason": "[fact] 계약 금액 미공시로 MW당 계약가치 산출 불가(04_sector neocloud su_2)."
 },
 {
  "candidate": "rates_exposure(매크로 KC-1) 축 반영",
  "decision": "rejected",
  "reason": "[fact] 03_signal에 기재된 매크로 의사 축이며 카드 축이 아니다 — 매크로 재료로 종목 thesis 축을 변경하지 않는다(P6·P13)."
 }
]
```

## kc_context

```json
"[fact] 03_signal/NBIS.json proposed_signal 🔴🔴(규칙1, KC-1 매크로 경로, 3회 연속) — 종목 KC 3건은 전건 not_met. 본 패치는 등급과 무관."
```
