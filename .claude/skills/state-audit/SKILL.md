---
name: state-audit
description: 모든 Run 시작 시 자동 실행. 승인 대기 건 보고, 산출물 존재·신선도 감사, config 스키마 검증, RunPlan 생성. run·approve·publish 등 어떤 명령이든 시작 전에 반드시 이 스킬을 먼저 수행한다.
---

# state-audit — 상태 감사 (S0, 필수 선행)

## 실행

```bash
python .claude/skills/state-audit/scripts/state_audit.py --command "<사용자 명령>" --run-id <YYYYMMDD_HHmm>
```

## 처리 순서 [CODE]

1. **승인 큐 보고 (최우선, D6):** `state/pending_approvals.json` 스캔 — pending 건 목록·경과일 출력, 14일 초과 건은 `expired`로 전환 기록
2. **config 로드 검증:** `config/*.yaml` 7종 스키마 검사. **임계 없는 `status: active` KC 발견 시 로드 실패 = 에스컬레이션(P11).** `status: draft` KC·벡터는 로드 제외 + 경고 목록 출력
3. **staleness 계산 (P16/D9):** 명령의 필수 입력별로 최신 산출물 `as_of` 대조. `unit: trading_days` 지표는 주말 제외 계산
4. **RunPlan 생성:** 부재 산출물 → 선행 단계 큐 삽입 / stale → 사용자 확인 항목으로 표기 / 재사용 → `reused_from` 기록

## 산출

`output/{run_id}/00_state_audit.json` — 승인 대기, RunPlan, 재사용 산출물 목록, staleness 표, draft 경고.

## 실패 처리

config 스키마 오류 → **에스컬레이션 (실행 중단)**. stale 산출물 → 사용자에게 [재실행 / 캐시 사용(provisional)] 확인 후 진행.
