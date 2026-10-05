# Historical episode

Authoritative source: `pylint-dev/pylint:4331:repair:d0591ba2a097`.

The report described a `confusing_consecutive_elif` functional fixture loading
`pylint.extensions.confusing_elif` through `[MASTER] load-plugins`. Its expected
`confusing-consecutive-elif` message at line 10, column 4, in `check_config`
was absent.

The reported initialization constructed the linter, installed its reporter,
initialized ordinary checkers, disabled suppression-related messages, read the
fixture configuration, and applied it. The proposed omission was failure to
register requested optional modules between reading and applying configuration.

The merged change in `pylint/testutils/lint_module_test.py` imported
`utils` from `pylint.utils`. Immediately after
`read_config_file(test_file.option_file)`, it checked
`cfgfile_parser.has_option("MASTER", "load-plugins")`, obtained the option with
`get`, normalized it with `utils._splitstrip`, and called
`load_plugin_modules(plugins)`. `load_config_file()` remained afterward.
The surrounding `except NoFileError: pass` remained.

The committed regression added `tests/functional/b/bad_builtins.py`, `.rc`,
and `.txt`. Its configuration loaded `pylint.extensions.bad_builtin` and set
`bad-functions=map,input,filter,print`. Four expected diagnostics exercised
activation and checker-specific configuration.

It also annotated functions in
`tests/functional/f/fixture_docparams_missing.py` and added the missing expected
output file. The report had identified this existing plugin fixture as a false
negative: plugin omission hid diagnostics, and its `.txt` file was missing.
The repair asserted those valid diagnostics instead of suppressing them.

These are historical report, implementation, and committed assertion facts.
The reporter described trying a local change that exposed the documentation
fixture. No historical successful CI or full-suite execution is supplied.

## Independent qualification: validation only

The supplied complete three-control report pins:
- original base `cd90e9ec218b4735c3406b757f48d4898a2aee5e`;
- fix `pylint-dev/pylint:pr:4332`;
- merge revision `d0591ba2a097312c41d544e4269eda5b809c47a0`;
- repair availability `2021-04-09T19:13:14Z`.

It reports verified historical artifact identity and direct issue closure.
Its closure locator is
`pylint-dev/pylint:4331:event:MDExOkNsb3NlZEV2ZW50NDU3NjAyNjUyMA==`.
This is a validation audit detail, not an added historical evidence card.

Qualification occurred at `2026-10-04T10:40:50.666371+00:00`.
All three controls used the same selected public functional tests and runtime
hash `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.
All used isolation designation
`linux-copied-user-mount-pid-net-chroot-nobody-no-capabilities-v1`;
none timed out.

| Control | Observed result |
| --- | --- |
| Original base | Exit 0; 29 passed, 1 skipped, 432 deselected. The new bad_builtins fixture was absent, and fixture_docparams_missing passed with its original insufficient expectations. |
| Base with regression artifacts | Exit 1; 2 failed, 28 passed, 1 skipped, 432 deselected. bad_builtins and fixture_docparams_missing failed because expected plugin diagnostics were absent, not because of import failure. |
| Historical fixed revision | Exit 0; 30 passed, 1 skipped, 432 deselected. Both strengthened plugin fixtures passed. |

The two fail-to-pass identities compare base-with-regression to historical
fixed. The 29 pass-to-pass identities compare original base to historical fixed;
they include fixture_docparams_missing, so these categories intentionally
overlap. `bad_reversed_sequence_py37` was skipped, not passed.

The observations digest is
`af43c4fa23953ef5a596c8290a0f4441f8a2a410ea9f88a055a8d2d378a31611`.
The authoritative report hash is copied in [provenance](provenance.json).

Scope is `changed-test-files-with-original-base-control`. Whole-project
regression was not checked, cross-project transfer is untested, and the report
was not a formal SWE run. Contemporary replay details are not historical
mechanisms or current Oracle bindings. This qualification did not execute
newly authored Skill cases and does not backdate new information.
