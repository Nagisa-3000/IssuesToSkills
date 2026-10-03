"""Export a public base tree and its single shallow commit from a pinned runtime.

This module has no dataset/solution loader. Its inputs are public identity and
an already-qualified image digest. Future Git objects stay inside the temporary
coordinator container and are never copied into the public task repository.
"""

from __future__ import annotations

import hashlib
import io
import os
import re
import tarfile
from pathlib import Path

from .history_census import fingerprint, now, write_json
from .public_snapshot import extract_public_archive, initialize_public_base
from .task_context import assert_public


def prepare_public_swe_base(client, image_id, repository_digest, base_commit, output):
    if not re.fullmatch(r"[0-9a-f]{40}", base_commit):
        raise ValueError("public SWE base must be pinned")
    image = client.images.get(image_id)
    if image.id != image_id or repository_digest not in image.attrs.get("RepoDigests", []):
        raise ValueError("public preparation image/digest differs from its qualified identity")
    output = Path(output).resolve()
    if output.exists():
        raise ValueError("public preparation output exists; preserve it and use a new version")
    container = client.containers.create(
        image.id,
        ["sleep", "infinity"],
        network_disabled=True,
        cap_drop=["ALL"],
        security_opt=["no-new-privileges:true"],
    )
    try:
        container.start()
        git = ["git", "-c", "safe.directory=/testbed", "-C", "/testbed"]
        worker = Path(__file__).with_name("git_tree_export.py").read_bytes()
        transfer = io.BytesIO()
        with tarfile.open(fileobj=transfer, mode="w") as archived:
            member = tarfile.TarInfo("arex-public-tree-export.py")
            member.size, member.mode = len(worker), 0o600
            archived.addfile(member, io.BytesIO(worker))
        container.put_archive("/tmp", transfer.getvalue())
        archive = container.exec_run(
            ["python3", "/tmp/arex-public-tree-export.py", "/testbed", base_commit]
        )
        commit = container.exec_run([*git, "cat-file", "commit", base_commit])
        tree = container.exec_run([*git, "rev-parse", base_commit + "^{tree}"])
        if any(result.exit_code for result in (archive, commit, tree)):
            raise ValueError("qualified image cannot export the pinned public base")
        raw_archive, raw_commit = archive.output, commit.output
        tree_id = tree.output.decode().strip()
        assert_public(raw_commit.decode("utf-8", errors="replace"))
    finally:
        container.remove(force=True)
    checkout = output / "checkout"
    checkout.mkdir(parents=True)
    extract_public_archive(raw_archive, checkout)
    inventory = {}
    for path in checkout.rglob("*"):
        if path.is_file():
            content = path.read_bytes()
            assert_public(content.decode("utf-8", errors="replace"))
            inventory[path.relative_to(checkout).as_posix()] = (
                "symlink:" + os.readlink(path)
                if path.is_symlink()
                else hashlib.sha256(content).hexdigest()
            )
    initialize_public_base(checkout, base_commit, raw_commit, tree_id)
    result = {
        "schema": "public-swe-base-preparation-v1",
        "checked_at": now(),
        "image_id": image_id,
        "repository_digest": repository_digest,
        "base_commit": base_commit,
        "base_tree": tree_id,
        "checkout": str(checkout),
        "file_count": len(inventory),
        "public_tree_sha256": fingerprint(inventory),
        "only_base_git_commit_exported": True,
        "private_dataset_loaded": False,
        "exporter_sha256": hashlib.sha256(worker).hexdigest(),
        "formal_SWE_solver_runs": 0,
    }
    write_json(output / "preparation.json", result)
    return result
