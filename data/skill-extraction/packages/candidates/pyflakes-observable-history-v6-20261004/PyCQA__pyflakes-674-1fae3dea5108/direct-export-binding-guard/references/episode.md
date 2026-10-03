# Historical episode

Authoritative SourceRecord: `PyCQA/pyflakes:674:repair:1fae3dea5108`

Repository: `PyCQA/pyflakes`  
Bug cluster: `PyCQA/pyflakes:674`  
Fix: `PyCQA/pyflakes:pr:675`  
Revision: `1fae3dea5108a006d35da9e9ab785ca1ed1bc998`

## Reported failure

The reporter installed `pyflakes==2.4.0`, placed this source in `foo.py`, and ran `pyflakes foo.py`:

```python
__all__, = (
    "fizz",
    "buzz",
)
```

The reported traceback reached `pyflakes/checker.py` at:

```python
if isinstance(source.value, (ast.List, ast.Tuple)):
```

and ended with:

```text
AttributeError: 'Tuple' object has no attribute 'value'
```

The report identified a source-shape mismatch involving indirect targets. Its suggestion to mark the input invalid was not the behavior implemented by the merged fix. This is static-analysis robustness, not a guarantee that the reproduction executes successfully as Python code.

## Merged implementation

In historical `pyflakes/checker.py`, the specialized branch gained an immediate-parent gate:

```python
elif (
        name == '__all__' and
        isinstance(self.scope, ModuleScope) and
        isinstance(
            node._pyflakes_parent,
            (ast.Assign, ast.AugAssign, ast.AnnAssign)
        )
):
    binding = ExportBinding(name, node._pyflakes_parent, self.scope)
```

Previously, this branch checked only the name and module scope. The supplied diff retained surrounding binding branches. An enclosing assignment is not sufficient: a name inside a tuple target has a tuple as its immediate parent.

## Committed regression assertion

Historical `pyflakes/test/test_imports.py` added:

```python
def test_ignored_when_not_directly_assigned(self):
    self.flakes('''
    import bar
    (__all__,) = ("foo",)
    ''', m.UnusedImport)
```

This asserts ordinary unused-import behavior despite an indirect `__all__` assignment. The regression's one-element right-hand side differs from the original reproduction's two strings.

The supplied evidence is a committed assertion, not a historical passing-run log. Historical test execution status is unknown.

## Later qualification

The supplied attestation was checked at `2026-10-03T19:13:39.334383+00:00`. It reports verified resolution, one fail-to-pass case, and 131 pass-to-pass cases under changed-test-files-with-original-base-control qualification. Whole-project regression and cross-project transfer are untested. This is later provenance only.

The authored inspection and validation operations are evidence-grounded instructions for current use, not claims of additional historical execution.

## Evidence

- [Title](evidence/title.md)
- [Report and reproduction](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Regression assertion](evidence/regression.md)
