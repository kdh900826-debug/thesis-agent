# ThesisPatch Set — MU (run 20260919_2209)

- **as_of** 2026-09-19 · 스킬 `thesis-refine`(S7) · 패치 **2건** (L4 후보 2건 전량 처리, 제외 0건, 신규 창작 0건)
- **카드 전문 확인(F20)**: `state/thesis_cards/MU.yaml` **71행 전문** 열람. 목록형 필드 실계수 — **axes 6** / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / earnings_checkpoints.items 7 / version_history 4
- **기대 개수**: A 적용 후 axes **6 (불변)** / B 적용 후 axes **7**
- **승인**: 2건 모두 `requires_human_approval: true` (F17). `state/thesis_cards/MU.yaml`·`state/pending_approvals.json` 미수정.
- **적용 순서**: 두 건 모두 승인 시 **A → B**. (A의 counts=6은 B 미적용 상태 전제 — B 선적용 시 A의 counts를 7로 갱신 후 재승인)
- **개별 적용 아티팩트**: `MU_axes_ip_litigation_observation.(json|md)` / `MU_axes_hbm_demand_decompose.(json|md)` — 승인 큐에는 이 2건을 각각 등재하라(`MU.json`은 patch_set 묶음이며 approvals.py 적용 대상이 아니다).

> 🚨 **선행 인간 결정 의존 — `depends_on_human_decision: axis_naming_standardization`**
> 축 명명 표준화 결정이 **선행되지 않으면 이 패치는 승인 부적절**하다. 3섹터 모두 종목 간 공유 축이 **0개**(neocloud 0/14, stablecoin 0/18)인 상태에서 개별 카드의 축 수만 늘리면 **공유 축 0이 고착**돼 섹터 결합 문제가 악화된다.
> 패치 자체는 생성했으나, **순서 결정은 사람 영역**이다(CLAUDE.md §9). 표준화 결정 확정 전 `approve` 금지.

---

## 패치 A — `axes[ip_litigation_risk]` 관측점 갱신 / `annotate` / priority medium

**등급 한계 고정(P4)**: `c_20260919_MU_5`(CAFC 판결, grade 1·confirmed)와 `c_20260919_MU_7`(ITC DN 3930, grade 1·confirmed)만 사실 단정. `c_20260919_MU_8`(CDCA 8:26-cv-02167)·`c_20260919_MU_9`(D.Del 1:26-cv-01014)는 **grade 4·confirmed=false**이므로 라벨에 '확인 대상 · 단독 근거 부적격' 표기를 붙여 기입했다. `c_20260919_MU_6`은 grade 1이나 inference·moderate로 표기.

**⚠️리스크 해소 아님**: 무효 인용된 특허 5건과 2026-08-12 신규 제소(ITC·CDCA)의 주장 특허 4건은 **번호가 겹치지 않는다** — 신규 소송의 청구는 소멸되지 않았다. 이 문장을 축 라벨 본문에 직접 심어 오독 경로를 차단했다.

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
-  - {id: ip_litigation_risk, label: "특허소송 리스크 — Netlist가 2026-08-12 ITC에 Micron 포함 4개사를 상대로 특허 4건(US 10,025,731 / 10,217,523 / 12,373,366 / 12,675,407, DDR5 RDIMM·MRDIMM) 침해 제소하며 배제명령·중지명령 청구, 별도로 캘리포니아중부지법(CDCA)에 Micron 단독 제소(특허 2건). 배경: 2026-02-20 CAFC 별건 판결로 $445M 배상 확정 이력. ITC 배제명령은 미국向 수입·매출 인식에 직접 작용하는 경로로 hbm_demand·sca_defense·china_supply 어디에도 매핑되지 않는 독립 리스크다. 2026-09-05 기준 ITC 조사개시(institution) 공지는 확인되지 않았으며 자료 부재는 반증이 아니다(P5). 추적점: ITC institution 투표, CDCA 답변 시한(2026-09-10, grade 4 미확인)"}
+  # 2026-09-19 ThesisPatch(annotate, run 20260919_2209) — 이전 축 서술은 아래 라벨 앞부분에 그대로 보존하고 관측점만 덧붙인다(P9, 삭제 없음). 축 수 6개 불변(전문 71행 기준 계수: hbm_demand·sca_defense·cycle_position·china_supply·valuation_paradox·ip_litigation_risk). ⚠️본 패치는 리스크 해소 기록이 아니다 — 2026-09-02 CAFC 무효 인용 특허 5건과 2026-08-12 신규 제소 주장 특허 4건은 번호가 겹치지 않는다. ⚠️CDCA 8:26-cv-02167·D.Del 1:26-cv-01014 두 식별자는 grade 4·confirmed=false 단독 소스이므로 사실 확정이 아니라 확인 대상으로 기재했다(P4).
+  - {id: ip_litigation_risk, label: "특허소송 리스크 — Netlist가 2026-08-12 ITC에 Micron 포함 4개사를 상대로 특허 4건(US 10,025,731 / 10,217,523 / 12,373,366 / 12,675,407, DDR5 RDIMM·MRDIMM) 침해 제소하며 배제명령·중지명령 청구, 별도로 캘리포니아중부지법(CDCA)에 Micron 단독 제소(특허 2건). 배경: 2026-02-20 CAFC 별건 판결로 $445M 배상 확정 이력. ITC 배제명령은 미국向 수입·매출 인식에 직접 작용하는 경로로 hbm_demand·sca_defense·china_supply 어디에도 매핑되지 않는 독립 리스크다. 2026-09-05 기준 ITC 조사개시(institution) 공지는 확인되지 않았으며 자료 부재는 반증이 아니다(P5). 추적점: ITC institution 투표, CDCA 답변 시한(2026-09-10, grade 4 미확인). 2026-09-19 관측점 갱신(ThesisPatch annotate, run 20260919_2209) — ① [fact · grade 1 · confirmed] 2026-09-02 CAFC가 Netlist v. Micron 항소 3건(24-1707 선례적 / 24-1859·24-1863 / 24-2240·24-2241)을 전부 인용(AFFIRMED)해 Netlist 특허 5건(US 10,949,339 / 11,016,918 / 11,232,054 / 8,787,060 / 9,318,160)의 쟁점 청구항이 무효 판단을 받았다(c_20260919_MU_5, 판결문 원문 직접 확인). ⚠️무효 5건은 2026-08-12 ITC·CDCA 신규 제소의 주장 특허 4건(10,025,731 / 10,217,523 / 12,373,366 / 12,675,407)과 번호가 겹치지 않는다 — 신규 소송의 청구는 소멸되지 않았으며 본 판결은 이 축의 리스크 해소가 아니다(c_20260919_MU_6, inference·moderate). 법률 사건의 결과이지 매출·마진·현금흐름·가이던스 수치가 아니므로 상향 근거로 쓸 수 없다(P2). ② [fact · grade 1 · confirmed] ITC 절차 식별자는 DN 3930으로 특정되고 접수공고(2026-08-17) 관보 게재까지 확인되나, 2026-09-19 시점 조사개시(institution) 공고는 관보 미게재다 — 부재는 미표결의 반증이 아니다(P5, c_20260919_MU_7). ③ [확인 대상 · grade 4 · confirmed=false · 단독 근거 부적격(P4)] CDCA 사건 식별자는 8:26-cv-02167(도켓상 제소일 2026-08-10)로 조회되며, 2026-09-02자 엔트리 #16에 답변기한 연장이 기록됐으나 연장 후 새 시한 날짜는 미특정이다(c_20260919_MU_8). 도켓상 제소일은 본 축이 기재한 2026-08-12와 불일치하나 어느 쪽도 정정하지 않고 병기한다(P9). ④ [확인 대상 · grade 4 · confirmed=false · 단독 근거 부적격(P4)] Micron이 Netlist를 상대로 제기한 비침해 확인의 소 D.Del 1:26-cv-01014(도켓상 제소일 2026-08-10)가 본 회차에 처음 포착됐다 — 대상 특허, ITC 조사개시 시 28 U.S.C. §1659 정지 해당 여부 모두 미확인이며 리스크 경감 근거로 단독 사용하지 않는다(c_20260919_MU_9). ③④는 사건 식별자 자체가 PACER 미러 단독 소스이므로 확정 사실이 아니라 확인 대상으로만 둔다. 추적점(갱신): ITC DN 3930 institution 표결·관보 공고 / CDCA 8:26-cv-02167 연장 답변시한 확정일과 답변 내용(grade 4 확인 대상) / D.Del 1:26-cv-01014 진행 상태·대상 특허(grade 4 확인 대상) / CAFC 2025-1936(Netlist v. Micron Technology Texas) 선고"}
```

### 왜

[fact] state/thesis_cards/MU.yaml 전문 71행을 읽고 목록형 필드를 실제 계수했다 — axes 6 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / earnings_checkpoints.items 7(F20). 본 패치는 기존 ip_litigation_risk 축 1개의 라벨에 관측점을 덧붙일 뿐이므로 axes는 6개 불변이다. [fact] 2026-09-02 CAFC가 Netlist v. Micron 항소 3건을 전부 AFFIRMED해 Netlist 특허 5건의 쟁점 청구항이 무효 판단을 받았다 — 판결문 PDF 원문 직접 확인, evidence_grade 1·confirmed(c_20260919_MU_5). 이 한 건만이 본 패치에서 사실로 단정 가능한 재료다(P4). [fact] 카드가 기재한 ITC 제소의 절차 식별자가 DN 3930으로 특정되고 접수공고(2026-08-17)까지 확인되나 조사개시 공고는 2026-09-19 시점 관보 미게재다 — 연방관보 공식 API 대사, grade 1·confirmed(c_20260919_MU_7). 미게재는 미표결의 반증이 아니다(P5). [fact] 직전 회차에 '1:26-cv-00246 / 5-26-cv-00246 상호 불일치'로 미해결 이월됐던 CDCA 사건 식별자가 본 회차에 8:26-cv-02167로 조회됐고, 카드에 한 번도 등재된 적 없는 D.Del 1:26-cv-01014(Micron→Netlist 비침해 확인의 소)가 신규 포착됐다 — 다만 두 건 모두 CourtListener/RECAP (PACER 미러, sources.yaml 미등재) 단독 소스로 evidence_grade 4·confirmed=false다(c_20260919_MU_8·c_20260919_MU_9). [fact] P4상 grade 3·4는 삼각검증용이며 단독 판단 근거가 될 수 없으므로, 두 식별자는 사실로 단정하지 않고 라벨 본문에 '확인 대상 · grade 4 · confirmed=false · 단독 근거 부적격' 표기를 붙여 기입했다. 카드의 기존 '추적점' 항목을 구체화하는 관측 단위 갱신이며 방향(강화·훼손) 판정은 포함하지 않는다. [fact] 무효 인용된 특허 5건(10,949,339 / 11,016,918 / 11,232,054 / 8,787,060 / 9,318,160)은 2026-08-12 신규 제소의 주장 특허 4건(10,025,731 / 10,217,523 / 12,373,366 / 12,675,407)과 번호가 겹치지 않는다(c_20260919_MU_6, grade 1·inference·moderate) — 따라서 라벨에 '신규 소송의 청구는 소멸되지 않았으며 본 판결은 이 축의 리스크 해소가 아니다'를 명시적으로 심어 오독 경로를 차단했다. [fact] 03_signal/MU.json은 이 재료를 P2 상향 게이트 부적격(revenue_recognized=false)으로 판정해 holding_reinforcement로만 분류했다 — 본 패치는 등급이 아니라 축의 관측점만 기입한다(P13). [fact] 도켓상 제소일 2026-08-10과 카드 기재 2026-08-12의 불일치는 grade 4 소스만으로 정정할 수 없으므로 양쪽을 병기 상태로 두었다(P9). [fact] 2026-09-30 FY26 Q4 실적은 본 패치 작성 시점에 미도래이며 어떤 추정치도 반영하지 않았다. 저 P/E를 밸류 근거로 쓰는 서술도 포함하지 않았다.

**근거 Claim**: c_20260919_MU_5, c_20260919_MU_8, c_20260919_MU_9, c_20260919_MU_6, c_20260919_MU_7

[fact] L4가 지정한 후보 근거는 c_20260919_MU_5·c_20260919_MU_8·c_20260919_MU_9 3건이다. 여기에 c_20260919_MU_6(특허 비중첩, grade 1·inference·moderate)과 c_20260919_MU_7(ITC DN 3930 특정 및 조사개시 미게재, grade 1·confirmed)을 추가로 적시했다 — 새 후보를 만든 것이 아니라 동일 후보 안에서 P4를 지키기 위한 조치다: (a) 'ITC DN 3930'이라는 식별자를 사실로 적으려면 grade 1 근거 c_7이 필요하고, (b) '리스크 해소로 읽히지 않게' 하려면 비중첩 판단 c_6이 근거로 필요하다. 등급별 사용 한계 — c_5(grade 1·confirmed): 사실 단정 가능. c_7(grade 1·confirmed): 사실 단정 가능. c_6(grade 1·inference·moderate): 추론으로 표기. c_8·c_9(grade 4·confirmed=false): 사실 단정 불가, 확인 대상으로만 기재(P4).

**F20 주석**: [fact] state/thesis_cards/MU.yaml 전문 71행을 읽은 뒤 before 문자열의 원문 일치(스크립트 substring 대조)와 목록형 필드 계수를 확인했다 — axes 6개(패치 후에도 6개), key_metrics 7, catalysts 4, risks 4, kill_conditions_ref 5, earnings_checkpoints.items 7, version_history 4. 부분 읽기 기반 '부재·누락' 판정은 하지 않았다. [fact] not_contains는 원문 라벨의 종결부 'grade 4 미확인)"}'를 지정한다 — after에서는 그 뒤로 관측점 문자열이 이어지므로 이 종결 형태가 사라지고, after 본문 어디에도 동일 문자열이 재등장하지 않는다(자기모순 없음, 2026-08-16 ap_20260816_0010 유형 자동 원복 사고 회피).

---

## 패치 B — `axes[hbm_demand]` 축 분해 / `decompose` / priority medium

> 🚨 **선행 인간 결정 의존 — `depends_on_human_decision: axis_naming_standardization`**
> 축 명명 표준화 결정이 **선행되지 않으면 이 패치는 승인 부적절**하다. 3섹터 모두 종목 간 공유 축이 **0개**(neocloud 0/14, stablecoin 0/18)인 상태에서 개별 카드의 축 수만 늘리면 **공유 축 0이 고착**돼 섹터 결합 문제가 악화된다.
> 패치 자체는 생성했으나, **순서 결정은 사람 영역**이다(CLAUDE.md §9). 표준화 결정 확정 전 `approve` 금지.

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
-  - {id: hbm_demand,       label: "HBM 매출 비중·마진 (AI CapEx 연동)"}
+  # 2026-09-19 ThesisPatch(decompose, run 20260919_2209) — 이전 축: {id: hbm_demand, label: "HBM 매출 비중·마진 (AI CapEx 연동)"}(P9 보존, 삭제 아님). 수요 강·약 차원과 생산 가동 연속성 차원을 분리한다(P8 준용). 축 수 6 → 7(전문 71행 기준 계수). 🚨선행 인간 결정 의존: depends_on_human_decision = axis_naming_standardization. 축 명명 표준화 결정이 선행되지 않으면 본 분해는 섹터 결합 문제를 악화시킬 수 있다 — 3섹터 모두 종목 간 공유 축이 0개(neocloud 0/14, stablecoin 0/18)인 상태에서 축 수만 늘리면 공유 축 0이 고착되기 때문이다. 순서 결정은 사람 영역이므로 선행 결정 없이 본 패치를 승인하는 것은 부적절하다.
+  - {id: hbm_demand_strength, label: "HBM 수요 강·약 — HBM 매출 비중·마진 (AI CapEx 연동). 분해 전 hbm_demand 축의 원래 방향 차원을 그대로 승계한다. 방향 판정은 확정된 매출·마진·현금흐름·가이던스 수치로만 한다(P2). 2026-09-19 시점 창 내 신규 수치 없음(c_20260919_MU_12) — 관측점: 2026-09-30 FY26 Q4 실적의 HBM 비중·마진(미도래, 추정 금지)"}
+  - {id: production_continuity, label: "생산 가동 연속성 — 수요와 무관하게 공급 실행이 끊길 수 있는 차원(대만 Taoyuan·Taichung 노사 조정 절차 등). 분해 사유: 대만 노사 리스크가 hbm_demand 축 아래 기록돼 왔으나 그 축의 방향(수요 강·약)과 리스크의 성격(가동 연속성)은 서로 다른 차원이며, 직전 회차 이월 항목이 본 회차에도 미해소다. ⚠️현재 유일 소스가 grade 3·confirmed=false(Reuters 재게재본, 회사 1차 공시 미등재, c_20260919_MU_11)이므로 이 축의 존재 근거는 '축 구조 문제'에 한정되며 방향(강화·훼손) 판정은 부여하지 않는다(P4 — 단독 판단 근거 불가). 03_signal/MU.json도 규칙3 하향 자격 기준(grade≤2) 미달로 판정했다. 관측점: 2026-09-21 2차 조정 결과, 파업투표 실시 여부, 본 사안의 회사 1차 자료(8-K·IR) 등재 여부"}
```

### 하위 축 (P8)

| id | 차원 | 관측 가능 | 방향 판정 | 활성화 조건 |
|---|---|---|---|---|
| `hbm_demand_strength` | 수요 강·약 | 예 | 미부여 | 확정된 매출·마진·가이던스 수치(회사 실적·1차 공시)로만 방향 판정(P2) |
| `production_continuity` | 생산 가동 연속성 | 아니오 | 미부여 | 회사 1차 자료(8-K·IR) 또는 grade≤2 소스로 조정 결렬·파업 개시·가동 영향이 확인될 때 부호 활성화. 현재 근거는 grade 3 단독이라 미활성 |

### 왜

[fact] state/thesis_cards/MU.yaml 전문 71행을 읽고 계수한 결과 axes는 6개이며 hbm_demand 축의 라벨은 'HBM 매출 비중·마진 (AI CapEx 연동)' 단문으로 수요 강·약 차원만 표현한다(F20). 본 패치 적용 시 axes는 7개가 된다. [fact] 그럼에도 대만 노사 리스크는 hbm_demand 축 아래 기록돼 왔다 — 03_signal/MU.json의 thesis_delta_summary가 c_20260919_MU_11을 axis=hbm_demand로 귀속시키고 있다. 축 방향(수요의 강·약)과 리스크 성격(생산 가동의 연속성)은 서로 다른 차원이며, 직전 회차 이월 항목이 본 회차에도 미해소다. [inference:medium] 성격이 다른 두 차원이 한 슬롯에 있으면 축 방향의 시계열 해석이 왜곡된다 — 가동 중단 리스크 증가를 'HBM 수요 약화'로 읽는 오독이 대표적이다. [fact] 본 분해는 P8의 엄격 요건(새 1차 자료가 기존 축 판정을 뒤집음)을 충족하지 않는다 — 축 판정이 뒤집힌 것이 아니라 축이 담는 대상이 갈라진 사례이며, 근거 재료 c_20260919_MU_11 자체가 grade 3·confirmed=false다. 따라서 이 claim은 축 구조 논거로만 사용하고 어떤 사실 주장이나 방향 판정의 근거로도 쓰지 않았다(P4). [fact] 하위 축 어느 쪽에도 방향(강화·훼손) 판정을 부여하지 않으며 이전 축 서술은 주석으로 보존한다(P9). [fact] 🚨선행 결정 의존성 — L4 기록에 따르면 축 명명 표준화 결정이 선행되지 않으면 개별 카드의 축 분해가 섹터 결합 문제를 악화시킨다. 3섹터 모두 종목 간 공유 축이 0개(neocloud 0/14, stablecoin 0/18)인 상태에서 축 수를 늘리면 공유 축 0이 고착되기 때문이다. 순서 결정은 사람 영역이므로(CLAUDE.md §9) 패치는 생성하되 선행 결정 없는 승인은 부적절하다 — depends_on_human_decision 필드로 고정 표기했다. [fact] 2026-09-30 FY26 Q4 실적은 미도래이며 어떤 추정치도 반영하지 않았다. 저 P/E를 밸류 근거로 쓰는 서술도 포함하지 않았다.

**근거 Claim**: c_20260919_MU_11

[fact] c_20260919_MU_11은 evidence_grade 3·confirmed=false(Reuters 기사의 Investing.com 재게재본, reuters.com 원문 역추적 실패, 회사 1차 공시 미등재)다. P4에 따라 사실 주장이나 방향 판정의 단독 근거로 쓸 수 없으므로 '축 구조가 서로 다른 차원을 한 슬롯에 담고 있다'는 구조 논거로만 사용했다. 금액 표기가 직전 회차 보도와 불일치한다는 점도 02_company/MU.json에 기록돼 있어 정량 근거로 사용하지 않았다.

**F20 주석**: [fact] state/thesis_cards/MU.yaml 전문 71행을 읽은 뒤 before 문자열의 원문 일치(다중 공백 정렬 'hbm_demand,' 뒤 7칸 포함)와 axes 6개 계수를 확인했다. 적용 후 기대 개수는 7개이며 expected_after.counts로 고정했다(F20). [fact] P9 보존 주석 안의 이전 축 표기는 '{id: hbm_demand, label: ...}' 단일 공백 형태이므로 not_contains(원문 다중 공백 정렬)와 충돌하지 않는다.

---

## 미패치 / 제외

- **제외한 후보: 없음** — L4 후보 2건 전량 패치화. 새 후보 창작 없음.
- [fact] risks·key_metrics·catalysts·earnings_checkpoints·valuation·conclusion·kill_conditions_ref는 수정하지 않았다 — 이번 창에 해당 필드를 부정확하게 만든 근거가 없다(P5). 미확인 항목은 03_signal/MU.json#unconfirmed_carried 9건으로 이월돼 있다. [fact] 2026-09-30 FY26 Q4 실적은 미도래이며 추정·선반영하지 않았다. 저 P/E를 밸류 근거로 쓰는 서술도 생성하지 않았다.
- 미확인 항목은 `output/20260919_2209/03_signal/MU.json#unconfirmed_carried`(9건)으로 이월 유지 — 본 스킬은 신규 unconfirmed를 생성하지 않았다(적재 대상 부재).

> 두 패치 모두 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).