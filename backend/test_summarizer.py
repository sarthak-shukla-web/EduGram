import pytest

from app.services import summarizer


def test_summarize_text_returns_summary(monkeypatch):
    expected_summary = "A stack follows the LIFO principle."

    def mock_generate_response(prompt):
        return expected_summary

    monkeypatch.setattr(
        summarizer,
        "generate_response",
        mock_generate_response,
    )

    result = summarizer.summarize_text(
        "A stack is a linear data structure that follows LIFO."
    )

    assert result == expected_summary


def test_summarize_text_rejects_empty_input():
    with pytest.raises((ValueError, TypeError)):
        summarizer.summarize_text("")