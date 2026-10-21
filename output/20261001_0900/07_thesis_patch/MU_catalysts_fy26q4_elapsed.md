# ThesisPatch — MU / catalysts — catalysts[0] '9/30 Q4 FY26 실적'에 경과·이행 표기 + 다음 실적 촉매(FQ1-27, 정확일 미공시) 병기 / amend

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `MU_catalysts_fy26q4_elapsed` · priority: medium
- **대상 필드**: `catalysts` — catalysts[0] '9/30 Q4 FY26 실적'에 경과·이행 표기 + 다음 실적 촉매(FQ1-27, 정확일 미공시) 병기
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — MU 5건(key_metrics / earnings_checkpoints / catalysts / risks / axes)은 서로 다른 행을 치환하고 counts는 각자 필드만 검사한다(드라이런 단독·순차 모두 통과). 권장: MU_key_metrics → MU_earnings_checkpoints → MU_catalysts → MU_risks → MU_axes
- **사전 확인(F20)**: `state/thesis_cards/MU.yaml` 전문 80행 열람, before 출현 1회 확인. 현재 계수 axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / version_history 8 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "catalysts", "n": 4}] · contains 2건 · not_contains 1건

## diff

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
-  - "9/30 Q4 FY26 실적 — 회사 공식 확정(2026-08-26 보도자료, 2026-09-30 14:30 MT 실적 발표·컨퍼런스콜)"
+  - "9/30 Q4 FY26 실적 — 회사 공식 확정(2026-08-26 보도자료, 2026-09-30 14:30 MT 실적 발표·컨퍼런스콜) — [경과 2026-10-01 정리] 2026-09-30 8-K(Item 2.02) 제출로 이행 완료(c_20261001_MU_1). 결과는 key_metrics·earnings_checkpoints 참조. 다음 실적 촉매: FQ1-27 실적(2026-12 추정, 정확일 미공시 — 회사 공지 전 가정, F1)"
```

## 왜

[fact] state/thesis_cards/MU.yaml 전문 80행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / earnings_checkpoints.items 8 / version_history 8(F20). [fact] catalysts 1번째 항목은 2026-09-30 실적을 미래 촉매로 기재하고 있으나 2026-09-30 Form 8-K(Item 2.02·9.01, accession 0000723125-26-000018)가 제출돼 촉매가 경과했다(c_20261001_MU_1, grade1·confirmed). 원문은 보존하고 경과 표기만 덧붙인다(P9). [inference · moderate] 다음 실적 촉매 월(2026-12)은 회사 확정 공지가 아닌 회계분기 구조상 가정이다(F1). [fact] '8/21 Apple CXMT/YMTC 상원 서한 시한' 항목도 일자가 경과했으나 창 내 결과를 보여 주는 Claim이 없어(c_9 무언급만 존재) 본 패치 범위에서 제외했다(근거 부족 — 패치 금지 규칙).

**역전 판정 주석**: [fact] 촉매 경과 표기이며 논거와 무관.

## 근거 Claim

c_20261001_MU_1

[fact] c_1: SEC EDGAR 8-K, grade1·confirmed.

출처: `output/20261001_0900/03_signal/MU.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/memory.json#axis_view,earnings_cycle_context · output/20261001_0900/03_input/arbiter_MU.json(수치·문구 대조)`

**F20 주석**: [fact] before는 카드 45행 전체 원문이며 출현 1회 확인. after는 닫는 따옴표 앞에 서술을 덧붙인 형태 — not_contains(원 항목 종결부+개행)로 덧붙임 적용을, contains 2번째로 원문 보존을 검증한다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
