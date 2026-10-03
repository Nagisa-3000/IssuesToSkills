"""Export exact pinned Git blobs, ignoring archive export-ignore/export-subst rules.

This worker is also copied into a coordinator container. It depends only on
Python's standard library and Git, and writes only a tar stream to stdout.
"""

from __future__ import annotations

import io
import re
import subprocess
import sys
import tarfile


def exact_git_tar(git, revision):
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Git tree export requires a pinned revision")
    raw_tree = subprocess.check_output([*git, "ls-tree", "-rz", "--full-tree", revision])
    entries = []
    for record in raw_tree.split(b"\x00"):
        if not record:
            continue
        header, path = record.split(b"\t", 1)
        mode, kind, oid = header.split(b" ")
        if kind != b"blob" or mode not in {b"100644", b"100755", b"120000"}:
            raise ValueError("public base contains an unsupported submodule or object mode")
        entries.append((mode, oid, path.decode("utf-8")))
    result = subprocess.run(
        [*git, "cat-file", "--batch"],
        input=b"\n".join(oid for _, oid, _ in entries) + b"\n",
        capture_output=True,
        check=True,
    )
    objects = io.BytesIO(result.stdout)
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w") as archived:
        for mode, oid, name in entries:
            header = objects.readline().rstrip(b"\n").split(b" ")
            if len(header) != 3 or header[:2] != [oid, b"blob"]:
                raise ValueError("Git blob export identity/type mismatch")
            size = int(header[2])
            content = objects.read(size)
            if len(content) != size or objects.read(1) != b"\n":
                raise ValueError("Git blob export was truncated")
            member = tarfile.TarInfo(name)
            member.mode = 0o755 if mode == b"100755" else 0o644
            if mode == b"120000":
                member.type, member.linkname = tarfile.SYMTYPE, content.decode("utf-8")
                archived.addfile(member)
            else:
                member.size = size
                archived.addfile(member, io.BytesIO(content))
    if objects.read():
        raise ValueError("Git blob export has unexpected trailing data")
    return output.getvalue()


if __name__ == "__main__":
    repository, revision = sys.argv[1:]
    sys.stdout.buffer.write(
        exact_git_tar(["git", "-c", "safe.directory=" + repository, "-C", repository], revision)
    )
