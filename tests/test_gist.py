import pytest
from unittest.mock import patch, MagicMock

from confamnode import models
from confamnode.client import ConfamNode
from confamnode.ansa import Ansa, Usage, Cost
from confamnode.exceptions import ConfamModelError



@pytest.fixture
def client():
    return ConfamNode(api_key="confam-sk-test-abc123")


@pytest.fixture
def mock_proxy_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "id": "confam-test-id",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "confam-speed",
        "choices": [{
            "index": 0,
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": "How far! I dey fine.",
                "reasoning": None,
                "tool_calls": None,
                "citations": None
            }
        }],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        },
        "confam": {
            "request_id": "confam-test-id",
            "cost": {"naira": 0.0, "naira_input": 0.0, "naira_output": 0.0},
            "is_local": False,
            "is_ngn_data_residency": False
        }
    }
    return mock


def test_gist_requires_model(client):
    with pytest.raises(TypeError):
        client.gist(messages=[{"role": "user", "content": "How far?"}])


def test_gist_requires_messages(client):
    with pytest.raises(TypeError):
        client.gist(model=models.SPEED)


def test_gist_rejects_invalid_model(client):
    with pytest.raises(ConfamModelError, match="Invalid model name"):
        client.gist(model="gpt-4o", messages="How far?")


def test_gist_returns_ansa_object(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert isinstance(ansa, Ansa)


def test_gist_returns_content(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert ansa.text == "How far! I dey fine."


def test_gist_has_model(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa =client.gist(model="confam-speed", messages="How far?")
        assert ansa.model == "confam-speed"


def test_gist_has_usage(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert isinstance(ansa.usage, Usage)
        assert ansa.usage.prompt_tokens == 10
        assert ansa.usage.completion_tokens == 20
        assert ansa.usage.total_tokens == 30


def test_gist_has_cost(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert isinstance(ansa.cost, Cost)
        assert isinstance(ansa.cost.naira, float)


def test_gist_comes_from_confam_object(client, mock_proxy_response):
    mock_proxy_response.json.return_value["confam"]["cost"] = {
        "naira": 0.596,
        "naira_input": 0.075,
        "naira_output": 0.521
    }
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model="confam-intelligence", messages="How far?")
        assert ansa.cost.naira == 0.596
        assert ansa.cost.naira_input == 0.075
        assert ansa.cost.naira_output == 0.521


def test_gist_has_finish_reason(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert ansa.finish_reason == "stop"


def test_gist_has_id(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert ansa.id.startswith("confam-")


def test_gist_has_raw(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert isinstance(ansa.raw, dict)
        assert "_hidden_params" not in ansa.raw


def test_gist_accepts_string_messages(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How far?")
        assert ansa is not None


def test_gist_converts_string_to_user_message_in_request(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response) as mock_post:
        client.gist(model=models.SPEED, messages="How far?")
        body = mock_post.call_args.kwargs["json"]
        user_msgs = [m for m in body["messages"] if m["role"] == "user"]
        assert user_msgs[0]["content"] == "How far?"


def test_gist_accepts_list_messages(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(
            model=models.SPEED,
            messages=[{"role": "user", "content": "How far?"}]
        )
        assert ansa is not None


def test_gist_rejects_invalid_messages_type(client):
    with pytest.raises(ValueError, match="messages must be a string or list"):
        client.gist(model=models.SPEED, messages=123)


def test_gist_passes_kwargs_to_proxy(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response) as mock_post:
        client.gist(model=models.SPEED, messages="How far?", temperature=0.7, max_tokens=500)
        body = mock_post.call_args.kwargs["json"]
        assert body["temperature"] == 0.7
        assert body["max_tokens"] == 500


def test_gist_does_not_prepend_openai_prefix(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response) as mock_post:
        client.gist(model="confam-speed", messages="How far?", temperature=0.7, max_tokens=500)
        body = mock_post.call_args.kwargs["json"]
        assert body["model"] == "confam-speed"
        assert "openai/" not in body["model"]


def test_gist_default_system_omits_system_field(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response) as mock_post:
        client.gist(model="confam-speed", messages="How far?")
        body = mock_post.call_args.kwargs["json"]
        assert "system" not in body


def test_gist_custom_system_passes_as_field(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response) as mock_post:
        client.gist(model=models.SPEED, messages="Who you be?", system="You are a Konga assistant")
        body = mock_post.call_args.kwargs["json"]
        assert body["system"] == "You are a Konga assistant"


def test_gist_system_none_passes_null(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response) as mock_post:
        client.gist(model=models.SPEED, messages="Who you be?", system=None)
        body = mock_post.call_args.kwargs["json"]
        assert "system" in body
        assert body["system"] is None


def test_gist_system_in_messages_list_is_respected(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response) as mock_post:
        client.gist(
            model=models.SPEED,
            messages=[
                {"role": "system", "content": "You are a Konga assistant"},
                {"role": "user", "content": "Who you be?"}
            ]
        )
        body = mock_post.call_args.kwargs["json"]
        assert body["messages"][0]["role"] == "system"
        assert body["messages"][0]["content"] == "You are a Konga assistant"


def test_gist_sets_local_from_confam_object(client, mock_proxy_response):
    mock_proxy_response.json.return_value["confam"]["is_local"] = True
    mock_proxy_response.json.return_value["confam"]["is_ngn_data_residency"] = True
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.NANO, messages="How you dey?")
        assert ansa.is_local is True
        assert ansa.is_ngn_data_residency is True


def test_sets_is_local_false_for_cloud_model(client, mock_proxy_response):
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.SPEED, messages="How you dey?")
        assert ansa.is_local is False
        assert ansa.is_ngn_data_residency is False


def test_gist_accepts_all_valid_models(client, mock_proxy_response):
    valid_models = [models.LITE, models.SPEED, models.REASONING, models.NANO]
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        for model in valid_models:
            ansa = client.gist(model=model, messages="How far?")
            assert ansa is not None


def test_gist_raises_on_proxy_error(client):
    mock_error_response = MagicMock()
    mock_error_response.status_code = 402
    mock_error_response.json.return_value = {"detail": "Insufficient wallet balance."}
    with patch("confamnode.client.httpx.post", return_value=mock_error_response):
        with pytest.raises(Exception):
            client.gist(model="confam-intelligence", messages="How far?")


def test_gist_reasoning_content_returned(client, mock_proxy_response):
    mock_proxy_response.json.return_value["choices"][0]["message"]["reasoning"] = "step by step..."
    with patch("confamnode.client.httpx.post", return_value=mock_proxy_response):
        ansa = client.gist(model=models.REASONING, messages="Think carefully")
        assert ansa.reasoning == "step by step..."

