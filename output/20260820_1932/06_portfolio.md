# 포트폴리오 뷰 — run 20260820_1932 (L4 / cio-portfolio)

- **as_of:** 2026-08-20T20:15+09:00 · staleness_days 0 · reused_from null
- **기본 판정:** `default_action = no_action`
- **🔴🔴 판정:** 없음 (human_confirmation_required=false, blocking=false)
- **입력(P17):** `04_sector/{memory,neocloud,stablecoin}.json` · `01_macro_kc.json` · `05_correlation.json` · `config/correlation_matrix.yaml` · `config/positions.yaml`
- **미로드:** `02_company/*` 원문 · `03_signal/*` 원문 · thesis card · `config/kill_conditions.yaml` · `config/coverage.yaml`

> [fact] 본 문서는 시나리오·사전 정의 한도·이격도만 기술한다. 행동 지시 동사, 목표 비중 단일값, 시점 지시를 포함하지 않는다(P15·F18). 포지션 행동은 사람의 결정이다(§9).

---

## 1. 기본 판정 근거 (P12)

| # | 사유 |
|---|---|
| 1 | [fact] 매크로 KC-1~10 전건 `not_met`, 그중 6건(KC-1·6·7·8·9·10) `provisional` — not_met은 확정이 아니다(F7) |
| 2 | [fact] 🔴🔴(KC met AND confirmed) 판정이 어느 계층에도 없다 |
| 3 | [fact] 시그널 후보 7종목 전건 등급 유지로 이관 — IREN 🟡 / NBIS 🟡 / CRWV 🟡 / MU 🟠 / CRCL 🔴 / COIN 🟠 / HOOD 🟡 (본 계층은 재해석하지 않는다, P13) |
| 4 | [fact] 3개 섹터 전부 섹터 방향 컨센서스 산출 불가 — §2 참조 |
| 5 | [fact] 관측된 유일한 사전 정의 한도 초과는 축 집중도이며, 임계(60)는 config 주석상 「⚠️초안」이고 지표가 단일 포지션으로 축퇴한 상태 |

[fact] 게이트 미충족은 실패가 아니라 정상 경로다(CLAUDE.md §7).

---

## 2. L3 에스컬레이션 소비 기록

### 2-1. neocloud — `sector_direction_computable = false` (esc-1, 명시적 소비)

- [fact] `coverage_count >= 2`인 축이 **0개**, 4개 축 전부 `dispersion = single_ticker`. Delta 기여 종목은 IREN·NBIS 2사이고 CRWV는 신규 1차 공시 0건으로 Delta 0건.
- [fact] 방향 일치도·분산은 **산출 대상 없음** — 「3사 일치」와도 「갈림」과도 다른 제3의 상태다.
- [fact] 본 계층은 이 파일에서 어떤 섹터 방향도 읽지 않았고, **어떤 시나리오도 neocloud 섹터 방향에 연결하지 않았다.**
- [fact] CRWV의 Delta 0건을 안정으로 읽지 않았다 — 관측 부재다(P5).
- [fact] 승계 이관 항목: 자본조달 구조의 공통·특이 판정 `not_determined_this_run`(esc-3), 3사 정의 표준 부재(esc-4).

### 2-2. stablecoin — `esc_1932_02` 제로섬 역노출 규모 프록시 최초 확보

- [fact] `05_correlation.json` → `inverse_exposure_review[iex_usdc_distribution_economics]`에 반영. CRCL·COIN 쌍의 `USDC_DISTRIBUTION_ECONOMICS` 축 표기를 **「공유 축·부호 반대」**로 갱신했다.
- [fact] 규모 프록시(발행자 측 단면): Coinbase 귀속 유통비용 3개월 **$324.6M**(Q2'25 $332.3M, −2.3% YoY) / 6개월 **$655.3M**(Q2'25 $635.5M, +3.1% YoY). 도출 분기 계열 Q1'26 약 $330.7M → Q2'26 $324.6M.
- [fact] **이번 window 부호 미확정** — 3개월 기준과 6개월 누적 기준의 부호가 반대다. 분배자(COIN) 측 수취 절대액은 미공시.
- [fact] CRCL·COIN 모두 `weight_range [0.0, 0.0]` — 이 부호 반대 관계는 현 포지션에 **실효 상쇄를 만들지 않는다**(구조 관측).
- [fact] 오독 차단: CRCL `reserve_income` strengthen과 COIN `usdc_economics` neutral을 두 종목 이해의 일치로 읽지 않았다. stablecoin 역시 4개 축 전부 coverage 1이며 섹터 공통 축 커버리지는 금리 1/3·규제 1/3·크립토 사이클 0/3이다.

### 2-3. memory — `single_ticker_view = true` / `dispersion_computed = false`

- [fact] 커버 종목 MU 1건, Delta 존재 축은 `china_supply` 1개(neutral, 근거 grade4·confirmed=false). 나머지 4축은 관측 부재이며 중립 관측이 아니다(P5). 어떤 축도 「low(전원 일치)」로 해석하지 않았다.
- [fact] 승계: `ip_litigation_risk` 신규 축 제안 계류(`escalation_pending_human_decision`), MU 종목 전용 KC 부재(arbiter 플래그).

### 2-4. 종합

[inference/강도: 높음] 3개 섹터 전부 섹터 방향 컨센서스가 산출되지 않았으므로, 이번 회차 시나리오는 **전부 사전 정의 매크로 KC와 config 한도에만 연결**된다 — 섹터 판정을 트리거로 삼은 시나리오는 **0건**이다.

---

## 3. 포지션 스냅샷 (`positions.yaml` as_of 2026-08-15, staleness 5일)

| 종목 | tier | weight_range | 비고 |
|---|---|---|---|
| IREN | Edge | [0.85, 0.95] | [fact] 기입 90% ±5%p |
| 현금 | — | [0.05, 0.15] | [fact] 기입 10% |
| MU | Base | [0.0, 0.0] | 미보유 |
| NBIS / CRWV | null | [0.0, 0.0] | 미보유 |
| CRCL / COIN / HOOD | Next | [0.0, 0.0] | 미보유 |

[fact] 비중 상단이 0을 넘는 종목이 IREN 1개이므로 축 집중도·KC 파급의 비중 지표가 전부 95.0으로 동일 산출된다. [inference/강도: 높음] 이번 회차 구별 정보를 담는 것은 비중 합계가 아니라 **노출 종목 수와 KC별 이격도**다.

---

## 4. 리밸런싱 시나리오 (12건 — 전건 사전 정의 KC·한도 연결, P11)

| # | 트리거 | 연결 | 현재 판정 | 이격도 | 파급(노출 종목) |
|---|---|---|---|---|---|
| sc_kc1 | FFR > 3.75 | KC-1 | not_met / provisional | **0.00pp — 경계 접촉** | RATES −: CRWV·IREN·MU·NBIS (4) |
| sc_kc2 | VIX ≥ 30 | KC-2 | not_met / confirmed | 14.84p (15.16 → 30, 약 1.98배) | RISK_APPETITE +: 6종목 |
| sc_kc3 | BTC < 55,000 **AND** VIX ≥ 25 | KC-3 | not_met / confirmed | BTC −23.43% / VIX 9.84p (AND) | CRYPTO +: COIN·CRCL·HOOD·IREN (4) |
| sc_kc4 | ON RRP ≥ $200B **AND** VIX ≥ 25 | KC-4 | not_met / confirmed | 임계의 약 0.16%(약 631배 필요) / VIX 9.84p | RISK_APPETITE +: 6종목 |
| sc_kc5 | TAIEX 20dma < 0 **AND** 1개월 < 0 | KC-5 | not_met / confirmed | 2.10p / **0.24p**(AND) | RISK_APPETITE +: 6종목 |
| sc_kc6 | SDLLMTK ≤ −30% (2주 지속) | KC-6 | not_met / provisional | 31.9p (+1.9% → −30%) | AI_CAPEX +: CRWV·IREN·MU·NBIS (4) |
| sc_kc7 | 하이퍼스케일러 합산 FCF < 0 (2분기) | KC-7 | not_met / provisional | **산출 불가** (value=null, unconfirmed) | AI_CAPEX +: 4종목 |
| sc_kc8 | Microsoft FCF < 0 | KC-8 | not_met / provisional | **산출 불가** (value=null, unconfirmed) | AI_CAPEX +: 4종목 |
| sc_kc9 | Brent ≥ 120 (1개월 지속) | KC-9 | not_met / provisional | 24.71p (95.29 → 120, 약 +25.9%) | **축 매핑 부재 — 파급 미산출** |
| sc_kc10 | IREN 계약 용량 10%+ 강제 감축 분류 또는 전력접속·인허가 취소·보류 공시 | KC-10 | not_met / provisional | **정의 불가**(이벤트형) | POWER_PERMIT −: IREN (1) |
| sc_axis_concentration | 축별 비중 상단 합 > 60 | `correlation_matrix.yaml` `concentration_threshold_pct` | **초과 — 8축 중 6축** | +35.0pp (95.0 대 60) | IREN |
| sc_position_band | IREN 비중이 [0.85, 0.95] 밖 또는 현금이 [0.05, 0.15] 밖으로 관측 | `positions.yaml` weight_range | 범위 내 | 상단·하한까지 각 5pp | IREN |

**요약** — 12건 / KC 연결 10건(KC-1~10 전건) / config 한도 연결 2건 / **섹터 방향 연결 0건** / 종목 전용 KC 연결 0건(P17상 `kill_conditions.yaml` 미로드).
**이격도 산출 가능 8건, 불가 4건**(KC-7·8 지표 미수집, KC-10 이벤트형, KC-9 파급 미산출).
**가장 좁은 이격도** — ① KC-1 FFR 0.00pp(단 staleness 22일·웹검색·provisional) ② KC-5 1개월 수익률 레그 0.24p ③ KC-5 20dma 레그 2.10p.

[fact] `predefined_consequence`는 `kill_conditions.yaml`에 사전 정의된 문구의 인용이며 본 계층의 지시가 아니다 — 상세는 `06_portfolio.json`의 각 시나리오 필드 참조.
[fact] KC-3은 사전 정의 consequence의 파급 대상(IREN·COIN·HOOD·CRCL)과 [CODE] 산출 `affected`가 정확히 일치하는 유일한 KC다. 파급 4종목 중 실제 보유는 IREN 1종목이다.

---

## 5. 축 집중도 경보 (절차 3 — 필수 포함)

**발령.** 임계 60 대 관측 95.0 → **+35.0pp 초과**, 8개 축 중 6개 축.

- **초과 축:** AI_CAPEX · RATES · CRYPTO · GPU_SUPPLY · POWER_PERMIT · RISK_APPETITE
- **미초과 축:** REGULATION 0.0 · USDC_DISTRIBUTION_ECONOMICS 0.0 — [fact] 노출 종목(COIN·CRCL·HOOD)이 전원 미보유여서 0.0이다. **위험 부재가 아니라 보유 부재의 결과**다.
- [fact] 6개 축 전부의 초과가 IREN 단일 포지션(상단 0.95)에서 발생한다 — 초과 축 수는 IREN이 노출된 축의 수와 같다.
- [inference/강도: 높음] 지표가 「IREN이 그 축에 노출되어 있는가」의 **이진 지표로 축퇴**했다. 6축 동시 초과를 6개의 독립 집중 위험으로 읽으면 오독이다.
- [fact] 종목 수 기준 상대 판정 병기 — RATES 7 / RISK_APPETITE 6 / AI_CAPEX·CRYPTO 각 4 / REGULATION·GPU_SUPPLY 각 3 / USDC_DISTRIBUTION_ECONOMICS 2 / POWER_PERMIT 1.
- [fact] 임계 60은 config 주석상 「⚠️초안」이며 임계 확정은 사람 몫이다.

---

## 6. 상관 레이어 갱신 (`05_correlation.json`)

[fact] `coefficient_used = false` — 수치형 상관계수 미산출. 등급(상·중·하) + 공유 축 + 근거만(P14).

- **21쌍** 산출. **「상」 등급 6쌍** — COIN·CRCL / COIN·HOOD / CRCL·HOOD / CRWV·IREN / CRWV·NBIS / IREN·NBIS.
- [fact] IREN이 「상」을 이루는 쌍은 CRWV·IREN, IREN·NBIS 2건이며 공유 축은 양쪽 모두 RISK_APPETITE·RATES·AI_CAPEX·GPU_SUPPLY 4축으로 동일하다.
- [inference/강도: 높음] 보유 종목이 1개이므로 21쌍 중 보유·보유 쌍은 0건이다 — 쌍별 공유도는 **실현된 동조 위험이 아니라 신규 후보 편입 시의 구조적 중첩 후보**를 보여준다.

### 6-1. 역노출 갱신

| 항목 | 갱신 |
|---|---|
| `USDC_DISTRIBUTION_ECONOMICS` (CRCL·COIN) | **updated** — 「자연 헤지」→ **「공유 축·부호 반대(제로섬 이전)」** 표기 갱신. 쌍 등급 「상」은 RATES·CRYPTO·REGULATION 3축의 같은 부호 노출에서 나온 값이므로, 부호 반대 1축으로 쌍 전체를 상쇄 관계로 읽지 않는다. 이번 window 부호 미확정, 규모는 발행자 측 단면만 정량화. |
| `OUSD_CONSORTIUM` (조건부) | **not_updated** — 부호 미확정 유지, [CODE] 집계 미포함 확인. 관측 시각 비대칭 해소로 잔존 비대칭(CRCL 단방향 위협 대 COIN 양면 노출)이 구조적임이 확인. **신규 감시 단서** — grade4 단독 「조건 확장」 보도가 사실이라면 두 역노출 항목의 독립성 가정이 무너진다(판정 미반영, P4). |
| `YIELD_BEARING_STABLECOIN_CLAUSE` (조건부) | **not_updated** — 신규 근거 전무. 2026-08-17 재무부 GENIUS 제3조 이행 NPRM은 **별개 트랙**이며 이자 조항 문언을 다루지 않아 갱신 근거로 사용하지 않았다(P5). 재판정 트리거 2026-09-15 유지. |
| RATES 축 부호 반대 쌍 | 스크립트 산출 그대로 유지(CRCL·CRWV는 헤지 강도 「상」). [fact] 상대 종목이 전원 미보유이므로 현 포지션에서 실현되는 상쇄는 없다. |

### 6-2. 벡터 변경 제안 (`vector_change_proposals` — 제안만, 자동 반영 금지)

| ID | 대상 | 유형 | 부호·강도 |
|---|---|---|---|
| vcp_..._01 | CRCL·COIN `USDC_DISTRIBUTION_ECONOMICS` basis | basis 갱신만 | 부호·강도 **변경 없음** — basis의 「크기 정량화 불가」 서술이 부정확해졌으나, 부호가 구간 의존이고 분배자 측 미공시·8-K 기한(2026-08-24) 미경과로 강도 상향 부적격 |
| vcp_..._02 | NBIS `RATES` | 이월 항목(−H 재검토)에 근거 첨부 | **변경 없음** — 상향 반대 근거(2030년물 $3.0B 쿠폰 0.50%·프리미엄 +40.0%, 익일 업사이즈)와 찬성 근거(전환사채 원금 합계 $10,041.8M + 신규 $5.0B + 리스 $1,625.3M + ABL SOFR+2.50%) 병존, 결제 미완(P7 1단계) |
| vcp_..._03 | IREN `CRYPTO` | 예약 상태 보고 | **변경 없음** — 8/27 재평가 예약 미도래, 매출 믹스 자료 부재(P5) |
| vcp_..._04 | CRWV `AI_CAPEX` basis | 「⚠️갱신 대상」 미해소 통지 | **변경 없음** — CRWV 신규 1차 공시 0건으로 갱신 근거 부재 |
| vcp_..._05 | 신규 축 후보 `ip_litigation_risk`(MU) | 카드 결정 이후로 유보 | **제안 없음** — 카드 축 결정 전 벡터 선반영 시 축 체계 불일치. 신설되어도 MU 단독·비중 0.0으로 쌍 공유도 기여 0, 집중도 기여 0.0% |
| vcp_..._06 | `conditional_exposures.OUSD_CONSORTIUM.status` | 감시 단서 1행 추가 | 부호 미확정 유지 |

[fact] 벡터 미해소 예약 3건이 잔존한다 — IREN CRYPTO 8/27 재평가, NBIS RATES −H 재검토 이월, CRWV AI_CAPEX basis ⚠️갱신 대상.
[fact] vcp_..._01의 근거에는 섹터 산출물이 Claim ID를 병기하지 않았다 — P17상 본 계층은 보완할 수 없으므로 승인 전 사람이 CRCL 02_company 산출물의 Claim ID를 대조할 필요가 있다.

---

## 7. ThesisPatch 후보 (4건 — 후보 식별까지, 패치 파일 미생성)

| 종목 | 카드 항목 | 성격 |
|---|---|---|
| **NBIS** | 전환사채 총액 가정 | [fact] 카드가 2026년 3월 발행분 부분치 $4,337.5M 사용 대 실제 원금 합계 $10,041.8M(6개 시리즈, grade1) — 약 2.3배 과소 계상. [inference/강도: 중간] `correlation_matrix.yaml` NBIS RATES basis의 「3사 중 민감도 최저」 상대 판단 전제와 인접 — 벡터 basis와 함께 검토 필요. 목록형 필드 → `expected_after.counts` 필수 |
| **IREN** | 완전희석 주수 | [fact] 495M 대 508M 출처 충돌·방법론 미특정(if-converted 대 treasury-stock). range + 방법론 명기 유형. 신규 희석 발생 아님(측정 불확실성) |
| **CRWV** | 이자 커버리지 정의 / CapEx 정합 | [fact] ~2.2x의 분자·분모·기간 기준 미명시, Q2 CapEx $9.4B(CFO) 대 $6,422M(GAAP) 약 $3.0B 불일치. [inference/강도: 중간] CRWV RATES −H basis의 근거 수치 자체 — 정의 확정 시 벡터 basis도 갱신 대상. 단 이번 회차 신규 근거 0건 |
| **MU** | 축 목록(`ip_litigation_risk` 추가) | [fact] 사람 판단 계류(`escalation_pending_human_decision`). 본 계층은 축 신설을 제안하지 않는다. 목록형 필드 → `expected_after.counts` 필수 |

**패치 미생성 사유** — [fact] F20은 before→after 생성 전 카드 **전문 정독**을 요구한다. [fact] `state/thesis_cards/*`는 cio-portfolio의 P17 허용 목록에 없고 이번 run 지시에도 포함되지 않았다. [inference/강도: 높음] 전문 미독 상태의 before→after 생성은 F20 위반(절단된 관측 → 없는 결손 생성)이므로 `refine thesis <TICKER>` 경로로 이관한다. [fact] ThesisPatch는 `requires_human_approval: true` 고정이며 승인 없는 카드 쓰기는 금지된다(F17).
**순서 제약** — [fact] neocloud esc-4: 개별 카드 수정만으로는 3사 정의가 서로 다른 기준으로 확정될 수 있어 **섹터 층위 일관 기준 결정이 선행**되는 편이 낫다. 위 NBIS·IREN·CRWV 3건은 동일 유형(정량 지표 정의 공백)이다.

---

## 8. 에스컬레이션 (6건 — 전건 비차단)

| ID | 유형 | 내용 |
|---|---|---|
| esc_pf_1932_01 | L1 입력 검증 | KC-4 ON RRP 단위 정합 확인 요청 — value 317,000,000 대 threshold 200,000,000,000(약 631배). [inference/강도: 중간] 달러 대 백만달러 혼재 가능성. 본 계층은 L1을 소급 수정하지 않는다(P13). 미확인 상태에서 넓은 이격도를 안전 여유로 해석 불가 |
| esc_pf_1932_02 | KC 임계 경계 | KC-1 이격도 0.00pp 경계 접촉 + staleness 22일 — 가장 좁은 이격도가 동시에 가장 오래된 근거다 |
| esc_pf_1932_03 | 스크립트·config 결손 | `KC_AXIS`에 KC-9 미매핑(매크로 10건 중 파급 9건만 산출) / 종목 전용 KC(KC-NBIS-3·KC-CRWV-3·KC-CRCL-3·KC-COIN-4)·IREN 전용 KC 미정의·MU 전용 KC 부재는 P17상 미로드로 이격도 미산출 |
| esc_pf_1932_04 | 지표 축퇴 | 축 집중도 6축·KC 파급 9건 전건 95.0 — 임계 60의 판별력 부재. 임계 확정은 사람 몫(U4 계열 잔여 부채) |
| esc_pf_1932_05 | L3 승계 | neocloud esc-2(AD-1~3 스크립트 잔여 왜곡)·esc-3(자본조달 귀속 판정)·esc-4(정의 표준)·esc-5(coverage.yaml), stablecoin esc_1932_01(`sources.yaml`에 home.treasury.gov 미등재 → 정부 1차 공시 계통적 등급 과소평가)·esc_1932_03(HOOD 2026-07-29 실적콜 발언 과거 run 미포착), memory의 축 신설 결정·MU 전용 KC 부재 |
| esc_pf_1932_06 | ThesisPatch 이관 | 후보 4건 식별, 패치 생성은 `refine thesis` 경로 |

---

## 9. 한계

- [fact] **P13** — 하위 산출물(시그널 등급·섹터 판정)을 소급 수정하지 않았고, 섹터 컨센서스·KC·상관을 개별 종목 시그널 근거로 인용하지 않았다.
- [fact] **P14** — 수치형 상관계수 미산출.
- [fact] **P15** — 행동 지시 동사·목표 비중 단일값·시점 지시 미포함. `predefined_consequence`는 config 사전 정의 문구의 인용이다.
- [fact] **P16** — `positions.yaml`·`correlation_matrix.yaml` 모두 as_of 2026-08-15(staleness 5일). 벡터 갱신은 승인 경로로만 가능하다.
- [fact] **벡터 의존** — 상관·집중도는 사람이 편집한 `correlation_matrix.yaml`에 의존하므로 벡터의 정확성이 이 레이어의 정확성 상한이다.

> 본 상관은 구조적 노출 판정이며 실제 가격 동조화를 예측하지 않는다. 축 노출이 낮아도 유동성 이벤트에서 동반 하락할 수 있다. 노출 벡터는 사람이 편집한 correlation_matrix.yaml에 의존하므로, 벡터의 정확성이 곧 이 레이어의 정확성 상한이다.

---
**검증** — `validate_output.py --layer correlation` PASS · `--layer portfolio` PASS
