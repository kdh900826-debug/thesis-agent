# ThesisPatch — IREN / risks[7]·key_metrics[1] — 가동 ARR 갭 기한 2027-01-31, 이연수익 $2,544M 갱신 (편집 2/2: key_metrics)

- **Run**: 20261106_1346 · as_of 2026-11-06 · `run earnings IREN`(S2E) · 근거 산출물 `output/20261106_1346/02_company/IREN.json`
- **patch_id**: `IREN_risks7_keymetrics1_arr_gap_deadline_b` · priority: high · 편집 1건
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인(F20)**: 카드 전문 142행 열람, before 출현 각 1회. 현재 계수 axes 6 / key_metrics 8 / catalysts 4 / risks 8 / earnings_checkpoints.items 14 — 적용 후에도 불변
- **적용 순서**: 단독(다른 high 패치와 대상 행 비중복)

## diff

```diff
--- key_metrics (before)
-  - "ARR 실행 갭 — $4.0B 전액 계약 완료(미계약 갭 해소). 신규 갭 = 가동 중 $1.0B(8/26 기준) 대 계약 $4.0B, 미가동 ~$3.0B의 2026-12-31 기한 가동 여부. ARR은 비GAAP이며 회사가 '인식 매출은 실질적으로 더 낮을 수 있다'고 명시"
+++ key_metrics (after 제안)
+  # 2026-11-06 ThesisPatch(amend, run 20261106_1346) — 이전: ARR 실행 갭 — $4.0B 전액 계약 완료(미계약 갭 해소). 신규 갭 = 가동 중 $1.0B(8/26 기준) 대 계약 $4.0B, 미가동 ~$3.0B의 2026-12-31 기한 가동 여부. ARR은 비GAAP이며 회사가 '인식 매출은 실질적으로 더 낮을 수 있다'고 명시
+  - "ARR 실행 갭 — $4.0B+ 전액 계약·자금 확보(11/5 회사 표현 fully contracted·fully funded, 확약 금융의 인출 조건 충족 전제 — 각주 5). 갭 = 가동 중 $1.0B(11/5 발표, 기준일 미기재) 대 계약 $4.0B+, 미가동 ~$3.0B의 2027-01-31(최대 2월 말; 종전 2026-12-31) 가동 여부. ARR은 비GAAP이며 회사가 '인식 매출은 실질적으로 더 낮을 수 있다'고 명시"
```

## 왜

[fact] 가동 ARR 기한이 2027-01-31로 바뀌었고(IREN-2611-C09), 보도자료의 가동 ARR $1bn에는 기준일이 없다(IREN-2611-C08). [fact] 9/30 이연수익은 $2,544M이다(IREN-2611-C19). 두 필드가 같은 기한을 담고 있어 한 패치로 묶었다(목록 2개 편집 — 각 편집마다 F20 검증).

## 근거 Claim

IREN-2611-C08, IREN-2611-C09

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 이전 문구는 after 안 주석으로 보존된다(P9).