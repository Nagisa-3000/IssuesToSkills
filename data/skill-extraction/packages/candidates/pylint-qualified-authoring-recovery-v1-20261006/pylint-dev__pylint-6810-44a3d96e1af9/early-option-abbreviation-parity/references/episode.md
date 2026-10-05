# Historical episode

SourceRecord: `pylint-dev/pylint:6810:repair:44a3d96e1af9`.

The issue title and body report that Pylint 2.14.0 produced W2901 with `--load-plugins=pylint.extensions.redefined_loop_name`, but no corresponding warning with `--load-plugin=...`. The reporter expected an invalid-argument warning. The repair instead made special early options support abbreviations consistently with the downstream argparse policy.

## Historical implementation owners

These paths identify historical artifacts, not bindings for a current checkout:

- `pylint/config/utils.py`: `PREPROCESSABLE_OPTIONS` and `_preprocess_options`.
- `tests/config/test_find_default_config_files.py`: `test_verbose_abbreviation`.
- `doc/whatsnew/2/2.14/full.rst`: abbreviation fix release note and issue closure.

Registry values changed from pairs to triples: argument-taking flag, callback, and matching length. Lengths include hyphens.

| Option | Length | Recorded competitor |
|---|---:|---|
| `--init-hook` | 8 | `--init-import` |
| `--rcfile` | 4 | `--recursive` |
| `--output` | 0 | `--output-format` |
| `--load-plugins` | 5 | `--long-help` |
| `--verbose` | 4 | `--variable-rgx` |
| `-v` | 2 | short spelling |
| `--enable-all-extensions` | 9 | `--enable` |

After option/value splitting, the matcher scans the registry. Zero uses exact equality; nonzero uses `option.startswith(option_name[:to_match])`. The selected canonical key supplies callback and argument-taking metadata. Unmatched original arguments remain forwarded.

This threshold rule can match strings sharing the configured prefix. It is not a proof of complete argparse equivalence or a guarantee that all misspellings are rejected. Current thresholds require current namespace evidence.

## Committed assertion

The regression uses `pop_pylintrc`, a temporary directory, a fake home, and a nested package fixture. It changes directory to `a/b/c`, expects `SystemExit` from `Run(["--ve"])`, then asserts stderr contains `No config file found, using default configuration`. The comment identifies this as verbose-only output.

This assertion was available at the historical commit. Historical CI/test execution is unknown.

## Later source qualification

The supplied validation-only controls were checked at `2026-10-04T14:49:56.961973+00:00`. They pin original base `76dcd07dcce5e3c13e2299a4c459d36fc90adcbf`, fixed revision `44a3d96e1af985c6ad290a51555b9c7ced0a7079`, issue 6810, and PR 6820, with verified direct closure and historical artifact identity.

The original base passed 13 tests. The base with the historical regression failed `test_verbose_abbreviation` and passed the same 13 adjacent tests. Its captured output showed an argument error rather than the required verbose message. The historical-fixed run passed all 14. All three runs used the same runtime digest, adopted the workspaces, and did not time out; exit codes were respectively 0, 1, and 0.

Exact scope: `changed-test-files-with-original-base-control`.

Exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

These complete controls support bounded causal source qualification. They do not backdate runtime observations, establish historical CI execution, or execute the newly authored Skill evaluation definitions.
