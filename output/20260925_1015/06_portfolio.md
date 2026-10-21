# L4 포트폴리오 통합 뷰 — run 20260925_1015

- **as_of**: 2026-09-25T10:48 / **staleness_days**: 0 / **reused_from**: 없음
- **produced_by**: cio-portfolio (L4)
- **default_action**: `no_action`
- **[fact]** 이 문서는 시나리오·한도·이격도만 보여준다. 매수·매도 지시가 아니다(P15·F18). 목표 비중 단일값과 시점 지시는 넣지 않았다.
- **[fact]** 등급·행동·임계 확정은 전부 사람의 권한이다(CLAUDE.md §9).
- **[fact]** 모든 주장 문장에 `[fact]` 또는 `[inference/강도]` 태그를 붙였다(P1).
- 구조화 원본: `06_portfolio.json`, `05_correlation.json`

---

## 0. 한 문단 요약

**[fact]** KC-1(FFR 4.00 > 3.75, confirmed)이 2회차 연속 met이다. 그사이 신규 FOMC는 없었다. **[fact]** 그래서 arbiter 규칙1이 IREN·NBIS·CRWV·MU 4종목에 🔴🔴 **후보**를 다시 냈다. **[fact]** 그런데 `state/signals.json`은 여전히 KC-1 이전 등급을 보여준다(as_of 2026-09-05, transitions 빈 배열). 09-19 run이 요청한 사람 확인 결과가 기록되지 않은 것이다. 따라서 이번 후보는 **미처리 요청을 다시 올리는 것**이다. **[fact]** KC-9는 brent 114.89 < 120으로 not_met이 됐다. L1은 duration이 사실상 리셋됐다고 기록했다. **[fact]** 실제 보유는 IREN 단독 + 현금이다. 🔴🔴 후보 4건 중 3건은 포지션에 영향이 없다. **[fact]** MU는 규칙1과 별개로 규칙3(비대칭 하향)도 독립 충족됐다(USITC 337-TA-1523 조사개시, grade 1). **[fact]** 🔴🔴가 포함된 run이므로 자동 실행 없이 사람 확인 요청으로 종료한다.

---

## 1. 입력과 격리 (P16·P17)

| 입력 | as_of | staleness | 비고 |
|---|---|---|---|
| `01_macro_kc.json` | 2026-09-25T10:18 | 0 | |
| `04_sector/{neocloud,memory,stablecoin}.json` (+aggregate) | 2026-09-25 | 0 | memory 파일의 reused_from은 스키마 참조 |
| `05_correlation.json` | 2026-09-25T10:37 (LLM 10:43) | 0 | |
| `03_signal/*.json` | 2026-09-25 | 0 | 구조화 판정 확인 전용 |
| `config/correlation_matrix.yaml` | 2026-08-15 | 41 | status: active → U4 중단 사유 아님 |
| `config/positions.yaml` | 2026-09-19 | 6 | |
| `config/kill_conditions.yaml` | 2026-08-15 | 41 | |
| `state/signals.json` | 2026-09-05 | 20 | 읽기 전용 |
| `state/pending_approvals.json` | — | — | 49건 중 pending 0건 |

**[fact]** `02_company/*` 원문, `_raw_*`, `state/thesis_cards/*`는 로드하지 않았다(P17). **[fact]** `state/`·`config/`에는 쓰지 않았다.

---

## 2. 매크로 KC 통합

| KC | 판정 | 이격 | 직전 회차 대비 |
|---|---|---|---|
| **KC-1** FFR>3.75 | **met / confirmed** | +0.25%p 초과 | 2회차 연속, 값 불변 |
| KC-2 VIX≥30 | not_met / confirmed | 14.33pt 여유 | |
| KC-3 BTC<55k & VIX≥25 | not_met / confirmed | BTC 29,653.665 USD · VIX 9.33pt 여유 | BTC 여유 확대 |
| KC-4 ON RRP≥200B & VIX≥25 | not_met / confirmed | 해석 불가($630M) | 경보 기능 상실 지속 |
| KC-5 TAIEX | not_met / confirmed | +3.44%p / +7.58%p | |
| KC-6 SDLLMTK | not_met / provisional | **산출 불가 — 입력 null** | 직전 3.2 → 공란 |
| KC-7 / KC-8 | not_met / provisional | 6.835B / 19.64B USD 여유 | as_of 06-30 |
| **KC-9** brent≥120(1개월) | **not_met / provisional** | 5.11 USD 미달 | **met → not_met** |
| KC-10 IREN 전력·인허가 | not_met / provisional | 이벤트형 | |

### KC-1 사전 정의 결과 문언과 현 장부의 대응

> `레버리지 전액 해제 + Edge/Next 50% 축소 검토` — `config/kill_conditions.yaml#macro.KC-1.consequence` 원문 인용(본 에이전트가 작성한 지시가 아님)

| 조항 | 현 장부 | 대상 |
|---|---|---|
| 레버리지 | 미사용. v32 레버리지 규칙은 Base 미보유로 비활성 | **없음** |
| Edge | IREN [0.85, 0.95] | **IREN 1종목** |
| Next | CRCL·COIN·HOOD 전부 미보유 | **없음** |
| (문언 밖) | MU(Base)·NBIS·CRWV 미보유 | 🔴🔴 후보지만 포지션 효과 없음 |

**[fact]** 위 표는 사전 정의 문언과 장부 상태를 대조한 사실일 뿐이다. 실행 여부·범위·시점은 사람이 판단한다.

### KC-9 duration — 10-10 시한은 실효를 잃었나

**[fact]** 관측 계열: 09-10 120.98 / 09-11 118.06 / 09-14 121.25 / 09-15 130.8 / 09-16 127.84 / 09-17 121.18 / 09-18 119.66 / 09-21 116.15 / 09-22 114.89.
**[inference/강]** 09-19 run이 설정한 시한 2026-10-10은 '09-10부터 1개월 연속'을 전제로 했다. 그 연속 구간이 09-11과 09-18 이후 두 번 끊겼으므로 시한은 충족할 수 없게 됐다. 즉 실효를 잃은 것으로 읽힌다.
**[fact]** 다만 `kill_conditions.yaml`에는 duration을 연속으로 셀지 누적으로 셀지가 정의돼 있지 않다. 리셋 확정과 정의 명문화는 사람이 할 일이다.
**[fact]** 직전 회차의 사람 override 제안(not_met·경고 유지)과 이번 자동 판정(not_met)은 일치한다.

---

## 3. 시그널 등급 (P13 — 인용, 수정 없음)

| 종목 | state 확정 | 후보 | 경로 | 규칙1이 없을 때 | 보유 |
|---|---|---|---|---|---|
| IREN | 🟡 | **🔴🔴** | KC-1 (2회차) | maintain | ○ |
| NBIS | 🟡 | **🔴🔴** | KC-1 (2회차) | maintain | ✕ |
| CRWV | 🟡 | **🔴🔴** | KC-1 (2회차) | maintain | ✕ |
| MU | 🟠 | **🔴🔴** | KC-1 (2회차) | **🔴 하향 후보(규칙3 독립 충족)** | ✕ |
| CRCL | 🔴 | 🔴 | — | maintain | ✕ |
| COIN | 🟠 | 🟠 | KC-COIN-3 met_candidate / unconfirmed | maintain | ✕ |
| HOOD | 🟡 | 🟡 | — | maintain | ✕ |

**[fact]** CRWV 03_signal에는 `human_confirmation_required` 필드가 없다(esc_L4_1015_18).
**[inference/강]** 🔴🔴 4건은 독립된 사건 4개가 아니다. 하나의 매크로 사건이 KC-1 파급 집합(CRWV·IREN·MU·NBIS, RATES 축)으로 번진 것이다.

---

## 4. 리밸런싱 뷰 (S6) — 시나리오 17건, 전부 사전 정의 KC·한도에 연결 (P11)

| ID | 트리거 (source) | 판정 | 이격 | 대상 |
|---|---|---|---|---|
| sc_01 | KC-1 | **met/confirmed** | +0.25%p 초과 | CRWV·IREN·MU·NBIS (상단 95.0) |
| sc_02 | KC-2 | not_met | 14.33pt | 6종목 |
| sc_03 | KC-3 | not_met | BTC 29,653.665 USD / VIX 9.33pt | COIN·CRCL·HOOD·IREN |
| sc_04 | KC-4 | not_met | 해석 불가 | 6종목 |
| sc_05 | KC-5 | not_met | +3.44%p / +7.58%p | 6종목 |
| sc_06 | KC-6 | not_met/prov. | 산출 불가(입력 null) | 4종목 |
| sc_07 | KC-7 | not_met/prov. | 6,835,000,000 USD | 4종목 |
| sc_08 | KC-8 | not_met/prov. | 19,640,000,000 USD | 4종목 |
| sc_09 | KC-9 | **not_met/prov.** | 5.11 USD 미달, duration 리셋 방향 | 4종목 (KC-1과 RATES 공유 — 중복 계상 금지) |
| sc_10 | KC-10 | not_met/prov. | 이벤트형 | IREN |
| sc_11 | 축 집중도 60%(초안) | **breach 6/8축** | +35.0pp | IREN |
| sc_12 | IREN 가격 라인 30/28 | 산출 불가 | 가격 피드 없음(4회차) | IREN |
| sc_13 | 레버리지 40% 규칙 | 비활성 | 분모 0 | — |
| sc_14 | 종목 KC 17건 파급 | 산출 불가 | 매핑 미정의 | — |
| sc_15 | **KC-COIN-3** | met_candidate/unconfirmed | 이벤트형 | COIN(미보유) |
| sc_16 | **KC-CRWV-3** | not_met/confirmed | 경고까지 +0.86x(2.36x) / 정태 추정 +0.71x(2.21x) | CRWV(미보유) |
| sc_17 | **KC-HOOD-3** | not_met/prov. | 산출 불가(상위 3개 주를 특정할 분모 미공시) | HOOD(미보유) |

**[fact]** 신규로 넣은 sc_15~17은 이번 회차 구조화 산출물에 판정 경계 관련 기록이 새로 생긴 종목 KC들이다.
- **sc_15** — **[fact]** 이 KC가 아직 발동하지 않은 이유는 사건이 없어서가 아니다. 근거 등급이 기준에 못 미치기 때문이다(portal.ct.gov 미등재 → grade 4). **[fact]** 그런데 config 문언은 발동 주체를 'SEC·CFTC·DOJ'로 한정한다. 또 '경미한 주정부 행정조치는 노이즈'라고 적고 있고, 주요 사업 열거에 예측시장은 없다. **[inference/중]** 따라서 도메인을 등재해 등급 문제가 풀려도, 이번 사건이 문언상 발동 대상인지는 따로 해석해야 한다.
- **sc_16** — **[fact]** 2026-09-22 8-K에서 교차부도 covenant 문턱이 처음 1차 공시됐다. 그 결과 '즉시 발동' 조건을 관측할 기준이 생겼다.
- **sc_17** — **[fact]** config에는 '상위 주 중 3개 이상' 기준이 있다. 그런데 arbiter는 2회차 연속 이 기준이 발췌본에 없다고 기록했다. 발췌본 생성 과정에서 빠진 것이다.

---

## 5. 축 집중도 경보 — **breach (8축 중 6축, 4회차 연속)**

| 축 | 노출 종목 수 | 보유 | 상단 |
|---|---|---|---|
| AI_CAPEX · RATES · CRYPTO · GPU_SUPPLY · POWER_PERMIT · RISK_APPETITE | 4·7·4·3·1·6 | IREN | **95.0** |
| REGULATION · USDC_DISTRIBUTION_ECONOMICS | 3·2 | — | 0.0 |

- **[fact]** 임계 60은 config상 '⚠️초안'이다.
- **[inference/강]** 판별력이 없다. IREN 단일 포지션 때문에 값이 95.0 아니면 0.0 둘 중 하나로만 나온다. 이 경보가 말해 주는 것은 축별 위험 순위가 아니라 **분산이 없다는 사실**이다.
- **[fact]** 현재 met인 유일한 매크로 KC(KC-1)의 전달 축은 RATES다. 이 축의 보유분은 IREN(-M) 하나뿐이다. 반대 부호(+) 종목은 전부 미보유다. **[inference/중]** 즉 장부 안에서 이 노출을 상쇄하는 부분이 0이다. 이는 구조를 기술한 것이며 조정 제안이 아니다.
- **[fact]** L3 stablecoin은 COIN·HOOD의 예측시장 노출을 헤지가 아니라 **동일 부호 공통 노출**로 판정했다.

---

## 6. 상관 레이어 요약 (`05_correlation.json`)

**[fact]** 입력 config가 바뀌지 않았으므로 [CODE] 산출은 직전 회차와 구조가 같다. pair_overlap 21쌍 중 '상' 6쌍, KC 파급 27건(매핑 10 / 미정의 17), 축 집중도 8건이다. 수치형 상관계수는 쓰지 않았다(P14).
**[fact]** 두 측정 체계가 서로 다른 답을 낸다. 벡터 기준으로 IREN–CRWV·IREN–NBIS는 '상'이지만, L3의 카드 축 렌즈로는 '하'다. 본 레이어는 둘을 조정하지 않는다.

### 노출 벡터 변경 제안 — 9건 (부호·강도 변경 요구 0건, 자동 수정 0건)

| ID | 대상 | 상태 | 요지 |
|---|---|---|---|
| vcp_01 | IREN.CRYPTO | 이월 4회차 | 예약 문언 기준일 교체 여부(FY27 Q1 10-Q 또는 채굴 종료 공시) |
| vcp_02 | NBIS.RATES | 이월 4회차 | NBIS 조달 관측 0건 — 강도 판단 불가 |
| vcp_03 | GPU_SUPPLY 축 | 이월 2회차 | 분해 대 축소 — 이번 회차 신규 근거 없음 |
| vcp_04 | KC-9→RATES | 감시 3회차 | 매핑 유지. 재검토 조건을 '10-10 시한' 대신 ENERGY 트리거 3개로 일원화할지 |
| vcp_05 | CRCL.RATES +H | 이월 2회차 | 이번 reserve_income weaken의 원인은 금리가 아니라 Binance 비용 |
| **vcp_06** | CRCL USDC_DISTRIBUTION_ECONOMICS | 신규 | Binance 5년 재계약 → 분배 구조가 다자화. basis 병기 + '제로섬' label 검토 |
| **vcp_07** | COIN.REGULATION basis | 신규 | 예측시장 주 집행 노출은 COIN·HOOD 같은 부호 → basis 병기. 역노출 신설은 불필요 |
| **vcp_08** | YIELD_BEARING 조건부 트리거 | 신규 | '09-15 표결' 날짜 기준이 사라짐 → 사건 기준으로 교체. $YLDS 수치 정합 |
| **vcp_09** | CRWV RATES·AI_CAPEX basis | 신규 | '~2.2x'(Q1'26)와 KC-CRWV-3 주석 2.36x(Q2'26)의 기준 시점 불일치 |

---

## 7. 섹터 층 입력과 한계 — 3개 섹터 전부 방향 미산출

- **neocloud** — **[fact]** 공유 축 0개(5회 연속)다. **[fact]** 원인이 하나 새로 확인됐다. NBIS는 변화가 없는 축에 delta를 내지 않는데, IREN·CRWV는 neutral delta를 모두 낸다(발행 규약 불일치). 그래서 NBIS와 CRWV가 이름이 같은 축 2개를 갖고 있는데도 집계에서 묶이지 않았다.
- **memory** — **[fact]** MU ip_litigation_risk가 weaken으로 바뀌었다(ITC 337-TA-1523). L3는 이를 MU 고유 요인으로 판정했다. **[fact]** SK하이닉스 라이선스 상태는 '미확인'이다. 'licensed'라는 전제는 오류였다(esc_20260925_memory_04).
- **stablecoin** — **[fact]** 명목 공유 축 1개(prediction_market)가 외견상 분산을 냈다. 하지만 원인은 정의 범위가 달라서다. HOOD 축만 분해돼 있다. **[fact]** CRCL 쪽 비용 증가의 수취자는 Binance다. 이를 COIN의 이득으로 거꾸로 계산하면 안 된다.
- **[inference/강]** 결합이 실패하는 원인은 세 겹이다. 명명 불일치, 무변화 축 delta 발행 규약, 같은 이름에 다른 정의. 명명만 표준화해서는 해소되지 않는다.

---

## 8. Thesis 정교화 (S7) — **후보 11건만 기록, ThesisPatch 생성 0건**

**[fact]** F20(전문 확인)과 P17(카드 로드 금지)이 충돌해 before→after는 만들지 않았다. 집행은 `refine thesis <TICKER>`로 한다. **[fact]** 직전 회차 후보는 2026-09-19~20에 전부 approved로 처리됐다(pending 0건).

| ID | 종목 | 필드 | op | 한 줄 | 사람 결정 종속 |
|---|---|---|---|---|---|
| tpc_01 | CRWV | key_metrics/thesis | amend | 마진 'YoY 하락 추세' 문구를 09-20 확정 기준(QoQ)에 맞춤 | 없음 |
| tpc_02 | CRWV | kill_conditions_ref | annotate | 교차부도 covenant 문턱을 KC-CRWV-3 관측 기준으로 병기 | 없음 |
| tpc_03 | MU | axes.ip_litigation_risk | amend | ITC 337-TA-1523 + CDCA/D.Del/CAFC 관측점 + 9/30 소송 각주 체크포인트 | 없음(축명 정규화는 종속) |
| tpc_04 | MU | risks | annotate | SK하이닉스 라이선스를 '미확인'으로 정정(카드에 해당 전제가 있을 때만) | 없음(문구 존재 확인이 먼저) |
| tpc_05 | NBIS | axes.on_demand_pricing_power | annotate | grade 3→1 격상, 10-01 발효·할인 전가를 관측점으로 | **부분 종속**(delta 발행 규약) |
| tpc_06 | CRCL | reserve_income·circulation/catalysts | amend | Binance 5년 재계약 반영 + Q3 요율 확인을 관측점으로 | 없음 |
| tpc_07 | CRCL | key_metrics.usdc_market_share | annotate | Visa '거래 유틸리티 70%'를 제3계열로 명시 | **종속**(제3계열 채택) |
| tpc_08 | CRCL | axes.diversification | annotate | Arc 첫 주 지표를 기준선으로(CEO가 지속성 유보) | 없음 |
| tpc_09 | CRCL | catalysts | amend | CLARITY: 재표결 미실시·레임덕 지연·이자부 조항 미해결 | 없음 |
| tpc_10 | COIN | axes.prediction_market | decompose | HOOD와 같은 분해 또는 사상 테이블 중 택일 | **종속**(표준화·방식 선택) |
| tpc_11 | HOOD | axes(토큰화 후보) | annotate | SEC Innovation Exemption·토큰화 계획을 독립 축 후보로 | **종속**(표준화 선행) |

**[fact]** 후보에서 뺀 항목: IREN BC Hydro 지연(근거 grade 4·scope=sector → unconfirmed로 적재). config 영역 항목(KC·sources·벡터)과 signals.json next_gate는 escalation 또는 vcp로 넘겼다.
**[inference/중]** 축을 늘리거나 쪼개는 패치(tpc_10·11)를 표준화 결정 없이 먼저 집행하면, 공유 축 0개 상태가 굳어질 수 있다.

---

## 9. 검증

| 산출물 | layer | 결과 |
|---|---|---|
| `05_correlation.json` | correlation | **PASS** (1회차) |
| `06_portfolio.json` | portfolio | **PASS** (1회차) |

---

## 10. 🔴🔴 사람 확인 요청 + 근거 패키지 (CLAUDE.md §7)

### 명시: state 공백
**[fact]** `state/signals.json`은 KC-1 이전 등급을 그대로 보여준다(IREN 🟡·NBIS 🟡·CRWV 🟡·MU 🟠, as_of 2026-09-05, transitions=[]). **[fact]** 2026-09-19 run이 요청한 사람 확인 결과는 어디에도 기록되지 않았다. **[fact]** 승인 큐에는 thesis_patch 유형만 있고, 🔴🔴 확인 결과를 담을 경로가 없다. **[inference/중]** 결정이 이미 내려졌는데 기록만 안 된 것인지, 아직 결정되지 않은 것인지는 본 레이어가 구분할 수 없다.

### 근거 패키지
1. KC-1 — `01_macro_kc.json#kc_status[KC-1]`: FFR 4.00 > 3.75 (FRED api, 09-24)
2. 사전 정의 문언과 장부 대응 — sc_01: 실질 대상은 Edge(IREN) 조항뿐
3. 후보 출처 — `03_signal/{IREN,NBIS,CRWV,MU}.json#kill_check·gate_check`: MU만 규칙3 독립 하향 경로가 함께 있음
4. 현행 확정 등급 — `state/signals.json`
5. KC-9 리셋 — `01_macro_kc.json#analyst_intervention[KC-9]`
6. 축 집중도 — `05_correlation.json#axis_concentration`
7. KC-COIN-3 게이트·문언 — sc_15
8. 섹터 한계 — `04_sector/*.json`

### 요청 결정사항
1. 🔴🔴 후보 4건을 확정할지 기각할지, 그리고 결정을 어디에 기록할지 지정 (MU는 두 경로를 대조) — esc_L4_1015_01
2. KC-9 duration 리셋 확정, 10-10 시한 실효 여부, 연속/누적 정의 — esc_L4_1015_02
3. 섹터 결합의 세 겹 결함 결정: 명명 매핑 + 무변화 축 delta 규약 + 분해 수준 정합 — esc_L4_1015_03
4. KC-COIN-3: sources.yaml 도메인 등재 + 문언 범위 해석 — esc_L4_1015_04·05
5. MU 전용 KC 임계 정의 (9/30 실적 5일 전) — esc_L4_1015_06
6. vcp_01~09 처리
7. tpc_01~11 집행 여부 (종속 4건)
8. CRCL next_gate에 Binance 요율 항목 추가 (signals.json)

### 에스컬레이션 총괄 — 19건 (top 3 / high 4 / medium 6 / low 6)
top: 01 🔴🔴 미기록 · 02 KC-9 duration · 03 섹터 결합 3겹 결함
high: 04 도메인 미등재가 KC 게이트까지 도달(portal.ct.gov·usitc.gov·michigan.gov·ago.mo.gov·supremecourt.gov·cftc.gov·senate.gov·federalregister.gov·cafc.uscourts.gov) · 05 KC-COIN-3 문언 범위 · 06 MU KC 미정의(5회) · 07 집중도 임계 초안
medium: 08 전제·발췌본 전달 결함 반복(SK하이닉스, KC-HOOD-3) · 09 GPU_SUPPLY · 10 종목 KC 매핑 · 11 KC-4 · 12 IREN 가격 라인 · 13 KC-6 입력 null
low: 14 에이전트 정의 파일 stale(company-mu 5축 대 7축, company-crcl 5축 대 8축, arbiter 축명 hbm_demand) · 15 집계기 라벨 의미 · 16 예측시장 역노출 재분류 · 17 MU 필터 잔여 참조 · 18 CRWV 확인 플래그 필드 없음 · 19 COIN 중복 계상 확인

**[fact]** 위 결정이 나오기 전까지 이 시스템이 자동으로 수행할 후속 단계는 없다. default_action은 `no_action`이다(P12).
