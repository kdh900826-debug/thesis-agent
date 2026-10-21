# -*- coding: utf-8 -*-
"""correlation-map — 축 공유도·KC 파급·축 집중도 (§6, P14·D1·D13).
사용: python correlation_map.py --run-id <id> --out <05_correlation.json>
matrix가 status: draft면 실행 중단(U4). 수치 상관계수를 절대 출력하지 않는다 — 등급(상/중/하)만.
"""
import argparse, itertools, json, sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 필요 — pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[4]
STRENGTH = {"H": 3, "M": 2, "L": 1}
PAIR_SCORE = {(3, 3): 3, (3, 2): 2, (2, 3): 2, (2, 2): 1, (3, 1): 1, (1, 3): 1}  # 그 외 = 0
# KC → (관련 축, 피해 노출 부호). 예: KC-1은 금리 상승 이벤트 → RATES "-" 노출 종목이 피해.
# KC-3은 BTC 하락 이벤트 → CRYPTO "+" 노출 종목이 피해 (VIX 레그는 KC-2가 별도 커버).
KC_AXIS = {"KC-1": [("RATES", "-")], "KC-2": [("RISK_APPETITE", "+")], "KC-3": [("CRYPTO", "+")],
           "KC-4": [("RISK_APPETITE", "+")], "KC-5": [("RISK_APPETITE", "+")],
           "KC-6": [("AI_CAPEX", "+")], "KC-7": [("AI_CAPEX", "+")],
           "KC-8": [("AI_CAPEX", "+")], "KC-10": [("POWER_PERMIT", "-")]}
DISCLAIMER = ("본 상관은 구조적 노출 판정이며 실제 가격 동조화를 예측하지 않는다. "
              "축 노출이 낮아도 유동성 이벤트에서 동반 하락할 수 있다. "
              "노출 벡터는 사람이 편집한 correlation_matrix.yaml에 의존하므로, "
              "벡터의 정확성이 곧 이 레이어의 정확성 상한이다.")


def grade(score):
    return "상" if score >= 5 else ("중" if score >= 2 else "하")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cm = yaml.safe_load((ROOT / "config" / "correlation_matrix.yaml").read_text(encoding="utf-8-sig"))
    if cm.get("status") == "draft":
        print("⛔ correlation_matrix.yaml이 draft 상태 — 노출 벡터 확정(U4) 후 status: active로 변경하세요. 실행 중단")
        sys.exit(1)
    pos_cfg = yaml.safe_load((ROOT / "config" / "positions.yaml").read_text(encoding="utf-8-sig"))
    exposures = cm["exposures"]
    tickers = sorted(exposures.keys())

    def upper(t):
        wr = (pos_cfg.get("positions", {}).get(t) or {}).get("weight_range")
        return wr[1] if wr else None

    # 쌍별 축 공유도 + 역방향 노출
    pair_overlap = []
    for a, b in itertools.combinations(tickers, 2):
        score, shared, inverse = 0, [], []
        for axis in set(exposures[a]) & set(exposures[b]):
            ea, eb = exposures[a][axis], exposures[b][axis]
            sa, sb = STRENGTH[ea["strength"]], STRENGTH[eb["strength"]]
            if ea["sign"] == eb["sign"]:
                s = PAIR_SCORE.get((sa, sb), 0)
                score += s
                if s > 0:
                    shared.append(axis)
            else:
                inverse.append({"axis": axis, "hedge_strength": grade(min(sa, sb) * 2),
                                "note": f"{a} {ea['sign']} vs {b} {eb['sign']} — 자연 헤지"})
        entry = {"pair": [a, b], "grade": grade(score), "shared_axes": shared}
        if inverse:
            entry["inverse_axes"] = inverse
        pair_overlap.append(entry)

    # KC 파급 — 피해 방향의 노출만 집계
    kc_prop = []
    for kc, axes in KC_AXIS.items():
        affected = [t for t in tickers
                    if any(ax in exposures[t] and exposures[t][ax]["sign"] == adverse_sign
                           for ax, adverse_sign in axes)]
        ws = [upper(t) for t in affected]
        known = [w for w in ws if w is not None]
        kc_prop.append({"kc_id": kc, "affected": affected, "count": len(affected),
                        "weight_pct_upper": round(sum(known) * 100, 1) if known else None})

    # 축 집중도 (범위 상단 기준 보수 판정, D13)
    threshold = cm.get("concentration_threshold_pct", 60)
    axis_conc = []
    for axis in cm.get("axes", {}):
        ts = [t for t in tickers if axis in exposures[t]]
        ws = [upper(t) for t in ts]
        known = [w for w in ws if w is not None]
        wsum = round(sum(known) * 100, 1) if known else None
        axis_conc.append({"axis": axis, "tickers": ts, "count": len(ts),
                          "weight_pct_upper": wsum,
                          "threshold_breach": (wsum >= threshold) if wsum is not None else None,
                          "basis": "positions.yaml 비중 범위 상단" if wsum is not None else "비중 미기입 — 종목 수 기준 상대 판정만"})

    out = {"as_of": datetime.now().isoformat(timespec="minutes"), "run_id": args.run_id,
           "pair_overlap": pair_overlap, "kc_propagation": kc_prop,
           "axis_concentration": axis_conc,
           "vector_change_proposals": [],  # [LLM] 단계에서 에이전트가 근거 Claim ID와 함께 제안만 추가
           "coefficient_used": False, "disclaimer": DISCLAIMER}
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {len(pair_overlap)}쌍 공유도 + KC 파급 {len(kc_prop)}건 + 축 집중도 {len(axis_conc)}건 → {args.out}")


if __name__ == "__main__":
    main()
