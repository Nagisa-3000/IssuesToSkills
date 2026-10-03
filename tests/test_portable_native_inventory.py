import importlib.util
import json
import shutil
from pathlib import Path

import pytest
from adaptive_fixture import make_fixture

from arex_skill_graph.adaptive_cli import read_references
from arex_skill_graph.pattern_contracts import load_native_package


def test_portable_inventory_reloads_copied_authoritative_package(tmp_path):
    package, _, policy = make_fixture(tmp_path / "original")
    root = Path(package.root).parent
    source = Path(__file__).resolve().parents[1] / "experiments/export_native_inventory.py"
    spec = importlib.util.spec_from_file_location("portable_inventory", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    inventory = module.portable_inventory({"references": [package.reference]}, root)
    (root / "portable.json").write_text(json.dumps(inventory))
    destination = tmp_path / "copied"
    shutil.copytree(root, destination)
    (reference,) = read_references(destination / "portable.json")
    loaded = load_native_package(reference, policy.temporal)
    assert loaded.reference["package_sha256"] == package.reference["package_sha256"]
    assert Path(loaded.root).is_relative_to(destination)
    for escape in ("../outside", str(tmp_path / "absolute")):
        inventory["references"][0]["package_path"] = escape
        (destination / "portable.json").write_text(json.dumps(inventory))
        with pytest.raises(ValueError, match="escapes"):
            read_references(destination / "portable.json")
