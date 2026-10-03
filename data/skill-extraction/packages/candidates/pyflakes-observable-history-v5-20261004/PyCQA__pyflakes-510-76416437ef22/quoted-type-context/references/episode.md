# Historical episode

Source: `PyCQA/pyflakes:510:repair:76416437ef22`.

The [issue title](evidence/title.md) describes a spurious unused-import warning for a type annotation used in a quoted cast. The [report](evidence/body.md) supplies:

```python
from typing import Union, cast

x = cast('Union[str, int]', 42)
reveal_type(x)
```

The reported analyzer output marked `typing.Union` unused and `reveal_type` undefined. The reporter explicitly considered the latter diagnostic correct.

The [merged implementation](evidence/fix.md), available on 2020-03-17, changed the historical annotation traversal owner at `pyflakes/checker.py`. It generalized typing-member recognition, introduced a restoring annotation context manager, processed recognized typing subscriptions in annotation context, and specially handled a quoted first argument of recognized `cast` calls before ordinary child traversal.

The [regression additions](evidence/regression.md) in historical `pyflakes/test/test_type_annotations.py` asserted clean analysis for partially quoted `Optional` and nested `Callable` assignments, quoted `cast`, renamed direct imports, and a string-valued second cast argument. These are historical assertions, not supplied historical execution logs.

## Qualification boundary

A qualification checked on 2026-10-03 reports verified resolution with four fail-to-pass and 31 pass-to-pass cases. Its scope is changed test files with original-base control. Whole-project regression and cross-project transfer were not tested. It is recorded in [provenance](provenance.json), separately from the four pre-cutoff evidence entries.

## Reuse boundary

Current owners and commands must be located afresh. The historical implementation recognizes direct imported aliases using import bindings and simple attributes rooted at the literal names `typing` or `typing_extensions`. It does not establish support for arbitrary module aliases or arbitrary callables named `cast`.
