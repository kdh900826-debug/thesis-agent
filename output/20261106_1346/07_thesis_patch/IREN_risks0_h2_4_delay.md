# ThesisPatch — IREN / risks[0] — Horizons 2-4 인도 리스크 갱신(목표 2027-01, 크레딧 협의 미종결)

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_risks0_h2_4_delay` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- risks (before)
-  - "Horizons 2-4 인도 리스크 — H1(50MW IT)은 2026년 8월 Microsoft 인도·인수 완료로 해소. 잔여 H2-4는 역년 Q4 2026 단계 인도 목표이나 Microsoft 계약상 인도 유예기간이 2026년 4분기 중반~2027년 2분기 초까지 확장됨이 10-K로 최초 확인 — 리스크 이관 유지, 후행 노출 기간 명시적 연장"
+++ risks (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: Horizons 2-4 인도 리스크 — H1(50MW IT)은 2026년 8월 Microsoft 인도·인수 완료로 해소. 잔여 H2-4는 역년 Q4 2026 단계 인도 목표이나 Microsoft 계약상 인도 유예기간이 2026년 4분기 중반~2027년 2분기 초까지 확장됨이 10-K로 최초 확인 — 리스크 이관 유지, 후행 노출 기간 명시적 연장
+  - "Horizons 2-4 인도 리스크 — H1(50MW IT)은 2026년 8월 Microsoft 인도·인수 후 리스 매출 인식 개시(FY27 Q1, 단독 금액 미분리). 잔여 H2-4 목표가 역년 Q4 2026에서 2027-01(최대 2월 말)로 이동(10-Q: 고객 요청 설계 변경·공급·제3자 지연, 달성 보장 없음). Microsoft 요청 변경분 지연은 크레딧 없이 인도일 연장되나 수수료·크레딧·비용 상환 협의 미종결. 계약상 인도 유예 상한 2027 Q2 초(10-K) — 리스크 이관 유지, 후행 노출 시점 2027 Q1로 이동"
```

## 왜

[fact] 10-Q는 H2-4 목표 이동과 사유, Microsoft 요청 변경분의 크레딧 없는 인도일 연장, 수수료·크레딧·비용 상환 협의 진행을 기재했다(IREN-2611-C10). [inference] 리스크는 소멸이 아니라 시점 이동이다(IREN-2611-I03·I04).

## 근거 Claim

IREN-2611-C10, IREN-2611-C11, IREN-2611-I03, IREN-2611-I04

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).