import importlib


def deep_learning_runtime_status() -> dict[str, str]:
    torch_available = importlib.util.find_spec("torch") is not None
    tf_available = importlib.util.find_spec("tensorflow") is not None
    return {
        "pytorch": "available" if torch_available else "not_installed",
        "tensorflow": "available" if tf_available else "not_installed",
    }
