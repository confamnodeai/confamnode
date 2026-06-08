import os
import litellm

from typing import Union, List, Dict

from confamnode import models
from confamnode.ansa import Ansa, Usage, Cost
from confamnode.exceptions import ConfamAuthError, ConfamModelError

VALID_MODELS = [
    models.LITE,
    models.SPEED,
    models.REASONING,

    models.INTELLIGENCE,
    models.DEEP_REASONING,
    models.CODE,
    models.CODE_PRO,
    models.VISION,
    models.AUDIO,
    models.TTS,
    
    models.NANO,

    models.EMBED_TEXT,
    models.EMBED_MULTIMODAL,
    models.EMBED_MULTIMODAL_2,

    # Paid embeddings
    models.EMBED_TEXT_PRO,
    models.EMBED_MULTIMODAL_PRO,
    models.EMBED_MULTILINGUAL,
    models.EMBED_SMALL,
    models.EMBED_0_6B,
    models.EMBED_TEXT_LOCAL,

    # Rerank
    models.RERANK,
    models.RERANK_FAST,
]

DEFAULT_BASE_URL = "https://api.confamnode.com/v1"
DEFAULT_USD_TO_NAIRA = 1400.0

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
        
        raw = litellm.completion(
            model=f"openai/{model}",
            messages=messages,
            api_key=self.litellm_key,
            base_url=self.base_url,
            **kwargs
        )

        if kwargs.get("stream", False):
            return ConfamStream(raw, model)

        hidden = getattr(raw, "_hidden_params", {})
        naira_cost = float(hidden.get("x_confam_naira_cost", 0.0))
        naira_input = float(hidden.get("x_confam_naira_input", 0.0))
        naira_output = float(hidden.get("x_confam_naira_output", 0.0))
        usd_cost = hidden.get("x_confam_usd_cost", None)
        if usd_cost is not None:
            usd_cost = float(usd_cost)

        # Extract text
        text = raw.choices[0].message.content or ""

        # Extract reasoning if present
        reasoning = getattr(raw.choices[0].message, "reasoning_content", None)

        # Extract tool calls if present
        tools = []
        if hasattr(raw.choices[0].message, "tool_calls") and raw.choices[0].message.tool_calls:
            tools = raw.choices[0].message.tool_calls

        # Extract citations
        citations = []
        if hasattr(raw.choices[0].message, "citations") and raw.choices[0].message.citations:
            citations = raw.choices[0].message.citations

        # Extract usage
        usage = Usage(
            prompt_tokens=raw.usage.prompt_tokens,
            completion_tokens=raw.usage.completion_tokens,
            total_tokens=raw.usage.total_tokens,
        )

        cost = Cost(
            naira=naira_cost,
            naira_input=naira_input,
            naira_output=naira_output,
            dollars=usd_cost
        )

        return Ansa(
            text=text,
            model=model,
            reasoning=reasoning,
            tools=tools,
            citations=citations,
            usage=usage,
            cost=cost,
            finish_reason=raw.choices[0].finish_reason,
            raw=raw,
        )
    

class ConfamStream:
    def __init__(self, raw_stream, model: str):
        self._raw_stream = raw_stream
        self._model = model
        self._chunks = []
        self._ansa = None

    def __iter__(self):
        for yarn in self._raw_stream:
            self._chunks.append(yarn)
            yield yarn
        # Build Ansa after stream completes
        self._ansa = self._build_ansa()

    def get_ansa(self) -> Ansa:
        if self._ansa is None:
            raise RuntimeError("Stream not complete yet. Iterate through all chunks first.")
        return self._ansa
    
    def _build_ansa(self) -> Ansa:
        # Collect text from all chunks
        text = "".join([
            c.choices[0].delta.content or ""
            for c in self._chunks
            if c.choices[0].delta.content
        ])

        # Get finish reason from last chunk
        finish_reason = self._chunks[-1].choices[0].finish_reason if self._chunks else "stop"

        # Usage — only available in last chunk for some providers
        last_chunk = self._chunks[-1] if self._chunks else None
        usage = Usage(
            prompt_tokens=getattr(getattr(last_chunk, "usage", None), "prompt_tokens", 0),
            completion_tokens=getattr(getattr(last_chunk, "usage", None), "completion_tokens", 0),
            total_tokens=getattr(getattr(last_chunk, "usage", None), "total_tokens", 0),
        )

        cost = Cost(naira=0.0) 

        return Ansa(
            text=text,
            model=self._model,
            usage=usage,
            cost=cost,
            finish_reason=finish_reason,
            raw=self._chunks,
        )