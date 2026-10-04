# Supporting historical episodes

The reviewed shared mechanism is:

**Extend a synchronous-only AST classification to include asynchronous function definitions under the runtime capability gate, reusing existing function semantics rather than changing downstream analysis.**

## Scope registration

Source: `PyCQA/pyflakes:401:repair:1f58890b3ea7`.

A module-level class `foo` followed by `async def func(foo: foo): pass` crashed during deferred argument binding. The traceback traversed `ARG`, scope lookup, binding, and parent traversal before attempting `Module.parent`. The report's suspected introducing revision is reported attribution, not independently established causality.

The historical implementation in `pyflakes/checker.py` added:

```python
if PY35_PLUS:
    _ast_node_scope[ast.AsyncFunctionDef] = FunctionScope,
```

The trailing comma belongs to the historical assignment. A current edit must inspect the actual registry representation rather than assume a scalar or tuple representation. The implementation did not modify parent traversal.

The committed regression in historical `pyflakes/test/test_type_annotations.py` was skipped below Python 3.5 and asserted no diagnostics for:

```python
class c: pass
async def func(c: c) -> None: pass
```

Cards: [title](evidence/scope-title.md), [body](evidence/scope-body.md), [fix](evidence/scope-fix.md), [regression](evidence/scope-regression.md).

## Overload recognition

Source: `PyCQA/pyflakes:470:repair:ee1eb0670a47`.

The report contrasted working synchronous typing overloads with an async sequence producing two unused-redefinition warnings.

Historical `pyflakes/checker.py` introduced a guarded `FUNCTION_TYPES` tuple: ordinary and async function definitions under `PY35_PLUS`, otherwise ordinary definitions only. `is_typing_overload` used that family while retaining typing decorator recognition.

The committed regression in historical `pyflakes/test/test_type_annotations.py` was skipped below Python 3.5. It asserted no diagnostics for two decorated async declarations with type comments and an undecorated async implementation returning its argument.

Cards: [title](evidence/overload-title.md), [body](evidence/overload-body.md), [fix](evidence/overload-fix.md), [regression](evidence/overload-regression.md).

## Reconstruction and qualification

The two histories remain separate realizations. Each modifying Action combines implementation and coverage; this does not assert a historical command sequence or test execution.

Historical execution logs were not supplied. Later independent replay reports were inspected for pinned issue/fix/revision identity, direct closure evidence, original-base controls, failing base-with-regression targets, passing fixed targets, and consistent runtime identities across all three runs.

The scope replay preserved eleven existing cases; the overload replay preserved 23. Neither checked whole-project regression or cross-project transfer. Replay records qualify already-public artifacts and remain validation-only provenance, not pre-cutoff evidence cards or authored Skill functional successes. Their authoritative hashes are retained in provenance.
