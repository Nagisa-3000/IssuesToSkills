# Historical episode

Authoritative source: `pylint-dev/pylint:3737:repair:3ed4b9c0cc18`.

## Report

The original report described Pylint 2.5.3, astroid 2.4.2, and Python 3.8.2:

```python
class Ipsum:
    def dolor(self, elit=None):
        pass


class LoremIpsum(Ipsum):
    def dolor(self, *args, **kwargs):
        super().dolor(*args, **kwargs)
```

Running `pylint lorem.py` reportedly emitted W0222, `signature-differs`, at the override. The intended correction was absence of that diagnostic, not absence of every possible lint message.

## Implementation and assertions

Revision `3ed4b9c0cc182e15cc50c1e17e37268035005757`, available `2020-12-31T08:22:37Z`, changed the branch in `pylint/checkers/classes.py` from:

```python
elif len(method1.args.defaults) < len(refmethod.args.defaults):
```

to:

```python
elif (
    len(method1.args.defaults) < len(refmethod.args.defaults)
    and not method1.args.vararg
):
```

The shown hunk retained the preceding `arguments-differ` branch. The guard checks positional variadic presence, not keyword variadic presence or the forwarding body.

The committed regression in `tests/functional/s/signature_differs.py` added `Ghij(Abcd)` with `abcd(self, *args, **kwargs)` returning `super().abcd(*args, **kwargs)` and no warning annotation. Existing `Cdef.abcd(self, aaa, bbbb=None)` retained its `[signature-differs]` annotation.

These are historical assertions. Historical CI/test execution is unknown. The authored validation operation is a requirement for current use, not a claim that its instructions were executed historically.

## Validation-only qualification audit

The supplied complete independent report pins base `b3b8ed290c6e2eee36a3aa7cc269cc97eb59150b`, issue `pylint-dev/pylint:3737`, fix `pylint-dev/pylint:pr:3988`, and the merge revision above. It records verified historical artifacts and a verified direct-closure relationship. The closure locator `pylint-dev/pylint:3737:event:MDExOkNsb3NlZEV2ZW50NDE1OTIwMzcwOA==` is a validation-only audit locator, not an additional historical evidence card.

At `2026-10-04T10:05:50.163275+00:00`, the report recorded:

| Control | Exit | Passed | Failed | Skipped | Deselected |
|---|---:|---:|---:|---:|---:|
| Original base | 0 | 29 | 0 | 5 | 381 |
| Base with regression | 1 | 28 | 1 | 5 | 381 |
| Historical fixed | 0 | 29 | 0 | 5 | 381 |

The original signature suite passed on the original base. Adding the committed regression to that base caused an unexpected `signature-differs` at line 30. The historical fixed revision passed the augmented suite. The observations record one fail-to-pass and 29 original-base-to-fixed pass-to-pass controls; the original signature suite is included in the latter count. The five skipped cases remained skipped.

All three runs used the same recorded pytest selection and runtime SHA256 `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, with no timeout and adopted workspaces. The pinned identities, observations, logs, exit codes, closure evidence, and runtime consistency support the narrow qualification. Skips and deselections are not evidence of passing coverage.

Report hash: `b34dd1cb43afc333a37465add3cb18e5bff1f5a50553cfc0872753c283b1d1e5`.

Observation hash: `5c06ac6bd4379489a0512d7bb314349f0e81497c625f1a57cfd6284c1a2928c8`.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; cross-project transfer is untested. This was not a formal SWE run and did not execute the newly authored Skill cases. The replay date is validation time, never historical availability. Contemporary runtime details and dependency warnings do not define the historical mechanism.

## Authoring boundary

The supplied four core entries support this Workflow. The source projection records retained census review and five other discussion entries; no additional evidence IDs or mechanisms are inferred from that metadata. Prior rejected authoring outputs are not independent repair sources. No authoritative upstream package, generation-context object, or enabled sealed reference was supplied.

## Evidence resources

- [Title](evidence/title.md)
- [Report](evidence/body.md)
- [Implementation](evidence/fix.md)
- [Regression assertions](evidence/regression.md)
- [Workflow](workflow.md)
- [Provenance](provenance.json)
