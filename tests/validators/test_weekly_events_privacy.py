# -*- coding: utf-8 -*-
"""weekly_events_render 공개용 가드 — 개인정보 문구 차단, 주 묶음, 산출물 스키마 변형 흡수."""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "weekly-events" / "scripts"))
import weekly_events_render as wer  # noqa: E402


def test_privacy_blocks_position_terms():
    for s in ["IREN 내 비중 85~95%", "IREN 보유, 나머지 미보유", "258주 @평단 $39.29",
              "$30 추가매수 중단", "config/positions.yaml", "집중 경보 6/8축", "koramai26@example.co.kr"]:
        assert wer.privacy_hits(s), s


def test_privacy_passes_public_text():
    s = "연준이 기준금리를 0.25%p 올림(3.75~4.00%). " + wer.DISCLAIMER
    assert wer.privacy_hits(s.replace(wer.DISCLAIMER, "")) == []


def test_rendered_page_has_no_private_terms():
    store = wer.load_json(wer.STORE)
    today = date(2026, 10, 5)
    data = wer.build(today, store, store["tickers"])
    page = wer.render_html(today, store, store["tickers"], data)
    assert wer.privacy_hits(page.replace(wer.DISCLAIMER, "")) == []
    assert "positions" not in page


def test_main_refuses_to_write_when_private(tmp_path, monkeypatch):
    store = wer.load_json(wer.STORE)
    store["headline"] = "IREN 내 비중 90%"
    p = tmp_path / "store.json"
    p.write_text(json.dumps(store, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(wer, "STORE", p)
    out = tmp_path / "page.html"
    assert wer.main(["--out", str(out), "--today", "2026-10-05"]) == 2
    assert not out.exists()


def test_ledger_links_and_threads_resolve():
    """원장의 links·threads가 전부 실제 이벤트·이야기를 가리킨다(끊긴 연결 0)."""
    store = wer.load_json(wer.STORE)
    data = wer.build(date(2026, 10, 9), store, store["tickers"])
    assert data["warnings"] == []
    ids = [e["id"] for e in store["events"]]
    assert len(ids) == len(set(ids)), "이벤트 id 중복"


def test_exposure_overlay_marks_matrix_and_off_matrix():
    store = {"tickers": ["NBIS"], "threads": [{"id": "t1", "title": "x", "tk": "NBIS", "events": ["a"]}],
             "events": [{"id": "a", "date": "2026-10-07", "tk": "NBIS", "text": "t", "threads": ["t1"],
                         "exposure": [{"tk": "NBIS", "axis": "금리·자금조달", "dir": "watch", "note": "n1"},
                                      {"tk": "NBIS", "axis": "전력·인허가", "dir": "up", "note": "n2"}]}]}
    data = wer.build(date(2026, 10, 9), store, ["NBIS"])
    assert ("NBIS", "금리·자금조달") in data["overlay"]
    assert [o["axis"] for o in data["off_matrix"]] == ["전력·인허가"]   # NBIS 매트릭스에 전력 축 없음
    assert data["threads"][0]["updated"] is True


def test_explainer_todo_flags_missing_and_stale():
    base = {"tickers": ["IREN"], "events": [
        {"id": "a", "date": "2026-10-07", "tk": "IREN", "text": "t"},
        {"id": "b", "date": "2026-09-08", "tk": "IREN", "text": "t"}]}
    # 이번 주 소식이 붙었는데 해설 없음 → 안내
    s1 = dict(base, threads=[{"id": "t1", "title": "x", "tk": "IREN", "events": ["a"]}])
    assert any("t1" in m for m in wer.build(date(2026, 10, 9), s1, ["IREN"])["explainer_todo"])
    # 해설 기준일 이후 새 소식 → 갱신 안내 + stale 표시
    s2 = dict(base, threads=[{"id": "t2", "title": "x", "tk": "IREN", "events": ["a"], "explainer": {"asof": "2026-09-30"}}])
    d2 = wer.build(date(2026, 10, 9), s2, ["IREN"])
    assert any("t2" in m for m in d2["explainer_todo"]) and d2["threads"][0].get("explainer_stale")
    # 지난 주 이야기·최신 해설 → 안내 없음
    s3 = dict(base, threads=[{"id": "t3", "title": "x", "tk": "IREN", "events": ["b"], "explainer": {"asof": "2026-10-09"}}])
    assert wer.build(date(2026, 10, 9), s3, ["IREN"])["explainer_todo"] == []


def test_tracked_table_flagged_until_checked_this_week():
    base = {"tickers": ["IREN"], "events": [{"id": "b", "date": "2026-09-08", "tk": "IREN", "text": "t"}]}
    tb = lambda asof: {"id": "sw", "asof": asof, "title": "x", "head": ["a"], "rows": [["1"]]}
    # 지난주에 확인한 추적 표 → 소식이 없어도 이번 주 재확인 안내 + stale 표시
    s1 = dict(base, threads=[{"id": "t1", "title": "x", "tk": "IREN", "events": ["b"],
                              "explainer": {"asof": "2026-10-09", "tables": [tb("2026-10-09")]}}])
    d1 = wer.build(date(2026, 10, 12), s1, ["IREN"])
    assert any("t1/sw" in m for m in d1["explainer_todo"]) and d1["threads"][0]["stale_tables"] == ["sw"]
    # 이번 주(월요일 이후)에 확인 → 안내 없음
    s2 = dict(base, threads=[{"id": "t2", "title": "x", "tk": "IREN", "events": ["b"],
                              "explainer": {"asof": "2026-10-12", "tables": [tb("2026-10-12")]}}])
    assert wer.build(date(2026, 10, 14), s2, ["IREN"])["explainer_todo"] == []
    # id 없는 표는 추적 대상이 아님
    s3 = dict(base, threads=[{"id": "t3", "title": "x", "tk": "IREN", "events": ["b"],
                              "explainer": {"asof": "2026-10-09", "tables": [{"title": "x", "head": ["a"], "rows": [["1"]]}]}}])
    assert wer.build(date(2026, 10, 12), s3, ["IREN"])["explainer_todo"] == []


def test_required_tables_flag_tickers_without_table():
    base = {"tickers": ["IREN", "NBIS"], "required_tables": {"dilution": ["IREN", "NBIS"]},
            "events": [{"id": "b", "date": "2026-09-08", "tk": "IREN", "text": "t"}]}
    tb = {"id": "dilution", "asof": "2026-10-12", "title": "x", "head": ["a"], "rows": [["1"]]}
    s = dict(base, threads=[{"id": "t1", "title": "x", "tk": "IREN", "events": ["b"], "explainer": {"asof": "2026-10-12", "tables": [tb]}}])
    todo = wer.build(date(2026, 10, 14), s, ["IREN", "NBIS"])["explainer_todo"]
    assert todo == ["NBIS/dilution: 종목 추적 표가 아직 없음 — 그 종목의 자금 이야기 해설에 표를 만들어야 함"]   # IREN은 있음


def test_per_share_range_change_and_dilution_rows():
    store = {"per_share": {"IREN": [
        {"asof": "2026-08-27", "rev_q": 137.2, "arr_live": 1000, "arr_contract": 4000, "sh_basic": 394.06, "sh_fd": 558.72},
        {"asof": "2026-11-06", "rev_q": 250.0, "arr_live": 2000, "arr_contract": None, "sh_basic": 420.0, "sh_fd": None}]}}
    s = wer.per_share_series(store, ["IREN", "NBIS"])
    new, old = s["IREN"]                                                      # 최신 입력이 위
    assert old["m"]["arr_live"] == {"lo": 1.79, "hi": 2.54, "chg": None}      # 완전희석~발행 범위, 첫 기록
    assert old["m"]["rev"]["hi"] == 1.39
    assert new["m"]["arr_live"] == {"lo": 4.76, "hi": 4.76, "chg": 87.6}      # 완전희석 없으면 발행 주식만, 발행 기준 변화율
    assert new["m"]["arr_contract"] is None and s["NBIS"] == []
    rows = wer.per_share_table_rows(new)
    assert [r[0][:2] for r in rows] == ["ⓒ "] * 3 and rows[2][1] == "—" and "▲ 87.6%" in rows[1][3]
    # 희석 점검표의 손으로 쓴 ⓒ 행은 자동 계산 행으로 바뀐다
    base = {"tickers": ["IREN"], "events": [{"id": "b", "date": "2026-09-08", "tk": "IREN", "text": "t"}], **store,
            "threads": [{"id": "t1", "title": "x", "tk": "IREN", "events": ["b"], "explainer": {"asof": "2026-11-09", "tables": [
                {"id": "dilution", "asof": "2026-11-09", "title": "x", "head": ["a"], "rows": [["ⓐ x", "1"], ["ⓒ old", "9"]]}]}}]}
    d = wer.build(date(2026, 11, 10), base, ["IREN"])
    r = d["threads"][0]["explainer"]["tables"][0]["rows"]
    assert r[0] == ["ⓐ x", "1"] and len(r) == 4 and r[1][1] == "$2.38~2.38"
    assert base["threads"][0]["explainer"]["tables"][0]["rows"][1] == ["ⓒ old", "9"]   # 원장 원본은 건드리지 않음


def test_weekly_prices_close_change_index_and_provisional():
    cache = {"as_of": "2026-10-10", "daily": {
        "IREN": [["2026-09-25", 44.12, False], ["2026-09-28", 41.72, False], ["2026-10-02", 41.76, False],
                 ["2026-10-08", 35.71, False], ["2026-10-09", 35.23, True]],
        "QQQ": [["2026-10-02", 749.58, False], ["2026-10-09", 751.24, True]]}}
    out = wer.weekly_prices(cache, ["IREN"], date(2026, 9, 28), date(2026, 10, 5))
    w1, w2 = out["weeks"]
    assert w1["v"]["IREN"]["close"] == 41.76 and w1["v"]["IREN"]["chg"] == -5.3   # 주 종가 = 그 주 마지막 거래일
    assert w1["v"]["IREN"]["idx"] == 100.0                                        # 첫 주 = 100
    assert w2["v"]["IREN"]["chg"] == -15.6 and w2["v"]["IREN"]["prov"] is True and w2["now"] is True
    assert "QQQ" in w2["v"]


def test_peer_contracts_sorted_recent_first_with_unit_price():
    peers = {"companies": {"A": "에이", "B": "비"}, "contracts": [
        {"id": "a1", "date": "2025-12-17", "co": "A", "it_mw": 245, "years": 15, "value_b": 7.0, "esc_pct": 3},
        {"id": "b1", "date": "2026-09-25", "co": "B", "value_b": None},
        {"id": "b2", "date": "2026-05-06", "co": "B", "gross_mw": 300, "unit_mw": 216, "years": 15, "value_b": 5.5}],
        "financing": [{"date": "2026-02-04", "co": "B"}, {"date": "2026-06-09", "co": "A"}]}
    t = wer.peer_tables(peers, date(2026, 10, 11))
    assert [c["id"] for c in t["contracts"]] == ["b1", "b2", "a1"]          # 최근 계약이 위
    assert [f["date"] for f in t["financing"]] == ["2026-06-09", "2026-02-04"]
    a1 = t["contracts"][2]["unit"]
    assert a1 == {"mw_yr": 1.9, "mw_yr_y1": 1.54}                              # $7.0B/15년/245MW ($M/MW·년), 3% 인상 첫해
    assert t["contracts"][1]["unit"] == {"mw_yr": 1.7}                           # unit_mw(추정 IT) 기준
    assert t["contracts"][0]["unit"] is None and t["contracts"][0]["recent"] is True
    assert t["contracts"][2]["recent"] is False


def test_monday_bucketing():
    assert wer.monday(date(2026, 10, 4)) == date(2026, 9, 28)   # 일요일 → 그 주 월요일
    assert wer.monday(date(2026, 9, 28)) == date(2026, 9, 28)


def test_kill_info_ignores_narrative_mentions():
    sig = {"kill_check": {"triggered": True, "trigger_source": "KC-1 단독 (KC-9는 met 해제)"}}
    assert wer.kill_info(sig) == (True, ["KC-1"])
    sig = {"kill_check": {"kill_priority_triggered": True, "kill_trigger_kc": ["KC-1"]}}
    assert wer.kill_info(sig) == (True, ["KC-1"])


def test_gate_info_schema_variants():
    a = {"gate_check": {"upgrade_gate": {"conditions_met": {"quantitative": False, "company_specific": True, "revenue_recognized": False}}}}
    b = {"gate_check": {"upgrade_gate": {"quantitative_evidence": True, "company_specific": True, "revenue_recognized": False}}}
    c = {"gate_check": {"upgrade_gate": {"conditions": {"quantitative_evidence": False, "company_specific": True, "revenue_recognized": False}}}}
    assert list(wer.gate_info(a).values()) == [False, True, False]
    assert list(wer.gate_info(b).values()) == [True, True, False]
    assert list(wer.gate_info(c).values()) == [False, True, False]
