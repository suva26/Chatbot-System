from app.core.settings import get_settings
from app.integrations.providers.base import LLMProvider
from app.integrations.providers.openai_provider import OpenAIProvider
from app.integrations.providers.gemini_provider import GeminiProvider
from app.integrations.providers.generic_provider import GenericProvider


def get_provider() -> LLMProvider:
    settings = get_settings()

    if settings.ai_provider == "openai":
        return OpenAIProvider(settings)

    if settings.ai_provider == "gemini":
        return GeminiProvider(settings)

    return GenericProvider(settings)
