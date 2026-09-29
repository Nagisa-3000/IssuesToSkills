#!/usr/bin/env bash
set -u
ROOT=/home/chenyujia/arex-skill-graph
export CODEX_HOME="$ROOT/.codex-rvnpu"
export GITHUB_OFFLINE_FALLBACK=1
mkdir -p "$CODEX_HOME" "$ROOT/data/skill-extraction/codex-runs"
for n in 1 2 3 4; do
  manifest="$ROOT/experiments/manifests/cross-project-common-80-deepseek-holdout/train-batch-${n}.json"
  out="$ROOT/data/skill-extraction/codex-runs/holdout-train-batch-${n}-20260928-retry3"
  if [ -f "$out/extraction-summary.json" ]; then
    echo "batch ${n}: already has summary, skipping"
    continue
  fi
  mkdir -p "$out"
  nohup python3 "$ROOT/experiments/run_codex_issue_episode_extraction_holdout.py" \
    --manifest "$manifest" \
    --output "$out" \
    --codex /usr/local/bin/codex \
    --max-cases 20 \
    --max-linked-prs 0 \
    > "$out/run.log" 2>&1 < /dev/null &
  pid=$!
  printf '%s\n' "$pid" > "$out/pid"
  echo "batch ${n}: pid ${pid}"
done
