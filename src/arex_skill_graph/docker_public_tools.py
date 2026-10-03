"""Public repository tools in a pinned SWE environment with a single workspace mount.

The checkout contains only the public base snapshot. Mounting it over /testbed
hides the image's repository and Git history. No evaluator files, Docker socket,
host home, credentials or network are exposed to the command process.
"""

from __future__ import annotations

import io
import os
import re
import tarfile
from pathlib import Path

from .action_contracts import digest
from .adaptive_runner import IsolationUnavailable
from .task_context import assert_public


class DockerPublicTools:
    isolation = "docker-public-base-mount-no-network-no-capabilities-v1"

    def __init__(
        self, checkout, ledger, *, client, image_id, repository_digest, conda_environment=None
    ):
        self.checkout, self.ledger = Path(checkout).resolve(), ledger
        if os.name != "posix" or not self.checkout.is_dir():
            raise IsolationUnavailable("Docker public tools require a local Linux snapshot")
        if (self.checkout / ".git").exists():
            raise ValueError("public Docker workspace must not contain Git history")
        if conda_environment is not None and not re.fullmatch(r"[a-zA-Z0-9_-]+", conda_environment):
            raise ValueError("invalid prepared environment name")
        self.client, self.image = client, client.images.get(image_id)
        if self.image.id != image_id or repository_digest not in self.image.attrs.get(
            "RepoDigests", []
        ):
            raise ValueError("Docker runtime image/digest differs from its frozen identity")
        assert_public(self.image.attrs.get("Config", {}).get("Env", []))
        self.conda_environment = conda_environment
        self.runtime_sha256 = digest(
            {
                "image_id": image_id,
                "repository_digest": repository_digest,
                "conda_environment": conda_environment,
                "isolation": self.isolation,
            }
        )

    def run(self, argv, *, timeout=60, stdin=None, charge=True, readonly_workspace=False):
        if not argv or any(not isinstance(a, str) or "\x00" in a for a in argv):
            raise ValueError("tool commands must be explicit argv arrays")
        assert_public(argv)
        if stdin is not None:
            assert_public(stdin.decode("utf-8", errors="replace"))
        if charge:
            self.ledger.charge("tool_calls", 1, "isolated public Docker repository tool")
        self.ledger.check_time()
        timeout = min(
            timeout,
            max(0.01, self.ledger.caps.seconds - (self.ledger.clock() - self.ledger.started)),
        )
        container = self.client.containers.create(
            self.image.id,
            ["sleep", "infinity"],
            entrypoint=[],
            network_disabled=True,
            cap_drop=["ALL"],
            security_opt=["no-new-privileges:true"],
            read_only=True,
            user=f"{os.getuid()}:{os.getgid()}",
            working_dir="/testbed",
            pids_limit=256,
            mem_limit="4g",
            nano_cpus=2_000_000_000,
            volumes={
                str(self.checkout): {
                    "bind": "/testbed",
                    "mode": "ro" if readonly_workspace else "rw",
                }
            },
            tmpfs={"/tmp": "rw,nosuid,nodev,size=1g"},
            environment={
                "HOME": "/tmp",
                "PYTHONHASHSEED": "0",
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTEST_ADDOPTS": "-p no:cacheprovider",
            },
        )
        try:
            container.start()
            redirect = ""
            if stdin is not None:
                stream = io.BytesIO()
                with tarfile.open(fileobj=stream, mode="w") as archive:
                    member = tarfile.TarInfo("arex-tool-stdin")
                    member.size, member.mode = len(stdin), 0o600
                    member.uid, member.gid = os.getuid(), os.getgid()
                    archive.addfile(member, io.BytesIO(stdin))
                container.put_archive("/tmp", stream.getvalue())
                redirect = " < /tmp/arex-tool-stdin"
            # All shell text is fixed. User argv remains positional arguments;
            # it is never interpolated into the wrapper's shell source.
            wrapper = (
                (
                    'source /opt/miniconda3/etc/profile.d/conda.sh && conda activate "$1" '
                    '&& shift && exec "$@"' + redirect
                )
                if self.conda_environment
                else ('exec "$@"' + redirect)
            )
            environment_args = [self.conda_environment] if self.conda_environment else []
            result = container.exec_run(
                [
                    "timeout",
                    str(timeout),
                    "bash",
                    "-c",
                    wrapper,
                    "arex-public-tool",
                    *environment_args,
                    *argv,
                ]
            )
            output = result.output[: 64 * 1024].decode("utf-8", errors="replace")
            exit_code = result.exit_code
            try:
                assert_public(output)
            except ValueError:
                output, exit_code = "Restricted tool output suppressed.", 125
            self.ledger.check_time()
            return {
                "argv": list(argv),
                "exit_code": exit_code,
                "output": output,
                "isolation": self.isolation,
            }
        except Exception as error:
            from .adaptive_budget import BudgetExceeded

            if isinstance(error, (BudgetExceeded, ValueError)):
                raise
            raise IsolationUnavailable(
                f"public Docker tool infrastructure failed ({type(error).__name__}); native output suppressed"
            ) from None
        finally:
            container.remove(force=True)

    def preflight(self):
        result = self.run(
            [
                "python",
                "-c",
                (
                    "import os; assert not os.path.exists('/testbed/.git'); "
                    "assert not os.path.exists('/var/run/docker.sock'); "
                    "assert not os.path.exists('/eval.sh'); "
                    "assert not os.path.exists('/repair.diff'); "
                    "assert not any(k in os.environ for k in ['AREX_LLM_API_KEY', 'OPENAI_API_KEY', 'GH_TOKEN', 'GITHUB_TOKEN']); "
                    "print('PUBLIC_DOCKER_ISOLATED')"
                ),
            ],
            charge=False,
        )
        if result["exit_code"] or "PUBLIC_DOCKER_ISOLATED" not in result["output"]:
            raise IsolationUnavailable(
                "public Docker preflight failed; no solver command was authorized"
            )
