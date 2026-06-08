import pytest
from unittest.mock import patch, MagicMock

from confamnode import models
from confamnode.ansa import Ansa
from confamnode.client import ConfamNode, ConfamStream


@pytest.fixture
def client():
    return ConfamNode(api_key="confam-sk-abc123")


@pytest.fixture
def mock_stream_response():
    yarn1 = MagicMock()
    yarn1.choices[0].delta.content = "How"
    yarn2 = MagicMock()
    yarn2.choices[0].delta.content = " far!"
    yarn3 = MagicMock()
    yarn3.choices[0].delta.content = None
    return iter([yarn1, yarn2, yarn3])


def test_gist_accepts_stream_true(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        ansa = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        assert ansa is not None


def test_gist_stream_returns_chunks(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        yarns = list(client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        ))
        assert len(yarns) == 3


def test_gist_stream_chunks_have_content(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        yarns = list(client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        ))
        assert yarns[0].choices[0].delta.content == "How"
        assert yarns[1].choices[0].delta.content == " far!"


def test_gist_stream_passes_stream_true_to_litellm(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        call_args = mock_call.call_args
        assert call_args.kwargs.get("stream") == True


def test_gist_stream_returns_confam_stream(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        stream = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        assert isinstance(stream, ConfamStream)


def test_gist_stream_returns_chunks(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        stream = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        yarns = list(stream)
        assert len(yarns) == 3


def test_gist_stream_chunks_have_content(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        stream = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        yarns = list(stream)
        assert yarns[0].choices[0].delta.content == "How"
        assert yarns[1].choices[0].delta.content == " far!"


def test_gist_stream_get_ansa_after_complete(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        stream = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        list(stream)  # consume stream
        ansa = stream.get_ansa()
        assert isinstance(ansa, Ansa)
        assert ansa.text == "How far!"


def test_gist_stream_ansa_has_model(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        stream = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        list(stream)
        ansa = stream.get_ansa()
        assert ansa.model == "confam-speed"


def test_gist_stream_get_ansa_before_complete_raises(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response):
        stream = client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        with pytest.raises(RuntimeError, match="Stream not complete"):
            stream.get_ansa()


def test_gist_stream_passes_stream_true_to_litellm(client, mock_stream_response):
    with patch("confamnode.client.litellm.completion", return_value=mock_stream_response) as mock_call:
        client.gist(
            model=models.SPEED,
            messages="How far?",
            stream=True
        )
        call_args = mock_call.call_args
        assert call_args.kwargs.get("stream") == True
