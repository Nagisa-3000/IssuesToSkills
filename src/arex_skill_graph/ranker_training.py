"""Historical pairwise training of a local language-model scoring head/encoder."""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from .action_contracts import digest
from .embeddings import TransformerEncoder
from .temporal_ranker_data import TrainingExample, pair_preferences, validate_training_snapshot
from .workflow_ranker import CRITERIA


def scoring_text(task_input, candidate):
    # Identity/hash/paths are provenance, not model features that can memorize answers.
    current = {
        "problem": task_input["public_problem"],
        "observations": [a["observation"] for a in task_input.get("anchors", [])],
        "facts": [{"key": f["key"], "value": f["value"]} for f in task_input.get("facts", [])],
        "semantic_reviews": [
            {"kind": c["key"].split(":")[0], "status": c["status"], "rationale": c["rationale"]}
            for c in task_input.get("checks", [])
        ],
        "bindings": [
            {"role": b["role"], "language": b["language"], "interface": b["interface"]}
            for b in task_input.get("bindings", [])
        ],
        "environment": task_input.get("environment", []),
    }
    history = {
        k: candidate[k]
        for k in (
            "candidate_kind",
            "summary",
            "mechanism",
            "conditions",
            "exclusions",
            "action_roles",
            "costs",
            "validation_summary",
        )
    }
    return json.dumps(
        {"current": current, "candidate": history}, ensure_ascii=False, sort_keys=True
    )


def calibration_utility(labels):
    """Aggregate controlled replicates; probe permission is separate from repair utility."""
    executions = [label for label in labels if label["label_source"] == "execution"]
    if executions:
        return sum(
            bool(label["outcome"] and label["regression_pass"]) for label in executions
        ) / len(executions)
    return sum(label["applicability"] == "adaptively_usable" for label in labels) / len(labels)


def paired_scoring_tensors(encoder, texts, *, gradients=False):
    queries, candidates = [], []
    for text in texts:
        value = json.loads(text)
        current, history = value["current"], value["candidate"]
        queries.append(
            json.dumps({"problem": current.pop("problem"), **current}, ensure_ascii=False)
        )
        candidates.append(
            json.dumps(
                {
                    "mechanism": history.pop("mechanism"),
                    "summary": history.pop("summary"),
                    **history,
                },
                ensure_ascii=False,
            )
        )
    return encoder.tensors(queries, text_pairs=candidates, gradients=gradients)


def train_ranker(
    payload,
    model_path,
    output_dir,
    *,
    epochs=20,
    learning_rate=0.01,
    seed=20261003,
    train_encoder=False,
    lora_rank=0,
    lora_target_modules=(),
):
    validate_training_snapshot(payload)
    if epochs <= 0 or learning_rate <= 0:
        raise ValueError("invalid training hyperparameters")
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("install the ranker optional dependencies") from exc
    random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    encoder = TransformerEncoder(str(model_path))
    if lora_rank:
        try:
            from peft import LoraConfig, TaskType, get_peft_model
        except ImportError as exc:
            raise RuntimeError(
                "LoRA requested but peft is not installed; prompted mode remains available"
            ) from exc
        if lora_rank < 1 or not lora_target_modules:
            raise ValueError("LoRA requires positive rank and explicit architecture target modules")
        encoder.model = get_peft_model(
            encoder.model,
            LoraConfig(
                r=lora_rank,
                lora_alpha=2 * lora_rank,
                target_modules=list(lora_target_modules),
                task_type=TaskType.FEATURE_EXTRACTION,
            ),
        )
        train_encoder = True
    if not train_encoder:
        for p in encoder.model.parameters():
            p.requires_grad_(False)
    head = torch.nn.Linear(encoder.dimensions, 4)
    params = list(head.parameters()) + (
        [p for p in encoder.model.parameters() if p.requires_grad] if train_encoder else []
    )
    optimizer = torch.optim.AdamW(params, lr=learning_rate)
    examples = [TrainingExample(**r) for r in payload["examples"]]
    training = [r for r in examples if r.split == "train"]
    development = [r for r in examples if r.split == "development"]
    if not training or not development:
        raise ValueError("training requires a separate historical development population")
    pairs = [p for p in pair_preferences(examples) if p["split"] == "train"]
    if not pairs:
        raise ValueError("verified within-query pairs are required")
    # One candidate feature per query; replicate outcomes supervise aggregate preferences.
    rows = {(r.query_id, r.candidate["id"]): r for r in training}
    keys = sorted(rows)
    key_index = {key: i for i, key in enumerate(keys)}
    texts = [scoring_text(rows[key].task_input, rows[key].candidate) for key in keys]
    labels = {"unrelated": 0, "probe_only": 1, "adaptively_usable": 2}
    y = torch.tensor([labels[rows[key].label["applicability"]] for key in keys])
    losses = []
    cached, cached_tokens = (
        paired_scoring_tensors(encoder, texts) if not train_encoder else (None, 0)
    )
    tokens_processed = cached_tokens
    for _ in range(epochs):
        encoder.model.train(train_encoder)
        features, tokens = (
            paired_scoring_tensors(encoder, texts, gradients=True) if train_encoder else (cached, 0)
        )
        tokens_processed += tokens
        scores = head(features)
        pair_losses = []
        for pair in pairs:
            left = key_index[(pair["query_id"], pair["left"])]
            right = key_index[(pair["query_id"], pair["right"])]
            target = torch.tensor(pair["target"], dtype=scores.dtype)
            # Tie target=0.5 is retained; inverse-propensity weight is bounded.
            weight = min(10.0, 1.0 / min(pair["sampling_probabilities"]))
            pair_losses.append(
                weight
                * torch.nn.functional.binary_cross_entropy_with_logits(
                    scores[left, 0] - scores[right, 0], target
                )
            )
        loss = torch.stack(pair_losses).mean() + 0.25 * torch.nn.functional.cross_entropy(
            scores[:, 1:], y
        )
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    encoder.model.eval()
    head.eval()
    dev_rows = {(r.query_id, r.candidate["id"]): r for r in development}
    dev_keys = sorted(dev_rows)
    dev_features, dev_tokens = paired_scoring_tensors(
        encoder, [scoring_text(dev_rows[k].task_input, dev_rows[k].candidate) for k in dev_keys]
    )
    tokens_processed += dev_tokens
    with torch.no_grad():
        predictions = head(dev_features)
    dev_y = torch.tensor([labels[dev_rows[k].label["applicability"]] for k in dev_keys])
    temperatures = [0.5, 1.0, 2.0, 4.0]
    temperature = min(
        temperatures,
        key=lambda t: float(torch.nn.functional.cross_entropy(predictions[:, 1:] / t, dev_y)),
    )
    values = sorted({float(s) for s in predictions[:, 0]})
    thresholds = [values[0] - 1, *values, values[-1] + 1]
    dev_utilities = torch.tensor(
        [
            calibration_utility(
                [row.label for row in development if (row.query_id, row.candidate["id"]) == key]
            )
            for key in dev_keys
        ]
    )

    # Calibrate rejection on development evidence only, separately from score ordering.
    def rejection_loss(threshold):
        accepted = predictions[:, 0] >= threshold
        return float((2 * accepted * (1 - dev_utilities) + (~accepted) * dev_utilities).sum())

    threshold = min(thresholds, key=lambda t: (rejection_loss(t), -t))
    output = Path(output_dir).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError("checkpoint output exists; never overwrite a frozen model")
    output.mkdir(parents=True, exist_ok=True)
    model_root = output / "base-model"
    if lora_rank:
        # Persist a standalone merged backbone, not an uncontrolled remote dependency.
        encoder.model = encoder.model.merge_and_unload()
    encoder.model.save_pretrained(model_root, safe_serialization=True)
    encoder.tokenizer.save_pretrained(model_root)
    torch.save(head.state_dict(), output / "head.pt")
    encoder_copy = TransformerEncoder(str(model_root))
    metadata = {
        "schema": "historical-language-workflow-ranker-v1",
        "dataset_sha256": payload["dataset_sha256"],
        "training_cutoff": payload["training_cutoff"],
        "main_cutoff": payload["main_cutoff"],
        "base_encoder": encoder_copy.descriptor(),
        "base_encoder_source_version": encoder.model_version,
        "head_sha256": hashlib.sha256((output / "head.pt").read_bytes()).hexdigest(),
        "epochs": epochs,
        "learning_rate": learning_rate,
        "seed": seed,
        "train_encoder": train_encoder,
        "lora_rank": lora_rank,
        "lora_target_modules": list(lora_target_modules),
        "loss_history": losses,
        "training_pairs": len(pairs),
        "training_queries": len({r.query_id for r in training}),
        "development_queries": len({r.query_id for r in development}),
        "use_threshold": threshold,
        "temperature": temperature,
        "rejection_calibration": "aggregate independent execution utility; reviewed full applicability only when execution is absent",
        "development_execution_candidates": sum(
            any(
                row.label["label_source"] == "execution"
                for row in development
                if (row.query_id, row.candidate["id"]) == key
            )
            for key in dev_keys
        ),
        "tokens_processed": tokens_processed,
        "input_encoding": "paired-query-candidate-longest-first-v1",
        "training_non_tie_pairs": sum(pair["target"] != 0.5 for pair in pairs),
        "objective": "verified within-query pairwise preferences with tie targets plus graded applicability",
        "repair_effectiveness_proven": False,
    }
    # Absolute paths are convenience only; reload resolves the self-contained base-model directory.
    metadata["base_encoder"]["model_path"] = "base-model"
    metadata["checkpoint_sha256"] = digest(metadata)
    (output / "ranker.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    return metadata


class TrainedRankerScorer:
    def __init__(self, checkpoint):
        import torch

        root = Path(checkpoint).resolve()
        metadata = json.loads((root / "ranker.json").read_text())
        if metadata.get("schema") != "historical-language-workflow-ranker-v1":
            raise ValueError("unsupported trained ranker checkpoint")
        if metadata["checkpoint_sha256"] != digest(
            {k: v for k, v in metadata.items() if k != "checkpoint_sha256"}
        ):
            raise ValueError("ranker metadata changed")
        if hashlib.sha256((root / "head.pt").read_bytes()).hexdigest() != metadata["head_sha256"]:
            raise ValueError("ranker weights changed")
        self.encoder = TransformerEncoder(str(root / "base-model"))
        if self.encoder.model_version != metadata["base_encoder"]["model_version"]:
            raise ValueError("ranker encoder inventory changed")
        self.head = torch.nn.Linear(self.encoder.dimensions, 4)
        self.head.load_state_dict(
            torch.load(root / "head.pt", map_location="cpu", weights_only=True)
        )
        self.head.eval()
        self.metadata, self.torch = metadata, torch
        self.model_version = "trained-ranker:" + metadata["checkpoint_sha256"]

    def evaluate(self, task, capsules, budget):
        budget.charge("model_calls", 1, "trained language-ranker batch")
        texts = [scoring_text(task.to_dict(), c.to_dict()) for c in capsules]
        pooled, tokens = (
            paired_scoring_tensors(self.encoder, texts)
            if self.metadata.get("input_encoding") == "paired-query-candidate-longest-first-v1"
            else self.encoder.tensors(texts)
        )
        budget.charge(
            "model_tokens", tokens + 4 * len(capsules), "trained ranker encoded inputs and scores"
        )
        with self.torch.no_grad():
            outputs = self.head(pooled)
            probabilities = self.torch.softmax(outputs[:, 1:] / self.metadata["temperature"], dim=1)
        rows = []
        for capsule, values, probs in zip(capsules, outputs.tolist(), probabilities.tolist()):
            grade = max(range(3), key=lambda k: probs[k])
            mode = (
                "reject"
                if grade == 0 or values[0] < self.metadata["use_threshold"]
                else "probe_only"
                if capsule.hard_mode == "probe_only" or grade == 1
                else "use"
            )
            refs = [a.id for a in task.anchors]
            criteria = {
                criterion: {
                    "rationale": "Learned prediction; current evidence and independent contract gates remain authoritative.",
                    "evidence_refs": refs,
                }
                for criterion in CRITERIA
            }
            rows.append(
                {
                    "id": capsule.id,
                    "mode": mode,
                    "utility": values[0],
                    "uncertainty": 1 - max(probs),
                    "criteria_evidence": criteria,
                    "unmet_preconditions": list(capsule.conditions) if mode == "probe_only" else [],
                    "rationale": "Historical supervised ranker prediction with current hard-mode restriction.",
                }
            )
        return {"evaluations": rows}
