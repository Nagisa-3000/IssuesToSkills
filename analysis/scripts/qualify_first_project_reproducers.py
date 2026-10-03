#!/usr/bin/env python3
"""Run reviewed development reproducers with isolated, pinned package versions.

This qualifies deterministic issue behavior; it does not measure Skill or Agent
effectiveness. Libraries and fixtures remain in an external temporary directory.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

VALID_PROTOCOL = """\
class A:
    def __init__(self, boo, far, *, hoo, haha):
        self._foo = boo
        self._bar = far
        self._hoo = hoo
        self._haha = haha

    def __getnewargs_ex__(self):
        args = (self._foo, self._bar)
        kwargs = {'hoo': self._hoo, 'haha': self._haha}
        return args, kwargs
"""

FORWARD_ANNOTATIONS = """\
from typing import Optional

class InnerModel1:
    model2: "Model2"
    mode2_no_err1: Optional["Model2"]
    mode2_no_err2: "Optional[Model2]"

class Model2:
    pass

def f():
    class InnerModel1:
        model2: "InnerModel2"
        mode2_err: Optional["InnerModel2"]
        mode2_no_err: "Optional[InnerModel2]"

    class InnerModel2:
        pass
"""


def run(libraries: Path, arguments: list[str]) -> tuple[subprocess.CompletedProcess, float]:
    environment = {"PATH": os.environ["PATH"], "PYTHONPATH": str(libraries),
                   "PYTHONDONTWRITEBYTECODE": "1"}
    start = time.perf_counter()
    result = subprocess.run([sys.executable, "-S", *arguments], env=environment,
                            text=True, capture_output=True, timeout=30, check=False)
    return result, round(time.perf_counter() - start, 4)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    fixtures = args.library_root / "fixtures"
    fixtures.mkdir(exist_ok=True)
    records = []
    for case, code in (
        ("valid-protocol", VALID_PROTOCOL),
        ("invalid-protocol-control", VALID_PROTOCOL.replace(
            "kwargs = {'hoo': self._hoo, 'haha': self._haha}", "kwargs = None")),
    ):
        path = fixtures / (case + ".py")
        path.write_text(code)
        for version in ("3.3.4", "3.3.5"):
            libraries = args.library_root / ("pylint-" + version)
            metadata, _ = run(libraries, ["-c", "import json,pylint,astroid; print(json.dumps({'pylint':pylint.__version__,'astroid':astroid.__version__}))"])
            if metadata.returncode:
                raise RuntimeError("Pinned Pylint library imports failed")
            result, seconds = run(libraries, ["-m", "pylint", "--disable=all",
                                             "--enable=invalid-getnewargs-ex-returned",
                                             "--reports=no", "--score=no", "--persistent=no",
                                             "--rcfile=/dev/null", "--output-format=json", str(path)])
            if result.returncode not in (0, 2):
                raise RuntimeError("Pylint case did not produce a normal diagnostic exit")
            messages = [{"symbol": item["symbol"], "line": item["line"]}
                        for item in json.loads(result.stdout)]
            records.append({"tool": "pylint", "requested_version": version,
                            "actual_versions": json.loads(metadata.stdout), "case": case,
                            "exit_code": result.returncode, "messages": messages, "elapsed_seconds": seconds})
    annotation_path = fixtures / "forward_annotations.py"
    annotation_path.write_text(FORWARD_ANNOTATIONS)
    for version in ("2.5.0", "3.1.0"):
        libraries = args.library_root / ("pyflakes-" + version)
        result, seconds = run(libraries, ["-m", "pyflakes", str(annotation_path)])
        if result.returncode not in (0, 1):
            raise RuntimeError("Pyflakes case did not produce a normal diagnostic exit")
        # Only this fixed fixture's named diagnostic is recorded, not raw output.
        records.append({"tool": "pyflakes", "requested_version": version, "case": "forward-annotations",
                        "exit_code": result.returncode,
                        "undefined_inner_model": "undefined name 'InnerModel2'" in result.stdout,
                        "elapsed_seconds": seconds})
    valid = [row for row in records if row["case"] == "valid-protocol"]
    controls = [row for row in records if row["case"] == "invalid-protocol-control"]
    if not (valid[0]["messages"] and not valid[1]["messages"] and all(row["messages"] for row in controls)):
        raise RuntimeError("Pylint false-positive repair or negative control did not reproduce")
    annotations = [row for row in records if row["case"] == "forward-annotations"]
    if not (annotations[0]["undefined_inner_model"] and not annotations[1]["undefined_inner_model"]):
        raise RuntimeError("Pyflakes forward-annotation version contrast did not reproduce")
    result = {"schema": "first-project-reproducer-qualification-v1",
              "python": sys.version.split()[0], "records": records,
              "Pylint_issue": "https://github.com/pylint-dev/pylint/issues/10208",
              "Pyflakes_issue": "https://github.com/PyCQA/pyflakes/issues/749",
              "shared_pylint_dependencies": ["astroid==3.3.8", "isort==5.13.2", "dill==0.3.9",
                                           "mccabe==0.7.0", "platformdirs==4.3.6", "tomlkit==0.13.2"],
              "interpretation": "Version contrast and a retained true-positive control qualify an inexpensive deterministic harness. They do not establish a causal effect from Skill packages.",
              "reviewed_examples_are_development_only": True}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"python": result["python"], "records": records}, ensure_ascii=False))


if __name__ == "__main__":
    main()
