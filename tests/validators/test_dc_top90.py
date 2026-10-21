# -*- coding: utf-8 -*-
"""Top 90 추적 — 점검 결과 합치기(단계 변경·사건 id·follow-up)와 주간 페이지 섹션 집계."""
import copy
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "weekly-events" / "scripts"))
import dc_top90_merge as m  # noqa: E402
import weekly_events_render as wer  # noqa: E402


def proj(pid, st, stage, gw, tickers=()):
    return {"id": pid, "no": int(pid[1:]), "name": f"P{pid}", "developer": "D", "state": st, "gw": gw, "power": "Grid",
            "stage_base": stage, "stage": stage, "stage_asof": "2026-07-07",
            "stage_history": [{"date": "2026-07-07", "stage": stage}], "status": "", "holds": [], "tickers": list(tickers),
            "aliases": [], "followup": None, "last_checked": None, "events": [], "data_issues": []}


BASE = {"projects": [proj("p01", "TX", "3", 2.0, ["IREN"]), proj("p02", "NY", "X", 1.0), proj("p03", "TX", "1", 3.0)],
        "events": [], "policies": [], "checked_through": None, "baseline_date": "2026-07-07",
        "stages": {"1": "착공 후 공사 중"}}

SWEEP = {"checked_at": "2026-10-20", "projects": [
    {"id": "p01", "stage_now": "1", "status_ko": "착공 확인", "holds": ["텍사스 인허가 중단"],
     "events": [{"date": "2026-09-01", "kind": "착공", "title_ko": "착공", "grade": 1, "src": []}],
     "followup": {"needed": True, "why": "동결", "questions": ["해제되나?"], "next_check": "2026-10-27"}},
    {"id": "p02", "stage_now": "X", "stage_candidate": "C", "status_ko": "중단 보도", "events": [], "followup": {"needed": False}},
]}


def test_merge_stage_event_followup_and_missing():
    L = copy.deepcopy(BASE)
    log = m.merge(L, [SWEEP], None, "2026-10-20")
    p1, p2 = L["projects"][0], L["projects"][1]
    assert p1["stage"] == "1" and p1["stage_history"][-1]["stage"] == "1"
    assert p1["events"] == ["d0901-p01-1"]
    ev = L["events"][0]
    assert ev["stage_change"] == {"pid": "p01", "from": "3", "to": "1"} and ev["logged"] == "2026-10-20" and not ev["rumor"]
    assert p1["followup"]["next_check"] == "2026-10-27" and p1["followup"]["closed"] is None
    assert any("IREN" in s for s in log["self"])
    # 단계 후보는 단계를 바꾸지 않고 follow-up 질문으로만
    assert p2["stage"] == "X" and p2["followup"] and "후보" in p2["followup"]["questions"][0]
    assert log["missing"] == ["p03"] and L["checked_through"] == "2026-10-20"
    # 같은 결과를 다시 합쳐도 사건이 중복되지 않는다
    m.merge(L, [SWEEP], None, "2026-10-20")
    assert len([e for e in L["events"] if e["projects"] == ["p01"]]) == 1


def test_merge_closes_followup_and_keeps_log():
    L = copy.deepcopy(BASE)
    m.merge(L, [SWEEP], None, "2026-10-20")
    nxt = {"checked_at": "2026-10-27", "projects": [{"id": "p01", "stage_now": "1", "events": [],
           "followup": {"answered": [{"q": "해제되나?", "a": "12/15 해제"}], "close": True, "close_why": "답 확인"}}]}
    log = m.merge(L, [nxt], None, "2026-10-27")
    fu = L["projects"][0]["followup"]
    assert fu["closed"] == {"date": "2026-10-27", "why": "답 확인"} and "12/15 해제" in fu["log"][-1]["note"]
    assert log["close"]


def test_dc_section_aggregates_and_overdue_notice():
    L = copy.deepcopy(BASE)
    m.merge(L, [SWEEP], {"policies": [{"id": "pol-tx", "scope": "TX", "title_ko": "감사", "timeline": [{"date": "2026-09-21", "what_ko": "중단", "grade": 1}]}]}, "2026-10-20")
    todo = []
    d = wer.dc_section(L, date(2026, 11, 2), todo)
    assert d["base"]["3"]["n"] == 1 and d["now"]["1"] == {"n": 2, "gw": 5.0}
    assert d["policies"][0]["n"] == 2 and d["policies"][0]["gw"] == 5.0 and d["policies"][0]["stage1"] == 2
    assert [e["id"] for e in d["recent"]] == ["d0901-p01-1"]
    assert any("확인일 2026-10-27 지남" in t for t in todo) and any("마지막 점검" in t for t in todo)
    assert d["weekly"]["2026-08-31"] == {"n": 1, "stage": 1}


def test_merge_month_dates_and_future_items():
    L = copy.deepcopy(BASE)
    sw = {"checked_at": "2026-10-20", "projects": [{"id": "p03", "stage_now": "1", "events": [
        {"date": "2026-08", "kind": "자금", "title_ko": "월 단위 사건", "grade": 3},
        {"date": "2026-10-22", "kind": "소송", "title_ko": "심리 예정", "grade": 1}]}]}
    log = m.merge(L, [sw], None, "2026-10-20")
    evs = [e for e in L["events"] if e["projects"] == ["p03"]]
    assert [e["id"] for e in evs] == ["d0801-p03-1"] and "월 단위" in evs[0]["date_approx"]
    assert any("예정 사항 제외" in x for x in log["issues"])
