from confamnode.models import (
    LITE, SPEED, REASONING,
    INTELLIGENCE, DEEP_REASONING, CODE, CODE_PRO, VISION, AUDIO, TTS,
    NANO,
    EMBED_TEXT, EMBED_MULTIMODAL, EMBED_MULTIMODAL_2, EMBED_TEXT_LOCAL,
    EMBED_TEXT_PRO, EMBED_MULTIMODAL_PRO, EMBED_MULTILINGUAL,
    EMBED_SMALL, EMBED_0_6B,
    RERANK, RERANK_FAST,
)


def test_model_constants_are_strings():
    assert isinstance(LITE, str)
    assert isinstance(SPEED, str)
    assert isinstance(REASONING, str)
    assert isinstance(INTELLIGENCE, str)
    assert isinstance(DEEP_REASONING, str)
    assert isinstance(CODE, str)
    assert isinstance(CODE_PRO, str)
    assert isinstance(VISION, str)
    assert isinstance(AUDIO, str)
    assert isinstance(TTS, str)
    assert isinstance(NANO, str)
    assert isinstance(EMBED_TEXT, str)
    assert isinstance(EMBED_MULTIMODAL, str)
    assert isinstance(EMBED_MULTIMODAL_2, str)
    assert isinstance(EMBED_TEXT_LOCAL, str)
    assert isinstance(EMBED_TEXT_PRO, str)
    assert isinstance(EMBED_MULTIMODAL_PRO, str)
    assert isinstance(EMBED_MULTILINGUAL, str)
    assert isinstance(EMBED_SMALL, str)
    assert isinstance(EMBED_0_6B, str)
    assert isinstance(RERANK, str)
    assert isinstance(RERANK_FAST, str)


def test_model_constants_start_with_confam():
    assert LITE.startswith("confam-")
    assert SPEED.startswith("confam-")
    assert REASONING.startswith("confam-")
    assert INTELLIGENCE.startswith("confam-")
    assert DEEP_REASONING.startswith("confam-")
    assert CODE.startswith("confam-")
    assert CODE_PRO.startswith("confam-")
    assert VISION.startswith("confam-")
    assert AUDIO.startswith("confam-")
    assert TTS.startswith("confam-")
    assert NANO.startswith("confam-")
    assert EMBED_TEXT.startswith("confam-")
    assert EMBED_MULTIMODAL.startswith("confam-")
    assert EMBED_MULTIMODAL_2.startswith("confam-")
    assert EMBED_TEXT_LOCAL.startswith("confam-")
    assert EMBED_TEXT_PRO.startswith("confam-")
    assert EMBED_MULTIMODAL_PRO.startswith("confam-")
    assert EMBED_MULTILINGUAL.startswith("confam-")
    assert EMBED_SMALL.startswith("confam-")
    assert EMBED_0_6B.startswith("confam-")
    assert RERANK.startswith("confam-")
    assert RERANK_FAST.startswith("confam-")


def test_model_constants_have_correct_values():
    assert LITE == "confam-lite"
    assert SPEED == "confam-speed"
    assert REASONING == "confam-reasoning"
    assert INTELLIGENCE == "confam-intelligence"
    assert DEEP_REASONING == "confam-deep-reasoning"
    assert CODE == "confam-code"
    assert CODE_PRO == "confam-code-pro"
    assert VISION == "confam-vision"
    assert AUDIO == "confam-audio"
    assert TTS == "confam-tts"
    assert NANO == "confam-nano"
    assert EMBED_TEXT == "confam-embed-text-1"
    assert EMBED_MULTIMODAL == "confam-embed-multimodal-1"
    assert EMBED_MULTIMODAL_2 == "confam-embed-multimodal-2"
    assert EMBED_TEXT_LOCAL == "confam-embed-text-local"
    assert EMBED_TEXT_PRO == "confam-embed-text-pro"
    assert EMBED_MULTIMODAL_PRO == "confam-embed-multimodal-pro"
    assert EMBED_MULTILINGUAL == "confam-embed-multilingual"
    assert EMBED_SMALL == "confam-embed-small"
    assert EMBED_0_6B == "confam-embed-0.6b"
    assert RERANK == "confam-rerank"
    assert RERANK_FAST == "confam-rerank-fast"