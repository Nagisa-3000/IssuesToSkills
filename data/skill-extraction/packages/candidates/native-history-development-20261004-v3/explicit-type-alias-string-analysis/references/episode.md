# Historical episode

Source: `PyCQA/pyflakes:671`. Resolution: pull request 679, merged revision `84da8cdaad574df7e692dff06ab561acc63d521c`.

The reporter used pyflakes 2.4.0 on Python 3.8.6/Linux and reported an unused `os.PathLike` import for:

```python
import sys
from os import PathLike

if sys.version_info[:2] >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

PathLikeStr: TypeAlias = "PathLike[str]"
```

The reported output was `foo.py:2:1 'os.PathLike' imported but unused`. A comparison using `"PathLike[str]"` in function parameter and return annotations produced no output.

The merged change in historical `pyflakes/checker.py`, `Checker.ANNASSIGN`, preserved target and annotation processing. Inside `if node.value`, it selected `handleAnnotation(node.value, node)` when `_is_typing(node.annotation, 'TypeAlias', self.scopeStack)` held, and retained `handleNode(node.value, node)` otherwise. An incidental type-comment correction from `ast.Ast` to `ast.AST` is not this Workflow's repair mechanism.

Historical `pyflakes/test/test_type_annotations.py` added `test_TypeAlias_annotations`, gated for Python 3.6 or later. Its six assertions used `typing_extensions.TypeAlias`:
- module-level and class-level `Bar` values: no diagnostics;
- module-level and class-level `'Bar'` values: no diagnostics;
- `bar: TypeAlias` without a value: no diagnostics;
- the no-value declaration with otherwise unused imported `Bar`: `m.UnusedImport`.

These are assertions available at the merged commit, not invented historical execution results. Completed closure metadata identifies the merged fix. Later qualification is recorded separately in provenance and is changed-test-only.

## Evidence index

- [Issue title](evidence/title.md)
- [Reported reproduction](evidence/body.md)
- [Maintainer localization](evidence/localization.md)
- [Contributor response](evidence/contributor-response.md)
- [Pull-request reference](evidence/pr-reference.md)
- [Completed closure](evidence/closure.md)
- [Merged implementation](evidence/fix.md)
- [Regression assertions](evidence/regression.md)
