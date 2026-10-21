# ThesisPatch — IREN / catalysts / amend

- **Run**: 20260829_1046 · 2026-08-29T10:46 (`run earnings IREN` — FY26 실적 대응 S2E)
- **대상 필드**: `catalysts` (expected_after.counts: catalysts=4 — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 검증**: before 문자열의 카드 원문 존재 확인 ✅ · 6건 동시 적용 dry-run에서 YAML 파싱 / contains / not_contains / counts 전건 통과 ✅

## diff

```diff
--- 
+++ 
@@ -1,5 +1,9 @@
 catalysts:
-  - "8/27 17:00 ET FY26 실적 — 최대 분수령"
-  - "Horizons 2-4 인도 ('later this year', 구체 일정 미공시)"
-  - "PUCT SB6 최종 규칙 (2026말)"
-  - "차세대 GPU 배정"
+  # 2026-08-29 ThesisPatch(amend, run 20260829_1046) — 8/27 촉매 소진, 후속 촉매로 대체. 항목 수 4개 불변.
+  # 이전: "8/27 17:00 ET FY26 실적 — 최대 분수령" (2026-08-27 발생·소진)
+  - "FY27 Q1 10-Q (2026년 11월 경) — ASC842 리스 매출 최초 인식 금액. 사전 정의 상향 게이트 ⑪(Horizon 1 인식 금액)의 유일한 관측점"
+  # 이전: "Horizons 2-4 인도 ('later this year', 구체 일정 미공시)" — 일정 구체화
+  - "Horizons 2-4 인도 — 역년 Q4 2026 단계 인도 목표, 계약상 유예 2026 Q4 중반~2027 Q2 초"
+  - "PUCT SB6 최종 규칙 (2026말) — IREN 적용 용량 MW 공개 시 KC-10 임계 대조 성립"
+  # 이전: "차세대 GPU 배정" — VR200 포트폴리오 편입 확인으로 관측 대상 구체화
+  - "가동 ARR $1.0B → $4.0B 진척 (회사 제시 기한 2026-12-31) / 차세대 GPU 배정 — VR200은 6/30 기준 설치·발주 포트폴리오에 편입 확인"
```

## 왜

[fact] 카드 1번 촉매 '8/27 17:00 ET FY26 실적'은 2026-08-27에 발생해 소진됐다. 소진된 촉매를 남겨두면 next_gate 판정이 과거를 가리킨다. [fact] 2번 촉매의 'later this year, 구체 일정 미공시'는 '역년 Q4 2026 + 유예 2027 Q2 초'로 갱신됐다(C16). [fact] 4번 '차세대 GPU 배정'은 VR200의 포트폴리오 편입 확인으로 관측 대상이 구체화됐다(C29). [inference:strong] 사전 정의 상향 게이트가 ⑪ 금액에 걸려 있고 그 유일한 관측점이 FY27 Q1 10-Q이므로 이를 1번 촉매로 승격하는 것이 게이트 구조와 정합적이다. [fact] 항목 수 4개 불변, 이전 값 주석 보존(P9).

**역전 판정 주석**: [fact] 소진 촉매 교체와 일정 구체화이며 방향 판정을 내리지 않는다.

**후속 주의**: [fact] state/signals.json의 IREN next_gate('8/27 실적의 과금 가동률·AI Cloud 매출 비중·MW당 매출')도 동일하게 소진됐다 — 등급 확정 시 사람이 함께 갱신해야 한다(F17: 에이전트는 signals.json을 자동 수정하지 않는다).

## 근거 Claim

IREN-2608-C10, IREN-2608-C14, IREN-2608-C16, IREN-2608-C24, IREN-2608-C29

출처: `output/20260829_1046/02_company/IREN.json` (validate-output --layer company PASS)
· 체크포인트 대조표: `output/20260829_1046/02E_earnings/IREN_checkpoints_20260827.md`

> 이 패치는 제안이며 자동 반영되지 않는다. 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
