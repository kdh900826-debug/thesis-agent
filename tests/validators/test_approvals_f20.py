# -*- coding: utf-8 -*-
"""F20(전문 확인 의무) — approvals.py 적용 후 검증·자동 원복 테스트.
유래: 2026-08-16 IREN 체크포인트 오인 패치(ap_20260816_0010) — 적용 후 항목 수 불일치(19≠13)를
사람이 수동으로 잡았던 사건. 이 테스트는 그 검증을 스크립트에 내장했음을 보증한다.
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "version-publish" / "scripts" / "approvals.py"
spec = importlib.util.spec_from_file_location("approvals", SCRIPT)
approvals = importlib.util.module_from_spec(spec)
sys.modules["approvals"] = approvals
spec.loader.exec_module(approvals)

CARD = """# Test Card
ticker: TST
version_history:
  - {date: "2026-08-16", change: 'init'}
axes:
  - {id: a1, label: "축1"}
  - {id: a2, label: "축2"}
items_field:
  items:
    - "하나"
    - "둘"
    - "셋"
"""


def make_card(tmp_path):
    card = tmp_path / "TST.yaml"
    card.write_text(CARD, encoding="utf-8")
    return card


def test_verify_pass(tmp_path):
    card = make_card(tmp_path)
    p = {"after": '  - {id: a2, label: "축2"}',
         "expected_after": {"contains": ["축1"], "not_contains": ["없어야함"],
                            "counts": [{"path": "items_field.items", "n": 3}]}}
    assert approvals.verify_after_apply(card, p) == []


def test_verify_count_mismatch(tmp_path):
    card = make_card(tmp_path)
    p = {"expected_after": {"counts": [{"path": "items_field.items", "n": 13}]}}
    errs = approvals.verify_after_apply(card, p)
    assert any("counts 불일치" in e and "3개" in e and "13개" in e for e in errs)


def test_verify_missing_after_string(tmp_path):
    card = make_card(tmp_path)
    errs = approvals.verify_after_apply(card, {"after": "카드에 없는 문자열"})
    assert any("after 문자열" in e for e in errs)


def test_verify_broken_yaml(tmp_path):
    card = tmp_path / "TST.yaml"
    card.write_text('key: "닫히지 않은 {중괄호: "값"\n  - 깨진: [', encoding="utf-8")
    errs = approvals.verify_after_apply(card, {})
    assert any("YAML 파싱 실패" in e for e in errs)


def test_verify_bad_count_path(tmp_path):
    card = make_card(tmp_path)
    errs = approvals.verify_after_apply(card, {"expected_after": {"counts": [{"path": "없는.경로", "n": 1}]}})
    assert any("경로 없음" in e for e in errs)


def test_apply_reverts_on_verify_failure(tmp_path, monkeypatch):
    """IREN 사건 재현: 중복 삽입으로 기대 개수 초과 → 자동 원복 + False."""
    (tmp_path / "state" / "thesis_cards").mkdir(parents=True)
    card = tmp_path / "state" / "thesis_cards" / "TST.yaml"
    card.write_text(CARD, encoding="utf-8")
    patch = {
        "ticker": "TST", "card_field": "items_field", "operation": "amend",
        "before": '    - "셋"',
        "after": '    - "셋"\n    - "넷(중복 오인 삽입)"',
        "expected_after": {"counts": [{"path": "items_field.items", "n": 3}]},  # 삽입하면 4가 되므로 실패해야 함
    }
    (tmp_path / "patches").mkdir()
    (tmp_path / "patches" / "p.json").write_text(json.dumps(patch, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(approvals, "ROOT", tmp_path)
    ok = approvals.apply_thesis_patch({"artifact": "patches/p.md"})
    assert ok is False
    assert card.read_text(encoding="utf-8") == CARD  # 원복 확인
    backups = list((tmp_path / "state" / "thesis_cards" / "backup").glob("TST_*.yaml"))
    assert len(backups) == 1  # 백업은 남는다


def test_apply_passes_with_correct_expectation(tmp_path, monkeypatch):
    (tmp_path / "state" / "thesis_cards").mkdir(parents=True)
    card = tmp_path / "state" / "thesis_cards" / "TST.yaml"
    card.write_text(CARD, encoding="utf-8")
    patch = {
        "ticker": "TST", "card_field": "items_field", "operation": "amend",
        "before": '    - "셋"',
        "after": '    - "셋"\n    - "넷"',
        "expected_after": {"counts": [{"path": "items_field.items", "n": 4}],
                           "contains": ['- "넷"']},
        "basis_claims": ["t"],
    }
    (tmp_path / "patches").mkdir()
    (tmp_path / "patches" / "p.json").write_text(json.dumps(patch, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(approvals, "ROOT", tmp_path)
    ok = approvals.apply_thesis_patch({"artifact": "patches/p.md"})
    assert ok is True
    assert '- "넷"' in card.read_text(encoding="utf-8")
    # 이력 라인이 YAML을 깨지 않는다 (2026-08-15 이스케이프 버그 회귀 방지)
    import yaml
    assert yaml.safe_load(card.read_text(encoding="utf-8")) is not None


def test_backup_unique_within_same_second(tmp_path, monkeypatch):
    """P9 백업 유일성 회귀 — 2026-09-20 CRWV_20260920_080500.yaml 충돌 사건.
    같은 초에 두 패치를 승인해도 백업 2개가 모두 남고, 첫 백업이 덮어씌워지지 않아야 한다."""
    (tmp_path / "state" / "thesis_cards").mkdir(parents=True)
    card = tmp_path / "state" / "thesis_cards" / "TST.yaml"
    card.write_text(CARD, encoding="utf-8")
    (tmp_path / "patches").mkdir()
    p1 = {"ticker": "TST", "card_field": "items_field", "operation": "amend",
          "before": '    - "셋"', "after": '    - "셋"\n    - "넷"',
          "expected_after": {"counts": [{"path": "items_field.items", "n": 4}]}, "basis_claims": ["t"]}
    p2 = {"ticker": "TST", "card_field": "items_field", "operation": "amend",
          "before": '    - "넷"', "after": '    - "넷"\n    - "다섯"',
          "expected_after": {"counts": [{"path": "items_field.items", "n": 5}]}, "basis_claims": ["t"]}
    (tmp_path / "patches" / "p1.json").write_text(json.dumps(p1, ensure_ascii=False), encoding="utf-8")
    (tmp_path / "patches" / "p2.json").write_text(json.dumps(p2, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(approvals, "ROOT", tmp_path)
    # 시계를 고정해 같은 초(마이크로초까지 동일)를 강제 — 순번 접미로만 구분돼야 한다
    class FrozenDT(approvals.datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 9, 20, 8, 5, 0, 0)
    monkeypatch.setattr(approvals, "datetime", FrozenDT)
    assert approvals.apply_thesis_patch({"artifact": "patches/p1.md"}) is True
    assert approvals.apply_thesis_patch({"artifact": "patches/p2.md"}) is True
    backups = sorted((tmp_path / "state" / "thesis_cards" / "backup").glob("TST_*.yaml"))
    assert len(backups) == 2
    # 첫 백업 = 원본 카드(p1 적용 전), 둘째 백업 = p1 적용 후 카드 — 서로 다른 내용이 모두 보존된다
    contents = {b.read_text(encoding="utf-8") for b in backups}
    assert len(contents) == 2
    assert CARD in contents


def test_unique_backup_path_no_overwrite(tmp_path):
    bdir = tmp_path / "backup"
    bdir.mkdir()
    a = approvals.unique_backup_path(bdir, "TST"); a.write_text("a")
    b = approvals.unique_backup_path(bdir, "TST")
    assert a != b and not b.exists()
