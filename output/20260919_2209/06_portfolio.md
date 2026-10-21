# L4 포트폴리오 통합 뷰 — run 20260919_2209

- **as_of**: 2026-09-19T23:10 / **staleness_days**: 0 / **reused_from**: 없음
- **produced_by**: cio-portfolio (L4)
- **default_action**: `no_action`
- **[fact]** 본 문서는 시나리오·한도·이격도만 제시한다 — 매수·매도 지시가 아니다(P15·F18). 목표 비중 단일값과 시점 지시를 포함하지 않는다.
- **[fact]** 등급·행동·임계 확정은 전부 사람의 권한이다(CLAUDE.md §9).
- **[fact]** 모든 주장 문장은 `[fact]` 또는 `[inference/강도]`로 태깅한다(P1).

---

## 0. 한 문단 요약

**[fact]** 2026-09-16 FOMC의 25bp 인상(목표범위 3.75~4.00%, 표결 12-0)으로 KC-1이 4개 run 연속 경계 접촉 끝에 최초로 임계를 초과했고, FRED DFEDTARU 대사로 `confirmed`가 확정됐다. **[fact]** 그 결과 arbiter 규칙1(Kill 우선)이 IREN·NBIS·CRWV·MU 4종목에서 발동해 🔴🔴 **후보**가 생성됐다 — 4건 전부 매크로 전이 단일 경로이며 종목 thesis 훼손에 기인한 것은 0건이다. **[fact]** 실제 보유는 IREN 단독이며 나머지 3건은 비중 0이다. **[fact]** 본 회차는 🔴🔴 포함 run이므로 자동 실행 없이 사람 확인 요청 + 근거 패키지로 종료한다(CLAUDE.md §7).

---

## 1. 입력과 격리 (P16·P17)

| 입력 | as_of | staleness_days | 비고 |
|---|---|---|---|
| `01_macro_kc.json` | 2026-09-19T22:12 | 0 | |
| `04_sector/neocloud.json` (+aggregate) | 2026-09-19 | 0 | |
| `04_sector/memory.json` (+aggregate) | 2026-09-19 | 0 | 파일 내 `reused_from` 기재는 직전 회차 참조분 |
| `04_sector/stablecoin.json` (+aggregate) | 2026-09-19 | 0 | |
| `05_correlation.json` | 2026-09-19T22:58 | 0 | 본 회차 재실행분 |
| `config/correlation_matrix.yaml` | 2026-08-15 | 35 | `status: active` — U4 중단 사유 아님 |
| `config/positions.yaml` | 2026-09-19 | 0 | 사용자 확인으로 as_of 갱신 |
| `config/kill_conditions.yaml` | 2026-08-15 | 35 | |
| `03_signal/*.json` | 2026-09-19 | 0 | **등급 후보 값 확인 전용** |

**[fact]** `02_company/*` 원문과 `state/thesis_cards/*`는 로드하지 않았다(P17). **[fact]** `03_signal`은 후보 등급 값 확인 목적으로만 열람했고 개별 종목 근거로 인용하거나 수정하지 않았다(P13).

---

## 2. 상관 레이어 [CODE] 재실행 (P9)

**[fact]** 기존 `05_correlation.json`은 22:15 생성분으로 `03_signal` 산출 이전 시점이었다. **[fact]** 재실행 전 원본을 `_05_correlation_preSignal_backup.json`으로 보존했다.

- 실행: `correlation_map.py --run-id 20260919_2209 --out output/20260919_2209/05_correlation.json`
- **diff 판정: 변화 없음**
- **[fact]** 원시 diff의 차이는 ① 최상위 `as_of`(22:15→22:58) ② `shared_axes` 배열 원소 순서뿐이다. 배열 순서를 정규화하고 `as_of`를 제외한 구조 비교 결과 두 산출은 동일했다 — pair_overlap 21쌍 등급·공유 축, KC 파급 27건, 축 집중도 8건, 매핑 커버리지(산출 10 / 미정의 17)가 전부 일치한다.
- **[inference/강]** `03_signal`은 상관 [CODE]의 입력이 아니다 — 스크립트는 `correlation_matrix.yaml`·`positions.yaml`·`kill_conditions.yaml`만 읽는다. 이 재실행은 산출 갱신이 아니라 시점 정합성 확인이었다.

### pair_overlap 신뢰도 상한 (고정 한계 문구)

**[fact]** pair_overlap의 공유 축은 `correlation_matrix.yaml`의 8개 축 위에서만 계산되며, 종목 카드의 축 체계와는 별개 집합이다. **[fact]** L3 보고 기준 카드 축 공유도는 neocloud 0/14, stablecoin 0/18(4 run 연속)이다. **[fact]** stablecoin에서 CRCL·COIN이 **동일한 2026-09-15 클로처 부결 사실을 같은 방향(weaken)으로** 매핑했으나 축 이름이 `regulation_sector_legislation` / `regulation`으로 달라 집계에서 분리됐다 — 결합 실패의 직접 증거다. **[inference/강]** 따라서 pair_overlap 등급은 사람이 수기로 정의한 벡터가 옳다는 가정 위에서만 성립하고 카드 축 체계로 교차검증되지 않는다. **신뢰도 상한 = 벡터 정의의 정확성.**

**[fact]** 본 레이어는 수치형 상관계수를 산출·표기하지 않았다(`coefficient_used: false`, P14).

---

## 3. 노출 벡터 변경 제안 [LLM] — 5건, 자동 수정 0건

**[fact]** `config/*.yaml`은 사용자 직접 편집 영역이다 — 제안만 기록했고 파일을 수정하지 않았다(CLAUDE.md §9). **[fact]** 어떤 제안도 개별 종목 시그널 근거로 사용되지 않았다(P13).

| ID | 대상 | 상태 | 요지 | 근거 Claim |
|---|---|---|---|---|
| vcp_01 | `IREN.CRYPTO` (+M) | 이월·미해소 | basis의 '8/27 재평가 예약' 문언 기준일 경과. 부호·강도 변경 근거 없음 | **0건** — `neocloud.json#axis_view[btc_mining]` null_observation (P5) |
| vcp_02 | `NBIS.RATES` (-M) | 이월·미해소 | 창 내 NBIS 신규 채무 발행 0건 → KC-NBIS-3 스프레드 미산출, 3사 비교쌍 부재 | `c_20260919_CRWV_1·2·3·4·13·14` (전부 CRWV 측 — NBIS 강도 변경 근거로는 부적격, P6) |
| vcp_03 | `axes.GPU_SUPPLY` 정의 | **신규** | 한 축이 '배정 접근권(순)'과 '감가·담보(역)' 두 반대 경로를 겸함 → P8 분해 검토 | `c_20260919_CRWV_8·9·10·12` |
| vcp_04 | KC-9 축 매핑 | 이월·감시 | KC-9→RATES 매핑 유지 제안. ENERGY_DIRECT_COST 재평가 트리거 3개 중 충족 0건 | **0건** (트리거 미충족, P5) |
| vcp_05 | `CRCL.RATES` (+H) | **신규·전제 정정** | L3가 받은 '벡터 미정의' 전제는 오류 — 실제로 `+H`로 정의돼 있다 | `c_20260919_CRCL_8` |

**vcp_03 상세** — **[fact]** 축 label이 'GPU 공급·감가'이고 indicators가 '배정 일정'·'감가상각 정책' 두 가지다. IREN·NBIS basis는 배정 경로, CRWV basis는 감가·담보 경로다. **[fact]** 본 회차 CRWV `gpu_priority` 축은 strengthen(2026-09-16 멀티랙 NVIDIA Vera Rubin NVL72 가동)인데 같은 종목의 벡터 부호는 `-H`다. **[inference/강]** 벡터가 틀린 것이 아니라 두 경로가 한 축에 합쳐져 있어 관측이 벡터에 대사되지 않는 것이다. **[fact]** MU는 2026-08-15에 같은 사유로 제거된 전례가 있으나 단순 제거는 CRWV 담보 경로(KC-CRWV-3 연동) 정보 손실을 낳는다 — 분해와 축소 중 선택은 사람 판단이다.

**vcp_05 상세** — **[fact]** L3 stablecoin `esc_2209_05`는 "오케스트레이터 전달에 따르면 correlation_matrix 벡터에 CRCL 금리 순방향 노출이 정의돼 있지 않다"를 전제로 제기하면서 P17상 스스로 확인 불가함을 명시했다. **[fact]** 본 레이어가 config를 직접 확인한 결과 `CRCL.RATES = {sign:+, strength:H}`로 정의돼 있다. **[fact]** 따라서 간극은 벡터 결손이 아니라 **하위 계층에 전달된 전제의 오류**다. **[fact]** 기록은 삭제하지 않고 정정 사유와 함께 보존한다(P9). **[inference/중]** 남는 실질 논점은 벡터 강도 H와 CRCL L2의 inference 강도 low 사이의 비대칭이나, 전자는 구조 논거·후자는 창 내 1차 자료 부재에서 온 것이라 서로 모순되지 않는다.

---

## 4. 포지션 현황 (`positions.yaml` as_of 2026-09-19, staleness 0)

| 종목 | 티어 | 비중 범위 |
|---|---|---|
| **IREN** | Edge | **[0.85, 0.95]** |
| 현금 | — | [0.05, 0.15] |
| MU | Base | [0.0, 0.0] |
| NBIS · CRWV | — | [0.0, 0.0] |
| CRCL · COIN · HOOD | Next | [0.0, 0.0] |

**[fact]** 레버리지 미사용. v32의 'Base 현금 대비 40% 상한' 규칙은 Base(MU) 미보유로 **비활성**이다.

**이진 축퇴** — **[fact]** 보유 종목이 1개이므로 축 집중도의 `weight_pct_upper`는 95.0 또는 0.0 두 값만 취한다. **[inference/강]** 축 간 상대 비교의 판별력이 구조적으로 없다(3회차 연속). **[inference/중]** 그럼에도 남는 정보는 하나 — 단일 포지션이 8축 중 6축에 동시 노출돼 있어 어떤 축이 움직여도 장부 전체가 같이 움직인다. 즉 이 경보는 **축별 순위가 아니라 분산 부재**를 가리킨다.

---

## 5. 시그널 등급 (P13 — 이월 인용, 수정 없음)

| 종목 | 직전 | 후보 | 전이 후보 | 경로 | 보유 |
|---|---|---|---|---|---|
| IREN | 🟡 | **🔴🔴** | kill_priority_candidate | KC-1 전이(규칙1) | ○ |
| NBIS | 🟡 | **🔴🔴** | Kill 우선 트리거(rule 1) | KC-1 전이(규칙1) | ✕ |
| CRWV | 🟡 | **🔴🔴** | Kill 후보(규칙1) | KC-1 전이(규칙1) | ✕ |
| MU | 🟠 | **🔴🔴** | kill_priority_candidate | KC-1 전이(규칙1, 종목 KC 미정의) | ✕ |
| CRCL | 🔴 | 🔴 | maintain | — | ✕ |
| COIN | 🟠 | 🟠 | maintain | — | ✕ |
| HOOD | 🟡 | 🟡 | maintain | — | ✕ |

**[fact]** 위 값은 `03_signal` 산출물에서 그대로 이월한 것이며 본 레이어는 어떤 등급도 변경·제안·소급 수정하지 않았다(P13). **[fact]** 전부 후보이며 확정은 사람의 권한이다. **[fact]** 🔴🔴 4건 전부 종목 thesis 훼손이 아니라 매크로 KC-1 전이다. **[inference/강]** 포트폴리오 층위에서 이 4건은 독립된 4개 사건이 아니라 **하나의 매크로 사건이 4개 종목으로 전이된 것**이다 — `05_correlation.json`의 KC-1 파급 집합(CRWV·IREN·MU·NBIS, RATES 축)과 정확히 일치한다.

---

## 6. 리밸런싱 뷰 (S6) — 시나리오 14건, 전부 사전 정의 연결

**[fact]** 14건 전부 사전 정의된 KC 또는 config 한도에 연결돼 있다 — `source`가 빈 시나리오는 0건이다(P11). **[fact]** 섹터 방향에서 유도한 시나리오는 **0건**이다(3개 섹터 전부 방향 미산출) — 커버리지 결손이지 위험 부재가 아니다(P5).

| ID | 트리거 | 연결 | 판정 | 이격 |
|---|---|---|---|---|
| sc_01 | FFR > 3.75% | KC-1 | **met / confirmed** | 임계 대비 **+0.25%p 초과** |
| sc_02 | VIX ≥ 30 | KC-2 | not_met / confirmed | 15.19pt 여유 |
| sc_03 | BTC < 55,000 AND VIX ≥ 25 | KC-3 | not_met / confirmed | BTC 26,235 USD·VIX 10.19pt 여유 |
| sc_04 | ON RRP ≥ 200B AND VIX ≥ 25 | KC-4 | not_met / confirmed | 산출되나 해석 불가(잔고 고갈) |
| sc_05 | TAIEX 20dma 하회 AND 1M 음전환 | KC-5 | not_met / confirmed | +2.0%p · +5.0%p 여유 |
| sc_06 | SDLLMTK ≤ -30%(2주) | KC-6 | not_met / provisional | 26.8%p 여유 |
| sc_07 | 하이퍼스케일러 합산 FCF < 0(2분기) | KC-7 | not_met / provisional | 68.35억 USD 여유 |
| sc_08 | MSFT FCF < 0 | KC-8 | not_met / provisional | 196.4억 USD 여유 |
| sc_09 | brent ≥ 120(1개월 지속) | KC-9 | **met / provisional — 조건부** | 가격 +10.8 USD 초과 / duration 미충족 |
| sc_10 | IREN 계약용량 10%+ 강제감축·인허가 취소 | KC-10 | not_met / provisional | 산출 불가(이벤트형) |
| sc_11 | 축 집중도 > 60% | config 한도 | **breach — 8축 중 6축** | **+35.0pp 초과** |
| sc_12 | IREN 종가 30 / 28 USD | config price_lines | 산출 불가 | 입력에 가격 피드 부재 |
| sc_13 | 레버리지 > Base 현금 40% | config(v32) | **비활성** | 분모 0 |
| sc_14 | 종목 KC 17건 | config#company | 파급 산출 불가 | 축 매핑 미정의 |

### sc_01 — KC-1 (핵심)

**[fact]** 판정: `met / confirmed`. FFR 4.00 > 임계 3.75, FOMC 2026-09-16 표결 12-0, FRED DFEDTARU api 대사 완료. 직전 4개 run 연속 '이격 0.00pp 경계 접촉' 끝에 최초 초과.

> **사전 정의 결과 문언(인용)** — `config/kill_conditions.yaml#macro.KC-1.consequence`:
> **"레버리지 전액 해제 + Edge/Next 50% 축소 검토"**

**[fact]** 위 문언은 **config의 원문 인용**이며 본 에이전트가 작성한 지시가 아니다. **[fact]** 사전 정의 문언의 인용과 에이전트의 지시는 다르다 — 본 에이전트는 어떤 행동 동사·목표 비중 단일값·시점도 생성하지 않았다(P15·F18).

**현 장부와의 대응관계(사실 기술)**

| 문언 구성 | 현 장부 상태 | 대응 |
|---|---|---|
| 레버리지 전액 해제 | **[fact]** 레버리지 미사용. Base 미보유로 v32 레버리지 규칙 비활성 | **해당 사항 없음** — 해제할 대상이 존재하지 않는다 |
| Next 50% 축소 검토 | **[fact]** CRCL·COIN·HOOD 전부 미보유(비중 0) | **대상 없음** |
| Edge 50% 축소 검토 | **[fact]** IREN = Edge, [0.85, 0.95] 보유 | **유일한 실질 대상** |

**[fact]** 위 표는 사전 정의 문언과 현 장부의 사실 대조다 — 문언의 실행 여부·범위·시점은 전부 사람의 판단이다(CLAUDE.md §9, P15). **[fact]** KC-1은 매크로 층위 판정이며 개별 종목 시그널의 근거로 사용되지 않는다(P6·P13).

### sc_09 — KC-9 (조건부, 발동 아님)

**[fact]** brent 130.8 > 임계 120(as_of 2026-09-15, stale_days 3 = 한도 3). **[fact]** 임계 상회 관측일은 2026-09-10(120.98)·09-14(121.25)·09-15(130.8)이고 09-11은 118.06으로 하회했다. **[fact]** `all_of` 조건의 duration '1개월 지속'이 충족되지 않았다 — 최초 상회 이후 9일, 연속 구간으로는 2거래일. **[fact]** 사람 override 제안은 `not_met`(경고 유지)이며 지속 시한은 **2026-10-10**이다. **[fact]** 본 레이어는 KC-9를 **발동으로 취급하지 않고 조건부로만 연결**했다. **[fact]** 자동 출력의 `met` 값은 유지한다(P9 — 기록 삭제 금지).

**[fact] 이중 계상 방지** — KC-1과 KC-9는 RATES 축을 공유하고 파급 종목 집합이 동일하다(`shared_axis_kc_groups[RATES]`) — 축 집중도에서 이 중복을 두 번 세지 않는다. **[fact] 구조적 공백** — 브렌트의 비(非)금리 전달 경로(도매 전력·가스)는 RATES 축이 포착하지 않으며 7종목 전부 전력 단위원가 기준 부호 판정 근거가 미확보다.

### 기타 주의 시나리오

- **sc_04 (KC-4)** — **[fact]** ON RRP 단위 오류 의심은 본 회차에 해소됐다(환산 버그가 아니라 실제 잔고 고갈). **[inference/중]** $200B 임계는 현 국면에서 사실상 도달 불가 구간이므로 이 KC는 **유동성 경보로 작동하지 않는다**.
- **sc_13** — **[inference/중]** KC-1·KC-2의 사전 정의 문언이 공통 참조하는 '레버리지'가 현 장부에 없는 원인이 이 규칙의 비활성이다. 즉 **KC-1 발동의 사전 정의 결과 중 절반은 구조적으로 무효**이고 남는 것은 Edge 조항뿐이다.
- **sc_14** — **[fact]** MU는 종목 KC 17건에도 포함되지 않는다(KC-MU-* 4 run 연속 미정의). 종목 층위 안전장치 부재가 매크로 전이로 대체되는 구조가 반복됐다.

---

## 7. 축 집중도 경보 — **breach (8축 중 6축)**

| 축 | 축 내 종목 수 | 보유 종목 | 비중 상단 | 임계(60) 초과 |
|---|---|---|---|---|
| RATES | 7 | IREN | **95.0** | ✔ |
| RISK_APPETITE | 6 | IREN | **95.0** | ✔ |
| AI_CAPEX | 4 | IREN | **95.0** | ✔ |
| CRYPTO | 4 | IREN | **95.0** | ✔ |
| GPU_SUPPLY | 3 | IREN | **95.0** | ✔ |
| POWER_PERMIT | 1 | IREN | **95.0** | ✔ |
| REGULATION | 3 | — | 0.0 | ✕ |
| USDC_DISTRIBUTION_ECONOMICS | 2 | — | 0.0 | ✕ |

**[fact]** 임계 대비 **+35.0pp 초과**. **[fact]** RATES 축에는 7종목 전부가 노출돼 있고 부호는 갈린다(IREN·NBIS·CRWV·MU 음 / CRCL·COIN·HOOD 양).

**[fact] 판별력 부재(3회차 연속)** — 6개 초과 축의 비중 상단이 전부 95.0으로 동일하고 2개 비초과 축은 전부 0.0이다. **[inference/강]** 이 수치로 축 간 위험 순위를 매길 수 없다. 경보가 가리키는 것은 특정 축의 크기가 아니라 **분산 부재**다.

**[fact] 자연 헤지 미작동** — 벡터에 정의된 역노출 쌍은 RATES 축(CRCL·COIN·HOOD 양 vs IREN·CRWV·NBIS·MU 음)과 USDC_DISTRIBUTION_ECONOMICS 축(COIN 양 vs CRCL 음) 두 계열인데, 두 계열 모두 반대편 종목이 전부 미보유다 — **벡터상 존재하는 헤지가 포지션상 존재하지 않는다**.

**[fact]** 임계값 60은 config 주석에 '⚠️초안'으로 표기돼 있어 **기준값 자체가 미확정**이다(U4 계열) — 초과 판정도 그만큼 잠정이다. **[fact]** 위 서술은 구조 기술이며 포지션 조정 제안이 아니다(P15).

---

## 8. 섹터 층 입력과 한계 — **3개 섹터 전부 방향 미산출**

| 섹터 | 컨센서스 | 공유 축 | 포트폴리오 관련성 |
|---|---|---|---|
| neocloud | `not_interpretable` | **0 / 14축** | **[fact]** 보유 종목 IREN의 6축 전부 null observation — 본 회차 보유 포지션에 신규 종목 고유 정보 공급 0건 |
| memory | 단일 종목 뷰 | — | **[fact]** MU 미보유. 실질 신규 관측은 `ip_litigation_risk` 1축(2026-09-02 CAFC 판결 3건, grade 1) |
| stablecoin | 미성립 (4 run 연속) | **0 / 18축** | **[fact]** CRCL·COIN·HOOD 전부 미보유. 벡터상 유일한 역노출 축(USDC_DISTRIBUTION_ECONOMICS)이 현 장부에서 미작동 |

**[fact] 구조적 무력화의 메커니즘** — 종목 카드가 각자 정의한 축 이름이 종목마다 달라, 축 이름 문자열 완전 일치로만 종목을 묶는 집계 스크립트가 어떤 축도 결합하지 못한다. **[fact]** 본 회차에 직접 증거가 확보됐다 — CRCL·COIN이 동일한 9/15 클로처 부결을 같은 방향(weaken)으로 매핑했으나 축 이름이 달라 분리됐다.

**[inference/강] 본 레이어에 미치는 효과** — 섹터 컨센서스 층이 '방향'을 공급하지 못하고 '관측 구조에 대한 기술'만 공급한다. 그 결과 본 포트폴리오 뷰의 시나리오는 전부 사전 정의 KC·config 한도에서 유도됐고 **섹터 방향 유도분은 0건**이다. **[inference/중]** 이는 시나리오 커버리지의 결손이지 섹터에 위험이 없다는 뜻이 아니다(P5). **[fact]** 같은 제약이 상관 레이어 `pair_overlap`의 신뢰도 상한으로도 작동한다(§2 참조).

**[fact] 측정 결함 관측** — HOOD 예측시장 훼손이 등급에 반영되지 못한 원인은 사실의 약함이 아니라 `sources.yaml` 도메인 미등재로 인한 **기계적 grade 4**다. 법원 승인 합의라는 확정 사실이 여기에 해당한다. **[fact]** 동일한 클로처 부결 사실이 COIN에서는 수동 예외로 grade 1, CRCL에서는 grade 3으로 적재돼 종목 간 등급 비대칭이 발생했다.

---

## 9. Thesis 정교화 (S7) — **후보 목록까지만, ThesisPatch 생성 0건**

**[fact]** ThesisPatch의 before→after 편집 생성은 F20(전문 확인 의무)이 thesis card 전문 로드를 요구하는데, 이는 본 에이전트의 P17 격리와 충돌한다. **[fact]** 따라서 후보만 기록한다 — 실제 패치는 오케스트레이터가 `refine thesis <TICKER>` 경로로 별도 집행한다. **[fact]** `approvals.py`를 호출하지 않았고 `state/thesis_cards/`에 쓰지 않았다(F17).

| 종목 | 우선도 | 대상 필드 | 제안 취지 | 근거 Claim | 충돌 |
|---|---|---|---|---|---|
| NBIS | high | 축 `monetization_mix` | 계약 단가(ACV/MW)와 on-demand 리스트 가격 분리(P8, 가칭 `on_demand_pricing_power`) | `NBIS_1·2·3` | 없음 (근거 grade 3 — 축 논거로만) |
| COIN | high | 축 목록 | 예측시장·이벤트 계약 축 슬롯 신설 (CT cease-and-desist 수신자에 Coinbase 포함) | `HOOD_3` | 타 종목 수집분 근거 — 차기 run의 COIN 수집 범위 확대 병행 필요 |
| CRWV | high | 축 `margin_trend` 기준 | YoY vs 시퀀셜 기준 고정(기준에 따라 부호 반전) | `CRWV_5·11` | 기준 선택은 정의 결정 — 에이전트가 고르는 것은 부적절 |
| CRWV | medium | 게이트 — 이자 커버리지 산식 | TTM vs 분기연환산 채택 확정 | `CRWV_1·14` | 없음 |
| IREN | medium | 관측점 — 전력·인허가 | BC Hydro 2026 Call for Demand 결과 + 소비 MWh(단위원가 산출용) | `IREN_3·4` | **유일한 보유 종목** — 전문 확인 후 집행 필수 |
| MU | medium | 축 `hbm_demand` | 수요 강·약 차원과 가동 연속성 차원 분리(P8) | `MU_11` | 근거 grade 3 |
| MU | medium | 관측점 — `ip_litigation_risk` | 특정된 식별자(ITC DN 3930, CDCA 8:26-cv-02167, D.Del 1:26-cv-01014) 반영 | `MU_5·8·9` | `MU_8·9`는 grade 4 |
| CRCL | medium | 축 `reserve_income` 서술 | 카드 금리 서술과 벡터 강도(+H)의 정합 확인 | `CRCL_8` | 벡터 수정은 config 영역 → vcp_05로 분리 |
| HOOD | medium | 축 `prediction_market` | 주 단위 집행 경로와 연방(CFTC) 경로 분리 | `HOOD_3` | 근거가 도메인 미등재로 grade 4 고착 |

**합계 9건 / 핵심 논거를 뒤집는(thesis_inverting) 후보 0건.**

**[fact]** 목록형 필드를 건드리는 후보(NBIS·IREN·MU 2건·COIN·HOOD)는 집행 시 `expected_after.counts`가 필수다(F20 — 2026-08-16 IREN 체크포인트 오인 패치 전례).

**[inference/중] 순서 주의** — 축 명명 표준화 결정이 선행되지 않으면 개별 카드의 축 분해 패치가 섹터 결합 문제를 오히려 악화시킬 수 있다(축 수가 늘면 공유 축 0개가 고착). 순서 결정은 사람 영역이다.

**제외 항목** — **[fact]** `kill_conditions.yaml`(KC-MU-*), `sources.yaml`(도메인 등재), `correlation_matrix.yaml`(축 분해)은 config 영역이므로 카드 패치가 아니라 escalation·vcp로 분리했다. 3사 축 명명 표준화는 단일 종목 패치로 분해할 수 없다.

---

## 10. 검증

| 산출물 | 레이어 | 결과 |
|---|---|---|
| `output/20260919_2209/05_correlation.json` | correlation | **PASS** |
| `output/20260919_2209/06_portfolio.json` | portfolio | **PASS** |

---

## 11. 🔴🔴 사람 확인 요청 + 근거 패키지 (CLAUDE.md §7)

**[fact]** 본 회차는 🔴🔴 후보를 포함하므로 이후 단계의 **자동 실행을 금지**하고 여기서 종료한다. **[fact]** `default_action`은 `no_action`이다(P12).

### 무슨 일이 있었나
**[fact]** 2026-09-16 FOMC 25bp 인상으로 FFR 목표범위가 3.75~4.00%가 되며 KC-1이 최초로 임계를 초과했고 `confirmed`로 확정됐다. **[fact]** arbiter 규칙1(Kill 우선)이 IREN·NBIS·CRWV·MU에서 발동해 🔴🔴 후보가 생성됐다.

### 무엇이 아닌가
**[fact]** 4건 중 종목 thesis 훼손에 기인한 것은 **0건**이다. **[fact]** 등급은 **후보**이며 확정이 아니다. **[fact]** 본 산출물은 어떤 포지션 행동도 지시하지 않는다.

### 근거 패키지

| 항목 | 경로 | 등급 |
|---|---|---|
| KC-1 판정 | `01_macro_kc.json#kc_status[KC-1]`, `#analyst_intervention[KC-1]` | 1차 공시 + FRED api 대사 |
| 사전 정의 결과 문언 | `config/kill_conditions.yaml#macro.KC-1.consequence` | config(사람 확정) |
| 🔴🔴 후보 4건 출처 | `03_signal/{IREN,NBIS,CRWV,MU}.json#transition_candidate` | arbiter 후보 판정 |
| 포지션 현황 | `config/positions.yaml` (as_of 2026-09-19) | 사용자 기입 |
| KC-9 조건부 상태 | `01_macro_kc.json#analyst_intervention[KC-9]` | FRED api + 사람 확인 |
| 축 집중도 경보 | `05_correlation.json#axis_concentration` | [CODE] 산출 |
| 섹터 층 한계 | `04_sector/{neocloud,memory,stablecoin}.json` | L3 구조화 산출물 |
| 상관 재실행 이력 | `_05_correlation_preSignal_backup.json` | P9 보존본 |

### 요청 결정사항

1. **[fact]** 🔴🔴 후보 4건의 등급 확정 또는 기각 (`esc_L4_2209_01`)
2. **[fact]** KC-9 duration override(`not_met`, 경고 유지) 확정 여부 — 시한 2026-10-10 (`esc_L4_2209_02`)
3. **[fact]** 축 명명 표준화 결정 — 미결정 시 섹터 컨센서스 미성립이 계속 반복된다 (`esc_L4_2209_03`)
4. **[fact]** config 4건 — `sources.yaml` 도메인 등재 / KC-MU-* 임계 / 축 집중도 임계 60 확정 / KC-4 임계 재정의 (`esc_L4_2209_04·05·06·10`)
5. **[fact]** 벡터 제안 5건(vcp_01~05)의 승인·기각·보류
6. **[fact]** ThesisPatch 후보 9건의 집행 여부 — 집행 시 `refine thesis <TICKER>` 별도 경로

### 에스컬레이션 총괄 — 14건 (top 3 / high 3 / medium 5 / low 3 · 신규 6 / 이월 8)

`esc_L4_2209_01`~`14` 전문은 `06_portfolio.json#escalation.items` 참조.

---

## 12. 본 회차 측정 한계 (P16·P17)

- **[fact]** 섹터 방향 입력 0건 — 3개 섹터 전부 컨센서스 미성립.
- **[fact]** 축 집중도 판별력 부재 — 보유 종목 1개로 인한 이진 축퇴(3회차 연속).
- **[fact]** 종목 KC 17건 파급 산출 불가 — 축 매핑 미정의(부재는 파급 없음이 아니다, P5).
- **[fact]** IREN 가격 라인 이격 산출 불가 — 입력 범위에 가격 피드 부재(3회차 연속).
- **[fact]** 노출 벡터 as_of 2026-08-15(35일 경과) — **본 레이어 정확성의 상한**.
- **[fact]** 축 집중도 임계 60이 config상 '⚠️초안' — 초과 판정 자체가 잠정.
- **[fact]** `esc_2209_06`(COIN 창 밖 4건 중복 확인)은 P17 격리로 본 레이어도 수행 불가 — 사람에게 재이관했다.
