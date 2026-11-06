# ThesisPatch — IREN / catalysts[3] — 가동 ARR 진척 기한 2027-01-31로 갱신, Dell GPU 주문 병기

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_catalysts3_arr_deadline_jan2027` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- catalysts (before)
-  - "가동 ARR $1.0B → $4.0B 진척 (회사 제시 기한 2026-12-31) / 차세대 GPU 배정 — VR200은 6/30 기준 설치·발주 포트폴리오에 편입 확인"
+++ catalysts (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: 가동 ARR $1.0B → $4.0B 진척 (회사 제시 기한 2026-12-31) / 차세대 GPU 배정 — VR200은 6/30 기준 설치·발주 포트폴리오에 편입 확인
+  - "가동 ARR $1.0B → $4.0B+ 진척 (회사 제시 기한 2027-01-31, 2월 말 연장 가능 — 11/5 보도자료 각주 4; 종전 2026-12-31) / 차세대 GPU 배정 — VR200은 6/30 기준 설치·발주 포트폴리오에 편입 확인, Dell 약 $6.7B GPU 주문(2026-09-28 체결, 인도 2027 역년 하반기 시작) 10-Q 확인"
```

## 왜

[fact] 가동 ARR $4B+ 목표 기한이 2027-01-31(2월 말 연장 가능)로 바뀌었다(IREN-2611-C09). [fact] 10-Q에 Dell 약 $6.7B GPU 주문이 기재됐다(IREN-2611-C16).

## 근거 Claim

IREN-2611-C09, IREN-2611-C16

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).