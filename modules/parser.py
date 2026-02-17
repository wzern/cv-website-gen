import pdfplumber
from pathlib import Path

def extract_text_from_cv(cv_dir: str = "cv") -> dict[str, str]:
    """Extract text from all PDFs in the cv folder, returns dict of filename: text"""
    cv_path = Path(cv_dir)
    results = {}

    for pdf_file in cv_path.glob("*.pdf"):
        with pdfplumber.open(pdf_file) as pdf:
            text = "\n".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )
            results[pdf_file.name] = text

    return results