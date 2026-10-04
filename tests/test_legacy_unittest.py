"""Regression tests for legacy harness identity, causal observations and skips."""

import subprocess
import sys
import textwrap

import pytest

from arex_skill_graph.history_verification import junit_observations
from arex_skill_graph.legacy_unittest import LEGACY_UNITTEST_SOURCE, legacy_unittest_command


def execute(tmp_path, code):
    folder = tmp_path / "pylint/test"
    folder.mkdir(parents=True)
    (folder / "test_adapter.py").write_text(textwrap.dedent(code))
    xml = tmp_path / "observations.xml"
    run = subprocess.run(
        [
            sys.executable,
            "-c",
            LEGACY_UNITTEST_SOURCE,
            "--start-dir",
            "pylint/test",
            "--module",
            "test_adapter.py",
            "--junitxml",
            str(xml),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    return run, junit_observations(xml)


def test_parameterized_load_tests_has_unique_fixture_identity(tmp_path):
    run, observed = execute(
        tmp_path,
        """
        import os
        import types
        import unittest
        class FixtureCase(unittest.TestCase):
            def __init__(self, name, passes):
                super().__init__('check_fixture')
                self._test_file = types.SimpleNamespace(source=os.path.join('pylint/test/functional', name))
                self.passes = passes
            def check_fixture(self):
                self.assertTrue(self.passes)
        def load_tests(loader, suite, pattern):
            return unittest.TestSuite([FixtureCase('a.py', True), FixtureCase('b.py', False)])
    """,
    )
    assert run.returncode == 1
    assert observed == {
        "test_adapter.FixtureCase::pylint/test/functional/a.py": "passed",
        "test_adapter.FixtureCase::pylint/test/functional/b.py": "failed",
    }


def test_skip_and_expected_failure_are_not_passing_controls(tmp_path):
    run, observed = execute(
        tmp_path,
        """
        import unittest
        class Checks(unittest.TestCase):
            @unittest.skip('unsupported runtime')
            def test_skip(self):
                self.fail()
            @unittest.expectedFailure
            def test_xfail(self):
                self.fail()
            @unittest.expectedFailure
            def test_unexpected_success(self):
                pass
    """,
    )
    assert run.returncode == 1
    assert sorted(observed.values()) == ["failed", "skipped", "skipped"]


def test_failed_subtest_cannot_appear_as_parent_pass(tmp_path):
    run, observed = execute(
        tmp_path,
        """
        import unittest
        class Checks(unittest.TestCase):
            def test_subtests(self):
                for value in (True, False):
                    with self.subTest(value=value):
                        self.assertTrue(value)
    """,
    )
    assert run.returncode == 1
    assert list(observed.values()) == ["failed"]


def test_skipped_subtest_conservatively_blocks_parent_pass(tmp_path):
    run, observed = execute(
        tmp_path,
        """
        import unittest
        class Checks(unittest.TestCase):
            def test_subtests(self):
                with self.subTest(value='unavailable'):
                    self.skipTest('unavailable')
                self.assertTrue(True)
    """,
    )
    assert run.returncode == 0
    assert list(observed.values()) == ["skipped"]


def test_duplicate_unittest_identity_rejected_before_execution(tmp_path):
    run, observed = execute(
        tmp_path,
        """
        import unittest
        class Checks(unittest.TestCase):
            def check(self):
                self.fail('must not execute')
        def load_tests(loader, suite, pattern):
            return unittest.TestSuite([Checks('check'), Checks('check')])
    """,
    )
    assert run.returncode != 0
    assert "duplicate legacy unittest identity" in run.stderr
    assert observed == {}


def test_no_tests_does_not_report_success(tmp_path):
    run, observed = execute(tmp_path, "import unittest\n")
    assert run.returncode == 5
    assert observed == {}


def test_loader_error_is_observed_and_nonpassing(tmp_path):
    run, observed = execute(tmp_path, "raise ImportError('dependency is unavailable')\n")
    assert run.returncode == 1
    assert list(observed.values()) == ["failed"]


def test_changed_fixtures_use_harness_and_outcome_independent_neighbors():
    files = ["pylint/test/test_functional.py"] + [
        f"pylint/test/functional/{name}.py" for name in ("a", "b", "d", "e", "f")
    ]
    command = legacy_unittest_command(["pylint/test/functional/c.txt"], files)
    assert command[:2] == ["python3", "-c"]
    assert command[command.index("--module") + 1] == "test_functional.py"
    fixtures = [command[i + 1] for i, arg in enumerate(command) if arg == "--fixture"]
    assert fixtures == [f"pylint/test/functional/{name}.py" for name in ("a", "b", "c", "d", "e")]
    assert not any(
        value.endswith("c.py") for i, value in enumerate(command) if command[i - 1] == "--module"
    )


def test_unit_module_executes_without_functional_name_filter():
    command = legacy_unittest_command(["pylint/test/unittest_checkers.py"], [])
    assert command[command.index("--module") + 1] == "unittest_checkers.py"
    assert "--fixture" not in command


def test_newer_layout_requires_separate_pytest_adapter():
    with pytest.raises(ValueError, match="different explicit adapter"):
        legacy_unittest_command(["tests/functional/unknown.py"], ["tests/test_functional.py"])
