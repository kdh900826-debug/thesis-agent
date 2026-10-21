# HOOD 소급 확인 (retrospective coverage check) — run 20260905_0839

발단: L3 stablecoin(esc_0618_03) → L4(06_portfolio.json)가 이관한 "과거 run 미포착 정황 3건". 카드(`state/thesis_cards/HOOD.yaml`, as_of 2026-08-15) 전문을 F20에 따라 확인 후 진행. 카드 axes: `aua_inflow` / `arpu_mix` / `crypto_cycle` / `prediction_market` / `rates_income` (5개). risks 5개.

---

## 1. 2026-07-29 Q2 실적콜 — 예측시장 매출 발언

**확정 사실 (1차 자료 원문 인용)**

- 출처: SEC 8-K (2026-07-29 제출, accession 0001783879-26-000113) Exhibit 99.1 주주서한. `sec.gov` — **grade 1**.
  > "event contracts revenue of $156 million, up over 10x" / "Transaction-based revenues increased 44% year-over-year to $776 million, primarily driven by event contracts revenue of $156 million, up over 10x, options revenue of $342 million, up 29%, and equities revenue of $129 million, up 95%, partially offset by cryptocurrencies revenue of $100 million, down 38%."
  > "Rothera... over 3.5 billion contracts traded to date" / 2분기 중 "13.6 billion contracts traded"
- 실적콜 구두 발언 교차확인(**grade 2**, 독립 3자 전사 2건 — The Motley Fool, The Globe and Mail): 두 전사 모두 "Event Contracts Revenue -- $156 million, representing a tenfold increase year over year with 13.6 billion contracts traded during the quarter"를 동일 인용. 다만 화자 귀속이 전사마다 다름(Fool: CFO Shiv Verma / Globe and Mail: CEO Vlad Tenev) — 수치 신뢰도와 무관한 화자 표기 불일치로 별도 unconfirmed 기록.
- **비중(%)은 회사가 직접 언급하지 않음** — $156M/$776M ≈ 20.1%는 본 에이전트의 파생 계산(사실과 추론 분리 표기).

**P3 판정**: 매출 라인 항목(사업부별 매출 breakdown)을 직접 변화시킴 — 노이즈 아님, 승격 대상.

**카드 축 매핑**: 기존 `prediction_market` 축("예측시장 — 매출 기여 vs 규제 리스크")에 정확히 대응. **신규 축 불필요.** 이 축이 신설된 이래 최초로 grade1 매출 실측치(P7 3단계, 매출 인식 확인)가 확보된 사례 — 지금까지는 애널리스트 온체인 추정(grade3·4)뿐이었음.

**패치 제안 요건 (승인은 사람)**: 대상 필드 `key_metrics`("예측시장 매출·거래량") 및 `conclusion` — before 후보: 현재 카드는 "매출 구성이... 규제 미확정 상품에 걸쳐 있어" 정도의 정성 서술만 있음. 근거 Claim: `c_retro_HOOD_001`(grade1), `c_retro_HOOD_003`(grade2). counts 영향 없음(목록 항목 추가가 아니라 수치 보강 성격 — 실제 패치 시 `expected_after.counts` 요건은 addition 여부에 따라 결정 필요).

**과거 run이 왜 놓쳤나**: 개별 판단 오류가 아니라 **run 스케줄/lookback-window 설계의 구조적 공백**. 최초 run(20260815_1408)의 조회기간이 `since=2026-08-08`로 07-29를 원천적으로 포함하지 않았고, 다음 run(20260820_1932)은 뒤늦게 발견했지만 "직전 run 이후 신규"라는 rolling-window 기준상 기간 외로 분류해 unconfirmed 이관만 하고 Claim화하지 않았으며, 09-05 run은 Morgan Stanley 재인용을 다시 노이즈로 폐기했다. 3회 연속으로 "기간 외"라는 사유로 통과된 것 — 최초 실적일을 커버하는 창이 애초에 존재하지 않았다.

---

## 2. RVII (Robinhood Ventures Fund II) IPO — 2026-08-13

**확정 사실**

- EDGAR 공시 체인(전부 `sec.gov`, **grade 1**, CIK 0002131040): N-2(2026-06-30, 최초 등록) → N-2/A(07-22, 08-03×2, 정정) → **8-A12B**(2026-07-20, 거래소 상장용 증권 등록) → **424B1**(2026-08-13, 최종 투자설명서 — 확정 조건 공시).
- 확정 조건: 800만주 @ $25.00, 총 공모대금 $2.0억(초과배정 전량 행사 시 최대 $2.555억), NYSE 티커 `RVII`, 결제/상장 2026-08-14.
- 사업 성격: "externally managed... closed-end company... elected to be regulated as a business development company (BDC) under the Investment Company Act of 1940." 투자전략은 Y Combinator 출신 비상장 스타트업 중심 초기·성장단계 포트폴리오.
- 투자자문사: Robinhood Ventures DE, LLC — **HOOD의 전액출자 자회사**. 자문보수: 순자산 연 2.00%(분기 지급) + 실현자본이득 20% 성과보수.
- **HOOD 손익 연결 구조**: RVII는 HOOD(CIK 0001783879)와 별개의 SEC 등록법인(CIK 0002131040)으로, 투자자는 RVII 주식을 직접 매수 — **HOOD 재무제표에 RVII 자체가 연결되지 않는다.** HOOD에 귀속되는 것은 자회사가 받는 자문보수뿐. 순자산 $2.0~2.3억 기준 연 기본관리보수 약 $400만~460만 추정(2분기 거래기반매출 $776M 대비 극히 미미).
- Fund I(RVFI, CIK 0002085091)이 이미 존재 — RVII는 두 번째 펀드로, 후속 펀드가 이어지면 소규모 수수료 수입이 누적될 수 있는 신규 계열.

**P3 판정**: RVII 자체의 자금조달·상장은 HOOD의 매출·마진·현금흐름을 직접 변화시키지 않는다(자문보수만 잠재적으로 영향, 아직 공시 없음) — 상장/출시 사실 자체는 P7상 "존재" 단계이며 "매출 전환"이 아님(P7 원칙, 종목 특이 주의사항과 일치).

**카드 축 매핑**: 기존 5개 축 어디에도 명확히 대응되지 않음. `arpu_mix`(크립토/예측시장/이자수입 3원 구성)에 억지로 넣기엔 카드 문언과 불일치. **신규 축 후보**로만 제안 가능 — 다만 현재 규모가 극소하여 즉시 신설 실익은 낮고, Fund I·II 누적 추이 감시용으로만 의미가 있음. 최종 판단은 사람 몫.

**패치 제안 요건**: (a) `axes`에 신규 축 추가 여부(예: `am_fee_income` — "자산운용 수수료 수입(RVII 등 펀드 스폰서십)") — before: 축 5개 리스트(counts=5), after 후보: 6개(counts=6, 신규 axis 추가). 근거 Claim: `c_retro_HOOD_005`~`007`(모두 grade1, 단 매출 인식 실측은 unconfirmed). (b) 또는 `key_metrics`/`catalysts`에 감시 항목으로만 추가(축 신설 대신 저강도 반영) — 두 옵션 모두 사람 승인 필요.

**과거 run이 왜 놓쳤나**: 이 항목은 사실 **완전히 놓친 것이 아니다.** 최초 run(20260815_1408)이 이미 grade1로 포착(`c_20260815_HOOD_005`)해 `arpu_mix` 축에 "P7 1단계 존재"로 반영한 바 있다. 그러나 카드에 대응 축이 없어 이 관측은 그 run의 산출물 파일에만 남았고, 후속 run은 신규 발표가 없으면 Delta를 재생성하지 않으며 P17 격리 규칙상 L2가 과거 `02_company/*.json` 원문을 열람할 수 없어 "이전에 포착됐는지"를 스스로 확인할 방법이 없었다. 그 결과 20260905_0618 run은 "직전 두 run에서도 흔적이 없다"고 기록했는데 이는 **부정확한 진단**이다 — 정확히는 "축이 없어 승계 경로가 끊겼고, 격리 규칙상 과거 기록과 대조가 불가능했다"이다. 개별 리서치 실패가 아니라 rolling-window + P17 격리 조합이 만든 구조적 유실이다.

---

## 3. UK 크립토 출시 (Bitstamp 경유) — 2026-08-10

**확정 사실**

- 출처: `robinhood.com` 공식 뉴스룸 (**grade 1**, config/sources.yaml 등재 도메인). Bitstamp UK Ltd.(FCA 등록 crypto-asset service provider) 경유, 50종 이상 자산(BTC·ETH·XRP·Hyperliquid 등), 거래수수료 0(계정유지·수탁수수료 없음), FX 스프레드 0.1%부터. 생성형AI 'Robinhood Cortex Digests for Crypto' UK 동시 출시. 기존 UK 주식·옵션·선물·ISA 라인업에 병행.
- Bloomberg·The Block 등 복수 2차 매체(grade 3)로 날짜·구조 교차확인.
- 실제 거래대금·매출 기여 수치는 **어떤 자료에도 없음** — unconfirmed.

**P3 판정**: 출시 발표 자체는 매출·가이던스·마진·현금흐름을 아직 변화시키지 않음(P7 1단계, 발표=존재이지 매출 기여 아님). 노이즈는 아니나(신규 지역 진출은 promote 대상 성격) 등급 근거로는 사용 불가.

**카드 축 매핑**: 기존 `crypto_cycle` 축("크립토 매출 비중 — KC-3 연동")의 하위 요소(국제 확장)로 대응 가능. **신규 축 불필요.**

**패치 제안 요건**: `key_metrics`/`catalysts`에 "국제(UK 등) 크립토 확장" 항목 명시 추가 여부 — before: catalysts 4개 항목(counts=4), after 후보 5개. 근거 Claim: `c_retro_HOOD_008`(grade1).

**과거 run이 왜 놓쳤나**: 이 건은 앞의 두 건과 성격이 다르다 — 08-10 사건은 최초 run(20260815_1408)의 조회기간(since 2026-08-08) **내부**에 있었음에도 그 run의 source-ingest(EDGAR+웹검색) 단계가 놓쳤다. 창 설계나 카드 축 부재 문제가 아니라 **순수한 리서치 커버리지 누락**이며, 이후 두 run(08-20, 09-05)도 소급 발견하지 못했다.

---

## 종합

세 건 모두 원문 1차 자료(SEC EDGAR 2개 계열 + 회사 공식 보도자료 1건)로 사실관계를 확정했으며, evidence_grade는 1(주력)·2(실적콜 구두 인용 교차확인) 수준으로 P4 기준을 충족한다.

- **1건(Q2 예측시장 매출)**은 기존 `prediction_market` 축에 정확히 대응하고, 이 축 최초의 grade1 매출 실측치라는 점에서 축의 신뢰도를 유의미하게 높이는 재료다.
- **1건(UK 크립토)**은 기존 `crypto_cycle` 축 하위로 무리 없이 흡수되며 아직 존재 단계(P7-1)에 머문다.
- **1건(RVII)**은 기존 축 어디에도 깔끔히 대응되지 않고, 신규 축 신설 여부는 등급 확정과 마찬가지로 사람이 판단할 사항이다 — 다만 규모가 현재 극소(연 추정 $400만대)여서 시급성은 낮다.

**HOOD 시그널(현행 🟡) 재판정 필요성에 대한 후보 의견 (등급 확정은 사람)**: 세 건 중 재판정 트리거로 가장 유력한 것은 1건(Q2 예측시장 매출 grade1 확정)이다 — 이는 P2가 요구하는 "확정된 매출 수치"이며 실제로 크립토·주식 매출을 상회하는 규모로 매출 mix의 질적 개선(다각화 성공) 근거가 된다. 다만 (a) 이 수치는 이미 5주 이상 지난 07-29 시점 자료이고 09-05 run이 이미 그 파생 재인용(애널리스트 PT 근거)까지는 알고 있었다는 점, (b) 월드컵 등 일회성 이벤트 기여분의 분리가 안 돼 있다는 점, (c) 규제 리스크(prediction_market 축의 반대편, KC-HOOD-3)가 별개로 여전히 살아있다는 점에서 단독으로 상향을 정당화하기보다는 **다음 Q3 실적에서 매출 잔존율을 확인하는 것을 전제조건으로 붙이는 정도가 적절**하다는 것이 본 에이전트의 후보 의견이다. RVII·UK 크립토 2건은 아직 P7 1~2단계에 머물러 있어 그 자체로는 재판정 근거가 되지 못한다(종목 특이 주의사항 — 존재≠매출 전환).
