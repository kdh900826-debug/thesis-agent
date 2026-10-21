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
           "KC-8": [("AI_CAPEX", "+")],
           # 2026-09-12 사용자 확정(갈래 A, 제안서 output/20260911_2308/08_proposal/ENERGY_axis_proposal.md).
           # KC-9는 브렌트 원유(FRED DCOILBRENTEU)를 재는 '거시 인플레 KC'로 확정하고 RATES에 매핑한다.
           # ENERGY 축은 신설하지 않았다 — 브렌트의 지배적 전달 경로가 유가→CPI→정책금리이고 그 경로를
           # RATES가 이미 포착하므로, 별도 축 신설은 KC-1과 같은 위험을 두 번 계상하게 된다.
           # 주의: 따라서 KC-1과 KC-9는 같은 축을 공유하며 파급 종목 집합이 겹친다. 이는 은폐된 이중
           # 계상이 아니라 의도된 공유이며, 아래 shared_axis_kc_groups에 명시적으로 드러낸다.
           # 금리를 경유하지 않는 직접 전력비 경로는 별도 KC(전력·가스 레그)가 정의될 때 재검토한다.
           "KC-9": [("RATES", "-")],
           "KC-10": [("POWER_PERMIT", "-")]}
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

    # KC 파급 — 피해 방향의 노출만 집계.
    # 2026-09-12 수정(무음 누락 제거): 이전 구현은 하드코딩된 KC_AXIS의 키를 순회했기 때문에,
    # kill_conditions.yaml에 active로 올라와 있어도 KC_AXIS에 매핑이 없는 KC는 산출물에서 경고 없이
    # 사라졌다(run 20260911_2308에서 매크로 KC-9 1건 + 종목 KC 17건 전부가 이렇게 유실됐고, 산출된
    # 파급은 9건뿐이었다). 이제 kill_conditions.yaml의 active KC 전수를 순회하고, 매핑이 없으면
    # 버리지 않고 mapping_status="undefined" 행으로 남긴다 — 부재를 값으로 표현해 보이게 한다(P5).
    kc_cfg = yaml.safe_load((ROOT / "config" / "kill_conditions.yaml").read_text(encoding="utf-8-sig"))

    def active_kcs(group):
        return [(k, s) for k, s in (kc_cfg.get(group) or {}).items() if s.get("status") == "active"]

    kc_prop, gaps = [], []
    for group in ("macro", "company"):
        for kc, spec in active_kcs(group):
            axes = KC_AXIS.get(kc)
            if axes is None:
                row = {"kc_id": kc, "group": group, "affected": None, "count": None,
                       "weight_pct_upper": None, "mapping_status": "undefined",
                       "note": ("KC_AXIS에 축 매핑이 정의되지 않아 파급을 산출할 수 없다. "
                                "이 부재는 '파급 없음'을 뜻하지 않는다(P5).")}
                if spec.get("ticker"):
                    row["ticker"] = spec["ticker"]
                kc_prop.append(row)
                gaps.append(kc)
                continue
            affected = [t for t in tickers
                        if any(ax in exposures[t] and exposures[t][ax]["sign"] == adverse_sign
                               for ax, adverse_sign in axes)]
            ws = [upper(t) for t in affected]
            known = [w for w in ws if w is not None]
            kc_prop.append({"kc_id": kc, "group": group, "affected": affected, "count": len(affected),
                            "weight_pct_upper": round(sum(known) * 100, 1) if known else None,
                            "mapping_status": "defined",
                            "mapped_axes": [{"axis": ax, "adverse_sign": sg} for ax, sg in axes]})

    # 같은 축을 공유하는 KC 묶음 — 파급 집합이 겹치는 것이 의도된 공유임을 드러낸다(이중 계상 가시화)
    axis_to_kcs = {}
    for kc, axes in KC_AXIS.items():
        for ax, _ in axes:
            axis_to_kcs.setdefault(ax, []).append(kc)
    shared_axis_kc_groups = [
        {"axis": ax, "kc_ids": sorted(ks),
         "note": ("동일 축을 공유하는 KC들이다 — 각각의 파급 종목 집합이 겹치는 것은 정상이며, "
                  "서로 다른 위험이 중복 계상된 것이 아니라 같은 전달 경로를 공유한다는 뜻이다. "
                  "축 집중도 합산 시 이 중복을 두 번 세지 않도록 주의한다.")}
        for ax, ks in sorted(axis_to_kcs.items()) if len(ks) > 1]

    kc_propagation_coverage = {
        "active_total": sum(len(active_kcs(g)) for g in ("macro", "company")),
        "macro_active": len(active_kcs("macro")), "company_active": len(active_kcs("company")),
        "mapped": sum(1 for r in kc_prop if r.get("mapping_status") == "defined"),
        "undefined": len(gaps), "undefined_kc_ids": gaps,
        "note": ("undefined는 축 매핑 미정의로 파급 산출이 불가능한 KC다. 값이 비어 있는 것이 아니라 "
                 "'산출 불가'라는 정보이며, 파급이 없다는 뜻이 아니다(P5). 매핑 추가는 사람 승인 영역이다."),
    }

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
           "kc_propagation_coverage": kc_propagation_coverage,
           "shared_axis_kc_groups": shared_axis_kc_groups,
           "axis_concentration": axis_conc,
           "vector_change_proposals": [],  # [LLM] 단계에서 에이전트가 근거 Claim ID와 함께 제안만 추가
           "coefficient_used": False, "disclaimer": DISCLAIMER}
    p = Path(args.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {len(pair_overlap)}쌍 공유도 + KC 파급 {len(kc_prop)}건 + 축 집중도 {len(axis_conc)}건 → {args.out}")
    cov = kc_propagation_coverage
    print(f"   KC 매핑 커버리지: active {cov['active_total']}건 중 산출 {cov['mapped']}건 / "
          f"매핑 미정의 {cov['undefined']}건")
    if gaps:
        print(f"   ⚠️ 축 매핑 미정의로 파급 산출 불가: {', '.join(gaps)}")
        print("      (부재는 '파급 없음'이 아니다 — 매핑 추가는 사람 승인 영역, P5·CLAUDE.md §9)")


if __name__ == "__main__":
    main()
