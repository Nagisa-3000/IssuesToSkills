#!/usr/bin/env python3
"""Export portable reference paths without changing authored package files or hashes."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import digest
from arex_skill_graph.adaptive_cli import read_json, write_json


def portable_inventory(value, root):
    root = Path(root).resolve()

    def convert(item):
        if isinstance(item, list):
            return [convert(row) for row in item]
        if isinstance(item, dict):
            result = {k: convert(v) for k, v in item.items()}
            if "package_path" in result:
                result["package_path"] = (
                    Path(result["package_path"]).resolve().relative_to(root).as_posix()
                )
            return result
        return item

    result = convert(value)
    result["reference_path_base"] = "inventory-directory"
    result["source_inventory_sha256"] = digest(value)
    result["authored_package_files_modified"] = False
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.input.resolve().parent != args.output.resolve().parent:
        raise ValueError("portable inventory must remain next to the source package directories")
    write_json(args.output, portable_inventory(read_json(args.input), args.input.parent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
