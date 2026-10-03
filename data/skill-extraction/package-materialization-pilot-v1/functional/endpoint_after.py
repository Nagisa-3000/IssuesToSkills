"""Synthetic repair produced by the current agent using the retrieved package."""

from urllib.parse import urlsplit


def build_client(config, environment, sdk_factory):
    mode = config.get("mode")
    if mode not in {"direct", "cloud"}:
        raise ValueError("declared provider mode is required")

    # Action 1: resolve the endpoint at its configuration owner boundary.
    slot = "CLOUD_ENDPOINT" if mode == "cloud" else "PRIMARY_ENDPOINT"
    endpoint = config.get("endpoint") or environment.get(slot)

    # Action 2: reject the selected endpoint before the external constructor.
    if endpoint:
        parsed = urlsplit(endpoint)
        if not parsed.hostname or parsed.scheme not in {"http", "https"}:
            raise ValueError("malformed endpoint")
        if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("remote endpoints require HTTPS")

    # Action 3: adapt accepted options, preserving explicit false values.
    provider_mode = config.get("provider_mode")
    if provider_mode is None:
        provider_mode = mode == "cloud"
    return sdk_factory(
        http_options={"base_url": endpoint} if endpoint else {},
        cloud=provider_mode,
    )
