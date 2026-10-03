# Historical episode

Authoritative source: `PyCQA/pyflakes:434:repair:232cb1d27ee1`.

The report described false F811 diagnostics for repeated overload declarations inside a class and for module-level declarations with an additional decorator. It stated that the simpler function case had previously been fixed in #320.

At revision `232cb1d27ee134bf96adc8f37e53589dc259b159`, the historical implementation in `pyflakes/checker.py` changed `is_typing_overload(value, scope)` to accept `scope_stack`.

The new name helper iterated `reversed(scope_stack)`. At the first scope containing the name, it returned whether the binding was an `ImportationFrom` whose `fullName` equaled `typing.overload`. An absent name returned `False`. A nearer non-typing binding was not bypassed to find an outer typing import.

The `isinstance(value.source, ast.FunctionDef)` guard remained. The exactly-one-decorator condition became `any(is_typing_overload_decorator(dec) for dec in value.source.decorator_list)`. The unused-redefinition branch continued testing `existing`, passing `self.scopeStack` instead of `self.scope`.

The attribute-recognition branch was unchanged and is only partially visible in the supplied diff. Its complete semantics must not be invented from that excerpt.

In `pyflakes/test/test_type_annotations.py`, the repair added:

- `test_overload_with_multiple_decorators`: two declarations with `@dec` above `@overload`, followed by an implementation with `@dec`.
- `test_overload_in_class`: two class-local overload declarations using an enclosing typing import, followed by an implementation.

Both called `self.flakes(...)` without expected diagnostics. These are historical assertions, not historical execution logs. The original report also showed `@overload` above another decorator.

## Evidence

- [Issue title](evidence/title.md)
- [Original report](evidence/report.md)
- [Merged implementation](evidence/implementation.md)
- [Regression assertions](evidence/regression.md)

The supplied qualification attestation is recorded separately in [provenance](provenance.json). It covers changed test files only, not whole-project regression or cross-project transfer.
