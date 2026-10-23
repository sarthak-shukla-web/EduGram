from pathlib import Path

from app.services.ai_engine import AIEngineError
from app.services.pdf_processor import extract_text, PDFProcessingError
from app.services.summarizer import summarize_text
from app.services.topic_extractor import extract_topics
from app.services.learning_path import generate_learning_path


class DocumentAnalysisError(Exception):
    """Raised when document analysis fails."""


def analyze_document(file_path: str | Path) -> dict:
    """
    Analyze a PDF and return its extracted text, summary,
    topics, and recommended learning path.
    """

    # Step 1: Extract text from the PDF.
    try:
        extracted_text = extract_text(file_path)
    except PDFProcessingError:
        raise
    except Exception as exc:
        raise DocumentAnalysisError(
            "Could not extract text from the uploaded document."
        ) from exc

    # Step 2: Generate a summary.
    try:
        summary = summarize_text(extracted_text)
    except Exception as exc:
        raise DocumentAnalysisError(
            "Could not summarize the study material."
        ) from exc

    # Step 3: Extract topics and subtopics.
    try:
        topic_result = extract_topics(extracted_text)
        topics = topic_result["topics"]
    except Exception as exc:
        raise DocumentAnalysisError(
            "Could not identify topics in the study material."
        ) from exc

    if not topics:
        raise DocumentAnalysisError(
            "No topics could be identified in the study material."
        )

    # Step 4: Generate a recommended learning path.
    try:
        learning_path_result = generate_learning_path(topics)
    except Exception as exc:
        raise DocumentAnalysisError(
            "Could not generate a learning path."
        ) from exc

    # Step 5: Return all results together.
    return {
        "filename": Path(file_path).name,
        "summary": summary,
        "topics": topics,
        "learning_path": learning_path_result["learning_path"],
    }