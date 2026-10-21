---
name: consensus-aggregate
description: L3 섹터 에이전트 실행 시 사용. 섹터 내 종목들의 Delta를 공통 축별로 집계해 방향 일치도와 분산을 계산한다.
---

# consensus-aggregate — 축별 방향·분산 집계 (S4)

## 실행

```bash
python .claude/skills/consensus-aggregate/scripts/consensus_aggregate.py --sector <S> --run-id <id>
```

## 처리 [CODE]

1. 섹터 내 각 종목의 `DeltaSet`에서 coverage.yaml의 `common_axes` 관련 Delta 추출
2. 축별 방향 집계: strengthen/weaken/neutral 지지 **종목 수** → `direction` (일치 시 그 방향, 갈리면 `diverge`). 같은 종목이 한 축에 낸 복수 Delta는 1표로 dedup
3. `dispersion`: low(전원 일치) / medium(1개 이탈) / high(방향 상충) — 커버 종목 2개 이상일 때만 계산
4. 축 커버 종목이 1개면 `dispersion: single_ticker`(비교 대상 부재 — low와 구분). 그 한 종목 안에서 방향이 갈리면 `direction: intra_ticker`(종목 간 diverge와 구분)
5. **종목 1건(MU) → 분산 계산 스킵 + 로그, 단일 종목 뷰로 표기**

## LLM 해석 단계 (스크립트 출력을 받아 에이전트가 수행)

- 일치/분산의 **의미** 해석: 섹터 요인 지배 vs 개별 실행 요인 지배
- 섹터 수준 미확인 항목(`sector_unconfirmed`) 정리

## 금지 (P13)

- 개별 종목 시그널 등급을 변경하는 필드 생성 금지 — `signal_mutation`은 항상 null
- 섹터 컨센서스를 개별 종목 상향 근거로 서술하는 문장 금지 (F13)
