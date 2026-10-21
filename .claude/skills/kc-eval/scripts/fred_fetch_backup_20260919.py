# -*- coding: utf-8 -*-
"""FRED 지표 수집 (D5) — 30Y(DGS30), ON RRP(RRPONTSYD), 브렌트(DCOILBRENTEU).
환경변수 FRED_API_KEY 필요 (무료 발급: https://fred.stlouisfed.org/docs/api/api_key.html).
사용: python fred_fetch.py --out <indicators.json>  (기존 파일에 병합)
"""
import argparse, json, os, sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests 필요 — pip install requests")
    sys.exit(2)

SERIES = {"yield_30y": "DGS30", "ON_RRP": "RRPONTSYD", "brent": "DCOILBRENTEU"}
UNIT_SCALE = {"ON_RRP": 1e9}  # RRPONTSYD 단위: 십억 달러 → USD 절대값으로 환산


def fetch(series_id, api_key):
    r = requests.get(
        "https://api.stlouisfed.org/fred/series/observations",
        params={"series_id": series_id, "api_key": api_key, "file_type": "json",
                "sort_order": "desc", "limit": 10},
        timeout=30,
    )
    r.raise_for_status()
    for obs in r.json().get("observations", []):
        if obs.get("value") not in (".", "", None):
            return float(obs["value"]), obs["date"]
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    key = os.environ.get("FRED_API_KEY")
    out = Path(args.out)
    data = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}

    if not key:
        print("⚠️ FRED_API_KEY 미설정 — FRED 지표는 웹검색 fallback으로 강등 (provisional). (§5-2)")
        sys.exit(0)  # 실패가 아니라 강등 — kc-eval이 미수집 지표를 provisional 처리

    for name, sid in SERIES.items():
        try:
            v, d = fetch(sid, key)
            if v is None:
                print(f"⚠️ {name}({sid}): 유효 관측치 없음 → unconfirmed")
                continue
            v = v * UNIT_SCALE.get(name, 1)
            data[name] = {"value": v, "as_of": d, "source_url": f"https://fred.stlouisfed.org/series/{sid}", "method": "api"}
            print(f"✅ {name} = {v} (as_of {d})")
        except Exception as e:
            print(f"⚠️ {name} 수집 실패: {e} → unconfirmed (P5 — 부재는 반증이 아님)")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
