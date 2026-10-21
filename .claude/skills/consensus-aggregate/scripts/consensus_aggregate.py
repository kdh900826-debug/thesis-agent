# -*- coding: utf-8 -*-
"""consensus-aggregate — 섹터 내 축별 방향·분산 집계 (S4, P13).
사용: python consensus_aggregate.py --sector <neocloud|memory|stablecoin> --run-id <id>
출력: output/{run_id}/04_sector/{sector}_aggregate.json — [LLM] 해석 전의 결정론 집계.
signal_mutation은 항상 null로 고정한다 — 개별 등급 변경 불가.
"""
import argparse, json, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 필요 — pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[4]

# ── 방향 라벨 정규화 (2026-09-19 추가, AD-5 수정)
# 유래: L2 에이전트가 delta.direction을 한국어("강화"/"약화"/"혼재")로 쓰는 경우가 있어
# 고정 키 dict 인덱싱이 KeyError로 죽었다(run 20260905_0618에서 neocloud 집계 중단 → 수기 대체).
# 정책: 별칭을 정규 라벨로 접고, 정규화 불가 라벨은 버리지 않고 별도 버킷에 담아 경고로 보고한다(P5·P9).
CANON = ("strengthen", "weaken", "neutral", "break", "mixed")
DIRECTION_ALIASES = {
    "강화": "strengthen", "개선": "strengthen", "상향": "strengthen",
    "positive": "strengthen", "strengthened": "strengthen", "strengthening": "strengthen",
    "약화": "weaken", "악화": "weaken", "하향": "weaken",
    "negative": "weaken", "weakened": "weaken", "weakening": "weaken",
    "중립": "neutral", "유지": "neutral", "무변화": "neutral", "unchanged": "neutral", "flat": "neutral",
    "훼손": "break", "붕괴": "break", "broken": "break", "invalidate": "break", "invalidated": "break",
    "혼재": "mixed", "상충": "mixed", "혼조": "mixed", "conflicting": "mixed", "mixed_signal": "mixed",
}


def normalize_direction(raw):
    """(정규 라벨, 원본, 정규화 성공 여부) — 실패해도 예외를 던지지 않는다."""
    if raw is None:
        return "neutral", None, True
    key = str(raw).strip()
    low = key.lower()
    if low in CANON:
        return low, key, True
    if key in DIRECTION_ALIASES:
        return DIRECTION_ALIASES[key], key, True
    if low in DIRECTION_ALIASES:
        return DIRECTION_ALIASES[low], key, True
    return "unnormalized", key, False



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sector", required=True)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()

    cov = yaml.safe_load((ROOT / "config" / "coverage.yaml").read_text(encoding="utf-8-sig"))
    sector = cov["sectors"].get(args.sector)
    if not sector:
        print(f"⛔ 알 수 없는 섹터: {args.sector}")
        sys.exit(1)
    members = sector["members"]

    run_dir = ROOT / "output" / args.run_id
    by_axis = defaultdict(lambda: {k: [] for k in CANON})
    deltas_used, missing, label_warnings = [], [], []
    for t in members:
        f = run_dir / "02_company" / f"{t}.json"
        if not f.exists():
            missing.append(t)
            continue
        data = json.loads(f.read_text(encoding="utf-8-sig"))
        for d in data.get("deltas", []):
            canon, raw, ok = normalize_direction(d.get("direction"))
            if not ok:
                label_warnings.append({"ticker": t, "axis": d.get("axis"), "raw_direction": raw})
            bucket = by_axis[d["axis"]].setdefault(canon, [])
            if t not in bucket:  # 지지 집계는 종목 단위 — 같은 종목의 복수 Delta는 1표
                bucket.append(t)
            deltas_used.append(d.get("id", d["axis"]))

    single = len(members) - len(missing) <= 1
    axis_view, single_axes = [], []
    for axis, dirs in by_axis.items():
        active = {k: v for k, v in dirs.items() if v}
        tickers = {t for v in active.values() for t in v}
        intra = sorted(t for t in tickers if sum(t in v for v in active.values()) >= 2)
        if len(tickers) <= 1:
            # 커버 종목 1개 — '전원 일치(low)'가 아니라 비교 대상 부재. 방향이 갈리면
            # 종목 간 diverge가 아닌 해당 종목 내부의 하위 사안 간 부호 차이다.
            direction = next(iter(active)) if len(active) == 1 else "intra_ticker"
            dispersion = "single_ticker"
            single_axes.append(axis)
        elif len(active) == 1:
            direction, dispersion = next(iter(active)), "low"
        else:
            direction = "diverge"
            counts = sorted((len(v) for v in active.values()), reverse=True)
            dispersion = "high" if len(counts) > 2 or counts[0] == counts[1] else "medium"
        axis_view.append({"axis": axis, "direction": direction,
                          "supporters": {k: v for k, v in dirs.items()},
                          "dispersion": dispersion,
                          "coverage_tickers": sorted(tickers),
                          "coverage_count": len(tickers),
                          "intra_ticker_dispersion": intra,
                          "interpretation": None})  # [LLM] 단계에서 에이전트가 채움

    out = {"sector": args.sector, "as_of": datetime.now().isoformat(timespec="minutes"),
           "run_id": args.run_id, "members": members, "missing_inputs": missing,
           "single_ticker_view": single,
           "axis_view": axis_view, "sector_unconfirmed": [],
           "signal_mutation": None,  # P13 고정
           "direction_label_warnings": label_warnings,
           "_note": ("단일 종목 뷰 — 분산 계산 스킵(설계서 S4)" if single else None)}
    dst = run_dir / "04_sector" / f"{args.sector}_aggregate.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    if label_warnings:
        print(f"⚠️ 정규화 실패 방향 라벨 {len(label_warnings)}건 — unnormalized 버킷 보존, 사람 확인 필요:")
        for w in label_warnings:
            print(f"   - {w['ticker']} / {w['axis']} / raw={w['raw_direction']!r}")
    if single_axes:
        print(f"ℹ️ 단일 종목 커버 축 {len(single_axes)}개 — 분산 계산 스킵(single_ticker): {', '.join(single_axes)}")
    print(f"✅ 집계 완료 → {dst.relative_to(ROOT)} (축 {len(axis_view)}개, 누락 입력: {missing or '없음'})")


if __name__ == "__main__":
    main()
