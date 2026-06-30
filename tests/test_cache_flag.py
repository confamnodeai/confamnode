"""
Tests for the per-request cache flag on ConfamNode.gist().

Caching is opt-OUT by default: identical requests must each return a fresh
response (critical for data-generation loops). cache=True flips the request
to read-from + write-to the cache. These tests pin down the exact payload
sent in each case so a future refactor can't silently flip the default.

No network: httpx.post is monkeypatched to capture the request body.
"""
import httpx
import pytest

from confamnode.client import ConfamNode
from confamnode.registry import VALID_MODELS

API_KEY = "confam-test"
MODEL = next(iter(VALID_MODELS))

CACHE_OFF = {"no-cache": True, "no-store": True}    # skip read + skip store


@pytest.fixture
def captured_body(monkeypatch):
    """Patch httpx.post to record the JSON body and return a valid 200."""
    box = {}

    def fake_post(url, headers=None, json=None, timeout=None):
        box["body"] = json

        class _Resp:
            status_code = 200
            text = ""

            def json(self):
                return {
                    "choices": [{"message": {"content": "hi"}, "finish_reason": "stop"}],
                    "usage": {},
                    "confam": {"cost": {"naira": 0.0}},
                }

        return _Resp()

    monkeypatch.setattr(httpx, "post", fake_post)
    return box


def _gist(**kwargs):
    ConfamNode(api_key=API_KEY).gist(model=MODEL, messages="x", **kwargs)


def test_cache_off_by_default(captured_body):
    _gist()
    assert captured_body["body"]["cache"] == CACHE_OFF


def test_cache_true_omits_field(captured_body):
    # cache=True lets the gateway apply its normal caching by sending NO cache
    # field -- the request shape proven to engage the cache.
    _gist(cache=True)
    assert "cache" not in captured_body["body"]


def test_cache_false_is_explicit_off(captured_body):
    _gist(cache=False)
    assert captured_body["body"]["cache"] == CACHE_OFF