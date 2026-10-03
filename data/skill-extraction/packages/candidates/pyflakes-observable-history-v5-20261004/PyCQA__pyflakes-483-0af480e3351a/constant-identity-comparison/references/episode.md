# Historical episode

Authoritative SourceRecord: `PyCQA/pyflakes:483:repair:0af480e3351a`.

The [issue title](evidence/title.md) identifies Python 3.8's literal identity warning. The [report](evidence/body.md) shows `x = 5` followed by `if x is ():` and reported compiler output warning that `==` may have been intended. The reporter requested static lint coverage.

The [merged implementation](evidence/fix.md), available at revision `0af480e3351ae40b4ae7f3ce7272a46fd4265dbd`, introduces version-aware singleton classification, recursive tuple-constant classification, and a constant-but-not-singleton predicate. The comparison handler applies that predicate to either operand of each identity-comparison pair and retains chain advancement. The diagnostic text expands to constant literals including tuples.

Historical paths are `pyflakes/checker.py`, `pyflakes/messages.py`, and `pyflakes/test/test_is_literal.py`. They must not be silently reused as current bindings.

The [regression diff](evidence/regression.md) adds assertions for empty tuples, nested all-constant tuples, and variable-containing tuples. These assertions were available at the historical commit. No historical test execution is shown.

The supplied SourceRecord marks the resolution verified. A separate qualification attestation checked in 2026 reports two fail-to-pass and 28 pass-to-pass checks, limited to changed test files with an original-base control. It is preserved in provenance without backdating. Whole-project regression and cross-project transfer remain untested.

The package authors a conditional applicability probe and repair/validation operations from this evidence; it does not claim that its authored operation cards were historically executed. One repair supports this Workflow. No second independent fix supports a Pattern or local template.
