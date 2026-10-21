# -*- coding: utf-8 -*-
"""D7 사전 필터 — signal-arbiter 호출 전 오케스트레이터가 실행 (P6·P13, F11·F13).
02_company/{T}.json에서 scope==company_specific Claim만 남긴 필터본을 03_input/에 생성한다.
arbiter 프롬프트에는 이 필터본 경로만 전달하고, 원문 경로는 노출하지 않는다.
사용: python filter_arbiter_input.py --run-id <id> --ticker <T>
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--ticker", required=True)
    args = ap.parse_args()
    t = args.ticker.upper()

    src = ROOT / "output" / args.run_id / "02_company" / f"{t}.json"
    if not src.exists():
        print(f"ERROR: {src} 부재 — L2 선행 실행 필요")
        sys.exit(1)
    data = json.loads(src.read_text(encoding="utf-8-sig"))

    claims = data.get("claims", [])
    kept = [c for c in claims if c.get("scope") == "company_specific"]
    removed = [{"id": c.get("id"), "scope": c.get("scope")} for c in claims if c.get("scope") != "company_specific"]
    kept_ids = {c.get("id") for c in kept}

    deltas = []
    for d in data.get("deltas", []):
        sup = [cid for cid in d.get("supporting_claims", []) if cid in kept_ids]
        if sup:  # company_specific 근거가 하나라도 남는 Delta만 통과
            deltas.append({**d, "supporting_claims": sup})

    out = {
        "as_of": data.get("as_of"),
        "ticker": t,
        "filtered_by": "filter_arbiter_input.py (P6/P13 — scope!=company_specific 물리적 제거)",
        "removed_claims": removed,
        "claims": kept,
        "deltas": deltas,
        "unconfirmed": data.get("unconfirmed", []),
    }
    dst = ROOT / "output" / args.run_id / "03_input" / f"arbiter_{t}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 필터본 생성: {dst.relative_to(ROOT)} (유지 {len(kept)} / 제거 {len(removed)} claims)")


if __name__ == "__main__":
    main()
