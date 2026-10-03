# Historical episode

SourceRecord: `PyCQA/pyflakes:771:repair:f2671ffe1785`

Repository: `PyCQA/pyflakes`  
Issue cluster: `PyCQA/pyflakes:771`  
Repair: `PyCQA/pyflakes:pr:772`  
Revision: `f2671ffe1785754f0e73d148635cbb38e673e169`

## Report

The [title](evidence/title.md) identifies an F811 false positive. The [body](evidence/body.md) reports Pyflakes 3.0.1 on Python 3.10.8/Linux. A function using `if`/`else` defined `fun` separately in its two branches without the complained-of diagnostic. A corresponding function using `match` with `case True` and `case False` produced:

```text
redef.py:24:13: redefinition of unused 'fun' from line 19
```

Both examples returned `fun` after the branch construct.

## Implementation

At the historical path `pyflakes/checker.py`, `getAlternatives(n)` already returned `[n.body]` for `ast.If` and `[n.body + n.orelse] + [[hdl] for hdl in n.handlers]` for `ast.Try`. The [repair](evidence/fix.md) changed the second condition to `elif` and added:

```python
elif sys.version_info >= (3, 10) and isinstance(n, ast.Match):
    return [mc.body for mc in n.cases]
```

This is a shared branch-classification change, not a blanket suppression of F811 and not the creation of a separate lexical scope per case.

## Regression

At the historical path `pyflakes/test/test_match.py`, the repair added `test_defined_in_different_branches`. It passed a function containing a match with `case 1` and `case _`, each defining `y`, followed by `return y`, to `self.flakes` without expected diagnostics. See [the assertion evidence](evidence/regression.md).

The supplied historical entries establish the code and assertion at the merged revision, not a historical test-run transcript.

## Qualification boundary

The later qualification is recorded verbatim in [provenance](provenance.json). Its checked-at timestamp is after the cutoff and is not pre-cutoff learned content. It supports verified resolution within changed test files only. It does not establish whole-project regression coverage or cross-project applicability.
