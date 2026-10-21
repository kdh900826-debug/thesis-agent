# ThesisPatch — CRWV / axes / annotate

- **Run**: 20260919_2209 · as_of 2026-09-19 (`thesis-refine` S7/C7, `refine thesis CRWV`)
- **patch_id**: `tp_20260919_2209_CRWV_axes_margin_basis` · **priority**: high
- **대상 필드**: `axes[id=margin_trend]` (expected_after.counts: axes=7 — F20)
- **operation**: `annotate` — 기존 서술 삭제 없이 주석 병기만 한다(P9)
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **사전 확인**: 대상 카드 **전문 75행** 열람 후 before 원문 일치·목록 항목 수(axes 7 · key_metrics 10) 확인 완료 (F20 — 부분 읽기 기반 '부재' 판정 없음)
- **동반 패치(동일 회차)**: `output/20260919_2209/07_thesis_patch/CRWV_key_metrics_coverage_basis.md` — key_metrics / 이자 커버리지 산식 병기(medium)

## diff

```diff
--- state/thesis_cards/CRWV.yaml (before)
+++ state/thesis_cards/CRWV.yaml (after 제안)
-  - {id: margin_trend,      label: "Adj. EBITDA 마진 추세 — ⚠️기준 기간 명시 필요. YoY 기준: Q2 59%(전년 62%)·H1 57%(전년 62%)로 압축 / 시퀀셜 기준: Q1 약 56%→Q2 59%로 개선. 기준에 따라 방향이 반대이므로 축 판정 시 기준을 먼저 고정한다 ⚠️갱신"}
+  # 2026-09-19 ThesisPatch(annotate, run 20260919_2209) — 이전 라벨 원문 보존(P9): - {id: margin_trend,      label: "Adj. EBITDA 마진 추세 — ⚠️기준 기간 명시 필요. YoY 기준: Q2 59%(전년 62%)·H1 57%(전년 62%)로 압축 / 시퀀셜 기준: Q1 약 56%→Q2 59%로 개선. 기준에 따라 방향이 반대이므로 축 판정 시 기준을 먼저 고정한다 ⚠️갱신"} / 기준 채택은 사람 결정이므로 에이전트는 두 기준의 1차 실측치만 병기한다. axes 7개 불변(전문 기준 계수, F20).
+  - {id: margin_trend,      label: "Adj. EBITDA 마진 추세 — ⚠️기준 기간 명시 필요. YoY 기준: Q2 59%(전년 62%)·H1 57%(전년 62%)로 압축 / 시퀀셜 기준: Q1 약 56%→Q2 59%로 개선. 기준에 따라 방향이 반대이므로 축 판정 시 기준을 먼저 고정한다 ⚠️갱신 [⚠️ 2026-09-19 기준 병기 주석(run 20260919_2209) — 2026-09-17 8-K Ex 99.2 34p가 5분기 Adj. EBITDA 조정표를 1차 공시해(c_20260919_CRWV_5, grade 1 fact, confirmed) 두 기준의 실측치가 모두 확정됐다. 분기 마진 실측: Q2'25 62% → Q3'25 61% → Q4'25 57% → Q1'26 56% → Q2'26 59%. (가) YoY 기준(Q2'26 59% 대 Q2'25 62%) = -3%p, 부호 압축. (나) 시퀀셜 기준(Q1'26 56% → Q2'26 59%) = +3%p, 부호 개선(Q1'26이 5분기 저점). 동일한 1차 수치에서 두 부호가 병존하므로, 어느 기준을 축 판정 기준으로 채택할지가 곧 방향 부호의 결정이다. 이는 측정 정의의 선택이지 관측의 판정이 아니므로 에이전트는 어느 편도 채택하지 않는다 — 기준 확정은 사람 결정 대기(CLAUDE.md §9, P2/P15). 참고 선행 단가지표(c_20260919_CRWV_11, grade 1 fact): 2026-07 SKU 전반 약 70% 가격 인상, Q2 체결계약 기대 contribution margin이 최근 분기 대비 약 25% 높음, Q3 단기계약 약 $40M/MW(+5~10%p). 단 회사 예시곡선은 다수 배치 동시 램프 시 aggregate contribution margin이 단기 25%→5%로 압축된 뒤 'mid 20%s' 안정화를 제시한 예시치이며 실적이 아니다. 기준 확정 시 (가)/(나) 중 하나를 축 판정 기준으로 고정하고 나머지는 참고치로 남긴다. 본 주석은 기존 라벨 서술을 삭제하지 않고 병기만 한다(P9)]"}
```

## 왜

[fact] state/thesis_cards/CRWV.yaml 전문 75행을 읽고 확인한 결과 margin_trend 축 라벨은 이미 '기준에 따라 방향이 반대이므로 축 판정 시 기준을 먼저 고정한다'고 요구하고 있으나, 고정할 기준 자체는 카드에 확정돼 있지 않다. [fact] 2026-09-17 8-K Ex 99.2 34p가 5분기 Adj. EBITDA 조정표(마진 62%·61%·57%·56%·59%)를 1차 공시해 두 기준의 실측치가 모두 확정됐다(c_20260919_CRWV_5, grade 1, confirmed). YoY 기준 Q2'26 59% 대 Q2'25 62% = -3%p(압축), 시퀀셜 기준 Q1'26 56% → Q2'26 59% = +3%p(개선)로 동일 1차 수치에서 부호가 갈린다. [fact] 선행 단가지표도 개선 방향이 관측된다 — 2026-07 SKU 전반 약 70% 가격 인상, Q2 체결계약 기대 contribution margin 최근 분기 대비 약 25% 높음, Q3 단기계약 약 $40M/MW(+5~10%p)(c_20260919_CRWV_11, grade 1). 다만 같은 자료의 회사 예시곡선(단기 25%→5% 압축 후 'mid 20%s' 안정화)은 예시치이지 실적이 아니므로 방향 판정 근거로 쓰지 않았다. [fact] 기준 선택은 방향 부호를 직접 결정하는 측정 정의의 선택이며 관측의 판정이 아니다 — 따라서 어느 한 기준을 채택하는 amend를 생성하지 않고, 두 기준과 각각의 부호를 병기한 뒤 '기준 확정은 사람 결정 대기'임을 카드에 명시하는 annotate로 처리했다(CLAUDE.md §9, P2/P15). [fact] 기존 라벨 서술은 한 글자도 삭제하지 않고 주석 블록만 덧붙였으며, 이전 라벨 원문은 YAML 주석으로 별도 보존했다(P9). [fact] axes는 전문 기준 7개(backlog_scale·funding_access·leverage_coverage·margin_trend·gpu_priority·customer_concentration·litigation)이며 본 패치로 변하지 않는다(F20).

**역전 판정 주석**: [fact] thesis 본문('네오클라우드 스케일 1위 / 백로그를 레버리지로 건설하고 매출로 상환')과 시그널 등급에 대한 판정을 포함하지 않는다. [fact] 축의 방향 부호를 확정하지 않고 두 측정 기준을 병기할 뿐이므로 논거 전복에 해당하지 않는다. 등급·행동 판정은 하지 않는다(P2/P15).

**사람 결정 경계**: [fact] 본 패치는 두 기준(산식)의 1차 실측치를 병기할 뿐 어느 쪽도 채택하지 않는다 — 채택은 측정 정의·KC 임계 확정 영역으로 사람의 권한이다(CLAUDE.md §9, P11, P2/P15). 등급·행동·목표치는 제안하지 않았다.

## 근거 Claim

c_20260919_CRWV_5, c_20260919_CRWV_11

출처: `output/20260919_2209/02_company/CRWV.json#claims[c_20260919_CRWV_5,c_20260919_CRWV_11] · output/20260919_2209/03_signal/CRWV.json#thesis_delta_summary[margin_trend]`

## 적용 후 자동 대조(expected_after.contains)

- `2026-09-19 기준 병기 주석(run 20260919_2209)`
- `(가) YoY 기준(Q2'26 59% 대 Q2'25 62%) = -3%p, 부호 압축`
- `(나) 시퀀셜 기준(Q1'26 56% → Q2'26 59%) = +3%p, 부호 개선`
- `기준 확정은 사람 결정 대기`

**F20 주석**: [fact] state/thesis_cards/CRWV.yaml 전문 75행을 읽은 뒤 before 문자열의 원문 일치를 확인하고 axes 7개·key_metrics 10개를 전체 파일 기준으로 계수했다 — 부분 읽기 기반의 '부재·누락' 판정을 하지 않았다(F20). [fact] 본 패치는 목록형 필드(axes)의 항목 문자열을 수정하므로 expected_after.counts를 포함했다(항목 수 불변 7).

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복). 승인 큐 등재는 오케스트레이터가 수행하며 본 스킬은 `state/thesis_cards/CRWV.yaml`·`state/pending_approvals.json`을 수정하지 않았다.
