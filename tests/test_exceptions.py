import pytest
from confamnode.client import ConfamNode
from confamnode.exceptions import ( 
    ConfamAuthError, 
    ConfamNodeError, 
    ConfamModelError,
    ConfamRequestError,
    ConfamProviderError,
    ConfamRateLimitError,
    ConfamInsufficientBalanceError,
)


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


def test_confam_insufficient_balance_error_default_message():
    error = ConfamInsufficientBalanceError()
    assert "insufficient" in str(error).lower()


def test_confam_insufficient_balance_error_is_subclass_of_confamnode_error():
    assert issubclass(ConfamInsufficientBalanceError, ConfamNodeError)


def test_confam_provider_error_default_message():
    error = ConfamProviderError()
    assert "temporarily unavailable" in str(error).lower()


def test_confam_provider_error_is_subclass_of_confamnode_error():
    assert issubclass(ConfamProviderError, ConfamNodeError)


def test_confam_request_error_default_message():
    error = ConfamRequestError()
    assert "could not be processed" in str(error).lower()


def test_confam_request_error_is_subclass_of_confamnode_error():
    assert issubclass(ConfamRequestError, ConfamNodeError)


def test_confam_insufficient_balance_error_accepts_custom_message():
    error = ConfamInsufficientBalanceError("custom detail here")
    assert str(error) == "custom detail here"