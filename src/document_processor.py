from pathlib import Path
import re

import pymupdf
import pytesseract
from pypdf import PdfReader


# ---------------------------------------------------------
# Tesseract configuration
# ---------------------------------------------------------

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ---------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Normalize extracted PDF/OCR text into clean readable text.
    """

    # Convert all whitespace characters into a single space.
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------------
# Normal PDF text extraction
# ---------------------------------------------------------

def extract_text_with_pypdf(file_path: str) -> str:
    """
    Extract text from a normal text-based PDF using pypdf.
    """

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


# ---------------------------------------------------------
# OCR extraction
# ---------------------------------------------------------

def extract_text_with_ocr(file_path: str) -> str:
    """
    Extract text from scanned/image-based PDFs using OCR.
    """

    document = pymupdf.open(file_path)

    pages = []

    total_pages = len(document)

    for page_number, page in enumerate(
        document,
        start=1
    ):

        print(
            f"OCR processing page "
            f"{page_number}/{total_pages}..."
        )

        # -------------------------------------------------
        # Render PDF page as a high-resolution image
        # -------------------------------------------------

        pixmap = page.get_pixmap(
            matrix=pymupdf.Matrix(2, 2),
            alpha=False
        )

        # Convert Pixmap into a PIL image.
        image = pixmap.pil_image()

        # -------------------------------------------------
        # Run Tesseract OCR
        # -------------------------------------------------

        text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        if text:
            pages.append(text)

    document.close()

    return "\n\n".join(pages)


# ---------------------------------------------------------
# Main PDF extraction function
# ---------------------------------------------------------

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF.

    First attempts normal PDF text extraction.

    If little or no text is extracted,
    automatically falls back to OCR.
    """

    path = Path(file_path)

    # -----------------------------------------------------
    # Validate file
    # -----------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {file_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            "The provided file is not a PDF."
        )

    print(
        f"\nReading PDF: {file_path}"
    )

    # -----------------------------------------------------
    # Step 1: Normal PDF extraction
    # -----------------------------------------------------

    print(
        "Trying normal PDF text extraction..."
    )

    raw_text = extract_text_with_pypdf(
        file_path
    )

    cleaned_text = clean_text(
        raw_text
    )

    print(
        f"Normal extraction characters: "
        f"{len(cleaned_text)}"
    )

    # -----------------------------------------------------
    # Step 2: Determine whether OCR is required
    # -----------------------------------------------------

    if len(cleaned_text) >= 100:

        print(
            "Text-based PDF detected."
        )

        print(
            "Using extracted PDF text."
        )

        return cleaned_text

    # -----------------------------------------------------
    # Step 3: OCR fallback
    # -----------------------------------------------------

    print(
        "Very little text was extracted."
    )

    print(
        "Scanned/image-based PDF detected."
    )

    print(
        "Falling back to OCR..."
    )

    ocr_text = extract_text_with_ocr(
        file_path
    )

    cleaned_ocr_text = clean_text(
        ocr_text
    )

    print(
        f"OCR extracted characters: "
        f"{len(cleaned_ocr_text)}"
    )

    # -----------------------------------------------------
    # Step 4: Make sure OCR actually found something
    # -----------------------------------------------------

    if not cleaned_ocr_text:

        raise ValueError(
            "No text could be extracted from "
            "the document, even after OCR."
        )

    return cleaned_ocr_text


# ---------------------------------------------------------
# Text chunking
# ---------------------------------------------------------

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> list[str]:
    """
    Split text into overlapping chunks.

    Args:
        text:
            Clean document text.

        chunk_size:
            Maximum number of characters per chunk.

        overlap:
            Number of characters shared between
            consecutive chunks.

    Returns:
        List of text chunks.
    """

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size."
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks


# ---------------------------------------------------------
# Standalone test
# ---------------------------------------------------------

if __name__ == "__main__":

    PDF_PATH = "data/uploads/test.pdf"

    text = extract_text_from_pdf(
        PDF_PATH
    )

    chunks = chunk_text(
        text
    )

    print(
        f"\nTotal chunks: {len(chunks)}"
    )

    for index, chunk in enumerate(
        chunks[:3],
        start=1
    ):

        print(
            f"\n--- CHUNK {index} ---\n"
        )

        print(chunk)