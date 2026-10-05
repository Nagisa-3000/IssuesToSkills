import copy
import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "original_release_query_preparation",
    Path(__file__).resolve().parents[1] / "experiments/prepare_original_release_queries.py",
)
_cli = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cli)


def source(at, filename="example-1.0.tar.gz"):
    return {
        "packagetype": "sdist",
        "upload_time_iso_8601": at,
        "filename": filename,
        "url": "https://files.pythonhosted.org/source/" + filename,
        "size": 10,
        "digests": {"sha256": "a" * 64},
    }


def test_select_latest_stable_pre_input_source_without_future_or_yank_labels():
    registry = {
        "releases": {
            "1.0": [source("2020-01-01T00:00:00Z")],
            "1.1": [{**source("2020-02-01T00:00:00Z"), "yanked": True}],
            "1.2": [source("2020-04-01T00:00:00Z")],
            "2.0rc1": [source("2020-02-01T00:00:00Z")],
        }
    }
    actual = _cli.select_source(registry, "example", "2020-03-01T00:00:00Z")
    assert actual["version"] == "1.1" and "yanked" not in actual["urls"][0]
    registry["releases"]["1.1"][0]["yanked"] = False
    assert _cli.select_source(registry, "example", "2020-03-01T00:00:00Z") == actual


def test_source_equal_to_input_time_is_not_eligible():
    registry = {"releases": {"1.0": [source("2020-01-01T00:00:00Z")]}}
    with pytest.raises(ValueError, match="strictly before"):
        _cli.select_source(registry, "example", "2020-01-01T00:00:00Z")


def test_ambiguous_latest_source_cannot_fall_back_to_convenient_older_version():
    registry = {
        "releases": {
            "1.0": [source("2020-01-01T00:00:00Z")],
            "1.1": [source("2020-02-01T00:00:00Z"), source("2020-02-01T00:00:01Z")],
        }
    }
    with pytest.raises(ValueError, match="ambiguous"):
        _cli.select_source(registry, "example", "2020-03-01T00:00:00Z")


@pytest.mark.parametrize(
    "change",
    [
        {"url": "https://example.invalid/archive.tar.gz"},
        {"filename": "../example-1.0.tar.gz"},
        {"filename": "dir\\archive.tar.gz"},
        {"digests": {"sha256": "invalid"}},
        {"size": 64 * 1024**2 + 1},
    ],
)
def test_untrusted_source_identity_is_rejected_before_download(change):
    item = source("2020-01-01T00:00:00Z")
    item.update(copy.deepcopy(change))
    with pytest.raises(ValueError, match="unsafe"):
        _cli.select_source({"releases": {"1.0": [item]}}, "example", "2020-02-01T00:00:00Z")
