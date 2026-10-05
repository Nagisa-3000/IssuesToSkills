# Historical episode

Authoritative source: `pylint-dev/pylint:5965:repair:025200c1fdb5`.

The [title](evidence/title.md) and [report](evidence/body.md) identify a Pylint 2.13.0 false positive: an enclosing function initializes `myvar`, an inner function declares `nonlocal myvar`, reads it in a `try`, and increments it in an `except IOError` handler. The report shows E0601 at the first read and expects no errors.

The [implementation](evidence/fix.md) adds an early return in historical `pylint/checkers/variables.py`. Before exception-handler assignment filtering, it checks children of `node.frame(future=True)` for a `nodes.Nonlocal` declaration containing `node.name`; if found, it returns the already-computed `found_nodes`. Earlier resolution logic remains in place.

The [regression assertions](evidence/regression.md) extend historical `tests/functional/u/used/used_before_assignment_issue4761.py` and its `.txt` expectations. The positive example declares `nonlocal count`. The negative control declares `nonlocal unrelated` but assigns to `count` in the handler; the read of `count` must still emit `used-before-assignment`. Existing expected control-flow diagnostics remain, with line numbers shifted by the inserted examples.

The ChangeLog describes a regression fix for 2.13.1; the supplied heading has release date TBA. No release-date or historical test-run success is inferred.

## Qualification boundary

The supplied validation-only report was checked at `2026-10-04T13:36:42.354301+00:00`, after the historical cutoff. It pins base `e73cfa840d47bee796795517c6d87906b81069d1`, repair `025200c1fdb579cbb8a90e1d539041f18e6eac2a`, issue 5965 and PR 5966, and attests direct closure and artifact verification.

The original-base control passed 17 selected tests. Adding the historical regression to the base yielded one failure and 16 passes, with an unexpected diagnostic at the declared-nonlocal read. The historical-fixed control passed 17 selected tests. All three runs report the same runtime hash and no timeout. These observations independently qualify the historical repair; they do not backdate execution knowledge or execute this Skill's evaluation definitions.

The scope declaration is `changed-test-files-with-original-base-control`. Broader whole-project and cross-project correctness are untested. The report's closure-event locator is validation metadata, not an additional packaged historical evidence card.
