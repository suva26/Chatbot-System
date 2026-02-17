from abc import ABC, abstractmethod

from app.models.schemas import ChatMessage


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, messages: list[ChatMessage], temperature: float = 0.3) -> str:
        raise NotImplementedError

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError
