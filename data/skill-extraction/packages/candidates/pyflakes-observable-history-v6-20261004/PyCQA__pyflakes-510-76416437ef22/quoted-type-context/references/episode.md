# Historical episode

Source: `PyCQA/pyflakes:510:repair:76416437ef22`.

The [report](evidence/body.md) used:

```python
from typing import Union, cast
x = cast('Union[str, int]', 42)
reveal_type(x)
```

The reported analyzer output incorrectly classified `Union` as unused. The report explicitly regarded the undefined `reveal_type` diagnostic as correct. The issue [title](evidence/title.md) identifies the same symptom.

The [merged implementation](evidence/fix.md), at revision `76416437ef22077b5e2949e78fa3000b3580e319`, changed historical `pyflakes/checker.py`:

- Introduced `TYPING_MODULES` for `typing` and `typing_extensions`.
- Generalized typing recognition through `_is_typing_helper`, checking scoped `ImportationFrom` bindings using `module` and `real_name`.
- Added `_is_any_typing_member` while retaining specific-member recognition through `_is_typing`.
- Added `_enter_annotation`, saving and restoring `_in_annotation` in `finally`, and reused it in the existing annotation decorator.
- Entered annotation context for children of subscriptions rooted in a recognized typing member, in the non-special-Literal branch.
- For a recognized `cast` with at least one positional argument and an `ast.Str` first argument, visited that first argument in annotation context, then retained normal child traversal.

Historical `pyflakes/test/test_type_annotations.py` added [assertions](evidence/regression.md) for partially quoted and nested type assignments, quoted casts, a runtime string in the second cast argument, and renamed imports. The diff does not supply historical test-run output.

A contemporary qualification, recorded separately in provenance, reports changed-test-file checks with original-base control: four fail-to-pass and 31 pass-to-pass. Its date is after the cutoff and it is not pre-cutoff learned content. It does not establish whole-project safety.

The reusable lesson is to enter existing annotation traversal only at semantically recognized type-bearing positions, while restoring context and retaining adjacent string behavior. The package does not infer that every typing API argument is a type expression.
