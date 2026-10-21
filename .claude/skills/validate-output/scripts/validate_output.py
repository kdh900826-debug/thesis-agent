# -*- coding: utf-8 -*-
"""validate-output — 발행 전 결정론 게이트 (P1~P17, F13~F19).
사용: python validate_output.py <산출물.json> --layer <layer> [--queue state/pending_approvals.json --approval-id <id>]
종료코드 0 = PASS, 1 = REJECT(위반 목록 출력), 2 = 실행 오류
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # thesis-agent/

GRADE_ORDER = ["🔴🔴", "🔴", "🟠", "🟡", "🟢"]

# P15/F18 — 지시 동사·목표 비중 단일값
DIRECTIVE_PATTERNS = [
    r"매수(?!·매도 지시가 아니)", r"매도(?! 지시가 아니)", r"사세요", r"파세요", r"익절", r"손절",
    r"\d+(\.\d+)?\s*%\s*(로|까지)\s*(축소|확대|조정|리밸런싱)",
    r"목표\s*비중\s*[:=]?\s*\d+(\.\d+)?\s*%",
]
# P14/F15 — 수치형 상관계수
COEFF_PATTERNS = [r"상관\s*(계수)?\s*[-+]?[01]?\.\d+", r"correlation\s*(coefficient)?\s*[-+]?[01]?\.\d+"]
# D3/F14 — 매크로 전망 서사
NARRATIVE_PATTERNS = [r"할 것으로 (보인다|예상)", r"전망(이다|된다)", r"가능성이 (높다|크다)", r"시나리오상", r"인하가 예상", r"인상이 예상"]


def all_text(obj):
    """중첩 구조의 모든 문자열을 순회."""
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from all_text(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from all_text(v)


def find_patterns(obj, patterns, skip_keys=()):
    hits = []
    def walk(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in skip_keys:
                    continue
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, str):
            for p in patterns:
                if re.search(p, o):
                    hits.append((path, p, o[:80]))
    walk(obj)
    return hits


def check_common(data, v):
    if "as_of" not in data:
        v.append("P16: 최상위 as_of 부재")
    def walk(o, path=""):
        if isinstance(o, dict):
            if "reused_from" in o and "staleness_days" not in o:
                v.append(f"P16: {path} reused_from 있으나 staleness_days 부재")
            for k, val in o.items():
                walk(val, f"{path}.{k}")
        elif isinstance(o, list):
            for i, val in enumerate(o):
                walk(val, f"{path}[{i}]")
    walk(data)


def check_company(data, v):
    for c in data.get("claims", []):
        cid = c.get("id", "?")
        for f in ("claim_type", "scope", "evidence_grade"):
            if f not in c:
                v.append(f"P1/P4: claim {cid} 필수 필드 {f} 부재")
        if c.get("claim_type") == "fact":
            if not c.get("source", {}).get("url"):
                v.append(f"P4: fact claim {cid} source.url 부재")
            if c.get("evidence_grade") not in (1, 2) and c.get("confirmed", True):
                v.append(f"P4: fact claim {cid} grade 3·4인데 confirmed=true (삼각검증용 — 단독 근거 불가)")
        if c.get("claim_type") == "inference" and not c.get("inference_strength"):
            v.append(f"P1: inference claim {cid} 강도 부재")
    for t in all_text(data):
        if re.search(r"(확인되지 않|찾지 못).{0,10}(없다|없음|아니다)", t):
            v.append(f"P5/F10: 정보 부재를 반증으로 사용 의심 — '{t[:60]}'")


def check_signal(data, v):
    for c in data.get("claims", data.get("input_claims", [])):
        if c.get("scope") != "company_specific":
            v.append(f"P6/P13/F13: scope={c.get('scope')} claim이 signal 입력에 존재 (id={c.get('id','?')})")
    prior, proposed = data.get("prior_signal"), data.get("proposed_signal")
    if prior in GRADE_ORDER and proposed in GRADE_ORDER:
        if GRADE_ORDER.index(proposed) > GRADE_ORDER.index(prior):  # 상향
            g = data.get("gate_check", {})
            for gate in ("quantitative_evidence", "company_specific", "revenue_recognized"):
                if not g.get(gate):
                    v.append(f"P2/P6/P7/F5: 상향 판정인데 게이트 {gate} 미충족/부재")
    alert = data.get("alert", {})
    if alert:
        need = ["ticker_event", "facts", "inference", "classification", "thesis_delta", "signal_verdict", "next_check"]
        for f in need:
            if not alert.get(f):
                v.append(f"7필드 알림: {f} 누락")


def check_macro(data, v):
    hits = find_patterns(data, NARRATIVE_PATTERNS, skip_keys=("consequence",))
    for path, p, s in hits:
        v.append(f"D3/F14: 전망 서사 의심 {path} — '{s}'")
    for kc in data.get("kc_status", data if isinstance(data, list) else []):
        if isinstance(kc, dict) and kc.get("verdict"):
            if kc.get("verdict") == "not_met" and kc.get("verdict_confidence") != "provisional":
                stale = any(i.get("stale_days", 0) > i.get("stale_limit", 9999) for i in kc.get("inputs", []))
                if stale:
                    v.append(f"P16/F7: {kc.get('kc_id')} stale 입력인데 not_met 확정")


def check_sector(data, v):
    if data.get("signal_mutation") is not None:
        v.append("P13: signal_mutation이 null이 아님 — 개별 등급 변경 불가")
    for k in data.keys():
        if "signal" in k.lower() and "mutation" not in k.lower():
            v.append(f"P13 의심: 섹터 산출물에 시그널 관련 필드 '{k}'")


def check_correlation(data, v):
    if data.get("coefficient_used") is not False:
        v.append("P14/F15: coefficient_used가 false가 아님")
    for path, p, s in find_patterns(data, COEFF_PATTERNS):
        v.append(f"P14/F15: 수치형 상관계수 표기 {path} — '{s}'")
    for pair in data.get("pair_overlap", []):
        if pair.get("grade") not in ("상", "중", "하"):
            v.append(f"P14: pair {pair.get('pair')} grade가 상/중/하가 아님: {pair.get('grade')}")


def check_portfolio(data, v):
    for path, p, s in find_patterns(data, DIRECTIVE_PATTERNS, skip_keys=("predefined_consequence", "source", "_comment")):
        v.append(f"P15/F18: 지시성 표현 {path} — '{s}'")
    if data.get("default_action") not in ("no_action", None):
        pass
    if "default_action" not in data:
        v.append("P12: default_action 필드 부재 (기본값 no_action 명시 필요)")
    for sc in data.get("scenarios", []):
        if not sc.get("source"):
            v.append(f"P11: 시나리오 '{sc.get('trigger','?')}'가 사전 정의 KC·한도에 연결되지 않음 (source 부재)")


def check_thesis_patch(data, v):
    patches = data if isinstance(data, list) else [data]
    for p in patches:
        if not p.get("basis_claims"):
            v.append(f"S7: 패치({p.get('ticker','?')}/{p.get('card_field','?')}) basis_claims 부재")
        if p.get("requires_human_approval") is not True:
            v.append("F17: requires_human_approval이 true가 아님")
        if p.get("operation") == "add_kc":
            txt = json.dumps(p.get("after", ""), ensure_ascii=False)
            if not re.search(r"\d", txt):
                v.append("P11: add_kc 패치에 정량 임계 부재")


def check_publish(args, v):
    if not args.queue or not args.approval_id:
        v.append("F19: publish 검증에는 --queue와 --approval-id가 필요")
        return
    q = json.loads(Path(args.queue).read_text(encoding="utf-8-sig"))
    entry = next((e for e in q.get("queue", []) if e.get("approval_id") == args.approval_id), None)
    if entry is None:
        v.append(f"F19: 승인 큐에 {args.approval_id} 없음")
    elif entry.get("status") != "approved":
        v.append(f"F19: {args.approval_id} status={entry.get('status')} — approved 아님. 발행 불가")


CHECKS = {
    "company": check_company, "signal": check_signal, "macro": check_macro,
    "sector": check_sector, "correlation": check_correlation,
    "portfolio": check_portfolio, "thesis_patch": check_thesis_patch,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact")
    ap.add_argument("--layer", required=True)
    ap.add_argument("--queue")
    ap.add_argument("--approval-id")
    args = ap.parse_args()

    violations = []
    if args.layer == "publish":
        check_publish(args, violations)
    else:
        try:
            data = json.loads(Path(args.artifact).read_text(encoding="utf-8-sig"))
        except Exception as e:
            print(f"ERROR: 산출물 로드 실패 — {e}")
            sys.exit(2)
        check_common(data, violations)
        fn = CHECKS.get(args.layer)
        if fn is None:
            print(f"ERROR: 알 수 없는 layer '{args.layer}'")
            sys.exit(2)
        fn(data, violations)

    if violations:
        print(f"REJECT ({len(violations)}건):")
        for x in violations:
            print(f"  - {x}")
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
