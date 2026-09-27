from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from urllib.request import Request

from arex_skill_graph.mining.github import GitHubClient, HttpResponse


class FakeTransport:
    def __init__(self, responses: dict[str, object]):
        self.responses = responses
        self.calls: list[Request] = []

    def __call__(self, request: Request, _timeout: float) -> HttpResponse:
        self.calls.append(request)
        payload = self.responses[request.full_url]
        return HttpResponse(
            status=200,
            headers={
                "etag": '"test-etag"',
                "x-ratelimit-remaining": "59",
            },
            body=json.dumps(payload).encode("utf-8"),
        )


class StatusTransport(FakeTransport):
    def __init__(
        self,
        responses: dict[str, object],
        statuses: dict[str, int],
    ):
        super().__init__(responses)
        self.statuses = statuses

    def __call__(self, request: Request, _timeout: float) -> HttpResponse:
        self.calls.append(request)
        payload = self.responses[request.full_url]
        return HttpResponse(
            status=self.statuses.get(request.full_url, 200),
            headers={"x-ratelimit-remaining": "59"},
            body=json.dumps(payload).encode("utf-8"),
        )


class GitHubMinerTests(unittest.TestCase):
    def test_cache_prevents_duplicate_network_request(self) -> None:
        url = "https://api.github.test/repos/example/harness/issues/42"
        transport = FakeTransport(
            {
                url: {
                    "number": 42,
                    "title": "Fix compaction replay",
                    "state": "closed",
                }
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            client = GitHubClient(
                directory,
                base_url="https://api.github.test",
                transport=transport,
            )
            first = client.get_json("/repos/example/harness/issues/42")
            second = client.get_json("/repos/example/harness/issues/42")

        self.assertEqual(first, second)
        self.assertEqual(len(transport.calls), 1)

    def test_merged_pr_with_implementation_and_tests_is_strong(self) -> None:
        base = "https://api.github.test/repos/example/harness"
        responses = {
            f"{base}/issues/42": {
                "number": 42,
                "title": "Fix duplicate transcript persistence",
                "body": "Fixes #7",
                "state": "closed",
                "state_reason": "completed",
                "html_url": "https://github.test/example/harness/pull/42",
                "created_at": "2026-01-01T00:00:00Z",
                "updated_at": "2026-01-02T00:00:00Z",
                "closed_at": "2026-01-02T00:00:00Z",
                "author_association": "MEMBER",
                "user": {"login": "maintainer"},
                "labels": [{"name": "bug"}],
                "pull_request": {"url": f"{base}/pulls/42"},
            },
            f"{base}/pulls/42": {
                "merged": True,
                "merged_at": "2026-01-02T00:00:00Z",
                "merge_commit_sha": "merge-sha",
                "base": {"ref": "main", "sha": "base-sha"},
                "head": {"ref": "fix/session", "sha": "head-sha"},
            },
            f"{base}/pulls/42/commits?per_page=100&page=1": [
                {
                    "sha": "commit-sha",
                    "html_url": "https://github.test/commit-sha",
                    "parents": [{"sha": "parent-sha"}],
                    "commit": {
                        "message": "fix session replay",
                        "author": {"date": "2026-01-02T00:00:00Z"},
                    },
                }
            ],
            f"{base}/pulls/42/files?per_page=100&page=1": [
                {
                    "filename": "src/session/replay.ts",
                    "status": "modified",
                    "additions": 12,
                    "deletions": 3,
                    "changes": 15,
                },
                {
                    "filename": "tests/session/replay.test.ts",
                    "status": "modified",
                    "additions": 20,
                    "deletions": 1,
                    "changes": 21,
                },
            ],
        }
        transport = FakeTransport(responses)

        with tempfile.TemporaryDirectory() as directory:
            client = GitHubClient(
                directory,
                base_url="https://api.github.test",
                transport=transport,
            )
            episode = client.fetch_episode("example/harness", 42)
            manifest = (
                Path(directory) / "episodes" / "example" / "harness" / "42.json"
            )

            self.assertTrue(manifest.exists())
            self.assertEqual(episode.kind, "pull_request")
            self.assertTrue(episode.merged)
            self.assertEqual(episode.linked_issue_numbers, [7])
            self.assertEqual(episode.quality.tier, "strong")
            self.assertEqual(episode.quality.implementation_files, 1)
            self.assertEqual(episode.quality.test_files, 1)

    def test_closed_issue_without_verified_pr_is_not_strong(self) -> None:
        url = "https://api.github.test/repos/example/harness/issues/8"
        transport = FakeTransport(
            {
                url: {
                    "number": 8,
                    "title": "Session occasionally fails",
                    "body": "",
                    "state": "closed",
                    "html_url": "https://github.test/example/harness/issues/8",
                    "labels": [],
                }
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            episode = GitHubClient(
                directory,
                base_url="https://api.github.test",
                transport=transport,
            ).fetch_episode("example/harness", 8)

        self.assertEqual(episode.kind, "issue")
        self.assertEqual(episode.quality.tier, "weak")

    def test_pr_endpoint_fallback_when_repository_issues_are_disabled(self) -> None:
        base = "https://api.github.test/repos/example/harness"
        issue_url = f"{base}/issues/9"
        pull_url = f"{base}/pulls/9"
        transport = StatusTransport(
            {
                issue_url: {"message": "Not Found"},
                pull_url: {
                    "number": 9,
                    "title": "Fix session checkpoint",
                    "body": "",
                    "state": "closed",
                    "html_url": "https://github.test/example/harness/pull/9",
                    "merged": True,
                    "merged_at": "2026-01-02T00:00:00Z",
                    "labels": [],
                    "user": {"login": "maintainer"},
                    "base": {"ref": "main", "sha": "base"},
                    "head": {"ref": "fix", "sha": "head"},
                },
                f"{pull_url}/commits?per_page=100&page=1": [],
                f"{pull_url}/files?per_page=100&page=1": [],
            },
            {issue_url: 404},
        )
        with tempfile.TemporaryDirectory() as directory:
            episode = GitHubClient(
                directory,
                base_url="https://api.github.test",
                transport=transport,
            ).fetch_episode("example/harness", 9)

        self.assertEqual(episode.kind, "pull_request")
        self.assertTrue(episode.merged)


if __name__ == "__main__":
    unittest.main()
