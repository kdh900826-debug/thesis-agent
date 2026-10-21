# -*- coding: utf-8 -*-
"""kc-eval — KC 임계 비교·stale 판정 (P11·P16, F7).
사용: python kc_eval.py --indicators <indicators.json> --out <01_macro_kc.json> [--include-company]
규칙: stale/웹검색/미수집 입력 → provisional 강제. stale 상태의 not_met 확정 금지.
duration 조건(2주 지속, 2분기 연속 등)은 자동 판정 불가 → needs_manual 표기.
"""
import argparse, json, sys
from datetime import datetime, date, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 필요 — pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[4]
OPS = {">": lambda a, b: a > b, ">=": lambda a, b: a >= b,
       "<": lambda a, b: a < b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b}


def trading_days_between(d0, d1):
    n, d = 0, d0
    while d < d1:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def age_of(as_of, unit, today):
    try:
        d = datetime.fromisoformat(str(as_of)).date()
    except (ValueError, TypeError):
        return None
    return trading_days_between(d, today) if unit == "trading_days" else (today - d).days


def eval_kc(kc_id, spec, indicators, limits, today):
    if spec.get("type") == "event":
        return {"kc_id": kc_id, "condition": spec.get("trigger"), "verdict": "not_met",
                "verdict_confidence": "provisional", "inputs": [],
                "note": "이벤트형 — 지표 피드가 아니라 L2 공시 관측으로 판정. 자동 확정 불가",
                "consequence": spec.get("consequence")}

    mode = "all_of" if "all_of" in spec else "any_of"
    conds = spec.get(mode, [])
    inputs, results, provisional, needs_manual = [], [], False, False

    for c in conds:
        m = c["metric"]
        ind = indicators.get(m)
        lim = limits.get(m)
        entry = {"name": m, "operator": c["operator"], "threshold": c["threshold"]}
        if ind is None:
            entry.update({"value": None, "status": "unconfirmed"})
            provisional = True
            results.append(None)
        else:
            entry["value"] = ind.get("value")
            entry["as_of"] = ind.get("as_of")
            entry["method"] = ind.get("method", "unknown")
            if lim:
                a = age_of(ind.get("as_of"), lim.get("unit", "calendar_days"), today)
                entry["stale_days"] = a
                entry["stale_limit"] = lim["limit"]
                if a is None or a > lim["limit"]:
                    provisional = True
            if entry["method"] == "web_search":
                provisional = True  # §5-2: 웹검색 수집 지표 근거 판정은 provisional 기본
            try:
                results.append(OPS[c["operator"]](ind["value"], c["threshold"]))
            except (TypeError, KeyError):
                results.append(None)
                provisional = True
        if c.get("duration"):
            entry["duration"] = c["duration"]
            needs_manual = True
            provisional = True
        inputs.append(entry)

    known = [r for r in results if r is not None]
    if not known:
        verdict = "not_met"
        provisional = True
    elif mode == "all_of":
        verdict = "met" if (len(known) == len(results) and all(known)) else "not_met"
        if len(known) < len(results):
            provisional = True
    else:
        verdict = "met" if any(known) else "not_met"
        if len(known) < len(results) and verdict == "not_met":
            provisional = True

    out = {"kc_id": kc_id, "condition": spec.get("description"), "inputs": inputs,
           "verdict": verdict, "verdict_confidence": "provisional" if provisional else "confirmed",
           "consequence": spec.get("consequence")}
    if needs_manual:
        out["note"] = "duration 조건 포함 — 지속성은 사람이 확인해야 confirmed 가능"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indicators", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--include-company", action="store_true")
    args = ap.parse_args()
    today = date.today()

    kc_cfg = yaml.safe_load((ROOT / "config" / "kill_conditions.yaml").read_text(encoding="utf-8-sig"))
    limits = yaml.safe_load((ROOT / "config" / "staleness.yaml").read_text(encoding="utf-8-sig")).get("limits", {})
    ind_path = Path(args.indicators)
    indicators = json.loads(ind_path.read_text(encoding="utf-8-sig")) if ind_path.exists() else {}

    statuses, skipped = [], []
    groups = ["macro"] + (["company"] if args.include_company else [])
    for g in groups:
        for kc_id, spec in (kc_cfg.get(g) or {}).items():
            if spec.get("status") == "draft":
                skipped.append(kc_id)
                continue
            if spec.get("status") != "active":
                continue
            statuses.append(eval_kc(kc_id, spec, indicators, limits, today))

    if statuses and all(not s["inputs"] or all(i.get("value") is None for i in s["inputs"])
                        for s in statuses if s.get("inputs")):
        print("⛔ 전 지표 미수집 — 에스컬레이션")
        sys.exit(1)

    result = {"as_of": datetime.now().isoformat(timespec="minutes"),
              "kc_status": statuses, "skipped_draft": skipped,
              "_note": "verdict_confidence=provisional은 stale/웹검색/미수집/duration 입력 포함을 의미. not_met은 확정이 아님(F7)."}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    met = [s["kc_id"] for s in statuses if s["verdict"] == "met"]
    print(f"KC {len(statuses)}건 판정 (draft 제외 {len(skipped)}건: {', '.join(skipped) if skipped else '-'})")
    if met:
        print(f"🔴🔴 MET: {', '.join(met)} — 자동 실행 금지, 사람 확인 요청 + 근거 패키지 제출로 종료")
    for s in statuses:
        print(f"  {s['kc_id']}: {s['verdict']} ({s['verdict_confidence']})")


if __name__ == "__main__":
    main()
