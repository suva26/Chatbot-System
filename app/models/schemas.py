from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=2)
    message: str = Field(..., min_length=1)
    session_id: str | None = None
    system_prompt: str = Field(
        default="You are a helpful AI assistant. Provide clear, concise, and accurate answers.",
        min_length=10,
    )
    temperature: float = Field(default=0.3, ge=0.0, le=1.5)


class ChatResponse(BaseModel):
    response: str
    session_id: str
    provider: str
    model: str
    history: list[ChatMessage] = Field(default_factory=list)


class DocumentChunk(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentIngestRequest(BaseModel):
    doc_id: str
    text: str
    source: str = "upload"


class DocumentIngestResponse(BaseModel):
    doc_id: str
    chunks: int
    vector_backend: str


class RetrievalRequest(BaseModel):
    query: str
    top_k: int = Field(default=3, ge=1, le=20)


class RetrievedChunk(BaseModel):
    doc_id: str
    chunk_id: str
    score: float
    text: str


class RetrievalResponse(BaseModel):
    results: list[RetrievedChunk]
