# Historical episode and learning boundary

Authoritative source: `pylint-dev/pylint:4555:repair:cbd3cc07515e`.

The original report described using pylint 2.7.2 with a 2.8.3 configuration containing `pylint.extensions.confusing_elif`. Plugin loading raised `ModuleNotFoundError`, aborting startup. The requested behavior was graceful failure with other checks continuing.

The merged repair at `cbd3cc07515e21ed08000941dc4883c86e84e208`, available at `2021-06-17T11:45:43Z`, added `E0013` / `bad-plugin-value`. In historical `pylint/lint/pylinter.py`, configured names remained in `_dynamic_plugins` before loading. Registration caught `ModuleNotFoundError` without reporting immediately. The configuration phase caught the same exception and emitted the dedicated diagnostic with plugin name and exception at line zero.

The guarded blocks enclosed registration and configuration-hook calls as well as imports. A `ModuleNotFoundError` from inside these calls was therefore also caught. The evidence does not establish precise discrimination between an absent plugin and every missing internal dependency.

Companion early-reporting changes were necessary:

- Historical `pylint/message/message_handler_mix_in.py` created a minimal statistics structure when `stats` was `None`.
- A missing absolute file path became the display path `configuration`.
- Historical `pylint/reporters/text.py` initialized `_template` to `line_format` and used the existing template as the fallback when setting the current module.

The new historical `tests/functional/p/plugin_does_not_exists.rc` configured `pylint.extensions.check_does_not_exists_in_venv`. Its Python fixture imported `ShadokInteger` from `shadok` on line 3. Expected output asserted the ordinary `import-error` there. This directly asserts continuation despite the missing configured plugin; it does not directly assert `bad-plugin-value`. The regression diff also deleted an empty `decorator_unused.txt`; no causal mechanism is inferred from that deletion.

These Actions and the Workflow are newly authored contracts grounded in the repair, not claims that these contracts or a current plan existed or executed historically.

## Validation-only qualification audit

The supplied complete controls were inspected, including original-base, base-with-regression, and historical-fixed observations, pinned identity, closure relationship, and runtime consistency.

Identity pins base `4dfaddf58129f1718340bf3b513a0270fe749354`, issue 4555, pull request 4583, and repair revision `cbd3cc07515e21ed08000941dc4883c86e84e208`. The report verifies the historical artifact and a direct-closure resolution relationship.

The selected functional-test runs showed:

- Original base: exit 0, 31 passed, two skipped; the new fixture was absent.
- Base with committed regression: exit 1, one failed, 31 passed, two skipped. The new fixture failed during configured plugin loading with `ModuleNotFoundError`.
- Historical fixed revision: exit 0, 32 passed, two skipped.

The report identifies one fail-to-pass and 31 pass-to-pass cases. The two skipped postponed-evaluation cases are not passes. All three runs used runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`; none timed out. Their observations digest is `cb3bae6dc5efe4d155f897e3248aa84a6265f4d056b82674be2626790730318a`.

Scope is `changed-test-files-with-original-base-control`, not whole-project regression or cross-project transfer. This was not a formal SWE run. The qualification checked at `2026-10-04T10:52:31.559637+00:00` is validation-only; it does not backdate new information or supply historical mechanism details. Contemporary dependencies and logs are not guidance. It does not execute the authored Skill cases.

Historical CI/test execution remains unknown. Only committed assertions and implementation were supplied as historical artifacts.

## Packaged evidence

- [Title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertions](evidence/regression.md)
