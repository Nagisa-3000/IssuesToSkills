# Historical episode

Authoritative source: `pylint-dev/pylint:6350:repair:cb37ae4fc24a`.

The [title](evidence/title.md) and [report](evidence/body.md) describe `ignore-imports` being ignored. Two files containing five identical imports produced duplicate-code output despite `--ignore-imports=y`. The report contrasted the reported 2.14 behavior with expected 2.12 behavior, in which unused-import diagnostics remained but duplicate-code did not.

The [merged implementation](evidence/fix.md) replaced option attributes on `Similar` with namespace-based storage. Integrated checker instances used the exact host configuration object; standalone instances created an `argparse.Namespace`. Runtime filtering and minimum-line consumers were migrated, and the custom synchronization override was removed.

Historical implementation owner: `pylint/checkers/similar.py`. Historical regression owner: `tests/test_similar.py`; fixtures were under `tests/regrtest_data/duplicate_code/ignore_imports/`. These paths are historical references only.

The [committed regression](evidence/regression.md) added an empty package initializer and two identical files importing argparse, math, os, random, and sys. The test enabled duplicate-code, disabled unused-import, enabled ignore-imports, and asserted exit status zero.

The [Workflow](workflow.md) reconstructs the mechanism from supplied report, implementation, and assertions. It does not claim that the diagnostic operations were separately logged historically. Preservation checks beyond the committed test are prospective current assurances, not additional historical test claims.

## Validation-only qualification

The supplied complete qualification report pins original base `86ed7fa47b501bfbab46a3fe84e02aea5a51376d`, merged repair `cb37ae4fc24a8756a5f965cdc6ab9c472f909ab0`, issue 6350, and PR 6358. It verifies the historical artifact and direct closure relationship.

The original base passed ten existing tests. The base with the committed regression passed those ten and failed the new ignore-imports test: duplicate-code appeared and status was 8 rather than 0. The historical fixed revision passed all eleven. All three runs used the same runtime hash, adopted their workspaces, and did not time out. These complete controls support the changed-test-file causal qualification, not whole-project correctness.

Qualification was checked on 2026-10-04. Its runtime and logs are validation-only input, not pre-cutoff historical mechanisms or newly executed Skill functional cases. Historical CI/test execution remains unknown. Qualification hashes and audit boundaries are preserved in [provenance](provenance.json).
