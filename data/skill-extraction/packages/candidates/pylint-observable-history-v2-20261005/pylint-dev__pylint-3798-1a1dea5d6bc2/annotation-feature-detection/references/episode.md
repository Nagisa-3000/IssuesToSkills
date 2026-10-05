# Historical repair episode

Authoritative source: `pylint-dev/pylint:3798:repair:1a1dea5d6bc2`.

The original report described Pylint 2.6.0 and earlier on Python 3.7. With an aliased future import, the containing-class return annotation produced a bogus undefined-variable warning:

```python
from __future__ import annotations as __annotations__

class C:
    @classmethod
    def create(cls) -> C:
        return cls()
```

The reporter stated that removing the alias removed the warning.

At revision `1a1dea5d6bc2f004293e3454a3a6e1385cfcf2db`, the historical detector was `is_postponed_evaluation_enabled` in `pylint/checkers/utils.py`. It previously retrieved `module.locals.get("annotations")`, then tested the first binding for `astroid.ImportFrom` and `modname == "__future__"`. The repair used:

```python
module = node.root()
return "annotations" in module.future_imports
```

The commit added `tests/functional/p/postponed_evaluation_activated_with_alias.py` and its companion `.rc`, setting `min_pyver=3.7`. The fixture covered a containing-class return annotation, a parameter referring to a later class, an attribute referring to a later class, and a self-referencing attribute. The changelog described the alias-related postponed-evaluation fix and stated `Close #3798`.

These paths are historical, not current owner bindings. The authored probe, safety controls, and execution procedure are conditional guidance derived from the mechanism; they are not asserted historical command executions.

## Independent qualification audit

The supplied complete three-arm report pins original base `83bc7593ac77e400bc42babbbc510c3d7fe7cc15`, PR 3868, the repair revision above, and direct closure of issue 3798. Identity, closure verification, historical artifact verification, per-case outcomes, and runtime consistency support source qualification.

- Original base: seven controls passed, one was skipped; the new alias fixture was absent.
- Base with committed regression: the alias fixture failed, seven controls passed, and one was skipped. Unexpected diagnostics were undefined-variable at lines 8 and 28, and used-before-assignment at lines 11 and 20.
- Historical fixed checkout: the alias fixture passed, the same seven controls passed, and the same control was skipped.

All three runs had the same runtime digest and no timeout. Exit codes were respectively 0, 1, and 0. The skipped control was `print_always_warns`.

Qualification was checked on `2026-10-04T10:09:41.178530+00:00`. Its scope is `changed-test-files-with-original-base-control`; it was not a formal SWE run and did not check whole-project regression. This validation time is not a historical evidence date. Runtime logs do not add historical mechanisms. The report does not execute the authored Skill functional cases.

Core evidence: [title](evidence/title.md), [report](evidence/body.md), [implementation](evidence/fix.md), [committed assertions](evidence/regression.md).
