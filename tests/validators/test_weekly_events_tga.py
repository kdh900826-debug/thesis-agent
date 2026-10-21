# -*- coding: utf-8 -*-
"""weekly_events_render 재무부 현금(TGA) — 주 묶음·계획 대비 계산, 캐시 없이도 렌더."""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "weekly-events" / "scripts"))
import weekly_events_render as wer  # noqa: E402

CACHE = {
    "as_of": "2026-10-18", "source": "test",
    "daily": [["2026-09-29", 936.6, 283.5, 306.5], ["2026-09-30", 984.0, 261.8, 214.4],
              ["2026-10-01", 893.7, 373.7, 464.0], ["2026-10-02", 871.2, 20.4, 42.9],
              ["2026-10-13", 920.2, 353.9, 306.2], ["2026-10-15", 934.7, 449.2, 400.3]],
    "plan": [{"id": "a", "label": "9월 말", "date": "2026-09-30", "value": 950},
             {"id": "b", "label": "10월 하순", "from": "2026-10-19", "to": "2026-10-31", "value": 1050, "band": 50},
             {"id": "c", "label": "12월 말", "date": "2026-12-31", "value": 850}],
}


def test_weekly_tga_groups_weeks_and_compares_plan():
    t = wer.weekly_tga(CACHE, date(2026, 9, 28), date(2026, 10, 12), date(2026, 10, 18))
    wk = {w["w"]: w for w in t["weeks"]}
    assert set(wk) == {"2026-09-28", "2026-10-12"}           # 10/5 주는 자료 없음 → 행 없음
    assert wk["2026-09-28"]["close"] == 871.2 and wk["2026-09-28"]["chg"] is None
    assert (wk["2026-09-28"]["lo"], wk["2026-09-28"]["hi"]) == (871.2, 984.0)
    assert wk["2026-10-12"]["now"] and wk["2026-10-12"]["chg"] is None   # 직전 주 자료 없으면 비교 없음
    plan = {p["id"]: p for p in t["plan"]}
    assert plan["a"]["actual"] == 984.0 and plan["a"]["gap"] == 34.0 and plan["a"]["state"] == "지남"
    assert plan["b"]["state"] == "아직" and "actual" not in plan["b"]
    assert plan["c"]["state"] == "아직"
    assert t["last"] == ["2026-10-15", 934.7]


def test_page_renders_without_tga_cache(monkeypatch, tmp_path):
    monkeypatch.setattr(wer, "TGA", tmp_path / "none.json")
    store = wer.load_json(wer.STORE)
    data = wer.build(date(2026, 10, 18), store, store["tickers"])
    assert data["tga"] is None
    page = wer.render_html(date(2026, 10, 18), store, store["tickers"], data)
    assert 'id="tga"' in page and wer.privacy_hits(page.replace(wer.DISCLAIMER, "")) == []
