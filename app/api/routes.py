from fastapi import APIRouter

from app.agents.workflows import AgentWorkflowService
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    DocumentIngestRequest,
    DocumentIngestResponse,
    RetrievalRequest,
    RetrievalResponse,
)
from app.services.chat_service import ChatService
from app.services.data_service import DataService
from app.services.document_service import DocumentService
from app.services.ml_exposure import deep_learning_runtime_status

router = APIRouter(tags=["chatbot"])
chat_service = ChatService()
doc_service = DocumentService()
agent_service = AgentWorkflowService()
data_service = DataService()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    return chat_service.chat(req)


@router.post("/documents/ingest", response_model=DocumentIngestResponse)
def ingest_document(req: DocumentIngestRequest) -> DocumentIngestResponse:
    return doc_service.ingest_document(doc_id=req.doc_id, text=req.text)


@router.post("/documents/retrieve", response_model=RetrievalResponse)
def retrieve(req: RetrievalRequest) -> RetrievalResponse:
    return doc_service.retrieve(query=req.query, top_k=req.top_k)


@router.get("/system/runtime")
def runtime_info() -> dict[str, dict[str, str]]:
    return {
        "deep_learning": deep_learning_runtime_status(),
        "agentic": agent_service.capability_report(),
    }


@router.get("/analytics/conversations")
def conversation_stats() -> dict[str, float]:
    return data_service.conversation_stats()
