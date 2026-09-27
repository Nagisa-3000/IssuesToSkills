from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

from arex_skill_graph.mining.profile import RepositoryProfiler


class RepositoryProfilerTests(unittest.TestCase):
    def test_profiles_strong_issue_anchored_change(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            self._git(repo, "init")
            self._git(repo, "config", "user.name", "Test User")
            self._git(repo, "config", "user.email", "test@example.com")
            source = repo / "agent" / "session.py"
            source.parent.mkdir()
            source.write_text("def compact():\n    return []\n", encoding="utf-8")
            test = repo / "tests" / "test_session.py"
            test.parent.mkdir()
            test.write_text("def test_compact():\n    assert True\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(
                repo,
                "commit",
                "-m",
                "fix(session): preserve persisted markers after compaction (#42)",
            )

            profile = RepositoryProfiler(repo, "example/harness").profile()
            self.assertEqual(profile.total_commits, 1)
            self.assertEqual(profile.strong_candidates, 1)
            self.assertEqual(profile.strong_episode_candidates, 1)
            self.assertEqual(profile.unique_issue_references, 1)
            self.assertEqual(profile.commits_with_test_evidence, 1)

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
