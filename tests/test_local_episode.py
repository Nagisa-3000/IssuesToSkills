from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from arex_skill_graph.mining.local_episode import LocalMergeEpisodeExtractor


class LocalMergeEpisodeTests(unittest.TestCase):
    def test_recovers_commits_files_and_quality_from_merge(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            self._git(repo, "init", "--initial-branch=master")
            self._git(repo, "config", "user.name", "Test User")
            self._git(repo, "config", "user.email", "test@example.com")
            readme = repo / "README.md"
            readme.write_text("base\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "initial")

            self._git(repo, "checkout", "-b", "fix-session")
            source = repo / "src" / "session.py"
            source.parent.mkdir()
            source.write_text("def checkpoint():\n    return True\n", encoding="utf-8")
            test = repo / "tests" / "test_session.py"
            test.parent.mkdir()
            test.write_text("def test_checkpoint():\n    assert True\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(
                repo,
                "commit",
                "-m",
                "fix(session): persist checkpoint before resume closes #7",
            )

            self._git(repo, "checkout", "master")
            self._git(
                repo,
                "merge",
                "--no-ff",
                "fix-session",
                "-m",
                "Merge pull request #42 from example/fix-session",
                "-m",
                "Persist session checkpoints before resume",
            )

            episode = LocalMergeEpisodeExtractor(
                repo,
                "example/harness",
            ).extract(42)

        self.assertEqual(episode.number, 42)
        self.assertEqual(episode.title, "Persist session checkpoints before resume")
        self.assertEqual(episode.linked_issue_numbers, [7])
        self.assertEqual(len(episode.commits), 1)
        self.assertEqual(
            {item["filename"] for item in episode.files},
            {"src/session.py", "tests/test_session.py"},
        )
        self.assertEqual(episode.quality.tier, "strong")

    def test_profiles_merge_episodes_and_writes_manifests(self) -> None:
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

            self._git(repo, "checkout", "-b", "session-cache")
            source = repo / "src" / "session_cache.py"
            source.parent.mkdir()
            source.write_text("def restore():\n    return True\n", encoding="utf-8")
            test = repo / "tests" / "test_session_cache.py"
            test.parent.mkdir()
            test.write_text("def test_restore():\n    assert True\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "feat(session): restore persisted cache")
            self._git(repo, "checkout", "master")
            self._git(
                repo,
                "merge",
                "--no-ff",
                "session-cache",
                "-m",
                "Merge pull request #51 from example/session-cache",
                "-m",
                "Restore persisted session cache",
            )

            manifests = root / "manifests"
            profile = LocalMergeEpisodeExtractor(repo, "example/harness").profile(
                candidate_limit=10,
                manifest_dir=manifests,
            )

            self.assertEqual(profile.matched_pr_merges, 1)
            self.assertEqual(profile.extracted_episodes, 1)
            self.assertEqual(profile.tier_counts, {"strong": 1})
            self.assertEqual(profile.selection_tier_counts, {"preferred": 1})
            self.assertIn("session_persistence", profile.module_family_counts)
            self.assertEqual(profile.candidates[0].number, 51)
            self.assertEqual(profile.candidates[0].selection_tier, "preferred")
            self.assertEqual(profile.family_candidates["session_persistence"][0].number, 51)
            self.assertEqual(len(list(manifests.rglob("*.json"))), 1)

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
