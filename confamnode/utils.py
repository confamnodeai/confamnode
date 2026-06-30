"""
Small internal helpers shared across the confamnode client.
"""


def extract_error(response) -> str:
    """
    Best-effort error detail from a non-2xx response, WITHOUT raising.
 
    The server's normal error shape is {"detail": "..."}, but gateway-level
    errors (e.g. a 429 throttle, a 502/504 from a proxy) often return an
    empty or non-JSON body. Calling response.json() directly on those bodies
    raises JSONDecodeError and swallows the status code -- the one thing the
    caller actually needs. So we parse defensively and always fall back to
    the raw text, then to a status-only message.
    """
    try:
        payload = response.json()
        if isinstance(payload, dict):
            detail = payload.get("detail") or payload.get("error") or payload.get("message")
            if detail:
                return str(detail)
    except Exception:
        pass
    text = (getattr(response, "text", "") or "").strip()
    return text or "no response body"