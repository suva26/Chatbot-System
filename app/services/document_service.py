from dataclasses import dataclass

from app.core.settings import get_settings
from app.integrations.providers.factory import get_provider
from app.integrations.vectorstores.factory import get_vector_store
from app.models.schemas import DocumentIngestResponse, RetrievalResponse


@dataclass
class Chunker:
    chunk_size: int = 400
    overlap: int = 50

    def split(self, text: str) -> list[str]:
        if len(text) <= self.chunk_size:
            return [text]

        chunks: list[str] = []
        step = self.chunk_size - self.overlap
        for start in range(0, len(text), step):
            chunks.append(text[start : start + self.chunk_size])
        return chunks


class DocumentService:
    def __init__(self) -> None:
        self.provider = get_provider()
        self.vector_store = get_vector_store()
        self.chunker = Chunker()

    def ingest_document(self, doc_id: str, text: str) -> DocumentIngestResponse:
        parts = self.chunker.split(text)
        for idx, chunk in enumerate(parts):
            chunk_id = f"{doc_id}-{idx}"
            embedding = self.provider.embed(chunk)
            self.vector_store.upsert(doc_id=doc_id, chunk_id=chunk_id, text=chunk, embedding=embedding)

        settings = get_settings()
        return DocumentIngestResponse(doc_id=doc_id, chunks=len(parts), vector_backend=settings.vector_backend)

    def retrieve(self, query: str, top_k: int) -> RetrievalResponse:
        embedding = self.provider.embed(query)
        return RetrievalResponse(results=self.vector_store.search(embedding=embedding, top_k=top_k))
