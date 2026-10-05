import hashlib

import pytest

from arex_skill_graph.historical_replay_controls import project_replay_production_diff


def section(before, after=None, mode=""):
    after = before if after is None else after
    return (
        f"diff --git a/{before} b/{after}\n{mode}"
        f"--- a/{before}\n+++ b/{after}\n@@ -1 +1 @@\n-old\n+new\n"
    )


def test_default_replay_retains_entire_native_diff():
    raw = section("ChangeLog") + section("pylint/checkers/classes.py")
    actual, witness = project_replay_production_diff(raw)
    assert actual == raw
    assert witness["excluded_sections"] == []
    assert witness["functional_control_scope_only"] is False


def test_functional_projection_preserves_every_code_and_configuration_hunk_byte():
    code = section("pylint/checkers/classes.py")
    config = section("setup.py")
    tests = section("tests/functional/ChangeLog")
    narrative = section("README.md")
    raw = section("CONTRIBUTORS.txt") + code + section("ChangeLog") + config + tests + narrative
    actual, witness = project_replay_production_diff(raw, "omit-release-metadata")
    assert actual == code + config + tests + narrative
    assert {x["after_path"] for x in witness["excluded_sections"]} == {
        "ChangeLog",
        "CONTRIBUTORS.txt",
    }
    assert witness["native_production_sha256"] == hashlib.sha256(raw.encode()).hexdigest()
    assert witness["controlled_production_sha256"] == hashlib.sha256(actual.encode()).hexdigest()
    assert witness["regression_assertions_modified"] is False
    assert witness["native_source_records_replaced"] is False
    assert witness["actor_may_read_known_repair"] is False
    assert witness["retained_section_bytes_unchanged"] is True


def test_release_note_exclusion_does_not_remove_documentation_programs():
    raw = section("doc/whatsnew/2.7.rst") + section("doc/ext/feature.py") + section("src/code.py")
    actual, witness = project_replay_production_diff(raw, "omit-release-metadata")
    assert actual == section("doc/ext/feature.py") + section("src/code.py")
    assert len(witness["excluded_sections"]) == 1


@pytest.mark.parametrize(
    "before,after,mode",
    [
        ("source.py", "ChangeLog", ""),
        ("ChangeLog", "source.py", ""),
        ("ChangeLog", "ChangeLog", "new mode 100755\n"),
    ],
)
def test_renames_and_executable_changes_cannot_masquerade_as_release_metadata(before, after, mode):
    raw = section(before, after, mode)
    actual, witness = project_replay_production_diff(raw, "omit-release-metadata")
    assert actual == raw
    assert not witness["excluded_sections"]


@pytest.mark.parametrize(
    "raw", ["not a Git diff\n", section("../escape.py"), section(".git/config")]
)
def test_malformed_or_escaping_projection_is_rejected(raw):
    with pytest.raises(ValueError):
        project_replay_production_diff(raw, "omit-release-metadata")


def test_metadata_only_projection_cannot_qualify_a_no_op_repair():
    with pytest.raises(ValueError, match="no production repair"):
        project_replay_production_diff(section("ChangeLog"), "omit-release-metadata")


def test_unknown_projection_cannot_silently_change_native_repair():
    with pytest.raises(ValueError, match="unsupported"):
        project_replay_production_diff(section("source.py"), "arbitrary-code-filter")


@pytest.mark.parametrize(
    "mode",
    [
        "index 1111111..2222222 100755\n",
        "index 1111111..2222222 120000\n",
        "new file mode 120000\n",
        "GIT binary patch\n",
    ],
)
def test_existing_executables_symlinks_and_binary_sections_are_retained(mode):
    raw = section("ChangeLog", mode=mode)
    actual, witness = project_replay_production_diff(raw, "omit-release-metadata")
    assert actual == raw
    assert not witness["excluded_sections"]
