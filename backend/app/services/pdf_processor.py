from pathlib import Path

import pymupdf


MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB
MAX_PAGES = 100


class PDFProcessingError(Exception):
    """Raised when a PDF cannot be processed safely."""


def extract_text(file_path: str | Path) -> str:
    """
    Extract readable text from a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text from the document.

    Raises:
        PDFProcessingError: If the PDF is invalid, empty,
        too large, or contains no extractable text.
    """
    path = Path(file_path)

    if not path.is_file():
        raise PDFProcessingError("The requested file does not exist.")

    if path.suffix.lower() != ".pdf":
        raise PDFProcessingError("Only PDF files are supported.")

    if path.stat().st_size > MAX_FILE_SIZE:
        raise PDFProcessingError("The PDF exceeds the 15 MB limit.")

    if path.stat().st_size == 0:
        raise PDFProcessingError("The uploaded file is empty.")

    try:
        with pymupdf.open(path) as document:
            if document.needs_pass:
                raise PDFProcessingError(
                    "Password-protected PDFs are not supported."
                )

            if len(document) == 0:
                raise PDFProcessingError("The PDF contains no pages.")

            if len(document) > MAX_PAGES:
                raise PDFProcessingError(
                    f"The PDF exceeds the {MAX_PAGES}-page limit."
                )

            extracted_pages = []

            for page in document:
                page_text = page.get_text("text").strip()

                if page_text:
                    extracted_pages.append(page_text)

            text = "\n\n".join(extracted_pages).strip()

            if not text:
                raise PDFProcessingError(
                    "No readable text was found. "
                    "The PDF may contain scanned images."
                )

            return text

    except PDFProcessingError:
        raise
    except Exception as exc:
        raise PDFProcessingError(
            "The PDF could not be read. Please check the file."
        ) from exc