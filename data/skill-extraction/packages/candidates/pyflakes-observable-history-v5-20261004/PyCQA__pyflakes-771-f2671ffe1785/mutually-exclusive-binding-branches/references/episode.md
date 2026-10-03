# Historical episode

SourceRecord: `PyCQA/pyflakes:771:repair:f2671ffe1785`

The report compared two Python functions returning a locally defined `fun`. An `if`/`else` version defined `fun` separately in its two branches without the reported warning. A `match` version defined it in `case True` and `case False`, and the reporter observed:

```text
redef.py:24:13: redefinition of unused 'fun' from line 19
```

The reported environment was Pyflakes 3.0.1, Python 3.10.8, Linux. This is the reporter's observation, not a package execution result.

At revision `f2671ffe1785754f0e73d148635cbb38e673e169`, the historical owner was `getAlternatives` in `pyflakes/checker.py`. The implementation retained the `ast.If` alternative `[n.body]` and the `ast.Try` alternatives `[n.body + n.orelse] + [[hdl] for hdl in n.handlers]`. It added:

```python
elif sys.version_info >= (3, 10) and isinstance(n, ast.Match):
    return [mc.body for mc in n.cases]
```

The historical regression owner was `pyflakes/test/test_match.py`. Its added `test_defined_in_different_branches` used `case 1` and `case _`, each defining `y`, followed by `return y`. The test calls `self.flakes` with no expected diagnostics.

These paths identify historical artifacts only. Current owners must be located before use.

## Resolution and qualification

The supplied authoritative source marks the repair as verified. The qualification attestation was checked on `2026-10-03T19:13:50.426845+00:00`, after the package knowledge cutoff. It reports one fail-to-pass and seven pass-to-pass outcomes under `changed-test-files-with-original-base-control`. It is contemporary provenance, not pre-cutoff learned content and not evidence of historical test execution.

Links: [report](evidence/body.md), [title](evidence/title.md), [implementation](evidence/fix.md), [regression assertion](evidence/regression.md).
