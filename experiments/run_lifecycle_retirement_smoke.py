#!/usr/bin/env python3
"""Exercise quarantine -> soft retirement on a detached training skill."""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from arex_skill_graph.lifecycle import LifecycleManager, SkillRecord, SkillStatus
from arex_skill_graph.store import CatalogStore

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument("--db",type=Path,required=True); p.add_argument("--snapshot",type=Path,required=True); p.add_argument("--output",type=Path,required=True); p.add_argument("--hnsw",type=Path,required=True); args=p.parse_args()
 records=[SkillRecord.from_json(x) for x in json.loads(args.snapshot.read_text())]
 manager=LifecycleManager()
 for r in records: manager.skills[r.skill_id]=r
 candidates=[r for r in records if r.status is SkillStatus.ACTIVE and not r.parent_ids]
 if not candidates: raise RuntimeError("no detached active skill available for retirement smoke")
 target=sorted(candidates,key=lambda r:r.skill_id)[0]
 before=target.to_json()
 parent_ids=manager.quarantine(target.skill_id,"controlled retirement smoke: detached skill failed revalidation")
 manager.retire(target.skill_id)
 after=manager.get(target.skill_id).to_json()
 with CatalogStore(args.db) as store:
  store.initialize(); store.persist_lifecycle_manager(manager); store.build_hnsw_index(args.hnsw,embedding_kind="routing",model_version="hash-v1")
 evidence={"schema_version":"lifecycle-retirement-smoke-v1","skill_id":target.skill_id,"before_status":before["status"],"after_status":after["status"],"parent_ids":list(parent_ids),"before":before,"after":after,"hnsw_exists":args.hnsw.exists()}
 args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({k:evidence[k] for k in ("skill_id","before_status","after_status","hnsw_exists")},ensure_ascii=False)); return 0
if __name__=="__main__": raise SystemExit(main())
