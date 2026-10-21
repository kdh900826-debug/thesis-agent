# -*- coding: utf-8 -*-
"""승인 큐 관리 (D6·D10, F17·F19).
사용:
  python approvals.py list
  python approvals.py add --type thesis_patch|version_publish --artifact <path>
  python approvals.py approve <approval_id>
  python approvals.py reject <approval_id> --note "<사유>"
approve(thesis_patch): 카드 백업 → before→after 적용 → version_history 이력 추가.
패치 artifact는 .md와 나란히 동일 이름의 .json(ThesisPatch 스키마)이 있어야 자동 적용 가능.
"""
import argparse, json, shutil, sys
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
QUEUE = ROOT / "state" / "pending_approvals.json"


def load_queue():
    return json.loads(QUEUE.read_text(encoding="utf-8-sig"))


def save_queue(q):
    QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")


def find(q, aid):
    for e in q["queue"]:
        if e["approval_id"] == aid:
            return e
    return None


def cmd_list(q):
    if not q["queue"]:
        print("승인 큐 비어 있음")
    for e in q["queue"]:
        print(f"{e['approval_id']}  [{e['status']}]  {e.get('type')}  {e.get('artifact')}  (created {e.get('created_at')})")


def cmd_add(q, args):
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    aid = f"ap_{ts}_{args.type}_{Path(args.artifact).stem.lower()}"
    q["queue"].append({
        "approval_id": aid, "type": args.type, "artifact": args.artifact,
        "created_at": date.today().isoformat(), "expires_after_days": 14,
        "status": "pending", "resolved_at": None, "note": None,
    })
    save_queue(q)
    print(f"✅ 큐 등재: {aid}")


def is_expired(e):
    try:
        created = datetime.fromisoformat(e["created_at"]).date()
    except (ValueError, TypeError):
        return False
    return (date.today() - created).days > e.get("expires_after_days", 14)


def verify_after_apply(card, p):
    """F20 — 적용 직후 검증. 위반 목록을 반환한다(빈 목록 = 통과).
    기본 검사: YAML 파싱 + after 문자열 존재. 패치 JSON의 expected_after로 추가 검사:
      {"contains": [...], "not_contains": [...], "counts": [{"path": "a.b", "n": 13}, ...]}
    """
    errs = []
    text = card.read_text(encoding="utf-8-sig")
    data = None
    try:
        import yaml
        data = yaml.safe_load(text)
    except ImportError:
        errs.append("F20: PyYAML 부재 — 파싱 검증 불가")
    except Exception as e:
        errs.append(f"F20: 적용 후 YAML 파싱 실패 — {str(e).splitlines()[0][:80]}")
    after = p.get("after")
    if after and after not in text:
        errs.append("F20: after 문자열이 적용 후 카드에 없음")
    exp = p.get("expected_after") or {}
    for s in exp.get("contains", []):
        if s not in text:
            errs.append(f"F20: contains 실패 — '{s[:40]}'")
    for s in exp.get("not_contains", []):
        if s in text:
            errs.append(f"F20: not_contains 실패 — '{s[:40]}'가 잔존")
    for c in exp.get("counts", []):
        if data is None:
            errs.append(f"F20: counts 검사 불가(YAML 미파싱) — {c.get('path')}")
            continue
        node = data
        for k in str(c.get("path", "")).split("."):
            if isinstance(node, dict) and k in node:
                node = node[k]
            else:
                node = None
                break
        if node is None or not hasattr(node, "__len__"):
            errs.append(f"F20: counts 경로 없음/계수 불가 — {c.get('path')}")
        elif len(node) != c.get("n"):
            errs.append(f"F20: counts 불일치 — {c.get('path')} = {len(node)}개 (기대 {c.get('n')}개)")
    return errs


def unique_backup_path(bdir, ticker):
    """충돌 없는 백업 경로. 마이크로초 타임스탬프 + 존재 시 순번 접미 — 기존 백업을 절대 덮어쓰지 않는다(P9)."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    p = bdir / f"{ticker}_{ts}.yaml"
    n = 1
    while p.exists():
        p = bdir / f"{ticker}_{ts}_{n}.yaml"
        n += 1
    return p


def apply_thesis_patch(entry):
    """D10: 백업 → 문자열 치환 적용 → 이력 추가. 실패 시 아무것도 쓰지 않는다."""
    pj = Path(str(ROOT / entry["artifact"])).with_suffix(".json")
    if not pj.exists():
        pj = ROOT / (entry["artifact"].rsplit(".", 1)[0] + ".json")
    if not pj.exists():
        print(f"⛔ 패치 JSON 부재: {pj} — 자동 적용 불가. reject 후 재생성 필요")
        return False
    patch = json.loads(pj.read_text(encoding="utf-8-sig"))
    patches = patch if isinstance(patch, list) else [patch]

    for p in patches:
        ticker = p["ticker"].upper()
        card = ROOT / "state" / "thesis_cards" / f"{ticker}.yaml"
        text = card.read_text(encoding="utf-8-sig")
        before, after = p.get("before"), p.get("after")
        if p.get("operation") in ("amend", "decompose") and before:
            if before not in text:
                print(f"⛔ {ticker}: before 문자열을 카드에서 찾지 못함 — 수동 검토 필요")
                return False
        # 백업 (적용 전) — P9 백업 유일성: 같은 초에 2건 승인 시 덮어쓰기 방지
        # (2026-09-20 CRWV_20260920_080500.yaml 충돌 사건 — 초 단위 타임스탬프가 원인)
        bdir = ROOT / "state" / "thesis_cards" / "backup"
        bdir.mkdir(exist_ok=True)
        backup_path = unique_backup_path(bdir, ticker)
        shutil.copy2(card, backup_path)
        # 적용 (P9 — 정정 표기: 이력 블록에 before 보존)
        if before and after:
            text = text.replace(before, after, 1)
        # change 문자열은 YAML 단일따옴표 스칼라로 기록 — before 발췌의 따옴표·줄바꿈이 YAML을 깨지 않도록 정규화
        excerpt = " / ".join(str(before)[:60].split())
        change = (f'ThesisPatch 적용({p.get("card_field","?")}/{p.get("operation","?")}) '
                  f'— 근거: {",".join(p.get("basis_claims", []))} / 이전: {excerpt}...').replace("'", "''")
        hist = f'  - {{date: "{date.today().isoformat()}", change: \'{change}\'}}\n'
        marker = "version_history:\n"
        idx = text.find(marker)
        if idx >= 0:
            ins = idx + len(marker)
            text = text[:ins] + hist + text[ins:]
        card.write_text(text, encoding="utf-8")
        # F20 — 적용 직후 검증. 실패 시 이 패치분만 자동 원복하고 중단(승인 미확정 유지)
        errs = verify_after_apply(card, p)
        if errs:
            shutil.copy2(backup_path, card)
            print(f"⛔ {ticker} 적용 후 검증 실패 → 백업 원복 완료 (backup/{backup_path.name}):")
            for x in errs:
                print(f"   - {x}")
            print("   패치 내용을 수정 후 재시도하라. 오류 경위는 P9에 따라 승인 큐 note에 기록할 것.")
            return False
        print(f"✅ {ticker} 카드에 패치 적용 + F20 검증 통과 (백업: backup/{backup_path.name})")
    return True


def cmd_resolve(q, aid, approve, note=None):
    e = find(q, aid)
    if e is None:
        print(f"⛔ 큐에 {aid} 없음")
        sys.exit(1)
    if e["status"] != "pending":
        print(f"⛔ {aid} status={e['status']} — pending 건만 처리 가능")
        sys.exit(1)
    if is_expired(e):
        e["status"] = "expired"
        save_queue(q)
        print(f"⛔ {aid} 만료(14일 초과) — 승인 불가. 해당 단계를 재실행하세요 (D6)")
        sys.exit(1)
    if not approve:
        e["status"] = "rejected"
        e["note"] = note
        e["resolved_at"] = date.today().isoformat()
        save_queue(q)
        print(f"✅ {aid} 반려 → ESCALATED (사유: {note})")
        return
    if e["type"] == "thesis_patch":
        if not apply_thesis_patch(e):
            sys.exit(1)
    e["status"] = "approved"
    e["resolved_at"] = date.today().isoformat()
    save_queue(q)
    print(f"✅ {aid} 승인 완료" + (" — version_publish.py로 발행을 진행하세요" if e["type"] == "version_publish" else ""))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p_add = sub.add_parser("add")
    p_add.add_argument("--type", required=True, choices=["thesis_patch", "version_publish"])
    p_add.add_argument("--artifact", required=True)
    p_app = sub.add_parser("approve")
    p_app.add_argument("approval_id")
    p_rej = sub.add_parser("reject")
    p_rej.add_argument("approval_id")
    p_rej.add_argument("--note", default="")
    args = ap.parse_args()

    q = load_queue()
    if args.cmd == "list":
        cmd_list(q)
    elif args.cmd == "add":
        cmd_add(q, args)
    elif args.cmd == "approve":
        cmd_resolve(q, args.approval_id, True)
    elif args.cmd == "reject":
        cmd_resolve(q, args.approval_id, False, args.note)


if __name__ == "__main__":
    main()
