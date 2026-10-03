"""Public, current-base observations used by planners and rankers."""

from __future__ import annotations

import ast
import hashlib
import re
import subprocess
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Mapping

from .action_contracts import CheckStatus, Port, Predicate, strict, strings, text, utc

FORBIDDEN_FIELDS = frozenset(
    {
        "gold_patch",
        "test_patch",
        "visible_test_patch",
        "hidden_test_patch",
        "gold",
        "solution_ref",
        "solution_commit",
        "solution_patch",
        "hidden_tests",
        "test_patch_path",
        "gold_derived_files",
        "gold_derived_commands",
        "gold_derived_problem_family",
    }
)


def assert_public(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key).lower().replace("-", "_") in FORBIDDEN_FIELDS:
                raise ValueError("evaluator-only input rejected")
            assert_public(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            assert_public(item)
    elif isinstance(value, str):
        from .direct_skill_extraction import safe_text

        if safe_text(value) != value:
            raise ValueError("credential-like input rejected; value suppressed")


@dataclass(frozen=True)
class EvidenceAnchor:
    id: str
    kind: str
    observation: str
    base_commit: str
    path: str = ""
    sha256: str = ""
    available_at: str = ""
    exit_code: int | None = None

    def __post_init__(self):
        text(self.id, "anchor ID")
        text(self.observation, "observation")
        if self.kind not in {
            "public_issue",
            "current_code",
            "reproduction",
            "public_test",
            "probe",
        }:
            raise ValueError("invalid public evidence kind")
        if not re.fullmatch(r"[0-9a-f]{40}", self.base_commit):
            raise ValueError("evidence requires current base commit")
        if self.path:
            from .action_contracts import contained_resource

            contained_resource(self.path)
            if not re.fullmatch(r"[0-9a-f]{64}", self.sha256):
                raise ValueError("code evidence requires content hash")
        if self.kind == "current_code" and not self.path:
            raise ValueError("current-code evidence needs a path")
        if self.available_at:
            utc(self.available_at)
        if self.exit_code is not None and (
            type(self.exit_code) is not int
            or self.kind not in {"probe", "reproduction", "public_test"}
        ):
            raise ValueError("only executed public observations can carry exit codes")

    @classmethod
    def from_dict(cls, value):
        return cls(**strict(value, cls))


@dataclass(frozen=True)
class ObservedFact:
    key: str
    value: str | bool
    evidence_refs: tuple[str, ...]

    def __post_init__(self):
        text(self.key, "observed fact key")
        if not isinstance(self.value, (str, bool)) or not self.evidence_refs:
            raise ValueError("observed fact requires a typed value and evidence")

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["evidence_refs"] = strings(d.get("evidence_refs", []))
        return cls(**d)


@dataclass(frozen=True)
class SemanticCheck:
    key: str
    status: CheckStatus
    rationale: str
    evidence_refs: tuple[str, ...]
    reviewer: str

    def __post_init__(self):
        object.__setattr__(self, "status", CheckStatus(self.status))
        text(self.key, "semantic check key")
        text(self.rationale, "semantic rationale")
        text(self.reviewer, "semantic reviewer")
        if self.status != CheckStatus.UNKNOWN and not self.evidence_refs:
            raise ValueError("semantic decisions require current evidence")

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["evidence_refs"] = strings(d.get("evidence_refs", []))
        return cls(**d)


@dataclass(frozen=True)
class Binding:
    role: str
    anchor_id: str
    symbol: str
    language: str
    interface: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self):
        for name in ("role", "anchor_id", "language", "interface"):
            text(getattr(self, name), "binding " + name)

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["evidence_refs"] = strings(d.get("evidence_refs", []))
        return cls(**d)


@dataclass(frozen=True)
class PortValue:
    port: Port
    evidence_refs: tuple[str, ...]

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["port"] = Port.from_dict(d["port"])
        d["evidence_refs"] = strings(d.get("evidence_refs", []))
        return cls(**d)


@dataclass(frozen=True)
class CurrentOracle:
    action_id: str
    source_oracle_id: str
    instruction: str
    command: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self):
        for name in ("action_id", "source_oracle_id", "instruction"):
            text(getattr(self, name), "current oracle " + name)
        if not self.command or not self.evidence_refs:
            raise ValueError("current oracle requires public argv and current evidence")
        strings(self.command)

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        for name in ("command", "evidence_refs"):
            d[name] = strings(d.get(name, []))
        return cls(**d)


@dataclass(frozen=True)
class TaskContext:
    task_id: str
    repository: str
    base_commit: str
    root: str
    public_problem: str
    input_available_at: str
    anchors: tuple[EvidenceAnchor, ...]
    facts: tuple[ObservedFact, ...] = ()
    checks: tuple[SemanticCheck, ...] = ()
    bindings: tuple[Binding, ...] = ()
    port_values: tuple[PortValue, ...] = ()
    goals: tuple[Predicate, ...] = ()
    environment: tuple[str, ...] = ()
    revision: int = 0
    oracles: tuple[CurrentOracle, ...] = ()

    def __post_init__(self):
        for key in ("task_id", "repository", "root", "public_problem"):
            text(getattr(self, key), key)
        if not re.fullmatch(r"[0-9a-f]{40}", self.base_commit):
            raise ValueError("task needs a pinned base SHA")
        utc(self.input_available_at)
        assert_public(self.to_dict())
        ids = {a.id for a in self.anchors}
        if not ids or len(ids) != len(self.anchors):
            raise ValueError("task needs unique public evidence anchors")
        if any(a.base_commit != self.base_commit for a in self.anchors):
            raise ValueError("evidence belongs to a different base")
        for collection, key in [(self.facts, "key"), (self.checks, "key"), (self.bindings, "role")]:
            if len({getattr(x, key) for x in collection}) != len(collection):
                raise ValueError("duplicate current fact/check/binding")
        for item in (*self.facts, *self.checks, *self.bindings, *self.port_values, *self.oracles):
            if not set(item.evidence_refs).issubset(ids):
                raise ValueError("current evidence reference is not closed")
            if (
                isinstance(item, (ObservedFact, Binding, PortValue, CurrentOracle))
                and not item.evidence_refs
            ):
                raise ValueError("observed state and binding require evidence")
        if len({v.port.name for v in self.port_values}) != len(self.port_values):
            raise ValueError("duplicate current port value")
        if len({(o.action_id, o.source_oracle_id) for o in self.oracles}) != len(self.oracles):
            raise ValueError("duplicate current oracle binding")
        if any(b.anchor_id not in ids for b in self.bindings):
            raise ValueError("binding anchor is missing")
        if any(not isinstance(f.value, (str, bool)) for f in self.facts):
            raise ValueError("invalid observed fact value")

    @classmethod
    def from_dict(cls, value):
        assert_public(value)
        d = strict(value, cls)
        for key, parser in [
            ("anchors", EvidenceAnchor),
            ("facts", ObservedFact),
            ("checks", SemanticCheck),
            ("bindings", Binding),
            ("port_values", PortValue),
            ("goals", Predicate),
            ("oracles", CurrentOracle),
        ]:
            d[key] = tuple(parser.from_dict(x) for x in d.get(key, []))
        d["environment"] = strings(d.get("environment", []))
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    def verify(self, *, verify_head: bool = True) -> None:
        root = Path(self.root).resolve()
        if not root.is_dir():
            raise ValueError("current checkout is unavailable")
        if verify_head:
            result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode or result.stdout.strip() != self.base_commit:
                raise ValueError("checkout HEAD differs from TaskContext base")
        for anchor in self.anchors:
            if anchor.path:
                candidate = root / anchor.path
                if (
                    candidate.is_symlink()
                    or not candidate.resolve().is_relative_to(root)
                    or not candidate.is_file()
                ):
                    raise ValueError("current evidence path is missing or escapes checkout")
                if hashlib.sha256(candidate.read_bytes()).hexdigest() != anchor.sha256:
                    raise ValueError(
                        "current evidence changed; refresh observations before replanning"
                    )
        for binding in self.bindings:
            anchor = next(a for a in self.anchors if a.id == binding.anchor_id)
            if not anchor.path:
                raise ValueError("binding requires current code evidence")
            source = (root / anchor.path).read_text(encoding="utf-8")
            extensions = {"Python": {".py", ".pyi"}, "Rust": {".rs"}}
            if (
                binding.language in extensions
                and Path(anchor.path).suffix not in extensions[binding.language]
            ):
                raise ValueError("bound language disagrees with current implementation file")
            if binding.language == "Python" and binding.symbol:
                qualified, bare = set(), set()

                def symbols(node, scope=()):
                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                            name = (*scope, child.name)
                            qualified.add(".".join(name))
                            bare.add(child.name)
                            symbols(child, name)
                        else:
                            symbols(child, scope)

                symbols(ast.parse(source))
                symbol = binding.symbol
                module = (
                    anchor.path.removesuffix(".py")
                    .removesuffix(".pyi")
                    .replace("/", ".")
                    .removeprefix("src.")
                )
                if symbol.startswith(module + "."):
                    symbol = symbol[len(module) + 1 :]
                if symbol not in qualified and symbol not in bare:
                    raise ValueError("bound Python symbol does not exist")
            elif binding.symbol and not re.search(
                r"\b" + re.escape(binding.symbol) + r"\b", source
            ):
                raise ValueError("bound symbol does not exist")
            # Existence is structural; the semantic owner check is separate.

    def condition(self, predicate: Predicate) -> CheckStatus:
        if predicate.evaluator == "evidence":
            fact = next((f for f in self.facts if f.key == predicate.key), None)
            if fact is None:
                return CheckStatus.UNKNOWN
            return CheckStatus.PASS if fact.value == predicate.value else CheckStatus.FAIL
        root = Path(self.root).resolve()
        key = predicate.key
        if key.startswith("role:"):
            binding = next((b for b in self.bindings if b.role == key.removeprefix("role:")), None)
            if binding is None:
                return CheckStatus.UNKNOWN
            if predicate.evaluator == "symbol_exists":
                return (
                    CheckStatus.PASS
                    if bool(binding.symbol) == predicate.value
                    else CheckStatus.FAIL
                )
            key = next(a.path for a in self.anchors if a.id == binding.anchor_id)
        path = root / key
        if not path.resolve().is_relative_to(root):
            return CheckStatus.FAIL
        if predicate.evaluator == "file_exists":
            exists = path.is_file()
            return CheckStatus.PASS if exists == predicate.value else CheckStatus.FAIL
        # Symbol predicates need a verified binding, not a regex semantic guess.
        bound = any(b.symbol == predicate.key for b in self.bindings)
        return CheckStatus.PASS if bound == predicate.value else CheckStatus.UNKNOWN

    def semantic(self, key: str) -> SemanticCheck:
        return next(
            (c for c in self.checks if c.key == key),
            SemanticCheck(
                key, CheckStatus.UNKNOWN, "Current evidence not yet established", (), "unreviewed"
            ),
        )

    def refined_query(self) -> str:
        return "\n".join(
            [
                self.public_problem,
                *(a.observation for a in self.anchors),
                *(f"{f.key}={f.value}" for f in self.facts),
            ]
        )

    def update(
        self, *, anchors=(), facts=(), checks=(), bindings=(), port_values=(), oracles=()
    ) -> TaskContext:
        def merged(old, new, key):
            values = {getattr(x, key): x for x in old}
            values.update({getattr(x, key): x for x in new})
            return tuple(values.values())

        old_anchors = {a.id: a for a in self.anchors}
        changed = {a.id for a in anchors if a.id in old_anchors and a != old_anchors[a.id]}

        def fresh(items):
            return tuple(x for x in items if not changed.intersection(x.evidence_refs))

        return replace(
            self,
            anchors=merged(self.anchors, anchors, "id"),
            facts=merged(fresh(self.facts), facts, "key"),
            checks=merged(fresh(self.checks), checks, "key"),
            bindings=merged(fresh(self.bindings), bindings, "role"),
            port_values=tuple(port_values) or fresh(self.port_values),
            oracles=tuple(oracles) or fresh(self.oracles),
            revision=self.revision + 1,
        )
