# Historical episode

Source: `PyCQA/pyflakes:447:repair:c9708a18a17f`.

The original report described Pyflakes 2.1.1 on Python 3.5.2 warning that `queue.Queue` was unused in:

```python
from queue import Queue
from typing import Optional

def foo(queue: Optional['Queue[int]'] = None) -> None:
    print(queue)
```

Quoting the complete annotation, `'Optional[Queue[int]]'`, was reported as a workaround. This contrast localized the issue to traversal of a quoted fragment inside an otherwise unquoted annotation.

The supplied merged implementation introduced annotation-context tracking, string-node handling within that context, a `Literal` exclusion, and special treatment for strings encountered while deferred work was already running. It generalized typing-name recognition while retaining overload handling.

The added regression assertions covered partially quoted return annotations, recognized `Literal` values, doubly quoted annotations, postponed annotations, and qualified `typing_extensions.overload`.

Historical owners were in `pyflakes/checker.py`; regression assertions were in `pyflakes/test/test_type_annotations.py`. These paths are historical locators, not current bindings.

The Workflow and Actions reconstruct a reusable repair procedure from the supplied report, diff, and assertions. They are not a claim that this precise task plan was historically executed. Historical test execution is unknown from the supplied core entries.

A qualification checked in 2026 reported verified resolution within changed test files using an original-base control: four fail-to-pass and 25 pass-to-pass cases. Its scope excludes whole-project regression and cross-project transfer. Its timestamp is later than the authoritative cutoff and it is retained only as a provenance attestation.
