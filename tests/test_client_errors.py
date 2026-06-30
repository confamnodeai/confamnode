"""
Tests for ConfamNode.gist() error handling.

The original bug: a non-2xx response with an empty / non-JSON body made the
SDK call response.json() in its error branch, which raised JSONDecodeError
and hid the HTTP status. These tests pin down that:
  - an empty error body raises a clean "ConfamNode error <status>: ..." with
    the status code intact (NOT a JSONDecodeError), and
  - the normal success path still works after the refactor.

No network: httpx.post is monkeypatched to return a fake response.
"""
import httpx
import pytest

from confamnode.client import ConfamNode
from confamnode.registry import VALID_MODELS

API_KEY = "confam-test"
MODEL = next(iter(VALID_MODELS))   # any valid model; we never really call out


class FakeResponse:
    def __init__(self, status_code, payload=None, *, json_raises=False, text=""):
        self.status_code = status_code
        self._payload = payload
        self._json_raises = json_raises
        self.text = text

    def json(self):
        if self._json_raises:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        return self._payload


def _patch_post(monkeypatch, response):
    monkeypatch.setattr(httpx, "post", lambda *a, **k: response)


def test_empty_error_body_raises_with_status_not_jsondecodeerror(monkeypatch):
    # The reproduction of the reported crash: 429, empty body.
    _patch_post(monkeypatch, FakeResponse(429, json_raises=True, text=""))
    client = ConfamNode(api_key=API_KEY)
    with pytest.raises(Exception) as exc:
        client.gist(model=MODEL, messages="hi")
    msg = str(exc.value)
    assert "429" in msg
    assert "no response body" in msg
    assert "JSONDecode" not in type(exc.value).__name__


def test_json_detail_error_surfaces_detail(monkeypatch):
    _patch_post(monkeypatch, FakeResponse(400, payload={"detail": "invalid model"}))
    client = ConfamNode(api_key=API_KEY)
    with pytest.raises(Exception) as exc:
        client.gist(model=MODEL, messages="hi")
    assert "400" in str(exc.value)
    assert "invalid model" in str(exc.value)


def test_html_gateway_error_surfaces_text(monkeypatch):
    _patch_post(monkeypatch, FakeResponse(502, json_raises=True,
                                          text="<html>502 Bad Gateway</html>"))
    client = ConfamNode(api_key=API_KEY)
    with pytest.raises(Exception) as exc:
        client.gist(model=MODEL, messages="hi")
    assert "502" in str(exc.value)
    assert "Bad Gateway" in str(exc.value)


def test_success_path_still_returns_ansa(monkeypatch):
    payload = {
        "id": "abc",
        "choices": [{"message": {"content": "hello"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
        "confam": {"request_id": "r1", "cost": {"naira": 0.0}},
    }
    _patch_post(monkeypatch, FakeResponse(200, payload=payload))
    client = ConfamNode(api_key=API_KEY)
    ansa = client.gist(model=MODEL, messages="hi")
    assert ansa.text == "hello"
    assert ansa.cost.naira == 0.0