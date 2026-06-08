import os
import pytest
from unittest.mock import patch

from confamnode.client import ConfamNode
from confamnode.exceptions import ConfamAuthError


def test_client_accepts_api_key():
    client = ConfamNode(api_key="confam-sk-abc123")
    assert client.api_key == "confam-sk-abc123"


def test_client_raises_error_without_api_key():
    with pytest.raises(ValueError, match="api_key is required"):
        ConfamNode()


def test_client_raises_error_on_invalid_key_format():
    with pytest.raises(ConfamAuthError, match="Invalid ConfamNode API key format"):
        ConfamNode(api_key="sk-openai-abc123")


def test_client_key_starts_with_confam_sk():
    client = ConfamNode(api_key="confam-sk-abc123")
    assert client.api_key.startswith("confam-sk-")


def test_client_strips_confam_prefix_for_litellm():
    client = ConfamNode(api_key="confam-sk-abc123")
    assert client.litellm_key == "sk-abc123"


def test_client_has_default_base_url():
    client = ConfamNode(api_key="confam-sk-abc123")
    assert client.base_url == "https://api.confamnode.com/v1"


def test_client_accepts_custom_base_url():
    client = ConfamNode(
        api_key="confam-sk-abc123",
        base_url="http://192.168.1.100:4000/v1"
    )
    assert client.base_url == "http://192.168.1.100:4000/v1"


def test_client_picks_up_api_key_from_environment():
    with patch.dict(os.environ, {"CONFAMNODE_API_KEY": "confam-sk-abc123"}):
        client = ConfamNode()
        assert client.api_key == "confam-sk-abc123"


def test_client_explicit_key_overrides_environment():
    with patch.dict(os.environ, {"CONFAMNODE_API_KEY": "confam-sk-env123"}):
        client = ConfamNode(api_key="confam-sk-explicit123")
        assert client.api_key == "confam-sk-explicit123"