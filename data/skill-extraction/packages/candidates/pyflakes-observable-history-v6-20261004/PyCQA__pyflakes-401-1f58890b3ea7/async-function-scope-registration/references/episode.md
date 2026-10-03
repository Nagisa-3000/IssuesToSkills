# Historical episode

Authoritative source: `PyCQA/pyflakes:401:repair:1f58890b3ea7`.

The report described a Python 3.7 crash analyzing a module-level class `foo` followed by `async def func(foo: foo): pass`. Its traceback passed through deferred function analysis, `ARGUMENTS`, `ARG`, argument binding, scope lookup, and parent traversal. `ARG` constructed `Argument(node.arg, self.getScopeNode(node))`; `addBinding` called `getParent(value.source)`; traversal then attempted to access `Module.parent`.

The report suspected revision `9dd73ec54411a563410872b47e76f0f89f34ecfe` introduced the bug. This is reported attribution, not independently established causal evidence.

## Implementation

The supplied merged diff in `pyflakes/checker.py` added:

```python
if PY35_PLUS:
    _ast_node_scope[ast.AsyncFunctionDef] = FunctionScope,
```

The trailing comma is part of the supplied assignment. The current repair must inspect the registry's actual value representation rather than silently substituting a different representation. The historical diff registers asynchronous function definitions under the Python 3.5-plus gate; it does not change parent traversal.

## Regression assertion

The supplied diff in `pyflakes/test/test_type_annotations.py` added:

```python
@skipIf(version_info < (3, 5), 'new in Python 3.5')
def test_annotated_async_def(self):
    self.flakes('''
    class c: pass
    async def func(c: c) -> None: pass
    ''')
```

No diagnostic arguments were passed to `self.flakes`. This is a historical assertion of analysis without expected diagnostics, available at the repair commit. Historical execution status is unknown because no execution log was supplied.

## Qualification boundary

The supplied later attestation was checked at `2026-10-03T19:13:07.955941+00:00`. It records verified resolution with original-base control, one fail-to-pass case, and eleven pass-to-pass cases, restricted to changed test files. Whole-project regression and cross-project transfer remain untested.

This attestation qualifies provenance; it is not pre-cutoff learned content and does not establish a historical execution event. Inspection and validation instructions in this package are conditional operational reconstructions grounded in the report, implementation, and regression, not claims of an observed historical command sequence.

See [title](evidence/title.md), [report](evidence/body.md), [implementation](evidence/fix.md), and [regression](evidence/regression.md).
