import pytest

from app.services import ai_engine


def test_generate_response_returns_ai_content(monkeypatch):
    expected_content = "A stack follows the LIFO principle."

    def mock_chat(**kwargs):
        assert kwargs["model"] == ai_engine.MODEL_NAME
        assert len(kwargs["messages"]) == 2

        return {
            "message": {
                "content": expected_content
            }
        }

    monkeypatch.setattr(ai_engine.ollama, "chat", mock_chat)

    result = ai_engine.generate_response(
        "Explain the stack data structure."
    )

    assert result == expected_content


def test_generate_response_strips_whitespace(monkeypatch):
    def mock_chat(**kwargs):
        return {
            "message": {
                "content": "  EduGram AI response  \n"
            }
        }

    monkeypatch.setattr(ai_engine.ollama, "chat", mock_chat)

    result = ai_engine.generate_response("Explain a stack.")

    assert result == "EduGram AI response"


def test_generate_response_rejects_empty_prompt():
    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        ai_engine.generate_response("")


def test_generate_response_rejects_blank_prompt():
    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        ai_engine.generate_response("   ")


def test_generate_response_supports_structured_output(monkeypatch):
    response_schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"}
        },
        "required": ["summary"],
    }

    def mock_chat(**kwargs):
        assert kwargs["format"] == response_schema

        return {
            "message": {
                "content": '{"summary": "A stack follows LIFO."}'
            }
        }

    monkeypatch.setattr(ai_engine.ollama, "chat", mock_chat)

    result = ai_engine.generate_response(
        "Summarize a stack.",
        response_format=response_schema,
    )

    assert result == '{"summary": "A stack follows LIFO."}'


def test_generate_response_wraps_ollama_errors(monkeypatch):
    def mock_chat(**kwargs):
        raise RuntimeError("Simulated Ollama failure")

    monkeypatch.setattr(ai_engine.ollama, "chat", mock_chat)

    with pytest.raises(ai_engine.AIEngineError, match="Could not generate"):
        ai_engine.generate_response("Explain a stack.")


def test_generate_response_rejects_empty_ai_response(monkeypatch):
    def mock_chat(**kwargs):
        return {
            "message": {
                "content": "   "
            }
        }

    monkeypatch.setattr(ai_engine.ollama, "chat", mock_chat)

    with pytest.raises(ai_engine.AIEngineError, match="empty response"):
        ai_engine.generate_response("Explain a stack.")