"""Privileged namespace launcher for a copied, mount-free public filesystem.

The broker supplies a closed filesystem. PID 1 stays a trusted supervisor; an
untrusted command cannot detach PID 1 and survive broker cancellation.
"""

from __future__ import annotations

import ctypes
import os
import resource
import select
import signal
import sys
from pathlib import Path


def _check(value, operation):
    if value != 0:
        raise OSError(ctypes.get_errno(), operation)


def _drop_privileges(libc):
    _check(libc.prctl(38, 1, 0, 0, 0), "freeze sandbox privileges")
    for capability in range(41):
        value = libc.prctl(24, capability, 0, 0, 0)
        if value and ctypes.get_errno() != 22:
            _check(value, "drop capability bounding set")
    os.setgroups([])
    os.setgid(65534)
    os.setuid(65534)

    class Header(ctypes.Structure):
        _fields_ = [("version", ctypes.c_uint32), ("pid", ctypes.c_int)]

    class Data(ctypes.Structure):
        _fields_ = [
            ("effective", ctypes.c_uint32),
            ("permitted", ctypes.c_uint32),
            ("inheritable", ctypes.c_uint32),
        ]

    data = (Data * 2)()
    _check(
        libc.capset(ctypes.byref(Header(0x20080522, 0)), ctypes.byref(data)), "clear capabilities"
    )


def _supervise(root, argv, libc):
    # This process is namespace PID 1 and never executes untrusted code itself.
    os.chroot(root)
    os.chdir("/workspace")
    os.closerange(3, 65536)
    _drop_privileges(libc)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    resource.setrlimit(resource.RLIMIT_NPROC, (256, 256))
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024**3,) * 2)
    child = os.fork()
    if child == 0:
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
    _, status = os.waitpid(child, 0)
    code = os.waitstatus_to_exitcode(status)
    # Exiting PID 1 terminates every descendant, including setsid/double forks.
    os._exit(code if code >= 0 else 128 - code)


def launch(root, argv):
    if os.geteuid() != 0:
        raise RuntimeError("copied namespace launcher requires privileged broker")
    libc = ctypes.CDLL(None, use_errno=True)
    ready_r, ready_w = os.pipe()
    go_r, go_w = os.pipe()
    child = os.fork()
    if child == 0:
        os.close(ready_r)
        os.close(go_w)
        try:
            # CLONE_NEWUSER | NEWNS | NEWNET | NEWPID; no mount operation.
            _check(
                libc.unshare(0x10000000 | 0x20000 | 0x40000000 | 0x20000000), "create namespaces"
            )
            os.write(ready_w, b"ready")
            os.close(ready_w)
            if os.read(go_r, 1) != b"x":
                os._exit(125)
            os.close(go_r)
            init = os.fork()
            if init == 0:
                _supervise(root, argv, libc)
            _, status = os.waitpid(init, 0)
            code = os.waitstatus_to_exitcode(status)
            os._exit(code if code >= 0 else 128 - code)
        except BaseException:  # noqa: BLE001 -- Forked setup failures must never resume in the host broker.
            os.write(2, b"Copied sandbox namespace/privilege setup failed.\n")
            os._exit(125)
    os.close(ready_w)
    os.close(go_r)
    try:
        if not select.select([ready_r], [], [], 10)[0] or os.read(ready_r, 16) != b"ready":
            raise RuntimeError("copied sandbox namespace readiness failed")
        # Map root for setup and nobody for execution. Only the trusted broker
        # owns host root; the actual command runs without IDs or capabilities 0.
        Path(f"/proc/{child}/uid_map").write_text("0 0 65536\n")
        Path(f"/proc/{child}/gid_map").write_text("0 0 65536\n")
        os.write(go_w, b"x")
    except BaseException:
        try:
            os.kill(child, signal.SIGKILL)
        except ProcessLookupError:
            pass
        os.waitpid(child, 0)
        raise
    finally:
        os.close(ready_r)
        os.close(go_w)
    _, status = os.waitpid(child, 0)
    code = os.waitstatus_to_exitcode(status)
    return code if code >= 0 else 128 - code


if __name__ == "__main__":
    sys.exit(launch(sys.argv[1], sys.argv[2:]))
