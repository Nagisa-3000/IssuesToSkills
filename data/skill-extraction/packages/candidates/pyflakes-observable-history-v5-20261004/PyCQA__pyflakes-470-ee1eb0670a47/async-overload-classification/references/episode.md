# Historical episode

Authoritative source: `PyCQA/pyflakes:470:repair:ee1eb0670a47`.

The [title](evidence/title.md) is “@overload of async functions”. The [report](evidence/body.md) shows synchronous overloads accepted while equivalent async overloads produce:

```text
18:1 redefinition of unused 'g' from line 14
22:1 redefinition of unused 'g' from line 18
```

The reported command was `python -m pyflakes .`; it is not a current command binding.

At revision `ee1eb0670a473a30f32208b7bd811282834486a6`, the [merged implementation](evidence/fix.md) changes historical path `pyflakes/checker.py`:

```python
if PY35_PLUS:
    FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
else:
    FUNCTION_TYPES = (ast.FunctionDef,)
```

In `is_typing_overload(value, scope_stack)`, the source-node guard changes from `isinstance(value.source, ast.FunctionDef)` to `isinstance(value.source, FUNCTION_TYPES)`. The existing decorator scan remains unchanged.

The [regression](evidence/regression.md) changes historical path `pyflakes/test/test_type_annotations.py`. It adds `test_typingOverloadAsync`, guarded by `@skipIf(version_info < (3, 5), 'new in Python 3.5')`. The source passed to `self.flakes` contains two decorated async declarations with type comments and an async implementation, without expected diagnostic arguments.

These are recorded implementation and test-assertion facts, not an invented historical execution sequence. Current inspection and validation operations reconstruct the corresponding public checks.

A qualification dated 2026-10-03 attests verified resolution in changed test files with original-base control: one fail-to-pass and 23 pass-to-pass cases. It is post-cutoff provenance metadata, not historical learned content. No whole-project regression or cross-project transfer was tested.
