# -*- coding: utf-8 -*-
"""weekly_events_render AI 신용 경보 — 기간별 변화·조합 읽기·단계 기준선·주 카드 값, 캐시 없이도 렌더."""
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "weekly-events" / "scripts"))
import weekly_events_render as wer  # noqa: E402


def _series(start, vals, step=1):
    d = date.fromisoformat(start)
    return [[(d + timedelta(days=i * step)).isoformat(), v] for i, v in enumerate(vals)]


def _cache(r10, hy, r2=None):
    n = len(r10)
    flat = lambda v: [v] * n
    return {"as_of": "2026-10-23", "source": "test",
            "series": {"DGS10": _series("2026-09-01", r10), "DGS2": _series("2026-09-01", r2 or flat(4.0)),
                       "BAMLH0A0HYM2": _series("2026-09-01", hy), "BAMLH0A3HYC": _series("2026-09-01", flat(9.0)),
                       "BAMLC0A4CBBB": _series("2026-09-01", flat(1.0)), "BAMLC0A0CM": _series("2026-09-01", flat(0.8)),
                       "ICSA": _series("2026-06-01", [220.0] * 21, step=7)},
            "ai_watch": {"asof": "2026-10-19", "rows": [{"id": "a", "state": "악화"}, {"id": "b", "state": "악화"},
                                                        {"id": "c", "state": "확인 전"}]}}


def test_video_signal_shape_and_stages():
    # 10년물은 내리고(5.4 → 4.8) 하이일드는 벌어진다(3.0 → 3.9): 영상이 말한 모양
    n = 45
    r10 = [round(5.4 - 0.6 * i / (n - 1), 2) for i in range(n)]
    hy = [round(3.0 + 0.9 * i / (n - 1), 2) for i in range(n)]
    todo = []
    today = date(2026, 10, 15)
    c = wer.credit_section(_cache(r10, hy), date(2026, 9, 28), wer.monday(today), today, todo)
    four = next(x for x in c["combos"] if x["w"] == "4주")
    assert four["combo"] == "금리↓ + 스프레드↑"
    assert four["d10"] < -0.25 and four["dhy"] > 0.5
    st = {s["n"]: s for s in c["stages"]}
    assert st[1]["met"] == 1                     # 악화 2개 ≥ 기준 2
    assert st[2]["conds"][0]["ok"] is True and st[2]["conds"][1]["ok"] is False
    assert st[3]["conds"][0]["ok"] is True       # 영상 신호 조건
    assert st[3]["conds"][1]["ok"] is False      # 2년물은 그대로 → 강세 스티프닝 아님
    assert st[3]["conds"][2]["ok"] is False      # 청구 변화 0%
    assert c["weeks"]["2026-10-12"]["DGS10"]["chg"] is not None   # 주 카드 값과 전주 대비
    assert not any("credit/ai_watch" in t for t in todo)           # 10/19 확인 ≥ 이번 주 월요일(10/12)


def test_ai_watch_todo_and_quiet_combo():
    todo = []
    today = date(2026, 10, 27)   # 이번 주 월요일 10/26 > ai_watch 확인일 10/19
    c = wer.credit_section(_cache([5.0] * 50, [3.0] * 50), date(2026, 9, 28), wer.monday(today), today, todo)
    assert all(x["combo"] == "뚜렷한 조합 없음" for x in c["combos"])
    assert all(s["met"] == 0 for s in c["stages"] if s["n"] > 1)
    assert any(t.startswith("credit/ai_watch: 1단계 AI 고유 지표를 이번 주에 확인하지 않음") for t in todo)


def test_curve_labels():
    assert wer.credit_combo(-0.2, 0.3, -0.4, 0.1)["curve"] == "강세 스티프닝"
    assert wer.credit_combo(-0.4, 0.3, -0.2, 0.1)["curve"] == "강세 플래트닝"
    assert wer.credit_combo(0.4, 0.3, 0.1, 0.1)["curve"] == "약세 스티프닝"
    assert wer.credit_combo(0.02, 0.03, 0.01, 0.1)["combo"] == "뚜렷한 조합 없음"


def test_page_renders_without_credit_cache(monkeypatch, tmp_path):
    monkeypatch.setattr(wer, "CREDIT", tmp_path / "none.json")
    store = wer.load_json(wer.STORE)
    data = wer.build(date(2026, 10, 23), store, store["tickers"])
    assert data["credit"] is None
    page = wer.render_html(date(2026, 10, 23), store, store["tickers"], data)
    assert 'id="credit"' in page and wer.privacy_hits(page.replace(wer.DISCLAIMER, "")) == []
