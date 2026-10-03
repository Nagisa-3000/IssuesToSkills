"""Focused constructor oracles for a portable, synthetic package-use task."""

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import unittest
from pathlib import Path

BUILD_CLIENT = None


class EndpointContractTests(unittest.TestCase):
    def setUp(self):
        self.calls = []

    def sdk(self, **kwargs):
        self.calls.append(kwargs)
        return kwargs

    def options(self, config, environment=None):
        return BUILD_CLIENT(config, environment or {}, self.sdk)

    def test_explicit_endpoint_wins(self):
        options = self.options(
            {"mode": "direct", "endpoint": "https://caller.invalid/v1"},
            {"PRIMARY_ENDPOINT": "https://fallback.invalid/v1"},
        )
        self.assertEqual(options["http_options"]["base_url"], "https://caller.invalid/v1")

    def test_cloud_environment(self):
        options = self.options(
            {"mode": "cloud"},
            {
                "PRIMARY_ENDPOINT": "https://primary.invalid/v1",
                "CLOUD_ENDPOINT": "https://cloud.invalid/v1",
            },
        )
        self.assertEqual(options["http_options"]["base_url"], "https://cloud.invalid/v1")

    def test_direct_environment(self):
        options = self.options(
            {"mode": "direct"},
            {
                "PRIMARY_ENDPOINT": "https://primary.invalid/v1",
                "CLOUD_ENDPOINT": "https://cloud.invalid/v1",
            },
        )
        self.assertEqual(options["http_options"]["base_url"], "https://primary.invalid/v1")

    def test_no_environment_crossing(self):
        options = self.options({"mode": "direct"}, {"CLOUD_ENDPOINT": "https://cloud.invalid/v1"})
        self.assertEqual(options["http_options"], {})

    def test_cloud_mode_without_inference(self):
        self.assertIs(self.options({"mode": "cloud"})["cloud"], True)

    def test_explicit_false_provider_mode(self):
        self.assertIs(
            self.options(
                {"mode": "cloud", "provider_mode": False, "endpoint": "https://endpoint.invalid"}
            )["cloud"],
            False,
        )

    def test_explicit_true_provider_mode(self):
        self.assertIs(self.options({"mode": "direct", "provider_mode": True})["cloud"], True)

    def test_named_loopback_http(self):
        self.assertEqual(
            self.options({"mode": "direct", "endpoint": "http://localhost:8080/v1"})[
                "http_options"
            ]["base_url"],
            "http://localhost:8080/v1",
        )

    def test_numeric_loopback_http(self):
        self.assertEqual(
            self.options({"mode": "direct", "endpoint": "http://127.0.0.1:8080/v1"})[
                "http_options"
            ]["base_url"],
            "http://127.0.0.1:8080/v1",
        )

    def test_ipv6_loopback_http(self):
        self.assertEqual(
            self.options({"mode": "direct", "endpoint": "http://[::1]:8080/v1"})["http_options"][
                "base_url"
            ],
            "http://[::1]:8080/v1",
        )

    def test_remote_plaintext_refused_before_constructor(self):
        with self.assertRaises(ValueError):
            self.options({"mode": "direct", "endpoint": "http://remote.invalid/v1"})
        self.assertEqual(self.calls, [])

    def test_malformed_refused_before_constructor(self):
        with self.assertRaises(ValueError):
            self.options({"mode": "direct", "endpoint": "not-an-endpoint"})
        self.assertEqual(self.calls, [])

    def test_default_sdk_options(self):
        self.assertEqual(self.options({"mode": "direct"}), {"http_options": {}, "cloud": False})

    def test_unknown_provider_defers_before_constructor(self):
        with self.assertRaises(ValueError):
            self.options({"mode": "unknown", "endpoint": "https://endpoint.invalid"})
        self.assertEqual(self.calls, [])


def main():
    global BUILD_CLIENT
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("synthetic_endpoint_client", args.module)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    BUILD_CLIENT = module.build_client
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(EndpointContractTests)
    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    print(
        json.dumps(
            {
                "tests_run": result.testsRun,
                "passed": result.testsRun - len(result.failures) - len(result.errors),
                "failures": [test.id().split(".")[-1] for test, _ in result.failures],
                "errors": [test.id().split(".")[-1] for test, _ in result.errors],
                "success": result.wasSuccessful(),
            },
            sort_keys=True,
        )
    )
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
