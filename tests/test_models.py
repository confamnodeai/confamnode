from confamnode.models import (
    LITE,
    SPEED,
    REASONING,
    VISION,
    AUDIO,
    TTS,
    NANO,
    EMBED_TEXT,
    EMBED_MULTIMODAL,
    EMBED_MULTIMODAL_2,
    EMBED_TEXT_LOCAL
)

def test_model_constants_are_strings():
    assert isinstance(LITE, str)
    assert isinstance(SPEED, str)
    assert isinstance(REASONING, str)
    assert isinstance(VISION, str)
    assert isinstance(AUDIO, str)
    assert isinstance(TTS, str)
    assert isinstance(NANO, str)
    assert isinstance(EMBED_TEXT, str)
    assert isinstance(EMBED_MULTIMODAL, str)
    assert isinstance(EMBED_MULTIMODAL_2, str)
    assert isinstance(EMBED_TEXT_LOCAL, str)


def test_model_constants_start_with_confam():
    assert LITE.startswith("confam-")
    assert SPEED.startswith("confam-")
    assert REASONING.startswith("confam-")
    assert VISION.startswith("confam-")
    assert AUDIO.startswith("confam-")
    assert TTS.startswith("confam-")
    assert NANO.startswith("confam-")
    assert EMBED_TEXT.startswith("confam-")
    assert EMBED_MULTIMODAL.startswith("confam-")
    assert EMBED_MULTIMODAL_2.startswith("confam-")
    assert EMBED_TEXT_LOCAL.startswith("confam-")


def test_model_constants_have_correct_values():
    assert LITE == "confam-lite"
    assert SPEED == "confam-speed"
    assert REASONING == "confam-reasoning"
    assert VISION == "confam-vision"
    assert AUDIO == "confam-audio"
    assert TTS == "confam-tts"
    assert NANO == "confam-nano"
    assert EMBED_TEXT == "confam-embed-text-1"
    assert EMBED_MULTIMODAL == "confam-embed-multimodal-1"
    assert EMBED_MULTIMODAL_2 == "confam-embed-multimodal-2"
    assert EMBED_TEXT_LOCAL == "confam-embed-text-local"

