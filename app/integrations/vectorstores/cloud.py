from app.integrations.vectorstores.base import VectorStore
from app.models.schemas import RetrievedChunk


class PgVectorStore(VectorStore):
    def upsert(self, doc_id: str, chunk_id: str, text: str, embedding: list[float]) -> None:
        raise NotImplementedError("Wire pgvector SQL insert/update here.")

    def search(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        raise NotImplementedError("Wire pgvector similarity query here.")


class PineconeStore(VectorStore):
    def upsert(self, doc_id: str, chunk_id: str, text: str, embedding: list[float]) -> None:
        raise NotImplementedError("Wire Pinecone upsert here.")

    def search(self, embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        raise NotImplementedError("Wire Pinecone query here.")
