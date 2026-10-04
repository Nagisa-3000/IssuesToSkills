"""Portable unittest/JUnit adapter for Pylint's pre-pytest functional suite.

Only actual test methods and functional fixtures become observations. The
adapter runs inside the configured sandbox; it supplies no host fallback.
"""

from __future__ import annotations

from pathlib import PurePosixPath

LEGACY_UNITTEST_SOURCE = r"""
import argparse
import os
import sys
import unittest
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('--start-dir', required=True)
parser.add_argument('--module', action='append', required=True)
parser.add_argument('--fixture', action='append', default=[])
parser.add_argument('--junitxml', required=True)
args = parser.parse_args()
root = os.path.realpath(os.getcwd())
output = os.path.realpath(args.junitxml)
if os.path.commonpath([root, output]) != root:
    raise ValueError('JUnit output escapes the public checkout')
loader = unittest.TestLoader()
suite = unittest.TestSuite()
for module in sorted(set(args.module)):
    suite.addTests(loader.discover(args.start_dir, pattern=module))

def flatten(item):
    if isinstance(item, unittest.TestSuite):
        for child in item:
            for case in flatten(child):
                yield case
    else:
        yield item

cases = []
identities = {}
for case in flatten(suite):
    fixture = getattr(case, '_test_file', None)
    if fixture is not None:
        name = os.path.relpath(os.path.realpath(fixture.source), root).replace(os.sep, '/')
        if args.fixture and name not in args.fixture:
            continue
        identity = (case.__class__.__module__ + '.' + case.__class__.__name__, name)
    else:
        identity = (case.__class__.__module__ + '.' + case.__class__.__name__, case.id())
    if identity in identities.values():
        raise ValueError('duplicate legacy unittest identity')
    identities[id(case)] = identity
    cases.append(case)

class Result(unittest.TestResult):
    def __init__(self):
        super(Result, self).__init__()
        self.rows = {}

    def record(self, test, state, message=''):
        # A skipped subtest conservatively makes its parent non-passing.
        parent = getattr(test, 'test_case', test)
        key = identities[id(parent)]
        old = self.rows.get(key)
        priority = {'passed': 0, 'skipped': 1, 'failed': 2, 'error': 3}
        if old is None or priority[state] >= priority[old[0]]:
            self.rows[key] = (state, message)

    def startTest(self, test):
        super(Result, self).startTest(test)

    def addSuccess(self, test):
        super(Result, self).addSuccess(test)
        self.record(test, 'passed')

    def addFailure(self, test, error):
        super(Result, self).addFailure(test, error)
        self.record(test, 'failed', self._exc_info_to_string(error, test))

    def addError(self, test, error):
        super(Result, self).addError(test, error)
        self.record(test, 'error', self._exc_info_to_string(error, test))

    def addSkip(self, test, reason):
        super(Result, self).addSkip(test, reason)
        self.record(test, 'skipped', reason)

    def addExpectedFailure(self, test, error):
        super(Result, self).addExpectedFailure(test, error)
        self.record(test, 'skipped', 'expected failure; not a passing qualification control')

    def addUnexpectedSuccess(self, test):
        super(Result, self).addUnexpectedSuccess(test)
        self.record(test, 'failed', 'unexpected success')

    def addSubTest(self, test, subtest, error):
        super(Result, self).addSubTest(test, subtest, error)
        if error is not None:
            self.record(test, 'failed', self._exc_info_to_string(error, subtest))

result = Result()
unittest.TestSuite(cases).run(result)
for case in cases:
    key = identities[id(case)]
    if key not in result.rows:
        result.rows[key] = ('error', 'test produced no completed unittest observation')
report = ET.Element('testsuite', {
    'name': 'arex-legacy-unittest', 'tests': str(len(cases)),
    'failures': str(sum(s == 'failed' for s, _ in result.rows.values())),
    'errors': str(sum(s == 'error' for s, _ in result.rows.values())),
    'skipped': str(sum(s == 'skipped' for s, _ in result.rows.values())),
})
for (classname, name), (state, message) in sorted(result.rows.items()):
    node = ET.SubElement(report, 'testcase', {'classname': classname, 'name': name})
    if state != 'passed':
        ET.SubElement(node, {'failed': 'failure', 'error': 'error', 'skipped': 'skipped'}[state]).text = message
ET.ElementTree(report).write(output, encoding='utf-8', xml_declaration=True)
print('LEGACY_UNITTEST tests=%d passed=%d failures=%d errors=%d skipped=%d' % (
    len(cases), sum(s == 'passed' for s, _ in result.rows.values()),
    sum(s == 'failed' for s, _ in result.rows.values()),
    sum(s == 'error' for s, _ in result.rows.values()),
    sum(s == 'skipped' for s, _ in result.rows.values())))
sys.exit(5 if not cases else 1 if any(s in ('failed', 'error') for s, _ in result.rows.values()) else 0)
"""


def legacy_unittest_command(paths, repository_files, *, neighbors=2):
    """Select old-layout actual harnesses before observing any replay result.

    Changed functional fixtures plus lexicographic base-tree neighbors are
    selected by public paths. Other changed unittest modules run in full.
    Fixture source files themselves are never treated as test modules.
    """
    if type(neighbors) is not int or not 0 <= neighbors <= 4:
        raise ValueError("legacy unittest neighbor bound is invalid")
    files = set(repository_files)
    prefix = "pylint/test/"
    functional_prefix = prefix + "functional/"
    functional = {
        str(PurePosixPath(path).with_suffix(".py"))
        for path in paths
        if path.startswith(functional_prefix)
        and PurePosixPath(path).suffix in {".py", ".txt", ".rc"}
    }
    modules = {
        PurePosixPath(path).name
        for path in paths
        if path.startswith(prefix)
        and not path.startswith(functional_prefix)
        and PurePosixPath(path).suffix == ".py"
        and PurePosixPath(path).name.startswith(("test", "unittest"))
        and PurePosixPath(path).parent == PurePosixPath(prefix)
    }
    if functional:
        if prefix + "test_functional.py" not in files:
            raise ValueError("legacy functional harness is absent from the pinned base")
        modules.add("test_functional.py")
    if not modules:
        raise ValueError("legacy unittest test layout requires a different explicit adapter")
    fixtures = set(functional)
    # A changed harness alone must execute its complete suite.
    if functional:
        existing = sorted(
            path
            for path in files
            if path.startswith(functional_prefix)
            and path.endswith(".py")
            and PurePosixPath(path).name != "__init__.py"
        )
        for path in sorted(functional):
            before = [name for name in existing if name < path]
            after = [name for name in existing if name > path]
            fixtures.update(before[-neighbors:] if neighbors else [])
            fixtures.update(after[:neighbors])
    command = ["python3", "-c", LEGACY_UNITTEST_SOURCE, "--start-dir", "pylint/test"]
    for module in sorted(modules):
        command.extend(("--module", module))
    for fixture in sorted(fixtures):
        command.extend(("--fixture", fixture))
    return command
