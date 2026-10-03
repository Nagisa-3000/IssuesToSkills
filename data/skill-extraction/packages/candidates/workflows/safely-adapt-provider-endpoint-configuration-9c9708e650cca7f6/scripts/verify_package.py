#!/usr/bin/env python3
"""Verify this copied package without importing AREX or contacting a service."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    hashes = manifest["files"]
    inventory = {str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()}
    if inventory != set(hashes) | {"manifest.json"}:
        raise SystemExit("FAIL: package inventory changed")
    for relative, expected in hashes.items():
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise SystemExit("FAIL: unsafe package reference")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit("FAIL: package content changed")
    encoded = json.dumps(hashes, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if hashlib.sha256(encoded.encode()).hexdigest() != manifest["package_sha256"]:
        raise SystemExit("FAIL: package hash changed")
    print("PASS: package content is intact; functional and holdout evals are separate")


if __name__ == "__main__":
    main()
