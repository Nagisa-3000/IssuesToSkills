# Historical episode: boolean usage state in an annotation binding

Source repair ID: `PyCQA/pyflakes:764:repair:e19886e58363`.

The original report described a regression in version 3.0, reproduced with version 3.0.1:

```python
test: int

test.__dict__


def fn():
    test = 1
```

Analysis crashed in `handleNodeStore` at:

```python
if used and used[0] is self.scope and name not in self.scope.globals:
```

The report said version 2.5.0 instead emitted an undefined-name diagnostic for the outer load and an unused-local diagnostic for the function assignment. Removing any of the annotation, attribute load, or local assignment avoided the reported exception. These are reporter observations, not newly executed results.

At historical revision `e19886e583637a7e2eec428cc036094b9630f2d0`, the merged implementation changed this branch in `pyflakes/checker.py`:

```python
binding = scope.get(name, None)
if isinstance(binding, Annotation) and not self._in_postponed_annotation:
    scope[name].used = (self.scope, node)
    continue
```

Only the assignment changed, from `scope[name].used = True`. The guard and `continue` remained. The structured value records the current scope and load node rather than only truthiness.

The added assertion in `pyflakes/test/test_type_annotations.py` was:

```python
def test_unused_annotation_in_outer_scope_reassigned_in_local_scope(self):
    self.flakes('''
    x: int
    x.__dict__
    def f(): x = 1
    ''', m.UndefinedName, m.UnusedVariable)
```

This is a regression assertion available at the historical commit. No historical test-run output is supplied.

## Qualification, separately dated

The supplied qualification attestation was checked at `2026-10-03T19:13:49.111996+00:00`. Its scope is `changed-test-files-with-original-base-control`; it records verified resolution, one fail-to-pass case, and 43 pass-to-pass cases. Whole-project regression and cross-project transfer are untested. This attestation is recorded in [provenance](provenance.json), not as a pre-cutoff evidence event.

## Evidence

- [Issue title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Regression assertion](evidence/regression.md)

The reusable Workflow's inspection and validation instructions are authored operational guidance from these observations, not a claim that the historical maintainer executed that exact sequence.
