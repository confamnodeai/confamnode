import pytest
from unittest.mock import patch, MagicMock
from confamnode.client import ConfamNode
from confamnode import models


@pytest.fixture
def client():
    return ConfamNode(api_key="confam-sk-abc123")


@pytest.fixture
def mock_stream_response():
    chunk1 = MagicMock()
    chunk1.choices[0].delta.content = "How"
    chunk2 = MagicMock()
    chunk2.choices[0].delta.content = " far!"
    chunk3 = MagicMock()
    chunk3.choices[0].delta.content = None
    return iter([chunk1, chunk2, chunk3])


def test_gist_accepts_stream_true(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        response = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        assert response is not None


def test_gist_stream_returns_chunks(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        chunks = list(client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        ))
        assert len(chunks) == 3


def test_gist_stream_chunks_have_content(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        chunks = list(client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        ))
        assert chunks[0].choices[0].delta.content == "How"
        assert chunks[1].choices[0].delta.content == " far!"


def test_gist_stream_passes_stream_true_to_litellm(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        call_args = mock_call.call_args
        assert call_args.kwargs.get("stream") == True

