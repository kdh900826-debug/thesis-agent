# ThesisPatch — MU / risks — risks에 'Netlist ITC 2개 전선(DDR5 337-TA-1523 + 2026-09-29 HBM 2차 제소)' 항목 추가(4 → 5) / amend

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `MU_risks_netlist_hbm_itc` · priority: high
- **대상 필드**: `risks` — risks에 'Netlist ITC 2개 전선(DDR5 337-TA-1523 + 2026-09-29 HBM 2차 제소)' 항목 추가(4 → 5)
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — MU 5건(key_metrics / earnings_checkpoints / catalysts / risks / axes)은 서로 다른 행을 치환하고 counts는 각자 필드만 검사한다(드라이런 단독·순차 모두 통과). 권장: MU_key_metrics → MU_earnings_checkpoints → MU_catalysts → MU_risks → MU_axes
- **사전 확인(F20)**: `state/thesis_cards/MU.yaml` 전문 80행 열람, before 출현 1회 확인. 현재 계수 axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / version_history 8 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "risks", "n": 5}] · contains 3건 · not_contains 0건

## diff

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
-  - "레버리지 (SOXL·단일종목 2x) decay"
+  - "레버리지 (SOXL·단일종목 2x) decay"
+  # 2026-10-01 ThesisPatch(amend, run 20261001_0900) — 항목 추가 4 → 5(전문 기준 계수). ip_litigation_risk 축(2026-09-05 신설)이 risks 목록에는 반영돼 있지 않았고, 2026-09-29 신규 제소가 thesis 핵심 제품(HBM)을 직접 겨냥해 risks 목록에 독립 항목으로 올린다. 기존 4개 항목 불변.
+  - "특허소송(Netlist ITC 2개 전선) — ① 337-TA-1523(DDR5 RDIMM·MRDIMM, 조사개시 2026-09-24 / 09-23 표기 자료 병기) ② 2026-09-29 신규 2차 ITC 제소: 특허 US 12,308,087·12,646,537, 대상 Micron HBM3E·HBM4·HBM4E, 배제명령·중지명령 청구(c_20261001_MU_10, grade1). ⚠️제소 ≠ 조사개시 ≠ 위반 판정 ≠ 배제명령 ≠ 매출 영향 — ②는 institution 미확정이며 매출·마진 영향은 미확인(P5·P7). 9/30 실적 자료 무언급(c_20261001_MU_9). 상세 관측점은 axes.ip_litigation_risk 참조"
```

## 왜

[fact] state/thesis_cards/MU.yaml 전문 80행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / earnings_checkpoints.items 8 / version_history 8(F20). [fact] risks 4개 항목(사이클 피크 역설·CXMT/YMTC·AI CapEx 감속·레버리지 decay)에 특허소송 리스크가 없다 — 전문 80행에서 risks 블록(50~54행)을 직접 확인했다. ip_litigation_risk는 axes에만 존재한다. [fact] Netlist가 2026-09-29 Micron HBM3E·HBM4·HBM4E를 직접 겨냥한 2차 ITC 제소를 제기했다(c_20261001_MU_10, grade1·confirmed, 자기공시+5개 이상 독립매체 삼각검증). thesis가 'HBM 수요의 AI CapEx 직접 연동'을 핵심 논거로 삼는 만큼 HBM 제품 대상 배제명령 청구는 risks 목록의 독립 항목 요건을 갖춘다. [fact] 03_signal은 이 재료로 규칙3(비대칭 하향) 자격을 2회 연속 독립 충족으로 기록했다 — 본 패치는 등급이 아니라 리스크 목록만 다룬다(P13). [fact] 337-TA-1523 조사개시일은 09-24(c_20260925_MU_3, 카드 기재)와 09-23(c_20261001_MU_11, grade3·confirmed=false)을 정정 없이 병기한다(P9).

**역전 판정 주석**: [inference · moderate] HBM 대상 배제명령 청구는 장래 미국向 HBM 매출 인식 경로에 작용할 수 있으나 현재는 제소 단계(institution 미확정)이며 핵심 논거를 뒤집는 확정 수치가 없다 — 리스크 목록 추가에 그치며 에스컬레이션 대상 아님. MU 전용 KC 신설 여부(5회 연속 미정의, esc_20261001_memory_01)는 사람 결정 영역이며 본 패치는 add_kc를 포함하지 않는다.

## 근거 Claim

c_20261001_MU_9, c_20261001_MU_10, c_20261001_MU_11

[fact] c_10·c_9 grade1·confirmed — 사실 단정. c_11 grade3·confirmed=false — 날짜 병기만(P4). 피조사자 구성(Nvidia·Broadcom·Google의 정식 respondent 여부)은 04_sector esc_20261001_memory_02에서 불일치가 기록돼 있어 risks 문구에 넣지 않았다.

출처: `output/20261001_0900/03_signal/MU.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/memory.json#axis_view,earnings_cycle_context · output/20261001_0900/03_input/arbiter_MU.json(수치·문구 대조)`

**F20 주석**: [fact] before는 카드 54행(risks 마지막 항목) 전체이며 출현 1회 확인. after는 해당 행을 보존하고 그 뒤에 주석 1행+항목 1행을 추가한다. counts risks 5로 추가가 정확히 1개임을 검증한다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
