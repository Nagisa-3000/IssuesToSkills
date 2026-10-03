import io
import tarfile
from types import SimpleNamespace

import pytest

from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_runner import IsolationUnavailable
from arex_skill_graph.docker_public_tools import DockerPublicTools


def public_tools(tmp_path):
    calls = []
    container = SimpleNamespace(
        start=lambda: calls.append(("start",)),
        put_archive=lambda path, data: calls.append(("archive", path, data)),
        exec_run=lambda argv: (
            calls.append(("exec", argv))
            or SimpleNamespace(exit_code=0, output=b"PUBLIC_DOCKER_ISOLATED")
        ),
        remove=lambda **kw: calls.append(("remove", kw)),
    )
    image = SimpleNamespace(
        id="sha256:synthetic",
        attrs={
            "RepoDigests": ["example/image@sha256:synthetic"],
            "Config": {"Env": ["PATH=/usr/bin"]},
        },
    )
    client = SimpleNamespace(
        images=SimpleNamespace(get=lambda _: image),
        containers=SimpleNamespace(
            create=lambda *args, **kwargs: calls.append(("create", args, kwargs)) or container
        ),
    )
    tools = DockerPublicTools(
        tmp_path,
        BudgetLedger(BudgetCaps()),
        client=client,
        image_id=image.id,
        repository_digest=image.attrs["RepoDigests"][0],
    )
    return tools, calls, container, image


def test_public_container_exposes_only_snapshot_with_frozen_runtime(tmp_path):
    tools, calls, _, _ = public_tools(tmp_path)
    tools.preflight()
    _, _, args = next(c for c in calls if c[0] == "create")
    assert args["network_disabled"] is True and args["cap_drop"] == ["ALL"]
    assert args["read_only"] is True and args["security_opt"] == ["no-new-privileges:true"]
    assert args["volumes"] == {str(tmp_path): {"bind": "/testbed", "mode": "rw"}}
    assert set(args["environment"]) == {
        "HOME",
        "PYTHONHASHSEED",
        "PYTHONDONTWRITEBYTECODE",
        "PYTEST_ADDOPTS",
    }
    assert calls[-1] == ("remove", {"force": True})
    assert tools.ledger.tool_calls == 0


def test_readonly_tools_and_stdin_use_positional_argv(tmp_path):
    tools, calls, _, _ = public_tools(tmp_path)
    argv = ["python", "-c", "print('$literal; unchanged')"]
    result = tools.run(argv, stdin=b"synthetic input", readonly_workspace=True)
    assert result["argv"] == argv and tools.ledger.tool_calls == 1
    _, _, args = next(c for c in calls if c[0] == "create")
    assert args["volumes"][str(tmp_path)]["mode"] == "ro"
    command = next(c[1] for c in calls if c[0] == "exec")
    assert command[-3:] == argv
    assert argv[-1] not in command[4]
    transferred = next(c[2] for c in calls if c[0] == "archive")
    with tarfile.open(fileobj=io.BytesIO(transferred)) as archive:
        (entry,) = archive.getmembers()
        assert entry.mode == 0o600 and archive.extractfile(entry).read() == b"synthetic input"


def test_container_is_removed_after_infrastructure_failure(tmp_path):
    tools, calls, container, _ = public_tools(tmp_path)
    container.exec_run = lambda argv: (_ for _ in ()).throw(
        RuntimeError("synthetic private detail")
    )
    with pytest.raises(IsolationUnavailable, match="native output suppressed") as error:
        tools.run(["python", "-V"])
    assert "synthetic private detail" not in str(error.value)
    assert calls[-1] == ("remove", {"force": True})


def test_image_or_git_history_drift_prevents_any_tool(tmp_path):
    tools, calls, _, image = public_tools(tmp_path)
    (tmp_path / ".git").mkdir()
    with pytest.raises(ValueError, match="Git history"):
        DockerPublicTools(
            tmp_path,
            tools.ledger,
            client=tools.client,
            image_id=image.id,
            repository_digest="example/image@sha256:synthetic",
        )
    assert not calls
