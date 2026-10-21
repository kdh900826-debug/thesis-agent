# ThesisPatch 인덱스 — CRWV (run 20261001_0900, as_of 2026-10-01)

- 패치 3건 (requires_human_approval: true, F17) — 카드 직접 쓰기 없음

- `CRWV_catalysts_vera_rubin_production` — catalysts / annotate — catalysts[2] 'Vera Rubin 최초 배포 일정' — Cognition 프로덕션 가동(2026-09-30)으로 이벤트 도래 주석, 매출 인식 미확인 · 의존: 없음
- `CRWV_axes_customer_concentration_new_names` — axes / annotate — axes[customer_concentration] — 신규 실명 고객(Cognition·MasterClass·Canva) 관측 주석, 정량 집중도 미갱신 · 의존: 없음
- `CRWV_earnings_checkpoints_margin_qoq_align` — earnings_checkpoints / amend — earnings_checkpoints.items[2] 'Adj. EBITDA 마진 59%에서 추가 하락 여부' — YoY 전제 잔여 문구를 확정 기준(QoQ)으로 정합 · 의존: 없음

## approval_order

```json
"[fact] 3건은 서로 다른 행을 치환하고 counts는 자기 필드만 검사 — 순서 무관(드라이런 정순·역순 PASS)."
```

## dry_run

```json
"[fact] scratchpad 사본에 approvals.py 동일 절차 적용 후 verify_after_apply — 단독·정순·역순 모두 PASS. 병합 미리보기: CRWV_dryrun_merged_preview.yaml. 실카드 미수정."
```

## memo_check

```json
"[fact] 직전 메모의 key_metrics '마진 59%로 하락 추세'·risks '마진 하락 추세(59%)'는 2026-09-25 승인 패치로 이미 QoQ 기준 정정 적용(카드 41~42·58~59행) — 충돌 없음, 재패치 불요. 잔여 YoY 전제 문구 1건(earnings_checkpoints '59%에서 추가 하락 여부')만 CRWV_earnings_checkpoints_margin_qoq_align으로 상정. [fact] axes.margin_trend 라벨 앞부분의 'YoY 기준 … 압축' 서술은 기준 병기 원문(P9 보존)이며 확정 기준 주석이 뒤따르므로 충돌로 보지 않았다."
```

## excluded_candidates

```json
[
 {
  "candidate": "axes gpu_priority Vera Rubin 프로덕션 주석",
  "decision": "merged",
  "reason": "[fact] 동일 재료(c_2)를 catalysts 패치에 기재 — 중복 패치 회피."
 },
 {
  "candidate": "CEO '주문 감소 없음' 발언 반영",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_CRWV_3 grade4·confirmed=false, 1차 원문 역추적 실패 — 단독 근거 불가(P4)."
 },
 {
  "candidate": "Cheyenne 88MW 앵커테넌트(Related Digital) 반영",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_CRWV_5 grade3·confirmed=false, 2025-10-07 기존 사실(창 내 신규 아님) — 근거 부족."
 },
 {
  "candidate": "earnings_checkpoints.date(Q3 실적일)",
  "decision": "skipped_logged",
  "reason": "[fact] 회사 공식 일정 Claim 없음 — null 유지(F1)."
 }
]
```

## kc_context

```json
"[fact] 03_signal/CRWV.json proposed_signal 🔴🔴(규칙1, KC-1 매크로 경로) — 종목 KC 3건 경고·발동 단계 모두 not_met. 본 패치는 등급과 무관."
```
