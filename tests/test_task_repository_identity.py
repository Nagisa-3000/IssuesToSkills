from dataclasses import replace
import subprocess

import pytest

from arex_skill_graph.task_context import EvidenceAnchor, TaskContext


def repository(path):
    path.mkdir()
    (path / 'public.txt').write_text('Public fixture content')
    git = ['git', '-C', str(path)]
    subprocess.run([*git, 'init', '-q'], check=True)
    subprocess.run([*git, 'add', '--all'], check=True)
    subprocess.run([*git, '-c', 'user.name=Fixture', '-c',
                    'user.email=fixture@example.invalid', 'commit', '-qm', 'Fixture'], check=True)
    return subprocess.check_output([*git, 'rev-parse', 'HEAD'], text=True).strip()


def task(root, head):
    return TaskContext('fixture:identity', 'synthetic/identity', head, str(root),
                       'Check fixture repository identity', '2026-10-05T00:00:00Z',
                       (EvidenceAnchor('current:issue', 'public_issue', 'Public repro', head),))


def test_current_checkout_cannot_inherit_an_ancestor_repository(tmp_path):
    parent = tmp_path / 'parent'
    head = repository(parent)
    nested = parent / 'unversioned-fixture'
    nested.mkdir()
    with pytest.raises(ValueError, match='root differs'):
        task(nested, head).verify()
    task(parent, head).verify()


def test_missing_git_identity_is_distinct_from_a_changed_head(tmp_path, monkeypatch):
    root = tmp_path / 'repository'
    head = repository(root)
    value = task(root, head)
    with pytest.raises(ValueError, match='HEAD differs'):
        replace(value, base_commit='a' * 40,
                anchors=(replace(value.anchors[0], base_commit='a' * 40),)).verify()
    monkeypatch.setattr(subprocess, 'run', lambda *a, **k: subprocess.CompletedProcess(
        a[0], 128, stdout='', stderr='Untrusted repository ownership'))
    with pytest.raises(ValueError, match='Git identity is unavailable'):
        value.verify()


def test_own_fixture_identity_survives_parent_repository_commits(tmp_path):
    parent = tmp_path / 'parent'
    repository(parent)
    nested = parent / 'independent-fixture'
    head = repository(nested)
    value = task(nested, head)
    value.verify()
    (parent / 'public.txt').write_text('Parent changed')
    git = ['git', '-C', str(parent)]
    subprocess.run([*git, 'add', 'public.txt'], check=True)
    subprocess.run([*git, '-c', 'user.name=Fixture', '-c',
                    'user.email=fixture@example.invalid', 'commit', '-qm', 'Parent update'], check=True)
    value.verify()
