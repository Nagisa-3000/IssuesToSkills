# Historical episode

SourceRecord: `PyCQA/pyflakes:561:repair:13cad915e6b1`  
Repository: `PyCQA/pyflakes`  
Repair: `PyCQA/pyflakes:pr:632`  
Revision: `13cad915e6b181b2f6a85efc2ead4856b23bccc0`

The [title](evidence/title.md) and [report](evidence/body.md) describe a false positive after renaming typing imports. The reporter compared PyFlakes 2.2.0 with 2.1.1 and supplied:

```python
import typing as ty
from typing_extensions import Literal as ty_Literal

@ty.overload
def request(
    decoder: ty_Literal["none"] = "none",
) -> None:
    ...
```

The reported symptom was an F821 undefined name `none`, attributed to treating a literal string as a forward reference.

## Supplied repair

In historical `pyflakes/checker.py`, `_is_typing_helper` gained a local `_module_scope_is_typing(name)` helper. It searches `reversed(scope_stack)` and stops at the first scope containing the name. It returns true only when that binding is an `Importation` whose `fullName` belongs to `TYPING_MODULES`; otherwise it returns false. Exhausting the scopes also returns false.

The attribute branch previously checked `node.value.id in TYPING_MODULES`. The repair instead calls `_module_scope_is_typing(node.value.id)`. The existing requirements that the receiver be an `ast.Name` and that `is_name_match_fn(node.attr)` succeed remain in the supplied diff. The direct `ast.Name` branch was not changed by that diff.

## Supplied regression

Historical `pyflakes/test/test_type_annotations.py` gained `test_aliased_import`. It invokes `self.flakes` on a snippet importing `typing as t`, defining two `@t.overload` declarations with `(None) -> None` and `(int) -> int` type comments, and then a concrete implementation of the same function. The assertion encodes acceptance without expected diagnostics.

The supplied diff does not establish execution of this test at the historical commit. Nor does it contain a new direct-import `Literal` alias regression.

## Qualification boundary

A qualification attestation checked at `2026-10-03T19:13:27.933710+00:00` reports verified resolution under `changed-test-files-with-original-base-control`, with one fail-to-pass and fifty pass-to-pass cases. Its runtime digest is retained in [provenance](provenance.json). This is later verification metadata, not a pre-cutoff historical event. Whole-project regression and cross-project transfer remain untested.

The [Workflow](workflow.md) organizes the supplied repair into conditional reusable operations. Its current probes are authored guidance, not a claim that the historical author executed this exact task sequence.
