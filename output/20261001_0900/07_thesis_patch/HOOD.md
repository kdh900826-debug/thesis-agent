# ThesisPatch 인덱스 — HOOD (run 20261001_0900, as_of 2026-10-01)

- 패치 1건 (requires_human_approval: true, F17) — 카드 직접 쓰기 없음

- `HOOD_axes_federal_jurisdiction_docket_26_338` — axes / annotate — axes[prediction_market_federal_jurisdiction] — 경과한 관측점(9/28 long conference) 정리: SCOTUS 26-338 도켓 상태·응답기한 10-14, D.Conn. 계류 · 의존: 없음

## approval_order

```json
"[fact] 1건 — 순서 의존 없음."
```

## dry_run

```json
"[fact] scratchpad 사본 적용 후 verify_after_apply PASS. 실카드 미수정."
```

## excluded_candidates

```json
[
 {
  "candidate": "key_metrics·axes.prediction_market — 9월 MTD 이벤트계약 약 44억 건·크립토 명목 약 $17B·주식 약 $267B·옵션 약 2.34억 건(2026-09-28 투자자 행사)",
  "decision": "ineligible",
  "reason": "[fact] c_20261001_HOOD_8 grade 4·confirmed=false — 회사 1차 URL을 특정했으나 본문 대조 실패(WebFetch 타임아웃), 수치는 2차 매체(BTIG 인용) 의존. preliminary·unaudited 월중(1~24일) 수치이며 회사는 정식 9월 지표를 Q3 실적과 함께 공개한다고 전해진다. [fact] 일평균 +21~25% 환산(c_9)은 inference이며 건수·명목액은 매출이 아니다(P7). → 카드 수치 반영 부적격(P4). 정식 9월 월간 운영지표(grade 1) 확보 시 key_metrics 갱신 후보로 이월."
 },
 {
  "candidate": "key_metrics 크립토 항목 '가스비 보조금 2026-09-29 종료 예정' → 종료 반영",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_HOOD_7 grade 4·confirmed=false(2차 크립토 매체) 단독 — 종료 자체는 예정대로였을 개연성이 높으나 1차 확인 없음. 9월 정식 운영지표와 함께 차기 run에서 일괄 갱신 권장."
 },
 {
  "candidate": "arpu_mix — 주말 24시간 거래 확대 계획",
  "decision": "skipped_logged",
  "reason": "[fact] c_20261001_HOOD_10 grade 4, 출시일·수수료 미공개 — P7 1단계(존재)이며 근거 부족."
 },
 {
  "candidate": "prediction_market_state_enforcement — 미시간·코네티컷·미주리",
  "decision": "no_change",
  "reason": "[fact] 03_signal·arbiter 모두 상태 변화 없음(c_4·c_5·c_6). 미주리 발신일 09-16 원문 재확인은 카드 기재와 일치 — 패치 불요."
 }
]
```

## kc_context

```json
"[fact] 03_signal/HOOD.json proposed_signal 🟡 — 본 패치는 등급과 무관."
```
