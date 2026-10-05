
import pathlib,json,sys,os,time,dataclasses
p=pathlib.Path("/home/chenyujia/tritonToLlvm/arex-skill-graph");sys.path.insert(0,str(p/"src"))
from arex_skill_graph.original_query_evaluator import original_query_evaluator,load_original_replay_authority
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.temporal_ranker_data import HistoricalQuery,execution_label_from_run
from arex_skill_graph.pattern_contracts import load_native_package
from arex_skill_graph.action_contracts import TemporalPolicy
from arex_skill_graph.historical_isolation import HistoricalIsolation
from arex_skill_graph.historical_replay_controls import replay_task_identity
from arex_skill_graph.history_census import fingerprint,write_json,redact_history
from arex_skill_graph.adaptive_cli import new_ledger
from arex_skill_graph.adaptive_guidance import index_native_package
from arex_skill_graph.adaptive_runner import AdaptiveSolver
from arex_skill_graph.workflow_ranker import WorkflowRanker
from arex_skill_graph.workflow_rewriter import bind_selection
from arex_skill_graph.plan_validation import ResourcePolicy,validate_task_plan
from arex_skill_graph.store import CatalogStore
from arex_skill_graph.llm_http import OpenAICompatibleConfig,OpenAICompatibleTransport
key=json.loads(sys.stdin.read())["api_key"]
d=pathlib.Path(sys.argv[1])
queries=json.loads((p/"tmp/pre2021-public-branch-source-gap-recovery-preparation-v1-20261006/results/queries.json").read_text())
raw=next(q for q in queries if q["task"]["task_id"]=="PyCQA/pyflakes:470")
task=TaskContext.from_dict(raw["task"])
query=HistoricalQuery(task,raw["bug_cluster_id"],raw["fix_id"],tuple(raw.get("aliases",())),tuple(raw.get("copied_from",())),raw.get("exposed",False))
os.environ["GIT_CONFIG_COUNT"]="1";os.environ["GIT_CONFIG_KEY_0"]="safe.directory";os.environ["GIT_CONFIG_VALUE_0"]=task.root
inv=json.loads((p/"tmp/qualified-cross-project-native-corpus-v3-20261006/qualification-inventory.json").read_text())
native=next(x for x in inv["results"] if x.get("verified_resolution") and x["issue_id"]==task.task_id)
verification=pathlib.Path(native["verification_path"])
controls=p/"tmp/pre2021-targeted-public-git-replay-controls-preparation-v1-20261006/results/cases/PyCQA__pyflakes-470"
review=p/"tmp/pyflakes-470-original-replay-independent-review-v1-20261006/review.json"
runtime=pathlib.Path(json.loads((p/"tmp/pre2021-input-compatible-runtime-map-preparation-v1-20261006/runtime-map.json").read_text())[task.task_id])
authority=load_original_replay_authority(task,verification,controls,review)
assert authority.independently_reviewed
control_done=json.loads((p/"tmp/pyflakes-470-original-query-evaluator-controls-v1-20261006/completion.json").read_text())
assert control_done["private_evaluator_controls_passed"] is True
pair_dir=p/"tmp/pyflakes-434-470-causal-cluster-independent-review-v1-20261006"
pair=json.loads((pair_dir/"review-response.json").read_text())
assert not pair["duplicate_groups"] and not pair["uncertain_groups"]
iso_path=p/"analysis/isolation/historical-causal-isolation-20261006-v2.json"
if not iso_path.exists():iso_path=p/"analysis/isolation/historical-causal-isolation-20261006-v1.json"
iso=HistoricalIsolation.load(iso_path)
policy=TemporalPolicy(task.input_available_at,*iso.query_exclusions(query))
refs=json.loads((p/"tmp/qualified-cross-project-native-corpus-v3-20261006/references.json").read_text())
ref=next(x for x in refs if any(s.startswith("PyCQA/pyflakes:434:repair:") for s in x["source_episode_ids"]))
package=load_native_package(ref,policy);iso.verify_sources(package.sources)
workflow=package.workflows[0]
plan=bind_selection(task,None,workflow.actions,(workflow,))
resources=ResourcePolicy(policy,(ref,));initial_report=validate_task_plan(plan,task,resources)
identity={"schema":"original-input-single-workflow-paired-pilot-v1","query":replay_task_identity(task),"candidate_reference":ref,"candidate_workflow_id":workflow.id,"candidate_sources_before_query":True,"causal_isolation_sha256":iso.sha256,"additional_pair_causal_review_sha256":fingerprint(json.loads((pair_dir/"cluster-review.json").read_text())),"initial_plan":plan.to_dict(),"initial_validation":initial_report.to_dict(),"branch_order":["B0","E1"],"arm_definitions":{"B0":"same solver without historical guidance","E1":"single historical Workflow with public binding/probes and normal adaptation or refusal"},"same_public_problem_and_original_source":True,"same_runtime_sha256":authority.completion["runtime_sha256"],"same_model":"openai/gpt-6.1-sol","same_model_endpoint":"https://llm.rvnpu.cn/v1","same_budget_caps":dataclasses.asdict(new_ledger().caps),"evaluator_only_artifacts_reach_actor":False,"source_and_historical_workflow_mutated":False,"registered_population":21,"available_public_queries":18,"pilot_queries":1,"formal_SWE_runs":0,"does_not_complete_M4_M6":True}
write_json(d/"study-identity.json",identity)
manifest_before=(pathlib.Path(ref["package_path"])/"manifest.json").read_bytes()
results=[];start=time.monotonic();all_calls=0
for arm in ("B0","E1"):
 branch=d/arm;branch.mkdir()
 if arm=="E1" and initial_report.status=="FAIL":
  row={"arm":arm,"status":"hard_rejected_unrun","report":initial_report.to_dict(),"failure_label_created":False};results.append(row);write_json(branch/"run.json",row);continue
 tr=OpenAICompatibleTransport(OpenAICompatibleConfig(key,"https://llm.rvnpu.cn/v1","openai/gpt-6.1-sol",timeout_seconds=900,max_output_tokens=12000,retries=0,stream_responses=True))
 ledger=new_ledger(tokenizer="cl100k_base")
 with CatalogStore(branch/"catalog.sqlite") as store:
  store.initialize()
  if arm=="E1":index_native_package(store,ref,policy)
  branch_resources=resources if arm=="E1" else ResourcePolicy(policy,())
  result=AdaptiveSolver(tr,WorkflowRanker(tr,model="openai/gpt-6.1-sol"),store,branch_resources,ledger,arm=arm,dependency_root=runtime,sandbox_backend="namespace-copy").run(
   task,evaluator=original_query_evaluator(verification,runtime,controls,independent_review_path=review),
   use_frozen_selection=True,initial_plan=plan if arm=="E1" else None)
 row={"query_id":task.task_id,"arm":arm,"status":"executed","run":result,"live_calls":tr.calls,"label":None,"formal_SWE_run":False}
 if arm=="E1" and result.get("solver_terminated") and result.get("evaluation",{}).get("evaluation_completed") is True and result.get("evaluation",{}).get("causal_controls_passed") is True:
  try:
   label=execution_label_from_run(query,workflow.id,"workflow",result,sampling_probability=1.0)
   row["label"]=dataclasses.asdict(dataclasses.replace(label,operational_mode=initial_report.mode))
  except ValueError as e:row["supervision_exclusion_reason"]=str(e)
 write_json(branch/"run.json",row);results.append(row);all_calls+=len(tr.calls)
 write_json(d/"progress.json",{"status":"running","completed_arms":len(results),"results":[{"arm":r["arm"],"resolved":r.get("run",{}).get("benchmark_resolved"),"solver_terminated":r.get("run",{}).get("solver_terminated"),"label_created":bool(r.get("label"))} for r in results],"actual_model_calls":all_calls,"elapsed_seconds":time.monotonic()-start,"formal_SWE_runs":0})
 print(json.dumps({"arm":arm,"solver_terminated":result.get("solver_terminated"),"resolved":result.get("benchmark_resolved"),"actual_model_calls":len(tr.calls),"label_created":bool(row.get("label"))}),flush=True)
 if any(c.get("successful") is False for c in tr.calls):break
assert (pathlib.Path(ref["package_path"])/"manifest.json").read_bytes()==manifest_before
authority.verify_unchanged(task)
write_json(d/"completion.json",{"schema":identity["schema"],"status":"terminal","completed_arms":len(results),"results":[{"arm":r["arm"],"status":r["status"],"solver_terminated":r.get("run",{}).get("solver_terminated"),"resolved":r.get("run",{}).get("benchmark_resolved"),"evaluation_completed":r.get("run",{}).get("evaluation",{}).get("evaluation_completed"),"utility_label_created":bool(r.get("label")),"failure_reason":r.get("run",{}).get("failure_reason")} for r in results],"actual_model_calls":all_calls,"all_actual_calls_serial":True,"elapsed_seconds":time.monotonic()-start,"utility_labels_created":sum(bool(r.get("label")) for r in results),"formal_SWE_runs":0,"independent_transfer_benefit_demonstrated":False,"goal_complete":False})
print(json.dumps({"status":"terminal","completed_arms":len(results),"actual_model_calls":all_calls,"formal_SWE_runs":0}))
