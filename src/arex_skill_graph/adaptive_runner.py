"""One shared reasoning/tool loop with enforced public-only Linux namespace tools.

The solver can see only its base snapshot and approved guidance. Hidden patches
are loaded by the independent evaluator after solver termination, never by any
model, planner, ranker or public tool process.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from contextlib import ExitStack
from dataclasses import replace
from pathlib import Path
from typing import ClassVar

from .action_contracts import digest
from .action_grounding import review_action_observation
from .action_observations import record_action_observation
from .adaptive_budget import BudgetedTransport, BudgetExceeded
from .adaptive_guidance import current_grounding, prepare_adaptive_guidance
from .execution_frontier import (
    action_execution_checks,
    declared_write_paths,
    ready_modifying_action,
)
from .git_tree_export import exact_git_tar
from .guidance_renderer import GuidanceRenderer
from .plan_validation import TaskWorkflowPlan, validate_task_plan
from .public_snapshot import extract_public_archive
from .skill_packages import _resolve
from .task_context import EvidenceAnchor, ObservedFact, assert_public
from .workspace_state import (
    copy_sealed_public_workspace,
    copy_verified_workspace_modes,
    public_workspace_execution_sha256,
    public_workspace_sha256,
)
from .workspace_transactions import run_scoped_command
from .workflow_rewriter import rebind_frozen_plan


class IsolationUnavailable(RuntimeError):
    pass


class NamespaceTools:
    isolation = "linux-user-mount-pid-net-chroot-no-capabilities-v1"

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

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()

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


TOOL_BACKENDS = ("namespace-bind", "namespace-copy")


def make_namespace_tools(checkout, ledger, dependency_root=None, *, backend="namespace-bind"):
    if backend == "namespace-bind":
        return NamespaceTools(checkout, ledger, dependency_root)
    if backend == "namespace-copy":
        from .copied_sandbox import CopiedNamespaceTools

        return CopiedNamespaceTools(checkout, ledger, dependency_root)
    raise ValueError("unknown sandbox backend; choose an explicit supported backend")


def snapshot_base(task, destination, *, resume_reviewed_state=False):
    task.verify()
    if type(resume_reviewed_state) is not bool:
        raise ValueError("public state resume mode must be an explicit boolean")
    destination = Path(destination)
    execution_seals = {a.sha256 for a in task.anchors if a.kind == "workspace_execution_snapshot"}
    if resume_reviewed_state:
        if len(execution_seals) != 1:
            raise ValueError("resuming current public state requires one consistent execution seal")
        copy_sealed_public_workspace(task.root, destination, next(iter(execution_seals)))
    else:
        raw = exact_git_tar(["git", "-C", task.root], task.base_commit)
        destination.mkdir()
        extract_public_archive(raw, destination)
        if execution_seals:
            copy_verified_workspace_modes(task.root, destination)
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


def bounded_public_view(value, *, text_limit=5000):
    """Present public excerpts without replacing the complete trajectory evidence."""
    if isinstance(value, str) and len(value) > text_limit:
        half = text_limit // 2
        return (
            value[:half]
            + "\n[PUBLIC TEXT EXCERPT: "
            + str(len(value))
            + " characters; sha256="
            + hashlib.sha256(value.encode()).hexdigest()
            + "; use focused reads/commands for omitted content]\n"
            + value[-half:]
        )
    if isinstance(value, dict):
        return {
            key: bounded_public_view(item, text_limit=text_limit) for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [bounded_public_view(item, text_limit=text_limit) for item in value]
    return value


def request_history_view(requests):
    """Avoid replaying complete file writes in every subsequent model request."""
    result = []
    for request in requests[-8:]:
        item = {**request, "arguments": dict(request["arguments"])}
        content = item["arguments"].get("content")
        if item["operation"] == "write_file" and isinstance(content, str):
            del item["arguments"]["content"]
            item["arguments"].update(
                content_characters=len(content),
                content_sha256=hashlib.sha256(content.encode()).hexdigest(),
            )
        result.append(bounded_public_view(item, text_limit=2000))
    return result


class AdaptiveSolver:
    SYSTEM = (
        "Solve the current public software issue using current repository observations. Historical guidance is conditional, not a patch to copy. "
        "Use the broker tools. Unknown plan prerequisites require public probes. Refresh observations after edits and failed oracles. "
        "No hidden evaluator, future history, host filesystem, network or credentials are accessible to tools. Return one request JSON: "
        "operation = list_files | read_file | write_file | run_public_command | read_skill_resource | refresh_guidance | drop_guidance | record_action_observation | finish; arguments is an object; rationale is text. "
        "list_files arguments: prefix (optional repository directory), offset (default 0), limit (1..200). "
        "read_file requires path, with optional start_line (1-based) and limit (1..400; default 200); "
        "write_file requires path and complete content (both strings). "
        "run_public_command requires argv, an array of command/argument strings, and optional timeout seconds; "
        "for shell syntax use argv=['bash','-c','the public shell command']. A command string alone is invalid. "
        "read_skill_resource requires package_id and resource strings. refresh_guidance accepts code_paths, a string array. "
        "record_action_observation requires action_id, current context_revision, summary and outputs. "
        "Each declared output has port_name, observation_ids and artifact_paths; cite actual broker results or current files. "
        "When the Action declares no output ports, use outputs=[] plus top-level observation_ids and artifact_paths; "
        "at least one actual witness is required. Do not invent a port. "
        "Execution and port recording are unreviewed and never prove prerequisites, effects or repair success. "
        "refresh_guidance independently reviews fresh recorded outputs before they can become current inputs. "
        "A strict functional Action catalog also requires actual ready prerequisites and action_id for modifications. "
        "Gather all current files and inputs before modifying an Action. A single public command may apply its full change across bound files; code changes invalidate consumed pre-edit evidence. "
        "While guidance is active, modifying write_file or command requests must provide action_id "
        "for an Action whose actual prerequisites and inputs are currently ready; planned effects are insufficient. "
        "drop_guidance and finish take empty arguments. "
        "Use public commands to search source and run tests. Read current files before changing them. "
        "Long output is presented as excerpts; use focused commands and paginated file reads to inspect omitted parts. "
        "Only recent observations are replayed. Finish once the repair and focused public checks are complete."
    )
    SCHEMA: ClassVar[dict] = {"type": "object", "required": ["operation", "arguments", "rationale"]}

    def __init__(
        self,
        transport,
        ranker,
        store,
        resource_policy,
        ledger,
        *,
        arm="E2",
        dependency_root=None,
        tools_factory=None,
        sandbox_backend="namespace-bind",
    ):
        self.transport, self.ranker, self.store = transport, ranker, store
        self.policy, self.ledger, self.arm = resource_policy, ledger, arm
        self.dependency_root = dependency_root
        self.tools_factory = tools_factory
        if sandbox_backend not in TOOL_BACKENDS:
            raise ValueError("unknown sandbox backend")
        self.sandbox_backend = sandbox_backend

    def run(
        self,
        task,
        *,
        evaluator=None,
        use_frozen_selection=False,
        initial_plan=None,
        initial_observations=(),
        recordable_actions=(),
        read_only_workspace=False,
        resume_reviewed_state=False,
        enforce_catalog_prerequisites=False,
    ):
        self.ledger.check_time()
        if type(read_only_workspace) is not bool:
            raise ValueError("public workspace mode must be explicitly boolean")
        if type(enforce_catalog_prerequisites) is not bool:
            raise ValueError("Action catalog execution mode must be boolean")
        if enforce_catalog_prerequisites and (not use_frozen_selection or not recordable_actions):
            raise ValueError(
                "Strict functional execution requires an explicit frozen Action catalog"
            )
        assert_public(initial_observations)
        observations, guidance_runs, requests, guidance_usage = (
            list(initial_observations),
            [],
            [],
            [],
        )
        ended, failed = False, ""
        action_catalog, action_observations, broker_observations = {}, [], {}
        action_output_reviews, reviewed_records = [], set()

        def register_actions(actions):
            for action in actions:
                old = action_catalog.get(action.id)
                if old is not None and old != action:
                    raise ValueError("Action observation identity changed its source contract")
                if old is None:
                    self.ledger.approve_root(action.package_id)
                    self.ledger.history(
                        json.dumps(
                            {"action_id": action.id, "outputs": [p.name for p in action.outputs]}
                        ),
                        "delivered Action observation catalog labels",
                    )
                    action_catalog[action.id] = action

        def ready_catalog_action(action_id, current):
            action = action_catalog.get(action_id)
            if (
                action
                and action.kind in {"edit", "bridge", "cleanup"}
                and action_execution_checks(action, current)["ready"]
            ):
                return action
            return None

        with (
            tempfile.TemporaryDirectory(prefix="arex-public-solver-") as scratch,
            ExitStack() as cleanup,
        ):
            scratch = Path(scratch)
            self.ledger.charge(
                "tool_calls", 2, "pinned base verification and public snapshot archive"
            )
            current = snapshot_base(
                task, scratch / "work", resume_reviewed_state=resume_reviewed_state
            )
            baseline = scratch / "baseline"
            shutil.copytree(current.root, baseline, symlinks=True)
            initial_snapshot = digest(
                {
                    p.relative_to(baseline).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in baseline.rglob("*")
                    if p.is_file()
                }
            )
            tools = (
                self.tools_factory(current.root, self.ledger)
                if self.tools_factory
                else make_namespace_tools(
                    current.root, self.ledger, self.dependency_root, backend=self.sandbox_backend
                )
            )
            cleanup.callback(getattr(tools, "close", lambda: None))
            self.ledger.charge("tool_calls", 1, "enforced namespace preflight")
            tools.preflight()
            policy = replace(self.policy, verify_head=False)
            selected = None
            prerequisite_probes = 0
            pending_guidance_refresh = False
            guidance = "Continue solving from current public evidence."

            def review():
                nonlocal current, guidance, selected, prerequisite_probes, pending_guidance_refresh
                prerequisite_probes = 0
                if self.ranker.transport is not None:
                    for record in action_observations:
                        if record["id"] in reviewed_records:
                            continue
                        if record.get("workspace_sha256") != public_workspace_sha256(
                            current.root
                        ) or record.get(
                            "workspace_execution_sha256"
                        ) != public_workspace_execution_sha256(current.root):
                            action_output_reviews.append(
                                {
                                    "record_id": record["id"],
                                    "status": "stale",
                                    "current_ports_promoted": [],
                                }
                            )
                        else:
                            current, output_review = review_action_observation(
                                current,
                                action_catalog[record["action_id"]],
                                record,
                                broker_observations,
                                self.ranker.transport,
                                self.ledger,
                                verify_head=False,
                            )
                            action_output_reviews.append(output_review)
                        reviewed_records.add(record["id"])
                if use_frozen_selection:
                    # Fixed-candidate supervision permits fresh current binding,
                    # never a new rewrite/composition/retrieval choice.
                    if initial_plan and self.ranker.transport is not None:
                        scoped = [
                            p
                            for p in policy.load()
                            if p.reference["skill_id"] in initial_plan.package_ids
                        ]
                        current = current_grounding(
                            current,
                            scoped,
                            self.ranker.transport,
                            self.ledger,
                            verify_head=policy.verify_head,
                        )
                    rebound = (
                        rebind_frozen_plan(initial_plan, current, policy) if initial_plan else None
                    )
                    report = validate_task_plan(rebound, current, policy) if rebound else None
                    if report and report.status == "FAIL":
                        rebound = None
                    result = {
                        "schema": "frozen-candidate-rebinding-v1",
                        "task_context": current.to_dict(),
                        "selected_plan": rebound.to_dict() if rebound else None,
                        "nominated_plan_id": initial_plan.id if initial_plan else None,
                        "candidate_generation_frozen": True,
                        "validation": report.to_dict() if report else None,
                        "guidance": GuidanceRenderer(policy, self.ledger).render(rebound, current)
                        if rebound
                        else "Continue normal public issue solving from current observations.",
                    }
                else:
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
                pending_guidance_refresh = False
                if selected:
                    register_actions(i.action for i in selected.instances)
                    guidance_usage.append(
                        {
                            "plan_id": selected.id,
                            "nominated_plan_id": initial_plan.id
                            if use_frozen_selection and initial_plan
                            else None,
                            "parent_workflow_ids": list(selected.parent_workflow_ids),
                            "context_revision": current.revision,
                        }
                    )

            try:
                if recordable_actions:
                    if not use_frozen_selection:
                        raise ValueError(
                            "Explicit functional Action catalogs require fixed selection"
                        )
                    authoritative = {a.id: a for p in policy.load() for a in p.actions}
                    if any(authoritative.get(a.id) != a for a in recordable_actions):
                        raise ValueError(
                            "Functional Action catalog differs from authored resources"
                        )
                    register_actions(recordable_actions)
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
                    if initial_plan:
                        register_actions(i.action for i in initial_plan.instances)
                    guidance = (
                        GuidanceRenderer(policy, self.ledger).render(initial_plan, current)
                        if initial_plan
                        else "No applicable guidance in the frozen candidate pool."
                    )
                elif self.arm != "B0":
                    review()
                while not ended:
                    self.ledger.check_time()
                    public_context = bounded_public_view(current.to_dict(), text_limit=2000)
                    public_context.pop("root")
                    request = BudgetedTransport(self.transport, self.ledger).complete(
                        system=self.SYSTEM,
                        user=json.dumps(
                            {
                                "current": public_context,
                                "guidance": guidance,
                                "public_workspace_read_only": read_only_workspace,
                                "strict_functional_action_catalog": enforce_catalog_prerequisites,
                                "functional_execution_frontier": [
                                    action_execution_checks(a, current)
                                    for a in action_catalog.values()
                                ]
                                if enforce_catalog_prerequisites
                                else [],
                                "action_observation_catalog": [
                                    {"action_id": a.id, "outputs": [p.name for p in a.outputs]}
                                    for a in action_catalog.values()
                                ],
                                "action_observation_assurance": "unreviewed; records do not promote facts or ports",
                                "public_tree": {
                                    "top_level": sorted(
                                        p.name for p in Path(current.root).iterdir()
                                    ),
                                    "listing_tool": "list_files",
                                },
                                "observations": bounded_public_view(observations[-8:]),
                                "earlier_observations_count": max(0, len(observations) - 8),
                                "previous_requests": request_history_view(requests),
                            }
                        ),
                        response_schema=self.SCHEMA,
                    )
                    assert_public(request)
                    if set(request) != {"operation", "arguments", "rationale"}:
                        raise ValueError("invalid solver request fields")
                    operation, args = request["operation"], request["arguments"]
                    if not isinstance(args, dict) or not isinstance(request["rationale"], str):
                        raise ValueError("invalid solver request")  # noqa: TRY004 -- JSON contract errors consistently use ValueError.
                    requests.append(request)
                    fields = {
                        "read_file": {"path": str},
                        "write_file": {"path": str, "content": str},
                        "run_public_command": {"argv": list},
                        "read_skill_resource": {"package_id": str, "resource": str},
                        "list_files": {},
                        "refresh_guidance": {},
                        "drop_guidance": {},
                        "record_action_observation": {
                            "action_id": str,
                            "context_revision": int,
                            "summary": str,
                            "outputs": list,
                        },
                        "finish": {},
                    }
                    if operation not in fields or any(
                        not isinstance(args.get(name), expected_type)
                        for name, expected_type in fields.get(operation, {}).items()
                    ):
                        observations.append(
                            {
                                "operation": operation,
                                "protocol_error": "Use a documented operation and its required argument fields. "
                                "run_public_command requires argv: an array, e.g. ['bash', '-c', 'ls']. "
                                "read/write_file require path; write_file also requires content.",
                            }
                        )
                        continue
                    if operation == "finish":
                        ended = True
                        continue
                    if operation == "list_files":
                        self.ledger.charge("tool_calls", 1, "public repository file listing")
                        prefix = args.get("prefix", "")
                        directory = (
                            _resolve(Path(current.root), prefix) if prefix else Path(current.root)
                        )
                        offset, limit = args.get("offset", 0), args.get("limit", 200)
                        if (
                            type(offset) is not int
                            or offset < 0
                            or type(limit) is not int
                            or not 1 <= limit <= 200
                            or not directory.is_dir()
                        ):
                            raise ValueError("invalid public file listing arguments")
                        files = sorted(
                            p.relative_to(current.root).as_posix()
                            for p in directory.rglob("*")
                            if p.is_file()
                        )
                        result = {
                            "operation": operation,
                            "files": files[offset : offset + limit],
                            "total": len(files),
                            "next_offset": offset + limit if offset + limit < len(files) else None,
                        }
                    elif operation in {"read_file", "write_file"}:
                        relative = args["path"]
                        if relative.startswith(".git/"):
                            raise ValueError("version history is not a solver input")
                        path = _resolve(Path(current.root), relative)
                        self.ledger.charge("tool_calls", 1, "public file " + operation)
                        if operation == "read_file":
                            start, limit = args.get("start_line", 1), args.get("limit", 200)
                            if (
                                type(start) is not int
                                or start < 1
                                or type(limit) is not int
                                or not 1 <= limit <= 400
                            ):
                                raise ValueError("invalid public file pagination")
                            lines = path.read_text().splitlines(keepends=True)
                            result = {
                                "operation": operation,
                                "path": relative,
                                "content": "".join(lines[start - 1 : start - 1 + limit]),
                                "start_line": start,
                                "total_lines": len(lines),
                                "next_line": start + limit if start + limit <= len(lines) else None,
                            }
                            assert_public(result)
                        else:
                            if read_only_workspace:
                                observations.append(
                                    {
                                        "operation": operation,
                                        "denied": "This public Action exercise has a read-only workspace.",
                                    }
                                )
                                continue
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
                            if pending_guidance_refresh:
                                observations.append(
                                    {
                                        "operation": operation,
                                        "denied": "The previous guided edit requires refreshed evidence or explicit drop_guidance before another modification.",
                                    }
                                )
                                continue
                            if selected:
                                modifying = ready_modifying_action(
                                    selected, current, args.get("action_id")
                                )
                                if modifying is None or relative not in declared_write_paths(
                                    modifying, current
                                ):
                                    observations.append(
                                        {
                                            "operation": operation,
                                            "denied": "Guided editing requires an actual ready Action and its bound write path; expected predecessor outputs are insufficient.",
                                        }
                                    )
                                    continue
                            if enforce_catalog_prerequisites:
                                modifying = ready_catalog_action(args.get("action_id"), current)
                                if modifying is None or relative not in declared_write_paths(
                                    modifying, current
                                ):
                                    observations.append(
                                        {
                                            "operation": operation,
                                            "denied": "The functional Action lacks actual current prerequisites, input ports or its bound write path.",
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
                            pending_guidance_refresh = selected is not None
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
                        modifying = (
                            ready_modifying_action(selected, current, args.get("action_id"))
                            if selected is not None
                            else None
                        )
                        catalog_modifying = ready_catalog_action(args.get("action_id"), current)
                        readonly = (
                            probe_only
                            or read_only_workspace
                            or pending_guidance_refresh
                            or (selected is not None and modifying is None)
                            or (enforce_catalog_prerequisites and catalog_modifying is None)
                        )

                        def invoke():
                            return tools.run(
                                args["argv"],
                                timeout=args.get("timeout", 60),
                                readonly_workspace=readonly,
                            )

                        allowed = None
                        if not readonly and (modifying or enforce_catalog_prerequisites):
                            allowed = declared_write_paths(modifying or catalog_modifying, current)
                            if enforce_catalog_prerequisites:
                                allowed &= declared_write_paths(catalog_modifying, current)
                        if allowed is not None:
                            self.ledger.charge(
                                "tool_calls", 1, "current Action command write-set audit"
                            )
                            result = run_scoped_command(current.root, allowed, invoke)
                            self.ledger.check_time()
                        else:
                            result = invoke()
                        result["workspace_execution_sha256"] = public_workspace_execution_sha256(
                            current.root
                        )
                        anchor_id = "current:probe:" + str(len(observations))
                        anchor = EvidenceAnchor(
                            anchor_id,
                            "probe",
                            json.dumps(bounded_public_view(result, text_limit=2000)),
                            current.base_commit,
                            exit_code=result["exit_code"],
                        )
                        current = replace(
                            current,
                            facts=tuple(
                                f for f in current.facts if f.key != "last_public_probe_passed"
                            ),
                        ).update(
                            anchors=(anchor,),
                            facts=(
                                ObservedFact(
                                    "last_public_probe_passed",
                                    result["exit_code"] == 0,
                                    (anchor_id,),
                                ),
                            )
                            if result.get("execution_available", True)
                            and result.get("exit_code") is not None
                            else (),
                        )
                    elif operation == "record_action_observation":
                        self.ledger.charge("tool_calls", 1, "witnessed Action output recording")
                        action = action_catalog.get(args["action_id"])
                        if action is None:
                            raise ValueError(
                                "Action observation was not delivered from an approved source"
                            )
                        try:
                            record = record_action_observation(
                                action,
                                args,
                                current,
                                broker_observations,
                                record_id="action-result:" + str(len(action_observations)),
                            )
                        except ValueError as exc:
                            result = {
                                "operation": operation,
                                "recorded": False,
                                "denied": str(exc),
                                "current_context_revision": current.revision,
                                "available_tool_observation_ids": sorted(broker_observations),
                            }
                        else:
                            action_observations.append(record)
                            result = {"operation": operation, "record": record}
                    elif operation == "drop_guidance":
                        self.ledger.charge(
                            "tool_calls", 1, "explicit fallback from conditional Skill guidance"
                        )
                        selected = None
                        pending_guidance_refresh = False
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
                        if anchor.kind in {"workspace_snapshot", "workspace_execution_snapshot"}:
                            workspace_hash = (
                                public_workspace_execution_sha256(current.root)
                                if anchor.kind == "workspace_execution_snapshot"
                                else public_workspace_sha256(current.root)
                            )
                            if workspace_hash != anchor.sha256:
                                changed_anchors.append(
                                    replace(
                                        anchor,
                                        sha256=workspace_hash,
                                        observation="Public workspace changed; reviewed Action outputs require renewed evidence.",
                                    )
                                )
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
                        pending_guidance_refresh = pending_guidance_refresh or selected is not None
                        current = current.update(anchors=tuple(changed_anchors))
                        selected = None
                        guidance = "Public tool changed current code; re-observe prerequisites and refresh guidance."
                    result["operation"] = operation
                    result["observation_id"] = "public:observation:" + str(len(observations))
                    result["context_revision"] = current.revision
                    if operation in {"read_file", "write_file", "run_public_command"}:
                        broker_observations[result["observation_id"]] = dict(result)
                    observations.append(result)
            except BudgetExceeded as exc:
                failed = str(exc)
            except (ValueError, RuntimeError, OSError, KeyError, TypeError) as exc:
                # Retain the attempted trajectory/denominator without exposing
                # native transport or container diagnostics to public output.
                failed = "solver or public-tool failure (" + type(exc).__name__ + ")"
            patch = patch_from_snapshot(baseline, Path(current.root))
            result = {
                "task_id": task.task_id,
                "arm": self.arm,
                "solver_ended": ended,
                "solver_terminated": True,
                "termination_reason": "finish" if ended else failed,
                "failure": failed,
                "base_commit": task.base_commit,
                "public_snapshot_sha256": initial_snapshot,
                "patch": patch,
                "patch_sha256": hashlib.sha256(patch.encode()).hexdigest(),
                "requests": requests,
                "public_observations": observations,
                "guidance_runs": guidance_runs,
                "action_observations": action_observations,
                "action_observations_semantically_verified": False,
                "action_output_reviews": action_output_reviews,
                "explicit_functional_action_catalog": bool(recordable_actions),
                "strict_functional_action_catalog": enforce_catalog_prerequisites,
                "public_workspace_read_only": read_only_workspace,
                "resumed_reviewed_public_state": resume_reviewed_state,
                "guidance_usage": guidance_usage,
                "candidate_generation_frozen": use_frozen_selection,
                "nominated_plan_id": initial_plan.id if initial_plan else None,
                "budget": self.ledger.snapshot(),
                "isolation": tools.isolation,
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


def hidden_evaluator_from_file(
    manifest_path, *, dependency_root=None, sandbox_backend="namespace-bind"
):
    """Defer reading private evaluation material until the solver has stopped."""

    def evaluate(task, patch):
        spec = json.loads(Path(manifest_path).read_text())
        if spec["task_id"] != task.task_id or spec["base_commit"] != task.base_commit:
            raise ValueError("independent evaluator identity mismatch")
        from .adaptive_budget import BudgetCaps, BudgetLedger

        with (
            tempfile.TemporaryDirectory(prefix="arex-hidden-evaluator-") as scratch,
            ExitStack() as cleanup,
        ):
            snapshot_base(task, Path(scratch) / "evaluation")
            work = Path(scratch) / "evaluation"
            tools = make_namespace_tools(
                work,
                BudgetLedger(BudgetCaps(tool_calls=100)),
                dependency_root,
                backend=sandbox_backend,
            )
            cleanup.callback(tools.close)
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
                "isolation": tools.isolation,
                "runtime_sha256": tools.runtime_sha256,
                "evaluator_version": spec["evaluator_version"],
                "evaluation_spec_sha256": digest(spec),
                "benchmark_exit_codes": [r["exit_code"] for r in benchmark],
                "regression_exit_codes": [r["exit_code"] for r in regression],
            }

    return evaluate
