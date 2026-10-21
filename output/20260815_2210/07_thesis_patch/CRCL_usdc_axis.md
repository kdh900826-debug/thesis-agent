# ThesisPatch — CRCL / axes / decompose (usdc_circulation 전제 정정 + P8 분해)

- **Run**: 20260815_2210 · 2026-08-15 (검토 세션)
- **대상 필드**: `axes` (축 `usdc_circulation`)
- **operation**: `decompose` (P8)
- **승인 필요**: ✅ `requires_human_approval: true`
- **핵심 논거 역전 여부**: ⚠️ **예** — 에스컬레이션(esc_20260815_1408_crcl_premise) 경유, **사용자 직접 결정 후 생성**

## 결정 경위 (자동 제안이 아니다)

run 20260815_1408의 thesis-refine은 본 건을 **자동 제안 금지 대상**으로 분류해 승인 큐에 등재하지 않고
`CRCL_escalation_usdc_circulation.md`로 에스컬레이션만 했다.
2026-08-15 검토 세션에서 사용자가 에스컬레이션 문서 검토 후 **"정정 + P8 분해"를 직접 결정**했고, 본 패치는 그 결정의 집행이다.

## 무엇을

```diff
- - {id: usdc_circulation,  label: "USDC 유통량 (축소 추세 — Reserve Income 분자)"}
+ # 2026-08-15 ThesisPatch(decompose, P8) — 이전 축: {id: usdc_circulation, label: "USDC 유통량 (축소 추세 — Reserve Income 분자)"}. …사용자 결정으로 정정
+ - {id: usdc_circulation_scale, label: "USDC 유통량 절대 규모·성장률 (Reserve Income 분자 — 분기말 스냅샷·30일 평잔 병기, KC-CRCL-1 측정 기준 정합. Q2'26 분기말 $73.3B +19% YoY·평잔 +25% YoY)"}
+ - {id: usdc_market_share,      label: "스테이블코인 시장 내 USDC 점유율 (경쟁 침식 관측 — KC-CRCL-2 판정 대상 -3%p QoQ. OUSD·$YLDS 실측 부재로 2026-08-15 Run 관측 불가)"}
```

## 왜

- [fact] 축 라벨의 "축소 추세" 전제는 Q2'26 1차 공시(grade 1)의 **$73.3B +19% YoY·평잔 +25% YoY**와 정면 상충 (`c_20260815_CRCL_002`).
- [fact] 반면 경쟁 침식(OUSD·$YLDS)은 실측 부재로 판정 불가 (`su_stablecoin_01`·`su_stablecoin_02`).
- [inference:strong] 방향 결론을 내장한 축은 판정 단위로 기능하지 못한다 — **파이 크기**와 **침식 여부**는 독립 관측 대상이므로 분해한다.

## 무엇을 하지 않는가

- thesis 문장("파이 성장이 경쟁 침식을 상쇄한다는 구조")은 **가설로서 유지** — 본 패치는 가설의 참/거짓을 판정하지 않는다.
- 시그널(현 🔴) 변경 없음(P13). KC-CRCL-1·2 임계 수정 없음(축 매핑만 재연결).
- 온체인 -2% 관측(`c_20260815_CRCL_007`)은 grade 4·unconfirmed — 판단 근거에서 제외(P4).

## 후속 미결

| 항목 | 상태 |
|---|---|
| 상관 벡터 `vcp_20260815_1408_01` (CRCL CRYPTO 축 강도 M 재검토) | 별개 건 — 미결 유지 |
| risks의 "$YLDS 등 — 리스크 등록부 누락, 패치 대기" | 본 패치 범위 밖 |
