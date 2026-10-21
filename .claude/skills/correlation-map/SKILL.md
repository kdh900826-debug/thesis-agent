---
name: correlation-map
description: L4 실행 시 또는 correlation_matrix.yaml 변경 시 사용. 축 공유도(상/중/하)·KC 파급·축 집중도를 산출한다. 수치형 상관계수는 절대 산출하지 않는다.
---

# correlation-map — 구조적 상관 매핑 (§6, P14, D1)

## 실행

```bash
python .claude/skills/correlation-map/scripts/correlation_map.py --run-id <id> --out output/{run_id}/05_correlation.json
```

## 처리 [CODE]

- `correlation_matrix.yaml`이 `status: draft`면 **실행 중단** + 사용자에게 벡터 확정 요청(U4)
- 쌍별 축 공유도: 같은 축·같은 부호 노출을 `H+H=3, H+M=2, M+M/H+L=1`로 합산 → 상(≥5)/중(2~4)/하(≤1) 3구간 (**수치 미출력, 등급만**)
- 역방향 노출: 같은 축 반대 부호 → 자연 헤지 (축명 + 상/중/하)
- KC 파급 시뮬: KC 1건 트리거 시 영향 종목 목록·수·합산 비중(positions.yaml 범위 상단)
  - **순회 대상은 `kill_conditions.yaml`의 `status: active` KC 전수**(매크로 + 종목)다. 스크립트 내부 `KC_AXIS` 딕셔너리의 키가 아니다.
  - 축 매핑이 없는 KC는 **버리지 않는다** — `mapping_status: "undefined"` + `affected: null` 행으로 남기고, 콘솔에 ⚠️ 경고와 KC ID 목록을 출력한다. **부재는 '파급 없음'이 아니다**(P5).
  - `kc_propagation_coverage`에 active 총건수·산출 건수·미정의 건수·미정의 KC ID를 집계한다. 새 KC를 `kill_conditions.yaml`에 추가하고 `KC_AXIS` 매핑을 빠뜨리면 이 값으로 즉시 드러난다.
  - 유래: 2026-09-12 수정. 이전 구현은 `KC_AXIS.items()`를 순회해 매핑 없는 KC가 **경고 없이 사라졌다** — run 20260911_2308에서 매크로 KC-9 1건 + 종목 KC 17건이 유실되고 파급이 9건만 산출됐다.
- `shared_axis_kc_groups`: 같은 축을 공유하는 KC 묶음. 파급 종목 집합이 겹치는 것이 **의도된 공유**임을 드러내 은폐된 이중 계상을 방지한다. 축 집중도 합산 시 이 중복을 두 번 세지 않는다.
  - 현재 묶음: `RATES ← KC-1·KC-9` / `AI_CAPEX ← KC-6·KC-7·KC-8` / `RISK_APPETITE ← KC-2·KC-4·KC-5`
- 축 집중도: 축별 비중(범위 상단) 합, `concentration_threshold_pct` 초과 여부. 비중 미기입 시 종목 수 기준 상대 판정 + 그 사실 명기

## KC-9 매핑 결정 (2026-09-12 사용자 확정 — 갈래 A)

- **KC-9(에너지 쇼크)는 `RATES(-)`에 매핑한다.** 근거: KC-9의 수집 지표는 브렌트 **원유**(FRED `DCOILBRENTEU`)이고, 이 지표가 포트폴리오에 닿는 지배적 경로는 원가가 아니라 거시(`유가↑ → CPI 에너지↑ → 정책금리↑`)다. 그 경로는 RATES 축이 이미 포착한다.
- **ENERGY 축은 신설하지 않았다.** 신설 시 KC-1과 같은 위험을 두 축에서 두 번 계상하게 되며, 7종목 전부 부호 확정 근거가 없어 벡터에 넣을 수 없다(P4·P5).
- 금리를 경유하지 않는 **직접 전력비 경로**(도매 전력가·천연가스 연계)는 전용 KC가 정의될 때 재검토한다. 제안서: `output/20260911_2308/08_proposal/ENERGY_axis_proposal.md`
- v1 원본 스크립트는 `scripts/correlation_map_v1_backup.py`에 보존(P9).

## LLM 판단 단계

- 이번 Run의 신규 Claim이 기존 노출 벡터를 바꾸는지 판단 → `vector_change_proposals`에 **제안만** (자동 반영 금지, 근거 Claim ID 첨부)

## 고정 문구 (산출물 말미 필수, §6-4)

> 본 상관은 구조적 노출 판정이며 실제 가격 동조화를 예측하지 않는다. 축 노출이 낮아도 유동성 이벤트에서 동반 하락할 수 있다. 노출 벡터는 사람이 편집한 correlation_matrix.yaml에 의존하므로, 벡터의 정확성이 곧 이 레이어의 정확성 상한이다.
