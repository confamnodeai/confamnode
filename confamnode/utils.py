"""
Small internal helpers shared across the confamnode client.
"""


import re
from confamnode.exceptions import (
    ConfamAuthError,
    ConfamNodeError,
    ConfamRequestError,
    ConfamProviderError,
    ConfamRateLimitError,
    ConfamInsufficientBalanceError,
)


def extract_error(response) -> str:
    """
    Best-effort error detail from a non-2xx response, WITHOUT raising.
 
    The server's normal error shape is {"detail": "..."}, but gateway-level
    errors (e.g. a 429 throttle, a 502/504 from a proxy, a 524 origin timeout)
    often return an empty or non-JSON body. Calling response.json() directly on
    those bodies raises JSONDecodeError and swallows the status code -- the one
    thing the caller actually needs. So we parse defensively and always fall
    back to something readable.
 
    HTML error pages (Cloudflare, nginx, ...) are summarised to their <title>
    rather than dumped in full, so error messages and logs stay readable.
    """
    # 1. Normal JSON error shape.
    try:
        payload = response.json()
        if isinstance(payload, dict):
            detail = payload.get("detail") or payload.get("error") or payload.get("message")
            if detail:
                return str(detail)
    except Exception:
        pass

    text = (getattr(response, "text", "") or "").strip()
    if not text:
        return  "no response body"
    
    # 2. HTML error page: the full page is noise. Pull the <title>, which
    #    carries the human-readable status (e.g. "524: A timeout occurred").
    if "<html" in text[:200].lower() or "<!doctype html" in text[:200].lower():
        m = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
            if title:
                return title
        return "HTML error page (no title)"
    
    # 3. Plain-text body: return it, truncated so we never dump a wall.
    return text if len(text) <= 300 else text[:297] + "..."


def raise_for_status(response):
    """
    Maps an HTTP error response to correct typed ConfamNode exception.
    Shared by gist() and embed() so both endpoints raise consistently.

    The status code is always embedded in the raised message (e.g.
    "ConfamNode error 429: ...") regardless of which typed exception is
    used -- this keeps the status code visible/greppable in logs and
    error messages even though the exception TYPE is what callers should
    actually catch programmatically.
    """
    if response.status_code < 400:
        return

    error = extract_error(response)
    status = response.status_code
    msg = f"ConfamNode error {status}: {error}"


    if status == 401:
        raise ConfamAuthError(msg)
    if status == 402:
        raise ConfamInsufficientBalanceError(msg)
    if status == 429:
        raise ConfamRateLimitError(msg)
    if status in (502, 503, 504):
        raise ConfamProviderError(msg)
    if status < 500:
        raise ConfamRequestError(msg)
    # Genuinely unexpected 5xx not covered above
    raise ConfamNodeError(msg)

