# Historical episode and qualification audit

Authoritative SourceRecord: `pylint-dev/pylint:5950:repair:9c90db16a860`.

## Report and repair

The [title](evidence/title.md) and [body](evidence/body.md) describe `pyreverse -ASmy -o .puml my_package/my_module.py` under Pylint 2.12.2. The reporter acknowledged the leading dot as a typo; `puml` without it worked. The diagnostic listed Graphviz formats and omitted native serializers.

The [merged implementation](evidence/fix.md) introduced `DIRECTLY_SUPPORTED_FORMATS` in `pylint/pyreverse/main.py`, containing `dot`, `vcg`, `puml`, `plantuml`, `mmd`, and `html`. Help and routing shared that inventory. Non-native requests checked Graphviz availability, announced fallback, and checked backend support before generation.

In `pylint/pyreverse/utils.py`, capability discovery used:

`subprocess.run(["dot", "-T?"], capture_output=True, check=False, encoding="utf-8")`

It parsed stderr's `Use one of:` list and compared exact whitespace-separated tokens. A known unsupported format exited 32. Unparseable stderr emitted a warning and returned, allowing generation to continue. Missing Graphviz also exited 32 with a dependency-specific message. `pylint/pyreverse/dot_printer.py` no longer repeated availability checking during conversion. ChangeLog and `doc/whatsnew/2.13.rst` recorded improved diagnostics and closure of issue 5950.

The [committed assertions](evidence/regression.md) in `tests/pyreverse/test_main.py` mocked subprocess, executable discovery, diagram construction, and writing. Supported `png` and uninterpretable capability responses each reached one writer call and exit 0; an explicitly unsupported request emitted the backend-specific message and exited 32. The unsupported test did not explicitly assert absence of writer calls. Historical CI/test execution is unknown.

## Validation-only qualification

The complete supplied qualification report was inspected as validation input, not historical mechanism evidence. It was checked at `2026-10-04T13:36:11.723471+00:00` and pins:

- Original base: `6de7100e4bed8641f898cef160e1874ec788ab96`.
- Issue: `pylint-dev/pylint:5950`.
- Fix: `pylint-dev/pylint:pr:5951`.
- Historical merged revision: `9c90db16a860d5e33b4916feb232a0a6fe9f420d`.
- Repair availability: `2022-03-22T19:00:27Z`.

The report verifies the historical artifact and direct closure relationship. Its closure reference is qualification identity data, not an additional historical evidence card.

All three controls used the same test-file argv, runtime hash, and isolation description, and none timed out. The argv was `python3 -m pytest tests/pyreverse/test_main.py -q --junitxml=/workspace/verification-results.xml`.

| Control | Observation | Exit |
|---|---|---|
| Original base | Two existing parameterized import-path cases passed | 0 |
| Base with regression assertions | Two existing cases passed; three new cases errored at fixture setup because the utility module lacked `subprocess` | 1 |
| Historical fixed revision | All five cases passed | 0 |

Thus the reported three fail-to-pass transitions include setup errors, not demonstrated behavioral assertion failures on the base. The two pass-to-pass cases check existing import-path behavior.

Runtime SHA-256: `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

Observations SHA-256: `92b2f1cc123affd3d76b5283d2d7fdfdfa7e451211ebb3fd1d658f9d4bb3a03d`.

Qualification report hash: `a56be973eeb7962e5cb9f3663a79788147dd224bd970b1808405e302254967e9`.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; this was not a formal SWE run. Later replay is not backdated historical CI, does not prove transfer, and does not execute this Skill's functional cases.
