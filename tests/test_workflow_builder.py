from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from arex_skill_graph.mining.local_episode import LocalMergeEpisodeExtractor
from arex_skill_graph.mining.workflow import ReviewedWorkflowBuilder
from arex_skill_graph.store import CatalogStore


class ReviewedWorkflowBuilderTests(unittest.TestCase):
    def test_builds_reviewed_workflow_steps_actions_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            repo.mkdir()
            self._git(repo, "init", "--initial-branch=master")
            self._git(repo, "config", "user.name", "Test User")
            self._git(repo, "config", "user.email", "test@example.com")
            (repo / "README.md").write_text("base\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "initial")

            self._git(repo, "checkout", "-b", "fix-compaction")
            source = repo / "src" / "compaction.py"
            source.parent.mkdir()
            source.write_text("def reserve():\n    return 1024\n", encoding="utf-8")
            test = repo / "tests" / "test_compaction.py"
            test.parent.mkdir()
            test.write_text("def test_reserve():\n    assert True\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "fix(compaction): reserve output tokens")
            self._git(repo, "checkout", "master")
            self._git(
                repo,
                "merge",
                "--no-ff",
                "fix-compaction",
                "-m",
                "Merge pull request #77 from example/fix-compaction",
                "-m",
                "Reserve output tokens during compaction",
            )

            manifest_root = root / "manifests"
            manifest_root.mkdir()
            episode = LocalMergeEpisodeExtractor(repo, "example/harness").extract(77)
            (manifest_root / "pr-77.json").write_text(
                json.dumps(episode.to_dict(), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            labels = root / "labels.json"
            labels.write_text(
                json.dumps(
                    {
                        "labels": [
                            {
                                "repository": "example/harness",
                                "number": 77,
                                "verdict": "usable",
                                "domain": "context_compaction",
                                "cross_repository_potential": "high",
                                "notes": "coherent test episode"
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            database = root / "catalog.db"
            with CatalogStore(database) as store:
                store.initialize()
                report = ReviewedWorkflowBuilder(manifest_root, labels).build_to_store(store)
                stats = store.stats()

        self.assertEqual(report.workflows_built, 1)
        self.assertEqual(report.workflow_steps_built, 1)
        self.assertEqual(report.actions_indexed, 1)
        self.assertEqual(report.commits_indexed, 1)
        self.assertEqual(report.validations_built, 1)
        self.assertEqual(stats["nodes"]["workflow"], 1)
        self.assertEqual(stats["nodes"]["workflow_step"], 1)
        self.assertEqual(stats["edges"]["has_step"], 1)
        self.assertEqual(stats["edges"]["executed_by"], 1)
        self.assertEqual(stats["edges"]["verifies"], 1)

    @staticmethod
    def _git(repo: Path, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
