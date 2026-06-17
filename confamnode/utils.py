def sanitize_raw(raw) -> dict:
    """
    Build sanitized raw dict.
    """
    return {
        "id": getattr(raw, "id", None),
        "finish_reason": getattr(
            getattr(raw, "choices", [None])[0],
            "finish_reason", None
        ) if getattr(raw, "choices", None) else None,
        "usage": {
            "prompt_tokens": getattr(getattr(raw, "usage", None), "prompt_tokens", 0),
            "completion_tokens": getattr(getattr(raw, "usage", None), "completion_tokens", 0),
        }
    }


def sanitize_stream_raw(chunks, finish_reason: str, usage) -> dict:
    """
    Build sanitized raw dict from streaming chunks.
    """
    return {
        "id": getattr(chunks[0], "id", None) if chunks else None,
        "finish_reason": finish_reason,
        "usage": {
            "prompt_tokens": getattr(usage, "prompt_tokens", 0),
            "completion_tokens": getattr(usage, "completion_tokens", 0),
        }
    }