# Historical episode

Authoritative repair source: `PyCQA/pyflakes:470:repair:ee1eb0670a47`.

The [title](evidence/title.md) concerns async overloads. The [report](evidence/body.md) supplies synchronous and asynchronous sequences, each with two overload declarations followed by an implementation. It reports two unused-redefinition warnings for the async sequence, while synchronous overloads already worked.

The [implementation](evidence/fix.md) adds a runtime-guarded `FUNCTION_TYPES` tuple and uses it in `is_typing_overload`. Under `PY35_PLUS`, the tuple contains `ast.FunctionDef` and `ast.AsyncFunctionDef`; otherwise it contains only `ast.FunctionDef`. The existing decorator-list recognition check remains.

The [regression assertion](evidence/regression.md) adds `test_typingOverloadAsync`, skipped below Python 3.5. It calls `self.flakes` with two decorated async declarations using type comments and `pass`, followed by an undecorated async implementation returning its argument. No expected diagnostics are supplied.

Historical implementation owner: `pyflakes/checker.py`. Historical regression owner: `pyflakes/test/test_type_annotations.py`. These paths are context, not bindings for another checkout.

The Workflow reconstructs the supported repair mechanism and its public validation obligations. Supplied historical evidence does not establish execution of this reconstructed sequence or of broader adjacent controls.

A qualification checked on 2026-10-03 reports one fail-to-pass and 23 pass-to-pass cases within changed test files, with original-base control. Whole-project regression and cross-project transfer are untested. This later attestation is not a backdated historical event. Its exact metadata is retained in [provenance](provenance.json).
