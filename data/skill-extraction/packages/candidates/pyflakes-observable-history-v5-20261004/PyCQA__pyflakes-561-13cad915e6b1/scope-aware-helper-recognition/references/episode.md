# Historical episode

Source: `PyCQA/pyflakes:561:repair:13cad915e6b1`.
Issue cluster: `PyCQA/pyflakes:561`.
Fix: `PyCQA/pyflakes:pr:632`.
Revision: `13cad915e6b181b2f6a85efc2ead4856b23bccc0`.

The reporter describes a PyFlakes 2.2.0 false positive absent in 2.1.1: renamed `Literal` imports cause string values to be analyzed as unresolved forward references, producing F821 undefined name `none`. The supplied reproduction combines `import typing as ty`, `from typing_extensions import Literal as ty_Literal`, `@ty.overload`, and `ty_Literal["none"]`.

The merged implementation in historical `pyflakes/checker.py` adds `_module_scope_is_typing(name)` inside `_is_typing_helper`. It traverses `reversed(scope_stack)`. At the first scope containing the name, it returns whether the binding is an `Importation` whose `fullName` is in `TYPING_MODULES`; absent bindings return false. Thus a shadowing binding terminates lookup even if it is not a supported import.

For an `ast.Attribute` with an `ast.Name` receiver, `_module_scope_is_typing(node.value.id)` replaces `node.value.id in TYPING_MODULES`. The helper-name predicate remains. The shown direct `ast.Name` branch is unchanged.

Historical `pyflakes/test/test_type_annotations.py` gains `test_aliased_import`. It imports `typing as t`, uses two `@t.overload` declarations with `(None) -> None` and `(int) -> int` type comments, and follows them with a concrete implementation. It calls `self.flakes` without expected diagnostics. The neighboring `test_not_a_typing_overload` is visible only as context.

## Boundaries

The supplied artifacts establish a merged mechanism and regression assertions available on 2021-10-05. No original execution log or test command is supplied. The regression does not itself assert the original Literal reproduction.

The Action decomposition and semantic dependency model are authored reconstructions, not additional historical events or a claim about the original author's operation order.

## Later qualification

The supplied attestation was checked at `2026-10-03T19:13:27.933710+00:00`. It reports verified resolution with one fail-to-pass and 50 pass-to-pass outcomes under `changed-test-files-with-original-base-control`.

This post-cutoff attestation is provenance only. Qualification covers changed test files; whole-project regression and cross-project transfer are untested. This package's functional eval definitions have not been executed.
