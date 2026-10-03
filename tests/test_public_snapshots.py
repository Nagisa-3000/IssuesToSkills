import io
import os
import subprocess
import tarfile

import pytest

from arex_skill_graph.git_tree_export import exact_git_tar
from arex_skill_graph.public_snapshot import extract_public_archive, initialize_public_base


def git(repository, *args, **kwargs):
    return subprocess.check_output(["git", "-C", str(repository), *args], **kwargs)


def test_exact_tree_preserves_ignored_files_links_and_excludes_future_objects(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    subprocess.run(["git", "init", "-q", str(source)], check=True)
    (source / ".gitattributes").write_text("kept.txt export-ignore\nsubst.txt export-subst\n")
    (source / ".gitignore").write_text("kept.txt\n")
    (source / "kept.txt").write_text("A tracked file matching ignore rules.\n")
    (source / "subst.txt").write_text("$Format:%H$\n")
    (source / "link.txt").symlink_to("kept.txt")
    git(source, "add", "--force", "--all")
    git(
        source,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-qm",
        "public base",
    )
    base = git(source, "rev-parse", "HEAD", text=True).strip()
    commit = git(source, "cat-file", "commit", base)
    tree = git(source, "rev-parse", base + "^{tree}", text=True).strip()
    (source / "future.txt").write_text(
        "Future fixture content must stay outside the public snapshot.\n"
    )
    git(source, "add", "--all")
    git(
        source,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-qm",
        "future fixture",
    )
    future = git(source, "rev-parse", "HEAD", text=True).strip()
    archive = exact_git_tar(["git", "-C", str(source)], base)
    destination = tmp_path / "public"
    destination.mkdir()
    extract_public_archive(archive, destination)
    initialize_public_base(destination, base, commit, tree)
    assert (destination / "kept.txt").read_text() == (source / "kept.txt").read_text()
    assert (destination / "subst.txt").read_text() == "$Format:%H$\n"
    assert os.readlink(destination / "link.txt") == "kept.txt"
    assert not (destination / "future.txt").exists()
    assert git(destination, "rev-list", "--count", "HEAD", text=True).strip() == "1"
    assert git(destination, "remote", text=True).strip() == ""
    missing = subprocess.run(
        ["git", "-C", str(destination), "cat-file", "-e", future], capture_output=True, check=False
    )
    assert missing.returncode != 0


@pytest.mark.parametrize("target", ["../../outside", "/tmp/outside"])
def test_archive_rejects_symlink_escape(tmp_path, target):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        member = tarfile.TarInfo("folder/link")
        member.type, member.linkname = tarfile.SYMTYPE, target
        archive.addfile(member)
    with pytest.raises(ValueError, match="escapes"):
        extract_public_archive(stream.getvalue(), tmp_path / "contained")
