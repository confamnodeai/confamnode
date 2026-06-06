import pytest
from confamnode.client import ConfamNode
from confamnode.exceptions import ConfamNodeError, ConfamAuthError, ConfamRateLimitError, ConfamModelError


def test_confam_auth_error_is_raised_on_bad_key():
    with pytest.raises(ConfamAuthError, match="Invalid ConfamNode API key format"):
        ConfamNode(api_key="sk-openai-abc123")

def test_confam_auth_error_is_subclass_of_confamnode_error():
    with pytest.raises(ConfamNodeError):
        ConfamNode(api_key="sk-openai-abc123")

def test_confam_rate_limit_error_message():
    error = ConfamRateLimitError()
    assert "upgrade your plan" in str(error).lower()

def test_confam_model_error_message():
    error = ConfamModelError("confam-wrong")
    assert "confam-wrong" in str(error)