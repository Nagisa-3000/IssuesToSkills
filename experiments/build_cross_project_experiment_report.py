#!/usr/bin/env python3
"""Build a single auditable report from the cross-project holdout artifacts."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def read(path: Path, default: Any) -> Any:
    if not path.exists(): return default
    return json.loads(path.read_text(encoding="utf-8"))

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--split",type=Path,required=True); p.add_argument("--admission",type=Path,required=True); p.add_argument("--retrieval",type=Path,required=True); p.add_argument("--closed-loop",type=Path,required=True); p.add_argument("--retirement",type=Path,required=True); p.add_argument("--qualification",type=Path,required=True); p.add_argument("--agent-comparison",type=Path); p.add_argument("--output",type=Path,required=True); args=p.parse_args()
    split=read(args.split,{}); admission=read(args.admission,{}); retrieval=read(args.retrieval,{}); closed=read(args.closed_loop,{}); retirement=read(args.retirement,{}); qualification=read(args.qualification,{}); agent=read(args.agent_comparison,{}) if args.agent_comparison else {}
    report={"schema_version":"arex-cross-project-skill-graph-experiment-v1","generated_at":"2026-09-28","split":split,"training_graph":{"admission":admission,"retrieval":retrieval},"closed_loop":{"success_skill":closed.get("retrieval_and_use",{}).get("success",{}).get("selected_skill_id"),"failure_skill":closed.get("retrieval_and_use",{}).get("failure",{}).get("selected_skill_id"),"revision_id":closed.get("feedback",{}).get("revision_id"),"resulting_status":closed.get("feedback",{}).get("resulting_status"),"hnsw_after_feedback":closed.get("hnsw",{}).get("after_feedback",{}).get("available"),"llm_calls":len(closed.get("llm",{}).get("calls",[]))},"retirement":retirement,"qualification":qualification,"agent_comparison":agent}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({"output":str(args.output),"train_cases":split.get("train_cases"),"held_out_cases":split.get("held_out_cases"),"qualified":qualification.get("qualified"),"agent_rows":agent.get("rows")},ensure_ascii=False)); return 0
if __name__=="__main__": raise SystemExit(main())
