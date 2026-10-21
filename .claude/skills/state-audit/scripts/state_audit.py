# -*- coding: utf-8 -*-
"""state-audit — 모든 Run의 필수 선행 단계 (S0, D6·D9·P11·P16).
사용: python state_audit.py --command "<명령>" --run-id <YYYYMMDD_HHmm>
출력: output/{run_id}/00_state_audit.json + 콘솔 요약. config 오류 시 종료코드 1(에스컬레이션).
"""
import argparse, json, sys
from datetime import datetime, date, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml 필요 — pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[4]
CONFIGS = ["coverage.yaml", "kill_conditions.yaml", "noise_filter.yaml",
           "sources.yaml", "staleness.yaml", "correlation_matrix.yaml", "positions.yaml"]


def trading_days_between(d0: date, d1: date) -> int:
    """주말 제외 경과 거래일 근사 (연방 공휴일 미반영 — 보수 방향은 provisional)."""
    if d1 <= d0:
        return 0
    n, d = 0, d0
    while d < d1:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def parse_date(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).date()
    except ValueError:
        return None


def staleness_of(as_of, limit_cfg, today):
    d = parse_date(as_of)
    if d is None:
        return {"age": None, "stale": True, "reason": "as_of 없음/파싱 불가"}
    unit = limit_cfg.get("unit", "calendar_days")
    age = trading_days_between(d, today) if unit == "trading_days" else (today - d).days
    return {"age": age, "unit": unit, "limit": limit_cfg["limit"], "stale": age > limit_cfg["limit"]}


def audit_configs(report):
    """스키마 검증 — 임계 없는 active KC = 로드 실패(P11)."""
    errors, warnings, cfgs = [], [], {}
    for name in CONFIGS:
        p = ROOT / "config" / name
        if not p.exists():
            errors.append(f"config/{name} 부재")
            continue
        try:
            cfgs[name] = yaml.safe_load(p.read_text(encoding="utf-8-sig"))
        except yaml.YAMLError as e:
            errors.append(f"config/{name} YAML 오류: {e}")
    kc = cfgs.get("kill_conditions.yaml", {})
    for group in ("macro", "company"):
        for kc_id, spec in (kc.get(group) or {}).items():
            status = spec.get("status")
            if status == "draft":
                warnings.append(f"{kc_id}: draft — 로드 제외 (임계 확정 후 active로 변경)")
                continue
            if status != "active":
                errors.append(f"{kc_id}: status가 active/draft가 아님")
                continue
            if spec.get("type") == "event":
                if not spec.get("trigger"):
                    errors.append(f"P11: {kc_id} (event형) trigger 부재")
                continue
            conds = spec.get("all_of") or spec.get("any_of") or []
            if not conds:
                errors.append(f"P11: {kc_id} 임계 조건 부재 — 로드 실패")
            for c in conds:
                if c.get("threshold") is None:
                    errors.append(f"P11: {kc_id} threshold 부재 — 로드 실패")
    cm = cfgs.get("correlation_matrix.yaml", {})
    if cm.get("status") == "draft":
        warnings.append("correlation_matrix.yaml: draft — L4 상관 레이어 실행 불가 (U4)")
    pos = cfgs.get("positions.yaml", {})
    if not pos.get("as_of"):
        warnings.append("positions.yaml: as_of 미기입 (R3) — 축 집중도는 종목 수 기준 상대 판정만 가능")
    report["config_errors"], report["config_warnings"] = errors, warnings
    return cfgs, errors


def audit_approvals(report, today):
    """승인 큐 최우선 보고 + 만료 처리 (D6)."""
    qp = ROOT / "state" / "pending_approvals.json"
    q = json.loads(qp.read_text(encoding="utf-8-sig")) if qp.exists() else {"queue": []}
    pending, expired_now = [], []
    for e in q.get("queue", []):
        if e.get("status") != "pending":
            continue
        created = parse_date(e.get("created_at"))
        limit = e.get("expires_after_days", 14)
        age = (today - created).days if created else None
        if age is not None and age > limit:
            e["status"] = "expired"
            expired_now.append(e["approval_id"])
        else:
            pending.append({"approval_id": e["approval_id"], "type": e.get("type"),
                            "age_days": age, "artifact": e.get("artifact")})
    if expired_now:
        qp.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
    report["pending_approvals"] = pending
    report["expired_now"] = expired_now


def audit_artifacts(report, cfgs, today):
    """최신 산출물·상태 파일 staleness (P16)."""
    limits = (cfgs.get("staleness.yaml") or {}).get("limits", {})
    items = {}
    runs = sorted((ROOT / "output").glob("*/"), reverse=True) if (ROOT / "output").exists() else []
    latest = runs[0] if runs else None
    def check_file(key, path, limit_key):
        if not path.exists():
            items[key] = {"exists": False}
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            as_of = data.get("as_of")
        except Exception:
            as_of = None
        lc = limits.get(limit_key)
        items[key] = {"exists": True, "path": str(path.relative_to(ROOT)),
                      **(staleness_of(as_of, lc, today) if lc else {"age": None})}
    if latest:
        report["latest_run"] = latest.name
        check_file("macro_kc", latest / "01_macro_kc.json", "SignalDecision")
        check_file("correlation", latest / "05_correlation.json", "CorrelationView")
    for card in (ROOT / "state" / "thesis_cards").glob("*.yaml"):
        c = yaml.safe_load(card.read_text(encoding="utf-8-sig"))
        st = staleness_of(c.get("as_of"), limits.get("ThesisCard", {"limit": 90, "unit": "calendar_days"}), today)
        if st.get("stale"):
            items[f"thesis_card_{card.stem}"] = {"exists": True, **st}
    pos = cfgs.get("positions.yaml") or {}
    if pos.get("as_of"):
        items["positions"] = staleness_of(pos["as_of"], limits.get("Positions", {"limit": 30, "unit": "calendar_days"}), today)
    report["artifacts"] = items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--command", default="")
    ap.add_argument("--run-id", default=datetime.now().strftime("%Y%m%d_%H%M"))
    args = ap.parse_args()
    today = date.today()
    report = {"as_of": today.isoformat(), "run_id": args.run_id, "command": args.command}

    audit_approvals(report, today)
    cfgs, errors = audit_configs(report)
    audit_artifacts(report, cfgs, today)

    out_dir = ROOT / "output" / args.run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "00_state_audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 콘솔 요약 — 승인 대기 최우선 (D6)
    if report["pending_approvals"]:
        print(f"⚠️ 승인 대기 {len(report['pending_approvals'])}건:")
        for e in report["pending_approvals"]:
            print(f"   {e['approval_id']} ({e['type']}, {e['age_days']}일 경과)")
    if report["expired_now"]:
        print(f"⛔ 만료 처리됨: {', '.join(report['expired_now'])} — 해당 단계 재실행 필요")
    for w in report["config_warnings"]:
        print(f"⚠️ {w}")
    if errors:
        print("⛔ config 오류 — 실행 중단 (에스컬레이션):")
        for e in errors:
            print(f"   {e}")
        sys.exit(1)
    print(f"✅ state-audit 완료 → output/{args.run_id}/00_state_audit.json")


if __name__ == "__main__":
    main()
