# Historical episode

SourceRecord: `PyCQA/pyflakes:574:repair:c23a81037d4f`.

The source identifies issue cluster `PyCQA/pyflakes:574`, fix `PyCQA/pyflakes:pr:580`, and revision `c23a81037d4f68067c4c987985d177ec7664de59`.

The [title](evidence/title.md) and [body](evidence/body.md) report:

```python
from typing import Annotated

Annotated[int, '>1']
```

with diagnostic:

```text
./pyflakes.py:3:16 syntax error in forward annotation '>1'
```

The [merged implementation](evidence/fix.md) changed historical `pyflakes/checker.py`. It introduced `_is_name_or_attr`, retained the existing `Literal` branch through that helper, and introduced a dedicated `Annotated` branch. For multi-argument tuple slices, the first argument retained the inherited annotation context and later arguments were traversed under `AnnotationState.NONE`. Direct `ast.Tuple` and older `ast.Index` wrapping a tuple were supported. Other slices retained normal traversal.

The [regression assertions](evidence/regression.md) were added in historical `pyflakes/test/test_type_annotations.py`:
- `Annotated['integer']`: `m.UndefinedName`;
- `Annotated['integer', 1]`: `m.UndefinedName`;
- `Annotated[int, '> 0']`: no diagnostic;
- `Union[Annotated['int', '>0'], 'integer']`: `m.UndefinedName`.

These are assertions available at the historical commit. The supplied evidence does not include a historical test-run log.

The qualification attestation dated `2026-10-03T19:13:29.506001+00:00` reports verified resolution, two fail-to-pass cases, and forty pass-to-pass cases. It is later provenance, not knowledge backdated before the cutoff. Its scope is changed test files with an original-base control; whole-project regression and cross-project transfer were not tested.
