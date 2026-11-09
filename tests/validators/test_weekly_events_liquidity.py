# -*- coding: utf-8 -*-
"""weekly_events_render 단기자금 유동성(SOFR·IORB·지급준비금) — 차이·연속 일수·주 묶음, 캐시 없이도 렌더."""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "weekly-events" / "scripts"))
import weekly_events_render as wer  # noqa: E402

CACHE = {
    "as_of": "2026-11-09", "source": "test",
    "series": {
        "SOFR": [["2026-10-19", 3.87], ["2026-10-20", 3.88], ["2026-10-21", 3.88], ["2026-10-22", 3.90],
                 ["2026-10-23", 3.92], ["2026-10-26", 3.93], ["2026-10-27", 3.95], ["2026-10-28", 3.94],
                 ["2026-10-29", 3.94], ["2026-10-30", 3.95], ["2026-11-02", 3.95], ["2026-11-03", 3.97],
                 ["2026-11-04", 3.94], ["2026-11-05", 3.92]],
        "IORB": [["2026-09-17", 3.90]],   # 고정선 — 마지막 변경일 하나만 있어도 그 뒤 날짜에 적용
        "WRESBAL": [["2026-10-21", 2962.6], ["2026-10-28", 2893.8], ["2026-11-04", 2930.1]],
        "RPONTSYD": [["2026-10-29", 0.011], ["2026-11-05", 0.0]],
    },
    "marks": [{"date": "2026-11-05", "label": "표시"}, {"date": "2026-01-01", "label": "기간 밖"}],
}


def test_liquidity_spread_streak_and_weeks():
    todo = []
    q = wer.liquidity_section(CACHE, date(2026, 10, 19), date(2026, 11, 2), date(2026, 11, 9), todo)
    n = q["now"]
    assert (n["d"], n["bp"]) == ("2026-11-05", 2)
    assert n["streak"] == 10 and n["streak_from"] == "2026-10-23"   # 10/22는 같음(0bp) → 연속에 넣지 않음
    assert (n["max_bp"], n["max_d"]) == (7, "2026-11-03")
    assert n["res"] == ["2026-11-04", 2930.1] and n["res_chg"] == 36.3
    w = q["weeks"]
    assert w["2026-10-19"]["above"] == 1 and w["2026-10-19"]["bp_max"] == 2
    assert w["2026-10-26"]["res"] == 2893.8 and w["2026-10-26"]["res_chg"] == -68.8
    assert w["2026-11-02"]["now"] and w["2026-11-02"]["days"] == 4 and w["2026-11-02"]["bp"] == 4.5
    assert [m["label"] for m in q["marks"]] == ["표시"]
    assert q["line"] == 2900 and todo == []


def test_alert_when_sofr_above_iorb_or_reserves_below_line():
    q = wer.liquidity_section(CACHE, date(2026, 10, 19), date(2026, 11, 2), date(2026, 11, 9), [])
    msgs = wer.liq_alerts(q)
    assert len(msgs) == 1 and "SOFR가 IORB 위" in msgs[0] and "10/23부터 10영업일" in msgs[0]   # 지준 2.930조 → 참고선 위
    q["now"]["res"] = ["2026-10-28", 2893.8]
    msgs = wer.liq_alerts(q)
    assert len(msgs) == 2 and "참고선 아래" in msgs[1] and "62억 달러" in msgs[1]
    q["now"].update(bp=0, res=["2026-11-04", 2930.1])
    assert wer.liq_alerts(q) == [] and wer.liq_alert_html(q) == "" and wer.liq_alerts(None) == []


def test_alert_rendered_at_page_top(monkeypatch, tmp_path):
    import json
    p = tmp_path / "liq.json"
    p.write_text(json.dumps(CACHE, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(wer, "LIQ", p)
    store = wer.load_json(wer.STORE)
    data = wer.build(date(2026, 11, 9), store, store["tickers"])
    page = wer.render_html(date(2026, 11, 9), store, store["tickers"], data)
    assert 'id="liq-alert"' in page and page.index('id="liq-alert"') < page.index("<h2>읽는 법</h2>")


def test_liquidity_stale_adds_todo():
    todo = []
    wer.liquidity_section(CACHE, date(2026, 10, 19), date(2026, 11, 23), date(2026, 11, 23), todo)
    assert any(t.startswith("liquidity:") for t in todo)


def test_page_renders_without_liquidity_cache(monkeypatch, tmp_path):
    monkeypatch.setattr(wer, "LIQ", tmp_path / "none.json")
    store = wer.load_json(wer.STORE)
    data = wer.build(date(2026, 11, 9), store, store["tickers"])
    assert data["liq"] is None
    page = wer.render_html(date(2026, 11, 9), store, store["tickers"], data)
    assert 'id="liq"' in page and wer.privacy_hits(page.replace(wer.DISCLAIMER, "")) == []
