"""Linux namespace tool worker. Invoked only by the public solver broker."""

from __future__ import annotations

import ctypes
import os
from pathlib import Path
import resource
import subprocess
import sys


def mount(*args):
    subprocess.run(
        ["mount", *args], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def readonly_bind(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    mount("--rbind", str(source), str(destination))
    points = []
    for line in Path("/proc/self/mountinfo").read_text().splitlines():
        columns = line.split()
        point = Path(columns[4].replace("\\040", " "))
        if point == destination or point.is_relative_to(destination):
            points.append((point, columns[5].split(",")))
    for point, options in sorted(points, key=lambda item: len(str(item[0])), reverse=True):
        locked = [
            o
            for o in options
            if o in {"noexec", "noatime", "nodiratime", "relatime", "strictatime"}
        ]
        mount("-o", ",".join(["remount", "bind", "ro", "nosuid", "nodev", *locked]), str(point))


def worker(root, checkout, dependency_root, workspace_mode, argv):
    # Prevent namespace mounts propagating into the host's shared mount tree.
    mount("--make-rprivate", "/")
    root = Path(root).resolve()
    root.mkdir()
    mount("-t", "tmpfs", "-o", "size=512m,nosuid,nodev", "tmpfs", str(root))
    for name in ("usr", "bin", "lib", "lib64"):
        source = Path("/" + name)
        if source.exists():
            readonly_bind(source.resolve(), root / name)
    if dependency_root != "-":
        readonly_bind(Path(dependency_root).resolve(), root / "opt/venv")
    (root / "workspace").mkdir()
    mount("--bind", str(Path(checkout).resolve()), str(root / "workspace"))
    if workspace_mode == "ro":
        mount("-o", "remount,bind,ro,nosuid,nodev", str(root / "workspace"))
    (root / "tmp").mkdir(mode=0o1777)
    (root / "proc").mkdir()
    mount("-t", "proc", "-o", "nosuid,nodev,noexec", "proc", str(root / "proc"))
    (root / "dev").mkdir()
    for name in ("null", "zero", "urandom", "random"):
        target = root / "dev" / name
        target.touch()
        mount("--bind", "/dev/" + name, str(target))
    (root / "etc").mkdir()
    (root / "etc/passwd").write_text("root:x:0:0:Sandbox:/tmp:/bin/sh\n")
    (root / "etc/group").write_text("root:x:0:\n")
    for name in ("ld.so.cache", "localtime"):
        source = Path("/etc") / name
        if source.is_file():
            (root / "etc" / name).write_bytes(source.read_bytes())
    os.chroot(root)
    os.chdir("/workspace")
    libc = ctypes.CDLL(None, use_errno=True)
    # No inherited directory descriptor or capability can escape the chroot.
    os.closerange(3, 1024)
    if libc.prctl(38, 1, 0, 0, 0) != 0:  # PR_SET_NO_NEW_PRIVS
        raise RuntimeError("cannot freeze privilege boundary")
    for capability in range(41):
        libc.prctl(24, capability, 0, 0, 0)  # PR_CAPBSET_DROP

    class Header(ctypes.Structure):
        _fields_ = [("version", ctypes.c_uint32), ("pid", ctypes.c_int)]

    class Data(ctypes.Structure):
        _fields_ = [
            ("effective", ctypes.c_uint32),
            ("permitted", ctypes.c_uint32),
            ("inheritable", ctypes.c_uint32),
        ]

    data = (Data * 2)()
    if libc.capset(ctypes.byref(Header(0x20080522, 0)), ctypes.byref(data)) != 0:
        raise RuntimeError("cannot drop sandbox capabilities")
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    os.execvpe(
        argv[0],
        argv,
        {
            "PATH": "/opt/venv/bin:/usr/bin:/bin",
            "HOME": "/tmp",
            "LANG": "C.UTF-8",
            "PYTHONHASHSEED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
        },
    )


if __name__ == "__main__":
    worker(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
