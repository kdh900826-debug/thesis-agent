# ThesisPatch — COIN / axes / amend (축 슬롯 신설)

- **Run**: 20260919_2209 · as_of 2026-09-19 (S7 `thesis-refine`)
- **대상 필드**: `axes` — **현재 5개 → 기대 6개** (`expected_after.counts: [{path: axes, n: 6}]`, F20)
- **operation**: `amend` (순수 추가 — 기존 5개 축 문자열 무변경, P9)
- **승인 필요**: 예 (`requires_human_approval: true`, F17) / **핵심 논거 역전**: 아니오
- **사전 확인**: `state/thesis_cards/COIN.yaml` **전문 61행** 열람 후 before 문자열 원문 일치(전문 내 1회 출현)·축 5개 계수 확인 완료 (F20 — 부분 읽기 기반 '부재' 판정 없음)
- **패치 건수**: 1건

---

## 🚨 선행 인간 결정 의존 — `depends_on_human_decision: "axis_naming_standardization"`

> **이 패치는 축 명명 표준화 결정이 내려지기 전에는 승인을 권장하지 않는다.**
>
> [fact] L4 기록 — 축 명명 표준화가 선행되지 않은 채 개별 카드의 축 신설·분해를 진행하면 섹터 결합 문제가 악화된다. 3섹터 모두 종목 간 **공유 축 0개**(neocloud 0/14, stablecoin 0/18) 상태이며, 이 상태에서 축 수만 늘리면 공유 축 0이 고착된다.
> [fact] 본 패치는 stablecoin 섹터의 COIN 축 수를 **5 → 6**으로 늘린다. 즉 위 위험의 직접 당사자다.
> [fact] 순서 결정(명명 표준화 먼저 / 이 패치 먼저)은 **사람 영역**이다(CLAUDE.md §9).

### 다만 — 이 건은 공유 축을 **늘릴** 기회이기도 하다 (제안, 결정은 사람)

[fact] 신설 대상은 HOOD 카드의 `prediction_market` 축과 **동일 실체**(예측시장·이벤트 계약)를 다룬다.
[inference:strong] 두 축의 id를 정합시키면 stablecoin 섹터의 종목 간 공유 축이 **0개 → 1개**가 된다 — 축 수 증가가 공유 축 0 고착으로만 귀결되지 않는 예외 경로다.

**축명 후보** (패치에는 ⓐ를 **잠정** 표기로 기입했다 — 확정 시 개명 가능):

| 후보 | id | 성질 |
|---|---|---|
| **ⓐ (잠정 채택)** | `prediction_market` | HOOD와 문자열 정합 → **공유 축 성립**. 명명 표준화 결정의 시범 사례가 될 수 있다 |
| ⓑ | `event_contract_regulation` | 규제 층위로 한정. 상품 라인업 재료를 포섭하지 못한다 |
| ⓒ | `prediction_market_event_contracts` | 실체 서술형이나 HOOD와 불일치 → 공유 축 미성립 |

---

## diff

```diff
--- state/thesis_cards/COIN.yaml (before)
+++ state/thesis_cards/COIN.yaml (after 제안)
   - {id: derivatives_base,  label: "파생상품·Base 생태계 확장"}
+  # 2026-09-19 ThesisPatch(amend, run 20260919_2209) — 축 1개 신설(5개 → 6개, 전문 기준 계수). 기존 5개 축은 문자 하나도 변경하지 않는다(P9). 신설 축은 **빈 관측 슬롯**이며 방향·노출 여부를 판정하지 않는다. ⚠️축 id `prediction_market`는 **잠정 표기**다 — 선행 결정 `axis_naming_standardization`(사람 영역) 미확정 상태이며, 확정 시 id·label이 변경될 수 있다. 잠정 id를 HOOD 카드의 `prediction_market` 축과 동일 문자열로 둔 것은 두 종목이 같은 실체(예측시장·이벤트 계약)를 다루므로 **종목 간 공유 축을 성립시킬 기회**이기 때문이며, 채택 여부는 사람이 결정한다. 대안 후보: ⓐ`prediction_market`(HOOD 정합 — 공유 축 성립) ⓑ`event_contract_regulation`(규제 층위 한정) ⓒ`prediction_market_event_contracts`(실체 서술형, HOOD와 불일치).
+  - {id: prediction_market,  label: "예측시장·이벤트 계약 (잠정 id — axis_naming_standardization 결정 전. 【관측 상태: 미관측(unconfirmed)】). 이 축은 COIN의 예측시장·이벤트 계약 사업과 그에 대한 주(州) 단위 규제 조치를 관측하기 위한 **빈 슬롯**이다. 신설 사유는 관측 단위의 부재 자체다 — 2026-09-19 run 기준 COIN 산출물(02_company·03_signal)에 이 실체를 다루는 Claim·Delta·unconfirmed가 0건이어서, 해당 사안이 발생하더라도 카드에 매핑될 자리가 없었다. ⚠️본 축은 COIN에 대한 어떠한 사실도 주장하지 않는다 — 특히 'COIN이 코네티컷 주 cease-and-desist를 수신했다'는 진술은 **카드에 기재하지 않는다**. 해당 정황은 타 종목(HOOD) 수집분에서 파생된 것으로 P4·P17상 COIN에 대한 사실 주장의 근거로 부적격이며, 차기 회차 `company-coin`의 COIN 자체 1차 수집(주 증권감독기관 공개 문서·회사 공시·IR)으로 **확인 대상**으로 남긴다. 슬롯이 비어 있다는 것은 '노출 없음'이 아니라 '아직 관측되지 않음'을 뜻한다(P5 — 정보 부재는 반증이 아니다). 다음 관측점: 차기 run의 company-coin 수집 범위 확대(주 단위 증권감독기관 조치·예측시장 상품 라인업), COIN 8-K·10-Q의 법적 절차 주석, 회사 공식 블로그·IR"}
```

## 왜

[fact] `state/thesis_cards/COIN.yaml` 전문 61행을 읽고 계수한 결과 axes는 **5개**다 — subscription_mix, trading_cycle, usdc_economics, regulation, derivatives_base.
[fact] 5개 축 어디에도 예측시장·이벤트 계약을 관측 대상으로 삼는 라벨이 없다. `regulation` 라벨은 "규제 — CLARITY Act 경로"로 **연방 입법 경로에 한정**되어 주(州) 단위 행정조치를 포섭하지 않고, `derivatives_base`는 파생상품·Base 생태계를 지목할 뿐 예측시장·이벤트 계약을 지목하지 않는다.
[fact] `output/20260919_2209/02_company/COIN.json`(claims 7 · deltas 5 · unconfirmed 8)과 `output/20260919_2209/03_signal/COIN.json`(claims 6 · unconfirmed_carried 8)을 전수 대조한 결과, 예측시장·이벤트 계약·코네티컷 주 조치에 해당하는 항목은 **0건**이다.
[inference:strong] 즉 이것은 "관측했으나 노출이 없다"가 아니라 **"관측 자체가 발생할 자리가 없다"**는 구조적 공백이다. 관측 단위가 없으면 차기 회차에 자체 1차 자료가 들어와도 매핑 대상이 없어 다시 유실된다.
[fact] 섹터 계층의 구조적 역노출 후보 `sie_event_contract_state_federal`은 COIN 측 대응 축이 없는 한 후보 이상으로 확정될 수 없다 — 본 패치는 그 확정을 **수행하지 않고**, 확정에 필요한 관측 자리만 연다.
[fact] 신설 축 라벨에는 방향·등급·노출 여부 판정이 없으며 관측 상태를 `unconfirmed`로 명시한다(P5).
[fact] 기존 5개 축은 before 행이 after 안에 원문 그대로 보존되고 신설 행이 뒤에 추가되는 형태로, 삭제·변경이 없다(P9).
[fact] `state/pending_approvals.json` 전 39건을 확인한 결과 pending 상태의 COIN thesis_patch는 없다(전부 approved 또는 expired) — 중복 패치 위험 없음.

## 🔶 타 종목 근거의 취급 — 사실 기재 금지

- **basis_claims**: `c_20260919_HOOD_3` — **유일한 근거가 타 종목(HOOD) 수집분이다.**
- [inference:strong] P4(자료 등급 위계)·P17(담당 범위 밖 원문 비적재)에 따라 이 근거는 **두 용도로 갈라 쓴다**:
  - ✅ **유효** — "COIN 카드에 대응 관측 단위가 없다"는 **구조적 공백의 필요성 논거**
  - ⛔ **부적격** — "Coinbase가 코네티컷 C&D를 수신했다"는 **COIN에 대한 사실 주장의 근거**
- [fact] 따라서 패치는 **빈 축 슬롯 신설 + 미관측(unconfirmed) 표기**에 그치며, 수신 사실을 카드에 **사실로 기재하지 않는다**. 라벨 안에 이 금지를 명문으로 박아 두어, 후속 회차에서 슬롯 존재를 근거로 사실이 역추정되는 것을 차단한다.
- [fact] 확인 경로는 **차기 회차 COIN 자체 수집**(주 증권감독기관 공개 문서 · COIN 8-K/10-Q 법적 절차 주석 · 회사 공식 블로그·IR)으로 이월한다.
- [fact] 본 패치 작성 중 HOOD의 `02_company` 산출물 원문은 **로드하지 않았다**(P17). 위 rationale에 적힌 범위를 넘어 참조하지 않았다.
- [fact] `key_metrics`·`risks`·`catalysts`에는 패치를 만들지 않았다 — COIN 자체 관측이 0건인 상태에서 지표·리스크 문장을 추가하면 미관측 사안을 사실처럼 심게 된다(P5·P4). 자체 관측 확보 후 별건 판단.

## ⚠️ conflict — 카드 패치 단독으로 해소되지 않는다

**`collection_scope_gap`: 차기 run의 `company-coin` 수집 범위 확대가 함께 필요하다.**

[fact] 현재 COIN 수집 경로는 EDGAR 서식·회사 IR·블로그 중심이며, **주(州) 단위 증권감독기관의 행정조치**(cease-and-desist 등)와 **예측시장·이벤트 계약 상품 라인업**은 수집 범위에 포함되어 있지 않다.
[inference:strong] 슬롯만 신설하고 수집 범위를 넓히지 않으면 이 축은 영구히 빈 채로 남고, '미관측'이 사실상 '무노출'로 오독될 위험이 생긴다(P5 위반 유도).
[fact] 수집 범위 변경은 `config/sources.yaml` 영역이며 에이전트는 **제안만** 한다(CLAUDE.md §9).

필요 후속(제안 — 사용자 결정):
1. 차기 run `company-coin` 수집 범위에 **주 단위 증권감독기관 행정조치 경로** 추가
2. 차기 run `company-coin` 수집 범위에 **COIN 예측시장·이벤트 계약 상품 라인업 확인** 추가

## 후속 주의 (downstream)

[fact] ① `config/kill_conditions.yaml` — 신설 축에 대응하는 KC는 없으며, 임계 없는 KC 신설은 금지이므로(P11) 본 패치는 KC를 제안하지 않는다. 신설 여부·임계는 사용자 영역이다. ② `kill_conditions_ref` 무수정. ③ `config/correlation_matrix.yaml` — 예측시장·이벤트 계약 규제의 노출 축 등재 여부는 `axis_naming_standardization` 결정 이후 판단 대상이며 본 패치는 벡터 변경을 제안하지 않는다. ④ 시그널 등급(🟠)에 대한 제안 없음(P13).

## 근거 Claim

`c_20260919_HOOD_3` (타 종목 수집분 — 위 「타 종목 근거의 취급」 절의 용도 제한이 적용된다)

출처: `output/20260919_2209/02_company/COIN.json#claims(7건 전수)·#deltas(5건 전수)·#unconfirmed(8건 전수)` — 해당 실체 **0건** 확인 · `output/20260919_2209/03_signal/COIN.json#claims(6건)·#unconfirmed_carried(8건)` — 동일 **0건** 확인 · `state/thesis_cards/COIN.yaml`(전문 61행, axes 5개)

**F20 주석**: [fact] 카드 전문 61행을 읽은 뒤 before 문자열(15행)의 원문 일치와 axes 5개 계수를 확인했다. [fact] before 문자열은 전문에서 **1회만** 출현해 치환 모호성이 없다. [fact] 목록형 필드를 건드리므로 `expected_after.counts: [{path: "axes", n: 6}]`를 필수 포함했다. [fact] `not_contains`는 **빈 목록**이다 — 순수 추가형 패치라 사라져야 할 문자열이 존재하지 않으며, 보존 대상 문자열을 not_contains에 넣어 자기모순을 만드는 것(2026-08-16 ap_20260816_0010 자동 원복 사고 유형)을 회피했다. [fact] 임시 사본에 패치를 모의 적용해 `approvals.verify_after_apply`를 실행한 결과 위반 0건, 적용 후 axes 6개 파싱 확인 — 원본 카드는 **무변경**이다(F17).

> 이 패치는 제안이며 자동 반영되지 않는다(F17). `state/thesis_cards/COIN.yaml`·`state/pending_approvals.json`은 본 스킬이 수정하지 않았다 — 승인 큐 등재는 오케스트레이터가, 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
