# ThesisPatch — MU / catalysts / amend

- **Run**: 20260905_0618 · 2026-09-05T06:18 (L4 병행 `thesis-refine`)
- **대상 필드**: `catalysts` (expected_after.counts: catalysts=4 — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: 대상 카드 전문 열람 후 before 문자열의 카드 원문 일치 확인 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음)

## diff

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
@@ -1 +1,2 @@
-  - "9/22 Q4 FY26 실적"
+  # 2026-09-05 ThesisPatch(amend, run 20260905_0618) — 이전: "9/22 Q4 FY26 실적". 9/22는 카드 v1 초기화 시점의 가정일이며 회사 공식 확정 공지에 근거하지 않는다(F1). 항목 수 4개 불변.
+  - "9/30 Q4 FY26 실적 — 회사 공식 확정(2026-08-26 보도자료, 2026-09-30 14:30 MT 실적 발표·컨퍼런스콜)"
```

## 왜

[fact] Micron이 2026-08-26 보도자료(GlobeNewswire + investors.micron.com 동일 확인, grade 1, c_20260905_MU_02)로 FY26 Q4 실적 발표일을 2026-09-30(산악시간 14:30)로 확정 공지했다. [fact] 카드 catalysts의 '9/22'는 v1 기계 판독본 초기화 시점의 가정일이며 회사 공지에 근거하지 않는다 — 애그리게이터·추정 캘린더 라벨을 1차 공시로 취급하지 않는다는 F1의 대상이다. [inference:strong] 실적일은 earnings_checkpoints 대조·run earnings 스케줄·시그널 next_gate가 공통으로 참조하는 기준점이므로 8일 오차를 방치하면 하위 산출물이 연쇄적으로 어긋난다. [fact] 항목 수 4개 불변(전문 기준 계수), 이전 값은 주석으로 보존(P9).

**역전 판정 주석**: [fact] 촉매 일자의 사실 정정이며 thesis 방향·등급 판정을 포함하지 않는다.

**후속 주의**: [fact] 동일 사유로 state/signals.json의 MU.next_gate('9/22 비트그로스 vs ASP 분해·선수금 방향')과 run earnings MU 스케줄도 정정 대상이나 본 패치 범위 밖이다 — 별도 제안 항목으로 보고서에 기록. [fact] 같은 catalysts 목록의 '8/21 Apple CXMT/YMTC 상원 서한 시한'은 시한이 경과했으나 Apple의 공개 응답 확인 자료가 grade 4·confirmed=false(c_20260905_MU_06)뿐이라 이번 패치에서 건드리지 않는다(P4·P5).

## 근거 Claim

c_20260905_MU_02

출처: `output/20260905_0618/02_company/MU.json#claims[c_20260905_MU_02] · #flags_for_thesis_refine[catalyst_date_correction]`

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
