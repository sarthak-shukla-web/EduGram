import pytest

from app.services import document_analyzer
from app.services.pdf_processor import PDFProcessingError
from app.services.document_analyzer import DocumentAnalysisError


def mock_pipeline(monkeypatch):
    """Mock all four stages of the document-analysis pipeline."""

    monkeypatch.setattr(
        document_analyzer,
        "extract_text",
        lambda file_path: "Sample study material about stacks.",
    )

    monkeypatch.setattr(
        document_analyzer,
        "summarize_text",
        lambda text: "A stack follows the LIFO principle.",
    )

    monkeypatch.setattr(
        document_analyzer,
        "extract_topics",
        lambda text: {
            "topics": [
                {
                    "name": "Stacks",
                    "subtopics": ["LIFO", "Push", "Pop"],
                    "description": "A Last In, First Out data structure.",
                }
            ]
        },
    )

    monkeypatch.setattr(
        document_analyzer,
        "generate_learning_path",
        lambda topics: {
            "learning_path": [
                {
                    "order": 1,
                    "topic": "Stacks",
                    "reason": "Start with the stack's basic concept.",
                }
            ]
        },
    )


def test_analyze_document_returns_complete_result(monkeypatch, tmp_path):
    mock_pipeline(monkeypatch)

    pdf_path = tmp_path / "sample.pdf"
    pdf_path.touch()

    result = document_analyzer.analyze_document(pdf_path)

    assert result["filename"] == "sample.pdf"
    assert result["summary"] == "A stack follows the LIFO principle."
    assert len(result["topics"]) == 1
    assert result["topics"][0]["name"] == "Stacks"
    assert len(result["learning_path"]) == 1
    assert result["learning_path"][0]["topic"] == "Stacks"


def test_analyze_document_propagates_pdf_processing_error(
    monkeypatch, tmp_path
):
    def mock_extract_text(file_path):
        raise PDFProcessingError("Invalid PDF.")

    monkeypatch.setattr(
        document_analyzer,
        "extract_text",
        mock_extract_text,
    )

    with pytest.raises(PDFProcessingError, match="Invalid PDF"):
        document_analyzer.analyze_document(tmp_path / "invalid.pdf")


def test_analyze_document_handles_summary_failure(monkeypatch, tmp_path):
    mock_pipeline(monkeypatch)

    def mock_summarize_text(text):
        raise RuntimeError("Simulated summary failure")

    monkeypatch.setattr(
        document_analyzer,
        "summarize_text",
        mock_summarize_text,
    )

    with pytest.raises(
        DocumentAnalysisError,
        match="Could not summarize",
    ):
        document_analyzer.analyze_document(tmp_path / "sample.pdf")


def test_analyze_document_handles_empty_topics(monkeypatch, tmp_path):
    mock_pipeline(monkeypatch)

    monkeypatch.setattr(
        document_analyzer,
        "extract_topics",
        lambda text: {"topics": []},
    )

    with pytest.raises(
        DocumentAnalysisError,
        match="No topics could be identified",
    ):
        document_analyzer.analyze_document(tmp_path / "sample.pdf")