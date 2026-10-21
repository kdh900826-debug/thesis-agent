# ThesisPatch — IREN / axes / annotate

- **Run**: 20260911_2308 · as_of 2026-09-12 (L4 `cio-portfolio` 병행 `thesis-refine`)
- **대상 필드**: `axes` (expected_after.counts: axes=6 — F20)
- **operation**: `annotate`
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인**: 대상 카드 **전문** 열람 후 before 문자열의 원문 일치·목록 항목 수 확인 완료 (F20 — 부분 읽기 기반 '부재' 판정 없음)

## diff

```diff
--- state/thesis_cards/IREN.yaml (before)
+++ state/thesis_cards/IREN.yaml (after 제안)
-  - {id: power_permit,         label: "전력·인허가 (TX SB6, PUCT, DC 모라토리엄)"}
+  # 2026-09-12 ThesisPatch(annotate, run 20260911_2308) — 이전 축: {id: power_permit, label: "전력·인허가 (TX SB6, PUCT, DC 모라토리엄)"}(P9 보존). 축은 유지하고 2026-09-08 회사 보도자료(grade 1, confirmed)로 확인된 ERCOT Batch Zero 분류 관측점을 병기한다. 축 수 6개 불변(전문 기준 계수). ⚠️분류는 조건부이며 최종 접속 승인이 아니다. SB6 비상 커테일먼트 트랙과 별개 규제 트랙이므로 KC-10 첫 번째 조건(계약 용량 10%+ 강제 감축 분류)의 분모 공백은 해소되지 않는다.
+  - {id: power_permit,         label: "전력·인허가 (TX SB6, PUCT, DC 모라토리엄). 관측점 2026-09-08(회사 보도자료 grade 1 confirmed): 2GW Sweetwater Hub(Sweetwater1 1,400MW + Sweetwater2 600MW) 전량이 ERCOT Batch Zero 심사에서 Base Load로 조건부 포함. 보도자료가 최종 접속 승인이 아님·에너지화 일자 미확정을 명시하며 송배전사업자 계통접속계약 체결을 전제로 단다 — 계약존재≠이행 3단 분리 준용(P7). 이 분류는 SB6 비상 커테일먼트 의무와 별개 규제 트랙이므로 KC-10의 계약 용량 10%+ 강제 감축 분류 조건과 대조되지 않으며, 그 조건의 분모인 SB6 적용 MW는 여전히 미공시다. Governor Abbott 지시 ERCOT 데이터센터 검증·감사(2026-12 완료 목표) 미종료. Sweetwater1 DC 용량 300MW는 2027 Q4 인도 목표이며 Childress Horizon 1-4와 별개 캠퍼스·별개 일정"}
```

## 왜

[fact] state/thesis_cards/IREN.yaml 전문(134행)을 읽고 확인한 결과 power_permit 축의 라벨은 '전력·인허가 (TX SB6, PUCT, DC 모라토리엄)' 단문이며 관측점 기준선이 없다. [fact] 이번 창의 유일한 실질 재료가 이 축에 들어왔다 — 2026-09-08 07:01 ET 회사 공식 보도자료로 2GW Sweetwater Hub(Sweetwater1 1,400MW + Sweetwater2 600MW) 전량이 ERCOT Batch Zero 심사에서 'Base Load'로 조건부 포함됐다(IREN-0911-C02, evidence_grade 1, confirmed, quantitative, stage=power_interconnection_classification(pre_final_approval)). [fact] 보도자료 자체가 '최종 접속 승인 아님·에너지화 일자 미확정'을 명시하고 송배전사업자 계통접속계약 체결을 전제로 단다. [fact] 03_signal/IREN.json은 이 재료를 규칙2의 명시 예외('분류 승인')로 분류해 holding_reinforcement로만 처리하고 등급을 유지했다 — 본 패치는 등급이 아니라 축의 관측점만 기입한다(P13). [fact] 같은 산출물의 IREN-0911-I01(inference, 강도 medium)은 (a) 지위가 조건부이고 Governor Abbott 지시 ERCOT 감사(2026-12 완료 목표)가 미종료이며 (b) Batch Zero 접속심사와 SB6 비상 커테일먼트 의무가 별개 규제 트랙이라 KC-10 첫 번째 조건의 갭을 메우지 못한다고 기록했다 — 이 두 캐비어트를 라벨 본문에 명시적으로 심었다. [fact] 카드 risks 항목의 'TX SB6 / ERCOT — … ⚠️IREN 계약 용량 중 적용 MW 미공시 — KC-10의 10%+ 임계 대조 분모 부재' 서술은 이번 재료로 해소되지 않으므로 수정하지 않았다(P5 — 부재는 반증이 아니다). [fact] 축 수는 전문 기준 6개(ai_cloud_conversion·execution_delivery·margin_structure·funding_dilution·power_permit·btc_mining)로 불변이며 이전 라벨은 주석으로 보존한다(P9·F20).

**역전 판정 주석**: [fact] thesis 본문(수직 통합 마진 우위 + 채굴→AI Cloud 전환)과 시그널 등급(🟡)에 대한 판정을 포함하지 않는다. [fact] 이 패치는 규제 진척을 '유리한 방향'으로 서술하지 않으며 조건부성·별개 트랙·감사 미종료를 함께 기입한다 — 상향 근거로 쓰일 수 없는 형태다(P2·P6).

**후속 주의**: [fact] earnings_checkpoints의 'SB6 적용 용량 MW (KC-10 임계 대조 분모)' 항목은 이번 재료로 관측되지 않았으므로 유지된다. [fact] catalysts의 'PUCT SB6 최종 규칙 (2026말)'도 별개 트랙이므로 수정하지 않았다. [fact] KC-10 자체의 임계·조건 수정은 config/kill_conditions.yaml 소관이며 사람 영역이다(CLAUDE.md §9).

## 근거 Claim

IREN-0911-C02, IREN-0911-I01

출처: `output/20260911_2308/03_signal/IREN.json#claims[IREN-0911-C02,IREN-0911-I01] · #thesis_delta_summary[power_permit] · output/20260911_2308/04_sector/neocloud.json#structural_observations[so-1]`

**F20 주석**: [fact] state/thesis_cards/IREN.yaml 전문 134행을 읽은 뒤 before 문자열의 원문 일치와 axes 6개 계수를 확인했다(F20). [fact] not_contains 문자열은 원문의 다중 공백 정렬(`power_permit,` 뒤 9칸)을 포함하며, P9 보존 주석은 단일 공백 형태로 기록했으므로 자기모순이 발생하지 않는다 — 2026-08-16 ap_20260816_0010 유형의 자동 원복 사고 회피.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
