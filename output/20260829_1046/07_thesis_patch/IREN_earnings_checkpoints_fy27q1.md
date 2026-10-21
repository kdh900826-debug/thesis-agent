# ThesisPatch — IREN / earnings_checkpoints / amend

- **Run**: 20260829_1046 · 2026-08-29T10:46 (`run earnings IREN` — FY26 실적 대응 S2E)
- **대상 필드**: `earnings_checkpoints` (expected_after.counts: earnings_checkpoints.items=13 — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 검증**: before 문자열의 카드 원문 존재 확인 ✅ · 6건 동시 적용 dry-run에서 YAML 파싱 / contains / not_contains / counts 전건 통과 ✅

## diff

```diff
--- 
+++ 
@@ -1,16 +1,22 @@
 earnings_checkpoints:
-  date: "2026-08-27"
+  # 2026-08-29 ThesisPatch(amend, run 20260829_1046) — 2026-08-27 체크포인트 세트 소진.
+  # 대조 결과는 output/20260829_1046/02E_earnings/IREN_checkpoints_20260827.md에 보존(P9).
+  # 이전: date "2026-08-27", items 13개(과금 가동률 / MFU / 매니지드 서비스 믹스 / Horizon 건설원가 실측 /
+  #   전력 단위원가 실측 / GPU 대체 조항 / 고객 다변화 / ARR 실현율 / 현금흐름 / 완전희석 주수 확정 /
+  #   Horizon 1 매출 인식 시점·금액 / Horizons 2-4 구체 일정 / SB6 적용 용량)
+  # 이 중 미확인 5건·상충 2건·부분 확인 4건을 이월하고, 신규 관측 대상 2건을 추가해 13개를 유지한다.
+  date: "2026-11 (FY27 Q1 10-Q — 정확일 미공시)"
   items:
-    - "과금 가동률"
-    - "MFU"
-    - "매니지드 서비스 믹스"
-    - "Horizon 건설원가 실측"
-    - "전력 단위원가 실측"
-    - "GPU 대체 조항 (GB300→VR200 단가 재협상)"
-    - "고객 다변화"
-    - "ARR 실현율 vs 가이던스"
-    - "현금흐름"
-    - "완전희석 주수 확정"
-    - "Horizon 1 매출 인식 시점·금액 (FY26 결산 기간 외 — 가이던스·콜 발언에서 확인)"
-    - "Horizons 2-4 구체 일정"
-    - "SB6 적용 용량"
+    - "과금 가동률 (8/27 미공개 — 이월)"
+    - "MFU (8/27 미공개 — 이월)"
+    - "매니지드 서비스 믹스 (Mirantis 첫 연결 분기)"
+    - "Horizon 건설원가 실측 (8/27 미공개 — 이월)"
+    - "전력 단위원가 $/MWh (부문별 전력비는 확보, 소비 MWh 미공시 — 이월)"
+    - "GPU 대체 조항 단가 재협상 (GB300→VR200, 8/27 미공개 — 이월)"
+    - "ASC842 리스 매출 최초 인식 금액 — Horizon 1분 분리 여부 [사전 정의 상향 게이트 ⑪]"
+    - "가동 중 ARR $1.0B → $4.0B 진척률 및 가동 MW"
+    - "Horizon 2-4 인도·인수 완료 여부 (유예 2027 Q2 초 소진 여부)"
+    - "완전희석 주수 range 갱신 (하한 394.06M / 상한 558.72M+)"
+    - "FY27 capex 확정치 및 조달 구성 (2차 매체 $25-30B — 등급 1·2 대조 필요)"
+    - "SB6 적용 용량 MW (KC-10 임계 대조 분모)"
+    - "AI Cloud 부문 감가상각 배분 (자체 ~14% vs 임차 ~5% 전제 검증용)"
```

## 왜

[fact] 카드의 earnings_checkpoints.date는 '2026-08-27'이고 그 이벤트는 발생·처리 완료됐다. 소진된 체크포인트 세트를 남겨두면 다음 run의 state-audit이 과거 게이트를 현재 게이트로 읽는다. [fact] 13항목 대조 결과 미확인 5건(① ② ④ ⑥ ⑪ 금액), 상충 2건(⑧ ⑩), 부분 확인 4건(③ ⑤ ⑦ ⑬), 확인 2건(⑨ ⑫)이다. [inference:strong] 미확인·상충·부분 확인 항목은 그대로 다음 관측점으로 이월돼야 하며, 확인 완료된 ⑨ 현금흐름·⑫ 일정은 신규 관측 대상(리스 매출 인식 금액, 가동 ARR 진척, 감가상각 배분)으로 교체하는 것이 정합적이다. [fact] 이전 date·13항목 전문은 주석에 보존했고 대조표 원본은 02E_earnings에 별도 보존된다(P9). 항목 수 13개 불변.

**역전 판정 주석**: [fact] 관측 항목 목록의 갱신이며 판정을 포함하지 않는다.

**후속 주의**: [fact] 이 패치가 승인되면 다음 run의 state-audit이 참조하는 next earnings gate가 FY27 Q1으로 이동한다. 정확한 발표일은 회사 공지 후 별도 amend로 확정해야 한다.

## 근거 Claim

IREN-2608-C10, IREN-2608-C14, IREN-2608-C15, IREN-2608-C16, IREN-2608-C19, IREN-2608-C22, IREN-2608-C23, IREN-2608-C25, IREN-2608-I02, IREN-2608-I04, IREN-2608-I06, IREN-2608-I12

출처: `output/20260829_1046/02_company/IREN.json` (validate-output --layer company PASS)
· 체크포인트 대조표: `output/20260829_1046/02E_earnings/IREN_checkpoints_20260827.md`

> 이 패치는 제안이며 자동 반영되지 않는다. 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
