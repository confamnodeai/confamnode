"""
Unit tests for confamnode.utils.extract_error.

Pure function, no network: just feed it fake responses and assert it never
raises and always produces a usable message.
"""
import pytest
from confamnode.utils import raise_for_status, extract_error
from confamnode.exceptions import (
    ConfamNodeError,
    ConfamAuthError,
    ConfamRequestError,
    ConfamProviderError,
    ConfamRateLimitError,
    ConfamInsufficientBalanceError
)


class _Resp:
    """Minimal stand-in for an httpx.Response, for raise_for_status tests."""
    def __init__(self, payload=None, *, json_raises=False, text=""):
        self._payload = payload
        self._json_raises = json_raises
        self.text = text

    def json(self):
        if self._json_raises:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        return self._payload

class _StatusResp:
    """Minimal stand-in for an httpx.Response, for raise_for_status tests."""
    def __init__(self, status_code, payload=None, *, json_raises=False, text=""):
        self.status_code = status_code
        self._payload = payload
        self._json_raises = json_raises
        self.text = text

    def json(self):
        if self._json_raises:
            raise ValueError("Expecting value: line 1 column 1 (char 0)")
        return self._payload


def test_raises_for_status_does_nothing_2xx():
    raise_for_status(_StatusResp(200)) # should not raise
    raise_for_status(_StatusResp(201))
    raise_for_status(_StatusResp(204))


def test_raise_for_status_401_raises_confam_auth_error():
    with pytest.raises(ConfamAuthError) as exc:
        raise_for_status(_StatusResp(401, payload={"detail": "bad key"}))
    assert "401" in str(exc.value)
    assert "bad key" in str(exc.value)


def test_raise_for_status_402_raises_insufficient_balance_error():
    with pytest.raises(ConfamInsufficientBalanceError) as exc:
        raise_for_status(_StatusResp(402, payload={"detail": "Insufficient wallet balance."}))
    assert "402" in str(exc.value)
    assert "Insufficient wallet balance" in str(exc.value)


def test_raise_for_status_429_raises_rate_limit_error():
    with pytest.raises(ConfamRateLimitError) as exc:
        raise_for_status(_StatusResp(429, json_raises=True, text=""))
    assert "429" in str(exc.value)


def test_raise_for_status_502_raises_provider_error():
    with pytest.raises(ConfamProviderError) as exc:
        raise_for_status(_StatusResp(502, json_raises=True, text=""))
    assert "502" in str(exc.value)


def test_raise_for_status_503_raises_provider_error():
    with pytest.raises(ConfamProviderError) as exc:
        raise_for_status(_StatusResp(503, json_raises=True, text=""))
    assert "503" in str(exc.value)


def test_raise_for_status_504_raises_provider_error():
    with pytest.raises(ConfamProviderError) as exc:
        raise_for_status(_StatusResp(504, json_raises=True, text=""))
    assert "504" in str(exc.value)


def test_raise_for_status_4xx_raises_request_error():
    with pytest.raises(ConfamRequestError) as exc:
        raise_for_status(_StatusResp(400, payload={"detail": "invalid model"}))
    assert "400" in str(exc.value)
    assert "invalid model" in str(exc.value)


def test_raise_for_status_422_raises_request_error():
    with pytest.raises(ConfamRequestError) as exc:
        raise_for_status(_StatusResp(422, payload={"detail": "validation error"}))
    assert "422" in str(exc.value)


def test_raise_for_status_unmapped_5xx_raises_base_error():
    # 500 isn't in the (502, 503, 504) tuple -- falls through to the
    # generic ConfamNodeError branch.
    with pytest.raises(ConfamNodeError) as exc:
        raise_for_status(_StatusResp(500, json_raises=True, text=""))
    assert "500" in str(exc.value)


def test_raise_for_status_524_falls_through_to_base_error():
    # Matches the existing gist-level test for Cloudflare 524s: not in
    # the explicit (502, 503, 504) tuple, so it lands in the generic
    # 5xx branch -- still typed, still has the status code and the
    # HTML <title> summary embedded.
    html = (
        "<!DOCTYPE html><html><head>"
        "<title>confamnode.com | 524: A timeout occurred</title>"
        "</head><body>...</body></html>"
    )
    with pytest.raises(ConfamNodeError) as exc:
        raise_for_status(_StatusResp(524, json_raises=True, text=html))
    msg = str(exc.value)
    assert "524" in msg
    assert "A timeout occurred" in msg


def test_raise_for_status_all_typed_exceptions_are_confamnode_error_subclasses():
    # Every specific exception raised by raise_for_status must still be
    # catchable via the base ConfamNodeError, for callers who don't want
    # to enumerate every specific subtype.
    for status in (401, 402, 429, 502, 503, 504, 400, 500):
        with pytest.raises(ConfamNodeError):
            raise_for_status(_StatusResp(status, json_raises=True, text=""))

def test_empty_body_returns_placeholder():
    # The exact case that crashed the SDK: empty 429 body.
    assert extract_error(_Resp(json_raises=True, text="")) == "no response body"


def test_non_json_text_body_is_returned_stripped():
    assert extract_error(_Resp(json_raises=True, text="  upstream timeout  ")) == "upstream timeout"


def test_html_error_page_summarised_to_title():
    # A Cloudflare 524 page: don't dump the whole page, surface the <title>.
    html = (
        "<!DOCTYPE html><html><head>"
        "<title>confamnode.com | 524: A timeout occurred</title>"
        "</head><body>...lots of markup...</body></html>"
    )
    assert extract_error(_Resp(json_raises=True, text=html)) == "confamnode.com | 524: A timeout occurred"


def test_html_without_title_falls_back():
    html = "<html><body>502 Bad Gateway</body></html>"
    assert extract_error(_Resp(json_raises=True, text=html)) == "HTML error page (no title)"


def test_long_plain_text_is_truncated():
    body = "x" * 500
    out = extract_error(_Resp(json_raises=True, text=body))
    assert len(out) == 300 and out.endswith("...")


def test_detail_key_is_preferred():
    assert extract_error(_Resp(payload={"detail": "invalid model"})) == "invalid model"


def test_error_key_fallback():
    assert extract_error(_Resp(payload={"error": "nope"})) == "nope"


def test_message_key_fallback():
    assert extract_error(_Resp(payload={"message": "hmm"})) == "hmm"


def test_non_dict_json_falls_back_to_text():
    # A JSON array (not a dict) shouldn't blow up; fall back to text.
    assert extract_error(_Resp(payload=["a", "b"], text="listy")) == "listy"