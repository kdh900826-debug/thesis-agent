# ThesisPatch — IREN / catalysts[1] — Horizons 2-4 인도 목표 2027-01(최대 2월 말)로 이동

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_catalysts1_h2_4_target_jan2027` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- catalysts (before)
-  - "Horizons 2-4 인도 — 역년 Q4 2026 단계 인도 목표, 계약상 유예 2026 Q4 중반~2027 Q2 초"
+++ catalysts (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: Horizons 2-4 인도 — 역년 Q4 2026 단계 인도 목표, 계약상 유예 2026 Q4 중반~2027 Q2 초
+  - "Horizons 2-4 인도 — 회사 목표가 역년 Q4 2026에서 2027-01(공급 상황에 따라 2월 말)로 이동(2026-11-05 보도자료·10-Q; 사유: 고객 요청 설계 변경·공급업체 일정·제3자 지연). 계약상 유예 상한 2027 Q2 초(10-K)는 유지. Microsoft 요청 변경분 지연은 지연 크레딧 없이 인도일 연장, 인도일·수수료·크레딧·비용 상환 협의는 미종결(10-Q)"
```

## 왜

[fact] 11/5 보도자료와 10-Q는 $4B+ ARR 목표의 가동 시점을 2026년 말에서 2027-01-31로 옮기고 2월 말까지 늘어날 수 있다고 기재했다(IREN-2611-C09·C10). [fact] 경영진은 비공식 전사에서 Microsoft의 네트워크 재구성 요청을 원인으로 설명했다(IREN-2611-C11, grade 2, 공식 웹캐스트 대조 미실시). [inference] 새 목표는 계약상 유예 상한(2027 Q2 초) 안에 있다(IREN-2611-I04).

## 근거 Claim

IREN-2611-C09, IREN-2611-C10, IREN-2611-C11, IREN-2611-I04

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).