import importlib
import uuid

from app.core.settings import get_settings
from app.integrations.providers.factory import get_provider
from app.models.schemas import ChatMessage, ChatRequest, ChatResponse
from app.services.data_service import DataService
from app.services.document_service import DocumentService


class ChatService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.provider = get_provider()
        self.docs = DocumentService()
        self.data = DataService()

    def _rag_context(self, message: str) -> str:
        retrieval = self.docs.retrieve(query=message, top_k=3)
        context = "\n".join(item.text for item in retrieval.results)
        return context.strip()

    def _tooling_status(self, prompt: str) -> str:
        langchain = importlib.util.find_spec("langchain")
        llama_index = importlib.util.find_spec("llama_index")
        return (
            ("LangChain available" if langchain else "LangChain unavailable")
            + " | "
            + ("LlamaIndex available" if llama_index else f"LlamaIndex unavailable, prompt size={len(prompt)}")
        )

    def chat(self, req: ChatRequest) -> ChatResponse:
        session_id = req.session_id or str(uuid.uuid4())
        context = ""
        history = self.data.get_recent_messages(session_id=session_id, limit=8)

        messages: list[ChatMessage] = [ChatMessage(role="system", content=req.system_prompt)]
        messages.extend(history)
        messages.append(
            ChatMessage(
                role="system",
                content=(
                    "Use retrieved knowledge if relevant. If not, answer directly. "
                    f"Retrieved context:\n{context or 'N/A'}\n"
                    f"Tooling checks: {self._tooling_status(req.message)}"
                ),
            )
        )
        messages.append(ChatMessage(role="user", content=req.message))

        answer = self.provider.generate(messages=messages, temperature=req.temperature)

        self.data.append_message(session_id=session_id, role="user", content=req.message)
        self.data.append_message(session_id=session_id, role="assistant", content=answer)
        self.data.log_chat_event(req.user_id, session_id, req.message, answer)

        updated_history = self.data.get_recent_messages(session_id=session_id, limit=10)
        return ChatResponse(
            response=answer,
            session_id=session_id,
            provider=self.provider.__class__.__name__,
            model=self.settings.ai_model,
            history=updated_history,
        )
