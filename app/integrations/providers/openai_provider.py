from __future__ import annotations

import importlib

from app.core.settings import Settings
from app.integrations.providers.base import LLMProvider
from app.models.schemas import ChatMessage


class OpenAIProvider(LLMProvider):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None
        if settings.openai_api_key and importlib.util.find_spec("openai"):
            from openai import OpenAI

            self._client = OpenAI(api_key=settings.openai_api_key)

    def generate(self, messages: list[ChatMessage], temperature: float = 0.3) -> str:
        if self._client is None:
            last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
            return (
                f"[OpenAI stub:{self.settings.ai_model}] {last_user}\n"
                "Set OPENAI_API_KEY and install openai package to get real model outputs."
            )

        response = self._client.chat.completions.create(
            model=self.settings.ai_model,
            temperature=temperature,
            messages=[{"role": m.role, "content": m.content} for m in messages],
        )
        return response.choices[0].message.content or ""

    def embed(self, text: str) -> list[float]:
        if self._client is None:
            truncated = text[:16].ljust(16)
            return [ord(ch) / 255.0 for ch in truncated]

        embedding = self._client.embeddings.create(model=self.settings.embedding_model, input=text)
        return embedding.data[0].embedding
