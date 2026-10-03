#!/usr/bin/env python3
"""Launch a repository experiment with a pipe-only, process-scoped credential.

The first stdin line is a JSON object containing api_key. This wrapper never
echoes it or writes environment/configuration files. Remaining argv specifies
a repository experiment script. Do not pass the credential on the command line.
"""

import json
import os
import runpy
import sys
from pathlib import Path


def main():
    try:
        line = sys.stdin.buffer.readline(4097)
        if len(line) > 4096 or not line.endswith(b"\n"):
            raise ValueError
        credential = json.loads(line)["api_key"]
        if not isinstance(credential, str) or not credential.strip():
            raise ValueError
        script = Path(sys.argv[1]).resolve()
        root = Path(__file__).resolve().parents[1]
        if not script.is_relative_to(root / "experiments") or script.suffix != ".py":
            raise ValueError
    except (ValueError, KeyError, IndexError, TypeError):
        print(
            "Invalid runtime credential pipe or experiment path; values suppressed.",
            file=sys.stderr,
        )
        return 2
    os.environ["AREX_LLM_API_KEY"] = credential
    line, credential = None, None
    sys.argv = [str(script), *sys.argv[2:]]
    try:
        runpy.run_path(str(script), run_name="__main__")
    finally:
        os.environ.pop("AREX_LLM_API_KEY", None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
