"""
Unit tests for confamnode.utils.extract_error.

Pure function, no network: just feed it fake responses and assert it never
raises and always produces a usable message.
"""
from confamnode.utils import extract_error


class _Resp:
    """Minimal stand-in for an httpx.Response."""
    def __init__(self, payload=None, *, json_raises=False, text=""):
        self._payload = payload
        self._json_raises = json_raises
        self.text = text

    def json(self):
        if self._json_raises:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        return self._payload


def test_empty_body_returns_placeholder():
    # The exact case that crashed the SDK: empty 429 body.
    assert extract_error(_Resp(json_raises=True, text="")) == "no response body"


def test_non_json_text_body_is_returned_stripped():
    assert extract_error(_Resp(json_raises=True, text="  upstream timeout  ")) == "upstream timeout"


def test_detail_key_is_preferred():
    assert extract_error(_Resp(payload={"detail": "invalid model"})) == "invalid model"


def test_error_key_fallback():
    assert extract_error(_Resp(payload={"error": "nope"})) == "nope"


def test_message_key_fallback():
    assert extract_error(_Resp(payload={"message": "hmm"})) == "hmm"


def test_non_dict_json_falls_back_to_text():
    # A JSON array (not a dict) shouldn't blow up; fall back to text.
    assert extract_error(_Resp(payload=["a", "b"], text="listy")) == "listy"