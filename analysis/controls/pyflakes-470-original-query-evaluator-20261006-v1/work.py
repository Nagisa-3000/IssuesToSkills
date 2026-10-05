
import pathlib,json,sys,os,time
p=pathlib.Path("/home/chenyujia/tritonToLlvm/arex-skill-graph");sys.path.insert(0,str(p/"src"))
from arex_skill_graph.original_query_evaluator import original_query_evaluator,load_original_replay_authority
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.history_census import write_json,fingerprint
d=pathlib.Path(sys.argv[1])
queries=json.loads((p/"tmp/pre2021-public-branch-source-gap-recovery-preparation-v1-20261006/results/queries.json").read_text())
task=TaskContext.from_dict(next(q["task"] for q in queries if q["task"]["task_id"]=="PyCQA/pyflakes:470"))
os.environ["GIT_CONFIG_COUNT"]="1";os.environ["GIT_CONFIG_KEY_0"]="safe.directory";os.environ["GIT_CONFIG_VALUE_0"]=task.root
inv=json.loads((p/"tmp/qualified-cross-project-native-corpus-v3-20261006/qualification-inventory.json").read_text())
row=next(x for x in inv["results"] if x.get("verified_resolution") and x["issue_id"]==task.task_id)
verification=pathlib.Path(row["verification_path"])
controls=p/"tmp/pre2021-targeted-public-git-replay-controls-preparation-v1-20261006/results/cases/PyCQA__pyflakes-470"
review=p/"tmp/pyflakes-470-original-replay-independent-review-v1-20261006/review.json"
runtime=pathlib.Path(json.loads((p/"tmp/pre2021-input-compatible-runtime-map-preparation-v1-20261006/runtime-map.json").read_text())[task.task_id])
authority=load_original_replay_authority(task,verification,controls,review)
evaluate=original_query_evaluator(verification,runtime,controls,independent_review_path=review)
start=time.monotonic();results={}
for name,patch in [("empty_submission",""),("private_known_repair",authority.diff["production_diff"])]:
 result=evaluate(task,patch);results[name]=result;write_json(d/(name+".json"),result)
 print(json.dumps({"phase":name,"completed":result["evaluation_completed"],"resolved":result["validated_resolved"]}),flush=True)
good=bool(results["empty_submission"]["evaluation_completed"] and not results["empty_submission"]["validated_resolved"] and results["private_known_repair"]["evaluation_completed"] and results["private_known_repair"]["validated_resolved"])
write_json(d/"completion.json",{"schema":"original-query-evaluator-actual-controls-v1","status":"terminal","private_evaluator_controls_passed":good,"independent_review_sha256":fingerprint(authority.review),"cohort_sha256":authority.cohort["cohort_sha256"],"results":results,"elapsed_seconds":time.monotonic()-start,"solver_branches":0,"utility_labels_created":0,"actual_model_calls":0,"formal_SWE_runs":0})
