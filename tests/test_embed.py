import pytest
from unittest.mock import patch, MagicMock

from confamnode import models
from confamnode.client import ConfamNode
from confamnode.ansa import EmbeddingResult, EmbeddingUsage
from confamnode.exceptions import (
    ConfamModelError,
    ConfamAuthError,
    ConfamInsufficientBalanceError,
    ConfamRateLimitError,
    ConfamProviderError,
    ConfamRequestError,
)

CLOUD_EMBED_MODEL = "google/gemini-embedding-001"

@pytest.fixture
def client():
    return ConfamNode(api_key="confam-sk-test-abc123")


@pytest.fixture
def mock_embed_response():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "object": "list",
        "data": [
            {"object": "embedding", "index": 0, "embedding": [0.1, 0.2, 0.3]}
        ],
        "model": CLOUD_EMBED_MODEL,
        "usage": {"prompt_tokens": 8, "total_tokens": 8},
        "confam": {
            "request_id": "confam-embed-test-id",
            "cost": {"naira": 0.004, "naira_input": 0.004},
            "is_local": True,
            "is_ngn_data_residency": True,
            "task_type_applied": "document",
        }
    }
    return mock


@pytest.fixture
def mock_embed_response_multi():
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {
        "object": "list",
        "data": [
            {"object": "embedding", "index": 0, "embedding": [0.1, 0.2]},
            {"object": "embedding", "index": 1, "embedding": [0.3, 0.4]},
        ],
        "model": CLOUD_EMBED_MODEL,
        "usage": {"prompt_tokens": 16, "total_tokens": 16},
        "confam": {
            "request_id": "confam-embed-test-id-2",
            "cost": {"naira": 0.008, "naira_input": 0.008},
            "is_local": True,
            "is_ngn_data_residency": True,
            "task_type_applied": "document",
        }
    }
    return mock


def test_embed_rejects_invalid_model(client):
    with pytest.raises(ConfamModelError, match="Invalid model name"):
        client.embed(model="text-embedding-ada-002", input="How you dey?")


def test_embed_returns_embedding_result(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert isinstance(result, EmbeddingResult)


def test_embed_single_string_input_returns_flat_vector(client, mock_embed_response):
    # Convenience unwrapping: a single string input should return one
    # flat vector, not a one-item list-of-lists.
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result.embeddings == [0.1, 0.2, 0.3]


def test_embed_list_input_returns_list_of_vectors(client, mock_embed_response_multi):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response_multi):
        result = client.embed(
            model=CLOUD_EMBED_MODEL,
            input=["How you dey?", "Wetin dey happen?"]
        )
        assert result.embeddings == [[0.1, 0.2], [0.3, 0.4]]


def test_embed_single_item_list_input_stays_a_list(client, mock_embed_response):
    # Even a ONE-item list should return a list, not get unwrapped like
    # a bare string would -- input shape determines output shape.
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input=["How you dey?"])
        assert result.embeddings == [[0.1, 0.2, 0.3]]


def test_embed_has_usage(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert isinstance(result.usage, EmbeddingUsage)
        assert result.usage.prompt_tokens == 8
        assert result.usage.total_tokens == 8


def test_embed_has_cost_from_confam_object(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result.cost.naira == 0.004
        assert result.cost.naira_input == 0.004


def test_embed_has_model(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result.model == "google/gemini-embedding-001"


def test_embed_has_id_from_confam_object(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result.id == "confam-embed-test-id"


# def test_embed_sets_is_local_from_confam_object(client, mock_embed_response):
#     with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
#         result = client.embed(model=models.EMBED_LOCAL, input="How you dey?")
#         assert result.is_local is True
#         assert result.is_ngn_data_residency is True


def test_embed_sets_is_local_false_for_cloud_embed_model(client, mock_embed_response):
    mock_embed_response.json.return_value["confam"]["is_local"] = False
    mock_embed_response.json.return_value["confam"]["is_ngn_data_residency"] = False
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result.is_local is False
        assert result.is_ngn_data_residency is False


def test_embed_captures_task_type_applied(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result.task_type_applied == "document"


def test_embed_task_type_applied_is_none_when_not_in_confam_object(client, mock_embed_response):
    mock_embed_response.json.return_value["confam"]["task_type_applied"] = None
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result.task_type_applied is None


def test_embed_sends_confam_key_in_authorization_header(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response) as mock_post:
        client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        call_headers = mock_post.call_args.kwargs["headers"]
        assert call_headers["Authorization"] == "Bearer confam-sk-test-abc123"


def test_embed_sends_model_and_input_in_body(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response) as mock_post:
        client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        body = mock_post.call_args.kwargs["json"]
        assert body["model"] == "google/gemini-embedding-001"
        assert body["input"] == "How you dey?"


def test_embed_omits_task_type_when_not_specified(client, mock_embed_response):
    # SDK shouldn't duplicate the server's own "document" default --
    # only send task_type if the caller actually specified one.
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response) as mock_post:
        client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        body = mock_post.call_args.kwargs["json"]
        assert "task_type" not in body


def test_embed_sends_task_type_when_specified(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response) as mock_post:
        client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?", task_type="query")
        body = mock_post.call_args.kwargs["json"]
        assert body["task_type"] == "query"


def test_embed_passes_kwargs_to_proxy(client, mock_embed_response):
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response) as mock_post:
        client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?", dimensions=256)
        body = mock_post.call_args.kwargs["json"]
        assert body["dimensions"] == 256


def test_embed_raises_confam_model_error_before_any_network_call(client):
    with patch("confamnode.client.httpx.post") as mock_post:
        with pytest.raises(ConfamModelError):
            client.embed(model="not-a-real-model", input="hi")
        mock_post.assert_not_called()


# --- Error-path tests, mirroring the typed exceptions raise_for_status maps ---

def test_embed_raises_auth_error_on_401(client):
    mock_error = MagicMock()
    mock_error.status_code = 401
    mock_error.json.return_value = {"detail": "Invalid API key"}
    with patch("confamnode.client.httpx.post", return_value=mock_error):
        with pytest.raises(ConfamAuthError):
            client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")


def test_embed_raises_insufficient_balance_error_on_402(client):
    mock_error = MagicMock()
    mock_error.status_code = 402
    mock_error.json.return_value = {"detail": "Insufficient wallet balance."}
    with patch("confamnode.client.httpx.post", return_value=mock_error):
        with pytest.raises(ConfamInsufficientBalanceError):
            client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")


def test_embed_raises_rate_limit_error_on_429(client):
    mock_error = MagicMock()
    mock_error.status_code = 429
    mock_error.json.return_value = {"detail": "Daily request limit reached."}
    with patch("confamnode.client.httpx.post", return_value=mock_error):
        with pytest.raises(ConfamRateLimitError):
            client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")


def test_embed_raises_provider_error_on_502(client):
    mock_error = MagicMock()
    mock_error.status_code = 502
    mock_error.json.return_value = {"detail": "The embedding provider is temporarily unavailable."}
    with patch("confamnode.client.httpx.post", return_value=mock_error):
        with pytest.raises(ConfamProviderError):
            client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")


def test_embed_raises_request_error_on_400(client):
    mock_error = MagicMock()
    mock_error.status_code = 400
    mock_error.json.return_value = {"detail": "Your request could not be processed."}
    with patch("confamnode.client.httpx.post", return_value=mock_error):
        with pytest.raises(ConfamRequestError):
            client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")


def test_embed_accepts_free_tier_embedding_model(client, mock_embed_response):
    mock_embed_response.json.return_value["model"] = "liquid/lfm-2.5-embedding-350m:free"
    mock_embed_response.json.return_value["confam"]["is_local"] = False
    mock_embed_response.json.return_value["confam"]["is_ngn_data_residency"] = False
    with patch("confamnode.client.httpx.post", return_value=mock_embed_response):
        result = client.embed(model=CLOUD_EMBED_MODEL, input="How you dey?")
        assert result is not None
        assert result.model == "liquid/lfm-2.5-embedding-350m:free"