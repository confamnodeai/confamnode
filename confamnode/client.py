import os
import litellm

from typing import Union, List, Dict

from confamnode import models
from confamnode.exceptions import ConfamAuthError, ConfamModelError

VALID_MODELS = [
    models.LITE,
    models.SPEED,
    models.REASONING,
    models.VISION,
    models.AUDIO,
    models.TTS,
    models.NANO
]

DEFAULT_BASE_URL = "https://api.confamnode.com/v1"


class ConfamNode:
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None
    ):
        # Pick up from environment if not provided
        api_key = api_key or os.environ.get("CONFAMNODE_API_KEY")

        if not api_key:
            raise ValueError("api_key is required")
        
        if not api_key.startswith("confam-sk-"):
            raise ConfamAuthError()
        
        self.api_key = api_key
        self.litellm_key = api_key.removeprefix("confam-")
        self.base_url = base_url or DEFAULT_BASE_URL

    def gist(
        self,
        model: str,
        messages: Union[str, List[Dict[str, str]]],
        **kwargs
    ) -> object:
        if model not in VALID_MODELS:
            raise ConfamModelError(model)
        
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        elif not isinstance(messages, list):
            raise ValueError("messages must be a string or list")
        
        response = litellm.completion(
            model=model,
            messages=messages,
            api_key=self.litellm_key,
            base_url=self.base_url,
            **kwargs
        )

        return response