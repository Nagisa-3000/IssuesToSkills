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


def test_old_functional_layout_runs_load_tests_and_fixed_base_neighbors():
    command = infer_historical_pytest_command(
        ["pylint/test/functional/singledispatch_functions_py3.py"],
        [
            "pylint/test/test_functional.py",
            "pylint/test/functional/signature_differs.py",
            "pylint/test/functional/simplifiable_if_statement.py",
            "pylint/test/functional/singledispatch_functions.py",
            "pylint/test/functional/singledispatch_functions_py3.py",
            "pylint/test/functional/singleton_comparison.py",
            "pylint/test/functional/slots_checks.py",
        ],
    )
    assert command[:2] == ["python3", "-c"]
    assert "load_tests" not in command[2] or "loader.discover" in command[2]
    assert "loader.discover" in command[2]
    assert command[command.index("--module") + 1] == "test_functional.py"
    fixtures = [command[i + 1] for i, value in enumerate(command) if value == "--fixture"]
    assert fixtures == [
        "pylint/test/functional/simplifiable_if_statement.py",
        "pylint/test/functional/singledispatch_functions.py",
        "pylint/test/functional/singledispatch_functions_py3.py",
        "pylint/test/functional/singleton_comparison.py",
        "pylint/test/functional/slots_checks.py",
    ]


def test_old_unittest_module_is_not_lost_by_pytest_filename_inference():
    command = infer_historical_pytest_command(
        ["pylint/test/unittest_checker.py"], ["pylint/test/unittest_checker.py"]
    )
    assert command[:2] == ["python3", "-c"]
    assert command[command.index("--module") + 1] == "unittest_checker.py"
    assert "--fixture" not in command
