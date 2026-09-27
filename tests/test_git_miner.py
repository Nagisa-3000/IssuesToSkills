from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

from arex_skill_graph.mining import GitCommitMiner
from arex_skill_graph.store import CatalogStore


class GitMinerTests(unittest.TestCase):
    def test_mines_commit_and_action_with_evidence_edge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / "repo"
            repo.mkdir()
            self._git(repo, "init")
            self._git(repo, "config", "user.name", "Test User")
            self._git(repo, "config", "user.email", "test@example.com")
            source = repo / "src" / "session.py"
            source.parent.mkdir()
            source.write_text("def persist_once():\n    return True\n", encoding="utf-8")
            test = repo / "tests" / "test_session.py"
            test.parent.mkdir()
            test.write_text(
                "def test_persist_once():\n    assert True\n",
                encoding="utf-8",
            )
            self._git(repo, "add", ".")
            self._git(
                repo,
                "commit",
                "-m",
                "fix(session): prevent duplicate transcript persistence (closes #42)",
            )

            db = root / "catalog.db"
            with CatalogStore(db) as store:
                store.initialize()
                report = GitCommitMiner(repo, "example/harness").mine_to_store(
                    store, limit=10
                )
                stats = store.stats()

            self.assertEqual(report.commits_indexed, 1)
            self.assertEqual(stats["nodes"]["commit"], 1)
            self.assertEqual(stats["nodes"]["action"], 1)
            self.assertEqual(stats["edges"]["evidenced_by"], 1)

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

