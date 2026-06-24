import os
import json
import httpx

from typing import Union, List, Dict

from confamnode.builders import parse_chunk
from confamnode.ansa import Ansa, Usage, Cost
from confamnode.registry import VALID_MODELS
from confamnode.exceptions import ConfamAuthError, ConfamModelError
from confamnode.config import DEFAULT_BASE_URL, DEFAULT_TIMEOUT, DEFAULT_CONNECT_TIMEOUT


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
        
        if not api_key.startswith("confam-"):
            raise ConfamAuthError()
        
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_BASE_URL

    def gist(
        self,
        model: str,
        messages: Union[str, List[Dict[str, str]]],
        system: str | None = "default",
        **kwargs
    ) -> "Ansa | ConfamStream":
        if model not in VALID_MODELS:
            raise ConfamModelError(model)
        
        # Handle string messages
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        elif not isinstance(messages, list):
            raise ValueError("messages must be a string or list")
        
        body = {
            "model": model,
            "messages": messages,
            **kwargs
        }

        # System message tri-state
        has_system_in_messages = any(m.get("role") == "system" for m in messages)
        if not has_system_in_messages:
            if system == "default":
                pass 
            else:
                body["system"] = system # None or custom string

        if kwargs.get("stream", False):
            http_client = httpx.Client(
                timeout=httpx.Timeout(DEFAULT_TIMEOUT, connect=DEFAULT_CONNECT_TIMEOUT)
            )
            req = http_client.build_request(
                "POST",
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=body,
            )
            stream_response = http_client.send(req, stream=True)

            if stream_response.status_code >= 400:
                stream_response.read()
                stream_response.close()
                http_client.close()
                error = stream_response.json().get("detail", "Requeest failed")
                raise Exception(f"ConfamNode error {stream_response.status_code}: {error}")
            
            return ConfamStream(stream_response, http_client, model)
        
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=httpx.Timeout(DEFAULT_TIMEOUT, connect=DEFAULT_CONNECT_TIMEOUT)
        )

        if response.status_code >= 400:
            error = response.json().get("detail", "Request failed")
            raise Exception(f"ConfamNode error {response.status_code}: {error}")

        data = response.json()
        msg = data["choices"][0]["message"]
        usage_data = data.get("usage", {})
        confam = data.get("confam", {})
        cost_data = confam.get("cost", {})

        return Ansa(
            id=confam.get("request_id", data.get("id", "")),
            text=msg.get("content") or "",
            model=model,
            reasoning=msg.get("reasoning"),
            tools=msg.get("tool_calls") or [],
            citations=msg.get("citations") or [],
            usage=Usage(
                prompt_tokens=usage_data.get("prompt_tokens", 0),
                completion_tokens=usage_data.get("completion_tokens", 0),
                total_tokens=usage_data.get("total_tokens", 0),
            ),
            cost=Cost(
                naira=cost_data.get("naira", 0.0),
                naira_input=cost_data.get("naira_input", 0.0),
                naira_output=cost_data.get("naira_output", 0.0),
            ),
            finish_reason=data["choices"][0].get("finish_reason", "stop"),
            raw={
                "id": data.get("id"),
                "usage": {
                    "prompt_tokens": usage_data.get("prompt_tokens", 0),
                    "completion_tokens": usage_data.get("completion_tokens", 0)
                }
            },
            is_local=confam.get("is_local", False),
            is_ngn_data_residency=confam.get("is_ngn_data_residency", False),
        )
    

class ConfamStream:
    def __init__(self, stream_response, http_client, model: str):
        self._stream_response = stream_response
        self._http_client = http_client
        self._model = model
        self._chunks = []
        self._ansa = None
        self._confam_meta = {}

    def __iter__(self):
        try:
            for line in self._stream_response.iter_lines():
                if not line or not line.startswith("data: "):
                    continue
                payload_str = line[len("data: "):]
                if payload_str.strip() == "[DONE]":
                    break
                try:
                    raw = json.loads(payload_str)
                except json.JSONDecodeError:
                    continue

                if "confam" in raw:
                    self._confam_meta = raw["confam"]
                    continue

                if not raw.get("choices"):
                    continue

                chunk = parse_chunk(raw)
                self._chunks.append(chunk)
                yield chunk
        finally:
            self._stream_response.close()
            self._http_client.close()

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
            if c.choices and c.choices[0].delta.content
        ])

        # Get finish reason from last chunk
        if self._chunks and self._chunks[-1].choices:
            finish_reason = self._chunks[-1].choices[0].finish_reason or "stop"

        usage_data = self._confam_meta.get("usage", {})
        cost_data = self._confam_meta.get("cost", {})

        return Ansa(
            id=self._confam_meta.get("request_id", ""),
            text=text,
            model=self._model,
            usage=Usage(
                prompt_tokens=usage_data.get("prompt_tokens", 0), 
                completion_tokens=usage_data.get("completion_tokens", 0), 
                total_tokens=usage_data.get("total_tokens", 0),
            ),
            cost=Cost(
                naira=cost_data.get("naira", 0.0),
                naira_input=cost_data.get("naira_input", 0.0),
                naira_output=cost_data.get("naira_output", 0.0),
            ),
            finish_reason=finish_reason,
            raw={
                "id": self._confam_meta.get("request_id", ""),
                "usage": {
                    "prompt_tokens": usage_data.get("prompt_tokens", 0), 
                    "completion_tokens": usage_data.get("completion_tokens", 0),
                    "total_tokens": usage_data.get("total_tokens", 0)
                }
            },
            is_local=self._confam_meta.get("is_local", False),
            is_ngn_data_residency=self._confam_meta.get("is_ngn_data_residency", False),
        )