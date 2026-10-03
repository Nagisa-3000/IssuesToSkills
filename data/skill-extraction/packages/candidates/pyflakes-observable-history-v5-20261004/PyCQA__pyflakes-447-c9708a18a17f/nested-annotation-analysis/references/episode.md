# Historical episode: nested quoted annotation import usage

Canonical Workflow ID: `workflow:verified-history:b2b64a5ca411f99a2e3c45e0`

Source episode ID: `PyCQA/pyflakes:447:repair:c9708a18a17f`

## Report

The [title](evidence/title.md) and [body](evidence/body.md), available on 2019-05-28, describe a spurious unused-import warning for a type used only in a nested quoted annotation. The report used:

```python
from queue import Queue
from typing import Optional

def foo(queue: Optional['Queue[int]'] = None) -> None:
    print(queue)
```

The reporter identified pyflakes 2.1.1 on Python 3.5.2 on Linux. Quoting the entire annotation, `'Optional[Queue[int]]'`, was reported as a workaround, not the durable repair.

## Historical implementation

The [merged implementation](evidence/fix.md) was available at revision `c9708a18a17fbf17e0d88c1d1675ac1a926c4565` on 2020-02-14.

Historical owners were in `pyflakes/checker.py`:

- `_is_typing` generalized typing-attribute recognition and was reused by overload recognition.
- `in_annotation` saved and restored annotation context with `try/finally`.
- `handleAnnotation` and `handleStringAnnotation` entered annotation context.
- Deferred postponed annotations invoked an annotation-wrapped node handler.
- `SUBSCRIPT` temporarily suppressed forward-string parsing for recognized `Literal` constructs.
- `STR` parsed nested annotation strings, deferring before deferred processing and calling directly during it.
- Python 3.8+ string-valued `CONSTANT` nodes delegated to `STR`.

These are historical paths and symbols, not automatic bindings in a current checkout.

## Historical regression assertions

The added assertions in `pyflakes/test/test_type_annotations.py` covered partial quoting, nested quoting within a fully quoted annotation, future annotations, Literal strings from both typing modules, multi-value Literal strings, and qualified `typing_extensions.overload`.

The supplied diff records test definitions at the historical commit. It does not supply a historical test-run transcript.

## Verification scope

The authoritative SourceRecord marks the resolution verified. A qualification attestation checked at `2026-10-03T19:13:17.571781+00:00` separately reports 4 fail-to-pass and 25 pass-to-pass checks, scoped to changed test files with original-base control. Its runtime SHA-256 is `e2638f0f36eaf8f7d2aeea4607c51f66d424587388e1d5a5e529fe22d5800c27`.

This later attestation is not pre-cutoff learned content or an additional historical event. Whole-project and cross-project outcomes are unknown.
