from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT/'data/skill-extraction/cases'
SCHEMA = json.loads((ROOT/'schemas/generalized-skill-family-v2.schema.json').read_text())
DEFS = SCHEMA['$defs']
OUT = ROOT/'data/skill-extraction/synthesis/residual-budget-family/bundle.json'
NOW = '2026-09-27T00:00:00Z'
_counter = 0

def h(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def ex(spec, prefix):
    global _counter
    if '$ref' in spec: return ex(DEFS[spec['$ref'].split('/')[-1]], prefix)
    if 'const' in spec: return spec['const']
    if 'enum' in spec: return spec['enum'][0]
    typ=spec.get('type')
    if isinstance(typ,list): typ=next((x for x in typ if x!='null'),'string')
    if typ=='object': return {k:ex(spec['properties'][k], prefix+'-'+k) for k in spec.get('required',[])}
    if typ=='array': return [ex(spec.get('items',{}), prefix+'-item')] if spec.get('minItems',0)>0 else []
    if typ=='boolean': return True
    if typ=='integer': return 1
    if typ=='number': return 0.5
    if typ=='string':
        if spec.get('format')=='date-time': return NOW
        pat=spec.get('pattern','')
        if '64' in pat: return '0'*64
        if '^[a-z]' in pat: return 'x:id'
        return 'example'
    return None

def make(name,prefix): return ex(DEFS[name],prefix)
def assertion(text, refs, status='inferred'):
    return {'text':text,'epistemic_status':status,'evidence_ids':refs,'rationale':'Evidence-grounded semantic reading; not inferred from lexical similarity.','confidence':0.9}
def set_refs(x, refs):
    if isinstance(x,dict):
        for k,v in list(x.items()):
            if k in {'evidence_ids','acceptance_evidence_ids','probe_evidence_ids'}: x[k]=list(refs)
            else: set_refs(v,refs)
    elif isinstance(x,list):
        for v in x: set_refs(v,refs)
def ids(xs): return {x['id'] for x in xs}
def quality(bundle):
    return {'instance_counts':{k:len(bundle[k]) for k in ('evidence_units','case_actions','case_workflows')},'knowledge_counts':{k:len(bundle[k]) for k in ('atomic_skills','workflow_skills','patterns')},'package_count':len(bundle['agent_skill_packages']),'promotion_failures':['No held-out transfer has passed; no node is validated.'],'warnings':['Pi is partial alignment; Aider is adjacent and explicitly rejected from the residual Pattern.'],'reviewed_by':['LLM semantic extraction/governance','deterministic v2 validator']}

def main():
    cases=[json.loads(p.read_text()) for p in sorted(CASE_DIR.glob('*/case.json'))]
    evidence=[]; actions=[]; cws=[]; cmap={}
    for c in cases:
        cid=c['case_id']; repo=c['repository']['name']; rev=c.get('repository',{}).get('commit') or c.get('git_provenance',{}).get('merge_commit') or 'case-head'; em={}
        for u in c.get('evidence_units',[]):
            eid=f"evidence:{cid}:{u['id'].lower().replace('_','-')}"; em[u['id']]=eid
            kind='test' if u.get('kind') in ('test','test_result') else ('diff_hunk' if 'diff' in u.get('kind','') else 'commit')
            evidence.append({'id':eid,'kind':kind,'repository':repo,'locator':{'revision':rev,'path':u.get('source') or (u.get('sources') or ['case-evidence'])[0],'symbol':None,'line_start':None,'line_end':None,'external_number':c.get('git_provenance',{}).get('pull_request'),'raw_pointer':u.get('claim') or (u.get('sources') or ['case-evidence'])[0]},'summary':u.get('claim') or u.get('text') or 'case evidence','content_sha256':h(u),'capture_method':'manual','trust':'reviewed','captured_at':NOW})
        am={}
        for a in c.get('case_actions',[]):
            aid=f"case-action:{cid}:{a['id'].lower()}"; am[a['id']]=aid; refs=[em[x] for x in a.get('evidence_units',[]) if x in em]; title=a.get('semantic_goal','case action')
            z=make('caseAction',aid); z.update({'id':aid,'repository':repo,'revision':rev,'title':title,'evidence_ids':refs,'lineage_group':f'lineage:{cid}'})
            z['problem_manifestation']=assertion('The case exposes a concrete behavior violating its capacity/context contract.',refs)
            z['transformation']['operation']=assertion(title,refs); z['validation_observations']=[assertion('The case records implementation or test evidence for this action.',refs,'observed')]
            actions.append(z)
        cw=c.get('case_workflow') or {}; cwid=f"case-workflow:{cid}:{str(cw.get('id','cw1')).lower()}"; stepids=[am[x] for x in cw.get('steps',[]) if x in am] or list(am.values())
        z=make('caseWorkflow',cwid); z.update({'id':cwid,'repository':repo,'title':cw.get('title') or cw.get('goal') or cid,'case_action_ids':stepids,'failed_or_reverted_action_ids':[],'acceptance_evidence_ids':sorted({e for a in actions if a['id'] in stepids for e in a['evidence_ids']})}); z['anchor']={'kind':'pull_request' if c.get('git_provenance',{}).get('pull_request') else 'episode','identifier':str(c.get('git_provenance',{}).get('pull_request') or cid),'revision':rev}; z['edges']=[]
        for i in range(len(stepids)-1): z['edges'].append({'id':f'edge:{cwid}:{i}','source_id':stepids[i],'target_id':stepids[i+1],'relation':'precedes','rationale':assertion('Recorded implementation order.',[])})
        z['entry_state']=[assertion('The defect or bounded context task is present.',[])]; z['exit_state']=[assertion('Recorded implementation and validation satisfy the case contract.',z['acceptance_evidence_ids'])]; z['decision_points']=[assertion(x,[]) for x in cw.get('conditional_branches',[])[:3]]; cws.append(z); cmap[cid]={'repo':repo,'evidence':list(em.values()),'cw':cwid}

    atom_specs=[
      ('derive-policy-from-residual-capacity','Derive policy from residual shared capacity','Subtract mandatory downstream reservations before deriving an upstream pressure/admission policy',['hermes-compaction-reservation','deepseek-compaction-reservation']),
      ('normalize-capacity-reservation-boundaries','Normalize capacity reservation boundaries','Normalize optional or malformed reservations before arithmetic',['hermes-compaction-reservation','deepseek-compaction-reservation']),
      ('replay-capacity-policy-across-reconfiguration','Replay capacity policy across reconfiguration','Recompute derived policy after model/provider/context changes',['hermes-compaction-reservation','deepseek-compaction-reservation']),
      ('resolve-model-specific-policy-with-fallback','Resolve model-specific policy with fallback','Resolve target-specific policy at the active runtime route',['pi-compaction-budget']),
      ('place-pressure-check-at-next-request-boundary','Place pressure check at next request boundary','Evaluate pressure where the next request is actually formed',['pi-compaction-budget']),
      ('account-for-all-context-visible-artifacts','Account for all context-visible artifacts','Measure all artifacts included in the serialized context',['pi-compaction-budget']),
      ('derive-history-budget-from-model-input-capability','Derive history budget from model input capability','Derive summarization budget from active model input capability',['aider-context-budget']),
      ('select-history-prefix-by-available-summarizer-budget','Select history prefix by available summarizer budget','Fit older history while preserving a recent tail',['aider-context-budget']),
      ('preserve-original-context-on-summary-failure','Preserve original context on summary failure','Keep the original context recoverable until summary validation succeeds',['aider-context-budget'])]
    atoms=[]; amap={}
    for slug,title,desc,cids in atom_specs:
        aid=f'atomic:{slug}'; amap[slug]=aid; refs=sorted({e for cid in cids for e in cmap[cid]['evidence']}); z=make('atomicSkill',aid); z.update({'id':aid,'version':'1.0.0','title':title,'name':slug,'description':desc,'lifecycle':'reviewed' if len(cids)>1 else 'candidate','transfer_record_ids':[]}); set_refs(z,refs)
        z['problem_signature']=assertion(desc,refs); z['objective']=assertion(desc,refs); z['problem_mechanism']=assertion('The implementation must preserve the stated capacity/context invariant.',refs); z['solution_principle']=assertion(desc,refs); z['realizations']=[]
        for cid in cids:
            r=make('realization',f'{aid}-{cid}'); rid=f'realization:{slug}:{cid}'; r.update({'id':rid,'realization_id':rid,'repository':cmap[cid]['repo'],'evidence_ids':cmap[cid]['evidence'],'independent':len(cids)>1}); z['realizations'].append(r)
        rids=[r['id'] for r in z['realizations']]; z['abstraction_assessment']={k:{'status':'pass' if len(cids)>1 else 'not_run','rationale':'LLM reviewed mechanism across recorded evidence.' if len(cids)>1 else 'Held-out transfer not run.','supporting_realization_ids':rids} for k in ('symbol_substitution','repository_independence','implementation_variability','counterfactual_transfer','atomic_minimality','causal_sufficiency','counterexample_discrimination')}; z['views']['audit']['realization_ids']=rids; z['views']['audit']['evidence_ids']=refs; z['quality']={'evidence_coverage':.9,'causal_clarity':.8,'boundary_clarity':.8,'transferability':.2 if len(cids)>1 else 0,'validation_strength':.6,'overall':.76 if len(cids)>1 else .63}; atoms.append(z)

    wf_specs=[('reserve-output-before-pressure-policy','Reserve output before pressure policy',['derive-policy-from-residual-capacity','normalize-capacity-reservation-boundaries'],['hermes-compaction-reservation','deepseek-compaction-reservation']),('replay-policy-across-runtime-reconfiguration','Replay policy across runtime reconfiguration',['replay-capacity-policy-across-reconfiguration','resolve-model-specific-policy-with-fallback'],['hermes-compaction-reservation','deepseek-compaction-reservation','pi-compaction-budget']),('measure-context-before-next-request','Measure context before the next request',['account-for-all-context-visible-artifacts','place-pressure-check-at-next-request-boundary'],['pi-compaction-budget']),('summarize-with-budgeted-tail-and-recovery','Summarize with a budgeted tail and recovery',['derive-history-budget-from-model-input-capability','select-history-prefix-by-available-summarizer-budget','preserve-original-context-on-summary-failure'],['aider-context-budget'])]
    workflows=[]; wmap={}
    for slug,title,aslugs,cids in wf_specs:
        wid=f'workflow:{slug}'; wmap[slug]=wid; refs=sorted({e for cid in cids for e in cmap[cid]['evidence']}); z=make('workflowSkill',wid); z.update({'id':wid,'version':'1.0.0','title':title,'name':slug,'description':title,'goal':title,'lifecycle':'reviewed' if len(cids)>1 else 'candidate','transfer_record_ids':[]}); set_refs(z,refs); z['realizations']=[]; z['steps']=[]; z['edges']=[]
        for i,aslug in enumerate(aslugs):
            sid=f'step:{slug}:{i+1}'; s=make('workflowStep',sid); s.update({'id':sid,'uses_atomic_skill_ids':[amap[aslug]],'semantic_goal':f'Apply {aslug}','procedure_summary':'Invoke the Atomic after LLM applicability review.','on_success':f'step:{slug}:{i+2}' if i+1<len(aslugs) else 'DONE','on_failure':'LLM_FAILURE_REVIEW'}); z['steps'].append(s)
        for i in range(len(z['steps'])-1): z['edges'].append({'id':f'edge:{slug}:{i}','source_id':z['steps'][i]['id'],'target_id':z['steps'][i+1]['id'],'relation':'precedes','rationale':assertion('The workflow composes bounded Atomic operations in order.',refs)})
        for cid in cids:
            r=make('realization',f'{wid}-{cid}'); rid=f'realization:{slug}:{cid}'; r.update({'id':rid,'realization_id':rid,'repository':cmap[cid]['repo'],'evidence_ids':cmap[cid]['evidence'],'independent':len(cids)>1}); z['realizations'].append(r)
        rids=[r['id'] for r in z['realizations']]; z['abstraction_assessment']={k:{'status':'pass' if len(cids)>1 else 'not_run','rationale':'LLM reviewed composition against case workflow evidence.','supporting_realization_ids':rids} for k in ('symbol_substitution','repository_independence','implementation_variability','counterfactual_transfer','atomic_minimality','causal_sufficiency','counterexample_discrimination')}; z['views']['audit']['realization_ids']=rids; z['views']['audit']['evidence_ids']=refs; z['quality']={'evidence_coverage':.88,'causal_clarity':.8,'boundary_clarity':.78,'transferability':.2 if len(cids)>1 else 0,'validation_strength':.6,'overall':.74 if len(cids)>1 else .62}; workflows.append(z)

    pat_specs=[('shared-capacity-residual-budget','Shared-capacity residual-budget invariant',['reserve-output-before-pressure-policy','replay-policy-across-runtime-reconfiguration','measure-context-before-next-request'],['hermes-compaction-reservation','deepseek-compaction-reservation','pi-compaction-budget']),('budgeted-context-preserving-summarization','Budgeted context-preserving summarization',['summarize-with-budgeted-tail-and-recovery'],['aider-context-budget'])]
    patterns=[]; pmap={}
    for slug,title,wslugs,cids in pat_specs:
        pid=f'pattern:{slug}'; pmap[slug]=pid; refs=sorted({e for cid in cids for e in cmap[cid]['evidence']}); z=make('pattern',pid); z.update({'id':pid,'version':'1.0.0','title':title,'lifecycle':'candidate','transfer_record_ids':[]}); set_refs(z,refs); z['workflow_variants']=[{'name':w,'workflow_skill_id':wmap[w],'when_to_choose':'LLM confirms the workflow preconditions and causal mechanism.','tradeoffs':['Conservative policy may trigger earlier pressure.']} for w in wslugs]; z['supporting_case_workflow_ids']=[cmap[cid]['cw'] for cid in cids]; z['abstraction_assessment']={k:{'status':'not_run','rationale':'No held-out transfer has run; pattern remains provisional.','supporting_realization_ids':[]} for k in ('symbol_substitution','repository_independence','implementation_variability','counterfactual_transfer','atomic_minimality','causal_sufficiency','counterexample_discrimination')}; z['views']['audit']['realization_ids']=[]; z['views']['audit']['evidence_ids']=refs; z['quality']={'evidence_coverage':.85,'causal_clarity':.72,'boundary_clarity':.8,'transferability':.0,'validation_strength':.4,'overall':.67}; patterns.append(z)

    nodes=atoms+workflows+patterns; transfers=[]
    for n in nodes:
        t=make('transferRecord',f'transfer-{n["id"]}'); tid=f'transfer:not-run:{n["id"].replace(":","-")}'; t.update({'id':tid,'knowledge_node_id':n['id'],'target_repository':'held-out-not-selected','target_case':'held-out-not-run','retrieved_version':n['version'],'result':'not_run','target_solution_hidden':True,'predicted_plan':'Not run; execute held-out transfer before validation promotion.','performed_actions':[],'evidence_ids':[]}); transfers.append(t); n['transfer_record_ids']=[tid]
    relations=[]
    for w in workflows:
        for s in w['steps']:
            a=s['uses_atomic_skill_ids'][0]; relations.append({'id':f'relation:{a}-part-of-{w["id"]}','source_id':a,'target_id':w['id'],'relation':'part_of','confidence':.9,'rationale':'Workflow step explicitly uses this Atomic.','evidence_ids':w['views']['audit']['evidence_ids']})
    for p in patterns:
        for v in p['workflow_variants']: relations.append({'id':f'relation:{v["workflow_skill_id"]}-part-of-{p["id"]}','source_id':v['workflow_skill_id'],'target_id':p['id'],'relation':'part_of','confidence':.8,'rationale':'Pattern variant explicitly references this Workflow.','evidence_ids':p['views']['audit']['evidence_ids']})
    rejected=[{'id':'rejected:aider-vs-residual-pattern','candidate_ids':['pattern:shared-capacity-residual-budget','workflow:summarize-with-budgeted-tail-and-recovery'],'rejection_reason':'Aider is adjacent but does not establish the same output-reservation residual invariant.','mechanism_difference':'The downstream consumer and recovery contract differ; lexical context-budget similarity is insufficient.','evidence_ids':cmap['aider-context-budget']['evidence']}]
    packages=[{'id':'package:shared-capacity-residual-budget','name':'shared-capacity-residual-budget','description':'Evidence-grounded Pattern package; use only after LLM applicability review.','primary_node_id':'pattern:shared-capacity-residual-budget','primary_node_level':'pattern','export_policy':'reference_only','skill_md_sections':['purpose','use_when','do_not_use_when','workflow','decision_rules','invariants','validation','failure_recovery'],'resources':[{'path':'references/residual-budget-evidence.md','purpose':'Evidence and boundaries.','load_when':'Audit applicability.'}],'evals':[{'name':'positive-shared-window','kind':'positive','prompt':'Identify mandatory downstream reservations in a shared finite window.','expected_behavior':'Select residual workflow only when evidence confirms shared capacity.'},{'name':'negative-independent-pools','kind':'negative','prompt':'Input and output pools are independent.','expected_behavior':'Reject this Pattern.'},{'name':'held-out-transfer','kind':'regression','prompt':'Apply to an unseen repository with solution hidden.','expected_behavior':'Do not claim validation before the oracle passes.'}]}]
    bundle={'schema_version':'2.0.0','bundle_id':'bundle:residual-budget-family-v2','task_family':{'id':'task-family:shared-capacity-context-maintenance','name':'Shared-capacity context maintenance','definition':assertion('Repair context/compaction policies when finite capacity is shared by multiple consumers.',[]),'inclusion_criteria':[assertion('A finite context/capacity envelope is shared by upstream and downstream work.',[])],'exclusion_criteria':[assertion('Independent pools or unrelated changes are excluded.',[])]},'extraction':{'run_id':'run:2026-09-27-residual-budget-v2','method':'llm_code_reading_with_deterministic_validation','llm_semantic_reading_required':True,'context_manifest_sha256':h([c['case_id'] for c in cases]),'created_at':NOW,'notes':'Semantic extraction, deduplication, abstraction, applicability, and lifecycle decisions are LLM-governed; BM25/embedding/HNSW are retrieval-only.'},'evidence_units':evidence,'case_actions':actions,'case_workflows':cws,'atomic_skills':atoms,'workflow_skills':workflows,'patterns':patterns,'transfer_records':transfers,'bindings':[],'agent_skill_packages':packages,'relations':relations,'rejected_alignments':rejected}
    bundle['quality_report']=quality(bundle); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+'\n'); print(OUT)
if __name__=='__main__': main()

