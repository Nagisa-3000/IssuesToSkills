#!/usr/bin/env python3
"""Small deterministic validator for compiled Agent Skill packages."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_SECTIONS = ("## use this skill when", "## do not use this skill when", "## required human-readable contract", "## compilation procedure")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    root = args.skill_dir.resolve()
    errors: list[str] = []
    source = root / "SKILL.md"
    if not source.exists():
        errors.append("missing SKILL.md")
    else:
        text = source.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append("SKILL.md must start with YAML frontmatter")
        frontmatter = text.split("---", 2)[1] if text.startswith("---") and text.count("---") >= 2 else ""
        name = re.search(r"^name:\s*([^\n]+)", frontmatter, re.MULTILINE)
        description = re.search(r"^description:\s*(.+)", frontmatter, re.MULTILINE)
        if not name or not NAME_RE.fullmatch(name.group(1).strip()):
            errors.append("frontmatter name must be lowercase hyphenated")
        if not description or len(description.group(1).strip()) < 20:
            errors.append("frontmatter description is missing or too short")
        lowered = text.lower()
        for section in REQUIRED_SECTIONS:
            if section not in lowered:
                errors.append(f"missing required guidance: {section}")
        if re.search(r"TODO|FIXME|<FILL_ME>|<INSERT_HERE>", text, re.IGNORECASE):
            errors.append("unfinished placeholder detected")
    for path in root.rglob("*"):
        if path.is_file() and path.name != "SKILL.md":
            try:
                path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                pass
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {root}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
