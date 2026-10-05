"""Real mount-free isolation tests; no namespace or filesystem operations mocked."""

import json
import os
import subprocess
import time
from pathlib import Path

import pytest

from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_runner import (
    TOOL_BACKENDS,
    AdaptiveSolver,
    IsolationUnavailable,
    hidden_evaluator_from_file,
    make_namespace_tools,
)
from arex_skill_graph.copied_sandbox import CopiedNamespaceTools, _copy_public_file
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.workflow_ranker import WorkflowRanker


@pytest.fixture
def copied_tools(tmp_path):
    if os.name != "posix" or os.geteuid() != 0:
        pytest.skip("copied namespace backend requires a privileged Linux broker")
    root = tmp_path / "public"
    root.mkdir()
    (root / "source.txt").write_text("original")
    with make_namespace_tools(root, BudgetLedger(), backend="namespace-copy") as tools:
        # Once privileged, a missing namespace is a real test failure, not a skip.
        tools.preflight()
        yield tools


def test_backend_selection_is_explicit_and_never_falls_back(monkeypatch, tmp_path):
    assert "namespace-copy" in TOOL_BACKENDS
    with pytest.raises(ValueError, match="unknown sandbox"):
        make_namespace_tools(tmp_path, BudgetLedger(), backend="host")
    monkeypatch.setattr(os, "geteuid", lambda: 2050)
    with pytest.raises(IsolationUnavailable, match="privileged Linux broker"):
        CopiedNamespaceTools(tmp_path, BudgetLedger())


def test_host_network_privileges_runtime_and_environment_denied(copied_tools, tmp_path):
    secret_control = tmp_path / "private-control.txt"
    secret_control.write_text("host-only data")
    code = """import os,pathlib,socket
assert os.getuid()==65534 and os.getgid()==65534 and os.getgroups()==[]
assert set(os.environ)<=set(['HOME','LANG','LC_CTYPE','PATH','LD_LIBRARY_PATH','PYTHONDONTWRITEBYTECODE','PYTHONHASHSEED'])
assert os.environ.get('LD_LIBRARY_PATH')=='/opt/python/lib:/opt/venv/lib'
assert not pathlib.Path(HOST_PATH).exists()
assert pathlib.Path('/').stat().st_ino==pathlib.Path('/..').stat().st_ino
for op in [lambda:os.setuid(0),lambda:os.chroot('/'),lambda:pathlib.Path('/usr/forbidden').write_text('x'),lambda:pathlib.Path('/opt/python/bin/python3.10').open('ab')]:
 try:op();raise AssertionError('boundary escaped')
 except (PermissionError,FileNotFoundError):pass
s=socket.socket();s.settimeout(.2)
try:s.connect(('1.1.1.1',80));raise AssertionError('network escaped')
except OSError:pass
pathlib.Path('/workspace/source.txt').write_text('permitted')
print('BOUNDARIES_OK')
""".replace("HOST_PATH", repr(str(secret_control)))
    result = copied_tools.run(["python3", "-c", code])
    assert result["exit_code"] == 0, result
    assert result["workspace_adopted"]
    assert (copied_tools.checkout / "source.txt").read_text() == "permitted"
    assert secret_control.read_text() == "host-only data"


def test_readonly_probe_denies_chmod_delete_create_and_rename(copied_tools):
    code = """import os,pathlib
for op in [lambda:pathlib.Path('source.txt').write_text('x'),lambda:os.chmod('source.txt',0o777),lambda:os.unlink('source.txt'),lambda:os.rename('source.txt','renamed'),lambda:pathlib.Path('new').mkdir()]:
 try:op();raise AssertionError('probe modified workspace')
 except PermissionError:pass
print('READONLY_OK')
"""
    result = copied_tools.run(["python3", "-c", code], readonly_workspace=True)
    assert result["exit_code"] == 0, result
    assert not result["workspace_adopted"]
    assert sorted(p.name for p in copied_tools.checkout.iterdir()) == ["source.txt"]
    assert (copied_tools.checkout / "source.txt").read_text() == "original"


@pytest.mark.parametrize(
    "operation", ["os.symlink('/etc/passwd','escaped')", "os.mkfifo('fifo')", "os.mkdir('.git')"]
)
def test_invalid_tree_is_rejected_atomically(copied_tools, operation):
    result = copied_tools.run(
        [
            "python3",
            "-c",
            "import os,pathlib;pathlib.Path('source.txt').write_text('bad');" + operation,
        ]
    )
    assert result["exit_code"] == 125, result
    assert not result["workspace_adopted"]
    assert (copied_tools.checkout / "source.txt").read_text() == "original"
    assert sorted(p.name for p in copied_tools.checkout.iterdir()) == ["source.txt"]


def _tagged_processes(tag):
    matches = []
    for entry in Path("/proc").iterdir():
        if entry.name.isdigit():
            try:
                if (entry / "comm").read_text().strip() == tag:
                    state = (entry / "stat").read_text().split(") ", 1)[1].split()[0]
                    if state != "Z":
                        matches.append(int(entry.name))
            except (FileNotFoundError, PermissionError, ProcessLookupError):
                pass
    return matches


def _detach_code(tag, timeout):
    return """import ctypes,os,pathlib,time
r,w=os.pipe()
pid=os.fork()
if pid==0:
 os.setsid()
 if os.fork():os._exit(0)
 os.close(r)
 libc=ctypes.CDLL(None);libc.prctl(15,TAG.encode(),0,0,0)
 os.write(w,b'x');os.close(w)
 time.sleep(20);pathlib.Path('late').write_text('leaked');os._exit(0)
os.close(w);assert os.read(r,1)==b'x';os.close(r)
pathlib.Path('source.txt').write_text('changed')
SLEEP
""".replace("TAG", repr(tag)).replace(
        "SLEEP", "time.sleep(20)" if timeout else "print('DETACHED_READY')"
    )


@pytest.mark.parametrize("timeout", [False, True])
def test_detached_double_forks_terminated_and_timeout_does_not_adopt(copied_tools, timeout):
    tag = "arex" + str(os.getpid()) + ("time" if timeout else "done")
    assert not _tagged_processes(tag)
    result = copied_tools.run(
        ["python3", "-c", _detach_code(tag, timeout)], timeout=2 if timeout else 30
    )
    assert result["exit_code"] == (124 if timeout else 0), result
    for _ in range(20):
        if not _tagged_processes(tag):
            break
        time.sleep(0.05)
    assert not _tagged_processes(tag), "detached sandbox process survived"
    assert result["workspace_adopted"] is (not timeout)
    assert (copied_tools.checkout / "source.txt").read_text() == (
        "original" if timeout else "changed"
    )
    assert not (copied_tools.checkout / "late").exists()


def test_git_stdin_patch_and_failed_checks_retain_valid_edits(copied_tools):
    patch = b"diff --git a/source.txt b/source.txt\n--- a/source.txt\n+++ b/source.txt\n@@ -1 +1 @@\n-original\n\\ No newline at end of file\n+fixed\n\\ No newline at end of file\n"
    applied = copied_tools.run(["git", "apply", "--whitespace=nowarn", "-"], stdin=patch)
    assert applied["exit_code"] == 0, applied
    failed = copied_tools.run(["bash", "-c", "printf retained > new.txt; exit 1"])
    assert failed["exit_code"] == 1 and failed["workspace_adopted"], failed
    assert (copied_tools.checkout / "source.txt").read_text() == "fixed"
    assert (copied_tools.checkout / "new.txt").read_text() == "retained"


def test_prepared_virtualenv_and_entrypoint_are_relocated(copied_tools, tmp_path):
    venv = tmp_path / "prepared"
    subprocess.run(["/usr/bin/python3", "-m", "venv", "--without-pip", str(venv)], check=True)
    version = subprocess.check_output(
        [str(venv / "bin/python"), "-c", "import sys;print('%d.%d'%sys.version_info[:2])"],
        text=True,
    ).strip()
    site = venv / ("lib/python" + version + "/site-packages")
    (site / "prepared_example.py").write_text("VALUE = 'relocated'\n")
    script = venv / "bin/check-prepared"
    script.write_text(
        "#!"
        + str(venv / "bin/python")
        + "\nimport prepared_example;print(prepared_example.VALUE)\n"
    )
    script.chmod(0o755)
    with make_namespace_tools(
        copied_tools.checkout, BudgetLedger(), venv, backend="namespace-copy"
    ) as tools:
        tools.preflight()
        python = tools.run(
            [
                "python3",
                "-c",
                "import sys,prepared_example;assert sys.prefix=='/opt/venv';print(prepared_example.VALUE)",
            ]
        )
        entry = tools.run(["check-prepared"])
        assert python["exit_code"] == entry["exit_code"] == 0, (python, entry)
        assert python["output"].strip() == entry["output"].strip() == "relocated"
        assert tools.runtime_sha256 != copied_tools.runtime_sha256


def test_solver_finishes_before_copied_independent_evaluator(copied_tools, tmp_path):
    from adaptive_fixture import make_fixture

    from arex_skill_graph.adaptive_cli import ReplayTransport

    _, task, policy = make_fixture(tmp_path / "task")
    marker = tmp_path / "evaluation.json"
    original = Path(task.root, "checker.py").read_text()
    fixed = original.replace("return True", "return context != 'type'")
    steps = [
        {
            "operation": "write_file",
            "arguments": {"path": "checker.py", "content": fixed},
            "rationale": "Repair current guard",
        },
        {
            "operation": "run_public_command",
            "arguments": {"argv": ["python3", "checker.py"]},
            "rationale": "Public current behavior",
        },
        {"operation": "finish", "arguments": {}, "rationale": "Done before independent evaluation"},
    ]

    class CheckingReplay(ReplayTransport):
        def complete(self, **kwargs):
            assert not marker.exists()
            return super().complete(**kwargs)

    def evaluate(task, patch):
        marker.write_text(
            json.dumps(
                {
                    "task_id": task.task_id,
                    "base_commit": task.base_commit,
                    "evaluator_version": "synthetic-copied-independent-v1",
                    "benchmark_commands": [["python3", "checker.py"]],
                    "regression_commands": [
                        [
                            "python3",
                            "-c",
                            "from checker import diagnostic;assert diagnostic('runtime')",
                        ]
                    ],
                }
            )
        )
        return hidden_evaluator_from_file(marker, sandbox_backend="namespace-copy")(task, patch)

    with CatalogStore(tmp_path / "empty.sqlite") as store:
        store.initialize()
        result = AdaptiveSolver(
            CheckingReplay(steps),
            WorkflowRanker(),
            store,
            policy,
            BudgetLedger(BudgetCaps(history_tokens=200000)),
            arm="B0",
            sandbox_backend="namespace-copy",
        ).run(task, evaluator=evaluate)
    assert result["solver_ended"] and result["validated_resolved"], result
    assert result["isolation"] == result["evaluation"]["isolation"] == copied_tools.isolation
    assert Path(task.root, "checker.py").read_text() == original
    assert result["budget"]["model_calls"] == 3


def test_migrated_interpreter_abi_mismatch_is_rejected(copied_tools, tmp_path):
    venv = tmp_path / "mismatched"
    subprocess.run(["/usr/bin/python3", "-m", "venv", "--without-pip", str(venv)], check=True)
    cfg = venv / "pyvenv.cfg"
    cfg.write_text("home = /usr/bin\ninclude-system-site-packages = false\nversion = 99.1.0\n")
    with pytest.raises(IsolationUnavailable, match="ABI disagrees"):
        make_namespace_tools(copied_tools.checkout, BudgetLedger(), venv, backend="namespace-copy")


def test_public_copy_preserves_execution_without_privileged_bits(tmp_path):
    source, target = tmp_path / "script", tmp_path / "copied"
    source.write_text("#!/bin/sh\nexit 0\n")
    source.chmod(0o4755)
    _copy_public_file(source, target)
    assert target.read_bytes() == source.read_bytes()
    assert target.stat().st_mode & 0o7777 == 0o755
    source.chmod(0o640)
    _copy_public_file(source, target)
    assert target.stat().st_mode & 0o7777 == 0o644


def test_public_executable_survives_readonly_command_and_adoption(copied_tools):
    script = copied_tools.checkout / "public-script"
    script.write_text("#!/bin/sh\nprintf SCRIPT_OK\n")
    script.chmod(0o755)
    readonly = copied_tools.run(["./public-script"], readonly_workspace=True)
    assert readonly["exit_code"] == 0 and readonly["output"] == "SCRIPT_OK", readonly
    assert not readonly["workspace_adopted"]
    adopted = copied_tools.run(
        ["python3", "-c", "from pathlib import Path;Path('source.txt').write_text('changed')"]
    )
    assert adopted["exit_code"] == 0 and adopted["workspace_adopted"], adopted
    assert script.stat().st_mode & 0o7777 == 0o755
    executed = copied_tools.run(["./public-script"])
    assert executed["exit_code"] == 0 and executed["output"] == "SCRIPT_OK", executed
    assert script.stat().st_mode & 0o7777 == 0o755


def test_scoped_actual_command_rolls_back_unrelated_files_and_permissions(copied_tools):
    from arex_skill_graph.workspace_state import public_workspace_execution_sha256
    from arex_skill_graph.workspace_transactions import run_scoped_command

    script = copied_tools.checkout / "public-script"
    script.write_text("#!/bin/sh\nexit 0\n")
    script.chmod(0o755)
    before = public_workspace_execution_sha256(copied_tools.checkout)
    result = run_scoped_command(
        copied_tools.checkout,
        {"source.txt"},
        lambda: copied_tools.run(
            [
                "python3",
                "-c",
                (
                    "import pathlib,os;pathlib.Path('source.txt').write_text('unaccepted');"
                    "pathlib.Path('extra.py').write_text('outside');os.chmod('public-script',0o644)"
                ),
            ]
        ),
    )
    assert result["exit_code"] == 125 and result["process_exit_code"] == 0, result
    assert result["workspace_rollback"] and not result["write_scope_accepted"]
    assert result["out_of_scope_paths"] == ["extra.py", "public-script"]
    assert public_workspace_execution_sha256(copied_tools.checkout) == before


def test_scoped_actual_command_retains_valid_bound_changes(copied_tools):
    from arex_skill_graph.workspace_transactions import run_scoped_command

    result = run_scoped_command(
        copied_tools.checkout,
        {"source.txt"},
        lambda: copied_tools.run(
            ["python3", "-c", "from pathlib import Path;Path('source.txt').write_text('accepted')"]
        ),
    )
    assert result["exit_code"] == 0 and result["write_scope_accepted"], result
    assert (copied_tools.checkout / "source.txt").read_text() == "accepted"


def test_shared_python_runtime_loads_after_relocation(tmp_path):
    runtime = os.environ.get("AREX_TEST_SHARED_PYTHON_RUNTIME")
    if not runtime:
        pytest.skip("provide an isolated virtualenv built from a shared Python interpreter")
    if os.name != "posix" or os.geteuid() != 0:
        pytest.skip("copied runtime verification requires a privileged Linux broker")
    runtime = Path(runtime).resolve()
    host = subprocess.check_output(
        [
            str(runtime / "bin/python"),
            "-I",
            "-c",
            (
                "import json,sys,sysconfig; print(json.dumps({'version':sys.version.split()[0],"
                "'shared':sysconfig.get_config_var('Py_ENABLE_SHARED')}))"
            ),
        ],
        text=True,
        env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
    )
    expected = json.loads(host)
    assert expected["shared"] == 1, "test requires an actual shared interpreter"
    checkout = tmp_path / "public"
    checkout.mkdir()
    with make_namespace_tools(
        checkout,
        BudgetLedger(BudgetCaps(seconds=300, tool_calls=5)),
        runtime,
        backend="namespace-copy",
    ) as tools:
        tools.preflight()
        result = tools.run(
            [
                "python3",
                "-c",
                (
                    "import ctypes,sys,sysconfig; "
                    "ctypes.CDLL(sysconfig.get_config_var('INSTSONAME') or sysconfig.get_config_var('LDLIBRARY')); "
                    "assert sys.prefix == '/opt/venv'; "
                    "print(sys.version.split()[0])"
                ),
            ],
            readonly_workspace=True,
        )
    assert result["exit_code"] == 0, result
    assert result["output"].strip() == expected["version"]
    assert result["workspace_adopted"] is False
