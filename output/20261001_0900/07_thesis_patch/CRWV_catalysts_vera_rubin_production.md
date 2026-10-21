# ThesisPatch — CRWV / catalysts — catalysts[2] 'Vera Rubin 최초 배포 일정' — Cognition 프로덕션 가동(2026-09-30)으로 이벤트 도래 주석, 매출 인식 미확인 / annotate

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `CRWV_catalysts_vera_rubin_production` · priority: medium
- **대상 필드**: `catalysts` — catalysts[2] 'Vera Rubin 최초 배포 일정' — Cognition 프로덕션 가동(2026-09-30)으로 이벤트 도래 주석, 매출 인식 미확인
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — CRWV 3건은 서로 다른 행(catalysts 53행 / axes 29행 / earnings_checkpoints 72행)을 치환하고 counts는 각자 필드만 검사한다. 권장: catalysts → axes → earnings_checkpoints
- **사전 확인(F20)**: `state/thesis_cards/CRWV.yaml` 전문 86행 열람, before 출현 1회 확인. 현재 계수 axes 7 / key_metrics 10 / catalysts 4 / risks 5 / kill_conditions_ref 4 / version_history 12 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "catalysts", "n": 4}] · contains 3건 · not_contains 1건

## diff

```diff
--- state/thesis_cards/CRWV.yaml (before)
+++ state/thesis_cards/CRWV.yaml (after 제안)
-  - "Vera Rubin 최초 배포 일정"
+  - "Vera Rubin 최초 배포 일정 [2026-10-01 관측 주석(annotate, run 20261001_0900) — 원문 보존(P9). [fact] 촉매 이벤트 도래: 2026-09-16 멀티랙 Vera Rubin NVL72 가동(bring-up) 공지(직전 run)에 이어, 2026-09-30 자사 블로그가 Cognition을 Vera Rubin NVL72에서 프로덕션 워크로드(트레이닝·강화학습·추론)를 운영하는 최초 고객으로 공시했다 — 수개월 내 수천 GPU 규모로 확장(c_20261001_CRWV_2, grade 1). [fact] P7 — 배포·실사용(이행) 단계까지 확인, 계약금액·과금 개시는 미공시로 매출 인식 단계는 미확인. 성능 수치(GB200 대비 처리량 4.8배 등)는 회사 제시치이며 매출·마진 수치가 아니다(P2). [inference:moderate] '최초 배포 일정'이라는 촉매의 일정 요소는 충족된 것으로 보나, 이 촉매가 thesis(GPU 공급 최우선권)에 주는 효과의 정량 확인은 Q3 2026 실적자료의 Vera Rubin 매출·고객 수 언급으로 이월한다]"
```

## 왜

[fact] state/thesis_cards/CRWV.yaml 전문 86행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 7 / key_metrics 10 / catalysts 4 / risks 5 / kill_conditions_ref 4 / earnings_checkpoints.items 8 / version_history 12(F20). [fact] catalysts의 'Vera Rubin 최초 배포 일정'은 미래 이벤트로만 기재돼 있으나 2026-09-30 CoreWeave 자체 공시로 Cognition이 Vera Rubin NVL72에서 프로덕션 워크로드를 운영 중임이 확인됐다(c_20261001_CRWV_2, grade1·confirmed) — 카드 상태가 사실과 어긋났다. [fact] 지시 쟁점 '카드 catalyst 충족 여부' 판정: 배포(가동)·실사용 단계까지는 1차 확인되나 계약금액·과금 미공시로 P7 3단 중 매출 인식은 미확인 — '일정 충족, 효과 미확인'으로 분리 기재했다(충족 판정 자체는 inference 태그). [fact] 03_signal은 gpu_priority 축 strengthen(strong)으로 기록했으나 상향 게이트 근거로 쓰지 않았다 — 본 패치는 등급과 무관(P13). 원문은 보존(P9).

**역전 판정 주석**: [fact] 촉매 상태 기입이며 thesis·conclusion을 수정하지 않는다. 방향은 thesis(GPU 공급 최우선권)와 정합.

## 근거 Claim

c_20261001_CRWV_2

[fact] c_2: coreweave.com 자사 블로그(grade1·confirmed). 2026-09-16 가동 공지는 c_2 원문이 직전 run 사실로 참조한 것이며 별도 Claim으로 인용하지 않았다.

출처: `output/20261001_0900/03_signal/CRWV.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/neocloud.json#axis_view · output/20261001_0900/03_input/arbiter_CRWV.json(수치·문구 대조)`

**F20 주석**: [fact] before는 53행 전체 원문이며 출현 1회 확인. not_contains는 원 단독 항목+개행으로, 덧붙임 적용 후 사라짐을 검증한다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
