# ThesisPatch — NBIS / risks / amend

- **Run**: 20260905_0618 · 2026-09-05T06:18 (L4 병행 `thesis-refine`)
- **대상 필드**: `risks` (expected_after.counts: risks=5 — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: 대상 카드 전문 열람 후 before 문자열의 카드 원문 일치 확인 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음)

## diff

```diff
--- state/thesis_cards/NBIS.yaml (before)
+++ state/thesis_cards/NBIS.yaml (after 제안)
@@ -1 +1,2 @@
-  - "CapEx $20-25B vs 현금 $8B → 추가 조달·ATM 희석"
+  # 2026-09-05 ThesisPatch(amend, run 20260905_0618) — 이전: "CapEx $20-25B vs 현금 $8B → 추가 조달·ATM 희석" (조달을 미래 가능성 단계로 서술, P9 주석 보존). 만료된 ap_20260820_2235_thesis_patch_nbis_risks_funding_realized의 재생성이며 2026-08-24 결제 완료를 반영해 단계 표기를 '예정'에서 '완료'로 갱신한다. 항목 수 5개 불변.
+  - "CapEx $20-25B 대비 조달 집행 완료 단계 — ATM $2.8B(12.7M주) 기집행, 전환사채 누적 원금 $10,041.8M(6/30) + 2026-08-24 신규 발행 $5.75B 클로징 완료(그린슈 전액 행사, 2030년물 0.50% $3.45B·2034년물 4.50% $2.3B) + 기존 2029·2031년물 $800M의 Class A 약 15.8M주 지분교환(계약 체결 확인, 주식 인도 완료 시점 unconfirmed). 추가 조달·희석은 '가능성'이 아니라 '실행 완료'이며 만기 구조는 단기(2029/2031)→장기(2030/2034)로 이관. 잔여 ATM 12.3M주 사용 여부는 1차 자료 미확인"
```

## 왜

[fact] 카드 risks는 '추가 조달·ATM 희석'을 미래 가능성으로 서술하나, 조달은 이미 대규모로 집행됐고 2026-08-24 클로징으로 결제까지 완료됐다(c_20260905_NBIS_01, grade 1). [fact] 직전 패치가 '결제 8/24 예정'으로 P7 3단 분리에 따라 유보했던 부분이 이번 run에서 '이행 완료'로 단계 전환됐다. [fact] 그린슈는 전액 행사돼 발행 규모가 $5.0B → $5.75B로 오히려 확대됐다. [fact] $800M 지분교환은 계약 체결까지만 확인되고 주식 인도 완료는 미확인이므로 unconfirmed 표기를 유지한다(P7·c_20260905_NBIS_02). [inference:strong] 리스크의 존재가 아니라 리스크의 단계(가능성 → 실행 완료) 표기가 낡았다 — 단계 갱신이 정합적 조치다. [fact] 항목 수는 전문 기준 5개로 불변(F20).

**역전 판정 주석**: [fact] 리스크 항목의 단계 표기 갱신이며 thesis 본문 판정과 무관하다. '저희석 확장' 문장 판정은 esc_20260905_0618_nbis_thesis_rewrite로 분리.

**후속 주의**: [fact] KC-NBIS-3(조달 조건 악화)와의 관계: 그린슈 전액 행사·업사이즈 성공은 KC 발동 방향이 아니다 — funding_access strengthen(이번 run Delta)과 정합한다. [fact] 잔여 ATM 12.3M주 사용 여부가 1차 자료로 확인되면 본 항목의 마지막 문장이 갱신 대상이 된다.

## 근거 Claim

c_20260905_NBIS_01, c_20260905_NBIS_02, c_20260905_NBIS_03, c_20260820_NBIS_02, c_20260820_NBIS_07, c_20260820_NBIS_08, c_20260820_NBIS_11

출처: `output/20260905_0618/02_company/NBIS.json#claims[c_20260905_NBIS_01/02] · #deltas[leverage_burden]`

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
