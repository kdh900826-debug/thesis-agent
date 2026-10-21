# 포트폴리오 뷰 — run 20260905_0618 (L4 / cio-portfolio)

- **as_of:** 2026-09-05T07:05+09:00 · staleness_days 0 · reused_from null
- **기본 판정:** `default_action = no_action`
- **🔴🔴 판정:** 없음 (human_confirmation_required=false, blocking=false)
- **입력(P17):** `04_sector/{memory,neocloud,stablecoin}.json` + 각 `*_aggregate.json` · `01_macro_kc.json` · `03_signal/*.json`(등급·게이트·kill_check 필드만) · `05_correlation.json` · `config/correlation_matrix.yaml` · `config/positions.yaml`
- **미로드:** `02_company/*` 원문 · `_raw_edgar_*` · `_raw_websearch_*` · thesis card 원문 · `config/kill_conditions.yaml` · `config/coverage.yaml` · 승인 큐

> [fact] 본 문서는 시나리오·사전 정의 한도·이격도만 기술한다. 행동 지시 동사, 목표 비중 단일값, 시점 지시를 포함하지 않는다(P15·F18). 포지션 행동은 사람의 결정이다(§9).

---

## 1. 기본 판정 근거 (P12)

| # | 사유 |
|---|---|
| 1 | [fact] 매크로 KC-1~10 **전건 `not_met`** — confirmed 4건(KC-2·3·4·5) / provisional 6건(KC-1·6·7·8·9·10). not_met은 확정이 아니다(F7) |
| 2 | [fact] 🔴🔴(KC met AND confirmed) 판정이 어느 계층에도 없다 |
| 3 | [fact] 시그널 후보 7종목 **전건 등급 유지**로 이관 — IREN 🟡 / NBIS 🟡 / CRWV 🟡 / MU 🟠 / CRCL 🔴 / COIN 🟠 / HOOD 🟡 (직전 run과 동일, 본 계층은 재해석하지 않는다, P13) |
| 4 | [fact] 3개 섹터 전부 섹터 방향 컨센서스 산출 불가 — §2 참조 |
| 5 | [fact] 관측된 유일한 사전 정의 한도 초과는 축 집중도이며, 임계(60)는 config 주석상 「⚠️초안」이고 지표가 단일 포지션으로 축퇴한 상태가 **2회차 연속** |
| 6 | [fact] 구조적 노출 그래프가 직전 run과 **완전히 동일** — `correlation_matrix.yaml`·`positions.yaml`이 as_of 2026-08-15로 불변이어서 [CODE] 산출 21쌍·9건·8축이 전부 일치. 노출 구조 변화에서 비롯된 신규 트리거 0건 |

[fact] 게이트 미충족은 실패가 아니라 정상 경로다(CLAUDE.md §7).

---

## 2. 매크로 KC 통합 및 L3 에스컬레이션 소비 기록

### 2-0. 매크로 KC 통합 (arbiter 스코프 밖 항목의 L4 통합)

[fact] 이번 회차 arbiter들이 매크로 KC를 자기 판정 스코프 밖으로 명시했다 — CRWV `not_evaluated_out_of_scope`, NBIS `not_provided_this_round`, MU `out_of_scope_for_this_agent`, CRCL은 「arbiter는 KC 정의 원문 미접근(P17)」 조건부 인용. neocloud 섹터 산출물도 「오케스트레이터/L4가 별도로 통합해야 한다」고 기록했다. 따라서 본 계층에서 통합한다.

| 구분 | 건수 | 항목 |
|---|---|---|
| verdict | 10건 전부 `not_met` | KC-1~10 |
| confirmed | 4건 | KC-2 · KC-3 · KC-4 · KC-5 (전부 api 입력·stale 한도 내) |
| provisional | 6건 | KC-1(web_search, staleness 38일) · KC-6·7·8·9(duration 또는 web_search) · KC-10(이벤트형, 자동 확정 불가) |
| 파급 산출 | 9건 | KC-9는 축 매핑 부재로 미산출 — 파급 부재를 뜻하지 않는다 |

[fact] 직전 run과 confirmed·provisional 건수 구성은 같으나 내용이 다르다 — 직전 run에서 KC-7·8은 `value=null`(미수집)이어서 provisional이었고, 이번 회차에는 값이 수집되어 이격도가 산출 가능해졌다. **provisional 사유가 「미수집」에서 「duration·web_search」로 이동한 것이며 확신도 등급 자체는 그대로다.**

[fact] 위 통합 결과는 어떤 개별 종목의 시그널 등급 근거로도 사용되지 않았다(P6·P13).

### 2-1. neocloud — `sector_direction_computable = false` (esc-1, 명시적 소비)

- [fact] `coverage_count >= 2`인 축이 **0개**, 10개 축 전부 `dispersion = single_ticker`. `comparable_axes_count = 0`, `dispersion_computable = false`.
- [fact] 방향 일치도·분산은 **산출 대상 없음** — 「3사 일치」와도 「갈림」과도 다른 제3의 상태이며 **2회차 연속**이다.
- [fact] 본 계층은 이 파일에서 어떤 섹터 방향도 읽지 않았고, **어떤 시나리오도 neocloud 섹터 방향에 연결하지 않았다.**
- **[fact] 이번 회차의 새로운 정보는 원인 진단이다** — 직전 회차는 3사 중 1사(CRWV)의 관측 부재가 중첩을 막았으나, 이번 회차는 **3사 전원이 재료를 냈는데도(Delta 4건→10건) 중첩이 0건**이었다. 섹터 계층은 이로써 축 정의 체계의 비공유(su_20260905_neocloud_003)가 공시 캘린더 비동기성과 독립된 제약임이 확인됐다고 판정했다.
- [fact] 집계 축 10개 중 **9개가 종목 카드 고유 축**이고 `coverage.yaml` common_axes에 직접 대응하는 축은 `power_permit` 1개뿐이다. IREN `margin_structure`는 null observation 기록(supporting_claims 빈 배열·magnitude 「없음」)이므로 실질 관측 축은 9개다.
- [fact] 오독 차단 — 축 수가 4개에서 10개로 늘어난 것을 컨센서스 개선으로 읽지 않았다. 섹터 계층이 수기 점검한 `provisional_cross_mapping_view`(IREN `execution_delivery` + CRWV `gpu_priority` → 「AI CapEx 전송체인」 매핑 시 coverage 2·방향 일치)는 `not_adopted_this_run`이며 본 계층도 채택하지 않았다.
- [fact] **집계 스크립트 중단 승계** — `consensus_aggregate.py`가 `KeyError: '혼재'`로 중단돼(AD-4) `neocloud_aggregate.json`은 수기 집계본이다. 원인은 L2 간 direction 라벨 규약 불일치(IREN 한국어 대 NBIS·CRWV 영문)와 스크립트의 미지 키 방어 부재(AD-5).
- [fact] 승계 이관: 자본조달 구조 공통·특이 판정 `not_determined_this_run`(esc-4, 2회차) · 축 라벨·정의 표준 결정(esc-3) · `coverage.yaml` 매핑 규칙(esc-5) · TX ERCOT/PUCT·NBIS Vineland 1차 자료 접근 한계(esc-6).

### 2-2. stablecoin — `esc_0618_02` 구조적 역노출 3건 갱신

| 항목 | 갱신 상태 | 내용 |
|---|---|---|
| `sie_usdc_distribution_economics` | **updated** | [fact] 분배계약 자동갱신 발효(2026-08-18) 이후 8-K 제출기한(약 2026-08-24)이 경과한 뒤 **12일까지 양사에서 계약변경 공시 부재**가 grade1 confirmed로 확인. CRCL은 EDGAR 재조회로 8/6~9/5 신규 8-K 0건, COIN은 유일한 신규 8-K(2026-09-02)를 **원문 확인**해 Item 5.02 이사회 인사 단독 건임을 확인. 부호 미활성화. |
| `sie_ousd_consortium` | **partially_updated** | [fact] OUSD 실체는 **3 run 연속 무변화**(미출시·실측 유통량 부재). CRCL `competition_ousd` 축이 strengthen으로 재활성화됐으나 **근거는 $YLDS이며 OUSD가 아니다.** |
| `sie_yield_bearing_stablecoin_clause` | **partially_updated** | [fact] 조항 문언·상원 절차 무변화(2026-09-15 클로처 표결 미도래, 추가 순연 없음). **정량 감시 계열 최초 확보** — $YLDS 유통량 1Q26 $598M → 2Q26 $556.033M(**QoQ −7.0%**), 양측 grade1 confirmed. 부호는 여전히 미부여. |

- [fact] 세 항목 모두 `sign_activated_this_window = false`다.
- **[fact] 규모 프록시는 갱신되지 않았다** — Coinbase 귀속 유통비용(3개월 $324.6M·6개월 $655.3M, 도출 분기 계열 Q1'26 약 $330.7M → Q2'26 $324.6M)은 직전 run 값 그대로이며 `reused_from = 20260820_1932` · `staleness_days = 16`으로 관리한다. COIN 측 수취 절대액은 두 run 연속 미공시 — **제로섬 총액 대사는 여전히 불가**다.
- **[inference/강도: 높음] 이번 회차의 구조적 발견** — 직전 run에서 CRCL:strengthen 대 COIN:neutral의 부호 차이는 **자료 접근 비대칭**에서 왔으나, 이번 회차에는 양사가 **동일한 비사건을 같은 등급(grade1)으로 확보한 상태에서도** 부호가 갈렸다. 즉 자료로 좁힐 수 있는 차이가 아니라 노출 구조에서 오는 차이다. 상관 레이어 관점의 함의는 **이 축의 역노출이 대칭적 제로섬이 아니라는 것** — 조건 「변경」은 양면에 반대 부호로 나타나지만 조건 「불변」은 발행자에게는 비용 악화 시나리오의 불발(강화), 분배자에게는 확장 서사의 미확인(어느 방향도 아님)로 작용한다. **[CODE]가 부여한 hedge_strength 「중」은 조건 변경 국면에만 적용되는 값으로 읽어야 한다.**
- [fact] CRCL·COIN 모두 `weight_range [0.0, 0.0]` — 이 부호 반대 관계는 현 포지션에 **실효 상쇄를 만들지 않는다**(구조 관측).
- [fact] 오독 차단 4건 — ① CRCL `reserve_income` strengthen과 COIN `usdc_economics` neutral을 두 종목 이해의 일치로 읽지 않았다. ② CRCL `competition_ousd`의 strengthen을 **OUSD 위협 완화로 읽지 않았다**. ③ CRCL `reserve_income`의 strengthen을 정량 실적 개선으로 읽지 않았다(근거는 공시 부재라는 부작위 관측). ④ 축 커버리지 4개→8개 확대를 컨센서스 개선으로 읽지 않았다(8개 축 전부 coverage 1).
- [fact] 계약 조건 원문의 최종 확인 지점은 양사 **Q3'26 10-Q 계약 주석**으로 이동했다(직전 run의 확인 지점이던 8-K 제출기한은 경과·해소).

### 2-3. memory — `single_ticker_view = true` / `dispersion_status = not_applicable`

- [fact] 커버 종목 MU 1건. Delta 축은 1개에서 **5개로 증가**했으나 방향은 `china_supply` 1개 weaken·나머지 4개 neutral이며, 그 neutral은 「no_change(신규 확정 수치 부재)」로 **방향성 판정이 아니다.**
- [fact] 섹터 산출물은 스크립트의 `dispersion: 'single_ticker'` 문자열을 승계하지 않고 `dispersion=null` · `not_applicable`로 명기했으며 **어떤 축도 「low(전원 일치)」로 해석해서는 안 된다**고 기록했다. 본 계층도 그렇게 해석하지 않았다.
- [fact] 승계: `ip_litigation_risk` 신규 축 제안이 **2개 Run 연속** 사람 판단 대기(섹터 판정 `company_specific_exposure_axis`) · MU 종목 전용 KC 부재 **2개 Run 연속** arbiter 플래그 · 대만 사업장 노사 리스크 신규 축 미매핑 · MU FY26 Q4 실적일 정정(카드 2026-09-22 → 공식 확정 2026-09-30, grade1 confirmed).
- [fact] 섹터 산출물은 축 대기 건에 §9의 **14일 초과 expired 규칙** 적용 여부 확인이 필요하다고 기록했다 — 승인 큐는 본 계층의 P17 허용 입력이 아니어서 상태를 확인하지 않았다.

### 2-4. 종합

[inference/강도: 높음] 3개 섹터 전부 섹터 방향 컨센서스가 산출되지 않았으므로, 이번 회차 시나리오는 **전부 사전 정의 매크로 KC와 config 한도에만 연결**된다 — 섹터 판정을 트리거로 삼은 시나리오는 **0건**이며 2회차 연속이다.
[fact] 다만 섹터 층위가 이번 회차에 기여한 것은 트리거가 아니라 **벡터 제안의 근거**다 — `vector_change_proposals` 8건 중 6건이 `04_sector` 산출물의 Claim·관측을 직접 근거로 삼는다.

---

## 3. 포지션 스냅샷 및 절대 집중도 판정 (`positions.yaml` as_of 2026-08-15, **staleness 21일**)

| 종목 | tier | weight_range | 비고 |
|---|---|---|---|
| IREN | Edge | [0.85, 0.95] | [fact] 기입 90% ±5%p (v32 258주 @평단 $39.29) |
| 현금 | — | [0.05, 0.15] | [fact] 기입 10% |
| MU | Base | [0.0, 0.0] | 미보유 |
| NBIS / CRWV | null | [0.0, 0.0] | 미보유 |
| CRCL / COIN / HOOD | Next | [0.0, 0.0] | 미보유 |

**절대 집중도 판정**

- [fact] 보유 종목은 IREN 1개이며 단일 종목이 포트폴리오의 대부분을 차지하는 **절대 집중 상태**다.
- [fact] IREN은 8개 축 중 **6개 축**에 노출(AI_CAPEX +H · CRYPTO +M · RATES −M · GPU_SUPPLY −M · POWER_PERMIT −H · RISK_APPETITE +M). 미노출은 REGULATION · USDC_DISTRIBUTION_ECONOMICS 2개.
- [fact] [CODE] 파급이 산출된 매크로 KC **9건 전건**의 영향 종목에 IREN이 포함된다.
- **[inference/강도: 높음] 판별력 부재(이력 명기)** — 이 구조 때문에 축 집중도 6축과 KC 파급 9건의 `weight_pct_upper`가 모두 정확히 **95.0**으로 동일 산출된다. 두 지표는 「IREN이 그 축·그 KC에 노출되어 있는가」의 **이진 지표로 축퇴**하며 축 간·KC 간 상대 심각도를 구별하지 못한다. 이 판별력 부재는 직전 run(esc_corr_1932_02·esc_pf_1932_04)에서 최초 기록됐고 **이번 회차가 2회차 연속**이다.
- [fact] 이번 회차에 구별 정보를 담는 것은 비중 합계가 아니라 **① 축·KC별 노출 종목 수 ② KC별 이격도 ③ 이격도 산출 가능 여부**다.
- [fact] 본 항목은 관측된 포지션 구조의 기술이며 비중 조정에 관한 판정을 포함하지 않는다(§9·P15).
- [fact] `positions.yaml` staleness가 직전 run 5일에서 **21일**로 늘었다. 기입값은 시가 재평가 결과가 아니므로 21일 경과분의 가격 변동은 반영되어 있지 않다.

---

## 4. 리밸런싱 시나리오 (12건 — 전건 사전 정의 KC·한도 연결, P11)

| # | 트리거 | 연결 | 현재 판정 | 이격도 | 파급(노출 종목) |
|---|---|---|---|---|---|
| sc_kc1 | FFR > 3.75 | KC-1 | not_met / provisional | **0.00pp — 경계 접촉** (staleness 38일) | RATES −: CRWV·IREN·MU·NBIS (4) |
| sc_kc2 | VIX ≥ 30 | KC-2 | not_met / confirmed | 15.47p (14.53 → 30, 약 2.06배) | RISK_APPETITE +: 6종목 |
| sc_kc3 | BTC < 55,000 **AND** VIX ≥ 25 | KC-3 | not_met / confirmed | BTC −31.10% / VIX 10.47p (AND) | CRYPTO +: COIN·CRCL·HOOD·IREN (4) |
| sc_kc4 | ON RRP ≥ $200B **AND** VIX ≥ 25 | KC-4 | not_met / confirmed | 임계의 약 0.34%(약 296배 필요) / VIX 10.47p | RISK_APPETITE +: 6종목 |
| sc_kc5 | TAIEX 20dma < 0 **AND** 1개월 < 0 | KC-5 | not_met / confirmed | **0.69p** / 2.79p (AND) | RISK_APPETITE +: 6종목 |
| sc_kc6 | SDLLMTK ≤ −30% (2주 지속) | KC-6 | not_met / provisional | 38.0p (+8.0% → −30%) | AI_CAPEX +: CRWV·IREN·MU·NBIS (4) |
| sc_kc7 | 하이퍼스케일러 합산 FCF < 0 (2분기) | KC-7 | not_met / provisional | **$6.835B** (신규 산출 가능, as_of 2026-06-30) | AI_CAPEX +: 4종목 |
| sc_kc8 | Microsoft FCF < 0 | KC-8 | not_met / provisional | **$19.64B** (신규 산출 가능, as_of 2026-06-30) | AI_CAPEX +: 4종목 |
| sc_kc9 | Brent ≥ 120 (1개월 지속) | KC-9 | not_met / provisional | 23.98p (96.02 → 120, 약 +25.0%) | **축 매핑 부재 — 파급 미산출** |
| sc_kc10 | IREN 계약 용량 10%+ 강제 감축 분류 또는 전력접속·인허가 취소·보류 공시 | KC-10 | not_met / provisional | **정의 불가**(이벤트형) | POWER_PERMIT −: IREN (1) |
| sc_axis_concentration | 축별 비중 상단 합 > 60 | `correlation_matrix.yaml` `concentration_threshold_pct` | **초과 — 8축 중 6축** | +35.0pp (95.0 대 60) | IREN |
| sc_position_band | IREN 비중이 [0.85, 0.95] 밖 또는 현금이 [0.05, 0.15] 밖으로 관측 | `positions.yaml` weight_range | 범위 내 | 상단·하한까지 각 5pp (staleness 21일) | IREN |

**요약** — 12건 / KC 연결 10건(KC-1~10 전건) / config 한도 연결 2건 / **섹터 방향 연결 0건** / 종목 전용 KC 연결 0건(P17상 `kill_conditions.yaml` 미로드).
**이격도 산출 가능 11건, 불가 1건**(sc_kc10 이벤트형). 직전 run은 8건/4건이었다 — KC-7·8 지표가 수집되어 개선됐으나 **확신도 개선은 아니다**(두 항목 모두 근거 시점 2026-06-30, staleness 67일, duration 조건 잔존으로 provisional).
**가장 좁은 이격도** — ① KC-1 FFR 0.00pp(staleness **38일**로 직전 run 22일에서 확대) ② KC-5 20dma 레그 0.69p ③ KC-5 1개월 수익률 레그 2.79p.
**이격도 변화** — 넓어진 항목: KC-2(14.84p→15.47p) · KC-3 BTC 레그(−23.43%→−31.10%) · KC-5 좁은 레그(0.24p→0.69p) · KC-6(31.9p→38.0p). 좁아진 항목: KC-9(24.71p→23.98p) 1건. KC-1은 0.00pp 불변이며 **입력도 갱신되지 않았다.**

[fact] `predefined_consequence`는 `kill_conditions.yaml`에 사전 정의된 문구의 인용이며 본 계층의 지시가 아니다 — 상세는 `06_portfolio.json`의 각 시나리오 필드 참조.
[fact] KC-3은 사전 정의 consequence의 파급 대상(IREN·COIN·HOOD·CRCL)과 [CODE] 산출 `affected`가 정확히 일치하는 유일한 KC다. 파급 4종목 중 실제 보유는 IREN 1종목이다. [fact] IREN의 CRYPTO 축 노출 근거(BTC 채굴 현금흐름)에 대해 이번 회차 섹터 산출물이 **채굴 사업의 2026년 12월 말 사실상 중단 기대치**를 기록했으나, 본 시나리오의 파급 목록은 **현행 벡터 기준**이며 벡터 재평가는 제안 단계다(vcp_..._01).

---

## 5. 축 집중도 경보 (절차 3 — 필수 포함)

**발령.** 임계 60 대 관측 95.0 → **+35.0pp 초과**, 8개 축 중 6개 축. **직전 run과 값·축 목록이 동일한 2회차 연속 경보.**

- **초과 축:** AI_CAPEX · RATES · CRYPTO · GPU_SUPPLY · POWER_PERMIT · RISK_APPETITE
- **미초과 축:** REGULATION 0.0 · USDC_DISTRIBUTION_ECONOMICS 0.0 — [fact] 노출 종목(COIN·CRCL·HOOD)이 전원 미보유여서 0.0이다. **위험 부재가 아니라 보유 부재의 결과**다.
- [fact] 6개 축 전부의 초과가 IREN 단일 포지션(상단 0.95)에서 발생한다 — 초과 축 수는 IREN이 노출된 축의 수와 같다.
- [inference/강도: 높음] 이 경보는 축 간 분산 부족을 새로 발견한 것이 아니라 **단일 종목 집중이라는 이미 알려진 상태를 축 언어로 재표현**한 것이다. 6축 동시 초과를 6개의 독립 집중 위험으로 읽으면 오독이다.
- [fact] 종목 수 기준 상대 판정 병기 — RATES 7 / RISK_APPETITE 6 / AI_CAPEX·CRYPTO 각 4 / REGULATION·GPU_SUPPLY 각 3 / USDC_DISTRIBUTION_ECONOMICS 2 / POWER_PERMIT 1.
- [fact] 임계 60은 config 주석상 「⚠️초안」이며 임계 확정은 사람 몫이다.
- **[fact] 이번 회차 추가 관측** — 초과 축 중 하나인 `GPU_SUPPLY`의 **축 정의 자체에 대한 검토 요청**을 등재했다(§6-3·esc_pf_0618_06).

---

## 6. 상관 레이어 (`05_correlation.json`)

[fact] `coefficient_used = false` — 수치형 상관계수 미산출. 등급(상·중·하) + 공유 축 + 근거만(P14).

**[fact] [CODE] 산출값이 직전 run과 완전히 동일하다** — 21쌍 공유도 등급·공유 축·역방향 노출, KC 파급 9건, 축 집중도 8축이 모두 일치하며 차이는 배열 나열 순서뿐이다. 원인은 입력 config가 as_of 2026-08-15로 불변이기 때문이다. **이번 회차 상관 레이어의 변화는 전부 [LLM] 해석·제안 블록에서만 발생했다.**

- **21쌍** 산출. **「상」 등급 6쌍** — COIN·CRCL / COIN·HOOD / CRCL·HOOD / CRWV·IREN / CRWV·NBIS / IREN·NBIS.
- [fact] IREN이 「상」을 이루는 쌍은 CRWV·IREN, IREN·NBIS 2건이며 공유 축은 양쪽 모두 AI_CAPEX·GPU_SUPPLY·RATES·RISK_APPETITE 4축으로 동일하다.
- [inference/강도: 높음] 보유 종목이 1개이므로 21쌍 중 보유·보유 쌍은 0건이다 — 쌍별 공유도는 **실현된 동조 위험이 아니라 신규 후보 편입 시의 구조적 중첩 후보**를 보여준다.

### 6-1. 역노출 뷰 갱신

| 항목 | 갱신 |
|---|---|
| `USDC_DISTRIBUTION_ECONOMICS` (CRCL·COIN) | **표기 유지 + 성질 갱신** — 직전 run의 「공유 축·부호 반대」 표기를 유지하되, **역노출이 대칭적 제로섬이 아니라는 관측을 추가**했다. 조건 「변경」은 양면에 반대 부호, 조건 「불변」은 양면에 같은 부호로 작용하지 않는다. hedge_strength 「중」은 **조건 변경 국면에만** 적용되는 값이다. 규모 프록시는 직전 run 값(staleness 16일), 부호 미활성화. |
| `OUSD_CONSORTIUM` (조건부) | **부호 미확정 유지**, [CODE] 집계 미포함 확인. OUSD 관측 3 run 연속 무변화. **축 슬롯 오염 관측** — `competition_ousd` 한 슬롯에 서로 다른 두 위협원(OUSD·$YLDS)이 담겨 축 공유도 판정 시 근거 Claim ID 확인이 필요하다(P14). 다만 이 축은 `axes` 8개에 없어 이번 [CODE] 공유도에는 유입되지 않았다. 독립성 감시 단서는 미해소 재이월. |
| `YIELD_BEARING_STABLECOIN_CLAUSE` (조건부) | **부호 미확정 유지**, exposures 승격 없음. **$YLDS 계열이 grade4 추정 → grade1 실측으로 격상**되어 조항 결과의 규모 대사 기준선이 마련됐다. 다만 `correlation_matrix.yaml`의 status 문언(「$YLDS 실측 $598M(grade 4, confirmed=false) — 근거 등급 미달로 벡터 미등재」)이 **부정확해졌다** → vcp_..._03. 재판정 트리거 2026-09-15 유지. |
| RATES 축 부호 반대 쌍 | 스크립트 산출 그대로 유지(CRCL·CRWV는 헤지 강도 「상」). [fact] 상대 종목이 전원 미보유이므로 현 포지션에서 실현되는 상쇄는 없다. |

### 6-2. 벡터 변경 제안 (8건 — 제안만, `auto_apply=false`, 자동 반영 금지)

**[fact] 8건 전부 부호 변경 0건 · 강도 변경 0건이다.** basis·status 문언 갱신, 예약 항목 상태 보고, 축 정의 검토 요청, 신규 축 유보로 구성된다.

| ID | 대상 | 유형 | 요지 |
|---|---|---|---|
| vcp_..._01 | IREN `CRYPTO` | 예약 **부분 트리거** | [fact] 「8/27 실적 후 재평가」 예약의 **시점 조건은 충족**(실적콜 재료 반영)됐으나 **내용 조건(매출 믹스 확인)은 미충족** — `ai_cloud_conversion` 신규 정량 데이터 부재, MW당 매출 2회차 연속 미관측. [fact] 관련 신규 사실 1건 확보 — CFO의 「2026년 12월 말까지 채굴 사실상 중단 기대」(grade2 confirmed). [inference/강도: 높음] basis의 「BTC 채굴 현금흐름」 근거가 소멸 예정이므로 **basis는 갱신 대상**이나, 「currently expect」는 확정 실행이 아니고 리스크는 소멸이 아니라 `ai_cloud_conversion` 축으로 **이관**이며 채굴 매출 비중을 계량할 수 없으므로 **강도 하향 근거로는 부적격**. 예약의 재판정 관측 지점을 IREN FY27 1분기 10-Q로 이동할 것을 제안. |
| vcp_..._02 | NBIS `RATES` | 이월 항목의 **트리거 해소·판정 불변** | [fact] 직전 run 트리거(2026-08-24 결제 완료 확인)가 **해소**됐다 — 6-K Ex-99.1(grade1)로 클로징 확정, 그린슈 전액 행사로 $5.0B → **$5.75B**(2030년물 0.50% $3.45B / 2034년물 4.50% $2.3B), 기존 $800M은 약 15.8M주 지분교환. [fact] KC-NBIS-3은 오히려 임계에서 멀어짐(상향 반대) 대 원금 총액 추정 약 $14,991.8M·발행수수료 미공시로 순조달액 미확정(상향 찬성). [inference/강도: 높음] `leverage_burden`↔`funding_access` 축 상충이 2회차 연속 미해소이므로 **트리거는 해소됐으나 판정은 변하지 않았다**. |
| vcp_..._03 | `conditional_exposures.YIELD_BEARING_STABLECOIN_CLAUSE.status` | status 문언 정정(승격 없음) | [fact] $YLDS가 grade1 confirmed로 격상($598M → $556.033M)되어 「근거 등급 미달」 사유가 부정확해졌다. **미등재 판단은 유지하되 사유를 「조항 문언 미확정으로 부호 판정 불가」로 갱신**할 것을 제안. exposures 승격은 제안하지 않는다. |
| vcp_..._04 | CRCL·COIN `USDC_DISTRIBUTION_ECONOMICS` basis | basis 갱신만(직전 run 승계) | [fact] basis가 기준선 확정 수단으로 지목한 「8/18 갱신 실행 공시」는 **발생하지 않았다** — 확인 지점이 Q3'26 10-Q 계약 주석으로 이동했다. 분배자 측 미공시·프록시 미갱신으로 강도 상향은 여전히 부적격. |
| vcp_..._05 | CRWV `AI_CAPEX` basis | 「⚠️갱신 대상」 미해소 + **수치 충돌 추가** | [fact] CRWV EDGAR 신규 제출 0건으로 2회차 연속 갱신 근거 부재. [fact] basis의 백로그 「~$104B」 대 섹터 산출물 인용 「약 $129B」 불일치 — 다만 후자는 inference/weak 인용이라 **단독 갱신 근거가 되지 못한다**. 표기는 유지하되 불일치 병기만 제안. |
| vcp_..._06 | `axes.GPU_SUPPLY` 축 정의 (+3사 노출) | **축 정의 검토 요청(신규)** | §6-3 참조 |
| vcp_..._07 | 신규 축 후보 `ip_litigation_risk`(MU) | 카드 결정 이후로 유보(2회차) | [fact] 2개 Run 연속 사람 판단 대기. 신설되어도 MU 단독·비중 0.0으로 쌍 공유도 기여 0, 집중도 기여 0.0%. 대만 노사 리스크가 신규 축 미매핑 항목으로 추가. |
| vcp_..._08 | `conditional_exposures.OUSD_CONSORTIUM.status` | 감시 노트 추가(직전 run 승계) | 독립성 가정 감시 단서 + OUSD 3 run 무변화 + 축 슬롯 위협원 혼재 3가지 병기 제안. 부호·강도 제안 없음(P4). |

### 6-3. 신규 관측 — `GPU_SUPPLY` 축 정의 검토 요청

- [fact] `GPU_SUPPLY` 축은 label 「GPU 공급·감가」, indicators 「배정 일정」·「감가상각 정책」으로 정의되며 IREN·NBIS·CRWV **3사 전원에 sign `−`**가 부여되어 있다.
- [fact] 섹터 산출물 so-2는 동일 유형의 물리적 자산(NVIDIA 차세대 GPU 랙)이 3사에서 **서로 다른 축으로 분산 계상**된다고 기록한다 — CRWV는 공급 우선권, IREN은 조달 담보·재원(GPU 파이낸싱 약 90%·선수금 약 절반)과 인도 일정으로 분해, NBIS는 이번 회차 GPU 관련 Delta 0건. 그리고 **동일 요인이 두 종목에 반대 부호로 걸릴 구조적 가능성**을 기록했다.
- **[inference/강도: 높음] 상관 레이어에 직접적이다** — [CODE]는 3사가 같은 부호를 갖는다는 전제로 CRWV·IREN, CRWV·NBIS, IREN·NBIS **세 쌍의 공유 축에 GPU_SUPPLY를 계상**했고 세 쌍 모두 「상」 등급이다. 전제가 흔들리면 세 쌍의 등급 근거 일부가 흔들린다.
- [fact] 그럼에도 **부호·강도 변경은 제안하지 않는다** — 검증에 필요한 3사 GPU 조달 조건·인도 일정·감가상각 정책 자료가 **2회차 연속 부재**하고(su_..._001·002), 섹터 산출물 자신이 이를 「구조적 가능성의 기록」으로 한정했다. **P8(축 하위 분해 후 독립 재평가) 적용 여부는 사람 판단이다.**

---

## 7. ThesisPatch 후보 (6건 — 후보 식별까지, 본 계층은 패치 파일 미생성)

> [fact] 산출 시점(2026-09-05T07:05) 기준 `output/20260905_0618/07_thesis_patch/`에 **별도 경로(`refine thesis`)가 생성한 파일이 존재**함이 파일 목록에서 확인된다. [fact] 본 계층은 그 파일들의 **내용을 로드하지 않았고 수정하지 않았다** — 타 계층 산출물이며 본 계층의 P17 허용 입력이 아니다. 아래 목록은 그와 대조되지 않은 **독립 식별 결과**이며 중복·불일치 확인은 오케스트레이터·사람의 몫이다.

| 종목 | 카드 항목 | 성격 |
|---|---|---|
| **MU** | catalysts / earnings_checkpoints — FY26 Q4 실적일 | [fact] 카드·`signals.json` 기재 2026-09-22 대 회사 공식 확정 **2026-09-30**(grade1 confirmed). **후보 중 유일하게 근거 등급이 확정적이며 단독 처리 가능.** 목록형 필드 → `expected_after.counts` 필수 |
| **MU** | 축 목록(`ip_litigation_risk`) / risks(대만 노사) | [fact] 2개 Run 연속 계류(`escalation_pending_human_decision`), 섹터 판정 `company_specific_exposure_axis`. 대만 노사 리스크 신규 등재 후보. §9 14일 초과 expired 규칙 적용 여부 확인 필요 |
| **IREN** | `btc_mining` / `ai_cloud_conversion` 축 전제·체크포인트 | [fact] 채굴 2026년 12월 말 사실상 중단 기대(grade2, 「currently expect」) — 리스크는 소멸이 아니라 `ai_cloud_conversion`으로 **완전 이관**. 그 축은 계량 지표(과금 가동률·MFU·MW당 매출)가 2회차 연속 미확보인 **「측정 수단이 없는 축」**. [inference/강도: 중간] `correlation_matrix.yaml` IREN CRYPTO basis와 직결 — vcp_..._01과 함께 검토 필요 |
| **NBIS** | 전환사채 총액 가정 | [fact] 직전 run 후보의 **규모 확대** — 신규 $5.75B 확정, 원금 총액 추정 약 $14,991.8M(단 inference/medium 추정치·순조달액 미확정). 단일값 대신 range·산출 근거 명기 필요. 목록형 필드 → `counts` 필수 |
| **CRWV** | 이자 커버리지 정의 / CapEx 정합 / 백로그 규모 | [fact] 이월 unconfirmed 3건 전부 미해소(2회차) + basis 「~$104B」 대 섹터 인용 「약 $129B」 충돌. 이번 회차 EDGAR 신규 제출 0건 — **근거 없는 패치 생성은 부적격** |
| **HOOD** | axes — RVII류 상품 대응 축 부재 / 과거 run 미포착 | [fact] 과거 run 미포착 정황 3건(2026-07-29 실적콜 예측시장 발언·RVII IPO 8/13·UK 크립토 출시 8/10) 이관. 소급 재작성은 P9 대상이며 본 계층 권한 밖 |

**패치 미생성 사유** — [fact] F20은 before→after 생성 전 카드 **전문 정독**을 요구한다. [fact] `state/thesis_cards/*`는 cio-portfolio의 P17 허용 목록에 없고 이번 run 지시에서 **thesis card 원문은 명시적 금지 입력**이다. [inference/강도: 높음] 전문 미독 상태의 before→after 생성은 F20 위반(절단된 관측 → 없는 결손 생성)이므로 `refine thesis <TICKER>` 경로로 이관한다. [fact] ThesisPatch는 `requires_human_approval: true` 고정이며 승인 없는 카드 쓰기는 금지된다(F17).
**순서 제약** — [fact] neocloud esc-3·esc-4: 3사 축 라벨·정의 표준 결정이 개별 카드 수정에 선행하는 편이 낫다. 위 NBIS·CRWV·IREN 3건은 동일 유형(정량 지표 정의·전제 공백)이다.

---

## 8. 에스컬레이션 (8건 — 전건 비차단)

| ID | 유형 | 상태 | 내용 |
|---|---|---|---|
| esc_pf_0618_01 | L1 입력 검증 | 이월 | KC-4 ON RRP 단위 정합 — value **675,000,000**(직전 317,000,000)로 갱신됐으나 threshold 200,000,000,000 대비 약 **296배** 격차 지속. 계열은 살아 있으나 단위 의문 미해소. 미확인 상태에서 넓은 이격도를 안전 여유로 해석 불가 |
| esc_pf_0618_02 | KC 임계 경계 | **악화** | KC-1 이격도 0.00pp 경계 접촉 + staleness **38일**(직전 22일) — 동일 입력이 갱신 없이 이월됐다. 가장 좁은 이격도가 동시에 가장 오래된 근거이며 그 격차가 벌어지고 있다 |
| esc_pf_0618_03 | 스크립트·config 결손 | 이월 | `KC_AXIS`에 KC-9 미매핑(10건 중 파급 9건만) / 종목 전용 KC 15건 + IREN 전용 KC 미정의 + MU 전용 KC 부재는 P17상 미로드로 이격도 미산출 |
| esc_pf_0618_04 | 지표 축퇴 | **2회차 연속** | 축 집중도 6축·KC 파급 9건 전건 95.0 — 임계 60의 판별력 부재. 임계 확정은 사람 몫(U4 계열 잔여 부채) |
| esc_pf_0618_05 | **config drift(신규)** | 신규 | 직전 run 벡터 제안 6건이 config에 미반영으로 관측 — `correlation_matrix.yaml`·`positions.yaml` as_of가 2026-08-15 불변(staleness 21일). 승인 큐는 P17 미허용 입력이라 미승인·승인 후 미적용·반려를 구분할 수 없다. 이번 제안 8건 중 4건이 직전 제안의 승계 — 지속되면 basis 서술과 관측 사실의 괴리가 누적된다 |
| esc_pf_0618_06 | **축 정의 리스크(신규)** | 신규 | `GPU_SUPPLY` 축 정의 검토 요청 — 「상」 등급 3쌍의 공유 축이며 종목별 반대 부호 가능성이 제기됐으나 검증 자료가 2회차 연속 부재. P8 적용 여부는 사람 판단 |
| esc_pf_0618_07 | L3 승계 | 이월 | neocloud esc-1~6(컨센서스 불가 2회차·집계 스크립트 KeyError 중단·축 라벨 표준·자본조달 귀속 판정·`coverage.yaml` 매핑·1차 자료 접근 한계), stablecoin esc_0618_01(`sources.yaml`에 federalregister.gov·cdn.ca9.uscourts.gov·home.treasury.gov 미등재)·esc_0618_03(HOOD 과거 run 미포착 3건)·esc_0618_04(CRCL `reused_from`·`staleness_days` 표기가 as_of와 부정합 — P16 규약 확인), memory의 축 신설 결정·MU 전용 KC 부재·MU 실적일 정정·`*.senate.gov` 등재 검토 |
| esc_pf_0618_08 | ThesisPatch 이관 | 이월 | 후보 6건 식별, 패치 생성은 `refine thesis` 경로. MU 실적일 정정 1건만 grade1 confirmed 근거로 단독 처리 가능 |

---

## 9. 한계

- [fact] **P12** — 게이트 미충족이므로 `default_action = no_action`이며 이는 정상 경로다.
- [fact] **P13** — 하위 산출물(시그널 등급·섹터 판정)을 소급 수정하지 않았고, 섹터 컨센서스·KC·상관을 개별 종목 시그널 근거로 인용하지 않았다.
- [fact] **P14** — 수치형 상관계수 미산출(`coefficient_used = false`).
- [fact] **P15** — 행동 지시 동사·목표 비중 단일값·시점 지시 미포함. `predefined_consequence`는 config 사전 정의 문구의 인용이다.
- [fact] **P16** — `positions.yaml`·`correlation_matrix.yaml` 모두 as_of 2026-08-15(각 staleness 21일). KC-1 입력 staleness 38일, KC-7·8 입력 staleness 67일, 역노출 규모 프록시 staleness 16일을 각 항목에 명기했다.
- [fact] **P17** — 구조화 산출물만 로드. `02_company/*` 원문·`_raw_*`·thesis card 원문·`kill_conditions.yaml`·`coverage.yaml`·승인 큐는 열지 않았다.
- [fact] **벡터 의존** — 상관·집중도는 사람이 편집한 `correlation_matrix.yaml`에 의존하므로 벡터의 정확성이 이 레이어의 정확성 상한이다. 미해소 항목 — IREN CRYPTO 재평가 예약(시점 충족·내용 미충족) · NBIS RATES −H 재검토(트리거 해소·판정 불변) · CRWV AI_CAPEX basis ⚠️갱신 대상(2회차 + 수치 충돌) · `YIELD_BEARING_STABLECOIN_CLAUSE` status 문언 부정확 · `GPU_SUPPLY` 축 정의 검토.
- [fact] **섹터 층위 기여** — 3개 섹터 전부 방향 컨센서스 미산출로 트리거 기여는 2회차 연속 0건이며, 기여는 벡터 제안 8건 중 6건의 근거로 나타났다.

> 본 상관은 구조적 노출 판정이며 실제 가격 동조화를 예측하지 않는다. 축 노출이 낮아도 유동성 이벤트에서 동반 하락할 수 있다. 노출 벡터는 사람이 편집한 correlation_matrix.yaml에 의존하므로, 벡터의 정확성이 곧 이 레이어의 정확성 상한이다.

---
**검증** — `validate_output.py --layer correlation` PASS · `--layer portfolio` PASS
