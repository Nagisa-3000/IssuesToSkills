import copy
import json

import pytest

from arex_skill_graph.action_contracts import digest
from arex_skill_graph.adaptive_budget import BudgetCaps, BudgetLedger
from arex_skill_graph.applicability_supervision import (
    CHECK_KEYS, label_from_review, review_applicability, seal_packet,
    validate_packet, validate_proposal,
)

SHA = 'a' * 64
BASE = 'b' * 40


def artifact(ident, role, text, **metadata):
    return {'id': ident, 'role': role, 'text': text, 'text_sha256': digest(text), **metadata}


def packet():
    task = {'task_id': 'current/repo:42', 'repository': 'current/repo', 'base_commit': BASE,
            'input_available_at': '2020-06-01T00:00:00Z',
            'public_problem': 'An async node is missed by a synchronous-only classification gate.'}
    candidate = {'id': 'workflow:history', 'candidate_kind': 'workflow', 'package_hashes': [SHA]}
    source = {'id': 'source:history', 'repository': 'history/repo',
              'bug_cluster_id': 'history/repo:1', 'fix_id': 'history/repo:pr:2',
              'revision': 'c' * 40, 'available_at': '2020-01-01T00:00:00Z',
              'evidence_refs': ['history:implementation', 'history:assertions'],
              'verified_resolution': True}
    evidence = [
        artifact('query', 'public_query', task['public_problem']),
        artifact('code', 'current_code', 'gate accepts the synchronous AST node only',
                 path='checker.py', base_commit=BASE),
        artifact('history', 'candidate_history', 'Historical omission of a supported async node.',
                 knowledge_available_at=source['available_at'],
                 package_sha256=SHA, source_ids=[source['id']]),
        artifact('oracle', 'privileged_label_oracle', 'Independent causal controls and assertion diff.',
                 learned_candidate_resource=False, historical_repair_available_at='2020-06-02T00:00:00Z'),
    ]
    return seal_packet(task, candidate, evidence, catalog_cutoff=task['input_available_at'],
                       catalog_sha256='d' * 64, main_cutoff='2024-01-01T00:00:00Z',
                       training_cutoff='2021-01-01T00:00:00Z',
                       query_identity={'bug_cluster_id': 'current/repo:42',
                                       'fix_id': 'current/repo:pr:43', 'aliases': [],
                                       'copied_from': [], 'exposed': False},
                       candidate_sources=[{'package_sha256': SHA, 'source': source}])


def reseal(value):
    value['packet_sha256'] = digest({k: v for k, v in value.items() if k != 'packet_sha256'})
    return value


def proposal(value, *, grade='adaptively_usable', overrides=None):
    overrides = overrides or {}
    return {'query_id': value['query_id'], 'candidate_id': value['candidate_id'],
            'grade': grade, 'limitations': ['Same model family; no repair efficacy established.'],
            'checks': [{'key': k, 'status': overrides.get(k, 'PASS'),
                        'evidence_refs': ['history', 'code', 'oracle'],
                        'rationale': 'Compare the historical causal contract and the actual base evidence.'}
                       for k in CHECK_KEYS]}


def review(value, proposed, **changes):
    return {'query_id': value['query_id'], 'candidate_id': value['candidate_id'],
            'proposal_sha256': digest(proposed), 'reviewed_grade': proposed['grade'],
            'verdict': 'ACCEPT',
            'check_reviews': [{'key': k, 'status': 'SUPPORTED',
                               'evidence_refs': ['history', 'code', 'oracle'],
                               'rationale': 'The cited evidence supports this precise claim.'}
                              for k in CHECK_KEYS],
            'rationale': 'All claims supported within the reported causal-control scope.', **changes}


def test_current_code_or_historical_evidence_change_invalidates_packet():
    value = packet()
    value['evidence'][1]['text'] = 'a different owner'
    with pytest.raises(ValueError, match='content changed'):
        validate_packet(value)
    reseal(value)
    with pytest.raises(ValueError, match='identity or content'):
        validate_packet(value)


@pytest.mark.parametrize('field,value', [
    ('main_cutoff', '2020-06-01T00:00:00Z'),
    ('catalog_cutoff', '2020-06-02T00:00:00Z'),
    ('catalog_cutoff', '2020-05-01T00:00:00Z'),
])
def test_query_and_catalog_cutoffs_cannot_be_relaxed(field, value):
    item = packet()
    item[field] = value
    with pytest.raises(ValueError, match='cutoff|temporal split'):
        validate_packet(reseal(item))


def test_development_review_uses_only_training_cutoff_catalog():
    item = packet()
    item['public_task']['input_available_at'] = '2022-01-01T00:00:00Z'
    item['input_available_at'] = item['public_task']['input_available_at']
    item['public_task_sha256'] = digest(item['public_task'])
    item['catalog_cutoff'] = item['training_cutoff']
    validate_packet(reseal(item))
    item['catalog_cutoff'] = item['input_available_at']
    with pytest.raises(ValueError, match='temporal split'):
        validate_packet(reseal(item))


@pytest.mark.parametrize('change', ['self_alias', 'duplicate_copy', 'same_fix', 'same_cluster', 'future'])
def test_query_answers_duplicates_and_future_history_are_excluded(change):
    item = packet()
    source = item['candidate_sources'][0]['source']
    if change == 'self_alias':
        source['aliases'] = [item['query_id']]
    elif change == 'duplicate_copy':
        item['query_identity']['copied_from'] = [source['id']]
    elif change == 'same_fix':
        source['fix_id'] = item['query_identity']['fix_id']
    elif change == 'same_cluster':
        source['bug_cluster_id'] = item['query_identity']['bug_cluster_id']
    else:
        source['available_at'] = item['catalog_cutoff']
    with pytest.raises(ValueError, match='excluded|cutoff'):
        validate_packet(reseal(item))


def test_exposed_queries_and_wrong_current_base_are_rejected():
    item = packet()
    item['query_identity']['exposed'] = True
    with pytest.raises(ValueError, match='exposed'):
        validate_packet(reseal(item))
    item = packet()
    item['evidence'][1]['base_commit'] = 'e' * 40
    with pytest.raises(ValueError, match='exact public base'):
        validate_packet(reseal(item))


def test_privileged_oracle_can_postdate_query_but_cannot_be_learned():
    item = packet()
    validate_packet(item)
    item['privileged_evidence_is_ranker_input'] = True
    with pytest.raises(ValueError, match='label-evaluator-only'):
        validate_packet(reseal(item))
    item = packet()
    item['evidence'][3]['learned_candidate_resource'] = True
    with pytest.raises(ValueError, match='learned resource'):
        validate_packet(reseal(item))
    item = packet()
    item['candidate']['gold_patch'] = 'private evaluator bytes'
    item['candidate_sha256'] = digest(item['candidate'])
    with pytest.raises(ValueError, match='evaluator-only'):
        validate_packet(reseal(item))


@pytest.mark.parametrize('change', ['source_date', 'source_id', 'package_hash', 'missing_package'])
def test_evidence_provenance_cannot_be_backdated_or_detached(change):
    item = packet()
    if change == 'source_date':
        item['evidence'][2]['knowledge_available_at'] = '2019-01-01T00:00:00Z'
    elif change == 'source_id':
        item['evidence'][2]['source_ids'] = ['unrelated-source']
    elif change == 'package_hash':
        item['evidence'][2]['package_sha256'] = 'f' * 64
    else:
        item['candidate']['package_hashes'].append('f' * 64)
        item['candidate_sha256'] = digest(item['candidate'])
    with pytest.raises(ValueError, match='backdated|provenance|coverage'):
        validate_packet(reseal(item))


@pytest.mark.parametrize('refs', [['history'], ['oracle'], ['history', 'invented-observation']])
def test_every_claim_requires_both_candidate_and_current_evidence(refs):
    item = packet()
    proposed = proposal(item)
    proposed['checks'][0]['evidence_refs'] = refs
    with pytest.raises(ValueError, match='both candidate|attributable evidence'):
        validate_proposal(proposed, item)


@pytest.mark.parametrize('grade,overrides', [
    ('adaptively_usable', {'binding': 'UNKNOWN'}),
    ('unrelated', {}),
    ('probe_only', {'mechanism': 'UNKNOWN'}),
    ('probe_only', {'binding': 'FAIL'}),
])
def test_grade_must_follow_supported_and_unresolved_checks(grade, overrides):
    item = packet()
    with pytest.raises(ValueError, match='needs'):
        validate_proposal(proposal(item, grade=grade, overrides=overrides), item)


@pytest.mark.parametrize('grade,overrides', [
    ('adaptively_usable', {}),
    ('unrelated', {'owner': 'FAIL'}),
    ('probe_only', {'binding': 'UNKNOWN'}),
])
def test_accepted_reviews_create_only_semantic_labels(grade, overrides):
    item = packet()
    proposed = proposal(item, grade=grade, overrides=overrides)
    label = label_from_review(item, proposed, review(item, proposed), reviewer='synthetic-review')
    assert label.label_source == 'evidence_review' and label.applicability == grade
    assert label.outcome is label.regression_pass is label.measured_cost is None
    assert label.operational_mode is None
    assert label.evidence_refs[0].startswith('applicability-evidence-review:')


@pytest.mark.parametrize('verdict', ['REJECT', 'UNKNOWN'])
def test_rejected_or_uncertain_review_never_creates_a_label(verdict):
    item = packet()
    proposed = proposal(item)
    assert label_from_review(item, proposed, review(item, proposed, verdict=verdict),
                             reviewer='synthetic-review') is None


def test_unknown_proposal_and_unsupported_acceptance_do_not_authorize_labels():
    item = packet()
    proposed = proposal(item, grade='unknown', overrides={'mechanism': 'UNKNOWN'})
    assert label_from_review(item, proposed, review(item, proposed), reviewer='synthetic-review') is None
    proposed = proposal(item)
    audited = review(item, proposed)
    audited['check_reviews'][0]['status'] = 'UNKNOWN'
    with pytest.raises(ValueError, match='contradicts'):
        label_from_review(item, proposed, audited, reviewer='synthetic-review')
    with pytest.raises(ValueError, match='proposal identity'):
        label_from_review(item, proposed, review(item, proposed, proposal_sha256='f' * 64),
                          reviewer='synthetic-review')


def test_proposal_is_not_a_label_and_independent_call_gets_original_evidence():
    item = packet()
    proposed = proposal(item)

    class Transport:
        calls = []

        def complete(self, **call):
            self.calls.append(copy.deepcopy(call))
            return proposed if len(self.calls) == 1 else review(item, proposed)

    transport = Transport()
    result = review_applicability(item, transport,
                                 BudgetLedger(BudgetCaps(history_tokens=60000)),
                                 reviewer='synthetic-review')
    assert len(transport.calls) == 2
    assert transport.calls[0]['system'] != transport.calls[1]['system']
    first = json.loads(transport.calls[0]['user'])
    assert first['evidence_packet'] == item
    assert first['allowed_citations'] == [{'id': e['id'], 'role': e['role']} for e in item['evidence']]
    assert json.loads(transport.calls[1]['user'])['allowed_citations'] == first['allowed_citations']
    second = json.loads(transport.calls[1]['user'])
    assert second['evidence_packet'] == item and second['proposal_sha256'] == digest(proposed)
    assert result['label']['label_source'] == 'evidence_review'
    assert result['human_reviewed'] is False and result['independent_model_family'] is False
    assert result['repair_utility_established'] is False


def test_invalid_proposal_stops_before_review_and_cannot_manufacture_supervision():
    item = packet()

    class Transport:
        calls = []

        def complete(self, **call):
            self.calls.append(call)
            return proposal(item, grade='adaptively_usable', overrides={'binding': 'UNKNOWN'})

    transport = Transport()
    with pytest.raises(ValueError, match='all six'):
        review_applicability(item, transport, BudgetLedger(BudgetCaps(history_tokens=60000)),
                             reviewer='synthetic-review')
    assert len(transport.calls) == 1


def test_response_schemas_enumerate_artifacts_not_inner_episode_or_anchor_ids():
    from arex_skill_graph.applicability_supervision import (
        PROPOSAL_SCHEMA, REVIEW_SCHEMA, evidence_response_schema,
    )

    item = packet()
    proposed = proposal(item)
    before = copy.deepcopy(PROPOSAL_SCHEMA)
    schemas = [(evidence_response_schema(PROPOSAL_SCHEMA, item), 'checks'),
               (evidence_response_schema(REVIEW_SCHEMA, item, proposal=proposed), 'check_reviews')]
    for schema, key in schemas:
        ids = schema['properties'][key]['items']['properties']['evidence_refs']['items']['enum']
        assert ids == [e['id'] for e in item['evidence']]
        assert 'current:issue' not in ids and 'history:implementation' not in ids
        assert schema['properties']['query_id']['const'] == item['query_id']
        assert schema['properties']['candidate_id']['const'] == item['candidate_id']
    assert schemas[1][0]['properties']['proposal_sha256']['const'] == digest(proposed)
    assert PROPOSAL_SCHEMA == before


def test_inner_source_citations_are_rejected_without_host_alias_repair():
    item = packet()
    proposed = proposal(item)
    proposed['checks'][0]['evidence_refs'] = ['history:implementation', 'current:issue']

    class Transport:
        calls = []

        def complete(self, **call):
            self.calls.append(call)
            return proposed

    transport = Transport()
    with pytest.raises(ValueError, match='attributable evidence'):
        review_applicability(item, transport, BudgetLedger(BudgetCaps(history_tokens=60000)),
                             reviewer='synthetic-review')
    assert len(transport.calls) == 1
