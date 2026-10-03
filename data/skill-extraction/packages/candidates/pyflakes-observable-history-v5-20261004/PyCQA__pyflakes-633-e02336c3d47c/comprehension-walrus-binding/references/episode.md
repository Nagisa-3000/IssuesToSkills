# Historical episode

Source: `PyCQA/pyflakes:633:repair:e02336c3d47c`.

The [title](evidence/title.md) identified assignment-expression targets in comprehensions as belonging to an outer scope. The [report](evidence/body.md) described a generator expression passed to `any`: `match := pattern.match(item)` was followed by `match.group(0)`. The reporter observed working runtime output, `JOHN`, but an F821 undefined-name warning for `match`, using pyflakes 2.3.1 through flake8 3.9.2 on CPython 3.9.5.

The [implementation](evidence/fix.md), available on 2022-05-30, changed historical `pyflakes/checker.py`. It introduced `NamedExprAssignment(Assignment)`, classified stored names whose parent statement was `ast.NamedExpr` under the Python 3.8+ guard, and changed insertion to walk backward over consecutive `GeneratorScope` entries only for that binding type. The resulting insertion targeted the nearest non-generator scope.

The [regression assertions](evidence/regression.md) added two Python 3.8+-guarded tests in historical `pyflakes/test/test_other.py`: a generator expression whose target was subsequently printed, and nested comprehensions whose two targets were subsequently printed. Both called `self.flakes` without expected diagnostics. The supplied historical record contains these assertions, not a contemporaneous test-run transcript.

A later qualification attestation verified resolution on changed test files with an original-base control: two fail-to-pass and 123 pass-to-pass cases. It was checked on 2026-10-03, after the authoritative cutoff. It is retained only as provenance and does not establish whole-project or cross-project behavior.

Historical filenames are documentation, not authorized bindings to a current checkout.
