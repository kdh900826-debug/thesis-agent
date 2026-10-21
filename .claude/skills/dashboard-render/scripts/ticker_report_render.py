# -*- coding: utf-8 -*-
"""종목별 상세 리포트(사람 열람용 정적 HTML) — run 산출물을 종목 단위로 재구성한다.
사용: python ticker_report_render.py --run-id 20260919_2209 [--out output/<run>/ticker_report.html]
입력(읽기만): 02_company/{T}.json · 03_signal/{T}.json · 03_kc_excerpt/{T}.json · 07_thesis_patch/*.json
             state/thesis_cards/{T}.yaml · state/signals.json · state/pending_approvals.json
원칙: 산출물을 재판정·요약하지 않고 그대로 노출한다(P1 태그·등급·후보 문구 보존). 등급 확정은 사람.
"""
import argparse, html, json, re
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
TICKERS = ["IREN", "NBIS", "CRWV", "MU", "CRCL", "COIN", "HOOD"]
SECTOR = {"IREN": "neocloud", "NBIS": "neocloud", "CRWV": "neocloud", "MU": "memory",
          "CRCL": "stablecoin", "COIN": "stablecoin", "HOOD": "stablecoin"}
SIG_CLASS = {"🟢": "s-green", "🟡": "s-yellow", "🟠": "s-orange", "🔴": "s-red", "🔴🔴": "s-kill"}
DIR_KO = {"strengthen": "강화", "weaken": "약화", "neutral": "중립", "mixed": "혼재", "break": "훼손"}


def esc(x):
    return html.escape("" if x is None else str(x), quote=True)


def load_json(p):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else None


def tag_text(s):
    """[fact]/[inference:..] 접두 태그를 칩으로 변환. 태그 없는 문장은 그대로."""
    s = esc(s)
    s = re.sub(r"\[(fact)\]", r'<span class="tag t-fact">fact</span>', s)
    s = re.sub(r"\[(inference)(?::([^\]]*))?\]", lambda m: f'<span class="tag t-inf">inference{(" · " + m.group(2)) if m.group(2) else ""}</span>', s)
    # arbiter 변형 표기: [P1] / [출처·시각] / [정량, 최우선] 류 짧은 대괄호 라벨 → 중립 칩
    s = re.sub(r"\[(P\d{1,2}|[^\[\]]{1,14})\]", lambda m: f'<span class="tag t-lbl">{m.group(1)}</span>', s)
    return s


_CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮"


def alert_field(v):
    """Alert 필드는 arbiter 산출물 간 타입이 제각각(str/list/dict)이다 — 전부 흡수해 문자 단위로 쪼개지는 일이 없게 한다."""
    def one(x):
        if isinstance(x, dict):
            txt = x.get("text") or x.get("summary") or ""
            if not txt:
                return "<dl class='mini'>" + "".join(f"<dt>{esc(k)}</dt><dd>{tag_text(val) if isinstance(val, str) else esc(json.dumps(val, ensure_ascii=False))}</dd>" for k, val in x.items()) + "</dl>"
            extra = [esc(x.get("source")), esc(x.get("timestamp")), esc(x.get("inference_strength"))]
            extra = " · ".join(e for e in extra if e)
            return tag_text(txt) + (f" <span class='small'>— {extra}</span>" if extra else "")
        return tag_text(x)
    if v is None or v == "":
        return "<span class='empty'>—</span>"
    if isinstance(v, list):
        return "<ul>" + "".join(f"<li>{one(x)}</li>" for x in v) + "</ul>"
    if isinstance(v, dict):
        return one(v)
    s = str(v)
    marks = [c for c in _CIRC if c in s]
    if len(marks) >= 2:  # "① … ② …" 한 문자열 → 항목 분리
        parts = re.split(r"(?=[" + _CIRC + r"])", s)
        parts = [p.strip() for p in parts if p.strip()]
        return "<ol class='circ'>" + "".join(f"<li>{tag_text(p)}</li>" for p in parts) + "</ol>"
    return tag_text(s)


def sig_chip(sig, label=None, small=False):
    cls = SIG_CLASS.get(sig, "s-none")
    return f'<span class="sig {cls}{" sm" if small else ""}">{esc(sig)}{(" " + esc(label)) if label else ""}</span>'


def grade_badge(g):
    if g in (None, "", "N/A"):
        return '<span class="grade g-na">—</span>'
    return f'<span class="grade g{esc(g)}">G{esc(g)}</span>'


def dir_chip(d):
    d = (d or "").lower()
    return f'<span class="dir d-{esc(d) or "none"}">{esc(DIR_KO.get(d, d or "—"))}</span>'


def li(items, fmt=lambda x: tag_text(x)):
    return "".join(f"<li>{fmt(i)}</li>" for i in items)


def render_ticker(t, run_id, card, comp, sig, kc, patches, applied_ids):
    sector = SECTOR[t]
    prior, proposed = sig.get("prior_signal", "?"), sig.get("proposed_signal", "?")
    kill = sig.get("kill_check", {})
    kill_on = bool(kill.get("kill_priority_triggered") or kill.get("triggered"))
    if not kill.get("kill_trigger_kc") and kill.get("trigger_source"):
        kill = dict(kill, kill_trigger_kc=[kill.get("trigger_source")])
    gate = sig.get("gate_check", {})
    up = gate.get("upgrade_gate", {}); cond = up.get("conditions", {})
    down = gate.get("downgrade_check", {})
    alert = sig.get("alert", {})
    claims = comp.get("claims", [])
    deltas = comp.get("deltas", [])
    unconf = comp.get("unconfirmed", [])
    noise = comp.get("discarded_noise_log", [])
    lb = comp.get("lookback_window", {})
    axes_label = {a.get("id"): a.get("label", "") for a in card.get("axes", [])}
    claim_by_id = {c.get("id"): c for c in claims}
    grades = [c.get("evidence_grade") for c in claims if c.get("claim_type") == "fact"]
    g_cnt = {g: grades.count(g) for g in (1, 2, 3, 4)}
    n_fact = sum(1 for c in claims if c.get("claim_type") == "fact")
    n_inf = len(claims) - n_fact
    d_cnt = {k: sum(1 for d in deltas if d.get("direction") == k) for k in ("strengthen", "weaken", "neutral")}

    # ── 헤더
    kill_kcs = ", ".join(k.get("kc_id", "") if isinstance(k, dict) else str(k) for k in kill.get("kill_trigger_kc", []))
    head = f"""
<header class="thead">
  <div class="trow">
    <div><span class="eyebrow">{esc(sector)}</span><h2>{t}</h2></div>
    <div class="transition">{sig_chip(prior, sig.get("prior_label"))}<span class="arrow">→</span>{sig_chip(proposed)}<span class="cand">후보</span></div>
  </div>
  <p class="thesis">{esc(card.get("thesis", "")).strip()}</p>
  <div class="kv">
    <div><dt>판정 성격</dt><dd>{tag_text(sig.get("transition_candidate", ""))}</dd></div>
    <div><dt>다음 게이트</dt><dd>{tag_text(sig.get("next_gate") or sig.get("prior_next_gate", ""))}</dd></div>
    <div><dt>조사 창</dt><dd><code>{esc(lb.get("since"))} → {esc(lb.get("until"))}</code> · 1차 사건일 {esc(comp.get("underlying_primary_event_date"))} · staleness {esc(comp.get("staleness_days"))}일</dd></div>
  </div>
  {"<div class='banner kill'><strong>Kill 우선 규칙 발동</strong> — " + esc(kill_kcs) + ". " + tag_text(kill.get("conclusion", "")) + "</div>" if kill_on else ""}
</header>"""

    # ── 게이트 체크
    def chk(v):
        return '<span class="chk ok">충족</span>' if v else '<span class="chk no">미충족</span>'
    gate_html = f"""
<section><h3>등급 판정 근거 <small>arbiter 규칙 — 확정은 사람</small></h3>
<div class="gates">
  <div class="gate"><div class="gname">규칙1 · Kill 우선</div><div class="gval">{'<span class="chk kill">트리거</span>' if kill_on else '<span class="chk ok">미해당</span>'}</div><p>{tag_text(kill.get("conclusion", ""))}</p></div>
  <div class="gate"><div class="gname">규칙2 · 상향 게이트</div><div class="gval">{chk(up.get("met"))}</div>
    <ul class="conds"><li>정량 근거 {chk(cond.get("quantitative_evidence"))}</li><li>회사 고유 {chk(cond.get("company_specific"))}</li><li>매출 인식 단계 {chk(cond.get("revenue_recognized"))}</li></ul>
    <p>{tag_text(up.get("basis", ""))}</p></div>
  <div class="gate"><div class="gname">규칙3 · 하향(비대칭)</div><div class="gval">{'<span class="chk no">트리거</span>' if down.get("met") else '<span class="chk ok">미해당</span>'}</div>
    <ul class="conds"><li>정량 훼손 {'있음' if down.get("quantitative_deterioration") else '없음'}</li><li>grade≤2 정성 훼손 {'있음' if down.get("qualitative_deterioration_grade_le_2") else '없음'}</li></ul>
    <p>{tag_text(down.get("basis", ""))}</p></div>
</div></section>"""

    # ── 축 Delta
    rows = []
    for d in deltas:
        ax = d.get("axis", "")
        sup = d.get("supporting_claims", []) or []
        sup_html = " ".join(f'<a href="#{t}-{esc(c)}" class="cid">{esc(c)}</a>' for c in sup)
        rt = d.get("risk_transfer_to") or []
        rt_html = (" · 리스크 이관 → " + esc(", ".join(map(str, rt)))) if rt else ""
        rows.append(f"""
<details class="axis">
  <summary><span class="axid">{esc(ax)}</span>{dir_chip(d.get("direction"))}<span class="axlabel">{esc(axes_label.get(ax, ""))[:140]}</span></summary>
  <div class="axbody">
    {"<div class='stage'><dt>단계</dt><dd>" + esc(d.get("stage")) + "</dd></div>" if d.get("stage") else ""}
    <div><dt>직전 상태</dt><dd>{tag_text(d.get("prior_state", ""))}</dd></div>
    <div><dt>이번 회차</dt><dd>{tag_text(d.get("new_state", ""))}</dd></div>
    {"<div><dt>주의</dt><dd>" + tag_text(d.get("caveat")) + "</dd></div>" if d.get("caveat") else ""}
    <div><dt>근거 Claim</dt><dd>{sup_html or "—"}{rt_html}</dd></div>
  </div>
</details>""")
    delta_html = f"""
<section><h3>Thesis 축 Delta <small>{len(deltas)}축 · 강화 {d_cnt['strengthen']} / 약화 {d_cnt['weaken']} / 중립 {d_cnt['neutral']}</small></h3>
{"".join(rows) or "<p class='empty'>Delta 없음</p>"}</section>"""

    # ── Claims
    crows = []
    for c in claims:
        src = c.get("source") or {}
        url = src.get("url") if isinstance(src, dict) else None
        stype = (src.get("type") if isinstance(src, dict) else src) or ""
        filed = src.get("filed_at") if isinstance(src, dict) else ""
        link = f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(stype or url)}</a>' if url else esc(stype)
        flags = []
        if c.get("out_of_window"): flags.append('<span class="flag">창 밖</span>')
        if c.get("confirmed") is False: flags.append('<span class="flag warn">unconfirmed</span>')
        if c.get("scope") and c.get("scope") != "company_specific": flags.append(f'<span class="flag">{esc(c.get("scope"))}</span>')
        crows.append(f"""
<article class="claim" id="{t}-{esc(c.get('id'))}">
  <div class="cmeta">{grade_badge(c.get("evidence_grade"))}<span class="tag {'t-fact' if c.get('claim_type')=='fact' else 't-inf'}">{esc(c.get("claim_type"))}{(" · " + esc(c.get("inference_strength"))) if c.get("inference_strength") else ""}</span>{"".join(flags)}<span class="cid mono">{esc(c.get("id"))}</span></div>
  <p>{esc(c.get("text"))}</p>
  <div class="csrc">출처 {link}{(" · " + esc(filed)) if filed else ""}{("<div class='cnote'>" + esc(c.get("note")) + "</div>") if c.get("note") else ""}</div>
</article>""")
    claims_html = f"""
<section><h3>확정 사실·추론 <small>fact {n_fact} · inference {n_inf} · 등급 G1 {g_cnt[1]} / G2 {g_cnt[2]} / G3 {g_cnt[3]} / G4 {g_cnt[4]}</small></h3>
<p class="hint">G1 1차 공시 · G2 경영진 직접 발언 · G3 2차 매체 · G4 애그리게이터. G3·G4는 삼각검증용이며 단독 판단 근거가 될 수 없다(P4).</p>
{"".join(crows) or "<p class='empty'>신규 Claim 없음 — 정보 부재는 반증이 아니다(P5)</p>"}</section>"""

    # ── KC
    def kc_row(k):
        if not isinstance(k, dict):
            k = {"kc_id": str(k), "condition": "(발췌본에 상세 없음)", "verdict": ""}
        v = k.get("verdict", "")
        cls = "kc-met" if v == "met" else "kc-ok"
        conf = k.get("verdict_confidence") or k.get("confidence") or ""
        inputs = k.get("inputs") or []
        ins = " · ".join(f"{esc(i.get('name'))} {esc(i.get('value'))} {esc(i.get('operator'))} {esc(i.get('threshold'))}" + (f" ({esc(i.get('duration'))})" if i.get('duration') else "") for i in inputs if isinstance(i, dict))
        return f"""<tr class="{cls}"><td class="mono">{esc(k.get("kc_id"))}</td><td>{esc(k.get("condition") or k.get("description"))}</td><td><span class="verdict {cls}">{esc(v)}</span> <small>{esc(conf)}</small></td><td class="mono small">{ins or "—"}</td><td class="small">{esc(k.get("consequence") or k.get("note") or k.get("basis") or "")}</td></tr>"""
    own = kill.get("own_company_kc") or []
    if own and not all(isinstance(x, dict) for x in own):
        # arbiter가 id 목록만 남긴 경우 → 발췌본 상세로 대체
        det = kc.get("own_company_kc_detail")
        own = det if isinstance(det, list) and det else own
    macro = kc.get("kc_status") or kill.get("macro_kc_propagating") or []
    kc_html = f"""
<section><h3>Kill Condition 상태</h3>
<h4>종목 전용 KC</h4>
{"<div class='tscroll'><table class='kct'><thead><tr><th>KC</th><th>조건</th><th>판정</th><th>입력</th><th>근거·결과</th></tr></thead><tbody>" + "".join(kc_row(k) for k in own) + "</tbody></table></div>" if own else "<p class='empty'>" + esc(kc.get("own_company_kc") if isinstance(kc.get("own_company_kc"), str) else "종목 전용 KC 미정의") + "</p>"}
<h4>파급되는 매크로 KC <small>노출 벡터상 불리 방향 축에 연결된 것만</small></h4>
<div class="tscroll"><table class="kct"><thead><tr><th>KC</th><th>조건</th><th>판정</th><th>입력</th><th>사전 정의 결과</th></tr></thead><tbody>{"".join(kc_row(k) for k in macro)}</tbody></table></div>
</section>"""

    # ── Alert / 다음 확인
    alert_html = f"""
<section><h3>알림 요약 <small>7필드 Alert</small></h3>
<div class="kv">
  <div><dt>이벤트</dt><dd>{alert_field(alert.get("ticker_event"))}</dd></div>
  <div><dt>확정 사실</dt><dd>{alert_field(alert.get("facts"))}</dd></div>
  <div><dt>추론</dt><dd>{alert_field(alert.get("inference"))}</dd></div>
  <div><dt>분류</dt><dd>{alert_field(alert.get("classification"))}</dd></div>
  <div><dt>Thesis 변화</dt><dd>{alert_field(alert.get("thesis_delta"))}</dd></div>
  <div><dt>신호 판정</dt><dd>{alert_field(alert.get("signal_verdict"))}</dd></div>
  <div><dt>다음 확인</dt><dd>{alert_field(alert.get("next_check"))}</dd></div>
</div></section>"""

    # ── 미확인 / 노이즈 / 패치
    unc_html = f"""
<section><h3>미확인·이월 <small>{len(unconf)}건 — 찾지 못함 ≠ 반증(P5)</small></h3>
<ul class="unc">{"".join(f"<li><strong>{esc(u.get('topic'))}</strong><span class='reason mono'>{esc(u.get('reason'))}</span><p>{esc(u.get('detail'))}</p></li>" for u in unconf) or "<li class='empty'>없음</li>"}</ul></section>"""
    noise_html = f"""
<section><details class="plain"><summary><h3>폐기한 노이즈 <small>{len(noise)}건 — P3 기준</small></h3></summary>
<ul class="noise">{"".join(f"<li><strong>{esc(n.get('title'))}</strong><p>{esc(n.get('reason'))}</p></li>" for n in noise) or "<li class='empty'>없음</li>"}</ul></details></section>"""
    tp = [p for p in patches if p.get("ticker") == t]
    tp_rows = []
    for p in tp:
        pid = p.get("_approval_id", "")
        st = applied_ids.get(pid, "생성")
        dep = p.get("depends_on_human_decision")
        tp_rows.append(f"""<li><div class="pmeta"><span class="chk {'ok' if st=='approved' else 'no'}">{'적용됨' if st=='approved' else esc(st)}</span><span class="mono small">{esc(p.get("card_field_detail") or p.get("card_field"))}</span><span class="mono small">{esc(p.get("operation"))}</span>{("<span class='flag warn'>선행 결정: " + esc(dep) + "</span>") if dep else ""}</div><p>{tag_text(p.get("reason", ""))[:900]}</p></li>""")
    tp_html = f"""
<section><h3>이번 회차 Thesis 카드 패치 <small>{len(tp)}건</small></h3>
<ul class="patches">{"".join(tp_rows) or "<li class='empty'>패치 없음" + ("" if t != "CRCL" else " — 근거 부적격(inference·scope=macro)으로 0건이 정당한 결과") + "</li>"}</ul></section>"""

    concl = f"""<section class="concl"><h3>카드 결론 <small>state/thesis_cards/{t}.yaml · as_of {esc(card.get("as_of"))}</small></h3><p>{esc(card.get("conclusion", "")).strip()}</p></section>"""

    return f'<div class="ticker" id="tk-{t}" hidden>{head}{gate_html}{delta_html}{claims_html}{kc_html}{alert_html}{unc_html}{tp_html}{noise_html}{concl}</div>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    run = ROOT / "output" / a.run_id
    out = Path(a.out) if a.out else run / "ticker_report.html"

    macro = load_json(run / "01_macro_kc.json") or {}
    signals = load_json(ROOT / "state" / "signals.json") or {}
    queue = (load_json(ROOT / "state" / "pending_approvals.json") or {}).get("queue", [])
    applied = {}
    patches = []
    for pj in sorted((run / "07_thesis_patch").glob("*.json")):
        d = load_json(pj)
        if not isinstance(d, dict) or "ticker" not in d or not d.get("before"):
            continue
        rel = f"output/{a.run_id}/07_thesis_patch/{pj.name}"
        for q in queue:
            if q.get("artifact", "").replace("\\", "/") == rel:
                d["_approval_id"] = q.get("id"); applied[q.get("id")] = q.get("status")
        patches.append(d)

    met = [k for k in macro.get("kc_status", []) if k.get("verdict") == "met"]
    tabs, panels = [], []
    for t in TICKERS:
        card = yaml.safe_load((ROOT / "state" / "thesis_cards" / f"{t}.yaml").read_text(encoding="utf-8-sig"))
        comp = load_json(run / "02_company" / f"{t}.json") or {}
        sig = load_json(run / "03_signal" / f"{t}.json") or {}
        kc = load_json(run / "03_kc_excerpt" / f"{t}.json") or {}
        prior, proposed = sig.get("prior_signal", "?"), sig.get("proposed_signal", "?")
        _k = sig.get("kill_check", {})
        kill_on = bool(_k.get("kill_priority_triggered") or _k.get("triggered"))
        tabs.append(f'<button class="tab" data-t="{t}" id="tab-{t}"><span class="tt">{t}</span><span class="tsec">{SECTOR[t]}</span><span class="tsig">{sig_chip(prior, small=True)}<span class="arrow">→</span>{sig_chip(proposed, small=True)}</span>{"<span class='tkill'>KC</span>" if kill_on else ""}</button>')
        panels.append(render_ticker(t, a.run_id, card, comp, sig, kc, patches, applied))

    met_html = " · ".join(f"<strong>{esc(k.get('kc_id'))}</strong> {esc(k.get('verdict'))}/{esc(k.get('verdict_confidence'))}" for k in met) or "발동 없음"
    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Thesis 종목 리포트</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#f6f7f9;--paper:#ffffff;--ink:#1a2330;--ink2:#4a5566;--ink3:#7b8494;--line:#dfe3ea;--line2:#eef0f4;--accent:#0f6e6e;--accent-bg:#e4f2f1;
--fact:#1f5f8b;--fact-bg:#e6f0f8;--inf:#7a4f9e;--inf-bg:#f0e9f7;--good:#1f7a4d;--good-bg:#e3f3ea;--warn:#a8650b;--warn-bg:#fbefd9;--bad:#a83232;--bad-bg:#fbe5e5;--kill:#7a1010;--kill-bg:#f7d6d6;
--g1:#1f5f8b;--g2:#2f7d6f;--g3:#a8650b;--g4:#8a8f99;--sh:0 1px 2px rgba(20,30,50,.06);}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0f1319;--paper:#161b23;--ink:#e6eaf0;--ink2:#aeb6c2;--ink3:#7f8895;--line:#2a3140;--line2:#1f2530;--accent:#4fb3b0;--accent-bg:#12302f;
--fact:#7fb3e0;--fact-bg:#15283a;--inf:#c1a3e0;--inf-bg:#2a1f3a;--good:#5fc48d;--good-bg:#12301f;--warn:#e0a95a;--warn-bg:#3a2a10;--bad:#e07a7a;--bad-bg:#3a1818;--kill:#ff9a9a;--kill-bg:#4a1414;--g1:#7fb3e0;--g2:#7fcbb8;--g3:#e0a95a;--g4:#8a8f99;--sh:none;}}}}
:root[data-theme="dark"]{{--bg:#0f1319;--paper:#161b23;--ink:#e6eaf0;--ink2:#aeb6c2;--ink3:#7f8895;--line:#2a3140;--line2:#1f2530;--accent:#4fb3b0;--accent-bg:#12302f;
--fact:#7fb3e0;--fact-bg:#15283a;--inf:#c1a3e0;--inf-bg:#2a1f3a;--good:#5fc48d;--good-bg:#12301f;--warn:#e0a95a;--warn-bg:#3a2a10;--bad:#e07a7a;--bad-bg:#3a1818;--kill:#ff9a9a;--kill-bg:#4a1414;--g1:#7fb3e0;--g2:#7fcbb8;--g3:#e0a95a;--g4:#8a8f99;--sh:none;}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.65 "IBM Plex Sans KR",-apple-system,"Segoe UI","Noto Sans KR",sans-serif;-webkit-font-smoothing:antialiased}}
.mono,code,.cid{{font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;font-size:.86em}} .small{{font-size:.85em;color:var(--ink2)}}
a{{color:var(--accent)}} h2,h3,h4{{text-wrap:balance;margin:0}}
.wrap{{max-width:1240px;margin:0 auto;padding-block:20px 48px;padding-inline:16px}}
.top{{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:baseline;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:16px}}
.top h1{{font-size:22px;font-weight:600;margin:0;letter-spacing:-.01em}} .top .meta{{color:var(--ink2);font-size:13px}}
.disclaimer{{font-size:12.5px;color:var(--ink2);background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:10px 14px;margin-bottom:16px}}
.macro{{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;font-size:13.5px;margin-bottom:18px;padding:10px 14px;border-left:3px solid var(--bad);background:var(--bad-bg);border-radius:0 6px 6px 0}}
.layout{{display:grid;grid-template-columns:232px 1fr;gap:24px;align-items:start}}
nav.rail{{position:sticky;top:env(safe-area-inset-top,0px);display:flex;flex-direction:column;gap:6px}}
.tab{{display:grid;grid-template-columns:1fr auto;grid-template-areas:"tt tkill" "tsec tsec" "tsig tsig";gap:2px 6px;text-align:left;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:10px 12px;cursor:pointer;color:var(--ink);font:inherit;box-shadow:var(--sh)}}
.tab:hover{{border-color:var(--accent)}} .tab[aria-selected="true"]{{border-color:var(--accent);background:var(--accent-bg)}} .tab:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.tab .tt{{grid-area:tt;font-weight:700;letter-spacing:.02em}} .tab .tsec{{grid-area:tsec;font-size:11.5px;color:var(--ink3);text-transform:uppercase;letter-spacing:.06em}} .tab .tsig{{grid-area:tsig;display:flex;gap:4px;align-items:center;margin-top:2px}} .tab .tkill{{grid-area:tkill;font-size:10.5px;font-weight:700;color:var(--kill);background:var(--kill-bg);border-radius:4px;padding:0 5px;align-self:start}}
.arrow{{color:var(--ink3);margin:0 4px}}
main{{min-width:0}} .ticker{{display:flex;flex-direction:column;gap:18px}}
section{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:18px 20px}} section h3{{font-size:16px;font-weight:600;margin-bottom:12px;display:flex;flex-wrap:wrap;gap:8px;align-items:baseline}} section h3 small,section h4 small{{font-weight:400;font-size:12.5px;color:var(--ink3)}} section h4{{font-size:13.5px;color:var(--ink2);margin:14px 0 8px}}
.thead{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:20px 22px}} .trow{{display:flex;flex-wrap:wrap;gap:12px 20px;justify-content:space-between;align-items:center}} .eyebrow{{font-size:11.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--ink3)}} .thead h2{{font-size:30px;font-weight:700;letter-spacing:-.01em;line-height:1.1}}
.transition{{display:flex;align-items:center;gap:6px;flex-wrap:wrap}} .cand{{font-size:11.5px;color:var(--ink3);border:1px dashed var(--line);border-radius:4px;padding:0 6px}}
.thesis{{margin:12px 0 0;color:var(--ink2);max-width:70ch}}
.sig{{display:inline-flex;align-items:center;gap:4px;border-radius:999px;padding:2px 10px;font-size:13px;font-weight:600;border:1px solid transparent}} .sig.sm{{padding:0 7px;font-size:11.5px}}
.s-green{{background:var(--good-bg);color:var(--good)}} .s-yellow{{background:var(--warn-bg);color:var(--warn)}} .s-orange{{background:#fde7d3;color:#9a4a0b}} .s-red{{background:var(--bad-bg);color:var(--bad)}} .s-kill{{background:var(--kill-bg);color:var(--kill);border-color:var(--kill)}} .s-none{{background:var(--line2);color:var(--ink3)}}
:root[data-theme="dark"] .s-orange,:root:not([data-theme="light"]) .s-orange{{background:#3a2410;color:#f0a86a}} @media (prefers-color-scheme: light){{:root:not([data-theme="dark"]) .s-orange{{background:#fde7d3;color:#9a4a0b}}}}
.kv{{display:grid;gap:10px 16px;margin-top:14px}} .kv>div{{display:grid;grid-template-columns:104px 1fr;gap:10px}} .kv dt{{color:var(--ink3);font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;padding-top:3px}} .kv dd{{margin:0;min-width:0;overflow-wrap:anywhere}} .kv ul,.kv ol{{margin:0;padding-left:18px}} .kv li{{margin:3px 0}}
.banner{{margin-top:14px;padding:10px 14px;border-radius:6px;font-size:14px}} .banner.kill{{background:var(--kill-bg);color:var(--ink);border-left:3px solid var(--kill)}}
.tag{{display:inline-block;font-size:10.5px;font-weight:600;letter-spacing:.04em;border-radius:3px;padding:0 5px;margin-right:4px;vertical-align:1px;font-family:"IBM Plex Mono",monospace}} .t-fact{{background:var(--fact-bg);color:var(--fact)}} .t-inf{{background:var(--inf-bg);color:var(--inf)}} .t-lbl{{background:var(--line2);color:var(--ink2)}}
ol.circ{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:4px}} ol.circ li{{overflow-wrap:anywhere}} dl.mini{{margin:0;display:grid;grid-template-columns:auto 1fr;gap:2px 10px;font-size:13.5px}} dl.mini dt{{color:var(--ink3)}} dl.mini dd{{margin:0}}
.gates{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}} .gate{{border:1px solid var(--line2);border-radius:8px;padding:12px 14px;background:var(--bg)}} .gname{{font-size:12.5px;color:var(--ink3);text-transform:uppercase;letter-spacing:.05em}} .gval{{margin:6px 0}} .gate p{{margin:8px 0 0;font-size:13.5px;color:var(--ink2)}} .conds{{list-style:none;padding:0;margin:6px 0 0;display:flex;flex-direction:column;gap:3px;font-size:13px}} .conds li{{display:flex;justify-content:space-between;gap:8px}}
.chk{{display:inline-block;font-size:11.5px;font-weight:600;border-radius:4px;padding:0 7px}} .chk.ok{{background:var(--good-bg);color:var(--good)}} .chk.no{{background:var(--line2);color:var(--ink2)}} .chk.kill{{background:var(--kill-bg);color:var(--kill)}}
.axis{{border-top:1px solid var(--line2)}} .axis:first-of-type{{border-top:0}} .axis summary{{display:flex;flex-wrap:wrap;align-items:center;gap:10px;padding:10px 0;cursor:pointer;list-style:none}} .axis summary::-webkit-details-marker{{display:none}} .axis summary::before{{content:"▸";color:var(--ink3);width:12px}} .axis[open] summary::before{{content:"▾"}}
.axid{{font-family:"IBM Plex Mono",monospace;font-weight:500;font-size:13.5px;min-width:190px}} .axlabel{{color:var(--ink3);font-size:12.5px;flex:1;min-width:200px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.dir{{font-size:11.5px;font-weight:600;border-radius:4px;padding:0 7px}} .d-strengthen{{background:var(--good-bg);color:var(--good)}} .d-weaken{{background:var(--bad-bg);color:var(--bad)}} .d-neutral{{background:var(--line2);color:var(--ink2)}} .d-mixed,.d-break{{background:var(--warn-bg);color:var(--warn)}}
.axbody{{display:grid;gap:8px;padding:4px 0 14px 22px;font-size:14px}} .axbody>div{{display:grid;grid-template-columns:84px 1fr;gap:10px}} .axbody dt{{color:var(--ink3);font-size:12px;text-transform:uppercase;letter-spacing:.05em;padding-top:2px}} .axbody dd{{margin:0;overflow-wrap:anywhere}}
.claim{{border-top:1px solid var(--line2);padding:12px 0}} .claim:first-of-type{{border-top:0;padding-top:4px}} .claim p{{margin:6px 0;overflow-wrap:anywhere}} .cmeta{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}} .cmeta .cid{{margin-left:auto;color:var(--ink3)}} .csrc{{font-size:12.5px;color:var(--ink2)}} .cnote{{margin-top:4px;color:var(--ink3);font-size:12.5px;border-left:2px solid var(--line);padding-left:8px}}
.grade{{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:11.5px;font-weight:600;border-radius:4px;padding:0 6px;color:#fff}} .g1{{background:var(--g1)}} .g2{{background:var(--g2)}} .g3{{background:var(--g3)}} .g4{{background:var(--g4)}} .g-na{{background:var(--line2);color:var(--ink3)}}
.flag{{font-size:10.5px;border-radius:3px;padding:0 5px;background:var(--line2);color:var(--ink2)}} .flag.warn{{background:var(--warn-bg);color:var(--warn)}}
.hint{{font-size:12.5px;color:var(--ink3);margin:-4px 0 10px}} .empty{{color:var(--ink3);font-style:italic}}
.tscroll{{overflow-x:auto}} .kct{{width:100%;min-width:760px;border-collapse:collapse;font-size:13px}} .kct th:nth-child(1){{width:80px}} .kct th:nth-child(2){{width:24%}} .kct th:nth-child(3){{width:120px}} .kct th{{text-align:left;font-weight:600;color:var(--ink3);font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;padding:6px 8px;border-bottom:1px solid var(--line)}} .kct td{{padding:7px 8px;border-bottom:1px solid var(--line2);vertical-align:top}} .kct tr.kc-met td{{background:var(--kill-bg)}}
.verdict{{font-weight:600;border-radius:4px;padding:0 6px;font-size:12px}} .verdict.kc-met{{background:var(--kill);color:#fff}} .verdict.kc-ok{{background:var(--good-bg);color:var(--good)}}
.unc,.noise,.patches{{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}} .unc li,.patches li{{border-top:1px solid var(--line2);padding-top:10px}} .unc li:first-child,.patches li:first-child{{border-top:0;padding-top:0}} .unc strong{{display:inline-block;margin-right:8px}} .unc .reason{{color:var(--ink3);font-size:11.5px}} .unc p,.noise p,.patches p{{margin:4px 0 0;font-size:13.5px;color:var(--ink2);overflow-wrap:anywhere}} .noise li{{font-size:13.5px}} .noise strong{{font-weight:500}}
.pmeta{{display:flex;flex-wrap:wrap;gap:8px;align-items:center}}
details.plain summary{{cursor:pointer;list-style:none}} details.plain summary::-webkit-details-marker{{display:none}} details.plain summary h3{{margin:0}} details.plain[open] summary h3{{margin-bottom:12px}}
.concl p{{margin:0;font-size:15px;max-width:72ch}}
@media (max-width:900px){{.layout{{grid-template-columns:1fr}} nav.rail{{position:static;flex-direction:row;overflow-x:auto;padding-bottom:6px}} .tab{{min-width:150px}} .gates{{grid-template-columns:1fr}} .kv>div,.axbody>div{{grid-template-columns:1fr}} .axlabel{{white-space:normal}}}}
@media (prefers-reduced-motion: no-preference){{.tab{{transition:border-color .15s}}}}
</style></head><body>
<div class="wrap">
  <div class="top"><h1>Thesis 종목 리포트</h1><div class="meta">run <code>{esc(a.run_id)}</code> · L1 as_of {esc(macro.get("as_of"))} · signals.json as_of {esc(signals.get("as_of"))} · 생성 {date.today().isoformat()}</div></div>
  <div class="disclaimer">본 페이지는 에이전트 산출물을 종목 단위로 재구성한 열람용이다. 모든 등급은 <strong>후보</strong>이며 확정 권한은 사람에게 있다. 매수·매도 지시·목표가를 포함하지 않는다. 문장의 <span class="tag t-fact">fact</span> / <span class="tag t-inf">inference</span> 태그와 자료 등급(G1~G4)은 원 산출물 그대로다.</div>
  <div class="macro"><span>매크로 KC 발동</span>{met_html}<span class="small">— 파급 종목은 각 탭의 <em>KC</em> 표시</span></div>
  <div class="layout">
    <nav class="rail" role="tablist" aria-label="종목">{"".join(tabs)}</nav>
    <main>{"".join(panels)}</main>
  </div>
</div>
<script>
(function(){{
  var tabs=[].slice.call(document.querySelectorAll('.tab')),panels={{}};
  tabs.forEach(function(b){{panels[b.dataset.t]=document.getElementById('tk-'+b.dataset.t);}});
  function show(t,push){{
    tabs.forEach(function(b){{b.setAttribute('aria-selected',b.dataset.t===t?'true':'false');}});
    Object.keys(panels).forEach(function(k){{panels[k].hidden=(k!==t);}});
    try{{localStorage.setItem('tk_tab',t);}}catch(e){{}}
    if(push){{try{{history.replaceState(null,'','#'+t);}}catch(e){{}}}}
  }}
  tabs.forEach(function(b){{b.addEventListener('click',function(){{show(b.dataset.t,true);window.scrollTo({{top:0}});}});}});
  document.addEventListener('click',function(e){{var a=e.target.closest('a.cid');if(!a)return;var id=a.getAttribute('href').slice(1);var el=document.getElementById(id);if(el){{e.preventDefault();el.scrollIntoView({{block:'center'}});el.style.outline='2px solid var(--accent)';setTimeout(function(){{el.style.outline='';}},1600);}}}});
  var init=(location.hash||'').slice(1);
  if(!panels[init]){{try{{init=localStorage.getItem('tk_tab');}}catch(e){{}}}}
  if(!panels[init]) init='IREN';
  show(init,false);
}})();
</script>
</body></html>
"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"✅ 종목 리포트 생성: {out}")


if __name__ == "__main__":
    main()
