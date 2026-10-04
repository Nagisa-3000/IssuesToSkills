#!/usr/bin/env python3
"""Add a pinned standalone interpreter's stdlib to an isolated prepared virtualenv.

The resulting runtime can be mounted at /opt/venv without depending on a host
home directory. Dependencies must already be installed; this script is offline.
"""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_runner import NamespaceTools
from arex_skill_graph.history_census import fingerprint, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("prepared-venv", "interpreter-prefix", "output-receipt"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args(argv)
    runtime, prefix = args.prepared_venv.resolve(), args.interpreter_prefix.resolve()
    if args.output_receipt.exists():
        raise ValueError("sealed runtime receipt exists; preserve it and prepare a new version")
    cfg = runtime / "pyvenv.cfg"
    original = cfg.read_text()
    if "include-system-site-packages = false" not in original:
        raise ValueError("a prepared isolated virtualenv is required")
    version = next(
        line.split("=", 1)[1].strip()
        for line in original.splitlines()
        if line.startswith("version =")
    )
    minor = ".".join(version.split(".")[:2])
    stdlib = prefix / "lib" / ("python" + minor)
    if not stdlib.is_dir():
        raise ValueError("pinned standalone interpreter stdlib is missing")
    shutil.copytree(
        stdlib,
        runtime / "lib" / stdlib.name,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("site-packages", "__pycache__"),
    )
    for path in (prefix / "lib").glob("libpython*.so*"):
        shutil.copy2(path, runtime / "lib" / path.name, follow_symlinks=True)
    cfg.write_text(
        "\n".join(
            "home = /opt/venv/bin"
            if line.startswith("home =")
            else "executable = /opt/venv/bin/python3"
            if line.startswith("executable =")
            else line
            for line in original.splitlines()
        )
        + "\n"
    )
    with __import__("tempfile").TemporaryDirectory(prefix="arex-portable-runtime-") as scratch:
        tools = NamespaceTools(
            scratch, BudgetLedger(BudgetCaps(seconds=120, tool_calls=5)), runtime
        )
        tools.preflight()
        result = tools.run(
            [
                "python3",
                "-c",
                "import sys,pytest,astroid; print(sys.version.split()[0]); print(pytest.__version__); print(astroid.__version__); assert sys.prefix == '/opt/venv'",
            ]
        )
        if result["exit_code"] or result["output"].splitlines()[0] != version:
            raise ValueError("portable interpreter and dependency preflight failed")
        files = {
            p.relative_to(runtime).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in runtime.rglob("*")
            if p.is_file()
        }
        write_json(
            args.output_receipt,
            {
                "schema": "portable-namespace-python-runtime-v1",
                "python_version": version,
                "prepared_virtualenv_config_sha256": hashlib.sha256(original.encode()).hexdigest(),
                "files": files,
                "files_sha256": fingerprint(files),
                "preflight": result,
                "runtime_sha256_before_receipt": tools.runtime_sha256,
                "historical_source_qualified": False,
            },
        )
    print(json.dumps({"prepared_python": version, "namespace_preflight": "passed"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
