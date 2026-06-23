import json
import pytest
from unittest.mock import patch, MagicMock

from confamnode import models
from confamnode.ansa import Ansa
from confamnode.client import ConfamNode, ConfamStream


@pytest.fixture
def client():
    return ConfamNode(api_key="confam-test-abc123")


def make_sse_lines(chunks, confam_cost=0.0):
    lines = []
    for chunk in chunks:
        lines.append(f"data: {json.dumps(chunk)}")
    lines.append(f"data: {json.dumps({
        'confam': {
            'request_id': 'confam-stream-test',
            'cost': {'naira': confam_cost, 'naira_input': 0.0, 'naira_output': confam_cost},
            'is_local': False,
            'is_ngn_data_residency': False
        }
    })}")
    lines.append("data: [DONE]")
    return lines


@pytest.fixture
def mock_sse_lines():
    return make_sse_lines([
        {"id": "confam-test", "object": "chat.completion.chunk", "created": 1,
         "model": "confam-speed",
         "choices": [{"index": 0, "delta": {"role": "assistant", "content": "How"}, "finish_reason": None}]},
        {"id": "confam-test", "object": "chat.completion.chunk", "created": 1,
         "model": "confam-speed",
         "choices": [{"index": 0, "delta": {"content": " far!"}, "finish_reason": None}]},
        {"id": "confam-test", "object": "chat.completion.chunk", "created": 1,
         "model": "confam-speed",
         "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]},
    ])


def make_mock_client(sse_lines):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_lines.return_value = iter(sse_lines)
    mock_response.close = MagicMock()

    mock_http_client = MagicMock()
    mock_http_client.__enter__ = MagicMock(return_value=mock_http_client)
    mock_http_client.__exit__ = MagicMock(return_value=False)
    mock_http_client.send.return_value = mock_response
    mock_http_client.build_request.return_value = MagicMock()
    return mock_http_client


def test_gist_stream_returns_confam_stream(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.SPEED, messages="How far?", stream=True)
        assert isinstance(stream, ConfamStream)


def test_gist_stream_returns_chunks(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.SPEED, messages="How far?", stream=True)
        yarns = list(stream)
        assert len(yarns)


def test_gist_stream_chunks_have_content(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.SPEED, messages="How far?", stream=True)
        yarns = list(stream)
        assert yarns[0].choices[0].delta.content == "How"
        assert yarns[1].choices[0].delta.content == " far!"
        assert yarns[2].choices[0].delta.content is None


def test_gist_stream_get_ansa_after_complete(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.SPEED, messages="How far?", stream=True)
        list(stream)
        ansa = stream.get_ansa()
        assert isinstance(ansa, Ansa)
        assert ansa.text == "How far!"


def test_gist_stream_has_model(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.SPEED, messages="How far?", stream=True)
        list(stream)
        ansa = stream.get_ansa()
        assert ansa.model == "confam-speed"


def test_gist_stream_get_ansa_before_complete_raises(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.SPEED, messages="How far?", stream=True)
        with pytest.raises(RuntimeError, match="Stream not complete"):
            stream.get_ansa()


def test_gist_stream_ansa_cost_from_confam_chunk(client):
    sse_lines = make_sse_lines([
        {"id": "confam-test", "object": "chat.completion.chunk", "created": 1,
         "model": "confam-intelligence",
         "choices": [{"index": 0, "delta": {"role": "assistant", "content": "hi"}, "finish_reason": None}]},
        {"id": "confam-test", "object": "chat.completion.chunk", "created": 1,
         "model": "confam-intelligence",
         "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]},
    ], confam_cost=0.596)

    mock_http_client = make_mock_client(sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model="confam-intelligence", messages="hi", stream=True)
        list(stream)
        ansa = stream.get_ansa()
        assert ansa.cost.naira == 0.596


def test_gist_stream_ansa_is_local_from_confam_chunk(client):
    sse_lines = [
        'data: {"id":"t","object":"chat.completion.chunk","created":1,"model":"confam-nano","choices":[{"index":0,"delta":{"content":"hi"},"finish_reason":null}]}',
        'data: ' + json.dumps({"confam": {"request_id": "confam-x", "cost": {"naira": 0.0, "naira_input": 0.0, "naira_output": 0.0}, "is_local": True, "is_ngn_data_residency": True}}),  # ← add "data: "
        "data: [DONE]"
    ]
    mock_http_client = make_mock_client(sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.NANO, messages="hi", stream=True)
        list(stream)
        ansa = stream.get_ansa()
        assert ansa.is_local is True
        assert ansa.is_ngn_data_residency is True

def test_gist_stream_ansa_is_local_false_for_cloud_model(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        stream = client.gist(model=models.SPEED, messages="How you dey?", stream=True)
        list(stream)
        ansa = stream.get_ansa()
        assert ansa.is_local is False
        assert ansa.is_ngn_data_residency is False


def test_gist_stream_sends_streams_true_in_body(client, mock_sse_lines):
    mock_http_client = make_mock_client(mock_sse_lines)
    with patch("confamnode.client.httpx.Client", return_value=mock_http_client):
        client.gist(model=models.SPEED, messages="How you dey?", stream=True)
        call_json = mock_http_client.build_request.call_args.kwargs["json"]
        assert call_json["stream"] is True