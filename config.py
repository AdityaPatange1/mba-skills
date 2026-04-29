from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    ollama_api_key: str
    ollama_base_url: str
    ollama_model: str
    temperature: float
    max_tokens: int


def load_config(model_override: str | None = None) -> AppConfig:
    load_dotenv()
    api_key = os.getenv("OLLAMA_API_KEY", "").strip()
    base_url = os.getenv("OLLAMA_BASE_URL", "https://ollama.com").strip()
    model = model_override or os.getenv("OLLAMA_MODEL", "llama3.1:8b-instruct-q8_0").strip()

    if not api_key:
        raise ValueError("OLLAMA_API_KEY is required. Set it in your .env file.")

    return AppConfig(
        ollama_api_key=api_key,
        ollama_base_url=base_url,
        ollama_model=model,
        temperature=float(os.getenv("OLLAMA_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("OLLAMA_MAX_TOKENS", "800")),
    )
