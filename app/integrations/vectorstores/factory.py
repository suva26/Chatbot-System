from app.core.settings import get_settings
from app.integrations.vectorstores.base import VectorStore
from app.integrations.vectorstores.cloud import PgVectorStore, PineconeStore
from app.integrations.vectorstores.in_memory import InMemoryVectorStore

_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _store

    if _store is not None:
        return _store

    settings = get_settings()

    if settings.vector_backend.lower() == "pgvector":
        _store = PgVectorStore()
    elif settings.vector_backend.lower() == "pinecone":
        _store = PineconeStore()
    else:
        _store = InMemoryVectorStore()

    return _store
