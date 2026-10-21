# L4 포트폴리오 통합 뷰 — run 20261001_0900

- **as_of**: 2026-10-02T23:05 (run 기준일 2026-10-01) / **staleness_days**: 0 / **reused_from**: 없음
- **produced_by**: cio-portfolio (L4) — 상관·포트폴리오 파트
- **default_action**: `no_action`
- **[fact]** 이 문서는 시나리오·한도·이격도만 보여준다. 포지션 행동 지시가 아니다(P15·F18). 목표 비중 단일값과 시점 지시는 넣지 않았다.
- **[fact]** 등급·행동·임계 확정은 전부 사람의 권한이다(CLAUDE.md §9).
- **[fact]** 모든 주장 문장에 `[fact]` 또는 `[inference/강도]` 태그를 붙였다(P1).
- **[fact]** thesis-refine/ThesisPatch(07_thesis_patch·승인 큐·thesis card)는 병렬 에이전트 소관이다. 이 파트는 그 파일들을 쓰지 않았다.
- **[fact]** 직전 시도가 API 한도로 산출물 없이 중단돼 run 기준일 다음 날 작성했다. 입력은 전부 run 기준일 산출물이다.
- 구조화 원본: `06_portfolio.json`, `05_correlation.json`

---

## 0. 한 문단 요약

**[fact]** KC-1(FFR 4.00 > 3.75, confirmed)이 3회 연속 met이다. 그사이 신규 FOMC는 없었다. **[fact]** 그래서 IREN·NBIS·CRWV는 🟡에서, MU는 🟠에서 🔴🔴 **후보**가 다시 나왔다. 네 건 모두 KC-1 하나에서 나왔고, 종목 KC가 훼손된 경우는 0건이다. **[fact]** MU에는 다른 경로도 하나 있다. Kill이 없더라도 ip_litigation_risk 때문에 🔴 하향 후보가 된다. 근거는 9/29 Netlist가 HBM을 직접 겨냥해 낸 2차 ITC 제소다. **[fact]** 🔴🔴 후보는 09-19·09-25·10-01 세 번 연속 사람 확정 기록이 없다(`signals.json` as_of 09-05). 그 구조적 원인은 승인 큐가 🔴🔴 결정을 받는 유형을 갖고 있지 않다는 데 있다. **[fact]** 축 집중도는 8축 중 6축이 임계를 넘었다(95.0 대 60 초안, 5회차 연속). **[fact]** 사용자가 요청한 한국 대미 에너지 투자(Project Star)는 §7에 별도로 정리했다. 섹터 재료이며, 종목 시그널 근거로 쓸 수 없다. **[fact]** 벡터 제안은 11건이다(이월 9, 신규 2). 이 중 부호·강도 변경을 요구하는 것은 0건이다. **[fact]** 🔴🔴가 포함된 run이므로 자동 실행 없이 사람 확인 요청으로 끝낸다(§12).

---

## 1. 입력과 격리 (P16·P17)

| 입력 | as_of | staleness | 비고 |
|---|---|---|---|
| `01_macro_kc.json` | 2026-10-01T22:00 | 0 | |
| `04_sector/{neocloud,memory,stablecoin}.json` | 2026-10-01 | 0 | stablecoin은 같은 run 중단 후 재실행본 |
| `05_correlation.json` | 2026-10-02T22:35 (LLM 22:50) | 0 | validate PASS |
| `config/correlation_matrix.yaml` | 2026-08-15 | 47 | status: active → U4 중단 사유 아님 |
| `config/positions.yaml` | 2026-09-19 | 12 | 30일 한도 이내 |
| `config/kill_conditions.yaml` | 2026-08-15 | 47 | 시나리오 임계 대조용 |
| `state/signals.json` · `pending_approvals.json` | 2026-09-05 (signals) | 26 | 읽기 전용 — 59건 전부 thesis_patch |

**[fact]** 다음 파일은 로드하지 않았다: `02_company/*` 원문, `03_signal/*`, `00_user_sources`(한국 투자 원본 포함), `_raw_*`, thesis card(P17). 등급 후보와 종목 KC 판정은 04_sector에 인용된 내용으로만 참조했다. **[fact]** `state/`·`config/`·`07_thesis_patch/`에는 쓰지 않았다.

---

## 2. 매크로 KC 통합

| KC | 판정 | 이격 | 직전 회차 대비 |
|---|---|---|---|
| **KC-1** FFR>3.75 | **met / confirmed** | +0.25%p 초과 | 3회 연속, 값 불변 |
| KC-2 VIX≥30 | not_met / confirmed | 13.74pt 여유 | 14.33 → 13.74 |
| KC-3 BTC<55k & VIX≥25 | not_met / confirmed | BTC 28,670.59 USD · VIX 8.74pt 여유 | BTC 여유 축소 |
| KC-4 ON RRP≥200B & VIX≥25 | not_met / confirmed | ON RRP 188,461,000,000 USD 미달 | $0.63B → $11.54B(약 18배), 임계 대비 여전히 낮음 |
| KC-5 TAIEX | not_met / confirmed | +2.92%p / +4.82%p | 여유 축소 |
| KC-6 SDLLMTK | not_met / provisional | **산출 불가 — 소스 상충으로 채택 보류** | 2회 연속 공백 |
| KC-7 / KC-8 | not_met / provisional | 6.835B / 19.64B USD 여유 | as_of 06-30(93일) |
| KC-9 brent≥120(1개월) | not_met / provisional | 6.04 USD 미달 | 113.96, 하회 지속 |
| KC-10 IREN 전력·인허가 | not_met / provisional | 이벤트형 | IREN 고유 관측 0건 |

### KC-1 사전 정의 결과 문언과 현 장부의 대응

> `레버리지 전액 해제 + Edge/Next 50% 축소 검토` — `config/kill_conditions.yaml#macro.KC-1.consequence` 원문 인용(본 에이전트가 작성한 지시가 아님)

| 조항 | 현 장부 | 대상 |
|---|---|---|
| 레버리지 | 미사용. v32 레버리지 규칙은 Base 미보유로 비활성 | **없음** |
| Edge | IREN [0.85, 0.95] | **IREN 1종목** |
| Next | CRCL·COIN·HOOD 전부 미보유 | **없음** |
| (문언 밖) | MU(Base)·NBIS·CRWV 미보유 | 🔴🔴 후보지만 포지션 효과 없음 |

**[fact]** 09-19·09-25 회차가 같은 문언에 대해 사람 확인을 요청했다. 그러나 `signals.json`·승인 큐·`positions.yaml` 어디에도 결정 기록이 없다. **[inference/중]** 결정을 내렸는데 기록하지 않은 것인지, 아직 결정하지 않은 것인지는 구분할 수 없다(P5).

### KC-9 duration

**[fact]** L1은 두 해석을 모두 기록했다. 연속 해석으로는 최장 4거래일(09-14~09-17), 누적 해석으로는 14거래일 중 6일이다. 둘 다 미충족이다. **[fact]** 어느 해석을 쓸지는 config에 정의돼 있지 않으므로 사람이 정할 사안이다(esc_L4_0900_04). **[fact]** KC-1과 RATES 축을 공유하므로 두 번 세지 않는다.

---

## 3. 시그널 등급 (P13 — 인용, 수정 없음)

| 종목 | 확정(state) | 후보 | 경로 | 종목 KC | 보유 |
|---|---|---|---|---|---|
| IREN | 🟡 | **🔴🔴** | KC-1 단독, 3회 연속 / 펀더멘털 경로 maintain | 미정의 | **보유** |
| NBIS | 🟡 | **🔴🔴** | KC-1 단독, 3회 연속 / maintain | KC-NBIS-1~3 not_met | — |
| CRWV | 🟡 | **🔴🔴** | KC-1 단독, 3회 연속 / maintain | KC-CRWV-1~3 not_met | — |
| MU | 🟠 | **🔴🔴** | KC-1 단독 / **펀더멘털 경로 🔴 하향 후보**(ip_litigation_risk) | 미정의 | — |
| CRCL | 🔴 | 🔴 유지 | — | KC-CRCL-1~4 not_met | — |
| COIN | 🟠 | 🟠 유지 | — | not_met, KC-COIN-3 (b)항 unresolved_fact | — |
| HOOD | 🟡 | 🟡 유지 | — | KC-HOOD-1~3 not_met | — |

- **[inference/강]** 🔴🔴 후보 4건은 독립된 사건 4개가 아니다. 하나의 매크로 상태가 KC-1 파급 집합(RATES 축)을 따라 네 종목에 전이된 것이다. 이 일치를 종목 근거로 쓰지 않는다(P13).
- **[fact] 결정 기록 경로 부재(시스템 갭, 재보고)** — 승인 큐 59건은 전부 `thesis_patch` 유형이다. 오케스트레이터에 따르면 큐는 thesis_patch/version_publish 유형만 받는다. **[inference/강]** 그래서 사람이 결정을 내려도 기록할 곳이 없다. arbiter가 매 run 같은 후보를 다시 만드는 이유가 이것이다(esc_L4_0900_02).

---

## 4. 이번 run에서 수정된 시스템 결함 — 종목 KC 발췌 (P9 기록)

- **[fact]** `make_kc_excerpt.py`가 종목 전용 KC의 임계 필드를 전 종목에서 빠뜨리고 있었다. 이번 run에 수정했고 회귀 테스트를 추가했다. 그 뒤 5종목(NBIS·CRWV·CRCL·COIN·HOOD) arbiter를 다시 돌렸다(오케스트레이터 전달).
- **[fact]** 재실행 후에도 등급 후보는 바뀌지 않았다. CRCL·HOOD는 warning 단계를 처음으로 trigger와 따로 판정했다. COIN KC 4종에는 warning 정의 자체가 없다(stablecoin `cp_1001_kc_excerpt_rerun_data_gap`).
- **[fact]** **직전 run까지 종목 KC 판정은 임계 없이 이뤄졌다.** 직전 L4의 sc_15~17은 그 판정을 인용했다. 직전에 올린 esc_L4_1015_08(KC-HOOD-3 발췌 누락)은 이 결함의 증상이었다. **[inference/중]** 직전 산출물은 P9에 따라 고치지 않았다. 소급 재판정이 필요한지는 사람이 판단한다(esc_L4_0900_03).
- **[fact]** KC-COIN-3에 대한 '연방 한정' 서술은 오류였다. 실제 조건은 '(a) SEC·CFTC·DOJ 신규 제소' 또는 '(b) 기관 불문, 주요 사업 영업정지·인가 취소'다(stablecoin esc_1001_06).

---

## 5. 리밸런싱 뷰 (S6) — 시나리오 18건, 전부 사전 정의 KC·한도에 연결 (P11)

| ID | 트리거 (source) | 판정 | 이격 | 대상 |
|---|---|---|---|---|
| sc_01 | KC-1 | **met/confirmed (3회)** | +0.25%p 초과 | CRWV·IREN·MU·NBIS (상단 95.0) |
| sc_02 | KC-2 | not_met | 13.74pt | 6종목 |
| sc_03 | KC-3 | not_met | BTC 28,670.59 USD / VIX 8.74pt | COIN·CRCL·HOOD·IREN |
| sc_04 | KC-4 | not_met | 188.461B USD 미달 (경보 해석력 약함) | 6종목 |
| sc_05 | KC-5 | not_met | +2.92%p / +4.82%p | 6종목 |
| sc_06 | KC-6 | not_met/prov. | 산출 불가(입력 null) | 4종목 |
| sc_07 | KC-7 | not_met/prov. | 6,835,000,000 USD | 4종목 |
| sc_08 | KC-8 | not_met/prov. | 19,640,000,000 USD | 4종목 |
| sc_09 | KC-9 | not_met/prov. | 6.04 USD 미달, duration 두 해석 모두 미충족 | 4종목 (RATES 공유 — 중복 계상 금지) |
| sc_10 | KC-10 | not_met/prov. | 이벤트형 | IREN |
| sc_11 | 축 집중도 60%(초안) | **breach 6/8축** | +35.0pp | IREN |
| sc_12 | IREN 가격 라인 30/28 | 산출 불가 | 가격 피드 없음(5회차) | IREN |
| sc_13 | 레버리지 40% 규칙 | 비활성 | 분모 0 | — |
| sc_14 | 종목 KC 17건 파급 | 산출 불가 | 매핑 미정의 | — |
| sc_15 | KC-COIN-3 | not_met, (b)항 unresolved_fact | 이벤트형 | COIN(미보유) |
| sc_16 | KC-CRWV-3 | not_met | 경고까지 +0.86x(2.36x) / 정태 추정 +0.71x(2.21x) | CRWV(미보유) |
| sc_17 | KC-HOOD-3 | not_met | 산출 불가(주별 매출 기여 미공시) | HOOD(미보유) |
| sc_18 | **KC-CRCL-2 (신규)** | not_met/prov. | 산출 불가(회사 정의 분모 신규치 부재) | CRCL(미보유) |

- **[fact]** 가장 가까운 이격은 sc_01(초과), sc_11(초과), sc_05(TAIEX 여유 축소), sc_09다. 단위가 서로 달라 크기를 직접 비교할 수는 없다.
- **sc_15** — **[fact]** 발췌 결함을 고친 뒤 재판정했다. 남은 미결은 두 가지다. 미시간 항소(26-1693)의 사실관계, 그리고 예측시장이 '주요 사업'에 해당하는지다. 직전 L4가 쓴 '근거등급 게이트' 사유는 이 재정의로 대체한다. **[inference/중]** config 주석의 '연방 기관 + 영업상 중대로 한정'이라는 표현이 오독의 출처였을 수 있다.
- **sc_17** — **[fact]** 아직 오지 않은 일정이 있다. 미시간 청산 기한 10-09, SCOTUS 26-338 응답 10-14, 미주리 약 10-16이다. HOOD L2는 제6순회 판결을 적재하지 않았다.
- **sc_18** — **[fact]** 이번에 새로 넣었다. OUSD가 공식 출시됐고 실측 유통량($477.3M → $468.4M, USDC 대비 약 0.6%, grade 3~4)이 처음 공시됐다. KC 문언이 지목한 경쟁 경로가 처음 관측된 것이다. 3자 집계 계열은 판정 계열이 아니다(P4).

---

## 6. 축 집중도 경보 — ⚠️ **breach (8축 중 6축, 5회차 연속)**

| 축 | 노출 종목 수 | 보유 | 상단 | 연결 KC |
|---|---|---|---|---|
| AI_CAPEX | 4 | IREN | **95.0** | KC-6·7·8 |
| RATES | 7 | IREN | **95.0** | **KC-1(met)**·KC-9 |
| CRYPTO | 4 | IREN | **95.0** | KC-3 |
| GPU_SUPPLY | 3 | IREN | **95.0** | — |
| POWER_PERMIT | **1** | IREN | **95.0** | KC-10 |
| RISK_APPETITE | 6 | IREN | **95.0** | KC-2·4·5 |
| REGULATION · USDC_DISTRIBUTION_ECONOMICS | 3·2 | — | 0.0 | — |

- **[fact]** 임계 60은 config상 '⚠️초안'이다(esc_L4_0900_08).
- **[inference/강]** 판별력이 없다. 보유 종목이 IREN 하나라서 값이 95.0 아니면 0.0으로만 나온다. 이 경보는 축별 위험 순위를 알려 주지 않는다. 알려 주는 것은 **단일 포지션이 6축에 동시에 노출돼 분산이 없다는 사실**이다.
- **[fact]** 현재 met인 KC-1의 전달 축은 RATES다. 이 축에서 보유분은 IREN(-M)뿐이다. 반대 부호(+)인 CRCL·COIN·HOOD는 모두 미보유다. **[inference/중]** 그래서 장부 안에 이 노출을 상쇄하는 부분이 없다. 구조를 기술한 것이며 조정 제안이 아니다.
- **[fact]** POWER_PERMIT은 벡터상 노출 종목이 IREN 하나뿐인 축이다. 이번 한국 투자 재료가 닿는 축이 바로 이 축이다(§7).

---

## 7. 한국 대미 에너지 투자 반영 (사용자 요청 — 2026-09-30 발표)

> **[fact]** 이 섹션은 04_sector 3개 파일이 인용한 L2 Claim 범위 안에서만 쓴다. `00_user_sources` 원본은 열지 않았다(P17).

### (a) 사실 (등급 표기)

| 내용 | 등급 | confirmed | scope | Claim |
|---|---|---|---|---|
| **[fact]** Project Star: 텍사스 Encinal(La Salle County) 6,472MW 가스 복합화력, $22.3B, NextEra Energy Resources·Related. 인접 Related Digital 5GW DC에 직접 공급하고 잉여분은 계통에 보낸다. 테넌트는 특정되지 않았다 | **1** (NextEra 뉴스룸·PR Newswire·commerce.gov 역추적 성공) | ✔ | sector | c_20261001_IREN_4 · NBIS_5 · CRWV_4 |
| **[fact]** 1단계 1,952MW는 2029년 상업운전, 전체 가동은 2032년. 보도자료는 텍사스 주지사의 DC 자가발전 지침과 부합한다고 명시 | **1** | ✔ | sector | 위와 같음 |
| **[fact]** 원전 8기(최대 $120B)·알래스카 LNG($50B+)는 미확정. 총 최대 $200B, 연 $20B 상한. $350B 패키지(관세 25→15%)의 첫 프로젝트 | **3** (MU L2 기준) / 미확정분은 확정 사실 아님 | ✘ | sector | c_20261001_MU_14 |
| **[fact]** IREN·NBIS·CRWV 3사 모두 원문에 자사 언급이 없다. delta는 0이고 company_specific 승격은 거부됐다. MU는 반도체 언급 0건이며 Section 232는 별개 체계다. 크립토 3종은 noise로 처리했다 | 구조화 기록 | — | — | — |
| **[fact]** Encinal은 IREN ERCOT 사이트와 다른 카운티·송전권역이다 | IREN L2 inference/weak | ✘ | sector | c_20261001_IREN_5 |

**[fact]** 사용자가 주입한 sector 자료의 라벨이 종목마다 다르다(NBIS discard / IREN·CRWV sector Claim / 크립토 noise). 실질 처리는 같다(esc_L4_0900_19).

### (b) 노출 벡터 함의 — 변화는 '제안'으로만

- **POWER_PERMIT** — **[inference/중]** L3 ki_2의 해석은 이렇다. 텍사스는 대형부하의 계통 연결을 **동결하는 방향이 아니다**. 비용을 매기고 자가발전을 유도하는 방향이다. DC 모라토리엄 ③단계(계통연결+인허가동결)로 넘어간다는 신호는 없다. **[inference/약]** 다만 위험이 계통 연결에서 **현장 발전설비 인허가**로 옮겨 갈 가능성은 있다. 같은 관할에서 관측된 사례는 없고, NBIS Vineland 사례는 다른 관할이며 unconfirmed다. → **vcp_11**: 축 지표 문언에 '현장 자가발전 인허가' 경로를 감시 항목으로 같이 적을지 검토 요청. IREN -H의 부호·강도 변경은 제안하지 않는다.
- **ENERGY_DIRECT_COST (보류 축)** — **[fact]** 재평가 트리거 3개 중 충족된 것은 0건이다. **[inference/강]** 공급이 2029년 이후이고 종목 연결도 없어 ENERGY 축 신설 보류를 바꿀 재료가 아니다(vcp_04 증거 갱신).
- **AI_CAPEX** — **[inference/중]** 전력 희소성이 실제로 있다는 확인은 되지만, 희소성이 줄어든다는 뜻은 아니다. 2026~2028년 용량 공급에는 기여하지 않는다. 벡터 변경 제안은 없다.
- **경쟁·테넌트** — **[inference/약]** 5GW 캠퍼스의 테넌트가 정해지지 않았다. 그래서 3사에 고객 기회인지 경쟁 공급인지 판정할 수 없다(P5).
- **MU·크립토 3종** — **[fact]** 벡터에 영향이 없다.

### (c) 실포지션(IREN, 범위 [0.85, 0.95]) 관점 관측점 — 시나리오·한도·이격도 언어

| 연결 | 상태 | 관측점 |
|---|---|---|
| sc_10 (KC-10) | not_met/prov., 이격 산출 불가 | **[fact]** Project Star는 KC-10 문언이 말하는 관측(IREN 감축 분류, 사이트 전력접속·인허가 취소·보류)이 아니다. KC-10은 IREN 고유 1차 공시로만 판정한다 |
| sc_11 (축 집중도) | breach | **[fact]** 재료가 닿는 POWER_PERMIT 축은 노출 종목이 IREN 하나뿐이고 상단 95.0 대 임계 60(초안)이다 |
| sc_09 (KC-9) | not_met | **[fact]** 지표(브렌트 원유)와 무관하다. 이격 6.04 USD 미달에 영향이 없다 |
| 관측점 ① | — | **[inference/약]** PUCT 대형부하 규칙(MW당 $50,000 재무보증)의 1차 원문 확인. 현재 grade 4다. 확인되면 벡터 basis('MW당 $50K 담보')의 관측 기준이 된다 |
| 관측점 ② | — | **[inference/약]** ERCOT DC 감사 최종 결과(2026-12 경). 텍사스가 ③단계로 넘어가는지 판별할 자료다 |
| 관측점 ③ | — | **[inference/약]** IREN 사이트의 현장 발전설비 인허가 공시 여부. 현재 0건이다 |
| 관측점 ④ | — | **[fact]** Related Digital 캠퍼스 테넌트 공표 여부 |

### (d) 종목 시그널 근거 불가 명기

**[fact]** 이 섹션의 어떤 내용도 IREN·NBIS·CRWV·MU의 상향·하향 근거가 아니다. 섹터·매크로 재료는 종목 근거가 될 수 없고(P6), 포트폴리오 뷰도 종목 시그널 근거가 될 수 없다(P13). **[fact]** L3 neocloud는 '전력 제약 완화 → 특정 종목 상향'이라는 추론을 명시적으로 배제했다. **[fact]** 3사의 🔴🔴 후보는 이 재료와 무관한 KC-1 경로에서 나왔다. 이 재료는 확정·기각 판단에도 쓰지 않는다.

---

## 8. 상관 레이어 요약 (`05_correlation.json`)

**[fact]** 입력 config가 바뀌지 않았으므로 [CODE] 산출은 직전 회차와 필드 단위로 같다. pair_overlap 21쌍 중 '상'이 6쌍이다. KC 파급은 27건(매핑 10 / 미정의 17)이고 축 집중도는 8건이다. 수치형 상관계수는 쓰지 않았다(P14). **[fact]** 측정 체계에 따라 등급이 갈린다. 벡터 기준으로는 NBIS–CRWV·IREN 쌍이 모두 '상'이다. L3 카드 축 기준으로는 NBIS–CRWV가 '중', IREN 쌍이 '하'다. 두 체계는 서로 다른 질문에 답하므로 조정하지 않았다.

### 노출 벡터 변경 제안 — 11건 (부호·강도 변경 요구 0건, 자동 수정 0건)

| ID | 대상 | 상태 | 요지 |
|---|---|---|---|
| vcp_01 | IREN.CRYPTO basis | 이월 5회차 | 예약 문언 기준일 교체(채굴 종료 목표 2026-12 불변) |
| vcp_02 | NBIS.RATES | 이월 5회차 | 강도 재검토 — 신규 조달 0건으로 판정 불가 |
| vcp_03 | GPU_SUPPLY 축 | 이월 3회차 | 분해/축소 — CRWV 배정 경로만 관측 발생 |
| vcp_04 | KC-9 매핑·ENERGY_DIRECT_COST | 이월 4회차(monitoring) | 트리거 0/3 충족, Project Star 반영해도 유지 |
| vcp_05 | CRCL.RATES | 이월 3회차 | 강도 H 재확인 시점 = Q3 실적 |
| vcp_06 | USDC_DISTRIBUTION_ECONOMICS | 이월 2회차 | basis 다자화 + label '제로섬' 검토 — OUSD로 보강 |
| vcp_07 | COIN.REGULATION basis | 이월 2회차 | 예측시장 경로 병기(제6순회 판결) |
| vcp_08 | YIELD_BEARING 트리거 | 이월 2회차 | 날짜 앵커 소멸, $YLDS 수치 교체 |
| vcp_09 | CRWV basis 시점 | 이월 2회차 | '~2.2x' 대 2.36x 기준 분기 명기 |
| **vcp_10** | **OUSD_CONSORTIUM** | **신규** | 재평가 트리거('공식 출시 + 실측 유통량') 충족이 관측됨. CRCL은 순수 경쟁 노출, COIN은 내부 헤지라 순부호 미확정. 근거 grade 3~4라 강도 근거로는 부족. 승격 검토를 시작할지가 사람 판단 대상 |
| **vcp_11** | **POWER_PERMIT 지표** | **신규** | 현장 자가발전 인허가 경로를 감시 항목으로 병기할지 검토(한국 투자 재료) |

**[fact]** vcp_01~09는 config가 바뀌지 않았고 승인 큐에도 vcp 처리 기록이 없다. 그래서 전부 미처리 상태로 이월했다. **[fact]** 검토했지만 제안하지 않은 항목은 다음과 같다. ENERGY 축 신설, NBIS·CRWV POWER_PERMIT 등재, MU 관세 축, MU ip_litigation 축(종목 고유이므로 KC 정의 대상), CRCL 거버넌스 축(카드 축 사안), NBIS AIB 계약, CRWV 고객명.

---

## 9. 섹터 층 입력과 한계 — 3개 섹터 전부 방향 미산출

- **neocloud** — **[fact]** 공유 축이 6회차 만에 처음으로 0에서 2개가 됐다(funding_access·customer_concentration, NBIS–CRWV). 원인은 NBIS가 무뉴스 축에 neutral을 명시해 발행 규약이 맞춰진 것이다. funding_access의 low는 양쪽 모두 관측이 없어서 일치한 것이다. customer_concentration의 high는 CRWV만 고객명을 공시한 사건 비대칭이다. 부호 상충은 없고, 'high'는 집계기의 1:1 규칙이 만든 표기다. IREN은 여전히 공유 축이 0개다.
- **memory** — **[fact]** 강화된 3축은 섹터 공통의 가격 주도 성장에서 왔다. 약화된 ip_litigation 축은 MU 고유 요인이다. SK하이닉스의 라이선스 상태는 '미확인'으로 통일했다.
- **stablecoin** — **[fact]** prediction_market에서 허위 diverge가 2회 연속 나왔다. 원인은 두 가지다. COIN은 단일 슬롯, HOOD는 3분해로 축 범위가 다르다. 그리고 HOOD는 제6순회 판결을 적재하지 않았다. 축 명명 표준화(esc_L4_2209_03)의 증거가 쌓이고 있다.
- **[inference/강]** 섹터 층에서 포트폴리오 층으로 넘어오는 방향 정보가 계속 0이다. 그래서 시나리오는 전부 KC·한도 기반이다.

---

## 10. Thesis 정교화 후보 (S7) — **후보 8건만 기록, ThesisPatch 생성 0건**

> **07_thesis_patch는 thesis-refine 병렬 에이전트 산출물과 사람이 대조한다.** 이 목록은 04_sector에서 뽑은 후보일 뿐이다. 07_thesis_patch·승인 큐·thesis card는 쓰거나 고치지 않았다.

| ID | 종목 | 카드 필드 | 의존 |
|---|---|---|---|
| tpc_01 | COIN·HOOD | prediction_market 정의 범위 정렬 | 표준화 결정 |
| tpc_02 | IREN·NBIS·CRWV | 축 명명(조달·레버리지·마진·실행 계열) | 표준화 결정 |
| tpc_03 | MU | ip_litigation_risk 관측점(2차 ITC institution·피조사자 구성), SK하이닉스 '미확인' 표기 | — |
| tpc_04 | CRCL | 신규 축 후보 management_governance_succession | 표준화와 함께 검토 권고 |
| tpc_05 | CRCL | competition_ousd_consortium 기준선($477.3M → $468.4M) | — |
| tpc_06 | NBIS | capacity_delivery 3자 임차 경로 관측점 | — |
| tpc_07 | IREN | power_permit 관측점(감시 항목만, 방향 근거 아님) | — |
| tpc_08 | COIN | KC-COIN-3 인용 문언 정정 확인 | 카드 전문 확인(F20) 필요 |

**[inference/중]** 명명 정렬(tpc_01·02)과 축 추가(tpc_04)를 표준화 결정 없이 따로 집행하면 결합 실패가 굳어질 수 있다.

---

## 11. 검증

| 산출물 | layer | 결과 |
|---|---|---|
| `05_correlation.json` | correlation | **PASS** (1회차) |
| `06_portfolio.json` | portfolio | **PASS** (1회차) |

**[fact]** 이 md 파일에도 같은 금지 규칙(P14·P15)을 적용했다. KC·가격 라인의 사전 정의 문언은 JSON의 `predefined_consequence` 필드에만 원문으로 인용했다.

---

## 12. 🔴🔴 사람 확인 요청 + 근거 패키지 (CLAUDE.md §7)

**[fact]** 이 산출물로 종료한다. 후속 자동 실행은 없다. `default_action`은 `no_action`이다(P12).

### 명시: state 공백과 시스템 갭

**[fact]** `state/signals.json`은 여전히 KC-1 이전 등급을 보여준다(IREN 🟡·NBIS 🟡·CRWV 🟡·MU 🟠, as_of 2026-09-05, transitions 0건). **[fact]** 승인 큐에는 🔴🔴 결정을 기록할 유형이 없다. **[inference/중]** 따라서 이번 🔴🔴 후보는 새 판정이 아니다. 처리되지 않은 요청을 세 번째로 다시 올리는 것이다. **[fact]** 4건 중 종목 KC 훼손에서 나온 것은 0건이다. 한국 투자 재료와도 무관하다.

### 근거 패키지

| 항목 | 경로 | 등급 | 요지 |
|---|---|---|---|
| KC-1 판정 | `01_macro_kc.json#kc_status[KC-1]` + `analyst_intervention[KC-1]` | FRED api | **[fact]** 4.00 > 3.75, 3회 연속 재확인 |
| 결과 문언 ↔ 장부 | `kill_conditions.yaml#macro.KC-1` + `positions.yaml` | config | **[fact]** 실질 대상은 Edge(IREN) 조항 하나 |
| 🔴🔴 경로 | `04_sector/neocloud.json#macro_kc_candidate_note`, `memory.json#kc_separation_note` | L3 인용 | **[fact]** 4건 규칙1 단독. MU는 펀더멘털 🔴 하향 경로 병존 |
| 확정 등급·기록 경로 | `state/signals.json`, `state/pending_approvals.json` | state | **[fact]** transitions 0건 / 큐 전부 thesis_patch |
| KC 발췌 결함 | `stablecoin.json#cp_1001_kc_excerpt_rerun_data_gap`, `06_portfolio.json#company_kc_excerpt_defect_record` | L3 + 오케스트레이터 | **[fact]** 재실행 후 등급 불변. 직전 판정은 임계 없이 이뤄짐 |
| KC-9 duration | `01_macro_kc.json#analyst_intervention[KC-9]` | FRED api | **[fact]** 두 해석 모두 미충족, 정의 미확정 |
| 축 집중도 | `05_correlation.json#axis_concentration` | [CODE] | **[fact]** 6/8축, 95.0 대 60(초안) |
| 한국 대미 투자 | `06_portfolio.json#korea_us_energy_investment` | grade 1 / 3 | **[fact]** scope=sector, 종목 근거 불가 |

### 요청 결정사항

1. **[fact]** 🔴🔴 후보 4건 확정·기각 — MU의 이중 경로 대조 포함 (esc_L4_0900_01, top)
2. **[fact]** 🔴🔴 결정 기록 경로 설계 — 승인 큐에 해당 유형 없음 (esc_L4_0900_02, top)
3. **[fact]** 직전 run 종목 KC 판정의 소급 재판정 필요 여부 + COIN warning 단계 정의 (esc_L4_0900_03)
4. **[fact]** KC-9 duration 정의(연속/누적) (esc_L4_0900_04)
5. **[fact]** 축 명명 표준화 — tpc_01·02 순서와 연동 (esc_L4_0900_05, top)
6. **[fact]** KC-COIN-3 (b)항 해당성 판단 + config 주석 문언 정리 (esc_L4_0900_06)
7. **[fact]** MU·IREN 종목 KC 정의 (esc_L4_0900_07)
8. **[fact]** 축 집중도 임계 60% 확정 (esc_L4_0900_08)
9. **[fact]** 벡터 제안 11건(vcp_01~11) 처리 (esc_L4_0900_12)
10. **[fact]** ThesisPatch 후보 8건과 07_thesis_patch(병렬 산출) 대조

### 에스컬레이션 총괄 — 20건 (top 3 / high 5 / medium 8 / low 4)

| ID | 우선 | 요지 |
|---|---|---|
| 01 | top | 🔴🔴 후보 4건 — 3회 연속 미기록 |
| 02 | top | 🔴🔴 결정 기록 경로 부재(시스템 갭) |
| 05 | top | 축 명명 표준화 — 증거 누적 |
| 03 | high | KC 발췌 결함의 과거 판정 영향 |
| 04 | high | KC-9 duration 정의 |
| 06 | high | KC-COIN-3 사실관계 + 서술 정정 |
| 07 | high | MU·IREN 종목 KC 부재 |
| 08 | high | 축 집중도 임계 초안 |
| 09 | medium | 1차 도메인 sources.yaml 미등재 |
| 10 | medium | 집계기 1:1 'high' 표기(2개 섹터 재현) |
| 11 | medium | HOOD 제6순회 판결 미적재 |
| 12 | medium | 벡터 제안 11건 |
| 13 | medium | 종목 KC 17건 매핑 미정의 |
| 14 | medium | KC-4 임계 기능 약화 |
| 15 | medium | IREN 가격 라인 이격 산출 불가(5회차) |
| 16 | medium | KC-6 입력 null |
| 17 | low | CRCL 신규 축 제안 |
| 18 | low | 예측시장 공통 노출 재분류 |
| 19 | low | P6/P13 경계 표기 규약 |
| 20 | low | USDC 유통량 상충·OUSD 출시일 불일치 |

**[fact]** 위 결정들이 내려지기 전에 이 시스템이 자동으로 수행할 후속 단계는 없다.
