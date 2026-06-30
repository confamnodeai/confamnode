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