# Merged namespace ownership repair

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6350:fix",
  "source_id": "pylint-dev/pylint:6350:repair:cb37ae4fc24a",
  "available_at": "2022-04-16T19:20:47Z",
  "kind": "historical_merged_implementation",
  "observation": "The diff in pylint/checkers/similar.py imported argparse and changed Similar initialization to assign self.namespace = self.linter.config for BaseChecker instances, otherwise argparse.Namespace(). It initialized min_similarity_lines, ignore_comments, ignore_docstrings, ignore_imports, and ignore_signatures on that namespace. LineSet construction and minimum-line checks, hashing, common-line initialization, and acceptance comparisons were migrated from copied self attributes to namespace values. SimilarChecker's constructor required a PyLinter argument, and its custom set_option synchronization override was removed. This supports the live-namespace mechanism. Contemporaneous test execution is unknown."
}
```
