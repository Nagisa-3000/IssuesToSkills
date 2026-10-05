# Historical episode

Authoritative source: `pylint-dev/pylint:7461:repair:fb30fe09d74d`.

The [title](evidence/title.md) described a crash when assigning a dictionary value to `None`. The [body](evidence/body.md) located the failure more precisely: the mutation-during-iteration checker read `iter_obj.name` when the iterator was an `Attribute` node.

The reproduction loops over `self.request_data`, copies the dictionary to `temp_post_data`, and assigns `temp_post_data[key] = None`. The reporter stated that removing this assignment or changing iteration to `.items()` avoided the crash. These are reported observations, not independently established historical executions.

## Historical locators and repair

- Checker: `pylint/checkers/modified_iterating_checker.py`.
- Dictionary owner: `ModifiedIterationChecker._modified_iterating_dict_cond`.
- Related helpers: `_modified_iterating_list_cond` and `_modified_iterating_set_cond`.
- Functional fixture: `tests/functional/m/modified_iterating.py`, class `MyClass2`.
- Release fragment: `doc/whatsnew/fragments/7461.bugfix`.

The [merged implementation](evidence/fix.md) narrows the three helper iterator annotations to `nodes.Name | nodes.Attribute`. In the dictionary condition, after existing guards and inference comparison, it selects `iter_obj.attrname` for `nodes.Attribute` and `iter_obj.name` otherwise. It retains the comparison against `node.targets[0].value.name`.

The [committed regression](evidence/regression.md) initializes `self.attribute = {}`, loops over that attribute, copies it into `tmp`, and assigns `tmp[key] = None`. It has no expected mutation diagnostic and says that no diagnostic should arise because a copy was made. Historical test execution and CI status are unknown.

The linked Workflow and Actions reconstruct the supported semantic repair and its verification obligations. They do not claim that an inspection session or validation execution was recorded historically.

## Validation-only qualification review

The supplied complete qualification controls pin:

- Original base: `f195969943a8f7949f0caab0f04ee15d1311d2b5`.
- Historical fixed revision: `fb30fe09d74de3dad2472309fb24396b65b8b81d`.
- Issue: `pylint-dev/pylint:7461`.
- Fix: `pylint-dev/pylint:pr:7472`.
- Verified resolution relationship: `direct_closure`.
- Public repair availability: `2022-09-16T07:24:19Z`.

At `2026-10-04T15:31:51.466661+00:00`, the original base passed 18 selected functional cases. Adding the committed regression to that base caused `modified_iterating` to fail with the unsupported `Attribute.name` access; 17 other selected cases passed. The historical fixed version passed all 18 selected cases.

The 18 selected identities were `mapping_context`, `mapping_context_py3`, `membership_protocol`, `membership_protocol_py3`, `metaclass_attr_access`, `method_cache_max_size_none`, `method_cache_max_size_none_py39`, `method_hidden`, `misplaced_bare_raise`, `misplaced_format_function`, `misplaced_future`, `mixin_class_rgx`, `modified_iterating`, `module___dict__`, `monkeypatch_method`, `multiple_imports`, `multiple_statements`, and `multiple_statements_single_line`.

All three controls used matching supplied runtime digests, adopted workspaces, and no timeout. Their exit codes were respectively 0, 1, and 0. The report establishes one regression-added fail-to-pass case and 18 original-base-to-fixed pass-to-pass cases. The original base's passing `modified_iterating` case did not yet contain the added regression.

Qualification scope: `changed-test-files-with-original-base-control`.

Exact scope limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

This is later validation of public historical artifacts, not historical CI, pre-cutoff learned content, a formal SWE run, or execution of the authored Skill evals. Replay commands and contemporary runtime details are not repair mechanisms. Qualification hashes and control metadata are recorded in [provenance.json](provenance.json).
