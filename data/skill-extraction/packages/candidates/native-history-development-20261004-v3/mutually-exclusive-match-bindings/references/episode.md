# Historical episode

Episode: `PyCQA/pyflakes:771`. Canonical Workflow:
`mutually-exclusive-match-bindings`.

The [title](evidence/title.md) identifies an F811 false positive.
The [report](evidence/body.md) contrasted two functions. Both defined `fun`
in separate branches and returned it afterward. The `if`/`else` example
did not produce the reported warning, while the `match` example with
`case True` and `case False` produced:

```text
redef.py:24:13: redefinition of unused 'fun' from line 19
```

The reporter used pyflakes 3.0.1, Python 3.10.8 on Linux.

The [merged implementation](evidence/fix.md) changed
`pyflakes/checker.py`, in `getAlternatives(n)`. The `ast.If` result remained
`[n.body]`. The `ast.Try` condition changed from `if` to `elif`, retaining
`[n.body + n.orelse] + [[hdl] for hdl in n.handlers]`. It added:

```python
elif sys.version_info >= (3, 10) and isinstance(n, ast.Match):
    return [mc.body for mc in n.cases]
```

The [regression](evidence/regression.md) added
`TestMatch.test_defined_in_different_branches` in
`pyflakes/test/test_match.py`. It defined `y` in `case 1` and `case _`,
then returned `y`. Its `self.flakes(...)` call supplied no expected diagnostics.
This is a historical assertion, not a supplied historical execution transcript.

PR 772 merged as `f2671ffe1785754f0e73d148635cbb38e673e169` at
2023-04-25T23:37:22Z. The [PR reference](evidence/pr-event.md) supplies identity
metadata. The [Ruff reference](evidence/cross-reference.md) supplies only an
issue identity, not an independent fix or cross-project validation.

## Separate qualification

The supplied qualification was checked at
2026-10-03T17:33:21.585847+00:00 and reports verified resolution, one
fail-to-pass and seven pass-to-pass cases under
`changed-test-files-with-original-base-control`. Whole-project regression and
cross-project transfer are untested. The exact attestation is retained in
[provenance](provenance.json), separately from pre-cutoff evidence.

## Adaptation boundary

Current operations reconstruct the supported repair mechanism; they are not an
execution log. Historical paths must not be silently reused as current bindings.
Sequential-redefinition and adjacent-behavior controls are current preservation
obligations, not claims that those particular controls were run historically.
