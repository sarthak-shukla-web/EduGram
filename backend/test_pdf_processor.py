import pytest
import fitz

from app.services.pdf_processor import (
    PDFProcessingError,
    extract_text,
)


def create_pdf(tmp_path, text="EduGram PDF testing"):
    """Create a small PDF for testing."""
    pdf_path = tmp_path / "sample.pdf"

    with fitz.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), text)
        document.save(pdf_path)

    return pdf_path


def test_extract_text_from_valid_pdf(tmp_path):
    pdf_path = create_pdf(tmp_path)

    result = extract_text(pdf_path)

    assert isinstance(result, str)
    assert "EduGram PDF testing" in result


def test_reject_invalid_pdf(tmp_path):
    pdf_path = tmp_path / "invalid.pdf"
    pdf_path.write_text("This is not a valid PDF.")

    with pytest.raises(PDFProcessingError):
        extract_text(pdf_path)


def test_reject_missing_pdf():
    with pytest.raises(PDFProcessingError):
        extract_text("file_that_does_not_exist.pdf")