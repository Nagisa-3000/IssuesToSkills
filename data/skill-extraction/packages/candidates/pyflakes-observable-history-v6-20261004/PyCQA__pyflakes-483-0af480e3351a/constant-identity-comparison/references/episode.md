# Historical episode

SourceRecord: `PyCQA/pyflakes:483:repair:0af480e3351a`

The original [title](evidence/title.md) and [report](evidence/body.md) concerned Python 3.8's `SyntaxWarning` for `is` with a literal. The reproduction assigned `x = 5`, then used `if x is ():`. The report showed `python3 -m py_compile test.py` emitting the warning and asked for analyzer coverage because provoking the warning through pytest was difficult.

The [merged implementation](evidence/fix.md) extended an existing literal-identity diagnostic. Historical owners were:
- `pyflakes/checker.py`: singleton and constant predicates, and `Checker.COMPARE`.
- `pyflakes/messages.py`: `IsLiteral` wording.
- `pyflakes/test/test_is_literal.py`: [regression assertions](evidence/regression.md).

The implementation recognized version-dependent singleton AST forms, recursively constant tuples, and non-singleton constants. It checked both operands for each identity comparison and advanced the left operand through chained comparisons. It broadened the diagnostic wording to mention constant literals including float and tuple.

The regression additions asserted a diagnostic for an empty tuple and a recursively constant tuple containing numbers, a string, a boolean, and nested tuples. They asserted no diagnostic for a tuple containing a variable.

These assertions were available at the merged revision on 2020-02-17. No historical test execution result is supplied. The implementation and tests are recorded as historical facts, not as a universally applicable current patch.

## Later qualification, not pre-cutoff learned content

A qualification checked at `2026-10-03T19:13:20.396117+00:00` reported verified resolution, two fail-to-pass cases, and 28 pass-to-pass cases. Its scope was `changed-test-files-with-original-base-control`. Whole-project regression and cross-project transfer were untested. This later attestation is retained in provenance and is not backdated into the historical evidence cards.

The canonical reusable [workflow](workflow.md) adapts this mechanism only after inspecting current owners and binding current public validation.
