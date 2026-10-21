# 포트폴리오 통합 뷰 — run 20260911_2308

- **as_of** 2026-09-12 · **계층** L4 (`cio-portfolio`) · **staleness_days** 0
- **기본 판정: `no_action` (행동 없음 / 등급 유지)** — KC 27건 전건 `not_met`, 🔴🔴 0건, 시그널 7종목 전건 유지, 섹터 방향 입력 0건.

> **이번 run 한 줄 요약**
> [fact] 판정은 직전 run과 동일하게 전부 멈춰 있지만, **위험의 위치가 움직였다** — 유가(KC-9) 이격도가 이번 회차에 가장 크게 좁아졌는데 하필 그 KC만 종목 파급 경로가 시스템에 정의돼 있지 않고, 금리(KC-1)는 4회 연속 임계에 0.00pp로 붙은 채 근거 자료만 45일째 늙고 있다.

> **본 문서의 성격**: 시나리오·사전 정의 한도·이격도만 기술한다. 행동 지시, 목표 비중 단일값, 시점 지시를 포함하지 않는다(P15). 포지션 행동과 등급 확정은 사람의 결정이다.

---

## 1. KC 이격도 보드 (근접순)

| # | KC | 조건 | 현재값 | 이격도 | 판정 | 파급 종목 | 비고 |
|---|---|---|---|---|---|---|---|
| 1 | **KC-1** | FFR(상단) > 3.75 | 3.75 | **0.00pp — 경계 접촉 (4회 연속)** | not_met / provisional | CRWV·IREN·MU·NBIS (4) | 근거 staleness 45일, 갱신 없음 |
| 2 | **KC-5** | TAIEX 20dma 하회 **AND** 1개월 수익률 음전환 | +2.03 / +3.12 | 20dma 레그 2.03%p · 1개월 레그 **3.12%p**(구속) | not_met / confirmed | 6종목 | 두 레그 모두 직전보다 넓어짐 |
| 3 | **KC-9** | Brent ≥ $120 (1개월 지속) | $109.51 | **+9.58% 필요 ($10.49) / 임계 대비 −8.74%** | not_met / provisional | **산출 불가 — 축 매핑 부재** | 이번 회차 최대 축소폭 |
| 4 | **KC-3** | BTC < 55,000 **AND** VIX ≥ 25 | 77,252.7 / 15.84 | BTC −28.80% · VIX +9.16p | not_met / confirmed | COIN·CRCL·HOOD·IREN (4) | 두 레그 모두 좁아짐 |
| 5 | **KC-2** | VIX ≥ 30 | 15.84 | +14.16p (약 1.89배) | not_met / confirmed | 6종목 | 15.47p → 14.16p |
| 6 | **KC-8** | MSFT FCF < 0 | +$19.64B | 부호 전환 필요 | not_met / provisional | CRWV·IREN·MU·NBIS (4) | 입력 as_of 6/30, 74일 |
| 7 | **KC-7** | 하이퍼스케일러 4사 합산 FCF < 0 (2분기 연속) | +$6.835B | 부호 전환 필요 | not_met / provisional | CRWV·IREN·MU·NBIS (4) | 직전 분기 수치 미수집 |
| 8 | **KC-6** | LLM 토큰지출 변화율 ≤ −30% (2주 지속) | +11.2% | 41.2%p 역방향 | not_met / provisional | CRWV·IREN·MU·NBIS (4) | 부호 자체가 반대, 더 넓어짐 |
| 9 | **KC-4** | ON RRP ≥ $200B **AND** VIX ≥ 25 | $5.255B / 15.84 | 약 38.1배 | not_met / confirmed | 6종목 | ⚠️단위 정합 미확인(이월) |
| — | **KC-10** | IREN 계약용량 10%+ 강제 감축 분류 또는 접속·인허가 취소·보류 | 이벤트형 | **산출 불가 — 분모(SB6 적용 MW) 미공시** | not_met / provisional | IREN (1) | 유일 보유 종목 직결 |

**단위 주석**: [fact] 위 순위는 "임계 도달에 필요한 해당 지표의 상대 변동폭"으로 환산해 정렬했다. 원 단위는 KC마다 다르므로(퍼센트포인트·지수 포인트·달러·배수·부호 전환) 이 순위는 참고용이며 KC 간 발동 확률의 비교 근거가 아니다. [fact] 오케스트레이터 지시문은 KC-9를 KC-1 다음으로 가까운 매크로 KC로 지목했는데, 상대 변동폭 기준으로는 KC-5의 구속 레그(3.12%p)가 그 사이에 들어온다 — 직전 run에서도 KC-5 두 레그가 2·3순위였다. 어느 쪽도 오류가 아니라 척도 선택의 문제다.

**종목 전용 KC 17건**(CRCL 4 · COIN 4 · HOOD 3 · NBIS 3 · CRWV 3): 전건 `not_met` / `provisional`. 입력 지표가 대부분 분기 공시 대기(unconfirmed)여서 이격도를 산출할 피연산자가 없고, 파급 대상 5종목이 전원 미보유라 시나리오로 승격하지 않았다. **IREN·MU는 종목 전용 KC가 0건**이다.

---

## 2. 이번 회차의 두 축 — KC-1과 KC-9

### 2-1. KC-1: 4회 연속 경계 접촉, 그리고 2026-09-16 FOMC

- [fact] FFR 상단 3.75 대 임계 `> 3.75`. 부등호가 strict이므로 **동일값은 `not_met`**이다.
- [fact] 입력은 2026-07-29 FOMC 성명(웹검색 수집)이며 **staleness 45일**(직전 run 38일에서 확대). **`config/staleness.yaml`에 FFR 한도 자체가 없어**(FFR_prob 7일만 존재) 이 45일이 한도 초과인지 자동 판정되지 않는다.
- [fact] 2026-09-11 BLS 1차 공시(8월 CPI): 헤드라인 +0.4% MoM·**3.4% YoY(전월과 동일)**, 코어 +0.3% MoM·**2.4% YoY(2.5%에서 하락)**, 에너지 +2.1% MoM·**+16.3% YoY**, 휘발유 +3.9% MoM·**+27.4% YoY**. CPI는 어떤 KC의 판정 입력도 아니며 맥락으로만 기록한다.
- [fact] 인상 확률은 1차 표시값 기준 **66.4%**(centralbank.watch, 데이터 타임스탬프 2026-09-10). CPI 발표 직후 2차 매체가 인용한 69% 계열은 1차 표시값이 아니므로 채택하지 않았다(P4). 전 run의 58.6%는 '동결' 확률이라 직접 비교 불가 계열이다.
- **[fact] 현 판정은 `not_met`이며 확률·전망으로 met 취급하지 않는다(F1·P5).**

**조건부 시나리오 `sc_kc1_hike25` (사전 정의 KC-1에 연결, 새 트리거 아님)**

| 항목 | 내용 |
|---|---|
| 성립 조건 | [fact] 25bp 인상 **1회**로 상단 3.75 → **4.00**이 되어 `> 3.75` 성립. 중간 단계가 없다 |
| 사전 정의 consequence | `레버리지 전액 해제 + Edge/Next 50% 축소 검토` (config/kill_conditions.yaml 인용, 본 계층의 지시가 아님) |
| 파급 (현행 벡터) | CRWV·IREN·MU·NBIS **4종목**, 비중 범위 상단 **95.0** |
| 실효 범위 | [fact] 현 포지션에 레버리지가 없으므로 consequence 첫 항목은 실효가 없고 둘째 항목만 남는다 — Edge 해당 보유 종목은 IREN 1건, Next 3종목은 전원 미보유 |
| 반대 방향 | [fact] 동결·인하 시 이격도는 0.00pp에 머물거나 넓어진다 |
| 헤지 | [fact] RATES 축의 반대 부호 종목(CRCL·COIN·HOOD)이 전원 미보유라 **현 구성에서 자연 헤지는 작동하지 않는다** — 95.0이 상쇄 없이 남는다 |

### 2-2. KC-9: 가장 빠르게 좁아지는 KC인데 감시 경로가 없다 ⚠️최상위

- [fact] Brent **$109.51**(FRED, as_of 2026-09-09, stale 2/3 거래일) 대 임계 `≥ $120 · 1개월 지속`. 임계까지 **+9.58%($10.49)**, 임계 대비 **−8.74%**.
- [fact] 최근 **1개월 약 +19.3% 상승** 구간(중동 긴장)이며, 8월 CPI의 에너지·휘발유 항목이 같은 방향의 후행 확인이다.
- [fact] **`correlation_map.py`의 `KC_AXIS`에 KC-9 매핑이 없다** → KC 파급이 9건만 산출되고 KC-9는 누락.
- [fact] **`correlation_matrix.yaml`의 `axes`에 ENERGY 축 자체가 없다** → 축 집중도에서도 대상이 아니다.
- [fact] 그 결과 **7종목 전부의 KC 발췌본에서 KC-9가 빠졌고**, 이번 회차에 종목 계층이 이 KC를 감시할 경로가 존재하지 않았다.
- [inference/강도: 높음] 직전 run에서는 "먼 KC의 매핑 누락"이었으나 이번에는 **"가장 빠르게 좁아지는 KC의 매핑 누락"**으로 성격이 바뀌었다.

**ENERGY 축 신설 — 제안만 (config 자동 수정 금지)**

| 종목 | 노출 후보와 판단 근거 | 부호·강도 |
|---|---|---|
| IREN | [inference/중간] 전력 다소비 사업이라 원가 경로 개연성. 단 ERCOT 도매가는 주로 가스 연계라 브렌트와 간접이고, 전력 조달 구조(고정가·헤지)가 미공시. BTC 채굴 부문은 전력가 상승 시 해시레이트 감소로 반대 효과 가능 — **부문별로 부호가 갈릴 수 있음** | 확정 불가 |
| CRWV·NBIS | [inference/중간] 동일한 DC 전력비 경로. 전력 조달 구조가 카드·공시에 정량화돼 있지 않아 강도 근거 없음 | 확정 불가 |
| MU | [inference/중간] 전공정 에너지 집약도 + 물류비. 자체 현금흐름 위주 구조라 RATES가 L인 것과 유사하게 간접일 수 있음 | 확정 불가 |
| CRCL·COIN·HOOD | [inference/높음] 직접 노출 경로 미확인. 다만 **에너지 → 인플레이션 → 정책금리** 경로로 RATES 축을 경유한 간접 노출 성립 가능 | 확정 불가 |

> ⚠️ **이중 계상 경고** [inference/강도: 높음] — 이번 회차의 인과 경로 자체가 "에너지 → CPI → 정책금리"이며 **그 경로는 이미 RATES 축이 포착하고 있다.** 새 축이 포착해야 하는 것은 **금리를 경유하지 않는 직접 원가 경로(전력·물류)**여야 하며, 그렇게 정의하지 않으면 같은 위험이 두 축에서 두 번 계상돼 집중도 지표가 왜곡된다.
> **최소 조치**: KC_AXIS에 KC-9를 추가하려면 매핑할 축이 먼저 있어야 하므로 축 정의가 선행돼야 한다. 임시로는 `conditional_exposures`에 감시 목록으로 올리는 방법이 있다.

---

## 3. 시그널 등급 (전건 승계 — 본 계층은 변경·재해석하지 않는다, P13)

| 종목 | 등급 | 판정 | 섹터 | 티어 | 보유 | 상향 게이트 미충족 사유 |
|---|---|---|---|---|---|---|
| IREN | 🟡 | maintain | neocloud | Edge | **보유** | revenue_recognized 미충족. Sweetwater Batch Zero는 규칙2 명시 예외('분류 승인') → holding_reinforcement |
| NBIS | 🟡 | maintain | neocloud | — | 미보유 | Palantir 제휴 quantitative=false, stage=partnership_announced |
| CRWV | 🟡 | maintain | neocloud | — | 미보유 | 신규 공시 0건 재확인은 리서치 절차 사실, 매출·마진 수치 아님 |
| MU | 🟠 | maintain | memory | Base | 미보유 | 유일 방향성 재료(대만 노사분쟁)가 grade 4·confirmed=false 단독 |
| CRCL | 🔴 | maintain | stablecoin | Next | 미보유 | Tazapay는 P7 1단계(계약 존재) — revenue_recognized 미충족 |
| COIN | 🟠 | maintain | stablecoin | Next | 미보유 | 유일 claim이 '신규 8-K 0건' 부재 확인, 부재는 반증 아님(P5) |
| HOOD | 🟡 | maintain | stablecoin | Next | 미보유 | 8월 운영지표는 grade 1 확정 수치이나 매출 인식 아님 |

[fact] 상향 트리거 0건 · 하향 트리거 0건 · 🔴🔴 0건 · 7종목 전건 `human_confirmation_required=false`. 직전 run과 등급이 전건 동일하다.
[fact] 가장 가까운 사전 정의 게이트는 **MU의 2026-09-30 FY26 Q4 실적**(회사 공식 확정일, grade 1). 나머지는 전부 11월경이며 정확일이 1차 자료로 확정되지 않았다(F1).

---

## 4. 포지션과 집중도

**스냅샷** (positions.yaml as_of 2026-08-15, **staleness 28일 / 한도 30일 — 여유 2일**)

- 보유: **IREN (Edge) 0.85~0.95** + **현금 0.05~0.15** · 나머지 6종목 미보유 · 레버리지 미사용
- [fact] IREN은 8개 축 중 6개에 노출돼 있고, 파급 산출된 **9개 KC 전부**의 affected에 포함된다.

**집중도 경보: 발령** — 8개 축 중 **6개 초과**(AI_CAPEX·RATES·CRYPTO·GPU_SUPPLY·POWER_PERMIT·RISK_APPETITE), 관측 **95.0** 대 임계 **60**, 초과폭 35.0pp. **3회차 연속 동일한 값·동일한 축 목록.**

> **이진 축퇴 — 판별력 없음** [inference/강도: 높음]
> [fact] 현 구성에서 이 지표가 가질 수 있는 값은 **95.0(IREN 노출 축)과 0.0(비노출 축) 두 가지뿐**이며 중간값이 없다. 그 결과 ① 임계를 40으로 낮추든 80으로 올리든 같은 6개 축이 초과로 나오고, ② IREN 비중이 밴드 안 어디에 있든 값이 같으며, ③ 다른 종목이 소규모로 편입돼도 95.0이 크게 바뀌지 않는다.
> [fact] 남은 정보는 "어느 축에 노출이 있고 없는가"라는 이진 정보뿐이며, 그것도 `correlation_matrix.yaml`의 IREN 벡터를 되읽는 것이다.
> [fact] **미초과 2개 축(REGULATION·USDC_DISTRIBUTION_ECONOMICS)의 0.0은 위험 부재가 아니라 보유 부재의 결과다.**
> [fact] **이 상태를 감지할 수 있는 사전 정의 한도(single-name cap, 단일 종목 절대 한도)는 config 어디에도 없다 — 3회차 연속 미해소 부채**(esc_pf_2308_03). 임계 확정은 사람의 전속 사항이므로 수치를 제안하지 않는다(P11).

**이번 회차 신규 관측 2건**: ① 집중도 경보는 **정의된 8개 축에 대해서만** 발령된다 — 정의되지 않은 위험원(에너지)은 경보 대상이 아니다. ② `positions.yaml`·`correlation_matrix.yaml`의 as_of가 28일로 각각 한도(30일)에 2일 남았다 — 다음 회차에 이 경보 전체가 provisional로 강등될 수 있다.

**상관 레이어 요약** (05_correlation.json 승계, 수치형 계수 없음 — P14)
- 21쌍: 상 6 / 중 7 / 하 8. 상 등급 = COIN-CRCL, COIN-HOOD, CRCL-HOOD, CRWV-IREN, CRWV-NBIS, IREN-NBIS
- [fact] 보유 종목이 1종목이라 **보유 종목 간 쌍은 0쌍** — 쌍별 공유도는 현 실현 위험이 아니라 신규 편입 시의 구조적 중복 지표다
- [fact] IREN이 포함된 '상' 쌍은 2쌍(CRWV·NBIS)이며 공유 축이 RATES·AI_CAPEX·RISK_APPETITE·GPU_SUPPLY 4개로 동일하다
- [fact] 역노출은 RATES 축에 집중돼 있으나 반대 부호 종목이 전원 미보유라 **작동하지 않는다**
- [fact] 벡터 변경 제안 **0건** — 이번 회차 신규 Delta가 전부 크기 미공시이거나 grade 4 단독이라 근거 등급 미달(P4)
- [fact] **[CODE] 산출값이 직전 run과 완전히 동일**(21쌍·9건·8축) — 두 config가 as_of 2026-08-15로 불변이기 때문

---

## 5. 섹터 계층 소비 — "측정 불능"의 통합

| 섹터 | 상태 | 소비 결과 |
|---|---|---|
| neocloud | `not_interpretable_this_run` (**3회 연속**) | 축 13개 중 **12개 single_ticker**, Delta 14건 중 **11건이 null observation**. 섹터 방향 입력 **0건** |
| stablecoin | 축 9개 전부 single_ticker, **공유 축 0개** (3회 연속) | `dominant_factor = measurement_not_available`. 섹터 방향 입력 **0건** |
| memory | 단일 종목(MU) 뷰 | 방향 이동 축 1개(hbm_demand)이나 근거가 grade 4·confirmed=false 단독 → 방향 미소비 |

**오독 차단 (neocloud esc-1의 명시적 요구 준수)**
- [fact] `neocloud_aggregate.json`의 `customer_concentration` **dispersion='low'를 섹터 방향 일치로 소비하지 않았다.** L3는 이 중첩이 기전이 다른 두 사안(NBIS의 Palantir **채널형 제휴**, 6-K Ex-99.1 / CRWV의 **서비스 상품 출시**, 자사 보도자료·8-K 미제출)을 같은 축명에 합친 **거짓 중첩**일 가능성이 높다고 판정했다(AD-7).
- [inference/강도: 높음] 직전 2회차는 "비교 축 부재"였고 이번은 "비교 축은 생겼으나 그 중첩이 거짓일 가능성이 높음"이다 — **오독 위험이 오히려 커졌다.**
- [fact] `dispersion=single_ticker`를 '이견 없음'으로, 집계본의 `single_ticker_view=false`를 '종목 간 비교 수행됨'으로 읽지 않았다(후자는 산출물이 2개 이상 존재한다는 뜻일 뿐이다).

### 직전 결론의 수정 — "개별 실행 요인 지배"는 이번 회차에 철회·보류됐다

- [fact] 직전 run들(20260820·20260905)의 섹터 계층은 **'종목 간 실질 이견 0건 → 개별 실행 요인 지배'**를 유지했고, 본 계층은 그것을 섹터 방향 입력 부재의 설명으로 승계했다.
- [fact] 이번 회차에 **두 섹터가 동시에 그 결론을 철회·보류**했다 — stablecoin은 `measurement_not_available`로 바꾸며 직전 판정을 승계하지 않는다고 명시했고, neocloud는 "섹터 요인 지배와 개별 실행 요인 지배 **어느 쪽도 판정할 수 없다**"고 기록했다.
- [fact] 근거는 '이견 0건'이라는 값에 최소 **세 종류의 인공물**이 섞여 있다는 판정이다: **(a) 빈 창**(Delta 14건 중 11건 null) · **(b) 축 명명 불일치로 인한 중첩 유실**(IREN `margin_structure` ↔ CRWV `margin_trend`) · **(c) scope=sector 재료의 축 승격 방침 비대칭**(CLARITY 9/15를 CRCL은 축으로 올리고 COIN은 P6를 이유로 올리지 않음).
- **[fact] 따라서 본 계층은 이번 회차 서술에서 '개별 실행 요인 지배'를 사용하지 않는다.** 대신 '섹터 방향 입력 0건'이라는 사실만 유지하고, 그 원인을 요인 귀속이 아니라 **측정 불능**으로 기록한다(P5).
- [inference/강도: 높음] **실무적 함의** — 직전까지는 "종목별 개별 요인이 지배적이므로 섹터 단위 리밸런싱 트리거가 불필요하다"는 읽기가 성립했으나, 이번 판정 아래에서 **그 읽기는 근거를 잃는다.** 섹터 요인의 존재가 부정된 것이 아니라 **미검증 상태로 되돌아갔기** 때문이다.
- [fact] 해소 조건: ① `coverage.yaml`의 common_axes와 카드 축 키 사이의 매핑 테이블 + null observation 제외 규칙, ② scope=sector 재료의 축 승격 통일 규칙. 둘 다 config·카드 영역이므로 **제안만** 했다.

---

## 6. 시나리오 요약

- **총 14건** — 매크로 KC 연결 11건(KC-1~10 + KC-1 조건부 분기) + config 한도 연결 3건. **섹터 방향 연결 0건 · 종목 KC 연결 0건.**
- [fact] 본 계층이 **새로 만든 트리거·임계는 0건**이며 전부 사전 정의된 KC 또는 config 한도에 `source`로 연결됐다(P11).
- 이격도 산출 가능 12건 / 불가 2건(`sc_kc10` 이벤트형·분모 미공시, `sc_limit_positions_band` 범위만 기입되는 설계) / **파급 산출 불가 1건**(`sc_kc9`).
- config 한도 연결 3건: 축 집중도 임계(60), 포지션 밴드, **신선도 한도(Positions·CorrelationView 각 30일, 현재 28일)**.

**이격도 변화**
- 좁아짐: **KC-9(최대 폭)**, KC-2(15.47p→14.16p), KC-3 BTC(−31.10%→−28.80%)·VIX(10.47p→9.16p)
- 넓어짐: KC-5 두 레그(0.69p→2.03p, 2.79p→3.12p), KC-6(38.0p→41.2p)
- 불변: **KC-1(0.00pp, 입력도 미갱신)**, KC-7·KC-8(입력 재사용)

---

## 7. ThesisPatch — 3건 생성·승인 큐 등재

[fact] 이번 run 지시로 대상 카드 **전문**을 읽고(CRCL 84행 · HOOD 67행 · IREN 134행) 패치를 생성했다(F20). `state/thesis_cards/`에 직접 쓰지 않았고 `requires_human_approval: true` 고정이다(F17).

| 승인 ID | 종목 | 필드 / 동작 | 내용 | counts |
|---|---|---|---|---|
| `ap_20260912_1738_thesis_patch_crcl` | CRCL | `axes` / amend | **diversification** 축이 ARC·CPN만 열거해 M&A 채널이 축 밖에 있었다 → Tazapay 확정계약(2026-09-08 8-K, grade 1, $400M 상당 전액 Circle Class A 주식, 규제승인·최대 15개월 종결 조건부) 병기. **P7 1단계(계약 존재)임을 라벨에 고정** | axes=8 불변 |
| `ap_20260912_1738_thesis_patch_hood` | HOOD | `key_metrics` / amend | 연속 3행(AUA·ARPU·크립토 매출 비중) 치환, 중간 ARPU 원문 유지. **AUA**: Total Platform Assets $383.7B(MoM +8%·YoY +26%), 순입금 $4.0B(TTM $74.1B), 펀드고객 28.6M. **크립토**: 명목거래액 $17.5B(MoM +61%·YoY −38%) + 가스비 보조금(9/29 종료 예정) 캐비어트 | key_metrics=7 불변 |
| `ap_20260912_1738_thesis_patch_iren` | IREN | `axes` / annotate | **power_permit** 축에 2026-09-08 관측점 병기 — 2GW Sweetwater Hub 전량 ERCOT Batch Zero **Base Load 조건부 포함**. ⚠️**조건부이며 최종 접속 승인 아님**, **SB6 커테일먼트와 별개 규제 트랙**이라 KC-10 첫 조건의 분모 공백 미해소, Abbott 지시 ERCOT 감사 미종료를 라벨 본문에 명시 | axes=6 불변 |

- [fact] 3건 전부 `reverses_core_thesis=false` — 축 신설·분해나 thesis 본문 재작성을 포함하지 않는다. 전부 기존 필드의 관측 기준선 기입 또는 관측 범위 명시다.
- [fact] 적용 전 **dry-run**으로 contains·not_contains·counts·YAML 파싱을 사전 검증했다(미리보기: `07_thesis_patch/{TICKER}_dryrun_merged_preview.yaml`). `not_contains`는 P9 보존 주석에 나타나지 않는 형태로 작성했다(2026-08-16 자동 원복 사고 유형 회피).
- **패치 미생성**: **NBIS Palantir 제휴** — 정량 수치 전무(달러·MW·GPU 수량·계약기간·최소구매약정 전부 부재)로 패치 부적격, L2도 후보 없음 판정 / **HOOD rates_income** — Margin Book $21.5B(+72% YoY) 대 증권대차수익 $36M(−32% YoY)의 방향 혼재로 arbiter가 단독 판정 근거 불가 판정 / **CRCL key_metrics 다각화 진척** — 종결·매출 기여 수치 부재.
- ⚠️ **대기 14일 초과 시 `expired`** (2026-08-20 run의 NBIS 패치 3건이 실제로 만료된 선례 있음).

---

## 8. 에스컬레이션 (12건 — 최상위 2 / 높음 5 / 보통 4 / 해소 1)

| ID | 우선 | 상태 | 요지 |
|---|---|---|---|
| **esc_pf_2308_02** | **최상위** | 이월·격상 | **KC-9 매핑 부재** — KC_AXIS에 KC-9 없음 + axes에 ENERGY 축 없음. 가장 빠르게 좁아지는 KC가 파급·집중도 양쪽에서 미산출. ENERGY 축 신설 제안(부호 미확정·RATES 이중 계상 경고 포함) |
| **esc_pf_2308_07** | **최상위** | 이월·격상 | **축 명명·정의·분해 표준 부재** — 이번 회차 양방향 실증: 중첩 유실(`margin_structure`↔`margin_trend`) + 거짓 중첩(`customer_concentration`, AD-7). 분해 단위 불일치·축 승격 방침 비대칭 포함. L3 4건 병합 |
| esc_pf_2308_01 | 높음 | 이월·악화 | **KC-1 0.00pp 4회 연속 + staleness 45일 + `staleness.yaml`에 FFR 한도 미정의** → KC-1 신선도가 산출되지 않음. FOMC 결과와 무관하게 FFR 갱신 필요 |
| esc_pf_2308_03 | 높음 | 이월·3회 연속 | **집중도 이진 축퇴 + single-name cap 미정의** — 임계 60의 판별력 부재. 임계 수치는 제안하지 않음(P11) |
| esc_pf_2308_04 | 높음 | L3 승계 | **CRWV $8.5B DDTL 4.0**(2026-03-31, A3/DBRS A(low), 투자적격 GPU 담보) 이력 공백 — 과거 CRWV run 3회 어디에도 Claim 부재. `funding_access` 기준선이 Ba2/BB+로 낮게 설정됐을 가능성 / `leverage_coverage`는 성격이 다름(서사·귀속 누락) |
| esc_pf_2308_06 | 높음 | 이월·3회 연속 | **KC-MU-\* 미정의 + 2026-09-30 FY26 Q4 실적 직전** — MU 축 6개 중 4개의 관측 창이 그 단일 이벤트로 수렴. **임계값은 제시하지 않고** 임계가 필요한 관측 항목 후보만 나열(비트그로스·ASP 분해 / SCA 커버리지·선수금 / HBM 캐파·믹스 / 대만 가동 연속성 / Netlist 구제수단) |
| esc_pf_2308_08 | 높음 | 이월·악화 | **섹터 컨센서스 3회 연속 측정 불능** — 상위 계층 소비 규칙 통지. '개별 실행 요인 지배' 결론 철회·보류 |
| esc_pf_2308_05 | 보통 | L3 승계 | **Netlist 관측 채널 3개 전부 실패** — EDGAR 0건 / CDCA 도켓 오식별(1:26-cv-00362는 Avnet 포함 E.D.Tex 이송 별건) / ITC는 Samsung 337-TA-1511 혼입 의심. 2026-09-10 답변시한 결과 미확인. **`sources.yaml`에 usitc.gov 등재 검토 제안** |
| esc_pf_2308_10 | 보통 | 이월 | **config·문서 결함 묶음** — `coverage.yaml` IREN(20-F/6-K)·NBIS(10-K/10-Q/8-K) edgar_forms 오기 / `correlation_matrix.yaml` as_of 정체·벡터 제안 미반영 / `company-crcl.md` '8/18 실적 임박' stale / **arbiter `gate_check` 필드명 불일치**(COIN·CRWV는 `quantitative`/`met`, 나머지는 `quantitative_evidence`/`result` — validator가 후자를 조회하므로 상향 발생 시 게이트 검증이 비활성화될 수 있음) / congress.gov 403·1차 도메인 미등재 |
| esc_pf_2308_11 | 보통 | 이월 | **KC-4 ON RRP 단위 정합** — $5.255B 대 임계 $200B, 약 38배 격차. 정합 확인 전까지 이격도를 액면대로 읽을 수 없음 |
| esc_pf_2308_12 | 보통 | 신규 | ThesisPatch 3건 승인 큐 등재 — 14일 만료 규칙 적용 대상 |
| **esc_pf_2308_09** | 기록만 | **해소** | **MU `ip_litigation_risk` 축 상충 — L2가 옳다.** 오케스트레이터가 `state/thesis_cards/MU.yaml`을 직접 확인한 결과 축이 실재하며 MU 카드 축은 **6개**다(2026-09-05 승인 적용분). arbiter 진술은 P17 격리로 카드를 보지 못해 직전 run 시점 서술을 승계한 **stale**이며 **결함이 아니라 격리 설계의 정상 동작**이다. [inference/중간] 다만 카드 승인·적용 시 arbiter 참조 축 목록이 함께 갱신되지 않으면 같은 상충이 재발할 수 있으며, 이 관찰은 esc_pf_2308_07 범위 안에 있다 |

---

## 9. 한계

- **P12** 게이트 미충족은 실패가 아니라 정상 경로다.
- **P13** 하위 계층 산출물을 소급 수정하지 않았고, 섹터 컨센서스·KC·상관을 개별 종목 시그널 근거로 인용하지 않았다.
- **P14** 수치형 상관계수를 산출하지 않았다 — 공유도는 등급(상·중·하) + 공유 축 + 근거로만 기술했다.
- **P15** 행동 지시 동사, 목표 비중 단일값, 시점 지시를 포함하지 않았다. `predefined_consequence`는 config에 사전 정의된 문구의 인용이다.
- **P16** 입력별 staleness — positions·correlation_matrix 28일(한도 30, 여유 2일) / FFR 45일(**한도 미정의**) / KC-7·8 입력 74일(FCF 한도 100 이내) / brent 2 거래일(한도 3).
- **P17** 02_company 원문·`_raw_*`·폐기본 `_COIN_corrupted_backup.json`을 열지 않았다. thesis card는 F20 의무에 따라 CRCL·HOOD·IREN 3건만 전문 열람했고 편집하지 않았다.
- **벡터 의존** 상관·집중도의 정확성 상한은 사람이 편집하는 `correlation_matrix.yaml`이다. 미해소 벡터 부채 5건 + 축 집합의 ENERGY 결손이 남아 있다.
- **이번 회차 산출 불가 항목 5가지** — ① KC-9 파급(축 매핑 부재) ② KC-10 이격도(이벤트형·분모 미공시) ③ 종목 KC 17건 이격도(입력 unconfirmed) ④ 실제 포지션 밴드 이탈 여부(범위만 기입되는 설계) ⑤ 섹터 방향(3개 섹터 전부). **판정 실패가 아니라 측정 수단 부재**이며 각각 escalation 또는 시나리오 note에 기록했다.

---

*검증: `validate_output.py --layer correlation / portfolio / thesis_patch` 전건 PASS (2026-09-12).*
