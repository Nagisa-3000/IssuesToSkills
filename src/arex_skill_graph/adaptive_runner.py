"""One shared reasoning/tool loop with enforced public-only Linux namespace tools.

The solver can see only its base snapshot and approved guidance. Hidden patches
are loaded by the independent evaluator after solver termination, never by any
model, planner, ranker or public tool process.
"""

from __future__ import annotations

from dataclasses import replace
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

from .action_contracts import digest
from .adaptive_budget import BudgetExceeded, BudgetedTransport
from .adaptive_guidance import prepare_adaptive_guidance
from .guidance_renderer import GuidanceRenderer
from .plan_validation import TaskWorkflowPlan, validate_task_plan
from .skill_packages import _resolve
from .task_context import EvidenceAnchor, ObservedFact, assert_public


class IsolationUnavailable(RuntimeError):
    pass


class NamespaceTools:
    def __init__(self, checkout, ledger, dependency_root=None):
        self.checkout, self.ledger = Path(checkout).resolve(), ledger
        if os.name != "posix" or not shutil.which("unshare"):
            raise IsolationUnavailable(
                "Linux user/mount/PID/network namespaces are required; no unsafe fallback"
            )
        self.worker = Path(__file__).with_name("sandbox_tool.py").resolve()
        self.dependency_root = Path(dependency_root).resolve() if dependency_root else None
        self.runtime_sha256 = "system-python-only"
        if self.dependency_root:
            cfg = self.dependency_root / "pyvenv.cfg"
            if (
                not cfg.is_file()
                or "include-system-site-packages = false" not in cfg.read_text().lower()
            ):
                raise ValueError("use a prepared isolated virtualenv without system-site packages")
            self.runtime_sha256 = digest(
                {
                    p.relative_to(self.dependency_root).as_posix(): hashlib.sha256(
                        p.read_bytes()
                    ).hexdigest()
                    for p in self.dependency_root.rglob("*")
                    if p.is_file()
                }
            )

    def run(self, argv, *, timeout=60, stdin=None, charge=True, readonly_workspace=False):
        if not argv or any(not isinstance(a, str) or "\x00" in a for a in argv):
            raise ValueError("tool commands must be explicit argv arrays")
        assert_public(argv)
        if charge:
            self.ledger.charge("tool_calls", 1, "isolated public repository tool")
        self.ledger.check_time()
        timeout = min(
            timeout,
            max(0.01, self.ledger.caps.seconds - (self.ledger.clock() - self.ledger.started)),
        )
        with tempfile.TemporaryDirectory(prefix="arex-isolated-") as scratch:
            command = [
                "unshare",
                "--user",
                "--map-root-user",
                "--mount",
                "--net",
                "--pid",
                "--fork",
                "--kill-child",
                "python3",
                str(self.worker),
                str(Path(scratch) / "root"),
                str(self.checkout),
                str(self.dependency_root) if self.dependency_root else "-",
                "ro" if readonly_workspace else "rw",
                *argv,
            ]
            with tempfile.TemporaryFile() as output:
                try:
                    result = subprocess.run(
                        command,
                        input=stdin,
                        stdout=output,
                        stderr=subprocess.STDOUT,
                        timeout=timeout,
                        check=False,
                        start_new_session=True,
                    )
                    exit_code = result.returncode
                except subprocess.TimeoutExpired:
                    exit_code = 124
                output.seek(0)
                text = output.read(64 * 1024).decode("utf-8", errors="replace")
        try:
            assert_public(text)
        except ValueError:
            text = "Restricted tool output suppressed."
            exit_code = 125
        return {
            "argv": list(argv),
            "exit_code": exit_code,
            "output": text,
            "isolation": "linux-user-mount-pid-net-chroot-no-capabilities-v1",
        }

    def preflight(self):
        result = self.run(
            [
                "python3",
                "-c",
                "import os,socket; assert not os.path.exists('/home'); assert not os.path.exists('/run'); print('ISOLATED')",
            ],
            charge=False,
        )
        if result["exit_code"] or "ISOLATED" not in result["output"]:
            raise IsolationUnavailable(
                "Namespace/mount/capability preflight failed; public tools were not executed"
            )


def snapshot_base(task, destination):
    task.verify()
    raw = subprocess.check_output(["git", "-C", task.root, "archive", task.base_commit])
    destination = Path(destination)
    destination.mkdir()
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        for member in archive.getmembers():
            if member.issym() or member.islnk() or not (member.isfile() or member.isdir()):
                raise ValueError("public base snapshot contains unsupported links or special files")
            _resolve(destination, member.name)
        archive.extractall(destination, filter="data")
    initial = replace(task, root=str(destination))
    initial.verify(verify_head=False)
    for path in destination.rglob("*"):
        if path.is_file():
            # Prevent literal credentials in tracked source from entering the solver mount.
            from .direct_skill_extraction import safe_text

            content = path.read_bytes().decode("utf-8", errors="replace")
            if safe_text(content) != content:
                raise ValueError(
                    "public snapshot contains restricted credential-like content; suppressed"
                )
    return initial


def patch_from_snapshot(baseline, checkout):
    result = subprocess.run(
        ["git", "diff", "--no-index", "--binary", "--no-prefix", str(baseline), str(checkout)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode not in {0, 1}:
        raise ValueError("could not derive solver patch")
    patch = result.stdout
    for directory, prefix in ((baseline, "a/"), (checkout, "b/")):
        patch = patch.replace(str(directory) + "/", prefix).replace(
            str(directory).lstrip("/") + "/", prefix
        )
    assert_public(patch)
    return patch


class AdaptiveSolver:
    SYSTEM = (
        "Solve the current public software issue using current repository observations. Historical guidance is conditional, not a patch to copy. "
        "Use the broker tools. Unknown plan prerequisites require public probes. Refresh observations after edits and failed oracles. "
        "No hidden evaluator, future history, host filesystem, network or credentials are accessible to tools. Return one request JSON: "
        "operation = read_file | write_file | run_public_command | read_skill_resource | refresh_guidance | drop_guidance | finish; arguments is an object; rationale is text."
    )
    SCHEMA = {"type": "object", "required": ["operation", "arguments", "rationale"]}

    def __init__(
        self, transport, ranker, store, resource_policy, ledger, *, arm="E2", dependency_root=None
    ):
        self.transport, self.ranker, self.store = transport, ranker, store
        self.policy, self.ledger, self.arm = resource_policy, ledger, arm
        self.dependency_root = dependency_root

    def run(self, task, *, evaluator=None, use_frozen_selection=False, initial_plan=None):
        self.ledger.check_time()
        observations, guidance_runs, requests, guidance_usage = [], [], [], []
        ended, failed = False, ""
        with tempfile.TemporaryDirectory(prefix="arex-public-solver-") as scratch:
            scratch = Path(scratch)
            self.ledger.charge(
                "tool_calls", 2, "pinned base verification and public snapshot archive"
            )
            current = snapshot_base(task, scratch / "work")
            baseline = scratch / "baseline"
            shutil.copytree(current.root, baseline)
            initial_snapshot = digest(
                {
                    p.relative_to(baseline).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in baseline.rglob("*")
                    if p.is_file()
                }
            )
            tools = NamespaceTools(current.root, self.ledger, self.dependency_root)
            self.ledger.charge("tool_calls", 1, "enforced namespace preflight")
            tools.preflight()
            policy = replace(self.policy, verify_head=False)
            selected = None
            prerequisite_probes = 0
            guidance = "Continue solving from current public evidence."

            def review():
                nonlocal current, guidance, selected, prerequisite_probes
                prerequisite_probes = 0
                result = prepare_adaptive_guidance(
                    current,
                    self.store,
                    policy,
                    self.ranker,
                    self.ledger,
                    arm=self.arm,
                    ground_with_model=self.ranker.transport is not None,
                )
                current = type(current).from_dict(result["task_context"])
                selected = (
                    TaskWorkflowPlan.from_dict(result["selected_plan"])
                    if result["selected_plan"]
                    else None
                )
                guidance = result["guidance"]
                guidance_runs.append(result)
                if selected:
                    guidance_usage.append(
                        {
                            "plan_id": selected.id,
                            "parent_workflow_ids": list(selected.parent_workflow_ids),
                            "context_revision": current.revision,
                        }
                    )

            try:
                if use_frozen_selection:
                    selected = initial_plan
                    if initial_plan:
                        guidance_usage.append(
                            {
                                "plan_id": initial_plan.id,
                                "parent_workflow_ids": list(initial_plan.parent_workflow_ids),
                                "context_revision": current.revision,
                            }
                        )
                    guidance = (
                        GuidanceRenderer(policy, self.ledger).render(initial_plan, current)
                        if initial_plan
                        else "No applicable guidance in the frozen candidate pool."
                    )
                elif self.arm != "B0":
                    review()
                while not ended:
                    self.ledger.check_time()
                    public_context = current.to_dict()
                    public_context.pop("root")
                    request = BudgetedTransport(self.transport, self.ledger).complete(
                        system=self.SYSTEM,
                        user=json.dumps(
                            {
                                "current": public_context,
                                "guidance": guidance,
                                "public_files": sorted(
                                    p.relative_to(current.root).as_posix()
                                    for p in Path(current.root).rglob("*")
                                    if p.is_file()
                                ),
                                "observations": observations,
                                "previous_requests": requests[-6:],
                            }
                        ),
                        response_schema=self.SCHEMA,
                    )
                    assert_public(request)
                    if set(request) != {"operation", "arguments", "rationale"}:
                        raise ValueError("invalid solver request fields")
                    operation, args = request["operation"], request["arguments"]
                    if not isinstance(args, dict) or not isinstance(request["rationale"], str):
                        raise ValueError("invalid solver request")
                    requests.append(request)
                    if operation == "finish":
                        ended = True
                        continue
                    if operation in {"read_file", "write_file"}:
                        relative = args["path"]
                        if relative.startswith(".git/"):
                            raise ValueError("version history is not a solver input")
                        path = _resolve(Path(current.root), relative)
                        self.ledger.charge("tool_calls", 1, "public file " + operation)
                        if operation == "read_file":
                            result = {
                                "operation": operation,
                                "path": relative,
                                "content": path.read_text(),
                            }
                            assert_public(result)
                        else:
                            if (
                                selected
                                and validate_task_plan(selected, current, policy).mode != "use"
                            ):
                                observations.append(
                                    {
                                        "operation": operation,
                                        "denied": "probe-only guidance requires observation/refresh or explicit drop_guidance before modifying code",
                                    }
                                )
                                continue
                            assert_public(args["content"])
                            path.parent.mkdir(parents=True, exist_ok=True)
                            path.write_text(args["content"])
                            refreshed = [
                                replace(
                                    a,
                                    sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                    observation="Current implementation changed; semantic facts require renewed evidence.",
                                )
                                for a in current.anchors
                                if a.path == relative
                            ]
                            current = current.update(anchors=tuple(refreshed))
                            selected = None
                            guidance = "Current code changed. Refresh guidance and establish actual postconditions before using historical directives again."
                            result = {"operation": operation, "path": relative, "written": True}
                    elif operation == "run_public_command":
                        probe_only = (
                            selected is not None
                            and validate_task_plan(selected, current, policy).mode != "use"
                        )
                        if probe_only:
                            prerequisite_probes += 1
                            if prerequisite_probes > self.ledger.caps.probes_per_round:
                                observations.append(
                                    {
                                        "operation": operation,
                                        "denied": "prerequisite probe cap reached; refresh or drop guidance",
                                    }
                                )
                                continue
                        result = tools.run(
                            args["argv"],
                            timeout=args.get("timeout", 60),
                            readonly_workspace=probe_only,
                        )
                        anchor_id = "current:probe:" + str(len(observations))
                        anchor = EvidenceAnchor(
                            anchor_id,
                            "probe",
                            json.dumps(result),
                            current.base_commit,
                            exit_code=result["exit_code"],
                        )
                        current = current.update(
                            anchors=(anchor,),
                            facts=(
                                ObservedFact(
                                    "last_public_probe_passed",
                                    result["exit_code"] == 0,
                                    (anchor_id,),
                                ),
                            ),
                        )
                    elif operation == "drop_guidance":
                        self.ledger.charge(
                            "tool_calls", 1, "explicit fallback from conditional Skill guidance"
                        )
                        selected = None
                        guidance = "Continue normal public issue solving from current observations."
                        result = {"operation": operation, "fallback_reason": request["rationale"]}
                    elif operation == "refresh_guidance":
                        for relative in args.get("code_paths", []):
                            path = _resolve(Path(current.root), relative)
                            anchor = EvidenceAnchor(
                                "current:code:" + relative,
                                "current_code",
                                "Current source inspected after public observation",
                                current.base_commit,
                                relative,
                                hashlib.sha256(path.read_bytes()).hexdigest(),
                            )
                            current = current.update(anchors=(anchor,))
                        review()
                        result = {"operation": operation, "guidance": guidance}
                    elif operation == "read_skill_resource":
                        if selected is None:
                            raise ValueError("no approved current plan resource")
                        self.ledger.charge("tool_calls", 1, "approved Skill resource read")
                        renderer = GuidanceRenderer(policy, self.ledger)
                        result = {
                            "operation": operation,
                            "content": renderer.read_resource(
                                args["package_id"], args["resource"], selected.package_ids
                            ),
                        }
                    else:
                        raise ValueError("unknown solver operation")
                    changed_anchors = []
                    for anchor in current.anchors:
                        if anchor.path:
                            path = _resolve(Path(current.root), anchor.path)
                            if not path.is_file():
                                raise ValueError(
                                    "public tool removed an anchored interface; refresh required"
                                )
                            actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                            if actual_hash != anchor.sha256:
                                changed_anchors.append(
                                    replace(
                                        anchor,
                                        sha256=actual_hash,
                                        observation="Tool changed current code; renew semantic observations.",
                                    )
                                )
                    if changed_anchors:
                        current = current.update(anchors=tuple(changed_anchors))
                        selected = None
                        guidance = "Public tool changed current code; re-observe prerequisites and refresh guidance."
                    observations.append(result)
            except BudgetExceeded as exc:
                failed = str(exc)
            patch = patch_from_snapshot(baseline, Path(current.root))
            result = {
                "task_id": task.task_id,
                "arm": self.arm,
                "solver_ended": ended,
                "failure": failed,
                "base_commit": task.base_commit,
                "public_snapshot_sha256": initial_snapshot,
                "patch": patch,
                "patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),
                "requests": requests,
                "public_observations": observations,
                "guidance_runs": guidance_runs,
                "guidance_usage": guidance_usage,
                "budget": self.ledger.snapshot(),
                "isolation": "linux-user-mount-pid-net-chroot-no-capabilities-v1",
                "runtime_sha256": tools.runtime_sha256,
                "benchmark_resolved": None,
                "validated_resolved": None,
            }
            # The callback is invoked only after the last possible model/tool/guidance call.
            if evaluator is not None:
                result["evaluation"] = evaluator(task, patch)
                result["benchmark_resolved"] = bool(
                    ended and not failed and result["evaluation"].get("benchmark_resolved")
                )
                result["validated_resolved"] = bool(
                    ended and not failed and result["evaluation"].get("validated_resolved")
                )
            assert_public(result)
            return result


def hidden_evaluator_from_file(manifest_path, *, dependency_root=None):
    """Defer reading private evaluation material until the solver has stopped."""

    def evaluate(task, patch):
        spec = json.loads(Path(manifest_path).read_text())
        if spec["task_id"] != task.task_id or spec["base_commit"] != task.base_commit:
            raise ValueError("independent evaluator identity mismatch")
        from .adaptive_budget import BudgetCaps, BudgetLedger

        with tempfile.TemporaryDirectory(prefix="arex-hidden-evaluator-") as scratch:
            snapshot_base(task, Path(scratch) / "evaluation")
            work = Path(scratch) / "evaluation"
            tools = NamespaceTools(work, BudgetLedger(BudgetCaps(tool_calls=100)), dependency_root)
            tools.preflight()
            applied = (
                tools.run(["git", "apply", "--whitespace=nowarn", "-"], stdin=patch.encode())
                if patch
                else {"exit_code": 0}
            )
            if applied["exit_code"]:
                return {
                    "benchmark_resolved": False,
                    "validated_resolved": False,
                    "reason": "solver patch failed to apply",
                }
            if spec.get("hidden_test_patch"):
                applied = tools.run(
                    ["git", "apply", "--whitespace=nowarn", "-"],
                    stdin=spec["hidden_test_patch"].encode(),
                )
                if applied["exit_code"]:
                    return {
                        "benchmark_resolved": False,
                        "validated_resolved": False,
                        "reason": "hidden evaluation setup failed",
                    }
            benchmark = [tools.run(argv) for argv in spec["benchmark_commands"]]
            regression = [tools.run(argv) for argv in spec.get("regression_commands", [])]
            # Persist outcomes and spec hashes, never private tests or their output/paths.
            passed = all(r["exit_code"] == 0 for r in benchmark) and bool(benchmark)
            return {
                "benchmark_resolved": passed,
                "validated_resolved": passed
                and bool(regression)
                and all(r["exit_code"] == 0 for r in regression),
                "evaluator_version": spec["evaluator_version"],
                "evaluation_spec_sha256": digest(spec),
                "benchmark_exit_codes": [r["exit_code"] for r in benchmark],
                "regression_exit_codes": [r["exit_code"] for r in regression],
            }

    return evaluate
