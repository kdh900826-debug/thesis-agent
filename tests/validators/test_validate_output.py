# -*- coding: utf-8 -*-
"""검증기 단위 테스트 (D12) — F13~F19를 고정 픽스처로 검증한다.
실행: cd thesis-agent && python -m pytest tests/validators -q
LLM 행동은 테스트하지 않는다 — '검증기가 잡는다'를 테스트한다.
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".claude" / "skills" / "validate-output" / "scripts" / "validate_output.py"


def run_validator(tmp_path, data, layer, extra=None):
    f = tmp_path / "artifact.json"
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    cmd = [sys.executable, str(SCRIPT), str(f), "--layer", layer] + (extra or [])
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")


def test_f13_sector_claim_in_signal_rejected(tmp_path):
    """F13: scope!=company_specific Claim이 signal 입력에 있으면 거부."""
    data = {"as_of": "2026-08-15", "claims": [
        {"id": "c1", "scope": "sector", "claim_type": "fact"}]}
    r = run_validator(tmp_path, data, "signal")
    assert r.returncode == 1 and "F13" in r.stdout


def test_f14_macro_narrative_rejected(tmp_path):
    """F14: 매크로 산출물의 전망 서술 거부."""
    data = {"as_of": "2026-08-15", "kc_status": [],
            "comment": "9월 인하 가능성이 높다"}
    r = run_validator(tmp_path, data, "macro")
    assert r.returncode == 1 and "F14" in r.stdout


def test_f15_correlation_coefficient_rejected(tmp_path):
    """F15: 수치형 상관계수 표기 거부."""
    data = {"as_of": "2026-08-15", "coefficient_used": False,
            "pair_overlap": [{"pair": ["IREN", "NBIS"], "grade": "상", "shared_axes": [],
                              "note": "상관 0.72 수준"}]}
    r = run_validator(tmp_path, data, "correlation")
    assert r.returncode == 1 and "F15" in r.stdout


def test_f16_reused_without_staleness_rejected(tmp_path):
    """F16/P16: reused_from 있는데 staleness_days 없으면 거부."""
    data = {"as_of": "2026-08-15", "kc_status": [], "cache": {"reused_from": "20260801_0900"}}
    r = run_validator(tmp_path, data, "macro")
    assert r.returncode == 1 and "P16" in r.stdout


def test_f17_patch_without_approval_flag_rejected(tmp_path):
    """F17: requires_human_approval != true 패치 거부."""
    data = {"as_of": "2026-08-15", "ticker": "IREN", "card_field": "risks",
            "operation": "amend", "basis_claims": ["c1"], "requires_human_approval": False}
    r = run_validator(tmp_path, data, "thesis_patch")
    assert r.returncode == 1 and "F17" in r.stdout


def test_f18_directive_verb_rejected(tmp_path):
    """F18: 'IREN 30%로 축소' 류 지시문 거부."""
    data = {"as_of": "2026-08-15", "default_action": "no_action",
            "scenarios": [{"trigger": "KC-3", "source": "config/kill_conditions.yaml#KC-3"}],
            "opinion": "IREN 비중을 30%로 축소하는 것이 좋겠다"}
    r = run_validator(tmp_path, data, "portfolio")
    assert r.returncode == 1 and "F18" in r.stdout


def test_f19_unapproved_publish_rejected(tmp_path):
    """F19: 승인 안 된 건의 publish 거부."""
    q = tmp_path / "queue.json"
    q.write_text(json.dumps({"queue": [{"approval_id": "ap_x", "status": "pending"}]}), encoding="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPT), "dummy", "--layer", "publish",
                        "--queue", str(q), "--approval-id", "ap_x"],
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 1 and "F19" in r.stdout


def test_clean_macro_passes(tmp_path):
    """정상 매크로 산출물은 통과."""
    data = {"as_of": "2026-08-15", "kc_status": [
        {"kc_id": "KC-2", "verdict": "not_met", "verdict_confidence": "provisional",
         "inputs": [{"name": "VIX", "value": 16.0, "stale_days": 3, "stale_limit": 2}]}]}
    r = run_validator(tmp_path, data, "macro")
    assert r.returncode == 0, r.stdout


def test_clean_sector_passes(tmp_path):
    data = {"as_of": "2026-08-15", "sector": "neocloud", "signal_mutation": None,
            "axis_view": [{"axis": "funding_capacity", "direction": "diverge", "dispersion": "high"}]}
    r = run_validator(tmp_path, data, "sector")
    assert r.returncode == 0, r.stdout


def test_signal_upgrade_without_gate_rejected(tmp_path):
    """F5/P2: 게이트 미충족 상향 거부."""
    data = {"as_of": "2026-08-15", "claims": [],
            "prior_signal": "🟡", "proposed_signal": "🟢",
            "gate_check": {"quantitative_evidence": True, "company_specific": True,
                           "revenue_recognized": False}}
    r = run_validator(tmp_path, data, "signal")
    assert r.returncode == 1 and "revenue_recognized" in r.stdout
