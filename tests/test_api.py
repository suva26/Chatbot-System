from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_document_and_chat_flow_with_session_memory() -> None:
    ingest = client.post(
        "/api/documents/ingest",
        json={"doc_id": "doc-1", "text": "FastAPI and vector databases enable document chat."},
    )
    assert ingest.status_code == 200
    assert ingest.json()["chunks"] >= 1

    first = client.post(
        "/api/chat",
        json={"user_id": "u1", "message": "How can document chat work?"},
    )
    assert first.status_code == 200
    first_payload = first.json()
    assert "response" in first_payload
    assert first_payload["provider"]
    assert first_payload["model"]
    assert len(first_payload["history"]) >= 2

    second = client.post(
        "/api/chat",
        json={
            "user_id": "u1",
            "session_id": first_payload["session_id"],
            "message": "Can you summarize your previous answer?",
        },
    )
    assert second.status_code == 200
    second_payload = second.json()
    assert second_payload["session_id"] == first_payload["session_id"]
    assert len(second_payload["history"]) >= 4


def test_runtime_info() -> None:
    resp = client.get("/api/system/runtime")
    assert resp.status_code == 200
    assert "deep_learning" in resp.json()
    assert "agentic" in resp.json()
