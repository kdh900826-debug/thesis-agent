# -*- coding: utf-8 -*-
"""dashboard-render — 요청 시에만 실행 (D11). 판정을 새로 생성하지 않는 읽기 전용 요약 HTML.
사용: python dashboard_render.py --out output/dashboard.html
"""
import argparse, html, json
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def age_days(as_of):
    try:
        return (date.today() - datetime.fromisoformat(str(as_of)[:10]).date()).days
    except (ValueError, TypeError):
        return None


def badge(as_of, limit):
    a = age_days(as_of)
    if a is None:
        return '<span class="stale">as_of 없음</span>'
    return f'<span class="{"stale" if a > limit else "fresh"}">{a}일 경과</span>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="output/dashboard.html")
    args = ap.parse_args()

    signals = load_json(ROOT / "state" / "signals.json") or {}
    queue = (load_json(ROOT / "state" / "pending_approvals.json") or {}).get("queue", [])
    runs = sorted((ROOT / "output").glob("*/")) if (ROOT / "output").exists() else []

    # state-audit만 수행된 run 폴더가 실제 산출물을 가리지 않도록,
    # 산출물별로 "그 파일이 존재하는 최신 run"을 각각 찾는다 (P16 — reused_from은 그대로 표기).
    def latest_with(name):
        for r in reversed(runs):
            if (r / name).exists():
                return r
        return None

    kc_run = latest_with("01_macro_kc.json")
    kc = load_json(kc_run / "01_macro_kc.json") if kc_run else None
    corr_run = latest_with("05_correlation.json")
    corr = load_json(corr_run / "05_correlation.json") if corr_run else None

    rows = ""
    for t, g in (signals.get("grades") or {}).items():
        rows += (f"<tr><td>{t}</td><td>{g.get('signal')}</td><td>{html.escape(g.get('label',''))}</td>"
                 f"<td>{html.escape(g.get('next_gate',''))}</td></tr>")

    kc_html = "<p>미실행 — <code>run macro</code> 필요</p>"
    if kc:
        kc_rows = "".join(
            f"<tr><td>{s['kc_id']}</td><td>{'⚠️ MET' if s['verdict']=='met' else '미충족'}</td>"
            f"<td>{s['verdict_confidence']}</td><td>{html.escape(str(s.get('consequence','')))}</td></tr>"
            for s in kc.get("kc_status", []))
        reused = f" / reused_from {kc.get('reused_from')} (staleness {kc.get('staleness_days')}일)" if kc.get("reused_from") else ""
        kc_html = (f"<p>as_of {kc.get('as_of')} {badge(kc.get('as_of'), 5)}{reused}"
                   f" / draft 제외: {', '.join(kc.get('skipped_draft', [])) or '-'}</p>"
                   f"<table><tr><th>KC</th><th>판정</th><th>확신도</th><th>사전 정의 결과</th></tr>{kc_rows}</table>")

    corr_html = "<p>미실행 또는 correlation_matrix draft 상태(U4)</p>"
    if corr:
        c_rows = "".join(
            f"<tr><td>{c['axis']}</td><td>{', '.join(c['tickers'])}</td>"
            f"<td>{c.get('weight_pct_upper') if c.get('weight_pct_upper') is not None else '비중 미기입'}</td>"
            f"<td>{'⚠️ 초과' if c.get('threshold_breach') else '-'}</td></tr>"
            for c in corr.get("axis_concentration", []))
        corr_html = f"<table><tr><th>축</th><th>노출 종목</th><th>비중 상단 합(%)</th><th>임계</th></tr>{c_rows}</table>"

    q_rows = "".join(
        f"<tr><td>{e['approval_id']}</td><td>{e['status']}</td><td>{e.get('type')}</td><td>{e.get('created_at')}</td></tr>"
        for e in queue) or "<tr><td colspan=4>비어 있음</td></tr>"

    page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>thesis-agent dashboard</title>
<style>body{{font-family:'Malgun Gothic',sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;background:#fafafa;color:#222}}
table{{border-collapse:collapse;width:100%;margin:.5rem 0 1.5rem}}td,th{{border:1px solid #ccc;padding:6px 10px;text-align:left;font-size:14px}}
th{{background:#eee}}.stale{{color:#b00;font-weight:bold}}.fresh{{color:#080}}footer{{margin-top:2rem;color:#777;font-size:13px;border-top:1px solid #ddd;padding-top:1rem}}</style></head><body>
<h1>Thesis Agent — 현황 (생성: {datetime.now().isoformat(timespec='minutes')})</h1>
<h2>① 시그널 등급 <small>(as_of {signals.get('as_of')} {badge(signals.get('as_of'), 7)})</small></h2>
<table><tr><th>종목</th><th>등급</th><th>상태</th><th>다음 게이트</th></tr>{rows}</table>
<h2>② 매크로 KC {'(run ' + kc_run.name.strip('\\\\/') + ')' if kc_run else ''}</h2>{kc_html}
<h2>③ 축 집중도 {'(run ' + corr_run.name.strip('\\\\/') + ')' if corr_run else ''}</h2>{corr_html}
<h2>④ 승인 대기 큐</h2><table><tr><th>ID</th><th>상태</th><th>유형</th><th>생성일</th></tr>{q_rows}</table>
<footer>본 대시보드는 판단 보조용 요약이며 매수·매도 지시가 아닙니다. 등급 확정·발행 승인·포지션 행동은 사람이 합니다.</footer>
</body></html>"""

    out = ROOT / args.out if not Path(args.out).is_absolute() else Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"✅ 대시보드 생성: {out}")


if __name__ == "__main__":
    main()
