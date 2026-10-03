# Historical episode

SourceRecord: `PyCQA/pyflakes:441:repair:4a807d45f9dd`

The [issue title](evidence/title.md) and [original report](evidence/body.md), available on 2019-03-19, describe this reproduction:

```python
from typing import TypeVar

class IdClass:
    Y = TypeVar('Y')

    def id(self, x: Y) -> Y:
        return x
```

The reporter observed `t.py:7: undefined name 'Y'` from `pyflakes t.py` and stated that MyPy accepted the annotations. That MyPy statement is reporter context, not an independently executed comparison in this package.

## Recorded repair

The [merged implementation](evidence/fix.md), available on 2019-07-03 at revision `4a807d45f9dd47266c82035bf6e04508a77f0258`, changed `pyflakes/checker.py`. After `self.pushScope()`, it changed:

```python
self.handleChildren(node, omit='decorator_list')
```

to:

```python
self.handleChildren(node, omit=['decorator_list', 'returns'])
```

The supplied diff establishes this omission, not a new annotation-resolution algorithm. A current realization must confirm that appropriate earlier annotation handling exists before using this mechanism.

## Recorded regression assertions

The [test diff](evidence/regression.md) in `pyflakes/test/test_type_annotations.py` added two Python-3-gated tests:

- `test_return_annotation_is_class_scope_variable`: a class-level `Y = TypeVar('Y')` is used in parameter and return annotations; `self.flakes(...)` specifies no expected diagnostics.
- `test_return_annotation_is_function_body_variable`: `def t(self) -> Y` contains `Y = 2` in the body; `self.flakes(..., m.UndefinedName)` requires an undefined-name diagnostic.

These are assertions present at the historical commit. The supplied historical entries do not include a contemporaneous test execution log.

## Qualification boundary

A later qualification attestation, dated 2026-10-03, reports verified resolution with changed-test-file/original-base control: one fail-to-pass and seventeen pass-to-pass. It explicitly leaves whole-project regression and cross-project transfer untested. It is retained in provenance without backdating it into the pre-cutoff evidence.
