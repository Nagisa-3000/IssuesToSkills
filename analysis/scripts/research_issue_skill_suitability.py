#!/usr/bin/env python3
"""Collect public issue/repair evidence for an exploratory first-project choice.

Existing GitHub CLI handles authentication. Raw responses are kept in memory;
credential-like literals are redacted before any output or persistence.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

SEARCHES = [
    ("pylint-historical", 'repo:pylint-dev/pylint is:issue is:closed closed:<2025-01-01 "false positive" sort:comments-desc'),
    ("ruff-historical", 'repo:astral-sh/ruff is:issue is:closed closed:<2025-01-01 "false positive" sort:comments-desc'),
    ("pyflakes-historical", 'repo:PyCQA/pyflakes is:issue is:closed closed:<2025-01-01 sort:comments-desc'),
    ("pylint-new", 'repo:pylint-dev/pylint is:issue is:closed created:2025-01-01..2026-10-03 "false positive" sort:created-asc'),
    ("gson-historical", 'repo:google/gson is:issue is:closed closed:<2025-01-01 sort:comments-desc'),
    ("jackson-historical", 'repo:FasterXML/jackson-databind is:issue is:closed closed:<2025-01-01 generics sort:comments-desc'),
    ("fastjson-historical", 'repo:alibaba/fastjson2 is:issue is:closed closed:<2025-01-01 generics sort:comments-desc'),
    ("gson-new", 'repo:google/gson is:issue is:closed created:2025-01-01..2026-10-03 sort:created-asc'),
    ("xarray-historical", 'repo:pydata/xarray is:issue is:closed closed:<2025-01-01 alignment sort:comments-desc'),
    ("pandas-historical", 'repo:pandas-dev/pandas is:issue is:closed closed:<2025-01-01 reindex sort:comments-desc'),
    ("polars-historical", 'repo:pola-rs/polars is:issue is:closed closed:<2025-01-01 null sort:comments-desc'),
    ("xarray-new", 'repo:pydata/xarray is:issue is:closed created:2025-01-01..2026-10-03 indexing sort:created-asc'),
    ("fastify-historical", 'repo:fastify/fastify is:issue is:closed closed:<2025-01-01 error sort:comments-desc'),
    ("express-historical", 'repo:expressjs/express is:issue is:closed closed:<2025-01-01 error sort:comments-desc'),
    ("hono-historical", 'repo:honojs/hono is:issue is:closed closed:<2025-01-01 error sort:comments-desc'),
    ("fastify-new", 'repo:fastify/fastify is:issue is:closed created:2025-01-01..2026-10-03 error sort:created-asc'),
]

ISSUE_FIELDS = """
  number title url body createdAt closedAt state stateReason
  repository { nameWithOwner }
  labels(first:15) { nodes { name } }
  timelineItems(last:20,itemTypes:[CLOSED_EVENT,CONNECTED_EVENT,CROSS_REFERENCED_EVENT]) {
    nodes {
      __typename
      ... on ClosedEvent {
        createdAt closer {
          __typename
          ... on PullRequest { number url title merged mergedAt repository { nameWithOwner } }
          ... on Commit { oid url messageHeadline committedDate }
        }
      }
      ... on CrossReferencedEvent {
        isCrossRepository referencedAt
        source {
          __typename
          ... on PullRequest { number url title merged mergedAt repository { nameWithOwner } }
        }
      }
    }
  }
"""


def sanitizer() -> list[re.Pattern]:
    tree = ast.parse(Path("src/arex_skill_graph/direct_skill_extraction.py").read_text())
    pattern = next(ast.literal_eval(node.value.args[0]) for node in ast.walk(tree)
                   if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name)
                   and target.id == "SECRET_PATTERN" for target in node.targets))
    return [
        re.compile(pattern),
        re.compile(r"(?i)(?:api[_-]?key|password|access[_-]?token|client[_-]?secret)"
                   r"\s*[\"']?\s*[:=]\s*[\"'][^\"'\r\n]+[\"']"),
        re.compile(r"(?i)authorization\s*[:=]\s*[\"']?(?:bearer|basic)\s+[^\s\"']+"),
        re.compile(r"(?i)[?&](?:token|api_key|access_token|password|signature|key)=[^&\s\"']+"),
    ]


def scrub(value: object, patterns: list[re.Pattern]) -> object:
    if isinstance(value, dict):
        return {key: scrub(item, patterns) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub(item, patterns) for item in value]
    if isinstance(value, str):
        for pattern in patterns:
            value = pattern.sub("[REDACTED]", value)
    return value


def graphql(gh: str, query: str, patterns: list[re.Pattern]) -> dict:
    response = subprocess.run([gh, "api", "graphql", "--input", "-"],
                              input=json.dumps({"query": query}), text=True,
                              capture_output=True, timeout=50, check=False)
    try:
        value = json.loads(response.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"GitHub read request failed (exit {response.returncode})") from None
    if value.get("errors"):
        messages = scrub([item.get("message", "GraphQL error") for item in value["errors"]], patterns)
        raise RuntimeError(f"GitHub GraphQL query errors: {messages}")
    if response.returncode:
        raise RuntimeError(f"GitHub read request failed (exit {response.returncode})")
    return scrub(value["data"], patterns)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gh", default="/mnt/c/Users/W/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe")
    parser.add_argument("--sample-size", type=int, default=6)
    parser.add_argument("--search-file", type=Path, help="Additional fixed purposive search queries")
    args = parser.parse_args()
    patterns = sanitizer()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    searches_input = json.loads(args.search_file.read_text()) if args.search_file else SEARCHES
    fields = [f"q{i}: search(query:{json.dumps(query)},type:ISSUE,first:{args.sample_size})"
              f" {{ issueCount nodes {{ ... on Issue {{ {ISSUE_FIELDS} }} }} }}"
              for i, (_, query) in enumerate(searches_input)]
    result = {}
    for offset in range(0, len(fields), 4):
        result.update(graphql(args.gh, "query { " + "\n".join(fields[offset:offset + 4]) + " }", patterns))
    searches = {}
    for index, (label, query) in enumerate(searches_input):
        value = result[f"q{index}"]
        searches[label] = {"query": query, "total_matches": value["issueCount"],
                           "sample_size": len(value["nodes"]), "issues": value["nodes"]}
        print(json.dumps({"search": label, "total_matches": value["issueCount"],
                          "sampled_issue_numbers": [issue["number"] for issue in value["nodes"]]}, ensure_ascii=False), flush=True)
    document = {"schema": "issue-skill-first-project-exploratory-v1",
                "observed_at": datetime.now(UTC).isoformat(),
                "historical_cutoff_exclusive": None if args.search_file else "2025-01-01",
                "temporal_contract": "Each stored query is authoritative; additional batches may mix exploratory cutoff dates.",
                "sampling_limit": "Purposive keyword samples, not random prevalence estimates or blind holdouts.",
                "searches": searches}
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
