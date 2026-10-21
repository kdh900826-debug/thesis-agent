# ThesisPatch — CRWV / axes — axes[customer_concentration] — 신규 실명 고객(Cognition·MasterClass·Canva) 관측 주석, 정량 집중도 미갱신 / annotate

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `CRWV_axes_customer_concentration_new_names` · priority: low
- **대상 필드**: `axes` — axes[customer_concentration] — 신규 실명 고객(Cognition·MasterClass·Canva) 관측 주석, 정량 집중도 미갱신
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — CRWV 3건은 서로 다른 행(catalysts 53행 / axes 29행 / earnings_checkpoints 72행)을 치환하고 counts는 각자 필드만 검사한다. 권장: catalysts → axes → earnings_checkpoints
- **사전 확인(F20)**: `state/thesis_cards/CRWV.yaml` 전문 86행 열람, before 출현 1회 확인. 현재 계수 axes 7 / key_metrics 10 / catalysts 4 / risks 5 / kill_conditions_ref 4 / version_history 12 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "axes", "n": 7}] · contains 3건 · not_contains 1건

## diff

```diff
--- state/thesis_cards/CRWV.yaml (before)
+++ state/thesis_cards/CRWV.yaml (after 제안)
-  - {id: customer_concentration, label: "고객 집중 (OpenAI·Meta 등)"}
+  - {id: customer_concentration, label: "고객 집중 (OpenAI·Meta 등) [2026-10-01 관측 주석(annotate, run 20261001_0900) — 원문 보존(P9). [fact] 신규 실명 고객 3곳: Cognition(Vera Rubin NVL72 프로덕션 1호 고객, c_20261001_CRWV_2, grade 1), MasterClass·Canva(2026-09-30 출시 CoreWeave Forge 상에서 구축 중, c_20261001_CRWV_1, grade 1). 세 곳 모두 계약금액·매출 비중 미공시. [inference:moderate] 고객명 다변화의 정성 근거이나 상위 고객 매출 비중 수치가 갱신되지 않아 정량적 집중도 완화 여부는 판단 불가 — L2·arbiter 방향은 약한 강화(weak)로 제한됐다. [fact] CEO의 '주문 감소 없음' 키노트 발언 보도는 grade 4·confirmed=false(1차 원문 미확인)로 본 주석에 근거로 쓰지 않는다(P4). 다음 관측점 = Q3 2026 10-Q의 고객 집중 공시(상위 고객 매출·백로그 비중)]"}
```

## 왜

[fact] state/thesis_cards/CRWV.yaml 전문 86행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 7 / key_metrics 10 / catalysts 4 / risks 5 / kill_conditions_ref 4 / earnings_checkpoints.items 8 / version_history 12(F20). [fact] customer_concentration 축 라벨은 'OpenAI·Meta 등'만 기재하고 있으나 2026-09-30 자사 공시 2건에서 Cognition·MasterClass·Canva가 실명 공시됐다(c_20261001_CRWV_1·c_20261001_CRWV_2, grade1·confirmed). 고객명은 P3상 노이즈가 아닌 변화 범주다. [fact] 계약금액·매출 비중이 미공시라 정량 집중도 판단은 하지 않았다(03_signal·04_sector 모두 weak strengthen, substantive_dispersion low). [fact] 축 id·정의·축 수 불변의 관측 주석이므로 axis_naming_standardization 의존 플래그를 부착하지 않았다. 다만 04_sector neocloud는 NBIS–CRWV customer_concentration 공유 축의 극성 정의(다변화 vs 앵커 신용도) 대조를 su_11로 미결 기록했다 — 본 주석은 극성 판정을 포함하지 않는다.

**역전 판정 주석**: [fact] 관측 주석이며 thesis·conclusion을 수정하지 않는다.

## 근거 Claim

c_20261001_CRWV_1, c_20261001_CRWV_2

[fact] c_1·c_2: coreweave.com 뉴스룸·블로그(grade1·confirmed). c_3(CEO 발언 보도, grade4·confirmed=false)는 근거에서 제외.

출처: `output/20261001_0900/03_signal/CRWV.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/neocloud.json#axis_view · output/20261001_0900/03_input/arbiter_CRWV.json(수치·문구 대조)`

**F20 주석**: [fact] before는 29행 전체 원문이며 출현 1회 확인. contains 3번째는 인접 축(litigation) 행 무손상을 검증한다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
