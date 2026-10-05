import pathlib,json,sys,tempfile,hashlib,os,datetime,difflib
p=pathlib.Path('/home/chenyujia/tritonToLlvm/arex-skill-graph')
sys.path.insert(0,str(p/'src'))
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.adaptive_runner import snapshot_base,make_namespace_tools
from arex_skill_graph.adaptive_budget import BudgetCaps,BudgetLedger
from arex_skill_graph.history_verification import junit_observations
from arex_skill_graph.history_census import fingerprint,write_json
d=pathlib.Path(sys.argv[1])
spec=json.loads((d/'control-spec.json').read_text())
task=TaskContext.from_dict(json.loads((d/'task.json').read_text()))
vpath=p/'tmp/pyflakes-repair-population-server-v6-20261004/verified/PyCQA__pyflakes-574-c23a81037d4f/verification.json'
assert hashlib.sha256((d/'task.json').read_bytes()).hexdigest()==spec['task_sha256']
assert hashlib.sha256(vpath.read_bytes()).hexdigest()==spec['native_verification_sha256']
assert hashlib.sha256((vpath.parent/'historical-diff.json').read_bytes()).hexdigest()==spec['historical_diff_file_sha256']
report=json.loads(vpath.read_text())
diff=json.loads((vpath.parent/'historical-diff.json').read_text())
mre="from typing import Annotated\n\nAnnotated[int, '>1']\n"
assert mre.strip() in task.public_problem.replace('\r\n','\n')
os.environ['GIT_CONFIG_COUNT']='1'
os.environ['GIT_CONFIG_KEY_0']='safe.directory'
os.environ['GIT_CONFIG_VALUE_0']=task.root
runtime=p/'tmp/pyflakes-server-runtime-v2-20261004'
def adapt_current_api(work):
    path=work/'pyflakes/checker.py'
    before=path.read_text()
    replacements=[
        ('def _enter_annotation(self):','def _enter_annotation(self, state=True):'),
        ('orig, self._in_annotation = self._in_annotation, True',
         'orig, self._in_annotation = self._in_annotation, state'),
        ('self._enter_annotation(AnnotationState.NONE)','self._enter_annotation(False)'),
        ('if slice_tuple is None or len(slice_tuple.elts) < 2:\n                self.handleNode(node.slice, node)',
         'if slice_tuple is None or len(slice_tuple.elts) < 2:\n                with self._enter_annotation():\n                    self.handleNode(node.slice, node)'),
        ('# the first argument is the type\n                self.handleNode(slice_tuple.elts[0], node)',
         '# the first argument is the type\n                with self._enter_annotation():\n                    self.handleNode(slice_tuple.elts[0], node)'),
    ]
    after=before
    for old,new in replacements:
        assert after.count(old)==1, ('current_api_mapping_not_exact',old,after.count(old))
        after=after.replace(old,new,1)
    assert 'AnnotationState' not in after
    path.write_text(after)
    return {'before_sha256':hashlib.sha256(before.encode()).hexdigest(),
            'after_sha256':hashlib.sha256(after.encode()).hexdigest(),
            'replacements':[{'old':old,'new':new} for old,new in replacements]}
edge_cases=[
    ('first_forward_name',"from typing import Annotated\nAnnotated['integer', '>0']\n",1,"undefined name 'integer'"),
    ('first_invalid_forward_syntax',"from typing import Annotated\nAnnotated['?', '>0']\n",1,"syntax error in forward annotation '?'"),
    ('metadata_name_is_value',"from typing import Annotated\nAnnotated[int, unknown_metadata]\n",1,"undefined name 'unknown_metadata'"),
    ('module_attribute',"import typing\ntyping.Annotated[int, '>0']\n",0,None),
    ('state_restored_after_metadata',"from typing import Annotated\n\ndef f(x: Annotated[int, '>0']):\n    pass\n\ndef g(x: 'missing_type'):\n    pass\n",1,"undefined name 'missing_type'"),
]
results=[]
for phase,patches in [
    ('original_base',()),
    ('base_with_unchanged_regressions',(diff['regression_diff'],)),
    ('evaluator_current_api_known_repair',(diff['production_diff'],diff['regression_diff'])),
]:
    with tempfile.TemporaryDirectory(prefix='arex-current-api-private-controls-') as scratch:
        work=pathlib.Path(scratch)/'workspace'
        snapshot_base(task,work)
        tools=make_namespace_tools(work,BudgetLedger(BudgetCaps(seconds=600)),runtime,backend='namespace-copy')
        try:
            tools.preflight()
            base_checker=(work/'pyflakes/checker.py').read_text()
            applied=[]
            for patch in patches:
                result=tools.run(['git','apply','--whitespace=nowarn','-'],stdin=patch.encode(),timeout=60)
                applied.append(result)
                if result['exit_code']!=0:
                    break
            assert all(r['exit_code']==0 for r in applied), 'patch_application_failed'
            adaptation=None
            if phase=='evaluator_current_api_known_repair':
                adaptation=adapt_current_api(work)
                adapted=''.join(difflib.unified_diff(base_checker.splitlines(keepends=True), (work/'pyflakes/checker.py').read_text().splitlines(keepends=True), fromfile='a/pyflakes/checker.py',tofile='b/pyflakes/checker.py'))
                assert adapted
                (d/'evaluator-only-current-repair.diff').write_text(adapted)
            probe=tools.run(['python3','-c',"import sys;from pyflakes.api import check;raise SystemExit(check(sys.stdin.read(),'original_issue.py'))"],stdin=mre.encode(),timeout=120)
            tested=tools.run([*report['command'],'--junitxml=/workspace/control-results.xml'],timeout=120)
            observations=junit_observations(work/'control-results.xml')
            edges=[]
            if phase=='evaluator_current_api_known_repair':
                for name,source,expected,diagnostic in edge_cases:
                    result=tools.run(['python3','-c',"import sys;from pyflakes.api import check;raise SystemExit(check(sys.stdin.read(),'boundary_probe.py'))"],stdin=source.encode(),timeout=60)
                    edges.append({'name':name,'source':source,'expected_exit_code':expected,'expected_diagnostic':diagnostic,'result':result,
                                  'passed':result['exit_code']==expected and (diagnostic is None or diagnostic in result['output'])})
            expected_names=spec['original_current_tests'] if phase=='original_base' else spec['expected_collected_tests']
            row={'phase':phase,'setup_complete':True,'patch_application':applied,'current_api_adaptation':adaptation,
                 'public_original_mre':probe,'focused_test_run':tested,'observations':observations,
                 'exact_current_cohort_collected':sorted(observations)==expected_names,
                 'fail_to_pass_outcomes':{k:observations.get(k) for k in spec['fail_to_pass']},
                 'current_pass_to_pass_outcomes':{k:observations.get(k) for k in spec['current_pass_to_pass']},
                 'boundary_probes':edges,'runtime_sha256':tools.runtime_sha256}
            results.append(row)
            write_json(d/(phase+'.json'),row)
            write_json(d/'progress.json',{'completed_phases':len(results),'phase':phase,'actual_LLM_calls':0})
            print(json.dumps({'phase':phase,'setup_complete':True,'MRE_exit_code':probe['exit_code'],'test_exit_code':tested['exit_code'],
                              'test_count':len(observations),'exact_cohort':row['exact_current_cohort_collected'],
                              'F2P':row['fail_to_pass_outcomes'],'boundary_passed':sum(x['passed'] for x in edges),'boundary_total':len(edges)}),flush=True)
        finally:
            tools.close()
task.verify()
unchanged=hashlib.sha256(vpath.read_bytes()).hexdigest()==spec['native_verification_sha256']
passed=(
    len(results)==3 and all(r['exact_current_cohort_collected'] for r in results)
    and len({r['runtime_sha256'] for r in results})==1 and unchanged
    and results[0]['focused_test_run']['exit_code']==0
    and results[0]['public_original_mre']['exit_code']==1
    and results[1]['focused_test_run']['exit_code']==1
    and results[1]['public_original_mre']['exit_code']==1
    and all(v=='failed' for v in results[1]['fail_to_pass_outcomes'].values())
    and all(v=='passed' for v in results[1]['current_pass_to_pass_outcomes'].values())
    and results[2]['focused_test_run']['exit_code']==0
    and results[2]['public_original_mre']['exit_code']==0
    and all(v=='passed' for v in results[2]['fail_to_pass_outcomes'].values())
    and all(v=='passed' for v in results[2]['current_pass_to_pass_outcomes'].values())
    and all(x['passed'] for x in results[2]['boundary_probes'])
)
completion={'schema':'published-original-current-api-control-completion-v1','query_id':task.task_id,
    'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'original_input_available_at':task.input_available_at,'published_source_base':task.base_commit,
    'control_spec_sha256':fingerprint(spec),'mechanical_current_api_controls_passed':bool(passed),
    'raw_historical_patch_controls_passed':False,'known_repair_adapted_for_current_api':True,
    'unchanged_historical_regression_assertions':True,'current_fail_to_pass_count':len(spec['fail_to_pass']),
    'current_pass_to_pass_count':len(spec['current_pass_to_pass']),
    'missing_historical_pass_to_pass':spec['missing_historical_pass_to_pass'],
    'native_source_record_unchanged':unchanged,'original_public_task_unchanged':True,
    'actor_may_read_evaluator_adaptation':False,'independent_review_complete':False,
    'solver_branches':0,'utility_labels_created':0,'formal_SWE_runs':0,'actual_LLM_calls':0,
    'runtime_sha256':results[0]['runtime_sha256'],'results_sha256':[fingerprint(row) for row in results],
    'qualification_scope':spec['qualification_scope']}
write_json(d/'completion.json',completion)
print(json.dumps(completion),flush=True)
sys.exit(0 if passed else 2)
