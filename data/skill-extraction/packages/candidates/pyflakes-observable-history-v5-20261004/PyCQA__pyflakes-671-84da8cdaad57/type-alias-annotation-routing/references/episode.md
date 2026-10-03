# Historical episode

## Identity

- SourceRecord: `PyCQA/pyflakes:671:repair:84da8cdaad57`
- Issue cluster: `PyCQA/pyflakes:671`
- Fix: `PyCQA/pyflakes:pr:679`
- Revision: `84da8cdaad574df7e692dff06ab561acc63d521c`
- Fix evidence available: `2022-02-13T16:32:09Z`

## Report

The reporter used pyflakes 2.4.0 on Python 3.8.6. An explicit alias, `PathLikeStr: TypeAlias = "PathLike[str]"`, caused an unused-import diagnostic for `os.PathLike`. The report selected `TypeAlias` from `typing` on Python 3.10 or newer and from `typing_extensions` otherwise.

Quoted function parameter and return annotations using `PathLike[str]` did not produce that diagnostic in the contrasting example.

## Implementation

The historical owner was `Checker.ANNASSIGN` in `pyflakes/checker.py`.

The change retained target processing and annotation processing. For a present value, it introduced:

```python
if _is_typing(node.annotation, 'TypeAlias', self.scopeStack):
    self.handleAnnotation(node.value, node)
else:
    self.handleNode(node.value, node)
```

The guard for a present value remained. The same diff corrected the type comment on `_is_name_or_attr` from `ast.Ast` to `ast.AST`; that incidental correction is not part of this workflow's required mechanism.

## Regression assertions

The historical regression owner was `pyflakes/test/test_type_annotations.py`, in `TestTypeAnnotations.test_TypeAlias_annotations`, guarded for Python 3.6 and newer.

Added assertions used `typing_extensions.TypeAlias` and covered:

- Unquoted `Bar` at module scope.
- Quoted `'Bar'` at module scope.
- Unquoted `Bar` in a class body.
- Quoted `'Bar'` in a class body.
- A `TypeAlias` declaration without a value.
- A value-less declaration alongside an otherwise unused imported `Bar`, expecting `UnusedImport`.

These are historical test definitions, not a claim that a historical test command was executed.

## Evidence

- [Issue title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Regression assertions](evidence/regression.md)

## Qualification boundary

The supplied later attestation was checked at `2026-10-03T19:13:37.470456+00:00`. It reports verified resolution under `changed-test-files-with-original-base-control`, with one fail-to-pass and 51 pass-to-pass cases. Its scope excludes whole-project regression and cross-project transfer. It is retained separately in [provenance](provenance.json), not presented as an event available before the cutoff.
