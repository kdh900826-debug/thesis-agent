# -*- coding: utf-8 -*-
"""회귀 테스트 — make_kc_excerpt 종목 전용 KC 임계 전달 (2026-10-01).

유래: own_company_kc_detail이 description/type/consequence 3키만 복사해
trigger·all_of·any_of·warning 등 임계 필드가 전 종목 발췌본에서 누락됐다.
signal-arbiter가 임계 없이 종목 KC를 판정하게 되어 전부 not_met/provisional로 귀결
(run 20260925_1015 KC-HOOD-3 '상위 3개 주' 누락으로 처음 보고, 20261001_0900에서 원인 확정).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".claude" / "scripts" / "make_kc_excerpt.py"
THRESHOLD_KEYS = {"trigger", "all_of", "any_of", "warning", "warning_trigger", "scope_note"}


def _latest_run_with_macro():
    runs = sorted(p for p in (ROOT / "output").iterdir()
                  if p.is_dir() and (p / "01_macro_kc.json").exists())
    return runs[-1]


def test_excerpt_carries_all_threshold_fields(tmp_path):
    src = _latest_run_with_macro()
    run_id = "zz_test_kc_excerpt"
    run_dir = ROOT / "output" / run_id
    try:
        run_dir.mkdir()
        shutil.copy(src / "01_macro_kc.json", run_dir / "01_macro_kc.json")
        subprocess.run([sys.executable, str(SCRIPT), "--run-id", run_id],
                       check=True, capture_output=True, env={"PYTHONIOENCODING": "utf-8",
                                                              **__import__("os").environ})
        cfg = yaml.safe_load((ROOT / "config" / "kill_conditions.yaml").read_text(encoding="utf-8-sig"))
        company = {k: v for k, v in (cfg.get("company") or {}).items() if v.get("status") == "active"}
        assert company, "active 종목 KC가 없으면 테스트 의미 없음"
        for kc_id, v in company.items():
            out = json.loads((run_dir / "03_kc_excerpt" / f"{v['ticker']}.json").read_text(encoding="utf-8"))
            detail = out["own_company_kc_detail"][kc_id]
            for key in THRESHOLD_KEYS & set(v):
                assert detail.get(key) == v[key], f"{kc_id}.{key} 발췌 누락/변형"
            assert "status" not in detail and "ticker" not in detail
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)
