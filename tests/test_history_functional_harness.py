"""Fixture-only historical repairs need their checker harness and base neighbors."""

import pytest

from arex_skill_graph.history_verification import infer_historical_pytest_command


def test_pylint_fixture_is_not_treated_as_a_pytest_module():
    command = infer_historical_pytest_command(
        ["tests/functional/n/names/test_binding.py", "tests/functional/n/names/test_binding.txt"],
        [
            "tests/test_functional.py",
            "tests/functional/n/names/test_binding.py",
            "tests/functional/n/names/runtime_binding.py",
            "tests/functional/other/unrelated.py",
        ],
    )
    assert command == [
        "python3",
        "-m",
        "pytest",
        "tests/test_functional.py",
        "-k",
        "runtime_binding or test_binding",
        "-q",
    ]


def test_mixed_unit_and_fixture_repair_does_not_deselect_unit_tests():
    command = infer_historical_pytest_command(
        ["tests/test_names.py", "tests/functional/a/annotation.py"],
        ["tests/test_functional.py", "tests/test_names.py"],
    )
    assert "-k" not in command and "tests/test_names.py" in command


def test_unknown_harness_is_deferred():
    with pytest.raises(ValueError, match="explicit verifier"):
        infer_historical_pytest_command(["tests/functional/annotation.py"], [])
