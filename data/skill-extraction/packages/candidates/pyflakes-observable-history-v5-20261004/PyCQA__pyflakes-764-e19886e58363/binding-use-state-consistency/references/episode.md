# Historical episode

SourceRecord: `PyCQA/pyflakes:764:repair:e19886e58363`.

The original report described a version 3.0 regression, reproduced with 3.0.1. An annotation-only module binding, an attribute read of that binding, and a same-name local assignment together caused `TypeError: 'bool' object is not subscriptable`. The report stated that removing any of those components avoided the exception. It reported that version 2.5.0 instead emitted undefined-name and unused-local diagnostics.

The traceback reached `handleNodeStore` in historical `pyflakes/checker.py`, where a truthy `used` value was indexed:

```python
if used and used[0] is self.scope and name not in self.scope.globals:
```

The merged implementation changed the annotation-read branch in that same historical file:

```diff
 if isinstance(binding, Annotation) and not self._in_postponed_annotation:
-    scope[name].used = True
+    scope[name].used = (self.scope, node)
     continue
```

The historical regression was added to `pyflakes/test/test_type_annotations.py`:

```python
def test_unused_annotation_in_outer_scope_reassigned_in_local_scope(self):
    self.flakes('''
    x: int
    x.__dict__
    def f(): x = 1
    ''', m.UndefinedName, m.UnusedVariable)
```

These paths describe the historical repair, not guaranteed locations in a current checkout.

## Resolution and execution status

The authoritative source marks this repair as independently verified. The supplied historical implementation and test establish the repair and asserted diagnostics at revision `e19886e583637a7e2eec428cc036094b9630f2d0`. No historical execution transcript was supplied.

A qualification checked in 2026 reports one fail-to-pass and 43 pass-to-pass results within changed test files, using original-base control. That is a later provenance attestation, not pre-cutoff knowledge. It does not establish whole-project regression safety or cross-project transfer.

## Evidence

- [Issue title](evidence/title.md)
- [Original report and traceback](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Regression assertions](evidence/regression.md)

The [workflow](workflow.md) records the sourced repair dependency model. The executable-looking evaluation files are definitions only, not execution results.
