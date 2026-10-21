# -*- coding: utf-8 -*-
"""dashboard-render v2 — 요청 시에만 실행 (D11). 판정을 새로 생성하지 않는 읽기 전용 요약 HTML.

v2 (2026-09-05): '현재 상태' 나열에서 '임계까지의 거리·방향·시점' 관제판으로 개편.
  ① KC 이격도 보드(근접순·run 시계열 스파크라인) ② 시그널·상향 게이트 체크리스트
  ③ 노출 매트릭스(부호·강도 + 실포지션) ④ 축별 Delta 추이(최근 3 run)
  ⑤ 촉매·관측점(카드 원문) ⑥ 승인 큐·데이터 품질
원칙: 판정 재생성 없음 / 수치형 상관계수 없음(P14) / 매수·매도 동사 없음(P15) /
  stale 데이터를 신선한 것처럼 보이지 않게(P16). 근접도 막대의 채움율만 본 스크립트의
  파생 계산이며(각주 명기) 판정 근거는 항상 원문 이격 문구다.
v1 원본: dashboard_render_v1_backup.py (P9 — 이력 보존)
사용: python dashboard_render.py --out output/dashboard.html
"""
import argparse, html, json, re
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

try:
    import yaml
except ImportError:
    yaml = None

DIR_GLYPH = {  # L2 방향 라벨 정규화 (판정 재해석 아님 — 표기 통일만)
    "strengthen": ("▲", "up", "강화"), "강화": ("▲", "up", "강화"),
    "weaken": ("▼", "dn", "훼손"), "훼손": ("▼", "dn", "훼손"),
    "neutral": ("●", "nu", "중립"), "중립": ("●", "nu", "중립"),
    "mixed": ("◆", "mx", "혼재"), "혼재": ("◆", "mx", "혼재"),
}
STR_KO = {"H": "상", "M": "중", "L": "하"}


def load_json(p):
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def load_yaml(p):
    if yaml is None:
        return None
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def esc(s):
    return html.escape(str(s if s is not None else ""))


def age_days(as_of):
    try:
        return (date.today() - datetime.fromisoformat(str(as_of)[:10]).date()).days
    except (ValueError, TypeError):
        return None


def fresh_badge(as_of, limit=7):
    a = age_days(as_of)
    if a is None:
        return '<span class="b b-stale">as_of 없음</span>'
    cls = "b-stale" if a > limit else "b-fresh"
    warn = "⚠ " if a > limit else ""
    return f'<span class="b {cls}">{warn}{a}일 경과</span>'


def fmt_num(v):
    if v is None:
        return "—"
    try:
        f = float(v)
    except (TypeError, ValueError):
        return esc(v)
    if abs(f) >= 1e9:
        return f"{f/1e9:,.2f}B"
    if abs(f) >= 1e6:
        return f"{f/1e6:,.1f}M"
    if f == int(f) and abs(f) < 1e6:
        return f"{int(f):,}"
    return f"{f:,.2f}"


# ── KC 근접도 (파생 계산 — 각주로 명기) ─────────────────────────────
def leg_fill(inp, hist_vals):
    """단일 레그의 근접도 0~1 (1=임계 접촉). |임계|>0이면 1-|gap|/|임계|,
    임계=0이면 run 시계열 범위를 분모로(범위 없으면 0 — 산출 불가는 낮게)."""
    v, t = inp.get("value"), inp.get("threshold")
    if v is None or t is None:
        return None
    try:
        v, t = float(v), float(t)
    except (TypeError, ValueError):
        return None
    gap = abs(v - t)
    if t != 0:
        return max(0.0, min(1.0, 1 - gap / abs(t)))
    rng = (max(hist_vals) - min(hist_vals)) if len(hist_vals) >= 2 else 0
    if rng > 0:
        return max(0.0, min(1.0, 1 - gap / rng))
    return 0.0


def kc_fill_class(fill):
    if fill is None:
        return None, "b-clear", "◇ 이벤트/산출불가", ""
    if fill >= 0.98:
        return fill, "b-touch", "⛔ 경계 접촉", "f-touch"
    if fill >= 0.75:
        return fill, "b-near", "◮ 근접", "f-near"
    if fill >= 0.50:
        return fill, "b-watch", "△ 주시", "f-watch"
    return fill, "b-clear", "○ 여유", "f-clear"


def gap_text(inp):
    v, t, op = inp.get("value"), inp.get("threshold"), inp.get("operator", "")
    name = inp.get("name", "")
    if v is None or t is None:
        return f"{esc(name)}: 값/임계 미정(이벤트형 또는 미수집)"
    try:
        fv, ft = float(v), float(t)
        gap = fv - ft
        pct = f" ({gap/ft*+100:+.1f}%)" if ft != 0 else ""
        return (f"{esc(name)} {fmt_num(fv)} {esc(op)} 임계 {fmt_num(ft)}"
                f" — 이격 {fmt_num(abs(gap))}{pct}")
    except (TypeError, ValueError):
        return f"{esc(name)}: {esc(v)} {esc(op)} {esc(t)}"


def sparkline(vals, w=110, h=26):
    vals = [float(v) for v in vals if v is not None]
    if len(vals) < 2:
        return '<div class="spark-cap" style="text-align:left">시계열 부족(첫 실측)</div>'
    pad, mn, mx = 3, min(vals), max(vals)
    if mx == mn:
        mx, mn = mx + 1, mn - 1
    pts = " ".join(
        f"{pad + (w-2*pad)*i/(len(vals)-1):.1f},{h-pad-(h-2*pad)*(v-mn)/(mx-mn):.1f}"
        for i, v in enumerate(vals))
    trend = "▴" if vals[-1] > vals[0] else ("▾" if vals[-1] < vals[0] else "→")
    return (f'<svg width="{w}" height="{h}" class="spark" role="img" aria-label="run 추이">'
            f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" class="sp-base"/>'
            f'<polyline points="{pts}" class="sp-line"/>'
            f'<circle cx="{pad + (w-2*pad):.1f}" cy="{h-pad-(h-2*pad)*(vals[-1]-mn)/(mx-mn):.1f}" r="3" class="sp-dot"/></svg>'
            f'<div class="spark-cap">{len(vals)}개 run {trend}</div>')


CSS = """
:root{color-scheme:light;
 --page:#f9f9f7;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;
 --grid:#e1e0d9;--ring:rgba(11,11,11,.10);
 --good:#0ca30c;--warn:#fab219;--serious:#ec835a;--critical:#d03b3b;--goodtx:#006300;
 --series:#2a78d6;
 --pos-l:#cde2fb;--pos-m:#86b6ef;--pos-h:#2a78d6;
 --neg-l:#f8d3d2;--neg-m:#ef9a99;--neg-h:#d03b3b;
 --cellw:#fff;--ncell:#f0efec;--chip:#efede8;
 --touchbg:#faeaea;--nearbg:#fdf1ea;--watchbg:#fdf6e2;}
@media (prefers-color-scheme:dark){:root{color-scheme:dark;
 --page:#0d0d0d;--surface:#1a1a19;--ink:#fff;--ink2:#c3c2b7;--muted:#898781;
 --grid:#2c2c2a;--ring:rgba(255,255,255,.10);--goodtx:#0ca30c;--series:#3987e5;
 --pos-l:#184f95;--pos-m:#2a78d6;--pos-h:#5598e7;
 --neg-l:#5c2323;--neg-m:#a94443;--neg-h:#e66767;
 --ncell:#262624;--chip:#262624;
 --touchbg:#331c1c;--nearbg:#332419;--watchbg:#332c14;}}
*{box-sizing:border-box}
body{margin:0;padding:0 20px 60px;background:var(--page);color:var(--ink);
 font-family:'Malgun Gothic','Segoe UI',sans-serif;font-size:14px;line-height:1.6}
.wrap{max-width:1060px;margin:0 auto}
.mono{font-family:Consolas,'Courier New',monospace}
.num{font-variant-numeric:tabular-nums}
header{padding:30px 0 6px}h1{font-size:23px;margin:0}
header .meta{color:var(--muted);font-size:12.5px;margin-top:2px}
h2{font-size:16.5px;margin:0}
.sec{margin-top:36px}
.sec-head{display:flex;gap:10px;align-items:baseline;border-bottom:2px solid var(--ink);
 padding-bottom:6px;margin-bottom:14px;flex-wrap:wrap}
.sec-head .note{color:var(--muted);font-size:12px}
.hero{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:11px;margin-top:16px}
.tile{background:var(--surface);border:1px solid var(--ring);border-radius:8px;padding:13px 15px}
.tile .k{font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.tile .v{font-size:20px;font-weight:700;margin-top:3px;line-height:1.3}
.tile .d{font-size:12px;color:var(--ink2);margin-top:3px}
.tile.alert{border-left:3px solid var(--critical);background:var(--touchbg)}
.tile.alert .v{color:var(--critical)}
.b{display:inline-flex;align-items:center;gap:3px;border-radius:99px;font-size:11px;
 padding:1px 8px;border:1px solid transparent;font-weight:500;white-space:nowrap}
.b-prov{background:var(--watchbg);color:var(--warn);border-color:var(--warn)}
.b-stale{background:var(--nearbg);color:var(--serious);border-color:var(--serious)}
.b-fresh{color:var(--muted);border-color:var(--grid)}
.b-touch{background:var(--touchbg);color:var(--critical);border-color:var(--critical);font-weight:700}
.b-near{background:var(--nearbg);color:var(--serious);border-color:var(--serious)}
.b-watch{background:var(--watchbg);color:var(--warn);border-color:var(--warn)}
.b-clear{color:var(--muted);border-color:var(--grid)}
.kc{background:var(--surface);border:1px solid var(--ring);border-radius:8px;
 padding:12px 15px;margin-bottom:9px}
.kc.touch{border-left:3px solid var(--critical)}
.kc.near{border-left:3px solid var(--serious)}
.kc.watch{border-left:3px solid var(--warn)}
.kc-top{display:flex;gap:9px;align-items:baseline;flex-wrap:wrap}
.kc-id{font-family:Consolas,monospace;font-weight:700;font-size:13px}
.kc-name{font-weight:700}
.kc-mid{display:grid;grid-template-columns:1fr 118px;gap:14px;align-items:center;margin-top:7px}
.bullet{height:13px;background:var(--ncell);border-radius:4px;position:relative;overflow:hidden}
.bullet .fill{position:absolute;left:0;top:0;bottom:0;border-radius:4px 3px 3px 4px;min-width:2px}
.bullet .thr{position:absolute;right:0;top:-3px;bottom:-3px;width:2px;background:var(--ink)}
.f-touch{background:var(--critical)}.f-near{background:var(--serious)}
.f-watch{background:var(--warn)}.f-clear{background:var(--pos-m)}
.kc-margin{font-size:12px;color:var(--ink2);margin-top:5px}
.kc-foot{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-top:7px;
 font-size:11.5px;color:var(--muted)}
.tk{background:var(--chip);border-radius:4px;padding:0 6px;font-family:Consolas,monospace;
 font-size:10.5px;color:var(--ink2)}
.tk.held{background:var(--pos-h);color:#fff;font-weight:600}
.spark{display:block}.sp-base{stroke:var(--grid);stroke-width:1}
.sp-line{fill:none;stroke:var(--series);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.sp-dot{fill:var(--series)}
.spark-cap{font-size:10px;color:var(--muted);text-align:right;margin-top:1px}
.sig-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(315px,1fr));gap:11px}
.sig{background:var(--surface);border:1px solid var(--ring);border-radius:8px;padding:13px 15px}
.sig-top{display:flex;gap:7px;align-items:center;flex-wrap:wrap}
.sig-top .t{font-family:Consolas,monospace;font-weight:700;font-size:15px}
.sig-top .lb{font-size:11.5px;color:var(--ink2)}
.gates{display:flex;gap:5px;margin:8px 0 7px;flex-wrap:wrap}
.gate{font-size:11px;border-radius:5px;padding:2px 8px;border:1px solid var(--grid);color:var(--muted)}
.gate.on{border-color:var(--good);color:var(--goodtx);font-weight:600}
.sig .blk{font-size:12px;color:var(--ink2);border-left:2px solid var(--grid);padding-left:8px;margin:7px 0}
.sig .nx{font-size:11.5px;color:var(--muted)}
.sig .nx b{color:var(--ink2);font-weight:500}
.mx-wrap,.dl-wrap{overflow-x:auto;background:var(--surface);border:1px solid var(--ring);
 border-radius:8px;padding:5px}
table.mx{border-collapse:separate;border-spacing:2px;width:100%;min-width:740px}
.mx th{font-size:10.5px;color:var(--muted);font-weight:500;padding:4px 5px;text-align:center}
.mx th.rowh,.mx td.rowh{text-align:left}
.mx td{text-align:center;font-family:Consolas,monospace;font-size:11.5px;padding:6px 4px;
 border-radius:4px;background:var(--ncell);color:var(--muted);min-width:60px}
.mx td.rowh{background:transparent;font-weight:700;color:var(--ink);font-size:12.5px;white-space:nowrap;
 font-family:inherit}
.mx td.rowh small{color:var(--muted);font-weight:400}
.mx .pL{background:var(--pos-l);color:var(--ink)}.mx .pM{background:var(--pos-m);color:var(--ink)}
.mx .pH{background:var(--pos-h);color:#fff;font-weight:700}
.mx .nL{background:var(--neg-l);color:var(--ink)}.mx .nM{background:var(--neg-m);color:var(--ink)}
.mx .nH{background:var(--neg-h);color:#fff;font-weight:700}
.mx tr.conc td{background:transparent;border-top:2px solid var(--grid);border-radius:0;
 font-size:11px;color:var(--ink2)}
.mx tr.conc td.over{color:var(--critical);font-weight:700}
.mx-legend{display:flex;gap:12px;flex-wrap:wrap;font-size:11.5px;color:var(--muted);margin-top:7px}
.sw{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:3px}
.posbar{height:7px;background:var(--ncell);border-radius:3px;overflow:hidden;margin-top:2px;width:88px}
.posbar i{display:block;height:100%;background:var(--series)}
table.dl{border-collapse:collapse;width:100%;min-width:600px;font-size:12.5px}
.dl th{font-size:11px;color:var(--muted);font-weight:500;text-align:left;padding:7px 11px;
 border-bottom:1px solid var(--grid)}
.dl th.c,.dl td.c{text-align:center}
.dl td{padding:4px 11px;border-bottom:1px solid var(--grid)}
.dl tr:last-child td{border-bottom:none}
.dl td.tick{font-family:Consolas,monospace;font-weight:700}
.dl td.ax{color:var(--ink2);font-size:12px}
.gl{font-weight:700}.gl.up{color:var(--goodtx)}.gl.dn{color:var(--critical)}
.gl.mx{color:var(--serious)}.gl.nu{color:var(--muted);font-weight:400}.gl.none{color:var(--grid)}
.card{background:var(--surface);border:1px solid var(--ring);border-radius:8px;
 padding:12px 15px;margin-bottom:9px}
.card h3{font-size:13px;margin:0 0 3px}
.card p,.card li{font-size:12px;color:var(--ink2);margin:0}
.card ul{margin:4px 0 0;padding-left:17px}
table.q{border-collapse:collapse;width:100%;font-size:12.5px;background:var(--surface);
 border:1px solid var(--ring);border-radius:8px}
.q th,.q td{padding:6px 11px;border-bottom:1px solid var(--grid);text-align:left}
.q tr:last-child td{border-bottom:none}
.q th{font-size:11px;color:var(--muted);font-weight:500}
footer{margin-top:40px;border-top:1px solid var(--grid);padding-top:12px;
 color:var(--muted);font-size:11.5px;line-height:1.7}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="output/dashboard.html")
    args = ap.parse_args()

    signals = load_json(ROOT / "state" / "signals.json") or {}
    queue = (load_json(ROOT / "state" / "pending_approvals.json") or {}).get("queue", [])
    runs = sorted(d for d in (ROOT / "output").glob("*/") if re.match(r"\d{8}_\d{4}", d.name)) \
        if (ROOT / "output").exists() else []

    def latest_with(name):
        for r in reversed(runs):
            if (r / name).exists():
                return r
        return None

    def runs_with(name, n=None):
        hit = [r for r in runs if (r / name).exists()]
        return hit[-n:] if n else hit

    tickers = list((signals.get("grades") or {}).keys())
    pending = [e for e in queue if e.get("status") == "pending"]

    # ── ① KC 이격도 ────────────────────────────────────────────
    kc_run = latest_with("01_macro_kc.json")
    kc = load_json(kc_run / "01_macro_kc.json") if kc_run else None
    kc_hist = {}   # indicator name -> [values across runs]
    for r in runs_with("01_macro_kc.json"):
        d = load_json(r / "01_macro_kc.json") or {}
        for s in d.get("kc_status", []):
            for inp in s.get("inputs", []):
                if inp.get("value") is not None:
                    kc_hist.setdefault(inp.get("name"), []).append(inp.get("value"))

    ripple = {}
    corr_run = latest_with("05_correlation.json")
    corr = load_json(corr_run / "05_correlation.json") if corr_run else None
    if corr:
        for rp in corr.get("kc_propagation", corr.get("kc_ripple", [])):
            ripple[rp.get("kc_id")] = rp

    kc_cards, nearest = [], None
    if kc:
        for s in kc.get("kc_status", []):
            inputs = s.get("inputs", [])
            legs = []
            for inp in inputs:
                f = leg_fill(inp, kc_hist.get(inp.get("name"), []))
                legs.append((f, inp))
            numeric = [(f, i) for f, i in legs if f is not None]
            fill = max(f for f, _ in numeric) if numeric else None  # AND형은 최근접 레그(감시 목적) — 각주 명기
            fillv, bcls, blabel, fcls = kc_fill_class(fill)
            is_and = len(inputs) > 1
            gaps = " / ".join(gap_text(i) for i in inputs) or "이벤트형 — 공시 관측으로 판정"
            if is_and:
                gaps += " (AND — 전 레그 동시 충족 필요)"
            prov = s.get("verdict_confidence") == "provisional"
            worst_stale = max([i.get("stale_days") or age_days(i.get("as_of")) or 0 for i in inputs] or [0])
            met = s.get("verdict") == "met"
            badges = ""
            if met:
                badges += '<span class="b b-touch">🔴 MET</span>'
            badges += f'<span class="b {bcls}">{blabel}</span>'
            if worst_stale > 7:
                badges += f'<span class="b b-stale">⚠ {worst_stale}일 경과</span>'
            if prov:
                badges += '<span class="b b-prov">provisional</span>'
            spark_name = inputs[0].get("name") if inputs else None
            spark = sparkline(kc_hist.get(spark_name, [])) if spark_name else \
                '<div class="spark-cap" style="text-align:left">이벤트형 — 시계열 없음</div>'
            rp = ripple.get(s.get("kc_id"), {})
            rp_tk = rp.get("affected") or rp.get("tickers") or []
            rp_w = rp.get("weight_pct_upper")
            held = {t for t in tickers}  # for chip style we need positions — filled later
            kc_cards.append({
                "id": s.get("kc_id"), "name": s.get("condition", ""),
                "fill": fillv, "fcls": fcls, "cls": bcls.replace("b-", ""),
                "badges": badges, "gaps": gaps,
                "consequence": s.get("consequence", ""),
                "spark": spark, "ripple": rp_tk, "ripple_w": rp_w,
                "sort": (-(fillv if fillv is not None else -1)),
            })
        kc_cards.sort(key=lambda c: c["sort"])
        nearest = next((c for c in kc_cards if c["fill"] is not None), None)

    # ── positions / matrix ─────────────────────────────────────
    pos_cfg = load_yaml(ROOT / "config" / "positions.yaml") or {}
    positions = {t: (v.get("weight_range") or [0, 0])[1]
                 for t, v in (pos_cfg.get("positions") or {}).items()}
    matrix = load_yaml(ROOT / "config" / "correlation_matrix.yaml") or {}
    axes = list((matrix.get("axes") or {}).keys())
    exposures = matrix.get("exposures") or {}

    conc = {c.get("axis"): c for c in (corr.get("axis_concentration", []) if corr else [])}

    def tk_chip(t):
        w = positions.get(t, 0)
        if w and w > 0:
            return f'<span class="tk held">{esc(t)} {w*100:.0f}%</span>'
        return f'<span class="tk">{esc(t)}</span>'

    kc_html = '<p class="card">미실행 — <code>run macro</code> 필요</p>'
    if kc_cards:
        parts = []
        for c in kc_cards:
            width = f"{(c['fill'] or 0)*100:.0f}%"
            ripple_html = " ".join(tk_chip(t) for t in c["ripple"]) or "미산출(축 매핑 부재 ≠ 파급 부재)"
            if c.get("ripple_w") is not None:
                ripple_html += f' <span class="num">· 포트 파급 {c["ripple_w"]}%</span>'
            parts.append(f"""
<div class="kc {c['cls'] if c['cls'] in ('touch','near','watch') else ''}">
 <div class="kc-top"><span class="kc-id">{esc(c['id'])}</span><span class="kc-name">{esc(c['name'])}</span>{c['badges']}</div>
 <div class="kc-mid">
  <div><div class="bullet"><div class="fill {c['fcls']}" style="width:{width}"></div><div class="thr"></div></div>
   <div class="kc-margin num">{c['gaps']}</div></div>
  <div>{c['spark']}</div>
 </div>
 <div class="kc-foot">파급: {ripple_html} · 발동 시(사전 정의): {esc(c['consequence'])}</div>
</div>""")
        reused = f" · reused_from {kc.get('reused_from')}" if kc.get("reused_from") else ""
        kc_html = (f'<p style="font-size:12px;color:var(--muted);margin:0 0 10px">'
                   f'run {esc(kc_run.name)} · as_of {esc(kc.get("as_of"))} {fresh_badge(kc.get("as_of"),5)}{reused}'
                   f' · draft 제외: {esc(", ".join(kc.get("skipped_draft", [])) or "-")}</p>' + "".join(parts))

    # ── ② 시그널 · 게이트 ─────────────────────────────────────
    sig_run = latest_with("03_signal")
    sig_cards = []
    for t, g in (signals.get("grades") or {}).items():
        sg = load_json(sig_run / "03_signal" / f"{t}.json") if sig_run else None
        gate = ((sg or {}).get("gate_check") or {}).get("upgrade_gate") or {}
        def gate_pill(key, label):
            on = bool(gate.get(key))
            return f'<span class="gate {"on" if on else ""}">{"✓" if on else "✗"} {label}</span>'
        gates_html = (gate_pill("quantitative", "정량") + gate_pill("company_specific", "회사 고유")
                      + gate_pill("revenue_recognized", "매출 인식")) if gate else \
            '<span class="gate">게이트 판정 산출물 없음</span>'
        nxt = (sg or {}).get("gate_check", {}).get("next_check") or (sg or {}).get("next_gate") or ""
        if len(nxt) > 260:
            nxt = nxt[:260] + "…"
        cand = (sg or {}).get("transition_candidate", "")
        held = f' · <b>보유 {positions.get(t,0)*100:.0f}%</b>' if positions.get(t, 0) > 0 else ""
        sig_cards.append(f"""
<div class="sig">
 <div class="sig-top"><span>{esc(g.get('signal'))}</span><span class="t">{esc(t)}</span>
  <span class="lb">{esc(g.get('label',''))} · since {esc(g.get('since',''))}{held}</span></div>
 <div class="gates">{gates_html}</div>
 <div class="blk"><b>다음 게이트:</b> {esc(g.get('next_gate',''))}</div>
 <div class="nx"><b>다음 관측{(' · 후보판정 ' + esc(cand)) if cand else ''}:</b> {esc(nxt) or '—'}</div>
</div>""")
    sig_html = f'<div class="sig-grid">{"".join(sig_cards)}</div>' if sig_cards else "<p>signals.json 없음</p>"

    # ── ③ 노출 매트릭스 ───────────────────────────────────────
    mx_html = '<p class="card">correlation_matrix.yaml 파싱 불가(PyYAML 필요) 또는 부재</p>'
    if axes and exposures:
        ax_short = [a if len(a) <= 12 else a[:10] + "…" for a in axes]
        head = "".join(f'<th title="{esc(a)}">{esc(s)}</th>' for a, s in zip(axes, ax_short))
        body = ""
        for t in (list(exposures.keys()) or tickers):
            w = positions.get(t, 0)
            bar = (f'<div class="posbar"><i style="width:{w*100:.0f}%"></i></div>' if w > 0 else "")
            row = (f'<td class="rowh">{esc(t)} <small class="num">{w*100:.0f}%</small>{bar}</td>')
            for a in axes:
                cell = (exposures.get(t) or {}).get(a)
                if not cell:
                    row += "<td>·</td>"
                else:
                    sign, st = cell.get("sign", "+"), str(cell.get("strength", "M"))[0].upper()
                    cls = ("p" if sign == "+" else "n") + st
                    basis = "; ".join(cell.get("basis", []))[:180]
                    row += (f'<td class="{cls}" title="{esc(t)} × {esc(a)}: {sign}{STR_KO.get(st,st)} — {esc(basis)}">'
                            f'{sign}{STR_KO.get(st, st)}</td>')
            body += f"<tr>{row}</tr>"
        conc_row = '<td class="rowh">축 집중도 <small>(임계 60)</small></td>'
        for a in axes:
            c = conc.get(a)
            if not c:
                conc_row += "<td>—</td>"
            else:
                v = c.get("weight_pct_upper")
                over = c.get("threshold_breach")
                conc_row += f'<td class="num {"over" if over else ""}">{v if v is not None else "—"}{" ⚠" if over else ""}</td>'
        cfg_age = fresh_badge(matrix.get("as_of"), 14)
        mx_html = f"""
<p style="font-size:12px;color:var(--muted);margin:0 0 8px">config as_of {esc(matrix.get('as_of'))} {cfg_age}
 · positions as_of {esc(pos_cfg.get('as_of'))} {fresh_badge(pos_cfg.get('as_of'),14)} — 시가 재평가 아님</p>
<div class="mx-wrap"><table class="mx">
 <thead><tr><th class="rowh">종목 · 보유(상단)</th>{head}</tr></thead>
 <tbody>{body}<tr class="conc">{conc_row}</tr></tbody></table></div>
<div class="mx-legend">
 <span><span class="sw" style="background:var(--pos-h)"></span>+상</span>
 <span><span class="sw" style="background:var(--pos-m)"></span>+중</span>
 <span><span class="sw" style="background:var(--pos-l)"></span>+하</span>
 <span><span class="sw" style="background:var(--neg-h)"></span>−상</span>
 <span><span class="sw" style="background:var(--neg-m)"></span>−중</span>
 <span><span class="sw" style="background:var(--neg-l)"></span>−하</span>
 <span>· = 매트릭스 미등재</span>
 <span>집중도 0 = 위험 부재가 아니라 <b>보유 부재</b>의 결과일 수 있음</span></div>"""

    # ── ④ Delta 추이 (최근 3 run) ────────────────────────────
    d_runs = [r for r in runs if (r / "02_company").exists()][-3:]
    delta = {}  # (ticker, axis) -> {run: direction}
    for r in d_runs:
        for f in (r / "02_company").glob("*.json"):
            if f.name.startswith("_") or "edgar" in f.name.lower() or "raw" in f.name.lower():
                continue
            t = f.stem.split("_")[0].upper()
            if t not in tickers:
                continue
            d = load_json(f) or {}
            for dl in d.get("deltas", []):
                ax = dl.get("axis") or dl.get("axis_id") or dl.get("id")
                di = dl.get("direction")
                if ax and di:
                    delta.setdefault((t, ax), {})[r.name] = str(di)
    dl_html = "<p class='card'>02_company 산출물 없음</p>"
    if delta:
        heads = "".join(f'<th class="c">{r.name[4:6]}/{r.name[6:8]}</th>' for r in d_runs)
        rows, last_t = "", None
        order = sorted(delta.keys(), key=lambda k: (tickers.index(k[0]) if k[0] in tickers else 99, k[1]))
        counts = {}
        for t, _ in order:
            counts[t] = counts.get(t, 0) + 1
        for (t, ax) in order:
            cells = ""
            for r in d_runs:
                di = delta[(t, ax)].get(r.name)
                if di is None:
                    cells += '<td class="c"><span class="gl none">·</span></td>'
                else:
                    gy, cl, _ = DIR_GLYPH.get(di, ("●", "nu", di))
                    cells += f'<td class="c"><span class="gl {cl}" title="{esc(di)}">{gy}</span></td>'
            tick_cell = f'<td class="tick" rowspan="{counts[t]}">{esc(t)}</td>' if t != last_t else ""
            last_t = t
            rows += f'<tr>{tick_cell}<td class="ax">{esc(ax)}</td>{cells}</tr>'
        dl_html = (f'<div class="dl-wrap"><table class="dl"><thead><tr><th>종목</th><th>축</th>{heads}'
                   f'</tr></thead><tbody>{rows}</tbody></table></div>'
                   '<p style="font-size:11.5px;color:var(--muted);margin-top:7px">'
                   '<span class="gl up">▲</span> 강화 · <span class="gl dn">▼</span> 훼손 · '
                   '<span class="gl mx">◆</span> 혼재 · <span class="gl nu">●</span> 중립 · '
                   '<span class="gl none">·</span> 해당 run 관측 없음(부재 ≠ 반증, P5) — L2 판정 원문 그대로</p>')

    # ── ⑤ 촉매·관측점 (카드 원문) ────────────────────────────
    ev_rows = ""
    for t in tickers:
        card = load_yaml(ROOT / "state" / "thesis_cards" / f"{t}.yaml") or {}
        ec = (card.get("earnings_checkpoints") or {})
        ec_date = ec.get("date") or "미확정"
        cats = [c for c in (card.get("catalysts") or []) if isinstance(c, str)][:4]
        cat_html = "<br>".join("· " + esc(c[:110] + ("…" if len(c) > 110 else "")) for c in cats) or "—"
        ev_rows += (f'<tr><td class="tick mono">{esc(t)}</td><td class="num">{esc(ec_date)}</td>'
                    f'<td style="font-size:12px;color:var(--ink2)">{cat_html}</td></tr>')
    ev_html = (f'<table class="q"><tr><th>종목</th><th>실적 체크포인트 일자</th><th>카드 촉매(원문, 최대 4건)</th></tr>'
               f'{ev_rows}</table>') if ev_rows else "<p>thesis card 없음</p>"

    # ── ⑥ 승인 큐 · 품질 ──────────────────────────────────────
    q_rows = "".join(
        f'<tr><td class="mono" style="font-size:11px">{esc(e.get("approval_id"))}</td>'
        f'<td>{esc(e.get("status"))}</td><td>{esc(e.get("created_at"))}</td></tr>'
        for e in pending) or '<tr><td colspan="3">비어 있음 ✓</td></tr>'
    prov_n = sum(1 for s in (kc or {}).get("kc_status", []) if s.get("verdict_confidence") == "provisional")

    # ── hero ──────────────────────────────────────────────────
    grade_line = " ".join(f'{esc(v.get("signal"))}{esc(t)}' for t, v in (signals.get("grades") or {}).items())
    over_axes = [a for a, c in conc.items() if c.get("threshold_breach")]
    hero_near = ("<div class='tile alert'><div class='k'>최근접 KC</div>"
                 f"<div class='v'>{esc(nearest['id'])} · 근접도 {nearest['fill']*100:.0f}%</div>"
                 f"<div class='d'>{esc(nearest['name'])} — 상세는 ① 참조</div></div>") if nearest and nearest["fill"] >= 0.75 else \
                (f"<div class='tile'><div class='k'>최근접 KC</div><div class='v'>{esc(nearest['id']) if nearest else '—'}</div>"
                 f"<div class='d'>{esc(nearest['name']) if nearest else 'run macro 필요'}</div></div>")
    hero = f"""
<div class="hero">
 {hero_near}
 <div class="tile"><div class="k">축 집중도</div><div class="v num">{len(over_axes)}/{len(axes) or '—'}축 초과</div>
  <div class="d">{esc(", ".join(over_axes) or "초과 없음")} — 단일 포지션 축퇴 여부는 ③ 참조</div></div>
 <div class="tile"><div class="k">시그널</div><div class="v" style="font-size:15px">{grade_line or '—'}</div>
  <div class="d">as_of {esc(signals.get('as_of'))} {fresh_badge(signals.get('as_of'),7)}</div></div>
 <div class="tile{' alert' if pending else ''}"><div class="k">승인 대기</div>
  <div class="v num">{len(pending)}건</div>
  <div class="d">{'처리 필요 — approve/reject' if pending else '큐 비어 있음'} · provisional KC {prov_n}건</div></div>
</div>"""

    page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>thesis-agent 임계 관제판</title><style>{CSS}</style></head><body><div class="wrap">
<header><h1>임계 관제판</h1>
<div class="meta">생성 {datetime.now().isoformat(timespec='minutes')} · 최신 run {esc(kc_run.name) if kc_run else '—'}
 · 판단 보조용 — 매수·매도 지시가 아닙니다</div>{hero}</header>

<section class="sec"><div class="sec-head"><h2>① KC 이격도 — 임계까지의 거리</h2>
<span class="note">근접순 정렬 · 막대 채움 = 근접도(본 스크립트 파생 계산※, AND형은 최근접 레그 기준) · 우측 세로선 = 발동 임계 · 판정 근거는 항상 이격 원문</span></div>
{kc_html}</section>

<section class="sec"><div class="sec-head"><h2>② 시그널 · 상향 게이트</h2>
<span class="note">상향은 3요건 동시 충족(정량 · 회사 고유 · 매출 인식) · 등급 확정은 사람 — 후보 판정만 표시</span></div>
{sig_html}</section>

<section class="sec"><div class="sec-head"><h2>③ 노출 매트릭스 — 부호·강도 × 실포지션</h2>
<span class="note">correlation_matrix.yaml 원본 그대로 · 수치형 상관계수 없음(P14) · 셀에 마우스를 올리면 근거(basis)</span></div>
{mx_html}</section>

<section class="sec"><div class="sec-head"><h2>④ 축별 Delta 추이 — 최근 {len(d_runs)}개 run</h2></div>
{dl_html}</section>

<section class="sec"><div class="sec-head"><h2>⑤ 촉매·관측점 — thesis card 원문</h2>
<span class="note">일자 등급은 카드 원문 표기를 따름 · '미확정'은 회사 IR 공식 공지 부재(F1)</span></div>
{ev_html}</section>

<section class="sec"><div class="sec-head"><h2>⑥ 승인 대기 큐</h2></div>
<table class="q"><tr><th>ID</th><th>상태</th><th>생성일</th></tr>{q_rows}</table></section>

<footer><b>본 대시보드는 판단 보조용 요약이며 매수·매도 지시가 아닙니다.</b>
 등급 확정·발행 승인·KC 임계 확정·포지션 행동은 전부 사람이 합니다(P12·P15).<br>
※ 근접도 채움율은 본 스크립트의 파생 계산(|임계|>0이면 1−|이격|/|임계|, 임계=0이면 run 시계열 범위 대비,
 AND형은 감시 목적상 가장 근접한 레그)으로 원 산출물에 없는 지표입니다 — 판정 근거는 각 막대 아래의 원문 이격 문구입니다.
 노출 부호·강도는 config 원본이며 가격 시계열 상관계수가 아닙니다(P14). Delta·게이트 판정은 계층 산출물의 원문 인용입니다.</footer>
</div></body></html>"""

    out = ROOT / args.out if not Path(args.out).is_absolute() else Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"✅ 대시보드 생성(v2): {out}")


if __name__ == "__main__":
    main()
