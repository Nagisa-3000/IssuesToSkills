#!/usr/bin/env bash
set -u
ROOT=/home/chenyujia/arex-skill-graph
PY=/home/chenyujia/.local/share/uv/python/cpython-3.12.13-linux-x86_64-gnu/bin/python3.12
CASES=$ROOT/data/skill-extraction/holdout-cases-20260928
mkdir -p "$ROOT/data/skill-extraction/holdout-qualification-20260928"
for n in 1 2 3 4; do
  out="$ROOT/data/skill-extraction/holdout-qualification-20260928/batch-${n}"
  if [ -f "$out/qualification-report.json" ]; then echo "batch $n already done"; continue; fi
  mkdir -p "$out"
  nohup "$PY" "$ROOT/experiments/qualify_cross_project_holdout_cases.py" \
    --cases "$CASES/case-batch-${n}.json" \
    --cases-root "$CASES" \
    --output-dir "$out" \
    --workspace-root "/tmp/arex-qualification-${n}-20260928" \
    > "$out/run.log" 2>&1 < /dev/null &
  echo "batch $n pid $!"
done
