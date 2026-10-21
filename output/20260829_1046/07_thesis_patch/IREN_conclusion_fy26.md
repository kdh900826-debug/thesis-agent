# ThesisPatch — IREN / conclusion / amend

- **Run**: 20260829_1046 · 2026-08-29T10:46 (`run earnings IREN` — FY26 실적 대응 S2E)
- **대상 필드**: `conclusion` (expected_after.counts: 해당 없음(목록형 필드 아님) — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 검증**: before 문자열의 카드 원문 존재 확인 ✅ · 6건 동시 적용 dry-run에서 YAML 파싱 / contains / not_contains / counts 전건 통과 ✅

## diff

```diff
--- 
+++ 
@@ -1,3 +1,12 @@
+# 2026-08-29 ThesisPatch(amend, run 20260829_1046) — 이전 conclusion:
+#   "계약의 물리적 이행은 1단계에 한해 입증됐으나 재무적 전환은 8/27에 처음 계량된다.
+#    상향 게이트는 정량 수치이며, 인도 완료 자체는 홀딩 강화 신호에 그친다."
 conclusion: >
-  계약의 물리적 이행은 1단계에 한해 입증됐으나 재무적 전환은 8/27에 처음 계량된다.
-  상향 게이트는 정량 수치이며, 인도 완료 자체는 홀딩 강화 신호에 그친다.
+  8/27 FY26 실적으로 물리적 이행과 재무적 전환이 각각 한 단계씩 진전했으나 서로 다른 계약에서 진전했다.
+  Horizon 1은 Microsoft에 인도·인수됐고(P7 2단 통과) Q4 AI Cloud 매출 비중은 51.4%로 채굴을 역전했다.
+  그러나 Microsoft·Horizon 계약은 ASC842 리스로 분류돼 FY26 인식 매출이 0이므로,
+  Q4 매출 역전을 만든 $70.5M에는 thesis의 핵심 계약이 포함돼 있지 않다.
+  즉 재무적 전환은 계량되기 시작했으나 thesis가 근거로 삼는 계약의 전환은 아직 손익계산서에 진입하지 않았다.
+  실행 갭의 성격도 이동했다 — "미계약 $600M"이 해소되고 "계약 완료·미가동 $3.0B"가 그 자리에 들어섰으며,
+  그 해소 기한(2026-12-31)이 Horizons 2-4 인도 기한과 같은 구간에 몰려 있다.
+  상향 게이트는 여전히 정량 수치이며, 다음 판정점은 FY27 Q1의 ASC842 리스 매출 최초 인식 금액이다.
```

## 왜

[fact] 현행 conclusion은 '재무적 전환은 8/27에 처음 계량된다'는 미래형 문장으로, 해당 이벤트가 지난 지금 카드의 결론이 과거를 가리킨다. [fact] 8/27 결과: Horizon 1 인도·인수 완료(C13), Q4 AI Cloud 비중 51.4% 역전(C03), Microsoft·Horizon 계약의 ASC842 분류로 FY26 리스 매출 인식 0(C14). [inference:strong] 세 사실을 함께 놓으면 '매출 역전은 일어났으나 그 역전을 만든 매출에 thesis 핵심 계약이 포함되지 않았다'는 것이 이번 분기의 정확한 요약이며, 현행 문장은 이 구분을 담지 못한다. [fact] 실행 갭의 재정의(I04)도 결론에 반영되지 않은 상태다.

**역전 판정 주석**: [fact] thesis 본문(수직 통합 마진 우위 + 채굴→AI Cloud 전환)의 방향을 유지하며, 진전 사실과 미진전 사실을 함께 기재한다. [inference:medium] 다만 'thesis 핵심 계약이 아직 손익계산서에 없다'는 서술은 기존 결론보다 유보적이므로 사람의 확인이 특히 필요하다.

**후속 주의**: [fact] 이 패치는 signals.json의 등급을 바꾸지 않는다 — 등급 확정은 사람이며 시그널 판정은 03_signal/IREN.json에 후보로만 존재한다.

## 근거 Claim

IREN-2608-C03, IREN-2608-C10, IREN-2608-C13, IREN-2608-C14, IREN-2608-C16, IREN-2608-I01, IREN-2608-I03, IREN-2608-I04

출처: `output/20260829_1046/02_company/IREN.json` (validate-output --layer company PASS)
· 체크포인트 대조표: `output/20260829_1046/02E_earnings/IREN_checkpoints_20260827.md`

> 이 패치는 제안이며 자동 반영되지 않는다. 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
