from app.core.settings import Settings
from app.integrations.providers.base import LLMProvider
from app.models.schemas import ChatMessage


class GenericProvider(LLMProvider):
    """Stub provider for Groq/Gemini/Claude showing extension points."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def generate(self, messages: list[ChatMessage], temperature: float = 0.3) -> str:
        last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        return f"[{self.settings.ai_provider}:{self.settings.ai_model}|temp={temperature}] {last_user}"

    def embed(self, text: str) -> list[float]:
        truncated = text[:16].rjust(16)
        return [ord(ch) / 255.0 for ch in truncated]
