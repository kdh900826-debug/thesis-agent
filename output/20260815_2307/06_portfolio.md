# L4 포트폴리오 뷰 — Run 20260815_2307

- **as_of**: 2026-08-15T23:07 · **run_id**: `20260815_2307`
- **default_action**: **`no_action`** — 발동(met) KC 0건
- **본 문서는 관점(view)이며 매수·매도 지시가 아니다.** 시나리오의 실행 여부와 방식은 전적으로 사람의 판단이다.

## 0. 이번 Run 한 줄 요약

> [fact] 신규 재료는 **stablecoin 섹터 1건**(CRCL·COIN·HOOD)에만 존재하고, 이 3종목의 비중은 **전부 0**이다.
> [inference:strong] 따라서 이번 Run의 산출 가치는 익스포저 조정이 아니라 **구조 이해(역노출 3건)** 와 **카드 정확성(ThesisPatch 3건)** 에 있다.

## 1. 입력 및 신선도 (P16)

| 입력 | 경로 | reused_from | staleness |
|---|---|---|---|
| stablecoin 섹터 | `04_sector/stablecoin.json` | 20260815_2252 | 0일 · **이번 Run 유일한 신규 생성분** |
| neocloud 섹터 | `04_sector/neocloud.json` | 20260815_1408 | 0일 · 신규 재료 없음 |
| memory 섹터 | `04_sector/memory.json` | 20260815_1408 | 0일 · 단일 종목 뷰(MU) |
| 매크로 KC | `01_macro_kc.json` | 20260815_1408 | 0일 |
| 상관 | `05_correlation.json` | — | 이번 Run 생성 |
| config | `correlation_matrix.yaml`(active) · `positions.yaml` · `kill_conditions.yaml` | — | 2026-08-15 사용자 확정본 |

[fact] `02_company/*` 원문과 `03_signal/*`은 로드하지 않았다(P17). 시그널 등급은 이번 Run 입력 화이트리스트에 없어 **참조·인용하지 않았다**.

## 2. 포지션 스냅샷

| 종목 | tier | 비중 범위 |
|---|---|---|
| **IREN** | Edge | **[85%, 95%]** — 258주 @평단 $39.29 |
| MU | Base | [0%, 0%] |
| NBIS · CRWV | — | [0%, 0%] |
| CRCL · COIN · HOOD | Next | [0%, 0%] |
| 현금 | — | [5%, 15%] |

[fact] 실보유는 IREN 1건. v32 레버리지 규칙(Base 현금 대비 40% 상한)은 **Base 미보유로 비활성**.

## 3. 집중도 경보 — 7개 축 중 **6개 임계 초과**

임계 `concentration_threshold_pct: 60` (⚠️초안 표기 상태) · 기준: positions.yaml 비중 범위 **상단** 합(D13, 보수적)

| 축 | 노출 종목 | 보유 익스포저(상단) | 임계 대비 | 판정 |
|---|---|---|---|---|
| AI_CAPEX | CRWV·IREN·MU·NBIS | 95.0% | **+35.0%p** | 🔴 초과 |
| RATES | 7종목 전건 | 95.0% | **+35.0%p** | 🔴 초과 |
| CRYPTO | COIN·CRCL·HOOD·IREN | 95.0% | **+35.0%p** | 🔴 초과 |
| GPU_SUPPLY | CRWV·IREN·NBIS | 95.0% | **+35.0%p** | 🔴 초과 |
| POWER_PERMIT | IREN | 95.0% | **+35.0%p** | 🔴 초과 |
| RISK_APPETITE | COIN·CRWV·HOOD·IREN·MU·NBIS | 95.0% | **+35.0%p** | 🔴 초과 |
| REGULATION | COIN·CRCL·HOOD | 0.0% | -60.0%p | ⚪ 이내 |

### 어떻게 읽어야 하나

- [inference:strong] 초과 폭이 6개 축 **전부 +35.0%p로 동일**한 이유는 축별 분산이 아니라 **IREN 단일 포지션이 6개 축 전부에 노출**되어 있기 때문이다. IREN이 노출된 축은 95%, 노출되지 않은 축(REGULATION)은 0%로 이분된다.
- [inference:strong] 즉 이 경보는 "특정 축에 집중" 이 아니라 **"단일 종목 집중이 축 집중으로 그대로 전사"** 이며, **축 단위 분산 조치로 해소되는 성격이 아니다**.
- [fact] REGULATION의 0.0%는 무노출이 아니라 **노출 3종목이 전부 미보유**라는 뜻이다(P5). 이번 Run의 규제 신규 재료는 전부 이 축에서 나왔고 익스포저는 0이다.
- [fact] **자연 헤지는 실효 없음** — 05_correlation.json의 역노출 9쌍도, 이번 Run에서 새로 확인된 stablecoin 내부 역노출 3건도 반대편 종목이 전부 비중 0이라 포트폴리오 수준 상쇄가 발생하지 않는다.

### ⚠️ 알려진 부채 — 단일 종목 절대 한도 미정의

[fact] config 어디에도 single-name cap이 없어 IREN 상단 95%의 이격을 **산출할 수 없다**. [fact] L4는 사전 정의되지 않은 기준을 생성하지 않는다(P11) — config 수정 **제안만** 가능하며 등재 위치는 `esc_20260815_2307_single_name_cap`.

## 4. 이격도 (사전 정의 한도에 대해서만)

| 항목 | 현재 | 한도 | 이격 | 상태 |
|---|---|---|---|---|
| 축 집중도 (6개 축) | 95.0% | 60.0% (⚠️초안) | +35.0%p | breach |
| 축 집중도 (REGULATION) | 0.0% | 60.0% | -60.0%p | within |
| 현금 비중 | [5%, 15%] | [5%, 15%] | 범위 내 | within |
| IREN 단일 종목 집중도 | [85%, 95%] | **미정의** | 산출 불가 | limit_undefined |
| IREN 가격 라인 ($30/$28) | 미관측 | price_lines.IREN | 산출 불가 | input_missing |
| KC-CRCL-2 (점유율 -3%p QoQ) | -1%p (회사 정의 계열, grade 1) | -3%p | -2%p 여유 | **분모 계열 미확정** |

## 5. 리밸런싱 시나리오 — 9건, 전부 `no_action`

[fact] 모든 시나리오는 사전 정의된 KC·한도에 `source`로 연결되어 있다(P11). `predefined_consequence`는 config에 **사람이 정의한** 결과의 원문 인용이며 L4의 지시가 아니다.

| # | 트리거 | source | 게이트 상태 | 축 | 조치 |
|---|---|---|---|---|---|
| 1 | KC-1 FFR > 3.75% | `kill_conditions.yaml#macro.KC-1` | not_met **provisional** (값 null) | RATES | `no_action` |
| 2 | KC-2 VIX ≥ 30 | `#macro.KC-2` | not_met confirmed (14.25) | RISK_APPETITE | `no_action` |
| 3 | KC-3 BTC < $55K **AND** VIX ≥ 25 | `#macro.KC-3` | not_met confirmed (BTC 63,060 / VIX 14.25) | CRYPTO | `no_action` |
| 4 | KC-4 ON_RRP ≥ $200B **AND** VIX ≥ 25 | `#macro.KC-4` | not_met confirmed (⚠️단위 이슈) | RISK_APPETITE | `no_action` |
| 5 | KC-6·7·8 AI CapEx 3단 | `#macro.KC-6·7·8` | not_met **provisional** (3건 전부 null) | AI_CAPEX | `no_action` |
| 6 | KC-9 Brent ≥ $120 (1개월) | `#macro.KC-9` | not_met **provisional** (93.26, stale 3/3) | 매핑 축 없음 | `no_action` |
| 7 | KC-10 IREN 전력·인허가 이벤트 | `#macro.KC-10` | not_met **provisional** (이벤트형) | POWER_PERMIT | `no_action` |
| 8 | KC-5 TAIEX 2조건 | `#macro.KC-5` | **판정 부재** (skipped_draft) | RISK_APPETITE | `no_action` |
| 9 | IREN 가격 라인 $30/$28 | `#price_lines.IREN` | **입력 부재** | 가격 기반 | `no_action` |

### 주목할 시나리오 3건

- **#7 KC-10 (POWER_PERMIT)** — 노출 종목이 IREN 1건뿐이면서 집중도 95%인 축. 실보유 익스포저와 가장 직접적으로 연결된 KC인데, neocloud 재사용분이라 **신규 관측 0건**이다. 직전 Run의 미해소 항목(2026-08-03 텍사스 ERCOT 신규 접속 감사·보류 지시, grade 4·confirmed=false, 적용 범위 unconfirmed)이 그대로 이월. 다음 계기는 **2026-08-27 IREN FY26 실적**.
- **#5 KC-6·7·8 (AI_CAPEX)** — 집중도가 가장 높은 축의 판정 지표 3건이 **두 Run 연속 전부 null**.
- **#3 KC-3 (CRYPTO)** — 실보유 IREN을 명시적으로 지목하는 유일한 매크로 KC. [fact] 크립토 재료는 여전히 상충하나(HOOD 7월 거래액 MoM -33% vs CRCL 유통량 +19% YoY), 04_sector는 직전 Run의 집계상 상충 소멸을 **"두 종목 관측의 수렴이 아니라 CRCL 축 재매핑의 산물"** 로 명시했다 — 측정 대상(플로우/스톡)·관측 구간(7월 월간/6·30 마감) 불일치는 그대로다. [fact] KC-3의 판정 지표는 BTC·VIX이며 둘 다 확정 미충족.

## 6. 노출 벡터 변경 제안 (제안만 — config 자동 수정 없음)

> [fact] `config/*.yaml`은 사용자 직접 편집 영역이다. 아래는 **전부 제안**이며 L4는 어떤 config도 수정하지 않았다.

| id | 대상 | 판단 | 직전 대비 |
|---|---|---|---|
| `vcp_20260815_2307_01` | `exposures.CRCL.CRYPTO` 강도 M | **미결 유지**, 근거 갱신 | ← `vcp_1408_01` 승계 |
| `vcp_20260815_2307_02` | `USDC_DISTRIBUTION_ECONOMICS` 축 신설 | **재제출**, 근거 강도 보강 | ← `vcp_1408_02` |
| `vcp_20260815_2307_03` | sign 스키마 확장(부호 미확정 표기) | **재제출**, 해당 항목 1→2건 | ← `vcp_1408_03` |
| `vcp_20260815_2307_04` | 이자부 스테이블코인 축 | **신설하지 않음** (조건부 유예) | 신규 |
| `vcp_20260815_2307_05` | `exposures.NBIS.RATES` -M → -H 재검토 | **이월**, 신규 근거 없음 | ← `vcp_1408_04` |
| `vcp_20260815_2307_06` | `exposures.IREN.CRYPTO` 예약 재평가 | **미도래** — 8/27 실적 대기 | 신규(config 예약분) |

**01 (CRCL CRYPTO)** — 직전 제안의 근거였던 "집계상 상충"은 사라졌으나, 04_sector는 그 소멸을 **CRCL이 `usdc_circulation_scale`을 방향 전제 없이 neutral로 판정한 결과**로 명시했고 측정 대상·구간 불일치는 남았다. [fact] QoQ가 분기말 -4.8% / 평잔 +1.7%로 갈린 사실도 새로 확인됐다. [inference:strong] basis "유통량이 크립토 활동과 연동"은 이번 창에서도 검증되지 않았고, 검증 불가 사유가 **"상충" → "대사 수단 부재"** 로 바뀌었을 뿐이다 → **강도 변경 확정 제안 없이 재검토 유지**.

**02 (역노출 축 신설)** — [fact] 근거 보강: CRCL CEO의 **"기존 조건대로"** 문언(grade 2 confirmed) + EDGAR 8-K 전건 조회로 Item 1.01·1.02 부재 확인(grade 1 confirmed). [fact] 그럼에도 05_correlation의 CRCL·COIN 쌍은 여전히 공유도 **'상'** (동일 부호 3축)이고 `inverse_axes`가 없다 → [inference:strong] **이번 공유도 '상'도 역노출 성분을 반영하지 않은 값**이다. [fact] 크기는 정량화 불가(COIN USDC 수익 절대액 미공시, 배분 조건 비공개, CRCL $410M은 파트너 합산) → strength 잠정 M.

**04 (이자부 스테이블코인 — 축 신설 안 함)** — [fact] 근거가 $YLDS $598M(grade 4, confirmed=false)과 CLARITY 60표 불확실성(grade 3)뿐이고 조항 문언 미확정. [inference:strong] 지금 축을 신설하면 **미검증 노출이 [CODE] 산출에 유입돼 공유도·집중도 수치를 오염**시킨다(P4·P14). **무기한 보류가 아니라 재판정 시점을 가진 유예** → 트리거: **2026-09-15 CLARITY 절차 표결 이후 문언 확정**.

**06 (IREN CRYPTO)** — [fact] config에 사용자 확정으로 "8/27 실적의 매출 믹스 확인 후 제안" 예약이 기재돼 있다. 2026-08-27 미도래 + neocloud 재사용분이라 관련 신규 자료 0건 → **근거 없이 예약을 앞당기지 않는다**. [fact] IREN은 CRYPTO 축 95% 집중도의 유일한 실보유 종목이므로 예약 항목 중 익스포저 영향이 가장 크다.

## 7. Thesis 정교화 (S7) — 신규 ThesisPatch 3건, 전부 CRCL

> [fact] 전부 `requires_human_approval: true` — 승인 전 카드에 적용되지 않는다(F17). [fact] 2026-08-15에 이미 승인·적용된 9건은 재제안하지 않았다. [fact] neocloud·memory는 재사용분이라 카드를 부정확하게 만든 신규 1차 자료가 없어 패치 대상이 CRCL 1종에 한정된다.

| 승인 큐 id | 필드 | op | 내용 | 핵심논거 역전 |
|---|---|---|---|---|
| `ap_20260815_2315_thesis_patch_crcl_risks_ylds` | `risks` | amend | "$YLDS 등 — 등록부 누락, 패치 대기" → **실측 등재**($598M, 1Q26, grade 4·confirmed=false, USDC 대비 1% 미만). **2026-08-15 이관 미결 건 해소** | ❌ |
| `ap_20260815_2315_thesis_patch_crcl_market_share_observed` | `axes` | amend | `usdc_market_share` 라벨의 **"실측 부재로 관측 불가"가 사실이 아니게 됨** — 회사 정의 점유율 28%→27%(-1%p QoQ, grade 1 confirmed) 최초 확보. 분모 정의가 다른 두 계열 병존을 명시 | ❌ |
| `ap_20260815_2315_thesis_patch_crcl_regulation_decompose` | `axes` | **decompose (P8)** | `regulation` 축에 **회사 개별 인허가(OCC·NYDFS, grade 1 confirmed)** 와 **섹터 입법(SEC 면제·CLARITY, grade 3·4 confirmed=false)** 이 반대 부호로 혼재해 **등급 위계 없이 상쇄**됨 → `regulation_company_licensing` / `regulation_sector_legislation`으로 분해 | ❌ |

### 제안하지 **않은** 것

- [fact] CRCL risks의 "금리 인하 시 … 자연 헤지" 항목 — 현 포지션에서 자연 헤지가 실효하지 않음이 확인됐으나 패치하지 않았다. **포트폴리오 계층 판정을 개별 종목 카드 근거로 내려보내는 것은 근거 방향 위반**(P13).
- [fact] CRCL diversification / key_metrics에 ARC 프리세일 각주 병기 — 기존 서술이 **부정확해진 것이 아니라 주석이 없을 뿐**이므로 S7 트리거 미해당.
- [fact] NBIS thesis 문장 — 이자부 부채 총액 재대조 전까지 **보류 유지**(다음 실적 Run).
- [fact] 에스컬레이션(json 없는 .md) 신규 생성 **0건** — 이번 Run의 패치 3건 모두 라벨에 방향 전제가 내장돼 있지 않아 핵심 논거를 뒤집지 않는다.

## 8. 에스컬레이션 — 신규 3건 · 이월 4건

### 신규

| id | 주제 | 사용자 조치 |
|---|---|---|
| `esc_20260815_2307_kccrcl2_denominator` | **KC-CRCL-2 판정 계열(분모) 미명시** — 회사 정의(27%)와 3자 집계(약 24%)의 분모가 달라 약 3%p 격차. 계열 미확정 시 **같은 임계가 다른 판정**을 낳는다 | `kill_conditions.yaml`에 판정 계열 명시 |
| `esc_20260815_2307_crcl_distribution_cost_figure` | **CRCL Q2'26 유통·거래·기타비용 수치 Run 간 불일치** — 이번 산출물 **$410M** vs run 1408 인용 **$412M**. 이 수치는 RLDC 마진 41%와 역노출 축 신설 제안의 기초 자료다 | 원문 대조 후 정정 대상 Run 확정 (정정은 신규 버전 발행, P9) |
| `esc_20260815_2307_iren_coverage` | **실보유 IREN 관측 커버리지 공백 지속** — 두 Run 연속 신규 근거 사실상 0건인 반면 이번 Run 신규 재료는 전부 비중 0 종목에 집중. **관측 자원과 익스포저의 비대칭 확대** | 8/27 실적 시점 `run ticker IREN` 계획 확인 / 조기 재실행 여부 |

### 이월 (직전 Run에서 미해소)

| id | 주제 |
|---|---|
| `esc_20260815_2307_kc5` | KC-5 상태 불일치 — config는 `active`, 매크로 산출물은 `skipped_draft`(verdict 없음), 그런데 상관은 파급을 산출 |
| `esc_20260815_2307_onrrp` | ON_RRP 수집값 단위 정합성 (자릿수 3자리 차이) |
| `esc_20260815_2307_single_name_cap` | 단일 종목 절대 집중도 한도 미정의 (**알려진 부채**) |
| `esc_20260815_2307_price_feed` | IREN 가격 라인 관측 입력 부재 |

## 9. 종목 KC 감시 (관측 기록 — 리밸런싱과 무관)

[fact] 종목 KC는 전부 **미보유 6종목** 대상이라 현 포지션 구성에서 시나리오로 연결되지 않는다. [fact] 이 절은 개별 종목 시그널 등급을 변경·제안하지 않는다(P13).

| KC | 상태 | 직전 Run 대비 |
|---|---|---|
| KC-CRCL-1 (유통량 수축) | 미충족 (경고 포함) | **신규** — QoQ 분해(분기말 -4.8% / 평잔 +1.7%) 최초 병기 |
| KC-CRCL-2 (점유율) | 회사 정의 계열 미충족 — **판정 기준 자체 미확립** | **신규** — "관측 부재" → "실측 확보, 기준 미확정" |
| KC-CRCL-3 / KC-COIN-4 (분배계약) | 미발동 — **2026-08-18 확인 대기** | 근거 강도 보강(CEO 문언 + EDGAR 8-K 부재), 상태 불변 |
| KC-COIN-1·2·3 | 판정 불가 — 신규 정량 공시 부재 | 불변 |
| KC-HOOD-1·2 | 미충족 (AND 조건이 사이클 노이즈를 걸러냄) | 총플랫폼자산 MoM -4%(사유 미기재) 추가, 판정 불변 |
| KC-HOOD-3 | 미충족 (CFTC 자문은 절차적 성격) | 불변 |
| KC-NBIS-2·3 | 미충족 / 스프레드 조건 판정 불가 | 불변 (재사용분) |
| KC-CRWV-3 | 차환·covenant 미충족 / 커버리지 판정 보류 | 불변 (재사용분) |
| KC-MU-* | 신규 재료 부재 | 불변 (재사용분) |

## 10. 제약 준수 (P11~P17)

| 원칙 | 준수 내용 |
|---|---|
| P11 | 전 시나리오가 사전 정의 KC·price_lines에 `source` 연결. 임의 트리거·임계 미생성 |
| P12 | 게이트 미충족 → 최상위·전 시나리오 `no_action` + 근거 서술 |
| P13 | 시그널 등급 변경·제안·**참조 없음**. 하위 산출물 오류(KC-5·ON_RRP·$410M)도 수정 없이 escalations로만 이관. 포트폴리오 판정을 카드 근거로 내려보내지 않음 |
| P14 | 수치형 상관계수 산출·인용 **없음** — 등급(상/중/하)+공유 축만 |
| P15/F18 | 지시 동사·목표 비중 단일값·시점 지시 **없음**. KC consequence는 `predefined_consequence` 필드에 원문 인용(사람이 config에 정의한 결과) |
| P16 | 전 재사용 입력에 `reused_from`·`staleness_days` 유지 |
| P17 | `02_company` 원문·`03_signal` 미로드. 카드는 S7 단계 한정 열람 |
| config 자율성 | **어떤 config도 수정하지 않음.** 벡터 변경은 전부 제안(`requires_user_edit`) |

---

**[fact] 본 산출물은 구조적 노출·사전 정의 게이트 상태·이격도를 기술한 관점(view)이며 매수·매도 지시가 아니다.** [fact] 축 집중도·KC 파급의 비중 수치는 positions.yaml의 사용자 기입 범위 상단에 의존하므로 기입값의 정확성이 이 레이어의 정확성 상한이다. [fact] 노출 벡터는 사람이 편집한 `correlation_matrix.yaml`에 의존한다.
