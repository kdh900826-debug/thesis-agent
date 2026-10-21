# ThesisPatch — MU / key_metrics — key_metrics 7개 중 6개 항목에 FY26 Q4(2026-09-30) 관측치 덧붙임 — SCA 16→26건·RPO·현금예치금·비트/ASP·HBM 마진 갭·CapEx 미재확인 / amend

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `MU_key_metrics_fy26q4_observations` · priority: high
- **대상 필드**: `key_metrics` — key_metrics 7개 중 6개 항목에 FY26 Q4(2026-09-30) 관측치 덧붙임 — SCA 16→26건·RPO·현금예치금·비트/ASP·HBM 마진 갭·CapEx 미재확인
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — MU 5건(key_metrics / earnings_checkpoints / catalysts / risks / axes)은 서로 다른 행을 치환하고 counts는 각자 필드만 검사한다(드라이런 단독·순차 모두 통과). 권장: MU_key_metrics → MU_earnings_checkpoints → MU_catalysts → MU_risks → MU_axes
- **사전 확인(F20)**: `state/thesis_cards/MU.yaml` 전문 80행 열람, before 출현 1회 확인. 현재 계수 axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / version_history 8 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "key_metrics", "n": 7}] · contains 5건 · not_contains 1건

## diff

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
-key_metrics:
-  - "HBM 매출 비중·마진"
-  - "SCA 건수 및 커버리지 (16건, DRAM 20%+ / NAND 1/3)"
-  - "LTA 비중 및 선수금·계약부채 잔액"
-  - "비트그로스 vs ASP 분해 ('순수 P 사이클' 가설 검증)"
-  - "HBM 마진 vs 범용 마진 (⚠️'HBM이 장기계약 대가로 마진이 더 낮다'는 미검증 가설 — 직접 확인 대상)"
-  - "NTM Forward P/E (~5.95-6.9x)"
-  - "CapEx $50B 계획"
+key_metrics:
+  # 2026-10-01 ThesisPatch(amend, run 20261001_0900) — FY26 Q4 실적(2026-09-30, 8-K Ex-99.1 grade1 + 준비발언 grade2) 관측치를 각 항목 원문 뒤에 덧붙인다. 원문(16건·$50B 등)은 삭제하지 않고 보존한다(P9). 항목 수 7개 불변. ⚠️관측치 기입이며 등급 상향 근거가 아니다 — arbiter upgrade_gate_result=not_met(P2·P7·P12).
+  - "HBM 매출 비중·마진 — [2026-09-30 관측] HBM 단독 매출·비중은 미공개(P5). 대리지표 Cloud Memory BU(HBM 귀속·HBM 전용 아님) FQ4-26 매출 $16,283M·매출총이익률 83%(c_20261001_MU_4, grade1). CEO: FQ4 HBM 매출 성장률이 전사 성장률 상회(c_20261001_MU_5, grade2, 정성)"
+  - "SCA 건수 및 커버리지 (16건, DRAM 20%+ / NAND 1/3) — [2026-09-30 관측] 누적 26건(분기 중 10건 신규), RPO 약 $150B, 26건 SCA·연장분 고객 재무약정 $32B(대부분 현금예치금)(CFO 직접, c_20261001_MU_6, grade2). 16건 시점 커버리지 비율(DRAM 20%+ / NAND 1/3)의 26건 기준 갱신치는 창 내 Claim에 없음(미확인, P5). ⚠️P7: RPO는 계약 존재(미인식 잔여계약)이며 이행·매출 인식이 아니다"
+  - "LTA 비중 및 선수금·계약부채 잔액 — [2026-09-30 관측] 고객 현금예치금 FQ4 수령 $12.3B·분기말 잔액 $12.7B(c_20261001_MU_6, grade2). LTA 비중 수치·계약부채 총액은 창 내 미확인(P5)"
+  - "비트그로스 vs ASP 분해 ('순수 P 사이클' 가설 검증) — [2026-09-30 관측] FQ4-26 DRAM 매출 $39.8B: 비트 QoQ 중간 한자릿수%·가격 QoQ 고10%대 / NAND 매출 $14.1B: 비트 QoQ 약 10%·가격 QoQ 약 30%(CFO 직접, c_20261001_MU_7, grade2). [inference] 가격 주도 패턴은 '구조적 수요 강화'와 '가격 사이클 후반부(피크 역설)' 양방향으로 해석 가능하며 판정은 사람 영역(03_signal 위임, P13)"
+  - "HBM 마진 vs 범용 마진 (⚠️'HBM이 장기계약 대가로 마진이 더 낮다'는 미검증 가설 — 직접 확인 대상) — [2026-09-30 관측] CEO가 2027 HBM 가격 인상 계약이 범용 DRAM과의 매출총이익률 갭을 '축소 중'이라고 직접 발언 — 갭의 존재·축소 방향은 grade2 fact, 크기(%p)는 비공개(c_20261001_MU_5). 대리지표 Cloud Memory BU 83% vs CDBU·MCBU 90%(c_20261001_MU_4). ⚠️'장기계약 대가로'라는 원인 부분은 여전히 미검증"
+  - "NTM Forward P/E (~5.95-6.9x)"
+  - "CapEx $50B 계획 — [2026-09-30 관측] 연간 $50B 총액은 보도자료·준비발언·콜에서 재확인되지 않음(정보 공백, 반증 아님 P5). FY27 capex: FQ1 약 $11.5B, 상반기 약 $25B, 하반기 '더 높음'(방향만)(CFO, c_20261001_MU_8, grade2). FY26 실적 capex(net) $27.37B(c_20261001_MU_2, grade1)"
```

## 왜

[fact] state/thesis_cards/MU.yaml 전문 80행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / earnings_checkpoints.items 8 / version_history 8(F20). [fact] 카드 key_metrics는 'SCA 16건' 등 2026-08-15 초기화 시점 수치를 유지하고 있으나 2026-09-30 FY26 Q4 실적에서 CFO가 SCA 누적 26건·RPO 약 $150B·고객 재무약정 $32B·현금예치금 잔액 $12.7B를 직접 제시했다(c_20261001_MU_6, grade2·confirmed) — 카드의 '16건'은 시점 수치로서 부정확해졌다. [fact] 비트/ASP 분해(c_7)·HBM 마진 갭 방향(c_5)·Cloud Memory BU 마진(c_4)은 카드가 '직접 확인 대상'으로 지정한 항목의 최초 실측 관측치다. [fact] 'CapEx $50B 계획'은 9/30 자료에서 재확인되지 않았으나(c_8) 정보 부재는 반증이 아니므로 원문을 삭제하지 않고 관측 공백만 표기했다(P5·P9). [fact] NTM Forward P/E 항목은 분모(주가)가 L4 입력에 없어 손대지 않았다(P10). [fact] 본 패치는 지표 관측치 기입이며 시그널 등급·상향 판정을 바꾸지 않는다 — 03_signal/MU.json upgrade_gate_result=not_met(sca_defense·hbm_demand_strength=holding_reinforcement, cycle_position=양면적)를 그대로 따른다(P13).

**역전 판정 주석**: [fact] thesis 본문(SCA·take-or-pay·최소가격 보장 방어구조)·conclusion을 수정하지 않는다. [inference · moderate] SCA 26건·현금예치금 증가는 방어 논거와 정합하며 HBM 마진 갭 '존재·축소'도 기존 경고 문구의 범위 안이다 — 핵심 논거 역전 아님.

## 근거 Claim

c_20261001_MU_2, c_20261001_MU_4, c_20261001_MU_5, c_20261001_MU_6, c_20261001_MU_7, c_20261001_MU_8

[fact] c_2·c_4(8-K Ex-99.1, grade1·confirmed), c_5~c_8(IR 공식 배포 준비발언, grade2·confirmed — CEO·CFO 직접 발언). 전부 03_signal/MU.json claims에 인용된 ID이며 수치는 03_input/arbiter_MU.json 원문과 대조했다.

출처: `output/20261001_0900/03_signal/MU.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/memory.json#axis_view,earnings_cycle_context · output/20261001_0900/03_input/arbiter_MU.json(수치·문구 대조)`

**F20 주석**: [fact] before는 카드 34~41행(key_metrics: 키부터 마지막 항목까지) 원문 복사이며 카드 내 출현 1회를 스크립트로 확인했다. not_contains는 원 단독 항목 '  - "CapEx $50B 계획"'+개행이며 after에서는 같은 행에 관측치가 이어지므로 사라진다. contains 2번째 항목은 16건 원문 보존(P9)을 검증한다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
