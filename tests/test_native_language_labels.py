from dataclasses import replace

import pytest
from adaptive_fixture import make_fixture


def test_native_port_language_casing_does_not_change_connection_type(tmp_path):
    package, _task, _policy = make_fixture(tmp_path)
    port = package.actions[0].outputs[0]
    assert replace(port, language="python").compatible(replace(port, language="Python"))
    assert not replace(port, language="python").compatible(replace(port, language="Rust"))
    assert not replace(port, state="unvalidated").compatible(replace(port, state="confirmed"))


def test_lowercase_python_binding_still_checks_ast_symbol_existence(tmp_path):
    _package, task, _policy = make_fixture(tmp_path)
    lower = replace(task, bindings=tuple(replace(b, language="python") for b in task.bindings))
    lower.verify()
    missing = replace(
        lower, bindings=tuple(replace(b, symbol="missing_python_symbol") for b in lower.bindings)
    )
    with pytest.raises(ValueError, match="Python symbol does not exist"):
        missing.verify()
    wrong_language = replace(
        lower, bindings=tuple(replace(b, language="rust") for b in lower.bindings)
    )
    with pytest.raises(ValueError, match="language disagrees"):
        wrong_language.verify()
