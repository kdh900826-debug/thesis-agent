# ThesisPatch 인덱스 — IREN (run 20261001_0900, as_of 2026-10-01)

- 패치 0건 (requires_human_approval: true, F17) — 카드 직접 쓰기 없음


## basis_claims_note

```json
"[fact] 패치 0건 — 본 basis_claims는 '패치 없음' 판정에 검토한 Claim 목록이다(검증기 스키마상 필수 필드, 컨테이너 dict). 승인 큐 미등재."
```

## zero_patch_reason

```json
"[fact] 조사 창(2026-09-24~10-01) IREN company_specific Claim은 2건뿐이며 둘 다 '신규 실질 1차 공시 부재'를 확인하는 내용이다 — 8-K·10-Q·10-K·424B·S-8 0건, 회사 보도자료 0건, 유일 신규 공시는 Citadel 계열 SCHEDULE 13G(5% 미만 수동지분 보고, c_20261001_IREN_1). 6개 회차 연속 신규 1차 근거 0건. 6개 축 delta 전부 neutral(arbiter 필터본). 카드 항목을 부정확하게 만든 신규 사실이 없으므로 0건이 정답이다(P5 — 부재는 반증이 아니며 카드 서술을 바꿀 근거도 아니다; P12)."
```

## excluded_candidates

```json
[
 {
  "candidate": "funding_dilution — Citadel 13G",
  "decision": "noise",
  "reason": "[fact] 수동지분 보고로 발행·전환과 무관, 완전희석 주수 range 갱신 불가(04_sector neocloud funding_dilution null_observation)."
 },
 {
  "candidate": "earnings_checkpoints BC Hydro Call for Demand 결과(통보 시점 2026-09 중순 기재)",
  "decision": "skipped_logged",
  "reason": "[fact] 이번 run company_specific Claim에 결과 공표 관련 내용 없음(scope=sector Claim 4건은 필터로 제거 — L4가 개별 카드 근거로 사용 불가, P6·P13). 기재된 통보 시점 경과 여부는 차기 run L2 확인 대상으로 이월."
 },
 {
  "candidate": "earnings_checkpoints.date '2026-11 (FY27 Q1 10-Q — 정확일 미공시)'",
  "decision": "no_change",
  "reason": "[fact] c_20261001_IREN_2: FY27 Q1 실적일 회사 공식 발표 없음 — 현 표기 유지가 타당."
 }
]
```

## kc_context

```json
"[fact] 03_signal/IREN.json proposed_signal 🔴🔴(규칙1, KC-1 매크로 단독 — 펀더멘털 6축 변화 없음). 본 0건 판정은 등급과 무관."
```
