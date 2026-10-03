# Historical episode

The authoritative repair source is `PyCQA/pyflakes:422:repair:2c29431eaeb9`, associated with issue cluster `PyCQA/pyflakes:422` and fix `PyCQA/pyflakes:pr:423`.

The original [title](evidence/title.md) reported “2.1.0 is broken.” The [body](evidence/body.md) supplied only an external CI job URL. Those entries do not independently identify a traceback, root cause, or test command.

## Implementation observation

The [merged implementation](evidence/fix.md) changed `is_typing_overload` in historical `pyflakes/checker.py`. In the bare-name branch, the existing checks were:

- `isinstance(node, ast.Name)`
- `node.id in scope`
- `scope[node.id].fullName == 'typing.overload'`

The repair inserted `isinstance(scope[node.id], ImportationFrom)` after scope membership and before the `.fullName` comparison. The diff then continued into the existing `ast.Attribute` alternative without showing a change to it.

This establishes a narrowly scoped mechanism: short-circuit on the binding class before reading metadata belonging to the from-import binding.

## Regression observation

The [test diff](evidence/regression.md) added `test_not_a_typing_overload` to historical `pyflakes/test/test_type_annotations.py`. It assigned `x = lambda f: f`, defined `t` with `@x`, assigned `y = lambda f: f`, and then defined `t` twice more with stacked `@x` and `@y`.

The assertion passed exactly two `m.RedefinedWhileUnused` expectations to `self.flakes`. The test's docstring identified an overload-detection regression in version 2.1.0.

These are assertions available at the historical commit. The supplied historical evidence does not contain a historical test execution transcript.

## Later qualification, not backdated evidence

The supplied qualification attestation was checked at `2026-10-03T19:13:13.277008+00:00`, after the authoritative cutoff. Its scope was `changed-test-files-with-original-base-control`; it reported verified resolution, one fail-to-pass case, and thirteen pass-to-pass cases.

Its runtime SHA-256 was `e2638f0f36eaf8f7d2aeea4607c51f66d424587388e1d5a5e529fe22d5800c27`.

This is a provenance attestation, not pre-cutoff learned content or an additional historical evidence card. It does not establish whole-project regression safety or cross-project transfer. The package's functional eval definitions have not been executed.
