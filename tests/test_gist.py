import pytest
from unittest.mock import patch, MagicMock
from confamnode.client import ConfamNode
from confamnode import models
from confamnode.exceptions import ConfamModelError


@pytest.fixture
def client():
    return ConfamNode(api_key="confam-sk-test-abc123")


@pytest.fixture
def mock_litellm_response():
    mock = MagicMock()
    mock.choices[0].message.content = "How far! I dey fine."
    mock.model = "confam-speed"
    mock.usage.prompt_tokens = 10
    mock.usage.completion_tokens = 20
    mock.usage.total_tokens = 30
    return mock


def test_gist_requires_model(client):
    with pytest.raises(TypeError):
        client.gist(messages=[{"role": "user", "content": "How far?"}])


def test_gist_requires_messages(client):
    with pytest.raises(TypeError):
        client.gist(model=models.SPEED)


def test_gist_rejects_invalid_model(client):
    with pytest.raises(ConfamModelError, match="Invalid model name"):
        client.gist(
            model="gpt-4o",
            messages=[{"role": "user", "content": "How far?"}]
        )


def test_gist_returns_content(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        response = client.gist(
            model=models.SPEED,
            messages=[{"role": "user", "content": "How far?"}]
        )
        assert response.choices[0].message.content == "How far! I dey fine."


def test_gist_accepts_all_valid_models(client, mock_litellm_response):
    valid_models = [
        models.LITE,
        models.SPEED,
        models.REASONING,
        models.NANO
    ]
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        for model in valid_models:
            response = client.gist(
                model=model,
                messages=[{"role": "user", "content": "How far?"}]
            )
            assert response is not None


def test_gist_sends_correct_model_to_litellm(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages=[{"role": "user", "content": "How far?"}]
        )
        call_args = mock_call.call_args
        assert "confam-speed" in call_args.kwargs.get("model", "") or \
                "confam-speed" in call_args.args
        

def test_gist_accepts_string_messages(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        response = client.gist(
            model=models.SPEED,
            messages="How far?"
        )
        assert response is not None


def test_gist_converts_string_to_message_list(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="How far?"
        )
        call_args = mock_call.call_args
        assert call_args.kwargs["messages"] == [{"role": "user", "content": "How far?"}]


def test_gist_accepts_lists_messages(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        response = client.gist(
            model=models.SPEED,
            messages=[{"role": "user", "content": "How far?"}]
        )
        assert response is not None


def test_gist_rejects_invalid_messages_type(client):
    with pytest.raises(ValueError, match="messages must be a string or list"):
        client.gist(
            model=models.SPEED,
            messages=123
        )


def test_gist_passes_kwargs_to_litellm(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="How far?",
            temperature=0.7,
            max_tokens=500
        )
        call_args = mock_call.call_args
        assert call_args.kwargs["temperature"] == 0.7
        assert call_args.kwargs["max_tokens"] == 500
