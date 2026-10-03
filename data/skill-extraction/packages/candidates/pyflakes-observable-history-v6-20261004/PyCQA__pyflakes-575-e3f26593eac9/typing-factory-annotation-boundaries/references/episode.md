# Historical episode

SourceRecord: `PyCQA/pyflakes:575:repair:e3f26593eac9`.

## Report

The issue title was “Nested TypedDict not supported.” The report used Pyflakes 2.2.0 with Python 3.8.0 on Darwin and showed:

```python
from typing import TypedDict

class Example(TypedDict):
    nested: TypedDict("Nested", {"foo/bar": str})
```

Reported diagnostics incorrectly named `Nested`, `foo`, and `bar` as undefined. Hoisting the functional `TypedDict` declaration outside the annotation was reported as a workaround. This is historical context, not a required repair strategy.

See [title](evidence/title.md) and [report](evidence/body.md).

## Implementation available on 2021-03-14

The supplied merged diff changed the call visitor in historical `pyflakes/checker.py`. It introduced `omit`, `annotated`, and `not_annotated` collections.

For recognized `TypedDict` calls with a dictionary second argument, dictionary values were treated as annotations; argument traversal excluding those values occurred under `AnnotationState.NONE`. Keyword values were likewise collected as annotations.

For recognized `NamedTuple` calls, the positional sequence form was partitioned only when the second argument was a tuple/list and every field entry was a tuple/list of length two. Field type elements were annotated; field-name elements were handled outside annotation context. Keyword values were annotated.

The same diff collected all positional `TypeVar` arguments after the first as annotations, collected its `bound` keyword value as an annotation, and handled other keyword traversal outside annotation context. For `cast`, its first argument was handled in annotation context whenever present, removing the prior string-only condition. The `cast` branch did not set `omit`, so the diff retained the ordinary child-traversal fallback afterward.

When `omit` was nonempty, the implementation first traversed non-annotation portions under `AnnotationState.NONE`, then traversed collected annotation nodes under `_enter_annotation()`. Otherwise it called ordinary `handleChildren(node)`.

See [implementation](evidence/fix.md). These facts describe the historical implementation; a current repair must use current ownership and AST semantics rather than mechanically transplanting the diff.

## Regression assertions

Historical `pyflakes/test/test_type_annotations.py` added:

- Clean nested functional `TypedDict` and `NamedTuple` cases in `List[...]`.
- Seven expected `UndefinedName` messages across seven statements containing genuine unresolved type references.
- Clean imported nested reference cases for `NamedTuple`, `TypeVar`, and `cast`.
- Class annotations containing functional `TypedDict` and `NamedTuple`, guarded for Python versions below 3.6.

The supplied source establishes these assertions at the historical commit. It does not contain historical test-run output.

See [regression](evidence/regression.md).

## Qualification and scope

The supplied qualification was checked on 2026-10-03, after the authoritative cutoff. It reports verified resolution with two fail-to-pass and 47 pass-to-pass cases, scoped to changed test files with original-base control. It does not establish whole-project regression or cross-project transfer.

The attestation is retained in [provenance](provenance.json), separately from historical evidence. The Action contracts are reusable retrospective repair operations; their expected effects are not claims of current execution.
