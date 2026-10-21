# ThesisPatch — IREN / earnings_checkpoints / amend (체크포인트 13개 복원)

- **Run**: 20260816_0000 · 2026-08-16 (8/27 실적 대응 준비 세션)
- **대상 필드**: `earnings_checkpoints.items`
- **operation**: `amend` (누락 복원)
- **승인 필요**: ✅ `requires_human_approval: true`
- **핵심 논거 역전 여부**: ❌ 아님 — 설계서 원문 항목의 복원(정합성 정정)

## 무엇을

카드의 체크포인트 7개에 설계서 v1 §5-1의 누락분 6개(⑧~⑬)를 복원해 13개로 만든다:

```diff
      - "고객 다변화"
+     - "ARR 실현율 vs 가이던스 (ARR $4.0B 중 미계약 ~$600M 실행 갭)"
+     - "현금흐름"
+     - "완전희석 주수 확정 (495M vs 508M 충돌 해소 — 단일값 사용 금지, F9 range 유지)"
+     - "Horizon 1 매출 인식 시점·금액 (FY26 결산 기간 외 사건 — 가이던스·콜 발언에서 확인. 유일한 revenue_recognized 상향 게이트 후보, P2·P7)"
+     - "Horizons 2-4 구체 일정"
+     - "SB6 적용 용량 (KC-10·power_permit 축 연결)"
```

## 왜 — 이 누락은 상향 판정 경로를 막는다

- [fact] 설계서 v1 §5-1 = 13개 / 카드 = 7개 / company-iren.md 에이전트 정의 = "13개 대조표 작성" — 삼자 불일치.
- [fact] S2E 성공 기준은 "카드의 체크포인트 **전 항목** 분류"다 — 카드가 6개를 누락하면 8/27 run earnings가 커버리지 결손을 무감지로 통과한다.
- [inference:strong] 누락분 ⑪ **Horizon 1 매출 인식 시점·금액**은 상향 3중 게이트의 `revenue_recognized`를 충족할 수 있는 **유일한 후보**다. 비중 95% 종목의 상향 판정 경로가 카드 결손으로 막혀 있던 셈이다.
- [fact] 실적일 8/27 17:00 ET는 회사 공식 발표로 재확인 완료 (GlobeNewswire 2026-08-13 + 8-K exhibit, grade 1).
