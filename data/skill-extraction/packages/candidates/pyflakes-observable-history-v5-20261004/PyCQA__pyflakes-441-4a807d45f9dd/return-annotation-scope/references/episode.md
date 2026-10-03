# Historical episode

Source: `PyCQA/pyflakes:441:repair:4a807d45f9dd`

Issue: `PyCQA/pyflakes:441`  
Repair: `PyCQA/pyflakes:pr:448`  
Revision: `4a807d45f9dd47266c82035bf6e04508a77f0258`

## Report

The [title](evidence/title.md) and [body](evidence/body.md) describe a class-bound `TypeVar` reported undefined in a method annotation:

```python
from typing import TypeVar

class IdClass:
    Y = TypeVar('Y')

    def id(self, x: Y) -> Y:
        return x
```

The supplied report shows `pyflakes t.py` producing `t.py:7: undefined name 'Y'`. The reporter also states that MyPy accepts the sample; this is a reported comparison, not independent verification in this package.

## Implementation

The [merged implementation evidence](evidence/fix.md) changes `pyflakes/checker.py` in `Checker`, after `self.pushScope()`:

```diff
-            self.handleChildren(node, omit='decorator_list')
+            self.handleChildren(node, omit=['decorator_list', 'returns'])
```

The narrow mechanism is to keep the return annotation out of the child traversal entered under the function scope while retaining the decorator omission. The supplied patch does not show the complete surrounding annotation-processing implementation. A current application therefore must establish that a correct annotation-processing pass remains.

## Regression assertions

The [regression evidence](evidence/regression.md) adds two Python-3-gated tests in `pyflakes/test/test_type_annotations.py`:

- `test_return_annotation_is_class_scope_variable`: a class-level `Y = TypeVar('Y')` is used in both parameter and return annotations, with no expected diagnostics.
- `test_return_annotation_is_function_body_variable`: `def t(self) -> Y` followed by a body-local `Y = 2` expects `m.UndefinedName`.

These are assertions available at the repair commit. No contemporaneous test-run output is supplied.

## Qualification boundary

A qualification checked on `2026-10-03T19:13:16.158530+00:00` reports verified resolution, one fail-to-pass, and seventeen pass-to-pass cases. It is explicitly limited to changed test files with original-base control; whole-project regression and cross-project transfer are untested. It is not backdated into the historical evidence cards.

The packaged inspection and validation procedures are evidence-derived reusable operations, not claims that the historical author executed the exact procedures or commands written here.
