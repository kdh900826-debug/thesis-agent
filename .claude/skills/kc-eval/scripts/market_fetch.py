# -*- coding: utf-8 -*-
"""시장 지표 수집 (D5) — BTC(Coinbase 공개 API, 키 불필요), VIX·브렌트 보조(yfinance 설치 시).
사용: python market_fetch.py --out <indicators.json>  (기존 파일에 병합)
"""
import argparse, json, sys
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests 필요 — pip install requests")
    sys.exit(2)


def fetch_btc(data):
    try:
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=30)
        r.raise_for_status()
        v = float(r.json()["data"]["amount"])
        data["BTC"] = {"value": v, "as_of": date.today().isoformat(),
                       "source_url": "https://api.coinbase.com/v2/prices/BTC-USD/spot", "method": "api"}
        print(f"✅ BTC = {v}")
    except Exception as e:
        print(f"⚠️ BTC 수집 실패: {e} → 웹검색 fallback (provisional)")


def fetch_yf(data, name, symbol):
    try:
        import yfinance as yf
    except ImportError:
        print(f"⚠️ yfinance 미설치 — {name}은 FRED(브렌트) 또는 웹검색 fallback (provisional)")
        return
    try:
        h = yf.Ticker(symbol).history(period="5d")
        if h.empty:
            raise ValueError("빈 응답")
        v = float(h["Close"].iloc[-1])
        d = h.index[-1].date().isoformat()
        data[name] = {"value": v, "as_of": d, "source_url": f"yfinance:{symbol}", "method": "api"}
        print(f"✅ {name} = {v} (as_of {d})")
    except Exception as e:
        print(f"⚠️ {name} 수집 실패: {e} → 웹검색 fallback (provisional)")


def fetch_taiex(data):
    """KC-5: TAIEX 종가 vs 20일 이동평균(%), 1개월 수익률(%)."""
    try:
        import yfinance as yf
    except ImportError:
        print("⚠️ yfinance 미설치 — TAIEX(KC-5)는 웹검색 fallback (provisional)")
        return
    try:
        h = yf.Ticker("^TWII").history(period="3mo")
        if len(h) < 21:
            raise ValueError("이력 부족")
        close = h["Close"]
        last, dma20 = float(close.iloc[-1]), float(close.tail(20).mean())
        m_ago = float(close.iloc[-22]) if len(close) >= 22 else float(close.iloc[0])
        d = h.index[-1].date().isoformat()
        data["TAIEX_vs_20dma_pct"] = {"value": round((last / dma20 - 1) * 100, 2), "as_of": d,
                                      "source_url": "yfinance:^TWII", "method": "api"}
        data["TAIEX_1m_return_pct"] = {"value": round((last / m_ago - 1) * 100, 2), "as_of": d,
                                       "source_url": "yfinance:^TWII", "method": "api"}
        print(f"✅ TAIEX vs 20dma = {data['TAIEX_vs_20dma_pct']['value']}% / 1m = {data['TAIEX_1m_return_pct']['value']}% (as_of {d})")
    except Exception as e:
        print(f"⚠️ TAIEX 수집 실패: {e} → 웹검색 fallback (provisional)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    data = json.loads(out.read_text(encoding="utf-8-sig")) if out.exists() else {}

    fetch_btc(data)
    fetch_yf(data, "VIX", "^VIX")
    fetch_taiex(data)
    if "brent" not in data:  # FRED 우선, 없으면 선물
        fetch_yf(data, "brent", "BZ=F")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("(FFR 확률·SDLLMTK·글로벌 자금흐름은 API 부재 — 에이전트가 웹검색으로 수치·출처·시각만 추가: method=web_search)")


if __name__ == "__main__":
    main()
