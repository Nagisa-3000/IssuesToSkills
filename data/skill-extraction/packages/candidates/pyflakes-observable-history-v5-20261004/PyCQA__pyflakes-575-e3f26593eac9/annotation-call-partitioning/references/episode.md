# Historical episode

SourceRecord: `PyCQA/pyflakes:575:repair:e3f26593eac9`.

The original report described Pyflakes 2.2.0 on Python 3.8.0 reporting undefined names `Nested`, `foo`, and `bar` for:

```python
from typing import TypedDict

class Example(TypedDict):
    nested: TypedDict("Nested", {"foo/bar": str})
```

Moving the `TypedDict` declaration outside the class annotation was reported as a workaround. This is a reported observation, not a newly executed reproduction.

The merged implementation at revision `e3f26593eac942435c3e8e114506172678d58ce1` changed the call visitor in historical `pyflakes/checker.py`. It introduced `omit`, `annotated`, and `not_annotated` collections. Selected child traversal used `AnnotationState.NONE`; actual type nodes used `_enter_annotation()`.

The historical regression additions were in `pyflakes/test/test_type_annotations.py`. They asserted clean handling of nested `TypedDict` and `NamedTuple`, diagnostics for unresolved forward references, and use of imported names inside nested type expressions. The class-based test was skipped below Python 3.6.

## Historical status

- Implementation: supplied merged diff, available 2021-03-14.
- Tests: supplied assertions at that commit; historical execution is unknown.
- Later qualification: changed-test-file scope only, checked 2026-10-03, two fail-to-pass and 47 pass-to-pass cases. This is a provenance attestation after the cutoff, not pre-cutoff learned content.
- Whole-project regression and cross-project transfer: untested in the supplied qualification.

The Actions reconstruct the supported repair mechanism as conditional reusable operations. They do not claim that each current probe or validation command was historically executed.
