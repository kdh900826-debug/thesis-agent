# ThesisPatch — IREN / risks[7]·key_metrics[1] — 가동 ARR 갭 기한 2027-01-31, 이연수익 $2,544M 갱신 (편집 1/2: risks)

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_risks7_keymetrics1_arr_gap_deadline_a` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- risks (before)
-  - "가동 ARR 갭 — 계약 ARR $4.0B 대 가동 중 ARR $1.0B(8/26 기준)의 ~$3.0B 차이를 2026-12-31까지 가동해야 하며, 그 기한이 Horizons 2-4 인도 기한과 동일 구간에 집중. 이연수익 잔액 $1,842.6M은 인도 실패 시 반환·서비스 크레딧 의무의 원천이 될 수 있음(계약 조건 원문 미공시)"
+++ risks (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: 가동 ARR 갭 — 계약 ARR $4.0B 대 가동 중 ARR $1.0B(8/26 기준)의 ~$3.0B 차이를 2026-12-31까지 가동해야 하며, 그 기한이 Horizons 2-4 인도 기한과 동일 구간에 집중. 이연수익 잔액 $1,842.6M은 인도 실패 시 반환·서비스 크레딧 의무의 원천이 될 수 있음(계약 조건 원문 미공시)
+  - "가동 ARR 갭 — 계약 ARR $4.0B+ 대 가동 중 ARR $1.0B(11/5 보도자료, 기준일 미기재 — 8/26 값과 같은 크기라 순증 미확인)의 ~$3.0B 차이를 2027-01-31(최대 2월 말; 종전 2026-12-31)까지 가동해야 하며, 그 기한이 Horizons 2-4 인도 목표와 같은 구간에 집중. 이연수익 잔액 $2,544M(리스 이연수익 $2,096M 포함, 9/30; 6/30 $1,842.6M)은 인도 실패 시 반환·서비스 크레딧 의무의 원천이 될 수 있음(계약 조건 원문 미공시)"
```

## 왜

[fact] 가동 ARR 기한이 2027-01-31로 바뀌었고(IREN-2611-C09), 보도자료의 가동 ARR $1bn에는 기준일이 없다(IREN-2611-C08). [fact] 9/30 이연수익은 $2,544M이다(IREN-2611-C19). 두 필드가 같은 기한을 담고 있어 한 패치로 묶었다(목록 2개 편집 — 각 편집마다 F20 검증).

## 근거 Claim

IREN-2611-C08, IREN-2611-C09, IREN-2611-C19, IREN-2611-I05

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).