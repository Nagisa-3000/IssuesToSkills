#!/usr/bin/env python3
"""Train a pinned local Transformer ranking head with historical development calibration."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.adaptive_cli import read_json
from arex_skill_graph.ranker_training import train_ranker


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset", type=Path, required=True)
    p.add_argument(
        "--model", type=Path, required=True, help="Pinned prepared local Transformer directory"
    )
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--learning-rate", type=float, default=0.01)
    p.add_argument("--seed", type=int, default=20261003)
    p.add_argument("--train-encoder", action="store_true")
    p.add_argument("--lora-rank", type=int, default=0)
    p.add_argument("--lora-target-module", action="append", default=[])
    a = p.parse_args(argv)
    metadata = train_ranker(
        read_json(a.dataset),
        a.model,
        a.output,
        epochs=a.epochs,
        learning_rate=a.learning_rate,
        seed=a.seed,
        train_encoder=a.train_encoder,
        lora_rank=a.lora_rank,
        lora_target_modules=a.lora_target_module,
    )
    print(
        f"Trained {metadata['training_pairs']} historical pairs; checkpoint {metadata['checkpoint_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
