# ThesisPatch — HOOD / axes / decompose

- **Run**: 20260919_2209 · as_of 2026-09-19 (`refine thesis HOOD`, S7)
- **대상 필드**: `axes` (L4 후보 표기: 축 정의 — prediction_market (연방·주 관할 분리))
- **operation**: `decompose` (P8 하위 축 분해)
- **축 목록 개수**: **현재 5개 → 기대 7개** (`expected_after.counts`: `[{"path": "axes", "n": 7}]` — F20 필수 충족)
  - 현재(카드 전문 계수): `aua_inflow`, `arpu_mix`, `crypto_cycle`, `prediction_market`, `rates_income`
  - 적용 후: 위 5개 + `prediction_market_state_enforcement`, `prediction_market_federal_jurisdiction` (상위 축 `prediction_market` 존치)
- **승인 필요**: ✅ `requires_human_approval: true` (F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: `state/thesis_cards/HOOD.yaml` **전문 71행 열람 후** before 1행의 원문 일치를 스크립트로 대조 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음). dry-run 병합본 YAML 파싱 + 축 7개 재계수 통과(`_HOOD_dryrun_merged_preview.yaml`).

---

## 🛑 선행 결정 없이는 승인 부적절 — `depends_on_human_decision: axis_naming_standardization`

> [fact] `output/20260919_2209/06_portfolio.json#thesis_patch_candidates.sequencing_note`: **축 명명 표준화 결정이 선행되지 않으면 개별 카드의 축 분해 패치(NBIS·MU·COIN·HOOD)가 섹터 결합 문제를 오히려 악화시킬 수 있다 — 축 수가 늘면 공유 축 0개 상태가 고착된다. 순서 결정은 사람 영역이다.**
>
> [fact] 본 회차 섹터 공유 축은 **stablecoin 0/18 · neocloud 0/14**이며 stablecoin은 4 run 연속 0개다(esc_L4_2209_03, 최상위 에스컬레이션).
> [fact] `04_sector/stablecoin.json#proposed_mapping_table`은 `HOOD:prediction_market`을 `cftc_product_regime_공통` 키에 사상해 두었다 — **본 분해는 그 사상 대상 자체를 바꾼다.** 매핑 테이블 갱신 없이 적용하면 공유 축 0개 상태가 그대로 굳는다.
> [fact] 따라서 **패치는 생성하되, `axis_naming_standardization`(coverage.yaml 공통축 매핑 도입 여부) 결정 전에 승인하는 것은 부적절하다.** 순서 결정은 사람 영역이다.
> [fact] 본 스킬은 `state/pending_approvals.json`에 등재하지 않았고 `approvals.py`를 호출하지 않았다 — 큐 등재는 오케스트레이터 소관(D10·F17).

## ⚠️ 근거 등급 한계 — 측정 결함이지 사실의 약함이 아니다 (소급 격상 없음)

[fact] 본 패치의 사실 근거 `c_20260919_HOOD_3·5·6·7·9`는 **전부 `evidence_grade: 4` · `confirmed: false`**다.
[fact] 사유는 사실관계 불확실성이 아니라 **`michigan.gov` · `portal.ct.gov` · `ago.mo.gov` · `cftc.gov` · `supremecourt.gov`가 `config/sources.yaml`에 미등재**라는 절차적·기계적 규칙이다 — 각 건은 4~5개 독립 매체로 교차확인됐다(02_company/HOOD.json 각 Claim note, 06_portfolio.json esc_L4_2209_04는 이를 `source_grading_defect`로 분류).
[fact] 그럼에도 **등급을 소급 격상하지 않는다(P4)** — `validate_output.py`의 'grade 3·4 + confirmed=true 금지' 규칙과도 정합한다.
[fact] **`config/sources.yaml`을 수정하지 않는다** — 사용자 직접 편집 영역이며(CLAUDE.md §9) 등재 제안은 esc_L4_2209_04로 이미 에스컬레이션돼 있다.
[fact] 결과적으로 **이 패치의 근거 등급 자체가 낮다.** 관측 단위를 분리하는 **구조 패치로만** 사용 가능하며, 하위 축 어느 쪽에도 방향 판정·시그널 등급 변경 근거를 부여하지 않는다.
[fact] **매출 영향 금액은 미시간·코네티컷·미주리 어느 건에서도 미공시**다(02_company/HOOD.json unconfirmed, `reason: not_disclosed`) — 금액·비중 추정을 하지 않았다(P5).

---

## diff

```diff
--- state/thesis_cards/HOOD.yaml (before)
+++ state/thesis_cards/HOOD.yaml (after 제안)
@@ -1 +1,4 @@
-  - {id: prediction_market, label: "예측시장 — 매출 기여 vs 규제 리스크. 기준선(Q2'26, 8-K Ex-99.1 grade 1): 이벤트 계약 매출 $156M·YoY 10배+, 분기 계약 13.6B건 — 거래매출 $776M 구성에서 크립토($100M)·주식($129M)을 추월(비중 ~20.1%는 파생 계산, inference). ⚠️Q3에서 월드컵 계절성 여부 확인 전까지 지속성 미검증 · 동일 축에 KC-HOOD-3 규제 리스크 상존(9순회 Kalshi 패소 판례, circuit split→SCOTUS 추적)"}
+  - {id: prediction_market, label: "예측시장 — 매출 기여 vs 규제 리스크. 기준선(Q2'26, 8-K Ex-99.1 grade 1): 이벤트 계약 매출 $156M·YoY 10배+, 분기 계약 13.6B건 — 거래매출 $776M 구성에서 크립토($100M)·주식($129M)을 추월(비중 ~20.1%는 파생 계산, inference). ⚠️Q3에서 월드컵 계절성 여부 확인 전까지 지속성 미검증 · 동일 축에 KC-HOOD-3 규제 리스크 상존(9순회 Kalshi 패소 판례, circuit split→SCOTUS 추적) / 2026-09-19 ThesisPatch(decompose, run 20260919_2209) 제안: 규제 리스크 경로를 하위 축 2개(prediction_market_state_enforcement, prediction_market_federal_jurisdiction)로 분해하고 본 축은 매출 기여 기준선 보유 축으로 존치한다 — 위 기준선 서술은 원문 그대로 보존하며 삭제하지 않는다(P9). 본 축 자체에는 방향 판정을 부여하지 않고 방향은 하위 축에서 독립 관측한다(P8)."}
+  # 2026-09-19 ThesisPatch(decompose, run 20260919_2209) — P8 분해 제안. 이전 상태: prediction_market 단일 축이 주(州) 게이밍법 집행 경로와 연방(CFTC) 관할 경로를 한 슬롯에 담아 본 회차 방향이 weaken 하나로 합산됐다. 두 경로는 집행 주체·관측 지표·시간 순서가 다르다 — 미시간 합의(2026-09-04 서명)는 CLARITY 클로처 표결(2026-09-15)에 선행하므로 한 축에서 합산하면 원인이 흐려진다. 상위 축 prediction_market은 매출 기여 기준선(Q2'26 $156M·13.6B건) 보유 축으로 존치하고 기존 서술은 삭제하지 않는다(P9). 축 수 5 → 7(카드 전문 기준 계수, F20). ⚠️근거 등급 한계: 하위 축 두 개의 관측 사실은 전부 evidence_grade 4·confirmed=false다 — 사실이 약해서가 아니라 michigan.gov·portal.ct.gov·ago.mo.gov·cftc.gov가 config/sources.yaml에 미등재라 기계적으로 부여된 등급이다(esc_L4_2209_04). 등급을 소급 격상하지 않으며(P4) config은 사용자 편집 영역이라 본 패치가 건드리지 않는다. ⚠️선행 결정 의존: axis_naming_standardization(esc_L4_2209_03) — 축 명명 표준화가 선행되지 않은 상태에서 축 수를 늘리면 섹터 공유 축 0개(stablecoin 0/18, neocloud 0/14) 상태가 고착된다. 선행 결정 전 승인은 부적절하다.
+  - {id: prediction_market_state_enforcement, label: "예측시장 규제 — 주(州) 집행 경로. 관측 단위: 개별 주의 명령·합의 및 Robinhood의 실제 상품 제공 중단 여부(주 수가 아니라 '실제 중단이 확정된 관할'을 센다). 2026-09 관측 — 미시간: 서부연방지법 승인 stipulation(2026-09-04 서명)으로 신규 sports event contract 제공 2026-09-09 중단, 기존 미결제 포지션 2026-10-09 청산, 제6순회 항소 종결까지 유효(c_20260919_HOOD_7). 코네티컷: 2026-09-10 Robinhood 포함 9개사 cease-and-desist 및 약 30건 소환장(c_20260919_HOOD_3). 미주리: 2026-09-16 기산 30일 내 중단 요구 cease-and-desist, 수신자 Robinhood Derivatives, LLC(c_20260919_HOOD_6). 코네티컷·미주리는 명령 발령 단계이며 이행 여부 미확인(unconfirmed). ⚠️세 건 모두 evidence_grade 4·confirmed=false(도메인 미등재 사유) — 단독 판단 근거 불가(P4). ⚠️매출 영향 금액은 회사·규제기관 어느 자료도 공개하지 않았다 — 주별 기여도 추정 금지(P5). 다음 관측점: 2026-10-09 미시간 청산 기한 실이행, 미주리 기한(약 2026-10-16) 도과 후 조치, Q3 실적의 주별 중단 반영분"}
+  - {id: prediction_market_federal_jurisdiction, label: "예측시장 규제 — 연방(CFTC·연방법원) 관할 경로. 관측 단위: 연방 전속관할을 확인·부인하는 절차의 진척과 그 계류 상태. 2026-09 관측 — CFTC가 D.Conn.에 코네티컷 주법 집행을 막는 예비적 금지명령을 신청하고 Robinhood가 소송참가를 신청(2026-09-11, 둘 다 계류, c_20260919_HOOD_5). Robinhood·Crypto.com의 연방대법원 상고 제출(제출일 2026-09-06/09-09로 매체 불일치, 도켓번호 미부여, 첫 검토 기회 2026-09-28 long conference, c_20260919_HOOD_9). 주 경로와 부호가 반대이며 시간 순서도 다르다 — 주 경로의 가장 무거운 사건(미시간 09-04 서명)이 CLARITY 클로처 표결(2026-09-15)에 선행한다. ⚠️본 경로의 관측 사실도 전부 evidence_grade 4·confirmed=false(cftc.gov·supremecourt.gov 미등재 사유) — 단독 판단 근거 불가(P4). 다음 관측점: 2026-09-28 SCOTUS long conference 처리, D.Conn. 예비적 금지명령·소송참가 인용 여부, CLARITY 재의동의 후 2차 클로처 실시 여부"}
```

> [fact] 카드 17행의 2026-09-05 annotate 주석행은 `before`에 포함하지 않아 **그대로 보존**된다(P9).
> [fact] 상위 축 `prediction_market`은 삭제하지 않는다 — 2026-09-05에 기입된 **매출 기여 기준선(Q2'26 이벤트 계약 매출 $156M · YoY 10배+ · 분기 13.6B건, 8-K Ex-99.1 grade 1, Q3 월드컵 계절성 미검증 캐비어트 포함)**은 두 하위 축 어느 쪽에도 귀속되지 않는 측정 기준선이므로 **원문 그대로 보존**하고 뒤에 분해 고지만 덧붙였다(P9).

## 왜

[fact] state/thesis_cards/HOOD.yaml 전문(71행)을 읽고 axes 목록을 계수한 결과 현재 축은 5개다 — aua_inflow, arpu_mix, crypto_cycle, prediction_market, rates_income(F20). 본 패치 적용 후 기대 축 수는 7개다. [fact] 본 회차 03_signal/HOOD.json의 thesis_delta_summary는 prediction_market 축을 weaken 방향으로 기록했고, 그 근거는 주(州) 게이밍법 집행(미시간·코네티컷·미주리)과 연방 관할 절차(CFTC의 D.Conn. 금지명령 신청·Robinhood 소송참가·SCOTUS 상고)의 충돌이다. [fact] 두 경로는 부호가 반대다 — 주 경로는 상품 가용성 축소, 연방 경로는 주 집행 저지 방향이며 둘 다 같은 창에 진행됐다. [fact] 시간 순서도 다르다 — 가장 무거운 미시간 stipulation은 2026-09-04 서명·09-09 이행이고 CLARITY 클로처 표결은 2026-09-15다(클로처 표결일은 본 회차 04_sector/stablecoin.json 및 06_portfolio.json esc_L4_2209_03에 기록된 사실이며, HOOD 등급 판정 근거로는 사용하지 않는다). [inference:medium] 부호와 시간 순서가 다른 두 경로가 한 축에 합산되면 축 방향 하나만 남고 원인이 소거되어, 다음 회차에 '무엇이 방향을 만들었는가'를 되짚을 수 없다 — L3 stablecoin이 기록한 오독 경로('규제 축 3/3 weaken을 공통 원인으로 읽는 것')와 같은 유형이다. [fact] 따라서 상위 축을 유지한 채 하위 축 2개를 신설해 각 경로를 독립 관측 단위로 분리한다(P8). [fact] 상위 축 prediction_market은 삭제하지 않는다 — 2026-09-05 패치로 기입된 매출 기여 기준선(Q2'26 이벤트 계약 매출 $156M·YoY 10배+·분기 13.6B건, 8-K Ex-99.1 grade 1, Q3 월드컵 계절성 미검증 캐비어트 포함)은 두 하위 축 어느 쪽에도 귀속되지 않는 측정 기준선이며, 그 서술을 원문 그대로 보존한다(P9). [fact] 본 패치는 방향 판정을 카드에 심지 않는다 — 하위 축 라벨에는 관측 사실과 다음 관측점만 기입하고 strengthen/weaken 부호를 부여하지 않는다. [fact] 매출 영향 금액은 미시간·코네티컷·미주리 어느 건에서도 공개되지 않았다(02_company/HOOD.json unconfirmed, reason=not_disclosed) — 금액·비중 추정을 하지 않았다(P5). [fact] 근거 등급 한계: 하위 축을 채우는 사실 Claim c_20260919_HOOD_3·5·6·7·9는 전부 evidence_grade 4·confirmed=false다. 각 Claim의 note에 기록된 대로 이 등급은 사실관계 불확실성이 아니라 michigan.gov·portal.ct.gov·ago.mo.gov·cftc.gov·supremecourt.gov가 config/sources.yaml에 미등재라는 절차적 사유로 부여됐고(4~5개 매체 교차확인은 완료), 06_portfolio.json esc_L4_2209_04가 이를 측정 결함으로 올렸다. [fact] 그럼에도 등급을 소급 격상하지 않으며(P4) config/sources.yaml도 수정하지 않는다 — config은 사용자 직접 편집 영역이다(CLAUDE.md §9). [fact] 그 결과 본 패치의 근거 등급 자체가 낮다 — 관측 단위를 분리하는 구조 패치로는 사용 가능하나, 어느 하위 축에도 방향 판정·등급 변경 근거를 부여하지 않는다. [fact] 선행 결정 의존: 06_portfolio.json thesis_patch_candidates.sequencing_note는 '축 명명 표준화 결정이 선행되지 않으면 개별 카드의 축 분해 패치가 섹터 결합 문제를 오히려 악화시킬 수 있다 — 축 수가 늘면 공유 축 0개 상태가 고착된다'고 기록했고, 순서 결정을 사람 영역으로 명시했다. [fact] 본 회차 섹터 공유 축은 stablecoin 0/18·neocloud 0/14다. [fact] 04_sector/stablecoin.json의 proposed_mapping_table은 HOOD:prediction_market을 cftc_product_regime_공통 키에 사상해 두었으므로, 본 분해는 그 사상 대상 자체를 바꾼다. [fact] 따라서 패치는 생성하되 axis_naming_standardization 결정 없이 승인하는 것은 부적절하다 — depends_on_human_decision 필드로 명시한다.

**역전 판정 주석**: [fact] thesis 본문(리테일 금융 수퍼앱·수익원 다각화)과 시그널 등급(🟡 유지 후보)에 대한 판정을 포함하지 않는다. [fact] 예측시장 규제 리스크의 존재·강도 판정을 바꾸지 않고 관측 단위를 둘로 나눌 뿐이다 — 에스컬레이션 대상이 아니다.

**후속 주의**: [fact] KC 재연결: KC-HOOD-3(예측시장 규제 금지, 중대 건 한정)은 현재 상위 축 prediction_market에 걸려 있다. [fact] 03_signal/HOOD.json은 KC-HOOD-3의 임계 문언에 수치·기준이 없어 met/not_met을 객관적으로 가를 근거가 부재하다고 기록하고 사람 확인을 요청했다. [fact] 본 분해가 승인되면 KC-HOOD-3을 어느 하위 축에 연결할지(또는 경로별로 임계를 나눌지)가 함께 결정돼야 한다 — 임계 신설·확정은 사람 영역이므로(P11·CLAUDE.md §9) 본 패치는 임계를 제안하지 않는다. [fact] 집계 영향: 04_sector/stablecoin.json proposed_mapping_table이 HOOD:prediction_market을 cftc_product_regime_공통에 사상해 두었으므로 분해 후에는 사상 대상이 하위 축 2개로 바뀐다 — 매핑 테이블 갱신 없이 적용하면 공유 축 0개 상태가 유지된다. [fact] key_metrics의 '예측시장(이벤트 계약) 매출·거래량' 항목은 본 패치 대상이 아니며 상위 축 기준선과 정합 상태로 유지된다 — 필드가 달라 충돌하지 않는다. [fact] 미채택 시 대안은 축 유지 + 라벨에 '방향 기록 시 주 경로·연방 경로를 구분 명기' 주석만 추가하는 annotate이며, 사용자 지시 시 재생성한다.

## 하위 축 (axis_decomposition)

| id | 관측 단위 | 이번 회차 관측(전부 grade 4·confirmed=false) | 방향 부여 | 다음 관측점 |
|---|---|---|---|---|
| `prediction_market_state_enforcement` | 개별 주의 명령·합의 및 실제 상품 제공 중단 확정 여부 | 미시간 법원 승인 stipulation(09-04 서명 / 09-09 신규 중단 / 10-09 청산, c_7) · 코네티컷 C&D 9개사(09-10, c_3) · 미주리 C&D 30일(09-16 기산, c_6) | **없음** (P4·P5) | 10-09 미시간 청산 실이행 · 미주리 기한 약 10-16 · Q3 실적 주별 반영분 |
| `prediction_market_federal_jurisdiction` | 연방 전속관할 확인·부인 절차의 진척과 계류 상태 | CFTC의 D.Conn. 예비적 금지명령 신청 + Robinhood 소송참가(09-11, 계류, c_5) · Robinhood·Crypto.com SCOTUS 상고(제출일 09-06/09-09 불일치, 도켓번호 미부여, c_9) | **없음** (P4) | 09-28 SCOTUS long conference · D.Conn. 인용 여부 · CLARITY 2차 클로처 실시 여부 |

[fact] 두 경로는 **부호가 반대**(주 = 가용성 축소 / 연방 = 주 집행 저지)이고 **시간 순서도 다르다** — 가장 무거운 미시간 합의(2026-09-04 서명)가 CLARITY 클로처 표결(2026-09-15)에 **선행**한다.
[inference:medium] 부호와 시간 순서가 다른 두 경로가 한 축에 합산되면 방향 하나만 남고 원인이 소거되어, 다음 회차에 '무엇이 방향을 만들었는가'를 되짚을 수 없다.

## 근거 Claim

`c_20260919_HOOD_3`, `c_20260919_HOOD_5`, `c_20260919_HOOD_6`, `c_20260919_HOOD_7`, `c_20260919_HOOD_9`, `c_20260919_HOOD_12`

[fact] L4 후보가 기재한 basis_claims는 c_20260919_HOOD_3 1건이며, 같은 축·같은 회차의 사실 Claim c_20260919_HOOD_5·6·7·9와 종합 추론 c_20260919_HOOD_12를 추가해 하위 축 각각의 근거를 명시했다. [fact] 추가분은 전부 output/20260919_2209/03_signal/HOOD.json 및 02_company/HOOD.json에 적재된 동일 회차 Claim이다. [fact] c_20260919_HOOD_12는 inference(강도 medium)이며 evidence_grade가 null이다 — 구조 근거로만 인용하고 등급 판정에 쓰지 않는다.

출처: `output/20260919_2209/06_portfolio.json#thesis_patch_candidates.candidates[HOOD] · #sequencing_note · output/20260919_2209/03_signal/HOOD.json#thesis_delta_summary[prediction_market] · #claims[c_20260919_HOOD_3,5,6,7,9,12] · output/20260919_2209/02_company/HOOD.json#deltas[prediction_market] · #unconfirmed · output/20260919_2209/04_sector/stablecoin.json#escalation[esc_2209_01,esc_2209_02]#proposed_mapping_table`

## F20 주석

[fact] state/thesis_cards/HOOD.yaml 전문 71행을 읽은 뒤 axes 목록을 계수했다 — 현재 5개(aua_inflow, arpu_mix, crypto_cycle, prediction_market, rates_income), 적용 후 기대 7개. [fact] before는 카드 내 1회만 등장하는 prediction_market 축 엔트리 1행 전체이며 원문 일치를 스크립트로 대조했다. [fact] not_contains는 그 1행 전체(말미 따옴표·중괄호 포함)로 지정했다 — after의 상위 축 라인은 같은 1행에 접미부가 덧붙어 더 길므로 not_contains 문자열과 일치하지 않는다(2026-08-16 자동 원복 사고 유형 회피). [fact] 2026-09-05 annotate 주석행(카드 17행)은 before에 포함하지 않아 그대로 보존된다(P9). [fact] state/thesis_cards/HOOD.yaml과 state/pending_approvals.json은 수정하지 않았다(F17).

---

> 이 패치는 **제안**이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → `expected_after` 자동 대조 → 실패 시 원복).
> **다만 본 건은 `depends_on_human_decision: axis_naming_standardization`이 걸려 있어, 그 선행 결정 전 승인은 부적절하다.**
