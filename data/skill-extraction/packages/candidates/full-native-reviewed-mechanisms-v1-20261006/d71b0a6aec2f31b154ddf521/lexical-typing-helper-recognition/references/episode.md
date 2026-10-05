# Supporting historical episodes

Two distinct clusters and fixes in `PyCQA/pyflakes` support this local template. Operational decompositions are authored guidance, not historical execution traces.

## Issue 434

Source: `PyCQA/pyflakes:434:repair:232cb1d27ee1`.

The report described F811 between overload declarations and implementation, including methods using module-level `from typing import overload` and functions with additional decorators.

Historical `pyflakes/checker.py`, revision `232cb1d27ee134bf96adc8f37e53589dc259b159`, changed `is_typing_overload` to accept `scope_stack`. Bare names traverse reversed scopes and terminate at the first binding, accepting only `ImportationFrom/fullName == typing.overload`. The diagnostic consumer passes `self.scopeStack`.

The fix also replaces singleton decorator recognition with any-match, retaining `ast.FunctionDef` and the existing attribute branch. This companion is not another independent source.

Historical `pyflakes/test/test_type_annotations.py` adds `test_overload_in_class` and `test_overload_with_multiple_decorators`, both expecting no diagnostics. Historical execution is unknown; dedicated new shadowing assertions are not supplied.

Evidence: [title](evidence/434-title.md), [body](evidence/434-body.md), [fix](evidence/434-fix.md), [regressions](evidence/434-regression.md).

## Issue 561

Source: `PyCQA/pyflakes:561:repair:13cad915e6b1`.

The report combines `typing as ty`, directly imported aliased Literal and `@ty.overload`, reporting undefined name `none`.

Historical `pyflakes/checker.py`, revision `13cad915e6b181b2f6a85efc2ead4856b23bccc0`, adds `_module_scope_is_typing` inside `_is_typing_helper`. Reversed-scope lookup terminates at the first binding and requires `Importation/fullName` membership in `TYPING_MODULES`, replacing receiver spelling membership. The simple-name receiver restriction, attribute matcher and direct-name branch remain.

Historical `pyflakes/test/test_type_annotations.py` adds `test_aliased_import`, expecting no diagnostics for two `@t.overload` declarations and implementation after `import typing as t`. It does not establish every renamed-Literal claim. Historical execution is unknown; dedicated new shadowing assertions are not supplied.

Evidence: [title](evidence/561-title.md), [body](evidence/561-body.md), [fix](evidence/561-fix.md), [regression](evidence/561-regression.md).

## Independent qualification boundary

Complete supplied reports pin base/fix identities and direct closure evidence. Original-base, base-with-committed-regression and historical-fixed observations use consistent runtime digests.

The 2026-10-04 replay of 434 records original base 15 passed, base with regressions 2 failed/15 passed and fixed 17 passed. The failing assertions are class-contained and multiple-decorator overload. The replay of 561 records original base 50 passed, base with regression 1 failed/50 passed and fixed 51 passed; the failing assertion is aliased overload. Existing checks remain passing in both comparisons.

These validation-only records qualify changed test files with original-base control. Neither checks whole-project regression or is a formal SWE run. They do not backdate historical execution or execute authored functional definitions. Exact hashes and validation times are retained in provenance.

The [primary](workflow.md) and [additional](realizations/561.md) realizations each cover only their own sourced Actions.
