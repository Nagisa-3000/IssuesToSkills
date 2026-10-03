# Historical episode

Source: `PyCQA/pyflakes:574:repair:c23a81037d4f`. Issue cluster: `PyCQA/pyflakes:574`. Fix: `PyCQA/pyflakes:pr:580`. Revision: `c23a81037d4f68067c4c987985d177ec7664de59`.

## Report

The [title](evidence/title.md) and [body](evidence/report.md) report:

```python
from typing import Annotated

Annotated[int, '>1']
```

The diagnostic was `./pyflakes.py:3:16 syntax error in forward annotation '>1'`.

## Repair mechanism

The [merged diff](evidence/implementation.md) in historical `pyflakes/checker.py` added `_is_name_or_attr`, matching `ast.Name.id` or terminal `ast.Attribute.attr`. Existing `Literal` handling adopted the helper while retaining its save/restore structure.

The new `Annotated` subscript branch visits the target, obtains a tuple from either a direct `ast.Tuple` slice or an older `ast.Index` wrapping a tuple, and falls back to normal slice traversal if there is no tuple or fewer than two elements.

For a multi-argument tuple, it visits the first element in the existing context and subsequent elements under `_enter_annotation(AnnotationState.NONE)`. It also visits `node.ctx`. Metadata therefore remains traversed; it is not made opaque.

Terminal-name recognition is an implementation fact, not evidence of general alias resolution.

## Regression assertions

The [test diff](evidence/regression.md) in historical `pyflakes/test/test_type_annotations.py` adds function-annotation assertions:

- `Annotated['integer']`: `m.UndefinedName`.
- `Annotated['integer', 1]`: `m.UndefinedName`.
- `Annotated[int, '> 0']`: no diagnostics.
- `Union[Annotated['int', '>0'], 'integer']`: `m.UndefinedName`.

These assertions were available at the historical commit. No historical execution results are supplied. The single-argument example is an analyzer input, not a claim of runtime-valid `Annotated` syntax.

## Qualification boundary

The supplied 2026 qualification attestation reports two fail-to-pass and forty pass-to-pass cases for changed test files with original-base control. It independently supports the supplied resolution status within that scope, but is not pre-cutoff learned content. Whole-project regression and cross-project transfer remain untested.

The [Workflow](workflow.md) reconstructs the evidenced mechanism; it does not claim the historical developers executed the exact authored operational sequence. Additional current invariant probes are proposed checks, not invented historical tests.
