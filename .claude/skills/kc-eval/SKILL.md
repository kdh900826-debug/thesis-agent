---
name: kc-eval
description: L1 macro-kc 실행 시 또는 종목 KC 판정이 필요할 때 사용. 지표를 수집(무료 API 우선)하고 kill_conditions.yaml의 임계와 비교해 KCStatus를 산출한다. stale 입력은 예외 없이 provisional.
---

# kc-eval — KC 임계 비교·stale 판정 (P11·P16, D5·D9)

## 실행

```bash
# 1) 지표 수집 (무료 API — FRED 키는 환경변수 FRED_API_KEY)
python .claude/skills/kc-eval/scripts/fred_fetch.py --out output/{run_id}/indicators.json
python .claude/skills/kc-eval/scripts/market_fetch.py --out output/{run_id}/indicators.json  # BTC·VIX·브렌트 병합

# 2) 판정
python .claude/skills/kc-eval/scripts/kc_eval.py --indicators output/{run_id}/indicators.json --out output/{run_id}/01_macro_kc.json
```

## API 부재 지표 (설계서 §5-2)

FFR 확률(CME FedWatch)·SDLLMTK·글로벌 자금흐름은 API가 없다 → **에이전트가 웹검색으로 수집하되 수치·출처·발표 시각만 추출**(기사 논평·전망 인용 금지, D3), `indicators.json`에 `{value, as_of, source_url, method: "web_search"}` 형식으로 추가한 뒤 kc_eval.py를 실행한다. `method: web_search` 지표에 근거한 판정은 **provisional 기본**.

## 판정 규칙

- `status: draft` KC는 로드하지 않고 경고 목록에만 출력. 임계 없는 `active` KC = 로드 실패(P11)
- stale 입력(staleness.yaml, 거래일/달력일 이원화) → `verdict_confidence: provisional` 강제. **stale 상태의 `not_met` 확정 금지(F7)**
- 지표 미수집 → 해당 KC `provisional` + `unconfirmed` 적재 후 계속. **전 지표 미수집 → 에스컬레이션**
- `type: event` KC(KC-10, KC-CRCL-3 등)는 지표 피드가 아니라 L2 Claim에서 관측 — kc_eval.py는 상태 유지만 기록

## 출력: `KCStatus[]` — `{kc_id, condition, inputs[{name,value,as_of,stale_days,method}], verdict, verdict_confidence, consequence}`
