# ThesisPatch 인덱스 — MU (run 20261001_0900, as_of 2026-10-01)

- 패치 5건 (requires_human_approval: true, F17) — 카드 직접 쓰기 없음

- `MU_key_metrics_fy26q4_observations` — key_metrics / amend — key_metrics 7개 중 6개 항목에 FY26 Q4(2026-09-30) 관측치 덧붙임 — SCA 16→26건·RPO·현금예치금·비트/ASP·HBM 마진 갭·CapEx 미재확인 · 의존: 없음
- `MU_earnings_checkpoints_fy26q4_gate_rollover` — earnings_checkpoints / amend — 경과한 2026-09-30 게이트 정리 — items 8개에 9/30 결과·다음 게이트 덧붙임, date를 FQ1-27(2026-12, 정확일 미공시)로 이월, FQ1-27 가이던스 대조 항목 추가(8 → 9) · 의존: 없음
- `MU_catalysts_fy26q4_elapsed` — catalysts / amend — catalysts[0] '9/30 Q4 FY26 실적'에 경과·이행 표기 + 다음 실적 촉매(FQ1-27, 정확일 미공시) 병기 · 의존: 없음
- `MU_risks_netlist_hbm_itc` — risks / amend — risks에 'Netlist ITC 2개 전선(DDR5 337-TA-1523 + 2026-09-29 HBM 2차 제소)' 항목 추가(4 → 5) · 의존: 없음
- `MU_axes_ip_litigation_hbm_second_itc` — axes / amend — axes[ip_litigation_risk] — 관측점 ⑨~⑫ 추가(HBM 2차 ITC 제소, 337-TA-1523 개시일 09-23/09-24 병기, 병행 절차, 9/30 실적 무언급) · 의존: 없음

## approval_order

```json
"[fact] 5건의 before 영역은 서로 겹치지 않고(key_metrics 34~41행 / earnings_checkpoints 59~71행 / catalysts 45행 / risks 54행 / axes 28행 종결부) 각 패치 counts는 자기 필드만 검사한다 — 순서 무관. 권장 순서: key_metrics → earnings_checkpoints → catalysts → risks → axes."
```

## dry_run

```json
"[fact] scratchpad 사본에 approvals.py 동일 절차(replace 1회 → version_history 삽입) 후 approvals.verify_after_apply 호출 — 5건 단독 PASS, 정순 순차 PASS, 역순 순차 PASS. 병합 미리보기: output/20261001_0900/07_thesis_patch/MU_dryrun_merged_preview.yaml. state/thesis_cards/ 미수정."
```

## excluded_candidates

```json
[
 {
  "candidate": "catalysts '8/21 Apple CXMT/YMTC 상원 서한 시한' 경과 정리",
  "decision": "skipped_logged",
  "reason": "[fact] 일자는 경과했으나 결과를 보여 주는 Claim이 없다(c_20261001_MU_9는 실적 자료 무언급만 확인). 근거 부족 → 패치 제외(P5)."
 },
 {
  "candidate": "key_metrics NTM Forward P/E 갱신",
  "decision": "skipped_logged",
  "reason": "[fact] 분자(EPS)는 갱신됐으나 분모(주가)가 L4 구조화 입력에 없어 P10 분해 불가 — 04_sector/memory.json valuation_paradox도 frame_only_no_denominator."
 },
 {
  "candidate": "axes production_continuity 대만 노조 파업투표(10월 초) 반영",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_MU_12 grade3·confirmed=false 단독, 회사 1차 자료 0건 — 카드 자체 제약(grade3 단독은 방향 미부여)에 따라 신규 관측 기입 보류."
 },
 {
  "candidate": "MU 전용 KC 신설(add_kc)",
  "decision": "escalated",
  "reason": "[fact] 5회 연속 미정의(esc_20261001_memory_01). 임계 수치 확정은 사람 영역(P11·§9) — 임계 없는 add_kc는 무효이므로 자동 제안하지 않는다."
 }
]
```

## instruction_check

```json
"[fact] 지시의 '337-TA-1523 개시일 09-23/09-24 불일치 병기'는 axes·risks·earnings_checkpoints 3개 패치에서 정정 없이 병기했다(c_20261001_MU_11 grade3·confirmed=false). 'SCA 26건(카드 16건 대비)'은 key_metrics에서 16건 원문 보존 + 26건 덧붙임으로 처리했다."
```

## kc_context

```json
"[fact] 03_signal/MU.json proposed_signal 🔴🔴(규칙1, KC-1 met+confirmed) — 사람 확인 대기. 본 패치 세트는 등급과 무관하며 자동 적용되지 않는다(§7)."
```
