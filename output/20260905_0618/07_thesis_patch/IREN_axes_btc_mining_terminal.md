# ThesisPatch — IREN / axes / annotate

- **Run**: 20260905_0618 · 2026-09-05T06:18 (L4 병행 `thesis-refine`)
- **대상 필드**: `axes` (expected_after.counts: axes=6 — F20)
- **operation**: `annotate`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: 대상 카드 전문 열람 후 before 문자열의 카드 원문 일치 확인 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음)

## diff

```diff
--- state/thesis_cards/IREN.yaml (before)
+++ state/thesis_cards/IREN.yaml (after 제안)
@@ -1 +1,2 @@
-  - {id: btc_mining,           label: "BTC 채굴 현금흐름 (KC-3 연동)"}
+  # 2026-09-05 ThesisPatch(annotate, run 20260905_0618) — 이전 축: {id: btc_mining, label: "BTC 채굴 현금흐름 (KC-3 연동)"}. 축은 유지하고 회사가 최초로 제시한 종료 목표 시점을 병기한다. 축 수 6개 불변(전문 기준 계수). ⚠️중복 방지 확인: 승인 대기 중인 ap_20260829_1107_* 6건의 대상 필드는 key_metrics·risks·catalysts·earnings_checkpoints·valuation·conclusion이며 axes를 건드리는 패치는 없다. 6건의 after 전문을 대조한 결과 채굴 종료 시점을 담은 서술도 없다 — 필드·내용 모두 비중복.
+  - {id: btc_mining,           label: "BTC 채굴 현금흐름 (KC-3 연동). ⚠️2026-08-27 FY26 실적콜에서 CFO Anthony Lewis가 'We currently expect mining operations to be effectively decommissioned by the end of December 2026'로 종료 목표 시점을 최초 제시 (grade 2 — Motley Fool·Seeking Alpha·Benzinga·stockanalysis.com 4개 독립 전사 문자열 일치. 회사 공식 웹캐스트 원본 대조는 미실시 — 잔여 캐비어트). 'currently expect'는 확정 실행이 아닌 현 시점 기대치 표명이므로 이행 완료로 취급하지 않는다(P7). 계획대로면 이 축의 현금흐름 기여는 2026-12월 말로 소멸하며, 리스크는 소멸이 아니라 ai_cloud_conversion으로 완전 이관된다 — 이후 현금흐름 방어선은 전적으로 AI Cloud 가동률·인도 진척에 의존한다. KC-3(BTC < $55,000 + VIX ≥ 25 → IREN 축소 검토)의 IREN 연동 근거도 채굴 종료 시 재검토 대상이나 KC 수정은 사용자 영역이다"}
```

## 왜

[fact] 2026-08-27 실적콜에서 CFO가 채굴 설비의 사실상 해체 완료 목표를 '2026년 12월 말'로 최초 제시했다(IREN-0905-C05, grade 2 — 4개 독립 전사 문자열 일치). Co-CEO도 동일 취지로 일관되게 언급했다. [fact] 카드 axes의 btc_mining은 종료 시점 정보 없이 'BTC 채굴 현금흐름 (KC-3 연동)'으로만 서술돼 있어, 축의 기여가 특정 시점에 소멸 예정이라는 사실이 카드 어디에도 없다. [fact] 축 수는 전문 기준 6개이며 본 패치는 개수를 바꾸지 않는다. [fact] 중복 방지 — 승인 대기 중인 ap_20260829_1107_* 6건의 대상 필드는 key_metrics·risks·catalysts·earnings_checkpoints·valuation·conclusion이고 axes를 건드리는 건은 없다. 6건 after 전문 대조 결과 채굴 종료 시점 서술도 없다. [inference:strong] 채굴 종료가 계획대로 진행되면 이 축은 리스크가 소멸하는 것이 아니라 ai_cloud_conversion으로 완전 이관된다(IREN-0905-I03) — 축 라벨에 종료 시점이 없으면 이 이관 구조가 카드에서 관측되지 않는다. [fact] 'currently expect'는 확정 실행이 아니므로 P7에 따라 이행 완료로 표기하지 않는다.

**역전 판정 주석**: [fact] thesis 본문('BTC 채굴 현금흐름을 AI Cloud 계약 매출로 전환한다')의 방향을 유지하며 재확인하는 서술이다 — 역전이 아니다. 축 삭제·통합도 하지 않는다.

**후속 주의**: [fact] 채굴 종료가 실제 완료되면 kill_conditions_ref의 'KC-3' 연동 근거와 config/kill_conditions.yaml의 KC-3 consequence('IREN 50% 축소 + Next 진입 보류 검토')가 재검토 대상이 되나, KC 수정·임계 확정은 사용자 영역이므로 본 패치는 제안하지 않고 표기만 한다(P11 · CLAUDE.md §9). [fact] FY27 capex $25-30bn(IREN-0905-C01, grade 2 승격)은 승인 대기 중인 ap_20260829_1107_thesis_patch_iren_earnings_checkpoints_fy27q1의 items에 이미 'FY27 capex 확정치 및 조달 구성 (2차 매체 $25-30B — 등급 1·2 대조 필요)'으로 포함돼 있어 중복 패치를 생성하지 않았다 — 등급 승격 사실은 보고서로만 전달한다.

## 근거 Claim

IREN-0905-C05, IREN-0905-I03

출처: `output/20260905_0618/02_company/IREN.json#claims[IREN-0905-C05] · #claims[IREN-0905-I03] · #deltas[btc_mining]`

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
