# -*- coding: utf-8 -*-
"""EDGAR 공시 수집 (D15 [CODE] 경로). SEC data API — User-Agent 필수, 키 불필요.
사용: python edgar_fulltext.py --ticker IREN --forms 8-K 10-Q "SCHEDULE 13G" --since 2026-08-01 --out <raw_items.json>
--forms는 정확 일치(와일드카드 불가). 서식은 coverage.yaml edgar_forms 기준 — 발행사 지위 변경 주의.
"""
import argparse, json, sys
from pathlib import Path

# Windows cp949 콘솔에서 한글·특수문자 print가 UnicodeEncodeError로 성공 실행을 exit 1로 만드는 것 방지
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print("ERROR: requests 필요 — pip install requests")
    sys.exit(2)

UA = {"User-Agent": "thesis-agent research koramai26@koramcofund.co.kr"}


def ticker_to_cik(ticker):
    r = requests.get("https://www.sec.gov/files/company_tickers.json", headers=UA, timeout=30)
    r.raise_for_status()
    for e in r.json().values():
        if e["ticker"].upper() == ticker.upper():
            return str(e["cik_str"]).zfill(10)
    return None


def recent_filings(cik, forms, since):
    r = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=UA, timeout=30)
    r.raise_for_status()
    rec = r.json()["filings"]["recent"]
    items = []
    for i in range(len(rec["form"])):
        form, fdate = rec["form"][i], rec["filingDate"][i]
        if forms and form not in forms:
            continue
        if since and fdate < since:
            continue
        acc = rec["accessionNumber"][i].replace("-", "")
        doc = rec["primaryDocument"][i]
        items.append({
            "id": f"edgar_{fdate}_{form}_{i}",
            "form": form, "filed_at": fdate,
            "title": rec.get("primaryDocDescription", [""] * len(rec["form"]))[i] or f"{form} filing",
            "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}",
            "domain": "sec.gov", "evidence_grade": 1, "method": "api",
        })
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--forms", nargs="*", default=[])
    ap.add_argument("--since", default=None, help="YYYY-MM-DD")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cik = ticker_to_cik(args.ticker)
    if cik is None:
        print(f"[WARN] {args.ticker}: CIK 미발견 — EDGAR 미등록 또는 티커 불일치. unconfirmed 적재(P5)")
        Path(args.out).write_text(json.dumps({"ticker": args.ticker, "items": [],
                                              "note": "CIK 미발견 — 부재는 반증이 아님"}, ensure_ascii=False, indent=2), encoding="utf-8")
        sys.exit(0)
    items = recent_filings(cik, set(args.forms), args.since)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"ticker": args.ticker, "cik": cik, "items": items},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    # cp949 콘솔에서 이모지 출력이 UnicodeEncodeError로 성공 실행을 exit 1로 만들므로 ASCII 유지
    print(f"[OK] {args.ticker} (CIK {cik}): {len(items)}건 -> {args.out}")
    print("   (뉴스·규제 재료는 웹검색[LLM] 경로로 보완 — sources.yaml 등급 매핑 + 1차 URL 역추적 의무)")


if __name__ == "__main__":
    main()
