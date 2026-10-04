import copy
import importlib.util
import json
import subprocess
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_temporal_ranker_training import make_dataset

from arex_skill_graph.action_contracts import digest

_spec = importlib.util.spec_from_file_location(
    'review_historical_applicability_cli',
    Path(__file__).resolve().parents[1] / 'experiments/review_historical_applicability.py',
)
_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cli)


def test_source_discovery_includes_production_and_assertion_owners():
    diff = {'paths': ['tests/test_gate.py'],
            'production_diff': '--- a/checker.py\n+++ b/checker.py\n',
            'regression_diff': '--- a/tests/test_gate.py\n+++ b/tests/test_gate.py\n'}
    assert _cli.changed_source_paths(diff) == ['checker.py', 'tests/test_gate.py']
    diff['production_diff'] = '--- /dev/null\n+++ b/new_gate.py\n'
    assert 'new_gate.py' in _cli.changed_source_paths(diff)


@pytest.mark.parametrize('path', ['../secret', '/etc/passwd', 'dir/../secret', 'dir\\secret'])
def test_source_discovery_rejects_escaping_paths(path):
    with pytest.raises(ValueError, match='unsafe'):
        _cli.changed_source_paths({'paths': [path], 'production_diff': '', 'regression_diff': ''})


def test_oracle_reads_pinned_base_bytes_not_later_worktree(tmp_path, monkeypatch):
    root = tmp_path / 'checkout'
    root.mkdir()
    for name in ('checker.py', 'test_gate.py'):
        (root / name).write_text('base_owner = True\n')
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture',
                    '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'base'], check=True)
    base = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
    (root / 'checker.py').write_text('later_private_repair = True\n')
    task = SimpleNamespace(task_id='current/repo:42', repository='current/repo', root=str(root),
                           base_commit=base)
    query = SimpleNamespace(task=task, bug_cluster_id=task.task_id, fix_id='current/repo:pr:43')
    report = {'identity': {'issue_id': task.task_id, 'base_commit': base, 'fix_id': query.fix_id,
                           'merge_commit': 'a' * 40, 'repair_available_at': '2020-06-02T00:00:00Z'},
              'qualification_scope': 'changed-test-files-with-original-base-control',
              'whole_project_regression_checked': False}
    diff = {'available_at': report['identity']['repair_available_at'], 'paths': ['test_gate.py'],
            'production_diff': '--- a/checker.py\n+++ b/checker.py\n',
            'regression_diff': '--- a/test_gate.py\n+++ b/test_gate.py\n'}
    verification = tmp_path / 'verified/verification.json'
    verification.parent.mkdir()
    verification.write_text(json.dumps(report))
    (verification.parent / 'historical-diff.json').write_text(json.dumps(diff))
    controls_dir = tmp_path / 'controls'
    controls = {'passed': True, 'same_protocol': True, 'task_id': task.task_id,
                'base_commit': base, 'solver_input_contains_control_results': False}
    control_path = controls_dir / 'current__repo-42/controls.json'
    control_path.parent.mkdir(parents=True)
    control_path.write_text(json.dumps(controls))
    checked = []
    monkeypatch.setattr(_cli, 'validate_historical_qualification',
                        lambda report, source, policy: checked.append((source, policy)))
    evidence = _cli.historical_oracle(query, {'verification_path': str(verification)},
                                       controls_dir, '2024-01-01T00:00:00Z')
    code = [e for e in evidence if e['role'] == 'current_code']
    assert {e['path'] for e in code} == {'checker.py', 'test_gate.py'}
    assert all(e['text'] == 'base_owner = True\n' and e['base_commit'] == base for e in code)
    assert len(checked) == 1 and checked[0][0].revision == 'a' * 40
    private = [e for e in evidence if e['role'] == 'privileged_label_oracle']
    assert len(private) == 1 and private[0]['learned_candidate_resource'] is False
    controls['base_commit'] = 'b' * 40
    control_path.write_text(json.dumps(controls))
    with pytest.raises(ValueError, match='matching independent causal controls'):
        _cli.historical_oracle(query, {'verification_path': str(verification)},
                                controls_dir, '2024-01-01T00:00:00Z')


def prepared_fixture(tmp_path, monkeypatch):
    dataset, package, _task, queries, _labels, _provider = make_dataset(tmp_path)
    values = {'queries': [asdict(q) for q in queries], 'references': [package.reference],
              'plans': {}, 'verifications': {'results': [
                  {'issue_id': q.task.task_id, 'fix_id': q.fix_id, 'verified_resolution': True}
                  for q in queries]}}
    dataset['source_input_hashes'] = {k: digest(v) for k, v in values.items()}
    dataset['dataset_sha256'] = digest({k: v for k, v in dataset.items() if k != 'dataset_sha256'})
    values['dataset'] = dataset
    paths = {}
    for key, value in values.items():
        paths[key] = tmp_path / (key + '.json')
        paths[key].write_text(json.dumps(value))
    args = SimpleNamespace(**paths, controls_dir=tmp_path / 'controls', output_dir=tmp_path / 'prepared')

    def oracle(query, *_):
        source = Path(query.task.root) / 'checker.py'
        return [
            _cli.entry('current:' + query.task.task_id, 'current_code', source.read_text(),
                       path='checker.py', base_commit=query.task.base_commit),
            _cli.entry('private:' + query.task.task_id, 'privileged_label_oracle',
                       'Synthetic qualification controls; no model or repair execution.',
                       learned_candidate_resource=False,
                       historical_repair_available_at='2023-07-01T00:00:00Z'),
        ]

    monkeypatch.setattr(_cli, 'historical_oracle', oracle)
    monkeypatch.setattr(_cli, 'oracle_input_hashes', lambda *_: {'synthetic': 'e' * 64})
    monkeypatch.setattr(_cli, 'transport_from_args',
                        lambda *_: pytest.fail('prepare-only must not contact a model'))
    manifest = _cli.prepare(args)
    return args, manifest


def seal_population(manifest):
    manifest['population_sha256'] = digest({k: v for k, v in manifest.items() if k != 'population_sha256'})
    return manifest


def test_preparation_seals_all_pairs_with_zero_calls_and_labels(tmp_path, monkeypatch):
    args, manifest = prepared_fixture(tmp_path, monkeypatch)
    assert len(manifest['packets']) == 6
    assert manifest['model_calls'] == manifest['labels_created'] == 0
    _cli.validate_population(manifest, args, args.output_dir / 'packets')
    assert not (args.output_dir / 'labels.json').exists()


@pytest.mark.parametrize('change', ['omit', 'duplicate', 'candidate', 'oracle', 'cutoff'])
def test_reuse_rejects_subset_duplicate_or_detached_frozen_evidence(tmp_path, monkeypatch, change):
    args, original = prepared_fixture(tmp_path, monkeypatch)
    manifest = copy.deepcopy(original)
    if change == 'omit':
        manifest['packets'].pop()
    elif change == 'duplicate':
        manifest['packets'].append(copy.deepcopy(manifest['packets'][0]))
    elif change == 'candidate':
        item = manifest['packets'][0]
        path = Path(item['packet_path'])
        packet = json.loads(path.read_text())
        packet['candidate']['mechanism'] = 'Different unsupported causal mechanism'
        packet['candidate_sha256'] = digest(packet['candidate'])
        packet['packet_sha256'] = digest({k: v for k, v in packet.items() if k != 'packet_sha256'})
        item['packet_sha256'] = packet['packet_sha256']
        path.write_text(json.dumps(packet))
    elif change == 'oracle':
        monkeypatch.setattr(_cli, 'oracle_input_hashes', lambda *_: {'synthetic': 'f' * 64})
    else:
        manifest['training_cutoff'] = '2022-01-01T00:00:00Z'
    with pytest.raises(ValueError, match='omitted|duplicate|detached|oracle changed|temporal identity'):
        _cli.validate_population(seal_population(manifest), args, args.output_dir / 'packets')
