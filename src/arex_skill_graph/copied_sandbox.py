"""Explicit mount-free namespace backend with checked, atomic workspace adoption.

A minimal trusted runtime is copied and sealed. Each command receives a fresh
filesystem and a copy of the public checkout; it never sees a host bind mount.
This backend requires root in the broker and never substitutes host execution.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

from .action_contracts import digest
from .adaptive_runner import IsolationUnavailable, NamespaceTools
from .direct_skill_extraction import safe_text
from .task_context import assert_public

_BACKEND = "linux-copied-user-mount-pid-net-chroot-nobody-no-capabilities-v1"
_ENV = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}
_COMMANDS = (
    "bash",
    "sh",
    "git",
    "rg",
    "find",
    "ls",
    "cat",
    "sed",
    "head",
    "tail",
    "grep",
    "sort",
    "uniq",
    "wc",
    "mkdir",
    "rm",
    "cp",
    "mv",
    "diff",
    "patch",
    "timeout",
    "true",
    "false",
)


def _contained_tree(root, *, maximum=512 * 1024**2, public=False):
    """Inspect lstat entries without following directory links or special files."""
    root = Path(root).resolve()
    result, size = {}, 0
    pending = [root]
    while pending:
        directory = pending.pop()
        for path in directory.iterdir():
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if public:
                if ".git" in path.relative_to(root).parts:
                    raise ValueError("public workspace cannot introduce Git history")
                assert_public(relative)
            if stat.S_ISLNK(mode):
                target = os.readlink(path)
                if Path(target).is_absolute() or not path.resolve().is_relative_to(root):
                    raise ValueError("copied filesystem symlink escapes its tree")
                result[relative] = ("symlink", target)
            elif stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                if path.stat().st_size > 16 * 1024**2:
                    raise ValueError("copied filesystem file exceeds size limit")
                size += path.stat().st_size
                if size > maximum:
                    raise ValueError("copied filesystem exceeds size limit")
                content = path.read_bytes()
                if public:
                    text = content.decode("utf-8", errors="replace")
                    if safe_text(text) != text:
                        raise ValueError("restricted workspace content suppressed")
                result[relative] = ("file", hashlib.sha256(content).hexdigest(), bool(mode & 0o111))
            else:
                raise ValueError("copied filesystem contains an unsupported special file")
    return result


def _copy_public_file(source, target):
    """Retain the executable bit while stripping privileged permission bits."""
    shutil.copyfile(source, target)
    Path(target).chmod(0o755 if Path(source).stat().st_mode & 0o111 else 0o644)
    return target


def _copy_tree(source, target, *, ignore=()):
    source = Path(source).resolve()
    # Closed symlinks may be retained, but no target outside the supplied tree.
    shutil.copytree(
        source,
        target,
        symlinks=True,
        ignore=shutil.ignore_patterns(*ignore),
        copy_function=shutil.copyfile,
    )
    _contained_tree(target, maximum=2 * 1024**3)


class RuntimeCopy:
    def __init__(self, root):
        self.root = root
        self.copied = set()

    def file(self, source, destination):
        source, destination = Path(source).resolve(), Path(destination)
        target = self.root / str(destination).lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.read_bytes() != source.read_bytes():
                raise IsolationUnavailable("trusted runtime paths conflict")
            return
        shutil.copyfile(source, target)
        target.chmod(0o555 if source.stat().st_mode & 0o111 else 0o444)

    def elf(self, source, destination, *, prefix=None):
        source = Path(source).resolve()
        self.file(source, destination)
        if source in self.copied or source.open("rb").read(4) != b"\x7fELF":
            return
        self.copied.add(source)
        linked = subprocess.run(
            ["/usr/bin/ldd", str(source)],
            capture_output=True,
            text=True,
            env={
                **_ENV,
                **(
                    {"LD_LIBRARY_PATH": str(prefix / "lib")}
                    if prefix and str(prefix) not in {"/usr", "/usr/local"}
                    else {}
                ),
            },
            cwd="/",
            timeout=30,
            check=False,
        )
        if linked.returncode and not any(
            text in linked.stdout + linked.stderr
            for text in ("not a dynamic executable", "statically linked")
        ):
            raise IsolationUnavailable("trusted runtime ELF dependencies unavailable")
        if "not found" in linked.stdout:
            raise IsolationUnavailable("trusted runtime ELF dependency missing")
        for name in re.findall(r"(/[^\s()]+)", linked.stdout):
            path = Path(name)
            if not path.is_file():
                continue
            destination = name
            if (
                prefix
                and str(prefix) not in {"/usr", "/usr/local"}
                and path.resolve().is_relative_to(prefix)
            ):
                destination = "/opt/python/" + path.resolve().relative_to(prefix).as_posix()
            self.elf(path, destination, prefix=prefix)

    def python(self, dependency_root):
        interpreter = (
            dependency_root / "bin/python" if dependency_root else Path("/usr/bin/python3")
        )
        if not interpreter.is_file():
            raise IsolationUnavailable("prepared dependency interpreter is unavailable")
        details = subprocess.run(
            [
                str(interpreter),
                "-I",
                "-S",
                "-c",
                (
                    "import json,sys,sysconfig; print(json.dumps(dict(prefix=sys.base_prefix, "
                    "stdlib=sysconfig.get_path('stdlib'), version='%d.%d'%sys.version_info[:2])))"
                ),
            ],
            cwd="/",
            env=_ENV,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if details.returncode:
            raise IsolationUnavailable("prepared dependency interpreter cannot initialize")
        info = json.loads(details.stdout)
        prefix = Path(info["prefix"]).resolve()
        version = info["version"]
        if dependency_root:
            configured = {
                key.strip(): value.strip()
                for line in (dependency_root / "pyvenv.cfg").read_text().splitlines()
                if "=" in line
                for key, value in [line.split("=", 1)]
            }
            recorded = configured.get("version", "")
            if ".".join(recorded.split(".")[:2]) != version:
                raise IsolationUnavailable(
                    "prepared virtualenv Python ABI disagrees with its interpreter"
                )
        python_bin = "/opt/python/bin/python" + version
        self.elf(interpreter, python_bin, prefix=prefix)
        stdlib = self.root / ("opt/python/lib/python" + version)
        _copy_tree(
            Path(info["stdlib"]),
            stdlib,
            ignore=(
                "__pycache__",
                "site-packages",
                "dist-packages",
                "config-*",
                "sitecustomize.py",
                "usercustomize.py",
            ),
        )
        for library in stdlib.rglob("*.so"):
            original = Path(info["stdlib"]) / library.relative_to(stdlib)
            self.elf(original, "/" + library.relative_to(self.root).as_posix(), prefix=prefix)
        (self.root / "usr/bin").mkdir(parents=True, exist_ok=True)
        os.symlink(python_bin, self.root / "usr/bin/python3")
        os.symlink("python3", self.root / "usr/bin/python")
        if dependency_root:
            venv = self.root / "opt/venv"
            (venv / "bin").mkdir(parents=True)
            (venv / "pyvenv.cfg").write_text(
                "home = /opt/python/bin\ninclude-system-site-packages = false\n"
                + "version = "
                + version
                + "\n"
            )
            for name in ("python", "python3", "python" + version):
                os.symlink(python_bin, venv / "bin" / name)
            site = dependency_root / ("lib/python" + version + "/site-packages")
            if site.exists():
                _copy_tree(
                    site,
                    venv / ("lib/python" + version + "/site-packages"),
                    ignore=("__pycache__",),
                )
                for library in site.rglob("*.so"):
                    self.elf(
                        library,
                        "/opt/venv/" + library.relative_to(dependency_root).as_posix(),
                        prefix=prefix,
                    )
            for script in (dependency_root / "bin").iterdir():
                if script.name.startswith("python") or not script.is_file():
                    continue
                content = script.read_bytes()
                if content.startswith(b"#!") and b"python" in content.split(b"\n", 1)[0]:
                    target = venv / "bin" / script.name
                    target.write_bytes(b"#!/opt/venv/bin/python\n" + content.split(b"\n", 1)[1])
                    target.chmod(0o555)
                elif content.startswith(b"\x7fELF"):
                    self.elf(script, "/opt/venv/bin/" + script.name, prefix=prefix)

    def build(self, dependency_root):
        for name in _COMMANDS:
            source = shutil.which(name, path=_ENV["PATH"])
            if source:
                self.elf(source, "/usr/bin/" + name)
        os.symlink("usr/bin", self.root / "bin")
        self.python(dependency_root)
        (self.root / "etc").mkdir()
        (self.root / "etc/passwd").write_text(
            "root:x:0:0:root:/tmp:/bin/sh\nsolver:x:65534:65534:solver:/tmp:/bin/sh\n"
        )
        (self.root / "etc/group").write_text("root:x:0:\nsolver:x:65534:\n")
        # Seal runtime directories and regular files after all copying.
        for path in self.root.rglob("*"):
            if path.is_symlink():
                continue
            path.chmod(0o555 if path.is_dir() or path.stat().st_mode & 0o111 else 0o444)
        return digest(
            {
                p.relative_to(self.root).as_posix(): (
                    {"symlink": os.readlink(p)}
                    if p.is_symlink()
                    else {
                        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                        "mode": p.stat().st_mode & 0o777,
                    }
                )
                for p in self.root.rglob("*")
                if p.is_symlink() or p.is_file()
            }
        )


class CopiedNamespaceTools(NamespaceTools):
    isolation = _BACKEND

    def __init__(self, checkout, ledger, dependency_root=None):
        if os.name != "posix" or os.geteuid() != 0:
            raise IsolationUnavailable(
                "copied namespace backend requires a privileged Linux broker; no host fallback"
            )
        super().__init__(checkout, ledger, dependency_root)
        self.worker = Path(__file__).with_name("copied_sandbox_worker.py").resolve()
        self._runtime = tempfile.TemporaryDirectory(prefix="arex-copied-runtime-")
        self.template = Path(self._runtime.name) / "runtime"
        self.template.mkdir()
        try:
            self.runtime_sha256 = RuntimeCopy(self.template).build(self.dependency_root)
        except BaseException:
            self.close()
            raise

    def close(self):
        self._runtime.cleanup()

    def _root(self, root, readonly):
        shutil.copytree(self.template, root, symlinks=True, copy_function=os.link)
        _contained_tree(self.checkout, public=True)
        work = root / "workspace"
        shutil.copytree(self.checkout, work, symlinks=True, copy_function=_copy_public_file)
        for path in [work, *work.rglob("*")]:
            os.chown(
                path, 0 if readonly else 65534, 0 if readonly else 65534, follow_symlinks=False
            )
            if not path.is_symlink():
                executable = path.is_dir() or path.stat().st_mode & 0o111
                path.chmod(
                    (0o555 if executable else 0o444)
                    if readonly
                    else (0o755 if executable else 0o644)
                )
        for name in ("tmp", "proc", "dev"):
            (root / name).mkdir()
        (root / "tmp").chmod(0o1777)
        for name, minor in (("null", 3), ("zero", 5), ("random", 8), ("urandom", 9)):
            os.mknod(root / "dev" / name, stat.S_IFCHR | 0o666, os.makedev(1, minor))
            (root / "dev" / name).chmod(0o666)
        return work

    def _adopt(self, work):
        _contained_tree(work, public=True)
        # Validate the complete tree before any change to the broker checkout.
        # Recopy files (no hardlinks), strip privileges and adopt by two renames.
        with tempfile.TemporaryDirectory(prefix="arex-adopt-", dir=self.checkout.parent) as scratch:
            staged, old = Path(scratch) / "staged", Path(scratch) / "old"
            shutil.copytree(work, staged, symlinks=True, copy_function=_copy_public_file)
            for path in [staged, *staged.rglob("*")]:
                if not path.is_symlink():
                    path.chmod(0o755 if path.is_dir() or path.stat().st_mode & 0o111 else 0o644)
            self.checkout.rename(old)
            try:
                staged.rename(self.checkout)
            except BaseException:
                old.rename(self.checkout)
                raise

    def run(self, argv, *, timeout=60, stdin=None, charge=True, readonly_workspace=False):
        if not argv or any(not isinstance(a, str) or "\x00" in a for a in argv):
            raise ValueError("tool commands must be explicit argv arrays")
        assert_public(argv)
        if charge:
            self.ledger.charge("tool_calls", 1, "copied isolated public repository tool")
        self.ledger.check_time()
        timeout = min(
            timeout,
            max(0.01, self.ledger.caps.seconds - (self.ledger.clock() - self.ledger.started)),
        )
        adopted, timed_out = False, False
        with tempfile.TemporaryDirectory(prefix="arex-copied-command-") as scratch:
            root = Path(scratch) / "root"
            try:
                work = self._root(root, readonly_workspace)
            except OSError as error:
                raise IsolationUnavailable("copied sandbox filesystem setup unavailable") from error
            self.ledger.check_time()
            timeout = min(
                timeout,
                max(0.01, self.ledger.caps.seconds - (self.ledger.clock() - self.ledger.started)),
            )
            with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as input_file:
                if stdin is not None:
                    input_file.write(stdin)
                    input_file.seek(0)
                process = subprocess.Popen(
                    [sys.executable, str(self.worker), str(root), *argv],
                    stdin=input_file,
                    stdout=output,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                    env=_ENV,
                    cwd="/",
                )
                try:
                    exit_code = process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=10)
                    exit_code = 124
                finally:
                    # Also kill the trusted namespace supervisor if the launcher
                    # fails unexpectedly. PID 1 exit kills detached descendants.
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                output.seek(0)
                text = output.read(64 * 1024).decode("utf-8", errors="replace")
            if not timed_out and not readonly_workspace and exit_code != 125:
                try:
                    self._adopt(work)
                    adopted = True
                except (OSError, ValueError, RuntimeError):
                    text, exit_code = (
                        "Unsafe workspace result rejected; original checkout preserved.",
                        125,
                    )
        try:
            assert_public(text)
        except ValueError:
            text, exit_code = "Restricted tool output suppressed.", 125
        return {
            "argv": list(argv),
            "exit_code": exit_code,
            "output": text,
            "isolation": self.isolation,
            "runtime_sha256": self.runtime_sha256,
            "workspace_adopted": adopted,
            "timed_out": timed_out,
        }

    def preflight(self):
        code = """import ctypes,os,socket,pathlib
assert os.getuid()==65534 and os.getgid()==65534 and os.getgroups()==[]
assert not pathlib.Path('/home').exists() and not pathlib.Path('/run').exists()
assert not pathlib.Path('/proc/self').exists()
libc=ctypes.CDLL(None,use_errno=True)
class H(ctypes.Structure): _fields_=[('version',ctypes.c_uint32),('pid',ctypes.c_int)]
class D(ctypes.Structure): _fields_=[('effective',ctypes.c_uint32),('permitted',ctypes.c_uint32),('inheritable',ctypes.c_uint32)]
d=(D*2)();assert libc.capget(ctypes.byref(H(0x20080522,0)),ctypes.byref(d))==0
assert all(x.effective==x.permitted==x.inheritable==0 for x in d)
assert libc.prctl(39,0,0,0,0)==1
try: os.setuid(0); raise AssertionError('privilege escape')
except PermissionError: pass
s=socket.socket();s.settimeout(.2)
try: s.connect(('1.1.1.1',80)); raise AssertionError('network escape')
except OSError: pass
print('COPIED_ISOLATED')
"""
        result = self.run(["python3", "-c", code], charge=False, readonly_workspace=True)
        if result["exit_code"] or "COPIED_ISOLATED" not in result["output"]:
            raise IsolationUnavailable(
                "copied namespace/capability preflight failed; no host fallback"
            )
