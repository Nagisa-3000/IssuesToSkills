#!/usr/bin/env python3
"""Merge paired no-skill/guided agent-run artifacts and qualification gates."""
from __future__ import annotations
import argparse, json, statistics
from pathlib import Path
from typing import Any

def load_rows(root: Path) -> list[dict[str, Any]]:
    rows=[]
    for path in root.glob("**/runs/**/result.json"):
        try:
            row=json.loads(path.read_text(encoding="utf-8"))
            case_dir=path.parent.parent
            guidance_path=case_dir/"guided"/"guidance.json"
            guidance=json.loads(guidance_path.read_text(encoding="utf-8")) if guidance_path.exists() else {}
            calls=guidance.get("transport_calls",[]) if isinstance(guidance,dict) else []
            row["retrieval_judge_calls"]=len(calls)
            row["retrieval_judge_input_tokens"]=sum(int((c.get("usage") or {}).get("prompt_tokens",(c.get("usage") or {}).get("input_tokens",0)) or 0) for c in calls if isinstance(c,dict))
            row["retrieval_judge_output_tokens"]=sum(int((c.get("usage") or {}).get("completion_tokens",(c.get("usage") or {}).get("output_tokens",0)) or 0) for c in calls if isinstance(c,dict))
            rows.append(row)
        except (json.JSONDecodeError,OSError): pass
    return rows

def load_qualification(paths: list[Path]) -> dict[str, dict[str, Any]]:
    result={}
    for path in paths:
        if not path.exists(): continue
        value=json.loads(path.read_text(encoding="utf-8"))
        for row in value.get("rows",[]): result[str(row["case_id"])]=row
    return result

def mean(items, key):
    vals=[float(item.get(key,0) or 0) for item in items]
    return statistics.mean(vals) if vals else 0.0

def arm_stats(rows):
    out={}
    for arm in ("no_skill","guided"):
        items=[r for r in rows if r.get("arm")==arm]
        out[arm]={
            "runs":len(items),"test_successes":sum(bool(r.get("test_success")) for r in items),
            "raw_test_successes":sum(bool(r.get("raw_test_success")) for r in items),
            "test_success_rate":sum(bool(r.get("test_success")) for r in items)/len(items) if items else 0,
            "agent_success_rate":sum(bool(r.get("agent_success")) for r in items)/len(items) if items else 0,
            "timeouts":sum(bool(r.get("agent",{}).get("timed_out")) for r in items),
            "mean_wall_seconds":mean(items,"total_wall_seconds"),
            "mean_input_tokens":mean([{"v":r.get("usage",{}).get("input_tokens",0)} for r in items],"v"),
            "mean_cached_input_tokens":mean([{"v":r.get("usage",{}).get("cached_input_tokens",0)} for r in items],"v"),
            "mean_output_tokens":mean([{"v":r.get("usage",{}).get("output_tokens",0)} for r in items],"v"),
            "mean_reasoning_output_tokens":mean([{"v":r.get("usage",{}).get("reasoning_output_tokens",0)} for r in items],"v"),
            "total_input_tokens":sum(int(r.get("usage",{}).get("input_tokens",0) or 0) for r in items),
            "total_output_tokens":sum(int(r.get("usage",{}).get("output_tokens",0) or 0) for r in items),
            "retrieval_judge_calls":sum(int(r.get("retrieval_judge_calls",0) or 0) for r in items),
            "retrieval_judge_input_tokens":sum(int(r.get("retrieval_judge_input_tokens",0) or 0) for r in items),
            "retrieval_judge_output_tokens":sum(int(r.get("retrieval_judge_output_tokens",0) or 0) for r in items),
            "prompt_estimated_tokens_mean":mean(items,"prompt_estimated_tokens"),
        }
    return out

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path); p.add_argument("--run-dir",type=Path,action="append",default=[]); p.add_argument("--qualification",type=Path,action="append",default=[]); p.add_argument("--output",type=Path,required=True); args=p.parse_args()
    run_dirs=args.run_dir or ([args.root] if args.root else [])
    if not run_dirs: raise SystemExit("--root or --run-dir is required")
    rows=[]
    for run_dir in run_dirs: rows.extend(load_rows(run_dir))
    q=load_qualification(args.qualification)
    paired={}
    for row in rows: paired.setdefault(str(row["case_id"]),{})[str(row["arm"])]=row
    pairs=[]
    for case_id,arms in sorted(paired.items()):
        b=arms.get("no_skill"); g=arms.get("guided"); qual=q.get(case_id,{})
        if b and g:
            pairs.append({"case_id":case_id,"qualified":bool(qual.get("qualified",False)),"oracle_unqualified":case_id in q and not bool(qual.get("qualified",False)),"no_skill":b,"guided":g,"guided_minus_baseline_test":int(bool(g.get("test_success")))-int(bool(b.get("test_success"))),"guided_minus_baseline_input_tokens":int(g.get("usage",{}).get("input_tokens",0))-int(b.get("usage",{}).get("input_tokens",0)),"guided_minus_baseline_wall_seconds":float(g.get("total_wall_seconds",0))-float(b.get("total_wall_seconds",0))})
    strict=[x for x in pairs if x["qualified"]]
    def pair_stats(items):
        return {"cases":len(items),"baseline_successes":sum(bool(x["no_skill"].get("test_success")) for x in items),"guided_successes":sum(bool(x["guided"].get("test_success")) for x in items),"guided_wins":sum(x["guided_minus_baseline_test"]>0 for x in items),"baseline_wins":sum(x["guided_minus_baseline_test"]<0 for x in items),"ties":sum(x["guided_minus_baseline_test"]==0 for x in items),"mean_guided_minus_baseline_input_tokens":statistics.mean(x["guided_minus_baseline_input_tokens"] for x in items) if items else 0,"mean_guided_minus_baseline_wall_seconds":statistics.mean(x["guided_minus_baseline_wall_seconds"] for x in items) if items else 0}
    report={"schema_version":"cross-project-guided-agent-comparison-v1","rows":len(rows),"paired_cases":len(pairs),"strict_qualified_cases":len(strict),"oracle_unqualified_cases":len(pairs)-len(strict),"arm_stats":arm_stats(rows),"paired_all":pair_stats(pairs),"paired_strict":pair_stats(strict),"leakage": {"solution_ref_prompt_violations":sum(bool(r.get("solution_ref_in_prompt")) for r in rows),"test_edit_violations":sum(bool(r.get("test_edit_violation")) for r in rows)},"pairs":pairs}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps({k:report[k] for k in ("rows","paired_cases","strict_qualified_cases","oracle_unqualified_cases","arm_stats","paired_strict","leakage")},ensure_ascii=False)); return 0
if __name__=="__main__": raise SystemExit(main())
