# ThesisPatch — NBIS / axes / decompose (P8 하위 축 분해)

- **Run**: 20260919_2209 · 2026-09-19T22:09 (L4 병행 `thesis-refine`, S7)
- **대상 필드**: `axes` (목록형 — expected_after.counts: axes=8, F20)
- **operation**: `decompose` · **축 수 7 → 8**
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: 대상 카드 **전문 열람**(103행) 후 axes 목록 실계수 = 7개, before 문자열 카드 원문 일치 확인 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음)

## 🚨 선행 결정 의존 — 이 결정 없이는 승인 부적절

> **`depends_on_human_decision: axis_naming_standardization`** (esc_L4_2209_03)
>
> [fact] 06_portfolio.json#sequencing_note: 축 명명 표준화 결정이 선행되지 않으면 개별 카드의 축 분해 패치(NBIS·MU·COIN·HOOD)가 섹터 결합 문제를 오히려 **악화**시킬 수 있다 — 축 수가 늘면 공유 축 0개 상태가 고착되기 때문이다.
> [fact] 현재 3섹터 모두 종목 간 공유 축 0개다 — neocloud 0/14, stablecoin 0/18, memory는 단일 종목.
> [inference:medium] 따라서 **패치는 생성하되, 축 명명 표준화 결정 이전의 승인은 부적절하다.** 순서 결정은 사람 영역이다.

## diff

```diff
--- state/thesis_cards/NBIS.yaml (before)
+++ state/thesis_cards/NBIS.yaml (after 제안)
@@ -1 +1,3 @@
-  - {id: monetization_mix,  label: "ACV/MW 3단 구조·소프트웨어 수익화"}
+  # 2026-09-19 ThesisPatch(decompose, P8, run 20260919_2209) — 이전 축: {id: monetization_mix, label: "ACV/MW 3단 구조·소프트웨어 수익화"}. 축 정의가 계약형 단가 체계(ACV/MW 3단)만 포괄하는데 본 회차 방향 근거는 on-demand 리스트 가격 인상(GPU 17~21%, CPU-only 25%, 메모리 약 41%, 2026-10-01 발효 예정)이어서 서로 다른 가격 레이어가 한 축에 합산됐다. ⚠️P4 한계 — 인상 보도는 grade 3·confirmed=false다. 축 분해(관측 단위 분리)의 논거로만 사용하며 어느 하위 축에도 방향 판정을 부여하지 않는다. ⚠️P7 — 2026-10-01은 발효 '예정'일이다. 가격 고지 ≠ 계약 갱신·체결 ≠ 매출 인식이며 본 주석 어디에도 매출 반영 주장은 없다. ⚠️선행 결정 의존(axis_naming_standardization, esc_L4_2209_03) — 3사 카드 축 명명 표준화가 결정되기 전에 축 수를 늘리면 neocloud 공유 축 0/14 고착을 악화시킬 수 있다. 표준화 결정 이전 승인은 부적절. 축 수 7 → 8(카드 전문 기준 계수, F20). 이전 축 서술은 삭제하지 않고 본 주석으로 보존한다(P9).
+  - {id: contract_monetization, label: "계약형 수익화 — ACV/MW 3단 구조(기본 ~$12M / 장기 ~$20-25M / 단기 ~$40-50M)·소프트웨어(Token Factory, Echo) 수익화. 2026-09-19 기준 본 레이어의 신규 정량 자료 없음. Reuters 보도상 다개월 대규모 클러스터 예약 고객에는 commitment discount가 적용되므로 on-demand 인상이 $1B+ 계약(Meta·MS·Q2 신규 4사)에 그대로 전가되는지는 미확인 — 아래 축과 부호가 분리될 수 있다"}
+  - {id: on_demand_pricing_power, label: "on-demand 리스트 가격 결정력 — 회사 공식 가격 페이지 기준선(2026-09-19 조회, grade 1): HGX H100 $3.85 / H200 $4.50 / B200 $7.15, GB300 NVL72 미게시. 2026-05 1차 인상(on-demand 평균 +29%·spot +51%)에 이어 2026-09-17 보도 기준 2026-10-01 발효 예정 2차 인상 고지(GPU 17~21%·CPU-only 25%·메모리 약 41%, grade 3·confirmed=false, 1차 공시 경로 부재). 보도된 '인상 전' 단가 3개 모델은 공식 페이지와 정확히 일치해 기준선만 교차검증됨. 부호 활성화 조건 = 2026-10-01 이후 nebius.com/prices 신단가 1차 확인 또는 Q3 2026 실적자료의 단가·ARPU 언급"}
```

## 왜

[fact] 카드 전문(state/thesis_cards/NBIS.yaml, 103행)을 열람해 axes 목록을 계수한 결과 현재 축은 7개다 — growth_arr, margin_transition, funding_access, leverage_burden, capacity_delivery, monetization_mix, customer_concentration(F20 전문 기준 계수). [fact] monetization_mix 축 정의는 "ACV/MW 3단 구조·소프트웨어 수익화"로 계약형 단가 체계만 포괄한다. [fact] 반면 본 회차 02_company/NBIS.json의 monetization_mix Delta(direction: strengthen)의 근거는 on-demand 리스트 가격 인상이다(c_20260919_NBIS_2 — GPU 17~21%, CPU-only 25%, 메모리 약 41%, 2026-10-01 발효 예정). [fact] L2 스스로 두 체계를 동일 지표로 혼용 인용하지 말 것을 c_20260919_NBIS_1 note에 기록했고, notes ③에서 하위 축 분해 여지(가칭 on_demand_pricing_power)를 명시했다. [fact] on-demand 기준선 단가는 회사 공식 가격 페이지(c_20260919_NBIS_1, grade 1, confirmed)로 확인되며 보도된 '인상 전' 단가 3개 모델과 정확히 일치한다(c_20260919_NBIS_3). [inference:strong] 성질이 다른 두 가격 레이어가 한 축에 합산되면 방향 신호가 섞인다 — commitment discount로 계약 고객에는 인상이 흡수될 수 있어 두 레이어의 부호가 항상 같지 않기 때문이다. [fact] P4 제약 — 인상 보도는 grade 3·confirmed=false이며 회사 뉴스룸·EDGAR 6-K에 대응 1차 공시가 없다. 따라서 본 패치는 관측 단위를 분리할 뿐이고 어느 하위 축에도 방향 판정을 부여하지 않는다. 방향 판정의 단독 근거로는 부적격이다. [fact] P7 제약 — 2026-10-01은 발효 예정일이며 가격 고지 단계다. 계약 갱신·체결 및 매출 인식과 분리되며 03_signal/NBIS.json의 상향 게이트도 revenue_recognized 미충족으로 not_met(vacuous)이다. [fact] 축 수 7 → 8. 이전 축 서술은 삭제하지 않고 주석으로 보존한다(P9). [fact] 선행 결정 의존 — 06_portfolio.json의 sequencing_note는 축 명명 표준화 결정이 선행되지 않으면 개별 카드의 축 분해 패치가 섹터 결합 문제를 악화시킬 수 있다고 기록했고, neocloud 공유 축 0/14·stablecoin 0/18 상태에서 축 수를 늘리면 공유 축 0이 고착된다. [inference:medium] 따라서 본 패치는 생성하되 axis_naming_standardization(esc_L4_2209_03) 결정 이전에는 승인이 부적절하다. 순서 결정은 사람 영역이다.

**역전 판정 주석**: [fact] 축 분해는 기존 판정을 뒤집지 않고 관측 단위를 세분한다 — monetization_mix의 기존 방향·강도 판정을 변경하지 않으며 하위 축 어느 쪽에도 새 방향을 부여하지 않는다. [fact] 2026-09-05 재작성된 thesis 문장('자본시장 접근성 + 부채>현금 전환', 선택지 A)과 동반 정정된 conclusion에는 접촉하지 않는다 — 본 패치는 axes 필드 단일 슬롯만 건드린다. [fact] 본 회차 🔴🔴 후보는 매크로 KC-1 경로이며 monetization_mix와 무관하다(03_signal/NBIS.json kill_check). 따라서 에스컬레이션 대상이 아니다.

**후속 주의**: [fact] ⚠️ 승인 순서 의존 — depends_on_human_decision: axis_naming_standardization. 3사 카드 축 명명 표준화(esc_L4_2209_03)가 결정되기 전 본 패치를 승인하면 neocloud 공유 축 0/14 상태에서 축 수만 늘어 섹터 컨센서스 미성립이 고착될 수 있다(06_portfolio.json#sequencing_note). 표준화 결정 후 재검토 권고. [fact] KC 재연결 불필요 — KC-NBIS-1/2/3은 대형 고객계약·용량 인도·조달 조건에 걸려 있고 monetization_mix에 연결된 KC는 없다. 하위 축에 정량 임계를 신설하지 않는다(P11 · CLAUDE.md §9 — 임계 확정은 사람 영역). [fact] key_metrics의 'ACV/MW 3단 구조' 항목은 본 패치로 변경하지 않는다 — on-demand 단가를 key_metrics에 신설하는 패치는 1차 자료 확인(2026-10-01 이후) 이전에는 P4상 근거 부족으로 생성하지 않았다. [fact] 미채택 시 대안은 축 유지 + 라벨에 '본 축은 계약형 ACV/MW 레이어만 포괄하며 on-demand 리스트 가격은 별도 레이어' 주석만 추가하는 annotate이며, 사용자 지시 시 재생성한다.

## 증거 한계 (패치 문안에 반영됨)

- **P4** — 방향 근거인 가격 인상 보도(`c_20260919_NBIS_2`)는 **grade 3 · confirmed=false**이며 회사 뉴스룸·EDGAR 6-K에 대응 1차 공시가 없다. 축 **분해의 논거**로는 사용 가능하나 **방향 판정 근거로는 단독 부적격** — 두 하위 축 모두 `current_direction: 판정 없음`으로 둔다.
- **P7** — 2026-10-01은 **발효 예정일**이다. 가격 고지 ≠ 계약 갱신·체결 ≠ 매출 인식. 본 패치 문안 어디에도 '매출 반영' 주장은 없으며, 03_signal의 상향 게이트도 `revenue_recognized` 미충족으로 not_met(vacuous)이다.
- **P9** — 이전 축 서술(`monetization_mix`)은 삭제하지 않고 주석으로 보존한다.
- **이력 정합** — 2026-09-05 thesis 재작성('순현금·저희석' → '자본시장 접근성 + 부채>현금 전환', 선택지 A)과 동반 conclusion 정정에는 접촉하지 않는다. 본 패치는 axes 단일 슬롯만 건드린다.

## 하위 축 (axis_decomposition)

| id | 관측 가능 | 관측 경로 | 현재 방향 | 부호 활성화 조건 |
|---|---|---|---|---|
| `contract_monetization` | ✅ | 분기 실적자료(ACV/MW 3단·ARR)·6-K 계약 공시 | 판정 없음 (신규 정량 자료 없음) | ACV/MW 단가 갱신 또는 신규 $1B+ 계약 조건 공시 |
| `on_demand_pricing_power` | ✅ | nebius.com/prices 공식 가격 페이지(grade 1) 정기 조회 | 판정 없음 (근거 grade 3·confirmed=false) | 2026-10-01 이후 신단가 1차 확인 또는 Q3 2026 단가·ARPU 언급 |

## 근거 Claim

c_20260919_NBIS_1, c_20260919_NBIS_2, c_20260919_NBIS_3

출처: `output/20260919_2209/02_company/NBIS.json#deltas[monetization_mix] · output/20260919_2209/02_company/NBIS.json#notes③ · output/20260919_2209/03_signal/NBIS.json#thesis_delta_summary[monetization_mix] · output/20260919_2209/06_portfolio.json#sequencing_note`

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 본 건은 승인 전 **axis_naming_standardization 결정이 선행돼야 한다.**
