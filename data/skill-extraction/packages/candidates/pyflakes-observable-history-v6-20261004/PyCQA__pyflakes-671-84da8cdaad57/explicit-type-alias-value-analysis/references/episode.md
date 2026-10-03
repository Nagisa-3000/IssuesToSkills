# Historical episode: explicit alias strings were not analyzed as types

SourceRecord: `PyCQA/pyflakes:671:repair:84da8cdaad57`.

The [title](evidence/title.md) and [report](evidence/body.md) describe an unused-import false positive for an explicit `TypeAlias` whose value is `"PathLike[str]"`. The reporter used Pyflakes 2.4.0 on Python 3.8.6. An ordinary function annotation containing the same string did not produce the reported unused-import diagnostic.

The [merged implementation](evidence/fix.md), at revision `84da8cdaad574df7e692dff06ab561acc63d521c`, changed the annotated-assignment visitor in historical `pyflakes/checker.py`. The visitor continued handling the target and declared annotation. For assignments with a value, it selected `handleAnnotation(node.value, node)` when `_is_typing(node.annotation, 'TypeAlias', self.scopeStack)` succeeded; otherwise it retained `handleNode(node.value, node)`.

The implementation also corrected the helper type comment from `ast.Ast` to `ast.AST`. That incidental correction is not the causal mechanism of this Skill.

The [regression assertions](evidence/regression.md) were added to historical `pyflakes/test/test_type_annotations.py`. They cover direct and string values in module and class scopes, a valueless alias declaration, and a valueless declaration with an actually unused import. They are guarded for Python versions supporting annotated assignments.

The historical evidence supplies implementation and test assertions, not a historical command log or recorded historical test run. The later qualification attestation is retained separately in provenance and is explicitly limited to changed test files.
