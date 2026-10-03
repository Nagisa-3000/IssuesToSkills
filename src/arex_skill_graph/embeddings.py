"""One versioned encoder for both catalog construction and query encoding."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from .text import hash_embedding, normalize


class HashEncoder:
    model_version = "hash-v1"
    dimensions = 256

    def encode(self, texts):
        return [hash_embedding(text) for text in texts]

    def descriptor(self):
        return {
            "kind": "feature-hash",
            "model_version": self.model_version,
            "dimensions": self.dimensions,
        }


class TransformerEncoder:
    """Pinned local transformer with attention-masked mean pooling; no remote code."""

    def __init__(self, model_path: str, *, max_length=512, local_files_only=True):
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "transformer encoder requires the ranker optional dependencies"
            ) from exc
        root = Path(model_path).resolve()
        if not root.is_dir():
            raise ValueError("use a prepared pinned local model directory")
        inventory = {
            p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*")
            if p.is_file()
        }
        self.fingerprint = hashlib.sha256(
            json.dumps(inventory, sort_keys=True).encode()
        ).hexdigest()
        self.model_version = (
            "transformer-mean-v1:" + self.fingerprint + ":length-" + str(max_length)
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            root, local_files_only=local_files_only, trust_remote_code=False
        )
        self.model = AutoModel.from_pretrained(
            root, local_files_only=local_files_only, trust_remote_code=False
        ).eval()
        self.dimensions = int(self.model.config.hidden_size)
        self.max_length, self.torch = max_length, torch
        self.path = str(root)
        self.calls = 0
        self.tokens_processed = 0

    def tensors(self, texts, *, gradients=False, text_pairs=None):
        texts = list(texts)
        pairs = list(text_pairs) if text_pairs is not None else None
        if pairs is not None and len(pairs) != len(texts):
            raise ValueError("paired encoder inputs need matching cardinality")
        batch = self.tokenizer(
            texts,
            text_pair=pairs,
            return_tensors="pt",
            padding=True,
            truncation="longest_first" if pairs is not None else True,
            max_length=self.max_length,
        )
        context = self.torch.enable_grad() if gradients else self.torch.no_grad()
        with context:
            hidden = self.model(**batch).last_hidden_state
            mask = batch["attention_mask"].unsqueeze(-1)
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp_min(1)
        tokens = int(batch["attention_mask"].sum().item())
        self.calls += 1
        self.tokens_processed += tokens
        return pooled, tokens

    def encode(self, texts):
        pooled, _ = self.tensors(texts)
        return [normalize(row) for row in pooled.detach().cpu().tolist()]

    def descriptor(self):
        return {
            "kind": "local-transformer-mean",
            "model_version": self.model_version,
            "dimensions": self.dimensions,
            "model_path": self.path,
            "max_length": self.max_length,
            "model_inventory_sha256": self.fingerprint,
        }


def validate_vectors(vectors, count, dimensions):
    if len(vectors) != count or any(len(v) != dimensions for v in vectors):
        raise ValueError("encoder vector count/dimensions mismatch")
    if any(not math.isfinite(float(x)) for v in vectors for x in v):
        raise ValueError("encoder returned nonfinite vectors")


def semantic_encoder_descriptor(encoder):
    return {key: value for key, value in encoder.descriptor().items() if key != "model_path"}
