from abc import ABC, abstractmethod

from app.models.schemas import RetrievedChunk


class VectorStore(ABC):
    @abstractmethod
    def upsert(self, doc_id: str, chunk_id: str, text: str, embedding: list[float]) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        raise NotImplementedError
