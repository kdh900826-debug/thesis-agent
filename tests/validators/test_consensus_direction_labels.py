# -*- coding: utf-8 -*-
"""회귀 테스트 — consensus_aggregate 방향 라벨 정규화 (AD-5, 2026-09-19).

유래: L2 에이전트가 delta.direction을 한국어("강화"/"약화"/"혼재")로 기입하면
고정 키 dict 인덱싱이 KeyError로 죽어 섹터 집계가 중단됐다
(run 20260905_0618 neocloud — 수기 집계로 대체).
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".claude" / "skills" / "consensus-aggregate" / "scripts" / "consensus_aggregate.py"


def _load():
    spec = importlib.util.spec_from_file_location("consensus_aggregate", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("raw,expected", [
    ("강화", "strengthen"), ("약화", "weaken"), ("중립", "neutral"),
    ("훼손", "break"), ("혼재", "mixed"), ("상충", "mixed"),
    ("strengthen", "strengthen"), ("WEAKEN", "weaken"), ("Mixed", "mixed"),
    (None, "neutral"),
])
def test_known_labels_normalize(raw, expected):
    canon, _, ok = _load().normalize_direction(raw)
    assert ok is True
    assert canon == expected


def test_unknown_label_is_preserved_not_raised():
    """정규화 실패 라벨은 예외를 던지지 않고 보존된다(P5 — 부재·미상은 폐기 사유가 아니다)."""
    canon, raw, ok = _load().normalize_direction("엉뚱한라벨")
    assert ok is False
    assert canon == "unnormalized"
    assert raw == "엉뚱한라벨"


def test_korean_direction_does_not_crash_aggregation(tmp_path, monkeypatch):
    """한국어 방향 라벨이 섞인 L2 산출물로 집계가 완주하고, 경고가 산출물에 남는다."""
    mod = _load()
    run_id = "29991231_0000"
    root = mod.ROOT
    company = root / "output" / run_id / "02_company"
    company.mkdir(parents=True, exist_ok=True)
    cov = __import__("yaml").safe_load((root / "config" / "coverage.yaml").read_text(encoding="utf-8-sig"))
    members = cov["sectors"]["stablecoin"]["members"]
    try:
        for i, t in enumerate(members):
            (company / f"{t}.json").write_text(json.dumps({
                "ticker": t,
                "deltas": [{"axis": "regulation", "direction": "강화" if i == 0 else "약화"},
                           {"axis": "demand", "direction": "미정의라벨"}],
            }, ensure_ascii=False), encoding="utf-8")
        monkeypatch.setattr("sys.argv", ["x", "--sector", "stablecoin", "--run-id", run_id])
        mod.main()
        out = json.loads((root / "output" / run_id / "04_sector" / "stablecoin_aggregate.json")
                         .read_text(encoding="utf-8"))
        assert out["direction_label_warnings"], "정규화 실패 라벨이 경고로 보고돼야 한다"
        assert all(w["raw_direction"] == "미정의라벨" for w in out["direction_label_warnings"])
        reg = next(a for a in out["axis_view"] if a["axis"] == "regulation")
        assert reg["supporters"]["strengthen"] and reg["supporters"]["weaken"]
    finally:
        import shutil
        shutil.rmtree(root / "output" / run_id, ignore_errors=True)
