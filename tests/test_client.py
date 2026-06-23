import os
import pytest
from unittest.mock import patch, MagicMock

from confamnode.client import ConfamNode
from confamnode.exceptions import ConfamAuthError


def test_client_accepts_api_key():
    client = ConfamNode(api_key="confam-abc123")
    assert client.api_key == "confam-abc123"


def test_client_raises_error_without_api_key():
    with pytest.raises(ValueError, match="api_key is required"):
        ConfamNode()


def test_client_raises_error_on_invalid_key_format():
    with pytest.raises(ConfamAuthError, match="Invalid ConfamNode API key format"):
        ConfamNode(api_key="sk-openai-abc123")


def test_client_key_starts_with_confam():
    client = ConfamNode(api_key="confam-abc123")
    assert client.api_key.startswith("confam-")


def test_client_does_not_have_litellm_key():
    client = ConfamNode(api_key="confam-abc123")
    assert not hasattr(client, "litellm_key")


def test_client_has_default_base_url():
    client = ConfamNode(api_key="confam-abc123")
    assert client.base_url == "https://api.confamnode.com/v1"


def test_client_accepts_custom_base_url():
    client = ConfamNode(
        api_key="confam-abc123",
        base_url="http://192.168.1.100:8000/v1"
    )
    assert client.base_url == "http://192.168.1.100:8000/v1"


def test_client_picks_up_api_key_from_environment():
    with patch.dict(os.environ, {"CONFAMNODE_API_KEY": "confam-abc123"}):
        client = ConfamNode()
        assert client.api_key == "confam-abc123"


def test_client_explicit_key_overrides_environment():
    with patch.dict(os.environ, {"CONFAMNODE_API_KEY": "confam-env123"}):
        client = ConfamNode(api_key="confam-explicit123")
        assert client.api_key == "confam-explicit123"


def test_client_sends_confam_key_in_authorization_header():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "confam-xxx",
        "object": "chat.completion",
        "created": 1,
        "model": "confam-speed",
        "choices": [{"index": 0, "finish_reason": "stop",
                     "message": {"role": "assistant", "content": "hi",
                                 "reasoning": None, "tool_calls": None, "citations": None}}],
        "usage": {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10},
        "confam": {"request_id": "confam-xxx",
                   "cost": {"naira": 0.0, "naira_input": 0.0, "naira_output": 0.0},
                   "is_local": False, "is_ngn_data_residency": False}
    }

    client = ConfamNode(api_key="confam-abc123")
    with patch("confamnode.client.httpx.post", return_value=mock_response) as mock_post:
        client.gist(model="confam-speed", messages="hi")
        call_headers = mock_post.call_args.kwargs["headers"]
        assert call_headers["Authorization"] == "Bearer confam-abc123"