# Historical episode

Authoritative source: `PyCQA/pyflakes:401:repair:1f58890b3ea7`.

The report supplied:

```python
class foo:
    pass

async def func(foo: foo):
    pass
```

On the reported Python 3.7 environment, the traceback passed through deferred function processing, argument binding, scope-node lookup, and parent traversal, ending in an attempt to read `parent` from a module.

The merged change in historical `pyflakes/checker.py` added:

```python
if PY35_PLUS:
    _ast_node_scope[ast.AsyncFunctionDef] = FunctionScope,
```

The trailing comma is part of the supplied implementation and makes the value tuple-shaped. A current repair must match its current classifier representation rather than transplant that syntax blindly.

The merged regression in historical `pyflakes/test/test_type_annotations.py` added:

```python
@skipIf(version_info < (3, 5), 'new in Python 3.5')
def test_annotated_async_def(self):
    self.flakes('''
    class c: pass
    async def func(c: c) -> None: pass
    ''')
```

No expected diagnostic arguments were supplied to `self.flakes`. This is a historical assertion, not a supplied historical execution result.

## Evidence

- [Reported title](evidence/title.md)
- [Public reproduction and traceback](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Regression assertion](evidence/regression.md)

## Qualification boundary

The supplied qualification was checked on 2026-10-03 and reports verified resolution: one fail-to-pass case and eleven pass-to-pass cases. It covers changed test files with original-base control only. It does not establish whole-project regression safety or cross-project transfer. It is retained in [provenance](provenance.json) as contemporary attestation, not as pre-cutoff learned content.

The workflow's diagnosis and validation operations are conditional guidance derived from the report and merged changes. The evidence does not establish the chronology of developer operations or historical validation execution.
