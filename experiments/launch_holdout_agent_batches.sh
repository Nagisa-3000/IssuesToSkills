#!/usr/bin/env bash
set -u
: "${OPENAI_API_KEY:?OPENAI_API_KEY must be provided at runtime}"
ROOT=/home/chenyujia/arex-skill-graph
RUNTIME=/home/chenyujia/arex-holdout-runtime
PY=$RUNTIME/.venv/bin/python
CASES=$ROOT/data/skill-extraction/holdout-cases-20260928
DB=$RUNTIME/catalog.sqlite
HNSW=$RUNTIME/catalog.hnsw
CODEX_HOME=$ROOT/.codex-rvnpu
for n in 1 2 3 4; do
  out="$ROOT/data/skill-extraction/holdout-agent-eval-batch-${n}-20260928"
  rm -rf "$out"
  mkdir -p "$out"
  nohup env PYTHONPATH="$RUNTIME/src:$RUNTIME" "$PY" "$RUNTIME/run_cross_project_holdout_agent_eval.py" \
    --cases "$CASES/case-batch-${n}.json" \
    --cases-root "$CASES" \
    --db "$DB" \
    --output-dir "$out" \
    --workspace-root "/tmp/arex-agent-batch-${n}-20260928" \
    --hnsw "$HNSW" \
    --api-key "$OPENAI_API_KEY" \
    --base-url https://llm.rvnpu.cn/v1 \
    --model openai/gpt-5.6-sol \
    --codex-home "$CODEX_HOME" \
    > "$out/run.log" 2>&1 < /dev/null &
  echo "batch $n pid $!"
done


