from pathlib import Path

import pytest

from arex_skill_graph.historical_solver_evaluator import restore_evaluation_paths


def test_restore_oracle_paths_preserves_production_and_removes_new_test(tmp_path):
    work, baseline = tmp_path / "work", tmp_path / "base"
    work.mkdir()
    baseline.mkdir()
    (baseline / "test_existing.py").write_text("base assertions")
    (work / "test_existing.py").write_text("solver assertions")
    (work / "test_new.py").write_text("solver added same regression file")
    (work / "checker.py").write_text("solver production repair")
    restore_evaluation_paths(work, baseline, ["test_existing.py", "test_new.py"])
    assert (work / "test_existing.py").read_text() == "base assertions"
    assert not (work / "test_new.py").exists()
    assert (work / "checker.py").read_text() == "solver production repair"
    with pytest.raises(ValueError):
        restore_evaluation_paths(work, baseline, ["../outside.py"])


def test_oracle_restoration_rejects_symlinks(tmp_path):
    work, baseline = tmp_path / "work", tmp_path / "base"
    work.mkdir()
    baseline.mkdir()
    (work / "production.py").write_text("repair")
    (work / "test.py").symlink_to(Path("production.py"))
    with pytest.raises(ValueError):
        restore_evaluation_paths(work, baseline, ["test.py"])
    assert (work / "production.py").read_text() == "repair"
