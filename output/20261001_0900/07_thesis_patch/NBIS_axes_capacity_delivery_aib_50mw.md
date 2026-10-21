# ThesisPatch — NBIS / axes — axes[capacity_delivery] — AIB Data Centers 50MW·12년 바인딩 임차 계약 관측 주석(P7 1단) / annotate

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `NBIS_axes_capacity_delivery_aib_50mw` · priority: medium
- **대상 필드**: `axes` — axes[capacity_delivery] — AIB Data Centers 50MW·12년 바인딩 임차 계약 관측 주석(P7 1단)
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — NBIS 2건은 서로 다른 축 행(on_demand_pricing_power 27행 종결부 / capacity_delivery 24행)을 치환하며 counts(axes 8)는 둘 다 불변 검사다. 권장: on_demand → capacity_delivery
- **사전 확인(F20)**: `state/thesis_cards/NBIS.yaml` 전문 106행 열람, before 출현 1회 확인. 현재 계수 axes 8 / key_metrics 7 / catalysts 4 / risks 5 / kill_conditions_ref 4 / version_history 10 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "axes", "n": 8}] · contains 3건 · not_contains 1건

## diff

```diff
--- state/thesis_cards/NBIS.yaml (before)
+++ state/thesis_cards/NBIS.yaml (after 제안)
-  - {id: capacity_delivery, label: "계약 전력·용량 인도 (연말 5GW, late Q4 온라인 전환)"}
+  - {id: capacity_delivery, label: "계약 전력·용량 인도 (연말 5GW, late Q4 온라인 전환) [2026-10-01 관측 주석(annotate, run 20261001_0900) — 위 원문은 P9에 따라 보존. (1)[fact] 2026-09-30 AIB Data Centers(NYSE American: AIB) 보도자료(GlobeNewswire, grade 1): NBIS가 미국 남동부 AIB 시설의 50MW critical IT capacity를 최초 12년 바인딩 계약으로 임차(갱신 옵션). 해당 50MW는 AIB의 기존 65MW·15년 전력공급계약에 기반. 달러 금액·가동일 미공시(c_20261001_NBIS_1). (2)[fact] P7 3단 중 1단(계약 체결)만 확인 — 인도·온라인 전환·매출 인식은 미확인이며 연말 5GW 목표 대비 진척 수치로 환산하지 않는다. (3)[inference:moderate] 자사 건설(Vineland) 외 3자 호스팅 임차 경로가 추가돼 조달 경로가 다변화됐으나 AIB(3자 개발사) 인도 실행 리스크가 새로 생긴다(03_signal risk_transfer_to). catalysts의 '자산경량(asset-light) 파트너십 모델 진척' 해당 여부는 회사 정의 미확인으로 판정하지 않는다. 다음 관측점 = NBIS 6-K·AIB 10-Q 각주의 계약 금액·가동일, Q3 2026 실적자료의 계약 전력 합계]"}
```

## 왜

[fact] state/thesis_cards/NBIS.yaml 전문 106행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 8 / key_metrics 7 / catalysts 4 / risks 5 / kill_conditions_ref 4 / earnings_checkpoints.items 8 / version_history 10(F20). [fact] capacity_delivery 축은 '연말 5GW, late Q4 온라인 전환'만 기재하고 있고 2026-09-30 AIB 50MW·12년 바인딩 임차 계약(c_20261001_NBIS_1, grade1·confirmed)은 카드 어디에도 없다 — 신규 계약 용량이라는 고객·수주성 사실(P3상 노이즈 아님)이 관측 단위에 미기재 상태다. [fact] 금액·가동일 미공시이므로 P7 1단(계약 존재)으로만 기재했고 5GW 대비 진척률 등 수치 환산은 하지 않았다. [fact] 03_signal은 holding_reinforcement(상향 근거 아님)로 분류했다 — 본 패치는 등급과 무관(P13). [fact] 축 정의·축 수 불변의 관측 주석이므로 axis_naming_standardization 의존 플래그를 부착하지 않았다.

**역전 판정 주석**: [fact] 용량 확보 사실의 관측 기입이며 thesis·conclusion을 수정하지 않는다.

## 근거 Claim

c_20261001_NBIS_1

[fact] c_1: GlobeNewswire 보도자료(sources.yaml grade_1 등재 도메인), confirmed. 거래상대방(AIB) 발표이며 NBIS 자체 6-K는 창 내 미확인.

출처: `output/20261001_0900/03_signal/NBIS.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/neocloud.json#axis_view · output/20261001_0900/03_input/arbiter_NBIS.json(수치·문구 대조)`

**F20 주석**: [fact] before는 24행 전체 원문이며 출현 1회 확인. 축 id 유지, 라벨 끝에 주석을 덧붙인다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
