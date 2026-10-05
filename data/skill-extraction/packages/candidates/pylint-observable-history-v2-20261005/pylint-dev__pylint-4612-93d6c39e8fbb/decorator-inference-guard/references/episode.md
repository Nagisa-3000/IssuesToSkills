# Historical episode

Authoritative source: `pylint-dev/pylint:4612:repair:93d6c39e8fbb`.

## Historical evidence

- [Title](evidence/title.md): crash involving a test function decorated with `@pytest.fixture`.
- [Body](evidence/body.md): Pylint 2.8.3 reported an uninferable membership TypeError.
- [Implementation](evidence/fix.md): invalid inference results were filtered before decorator-name matching.
- [Regression](evidence/regression.md): committed analyzer input with a fixture-decorated function using `open(...).read()` without `with`.

The historical owner was `decorated_with` in `pylint/checkers/utils.py`. Its old expression was:

```python
i is not None and i.qname() in qnames or i.name in qnames
```

The merged implementation was:

```python
if any(
    i.name in qnames or i.qname() in qnames
    for i in decorator_node.infer()
    if i is not None and i != astroid.Uninferable
):
    return True
```

The shown surrounding `except astroid.InferenceError` remained. The filter precedes both attribute accesses; the old boolean expression guarded only its first branch against `None`.

The repair added `tests/functional/r/regression/regression_4612_crash_pytest_fixture.py`:

```python
# pylint: disable=missing-docstring,consider-using-with,redefined-outer-name

import pytest


@pytest.fixture
def qm_file():
    qm_file = open("src/test/resources/example_qm_file.csv").read()
    return qm_file
```

This file is analyzer input. It does not establish execution of the fixture or runtime existence of the CSV. The core evidence establishes a committed regression, not historical CI execution. Historical test-execution status remains unknown.

The package's current probes, contracts, and adjacent-behavior checks are authored guidance grounded in this repair. They are not additional historical executions.

## Validation-only qualification inspection

The complete supplied original-base, base-with-regression, and historical-fixed controls were inspected together. They pin:

- Original base: `eba42d08550cd6560e81711c30efcac0c20d10b2`.
- Fixed revision: `93d6c39e8fbb370ab30b929db12792216cfb2b58`.
- Issue: `pylint-dev/pylint:4612`.
- Fix: `pylint-dev/pylint:pr:4613`.
- Repair availability: `2021-06-23T20:31:17Z`.
- Verified resolution relationship: direct closure.
- Validation time: `2026-10-04T10:56:22.592835+00:00`.

The original base passed 24 selected existing regressions; the new regression was absent. Adding the committed regression to the base yielded one failure at the unguarded decorator-name membership expression and 24 passing controls. The historical fixed state passed all 25 selected cases. The three exit codes were 0, 1 and 0; none timed out.

All runs and the top-level report use runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`. The report verifies the historical artifact and issue relationship. The observations digest is `e02c8707d13f443ac15a343f2604713d2f7d2855c86d05921353cac0ee1ea8b3`. The authoritative qualification report hash is `55109bc85754b62f2ad81ddc30f9653be751e47b75cf2d5f11c4f86284ab2b0a`.

Scope is `changed-test-files-with-original-base-control`. This supports causal resolution within the supplied scope, not whole-project correctness or cross-project transfer. It was not a formal SWE run.

The later replay is validation-only provenance, never backdated historical learned content. It does not establish historical CI status or execute this Skill's functional cases. Replay commands and contemporary runtime details are not current command bindings or historical repair mechanisms. The complete caller-supplied report remains authoring audit input, separate from historical evidence cards and Skill functional outcomes.
