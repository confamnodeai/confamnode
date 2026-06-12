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
        ansa = client.gist(
            model=models.SPEED,
            messages=[{"role": "user", "content": "How far?"}]
        )
        assert ansa.text == "How far! I dey fine."


def test_gist_accepts_all_valid_models(client, mock_litellm_response):
    valid_models = [
        models.LITE,
        models.SPEED,
        models.REASONING,
        models.NANO
    ]
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        for model in valid_models:
            ansa = client.gist(
                model=model,
                messages=[{"role": "user", "content": "How far?"}]
            )
            assert ansa is not None


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
        ansa = client.gist(
            model=models.SPEED,
            messages="How far?"
        )
        assert ansa is not None


def test_gist_converts_string_to_message_list(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="How far?"
        )
        call_args = mock_call.call_args
        messages = call_args.kwargs["messages"]
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "How far?"


def test_gist_accepts_lists_messages(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model=models.SPEED,
            messages=[{"role": "user", "content": "How far?"}]
        )
        assert ansa is not None


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


def test_gist_prepends_openai_prefix_to_model(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model="confam-speed",
            messages="How far?"
        )
        call_args = mock_call.call_args
        assert call_args.kwargs["model"] == "openai/confam-speed"


def test_gist_returns_ansa_object(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert isinstance(ansa, Ansa)


def test_gist_has_test(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert ansa.text == "How far! I dey fine."

    
def test_gist_has_model(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert ansa.model == "confam-speed"


def test_gist_has_usage(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert isinstance(ansa.usage, Usage)
        assert ansa.usage.prompt_tokens == 10
        assert ansa.usage.completion_tokens == 20
        assert ansa.usage.total_tokens == 30


def test_gist_has_cost(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert isinstance(ansa.cost, Cost)
        assert isinstance(ansa.cost.naira, float)


def test_gist_has_finish_reason(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert ansa.finish_reason is not None


def test_gist_has_id(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert ansa.id.startswith("confam-")


def test_gist_has_raw(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model="confam-speed",
            messages="How far?"
        )
        assert ansa.raw is not None


def test_gist_adds_default_system_message(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="Who are you?"
        )
        call_args = mock_call.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0]["role"] == "system"
        assert "ConfamNode" in messages[0]["content"]


def test_gist_custom_system_parameter_overrides_default(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="Who are you?",
            system="You are a Konga assistant"
        )
        call_args = mock_call.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a Konga assistant"


def test_gist_system_none_disbales_system_message(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="Who are you?",
            system=None
        )
        call_args = mock_call.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0]["role"] == "user"


def test_gist_system_in_messages_list_is_respected(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages=[
                {"role": "system", "content": "You are a Konga assistant"},
                {"role": "user", "content": "Who are you?"}
            ]
        )
        call_args = mock_call.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a Konga assistant"


def test_gist_default_system_message_contains_nigeria(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="Where are you from?"
        )
        call_args = mock_call.call_args
        messages = call_args.kwargs["messages"]
        assert "Nigeria" in messages[0]["content"]


def test_gist_default_system_message_does_not_reveal_underlying_model(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="What model are you?"
        )
        call_args = mock_call.call_args
        messages = call_args.kwargs["messages"]
        system_content = messages[0]["content"]
        assert "Gemini" not in system_content
        assert "GPT" not in system_content
        assert "Llama" not in system_content


def test_gist_sets_is_local_false_for_cloud_model(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model=models.SPEED,
            messages="How you dey?"
        )
        assert ansa.is_local == False
        assert ansa.is_ngn_data_residency == False


def test_gist_sets_is_local_true_for_nano(client, mock_litellm_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_litellm_response):
        ansa = client.gist(
            model=models.NANO,
            messages="How you dey?"
        )
        assert ansa.is_local == True
        assert ansa.is_ngn_data_residency == True