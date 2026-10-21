# -*- coding: utf-8 -*-
"""Top 90 점검 결과(dc-top90-tracker 묶음별 JSON + 정책 JSON)를 원장 state/dc_top90.json에 합친다.

사용:
  python dc_top90_merge.py output/dc_top90_sweeps/<YYYYMMDD> [--dry-run]

하는 일: 백업 → 프로젝트별 상태·묶임·확인일 갱신 → 단계 변경(stage_now가 다르면 stage_history·사건에 기록)
→ 새 사건에 고정 id(d<MMDD>-<pNN>-<n>) 부여(같은 날짜·제목은 건너뜀) → follow-up 열기·갱신·닫기
→ policies.json이 있으면 정책을 id 기준으로 교체(이전 timeline은 날짜·내용이 겹치지 않는 것만 보존) → checked_through 갱신.
세 종목(IREN·NBIS·CRWV) 관련 프로젝트의 새 사건은 주간 이벤트 원장 반영 후보로 출력한다(원장 weekly_events.json은 고치지 않음).
단계 후보(stage_candidate)는 단계를 바꾸지 않고 follow-up 질문으로만 남긴다.
"""
import argparse, json, re, shutil, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DC = ROOT / "state" / "dc_top90.json"
SELF = {"IREN", "NBIS", "CRWV"}
STAGES = {"0", "1", "2", "3", "X", "C"}


def norm_date(d, checked):
    """사건 날짜를 YYYY-MM-DD로 맞춘다. 월까지만 있으면 1일로, 없으면 점검일로 두고 원래 표기를 approx로 돌려준다."""
    d = (d or "").strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        return d, None
    if re.match(r"^\d{4}-\d{2}$", d):
        return f"{d}-01", f"{d} (날짜는 월 단위)"
    return checked, f"날짜 미상 — 점검일 {checked}로 기록"


def ev_id(d, pid, used):
    base = f"d{d[5:7]}{d[8:10]}-{pid}-"
    n = 1
    while f"{base}{n}" in used:
        n += 1
    used.add(f"{base}{n}")
    return f"{base}{n}"


def merge(L, sweeps, policies, checked):
    by_id = {p["id"]: p for p in L["projects"]}
    used = {e["id"] for e in L.get("events", [])}
    seen = {(e.get("date"), e.get("title")) for e in L.get("events", [])}
    log = {"stage": [], "cand": [], "new": 0, "open": [], "close": [], "self": [], "missing": [], "issues": []}
    covered = set()
    for sw in sweeps:
        for r in sw.get("projects", []):
            p = by_id.get(r.get("id"))
            if not p:
                log["issues"].append(f"원장에 없는 id: {r.get('id')}")
                continue
            if r.get("searched") is False:   # 검색 한도 등으로 실제 확인 못 함 — 확인일·상태를 건드리지 않고 '점검 안 됨'으로 남긴다
                for e in r.get("events") or []:
                    log["issues"].append(f"{p['id']} searched=false인데 사건이 있음 — 사건만 반영: {e.get('title_ko', '')}")
                if not r.get("events"):
                    continue
            else:
                covered.add(p["id"])
                p["last_checked"] = checked
            if r.get("status_ko"):
                p["status"] = r["status_ko"]
            p["holds"] = r.get("holds") or []
            for t in r.get("tickers_touched") or []:
                if t not in p["tickers"]:
                    p["tickers"].append(t)
            for di in r.get("data_issues") or []:
                if di not in p["data_issues"]:
                    p["data_issues"].append(di)
            new_ids = []
            for e in sorted(r.get("events") or [], key=lambda x: x.get("date") or ""):
                d, approx = norm_date(e.get("date"), checked)
                if d > checked:   # 예정 사항(심리·표결 등)은 사건이 아니다 — follow-up 확인일로만 다룬다
                    log["issues"].append(f"{p['id']} 예정 사항 제외(follow-up next_check로 확인): {d} {e.get('title_ko', '')}")
                    continue
                if (d, e.get("title_ko")) in seen:
                    continue
                seen.add((d, e.get("title_ko")))
                eid = ev_id(d, p["id"], used)
                g = e.get("grade") or 3
                L["events"].append({"id": eid, "date": d, "logged": checked, "projects": [p["id"]], "kind": e.get("kind", "기타"),
                                    "title": e.get("title_ko", ""), "detail": e.get("detail_ko") or [], "grade": g,
                                    "rumor": g >= 3, "src": e.get("src") or [], "stage_change": None,
                                    **({"date_approx": approx} if approx else {})})
                p["events"].append(eid); new_ids.append(eid); log["new"] += 1
                if SELF & set(p["tickers"]):
                    log["self"].append(f"{eid} [{'/'.join(sorted(SELF & set(p['tickers'])))}] {p['name']}: {e.get('title_ko', '')}")
            sn = r.get("stage_now")
            if sn in STAGES and sn != p["stage"]:
                frm = p["stage"]
                p["stage"], p["stage_asof"] = sn, checked
                p["stage_history"].append({"date": checked, "stage": sn, "src": f"점검 {checked}", "note": r.get("status_ko", "")})
                tgt = next((x for x in L["events"] if new_ids and x["id"] == new_ids[-1]), None)   # 가장 최근 새 사건에 단계 변경을 붙인다
                if tgt:
                    tgt["stage_change"] = {"pid": p["id"], "from": frm, "to": sn}
                else:
                    eid = ev_id(checked, p["id"], used)
                    L["events"].append({"id": eid, "date": checked, "logged": checked, "projects": [p["id"]], "kind": "단계",
                                        "title": f"단계 변경 {frm} → {sn}", "detail": [r.get("status_ko", "")], "grade": None,
                                        "rumor": False, "src": [], "stage_change": {"pid": p["id"], "from": frm, "to": sn}})
                    p["events"].append(eid)
                log["stage"].append(f"{p['id']} {p['name']}: {frm} → {sn}")
            cand = r.get("stage_candidate")
            f_in = r.get("followup") or {}
            if cand and cand != p["stage"]:
                log["cand"].append(f"{p['id']} {p['name']}: {p['stage']} → {cand} 후보")
                q = f"단계 {p['stage']} → {cand} 후보 — 회사·정부 문서 또는 다른 언론 2곳으로 확인되나?"
                f_in = dict(f_in, needed=True, questions=list(dict.fromkeys((f_in.get("questions") or []) + [q])),
                            why=f_in.get("why") or "단계 변경 후보")
            fu = p.get("followup")
            if fu and not fu.get("closed"):
                ans = "; ".join(f"{a.get('q', '')} → {a.get('a', '')}" for a in f_in.get("answered") or [])
                fu.setdefault("log", []).append({"date": checked, "note": ans or (r.get("status_ko") or "새 소식 없음"), "events": new_ids})
                if f_in.get("close"):
                    fu["closed"] = {"date": checked, "why": f_in.get("close_why", "")}
                    log["close"].append(f"{p['id']} {p['name']}: {f_in.get('close_why', '')}")
                else:
                    if f_in.get("questions"):
                        fu["questions"] = f_in["questions"]
                    if f_in.get("next_check"):
                        fu["next_check"] = f_in["next_check"]
                    if f_in.get("why"):
                        fu["why"] = f_in["why"]
            elif f_in.get("needed"):
                if fu:   # 닫힌 follow-up은 이력으로 남기고 새로 연다
                    p.setdefault("followup_history", []).append(fu)
                p["followup"] = {"opened": checked, "why": f_in.get("why", ""), "questions": f_in.get("questions") or [],
                                 "next_check": f_in.get("next_check") or "", "log": [], "closed": None}
                log["open"].append(f"{p['id']} {p['name']}: {f_in.get('why', '')}")
    log["missing"] = sorted(set(by_id) - covered)
    if policies:
        old = {x["id"]: x for x in L.get("policies", [])}
        for pol in policies.get("policies", []):
            prev = old.get(pol["id"], {})
            tl = [{"date": t.get("date", ""), "what": t.get("what_ko", t.get("what", "")), "grade": t.get("grade"),
                   "src": t.get("src") or []} for t in pol.get("timeline", [])]
            keys = {(t["date"], t["what"]) for t in tl}
            tl = [t for t in prev.get("timeline", []) if (t["date"], t["what"]) not in keys] + tl
            tl.sort(key=lambda t: t["date"] or "")
            old[pol["id"]] = {"id": pol["id"], "scope": pol.get("scope", ""), "title": pol.get("title_ko", prev.get("title", "")),
                              "status": pol.get("status_ko", ""), "effect": pol.get("effect", ""),
                              "applies_to": pol.get("applies_to_ko", ""), "timeline": tl,
                              "next": [{"date": n.get("date", ""), "what": n.get("what_ko", n.get("what", ""))} for n in pol.get("next", [])],
                              "asof": checked}
        L["policies"] = list(old.values())
        if policies.get("election_watch"):
            L["election_watch"] = [{"state": x.get("state", ""), "what": x.get("race_or_measure_ko", x.get("what", "")),
                                    "why": x.get("why_ko", x.get("why", "")), "date": x.get("date", "")}
                                   for x in policies["election_watch"]]
    L["checked_through"] = checked
    L["updated_at"] = date.today().isoformat()
    return log


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("sweep_dir")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    d = Path(a.sweep_dir)
    sweeps = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("g*.json"))]
    pf = d / "policies.json"
    policies = json.loads(pf.read_text(encoding="utf-8")) if pf.exists() else None
    if not sweeps and not policies:
        print(f"점검 결과 없음: {d}")
        return 1
    checked = next((s.get("checked_at") for s in sweeps if s.get("checked_at")), None) or (policies or {}).get("checked_at") or date.today().isoformat()
    L = json.loads(DC.read_text(encoding="utf-8"))
    log = merge(L, sweeps, policies, checked)
    print(f"점검일 {checked} · 묶음 {len(sweeps)}개 · 새 사건 {log['new']}건 · 정책 {'갱신' if policies else '없음'}")
    for k, label in (("stage", "단계 변경"), ("cand", "단계 후보(미변경)"), ("open", "follow-up 열림"),
                     ("close", "follow-up 닫힘"), ("self", "세 종목 관련 새 사건 — 주간 이벤트 원장 반영 후보"), ("issues", "문제")):
        if log[k]:
            print(f"[{label}] {len(log[k])}건")
            for x in log[k]:
                print(f"  - {x}")
    if log["missing"]:
        print(f"[점검 안 된 프로젝트] {len(log['missing'])}건: {', '.join(log['missing'])}")
    if a.dry_run:
        print("(dry-run — 원장 미기록)")
        return 0
    bk = ROOT / "state" / "backup" / f"dc_top90_{checked.replace('-', '')}_pre_merge.json"
    bk.parent.mkdir(parents=True, exist_ok=True)
    if not bk.exists():
        shutil.copy2(DC, bk)
    DC.write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"원장 기록: {DC} (백업 {bk.name})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
