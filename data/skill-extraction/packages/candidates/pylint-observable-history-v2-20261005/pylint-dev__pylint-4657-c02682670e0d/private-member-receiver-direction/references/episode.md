# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:4657:repair:c02682670e0d`.

The report described Pylint 2.9.3 and astroid 2.6.2 emitting W0238 for a private attribute mutated through `cls` in a classmethod even though a property read it through `self`. The expected behavior was no unused-private-member diagnostic.

The merged repair changed historical `pylint/checkers/classes.py`. Equal attribute names remained required. Instead of requiring equal receiver names, it recognized a `cls` assignment as used by `cls` or `self` reads, and a `self` assignment as used only by a `self` read. The implementation explicitly checks these names; it does not establish arbitrary alias or inheritance support.

Historical regression resources were:
- `tests/functional/u/unused/unused_private_member.py`
- `tests/functional/u/unused/unused_private_member.txt`

The fixture added the classmethod mutation/property read without an unused-private-member expectation. Its inverse-direction case assigned `self.__attr_c` but returned `cls.__attr_c`: the assignment retained an unused-private-member expectation, and unbound `cls` retained undefined-variable. The expected-output diff retained seven existing private-member diagnostics, added `HIGH` confidence annotations, and added the two negative-case diagnostics.

The changelog stated that the change fixed the false positive and closed #4657. The supplied historical evidence does not establish historical CI execution.

## Validation-only qualification audit

The complete supplied independent qualification controls were inspected. They pin:
- original base `6f066733e23a61d83580cd1898e6b8afab8fafea`;
- merge revision `c02682670e0d267d9e055347f3c9043f2550e205`;
- fix `pylint-dev/pylint:pr:4663`;
- issue `pylint-dev/pylint:4657`;
- a verified direct-closure relationship.

The check occurred at `2026-10-04T11:01:15.708132+00:00`, not in 2021. All controls had runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, consistent isolation, and no timeout.

Original base: exit 0, 18 selected tests passed.
Base with committed regressions: exit 1, target `tests.test_functional::test_functional[unused_private_member]` failed because of an unexpected unused-private-member diagnostic at line 116; 17 other tests passed.
Historical fixed: exit 0, all 18 selected tests passed.

The report lists one fail-to-pass transition from base-with-regression to fixed. Its 18 pass-to-pass entries compare original-base to fixed, including the target. Those are distinct controls.

Qualification scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; cross-project transfer is untested; this was not a formal SWE run. Contemporary runtime/log observations are validation-only provenance, not historical mechanisms or execution of the authored Skill. The report hash is retained in [provenance](provenance.json).

The source projection reports 12 other discussion entries but supplies no additional core evidence from them. No extra historical evidence IDs or mechanisms are inferred.
