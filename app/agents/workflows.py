import importlib


class AgentWorkflowService:
    """Basic exposure layer for LangGraph/CrewAI capabilities."""

    def capability_report(self) -> dict[str, str]:
        langgraph = importlib.util.find_spec("langgraph") is not None
        crewai = importlib.util.find_spec("crewai") is not None
        return {
            "langgraph": "available" if langgraph else "not_installed",
            "crewai": "available" if crewai else "not_installed",
        }
