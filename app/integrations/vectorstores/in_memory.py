from dataclasses import dataclass
import numpy as np

from app.integrations.vectorstores.base import VectorStore
from app.models.schemas import RetrievedChunk


@dataclass
class _VectorRecord:
    doc_id: str
    chunk_id: str
    text: str
    embedding: list[float]


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self.records: list[_VectorRecord] = []

    def upsert(self, doc_id: str, chunk_id: str, text: str, embedding: list[float]) -> None:
        self.records.append(
            _VectorRecord(
                doc_id=doc_id,
                chunk_id=chunk_id,
                text=text,
                embedding=embedding,
            )
        )

    def search(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        if not self.records:
            return []

        query = np.array(embedding, dtype=float)
        scored: list[RetrievedChunk] = []

        for record in self.records:
            candidate = np.array(record.embedding, dtype=float)
            denom = np.linalg.norm(query) * np.linalg.norm(candidate)

            score = float(np.dot(query, candidate) / denom) if denom else 0.0

            scored.append(
                RetrievedChunk(
                    doc_id=record.doc_id,
                    chunk_id=record.chunk_id,
                    score=score,
                    text=record.text,
                )
            )

        scored.sort(key=lambda item: item.score, reverse=True)

        return scored[:top_k]
