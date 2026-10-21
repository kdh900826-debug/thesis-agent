# -*- coding: utf-8 -*-
"""주간 이벤트 페이지(공개용 정적 HTML) — 쉬운 말 이벤트 원장 + run 산출물 자동 항목을 주 단위로 묶는다.

사용:
  python weekly_events_render.py [--out output/weekly_events.html] [--today YYYY-MM-DD]
  python weekly_events_render.py --pending        # 원장에 아직 정리되지 않은 신규 Claim 목록 → output/weekly_events_pending.json
  python weekly_events_render.py --check-only     # 개인정보 검사만 (파일 미기록)

입력(읽기만): state/weekly_events.json(쉬운 말 원장) · state/signals.json(등급·전이) ·
             output/<run>/03_signal/{T}.json(점검 결과·상향 게이트) · output/<run>/02_company/{T}.json(--pending 전용) ·
             config/correlation_matrix.yaml(노출 부호·강도)
자동 생성 항목: 시스템 점검(run별 등급 후보) · 등급 확정(signals.json transitions) · 현재 등급 카드 · 상향 게이트 · 노출 매트릭스.
공개 전제: config/positions.yaml은 읽지 않는다. 보유 비중·보유 여부·평단·개인 가격선 같은 문구가 결과물에 있으면
         파일을 쓰지 않고 종료 코드 2로 멈춘다(privacy_hits). 판정은 새로 만들지 않는다 — 산출물 원문의 등급·게이트를 옮길 뿐이다.
"""
import argparse, html, json, re, sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
STORE = ROOT / "state" / "weekly_events.json"
RUN_RE = re.compile(r"^\d{8}_\d{4}$")

AXIS_KO = {"AI_CAPEX": "AI 투자 경기", "RATES": "금리·자금조달", "GPU_SUPPLY": "GPU 공급",
           "POWER_PERMIT": "전력·인허가", "CRYPTO": "비트코인", "RISK_APPETITE": "투자 심리",
           "REGULATION": "규제", "USDC_DISTRIBUTION_ECONOMICS": "USDC 분배"}
# 축 방향 쉬운 말: 부호 + 이면 '좋아지면 ↑', - 이면 '오르면/막히면 ↓'
AXIS_DOWN_VERB = {"RATES": "오르면", "GPU_SUPPLY": "막히면", "POWER_PERMIT": "막히면"}
AXIS_UP_VERB = {"CRYPTO": "오르면", "RISK_APPETITE": "좋으면"}
KC_KO = {"KC-1": "기준금리 3.75% 초과", "KC-9": "유가 쇼크", "KC-10": "IREN 전력·인허가", "KC-3": "비트코인 급락"}

# 공개 금지 문구 — 개인 포지션·계좌 정보. 회사 재무를 말할 때도 '보유' 대신 다른 말을 쓴다(오탐 방지보다 차단 우선).
PRIVACY_PATTERNS = [
    r"비중", r"보유", r"포지션", r"평단", r"추가\s?매수", r"positions\.yaml", r"weight_range", r"cash_weight",
    r"집중\s?경보", r"내\s?계좌", r"내\s?결정", r"내\s?비중", r"\d+\s?주\s?@", r"[\w.+-]+@[\w-]+\.[\w.]+",
]
DISCLAIMER = "이 페이지는 판단을 돕기 위한 정리이며 매수·매도 지시가 아닙니다."

# 주가 캐시 — 공개 시장 데이터(종가)만. 렌더는 캐시만 읽고, 수집은 --update-prices에서만 한다(오프라인 재현성).
PRICES = ROOT / "state" / "weekly_prices.json"
BENCH = "QQQ"   # 비교 기준(나스닥100 ETF) — 판정에 쓰지 않는 참고선

# 업계 계약 비교 원장 — 채굴사 출신 데이터센터의 AI 임대·클라우드 계약과 자금 조달(공개 자료만). 판정에 쓰지 않는 참고 표.
PEERS = ROOT / "state" / "peer_contracts.json"

# 재무부 현금(TGA) 캐시 — 공개 정부 자료. 렌더는 캐시만 읽고, 수집은 --update-tga에서만 한다.
# plan(재무부 분기 차입 계획의 잔고 가정)은 사람이 원장처럼 적고 수집 때 보존된다. 판정에 쓰지 않는 참고 표.
TGA = ROOT / "state" / "weekly_tga.json"
TGA_API = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance"


def unit_price(c):
    """평균 단가 = 계약가치 ÷ 기간 ÷ 용량(계산값, $M / MW·년). unit_mw가 있으면 그 용량 기준(예: IT 용량 추정치), 없으면 it_mw.
    esc_pct(연 인상률 %)가 있으면 첫해 단가도 — 매년 같은 비율로 오르는 임대료의 합이 계약가치라는 가정."""
    mw = c.get("unit_mw") or c.get("it_mw")
    v, yrs = c.get("value_b"), c.get("years")
    if not (mw and v and yrs):
        return None
    out = {"mw_yr": round(v * 1000 / yrs / mw, 2)}
    g = c.get("esc_pct")
    if g:
        total = sum((1 + g / 100) ** i for i in range(int(yrs)))
        out["mw_yr_y1"] = round(v * 1000 / total / mw, 2)
    return out


def peer_tables(peers, today=None):
    """계약·자금 조달을 최근 날짜 순으로 정렬하고 단가를 붙인다. 발표 30일 이내 계약은 recent 표시."""
    if not peers:
        return None
    cos = peers.get("companies", {})
    contracts = []
    for c in peers.get("contracts", []):
        recent = bool(today and c.get("date") and (today - date.fromisoformat(c["date"])).days <= 30)
        contracts.append(dict(c, co_name=cos.get(c.get("co"), c.get("co")), unit=unit_price(c), recent=recent))
    contracts.sort(key=lambda c: (c.get("date", ""), c.get("co", "")), reverse=True)
    fin = [dict(f, co_name=cos.get(f.get("co"), f.get("co"))) for f in peers.get("financing", [])]
    fin.sort(key=lambda f: (f.get("date", ""), f.get("co", "")), reverse=True)
    return {"asof": peers.get("asof", ""), "note": peers.get("note", []), "companies": cos,
            "contracts": contracts, "financing": fin}


def fetch_prices(tickers, start, today):
    """yfinance 일별 종가. 당일 일봉 종가가 비어 있으면(게시 지연) 1시간 봉 마지막 값으로 채우고 provisional 표시."""
    import yfinance as yf
    syms = list(tickers) + [BENCH]
    df = yf.download(syms, start=start.isoformat(), end=(today + timedelta(days=1)).isoformat(),
                     progress=False, auto_adjust=False)["Close"]
    out = {}
    for t in syms:
        rows = []
        for idx, v in df[t].items():
            d = idx.date().isoformat()
            if v == v:   # NaN 제외
                rows.append([d, round(float(v), 2), False])
            elif idx.date() >= today - timedelta(days=4):
                h = yf.Ticker(t).history(period="5d", interval="1h")
                h = h[[x.date() == idx.date() for x in h.index]]
                if len(h):
                    rows.append([d, round(float(h["Close"].iloc[-1]), 2), True])
        out[t] = rows
    return out


def update_prices(tickers, start, today):
    cache = load_json(PRICES) or {"daily": {}}
    new = fetch_prices(tickers, start, today)
    for t, rows in new.items():
        merged = {r[0]: r for r in cache["daily"].get(t, [])}
        merged.update({r[0]: r for r in rows})          # 같은 날짜는 새 값(확정치)이 잠정치를 덮는다
        cache["daily"][t] = [merged[k] for k in sorted(merged)]
    cache.update({"as_of": today.isoformat(), "source": "yfinance (일봉 종가, 게시 지연 시 1시간 봉 마지막 값 = 잠정)",
                  "benchmark": BENCH})
    PRICES.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return cache


def weekly_prices(cache, tickers, first_monday, this_monday):
    """주(월~일)별 마지막 종가와 전주 대비 등락. 첫 주 종가 = 100 지수도 함께."""
    if not cache:
        return None
    series = {}
    for t in list(tickers) + [BENCH]:
        rows = cache.get("daily", {}).get(t, [])
        by_w = {}
        for d, c, prov in rows:
            w = monday(date.fromisoformat(d))
            by_w[w] = (d, c, prov)           # 행이 날짜순이라 마지막 값이 그 주 종가
        series[t] = by_w
    weeks, w = [], first_monday
    while w <= this_monday:
        weeks.append(w)
        w += timedelta(days=7)
    out = {"weeks": [], "tickers": list(tickers), "bench": BENCH, "as_of": cache.get("as_of"), "source": cache.get("source", "")}
    base = {t: next((series[t][x][1] for x in weeks if x in series[t]), None) for t in series}
    for w in weeks:
        rec = {"w": w.isoformat(), "label": f"{md(w)}~{md(w + timedelta(days=6))}", "now": w == this_monday, "v": {}}
        prev_w = w - timedelta(days=7)
        for t, by_w in series.items():
            if w not in by_w:
                continue
            d, c, prov = by_w[w]
            p = by_w.get(prev_w)
            chg = round((c / p[1] - 1) * 100, 1) if p else None
            idx = round(c / base[t] * 100, 1) if base[t] else None
            rec["v"][t] = {"close": c, "chg": chg, "idx": idx, "last": md(date.fromisoformat(d)), "prov": prov}
        out["weeks"].append(rec)
    return out


TGA_KEYS = {"Treasury General Account (TGA) Closing Balance": "close", "Total TGA Deposits (Table II)": "dep",
            "Total TGA Withdrawals (Table II) (-)": "wd"}


def fetch_tga(start):
    """재무부 일일 재무제표(DTS) 영업현금잔고 표 → [[날짜, 마감 잔고, 들어온 돈, 나간 돈]] ($B). 원자료 단위는 $M."""
    import urllib.request
    url = (TGA_API + f"?filter=record_date:gte:{start.isoformat()}&fields=record_date,account_type,open_today_bal"
           "&sort=record_date&page%5Bsize%5D=10000")
    with urllib.request.urlopen(url, timeout=30) as r:
        rows = json.load(r)["data"]
    by = {}
    for x in rows:
        k, v = TGA_KEYS.get(x["account_type"]), x.get("open_today_bal")
        if k and v not in (None, "", "null"):
            by.setdefault(x["record_date"], {})[k] = round(float(v) / 1000, 1)
    return [[d, v["close"], v.get("dep"), v.get("wd")] for d, v in sorted(by.items()) if "close" in v]


def update_tga(start, today):
    cache = load_json(TGA) or {"daily": [], "plan": []}
    merged = {r[0]: r for r in cache.get("daily", [])}
    merged.update({r[0]: r for r in fetch_tga(start)})
    cache["daily"] = [merged[k] for k in sorted(merged)]
    cache.update({"as_of": today.isoformat(),
                  "source": "미국 재무부 일일 재무제표(Daily Treasury Statement) 영업현금잔고 — Fiscal Data API"})
    TGA.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return cache


def weekly_tga(cache, first_monday, this_monday, today):
    """주별 마지막 잔고·전주 대비·주중 최저~최고·들어온/나간 돈 합계 + 최근 1년 일별 선 + 재무부 계획 대비."""
    if not cache or not cache.get("daily"):
        return None
    daily = cache["daily"]
    by_w = {}
    for r in daily:
        by_w.setdefault(monday(date.fromisoformat(r[0])), []).append(r)
    weeks, w = [], first_monday
    while w <= this_monday:
        rs = by_w.get(w)
        if rs:
            prev = by_w.get(w - timedelta(days=7))
            last = rs[-1]
            weeks.append({"w": w.isoformat(), "label": f"{md(w)}~{md(w + timedelta(days=6))}", "now": w == this_monday,
                          "close": last[1], "last": md(date.fromisoformat(last[0])),
                          "chg": round(last[1] - prev[-1][1], 1) if prev else None,
                          "lo": min(r[1] for r in rs), "hi": max(r[1] for r in rs),
                          "dep": round(sum(r[2] or 0 for r in rs), 1), "wd": round(sum(r[3] or 0 for r in rs), 1),
                          "days": len(rs)})
        w += timedelta(days=7)
    start = (today - timedelta(days=365)).isoformat()
    last_d = daily[-1][0]
    plan = []
    for p in cache.get("plan", []):
        q = dict(p)
        if p.get("date"):                       # 시점 가정: 그날(없으면 직전 영업일) 마감 잔고와 비교
            hit = [r for r in daily if r[0] <= p["date"]]
            if p["date"] <= last_d and hit:
                q["actual"], q["actual_d"] = hit[-1][1], hit[-1][0]
                q["state"] = "지남"
            else:
                q["state"] = "아직"
        else:                                   # 기간 예상: 기간 안 최고치(지금까지)
            inr = [r for r in daily if p["from"] <= r[0] <= p["to"]]
            if inr:
                top = max(inr, key=lambda r: r[1])
                q["actual"], q["actual_d"] = top[1], top[0]
                q["state"] = "진행 중" if last_d < p["to"] else "지남"
            else:
                q["state"] = "아직"
        if "actual" in q:
            q["gap"] = round(q["actual"] - p["value"], 1)
        plan.append(q)
    return {"weeks": weeks, "daily": [r for r in daily if r[0] >= start], "plan": plan, "plan_note": cache.get("plan_note", ""),
            "as_of": cache.get("as_of"), "source": cache.get("source", ""), "last": [last_d, daily[-1][1]]}


PS_METRICS =[("rev", "주당 최근 분기 매출(연환산)"), ("arr_live", "주당 가동 중 ARR"), ("arr_contract", "주당 계약 ARR")]


def usd_m(v):
    """$M → '$1.37억' (1억 달러 = $100M)."""
    return "$" + f"{v / 100:.2f}".rstrip("0").rstrip(".") + "억"


def per_share_series(store, tickers):
    """원장 per_share의 원본 숫자($M·백만 주)로 주당 매출·ARR을 계산한다(계산값 — 회사 공표치 아님).
    주식 수 분모는 완전희석(큰 수 → 작은 값)~발행(작은 수 → 큰 값) 범위, 변화율은 발행 주식 기준 직전 입력 대비."""
    out = {}
    for tk in tickers:
        snaps = sorted(store.get("per_share", {}).get(tk, []), key=lambda s: s["asof"])
        rows, prev = [], None
        for s in snaps:
            basic = s["sh_basic"]
            fd = max(s.get("sh_fd") or basic, basic)
            nums = {"rev": s["rev_q"] * 4 if s.get("rev_q") is not None else None,
                    "arr_live": s.get("arr_live"), "arr_contract": s.get("arr_contract")}
            m = {}
            for k, num in nums.items():
                if num is None:
                    m[k] = None
                    continue
                m[k] = {"lo": round(num / fd, 2), "hi": round(num / basic, 2), "chg": None}
                if prev and prev.get(k):
                    m[k]["chg"] = round((num / basic) / (prev[k]["_hi"]) * 100 - 100, 1)
                m[k]["_hi"] = num / basic
            rows.append({**{k: v for k, v in s.items()}, "m": m})
            prev = m
        for r in rows:
            for v in r["m"].values():
                if v:
                    v.pop("_hi", None)
        out[tk] = rows[::-1]   # 최신 입력이 위
    return out


def per_share_table_rows(r):
    """희석 점검표(dilution) ⓒ 행 — 최신 per_share 입력에서 자동 생성."""
    src = {"rev": f"{r.get('rev_q_period', '최근 분기')} 매출 {usd_m(r['rev_q']) if r.get('rev_q') is not None else ''} × 4",
           "arr_live": f"가동 중 ARR {usd_m(r['arr_live']) if r.get('arr_live') is not None else ''}" + (f"({r['arr_live_asof']})" if r.get("arr_live_asof") else ""),
           "arr_contract": f"계약 ARR {usd_m(r['arr_contract']) if r.get('arr_contract') is not None else ''}"}
    out = []
    for k, label in PS_METRICS:
        v = r["m"].get(k)
        if not v:
            out.append([f"ⓒ {label}", "—", "이번 입력에 숫자 없음(회사가 공개하지 않으면 그대로 둠)", ""])
            continue
        chg = "첫 기록" if v["chg"] is None else f"{'▲' if v['chg'] > 0 else '▼' if v['chg'] < 0 else '–'} {abs(v['chg'])}% (발행 주식 기준, 직전 입력 대비)"
        out.append([f"ⓒ {label}", f"${v['lo']:.2f}~{v['hi']:.2f}",
                    f"자동 계산: {src[k]} ÷ 완전희석~발행 주식 수 ({r['asof']} 입력)", chg])
    return out


def load_json(p):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else None


def privacy_hits(text):
    hits = []
    for pat in PRIVACY_PATTERNS:
        for m in re.finditer(pat, text):
            s = max(0, m.start() - 20)
            hits.append((pat, text[s:m.end() + 20].replace("\n", " ")))
    return hits


def monday(d):
    return d - timedelta(days=d.weekday())


def md(d):
    return f"{d.month}/{d.day}"


def run_dirs():
    out = ROOT / "output"
    return sorted(p for p in out.iterdir() if p.is_dir() and RUN_RE.match(p.name)) if out.exists() else []


def run_date(run_dir, doc):
    s = (doc or {}).get("as_of") or ""
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        return datetime.strptime(run_dir.name[:8], "%Y%m%d").date()


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def kill_info(sig):
    """arbiter 산출물 간 키 불일치 흡수: triggered/kill_priority_triggered, trigger_source/kill_trigger_kc."""
    kc = sig.get("kill_check") or {}
    trig = kc.get("triggered", kc.get("kill_priority_triggered"))
    # 항목마다 맨 앞 KC만 쓴다 — "KC-1 단독 (KC-9는 해제됨)" 같은 서술 속 언급을 원인으로 오독하지 않기 위함
    src = []
    for x in as_list(kc.get("trigger_source", kc.get("kill_trigger_kc"))):
        m = re.match(r"\s*(KC-[A-Z]*-?\d+)", str(x))
        if m:
            src.append(m.group(1))
    return bool(trig), sorted(set(src))


def gate_info(sig):
    """상향 게이트 3요건 — 스키마 변형(conditions_met / conditions / 최상위 키) 흡수. 값이 없으면 None."""
    gc = sig.get("gate_check") or {}
    ug = gc.get("upgrade_gate") or {}
    conds = ug.get("conditions_met") or ug.get("conditions") or {}

    def pick(*keys):
        for src in (conds, ug, gc):
            for k in keys:
                if isinstance(src.get(k), bool):
                    return src[k]
        return None
    return {"숫자 확인": pick("quantitative", "quantitative_evidence"),
            "회사 고유": pick("company_specific"),
            "매출 인식": pick("revenue_recognized")}


def kc_plain(src):
    return ", ".join(f"{k}({KC_KO[k]})" if k in KC_KO else k for k in src)


def collect_signals(tickers):
    """run별 03_signal을 날짜 단위로 모은다. 같은 날 여러 run이면 종목별 마지막 run을 쓴다."""
    by_day = {}
    latest = {}
    for rd in run_dirs():
        for t in tickers:
            sig = load_json(rd / "03_signal" / f"{t}.json")
            if not sig or not sig.get("proposed_signal"):
                continue
            d = run_date(rd, sig)
            by_day.setdefault(d, {})[t] = (rd.name, sig)
            latest[t] = (rd.name, d, sig)
    return dict(sorted(by_day.items())), latest


def system_events(by_day, tickers):
    events, streak = [], {t: 0 for t in tickers}
    for d, per in by_day.items():
        parts, kcs = [], set()
        for t in tickers:
            if t not in per:
                continue
            _, sig = per[t]
            prior, prop = sig.get("prior_signal"), sig.get("proposed_signal")
            if prop and prior and prop != prior:
                streak[t] += 1
                parts.append(f"{t} {prop} 후보" + (f"({streak[t]}회 연속)" if streak[t] > 1 else ""))
            else:
                streak[t] = 0
                parts.append(f"{t} {prop} 유지")
            trig, src = kill_info(sig)
            if trig:
                kcs.update(src)
        why = (f"손절 조건 {kc_plain(sorted(kcs))}이 우선 적용된 결과입니다. 확정은 사람이 합니다." if kcs
               else "등급 후보는 시스템이 내고, 확정은 사람이 합니다.")
        events.append({"date": d.isoformat(), "tk": "공통", "kind": "system",
                       "text": "시스템 점검: " + " · ".join(parts), "why": why})
    return events


def decision_events(signals, tickers):
    groups = {}
    for tr in (signals or {}).get("transitions", []):
        if tr.get("ticker") not in tickers or not tr.get("decided_on"):
            continue
        key = (tr["decided_on"][:10], tr.get("from"), tr.get("to"), tuple(as_list(tr.get("trigger_source"))))
        groups.setdefault(key, []).append(tr["ticker"])
    out = []
    for (d, frm, to, src), tks in sorted(groups.items()):
        why = f"사유: 손절 조건 {kc_plain(list(src))} 충족이 여러 번 연속 확인됨." if src else ""
        out.append({"date": d, "tk": "공통", "kind": "decision", "eff": "neu",
                    "text": f"등급 확정: {'·'.join(tks)} {frm} → {to}", "why": why})
    return out


def exposure_rows(tickers):
    cm = yaml.safe_load((ROOT / "config" / "correlation_matrix.yaml").read_text(encoding="utf-8")) or {}
    exp = cm.get("exposures") or {}
    axes = [a for a in AXIS_KO if any(a in (exp.get(t) or {}) for t in tickers)]
    rows = []
    for t in tickers:
        cells = []
        for a in axes:
            v = (exp.get(t) or {}).get(a)
            if not v:
                cells.append(("na", "—"))
                continue
            strong = "크게 " if v.get("strength") == "H" else ""
            if v.get("sign") == "+":
                cells.append(("up", f"{AXIS_UP_VERB.get(a, '좋아지면')} {strong}↑"))
            else:
                cells.append(("dn", f"{AXIS_DOWN_VERB.get(a, '나빠지면')} {strong}↓"))
        rows.append((t, cells))
    return [AXIS_KO[a] for a in axes], rows


DIR_KO = {"up": "유리 쪽", "down": "불리 쪽", "watch": "관찰"}


def short(s, n=60):
    s = str(s or "")
    return s if len(s) <= n else s[:n].rstrip() + "…"


def link_events(events, store, tickers, this_monday, warnings, todo):
    """원장 이벤트의 links·threads·exposure를 화면용으로 풀어 쓴다. 판정은 만들지 않고 원장 서술을 연결만 한다."""
    by_id = {e["id"]: e for e in events if e.get("id")}
    axes, rows = exposure_rows(tickers)
    cell = {(t, a): c for t, cs in rows for a, c in zip(axes, cs)}
    thread_title = {t["id"]: t["title"] for t in store.get("threads", [])}
    overlay, off = {}, []
    for e in events:
        rl = []
        for l in e.get("links", []):
            tgt = by_id.get(l.get("id"))
            if not tgt:
                warnings.append(f"{e.get('id')}: 없는 링크 {l.get('id')}")
                continue
            rl.append({"id": tgt["id"], "dt": tgt["dt"], "tk": tgt["tk"], "text": short(tgt["text"]), "why": l.get("why", "")})
        e["links"] = rl
        th = []
        for tid in e.get("threads", []):
            if tid not in thread_title:
                warnings.append(f"{e.get('id')}: 없는 이야기 {tid}")
                continue
            th.append({"id": tid, "title": thread_title[tid]})
        e["threads"] = th
        ex = []
        for x in e.get("exposure", []):
            c = cell.get((x.get("tk"), x.get("axis")))
            in_matrix = bool(c and c[0] != "na")
            y = dict(x, in_matrix=in_matrix, cell=c[1] if in_matrix else "")
            ex.append(y)
            if monday(e["_d"]) == this_monday:
                if in_matrix:
                    overlay.setdefault((x["tk"], x["axis"]), []).append({"dir": x.get("dir"), "note": x.get("note", ""), "dt": e["dt"]})
                else:
                    off.append({"tk": x.get("tk"), "axis": x.get("axis"), "dir": x.get("dir"), "note": x.get("note", ""), "dt": e["dt"]})
        e["exposure"] = ex
    threads = []
    for t in store.get("threads", []):
        evs = []
        for i in t.get("events", []):
            if i not in by_id:
                warnings.append(f"{t['id']}: 없는 이벤트 {i}")
                continue
            evs.append(by_id[i])
        evs.sort(key=lambda e: e["_d"])
        last = max((e["_d"] for e in evs), default=date.min)
        threads.append({**{k: v for k, v in t.items() if k != "events"},
                        "updated": any(monday(e["_d"]) == this_monday for e in evs), "_last": last,
                        "items": [{"id": e["id"], "dt": e["dt"], "tk": e["tk"], "text": short(e["text"], 80), "eff": e.get("eff", ""),
                                   "rumor": bool(e.get("rumor")), "now": monday(e["_d"]) == this_monday} for e in evs]})
    threads.sort(key=lambda t: (t["updated"], t.get("tk") == "공통", t["_last"]), reverse=True)  # 공통(매크로) 이야기는 등급의 원인이라 앞에
    for t in threads:
        ex = t.get("explainer")
        if t["updated"] and not ex:
            todo.append(f"{t['id']}: 이번 주 소식이 붙었는데 상세 해설(explainer)이 없음")
        elif ex and ex.get("asof") and t["_last"] > date.fromisoformat(ex["asof"]):
            t["explainer_stale"] = True
            todo.append(f"{t['id']}: 해설 기준일({ex['asof']}) 이후 새 소식이 있음 — 해설 갱신 필요")
        # 추적 표(id가 있는 explainer.tables)는 소식 유무와 무관하게 매주 칸별로 다시 확인한다
        stale = [tb["id"] for tb in (ex or {}).get("tables", [])
                 if tb.get("id") and (not tb.get("asof") or date.fromisoformat(tb["asof"]) < this_monday)]
        for tid in stale:
            todo.append(f"{t['id']}/{tid}: 추적 표를 이번 주에 확인하지 않음 — 칸별 재확인 후 asof 갱신 필요")
        t["stale_tables"] = stale
        t["last"] = md(t.pop("_last")) if t["items"] else ""
    # 종목마다 있어야 하는 추적 표(원장 required_tables, 예: 희석 점검표 dilution) — 아직 없으면 만들라고 안내
    for tid, tks in store.get("required_tables", {}).items():
        for tk in tks:
            if not any(t.get("tk") == tk and any(tb.get("id") == tid for tb in (t.get("explainer") or {}).get("tables", []))
                       for t in threads):
                todo.append(f"{tk}/{tid}: 종목 추적 표가 아직 없음 — 그 종목의 자금 이야기 해설에 표를 만들어야 함")
    return threads, overlay, off


def build(today, store, tickers):
    signals = load_json(ROOT / "state" / "signals.json") or {}
    by_day, latest = collect_signals(tickers)

    events = [dict(e) for e in store.get("events", [])]
    events += system_events(by_day, tickers) + decision_events(signals, tickers)
    for e in events:
        e["_d"] = date.fromisoformat(e["date"])
        e.setdefault("dt", md(e["_d"]))
    warnings, todo = [], []
    threads, overlay, off = link_events(events, store, tickers, monday(today), warnings, todo)

    # 주 묶음: 첫 이벤트 주 ~ 이번 주, 최신 주 먼저
    first = monday(min(e["_d"] for e in events)) if events else monday(today)
    weeks, w = [], monday(today)
    titles = store.get("week_titles", {})
    while w >= first:
        items = sorted((e for e in events if monday(e["_d"]) == w), key=lambda e: e["_d"], reverse=True)
        wend = w + timedelta(days=6)
        title = titles.get(w.isoformat()) or ("이번 주" if w == monday(today) else f"소식 {len(items)}건")
        weeks.append({"d": f"{md(w)} ~ {md(wend)}", "title": title, "now": w == monday(today),
                      "items": [{k: v for k, v in e.items() if k != "_d" and k != "date"} for e in items]})
        w -= timedelta(days=7)

    # 현재 등급 카드
    grades = signals.get("grades", {})
    status = []
    for t in tickers:
        g = grades.get(t, {})
        since = g.get("since", "")
        prev = next((tr for tr in reversed(signals.get("transitions", []))
                     if tr.get("ticker") == t and tr.get("to") == g.get("signal")), None)
        since_txt = f"{md(date.fromisoformat(since[:10]))} 확정" if since[:10] else ""
        if prev and prev.get("from"):
            since_txt += f" (이전 {prev['from']})"
        gate, gate_asof = {}, ""
        if t in latest:
            gate, gate_asof = gate_info(latest[t][2]), md(latest[t][1])
        status.append({"tk": t, "sig": g.get("signal", "?"), "since": since_txt,
                       "gate": [[k, v] for k, v in gate.items()], "gate_asof": gate_asof,
                       "next": store.get("status_notes", {}).get(t, "")})

    prices = weekly_prices(load_json(PRICES), tickers, first, monday(today))
    if prices:
        by_w = {r["w"]: r for r in prices["weeks"]}
        cur = monday(today)
        for wk in weeks:   # 각 주 카드에 그 주의 등락을 붙인다
            r = by_w.get(cur.isoformat()); wk["price"] = r["v"] if r else {}
            cur -= timedelta(days=7)
    tga = weekly_tga(load_json(TGA), first, monday(today), today)
    if tga:
        by_t = {r["w"]: r for r in tga["weeks"]}
        cur = monday(today)
        for wk in weeks:   # 각 주 카드에 그 주의 재무부 현금 잔고를 붙인다
            wk["tga"] = by_t.get(cur.isoformat())
            cur -= timedelta(days=7)

    upcoming = [u for u in store.get("upcoming", [])
                if not u.get("until") or date.fromisoformat(u["until"]) >= today]
    # 주당 매출·ARR — 원장 per_share 원본 숫자로 계산하고, 희석 점검표의 ⓒ 행을 최신 입력으로 바꿔 끼운다
    per_share = per_share_series(store, tickers)
    if "per_share" in store:
        for tk in tickers:
            if not per_share.get(tk):
                todo.append(f"{tk}/per_share: 주당 매출·ARR 입력이 아직 없음 — 원장 per_share에 원본 숫자를 넣어야 함")
    for t in threads:
        ex = t.get("explainer")
        if not (ex and per_share.get(t.get("tk"))):
            continue
        tables = []
        for tb in ex.get("tables", []):
            if tb.get("id") == "dilution":
                tb = dict(tb, rows=[r for r in tb["rows"] if not str(r[0]).startswith("ⓒ")] + per_share_table_rows(per_share[t["tk"]][0]))
            tables.append(tb)
        t["explainer"] = dict(ex, tables=tables)

    axes, exp_rows = exposure_rows(tickers)
    last_check = max((d for d in by_day), default=None)
    return {"weeks": weeks, "status": status, "upcoming": upcoming, "axes": axes, "exp_rows": exp_rows,
            "last_check": last_check, "first_week": first, "threads": threads, "overlay": overlay,
            "off_matrix": off, "warnings": warnings, "explainer_todo": todo, "prices": prices, "tga": tga,
            "peers": peer_tables(load_json(PEERS), today), "per_share": per_share}


def esc(x):
    return html.escape("" if x is None else str(x), quote=True)


def render_html(today, store, tickers, data):
    lc = data["last_check"]
    stale = ""
    if lc and (today - lc).days > 10:
        stale = (f'<div class="callout warn">마지막 시스템 점검이 {md(lc)}({(today - lc).days}일 전)입니다. '
                 f'그 뒤 소식은 아직 반영되지 않았을 수 있습니다.</div>')
    exp_head = "".join(f"<th>{esc(a)}</th>" for a in data["axes"])

    def marks(t, a):
        ov = data["overlay"].get((t, a), [])
        if not ov:
            return ""
        sym = {"up": "▲", "down": "▼", "watch": "●"}
        tip = " / ".join(f"{o['dt']} {DIR_KO.get(o['dir'], '')}: {o['note']}" for o in ov)
        return f'<div class="wk-mark" title="{esc(tip)}">' + "".join(f'<span class="m {o["dir"]}">{sym.get(o["dir"], "●")}</span>' for o in ov) + "</div>"
    exp_body = "".join(
        f'<tr><td><span class="tk {t}">{t}</span></td>' + "".join(
            f'<td><span class="ex {c}">{esc(s)}</span>{marks(t, a)}</td>' for a, (c, s) in zip(data["axes"], cells)) + "</tr>"
        for t, cells in data["exp_rows"])
    wk_notes = "".join(
        f'<li><span class="tk {t}">{t}</span> · {esc(a)}: ' + " / ".join(f'<span class="m {o["dir"]}">{DIR_KO.get(o["dir"], "")}</span> {esc(o["note"])} ({esc(o["dt"])})' for o in ov) + "</li>"
        for (t, a), ov in sorted(data["overlay"].items()))
    off_notes = "".join(
        f'<li><span class="tk {esc(o["tk"])}">{esc(o["tk"])}</span> · {esc(o["axis"])}: <span class="m {o["dir"]}">{DIR_KO.get(o["dir"], "")}</span> {esc(o["note"])} ({esc(o["dt"])})</li>'
        for o in data["off_matrix"])
    week_exp = ""
    if wk_notes or off_notes:
        week_exp = ('<div class="wk-exp"><b>이번 주 매트릭스 움직임</b> <span class="small">(▲ 유리 쪽 · ▼ 불리 쪽 · ● 관찰 — 칸 위 표시와 같음)</span>'
                    + (f"<ul>{wk_notes}</ul>" if wk_notes else "")
                    + (f'<b>매트릭스 밖 노출 (관찰 메모)</b> <span class="small">— 지금 매트릭스에 없는 축에 닿은 소식. 매트릭스 변경은 사용자 결정 영역</span><ul>{off_notes}</ul>' if off_notes else "")
                    + "</div>")
    payload = json.dumps({"status": data["status"], "upcoming": data["upcoming"], "weeks": data["weeks"],
                          "threads": data["threads"], "prices": data["prices"], "tga": data.get("tga"), "peers": data.get("peers"),
                          "per_share": data.get("per_share")},
                         ensure_ascii=False, default=str).replace("</", "<\\/")
    tks = " · ".join(tickers)
    filters = "".join(f'<button data-f="{t}">{t}</button>' for t in tickers)
    fw = data["first_week"]
    period = f"{fw.year}년 {fw.month}/{fw.day} 주부터"
    return TEMPLATE.format(
        tks=esc(tks), period=esc(period), today=today.isoformat(), last_check=esc(lc.isoformat() if lc else "없음"),
        headline=esc(store.get("headline", "")), stale=stale, exp_head=exp_head, exp_body=exp_body, week_exp=week_exp,
        filters=filters, payload=payload, disclaimer=DISCLAIMER, updated=esc(store.get("updated_at", "")))


def pending(store, tickers):
    """curated_through_run 이후 run의 신규 Claim·비중립 Delta — 쉬운 말 정리 대상."""
    after = store.get("curated_through_run", "")
    out = []
    for rd in run_dirs():
        if rd.name <= after:
            continue
        for t in tickers:
            comp = load_json(rd / "02_company" / f"{t}.json")
            if not comp:
                continue
            for c in comp.get("claims", []):
                s = c.get("source") or {}
                out.append({"run": rd.name, "ticker": t, "id": c.get("id"), "filed_at": s.get("filed_at"),
                            "evidence_grade": c.get("evidence_grade"), "confirmed": c.get("confirmed"),
                            "scope": c.get("scope"), "claim_type": c.get("claim_type"), "text": c.get("text")})
            for dl in comp.get("deltas", []):
                if str(dl.get("direction")).lower() not in ("neutral", "중립", "none"):
                    out.append({"run": rd.name, "ticker": t, "delta_axis": dl.get("axis"),
                                "direction": dl.get("direction"), "stage": dl.get("stage"), "text": dl.get("new_state")})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "output" / "weekly_events.html"))
    ap.add_argument("--today", default=None)
    ap.add_argument("--pending", action="store_true")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--update-prices", action="store_true", help="yfinance로 일별 종가를 받아 state/weekly_prices.json 갱신 후 렌더")
    ap.add_argument("--update-tga", action="store_true", help="재무부 일일 재무제표로 TGA 잔고를 받아 state/weekly_tga.json 갱신 후 렌더")
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    store = load_json(STORE)
    if store is None:
        print(f"원장 없음: {STORE}")
        return 1
    tickers = store.get("tickers") or ["IREN", "NBIS", "CRWV"]

    if a.pending:
        items = pending(store, tickers)
        p = ROOT / "output" / "weekly_events_pending.json"
        p.write_text(json.dumps({"curated_through_run": store.get("curated_through_run"), "items": items},
                                ensure_ascii=False, indent=1), encoding="utf-8")
        runs = sorted({i["run"] for i in items})
        print(f"정리 대기 {len(items)}건 (run: {', '.join(runs) or '없음'}) → {p}")
        return 0

    today = date.fromisoformat(a.today) if a.today else date.today()
    if a.update_prices:
        first = min(date.fromisoformat(e["date"]) for e in store.get("events", []))
        c = update_prices(tickers, monday(first) - timedelta(days=14), today)
        last = {t: (rows[-1] if rows else None) for t, rows in c["daily"].items()}
        print("주가 갱신: " + " · ".join(f"{t} {r[0]} {r[1]}{'(잠정)' if r[2] else ''}" for t, r in last.items() if r))
    if a.update_tga:
        try:
            c = update_tga(today - timedelta(days=400), today)
            print(f"TGA 갱신: {c['daily'][-1][0]} ${c['daily'][-1][1]:,.1f}B ({len(c['daily'])}일)")
        except Exception as ex:   # 네트워크 실패 시 캐시로 렌더
            print(f"TGA 갱신 실패 — 캐시로 렌더: {ex}")
    data = build(today, store, tickers)
    for w in data["warnings"]:
        print(f"경고(연결): {w}")
    for w in data["explainer_todo"]:
        print(f"안내(해설): {w}")
    page = render_html(today, store, tickers, data)
    hits = privacy_hits(page.replace(DISCLAIMER, ""))
    if hits:
        print("개인정보 의심 문구 발견 — 파일을 쓰지 않습니다:")
        for pat, ctx in hits:
            print(f"  [{pat}] …{ctx}…")
        return 2
    if a.check_only:
        print("개인정보 검사 통과")
        return 0
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    n = sum(len(w["items"]) for w in data["weeks"])
    print(f"생성: {out} — {len(data['weeks'])}주 · 항목 {n}건 · 마지막 점검 {data['last_check']}")
    return 0


TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>네오클라우드 주간 이벤트</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f7f6f3;--card:#fff;--ink:#1d1d1f;--ink2:#55575c;--ink3:#8a8c91;--line:#e4e2dc;
--IREN:#2a78d6;--NBIS:#eb6834;--CRWV:#1baf7a;--macro:#5b6270;--bench:#8a8c91;
--good:#1a7f37;--bad:#cf222e;--mix:#b7791f;--neu:#8a8c91;--goodbg:#e8f5ec;--badbg:#fdecee;--mixbg:#fbf3e2;--neubg:#f0f0ee;--chip:#f0efea;--hl:#fff8e1}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#121316;--card:#1b1d21;--ink:#ececee;--ink2:#b4b6bb;--ink3:#83868c;--line:#2c2f35;
--IREN:#3987e5;--NBIS:#d95926;--CRWV:#199e70;--macro:#9aa3b2;--bench:#83868c;--good:#3fb950;--bad:#ff7b72;--mix:#e3b341;--neu:#8b949e;
--goodbg:#16291c;--badbg:#2d1719;--mixbg:#2b2312;--neubg:#24262b;--chip:#25282d;--hl:#2a2614}}}}
:root[data-theme="dark"]{{--bg:#121316;--card:#1b1d21;--ink:#ececee;--ink2:#b4b6bb;--ink3:#83868c;--line:#2c2f35;
--IREN:#3987e5;--NBIS:#d95926;--CRWV:#199e70;--macro:#9aa3b2;--bench:#83868c;--good:#3fb950;--bad:#ff7b72;--mix:#e3b341;--neu:#8b949e;
--goodbg:#16291c;--badbg:#2d1719;--mixbg:#2b2312;--neubg:#24262b;--chip:#25282d;--hl:#2a2614}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Sans KR",-apple-system,"Malgun Gothic",sans-serif;font-size:15px;line-height:1.65;word-break:keep-all}}
.wrap{{max-width:980px;margin:0 auto;padding:28px 16px 64px}}
h1{{font-size:26px;margin:0 0 4px;letter-spacing:-.3px}} h2{{font-size:19px;margin:40px 0 12px}}
.sub{{color:var(--ink2);margin:0 0 20px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
.tk{{font-weight:700;letter-spacing:.3px;color:var(--ink);white-space:nowrap}} .tk::before{{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:1px;background:var(--macro)}}
.tk.IREN::before{{background:var(--IREN)}} .tk.NBIS::before{{background:var(--NBIS)}} .tk.CRWV::before{{background:var(--CRWV)}}
.status .big{{font-size:22px;margin:4px 0 2px}} .meta{{color:var(--ink2);font-size:13.5px}}
.gate{{display:flex;gap:6px;flex-wrap:wrap;margin:10px 0 6px}}
.g{{font-size:12.5px;padding:2px 8px;border-radius:999px}} .g.ok{{background:var(--goodbg);color:var(--good)}} .g.no{{background:var(--neubg);color:var(--ink3)}}
.next{{font-size:13.5px;color:var(--ink2);border-top:1px dashed var(--line);padding-top:8px;margin-top:8px}}
.howto{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}} .howto b{{display:block;margin-bottom:2px}} .howto p{{margin:0;color:var(--ink2);font-size:14px}}
.callout{{background:var(--hl);border-radius:10px;padding:12px 14px;font-size:14px;margin-top:12px}} .callout.warn{{border:1px solid var(--mix)}}
table{{width:100%;border-collapse:collapse;font-size:14px}} th,td{{padding:9px 8px;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}}
th{{color:var(--ink2);font-weight:500;font-size:13px}} td:first-child,th:first-child{{text-align:left}} .tblwrap{{overflow-x:auto}}
.ex{{display:inline-block;padding:1px 8px;border-radius:6px;font-size:13px}} .ex.up{{background:var(--goodbg);color:var(--good)}} .ex.dn{{background:var(--badbg);color:var(--bad)}} .ex.na{{color:var(--ink3)}}
.legend{{font-size:13px;color:var(--ink2);margin-top:8px}}
.filters{{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 16px;position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:5}}
.filters button{{font:inherit;font-size:14px;padding:5px 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}}
.filters button.on{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
.week{{margin-bottom:16px}} .wk-h{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:8px}}
.wk-date{{font-size:13px;color:var(--ink3)}} .wk-title{{font-weight:700;font-size:16.5px}} .wk-now{{font-size:12px;background:var(--ink);color:var(--bg);padding:1px 8px;border-radius:999px}}
.ev{{display:grid;grid-template-columns:62px 54px 1fr;gap:10px;padding:10px 0;border-top:1px solid var(--line)}} .ev:first-of-type{{border-top:none}}
@media(max-width:560px){{.ev{{grid-template-columns:50px 1fr}}.ev .who{{grid-column:1;grid-row:2}}.ev .body{{grid-column:2;grid-row:1/3}}}}
.ev .d{{font-size:13px;color:var(--ink3);padding-top:2px}} .ev .who{{font-size:13px;padding-top:2px}}
.ev .body p{{margin:0}} .ev .why{{color:var(--ink2);font-size:14px;margin-top:3px}}
.tags{{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}} .t{{font-size:12px;padding:1px 8px;border-radius:6px;background:var(--chip);color:var(--ink2)}}
.t.good{{background:var(--goodbg);color:var(--good)}} .t.bad{{background:var(--badbg);color:var(--bad)}} .t.mix{{background:var(--mixbg);color:var(--mix)}} .t.neu{{background:var(--neubg);color:var(--neu)}}
.t.rumor{{border:1px dashed var(--ink3);background:transparent;color:var(--ink3)}} .t.sys{{background:transparent;border:1px solid var(--line)}}
.ev.system .body > p:first-child{{color:var(--ink2)}} .ev.decision{{background:var(--hl);border-radius:8px;padding-left:8px;padding-right:8px}}
.empty{{color:var(--ink3);font-size:14px;padding:6px 0}} .ps+.ps{{margin-top:14px}}.foot{{color:var(--ink3);font-size:12.5px;margin-top:36px;line-height:1.7}}
.small{{font-size:12.5px;color:var(--ink3);font-weight:400}}
.wk-mark{{margin-top:3px;font-size:11px;letter-spacing:1px;cursor:help}}
.m.up{{color:var(--good)}} .m.down{{color:var(--bad)}} .m.watch{{color:var(--mix)}}
.wk-exp{{margin-top:14px;padding-top:12px;border-top:1px dashed var(--line);font-size:14px}} .wk-exp ul{{margin:6px 0 10px;padding-left:18px}} .wk-exp li{{margin:3px 0}}
.detail{{margin:8px 0 0;padding-left:18px;font-size:14px}} .detail li{{margin:3px 0}}
.sec{{margin-top:10px;font-size:13.5px}} .sec-h{{font-size:12.5px;color:var(--ink3);font-weight:500;margin-bottom:3px}}
.exrow{{display:flex;gap:6px;align-items:baseline;flex-wrap:wrap;margin:3px 0}}
.exk{{font-size:12px;padding:1px 7px;border-radius:6px;white-space:nowrap}} .exk.up{{background:var(--goodbg);color:var(--good)}} .exk.down{{background:var(--badbg);color:var(--bad)}} .exk.watch{{background:var(--mixbg);color:var(--mix)}}
.cellref{{font-size:12px;color:var(--ink3)}} .offm{{font-size:11.5px;border:1px dashed var(--ink3);color:var(--ink3);padding:0 6px;border-radius:6px}}
.basis{{font-size:12.5px;color:var(--ink3);margin-top:4px}}
.lnk a,.thr a{{color:inherit;text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:3px}}
.lnk li{{margin:2px 0}} .lnk ul{{margin:0;padding-left:18px}}
.t.thread{{background:transparent;border:1px solid var(--macro);color:var(--macro)}} a.t{{text-decoration:none}}
.thr{{margin-bottom:12px}} .thr h3{{font-size:16px;margin:0 0 4px}} .thr .st{{font-size:14px;margin:6px 0}} .thr .nx{{font-size:13.5px;color:var(--ink2)}}
.tl{{list-style:none;margin:10px 0 0;padding:0 0 0 14px;border-left:2px solid var(--line)}} .tl li{{position:relative;overflow-wrap:anywhere;font-size:13.5px;margin:4px 0;color:var(--ink2)}}
.tl li::before{{content:"";position:absolute;left:-19px;top:8px;width:8px;height:8px;border-radius:50%;background:var(--line)}}
.tl li.good::before{{background:var(--good)}} .tl li.bad::before{{background:var(--bad)}} .tl li.mix::before{{background:var(--mix)}}
.tl li.now{{color:var(--ink);font-weight:500}} .tl .dt{{color:var(--ink3);display:inline-block;min-width:40px}}
.upd{{font-size:11.5px;background:var(--ink);color:var(--bg);padding:1px 7px;border-radius:999px;margin-left:6px;vertical-align:2px}}
.ev:target,.thr:target{{outline:2px solid var(--mix);outline-offset:4px;border-radius:8px}}
details.xp{{margin-top:10px;border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:var(--bg)}} details.xp summary{{cursor:pointer;font-size:13.5px;font-weight:500}}
.xsec{{margin-top:12px}} .xs{{font-size:14px;margin:10px 0 0}} .gate-x{{margin:8px 0 4px}} .gate-tb{{margin:8px 0 0 18px}}
table.xt{{font-size:13px}} table.xt td{{white-space:normal;text-align:left;vertical-align:top}} table.xt th{{text-align:left}}
.pc-wrap{{position:relative}} svg.pc{{width:100%;height:auto;display:block;overflow:visible}}
svg.pc .grid line{{stroke:var(--line);stroke-width:1}} svg.pc text{{fill:var(--ink3);font-size:11px;font-family:inherit}}
svg.pc .ln{{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}} svg.pc .bench{{stroke:var(--bench);stroke-dasharray:4 3;stroke-width:1.5}}
svg.pc .dot{{stroke:var(--card);stroke-width:2}} svg.pc .xh{{stroke:var(--ink3);stroke-width:1;stroke-dasharray:2 3}}
svg.pc text.end{{fill:var(--ink);font-weight:600;font-size:12px}}
.pc-tip{{position:absolute;pointer-events:none;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:12.5px;box-shadow:0 4px 14px rgba(0,0,0,.12);display:none;min-width:170px;z-index:4}}
.pc-tip .r{{display:flex;justify-content:space-between;gap:12px}} .pc-legend{{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;margin:4px 0 8px}}
.lg-bench::before{{content:"";display:inline-block;width:14px;border-top:2px dashed var(--bench);margin-right:5px;vertical-align:3px}}
.chg.up{{color:var(--good)}} .chg.down{{color:var(--bad)}} .chg.flat{{color:var(--ink3)}}
svg.pc .tga{{stroke:var(--macro);stroke-width:1.6}} svg.pc .period{{fill:var(--hl)}} svg.pc text.pl{{fill:var(--ink2);font-size:11px}} svg.pc text.halo{{paint-order:stroke;stroke:var(--card);stroke-width:4px;stroke-linejoin:round}}
svg.pc .plan-band{{fill:var(--mixbg);stroke:var(--mix);stroke-dasharray:3 3;stroke-width:1}} svg.pc .plan-pt{{fill:var(--card);stroke:var(--mix);stroke-width:2}}
.lg-tga::before{{content:"";display:inline-block;width:14px;border-top:2px solid var(--macro);margin-right:5px;vertical-align:3px}}
.lg-plan::before{{content:"";display:inline-block;width:10px;height:10px;border:2px solid var(--mix);border-radius:50%;margin-right:5px;vertical-align:-1px}}
.wk-tga{{font-size:12.5px;color:var(--ink2);margin:-4px 0 8px}}
.wk-price{{font-size:12.5px;color:var(--ink2);margin:-2px 0 8px;display:flex;gap:12px;flex-wrap:wrap}}
table.pt td,table.pt th{{text-align:right}} table.pt td:first-child,table.pt th:first-child{{text-align:left}}
details.tlwrap summary{{cursor:pointer;font-size:13px;color:var(--ink3);margin-top:8px}}
.pf{{display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 10px}} .pf button{{font:inherit;font-size:13px;padding:3px 11px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}}
.pf button.on{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
table.peer td,table.peer th{{font-size:13px;padding:9px 6px}} table.peer td.num{{text-align:right;min-width:92px}} table.peer td.num b,table.peer .nw{{white-space:nowrap}} table.peer td.who{{min-width:170px;max-width:280px}} table.peer tr.self td{{background:var(--hl)}}
table.peer .co{{font-weight:700;white-space:nowrap}} table.peer .src a{{color:var(--ink3);font-size:12px;margin-right:6px}}
.t.new{{background:var(--ink);color:var(--bg)}}
</style>
</head>
<body>
<div class="wrap">
<h1>{tks} 주간 이벤트</h1>
<p class="sub">{period} 주 단위 정리 · 생성일 {today} · 마지막 시스템 점검 {last_check} · 원장 갱신 {updated}</p>
<div class="grid3" id="status"></div>
<div class="callout"><b>지금 가장 중요한 한 줄:</b> {headline}</div>
{stale}
<h2>읽는 법</h2>
<div class="card howto">
<div><b>🟡 → 🔴🔴 (시그널 등급)</b><p>🟡는 '지켜보는 중', 🔴🔴는 '손절 조건이 걸렸으니 최우선으로 다시 볼 것'입니다. 시스템은 후보만 내고, 확정은 사람이 합니다.</p></div>
<div><b>상향 게이트 (등급을 올리는 조건)</b><p>세 가지가 <u>동시에</u> 맞아야 합니다. ① 숫자로 확인됐다 ② 그 회사만의 일이다 ③ 실제 매출로 장부에 잡혔다. 계약·가격표·발표만으로는 올라가지 않습니다.</p></div>
<div><b>노출 매트릭스 (무엇에 흔들리나)</b><p>각 종목이 금리·AI 투자·전력 같은 외부 요인이 바뀔 때 어느 쪽으로 움직이기 쉬운지 표시한 지도입니다.</p></div>
</div>
<h2>노출 매트릭스 — 무엇이 이 종목들을 움직이나</h2>
<div class="card"><div class="tblwrap"><table><thead><tr><th>종목</th>{exp_head}</tr></thead><tbody>{exp_body}</tbody></table></div>
<div class="legend">"크게" = 영향 강함 · 표시 없음 = 중간 · — = 해당 없음. 이번 🔴🔴를 만든 '금리·자금조달' 칸은 세 종목 모두 '오르면 ↓'이고, 빚을 가장 많이 쓰는 쪽이 가장 민감합니다.</div>
{week_exp}</div>
<h2>다가오는 일정 — 등급이 바뀔 수 있는 관문</h2>
<div class="card" id="upcoming"></div>
<h2>추적 중인 이야기 — 과거 소식과 이번 주를 잇는 흐름</h2>
<p class="sub" style="margin-top:-4px">여러 주에 걸쳐 이어지는 사건을 묶었습니다. 이번 주에 새 소식이 붙은 이야기가 위에 옵니다. 항목을 누르면 해당 주의 소식으로 이동합니다.</p>
<div id="threads"></div>
<h2>업계 AI 계약 비교 — 채굴사 출신 데이터센터 (최근 계약이 위)</h2>
<p class="sub" style="margin-top:-4px">비트코인 채굴에서 AI 데이터센터로 옮겨 간 회사들이 빅테크·AI 연구소와 맺은 계약입니다. IREN 계약이 업계 조건과 비교해 어디쯤인지 보려는 참고 표이며, 시스템 판정에는 쓰지 않습니다.</p>
<div class="card" id="peers"></div>
<h2>주당 매출·ARR 추이 — 매출이 주식 수보다 빨리 느는가</h2>
<p class="sub" style="margin-top:-4px">회사가 낸 매출·연환산 매출(ARR)을 주식 수로 나눈 값입니다. 주식이 늘어도 이 값이 오르면 매출이 희석보다 빠르게 늘고 있다는 뜻입니다(해석). 앞 숫자는 완전희석, 뒤 숫자는 발행 주식 기준이며 모두 계산값입니다.</p>
<div class="card" id="pershare"></div>
<h2>주간 주가 추이</h2>
<div class="card" id="prices"></div>
<h2>미국 재무부 현금(TGA) 잔고 추이</h2>
<p class="sub" style="margin-top:-4px">미국 재무부가 연준에 둔 통장(TGA, Treasury General Account)의 하루 마감 잔고입니다. 잔고가 늘면 그만큼 은행 시스템의 돈(지급준비금)이 재무부 통장으로 옮겨 가고, 줄면 다시 풀립니다. 세금이 들어오는 날(분기 중순 법인세·개인 세금 마감일)에는 늘고, 월초 지급일에는 줄어드는 날짜 패턴이 큽니다. 동그라미·띠는 재무부가 분기 국채 발행 계획에서 밝힌 잔고 가정으로, 약속이 아니라 국채를 얼마나 찍을지 계산하려고 쓴 전제입니다.</p>
<div class="card" id="tga"></div>
<h2>주별 이벤트 (최근 주부터)</h2>
<div class="filters" id="filters"><button data-f="all" class="on">전체</button>{filters}<button data-f="hide-rumor">2차 보도 숨기기</button></div>
<div id="weeks"></div>
<p class="foot">{disclaimer}<br>'2차 보도'는 회사 공시·공식 페이지로 확인되지 않은 언론·법무법인 보도로, 시스템이 단독 판단 근거로 쓰지 않는 자료입니다.<br>
'시스템 점검'·'등급 확정' 항목과 상향 게이트·노출 매트릭스는 점검 산출물에서 자동으로 옮긴 것이고, 나머지 설명은 사람이 읽기 쉽게 다시 쓴 요약입니다. 날짜 미발표 일정은 '예상'으로 표시했습니다.<br>
'매트릭스 영향'(유리 쪽·불리 쪽·관찰)과 '추적 중인 이야기'의 연결은 점검 산출물의 축 판정과 노출 매트릭스 정의를 바탕으로 정리한 해석이며, 시스템의 확정 판정이 아닙니다. 판정 근거가 있으면 '점검 판정'으로 따로 적었습니다.</p>
</div>
<script>
const DATA = {payload};
const effLabel = {{good:"좋은 쪽",bad:"나쁜 쪽",mix:"양면",neu:"중립·대기"}};
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
const tkSpan = x => `<span class="tk ${{esc(x)}}">${{esc(x)}}</span>`;
document.getElementById("status").innerHTML = DATA.status.map(s => `
 <div class="card status"><div>${{tkSpan(s.tk)}}</div><div class="big">${{esc(s.sig)}}</div><div class="meta">${{esc(s.since)}}</div>
 <div class="gate">${{s.gate.map(([n,ok]) => `<span class="g ${{ok?"ok":"no"}}">${{ok===true?"✓":ok===false?"✗":"?"}} ${{esc(n)}}</span>`).join("")}}</div>
 <div class="meta" style="font-size:12.5px">상향 게이트 (${{esc(s.gate_asof)}} 점검 기준)</div>
 ${{s.next?`<div class="next">${{esc(s.next)}}</div>`:""}}</div>`).join("");
document.getElementById("upcoming").innerHTML = DATA.upcoming.length ? DATA.upcoming.map(u => `
 <div class="ev"><div class="d">${{esc(u.dt)}}</div><div class="who">${{String(u.tk).split("·").map(tkSpan).join("<br>")}}</div>
 <div class="body"><p><b>${{esc(u.title)}}</b></p><p class="why">${{esc(u.why)}}</p></div></div>`).join("") : `<div class="empty">등록된 일정이 없습니다.</div>`;
function render(f) {{
 document.getElementById("weeks").innerHTML = DATA.weeks.map(w => {{
  const items = w.items.filter(it => f==="hide-rumor" ? !it.rumor : f==="all" || it.tk===f || it.tk==="공통");
  const body = items.length ? items.map(it => {{
   const tags = [];
   if (it.eff && it.kind!=="system") tags.push(`<span class="t ${{it.eff}}">${{effLabel[it.eff]}}</span>`);
   if (it.axis) tags.push(`<span class="t">노출: ${{esc(it.axis)}}</span>`);
   if (it.rumor) tags.push(`<span class="t rumor">2차 보도</span>`);
   if (it.kind==="system") tags.push(`<span class="t sys">시스템 점검</span>`);
   if (it.kind==="decision") tags.push(`<span class="t sys">확정·결정</span>`);
   (it.threads||[]).forEach(t => tags.push(`<a class="t thread" href="#${{esc(t.id)}}">이야기: ${{esc(t.title)}}</a>`));
   return `<div class="ev ${{it.kind||""}}"${{it.id?` id="ev-${{esc(it.id)}}"`:""}}><div class="d">${{esc(it.dt)}}</div><div class="who">${{tkSpan(it.tk)}}</div>
    <div class="body"><p>${{esc(it.text)}}</p>${{it.why?`<p class="why">${{esc(it.why)}}</p>`:""}}${{extra(it)}}${{tags.length?`<div class="tags">${{tags.join("")}}</div>`:""}}</div></div>`;
  }}).join("") : `<div class="empty">${{w.now ? "이번 주에 기록된 소식이 아직 없습니다." : "이 주에는 해당 소식이 없습니다."}}</div>`;
  return `<div class="card week"><div class="wk-h"><span class="wk-date">${{esc(w.d)}}</span><span class="wk-title">${{esc(w.title)}}</span>${{w.now?'<span class="wk-now">이번 주</span>':""}}</div>${{priceLine(w)}}${{tgaLine(w)}}${{body}}</div>`;
 }}).join("");
 renderThreads(f);
}}
const dirLabel = {{up:"유리 쪽",down:"불리 쪽",watch:"관찰"}};
function extra(it) {{
 let h = "";
 if (it.detail && it.detail.length) h += `<ul class="detail">${{it.detail.map(d => `<li>${{esc(d)}}</li>`).join("")}}</ul>`;
 if (it.exposure && it.exposure.length) {{
  h += `<div class="sec"><div class="sec-h">노출 매트릭스 영향</div>` + it.exposure.map(x => `<div class="exrow">${{tkSpan(x.tk)}}<span>· ${{esc(x.axis)}}</span>
   <span class="exk ${{esc(x.dir)}}">${{dirLabel[x.dir]||esc(x.dir)}}</span>
   ${{x.in_matrix ? `<span class="cellref">(매트릭스: ${{esc(x.cell)}})</span>` : `<span class="offm">매트릭스 밖</span>`}}
   <span>${{esc(x.note)}}</span></div>`).join("") + (it.basis?`<div class="basis">${{esc(it.basis)}}</div>`:"") + `</div>`;
 }}
 if (it.links && it.links.length) {{
  h += `<div class="sec lnk"><div class="sec-h">관련 과거 소식</div><ul>` + it.links.map(l => `<li><a href="#ev-${{esc(l.id)}}">${{esc(l.dt)}} ${{esc(l.tk)}} — ${{esc(l.text)}}</a>${{l.why?` <span class="why">· ${{esc(l.why)}}</span>`:""}}</li>`).join("") + `</ul></div>`;
 }}
 return h;
}}
function explainer(t) {{
 const x = t.explainer; if (!x) return "";
 const tbl = (head, rows) => `<div class="tblwrap"><table class="xt"><thead><tr>${{head.map(h=>`<th>${{esc(h)}}</th>`).join("")}}</tr></thead><tbody>${{rows.map(r=>`<tr>${{r.map(c=>`<td>${{esc(c)}}</td>`).join("")}}</tr>`).join("")}}</tbody></table></div>`;
 let h = `<details class="xp" open><summary>자세히 보기 — 관문·경로·영향 (${{esc(x.asof)}} 점검 기준${{t.explainer_stale?" · <b>새 소식 반영 전</b>":""}})</summary>`;
 if (x.summary) h += `<p class="xs"><b>한 줄 답:</b> ${{esc(x.summary)}}</p>`;
 if (x.context) h += `<div class="xsec"><div class="sec-h">${{esc(x.context.title)}}</div>${{tbl(x.context.head||["구분","규모","비고"], x.context.rows)}}${{x.context.note?`<p class="small">${{esc(x.context.note)}}</p>`:""}}</div>`;
 if (x.tables && x.tables.length) h += x.tables.map(tb => `<div class="xsec"><div class="sec-h">${{esc(tb.title)}}${{tb.asof?` <span class="small" style="font-weight:400">(${{esc(tb.asof)}} 확인${{(t.stale_tables||[]).includes(tb.id)?" · <b>이번 주 재확인 전</b>":""}})</span>`:""}}</div>${{tbl(tb.head, tb.rows)}}${{tb.note?`<p class="small">${{esc(tb.note)}}</p>`:""}}</div>`).join("");
 if (x.gates && x.gates.length) h += `<div class="xsec"><div class="sec-h">관문별 상태</div>` + x.gates.map(g => `<div class="gate-x"><div><b>${{esc(g.name)}}</b> <span class="exk ${{esc(g.dir||"watch")}}">${{esc(g.state)}}</span></div><ul class="detail">${{(g.points||[]).map(p=>`<li>${{esc(p)}}</li>`).join("")}}</ul>${{(g.tables||[]).map(tb => `<div class="gate-tb">${{tb.title?`<div class="small"><b>${{esc(tb.title)}}</b></div>`:""}}${{tbl(tb.head, tb.rows)}}${{tb.note?`<p class="small">${{esc(tb.note)}}</p>`:""}}</div>`).join("")}}</div>`).join("") + `</div>`;
 if (x.scenarios) h += `<div class="xsec"><div class="sec-h">${{esc(x.scenarios.title||"나빠지는 경로별")}}</div>${{tbl(x.scenarios.head||["경우","지금까지 관측","판단"], x.scenarios.rows)}}${{x.scenarios.conclusion?`<p class="xs"><b>정리:</b> ${{esc(x.scenarios.conclusion)}}</p>`:""}}</div>`;
 if (x.impact && x.impact.length) h += `<div class="xsec"><div class="sec-h">무엇에 영향이 가나</div><ul class="detail">${{x.impact.map(([k,v])=>`<li><b>${{esc(k)}}:</b> ${{esc(v)}}</li>`).join("")}}</ul></div>`;
 if (x.watch && x.watch.length) h += `<div class="xsec"><div class="sec-h">언제 알 수 있나</div><ul class="detail">${{x.watch.map(([k,v])=>`<li><b>${{esc(k)}}</b> — ${{esc(v)}}</li>`).join("")}}</ul></div>`;
 if (x.caveats && x.caveats.length) h += `<div class="xsec"><div class="sec-h">확인이 덜 된 부분</div><ul class="detail small">${{x.caveats.map(c=>`<li>${{esc(c)}}</li>`).join("")}}</ul></div>`;
 return h + `</details>`;
}}
const arrow = c => c==null ? "" : c>0 ? "▲" : c<0 ? "▼" : "–";
const chgCls = c => c==null ? "flat" : c>0 ? "up" : c<0 ? "down" : "flat";
const fmtChg = c => c==null ? "—" : `${{arrow(c)}} ${{Math.abs(c).toFixed(1)}}%`;
const fmtPx = v => v>=100 ? v.toFixed(2) : v.toFixed(2);
function priceLine(w) {{
 if (!w.price || !Object.keys(w.price).length || !DATA.prices) return "";
 const ts = DATA.prices.tickers, b = DATA.prices.bench;
 const part = t => w.price[t] ? `<span>${{t===b?`<span class="lg-bench"></span>비교 ${{esc(t)}}`:tkSpan(t)}} $${{fmtPx(w.price[t].close)}} <span class="chg ${{chgCls(w.price[t].chg)}}">${{fmtChg(w.price[t].chg)}}</span>${{w.price[t].prov?" (잠정)":""}}</span>` : "";
 return `<div class="wk-price"><span class="small">주가(주간 종가·전주 대비${{w.now?", 진행 중인 주":""}}):</span>${{[...ts, b].map(part).join("")}}</div>`;
}}
function renderPrices() {{
 const P = DATA.prices, el = document.getElementById("prices");
 if (!P || !P.weeks.length) {{ el.innerHTML = `<div class="empty">주가 데이터가 없습니다 (--update-prices로 수집).</div>`; return; }}
 const ts = P.tickers, b = P.bench, all = [...ts, b], W = P.weeks;
 const css = getComputedStyle(document.documentElement);
 const col = t => t===b ? css.getPropertyValue("--bench").trim() : css.getPropertyValue("--"+t).trim();
 const vals = W.flatMap(w => all.map(t => w.v[t] && w.v[t].idx)).filter(v => v!=null);
 let lo = Math.min(...vals, 100), hi = Math.max(...vals, 100); const pad = (hi-lo)*0.08; lo -= pad; hi += pad;
 const w0 = 640, h0 = 260, ml = 40, mr = 70, mt = 12, mb = 28, iw = w0-ml-mr, ih = h0-mt-mb;
 const x = i => ml + (W.length===1 ? iw/2 : i*iw/(W.length-1)), y = v => mt + (hi-v)/(hi-lo)*ih;
 const step = (hi-lo) > 60 ? 20 : 10, ticks = [];
 for (let v = Math.ceil(lo/step)*step; v <= hi; v += step) ticks.push(v);
 let g = `<g class="grid">${{ticks.map(v => `<line x1="${{ml}}" x2="${{ml+iw}}" y1="${{y(v)}}" y2="${{y(v)}}"/><text x="${{ml-6}}" y="${{y(v)+4}}" text-anchor="end">${{v}}</text>`).join("")}}</g>`;
 g += `<line x1="${{ml}}" x2="${{ml+iw}}" y1="${{y(100)}}" y2="${{y(100)}}" stroke="var(--ink3)" stroke-width="1"/>`;
 g += W.map((w,i) => (i%2===0||i===W.length-1) ? `<text x="${{x(i)}}" y="${{h0-8}}" text-anchor="middle">${{esc(w.label.split("~")[0])}}</text>` : "").join("");
 const lines = all.map(t => {{
  const pts = W.map((w,i) => w.v[t] && w.v[t].idx!=null ? [x(i), y(w.v[t].idx)] : null).filter(Boolean);
  if (!pts.length) return "";
  const d = pts.map((p,i) => (i?"L":"M")+p[0].toFixed(1)+" "+p[1].toFixed(1)).join(" ");
  const last = pts[pts.length-1], lw = [...W].reverse().find(w => w.v[t]);
  return `<path class="ln ${{t===b?"bench":""}}" d="${{d}}" style="stroke:${{col(t)}}"/>` +
   (t===b ? "" : `<circle class="dot" cx="${{last[0]}}" cy="${{last[1]}}" r="4" style="fill:${{col(t)}}"/>`) +
   `<text class="end" x="${{last[0]+8}}" y="${{last[1]+4}}">${{esc(t)}} ${{lw.v[t].idx.toFixed(0)}}</text>`;
 }}).join("");
 const first = W[0], lastW = W[W.length-1];
 const legend = `<div class="pc-legend">${{ts.map(t => tkSpan(t)).join("")}}<span class="lg-bench">${{esc(b)}} (나스닥100 ETF, 비교용)</span></div>`;
 const svg = `<div class="pc-wrap"><svg class="pc" viewBox="0 0 ${{w0}} ${{h0}}" role="img" aria-label="주간 종가 지수 추이(${{esc(first.label)}} 주 = 100)">${{g}}${{lines}}<line class="xh" id="pcx" y1="${{mt}}" y2="${{mt+ih}}" style="display:none"/><rect id="pchit" x="${{ml}}" y="${{mt}}" width="${{iw}}" height="${{ih}}" fill="transparent"/></svg><div class="pc-tip" id="pctip"></div></div>`;
 const rows = [...W].reverse().map(w => `<tr><td>${{esc(w.label)}}${{w.now?" (진행 중)":""}}</td>${{all.map(t => w.v[t] ? `<td>$${{fmtPx(w.v[t].close)}}${{w.v[t].prov?"*":""}}</td><td class="chg ${{chgCls(w.v[t].chg)}}">${{fmtChg(w.v[t].chg)}}</td>` : "<td>—</td><td>—</td>").join("")}}</tr>`).join("");
 const table = `<details class="xp" style="margin-top:12px"><summary>표로 보기 — 주별 종가·전주 대비</summary><div class="tblwrap"><table class="pt xt"><thead><tr><th>주</th>${{all.map(t => `<th>${{esc(t)}} 종가</th><th>등락</th>`).join("")}}</tr></thead><tbody>${{rows}}</tbody></table></div></details>`;
 el.innerHTML = `<p class="small" style="margin:0 0 6px">${{esc(first.label)}} 주 종가를 100으로 맞춘 지수입니다(세 종목의 주가 수준이 달라 직접 비교하려고 맞춤). 점선은 비교용 나스닥100. 마지막 값: ${{esc(lastW.label)}} ${{Object.values(lastW.v).some(v=>v.prov)?"— 일부 잠정(*)":""}}</p>` + legend + svg + table +
  `<p class="small" style="margin:8px 0 0">출처: ${{esc(P.source)}} · 수집 ${{esc(P.as_of)}}. 주가는 같은 주의 소식과 나란히 놓았을 뿐, 소식이 주가를 움직였다는 뜻은 아닙니다.</p>`;
 const hit = document.getElementById("pchit"), xh = document.getElementById("pcx"), tip = document.getElementById("pctip"), svgEl = el.querySelector("svg");
 hit.addEventListener("mousemove", ev => {{
  const pt = svgEl.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
  const lp = pt.matrixTransform(svgEl.getScreenCTM().inverse());
  const i = Math.max(0, Math.min(W.length-1, Math.round((lp.x-ml)/(iw/Math.max(1,W.length-1)))));
  const w = W[i]; xh.setAttribute("x1", x(i)); xh.setAttribute("x2", x(i)); xh.style.display = "";
  tip.innerHTML = `<b>${{esc(w.label)}}${{w.now?" (진행 중)":""}}</b>` + all.filter(t => w.v[t]).map(t => `<div class="r"><span>${{t===b?`<span class="lg-bench"></span>${{esc(t)}}`:tkSpan(t)}}</span><span>$${{fmtPx(w.v[t].close)}} <span class="chg ${{chgCls(w.v[t].chg)}}">${{fmtChg(w.v[t].chg)}}</span></span></div>`).join("");
  tip.style.display = "block";
  const box = el.querySelector(".pc-wrap").getBoundingClientRect(), px = ev.clientX - box.left;
  tip.style.left = (px > box.width/2 ? px - tip.offsetWidth - 14 : px + 14) + "px"; tip.style.top = "8px";
 }});
 hit.addEventListener("mouseleave", () => {{ tip.style.display = "none"; xh.style.display = "none"; }});
}}
renderPrices();
const eokS = v => {{ if (v==null) return "—"; const e = Math.round(Math.abs(v)*10), j = Math.floor(e/10000), r = e%10000;
 return j ? `${{j}}조${{r?" "+r.toLocaleString()+"억":""}}` : `${{r.toLocaleString()}}억`; }};
const eok = v => v==null ? "—" : `${{eokS(v)}} 달러`;
const eokChg = v => v==null ? "—" : `${{v>0?"▲":v<0?"▼":"–"}} ${{eokS(v)}}`;
const mdj = d => {{ const [, m, dd] = d.split("-"); return `${{+m}}/${{+dd}}`; }};
function tgaLine(w) {{
 if (!w.tga) return "";
 return `<div class="wk-tga"><span class="small">재무부 현금(TGA):</span> ${{eok(w.tga.close)}} (${{esc(w.tga.last)}} 마감) · 전주 대비 ${{eokChg(w.tga.chg)}}</div>`;
}}
function renderTGA() {{
 const T = DATA.tga, el = document.getElementById("tga");
 if (!T || !T.daily.length) {{ el.innerHTML = `<div class="empty">TGA 데이터가 없습니다 (--update-tga로 수집).</div>`; return; }}
 const D = T.daily, P = T.plan || [], W = T.weeks, L = D[D.length-1];
 const ts = d => Date.parse(d + "T00:00:00Z");
 const t0 = ts(D[0][0]), t1 = Math.max(ts(L[0]), ...P.map(p => ts(p.to || p.date)));
 const vals = D.map(r => r[1]).concat(P.flatMap(p => [p.value + (p.band||0), p.value - (p.band||0)]));
 let lo = Math.min(...vals), hi = Math.max(...vals); const pad = (hi-lo)*0.1; lo -= pad; hi += pad;
 const w0 = 640, h0 = 260, ml = 52, mr = 18, mt = 14, mb = 28, iw = w0-ml-mr, ih = h0-mt-mb;
 const x = d => ml + (ts(d)-t0)/(t1-t0)*iw, y = v => mt + (hi-v)/(hi-lo)*ih;
 const ticks = []; for (let v = Math.ceil(lo/100)*100; v <= hi; v += 100) ticks.push(v);
 let g = `<g class="grid">${{ticks.map(v => `<line x1="${{ml}}" x2="${{ml+iw}}" y1="${{y(v)}}" y2="${{y(v)}}"/><text x="${{ml-6}}" y="${{y(v)+4}}" text-anchor="end">${{eokS(v)}}</text>`).join("")}}</g>`;
 const months = [];
 {{ const d0 = new Date(t0); let m = new Date(Date.UTC(d0.getUTCFullYear(), d0.getUTCMonth()+1, 1));
   while (m.getTime() <= t1) {{ months.push(m.toISOString().slice(0,10)); m = new Date(Date.UTC(m.getUTCFullYear(), m.getUTCMonth()+1, 1)); }} }}
 g += months.map((m,i) => i%2===0 ? `<text x="${{x(m)}}" y="${{h0-8}}" text-anchor="middle">${{m.slice(2,4)}}.${{+m.slice(5,7)}}</text>` : "").join("");
 if (W.length) {{ const a = x(W[0].w), b = x(L[0]);
  g = `<rect class="period" x="${{a}}" y="${{mt}}" width="${{Math.max(0,b-a)}}" height="${{ih}}"/><text class="pl" x="${{a+4}}" y="${{h0-mb-6}}">이 페이지 기간</text>` + g; }}
 const plan = P.map(p => p.date
  ? `<circle class="plan-pt" cx="${{x(p.date)}}" cy="${{y(p.value)}}" r="5"/><text class="pl halo" x="${{x(p.date)}}" y="${{y(p.value)+(p.value>L[1]?-10:18)}}" text-anchor="${{x(p.date)>ml+iw-60?"end":"middle"}}">${{esc(p.short||p.label)}}</text>`
  : `<rect class="plan-band" x="${{x(p.from)}}" y="${{y(p.value+(p.band||0))}}" width="${{Math.max(3,x(p.to)-x(p.from))}}" height="${{Math.max(3,y(p.value-(p.band||0))-y(p.value+(p.band||0)))}}"/><text class="pl" x="${{(x(p.from)+x(p.to))/2}}" y="${{y(p.value+(p.band||0))-6}}" text-anchor="middle">${{esc(p.short||p.label)}}</text>`).join("");
 const path = D.map((r,i) => (i?"L":"M")+x(r[0]).toFixed(1)+" "+y(r[1]).toFixed(1)).join(" ");
 const line = `<path class="ln tga" d="${{path}}"/><circle class="dot" cx="${{x(L[0])}}" cy="${{y(L[1])}}" r="4" style="fill:var(--macro)"/>` +
  `<text class="end halo" x="${{x(L[0])-8}}" y="${{y(L[1])+(L[1]>(lo+hi)/2?24:-12)}}" text-anchor="end">${{mdj(L[0])}} ${{eokS(L[1])}}</text>`;
 const svg = `<div class="pc-wrap"><svg class="pc" viewBox="0 0 ${{w0}} ${{h0}}" role="img" aria-label="재무부 현금 잔고 일별 추이(최근 1년)와 재무부 계획 가정">${{g}}${{plan}}${{line}}<line class="xh" id="tgx" y1="${{mt}}" y2="${{mt+ih}}" style="display:none"/><rect id="tghit" x="${{ml}}" y="${{mt}}" width="${{iw}}" height="${{ih}}" fill="transparent"/></svg><div class="pc-tip" id="tgtip"></div></div>`;
 const legend = `<div class="pc-legend"><span class="lg-tga">하루 마감 잔고</span>${{P.length?`<span class="lg-plan">재무부 계획 가정 (띠 = 예상 범위)</span>`:""}}</div>`;
 const src = p => p.url ? `<a href="${{esc(p.url)}}" target="_blank" rel="noopener">${{esc(p.src||"출처")}}</a>` : esc(p.src||"");
 const ptable = P.length ? `<div class="xsec"><div class="sec-h">재무부 계획 가정과 실제</div><div class="tblwrap"><table class="xt"><thead><tr><th>계획</th><th>시점</th><th>재무부 가정</th><th>실제</th><th>차이</th><th>상태</th><th>출처</th></tr></thead><tbody>` +
  P.map(p => `<tr><td>${{esc(p.label)}}</td><td>${{p.date?mdj(p.date):`${{mdj(p.from)}}~${{mdj(p.to)}}`}}</td><td>${{eok(p.value)}}${{p.band?`<div class="small">±${{eokS(p.band)}}</div>`:""}}</td>` +
   `<td>${{p.actual!=null?`${{eok(p.actual)}}<div class="small">${{mdj(p.actual_d)}} ${{p.date?"마감":"까지 최고"}}</div>`:"—"}}</td><td>${{p.gap!=null?eokChg(p.gap):"—"}}</td><td>${{esc(p.state)}}</td><td class="small">${{src(p)}}</td></tr>`).join("") +
  `</tbody></table></div>${{T.plan_note?`<p class="small">${{esc(T.plan_note)}}</p>`:""}}</div>` : "";
 const wrows = [...W].reverse().map(w => `<tr><td>${{esc(w.label)}}${{w.now?" (진행 중)":""}}</td><td><b>${{eok(w.close)}}</b><div class="small">${{esc(w.last)}} 마감</div></td><td>${{eokChg(w.chg)}}</td><td>${{eokS(w.lo)}} ~ ${{eokS(w.hi)}}</td><td>${{eokS(w.dep)}}</td><td>${{eokS(w.wd)}}</td></tr>`).join("");
 const wtable = `<div class="xsec"><div class="sec-h">주별 잔고 (최근 주부터)</div><div class="tblwrap"><table class="xt"><thead><tr><th>주</th><th>주말 잔고</th><th>전주 대비</th><th>주중 최저~최고</th><th>들어온 돈 합계</th><th>나간 돈 합계</th></tr></thead><tbody>${{wrows}}</tbody></table></div>` +
  `<p class="small">'들어온 돈'에는 세금뿐 아니라 국채를 팔아 받은 돈이, '나간 돈'에는 정부 지출과 만기 국채 상환이 함께 들어 있습니다. 그래서 두 합계는 매우 크고, 둘의 차이만큼 잔고가 바뀝니다.</p></div>`;
 el.innerHTML = `<p class="small" style="margin:0 0 6px">최근 1년 하루 마감 잔고입니다. 노란 바탕은 이 페이지가 다루는 기간입니다. 마지막 값: ${{mdj(L[0])}} ${{eok(L[1])}} (재무부는 다음 영업일 오후에 공표합니다).</p>` + legend + svg + ptable + wtable +
  `<p class="small" style="margin:8px 0 0">출처: ${{esc(T.source)}} · 수집 ${{esc(T.as_of)}}. 이 잔고는 주가와 나란히 놓았을 뿐, 잔고 변화가 주가를 움직였다는 뜻은 아닙니다.</p>`;
 const hit = document.getElementById("tghit"), xh = document.getElementById("tgx"), tip = document.getElementById("tgtip"), svgEl = el.querySelector("svg");
 const xs = D.map(r => x(r[0]));
 hit.addEventListener("mousemove", ev => {{
  const pt = svgEl.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
  const lx = pt.matrixTransform(svgEl.getScreenCTM().inverse()).x;
  let i = 0; for (let k = 1; k < xs.length; k++) if (Math.abs(xs[k]-lx) < Math.abs(xs[i]-lx)) i = k;
  const r = D[i], pr = D[i-1];
  xh.setAttribute("x1", xs[i]); xh.setAttribute("x2", xs[i]); xh.style.display = "";
  tip.innerHTML = `<b>${{esc(r[0])}}</b><div class="r"><span>마감 잔고</span><span>${{eok(r[1])}}</span></div>` +
   (pr ? `<div class="r"><span>전날 대비</span><span>${{eokChg(r[1]-pr[1])}}</span></div>` : "") +
   (r[2]!=null ? `<div class="r"><span>들어온 돈</span><span>${{eok(r[2])}}</span></div><div class="r"><span>나간 돈</span><span>${{eok(r[3])}}</span></div>` : "");
  tip.style.display = "block";
  const box = el.querySelector(".pc-wrap").getBoundingClientRect(), px = ev.clientX - box.left;
  tip.style.left = (px > box.width/2 ? px - tip.offsetWidth - 14 : px + 14) + "px"; tip.style.top = "8px";
 }});
 hit.addEventListener("mouseleave", () => {{ tip.style.display = "none"; xh.style.display = "none"; }});
}}
renderTGA();
let peerCo = "all";
function renderPeers() {{
 const P = DATA.peers, el = document.getElementById("peers");
 if (!P || !P.contracts.length) {{ el.innerHTML = `<div class="empty">업계 계약 자료가 없습니다 (state/peer_contracts.json).</div>`; return; }}
 const cos = [...new Set(P.contracts.map(c => c.co))];
 const self = new Set(DATA.status.map(s => s.tk));
 const money = v => v==null ? "—" : `$${{v>=10?v.toFixed(1):v.toFixed(2).replace(/0$/,"")}}B`;
 const srcs = s => (s||[]).map(x => `<a href="${{esc(x.u)}}" target="_blank" rel="noopener">${{esc(x.t)}}</a>`).join("");
 const show = c => peerCo==="all" || c.co===peerCo;
 const rows = P.contracts.filter(show).map(c => {{
  const u = c.unit, mw = c.it_mw ? `${{c.it_mw.toLocaleString()}}MW` : (c.gross_mw ? `전체 ${{c.gross_mw.toLocaleString()}}MW` : "비공개");
  const who = [c.tenant, c.end_user?`실사용 ${{c.end_user}}`:"", c.backstop?`보증 ${{c.backstop}}`:""].filter(Boolean).join(" · ");
  const tags = (c.recent?`<span class="t new">최근 30일</span> `:"") + (c.rumor?`<span class="t rumor">2차 보도</span>`:"");
  const esc_ = c.esc_pct!=null ? ` · 연 ${{c.esc_pct}}% 인상` : "";
  return `<tr class="${{self.has(c.co)?"self":""}}"><td class="nw">${{esc(c.date)}}${{c.signed?`<div class="small">${{esc(c.signed)}}</div>`:""}}</td>
   <td><span class="co">${{esc(c.co_name)}}</span><div class="small">${{esc(c.site)}}</div></td>
   <td class="who">${{esc(who)}}<div class="small">${{esc(c.kind)}}${{c.note?" — "+esc(c.note):""}}</div>${{tags?`<div>${{tags}}</div>`:""}}</td>
   <td class="num"><b>${{mw}}</b>${{c.it_mw&&c.gross_mw?`<div class="small">전체 ${{c.gross_mw}}MW</div>`:""}}</td>
   <td class="num"><b>${{money(c.value_b)}}</b><div class="small nw">${{c.years?c.years+"년":"기간 비공개"}}</div>${{c.ext?`<div class="small">연장 ${{esc(c.ext)}}</div>`:""}}${{c.value_note?`<div class="small">${{esc(c.value_note)}}</div>`:""}}</td>
   <td class="num">${{u?`<b>$${{u.mw_yr.toFixed(2)}}M</b>${{u.mw_yr_y1?`<div class="small nw">첫해 $${{u.mw_yr_y1.toFixed(2)}}M${{esc_}}</div>`:(esc_?`<div class="small">${{esc_.slice(3)}}</div>`:"")}}${{c.unit_note?`<div class="small">${{esc(c.unit_note)}}</div>`:""}}`:`—${{esc_?`<div class="small">${{esc_.slice(3)}}</div>`:""}}`}}</td>
   <td>${{esc(c.status||"")}}<div class="src">${{srcs(c.src)}}</div></td></tr>`;
 }}).join("");
 const frows = P.financing.filter(show).map(f => `<tr class="${{self.has(f.co)?"self":""}}"><td class="num">${{esc(f.date)}}</td><td><span class="co">${{esc(f.co_name)}}</span><div class="small">${{esc(f.target||"")}}</div></td>
   <td>${{esc(f.instrument)}}</td><td class="num">${{money(f.amount_b)}}</td><td class="num">${{esc(f.rate)}}</td><td class="num">${{esc(f.maturity||"")}}</td>
   <td>${{esc(f.note||"")}}<div class="src">${{srcs(f.src)}}</div></td></tr>`).join("");
 const btn = (k, label) => `<button data-co="${{esc(k)}}" class="${{peerCo===k?"on":""}}">${{esc(label)}}</button>`;
 el.innerHTML = `<div class="pf">${{btn("all","전체")}}${{cos.map(k => btn(k, P.companies[k]||k)).join("")}}</div>
  <div class="tblwrap"><table class="xt peer"><thead><tr><th>발표일</th><th>회사·캠퍼스</th><th>상대방·형태</th><th>용량(IT)</th><th>계약가치·기간</th><th>평균 단가<br><span class="small">MW·년당 $</span></th><th>진행·출처</th></tr></thead><tbody>${{rows}}</tbody></table></div>
  <details class="xp" style="margin-top:12px"><summary>자금 조달 조건 — 금액·금리·만기 (최근 순)</summary><div class="tblwrap"><table class="xt peer"><thead><tr><th>날짜</th><th>회사·대상</th><th>수단</th><th>금액</th><th>금리</th><th>만기</th><th>비고·출처</th></tr></thead><tbody>${{frows||'<tr><td colspan="7">해당 자료 없음</td></tr>'}}</tbody></table></div></details>
  <ul class="detail small">${{(P.note||[]).map(n => `<li>${{esc(n)}}</li>`).join("")}}</ul>
  <p class="small" style="margin:6px 0 0">자료 기준일 ${{esc(P.asof)}} · 노란 줄 = 이 페이지가 다루는 종목. 단가는 회사가 공개한 숫자로 계산한 값이며 회사가 밝힌 단가가 아닙니다.</p>`;
 el.querySelector(".pf").addEventListener("click", e => {{ const b = e.target.closest("button"); if (!b) return; peerCo = b.dataset.co; renderPeers(); }});
}}
renderPeers();
function renderPerShare() {{
 const P = DATA.per_share || {{}}, el = document.getElementById("pershare");
 const M = [["rev","주당 분기 매출<br><span class='small'>연환산</span>"],["arr_live","주당 가동 ARR"],["arr_contract","주당 계약 ARR"]];
 const amt = v => v==null ? "" : `$${{+(v/100).toFixed(2)}}억`;
 const sh = v => v==null ? "—" : `${{(v/100).toFixed(2)}}억 주`;
 const cell = v => !v ? `<td class="num">—</td>` : `<td class="num"><b>$${{v.lo.toFixed(2)}}~${{v.hi.toFixed(2)}}</b>${{v.chg==null?"":`<div class="small nw"><span class="chg ${{chgCls(v.chg)}}">${{fmtChg(v.chg)}}</span></div>`}}</td>`;
 const blocks = DATA.status.map(s => s.tk).map(tk => {{
  const rows = P[tk] || [];
  if (!rows.length) return `<div class="ps"><div class="sec-h">${{tkSpan(tk)}}</div><div class="empty">아직 입력 없음 — 다음 주간 갱신에서 작성</div></div>`;
  const body = rows.map(r => `<tr><td class="nw">${{esc(r.asof)}}<div class="small">${{esc(r.label||"")}}</div></td>
   ${{M.map(([k]) => cell(r.m[k])).join("")}}
   <td class="num">${{sh(r.sh_fd)}} / ${{sh(r.sh_basic)}}<div class="small">${{esc(r.sh_fd_asof||"")}} / ${{esc(r.sh_basic_asof||"")}}</div></td>
   <td class="small">${{[r.rev_q!=null?`${{esc(r.rev_q_period||"분기")}} 매출 ${{amt(r.rev_q)}}`:"", r.arr_live!=null?`가동 ARR ${{amt(r.arr_live)}}${{r.arr_live_asof?" ("+esc(r.arr_live_asof)+")":""}}`:"", r.arr_contract!=null?`계약 ARR ${{amt(r.arr_contract)}}`:""].filter(Boolean).join(" · ")}}${{r.src?`<div>${{esc(r.src)}}</div>`:""}}</td></tr>`).join("");
  return `<div class="ps"><div class="sec-h">${{tkSpan(tk)}}</div><div class="tblwrap"><table class="xt"><thead><tr><th>입력 시점</th>${{M.map(([,h]) => `<th>${{h}}</th>`).join("")}}<th>주식 수<br><span class="small">완전희석 / 발행</span></th><th>원본 숫자·출처</th></tr></thead><tbody>${{body}}</tbody></table></div></div>`;
 }}).join("");
 el.innerHTML = blocks + `<p class="small" style="margin:6px 0 0">변화율(▲▼)은 발행 주식 기준 직전 입력 대비입니다. ARR은 회계 기준 숫자가 아니며, 회사가 ARR을 공개하지 않으면 '—'입니다.</p>`;
}}
renderPerShare();
function renderThreads(f) {{
 const list = DATA.threads.filter(t => f==="all" || f==="hide-rumor" || t.tk===f || t.tk==="공통");
 document.getElementById("threads").innerHTML = list.map(t => {{
  const items = t.items.filter(i => f!=="hide-rumor" || !i.rumor);
  const recent = items.slice(-4), older = items.slice(0, -4);
  const li = i => `<li class="${{esc(i.eff)}} ${{i.now?"now":""}}"><a href="#ev-${{esc(i.id)}}"><span class="dt">${{esc(i.dt)}}</span> ${{i.tk!==t.tk?esc(i.tk)+" · ":""}}${{esc(i.text)}}</a>${{i.rumor?' <span class="small">(2차 보도)</span>':""}}</li>`;
  return `<div class="card thr" id="${{esc(t.id)}}"><h3>${{esc(t.title)}}${{t.updated?'<span class="upd">이번 주 업데이트</span>':""}}</h3>
   <div class="small">관련 매트릭스 축: ${{(t.axes||[]).map(esc).join(" · ")||"—"}} · 소식 ${{items.length}}건 · 마지막 ${{esc(t.last)}}</div>
   <p class="st"><b>지금 상태:</b> ${{esc(t.status)}}</p><p class="nx"><b>다음에 볼 것:</b> ${{esc(t.next)}}</p>
   ${{explainer(t)}}
   ${{older.length?`<details class="tlwrap"><summary>이전 소식 ${{older.length}}건 펼치기</summary><ul class="tl">${{older.map(li).join("")}}</ul></details>`:""}}
   <ul class="tl">${{recent.map(li).join("")}}</ul></div>`;
 }}).join("") || `<div class="empty">해당 종목의 추적 이야기가 없습니다.</div>`;
}}
let cur = "all";
render(cur);
document.getElementById("filters").addEventListener("click", e => {{
 const b = e.target.closest("button"); if (!b) return;
 document.querySelectorAll("#filters button").forEach(x => x.classList.toggle("on", x===b));
 cur = b.dataset.f; render(cur);
}});
document.addEventListener("click", e => {{
 const a = e.target.closest('a[href^="#ev-"]'); if (!a) return;
 if (!document.querySelector(a.getAttribute("href"))) {{
  document.querySelectorAll("#filters button").forEach(x => x.classList.toggle("on", x.dataset.f==="all"));
  cur = "all"; render(cur);
 }}
}});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
