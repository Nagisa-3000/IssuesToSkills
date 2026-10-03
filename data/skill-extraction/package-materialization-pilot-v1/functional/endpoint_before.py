"""Deliberately broken synthetic client boundary; never contacts a provider."""


def build_client(config, environment, sdk_factory):
    endpoint = environment.get("PRIMARY_ENDPOINT") or config.get("endpoint")
    return sdk_factory(
        http_options={"base_url": endpoint},
        cloud=bool(config.get("inferred_cloud", False)),
    )
