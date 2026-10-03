# Historical episode

SourceRecord: `PyCQA/pyflakes:605:repair:43541ee1dd39`

The report described an annotation-related regression in which an annotation-only declaration of `__all__` clobbered an existing `ExportBinding`, so an exported import was no longer considered used.

The public reproduction was:

```python
from typing import TYPE_CHECKING, List

from y import z

if not TYPE_CHECKING:
    __all__ = ("z",)
else:
    __all__: List[str]
```

The repair changed the scope insertion logic in historical `pyflakes/checker.py` from unconditional replacement to:

```python
# don't treat annotations as assignments if there is an existing value
# in scope
if value.name not in self.scope or not isinstance(value, Annotation):
    self.scope[value.name] = value
```

Thus a new name can still receive an annotation binding, and a non-annotation incoming binding still replaces the previous binding. The preceding propagation of `.used` state was not removed by the supplied diff.

Historical `pyflakes/test/test_type_annotations.py` added `test_type_annotation_clobbers_all`, guarded by `skipIf(version_info < (3, 6), 'new in Python 3.6')`. Its `self.flakes(...)` call supplied no expected diagnostics for the reproduction above.

The workflow is a conditional operational reconstruction of this repair, not an assertion that every inspection or validation operation below was historically executed. The original report suggested `setdefault`; the merged guard is narrower and permits ordinary replacement.

The authoritative source predates the cutoff. The 2026 qualification is retained separately in provenance; it is not backdated into the historical evidence.
