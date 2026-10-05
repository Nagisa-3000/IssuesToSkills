#!/usr/bin/env python3
"""Prepare isolated historical evidence; independently review applicability without utility claims."""

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import asdict, replace
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from arex_skill_graph.action_contracts import SourceRecord, TemporalPolicy, digest, utc
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.adaptive_cli import read_json, read_references, transport_from_args
from arex_skill_graph.applicability_supervision import (
    review_applicability,
    seal_packet,
    validate_packet,
)
from arex_skill_graph.historical_isolation import HistoricalIsolation
from arex_skill_graph.history_census import write_json
from arex_skill_graph.llm_http import safe_text
from arex_skill_graph.pattern_contracts import load_native_package
from arex_skill_graph.plan_validation import ResourcePolicy, TaskWorkflowPlan
from arex_skill_graph.qualification_authority import validate_historical_qualification
from arex_skill_graph.task_context import TaskContext
from arex_skill_graph.temporal_ranker_data import HistoricalQuery, validate_training_snapshot
from arex_skill_graph.workflow_ranker import plan_capsule, workflow_capsule


def entry(ident, role, text, **metadata):
    return {'id': ident, 'role': role, 'text': text, 'text_sha256': digest(text), **metadata}


def safe_source_path(relative):
    if (not isinstance(relative, str) or not relative or
            PurePosixPath(relative).is_absolute() or '..' in PurePosixPath(relative).parts or
            '\\' in relative or '\x00' in relative or '\n' in relative):
        raise ValueError('unsafe historical oracle source path')
    return relative


def changed_source_paths(diff):
    """Read both production and assertion owners; paths alone is the test-only scope."""
    paths = [safe_source_path(p) for p in diff['paths']]
    for key in ('production_diff', 'regression_diff'):
        for line in diff[key].splitlines():
            if not line.startswith(('--- ', '+++ ')):
                continue
            relative = line[4:].split('\t', 1)[0]
            if relative.startswith('"'):
                relative = ast.literal_eval(relative)
            if relative == '/dev/null':
                continue
            if not relative.startswith(('a/', 'b/')):
                raise ValueError('historical oracle diff lacks a repository-relative path')
            paths.append(safe_source_path(relative[2:]))
    if not paths:
        raise ValueError('historical label oracle has no current source paths')
    return sorted(set(paths))


def oracle_input_hashes(query, verification_row, controls_dir):
    verification = Path(verification_row['verification_path'])
    case = query.task.task_id.replace('/', '__').replace(':', '-')
    return {key: digest(read_json(path)) for key, path in {
        'verification': verification,
        'diff': verification.parent / 'historical-diff.json',
        'controls': controls_dir / case / 'controls.json',
    }.items()}


def historical_oracle(query, verification_row, controls_dir, main_cutoff):
    path = Path(verification_row['verification_path'])
    report = read_json(path)
    diff = read_json(path.parent / 'historical-diff.json')
    identity = report['identity']
    if (identity['issue_id'] != query.task.task_id or identity['base_commit'] != query.task.base_commit
            or identity['fix_id'] != query.fix_id or diff['available_at'] != identity['repair_available_at']):
        raise ValueError('historical label oracle differs from the query/repair identity')
    source = SourceRecord(query.task.task_id + ':repair:' + identity['merge_commit'][:12],
                          query.task.repository, query.bug_cluster_id, query.fix_id,
                          identity['merge_commit'], identity['repair_available_at'],
                          ('label-oracle:implementation', 'label-oracle:assertions'),
                          aliases=(query.task.task_id,), verified_resolution=True)
    validate_historical_qualification(report, source, TemporalPolicy(main_cutoff))
    case = query.task.task_id.replace('/', '__').replace(':', '-')
    controls = read_json(controls_dir / case / 'controls.json')
    if (controls.get('passed') is not True or controls.get('same_protocol') is not True or
            controls.get('task_id') != query.task.task_id or
            controls.get('base_commit') != query.task.base_commit or
            controls.get('solver_input_contains_control_results') is not False):
        raise ValueError('historical label oracle lacks matching independent causal controls')
    git = ['git', '--literal-pathspecs', '-C', query.task.root]
    current = []
    for relative in changed_source_paths(diff):
        listing = subprocess.run([*git, 'ls-tree', '-z', '--name-only', query.task.base_commit,
                                  '--', relative], capture_output=True, text=True, check=True)
        if listing.stdout.rstrip('\x00') == relative:
            text = subprocess.check_output([*git, 'show', query.task.base_commit + ':' + relative], text=True)
        else:
            text = 'Exact git ls-tree confirms this path is absent in the public base: ' + relative
        current.append(entry('public-base:' + query.task.base_commit + ':' + relative,
                             'current_code', text, path=relative, base_commit=query.task.base_commit))
    private = json.dumps({'historical_production_diff': diff['production_diff'],
                          'historical_regression_assertions': diff['regression_diff'],
                          'independent_causal_controls': controls,
                          'qualification_scope': report['qualification_scope'],
                          'whole_project_regression_checked': report['whole_project_regression_checked'],
                          'available_at': identity['repair_available_at'],
                          'verification_sha256': digest(report)}, ensure_ascii=False)
    current.append(entry('privileged-history-label-oracle:' + digest(private),
                         'privileged_label_oracle', private,
                         learned_candidate_resource=False,
                         historical_repair_available_at=identity['repair_available_at']))
    return current


def causal_isolation_for_dataset(dataset, args):
    """Keep reviewed identities host-only and attached to the exact dataset input."""
    path = getattr(args, 'causal_isolation', None)
    raw = read_json(path) if path else None
    expected = dataset.get('source_input_hashes', {}).get('causal_isolation')
    if (digest(raw) if raw is not None else None) != expected:
        raise ValueError('historical review causal isolation differs from frozen dataset')
    isolation = HistoricalIsolation.from_dict(raw) if raw is not None else None
    if any(a.get('causal_isolation_sha256') != (isolation.sha256 if isolation else None)
           for a in dataset.get('audits', [])):
        raise ValueError('historical dataset causal isolation audit changed')
    return isolation


def candidate_policy(query, cutoff, isolation):
    exclusions = (isolation.query_exclusions(query) if isolation else
                  ((query.task.task_id, *query.aliases, *query.copied_from),
                   (query.bug_cluster_id,), (query.fix_id,)))
    return TemporalPolicy(cutoff, *exclusions)


def prepare(args):
    dataset = validate_training_snapshot(read_json(args.dataset))
    isolation = causal_isolation_for_dataset(dataset, args)
    queries_raw, plans = read_json(args.queries), read_json(args.plans)
    if dataset['source_input_hashes'].get('queries') != digest(queries_raw) or \
            dataset['source_input_hashes'].get('references') != digest(read_json(args.references)) or \
            dataset['source_input_hashes'].get('plans') != digest(plans):
        raise ValueError('historical review changed its frozen query/catalog/Plan inputs')
    queries = {r['task']['task_id']: HistoricalQuery(TaskContext.from_dict(r['task']),
               r['bug_cluster_id'], r['fix_id'], tuple(r.get('aliases', [])),
               tuple(r.get('copied_from', [])), r.get('exposed', False)) for r in queries_raw}
    refs = read_references(args.references)
    reference_by_hash = {r['package_sha256']: r for r in refs}
    verification_rows = {(r['issue_id'], r['fix_id']): r for r in read_json(args.verifications)['results']
                         if r['verified_resolution']}
    pairs = {}
    for example in dataset['examples']:
        key = (example['query_id'], example['candidate']['id'])
        if key in pairs and digest(pairs[key]['candidate']) != digest(example['candidate']):
            raise ValueError('one candidate changed across reviewed observations')
        pairs[key] = example
    oracle_cache, native_cache, packets, oracle_hashes = {}, {}, [], {}
    for (qid, cid), example in sorted(pairs.items()):
        query = queries[qid]
        if query.exposed or utc(query.task.input_available_at) >= utc(dataset['main_cutoff']):
            raise ValueError('formal/exposed query cannot create historical supervision')
        query.task.verify()
        public = query.task.to_dict()
        public.pop('root')
        if digest(public) != digest(example['task_input']):
            raise ValueError('historical reviewer public input differs from training features')
        if qid not in oracle_cache:
            oracle_cache[qid] = historical_oracle(query, verification_rows[(qid, query.fix_id)],
                                                  args.controls_dir, dataset['main_cutoff'])
        oracle_hashes[qid] = oracle_input_hashes(query, verification_rows[(qid, query.fix_id)],
                                                args.controls_dir)
        candidate = example['candidate']
        hashes = candidate['package_hashes']
        if not hashes or len(set(hashes)) != len(hashes) or len(hashes) > 2:
            raise ValueError('historical review candidate has invalid/excessive resource roots')
        policy = candidate_policy(query, example['catalog_cutoff'], isolation)
        packages = []
        for sha in hashes:
            if sha not in native_cache:
                native_cache[sha] = load_native_package(reference_by_hash[sha])
            package = native_cache[sha]
            if isolation is not None:
                isolation.verify_sources(package.sources)
            package.admit(policy)
            packages.append(package)
        resources = ResourcePolicy(policy, tuple(p.reference for p in packages))
        if candidate['candidate_kind'] == 'workflow':
            actual = next(w for p in packages for w in p.workflows if w.id == cid)
            capsule = workflow_capsule(actual, query.task, resources)
        else:
            actual = next(TaskWorkflowPlan.from_dict(p) for p in plans[qid] if p['id'] == cid)
            capsule, _ = plan_capsule(actual, query.task, resources)
        if digest(capsule.to_dict()) != digest(candidate):
            raise ValueError('applicability candidate differs from the authoritative native resource')
        evidence = [entry('public-query:' + digest(public), 'public_query', query.task.public_problem),
                    *oracle_cache[qid]]
        for package in packages:
            root = Path(package.root)
            at = max((s.available_at for s in package.sources), key=utc)
            selected = [root / 'SKILL.md', root / 'references/workflow.md', *sorted((root / 'references/actions').glob('*.md')),
                        *sorted((root / 'references/evidence').glob('*.md'))]
            for file in selected:
                relative = file.relative_to(root).as_posix()
                evidence.append(entry('candidate-resource:' + package.reference['package_sha256'] + ':' + relative,
                                      'candidate_history', file.read_text(),
                                      knowledge_available_at=at,
                                      package_sha256=package.reference['package_sha256'],
                                      source_ids=[s.id for s in package.sources]))
        packet = seal_packet(
            public, candidate, evidence, catalog_cutoff=example['catalog_cutoff'],
            catalog_sha256=example['temporal_catalog_sha256'],
            main_cutoff=dataset['main_cutoff'], training_cutoff=dataset['training_cutoff'],
            query_identity={'bug_cluster_id': query.bug_cluster_id, 'fix_id': query.fix_id,
                            'aliases': list(query.aliases), 'copied_from': list(query.copied_from),
                            'exposed': query.exposed},
            candidate_sources=[{'package_sha256': p.reference['package_sha256'], 'source': asdict(s)}
                               for p in packages for s in p.sources],
        )
        ident = digest((qid, cid))[:24]
        packet_path = args.output_dir / 'packets' / (ident + '.json')
        write_json(packet_path, packet)
        packets.append({'id': ident, 'query_id': qid, 'candidate_id': cid,
                        'candidate_kind': candidate['candidate_kind'],
                        'packet_path': str(packet_path.resolve()), 'packet_sha256': packet['packet_sha256']})
    manifest = {'schema': 'historical-applicability-review-population-v2',
                'dataset_sha256': dataset['dataset_sha256'],
                'input_file_hashes': {k: digest(read_json(getattr(args, k))) for k in
                                     ('dataset', 'queries', 'references', 'plans', 'verifications')},
                'main_cutoff': dataset['main_cutoff'], 'training_cutoff': dataset['training_cutoff'],
                'oracle_input_hashes': oracle_hashes,
                'packets': packets, 'prepared_at': datetime.now(UTC).isoformat(),
                'model_calls': 0, 'labels_created': 0, 'formal_SWE_runs': 0,
                'privileged_artifacts_are_label_evaluator_only': True}
    if getattr(args, 'causal_isolation', None):
        manifest['input_file_hashes']['causal_isolation'] = digest(read_json(args.causal_isolation))
    manifest['population_sha256'] = digest(manifest)
    write_json(args.output_dir / 'prepared-population.json', manifest)
    return manifest


def validate_population(manifest, args, packet_root):
    """Reuse the complete immutable pool only; no forged subset or detached packets."""
    if (manifest.get('schema') != 'historical-applicability-review-population-v2' or
            manifest.get('population_sha256') != digest({k: v for k, v in manifest.items()
                                                         if k != 'population_sha256'}) or
            manifest.get('privileged_artifacts_are_label_evaluator_only') is not True or
            any(manifest.get(k) != 0 for k in ('model_calls', 'labels_created', 'formal_SWE_runs'))):
        raise ValueError('invalid or changed prepared historical population')
    required = {'dataset', 'queries', 'references', 'plans', 'verifications'}
    if getattr(args, 'causal_isolation', None):
        required.add('causal_isolation')
    if set(manifest['input_file_hashes']) != required:
        raise ValueError('prepared historical review input coverage changed')
    for key, sha in manifest['input_file_hashes'].items():
        if digest(read_json(getattr(args, key))) != sha:
            raise ValueError('prepared historical review input changed: ' + key)
    dataset = validate_training_snapshot(read_json(args.dataset))
    isolation = causal_isolation_for_dataset(dataset, args)
    if (dataset['dataset_sha256'] != manifest['dataset_sha256'] or
            dataset['main_cutoff'] != manifest['main_cutoff'] or
            dataset['training_cutoff'] != manifest['training_cutoff']):
        raise ValueError('prepared historical temporal identity changed')
    expected = {(e['query_id'], e['candidate']['id']): e for e in dataset['examples']}
    query_rows = read_json(args.queries)
    queries = {r['task']['task_id']: HistoricalQuery(TaskContext.from_dict(r['task']),
               r['bug_cluster_id'], r['fix_id'], tuple(r.get('aliases', [])),
               tuple(r.get('copied_from', [])), r.get('exposed', False)) for r in query_rows}
    verifications = {(r['issue_id'], r['fix_id']): r for r in read_json(args.verifications)['results']
                     if r['verified_resolution']}
    qids = {q for q, _ in expected}
    if set(manifest['oracle_input_hashes']) != qids:
        raise ValueError('prepared oracle identity coverage changed')
    for qid in qids:
        query = queries[qid]
        if query.exposed:
            raise ValueError('exposed query cannot create historical supervision')
        query.task.verify()
        if oracle_input_hashes(query, verifications[(qid, query.fix_id)], args.controls_dir) != \
                manifest['oracle_input_hashes'][qid]:
            raise ValueError('prepared historical label oracle changed')
    seen = set()
    for item in manifest['packets']:
        key = (item['query_id'], item['candidate_id'])
        if key not in expected or key in seen or item['id'] != digest(key)[:24]:
            raise ValueError('prepared population has missing/duplicate/foreign candidate identity')
        seen.add(key)
        path = Path(item['packet_path'])
        if path.is_symlink() or path.resolve().parent != packet_root.resolve():
            raise ValueError('prepared evidence path escapes the frozen packet directory')
        packet = validate_packet(read_json(path))
        example = expected[key]
        query = queries[key[0]]
        sources = tuple(SourceRecord.from_dict(row['source']) for row in packet['candidate_sources'])
        policy = candidate_policy(query, example['catalog_cutoff'], isolation)
        if isolation is not None:
            isolation.verify_sources(sources)
        for source in sources:
            policy.check(source)
        expected_identity = {'bug_cluster_id': query.bug_cluster_id, 'fix_id': query.fix_id,
                             'aliases': list(query.aliases), 'copied_from': list(query.copied_from),
                             'exposed': query.exposed}
        if (packet['packet_sha256'] != item['packet_sha256'] or
                (packet['query_id'], packet['candidate_id']) != key or
                packet['candidate_kind'] != item['candidate_kind'] or
                packet['public_task_sha256'] != digest(example['task_input']) or
                packet['candidate_sha256'] != digest(example['candidate']) or
                packet['catalog_sha256'] != example['temporal_catalog_sha256'] or
                packet['catalog_cutoff'] != example['catalog_cutoff'] or
                packet['query_identity'] != expected_identity or
                packet['main_cutoff'] != dataset['main_cutoff'] or
                packet['training_cutoff'] != dataset['training_cutoff']):
            raise ValueError('prepared evidence detached from its authoritative frozen candidate')
    if seen != set(expected):
        raise ValueError('prepared review omitted frozen candidate/query pairs')
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('dataset', 'queries', 'references', 'plans', 'verifications', 'controls-dir', 'output-dir'):
        parser.add_argument('--' + key, type=Path, required=True)
    parser.add_argument('--causal-isolation', type=Path,
                        help='Accepted host-only causal index required by the frozen dataset')
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--prepared-population', type=Path)
    parser.add_argument('--model')
    parser.add_argument('--base-url')
    parser.add_argument('--api-key-env', default='AREX_LLM_API_KEY')
    parser.add_argument('--http-backend', choices=['native', 'windows_pipe'], default='native')
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError('preserve historical applicability reviews; use a new version')
    args.output_dir.mkdir(parents=True)
    try:
        if args.prepared_population:
            manifest = validate_population(read_json(args.prepared_population), args,
                                           args.prepared_population.parent / 'packets')
            write_json(args.output_dir / 'reused-population.json', manifest)
        else:
            manifest = prepare(args)
            validate_population(manifest, args, args.output_dir / 'packets')
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as error:
        write_json(args.output_dir / 'preparation-failure.json', {
            'failure_type': type(error).__name__, 'failure_reason': safe_text(str(error)),
            'prepared_population_validated': False, 'model_calls': 0,
            'labels_created': 0, 'formal_SWE_runs': 0,
        })
        raise
    if args.prepare_only:
        print(json.dumps({'prepared_packets': len(manifest['packets']), 'model_calls': 0,
                          'labels_created': 0, 'formal_SWE_runs': 0}))
        return 0
    if not args.model or not args.base_url:
        parser.error('actual independent reviews require model and base URL')
    accepted, rows = [], []
    for item in manifest['packets']:
        transport, ledger = None, None
        try:
            packet = read_json(Path(item['packet_path']))
            validate_packet(packet)
            if packet['packet_sha256'] != item['packet_sha256']:
                raise ValueError('prepared historical evidence packet changed')
            transport = transport_from_args(args)
            transport.config = replace(transport.config, max_output_tokens=5000,
                                       timeout_seconds=180, stream_responses=True)
            ledger = BudgetLedger(BudgetCaps(history_tokens=60000, model_tokens=1000000))
            result = review_applicability(packet, transport, ledger,
                                          reviewer='fresh-context-evidence-review:' + args.model)
            if result['label'] is not None:
                accepted.append(result['label'])
        except (ValueError, RuntimeError, OSError, KeyError, TypeError) as error:
            result = {'status': 'review_protocol_or_infrastructure_failure',
                      'failure_type': type(error).__name__,
                      'failure_reason': safe_text(str(error), [transport.config.api_key] if transport else []),
                      'label': None, 'no_semantic_grade_filled_by_host': True,
                      'budget': ledger.snapshot() if ledger else None}
        if transport is not None:
            write_json(args.output_dir / 'audits' / (item['id'] + '-transcript.json'),
                       {'calls': transport.calls, 'transcripts': transport.transcripts})
        result.update({'packet_sha256': item['packet_sha256'],
                       'model_calls': len(transport.calls) if transport else 0,
                       'formal_SWE_runs': 0})
        write_json(args.output_dir / 'audits' / (item['id'] + '-review.json'), result)
        rows.append({'query_id': item['query_id'], 'candidate_id': item['candidate_id'],
                     'status': result.get('status', 'review_completed'),
                     'applicability': result.get('label', {}).get('applicability')
                     if result.get('label') else None,
                     'model_calls': result['model_calls']})
        write_json(args.output_dir / 'labels.json', accepted)
        write_json(args.output_dir / 'progress.json', {'completed': len(rows),
                   'scheduled': len(manifest['packets']), 'accepted_labels': len(accepted),
                   'results': rows, 'formal_SWE_runs': 0})
    write_json(args.output_dir / 'completion.json', {'results': rows,
               'accepted_labels': len(accepted), 'formal_SWE_runs': 0,
               'human_reviewed': False, 'independent_model_family': False,
               'repair_utility_established': False})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
