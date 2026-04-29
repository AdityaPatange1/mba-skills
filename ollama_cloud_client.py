from __future__ import annotations

from typing import List, Dict

from ollama import Client

from config import AppConfig


class OllamaCloudClient:
    def __init__(self, config: AppConfig) -> None:
        self._client = Client(
            host=config.ollama_base_url,
            headers={"Authorization": f"Bearer {config.ollama_api_key}"},
        )
        self._model = config.ollama_model
        self._temperature = config.temperature
        self._max_tokens = config.max_tokens

    def chat(self, messages: List[Dict[str, str]]) -> str:
        response = self._client.chat(
            model=self._model,
            messages=messages,
            options={"temperature": self._temperature, "num_predict": self._max_tokens},
        )
        message = response.get("message", {})
        return str(message.get("content", "")).strip()
