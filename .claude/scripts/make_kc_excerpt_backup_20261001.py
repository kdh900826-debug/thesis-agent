# -*- coding: utf-8 -*-
"""P17 KC 발췌본 생성 — signal-arbiter 호출 전 오케스트레이터가 실행.

signal-arbiter는 `01_macro_kc.json` 전문을 읽을 수 없다(P17: 서사부 접근 금지).
대신 오케스트레이터가 종목별로 "그 종목에 불리 방향으로 파급되는 KC"만 발췌해 전달한다.
파급 판정은 correlation_map.py와 동일한 KC_AXIS·노출 벡터 규약을 따른다 — 두 곳의 규약이
갈라지지 않도록 KC_AXIS를 correlation_map.py에서 직접 import 한다(단일 출처).

2026-09-19 신설: 종전에는 매 run 수기 생성이라 재현성·일관성이 보장되지 않았다.
사용: python .claude/scripts/make_kc_excerpt.py --run-id <id>
"""
import argparse, importlib.util, json, sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 필요 — pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]


def load_kc_axis():
    p = ROOT / ".claude" / "skills" / "correlation-map" / "scripts" / "correlation_map.py"
    spec = importlib.util.spec_from_file_location("correlation_map", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.KC_AXIS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()

    run_dir = ROOT / "output" / args.run_id
    macro = json.loads((run_dir / "01_macro_kc.json").read_text(encoding="utf-8-sig"))
    kc_by_id = {s["kc_id"]: s for s in macro["kc_status"]}
    kc_cfg = yaml.safe_load((ROOT / "config" / "kill_conditions.yaml").read_text(encoding="utf-8-sig"))
    cm = yaml.safe_load((ROOT / "config" / "correlation_matrix.yaml").read_text(encoding="utf-8-sig"))
    exposures = cm["exposures"]
    KC_AXIS = load_kc_axis()

    company_kc = kc_cfg.get("company") or {}
    dst_dir = run_dir / "03_kc_excerpt"
    dst_dir.mkdir(parents=True, exist_ok=True)

    for t in sorted(exposures):
        propagating, undefined = [], []
        for kc_id in kc_by_id:
            axes = KC_AXIS.get(kc_id)
            if axes is None:
                undefined.append(kc_id)
                continue
            if any(ax in exposures[t] and exposures[t][ax]["sign"] == adverse
                   for ax, adverse in axes):
                propagating.append(kc_id)
        own = {k: v for k, v in company_kc.items()
               if v.get("status") == "active" and v.get("ticker") == t}
        out = {
            "_note": ("오케스트레이터가 생성한 KC 발췌본(P17). signal-arbiter는 이 파일과 "
                      "03_input/arbiter_{T}.json, state/signals.json 외에는 읽지 않는다. "
                      "매크로 KC는 correlation_matrix.yaml 노출 벡터상 해당 종목이 불리 방향으로 "
                      "노출된 축에 연결된 것만 발췌했다. 발췌 제외는 '해당 종목과 무관'이 아니라 "
                      "'불리 방향 노출 축 없음'을 뜻한다(P5)."),
            "generated_by": ".claude/scripts/make_kc_excerpt.py",
            "run_id": args.run_id,
            "as_of": datetime.now().isoformat(timespec="minutes"),
            "ticker": t,
            "own_company_kc": (sorted(own) if own
                               else "kill_conditions.yaml#company에 해당 종목 전용 active KC 미정의"),
            "own_company_kc_detail": {k: {"description": v.get("description"),
                                          "type": v.get("type", "metric"),
                                          "consequence": v.get("consequence")} for k, v in own.items()} or None,
            "macro_kc_propagating_to_ticker": propagating,
            "macro_kc_axis_mapping_undefined": undefined or None,
            "kc_status": [kc_by_id[k] for k in propagating],
        }
        (dst_dir / f"{t}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        flag = " ⚠️MET포함" if any(kc_by_id[k]["verdict"] == "met" for k in propagating) else ""
        print(f"✅ {t}: 파급 매크로 KC {len(propagating)}건 {propagating} / 전용 KC {len(own)}건{flag}")


if __name__ == "__main__":
    main()
