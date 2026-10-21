# ThesisPatch 인덱스 — COIN (run 20261001_0900, as_of 2026-10-01)

- 패치 0건 (requires_human_approval: true, F17) — 카드 직접 쓰기 없음


## basis_claims_note

```json
"[fact] 패치 0건 — 본 basis_claims는 '패치 없음' 판정에 검토한 Claim 목록이다(검증기 스키마상 필수 필드, 컨테이너 dict). 승인 큐 미등재."
```

## zero_patch_reason

```json
"[fact] 검토 후보 2건 모두 패치 요건 미충족 — 아래 excluded_candidates 참조. 0건은 정상 경로다(P12)."
```

## excluded_candidates

```json
[
 {
  "candidate": "KC-COIN-3 '연방 한정' 서술 정정",
  "decision": "no_target_in_card",
  "reason": "[fact] state/thesis_cards/COIN.yaml 전문 64행에서 '연방' 문자열 0건 — 카드는 kill_conditions_ref에 'KC-COIN-3' ID만 기재하고 trigger 서술을 담지 않는다. 정정 대상 문구가 카드에 없으므로 패치 불요. [fact] config/kill_conditions.yaml KC-COIN-3 trigger 원문은 '(a) SEC·CFTC·DOJ의 신규 제소, 또는 (b) 주요 사업(거래·스테이킹·스테이블코인) 대상 영업정지·인가 취소'(기관 불문)이며 03_signal 재판정·04_sector esc_1001_06과 일치한다. [fact] 다만 config 136행 주석 '# 2026-08-15 사용자 확정 — 연방 기관 + 영업상 중대로 한정'이 trigger (b)의 기관 불문 문언과 어긋나 오독 소지가 있다 — config는 사용자 편집 영역이므로 주석 문구 정리를 제안만 한다(§9). [fact] 미시간 항소(6th Cir. No. 26-1693)의 (b)항 해당 여부는 03_signal이 unresolved_fact로 사람 판단에 넘겼다."
 },
 {
  "candidate": "derivatives_base — Coinbase Clearing DCO 등록(2026-09-28)",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_COIN_3 grade 3·confirmed=false 단독(The Block 보도), CFTC 등록명령 원문·등록번호 1차 미대조 — P4상 단독 근거 불가. [fact] 등록은 완전담보 상품 청산 한정이며 매출 영향 수치 없음, 개별주식 무기한선물은 여전히 Approval Pending(c_4, grade4). 차기 run에서 cftc.gov 1차 문서 확보 시 derivatives_base 관측 주석 후보로 이월(unconfirmed)."
 },
 {
  "candidate": "usdc_economics·catalysts 'OUSD 출시 및 COIN 분배 조건 공개' — OUSD 참여 구조",
  "decision": "skipped_logged",
  "reason": "[fact] c_5(grade3)·c_6(grade4) 모두 confirmed=false, coinbase.com 1차 블로그 403 접근 실패 3회 연속. 카드 지시상 OUSD 참여는 강세 재료로 기본 분류하지 않으며 03_signal도 neutral(순효과 미확정). CRCL 카드와 달리 COIN 카드에는 이 관측에 대한 사전 정의 활성화 조건이 없어 grade 3·4 단독 기입 실익이 낮다 — 차기 run 1차 확보 후 재검토."
 }
]
```

## kc_context

```json
"[fact] 03_signal/COIN.json decision=maintain(🟠), Kill 미발동(KC-COIN-3 unresolved_fact — 사람 판단 미결)."
```
