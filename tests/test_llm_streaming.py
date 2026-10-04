"""Long native bundles require a complete stream and retain reported usage."""

import json

import pytest

from arex_skill_graph.llm_http import completion_from_sse


def event(content=None, finish=None, **extra):
    return (
        "data: "
        + json.dumps(
            {
                "id": "response-1",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": content},
                        "finish_reason": finish,
                    }
                ],
                **extra,
            }
        )
        + "\n\n"
    )


def test_stream_assembles_unicode_bundle_and_usage():
    raw = event("AREX-SKILL-BUNDLE 1\n") + event("中文正文\n", "stop")
    raw += 'data: {"id":"response-1","choices":[],"usage":{"total_tokens":42}}\n\n'
    raw += "data: [DONE]\n\n"
    response = completion_from_sse(raw)
    assert response["choices"][0]["message"]["content"] == "AREX-SKILL-BUNDLE 1\n中文正文\n"
    assert response["usage"]["total_tokens"] == 42


@pytest.mark.parametrize(
    "raw",
    [
        event("partial", "stop"),
        event("partial") + "data: [DONE]\n\n",
        event("a", "stop") + event("after finish") + "data: [DONE]\n\n",
        event("a") + event("b", "stop").replace("response-1", "response-2") + "data: [DONE]\n\n",
        event("a", "stop") + "data: [DONE]\n\ndata: {}\n\n",
    ],
)
def test_partial_or_mixed_response_never_becomes_a_completed_bundle(raw):
    with pytest.raises(ValueError):
        completion_from_sse(raw)
